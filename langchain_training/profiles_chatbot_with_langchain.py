from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class ChatBot:
    def __init__(self, _api_key, model, max_history=6):
        self.api_key = _api_key
        self.model_name = model  # Store model name instead of client
        self.conversation_history = []
        self.max_history = max_history
        # Initialize LangChain Mistral model
        self.model = init_chat_model(
            model=model,
            model_provider="mistralai",
            api_key=self.api_key
        )
        self.db_client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
        self.initialize_context()

    def reset_history(self):
        self.conversation_history = []
        self.initialize_context()  # Reload profiles

    def initialize_context(self):
        try:
            db = self.db_client["app-dev"]  # Replace with your actual database name
            collection = db["profiles"]
            # Fetch all profiles but only specific fields
            projection = {
                "firstName": 1,
                "lastName": 1,
                "areaOfExpertise": 1,
                "currentLocation": 1,
                "_id": 0
            }
            profiles = list(collection.find({}, projection))
            if not profiles:
                profiles_context = "No profiles found in the database."
            else:
                profiles_context = "Here are the profiles in the database (limited to key fields):\n"
                for profile in profiles:
                    # Handle nested currentLocation field
                    location = profile.get("currentLocation", {})
                    location_str = f"{location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}, {location.get('country', 'Unknown')}"
                    profile_str = (
                        f"firstName: {profile.get('firstName', 'Unknown')}, "
                        f"lastName: {profile.get('lastName', 'Unknown')}, "
                        f"areaOfExpertise: {profile.get('areaOfExpertise', 'Unknown')}, "
                        f"currentLocation: {location_str}"
                    )
                    profiles_context += f"- {profile_str}\n"
                profiles_context += "\nNote: Only basic fields are included for each profile."
            system_message = SystemMessage(content=profiles_context)
            self.conversation_history.append(system_message)
            print(f"System message added with {len(profiles)} profiles")
        except Exception as e:
            print(f"Error fetching profiles from MongoDB: {e}")
            system_message = SystemMessage(content="Unable to load profiles due to a database error.")
            self.conversation_history.append(system_message)
        finally:
            self.db_client.close()

    def get_user_input(self):
        user_input = input("\nYou: ")
        user_message = HumanMessage(content=user_input)
        self.conversation_history.append(user_message)
        # Filter non-system messages for history trimming
        non_system_messages = [msg for msg in self.conversation_history if not isinstance(msg, SystemMessage)]
        if len(non_system_messages) > self.max_history:
            system_message = self.conversation_history[0] if isinstance(self.conversation_history[0], SystemMessage) else None
            trimmed_history = [msg for msg in self.conversation_history if not isinstance(msg, SystemMessage)][-self.max_history:]
            self.conversation_history = ([system_message] if system_message else []) + trimmed_history
        return user_message

    def send_request(self):
        # Use LangChain's streaming capability
        buffer = ""
        for chunk in self.model.stream(self.conversation_history):
            content = chunk.content
            print(content, end='')
            buffer += content

        if buffer.strip():
            assistant_message = AIMessage(content=buffer)
            self.conversation_history.append(assistant_message)

    def run(self):
        print("Chatbot started. Type 'exit' to quit.")
        while True:
            message = self.get_user_input()
            if message and message.content.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if message:  # Only send request if input was valid
                self.send_request()

if __name__ == "__main__":
    api_key = os.getenv('MISTRAL_API_KEY')
    mongo_uri = os.getenv("MONGO_CONNECTION_STRING")
    if api_key is None:
        print('Please set the environment variable Mistral api key')
        exit(1)
    if not mongo_uri:
        print("Please set the MONGO_CONNECTION_STRING environment variable.")
        exit(1)
    chat_bot = ChatBot(api_key, model='mistral-large-latest')
    chat_bot.run()






#### Under construction



# from langchain.chat_models import init_chat_model
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.memory import ConversationBufferWindowMemory
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.messages import HumanMessage
# import os
# from dotenv import load_dotenv
# from pymongo import MongoClient
#
# load_dotenv()
#
# class ChatBot:
#     def __init__(self, _api_key, model, max_history=6):
#         self.api_key = _api_key
#         self.model_name = model
#         self.max_history = max_history
#         # Initialize LangChain Mistral model
#         self.model = init_chat_model(
#             model=model,
#             model_provider="mistralai",
#             api_key=self.api_key
#         )
#         # Initialize memory to store conversation history
#         self.memory = ConversationBufferWindowMemory(
#             k=max_history,
#             return_messages=True,
#             memory_key="history"
#         )
#         # Initialize MongoDB client
#         self.db_client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
#         # Initialize system context from MongoDB
#         self.system_context = self._fetch_profiles()
#         # Create prompt template with system context embedded
#         self.prompt = self._create_prompt_template()
#         # Initialize runnable chain with history
#         self.chain = self._create_runnable_chain()
#
#     def _fetch_profiles(self):
#         """
#         Fetch profiles from MongoDB and return formatted context.
#         """
#         try:
#             db = self.db_client["app-dev"]
#             collection = db["profiles"]
#             projection = {
#                 "firstName": 1,
#                 "lastName": 1,
#                 "areaOfExpertise": 1,
#                 "currentLocation": 1,
#                 "_id": 0
#             }
#             profiles = list(collection.find({}, projection))
#             if not profiles:
#                 return "No profiles found in the database."
#             profiles_context = "Here are the profiles in the database (limited to key fields):\n"
#             for profile in profiles:
#                 location = profile.get("currentLocation", {})
#                 location_str = f"{location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}, {location.get('country', 'Unknown')}"
#                 profile_str = (
#                     f"firstName: {profile.get('firstName', 'Unknown')}, "
#                     f"lastName: {profile.get('lastName', 'Unknown')}, "
#                     f"areaOfExpertise: {profile.get('areaOfExpertise', 'Unknown')}, "
#                     f"currentLocation: {location_str}"
#                 )
#                 profiles_context += f"- {profile_str}\n"
#             profiles_context += "\nNote: Only basic fields are included for each profile."
#             print(f"System context initialized with {len(profiles)} profiles")
#             return profiles_context
#         except Exception as e:
#             print(f"Error fetching profiles from MongoDB: {e}")
#             return "Unable to load profiles due to a database error."
#         finally:
#             self.db_client.close()
#
#     def _create_prompt_template(self):
#         """
#         Create a ChatPromptTemplate with embedded system context.
#         """
#         system_prompt = self.system_context
#         return ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             MessagesPlaceholder(variable_name="history"),
#             ("human", "{input}")
#         ])
#
#     def _get_session_history(self, session_id: str):
#         """
#         Return the memory instance for the given session ID.
#         """
#         # For simplicity, use the same memory for the default session
#         return self.memory
#
#     def _create_runnable_chain(self):
#         """
#         Create a runnable chain with message history.
#         """
#         # Create the base chain (prompt + model)
#         chain = self.prompt | self.model
#         # Wrap with message history
#         return RunnableWithMessageHistory(
#             runnable=chain,
#             get_session_history=self._get_session_history,
#             input_messages_key="input",
#             history_messages_key="history"
#         )
#
#     def reset_history(self):
#         """
#         Clear conversation history and reload profile context.
#         """
#         self.memory.clear()
#         self.system_context = self._fetch_profiles()
#         self.prompt = self._create_prompt_template()
#         self.chain = self._create_runnable_chain()
#
#     def get_user_input(self):
#         """
#         Get user input and return as a HumanMessage.
#         """
#         user_input = input("\nYou: ")
#         return HumanMessage(content=user_input)
#
#     def send_request(self, user_message):
#         """
#         Send user input through the runnable chain and stream the response.
#         """
#         if not user_message.content.strip():
#             return
#         # Stream response using RunnableWithMessageHistory
#         for chunk in self.chain.stream(
#                 {"input": user_message.content},
#                 config={"configurable": {"session_id": "default"}}  # Required for memory
#         ):
#             content = getattr(chunk, 'content', chunk) if hasattr(chunk, 'content') else ''
#             if isinstance(content, str) and content.strip():
#                 print(content, end='')
#         print()  # Newline after streaming
#
#     def run(self):
#         """
#         Main loop to run the chatbot.
#         """
#         print("Chatbot started. Type 'exit' to quit.")
#         while True:
#             message = self.get_user_input()
#             if message.content.lower() in ["exit", "quit"]:
#                 print("Goodbye!")
#                 break
#             self.send_request(message)
#
# if __name__ == "__main__":
#     api_key = os.getenv('MISTRAL_API_KEY')
#     mongo_uri = os.getenv("MONGO_CONNECTION_STRING")
#     if api_key is None:
#         print('Please set the environment variable Mistral API key')
#         exit(1)
#     if not mongo_uri:
#         print("Please set the MONGO_CONNECTION_STRING environment variable.")
#         exit(1)
#     chat_bot = ChatBot(api_key, model='mistral-large-latest')
#     chat_bot.run()













# from langchain.chat_models import init_chat_model
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.memory import ConversationBufferWindowMemory
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# import os
# from dotenv import load_dotenv
# from pymongo import MongoClient
#
# load_dotenv()
#
# class ChatBot:
#     def __init__(self, _api_key, model, max_history=6):
#         self.api_key = _api_key
#         self.model_name = model
#         self.max_history = max_history
#         # Initialize LangChain Mistral model
#         self.model = init_chat_model(
#             model=model,
#             model_provider="mistralai",
#             api_key=self.api_key
#         )
#         # Initialize memory to store conversation history
#         self.memory = ConversationBufferWindowMemory(
#             k=max_history,
#             return_messages=True
#         )
#         # Initialize MongoDB client
#         self.db_client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
#         # Create prompt template
#         self.prompt = self._create_prompt_template()
#         # Initialize system context
#         self._initialize_context()
#
#     def _fetch_profiles(self):
#         """
#         Fetch profiles from MongoDB and return formatted context.
#         """
#         try:
#             db = self.db_client["app-dev"]
#             collection = db["profiles"]
#             projection = {
#                 "firstName": 1,
#                 "lastName": 1,
#                 "areaOfExpertise": 1,
#                 "currentLocation": 1,
#                 "_id": 0
#             }
#             profiles = list(collection.find({}, projection))
#             if not profiles:
#                 return "No profiles found in the database."
#             profiles_context = "Here are the profiles in the database (limited to key fields):\n"
#             for profile in profiles:
#                 location = profile.get("currentLocation", {})
#                 location_str = f"{location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}, {location.get('country', 'Unknown')}"
#                 profile_str = (
#                     f"firstName: {profile.get('firstName', 'Unknown')}, "
#                     f"lastName: {profile.get('lastName', 'Unknown')}, "
#                     f"areaOfExpertise: {profile.get('areaOfExpertise', 'Unknown')}, "
#                     f"currentLocation: {location_str}"
#                 )
#                 profiles_context += f"- {profile_str}\n"
#             profiles_context += "\nNote: Only basic fields are included for each profile."
#             print(f"System context initialized with {len(profiles)} profiles")
#             return profiles_context
#         except Exception as e:
#             print(f"Error fetching profiles from MongoDB: {e}")
#             return "Unable to load profiles due to a database error."
#         finally:
#             self.db_client.close()
#
#     def _create_prompt_template(self):
#         """
#         Create a ChatPromptTemplate for system and user messages.
#         """
#         return ChatPromptTemplate.from_messages([
#             ("system", "{system_context}"),
#             ("human", "{input}")
#         ])
#
#     def _initialize_context(self):
#         """
#         Initialize system context and store in memory.
#         """
#         system_context = self._fetch_profiles()
#         system_message = SystemMessage(content=system_context)
#         self.memory.save_context(
#             inputs={},
#             outputs={"output": system_message.content}
#         )
#
#     def reset_history(self):
#         """
#         Clear conversation history and reload profile context.
#         """
#         self.memory.clear()
#         self._initialize_context()
#
#     def get_user_input(self):
#         """
#         Get user input and store in memory.
#         """
#         user_input = input("\nYou: ")
#         user_message = HumanMessage(content=user_input)
#         self.memory.save_context(
#             inputs={"input": user_input},
#             outputs={}
#         )
#         return user_message
#
#     def send_request(self, user_message):
#         """
#         Send user input through the model and stream the response.
#         """
#         if not user_message.content.strip():
#             return
#         # Get current history from memory
#         history = self.memory.load_memory_variables({})["history"]
#         # Create prompt with system context and history
#         system_context = history[0].content if history and isinstance(history[0], SystemMessage) else "No context available."
#         prompt_messages = self.prompt.invoke({
#             "system_context": system_context,
#             "input": user_message.content
#         }).to_messages()
#         # Append history (excluding system message) to prompt
#         user_assistant_history = [msg for msg in history if not isinstance(msg, SystemMessage)]
#         prompt_messages = prompt_messages[:1] + user_assistant_history + prompt_messages[1:]
#         # Stream response
#         buffer = ""
#         for chunk in self.model.stream(prompt_messages):
#             content = chunk.content
#             print(content, end='')
#             buffer += content
#         print()  # Newline after streaming
#         # Save assistant response to memory
#         if buffer.strip():
#             self.memory.save_context(
#                 inputs={},
#                 outputs={"output": buffer}
#             )
#
#     def run(self):
#         """
#         Main loop to run the chatbot.
#         """
#         print("Chatbot started. Type 'exit' to quit.")
#         while True:
#             message = self.get_user_input()
#             if message.content.lower() in ["exit", "quit"]:
#                 print("Goodbye!")
#                 break
#             self.send_request(message)
#
# if __name__ == "__main__":
#     api_key = os.getenv('MISTRAL_API_KEY')
#     mongo_uri = os.getenv("MONGO_CONNECTION_STRING")
#     if api_key is None:
#         print('Please set the environment variable Mistral API key')
#         exit(1)
#     if not mongo_uri:
#         print("Please set the MONGO_CONNECTION_STRING environment variable.")
#         exit(1)
#     chat_bot = ChatBot(api_key, model='mistral-large-latest')
#     chat_bot.run()





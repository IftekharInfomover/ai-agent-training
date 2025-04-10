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
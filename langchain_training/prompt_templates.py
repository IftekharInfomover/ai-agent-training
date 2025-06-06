from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
import os
import getpass
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

    model = init_chat_model('mistral-large-latest', model_provider='mistralai')
    system_template = "Translate the following from English into {language}"

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )
    print(prompt_template)
    print(prompt_template.messages)

    prompt = prompt_template.invoke({"language": "Urdu", "text": "His name is Iqbal"})

    print(prompt)
    print(prompt.to_messages())
    response = model.invoke(prompt)
    print(response.content)

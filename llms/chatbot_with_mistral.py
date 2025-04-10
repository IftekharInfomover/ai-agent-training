import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    api_key = os.getenv('MISTRAL_API_KEY')

    if api_key is None:
        print('You need to set you api key')
        exit(1)

    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": "What is meaning of name Iftekhar?",
            },
        ]
    )
    print(chat_response.choices[0].message.content)




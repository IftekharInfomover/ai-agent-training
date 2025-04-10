import os
from google import genai
from dotenv import load_dotenv


load_dotenv()


if __name__ == '__main__':
    api_key = os.getenv('GEMINI_API_KEY')

    if api_key is None:
        print('You need to set you api key')
        exit(1)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Explain how AI works",
    )

    print(response.text)




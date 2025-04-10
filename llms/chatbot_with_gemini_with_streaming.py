# import os
# from google import genai
# from dotenv import load_dotenv
#
#
# load_dotenv()
#
#
# if __name__ == '__main__':
#     api_key = os.getenv('GEMINI_API_KEY')
#
#     if api_key is None:
#         print('You need to set you api key')
#         exit(1)
#
#     client = genai.Client(api_key=api_key)
#
#     response = client.models.generate_content_stream(
#         model="gemini-2.0-flash",
#         contents=["Explain Mughals were defeated"]
#     )
#     for chunk in response:
#         print(chunk.text, end="")





##### 2nd approach - Streaming text, Structured, Configurable, Modular and long response use case.
# import os
# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
#
#
# load_dotenv()
# def generate():
#     client = genai.Client(
#         api_key=os.environ.get("GEMINI_API_KEY"),
#     )
#
#     model = "gemini-2.0-flash"
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_text(text="""Who were Mughals?"""),
#             ],
#         ),
#     ]
#     generate_content_config = types.GenerateContentConfig(
#         response_mime_type="text/plain",
#     )
#
#     for chunk in client.models.generate_content_stream(
#             model=model,
#             contents=contents,
#             config=generate_content_config,
#     ):
#         print(chunk.text, end="")
#
# if __name__ == "__main__":
#     generate()
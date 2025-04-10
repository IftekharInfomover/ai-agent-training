
### Using nvidia/llama-3.1-nemotron-nano-8b-v1:free via openAI SDK
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
#
#
# load_dotenv()
#
# api_key=os.environ.get("OPENAI_API_KEY")
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=api_key,
# )
#
# completion = client.chat.completions.create(
#     extra_headers={
#         "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#         "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#     },
#     model="nvidia/llama-3.1-nemotron-nano-8b-v1:free",
#     messages=[
#         {
#             "role": "user",
#             "content": "What is the meaning of life?"
#         }
#     ]
# )
#
# print(completion.choices[0].message.content)





####Using nvidia/llama-3.3-nemotron-super-49b-v1:free via openAI SDK
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# api_key=os.environ.get("OPENAI_API_KEY")
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=api_key,
# )
#
# completion = client.chat.completions.create(
#     extra_headers={
#         "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#         "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#     },
#     model="nvidia/llama-3.3-nemotron-super-49b-v1:free",
#     messages=[
#         {
#             "role": "user",
#             "content": "What is fuel?"
#         }
#     ]
# )
#
# print(completion.choices[0].message.content)





####Using deepseek/deepseek-v3-base:free via openAI SDK
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# api_key=os.environ.get("OPENAI_API_KEY")
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=api_key,
# )
#
# completion = client.chat.completions.create(
#     extra_headers={
#         "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#         "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#     },
#     model="deepseek/deepseek-v3-base:free",
#     messages=[
#         {
#             "role": "user",
#             "content": "What is the capital of United States of America"
#         }
#     ]
# )
#
# print(completion.choices[0].message.content)
#



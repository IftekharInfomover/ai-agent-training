import os
from typing import Optional, List
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.utils.function_calling import tool_example_to_messages
from dotenv import  load_dotenv


load_dotenv()


class Person(BaseModel):
    """Information about a person."""
    name: Optional[str] = Field(default=None, description="The name of the person")
    hair_color: Optional[str] = Field(
        default=None, description="The color of the person's hair if known"
    )
    height_in_meters: Optional[str] = Field(
        default=None, description="Height measured in meters"
    )

class Data(BaseModel):
    """Extracted data about people."""
    # Creates a model so that we can extract multiple entities.
    people: List[Person]


class Extraction:

    def __init__(self, _api_key, ):
        self.api_key = _api_key
        self.llm = init_chat_model("mistral-large-latest", model_provider="mistralai")
        self.prompt_template = self.prompt_template()


    @staticmethod
    def prompt_template():
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm. "
                    "Only extract relevant information from the text. "
                    "If you do not know the value of an attribute asked to extract, "
                    "return null for the attribute's value.",
                ),
                # Please see the how-to about improving performance with
                # reference examples.
                # MessagesPlaceholder('examples'),
                ("human", "{text}"),
            ]
        )
        return prompt_template


    def structured_output_person(self):
        structured_llm = self.llm.with_structured_output(schema=Person)
        text = "Alan Smith is 6 feet tall and has blond hair."
        prompt = self.prompt_template.invoke({"text": text})
        response = structured_llm.invoke(prompt)
        print(response)

    def structured_output_with_multiple_entities(self):
        structured_llm = self.llm.with_structured_output(schema=Data)
        text = "My name is Jeff, my hair is black and i am 6 feet tall. Anna has the same color hair as me."
        prompt = self.prompt_template.invoke({"text": text})
        response = structured_llm.invoke(prompt)
        return response


    def tool_call(self):
        examples = [
            (
                "The ocean is vast and blue. It's more than 20,000 feet deep.",
                Data(people=[]),
            ),
            (
                "Fiona traveled far from France to Spain.",
                Data(people=[Person(name="Fiona", height_in_meters=None, hair_color=None)]),
            ),
        ]


        messages = []

        for txt, tool_call in examples:
            if tool_call.people:
            # This final message is optional for some providers
                ai_response = "Detected people."
            else:
                ai_response = "Detected no people."
            messages.extend(tool_example_to_messages(txt, [tool_call], ai_response=ai_response))

        for message in messages:
            message.pretty_print()


if __name__ == "__main__":
    api_key = os.getenv('MISTRAL_API_KEY')
    if api_key is None:
        print('Please set the environment variable Mistral API key')
        exit(1)
    extract = Extraction(api_key)










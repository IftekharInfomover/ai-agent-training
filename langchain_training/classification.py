import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()




class TextClassifier:

    def __init__(self, _api_key, ):
        self.api_key = _api_key
        self.llm = init_chat_model("mistral-large-latest", model_provider="mistralai")
        self.tagging_prompt = self.tagging_prompt()

    @staticmethod
    def tagging_prompt():
        tagging_prompt = ChatPromptTemplate.from_template(
            """
        Extract the desired information from the following passage.
        
        Only extract the properties mentioned in the 'Classification' function.
        
        Passage:
        {input}
        """
        )
        return tagging_prompt


    class Classification(BaseModel):
        sentiment: str = Field(description="The sentiment of the text")
        aggressiveness: int = Field(
            description="How aggressive the text is on a scale from 1 to 10"
        )
        language: str = Field(description="The language the text is written in")

        # model = self.llm.with_structured_output()


    def classifier(self):
        model = self.llm.with_structured_output(self.Classification)
        inp = "I am incredibly happy to have met you! I think we will be very good friends!"
        prompt = self.tagging_prompt.invoke({"input": inp})
        response = model.invoke(prompt)
        return response.model_dump()


    class SchemedClassification(BaseModel):
        sentiment: str = Field(..., enum=["happy", "neutral", "sad"])
        aggressiveness: int = Field(
            ...,
            description="describes how aggressive the statement is, the higher the number the more aggressive",
            enum=[1, 2, 3, 4, 5],
        )
        language: str = Field(
            ..., enum=["urdu", "english", "hindi", "german", "italian"]
        )

    def schemed_classifier(self):
        model = self.llm.with_structured_output(self.SchemedClassification)
        inp = "I am incredibly happy to have met you! I think we will be very good friends!"
        prompt = self.tagging_prompt.invoke({"input": inp})
        response = model.invoke(prompt)
        return response.model_dump()


if __name__ == "__main__":
    api_key = os.getenv('MISTRAL_API_KEY')
    if api_key is None:
        print('Please set the environment variable Mistral API key')
        exit(1)
    classify = TextClassifier(api_key)
    print(classify.classifier())
    print(classify.schemed_classifier())







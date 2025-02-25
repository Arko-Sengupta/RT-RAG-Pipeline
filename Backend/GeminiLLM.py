import os
import logging
from google import genai
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv(".env")

class GeminiLLM:

    def __init__(self) -> None:
        """
        Initializes the GeminiLLM class by setting up the client and model.
        """
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = os.getenv("GEMINI_MODEL")

    def GeminiFlash(self, text: str, query: str) -> str:
        """
        Sends input text and a query to the Gemini model and retrieves the response.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model, contents=[text, query]
            )
            
            return response.text
        except Exception as e:
            logging.error("An Error Occurred: ", exc_info=e)
            raise e

    def run(self, text: str, query: str) -> str:
        """
        A wrapper function that calls the GeminiFlash method.
        """
        try:
            return self.GeminiFlash(text=text, query=query)
        except Exception as e:
            logging.error("An Error Occurred: ", exc_info=e)
            raise e
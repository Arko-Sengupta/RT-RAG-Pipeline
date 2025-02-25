import os
import logging
import requests
import streamlit as st
from dotenv import load_dotenv

# Configure Logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

# Load Environment Variables
load_dotenv(".env")

class RealTimeSearch_UI:

    def __init__(self) -> None:
        """
        Initializes the RealTimeSearch_UI class by loading environment variables.
        """
        self.title = os.getenv("TITLE", "Real Time Search")
        self.real_time_search_api = os.getenv("REALTIMESEARCH_API")

    def App_Interface(self) -> None:
        """
        Renders the Streamlit-based user interface for the real-time search application.
        """
        try:
            st.header(self.title)

            url = st.text_input("Enter URL:", "https://www.example.com")
            query = st.text_input("Enter Search Query:")

            if st.button("Search"):
               with st.spinner("Searching..."):
                   if url and query:
                       try:
                           response = requests.post(self.real_time_search_api, json={'data': {"URL": url, "Query": query}})
                           response_json = response.json()

                           result = response_json["response"]

                           if result:
                               st.text(result)
                           else:
                               st.write("No Results Found.")
                       except requests.exceptions.RequestException as e:
                           st.error(f"Error fetching data: {e}")
                   else:
                       st.warning("Please provide both URL and Query.")
        except Exception as e:
            logging.error("An Error Occurred: ", exc_info=e)
            raise e

    def run(self) -> None:
        """
        Executes the application by running the App_Interface method.
        """
        try:
            self.App_Interface()
        except Exception:
            logging.error('An Error Occurred during Application Execution', exc_info=True)
            st.error("An Error Occurred!")

if __name__ == '__main__':

    App = RealTimeSearch_UI()
    App.run()
import logging
from flask import Blueprint, Flask, jsonify, request
from Backend.Scraper import Scraper
from Backend.GeminiLLM import GeminiLLM

# Configure Logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

class RealTimeSearch:
    
    def __init__(self, URL: str) -> None:
        self.scraper = Scraper(URL=URL)
        self.geminiLLM = GeminiLLM()
        
    def GenerateResponse(self, Query: str) -> str:
        """
        Generates a response based on the scraped data and the user's query.
        """
        try:
            text = self.scraper.run()
            response = self.geminiLLM.run(text=text, query=Query)
            
            return response
        except Exception as e:
            logging.error("An Error Occured: ", exc_info=e)
            raise e
        
class RealTimeSearch_API:
    
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.real_time_search_blueprint = Blueprint('real_time_search', __name__)
        self.real_time_search_blueprint.add_url_rule('/search', 'real_time_search', self.real_time_search, methods=['POST'])

    def real_time_search(self) -> tuple:
        """
        Handles the /search endpoint and processes the user's request.
        """
        try:
            data = request.get_json()
            URL, Query = data["data"]["URL"], data["data"]["Query"]
            
            self.real_time_search_ = RealTimeSearch(URL=URL)
            response = self.real_time_search_.GenerateResponse(Query=Query)
            
            return jsonify({'response': response}), 200
        except Exception as e:
            logging.error('An error occurred: ', exc_info=e)
            return jsonify({'Error': str(e)}), 400

    def run(self) -> None:
        """
        Starts the Flask application and registers the real-time search blueprint.
        """
        try:
            self.app.register_blueprint(self.real_time_search_blueprint)
            self.app.run(debug=True)
        except Exception as e:
            logging.error('An error occurred: ', exc_info=e)
            raise e
        

server = RealTimeSearch_API()
if __name__ == '__main__':

    server.run()
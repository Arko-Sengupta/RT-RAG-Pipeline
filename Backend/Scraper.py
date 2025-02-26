import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configure Logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.WARNING)

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in Headless Mode (Optional)
options.set_capability('timeouts', {'implicit': 10})

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.set_page_load_timeout(30)
driver.set_script_timeout(30)

class Scraper:
    """
    A web scraper class that extracts and processes textual content from a given URL.
    """

    def __init__(self, URL: str) -> None:
        """
        Initializes the Scraper with a URL and a list of HTML tags to extract text from.
        """
        self.URL = URL
        self.Tags = ["h1", "h2", "h3", "h4", "h5", "h6",
                     "p", "span", "strong", "em", "b", "i",
                     "u", "small", "mark", "del", "ins", "sup",
                     "sub", "abbr", "cite", "code", "pre", "blockquote",
                     "q", "li", "dt", "dd", "a", "button",
                     "label", "th", "td", "caption", "figcaption", "legend"]

    def OptimizedString(self, text: str) -> str:
        """
        Cleans and optimizes a given string by removing special characters and whitespace.
        """
        try:
            text = re.sub(r'[\n\r\t\f\v]', '', text)
            text = re.sub(r'[^A-Za-z0-9\s]', '', text)
            return text
        except Exception as e:
            logging.error("An Error Occurred: ", exc_info=e)
            raise e

    def TagText(self, driver: webdriver.Chrome) -> str:
        """
        Extracts and optimizes text content from the web page based on specified HTML tags.
        """
        try:
            Text = []
            for ele in self.Tags:
                Text.extend(driver.find_elements(By.TAG_NAME, ele))

            Text = [self.OptimizedString(t.text.strip()) for t in Text]
            Text = ''.join(Text)
            return Text
        except Exception as e:
            logging.error("An Error Occurred: ", exc_info=e)
            raise e

    def run(self) -> str:
        """
        Initiates the scraping process, navigates to the URL, and extracts text content.
        """
        try:
            driver.get(self.URL)
            time.sleep(10)

            text_array = self.TagText(driver)
            return text_array
        except Exception as e:
            logging.error("An Error Occurred: ", exc_info=e)
            raise e
        finally:
            driver.quit()
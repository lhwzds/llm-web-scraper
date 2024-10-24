from seleniumwire import webdriver 
# from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # 导入 Options 类
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  # 自动管理 ChromeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
from pydantic import BaseModel
from urllib.parse import urljoin
from rich.console import Console
from rich import print

class AnswerDetail(BaseModel):
    subAnswer: str

class QuestionResponse(BaseModel):
    title: str
    answerList: list[AnswerDetail]

class CompleteResponse(BaseModel):
    response: list[QuestionResponse]
    
class RufusClient:
    def __init__(self, api_key, verbose=False):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.verbose = verbose 
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # headless mode
        chrome_options.add_argument('--disable-gpu') # disable gpu
        chrome_options.add_argument('--no-sandbox')  
        chrome_options.add_argument('--disable-dev-shm-usage')  

        # Disable images css 
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.javascript": 1  # 如需禁用JS，将值设为2
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Initialize WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
    def scrape(self, url):
        self.driver.get(url)
        
        # Give time for the page to load completely
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Get status_code from request
        status_code = None
        for request in self.driver.requests:
            if request.response and request.url == url:
                status_code = request.response.status_code
                break
            
        if status_code == 200:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            texts = soup.get_text()
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            
            full_link_lst = set()
            for link in links:
                full_link = urljoin(url, link)
                full_link_lst.add(full_link)
            full_link_lst=list(full_link_lst)
        
            return texts, full_link_lst
        else:
            if self.verbose:
                print(f"[red]No accessScraping main URL... to website, Error code: {status_code}[/red]")
            return None

    def analyze(self, instruction, documents):
        # analyse using chatgpt api
        try:
            MAX_DOCUMENT_LENGTH = 3000  # Adjust this value based on token estimation
            # If the document exceeds the limit, truncate it
            if len(documents) > MAX_DOCUMENT_LENGTH:
                documents = documents[:MAX_DOCUMENT_LENGTH] + "...(truncated)" 
                
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a helpful web scraper."},
                    {"role": "system", "content": "You need to output everything in json format."},
                    {"role": "user", "content": f"Finish Task : {instruction}\n in Document : \n{documents}"}
                ],
                response_format=CompleteResponse,
                max_tokens=5000
            )
            
            final_response = completion.choices[0].message
            
            if final_response.parsed:
                return completion.choices[0].message
            elif final_response.refusal:
                if self.verbose:
                    print(f"[red]Analysis refused: {final_response.refusal}[/red]")
                pass
                
        
        except Exception as e:
            
            if self.verbose:
                if isinstance(e, openai.LengthFinishReasonError):
                    print(f"[red]Too many tokens: {e}[/red]")
                    pass
                else:
                    print(f"[red]Error occurred during analysis: {e}[/red]")
                    pass
            
            
        

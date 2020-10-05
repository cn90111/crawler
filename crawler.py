import requests
from bs4 import BeautifulSoup

class Crawler():    
    def __init__(self, url):
        self.url = url

    def set_url(self, url):
        self.url = url

    def get_url(self, url):
        return self.url

    def get_response(self):
        return requests.get(self.url)

    def get_select_element(self, select_tag, full_text=None):
        if not full_text:
            full_text = self.get_full_text()        
        soup = BeautifulSoup(full_text, "html.parser")
        element = soup.select(select_tag)
        return element

    def get_next_element(self, element, neighbor_tag):
        return element.find_next(neighbor_tag)

    def need_login(self, select_tag, full_text=None):
        login_button = self.get_select_element(select_tag, full_text=full_text)
        if login_button:
            return True
        return False
    
    def login(self, login_url, login_parameter):
        requests.post(login_url, login_parameter)
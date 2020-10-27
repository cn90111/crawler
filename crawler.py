import requests
from bs4 import BeautifulSoup

class Crawler():    
    def __init__(self, url, headers=None, proxies=None):
        self.url = url
        
        self.headers = headers
        self.proxies = proxies

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def get_response(self):
        return requests.get(self.url, proxies=self.proxies, headers=self.headers)

    def get_select_element_list(self, select_tag, full_text=None):
        if not full_text:
            full_text = self.get_response().text
        soup = BeautifulSoup(full_text, "html.parser")
        element_list = soup.select(select_tag)
        return element_list

    def get_next_element(self, element, neighbor_tag):
        return element.find_next(neighbor_tag)

    def need_login(self, select_tag, full_text=None):
        if not full_text:
            full_text = self.get_response().text
        login_button = self.get_select_element(select_tag, full_text=full_text)
        if login_button:
            return True
        return False
    
    def login(self, login_url, login_parameter):
        response = requests.post(login_url, login_parameter, proxies=self.proxies, headers=self.headers)
        
    def remove_html(self, select_tag, full_text=None):
        if not full_text:
            full_text = self.get_response().text
        soup = BeautifulSoup(full_text, "html.parser")
        delete_elements = soup.select(select_tag)
        for element in delete_elements:
            element.decompose()
        return soup
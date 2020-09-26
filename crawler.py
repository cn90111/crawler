'''
Bird, Steven, Edward Loper and Ewan Klein (2009).
Natural Language Processing with Python.  O'Reilly Media Inc.
'''

import requests
from bs4 import BeautifulSoup

class Crawler():
    def __init__(self, url):
        self.url = url

    def get_full_text(self):
        response = requests.get(self.url)
        return response.text
        
    def get_select_text(self, select_tag, full_text=None):
        if not full_text:
            full_text = self.get_full_text()        
        soup = BeautifulSoup(full_text, "html.parser")
        element = soup.select(select_tag)
        return element
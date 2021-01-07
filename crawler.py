import requests
from bs4 import BeautifulSoup
from splinter import Browser

class Crawler():
    def __init__(self, url, headers=None, proxies=None):
        self.url = url
        self.headers = headers
        self.proxies = proxies
        
        self.browser = None
        self.BROWSER_LIST = ['firefox', 'chrome']
        self.FIND_MODE = ['css', 'xpath', 'tag', 'name', 'text', 'id', 'value']

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url
        
    def set_headers(self, headers):
        self.headers = headers
        
    def get_headers(self):
        return self.headers
        
    def set_proxies(self, proxies):
        self.proxies = proxies
        
    def get_proxies(self):
        return self.proxies
        
    def get_response(self, url=None):
        if url:
            return requests.get(url, proxies=self.proxies, headers=self.headers)
        return requests.get(self.url, proxies=self.proxies, headers=self.headers)

    def get_select_element_list(self, select_tag, full_text=None):
        if not full_text:
            full_text = self.get_response().text
        soup = BeautifulSoup(full_text, "html.parser")
        element_list = soup.select(select_tag)
        return element_list
    
    def get_parent(self, element):
        return element.find_parent()

    def get_previous_element(self, element):
        return element.previous_element
        
    def get_previous_sibling(self, element):
        return element.previous_sibling
        
    def get_next_element(self, element, neighbor_tag=None):
        if neighbor_tag:
            return element.find_next(neighbor_tag)
        return element.next_element

    def need_login(self, select_tag, full_text=None):
        if not full_text:
            full_text = self.get_response().text
        login_button = self.get_select_element_list(select_tag, full_text=full_text)
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
        
    def open_browser(self, browser_name=None):
        if browser_name:
            if browser_name in self.BROWSER_LIST:
                self.browser = Browser(browser_name)
            else:
                raise AttributeError('browser unsupport, support list: '+str(self.BROWSER_LIST))
        else:
            self.browser = Browser()
        self.browser.visit(self.url)
        
    def close_browser(self):
        if not self.browser:
            raise Exception('Please call open_browser() first')
        self.browser.quit()
        self.browser = None
        
    def go_to_url(self, url=None):
        if not self.browser:
            raise Exception('Please call open_browser() first')
        if url:
            self.browser.visit(url)
        else:
            self.browser.visit(self.url)
    
    def find_element_list(self, mode, select_tag):
        element_list = None
        if not self.browser:
            raise Exception('Please call open_browser() first')
        if mode not in self.FIND_MODE:
            raise AttributeError('mode unsupport, mode list: '+str(self.FIND_MODE))
        if mode == 'css':
            element_list = self.browser.find_by_css(select_tag)
        elif mode == 'xpath':
            element_list = self.browser.find_by_xpath(select_tag)
        elif mode == 'tag':
            element_list = self.browser.find_by_tag(select_tag)
        elif mode == 'name':
            element_list = self.browser.find_by_name(select_tag)
        elif mode == 'text':
            element_list = self.browser.find_by_text(select_tag)
        elif mode == 'id':
            element_list = self.browser.find_by_id(select_tag)
        elif mode == 'value':
            element_list = self.browser.find_by_value(select_tag)
        else:
            raise Exception('find_element_list exception: ' + mode)
        return element_list
        
    def get_browser_html(self):
        if not self.browser:
            raise Exception('Please call open_browser() first')
        return self.browser.html
        
    def get_browser_url(self):
        if not self.browser:
            raise Exception('Please call open_browser() first')
        return self.browser.url
    
    def fix_vaild_file_name(self, file_name):
        invalid_char_list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|'] # for windows invalid file name
        for invalid_char in invalid_char_list:
            file_name = file_name.replace(invalid_char, '')
        return file_name
                    
    def download_image(self, download_url, image_name=None):
        if not image_name:
            image_name = download_url.split('/')[-1]
        image_name = self.fix_vaild_file_name(image_name)
        response = requests.get(download_url, proxies=self.proxies, headers=self.headers)
        with open(image_name, 'wb') as file:
            file.write(response.content)
            
    def get_cookie(self):
        if not self.browser:
            raise Exception('Please call open_browser() first')
        return self.browser.cookies.all()
        
    def get_alert(self):
        if not self.browser:
            raise Exception('Please call open_browser() first')
        return self.browser.get_alert()
        
    def get_html_tag(self, element):
        string = str(element)
        first_index = string.find('<') + 1
        last_index = string.find('>')
        if last_index > string.find(' '):
            last_index = string.find(' ')
        tag = string[first_index : last_index]
        return tag
    
    def get_all_feature(self, element):
        feature_dict = {}
        keys = element.attrs.keys()
        for key in keys:
            feature_dict[key] = element.get(key)
        return feature_dict
        
    def get_element_feature(self, element):
        id = element.get('id')
        if id:
            return 'id', id

        tag = self.get_html_tag(element)
        feature_dict = self.get_all_feature(element)
        xpath = '/' + tag + '['
        for feature, value in feature_dict.items():
            xpath = xpath + '@' + feature + '=\'' + value + '\''
            xpath = xpath + ' and '
        xpath = xpath[:-5] # delete ' and '
        xpath = xpath + ']'
        
        while tag != 'div' and tag != 'tbody':
            element = self.get_parent(element)
            tag = self.get_html_tag(element)
            if tag:
                xpath = '//' + tag + xpath
        if feature:
            return 'xpath', xpath
            
        raise Exception('no match feature')
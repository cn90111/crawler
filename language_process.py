'''
Bird, Steven, Edward Loper and Ewan Klein (2009).
Natural Language Processing with Python.  O'Reilly Media Inc.
'''
import nltk
import jieba
import re
from translate import Translator

class LanguageProcess():
    def __init__(self, mode='english'):
        self.MODE = ['traditional_chinese', 'english', 'simplified_chinese']
        if mode:
            if mode not in self.MODE:
                raise AttributeError('mode unsupport, mode list: '+str(self.MODE))
            elif mode == 'traditional_chinese':
                jieba.set_dictionary('dict.txt.big')
        self.mode = mode
        
    def get_sentence(self, text):
        sentence_list = None
        if self.mode == 'english':
            sentence_list = nltk.sent_tokenize(text)
        elif self.mode == 'traditional_chinese' or self.mode == 'simplified_chinese':
            raise AttributeError('chinese unsupport')
        return sentence_list
        
    def get_word(self, text):
        word_list = None
        if self.mode == 'english':
            word_list = nltk.word_tokenize(text)
        elif self.mode == 'traditional_chinese' or self.mode == 'simplified_chinese':
            word_list = jieba.cut(text, cut_all=False)
        return word_list
        
    # need network
    def translate(self, word, from_lang, to_lang='english'):
        translator= Translator(from_lang=from_lang,to_lang=to_lang)
        return translator.translate(word)
        
    def is_english(self, word):
        english_check = r'[a-zA-Z]+'
        return re.fullmatch(english_check, word)
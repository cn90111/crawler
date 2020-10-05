'''
Bird, Steven, Edward Loper and Ewan Klein (2009).
Natural Language Processing with Python.  O'Reilly Media Inc.
'''
import nltk

class LanguageProcess():
    def get_sentence(self, text):
        return nltk.sent_tokenize(text)
        
    def get_word(self, text):
        return nltk.word_tokenize(text)
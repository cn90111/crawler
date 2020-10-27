#https://www.itread01.com/content/1549674027.html

from gensim.models.keyedvectors import KeyedVectors

class KeyWord():
    def __init__(self, loading_model=True):
        self.model = None
        if loading_model:
            print('loading model')
            self.model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
            print('loading finish')
        
    def get_similarity(self, key_word, check_word):
        if self.model:
            return self.model.similarity(key_word, check_word)
        raise Exception('not load word2vec model')
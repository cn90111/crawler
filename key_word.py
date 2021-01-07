#https://www.itread01.com/content/1549674027.html

from gensim.models.keyedvectors import KeyedVectors
from gensim.models import word2vec

class KeyWord():
    def __init__(self, mode='english', loading_model=True):
        self.model = None
        self.MODEL_LIST = ['english', 'traditional_chinese']
        
        if loading_model:
            print('loading model')
            if mode == 'english':
                self.model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
            elif mode == 'traditional_chinese':
                self.model = word2vec.Word2Vec.load("20180309wiki_model.bin")
            else:
                raise AttributeError('mode unsupport, support list: '+str(self.MODEL_LIST))
            print('loading finish')
        
    def get_similarity(self, key_word, check_word):
        if self.model:
            return self.model.similarity(key_word, check_word)
        raise Exception('not load word2vec model')
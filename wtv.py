from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import pandas as pd

data_pre = pd.read_csv('C:/Users/User/et_pre.csv')
data_pre_2 = data_pre.dropna()

word = []
for i in data_pre_2['text']:
    word.append(i.split())

embedding_model = Word2Vec(word, window=2, min_count=10, epochs=1000, workers=-1, sg=1)
embedding_model.wv.save_word2vec_format('everytime_wtv')
import gensim
from gensim.models import Word2Vec
from allennlp.modules.elmo import Elmo, batch_to_ids
from bert_serving.client import BertClient
import numpy as np
from elmoformanylangs import Embedder
import pickle
from pywordseg import *



test_word = "數位語音處理概論"

def trans_w2v(text):
	model = Word2Vec.load("pretrained/zh.bin")
	vector = model.wv[text]
	print(vector)

def trans_bert(dic):
	#bert-serving-start -model_dir chinese_L-12_H-768_A-12/
	sents = []
	for key in dic:
		sents.append(dic[key])
	bc = BertClient()
	vector = bc.encode(sents)
	print(vector.shape)
	i = 0
	for key in dic:
		dic[key] = vector[i]
		i += 1
	return dic

def trans_elmo(dic):
	e = Embedder('pretrained/')
	sents = []
	seg = Wordseg(batch_size=8, device="cuda:0", embedding='elmo', elmo_use_cuda=False, mode="TW")
	for key in dic:
		sents.append(dic[key])
	sents = seg.cut(sents)
	vector = e.sents2elmo(sents, -1)
	print(len(vector))
	i = 0
	for key in dic:
		dic[key] = vector[i][0]
		i += 1
	return dic

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
	course_dict = load_obj('course')
	course_dict = trans_bert(course_dict)
	save_obj(course_dict, 'embedding/embedding_bert')
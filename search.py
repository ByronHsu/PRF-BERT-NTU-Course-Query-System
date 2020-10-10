import pickle
from bert_serving.client import BertClient
import numpy as np

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def topK(vector, rank_list, K):
	dot = np.dot(rank_list, vector.transpose())
	norma = np.linalg.norm(vector)
	normb = np.linalg.norm(rank_list, axis = 1)
	cos_sim = dot.flatten() / (norma * normb)
	cos_sim_rank = np.flip(np.argsort(cos_sim))

	top_k_index = cos_sim_rank[:K]
	bottom_k_index = cos_sim_rank[-K:]
	return top_k_index, bottom_k_index

def topK_result(top_k_index, bottom_k_index, K):
	original_dict = load_obj('course')
	top_result = [0] * K
	bottom_result = [0] * K
	for i, (k, v) in enumerate(original_dict.items()):
		if i in top_k_index:
			top_result[np.where(top_k_index == i)[0][0]] = v
		elif i in bottom_k_index:
			bottom_result[np.where(bottom_k_index == i)[0][0]] = v
	return top_result, bottom_result

def PRF(query, rank_list, top_k_index, bottom_k_index, K):
	alpha = 1
	beta = 0.75
	gamma = 0.15
	rel = np.sum(rank_list[top_k_index], axis = 0) / K
	irrel = np.sum(rank_list[bottom_k_index], axis = 0) / K
	query = (alpha * query + beta * rel - gamma * irrel) / (alpha + beta - gamma)
	return query




if __name__ == '__main__':
	#bert-serving-start -model_dir chinese_L-12_H-768_A-12/
	embedding_dict = load_obj('embedding/embedding_bert')
	K = 10
	prf_iteration = 10

	query = input()
	bc = BertClient()
	vector = bc.encode([query])

	rank_list = []
	for key in embedding_dict:
		rank_list.append([embedding_dict[key]])
	rank_list = np.array(rank_list).squeeze()

	top_k_index, bottom_k_index = topK(vector, rank_list, K)

	top_result, bottom_result = topK_result(top_k_index, bottom_k_index, K)

	for i in range(prf_iteration):
		vector = PRF(vector, rank_list, top_k_index, bottom_k_index, K)

		top_k_index, bottom_k_index = topK(vector, rank_list, K)

		top_result, bottom_result = topK_result(top_k_index, bottom_k_index, K)
	
	for i in range(K):
		print("TOP %d, RANK: %d, RESULT: %s" % (K, i, top_result[i]))
	for i in range(K):
		print("BOTTOM %d, RANK: %d, RESULT: %s" % (K, rank_list.shape[0] - K + i + 1, bottom_result[i]))
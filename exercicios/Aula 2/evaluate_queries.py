import pickle
import random
import numpy as np

PATH = 'd:/desv/projetos/IA368dd/exercicios/Aula 2/data/'
K = 10

def calculate_dcg(ratings, K):
    return sum((2 ** ratings - 1) / np.log2(np.array(range(2, K+2))))

ratings = {}

print('Loading the queries ratings and calculating iDCG...')
for line in open(PATH + '2020qrels-pass.txt'):
    qid, q0, docid, rating = [int(field) for field in line.rstrip().split()]
    assert q0 == 0
    if qid not in ratings:
        ratings[qid] = {}
    ratings[qid][docid] = rating

iDCG = {}
for qid, docs_ratings in ratings.items():
    best_ratings = np.array(sorted(docs_ratings.values(), reverse=True)[:K])
    iDCG[qid] = calculate_dcg(best_ratings, K)
    #print(qid, best_ratings, iDCG[qid])

print('Loading the results from boolean search and calculating nDCG...')
with open(PATH + 'retrieved_boolean.pickle', 'rb') as f:
    results_boolean = pickle.load(f)

nDCG_boolean = {}
#print('qid #result selected_10')
for qid, docs in results_boolean.items():
    selected_docs = [int(doc_id) for doc_id in random.sample(docs, K)]
    ratings_docs = np.array([ratings[qid].get(doc_id, 0) for doc_id in selected_docs])
    nDCG_boolean[qid] = calculate_dcg(ratings_docs, K) / iDCG[qid]
    #print(qid, ratings_docs, nDCG_boolean[qid])


print(f'\tnDCG@{K} = {(sum(nDCG_boolean.values()) / len(nDCG_boolean)):.4f} (averaged among all queries)')

#bDCG = {}
#for qid, docs in results_boolean.items():
#    best_docs = np.array(sorted([ratings[qid].get(doc_id, 0) for doc_id in docs], reverse=True)[:K])
#    bDCG[qid] = calculate_dcg(best_docs, K) / iDCG[qid]
#print(f'\t\twith best possible ordering: {(sum(bDCG.values()) / len(nDCG)):.4f}', )


print('Loading the results from tf-idf  search and calculating nDCG...')
with open(PATH + 'retrieved_tf_idf.pickle', 'rb') as f:
    results_tf_idf = pickle.load(f)

nDCG_tfidf = {}
for qid, results in results_tf_idf.items():
    ratings_docs = np.array([ratings[qid].get(doc_id, 0) for _, doc_id in results][:K])
    nDCG_tfidf[qid] = calculate_dcg(ratings_docs, K) / iDCG[qid]
    #print(qid, ratings_docs, nDCG_tfidf[qid])

print(f'\tnDCG@{K} = {(sum(nDCG_tfidf.values()) / len(nDCG_tfidf)):.4f} (averaged among all queries)')

results = '''
Loading the queries ratings and calculating iDCG...
Loading the results from boolean search and calculating nDCG...
        nDCG@10 = 0.0049 (averaged among all queries)
Loading the results from tf-idf  search and calculating nDCG...
        nDCG@10 = 0.1462 (averaged among all queries)
'''

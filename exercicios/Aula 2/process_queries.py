# pre-requisito: 
# - pip install nltk
# - cd data

import pickle
import nltk
import datetime

from math import log
from nltk.corpus import stopwords
from string import punctuation

PATH = 'd:/desv/projetos/IA368dd/exercicios/Aula 2/data/'

# Preparation - preprocessing function and inverted index

nltk.download('stopwords')
nltk.download('punkt')
stopwords_list = set(stopwords.words('english'))

def preprocess(text):
    # Convert the text to lowercase
    text = text.lower()
    # Tokenize the text into individual words
    tokens = nltk.word_tokenize(text)
    # Remove punctuation
    tokens = [token for token in tokens if token not in punctuation]
    # Remove stopwords from the text
    tokens = [token for token in tokens if token not in stopwords_list]
    ### Return the preprocessed text as a list of tokens
    return tokens

def now():
    return datetime.datetime.now().strftime("%H:%M:%S")

# Load the inverted index
print(f'Loading the inverted index... {now()}')
with open(PATH + 'inverted_index.pickle', 'rb') as f:
    inverted_index = pickle.load(f)

# TF-IDF Search - Load the term frequences

print(f'Loading the term frequences... {now()}')
with open(PATH + 'term_frequencies.pickle', 'rb') as f:
    term_frequencies = pickle.load(f)

# TF-IDF Search - Load the doc lengths

print(f'Loading the doc lengths... {now()}')
with open(PATH + 'doc_lengths.pickle', 'rb') as f:
    doc_lengths = pickle.load(f)

# Download the ratings from TREC 2020 DL Passages

print(f'Loading the queries and rating... {now()}')
ratings = {}

for line in open(PATH + '2020qrels-pass.txt'):
    qid, q0, docid, rating = [int(field) for field in line.rstrip().split()]
    assert q0 == 0
    if qid not in ratings:
        ratings[qid] = {}
    ratings[qid][docid] = rating

queries = {}

for line in open(PATH + 'msmarco-test2020-queries.tsv'):
    qid, query = line.rstrip().split('\t')
    qid = int(qid)
    if qid in ratings:
        queries[qid] = query

print('\t', len(queries), 'queries loaded.')


# Query processing - Boolean Search

print(f'Processing queries (boolean search)... {now()}')
def process_boolean(query):
    #print('Query:', query)
    tokens = preprocess(query)
    #print('Preprocessed:', tokens)
    return {token: inverted_index.get(token, {}) for token in tokens}
    
def process_consolidated_boolean(query):
    result = process_boolean(query)
    consolidated = set()
    for docs in result.values():
        consolidated = consolidated.union(docs)
    return sorted([int(doc) for doc in consolidated])

print(f'Saving results... {now()}')
results = {qid: process_consolidated_boolean(query) for qid, query in queries.items()}
with open(PATH + 'retrieved_boolean.pickle', 'wb') as f:
    pickle.dump(results, f)

#relevants = sorted([docid for docid in ratings[qid].keys() if ratings[qid][docid] > 0])
#scores = [ratings[qid].get(docid, 0) for docid in result]


# Query processing - TF-IDF Search

print(f'Processing queries (TF-IDF search)... {now()}')
    
def process_tfidf(query):
    rank = {}
    N = len(doc_lengths)
    result = process_boolean(query)
    for term, docs in result.items():
        idf = log(N / len(docs))
        for doc_id in docs:
            tf = term_frequencies[doc_id].get(term, 0) / doc_lengths[doc_id]
            rank[doc_id] = rank.get(doc_id, 0) + tf * idf
    return rank

def process_tfidf_top_k(query, k):
    assert k > 0
    rank = process_tfidf(query)
    base = [(score, int(doc_id)) for doc_id, score in rank.items()]
    return sorted(base)[::-1][:k]

results = {qid: process_tfidf_top_k(query, 10) for qid, query in queries.items()}

print(f'Saving results... {now()}')
with open(PATH + 'retrieved_tf_idf.pickle', 'wb') as f:
    pickle.dump(results, f)

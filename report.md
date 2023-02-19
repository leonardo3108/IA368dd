# Building a Simple Information Retrieval System using BM25 and evaluated in the CISI collection.

## Introduction

The notebook demonstrates how to use the BM25 algorithm for information retrieval on the Glasgow CISI dataset. 

BM25 is a ranking function that is commonly used in search engines and information retrieval systems. 

The Glasgow CISI dataset is a standard test collection for evaluating information retrieval systems. 
It consists of a set of documents and queries, along with relevance judgments that can be used to evaluate the performance of retrieval systems.

## Methodology

The notebook first installs the required packages, including nltk and rank-bm25. 
It then defines a function to preprocess the documents and queries by converting the text to lowercase, removing non-alphanumeric characters, tokenizing the text, removing stopwords, and stemming the tokens. 
The nltk package is used for tokenization, stopwords removal, and stemming.

Next, the notebook loads the documents from the CISI.ALL file and preprocesses them using the function defined earlier. 
The preprocessed documents are stored in a list. The BM25 index is then built using the BM25Okapi class from the rank-bm25 package.

The notebook then loads the queries from the CISI.QRY file and preprocesses them using the same function. 
The preprocessed queries are stored in a list. The queries are then performed using the BM25 index, and the top 10 documents for each query are retrieved (K=10).

The results of the queries are stored in a dictionary, where the keys are the query IDs and the values are lists of document IDs. 
The notebook prints the top 10 results for each query.

Finally, the evaluation is made from the relation of relevant documents for each query from CISI.REL file. 
Comparing the list of retrieved documens with relevant documents for each query, we obtain the number of true positives, false positives and false negatives, so we calculate the precision@10, recal@10 and F1@10 metrics.

## Results

The notebook successfully performs information retrieval on the Glasgow CISI dataset using the BM25 algorithm. 
The results was evaluated, and we obtained:
*  Precision (@10 documents): 4,3%
*  Recall (@10 documents): 1,5%
*  F1 (@10 documents): 2,3%
The notebook also prints the top 10 results for each query.

## Conclusion

In conclusion, the notebook provides a useful example of how to use the BM25 algorithm for information retrieval on a standard test collection such as the Glasgow CISI dataset. 
The notebook demonstrates how to preprocess the documents and queries using the nltk package and how to build a BM25 index using the rank-bm25 package. 
The notebook also shows how to perform queries and retrieve the top documents for each query. 
The notebook also evaluates the results obtained, with metrics precision, recall and F1 at 10 documents.
Overall, the notebook provides a good starting point for anyone interested in using the BM25 algorithm for information retrieval.

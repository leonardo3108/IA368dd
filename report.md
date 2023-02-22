# Building a Simple Information Retrieval System using BM25 and GPT-3 and evaluated in the CISI collection

## Introduction

The notebook demonstrates how to use the BM25 algorithm for information retrieval on the Glasgow CISI dataset. 

### BM25

BM25 (Best Matching 25) is a ranking algorithm used in information retrieval (IR) to evaluate the relevance of documents to a user's query. It is one of the most widely used ranking algorithms in modern search engines and has proven to be effective in a variety of settings.

It is an improvement over the popular TF-IDF (Term Frequency-Inverse Document Frequency) method, which assigns weights to terms in a document based on their frequency and rarity across a corpus of documents.

The BM25 formula is as follows:

$$
BM25(q, D) = \sum_ {q_i}\left\lbrack{(k + 1) * f(q_i, D) \over f(q_i, D) + k * (1 - b + b * {|D| \over avgdl}) } * log{N - n(q_i) + 0.5 \over n(q_i) + 0.5}\right\rbrack
$$

where:
- $q$: a query containing one or more terms
- $D$: a document in the corpus
- $q_i$: a term in the query
- $f(q_i, D)$: the frequency of term $q_i$ in document $D$
- $N$: the total number of documents in the corpus
- $n(q_i)$: the number of documents in the corpus containing term $q_i$
- $avgdl$: the average length of documents in the corpus
- $k$ and $b$: free parameters used to control the impact of term frequency and document length on the relevance score. Typically, $k = 1.2$ and $b = 0.75$ are used as default values.

The formula calculates a score for each document based on the term frequencies in the document and the query, as well as some characteristics of the corpus. The score represents the relevance of the document to the query, with higher scores indicating greater relevance.

In general, BM25 is a more complex ranking function than TF-IDF, but it has been shown to perform better in many information retrieval tasks, especially those involving longer queries and larger document collections.

The BM25 algorithm is important for information retrieval because it provides a way to rank documents based on their relevance to a user's query, which is crucial for any search engine. By ranking the documents, the search engine can present the most relevant results to the user, which can improve the user's search experience and increase the likelihood that they will find what they are looking for.

### Glasgow CISI dataset

The Glasgow CISI dataset is a benchmark dataset used for evaluating information retrieval (IR) systems. It was developed by the University of Glasgow's Department of Computing Science in collaboration with the Chemical Abstracts Service and is a standard test collection for evaluating IR models.

The Glasgow CISI dataset consists of a corpus of 1460 documents, covering the fields of chemistry, physics, and electronics. It also includes a set of 112 queries, each with a corresponding set of relevant documents, which were assessed by human judges. The relevance judgments are binary, indicating whether a document is relevant or not for a given query.

The CISI dataset has been used in a number of research studies to evaluate the effectiveness of various IR models, including vector space models, probabilistic models, and language models. It has also been used to evaluate the effectiveness of different indexing methods, query expansion techniques, and relevance feedback mechanisms.

The Glasgow CISI dataset has been widely used as a standard benchmark for evaluating the performance of IR systems, and it continues to be used as a reference dataset for developing and evaluating new IR models and techniques. The dataset is freely available for academic research purposes.

### GPT-3

GPT-3 (Generative Pre-trained Transformer 3) is a state-of-the-art natural language processing model developed by OpenAI. It is one of the most advanced language models available and has been trained on a massive amount of text data to generate high-quality text output.

It is based on a deep learning architecture called a transformer network. The transformer network was first introduced in a 2017 research paper by Vaswani et al. called "Attention Is All You Need". The transformer network is a type of neural network that uses attention mechanisms to process input sequences and generate output sequences.

In GPT-3, the transformer network has been further optimized and trained on a massive amount of text data, allowing it to generate high-quality text output in a wide range of contexts. It is also able to perform a range of natural language processing tasks, such as language translation, summarization, and question answering, as well as generate text that mimics human writing style and tone.

We've had made a small [test of using GPT3 online via API](GPT3_Test.ipynb).

### ChatGPT

ChatGPT is a specific instance of GPT-3 that has been fine-tuned on conversational data, allowing it to carry out human-like conversations with users on a wide range of topics.

It's worth noting that while GPT-3 and ChatGPT are incredibly powerful tools, they are not perfect and may occasionally generate inaccurate or irrelevant information. It's important to carefully review any output they produce and verify that it meets your needs before using it in a real-world application.

While ChatGPT are not designed specifically for writing code, they can still be used to generate code snippets or to assist with writing code-related text. For example, you could provide a description of what you want your code to accomplish, and ChatGPT may be able to provide suggestions for specific functions or code snippets that could help you achieve your goals.

Alternatively, if you provide ChatGPT with a detailed report template and some data or analysis results, it could generate a report for you by filling in the appropriate sections based on the information provided.


## Methodology

The [notebook](Baseline_BM25.ipynb) first installs the required packages, including nltk and rank-bm25. 
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

### Use of ChatGTP in code and report

Most of this report was automatically generated from [ChatGPT](chats/Saved_Chat_GPT_1.md#generate-a-report-about-this), and then adjusted to include the evaluation, more [BM25 explanation](chats/Saved_Chat_GPT_1.md#please-explain-me-about-the-bm25-and-its-importance-for-information-retrieval) and [formula](chats/Saved_Chat_GPT_2.md#please-explain-me-the-bm25-formula), [dataset description](chats/Saved_Chat_GPT_5.md#can-you-describe-me-the-glasgow-cisi-dataset-for-information-retrieval) and even a [self description](chats/Saved_Chat_GPT_6.md).

Even the [code](Baseline_BM25.ipynb) was mostly generated from ChatGPT, then the code was revised, tested and adjusted to perform well the desired tasks.
Details of the use and adjusts and commented along the [code](Baseline_BM25.ipynb).

## Results

The notebook successfully performs information retrieval on the Glasgow CISI dataset using the BM25 algorithm. 
The results was evaluated, and we obtained:
*  **Precision (@10 documents): 24.7%**
*  **Recall (@10 documents): 8.9%**
*  **F1 (@10 documents): 13.1%**
The notebook also prints the top 10 results for each query.

It's important to note that the CISI dataset lacks of relevant documents for many queries. Because of that, precision@10 could not be better than [64.5%](Precision_problems_with_CISI_dataset.ipynb).

## Conclusion

In conclusion, the notebook provides a useful example of how to use the BM25 algorithm for information retrieval on a standard test collection such as the Glasgow CISI dataset. 

It demonstrates how to preprocess the documents and queries using the nltk package and how to build a BM25 index using the rank-bm25 package, and how to perform queries and retrieve the top documents for each query. It also evaluates the results obtained, with metrics precision, recall and F1 at 10 documents.

Finally, this works demonstrate the power of using GPT-3 for producing code, reporting and sharing knowledge.
Overall, the notebook provides a good starting point for anyone interested in information retrieval and use of GPT-3 and ChatGPT.

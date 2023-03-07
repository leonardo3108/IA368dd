# pre-requisito: 
# - pip install nltk
# - cd data

import nltk
import pickle

from nltk.corpus import stopwords
from string import punctuation
from collections import Counter

# Download the stopwords and punctuation lists from NLTK
nltk.download('stopwords')
nltk.download('punkt')

stopwords_list = set(stopwords.words('english'))

# Define a function to preprocess a text string
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

print()
query = 'The Manhattan Project and its atomic bomb helped bring an end to World War II. Its legacy of peaceful uses of atomic energy continues to have an impact on history and science.'
print('Test of preprocessing:')
print(f'Query: {query}')
print(preprocess(query))
print()

# Define a dictionary to store the inverted index
inverted_index = {}

### Define a dictionary to store the document lengths
doc_lengths = {}

### Define a dictionary to store the term frequencies
term_frequencies = {}

# Open the MSMARCO collection file for reading
print('Processing documents:')
with open('collection.tsv', 'r', encoding='utf-8') as collection_file:
    # Loop over each line in the file
    for line_nr, line in enumerate(collection_file):
        # Split the line into document ID and text
        doc_id, text = line.strip().split('\t')
        # Preprocess the text
        tokens = preprocess(text)
        # Create a bag-of-words for the preprocessed text
        word_counts = Counter(tokens)
        # Add the document length to the dictionary
        doc_lengths[doc_id] = sum(word_counts.values())        
        # Loop over each word in the bag-of-words
        for word, count in word_counts.items():
            # Add the document ID to the inverted index for this word
            if word not in inverted_index:
                inverted_index[word] = set()
            inverted_index[word].add(doc_id)
            # Add the term frequency to the dictionary
            if doc_id not in term_frequencies:
                term_frequencies[doc_id] = {}
            term_frequencies[doc_id][word] = count
        if line_nr % 10000 == 0 and line_nr > 0:
            print(f'\tprocessing doc_id {doc_id}')
            #if line_nr >= 1000: break

# Print the inverted index size
print()
print('Results: inverted index', len(inverted_index.keys()), '- doc lengths', len(doc_lengths.keys()), '- term frequencies', len(term_frequencies.keys()))
print()

def save_dict_to_file(my_dict, filename):
    '''
    Save a dictionary to a file using pickle.

    Args:
        my_dict (dict): The dictionary to be saved.
        filename (str): The name of the file to which the dictionary should be saved.

    Returns:
        None
    '''
    # Open the file for writing
    with open(filename, 'wb') as f:
        # Use the pickle.dump method to save the dictionary to the file
        pickle.dump(my_dict, f)
        print(f'Saved file {filename}.')
		
save_dict_to_file(inverted_index, 'inverted_index.pickle')
save_dict_to_file(doc_lengths, 'doc_lengths.pickle')
save_dict_to_file(term_frequencies, 'term_frequencies.pickle')
			

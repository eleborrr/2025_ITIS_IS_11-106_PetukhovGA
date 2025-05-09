import os
import math
from collections import defaultdict
import csv

def load_documents(directory):
    documents = {}
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            doc_id = int(filename.replace(".txt", "").split('_')[2])
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                words = file.read().split()
                documents[doc_id] = words
    return documents

def calculate_tf(documents):
    tf = defaultdict(dict)
    for doc_id, words in documents.items():
        total_words = len(words)
        word_counts = defaultdict(int)
        for word in words:
            word_counts[word] += 1
        for word, count in word_counts.items():
            tf[word][doc_id] = round(count / total_words, 6)
    return tf

def calculate_idf(documents):
    idf = {}
    total_docs = len(documents)
    doc_freq = defaultdict(int)
    
    for doc_id, words in documents.items():
        unique_words = set(words)
        for word in unique_words:
            doc_freq[word] += 1
    
    for word, freq in doc_freq.items():
        idf[word] = round(math.log(total_docs / freq), 6)
    
    return idf

def calculate_tfidf(tf, idf):
    tfidf = defaultdict(dict)
    for word, doc_tf in tf.items():
        for doc_id, tf_value in doc_tf.items():
            tfidf[word][doc_id] = round(tf_value * idf[word], 6)
    return tfidf

def save_to_csv(data, filename, header):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for key, values in data.items():
            for subkey, value in values.items():
                writer.writerow([key, subkey, value])

directory = '..\\Task2\\processed_documents'
documents = load_documents(directory)

tf = calculate_tf(documents)
save_to_csv(tf, 'tf.csv', ['Term', 'Document', 'TF'])

idf = calculate_idf(documents)
with open('idf.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Term', 'IDF'])
    for term, value in idf.items():
        writer.writerow([term, value])

tfidf = calculate_tfidf(tf, idf)
save_to_csv(tfidf, 'tfidf.csv', ['Term', 'Document', 'TF-IDF'])

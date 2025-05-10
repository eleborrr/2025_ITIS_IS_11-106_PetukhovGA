import csv
import math
from collections import defaultdict

def load_csv_to_dict(filename):
    data = defaultdict(dict)
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            term, doc_id, value = row
            data[term][int(doc_id)] = float(value)
    return data

def load_idf(filename):
    idf = {}
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            term, value = row
            idf[term] = float(value)
    return idf

def vectorize_query(query, idf):
    query_terms = query.split()
    query_vector = {}
    for term in query_terms:
        if term in idf:
            tf = query_terms.count(term) / len(query_terms)
            print(idf[term])
            query_vector[term] = idf[term] * tf
    return query_vector

def cosine_similarity(query_vector, full_doc_vector):
    dot_product = sum(
        q_weight * full_doc_vector[term]
        for term, q_weight in query_vector.items()
        if term in full_doc_vector
    )
    
    query_norm = math.sqrt(sum(q**2 for q in query_vector.values()))
    doc_norm = math.sqrt(sum(d**2 for d in full_doc_vector.values()))
    
    return dot_product / (query_norm * doc_norm) if (query_norm * doc_norm) != 0 else 0

def vector_search(query, tfidf, idf, top_n=10):
    query_vector = vectorize_query(query, idf)
    scores = {}
    
    relevant_docs = set()
    for term in query_vector:
        relevant_docs.update(tfidf.get(term, {}).keys())
    
    for doc_id in relevant_docs:
        full_doc_vector = {}
        for term in tfidf:
            if doc_id in tfidf[term]:
                full_doc_vector[term] = tfidf[term][doc_id]
        
        similarity = cosine_similarity(query_vector, full_doc_vector)
        scores[doc_id] = similarity
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

tfidf = load_csv_to_dict('..\Task4\\tfidf.csv')
idf = load_idf('..\Task4\\idf.csv')

queries = [
    "вк",
    "статистика",
    "россия",
    "вк статистика",
    "вк статистика россия"
]

for query in queries:
    results = vector_search(query, tfidf, idf, 100)
    print(f"Результаты для запроса '{query}':")
    for doc_id, score in results:
        print(f"Документ {doc_id}: вес = {score:.6f}")
    print()

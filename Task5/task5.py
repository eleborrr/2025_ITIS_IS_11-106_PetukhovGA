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
            query_vector[term] = idf[term]
    return query_vector

def cosine_similarity(query_vector, doc_vector):
    dot_product = 0
    query_norm = 0
    doc_norm = 0
    
    for term, q_weight in query_vector.items():
        if term in doc_vector:
            dot_product += q_weight * doc_vector[term]
        query_norm += q_weight ** 2
    
    for weight in doc_vector.values():
        doc_norm += weight ** 2
    
    if query_norm == 0 or doc_norm == 0:
        return 0
    
    return dot_product / (math.sqrt(query_norm) * math.sqrt(doc_norm))

def vector_search(query, tfidf, idf, top_n=10):
    query_vector = vectorize_query(query, idf)
    scores = defaultdict(float)
    
    relevant_docs = set()
    for term in query_vector:
        if term in tfidf:
            relevant_docs.update(tfidf[term].keys())
    
    for doc_id in relevant_docs:
        doc_vector = {}
        for term in query_vector:
            if term in tfidf and doc_id in tfidf[term]:
                doc_vector[term] = tfidf[term][doc_id]
        similarity = cosine_similarity(query_vector, doc_vector)
        scores[doc_id] = similarity
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:top_n]

tfidf = load_csv_to_dict('..\Task4\\tfidf.csv')
idf = load_idf('..\Task4\\idf.csv')

queries = [
    "быстрая сортировка алгоритм",
    "искусственный интеллект",
    "когда дуров основал вконтакте"
]

for query in queries:
    results = vector_search(query, tfidf, idf)
    print(f"Результаты для запроса '{query}':")
    for doc_id, score in results:
        print(f"Документ {doc_id}: вес = {score:.6f}")
    print()


# Результаты для запроса 'быстрая сортировка алгоритм':
# Документ 45: вес = 0.870932
# Документ 7: вес = 0.870932
# Документ 14: вес = 0.491404
# Документ 55: вес = 0.491404
# Документ 23: вес = 0.491404
# Документ 91: вес = 0.491404
# Документ 1: вес = 0.491404
# Документ 65: вес = 0.491404
# Документ 46: вес = 0.491404
# Документ 77: вес = 0.491404

# Результаты для запроса 'искусственный интеллект':
# Документ 1: вес = 1.000000
# Документ 23: вес = 1.000000
# Документ 28: вес = 1.000000
# Документ 36: вес = 1.000000
# Документ 50: вес = 1.000000
# Документ 35: вес = 0.999999
# Документ 77: вес = 0.999999
# Документ 49: вес = 0.999999
# Документ 44: вес = 0.998808
# Документ 2: вес = 0.997478

# Результаты для запроса 'когда дуров основал вконтакте':
# Документ 35: вес = 1.000000
# Документ 36: вес = 0.999999
# Документ 22: вес = 0.997024
# Документ 25: вес = 0.962825
# Документ 9: вес = 0.953900
# Документ 10: вес = 0.952423
# Документ 73: вес = 0.926151
# Документ 13: вес = 0.872656
# Документ 24: вес = 0.864068
# Документ 2: вес = 0.711068
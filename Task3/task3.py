import os
from collections import defaultdict

def build_inverted_index(directory):
    inverted_index = defaultdict(list)
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            doc_id = int(filename.replace(".txt", "").split('_')[2])
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                words = file.read().split()
                for word in set(words):
                    inverted_index[word].append(doc_id)
    return inverted_index

def save_inverted_index(inverted_index, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for word in sorted(inverted_index.keys()):
            docs = ','.join(map(str, sorted(inverted_index[word])))
            file.write(f"{word}:{docs}\n")

def load_inverted_index(index_file):
    inverted_index = {}
    with open(index_file, 'r', encoding='utf-8') as file:
        for line in file:
            word, docs = line.strip().split(':')
            inverted_index[word] = set(map(int, docs.split(',')))
    return inverted_index

def boolean_search(query, inverted_index):
    all_docs = set()
    for docs in inverted_index.values():
        all_docs.update(docs)

    tokens = query.split()

    stack = []  
    ops = []    

    precedence = {'&': 2, '|': 1}

    for token in tokens:
        if token in ('&', '|'):
            while (ops and ops[-1] != '(' and
                   precedence.get(ops[-1], 0) >= precedence.get(token, 0)):
                apply_operator(stack, ops.pop(), all_docs)
            ops.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops[-1] != '(':
                apply_operator(stack, ops.pop(), all_docs)
            ops.pop()
        else: 
            word = token.lstrip('!')
            negated = token.startswith('!')

            docs = inverted_index.get(word, set())
            if negated:
                docs = all_docs - docs

            stack.append(docs)

    while ops:
        apply_operator(stack, ops.pop(), all_docs)

    return sorted(stack[-1]) if stack else []


def apply_operator(stack, op, all_docs):
    if op == '!':
        a = stack.pop()
        stack.append(all_docs - a)
    else:
        b = stack.pop()
        a = stack.pop()
        if op == '&':
            stack.append(a & b)
        elif op == '|':
            stack.append(a | b)

inverted_index = load_inverted_index('inverted_index.txt')

queries = [
    "вконтакте & павел дуров | груша",
    "облепиха & мёд | каравай",
    "интернет | муха | виталий",
    "компания | !бизнес | !деньги",
    "онлайн & пользователь & сайт"
]

for query in queries:
    try:
        result = boolean_search(query, inverted_index)
        print(f"Результат запроса '{query}': {result}")
    except ValueError as e:
        print(f"Ошибка в запросе '{query}': {e}")


# directory = '..\Task2\processed_documents'
# inverted_index = build_inverted_index(directory)

# save_inverted_index(inverted_index, 'inverted_index.txt')

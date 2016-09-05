import stemmer

inverted_index = {}

def and_comp(set1, set2):
    #print '\t', set1, '^', set2
    return set1.intersection(set2)

def or_comp(set1, set2):
    #print '\t', set1, 'U', set2
    return set1.union(set2)

def and_not_comp(set1, set2):
    #print '\t', set1, '-', set2
    return set2.difference(set1)

def clean(str):
    str = str.replace(',', '').replace('(', '').replace(')', '').replace('\'', '').replace('"', '').replace(';', '').replace('.', '')
    return str

operators = {'&&': and_comp, '||': or_comp, '&^': and_not_comp}

stemmer = stemmer.PorterStemmer()

def index(id, doc):
    terms = doc.split()

    for term in terms:
        term = term.lower()
        term = clean(term)

        doc_ids = inverted_index.get(term)
        if doc_ids:
            doc_ids.add(id)
        else:
            inverted_index[term] = set()
            inverted_index[term].add(id)

def index_stem(id, doc):
    terms = doc.split()

    for term in terms:
        term = term.lower()
        term = clean(term)
        term = stemmer.stem(term, 0, len(term)-1)

        doc_ids = inverted_index.get(term)
        if doc_ids:
            doc_ids.add(id)
        else:
            inverted_index[term] = set()
            inverted_index[term].add(id)

def search(tokens):
    prev_doc_ids = set()
    accumulate = or_comp

    for token in tokens:
        token = token.lower()

        if operators.get(token[0:2]):
            accumulate = operators[token[0:2]]
            #print 'operators', accumulate
            token = token[2:]

        doc_ids = inverted_index.get(token)
        #print token, '=', doc_ids
        if doc_ids:
            doc_ids = accumulate(doc_ids, prev_doc_ids)
            #print accumulate, '=', doc_ids
            prev_doc_ids = set(doc_ids)

    l = list(doc_ids)
    l.sort()
    print '\t', tokens, '-->', l

def search_stem(tokens):
    prev_doc_ids = set()
    accumulate = or_comp

    for token in tokens:
        token = token.lower()
        token = stemmer.stem(token, 0, len(token)-1)

        if operators.get(token[0:2]):
            accumulate = operators[token[0:2]]
            #print 'operators', accumulate
            token = token[2:]

        doc_ids = inverted_index.get(token)
        #print token, '=', doc_ids
        if doc_ids:
            doc_ids = accumulate(doc_ids, prev_doc_ids)
            #print accumulate, '=', doc_ids
            prev_doc_ids = set(doc_ids)

    l = list(doc_ids)
    l.sort()
    print '\t', tokens, '-->', l

docs = {
    1:'Love will tear us apart',
    2:'All you need is love',
    3:'Run the world (Girls)',
    4:'Love makes the world go round',
    5:'Back in black',
    6:'Lovely Rita',
    7:'The man who sold the world',
    8:'The most beautiful girl in the world',
    9:'Lovin\' you',
    10:'Crazy in love'
}

queries = ['World', 'Love', 'World &&Girl', 'Love ||World', 'Love &^World']

def create_index():
    for k,v in docs.items():
        index(k, v)

def create_index_stem():
    for k,v in docs.items():
        index_stem(k, v)
    print inverted_index

def normal_search():
    create_index()

    for query in queries:
        query = query.lower()
        tokens = query.split()

        search(tokens)

def stem_search():
    create_index_stem()

    for query in queries:
        query = query.lower()
        tokens = query.split()

        search_stem(tokens)

#stem_search()
normal_search()

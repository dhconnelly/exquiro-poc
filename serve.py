import json
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import torch
from flask import Flask, request
import sys

corpus_path = sys.argv[1]
embeddings_path = sys.argv[2]

device = torch.device('mps')

print('loading corpus...')
with open(corpus_path) as f:
    corpus = json.load(f)

print('loading embeddings...')
with open(embeddings_path) as f:
    corpus_embeddings = torch.load(embeddings_path)
texts = [(chapter, work, book)
         for work in corpus
         for book in work['books']
         for chapter in book['chapters']]

print('loading static site...')
with open('index.html') as f:
    index = f.read()

top_k = 30
bi_encoder = SentenceTransformer('msmarco-distilbert-base-tas-b', device=device)
bi_encoder.max_seq_length = 512
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2', device=device)

def search(query):
    # retrieval
    query_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    query_embedding = query_embedding.to(device)
    query_embedding = torch.nn.functional.normalize(query_embedding, dim=-1)
    hits = util.semantic_search(
            query_embedding, corpus_embeddings,
            top_k=top_k, score_function=util.dot_score)
    hits = hits[0]

    # ranking
    # https://www.sbert.net/examples/applications/retrieve_rerank/README.html
    ranking_inputs = [(query, texts[hit['corpus_id']][0]) for hit in hits]
    scores = cross_encoder.predict(ranking_inputs)
    for idx, score in enumerate(scores):
        hits[idx]['cross_score'] = score
    rank_by = 'cross_score'
    ranked = sorted(hits, key=lambda hit: hit[rank_by], reverse=True)

    return ranked[:5]

app = Flask(__name__)

def render(result):
    chapter, work, book = result
    title = f'<td>{work["title"]}</td>'
    author = f'<td>{work["author"]}</td>'
    book = f'<td>{book["name"]}</td>'
    text = f'<td>{chapter}</td>'
    return f'<tr>{author} {title} {book} {text}</tr>'

@app.route('/search', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return index
    else:
        query = request.form.get('search', None)
        if not query:
            return ''
        nn_results = search(query)
        results = [texts[result['corpus_id']] for result in nn_results]
        rendered_results = ''.join([render(result) for result in results])
        return rendered_results

if __name__ == '__main__':
    print('starting search service at http://127.0.0.1:8080/search')
    app.run(debug=True, port=8080)

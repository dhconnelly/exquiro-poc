import json
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import torch

def main(args):
    # Retrieve and re-rank method:
    # https://www.sbert.net/examples/applications/retrieve_rerank/README.html

    query = args[0]
    corpus_path = args[1]
    embeddings_path = args[2]
    print(f"searching in {corpus_path} via {embeddings_path} for {query}")
    with open(corpus_path) as f:
        corpus = json.load(f)
    with open(embeddings_path) as f:
        corpus_embeddings = torch.load(embeddings_path)
    texts = [chapter
             for work in corpus
             for book in work['books']
             for chapter in book['chapters']]

    # retrieval
    top_k = 30
    bi_encoder = SentenceTransformer('sentence-transformers/msmarco-distilbert-cos-v5')
    query_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)
    hits = hits[0]

    # ranking
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    ranking_inputs = [(query, texts[hit['corpus_id']]) for hit in hits]
    scores = cross_encoder.predict(ranking_inputs)
    for idx, score in enumerate(scores):
        hits[idx]['cross_score'] = score
    ranked = sorted(hits, key=lambda hit: hit['cross_score'], reverse=True)

    print('-' * 80)
    for hit in ranked[:3]:
        idx = hit['corpus_id']
        print(idx, "(Score: {:.4f})".format(hit['cross_score']))
        print(texts[idx])


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

import json
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import torch

device = torch.device('mps')

def main(args):
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
    top_k = 100
    bi_encoder = SentenceTransformer('msmarco-distilbert-base-v4', device=device)
    bi_encoder.max_seq_length = 512
    query_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)
    hits = hits[0]

    # ranking
    # https://www.sbert.net/examples/applications/retrieve_rerank/README.html
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2', device=device)
    ranking_inputs = [(query, texts[hit['corpus_id']]) for hit in hits]
    scores = cross_encoder.predict(ranking_inputs)
    for idx, score in enumerate(scores):
        hits[idx]['cross_score'] = score
    rank_by = 'cross_score'
    ranked = sorted(hits, key=lambda hit: hit[rank_by], reverse=True)

    print('-' * 80)
    for hit in ranked[:3]:
        idx = hit['corpus_id']
        print(idx, "(Score: {:.4f})".format(hit[rank_by]))
        print(texts[idx])


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

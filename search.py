import json
from sentence_transformers import SentenceTransformer, util
import torch

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

    model = SentenceTransformer('sentence-transformers/msmarco-distilbert-cos-v5')
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]
    for hit in hits:
        idx = hit['corpus_id']
        print(idx, "(Score: {:.4f})".format(hit['score']))
        print(texts[idx])

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

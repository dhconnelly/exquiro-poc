import json
from sentence_transformers import SentenceTransformer, util
import torch

def main(args):
    input_path = args[0]
    output_path = args[1]
    print(f'embedding from {input_path} to {output_path}')
    with open(input_path) as f:
        corpus = json.load(f)
    texts = [chapter
             for work in corpus
             for book in work['books']
             for chapter in book['chapters']]

    model = SentenceTransformer('sentence-transformers/msmarco-distilbert-cos-v5')
    corpus_embeddings = model.encode(texts, convert_to_tensor=True)
    torch.save(corpus_embeddings, output_path)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])


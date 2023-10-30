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

    model = SentenceTransformer('msmarco-distilbert-base-v4')
    model.max_seq_length = 512
    print('max sequence length:', model.max_seq_length)
    too_long = len([text for text in texts if len(text) > model.max_seq_length])
    if too_long > 0:
        print(f'WARNING: {too_long} (of {len(texts)}) texts are longer than max sequence length')
    corpus_embeddings = model.encode(texts, convert_to_tensor=True)
    torch.save(corpus_embeddings, output_path)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])


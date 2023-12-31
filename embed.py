import json
from sentence_transformers import SentenceTransformer, util
import torch

device = torch.device('mps')

def main(args):
    output_path = args[0]
    input_path = args[1]
    print(f'embedding from {input_path} to {output_path}')
    with open(input_path) as f:
        corpus = json.load(f)
    texts = [chapter
             for work in corpus
             for book in work['books']
             for chapter in book['chapters']]

    model = SentenceTransformer('msmarco-distilbert-base-tas-b', device=device)
    model.max_seq_length = 512
    too_long = len([text for text in texts if len(text) > model.max_seq_length])
    if too_long > 0:
        print(f'WARNING: {too_long} (of {len(texts)}) texts are longer than max sequence length ({model.max_seq_length})')
    corpus_embeddings = model.encode(texts, convert_to_tensor=True)
    corpus_embeddings.to(device)
    corpus_embeddings = util.normalize_embeddings(corpus_embeddings)
    torch.save(corpus_embeddings, output_path)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])


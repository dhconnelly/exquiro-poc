# exquiro: proof of concept

## getting started

    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## usage

    # preprocess corpus
    python preprocess.py corpus.json corpus/*

    # generate embeddings
    python embed.py corpus.json corpus.embed

    # start the search server
    python search.py corpus.json corpus.embed

    # now open http://127.0.0.1:5000 and make some queries :)

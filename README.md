# exquiro: proof of concept

## getting started

    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## usage

    # extract data from corpus/* and serialize to corpus.json
    python preprocess.py corpus.json corpus/*

    # generate embeddings from corpus.json into corpus.embed
    python embed.py corpus.embed corpus.json

    # start the search server, using corpus.json corpus.embed
    python search.py corpus.json corpus.embed

    # now open http://127.0.0.1:5000 and make some queries :)

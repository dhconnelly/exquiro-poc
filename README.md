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

    # issue a query
    python search.py "should i engage in politics" corpus.json corpus.embed

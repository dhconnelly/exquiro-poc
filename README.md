# exquiro: proof of concept

## getting started

    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## usage

    # preprocess corpus
    python preprocess.py corpus/cicero.xml cicero.json

    # generate embeddings
    python embed.py cicero.json cicero.embed

    # issue a query
    python search.py "should i engage in politics" cicero.json cicero.embed

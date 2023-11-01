# exquiro: a proof of concept

An attempt to build a different kind of search engine for classical literature.

Existing digital classics projects like the [Perseus Digital Library](https://www.perseus.tufts.edu/hopper/) offer a feature-rich reading environment and comprehensive collection of works, in both the original and translation. Here's how the project [describes its search functionality](Searching: Users can not only read passages from texts, but use a suite of search tools to find what they are looking for, in any of the languages the Hopper supports. These search tools include word and phrase searches, in individual texts or collections. These searches include the option to search all possible inflections of a word, making them extremely powerful for morphologically rich languages like Greek, Latin and Arabic (e.g., a lemmatized search for the root form sum would also find documents containing the inflected forms est and sunt). For Classical texts, which have a well-adopted citation scheme, users can navigate a text by typing canonical abbreviations (e.g., Thuc. 1.24). The Hopper also provides functionality to search and browse the tagged named entities (places, people, dates, and date ranges) in a corpus, and includes an architecture for presenting archaeological artifact and image data, which is separate from the reading environment.):

> Searching: Users can not only read passages from texts, but use a suite of search tools to find what they are looking for, in any of the languages the Hopper supports. These search tools include word and phrase searches, in individual texts or collections. These searches include the option to search all possible inflections of a word, making them extremely powerful for morphologically rich languages like Greek, Latin and Arabic (e.g., a lemmatized search for the root form sum would also find documents containing the inflected forms est and sunt). For Classical texts, which have a well-adopted citation scheme, users can navigate a text by typing canonical abbreviations (e.g., Thuc. 1.24). The Hopper also provides functionality to search and browse the tagged named entities (places, people, dates, and date ranges) in a corpus, and includes an architecture for presenting archaeological artifact and image data, which is separate from the reading environment.

This is obviously great tool for scholars, and when I was taking Latin classes for several years I used Perseus (and other sites like [The Latin Library](https://www.thelatinlibrary.com/) and [LacusCurtius](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/home.html) a great deal. On the other hand, the search results for the queries [[meaning of life]](https://www.perseus.tufts.edu/hopper/searchresults?q=meaning+of+life) or [[burnout]](https://www.perseus.tufts.edu/hopper/searchresults?q=burnout) or [[how to cope with loss]](https://www.perseus.tufts.edu/hopper/searchresults?q=how+to+cope+with+loss) don't exactly offer the layman in the right direction. Using general-purpose search engines like Google does give topical results to queries like [[what did the greeks and romans say about the meaning of life]](https://www.google.com/search?q=what+did+the+greek+and+romans+say+about+the+meaning+of+life), but they're generally second-hand or (worse) coming from Quora and Medium. There's a ton of fascinating and fantastic writing from antiquity and I think it should be easy to find.

The project was inspired by the description of embedding-based semantic search as "vibes-based search" in [this excellent blog post about Embeddings](https://simonwillison.net/2023/Oct/23/embeddings/) by Simon Willison and the [tutorial on Semantic Search](https://www.sbert.net/examples/applications/semantic-search/README.html) from the [Sentence Transformers](https://www.sbert.net/index.html) project. For the corpus I'm using the [full archive download from Perseus](https://www.perseus.tufts.edu/hopper/opensource/download), but since I'm not a lawyer and just want to build something cool, and not figure out how to work with [these licensing terms](https://www.perseus.tufts.edu/hopper/help/copyright), I'll be using different (public domain) sources for the production version I'm working on. More to come :)

## conclusions

The search quality isn't fantastic right now, but it is clearly doing *something*, and for the given task I think it's doing better than existing tools. I'm working on a production version now with some better and more robust tools. More to come :)

## getting started

you need python3. then:

    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## usage

to process the data, generate embeddings, and run the search server locally:

    # extract data from corpus/* and serialize to corpus.json
    python preprocess.py corpus.json corpus/*

    # generate embeddings from corpus.json into corpus.embed
    python embed.py corpus.embed corpus.json

    # start the search server, using corpus.json corpus.embed
    python serve.py corpus.json corpus.embed

    # now open http://127.0.0.1:5000 and make some queries :)

## license

All texts in `corpus` come from the [Perseus Digital Library](https://www.perseus.tufts.edu/hopper/) and are therefore subject to the terms described [here](https://www.perseus.tufts.edu/hopper/help/copyright). (Since this site is not deployed, I am interpreting this repository as *not* being in violation of the statement "Any commercial use or publication without authorization is strictly prohibited.")

All of the other files are released under the MIT license; see LICENSE for more
details.


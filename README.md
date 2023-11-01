# exquiro: a proof of concept

An attempt to build a different kind of search engine for classical literature.

## TODO before open-sourcing

- [ ] clean up the code
- [ ] use flags
- [ ] make torch device optional
- [ ] maybe just give instructions to download the perseus archive to avoid getting into trouble

## background

Existing digital classics projects like the [Perseus Digital Library](https://www.perseus.tufts.edu/hopper/) offer a feature-rich reading environment and comprehensive collection of works, in both the original and translation. Here's how the project [describes its search functionality](https://www.perseus.tufts.edu/hopper/opensource):

> Searching: Users can not only read passages from texts, but use a suite of search tools to find what they are looking for, in any of the languages the Hopper supports. These search tools include word and phrase searches, in individual texts or collections. These searches include the option to search all possible inflections of a word, making them extremely powerful for morphologically rich languages like Greek, Latin and Arabic (e.g., a lemmatized search for the root form sum would also find documents containing the inflected forms est and sunt). For Classical texts, which have a well-adopted citation scheme, users can navigate a text by typing canonical abbreviations (e.g., Thuc. 1.24). The Hopper also provides functionality to search and browse the tagged named entities (places, people, dates, and date ranges) in a corpus, and includes an architecture for presenting archaeological artifact and image data, which is separate from the reading environment.

This is a great tool for scholars, and when I was taking Latin courses a few years back I relied a lot on Perseus and other sites like [The Latin Library](https://www.thelatinlibrary.com/) and [LacusCurtius](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/home.html). On the other hand, the search results for the queries [[meaning of life]](https://www.perseus.tufts.edu/hopper/searchresults?q=meaning+of+life) or [[burnout]](https://www.perseus.tufts.edu/hopper/searchresults?q=burnout) or [[how to cope with loss]](https://www.perseus.tufts.edu/hopper/searchresults?q=how+to+cope+with+loss) don't exactly point the layman in the right direction. Using general-purpose search engines like Google does give topical results to queries like [[what did the greeks and romans say about the meaning of life]](https://www.google.com/search?q=what+did+the+greek+and+romans+say+about+the+meaning+of+life), but they're generally second-hand and even (sigh) coming from Quora and Medium. There's a ton of fascinating and fantastic writing from antiquity and I think it should be easy to find.

The project was inspired by the description of embedding-based semantic search as "vibes-based search" in [this excellent blog post about Embeddings](https://simonwillison.net/2023/Oct/23/embeddings/) by Simon Willison. To build this proof-of-concept I followed the [tutorial on Semantic Search](https://www.sbert.net/examples/applications/semantic-search/README.html) from the [Sentence Transformers](https://www.sbert.net/index.html) project. For the corpus I'm using the [full archive download from Perseus](https://www.perseus.tufts.edu/hopper/opensource/download), but since I'm not a lawyer and just want to build something cool instead of figuring out how to work with [these licensing terms](https://www.perseus.tufts.edu/hopper/help/copyright), I'll be using different (public domain) sources in the future.

## results

The search quality isn't fantastic right now, but it is clearly doing *something*, and for the given task I think it's doing better than existing tools. Using the texts in `corpus` -- Homer's Iliad and Odyssey as well as Cicero's letters, orations, On Duties, On Friendship, On Old Age, -- the top result for [[meaning of life]] is this passage:

> It will be our duty, then, not to listen to those besotted men of pleasure when they argue about friendship, of which they understand neither the practice nor the theory. For what person is there, in the name of gods and men! who would wish to be surrounded by unlimited wealth and to abound in every material blessing, on condition that he love no one and that no one love him? Such indeed is the life of tyrants—a life, I mean, in which there can be no faith, no affection, no trust in the continuance of goodwill; where every act arouses suspicion and anxiety and where friendship has no place.

and all of the results for [[how did achilles kill hector]] are reasonable. There's still work to be done of course, and I'm working on a production version now. More to come :)

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

    # now open http://127.0.0.1:8080/search and make some queries :)

## license

All texts in `corpus` come from the [Perseus Digital Library](https://www.perseus.tufts.edu/hopper/) and are therefore subject to the terms described [here](https://www.perseus.tufts.edu/hopper/help/copyright). (Since this site is not deployed, I am interpreting this repository as *not* being in violation of the statement "Any commercial use or publication without authorization is strictly prohibited.")

All of the other files are released under the MIT license; see LICENSE for more
details.


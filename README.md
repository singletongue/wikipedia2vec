Wikipedia2Vec
=============

[![Fury badge](https://badge.fury.io/py/wikipedia2vec.png)](http://badge.fury.io/py/wikipedia2vec)
[![CircleCI](https://circleci.com/gh/studio-ousia/wikipedia2vec/tree/master.svg?style=svg)](https://circleci.com/gh/studio-ousia/wikipedia2vec/tree/master)

Introduction
------------

Wikipedia2Vec is a tool for obtaining quality embeddings (vector representations) of words and Wikipedia entities from  Wikipedia.
It is developed and maintained by [Studio Ousia](http://www.ousia.jp).

This tool enables you to learn embeddings that map words and entities into a unified continuous vector space.
The embeddings can be used as word embeddings, entity embeddings, and the unified embeddings of words and entities.
They are used in the state-of-the-art models of various tasks such as [entity linking](https://arxiv.org/abs/1601.01343), [named entity recognition](http://www.aclweb.org/anthology/I17-2017), [entity relatedness](https://arxiv.org/abs/1601.01343), and [question answering](https://arxiv.org/abs/1803.08652).

The embeddings can be easily built from a publicly available Wikipedia dump.
The code is implemented in Python, and optimized using Cython and BLAS.

How It Works
------------

<img src="http://studio-ousia.github.io/wikipedia2vec/img/model.png" width="600" />

Wikipedia2Vec is based on the [Word2vec's skip-gram model](https://en.wikipedia.org/wiki/Word2vec) that learns to predict neighboring words given each word in corpora.
We extend the skip-gram model by adding the following two sub-models:

- *The KB link graph model* that learns to estimate neighboring entities given an entity in the link graph of Wikipedia entities.
- *The anchor context model* that learns to predict neighboring words given an entity using an anchor link pointing to the entity and their neighboring words.

By jointly optimizing the skip-gram model and these two sub-models, our model simultaneously learns the embedding of words and entities from Wikipedia.
For further details, please refer to our paper: [Joint Learning of the Embedding of Words and Entities for Named Entity Disambiguation](https://arxiv.org/abs/1601.01343).

Pretrained Embeddings
---------------------

(coming soon)

Installation
------------

If you want to train embeddings on your machine, it is highly recommended to install a BLAS library before installing this tool.
We recommend to use [OpenBLAS](https://www.openblas.net/) or [Intel Math Kernel Library](https://software.intel.com/en-us/mkl).

Wikipedia2Vec can be installed from PyPI:

```
% pip install Wikipedia2Vec
```

To process Japanese Wikipedia dumps, it is also required to install [MeCab](http://taku910.github.io/mecab/) and [its Python binding](https://pypi.python.org/pypi/mecab-python3).

Learning Embeddings
-------------------

First, you need to download a source Wikipedia dump file (e.g., enwiki-latest-pages-articles.xml.bz2) from [Wikimedia Downloads](https://dumps.wikimedia.org/).
The English dump file can be obtained by:

```
% wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
```

Note that, you do not need to decompress the dump file.

Then, the embeddings can be built from a Wikipedia dump using the *train* command:

```
% wikipedia2vec train DUMP_FILE MODEL_FILE
```

*Options:*

- *--dim-size*: The number of dimensions of the embeddings (default: 100)
- *--window*: The maximum distance between the target item (word or entity) and the context word to be predicted (default: 5)
- *--iteration*: The number of iterations for Wikipedia pages (default: 3)
- *--negative*: The number of negative samples (default: 5)
- *--lowercase/--no-lowercase*: Whether to lowercase words and phrases (default: True)
- *--min-word-count*: A word is ignored if the total frequency of the word is lower than this value (default: 10)
- *--min-entity-count*: An entity is ignored if the total frequency of the entity appearing as the referent of an anchor link is lower than this value (default: 5)
- *--link-graph/--no-link-graph*: Whether to learn from the Wikipedia link graph (default: True)
- *--links-per-page*: The number of contextual entities to be generated from the link graph for processing each page (default: 10)
- *--phrase/--no-phrase*: Whether to learn the embeddings of phrases (default: True)
- *--min-link-count*: A phrase is ignored if the total frequency of the phrase appearing as an anchor link is lower than this value (default: 10)
- *--min-link-prob*: A phrase is ignored if the probability of the phrase appearing as an anchor link is lower than this value (default: 0.1)
- *--max-phrase-len*: The maximum number of words in a phrase (default: 4)
- *--init-alpha*: The initial learning rate (default: 0.025)
- *--min-alpha*: The minimum learning rate (default: 0.0001)
- *--sample*: The parameter that controls downsampling of high frequency words (default: 1e-4)

The *train* command internally runs the four commands described below (i.e., *build_phrase_dictionary*, *build_dictionary*, *build_link_graph*, and *train_embedding*).

### Building Phrase Dictionary

The *build_phrase_dictionary* command constructs a dictionary consisting of phrases extracted from Wikipedia.
We extract all phrases that appear as an anchor link in Wikipedia, and reduce them using the three thresholds such as *min_link_count*, *min_link_prob*, and *max_phrase_len*.
Detected phrases are treated as words in the subsequent steps.

```
% wikipedia2vec build_phrase_dictionary DUMP_FILE PHRASE_DIC_NAME
```

*Options:*

- *--lowercase/--no-lowercase*: Whether to lowercase phrases (default: True)
- *--min-link-count*: A phrase is ignored if the total frequency of the phrase appearing as an anchor link is lower than this value (default: 10)
- *--min-link-prob*: A phrase is ignored if the probability of the phrase appearing as an anchor link is lower than this value (default: 0.1)
- *--max-phrase-len*: The maximum number of words in a phrase (default: 4)

### Building Dictionary

The *build\_dictionary* command builds a dictionary of words and entities.

```
% wikipedia2vec build_dictionary DUMP_FILE DIC_FILE
```

*Options:*

- *--phrase*: The phrase dictionary file generated using the *build\_phrase\_dictionary* command
- *--lowercase/--no-lowercase*: Whether to lowercase words (default: True)
- *--min-word-count*: A word is ignored if the total frequency of the word is lower than this value (default: 10)
- *--min-entity-count*: An entity is ignored if the total frequency of the entity appearing as the referent of an anchor link is lower than this value (default: 5)

### Building Link Graph

The *build\_link\_graph* command generates a sparse matrix representing the link structure between Wikipedia entities.

```
% wikipedia2vec build_link_graph DUMP_FILE DIC_FILE LINK_GRAPH_FILE
```

There is no option in this command.

### Learning Embeddings

The *train_embedding* command runs the training of the embeddings.

```
% wikipedia2vec train_embedding DUMP_FILE DIC_FILE MODEL_FILE
```

*Options:*

- *--link-graph*: The link graph file generated using the *build\_link\_graph* command
- *--dim-size*: The number of dimensions of the embeddings (default: 100)
- *--window*: The maximum distance between the target item (word or entity) and the context word to be predicted (default: 5)
- *--iteration*: The number of iterations for Wikipedia pages (default: 3)
- *--negative*: The number of negative samples (default: 5)
- *--links-per-page*: The number of contextual entities to be generated from the link graph for processing each page (default: 10)
- *--init-alpha*: The initial learning rate (default: 0.025)
- *--min-alpha*: The minimum learning rate (default: 0.0001)
- *--sample*: The parameter that controls downsampling of high frequency words (default: 1e-4)

### Saving Embeddings in Text Format

*save\_text* outputs a model in a text format.

```
% wikipedia2vec save_text MODEL_FILE OUT_FILE
```

Sample Usage
------------

```python
>>> from wikipedia2vec import Wikipedia2Vec

>>> wiki2vec = Wikipedia2Vec.load(MODEL_FILE)

>>> wiki2vec.get_word_vector(u'the')
memmap([ 0.01617998, -0.03325786, -0.01397999, -0.00150471,  0.03237337,
...
       -0.04226106, -0.19677088, -0.31087297,  0.1071524 , -0.09824426], dtype=float32)

>>> wiki2vec.get_entity_vector(u'Scarlett Johansson')
memmap([-0.19793572,  0.30861306,  0.29620451, -0.01193621,  0.18228433,
...
        0.04986198,  0.24383858, -0.01466644,  0.10835337, -0.0697331 ], dtype=float32)

>>> wiki2vec.most_similar(wiki2vec.get_word(u'yoda'), 5)
[(<Word yoda>, 1.0),
 (<Entity Yoda>, 0.84333622),
 (<Word darth>, 0.73328167),
 (<Word kenobi>, 0.7328127),
 (<Word jedi>, 0.7223742)]

>>> wiki2vec.most_similar(wiki2vec.get_entity(u'Scarlett Johansson'), 5)
[(<Entity Scarlett Johansson>, 1.0),
 (<Entity Natalie Portman>, 0.75090045),
 (<Entity Eva Mendes>, 0.73651594),
 (<Entity Emma Stone>, 0.72868186),
 (<Entity Cameron Diaz>, 0.72390842)]
```

Reference
---------

If you use Wikipedia2Vec in a scientific publication, please cite the following paper:

    @InProceedings{yamada-EtAl:2016:CoNLL,
      author    = {Yamada, Ikuya  and  Shindo, Hiroyuki  and  Takeda, Hideaki  and  Takefuji, Yoshiyasu},
      title     = {Joint Learning of the Embedding of Words and Entities for Named Entity Disambiguation},
      booktitle = {Proceedings of The 20th SIGNLL Conference on Computational Natural Language Learning},
      month     = {August},
      year      = {2016},
      address   = {Berlin, Germany},
      pages     = {250--259},
      publisher = {Association for Computational Linguistics}
    }

License
-------

[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
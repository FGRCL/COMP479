# Concordia.ca Indexer

## Running the indexer
use `index.py` to create the inverted index for the concordia domain. Use the following options
```
optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        File path for the final index
  --maxpages MAXPAGES, -m MAXPAGES
                        The max number of pages to crawl
```
Don't specify the `--maxpages` options to crawl an unlimited number of pages.
Don't specify the `--maxpages` options to crawl an unlimited number of pages.

example: `python index.py -m 100 -o index/index.pickle`. A pre-made index is located in `index/index.pickle`

## Making queries

use `query.py` to make queries to the index. The following program options are available
```
-h, --help            show this help message and exit
--index INDEX, -i INDEX
                    Path to the inverted index to use
--query QUERY, -q QUERY
                    the use query
--rankingalgorithm {tfidf,bm25}, -ra {tfidf,bm25}
                    The ranking algorithm to use
--output OUTPUT, -o OUTPUT
                    The output file    
```
example `python query.py -i index/index.pickle -o out/results.txt -q "cool query" -ra bm25`
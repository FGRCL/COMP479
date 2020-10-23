# Inverted Index Implementation for Reuters-21578

You can use poetry to install the python environment with the required dependencies with `poetry install`. Or install the following dependencies in your environment:

```
python = "^3.8"
beautifulsoup4 = "*"
lxml = "*"
nltk = "*"
```

## Creating the inverted index
Use the script `ir/p2/indexer.py` to create your inverted index. The script has the following options:
```
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Reuters collection directory
  -i INDEX, --index INDEX
                        The index outputfile
  -s STOPWORDS, --stopwords STOPWORDS
                        remove the stopwords in the given list from the index
  -rmn, --removenumbers
                        remove numbers from the index
  -cf, --casefolding    case fold the terms before indexing them
  -st, --stemming       stem the terms before indexing them
```
All tokens on the filters are optional

## Performing single term queries
Use the script `ir/p2/query.py` to perform single term queries on the inverted index. The script has the following options:
```
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        The inverted index to use
  -t term [term ...], --terms term [term ...]
                        A list of terms to perform single term queries on
  -o OUTPUT, --output OUTPUT
                        The path for the ouput file
```
The `stdout` will be used as output if not specified.
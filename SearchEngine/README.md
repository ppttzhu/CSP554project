# Elasticsearch and Solr

## How to run

1. Clone this repository and [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) repository in the same directory.
2. Follow install.sh to install elasticsearch, solr, and python packages. For example: `sudo sh install.sh`
3. Run index.py to load json files and create index.
Clear database: `python3 index.py preprocess` 
Run elasticsearch: `python3 index.py elasticsearch` 
Run solr: `python3 index.py solr` 
4. Run query.py to search.
Prepare data: `python3 query.py preprocess` 
Run elasticsearch: `python3 query.py elasticsearch` 
Run solr: `python3 query.py solr` 
5. In the meantime, run following command in terminal to track memory use:
`top -b -n300 | grep elastic >> memory_use.log`
`top -b -n300 | grep solr >> memory_use.log`
6. Run analysis.py to analyse logs and results.
`python3 analysis.py` 

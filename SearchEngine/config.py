import sys, logging
from elasticsearch import Elasticsearch
import pysolr

poetry_dir = '/mnt/Files/HP/Graduate/IIT/2019Fall/CSP554/Project/chinese-poetry'

# Elasticsearch
es = Elasticsearch()

# Solr
port = '7574'
solr_dict = {
    'poetry': pysolr.Solr('http://localhost:%s/solr/poetry' % port, always_commit=True),
    'author': pysolr.Solr('http://localhost:%s/solr/author' % port, always_commit=True)
    }

# logging
log_level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('__main__')
logger.setLevel(log_level)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
handler.setFormatter(logging.Formatter(format))
logger.addHandler(handler)
handler = logging.FileHandler('search_engine.log', 'a', 'gb2312')  # 'gb2312' for Chinese, not 'utf-8'
handler.setLevel(log_level)
handler.setFormatter(logging.Formatter(format))
logger.addHandler(handler)

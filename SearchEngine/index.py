import json, os, datetime, requests
from elasticsearch import Elasticsearch, helpers
import pysolr
from config import *

sub_dir_names = [
    # sub_dir, category, name_pattern
#     ('ci', '宋词', 'ci.song'),
    ('ci', '宋代词人', 'author.song'),
#     ('json', '宋诗', 'poet.song'),
#     ('json', '唐诗', 'poet.tang'),
    ('json', '宋代诗人', 'authors.song'),
    ('json', '唐代诗人', 'authors.tang'),
#     ('lunyu', '论语', 'lunyu'),
#     ('shijing', '诗经', 'shijing'),
#     ('sishuwujing', '大学', 'daxue'),
#     ('sishuwujing', '孟子', 'mengzi'),
#     ('sishuwujing', '中庸', 'zhongyong'),
#     ('wudai', '花间集', 'huajianji'),
#     ('wudai', '南唐诗', 'poetrys'),
    ('wudai', '南唐诗人', 'authors'),
#     ('youmengying', '幽梦影', 'youmengying')
]


def main():
#     preprocess()
    load_files('elasticsearch')
#     load_files('solr')


def preprocess():
    # Parameters 
    numShards = 1
    numReplica = 1
    
    logging.getLogger(__name__).debug('Preparing Elasticsearch...')
    
    # Elasticsearch
    # Delete indices if exist to avoid multiple indexing
    es.indices.delete(index='poetry', ignore=[400, 404])
    es.indices.delete(index='author', ignore=[400, 404])
    # Create new indices
    request_body = {
        "settings" : {
            "number_of_shards": numShards,
            "number_of_replicas": numReplica
        }
    }
    es.indices.create(index='poetry', body=request_body)
    es.indices.create(index='author', body=request_body)
    
    logging.getLogger(__name__).debug('Preparing Solr...')
    
    # Solr
    # Delete collections if exist to avoid multiple indexing
    requests.get("http://localhost:%s/solr/admin/collections?action=DELETE&name=poetry" % port)
    requests.get("http://localhost:%s/solr/admin/collections?action=DELETE&name=author" % port)
    # Create new collections
    r1 = requests.get("http://localhost:%s/solr/admin/collections?action=CREATE&name=poetry&numShards=%d&replicationFactor=%d" % (port, numShards, numReplica))
    r2 = requests.get("http://localhost:%s/solr/admin/collections?action=CREATE&name=author&numShards=%d&replicationFactor=%d" % (port, numShards, numReplica))
    if json.loads(r1.text)['responseHeader']['status'] == 0 and json.loads(r2.text)['responseHeader']['status'] == 0:
        logging.getLogger(__name__).debug('Success building Solr collections.')
    else:
        logging.getLogger(__name__).debug('Failed building Solr collections.')


def load_files(engine):
    logging.getLogger(__name__).info('Runing %s...' % engine)
    used_time = 0
    for sub_dir_name in sub_dir_names:
        sub_dir, category, name_pattern = sub_dir_name
        database = 'author' if name_pattern[:6] == 'author' else 'poetry'
        for roots, directories, files in os.walk(os.path.join(poetry_dir, sub_dir)):
            for file in files:
                if file[:len(name_pattern)] == name_pattern and file[-4:].lower() == 'json':
                    logging.getLogger(__name__).debug("Dealing with file: %s" % file)
                    used_time += index_file(engine, os.path.join(roots, file), database, category)
    logging.getLogger(__name__).info('%s takes %.4f s.' % (engine, used_time))

                
def index_file(engine, file_path, database, category):
    fp = open(file_path, 'r')
    content = fp.read()
    json_files = json.loads(content)
    if type(json_files) is dict:
        json_files = [json_files]
    logging.getLogger(__name__).info("Making index for %s. (%d items)" % (category, len(json_files)))
#     # index each json object one by one: (Solr will be very slow) 
#     for i in range(len(json_files)):
#         content = json_files[i]
#         content['category'] = category
#         if engine == 'elasticsearch':
#             es.index(index=database, body=content)
#         elif engine == 'solr':
#             solr_dict[database].add([content])
    # index whole json object list with one command:
    for i in range(len(json_files)):
        json_files[i]['category'] = category
        if engine == 'elasticsearch':
            json_files[i] = { "_index" : database, "_source" : json_files[i] }
    start = datetime.datetime.now()
    if engine == 'elasticsearch':
        helpers.bulk(es, json_files)
    elif engine == 'solr':
        solr_dict[database].add(json_files)
    used_time = (datetime.datetime.now() - start).total_seconds()
    fp.close()
    logging.getLogger(__name__).info("Finished within %.2f s." % used_time)
    if engine == 'elasticsearch':
        # elasticsearch has time lag for the following queries
        num = es.indices.stats(index=database)['_all']['primaries']['docs']['count']
    elif engine == 'solr':
        num = solr_dict[database].search(q="*:*").hits
    logging.getLogger(__name__).info("%d items in %s." % (num, database))
    return used_time


if __name__ == '__main__':
    main()

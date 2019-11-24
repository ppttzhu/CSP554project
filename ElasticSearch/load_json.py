import json, os, datetime, sys, logging, requests
from elasticsearch import Elasticsearch
import pysolr

root_dir = '/mnt/Files/HP/Graduate/IIT/2019Fall/CSP554/Project/chinese-poetry'
sub_dir_names = [
    # sub_dir, category, name_pattern
    ('ci', '宋词', 'ci.song'),
    ('ci', '宋代词人', 'author.song'),
    ('json', '宋诗', 'poet.song'),
    ('json', '唐诗', 'poet.tang'),
    ('json', '宋代诗人', 'authors.song'),
    ('json', '唐代诗人', 'authors.tang'),
    ('lunyu', '论语', 'lunyu'),
    ('shijing', '诗经', 'shijing'),
    ('sishuwujing', '大学', 'daxue'),
    ('sishuwujing', '孟子', 'mengzi'),
    ('sishuwujing', '中庸', 'zhongyong'),
    ('wudai', '花间集', 'huajianji'),
    ('wudai', '南唐诗', 'poetrys'),
    ('wudai', '南唐诗人', 'authors'),
    ('youmengying', '幽梦影', 'youmengying')
]

engine = ''

# Elasticsearch
es = Elasticsearch()

# Solr
port = '7574'
solr_dict = {
    'poetry': pysolr.Solr('http://localhost:%s/solr/poetry' % port, always_commit=True),
    'author': pysolr.Solr('http://localhost:%s/solr/author' % port, always_commit=True)
    }


def main():
    global engine
    preprocess()
    
    logging.getLogger(__name__).info('Runing Elasticsearch...')
    engine = 'elasticsearch'
    start = datetime.datetime.now()
    load_files()
    logging.getLogger(__name__).info('Elasticsearch takes %.1f s.' % (datetime.datetime.now() - start).total_seconds())
    
    logging.getLogger(__name__).info('Runing Solr...')
    engine = 'solr'
    start = datetime.datetime.now()
    load_files()
    logging.getLogger(__name__).info('Solr takes %.1f s.' % (datetime.datetime.now() - start).total_seconds())

    
def preprocess():
    
    logging.getLogger(__name__).debug('Preparing...')
    
    # Elasticsearch
    # Remove index to avoid multiple indexing
    es.indices.delete(index='poetry')
    es.indices.delete(index='author')
    
    # Solr
    # Delete collections if exist
    requests.get("http://localhost:%s/solr/admin/collections?action=DELETE&name=poetry" % port)
    requests.get("http://localhost:%s/solr/admin/collections?action=DELETE&name=author" % port)
    # Create new collections
    numShards = 1
    replicationFactor = 1
    r1 = requests.get("http://localhost:%s/solr/admin/collections?action=CREATE&name=poetry&numShards=%d&replicationFactor=%d" % (port, numShards, replicationFactor))
    r2 = requests.get("http://localhost:%s/solr/admin/collections?action=CREATE&name=author&numShards=%d&replicationFactor=%d" % (port, numShards, replicationFactor))
    if json.loads(r1.text)['responseHeader']['status'] == 0 and json.loads(r2.text)['responseHeader']['status'] == 0:
        logging.getLogger(__name__).debug('Success building Solr collections.')
    else:
        logging.getLogger(__name__).debug('Failed building Solr collections.')


def load_files():
    for sub_dir_name in sub_dir_names:
        sub_dir, category, name_pattern = sub_dir_name
        database = 'author' if name_pattern[:6] == 'author' else 'poetry'
        for file in os.listdir(os.path.join(root_dir, sub_dir)):
            filename = os.fsdecode(file)
            if filename[:len(name_pattern)] == name_pattern and filename[-4:].lower() == 'json':
                logging.getLogger(__name__).debug("Dealing with file: %s" % filename)
                index_file(os.path.join(root_dir, sub_dir, filename), database, category)

                
def index_file(file_path, database, category):
    global engine
    fp = open(file_path, 'r')
    content = fp.read()
    json_files = json.loads(content)
    if type(json_files) is dict:
        json_files = [json_files]
    logging.getLogger(__name__).info("Making index for %s. (%d items)" % (category, len(json_files)))
    for i in range(len(json_files)):
        content = json_files[i]
        content['category'] = category
        if engine == 'elasticsearch':
            es.index(index=database, body=content)
        elif engine == 'solr':
            solr_dict[database].add([content])
    fp.close()
    logging.getLogger(__name__).info("%d files added." % len(json_files))
    if engine == 'elasticsearch':
        num = es.search(index=database, body={"query": {"match_all": {}}})['hits']['total']['value']
    elif engine == 'solr':
        r = requests.get('http://localhost:%s/solr/%s/select?indent=on&q=*:*' % (port, database))
        num = json.loads(r.text)['response']['numFound']
    logging.getLogger(__name__).info("%d items in %s." % (num, database))


log_level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handler.setFormatter(logging.Formatter(format))
logger.addHandler(handler)
logging.basicConfig(filename='load_json.log', filemode='a', format=format)

if __name__ == '__main__':
    main()

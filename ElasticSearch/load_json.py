import json, os, datetime, sys, logging
from elasticsearch import Elasticsearch

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
es = Elasticsearch()


def make_index(file_path, index, category):
    fp = open(file_path, 'r')
    content = fp.read()
    json_files = json.loads(content)
    if type(json_files) is dict:
        json_files = [json_files]
    logging.getLogger(__name__).info("Making index for %s. (%d items)" % (category, len(json_files)))
    for i in range(len(json_files)):
        content = json_files[i]
        content['category'] = category
        es.index(index=index, body=content)
    fp.close()
    logging.getLogger(__name__).info("%d files added." % len(json_files))
    res = es.search(index=index, body={"query": {"match_all": {}}})
    logging.getLogger(__name__).info("%d items in %s." % (res['hits']['total']['value'], index))


def main():
    for sub_dir_name in sub_dir_names:
        sub_dir, category, name_pattern = sub_dir_name
        index = 'author' if name_pattern[:6] == 'author' else 'poetry'
        for file in os.listdir(os.path.join(root_dir, sub_dir)):
            filename = os.fsdecode(file)
            if filename[:len(name_pattern)] == name_pattern and filename[-4:].lower() == 'json':
                logging.getLogger(__name__).debug("Dealing with file: %s" % filename)
                make_index(os.path.join(root_dir, sub_dir, filename), index, category)


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
    # Remove index to avoid multiple indexing
    es.indices.delete(index='poetry')
    es.indices.delete(index='author')
    start = datetime.datetime.now()
    main()
    logging.getLogger(__name__).info('Done. Takes %.1f s.' % (datetime.datetime.now() - start).total_seconds())

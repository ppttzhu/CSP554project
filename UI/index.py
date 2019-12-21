import json, os, datetime, requests
from elasticsearch import Elasticsearch, helpers

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

poetry_dir = "/mnt/Files/HP/Graduate/Gits/chinese-poetry"

# Elasticsearch
es = Elasticsearch()

# Punctuations, used for Start and End search
punctuations = ["，", "。", "！", "？"]

def main():
    preprocess()
    load_files()

def preprocess():
    # Parameters 
    numShards = 1
    numReplica = 1
    
    print('Preparing Elasticsearch...')
    
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
    

def load_files():
    if not os.path.isdir(poetry_dir):
        print('%s does not exist, please pull data from github.' % poetry_dir)
        return 
    used_time = 0
    for sub_dir_name in sub_dir_names:
        sub_dir, category, name_pattern = sub_dir_name
        database = 'author' if name_pattern[:6] == 'author' else 'poetry'
        for roots, directories, files in os.walk(os.path.join(poetry_dir, sub_dir)):
            for file in files:
                if file[:len(name_pattern)] == name_pattern and file[-4:].lower() == 'json':
                    print("Dealing with file: %s" % file)
                    used_time += index_file(os.path.join(roots, file), database, category)
    print('Takes %.4f s.' % used_time)

                
def index_file(file_path, database, category):
    fp = open(file_path, 'r')
    content = fp.read()
    json_files = json.loads(content)
    if type(json_files) is dict:
        json_files = [json_files]
    print("Making index for %s. (%d items)" % (category, len(json_files)))
    for i in range(len(json_files)):
        json_files[i]['category'] = category
        if "paragraphs" in json_files[i]:
            for j in range(len(json_files[i]["paragraphs"])):
                for punctuation in punctuations:
                    json_files[i]["paragraphs"][j] =  json_files[i]["paragraphs"][j].replace(punctuation, "end" + punctuation + "start")
                json_files[i]["paragraphs"][j] = "start" +  json_files[i]["paragraphs"][j] + "end" 
                json_files[i]["paragraphs"][j] = json_files[i]["paragraphs"][j].replace("startend", "")
        json_files[i] = { "_index" : database, "_source" : json_files[i]}
    start = datetime.datetime.now()
    helpers.bulk(es, json_files)
    used_time = (datetime.datetime.now() - start).total_seconds()
    fp.close()
    print("Finished within %.4f s." % used_time)
    return used_time


if __name__ == '__main__':
    main()

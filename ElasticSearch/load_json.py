import json, os
from elasticsearch import Elasticsearch

directory = '/mnt/Files/HP/Graduate/IIT/2019Fall/CSP554/Project/chinese-poetry/json/poet.song.1000.json'
es = Elasticsearch()

f = os.open(directory)
content = f.read()
json_files = json.loads(content)
for i in range(0, len(json_files)):
    es.index(index='testpoetry', id=i+1, body=json_files[i])

res = es.get(index="testpoetry", id=1)
print(res['_source'])
   
res = es.search(index="testpoetry", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

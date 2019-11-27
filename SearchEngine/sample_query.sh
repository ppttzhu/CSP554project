# Elasticsearch ==============================================

curl -X POST "localhost:9200/testpoetry/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "multi_match": {
      "query": "朱貞白",
      "fields": ["author"],
      "operator":   "and" 
    }
  }
}
'

curl -X POST "localhost:9200/testpoetry/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match" : {
            "author" : {
                "query" : "朱貞白",
                "operator":   "and" 
            }
        }
    }
}
'

curl -X GET "localhost:9200/test-index/_search?q=kimchy"

curl -X POST "localhost:9200/test-index/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match" : {
            "author" : {
                "query" : "kimchy",
                "operator":   "and" 
            }
        }
    }
}
'

# Solr ==============================================

curl -X GET     "http://localhost:7574/solr/admin/collections?action=CREATE&name=test&numShards=1&replicationFactor=1" 

curl -X POST -H 'Content-Type: application/json' 'http://localhost:7574/solr/test/update/json/docs' --data-binary '
{
  "id": "66kfkkffk",
  "title": "Doc ddddd1"
}'


curl 'http://localhost:7574/solr/test/update?commit=true' --data-binary @/mnt/Files/HP/Graduate/IIT/2019Fall/CSP554/Project/chinese-poetry/json/poet.song.1000.json -H 'Content-type:application/json'

curl -X GET "http://localhost:7574/solr/test/select?indent=on&q=*:*"

# Elasticsearch ==============================================

curl -X POST "localhost:9200/poetry/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "multi_match": {
      "query": "苏轼",
      "fields": ["author"],
      "operator":   "and" 
    }
  }
}
'

curl -X POST "localhost:9200/poetry/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match" : {
            "author" : {
                "query" : "苏轼",
                "operator":   "and" 
            }
        }
    }
}
'

curl -X GET "localhost:9200/test-index/_search?q=kimchy"

curl -X POST "localhost:9200/author/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match_all" : {
        }
    }
}
'

curl -X PUT "http://localhost:9200/poetry/_settings" -d '{ "index" : { "max_result_window" : 500000 } }'

curl -X GET "localhost:9200/poetry/_settings?pretty"

curl -X GET "localhost:9200/poetry/_stats/docs"

curl -X POST "localhost:9200/author/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "_source": ["name"],
    "query": {
        "match_all" : {}
    }
}
'

curl -X POST "localhost:9200/poetry/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 10000000,
  "query" : {
    "bool" : { 
      "should" : [
            {"match" : {
                "author" : {
                    "query" : "苏轼",
                    "operator":   "and" 
                    }
                }
            },
            {"term" : {"paragraphs": "一"}}
      ]
    }
  }
}
'

curl -X PUT "localhost:9200/poetry/_settings?pretty" -H 'Content-Type: application/json' -d'
{
    "index" : {
        "max_result_window" : "10000000"
    }
}
'

curl -X GET "localhost:9200/poetry/_settings?pretty"

# Solr ==============================================

curl -X GET "http://localhost:7574/solr/admin/collections?action=CREATE&name=test&numShards=1&replicationFactor=1" 

curl -X POST -H 'Content-Type: application/json' 'http://localhost:7574/solr/test/update/json/docs' --data-binary '
{
  "id": "66kfkkffk",
  "title": "Doc ddddd1"
}'


curl 'http://localhost:7574/solr/test/update?commit=true' --data-binary @/mnt/Files/HP/Graduate/IIT/2019Fall/CSP554/Project/chinese-poetry/json/poet.song.1000.json -H 'Content-type:application/json'

curl -X GET "http://localhost:7574/solr/poetry/select?indent=on&q=*:*"
curl -X GET "http://localhost:7574/solr/poetry/select?indent=on&q=*:*&fq=title:Doc"
# get all fields names
curl -X GET "http://localhost:7574/solr/poetry/select?q=author:李清照"

curl 'http://localhost:7574/solr/poetry/select?sow=true' -d '
{
  "query": "author:李清照"
}'



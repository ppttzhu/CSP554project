# Start ElasticSearch
sudo systemctl start elasticsearch.service

# Stop ElasticSearch
sudo systemctl stop elasticsearch.service

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
    "match_phrase": {
      "paragraphs": "s莫"
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
  "size": 100,
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


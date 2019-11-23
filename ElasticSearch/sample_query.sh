# sample query

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

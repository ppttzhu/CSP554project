from config import *


def main():
    docs, hits = single_search('elasticsearch', 'poetry', ['paragraphs'], '下')
    print(hits)
    print(docs)
    docs, hits = single_search('solr', 'poetry', ['paragraphs'], '下')
    print(hits)
    print(docs)


def single_search(engine, database, fields, query):
    if engine == 'elasticsearch':
        request_body = {
          "query": {
            "multi_match": {
              "query": query,
              "fields": fields,
              "operator":  "and" 
            }
          }
        }
        response = es.search(index=database, body=request_body)
        docs, hits = response['hits']['hits'], response['hits']['total']['value']
    elif engine == 'solr':
        q = ""
        for field in fields:
            q += field + ":" + query
        response = solr_dict[database].search(q=q)
        docs, hits = response.docs, response.hits
    else:
        return None, None
    return docs, hits
    
    
if __name__ == '__main__':
    main()

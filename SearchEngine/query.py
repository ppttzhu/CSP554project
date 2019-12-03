from config import *
import pandas as pd
import datetime


def main():
    chinese_characters = load_chinese_characters("3500commonChinesecharacters.xls")
    for engine in ['elasticsearch', 'solr']:
        logging.getLogger(__name__).info('Runing %s...' % engine)
        start = datetime.datetime.now()
        for i in range(10):  # len(chinese_characters)
            docs, hits = single_search(engine, 'poetry', ['paragraphs'], chinese_characters[i])
            logging.getLogger(__name__).info(hits)
#             print(docs)
        used_time = (datetime.datetime.now() - start).total_seconds()
        logging.getLogger(__name__).info('%s takes %.1f s.' % (engine, used_time))


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

    
def load_chinese_characters(file_name):
    xls = pd.ExcelFile(file_name)
    sheetX = xls.parse(0)  # 0 is the sheet number
    chinese = sheetX['ch']  # ch is the column name
    return chinese

 
if __name__ == '__main__':
    main()

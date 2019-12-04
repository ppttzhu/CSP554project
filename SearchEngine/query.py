from config import *
import pandas as pd
import datetime, sys
from elasticsearch import helpers

def main():
    if (len(sys.argv) < 2):
        logging.getLogger(__name__).warning("Please run this script follow by argument: elasticsearch, solr or preprocess")
    elif sys.argv[1] == "preprocess":
        save_poem_writers("data/ChinesePoemWritters.txt")
    elif sys.argv[1] == "elasticsearch":
        run("elasticsearch", "single_search")
        run("elasticsearch", "multi_search_and")
        run("elasticsearch", "multi_search_or")
    elif sys.argv[1] == "solr":
        run("solr", "single_search")
        run("solr", "multi_search_and")
        run("solr", "multi_search_or")
    else:
        logging.getLogger(__name__).warning("Please run this script follow by argument: elasticsearch, solr or preprocess")


def run(engine, experiment):
    chinese_characters = load_chinese_characters("data/3500commonChinesecharacters.xls")
    writers = load_poem_writers("data/ChinesePoemWritters.txt")
    results = []
    logging.getLogger(__name__).info('Runing %s %s...' % (engine, experiment))
    start = datetime.datetime.now()
    if experiment == 'single_search':
        for i in range(len(chinese_characters)):
            docs, hits = search(engine, 'poetry', [('paragraphs' , chinese_characters[i])])
            results.append((chinese_characters[i], hits))
    elif experiment == 'multi_search_and':
        for i in range(1000):  # len(chinese_characters)
            for j in range(1000):  # len(writers)
                fields_queries = [('paragraphs' , chinese_characters[i]), ('author', writers[j])]
                docs, hits = search(engine, 'poetry', fields_queries, 'AND')
                results.append((writers[j] + ',' + chinese_characters[i], hits))
    elif experiment == 'multi_search_or':
        for i in range(1000):  # len(chinese_characters)
            for j in range(1000):  # len(writers)
                fields_queries = [('title', chinese_characters[i]), ('paragraphs' , chinese_characters[i]), ('author', writers[j])]
                docs, hits = search(engine, 'poetry', fields_queries, 'OR')
                results.append((writers[j] + ',' + chinese_characters[i], hits))
    used_time = (datetime.datetime.now() - start).total_seconds()
    logging.getLogger(__name__).info('%s takes %.4f s.' % (engine, used_time))
    # Save to hits results to file
    if not os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')):
        os.mkdir('results')
    out_file_name = "results/%s.txt" % (engine + '_' + experiment)
    fp = open(out_file_name, 'w+')
    for item in results:
        fp.write(engine + ',' + item[0] + ',' + str(item[1]) + '\n')
    fp.close()
    logging.getLogger(__name__).info('Results saved to %s.' % out_file_name)


def search(engine, database, fields_queries, operator=""):
    if engine == 'elasticsearch':
        if len(fields_queries) > 1: 
            # multi_search
            fields_queries_list = []
            for filed, query in fields_queries:
                if len(query) > 1:
                    fields_queries_list.append({"match" : {filed : {"query" : query, "operator":"and" }}})
                else:
                    fields_queries_list.append({"term" : {filed: query}})
            if operator == "AND": 
                operator = "must"  
            elif operator == "OR":
                operator = "should"  
            request_body = {
                "query" : {
                    "bool" : { 
                        operator : fields_queries_list
                    }
                }
            }
        else: 
            # single_search
            field, query = fields_queries[0]
            request_body = {
                "query": {
                    "match": {
                        field: {
                            "query": query,
                        }
                    }
                }
            }
        response = es.search(index=database, body=request_body)
        response = helpers.scan(es, query=request_body, index=database)
        docs = list(response)
        hits = len(docs)
    elif engine == 'solr':
        q = fields_queries[0][0] + ":" + fields_queries[0][1]
        for i in range(1, len(fields_queries)):
            q += " " + operator + " " + fields_queries[i][0] + ":" + fields_queries[i][1]
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


def save_poem_writers(file_name):
    request_body = {
            "_source": ["name"],
            "size": 10000,
            "query": {
                "match_all" : {}
            }
        }
    response = es.search(index='author', body=request_body)
    fp = open(file_name, 'w+')
    for dict in response['hits']['hits']:
        writer = dict['_source']['name']
        if len(writer) > 1 and '□' not in writer and '{' not in writer and '（' not in writer and not any(char.isdigit() for char in writer):
            fp.write(writer + '\n')
    fp.close()
    logging.getLogger(__name__).info('Results saved to %s.' % file_name)
    
    
def load_poem_writers(file_name):
    fp = open(file_name, 'r')
    writers = []
    for line in fp:
        writers.append(line[:-1])
    fp.close()
    return writers

 
if __name__ == '__main__':
    main()

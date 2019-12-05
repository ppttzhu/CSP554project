import os, re
from config import *
from collections import defaultdict


def main():
    analyse_memory_use()
    analyse_query_hit()

    
def analyse_memory_use():
    if not os.path.exists('memory_use.log'):
        logging.getLogger(__name__).warning("memory_use.log does not exist. Please run top.")
        return
    fp = open('memory_use.log', 'r')
    dict = defaultdict(list)
    cur = 0
    for line in fp:
        linel = re.sub(' +', ' ', line[:-1]).split(' ')
        if linel[0] == 'Process:':
            for key in dict:
                logging.getLogger(__name__).info("%s Average, Max, Min: %.4f, %.4f, %.4f" % (key, sum(dict[key]) / len(dict[key]), max(dict[key]), min(dict[key])))
            dict = defaultdict(list)
            cur = 0
            logging.getLogger(__name__).info("%s" % line[:-1])
        else:
            if linel[2] == 'elastic+':
                cur %= 2
                engine = 'elasticsearch'
            elif linel[2] == 'solr':
                cur %= 4
                engine = 'solr'
            type = ['virtual', 'physical', 'shared']
            for i in range(5, 8):
                # calculate in MB
                if 'g' in linel[i]: 
                    value = float(linel[i][:-1]) * 1024
                elif 'm' in linel[i]: 
                    value = float(linel[i][:-1])
                else:
                    value = int(linel[i]) / 1024
                if cur == 0:
                    dict[engine + "_" + type[i - 5]].append(value)
                else:
                    dict[engine + "_" + type[i - 5]][-1] += value
            cur += 1
    fp.close()
    for key in dict:
        logging.getLogger(__name__).info("%s Average, Max, Min: %.4f, %.4f, %.4f" % (key, sum(dict[key]) / len(dict[key]), max(dict[key]), min(dict[key])))


def analyse_query_hit():
    if not os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')):
        logging.getLogger(__name__).warning("/results directory does not exist. Please run query.py.")
        return
    file_names = ['elasticsearch_single_search', 'elasticsearch_multi_search_and', 'elasticsearch_multi_search_or',
                  'solr_single_search', 'solr_multi_search_and', 'solr_multi_search_or']
    for file_name in file_names:
        fp = open('results/' + file_name + ".txt", 'r')
        hit = 0
        for line in fp:
            linel = line[:-1].split(',')
            if 'single' in file_name:
                hit += min(10000, int(linel[2]))
            else:
                hit += min(10000, int(linel[3]))
        logging.getLogger(__name__).info("%s has hit: %d" % (file_name, hit))
        fp.close()

        
if __name__ == '__main__':
    main()

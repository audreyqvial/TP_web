
# coding: utf-8

import sys
import re
import numpy as np
import nltk as nltk
from nltk import SnowballStemmer
from parser import Parser
from simpleKB import SimpleKB
from page import Page

if len(sys.argv) > 1:
  yago_links = sys.argv[1]
  yago_label = sys.argv[2]
  wiki_input = sys.argv[3]
  output = sys.argv[4]
else:
  yago_links = "yago/yagoLinks.tsv" 
  yago_label = "yago/yagoLabels.tsv"
  wiki_input = "wikipedia-ambiguous.txt"
  output = "result.txt"

yago = SimpleKB(yago_links, yago_label)
stemmer = SnowballStemmer('english')

def get_goldenStandard(fileName):
    with open(fileName, encoding="utf-8") as file:
        print("Loading",fileName,end="...",flush=True)
        n_entities = 0
        golden_standard = {}
        for line in file:
            splitLine = line.split('\t')

            key = splitLine[0]
            value = splitLine[1].strip('"\n')
            if key not in golden_standard.keys():
                golden_standard[key] = value
                n_entities += 1
            else:
                golden_standard[key].append(value)
    file.close()
    return n_entities, golden_standard

def get_page_info(page):
    page_title = page.title
    page_content = page.content
    page_label = page.label()
    possible_label = yago.rlabels[page_label]
    possible_links = [yago.links[i] for i in possible_label]

    return page_title, page_content, page_label, possible_label, possible_links

def get_useful_rlabel(possible_label):
    useful_label = {}
    tkn = nltk.word_tokenize
    for lbl in possible_label:
        lbl1 = lbl.lower().replace('<',' ').replace('>',' ').replace('_',' ').replace('(','').replace(')','').replace(',','')  
        useful_label[lbl] = tkn(lbl1)
    return useful_label

def stem_data(doc): 
    path_stop = './english.stop'
    stop_words = open(path_stop).read().split('\n')
    punct = [';', ',', '.', '!', ':', '?', "(",")"]
    stop_words.extend(punct)
    all_stem = [stemmer.stem(text) for text in doc if text not in stop_words]

    return set(all_stem)


def pre_proc(content):
    path_stop = './english.stop'
    stop_words = open(path_stop).read().split('\n')
    punct = [';', ',', '.', '!', ':', '?', "(",")"]
    stop_words.extend(punct)
    tkn = nltk.word_tokenize
    list_content = tkn(content.lower())
    new_list_content = [i for i in list_content if i not in stop_words]
    if new_list_content:
        stem_content = stem_data(new_list_content)
        return new_list_content, stem_content
    else:
        return list_content, None



def get_useful_links(possible_links, possible_label, content):
    dict_links = {}
    tkn = nltk.word_tokenize
    for key, links in zip(possible_label,possible_links):
        list_link = []
        for el in links:
            el1 = el.lower().replace('<','').replace('>','').replace('_',' ')
            list_link.extend(tkn(el1))
        stem_link = stem_data(list_link)
        dict_links[key] = stem_link

    proc_content, proc_stem = pre_proc(content)
    dict_link_score = {}
    for k, v in dict_links.items():
        score = 0
        for s in proc_stem:
            if s in v:
                score += 2
            else:
                score -= 2
        dict_link_score[k] = score
    return dict_links, dict_link_score


def get_right_label(content, possible_label, possible_links):
    tkn = nltk.word_tokenize
    list_content = tkn(content.lower())
    useful_label = get_useful_rlabel(possible_label)
    dict_weight = {}
    if useful_label:
        for key, list_label in useful_label.items():
            weight = 0
            for lbl in list_label:
                if lbl in list_content:
                    weight += 1
                else:
                    weight -= 1
            dict_weight[key] = weight
        #print(dict_weight)
        value_weight = list(dict_weight.values())
        key_weight = list(dict_weight.keys())
        list_max = [i for i in value_weight if i==max(value_weight)]
        #from_possible_label = Counter(dict_weight)
        if len(list_max) > 1:
            _, dict_link_score = get_useful_links(possible_links, possible_label, content)
            #from_possible_link = Counter(dict_link_score)
            for k, v in dict_link_score.items():
                if k in dict_weight.keys():
                    dict_weight[k] += v
                else:
                    dict_weight[k] = v
            new_value_weight = list(dict_weight.values())
            new_key_weight = list(dict_weight.keys())
            #print(new_value_weight)
            return new_key_weight[new_value_weight.index(max(new_value_weight))]
        else:
            return key_weight[value_weight.index(max(value_weight))]
    else:
        return None
    

def get_result(wiki_input, output):
    with open(output, 'w', encoding="utf-8") as output:
        n_entities_wiki = 0
        for page in Parser(wiki_input):
            n_entities_wiki += 1
            page_title, page_content, page_label, possible_label, possible_links = get_page_info(page)
            matched_label = get_right_label(page_content, possible_label, possible_links)
            result = page.title+"\t"+matched_label+"\n"
            output.write(result)
    output.close()
    return n_entities_wiki


def get_score(filename, output):
    '''calculate the score to know how close we are from the golden standard'''
    n_golden, golden_standard = get_goldenStandard(filename)
    n_wiki, wiki_output = get_goldenStandard(output)
    golden_keys = set(golden_standard.keys())
    result_keys = set(wiki_output.keys())
    intersect_keys = golden_keys.intersection(result_keys)
    n_total = len(intersect_keys)
    print("intersect: ",n_total)
    count_ok = 0
    for k in intersect_keys:
        if wiki_output[k] == golden_standard[k]:
            count_ok += 1
    return count_ok*100.0/float(n_total)


if __name__ == '__main__':
  n_entities, golden_standard = get_goldenStandard("goldstandard-sample/goldstandard-sample.tsv")
  #print("le nb d\'entités trouvées dans le golden standard est: ", n_entities)
  #print(golden_standard)
  n_entities_wiki = get_result(wiki_input, output)
  print(' ')
  #print("le nb d\entrée wiki est: ", n_entities_wiki)output)
  score_final = get_score("goldstandard-sample/goldstandard-sample.tsv", output)
  print("score_final", score_final)




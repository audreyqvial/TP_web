
# coding: utf-8

'''Extracts type facts from a wikipedia file
usage: extractor.py wikipedia.txt output.txt

Every line of output.txt contains a fact of the form
    <title> TAB <type>
where <title> is the title of the Wikipedia page, and
<type> is a simple noun (excluding abstract types like
sort, kind, part, form, type, number, ...).

If you do not know the type of an entity, skip the article.
(Public skeleton code)'''

from parser import Parser
import sys
import nltk as nltk
import itertools
from page import Page

tag = nltk.pos_tag
tkn = nltk.word_tokenize

if len(sys.argv)!= 3:
    print(__doc__)
    sys.exit(-1)
else:
    wiki_input = sys.argv[1]
    output = sys.argv[2]

golden_standard = "gold-standard-sample.tsv"

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
    return page_title, page_content


def getPOS(list_token):
    return tag(list_token)


def pre_proc(content):
    path_stop = './english.stop'
    #stop_words = open(path_stop).read().split('\n')
    punct = [';', ',', '.', '!', ':', '?', "(",")"]
    list_relation = ["is a sort of", "is a kind of", "is a type of","is the sort of", "is the kind of", "is the type of" , "such as"]
    list_to_remove = ["word for","form of", "forms of", "part of", "range of"]
    if content:
        for i in list_relation:
            if i in content:
                content = content.replace(i,"is")
        for i in list_to_remove:
        	if i in content:
        		content = content.replace(i,"")
        #stop_words.extend(punct)
        tkn = nltk.word_tokenize
        list_content = tkn(content.lower())
        new_list_content = [i for i in list_content if i not in punct]
        if new_list_content:
            return new_list_content, getPOS(new_list_content)
        else:
            return None, None
    else:
        return None, None


def get_subpart(proc_content):
    pos_verb = ['VBZ', 'MD','VBD']
    list_index_verb = []
    if proc_content:
        #print(proc_content)
        for i, token in enumerate(proc_content):
            if token[1] in pos_verb:
                list_index_verb.append(i)
        list_of_list = []
        list_of_tag = []
        for i in range(len(list_index_verb)):
            #print(proc_content[i][1])
            v = list_index_verb[i]
            if list_index_verb[i] != list_index_verb[-1]:
                w = list_index_verb[i+1]
                list_of_list.append(proc_content[v:w])
                for tok in proc_content[v:w]:
                    list_of_tag.append(tok[1])
                #list_of_tag = [proc_content[i][1] for i in proc_content[v:w]]
            else:
                list_of_list.append(proc_content[v:])
                for tok in proc_content[v:]:
                    list_of_tag.append(tok[1])
                #list_of_tag = [proc_content[i][1] for i in proc_content[v:]]
        return list_of_list, list_of_tag
    else:
        return None, None


def get_pattern():
    pos_noun = ['NN','NNS','NNP','NNPS']
    tri = list(itertools.product(pos_noun,pos_noun,pos_noun))
    bi = list(itertools.product(pos_noun,pos_noun))
    list_bi = [[i,j] for (i,j) in bi]
    list_tri = [[i,j,k] for (i,j,k) in tri]
    return list_tri, list_bi


def find_pattern(list_of_tag):
    list_tri, list_bi = get_pattern()
    list_index_bi = []
    list_index_tri = []
    n = len(list_of_tag)
    index_of_tag = [i for i in range(len(list_of_tag))]
    for pos1, i in zip(list_of_tag, index_of_tag):
        if i <= n-2:
            pos2 = list_of_tag[i+1]
            pattern_bi = [pos1, pos2]
            if pattern_bi in list_bi:
                list_index_bi.append(i)
            
        if i <= n-3:
            pos2 = list_of_tag[i+1]
            pos3 = list_of_tag[i+2]
            pattern_tri = [pos1, pos2, pos3]
            if pattern_tri in list_tri:
                list_index_tri.append(i)

                
    return list_index_bi, list_index_tri


def extractType(page):
    '''si le token a un POS de nom, on regarde s'il est suivi d'un autre nom (ex: 'computer program') 
    ou d'un possessif (ex 'earth's atmosphere). Si c'est le cas, le nom qui suit obtient un score plus fort
    Si le nom apparait en premier après un verbe, sans qu'il soit suivi d'autre nom, il obtient un score plus fort
    si le token n'est pas un nom, il obtient un score negatif'''

    page_title, content = get_page_info(page)
    new_list_content, proc_content = pre_proc(content)
    if proc_content is None:
        return page_title, content, None, None 
    
    sub_part, sub_tag = get_subpart(proc_content)
         
    if sub_part is None:
        return page_title, content, None, None
    
    list_index_bi, list_index_tri = find_pattern(sub_tag)
    weight_test = {}
    pos_noun = ['NN','NNS','NNP','NNPS']
    list_to_exclude = ['sort', 'kind', 'part', 'form', 'type', 'sorts', 'kinds', 'parts', 'forms', 'types']
    for i, list_s in enumerate(sub_part):
        if list_s:
            n_list = len(list_s)
            for j, token in enumerate(list_s):                
                if token[0] not in weight_test.keys():
                    if (j in list_index_bi) and (j <= n_list-2):
                        word_plus1 = list_s[j+1]
                        weight_test[token[0]] = 2.0/float(j+i+20)
                        weight_test[word_plus2[0]] = 2.0/float(j+i+1)
                    if (j in list_index_tri) and (j <= n_list-3):
                        word_plus1 = list_s[j+1]
                        word_plus2 = list_s[j+2]
                        weight_test[token[0]] = 2.0/float(j+i+20)
                        weight_test[word_plus1[0]] = 2.0/float(j+i+10)
                        weight_test[word_plus2[0]] = 2.0/float(j+i+1)
                    if j <= n_list-3:
                        word_plus1 = list_s[j+1]
                        word_plus2 = list_s[j+2]                  
                        if (token[1] in pos_noun) and (word_plus1[1]=='POS') and (word_plus2[1] in pos_noun) and (word_plus2[0] not in list_to_exclude):#on regarde les possessifs
                            weight_test[token[0]] = 2.0/float(j+i+20)
                            weight_test[word_plus2[0]] = 2.0/float(j+i+1)

                    if (token[1] in pos_noun) and (token[0] not in list_to_exclude):
                        weight_test[token[0]] = 2.0/float(j+i+1)
                    else:
                        weight_test[token[0]] = -1.0/float(j+i+1)

                else:#le nom est déjà dans le dictionnaire et est déjà apparu en premier
                    if (token[1] in pos_noun) and (token[0] not in list_to_exclude):
                        weight_test[token[0]] += 1.0/float(j+i+30)
                    else:
                        weight_test[token[0]] -= 1.0/float(j+i+30)

    test_value_weight = list(weight_test.values())
    test_key_weight = list(weight_test.keys())
    if test_value_weight:

        return page_title, content, test_key_weight[test_value_weight.index(max(test_value_weight))], weight_test
    else:
        return page_title, content, None, None


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
    n_entities, goldenStandard = get_goldenStandard(golden_standard)
    print(n_entities)
    with open(output, 'w', encoding="utf-8") as f:
        for page in Parser(wiki_input):       
            title, content, typ, weight_test = extractType(page)
            if typ:
                f.write(title + "\t" + typ + "\n")
            if weight_test:
                print(content)
                print(weight_test)
                print(title, typ)
                print('-----------')
                print(' ')
    f.close()
    print("score %: ", get_score(golden_standard, output))



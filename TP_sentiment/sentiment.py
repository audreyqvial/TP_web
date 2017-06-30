import os
import csv as csv
import nltk as nltk
import re
import numpy as np
import pandas as pd
from collections import Counter
from IPython.display import display, HTML
from nltk.corpus import wordnet as wn
from sentiwordnet import SentiWordNetCorpusReader, SentiSynset

csvTweetData = '/home/audrey/Audrey/Cours/INF344/TP/TP_sentiment/testdata.manual.2009.06.14.csv'
colonne = ['Notes_tweet','Index','Date','Subject','Author','Tweet']
df1 = pd.read_csv(csvTweetData, sep=',', header=None)
df1.columns = colonne
print(df1.shape)
print(display(df1.iloc[0:10]))
N,_ = df1.shape

f = open('/home/audrey/Audrey/Cours/INF344/TP/TP_sentiment/dico_slang.txt')
slanglines = f.readlines()     
f.close()

list_slang = [x.replace('\t',' ').replace('\n','') for x in slanglines]
#print(list_slang[0].split())
#print(list_slang)
slang = [l.split()[0] for l in list_slang if l]
translate_slang = [' '.join(l.split()[1:]) for l in list_slang if l]
dico_slang = {}
for i,j in zip(slang,translate_slang):
    dico_slang[i] = j
print(dico_slang)

dico_tweet = {}
dico_tweet['Index'] = df1['Index'].tolist()
temp1 = []
temp2 = []
temp3 = []
destinataire = []
hashtag = []
RT = []
url = []
clean_tweet = []
for tweet in df1['Tweet']:
    m1 = re.findall('@(\w+)',tweet) #regex pour les destinataires
    m2 = re.findall('#(\w+)', tweet) #regex pour les hashtags
    m3 = re.findall('RT', tweet) #regex pour les retweets
    m4 = re.findall('(http(s?):\/\/)+([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?', tweet) #regex pour les urls
    if m1:
        temp1.append(m1)
        destinataire.extend(m1)
    else:
        temp1.append('Nan')
    if m2:
        temp2.append(m2)
        hashtag.extend(m2)
    else:
        temp2.append('Nan')
    if  m3:
        RT.extend(m3)
    if m4:
        m4 = ''.join(m4[0])
        temp3.append(m4)
        url.extend(m4)
    else:
        temp3.append('Nan')

    #on enlève tous les retweets
    t = re.sub('RT','', tweet)
    #on enlève les hashtags des tweets
    t = re.sub('#(\w+)','', t, flags = re.UNICODE)
    #on enlève les destinataires des tweets
    t = re.sub('@(\w+)','', t, flags = re.UNICODE)
    #on enlève les urls des tweets
    t = re.sub('(http(s?):\/\/)+([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?', '',t)
    # remplacer &amp; par &
    t = re.sub('&amp;',' and ',t)
    #regex pour enlever les caractères spéciaux ou la ponctuation
    t = re.sub("['/'|'...'|':'|'&'|','|';'|'.'|'!'|'--'|'_'|'*'|'-'|'``'|'?'|'//'|'+'|'='|'$'|'@'|'#'|'""']", ' ',t)
    clean_tweet.append(t)

dico_tweet['Destinataire'] = temp1
dico_tweet['hashtag'] = temp2
dico_tweet['url'] = temp3

#print(destinataire)
print(clean_tweet)

print('Nombre d\'url: ', len(url))
print('Nombre de hashtags: ', len(hashtag))
print('Nombre de destinataires différents: ', len(set(destinataire)))
print('Nombre de retweet: ', len(RT))
print(len(destinataire))

tkn = nltk.word_tokenize
words = [tkn(x) for x in clean_tweet]
print(words)

words_noslang = []
for w in words:
    for k,v in dico_slang.items():
        if k in w:
            #print(k)
            w = list(filter(lambda x: x!= k, w))
            w.append(v)
            #print(w)
    words_noslang.append(w) 
print(words_noslang)            

tag = nltk.pos_tag
tag_list_tot = []
tag_list = [tag(words_noslang[i]) for i in range(N)]
print(tag_list)
for i in range(N):
    tag_list_tot.extend(tag(words_noslang[i]))

tot_pos = [tag_list_tot[i][1] for i in range(len(tag_list_tot))]
count_VB = Counter(tot_pos)
print(count_VB)
verb_tag = ['VB', 'VBZ' , 'VBP', 'VBG', 'VBN', 'VBD']
sum_vb = 0
for k,v in  count_VB.items():
    if k in verb_tag:
        sum_vb += v
print('Le nombre total de POS verbes sur l\'ensemble des tweets est: ', sum_vb)

swn_filename = '/home/audrey/Audrey/Cours/INF344/TP/TP_sentiment/SentiWordNet_3.0.0_20130122.txt'
swn = SentiWordNetCorpusReader(swn_filename)
swn.senti_synset('breakdown.n.03')
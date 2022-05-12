# # NLP Pkgs
# import spacy 
# # nlp = spacy.load('en')
# nlp = spacy.blank("en")
# # Pkgs for Normalizing Text
# from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation
# # Import Heapq for Finding the Top N Sentences
# from heapq import nlargest





# def text_summarizer(raw_docx):
#     raw_text = raw_docx
#     docx = nlp(raw_text)
#     stopwords = list(STOP_WORDS)
#     # Build Word Frequency # word.text is tokenization in spacy
#     word_frequencies = {}  
#     for word in docx:  
#         if word.text not in stopwords:
#             if word.text not in word_frequencies.keys():
#                 word_frequencies[word.text] = 1
#             else:
#                 word_frequencies[word.text] += 1

#     maximum_frequncy = max(word_frequencies.values())

#     for word in word_frequencies.keys():  
#         word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
#     # Sentence Tokens
#     sentence_list = [sentence for sentence in docx.sents]

#     # Sentence Scores
#     sentence_scores = {}  
#     for sent in sentence_list:  
#         for word in sent:
#             if word.text.lower() in word_frequencies.keys():
#                 if len(sent.text.split(' ')) < 30:
#                     if sent not in sentence_scores.keys():
#                         sentence_scores[sent] = word_frequencies[word.text.lower()]
#                     else:
#                         sentence_scores[sent] += word_frequencies[word.text.lower()]


#     summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
#     final_sentences = [ w.text for w in summarized_sentences ]
#     summary = ' '.join(final_sentences)
#     return summary



from bs4 import element
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

import bs4
import urllib.request as url
import re
from nltk import sent_tokenize
from nltk import word_tokenize
import string
import time


def read_article(filedata):
    # file = open(file_name, "r", encoding='utf-8')
    # filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []

    for sentence in article:
        # print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))

    sentences.pop() 
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []

    sentences =  read_article(file_name)

    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    # print(ranked_sentence)
    for i in range(top_n):
        try :
            summarize_text.append(" ".join(ranked_sentence[i][1]))
        except IndexError :
            continue

    final_summerized_text = ". ".join(summarize_text)
    print("Summarize Text: \n", final_summerized_text)
    # with open('summerize_text.txt', "w", encoding='utf-8') as f :
    #         f.write(final_summerized_text)

    # print("Summarize Text: \n", ". ".join(summarize_text))

    return final_summerized_text


def write_to_file(file_name) :
    url_name = input('Enter the url of paragraph: ')
    if url_name.strip().lower() == 'no' :
        return
    web = url.urlopen(url_name)
    page = bs4.BeautifulSoup(web, 'html.parser')
    elements = page.find_all('p')
    article = ''
    for i in elements :
        article += (i.text)

    processed = article.replace(r'^\s+|\s+?$','')
    processed = processed.replace('\n',' ')
    processed = processed.replace("\\",'')
    processed = processed.replace(",",'')
    processed = processed.replace('"','')
    processed = re.sub(r'\[[0-9]*\]','',processed)

    with open(file_name, "w", encoding='utf-8') as f :
        f.write(processed)


def text_summarizer(raw_docx):
    return generate_summary(raw_docx, 7)


# f_name = 'file.txt'

# url_name = input('Enter the url of paragraph: ')
# web = url.urlopen(url_name)
# page = bs4.BeautifulSoup(web, 'html.parser')
# elements = page.find_all('p')
# article = ''
# for i in elements :
#     article += (i.text)

# processed = article.replace(r'^\s+|\s+?$','')
# processed = processed.replace('\n',' ')
# processed = processed.replace("\\",'')
# processed = processed.replace(",",'')
# processed = processed.replace('"','')
# processed = re.sub(r'\[[0-9]*\]','',processed)

# with open(f_name, "w", encoding='utf-8') as f :
#     f.write(processed)

# if we don't want to take input from the web using url we can comment the below line...


# write_to_file(f_name) # writing into file using web url
# time.sleep(1)
# generate_summary(f_name, 10)

# with open(f_name, "w") as f :
#     f.write('my name is atul')

# Coronaviruses are zoonotic, meaning they are transmitted between animals and people. Detailed investigations found that SARS-CoV was transmitted from civet cats to humans and MERS-CoV from dromedary camels to humans. Several known coronaviruses are circulating in animals that have not yet infected humans.Common signs of infection include respiratory symptoms, fever, cough, shortness of breath and breathing difficulties. In more severe cases, infection can cause pneumonia, severe acute respiratory syndrome, kidney failure and even death.Standard recommendations to prevent infection spread include regular hand washing, covering mouth and nose when coughing and sneezing, thoroughly cooking meat and eggs. Avoid close contact with anyone showing symptoms of respiratory illness such as coughing and sneezing.
 



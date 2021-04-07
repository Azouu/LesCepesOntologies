import mmap

from owlready2 import *
import os
import numpy as np
import gensim
from gensim.models import KeyedVectors

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict
import csv
import sys
import re
import pandas as pd




def read_nasari(source):
    nasari_vectors= {}
    with open(source, encoding="utf8") as src:
        for line in csv.reader(src, delimiter='\t', quoting=csv.QUOTE_NONE):
            nasari_vectors[line[0]] = line[1]
    #df = pd.DataFrame(data=nasari_vectors)
    #return df
    return nasari_vectors


def read_nasari2(source):
    nasari_vectors= {}
    with open(source, encoding="utf8") as src:
        for line in csv.reader(src, delimiter='\t', quoting=csv.QUOTE_NONE):
            nasari_vectors[line[0]] = line[2:]
    #df = pd.DataFrame(data=nasari_vectors)
    #return df
    return nasari_vectors

def flatten(liste) :
    flat_list = [item for sublist in liste for item in sublist]
    return flat_list

def getVectInId(listeVect,vect):
    for i in range(len(listeVect)):
        if listeVect[i] == vect:
            return i+1

            
    


def match2(id1,id2,dico1,dico2):
    #récuperation de la liste des vecteurs pour l'id1
    for id,listAll in dico1.items():
        if id == id1:
            listID1 = [w[:12] for w in listAll]
          
    
    #récuperation de la liste des vecteurs pour l'id2
    for id,listAll in dico2.items():
        if id == id2:
            listID2 = [w[:12] for w in listAll]

    
    #récupération de l'intersection des vecteurs (vecteurs commun aux 2) => O dans le pdf 
    list1set = set(listID1)
    intersection = list(list1set.intersection(listID2))
    
    top = 0
    bot = 0
    
    
    for i in range(len(intersection)):
        rangListe1 = getVectInId(listID1,intersection[i])
        rangListe2 = getVectInId(listID2,intersection[i])
        top += ((rangListe1 + rangListe2)**-1)
        bot += (2*i+1)**-1

            
    return (top / bot) if bot != 0 else top
        
        
        
        
        
    
    

if __name__ == '__main__':


    onto_path.append("./ont/fr/")
    onto_fr = get_ontology("conference-fr").load()
    onto_path.append("./ont/en/")
    onto_en = get_ontology("./conference-en").load()

    classes_fr = list(onto_fr.classes())
    classes_en = list(onto_en.classes())

    labels_fr = flatten([classe.label for classe in classes_fr])
    labels_en = flatten([classe.label for classe in classes_en])
    print(labels_fr)
    print(labels_en)



    french_nasari = read_nasari2('./nasaritest2.txt')
    print(match2("bn:00000004n","bn:00000005n",french_nasari,french_nasari))
    # english_nasari = read_nasari('./NASARI_unified_english.txt')


    # #terme = labels_fr[0]
    # terme = "Président"
    # # Chercher l'ID de president
    # bn = None
    # for id, title in french_nasari.items() :
    #     if title == terme :
    #         bn = id

    # print(bn)

    # translation = None
    # for id, title in english_nasari.items() :
    #     if id == bn :
    #         translation = title

    # print(translation)

    # for label in labels_en :
    #     if label.lower() == translation.lower() :
    #         print("OK")


    











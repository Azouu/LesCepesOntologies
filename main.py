import mmap

from owlready2 import *
import os
import numpy as np


from collections import defaultdict
import csv
import sys
import re
import pandas as pd

import nltk
import spacy



def read_nasari(source):
    nasari_id_title = {}
    nasari_id_vector = {}
    with open(source, encoding="utf8") as src:
        for line in csv.reader(src, delimiter='\t', quoting=csv.QUOTE_NONE):
            nasari_id_title[line[0]] = line[1]
            nasari_id_vector[line[0]] = {}
            dim_split = [dim.split("_") for dim in line[2:]]
            nasari_id_vector[line[0]] = {dim: float(score) for [dim, score] in dim_split}
    return nasari_id_title, nasari_id_vector




def flatten(liste) :
    flat_list = [item for sublist in liste for item in sublist]
    return flat_list

def getVectInId(listeVect,vect):
    for i in range(len(listeVect)):
        if listeVect[i] == vect:
            return i+1

def getSubject(string) :
    pass


def match2(id1, id2, dico1, dico2):
    # récuperation de la liste des vecteurs pour l'id1
    listID1 = list(dico1[id1].keys())

    # récuperation de la liste des vecteurs pour l'id2
    listID2 = list(dico2[id2].keys())


    # récupération de l'intersection des vecteurs (vecteurs commun aux 2) => O dans le pdf
    intersection = list(set(listID1) & set(listID2))

    top = 0
    bot = 0

    for i in range(len(intersection)):
        rangListe1 =  listID1.index(intersection[i]) + 1
        rangListe2 =  listID2.index(intersection[i]) + 1
        top += ((rangListe1 + rangListe2) ** -1)
        bot += (2 * (i+1)) ** -1

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



    french_nasari_IT, french_nasari_IV = read_nasari('./NASARI_unified_french.txt')
    english_nasari_IT, english_nasari_IV = read_nasari('./NASARI_unified_english.txt')

    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
    for token in doc:
        print(token.text)

    nlp = spacy.load('fr_core_news_sm')
    doc = nlp('Demain je travaille à la maison')
    sub_toks = {tok: tok.dep_ for tok in doc}
    print(sub_toks)


    nlp = spacy.load('en_core_web_sm')
    for sent in labels_en :
        doc = nlp(str(sent))
        sub_toks = {tok:tok.dep_ for tok in doc}
        print(sub_toks)

    nlp = spacy.load('fr_core_news_sm')
    for sent in labels_fr:
        doc = nlp(str(sent))
        sub_toks = {tok: tok.dep_ for tok in doc}
        print(sub_toks)

    # alignement sur les labels monotermes
    # sélection et pre-processing des termes
    labels_fr_mono = [label.lower() for label in labels_fr if len(label.split()) == 1 ]
    print(labels_fr_mono)

    #marche pas encore
    for id, title in french_nasari_IT.items():
        doc = nlp(str(title))
        sub_toks = {tok: tok.dep_ for tok in doc if tok.dep_ == labels_fr_mono[0]}
        print(sub_toks)

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





    











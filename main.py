import mmap

from owlready2 import *
import os
import numpy as np


from collections import defaultdict
import csv
import sys 
import re
import pandas as pd
from fuzzywuzzy import fuzz
import string
from xml.dom import minidom
from nltk.tag import StanfordPOSTagger


def setupStanford(pathToStan):
    stanford_dir = pathToStan
    modelfile = stanford_dir + "/models/french_ud.tagger"
    jarfile = stanford_dir+"/stanford-postagger.jar"
    
    

def getAlignementClass(source):
    listAlign = []
    xmldoc = minidom.parse(source)
    ent1 = xmldoc.getElementsByTagName('entity1')
    ent2 = xmldoc.getElementsByTagName('entity2')
    for i in range(len(ent1)):
        classe1 = ent1[i].attributes['rdf:resource'].value
        classe2 = ent2[i].attributes['rdf:resource'].value
        listAlign.append((formatforFinder(classe1),formatforFinder(classe2)))
    return listAlign


def getAlignementsLabels(classAlignement,lang1,lang2):
    listRes = []
    for c in classAlignement:
        listRes.append(findCouple(c,lang1,lang2))
    return listRes

def findOntInOWL(ont,classLang1,classLang2):
    idfind = 0
    for o in classLang1:
        if str(o) == ont.lstrip():
            return (classLang1[idfind].label)
        idfind = idfind + 1
        
    idfind = 0
    for o in classLang2:
        if str(o) == ont.lstrip():
            return (classLang2[idfind].label)
        idfind = idfind + 1
        
        
def findCouple(couple,ontLang1,ontLang2):
    return ((findOntInOWL(couple[0],ontLang1,ontLang2)),(findOntInOWL(couple[1],ontLang2,ontLang1)))
    

def formatforFinder(classe):
    return (classe[7:].replace("#",".")).replace("_","-")

            
        
    


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
        bot += (2 * i + 1) ** -1

    return (top / bot) if bot != 0 else top


        
        
def findOntInNASARI(ont,dico):
    
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    tmp = ' '.join(word for word in ont.translate(translator).split() if len(word)>3) 
    ontFin = tmp.split()
    tabScore = [0] * len(ontFin)
    tabTitle = [''] * len(ontFin)
    tabID = [0] * len(ontFin)
    print(ontFin) 
    
    for id,title in dico.items():
        for i in range(len(ontFin)) :
            curScore = fuzz.token_sort_ratio(ontFin[i],title)
            if (curScore > tabScore[i]):
                tabScore[i] = curScore
                tabTitle[i] = title
                tabID[i] = id
    return tabScore,tabTitle,tabID



    
            

if __name__ == '__main__':


    onto_path.append("./ont/fr/")
    onto_fr = get_ontology("conference-fr").load()
    onto_path.append("./ont/en/")
    onto_en = get_ontology("./conference-en").load()

    classes_fr = list(onto_fr.classes())
    classes_en = list(onto_en.classes())
    
    
    ref = getAlignementClass('conference-conference-en-fr.rdf')
    print(ref[2])
    refLab = getAlignementsLabels(ref, classes_fr, classes_en)
    print(refLab[2])
    
    
    

    labels_fr = flatten([classe.label for classe in classes_fr])
    labels_en = flatten([classe.label for classe in classes_en])
    print(labels_fr[4])
    print(labels_en)



    french_nasari_IT, french_nasari_IV = read_nasari('./NASARI_unified_french.txt')
    english_nasari_IT, english_nasari_IV = read_nasari('./NASARI_unified_english.txt')
    
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
    labels_fr_mono = [label for label in labels_fr if len(label.split()) == 1 ]
    labels_fr_multi = [label for label in labels_fr if len(label.split()) > 1 ]
    print(labels_fr_mono)

    dico_labels_mono = {}
    for label in labels_fr_mono :
        dico_labels_mono[label] = {id:title for id,title in french_nasari_IT.items() if remove_accents(label.lower()) in remove_accents(title.lower()) }

    print(dico_labels_mono)


    dico = {}
    for label in labels_en :
        dico[label] = [id for id,title in english_nasari_IT.items() if remove_accents(label.lower()) in remove_accents(title.lower()) ]

    # select label with the most common bn
    for tomatch in labels_fr_mono :
        matched = [label for label,bns in dico.items() if len(set(bns) & set(dico_labels_mono[tomatch].keys())) > 0]
        print(tomatch)
        print(matched)
        print()

    # Part-of speech fr to eng
    label_and_root_fr  = {}
    for label in labels_fr_multi :
        doc = nlp(str(label))
        tmp = [tok.text for tok in doc if tok.dep_ == 'ROOT']
        # Pour l'instant on fait que pour ceux qui ont une seule racine
        if len(tmp) == 1 :
            label_and_root_fr[label] = tmp[0]

    nlp_en =  spacy.load('en_core_web_sm')
    label_and_root_en  = {}
    for label in labels_en :
        doc = nlp_en(str(label))
        tmp = [tok.text for tok in doc if tok.dep_ == 'ROOT']
        # Pour l'instant on fait que pour ceux qui ont une seule racine
        if len(tmp) == 1:
            label_and_root_en[label] = tmp[0]

    print(label_and_root_en)
    dico_labels_multi_fr = {}

    for label, subject in label_and_root_fr.items() :
        dico_labels_multi_fr[label] = {id: title for id, title in french_nasari_IT.items() if
                                   remove_accents(subject.lower()) in remove_accents(title.lower())}


    dico_labels_eng = {}
    for label, subject in label_and_root_en.items() :
        dico_labels_eng[label] = [id for id,title in english_nasari_IT.items() if remove_accents(subject.lower()) in remove_accents(title.lower()) ]

    #Essai sur les 5 premiers labels
    tmp = list(dico_labels_multi_fr.keys())
    for i in range(5) :
        tomatch  = tmp[i]
        matched = [label for label, bns in dico_labels_eng.items() if
                       len(set(bns) & set(dico_labels_multi_fr[tomatch].keys())) > 0]
        print(tomatch)
        print(matched)
        print()

    











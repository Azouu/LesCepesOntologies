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

def flatten(liste) :
    flat_list = [item for sublist in liste for item in sublist]
    return flat_list

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



    french_nasari = read_nasari('./NASARI_unified_french.txt')
    english_nasari = read_nasari('./NASARI_unified_english.txt')

    #terme = labels_fr[0]
    terme = "Président"
    # Chercher l'ID de president
    bn = None
    for id, title in french_nasari.items() :
        if title == terme :
            bn = id

    print(bn)

    translation = None
    for id, title in english_nasari.items() :
        if id == bn :
            translation = title

    print(translation)

    for label in labels_en :
        if label.lower() == translation.lower() :
            print("OK")












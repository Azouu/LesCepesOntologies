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




def read_nasari(source):
    nasari_vectors= {}
    with open(source, encoding="utf8") as src:
        for line in csv.reader(src, delimiter='\t', quoting=csv.QUOTE_NONE):
            nasari_vectors[line[0]] = line[1]
    return nasari_vectors

if __name__ == '__main__':


    onto_path.append("./ont/fr/")
    onto_fr = get_ontology("conference-fr").load()
    onto_path.append("./ont/en/")
    onto_en = get_ontology("./conference-en").load()

    classes_fr = list(onto_fr.classes())
    classes_en = list(onto_en.classes())

    labels_fr = [classe.label for classe in classes_fr]
    labels_en = [classe.label for classe in classes_en]
    print(labels_fr)
    print(labels_en)

    president = labels_fr[0]

    #with open('./NASARI_lexical_french.txt', encoding="utf8") as file :
    print(read_nasari('./NASARI_unified_french.txt'))











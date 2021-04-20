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

import unicodedata

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
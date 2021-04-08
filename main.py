import mmap

from owlready2 import *
import os
import numpy as np


from collections import defaultdict
import csv
import sys
import re
import pandas as pd




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

    print(match2("bn:00000002n","bn:00000002n",french_nasari_IV,french_nasari_IV))
    print(french_nasari_IT["bn:00000002n"])
    print(english_nasari_IT["bn:00000002n"])
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


    











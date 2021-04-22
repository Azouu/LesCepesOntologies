import mmap

from owlready2 import *
from googletrans import Translator
import editdistance
import spacy
from deep_translator import GoogleTranslator

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

    dico = {}
    preprocessed_labels = [label + " conférence" for label in labels_fr]
    for label, preprocessed_label in zip(labels_fr, preprocessed_labels) :
        dico[label] = GoogleTranslator(source='fr', target='en').translate(preprocessed_label)



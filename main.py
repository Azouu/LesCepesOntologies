
import spacy
import utils
from OntologyReader import OntologyReader
from NasariReader import NasariReader
from fuzzywuzzy import fuzz
import string
from xml.dom import minidom

import string
from xml.dom import minidom

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

    ontology_name = 'conference'
    source_language = 'fr'
    target_language = 'en'

    onto_reader = OntologyReader(ontology_name, source_language, target_language)

    # ref = getAlignementClass('ref/en-fr/conference-conference-en-fr.rdf')
    # print(ref[2])
    # refLab = getAlignementsLabels(ref, onto_reader.getClassLabels('source'), onto_reader.getClassLabels('target'))
    # print(refLab[2])

    source_nasari = NasariReader('NASARI_unified_french.txt', 'fr')
    target_nasari = NasariReader('NASARI_unified_english.txt', 'en')

    source_class_labels = onto_reader.getClassLabels('source')
    target_class_labels = onto_reader.getClassLabels('target')

    source_dict = { label : source_nasari.getBNForString(label) for label in source_class_labels }
    target_dict = { label : target_nasari.getBNForString(label) for label in target_class_labels }

    dico_nasari_score = {}
    for source_label in source_class_labels :
            matched = [target_label for target_label in target_class_labels if  len(set(source_dict[source_label]) & set(target_dict[target_label])) > 0]
            dico_nasari_score[source_label] = {target_label: len(set(source_dict[source_label]) & set(target_dict[target_label])) for target_label in matched}

    dico = {}
    for target_label in target_class_labels :
        dico[target_label] = len([x for x in dico_nasari_score.keys() if target_label in dico_nasari_score[x].keys()])

    threshold = 0.7
    to_remove = [v for v,x in dico.items() if x / len(target_class_labels) > threshold]
    print(to_remove)

    for source_label in source_class_labels:
        intersect = set(dico_nasari_score[source_label]) & set(to_remove)
        for l in intersect :
            dico_nasari_score[source_label].pop(l,None)

    my_dictionary = {}
    for source_label in source_class_labels :
        my_dictionary[source_label] = {k: v/sum(dico_nasari_score[source_label].values()) for k, v in dico_nasari_score[source_label].items()}




















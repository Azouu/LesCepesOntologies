
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

    ontology_name = 'conference'
    source_language = 'fr'
    target_language = 'en'

    onto_reader = OntologyReader(ontology_name, source_language, target_language)

    ref = getAlignementClass('conference-conference-en-fr.rdf')
    print(ref[2])
    refLab = getAlignementsLabels(ref, onto_reader.getClassLabels('source'), onto_reader.getClassLabels('target'))
    print(refLab[2])

    source_nasari = NasariReader('NASARI_unified_french.txt', 'fr')
    target_nasari = NasariReader('NASARI_unified_english.txt', 'en')

    source_class_labels = onto_reader.getClassLabels('source')
    target_class_labels = onto_reader.getClassLabels('target')

    source_dict = { label : source_nasari.getBNForString(label) for label in source_class_labels }
    target_dict = { label : target_nasari.getBNForString(label) for label in target_class_labels }

    dico_nasari_score = {}
    for source_label in source_class_labels :
            matched = [target_label for target_label in target_class_labels if  len(set(source_dict[source_label]) & set(target_dict[target_label])) > 0]
            #tmp = [1/(len(target_label.split()) * len(target_dict[target_label])) for target_label in matched]
            print(source_label)
            print(matched)
            print()
















import mmap

from owlready2 import *
from googletrans import Translator
import editdistance
import spacy
from deep_translator import GoogleTranslator
from nltk.tokenize import word_tokenize
import Levenshtein
from nltk.corpus import stopwords
import numpy as np
from AlignmentReader import *
from OntologyReader import *
from ranking import *
from NasariReader import *
import pandas as pd
import itertools
from sklearn.linear_model import Perceptron
import sklearn
from sklearn.metrics import accuracy_score

def flatten(liste) :
    flat_list = [item for sublist in liste for item in sublist]
    return flat_list


def stringSimLevenshtein(label,translation): 
    listeComp = []
    #tokenization of the translation
    tokTrans = word_tokenize(translation)
    #suppression of stopwords
    tokTrans = [word for word in tokTrans if not word in stopwords.words()]
    
    #tokenization of label
    tokLab = word_tokenize(label)
    #suppression of stopwords
    tokLab = [word for word in tokLab if not word in stopwords.words()]
    
    #evaluation of levenshtein distance for each token of each labels
    for tt in tokTrans:
        for tl in tokLab:
            listeComp.append(Levenshtein.distance(tt,tl))
            
    #returns the mean of levensthein distances between all tokens
    return np.mean(listeComp)

def stringSim1Trans(labels,translation,dicoTrans):
    listeRes = {}
    dico = {}
    val_list = list(dicoTrans.values())
    key_list = list(dicoTrans.keys())
    #for each labels of the targetted ontology
    for lab in labels: 
        #uses the function above to get the mean of levenshtein distance
        sim = stringSimLevenshtein(lab.lower(), translation.lower())
        #penalise labels if too much difference in length or if conference in label to avoid matching with conference all the time
        if(len(lab) > 2*len(translation) or len(translation) > 2*len(lab) or "conference" in lab.lower()):
              sim = sim+1
        dico[lab] = sim   
    #returns the couple where the levenshtein distance is minimal
    pos = val_list.index(translation)
    listeRes[key_list[pos]] = dico
    return listeRes

def stringSim(lab,dicoTrans):
    finalDico = {}
    for trans in dicoTrans.values():
        finalDico.update(stringSim1Trans(labels_en,trans,dicoTrans))
    return finalDico


def nasariSim():
    ontology_name = 'conference'
    source_language = 'fr'
    target_language = 'en'

    onto_reader = OntologyReader(ontology_name, source_language, target_language)

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


    for source_label in source_class_labels:
        intersect = set(dico_nasari_score[source_label]) & set(to_remove)
        for l in intersect :
            dico_nasari_score[source_label].pop(l,None)

    my_dictionary = {}
    for source_label in source_class_labels :
        my_dictionary[source_label] = {k: v/sum(dico_nasari_score[source_label].values()) for k, v in dico_nasari_score[source_label].items()}

    return(my_dictionary)
            
def combineFeatures(stringFeatures,nasariFeatures):

    keys = list(stringFeatures.keys())
    vals = list(stringFeatures.values())
    allMatch = list(vals[0].keys())
    
    n = 2
    features = np.ndarray((len(keys),len(allMatch),n))
    
    for i in range(len(keys)):
        for j in range(len(allMatch)):                
                if(allMatch[j] not in nasariFeatures[keys[i]]):
                    valNasari = 0
                else:
                    valNasari = nasariFeatures[keys[i]][allMatch[j]]
                valString = stringFeatures[keys[i]][allMatch[j]]
                features[i][j][0] = valString
                features[i][j][1] = valNasari
    features = features.reshape(len(keys)*len(allMatch),n)
    return features               
         

if __name__ == '__main__':

    onto_path.append("./ont/fr/")
    onto_fr = get_ontology("conference-fr").load()
    onto_path.append("./ont/en/")
    onto_en = get_ontology("./conference-en").load()

    classes_fr = list(onto_fr.classes()) 
    classes_en = list(onto_en.classes())

    labels_fr = flatten([classe.label for classe in classes_fr])
    labels_en = flatten([classe.label for classe in classes_en])
    
    uniqLabFR = list(dict.fromkeys(labels_fr))
   
    uniqLabEN = list(dict.fromkeys(labels_en))
    
    #Reading reference alignement from file named alig.rdf and turns it into a DataFrame
    alig = AlignmentReader("conference","conference","en","fr")
    alig.getAlignementClass()
    alig.getAlignementsLabels()
    yLabels = alig.binaryAligForSVM()
    yLabels = yLabels.reshape((len(uniqLabFR)*len(uniqLabEN)))
    listeToPass = list(itertools.product(uniqLabEN,uniqLabFR))
    listeToPass = [(y, x) for x, y in listeToPass]
    Y = pd.DataFrame([yLabels],columns=listeToPass)
    Y = Y.transpose()
    #the dataframe returned has one binary column : 
    #1 = there is an alignement between the 2 labels
    #0 = there is no alignement between the 2 labels
    #The rows are every possible couple of labels (l1,l2) from the 2 ontologies
    

    
    #FR to EN translation
    dico = {}
    preprocessed_labels = []
    for label in labels_fr:
        if "Conférence" in label or "conférence" in label:
            preprocessed_labels.append(label)
        else :
            preprocessed_labels.append(label + " conférence")
    
    for label, preprocessed_label in zip(labels_fr, preprocessed_labels) :
        dico[label] = GoogleTranslator(source='fr', target='en').translate(preprocessed_label)
        
        
    #getting features from NASARI Similarity and String Similarity 
    
    # for string features the format is a dictionnary with : 
    # keys = French Label 
    # values = another dictionnary with :
        # keys = English Label
        # values = mean of levenshtein distance between each words
    stringFeatures = stringSim(labels_en,dico)
    
    # for NASARI features the format is a dictionnary with :
    # keys = French Label 
    # values = another dictionnary with :
        # keys = English Label
        # values = similarity calculated with NASARI vectors
    nasariFeatures = nasariSim()
    
    # combining the feature into a single array with :
    # column 1 = string similarity
    # column 2 = nasari similarity
    X = combineFeatures(stringFeatures,nasariFeatures)
    
    # putting the combined features into a DataFrame for clearer row names
    # names are now the couple of labels from the 2 ontologies
    X_pd = pd.DataFrame(X,columns = ["string sim","nasari sim"],index = 
                        list(itertools.product(uniqLabFR,uniqLabEN)))
    
    # adding labels from reference alignement to the dataframe
    df = X_pd.join(Y)
    
    #prepare data for the perceptron with 80% of data for training 
    #and 20% for testing
    X_train = df.sample(frac=0.8,random_state=100)
    X_test = df.drop(X_train.index)
    
    y_train = X_train.drop(X_train.columns[[0,1]],axis=1)
    y_test = X_test.drop(X_test.columns[[0,1]],axis=1)
    X_train = X_train.drop(X_train.columns[[2]],axis=1)
    X_test = X_test.drop(X_test.columns[[2]],axis=1)
    
    
    ####PERCEPTRON####
    sc = sklearn.preprocessing.StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)
    
    n_iter = 40
    eta0 = 0.1
    
    #create perceptron instance
    ppn = Perceptron(max_iter=n_iter,eta0=eta0,random_state=100)
    
    #fit the model
    ppn.fit(X_train_std,y_train.values.ravel())
    
    #make predictions
    y_pred = ppn.predict(X_test_std)
    
    
    #measure results
    print("accuracy =",accuracy_score(y_test,y_pred))
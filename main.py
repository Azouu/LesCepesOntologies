import sklearn
from deep_translator import GoogleTranslator
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_validate
from AlignmentReader import *
from OntologyReader import *
from NasariReader import *
import pandas as pd
import itertools
from sklearn.linear_model import Perceptron
from SimilarityCalculator import *
import warnings
warnings.filterwarnings('always')

def combineFeatures(stringFeatures,nasariFeatures, n=2):

    keys = list(stringFeatures.keys())
    vals = list(stringFeatures.values())
    allMatch = list(vals[0].keys())
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

    source_ontology_name = 'conference'
    target_ontology_name = source_ontology_name
    source_language_domain = 'conférence'
    source_language = 'fr'
    target_language = 'en'
    number_cross_validation = 3
    source_nasari = NasariReader('NASARI_unified_french.txt', source_language)
    target_nasari = NasariReader('NASARI_unified_english.txt', target_language)

    onto_reader = OntologyReader(source_ontology_name, source_language, target_language)

    source_class_labels = onto_reader.getClassLabels('source')
    target_class_labels = onto_reader.getClassLabels('target')
    
    source_uniqLab = list(dict.fromkeys(source_class_labels))
   
    target_uniqLab = list(dict.fromkeys(target_class_labels))
    
    #Reading reference alignement from file named alig.rdf and turns it into a DataFrame
    alig = AlignmentReader(source_ontology_name, target_ontology_name,target_language,source_language)
    alig.getAlignementClass()
    alig.getAlignementsLabels()
    yLabels = alig.binaryAligForSVM()
    yLabels = yLabels.reshape((len(source_uniqLab)*len(target_uniqLab)))
    listeToPass = list(itertools.product(target_uniqLab,source_uniqLab))
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
    for label in source_class_labels:
        if source_language_domain in label.lower():
            preprocessed_labels.append(label)
        else :
            preprocessed_labels.append(label + " " + source_language_domain)
    
    for label, preprocessed_label in zip(source_class_labels, preprocessed_labels) :
        dico[label] = GoogleTranslator(source=source_language, target=target_language).translate(preprocessed_label)
        
        
    #getting features from NASARI Similarity and String Similarity 
    similarity_calculator = SimilarityCalculator()
    # for string features the format is a dictionnary with : 
    # keys = French Label 
    # values = another dictionnary with :
        # keys = English Label
        # values = mean of levenshtein distance between each words
    stringFeatures = similarity_calculator.stringSim(dico, target_class_labels)
    
    # for NASARI features the format is a dictionnary with :
    # keys = French Label 
    # values = another dictionnary with :
        # keys = English Label
        # values = similarity calculated with NASARI vectors
    nasariFeatures = similarity_calculator.nasariSim(source_class_labels, target_class_labels, source_nasari, target_nasari)
    
    # combining the feature into a single array with :
    # column 1 = string similarity
    # column 2 = nasari similarity
    X = combineFeatures(stringFeatures,nasariFeatures)
    
    # putting the combined features into a DataFrame for clearer row names
    # names are now the couple of labels from the 2 ontologies
    X_pd = pd.DataFrame(X,columns = ["string sim","nasari sim"],index = 
                        list(itertools.product(source_uniqLab,target_uniqLab)))
    
    # adding labels from reference alignement to the dataframe
    df = X_pd.join(Y)
    
    #prepare data for the perceptron with 80% of data for training 
    #and 20% for testing
    X_train = df.sample(frac=0.8,random_state=100)
    X_test = df.drop(X_train.index)

    y = df.drop(df.columns[[0,1]],axis=1)
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

    # measure results
    print('Test on one set (80/20):')
    print("accuracy =", accuracy_score(y_test, y_pred))
    print("precision =", precision_score(y_test,y_pred))
    print("recall =", recall_score(y_test,y_pred))
    print("f-score =", f1_score(y_test,y_pred))

    scoring = ['precision_macro', 'recall_macro', 'f1_macro']
    scores = cross_validate(ppn, X, Y.to_numpy().flatten(), cv=number_cross_validation, scoring=scoring)

    #measure results
    print("average precision =", scores['test_precision_macro'].mean())
    print("average recall =", scores['test_recall_macro'].mean())
    print("average f-score =", scores['test_f1_macro'].mean())

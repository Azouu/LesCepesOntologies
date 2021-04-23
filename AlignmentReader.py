from fuzzywuzzy import fuzz
import string
from xml.dom import minidom
from OntologyReader import *
from sklearn.model_selection import train_test_split
import numpy as np

class AlignmentReader :
    def __init__(self, ontology1_name:str,ontology2_name:str, lang1:str, lang2:str):
        self.ontology1_name = ontology1_name
        self.ontology2_name = ontology2_name
        self.lang1 = lang1
        self.lang2 = lang2
        
        self.path = ontology1_name + "-" + ontology2_name + "-" + lang1 + "-" + lang2 + ".rdf"
        
        self.aligIDs = []
        self.aligLabels = []
        
        self.ont1 = OntologyReader(ontology1_name,lang1,lang2)
        self.ont2 = OntologyReader(ontology2_name,lang1,lang2)
                                   
    
    def findInAlig(self,ont):
        for i in range(len(self.aligLabels)):
            if (self.aligLabels[i][0] == [ont]) or (self.aligLabels[i][1] == [ont]):
                return(self.aligLabels[i])
           
        
    #function to get an array of 0 and 1 to say if an alignement between
    #the two labels exists in the reference alignement
    def binaryAligForSVM(self):
        lab1 = self.ont1.getClassLabels("source")
        lab2 = self.ont2.getClassLabels("target")
        lab1 = list(dict.fromkeys(lab1))
        lab2 = list(dict.fromkeys(lab2))
        res = np.ndarray((len(lab1),len(lab2)))
        for o in range(len(lab1)):
            for o2 in range(len(lab2)):
                
                if(self.findInAlig(lab1[o])[1] == [lab2[o2]]):

                    res[o][o2] = 1
                else:
                    res[o][o2] = 0
        return res                    
                    
                
        
    
    
    #returns an array of couples with the IDs of the ontology aligned in the
    #ref alignement
    def getAlignementClass(self):
        listAlign = []
        xmldoc = minidom.parse(self.path)
        ent1 = xmldoc.getElementsByTagName('entity1')
        ent2 = xmldoc.getElementsByTagName('entity2')
        for i in range(len(ent1)):
            classe1 = ent1[i].attributes['rdf:resource'].value
            classe2 = ent2[i].attributes['rdf:resource'].value
            listAlign.append((self.formater(classe1),self.formater(classe2)))
        self.aligIDs = listAlign
  
    #returns an array of couples with the labels of the ontology aligned in the
    #ref alignement
    def getAlignementsLabels(self):
        listRes = []
        for c in self.aligIDs:
            listRes.append(self.findCouple(c,self.lang1,self.lang2))
        self.aligLabels = listRes
        
    def samplePicker(self):
        X_train, X_test, y_train, y_test = train_test_split(self.aligLabels)
        
        
        
    #########################################################################
        
    def formater(self,classe):
        return (classe[7:].replace("#",".")).replace("_","-")
    
    def findOntInOWL(self,ont,class1,class2):
        idfind = 0
        for o in self.ont1.getClasses("source"):
            if str(o) == ont.lstrip():
                return (self.ont1.getClasses("source")[idfind].label)
            idfind = idfind + 1
    
        idfind = 0
        for o in self.ont2.getClasses("target"):
            if str(o) == ont.lstrip():
                return (self.ont2.getClasses("target")[idfind].label)
            idfind = idfind + 1
            
    def findCouple(self,couple,lang1,lang2):
        return ((self.findOntInOWL(couple[0],self.ont1.getClassLabels,self.ont2.getClassLabels)),(self.findOntInOWL(couple[1],self.ont2.getClassLabels,self.ont1.getClassLabels)))
from owlready2 import *
from utils import flatten

class OntologyReader :

    def __init__(self, ontology_name:str, source_language:str, target_language:str):
        self.ontology_name = ontology_name
        self.source_language = source_language
        self.target_language = target_language

        source_path = "./ont/" + source_language + "/"
        onto_path.append(source_path)
        source_name = ontology_name + "-" + source_language
        self.source_ontology = get_ontology(source_name).load()

        target_path = "./ont/" + target_language
        onto_path.append(target_path)
        target_name = ontology_name + "-" + target_language
        self.target_ontology = get_ontology(target_name).load()


    def getClasses (self, ontology_label:str) :
        if ontology_label == 'source' :
            return list(self.source_ontology.classes())
        elif ontology_label == 'target' :
            return list(self.target_ontology.classes())

    def getClassLabels(self, ontology_label:str) :
        return flatten([classe.label for classe in self.getClasses(ontology_label)])







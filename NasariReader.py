import csv
from utils import is_substring
import spacy

class NasariReader :

    def __init__(self, filepath, language):
        self.filepath = filepath
        self.language = language
        self.dictionnary = self.readNasariUnified(filepath)
        if self.language == 'en' or self.language =='english' :
            self.nlp = spacy.load('en_core_web_sm')
        elif self.language == 'fr' or self.language == 'french' :
            self.nlp = spacy.load('fr_core_news_sm')

    def readNasariUnified(self, source):
        dictionnary_id_title = {}
        with open(source, encoding="utf8") as src:
                for line in csv.reader(src, delimiter='\t', quoting=csv.QUOTE_NONE):
                    dictionnary_id_title[line[0]] = line[1]
                    # nasari_id_vector[line[0]] = {}
                    # dim_split = [dim.split("_") for dim in line[2:]]
                    # nasari_id_vector[line[0]] = {dim: float(score) for [dim, score] in dim_split}
        return dictionnary_id_title

    def getBNForString(self, string):
        if len(string.split()) == 1 :
            return [id for id,title in self.dictionnary.items() if is_substring(string,title)]
        else :
            processed_string = str(string)
            doc = self.nlp(processed_string)
            subject = [tok.text for tok in doc if tok.dep_ == 'ROOT'][0] # nominal sentences and take only one root
            return [id for id, title in self.dictionnary.items() if is_substring(subject,title)]





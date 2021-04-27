# Overview 
This system is a cross-lingual ontology matching system that performs matching on two ontologies in OWL format. For now it performs matching on class labels.
It is designed as running `main.py` after an initial system tuning (see apropriate section).
For now the system performs matching on ontologies of the same domain in french and english. To add a language see the System Tuning section et the Note section.
The systems returns first the precision, recall, and f1-score after a 80/20 split of the labels pairs.
Then it performs cross-validation and returns the average for each metric.
The system only uses 2 features : string similarity using levenshtein distance, and a nasari similarity metric.
The system can be highly improved for now. 
# Dependencies
* owlready2 0.29
* spacy 3.0.5
* deep-translator 1.4.2
* scikit-learn 0.24.1
* pandas 1.2.3
* nltk 3.5
Please note that in order to use NLTK correctly, you have to run the following commands in your Python Console before starting the program :
```
import nltk
nltk.download('stopwords')
```
```
import nltk
nltk.download('word_tokenize')
```
Or you can simply run the following commands in your terminal :
```
python -m nltk.downloader stopwords
python -m nltk.downloader word_tokenize
```
* NASARI : http://lcl.uniroma1.it/nasari/

# How to setup the directory
The default setup directory is :
* A folder with the name `ont/` containing folders with the language initials. Please make sure you use the same initials as for the system's parameters tuning. 
* A reference alignement file in RDF format with the name format `<source_ontology_name>-<target_ontology_name>-<source_language_initials>-<target_language_initials>
* Two NASARI unified .txt files in the desired languages. You can download them at NASARI.

* System tuning :
The system is currently parametered to run on the Conference Ontology of the Mutltifarm dataset (see https://www.irit.fr/recherches/MELODI/multifarm/ ), matching between english and french ontologies.
However, if you want to tune the system, go to `main.py` file and change the parameters from line 35. 
The two ontologies of a pair are identified by the labels source and target in the code.
Parameters are :
* `source_ontology_name`
*  `target_ontology_name`
* `source_language_domain` : name of the domain on an ontology in the source language
* source_language : initials of the source language ('fr','en')
* target_language 
* number_cross_validation
Please use the initials of the folders in the ont/ folder as source_language or target_language content.
Make sure they fit with the spacy languages, see https://spacy.io/usage/models .
If you want to add a language, go to `NasariReader.py` and add the corresponding lines of codes to using the information in https://spacy.io/usage/models : 
`
        if self.language == 'en' or self.language =='english' :
            self.nlp = spacy.load('en_core_web_sm')
        elif self.language == 'fr' or self.language == 'french' :
            self.nlp = spacy.load('fr_core_news_sm')
 `
* source_nasari and target_nasari : file name of the NASARI_unified files in the main folder.

# Note 
The system can only perform ontology matching on ontologies of languages that have an appropriate NASARI_unified file.

# Credits 
Université Paul Sabatier - Toulouse

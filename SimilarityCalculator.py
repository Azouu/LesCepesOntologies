from nltk.tokenize import word_tokenize
import Levenshtein
from nltk.corpus import stopwords
import numpy as np

class SimilarityCalculator :

    def stringSimLevenshtein(self,label, translation):
        listeComp = []
        # tokenization of the translation
        tokTrans = word_tokenize(translation)
        # suppression of stopwords
        tokTrans = [word for word in tokTrans if not word in stopwords.words()]

        # tokenization of label
        tokLab = word_tokenize(label)
        # suppression of stopwords
        tokLab = [word for word in tokLab if not word in stopwords.words()]

        # evaluation of levenshtein distance for each token of each labels
        for tt in tokTrans:
            for tl in tokLab:
                listeComp.append(Levenshtein.distance(tt, tl))

        # returns the mean of levensthein distances between all tokens
        return np.mean(listeComp)

    def stringSim1Trans(self, labels, translation, dicoTrans):
        listeRes = {}
        dico = {}
        val_list = list(dicoTrans.values())
        key_list = list(dicoTrans.keys())
        # for each labels of the targetted ontology
        for lab in labels:
            # uses the function above to get the mean of levenshtein distance
            sim = self.stringSimLevenshtein(lab.lower(), translation.lower())
            # penalise labels if too much difference in length or if conference in label to avoid matching with conference all the time
            if (len(lab) > 2 * len(translation) or len(translation) > 2 * len(lab) or "conference" in lab.lower()):
                sim = sim + 1
            dico[lab] = sim
            # returns the couple where the levenshtein distance is minimal
        pos = val_list.index(translation)
        listeRes[key_list[pos]] = dico
        return listeRes

    def stringSim(self, dicoTrans, target_class_labels):
        finalDico = {}
        for trans in dicoTrans.values():
            finalDico.update(self.stringSim1Trans(target_class_labels, trans, dicoTrans))
        return finalDico

    def nasariSim(self, source_class_labels, target_class_labels, source_nasari, target_nasari, threshold=0.7):
        source_dict = {label: source_nasari.getBNForString(label) for label in source_class_labels}
        target_dict = {label: target_nasari.getBNForString(label) for label in target_class_labels}
        # compute dictionnary with the form {label_source : label_target : <number of bn ids in common>}
        dico_nasari_score = {}
        for source_label in source_class_labels:
            matched = [target_label for target_label in target_class_labels if
                       len(set(source_dict[source_label]) & set(target_dict[target_label])) > 0]
            dico_nasari_score[source_label] = {
                target_label: len(set(source_dict[source_label]) & set(target_dict[target_label])) for target_label in
                matched}
        # remove target labels from every key if they appear too many times (remove noise)
        dico = {}
        for target_label in target_class_labels:
            dico[target_label] = len(
                [x for x in dico_nasari_score.keys() if target_label in dico_nasari_score[x].keys()])
        to_remove = [v for v, x in dico.items() if x / len(target_class_labels) > threshold]
        for source_label in source_class_labels:
            intersect = set(dico_nasari_score[source_label]) & set(to_remove)
            for l in intersect:
                dico_nasari_score[source_label].pop(l, None)
        # compute dictionnary with the forme {label : score}
        dict_scores = {}
        for source_label in source_class_labels:
            dict_scores[source_label] = {k: v / sum(dico_nasari_score[source_label].values()) for k, v in
                                         dico_nasari_score[source_label].items()}
        return (dict_scores)

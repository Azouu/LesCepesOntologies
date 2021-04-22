import unicodedata

### STRING PRE-PROCESSING ####
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

def is_substring(source, target) :
    return remove_accents(source.lower()) in remove_accents(target.lower())

### LIST UTILS ###
def flatten(liste) :
    flat_list = [item for sublist in liste for item in sublist]
    return flat_list
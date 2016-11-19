import spacy

en_nlp = spacy.load('en')

def get_speech_tags(text):
    doc = en_nlp(text.decode('utf-8'))
    nouns = []
    verbs = []
    adjectives = []
    comperatives = []
    for word in doc:
        if word.tag_.startswith('NN'):
            nouns.append(word)
        elif word.tag_.startswith('VB'):
            verbs.append(word)
        elif word.tag_ == 'JJ':
            adjectives.append(word)
        elif word.tag_ == 'JJR' or word.tag_ == 'RBR':
            comperatives.append(word)
    return {'nouns':nouns, 'verbs':verbs, 'adjectives':adjectives, 'comperatives':comperatives}


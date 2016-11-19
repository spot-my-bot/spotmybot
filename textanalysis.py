import spacy

en_nlp = spacy.load('en')

def get_speech_tags(text):
    doc = en_nlp(text.decode('utf-8'))
    nouns = []
    verbs = []
    adjectives = []
    comparatives = []
    for word in doc:
        if word.tag_.startswith('NN'):
            nouns.append(str(word))
        elif word.tag_.startswith('VB'):
            verbs.append(str(word))
        elif word.tag_ == 'JJ':
            adjectives.append(str(word))
        elif word.tag_ == 'JJR' or word.tag_ == 'RBR':
            comparatives.append(str(word))
    return {'nouns':nouns, 'verbs':verbs, 'adjectives':adjectives, 'comparatives':comparatives}

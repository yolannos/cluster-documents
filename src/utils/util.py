# Treatment of cleaned text: tokenisation, stemming and lemmatisation
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
import pickle

import utils.extract_text as extract_text
import utils.util as util

def prediction(path):

    # extract text from pdf
    extract = extract_text.ExtractText(file=path, method='text')
    doc = extract.extract()

    # cleaning of the text extracted
    doc = util.cleaning(doc)

    # load the different tools needed for the prediction
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('model/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('model/decomposition.pkl', 'rb') as f:
        decomposition = pickle.load(f)

    # apply the necessary transofrmations
    trans = vectorizer.transform([doc]) # input must be a list of string aka whole text in one str
    trans_svd = decomposition.transform(trans)

    # execute the prediction
    return model.predict(trans_svd)

def cleaning(document):
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")
    # Process whole documents
    document = document.replace("\\n"," ")
    doc = nlp(document)

    # Tokenisation
    token_list = []
    for token in doc:
        token_list.append(token.text)

    # Create list of word tokens after removing stopwords
    filtered_sentence =[] 

    for word in token_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word)
            
    doc = nlp(' '.join(filtered_sentence))

    #Lematization
    lemma_word = [] 
    for token in doc:
        lemma_word.append(token.lemma_)

    #Remove punctuation
    doc = ' '.join(word.strip(string.punctuation) for word in lemma_word)
    
    return doc
import sys
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
import pickle
import src.utils.extract_text as extract_text


class Prediction:

    def __init__(self):
        if 'en_core_web_sm' in sys.modules:
            print("installed")

        # Load English tokenizer, tagger, parser and NER
        self.nlp = spacy.load("en_core_web_sm")
        # load the different tools needed for the prediction
        with open('model/model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open('model/vectorizer.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open('model/decomposition.pkl', 'rb') as f:
            self.decomposition = pickle.load(f)

    def predict(self, path):

        # extract text from pdf
        extract = extract_text.ExtractText(file=path, method='text')
        doc = extract.extract()

        # cleaning of the text extracted
        doc = self.cleaning(doc)

        # apply the necessary transofrmations
        trans = self.vectorizer.transform([doc]) # input must be a list of string aka whole text in one str
        trans_svd = self.decomposition.transform(trans)

        # execute the prediction
        return self.model.predict(trans_svd)

    def cleaning(self, document):

        # Process whole documents
        document = document.replace("\\n"," ")
        doc = self.nlp(document)

        # Tokenisation
        token_list = []
        for token in doc:
            token_list.append(token.text)

        # Create list of word tokens after removing stopwords
        filtered_sentence =[]
        self.nlp.Defaults.stop_words |= {'total', 'report', 'annual', 'period', 'date', 'para', 'statement', 'number', 'expenditure',
                           'director', 'result', 'financial', 'review', 'strategy', 'committee', 'executive', 'page',
                           'trustee', 'charity', 'principal', 'signature', 'disclosure', 'performance', 'work',
                           'association', 'trust', 'behalf', 'secretary', 'meeting', 'council', 'year', 'end', 'give',
                           'content', 'message', 'chairman', 'chief', 'officer', 'audit', 'independent', 'charitable',
                           'auditor', 'balance', 'budget', 'end', 'road', 'investment', 'fund', 'cash', 'examiner',
                           'january', 'february', 'march', 'april', 'may', 'june', 'july', 'asset',  'accounting',
                           'general', 'account', 'name', 'unrestricted', 'accordance', 'continue', 'restrict',
                           'cost', 'value', 'company', 'also', 'scheme', 'tot', 'provide',
                           'august', 'september', 'october', 'november', 'december', 'income', 'fund', 'examination'}
        for word in token_list:
            lexeme = self.nlp.vocab[word]
            if lexeme.is_stop == False:
                filtered_sentence.append(word)

        doc = self.nlp(' '.join(filtered_sentence))

        # lematization
        lemma_word = []
        for token in doc:
            lemma_word.append(token.lemma_)

        # remove punctuation
        doc = ' '.join(word.strip(string.punctuation) for word in lemma_word)

        return doc

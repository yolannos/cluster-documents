import utils.extract_text as extract
import utils.util as util
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

pdf = './dataset/test3.pdf'

extract = extract.extractText(pdf)

doc = extract.extract()

doc = util.cleaning(doc)


with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('model/decomposition.pkl', 'rb') as f:
    decomposition = pickle.load(f)


trans = vectorizer.transform([doc]) # input must be a list of string aka whole text in one str
trans_svd = decomposition.transform(trans)

x = model.predict(trans_svd)
print(x)
# print(type(trans))

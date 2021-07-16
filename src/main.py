import utils.extract_text as extract
import utils.util as util
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

pdf = './dataset/testpdf.pdf'

extract = extract.extractText(pdf)

doc = extract.extract()

doc = [util.cleaning(doc)]

with open('model_kmeans.pkl', 'rb') as f:
    model = pickle.load(f)

vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
trans = vectorizer.fit_transform(doc) # input must be a list of string aka whole text in one str
svd = TruncatedSVD(100)
trans_svd = svd.fit_transform(trans)

x = model.predict(trans_svd)
print(type(trans))

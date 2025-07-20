import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

nltk.data.path.append("./nltk_data")

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    keywords = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return list(set(keywords))

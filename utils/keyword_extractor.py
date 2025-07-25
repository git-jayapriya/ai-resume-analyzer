import nltk
import os
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    keywords = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return list(set(keywords))

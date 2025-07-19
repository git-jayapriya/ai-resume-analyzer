from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_skills(resume_keywords, jd_keywords):
    matched = list(set(resume_keywords) & set(jd_keywords))
    missing = list(set(jd_keywords) - set(resume_keywords))
    return matched, missing

def calculate_similarity(text1, text2):
    vect = TfidfVectorizer()
    tfidf = vect.fit_transform([text1, text2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return score * 100
    
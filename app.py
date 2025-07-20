import streamlit as st
import asyncio
from utils.file_reader import extract_text_from_file
from utils.keyword_extractor import extract_keywords
from utils.similarity_checker import match_skills, calculate_similarity 
import nltk 
import os
nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('stopwords')
#nltk.download('omw-1.4') 
#nltk.data.path.append("./nltk_data")
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

# Download required datasets
#nltk.download("punkt", download_dir=nltk_data_dir)
#nltk.download("wordnet", download_dir=nltk_data_dir)
#nltk.download("stopwords", download_dir=nltk_data_dir)

# --- Manual Suggestions ---
suggestions_data = {
    "Python": {"course_name": "Complete Python Bootcamp", "duration": "24 hrs", "rating": "4.7★", "link": "https://www.udemy.com/course/complete-python-bootcamp/"},
    "SQL": {"course_name": "SQL Bootcamp 2024", "duration": "30 hrs", "rating": "4.8★", "link": "https://www.udemy.com/course/the-complete-sql-bootcamp/"},
    "Machine Learning": {"course_name": "Machine Learning by Andrew Ng", "duration": "60 hrs", "rating": "4.9★", "link": "https://www.coursera.org/learn/machine-learning"},
    "Deep Learning": {"course_name": "Deep Learning Specialization", "duration": "80 hrs", "rating": "4.8★", "link": "https://www.coursera.org/specializations/deep-learning"},
    "Data Science": {"course_name": "IBM Data Science Professional Certificate", "duration": "80 hrs", "rating": "4.7★", "link": "https://www.coursera.org/professional-certificates/ibm-data-science"},
    "AI": {"course_name": "AI For Everyone by Andrew Ng", "duration": "10 hrs", "rating": "4.8★", "link": "https://www.coursera.org/learn/ai-for-everyone"},
    "Excel": {"course_name": "Excel Skills for Data Analysis", "duration": "10 hrs", "rating": "4.6★", "link": "https://www.coursera.org/learn/excel-data-analysis"},
    "Power BI": {"course_name": "Power BI Up & Running", "duration": "12 hrs", "rating": "4.6★", "link": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/"},
    "Tableau": {"course_name": "Data Visualization with Tableau", "duration": "12 hrs", "rating": "4.7★", "link": "https://www.coursera.org/specializations/data-visualization"},
    "Statistics": {"course_name": "Statistics with Python", "duration": "25 hrs", "rating": "4.7★", "link": "https://www.coursera.org/specializations/statistics-with-python"},
    "R Programming": {"course_name": "R Programming by Johns Hopkins", "duration": "20 hrs", "rating": "4.5★", "link": "https://www.coursera.org/learn/r-programming"},
    "A/B Testing": {"course_name": "A/B Testing by Google", "duration": "2 hrs", "rating": "4.6★", "link": "https://www.udacity.com/course/ab-testing--ud257"},
    "Marketing Analytics": {"course_name": "Marketing Analytics", "duration": "18 hrs", "rating": "4.6★", "link": "https://www.coursera.org/specializations/marketing-analytics"},
    "BigQuery": {"course_name": "Analyzing BigQuery Data", "duration": "10 hrs", "rating": "4.7★", "link": "https://www.coursera.org/learn/bigquery-for-data-analysts"},
    "AWS": {"course_name": "AWS Data Engineering", "duration": "15 hrs", "rating": "4.6★", "link": "https://aws.amazon.com/certification/certified-data-engineer-associate/"},
    "GCP": {"course_name": "Google Cloud Fundamentals", "duration": "10 hrs", "rating": "4.7★", "link": "https://www.coursera.org/learn/gcp-fundamentals"},
    "Azure": {"course_name": " Microsoft Azure Data Scientist ", "duration": "16 hrs", "rating": "4.6★", "link": "https://learn.microsoft.com/en-us/credentials/certifications/azure-data-scientist/?practice-assessment-type=certification"},
    "ETL": {"course_name": "ETL Basics for Data Engineers", "duration": "8 hrs", "rating": "4.6★", "link": "https://www.udemy.com/course/the-complete-etl-testing-course/?couponCode=PMNVD2025"},
    "Data Modeling": {"course_name": " Advanced Data Modeling ", "duration": "4 weeks", "rating": "4.3★", "link": "https://www.coursera.org/learn/advanced-data-modeling"},
    "Numpy": {"course_name": "Numerical Python with Numpy", "duration": "3.5 hrs", "rating": "4.4★", "link": "https://www.udemy.com/course/the-numpy-mindset-numerical-python/?couponCode=PMNVD2025"},
    "Pandas": {"course_name": "Data Analysis with Pandas", "duration": "6 hrs", "rating": "4.8★", "link": "https://www.udemy.com/course/data-analysis-with-pandas/"},
    "Flask": {"course_name": "Flask Framework complete course", "duration": "6 hrs", "rating": "4.5★", "link": "https://www.udemy.com/course/flask-framework-complete-course-for-beginners/?couponCode=PMNVD2025"},
    "Django": {"course_name": "Python Django - The Practical Guide", "duration": "35 hrs", "rating": "4.7★", "link": "https://www.udemy.com/course/python-django-the-practical-guide/"},
    "Streamlit": {"course_name": "Streamlit Tutorial", "duration": "3 hrs", "rating": "4.6★", "link": "https://www.youtube.com/watch?v=JwSS70SZdyM"},
    "ChatGPT": {"course_name": "ChatGPT for Data Science", "duration": "4 weeks", "rating": "4.5★", "link": "https://www.udemy.com/course/chatgpt-for-data-science-and-data-analysis-in-python/?utm_source=adwords&utm_medium=udemyads&utm_campaign=Search_DSA_Alpha_Prof_la.EN_cc.India&campaigntype=Search&portfolio=India&language=EN&product=Course&test=&audience=DSA&topic=Data_Science&priority=Alpha&utm_content=deal4584&utm_term=_._ag_160270535185_._ad_696202838301_._kw__._de_c_._dm__._pl__._ti_dsa-1677974310676_._li_1007809_._pd__._&matchtype=&gad_source=1&gad_campaignid=21178559971&gbraid=0AAAAADROdO2kqGDmzL0FH8IbgOuqhbU1d&gclid=Cj0KCQjwhO3DBhDkARIsANxrhTpTBKxH6DUEBf1S4OOV7SFznTg1l_QXkxMTin2zBVb5lAwZRnX2_MIaAua4EALw_wcB&couponCode=PMNVD2025"},
    "Data Engineering": {"course_name": "Data Engineering with Google Cloud", "duration": "30 hrs", "rating": "4.5★", "link": "https://www.coursera.org/professional-certificates/ibm-data-engineer?irclickid=3t6RuJ3kxxycUhqTA7xiWV%3AqUkp02BwAOy1S000&irgwc=1&utm_medium=partners&utm_source=impact&utm_campaign=3919688&utm_content=b2c&utm_campaignid=Spiderum%20ecom&utm_term=14726_CR_1164545_&gad_source=1"},
    "Generative AI": {"course_name": "Generative AI for Everyone", "duration": "10 hrs", "rating": "4.8★", "link": "https://www.coursera.org/learn/generative-ai-for-everyone"},
    "Math for ML": {"course_name": "Mathematics for Machine Learning", "duration": "40 hrs", "rating": "4.6★", "link": "https://www.coursera.org/specializations/mathematics-machine-learning"},
    "Computer Vision": {"course_name": "Deep Learning for Computer Vision", "duration": "25 hrs", "rating": "4.7★", "link": "https://www.coursera.org/learn/convolutional-neural-networks"},
    "Natural Language Processing": {"course_name": "Natural Language Processing Specialization", "duration": "60 hrs", "rating": "4.8★", "link": "https://www.coursera.org/specializations/natural-language-processing"},
    "Others": {"course_name": "Explore skills on GeeksforGeeks or Kaggle Learn", "duration": "Varies", "rating": "⭐", "link": "https://www.geeksforgeeks.org/"}
}


# --- UI Layout ---
st.set_page_config(page_title="AI Resume–Job Matching", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #fef7f7; padding: 2rem; border-radius: 10px;}
    </style>
    <div class="main">
    <h1>📄 AI Resume–Job Matching & Skill Gap Analyzer</h1>
    </div>
""", unsafe_allow_html=True)

resume_file = st.file_uploader("📎 Upload Resume", type=["pdf", "docx", "txt"])
job_description = st.text_area("🧾 Paste Job Description")

if st.button("🎯 Match Now"):
    if resume_file and job_description:
        resume_text = extract_text_from_file(resume_file)
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(job_description)

        matched, missing = match_skills(resume_keywords, jd_keywords)
        similarity = calculate_similarity(resume_text, job_description)

        st.success(f"🔍 Resume-Job Similarity Score: {similarity:.2f}%")
        st.markdown("---")

        st.markdown("### ✅ Matched Skills")
        st.markdown(
            "<div style='background-color:#eafbea;padding:10px;border-radius:10px;'>"
            + ", ".join(f"<span style='color:green;font-weight:bold'>{skill}</span>" for skill in matched)
            + "</div>",
            unsafe_allow_html=True
        )

        st.markdown("### ❌ Missing Skills")
        st.markdown(
            "<div style='background-color:#ffecec;padding:10px;border-radius:10px;'>"
            + ", ".join(f"<span style='color:#d91e18;font-weight:bold'>{skill}</span>" for skill in missing)
            + "</div>",
            unsafe_allow_html=True
        )

        def display_upskilling_suggestions(suggestions_data):
            st.markdown("### 📘 Upskilling Suggestions (AI)")
            if not suggestions_data:
                st.info("🎯 You're all set! No critical skill gaps found.")
                return
            
            for skill, resource in suggestions_data.items():
                st.markdown(f"""
                <div style="background-color: #fce2e2; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h4 style="margin: 0;">🧠 Skill: <span style="color:#f72585;">{skill}</span></h4>
                    <p style="margin: 5px 0;color:#333;"><strong>📚 Recommended Resource:</strong> {resource['course_name']}</p>
                    <p style="margin: 5px 0;">🕒 Duration: {resource['duration']} | ⭐ Rating: {resource['rating']}</p>
                    <a href="{resource['link']}" target="_blank">🔗 Visit Course</a>
                </div>
                """, unsafe_allow_html=True)

        display_upskilling_suggestions({
            k: v for k, v in suggestions_data.items()
            if k.lower() in [m.lower() for m in missing]
        })

    else:
        st.warning("⚠️ Please upload both a resume and job description to continue.")

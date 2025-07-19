import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Optional: Use gpt-4 if you have access
MODEL_NAME = "gpt-3.5-turbo"

async def get_upskilling_suggestions(jd_text, missing_skills):
    prompt = f"""You are a career assistant.
Here is the job description: {jd_text}
The candidate is missing the following skills: {', '.join(missing_skills)}.
Please suggest brief, clear upskilling paths or learning resources for these missing skills."""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert career coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API failed: {e}")
        # 🔁 Return dummy upskilling suggestions
        return f"Suggested Upskilling Topics: {', '.join(missing_skills)}.\nTry exploring courses on Coursera, Udemy, or freeCodeCamp related to these skills."

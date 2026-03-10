import streamlit as st
import pdfplumber

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    st.subheader("Extracted Resume Text Preview:")
    st.write(text[:1000])

    skills_list = [
        "python", "java", "c++", "sql",
        "machine learning", "data analysis",
        "html", "css", "power bi",
        "pandas", "numpy", "scikit-learn"
    ]

    detected_skills = []
    resume_lower = text.lower()

    for skill in skills_list:
        if skill in resume_lower:
            detected_skills.append(skill)

    st.subheader("Detected Skills:")
    st.write(detected_skills)

    st.subheader("Paste Job Description")
    job_description = st.text_area("Enter Job Description Here")

    if job_description:

        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        documents = [text, job_description]

        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(documents)

        similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        match_percentage = round(similarity_score[0][0] * 100, 2)

        st.subheader("Resume Match Percentage:")
        st.write(f"{match_percentage}%")

        # Missing Skills
        jd_lower = job_description.lower()
        missing_skills = []

        for skill in skills_list:
            if skill in jd_lower and skill not in resume_lower:
                missing_skills.append(skill)

        st.subheader("Missing Skills:")
        st.write(missing_skills)

        # Resume Score
        jd_score = match_percentage * 0.5
        skills_score = min(len(detected_skills) * 3, 30)

        length_score = 0
        if len(text) > 1500:
            length_score = 20
        elif len(text) > 800:
            length_score = 10
        else:
            length_score = 5

        total_score = round(jd_score + skills_score + length_score, 2)

        st.subheader("Overall Resume Score:")
        st.success(f"{total_score} / 100")

        # Suggestions
        st.subheader("AI Resume Improvement Suggestions")

        suggestions = []

        if match_percentage < 50:
            suggestions.append("Your resume does not match the job description well. Try adding more relevant keywords from the job description.")

        if missing_skills:
            suggestions.append(f"You are missing important skills: {', '.join(missing_skills)}")

        if len(text) < 800:
            suggestions.append("Your resume content is short. Add more project details, achievements, and experience.")

        if "project" in resume_lower and "%" not in text:
            suggestions.append("Try adding measurable achievements in your projects (e.g., improved performance by 20%).")

        if not suggestions:
            suggestions.append("Great job! Your resume looks strong for this job role.")

        for tip in suggestions:
            st.warning(tip)
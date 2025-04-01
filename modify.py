#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pdfplumber
import docx
import re
import openai
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def parse_resume(file):
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return None

def extract_sections(resume_text):
    sections = {}
    current_section = "Other"
    lines = resume_text.split("\n")
    for line in lines:
        if re.match(r"^\s*[A-Z][A-Za-z ]+:\s*$", line):
            current_section = line.strip()
            sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(line)
    return sections

def extract_skills_with_gpt(job_desc):
    prompt = f"""
    Extract key skills, tools, technologies, and any relevant information from the following job description.
    Classify them into appropriate resume sections such as 'Technical Skills', 'Certifications', 'Experience', 'Projects', etc.
    Provide the output as a JSON object where keys are section names and values are lists of skills.
    Job Description:
    {job_desc}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI expert in resume optimization."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        extracted_text = response.choices[0].message.content.strip()
        extracted_data = json.loads(extracted_text)
        return extracted_data
    except json.JSONDecodeError:
        st.error("Error: Failed to parse extracted skills from OpenAI response.")
        return {}
    except openai.error.OpenAIError as e:
        st.error(f"Error extracting skills: {e}")
        return {}

def get_user_approval(extracted_data):
    approved_data = {}
    for section, items in extracted_data.items():
        approved_items = []
        for item in items:
            if st.checkbox(f"Add to {section}: {item}?"):
                approved_items.append(item)
        if approved_items:
            approved_data[section] = approved_items
    return approved_data

def update_resume(sections, approved_data):
    for section, items in approved_data.items():
        if section in sections:
            sections[section].append(", ".join(items))
        else:
            sections[section] = [", ".join(items)]
    return "\n".join([f"{sec}\n" + "\n".join(content) for sec, content in sections.items()])

def calculate_ats_score(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0] * 100

st.title("AI-Powered Resume Enhancer with ATS Scoring")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
job_description = st.text_area("Paste the job description here")

if uploaded_file and job_description:
    resume_text = parse_resume(uploaded_file)
    sections = extract_sections(resume_text)
    extracted_data = extract_skills_with_gpt(job_description)
    approved_data = get_user_approval(extracted_data)
    updated_resume_text = update_resume(sections, approved_data)
    
    ats_score_old = calculate_ats_score(job_description, resume_text)
    ats_score_new = calculate_ats_score(job_description, updated_resume_text)
    
    st.write(f"### ATS Score (Old Resume): {ats_score_old:.2f}%")
    st.write(f"### ATS Score (New Resume): {ats_score_new:.2f}%")
    
    st.download_button("Download Updated Resume", updated_resume_text, file_name="Updated_Resume.txt")


# In[ ]:





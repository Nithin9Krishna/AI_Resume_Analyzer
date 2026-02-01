# AI Resume Analyzer
````markdown

## Overview

AI Resume Analyzer is a practical resume–job matching system designed to help recruiters, hiring managers, and candidates evaluate how well a resume aligns with a specific job description.

Instead of relying purely on keyword matching, this project combines semantic understanding, skill comparison, and experience analysis to produce a clearer and more realistic evaluation of candidate fit.

The output includes structured scores, matched and missing skills, and a short recruiter-friendly summary that can be reviewed quickly.

---

## Why This Project

Resume screening is often time-consuming and inconsistent. Many automated tools depend heavily on keyword frequency, which can lead to:
- Missing relevant experience phrased differently
- Overvaluing buzzwords
- Ignoring project-level or applied experience

This project aims to improve resume screening by combining multiple evaluation signals rather than relying on a single metric.

---

## How the System Works

The analysis pipeline follows a structured flow:

1. Resume PDF is converted into clean text
2. Job description is cleaned and filtered to retain relevant sections
3. Semantic similarity between resume and job description is calculated
4. Skills are extracted dynamically from the job description
5. Resume skills and experience are compared against job requirements
6. Results are combined into final scores and a readable summary

---

## Key Components

### 1. Resume Text Extraction

Resumes are uploaded as PDF files and converted into plain text using a PDF reader utility.

This step is important because resumes vary widely in formatting, and downstream analysis requires clean text input.

**File:** `pdf_reader.py`

```python
def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
````

---

### 2. Semantic Match Analysis

This component measures how closely the resume content aligns with the job description at a **role level**, rather than just matching keywords.

**Model used:**
`sentence-transformers/all-MiniLM-L6-v2`

This model converts text into dense vector embeddings that capture semantic meaning. Cosine similarity between resume and job description embeddings is used as the semantic match score.

**File:** `ai_analyzer.py`

```python
resume_embedding = model.encode(resume_text)
jd_embedding = model.encode(cleaned_jd)
similarity = cosine_similarity([resume_embedding], [jd_embedding])[0][0]
```

The semantic score reflects whether the candidate’s background broadly matches the role’s expectations.

---

### 3. Job-Driven Skill Matching

Instead of relying on a fixed skill list, skills are extracted dynamically from the job description.

**Process:**

* Job description is cleaned
* Technical skills and key terms are identified
* Each skill is checked against the resume text
* Skills are classified as matched or missing

**File:** `skill_gap.py`

```python
if skill in resume_text.lower():
    matched_skills.append(skill)
else:
    missing_skills.append(skill)
```

This ensures the analysis adapts to different roles without manual updates.

---

### 4. Project and Experience Matching

Beyond skill names, the system evaluates whether the resume demonstrates applied experience, such as:

* Use of frameworks and tools
* API development
* Model deployment or pipelines
* Real-world project implementation

This helps distinguish between theoretical knowledge and hands-on experience.

---

### 5. Scoring Strategy

The final evaluation uses a weighted scoring approach to reflect real recruiter decision-making.

| Component            | Weight |
| -------------------- | ------ |
| Skill Match Score    | 50%    |
| Project Match Score  | 30%    |
| Semantic Match Score | 20%    |

```python
final_score = (
    0.5 * skill_match_score +
    0.3 * project_match_score +
    0.2 * semantic_score
)
```

This prevents any single metric from dominating the evaluation.

---

### 6. Recruiter Summary Generation

The final step converts numerical results into a short, readable paragraph.

The summary highlights:

* Overall fit
* Strong areas
* Key gaps or improvement areas

**File:** `summary_generator.py`

Example output:

> The candidate shows a moderate to strong alignment with the role. The resume demonstrates relevant experience in Generative AI, Python, and RAG-based systems. Additional exposure to SQL and NoSQL databases would further strengthen the profile.

---

## Application Interface

The project supports two modes of execution:

### Command Line

For quick testing and debugging.

```bash
python src/main.py
```

### Web Interface (Streamlit)

A simple UI for uploading resumes and pasting job descriptions.

```bash
streamlit run src/app.py
```

---

## Project Structure

```
AI_Resume_Analyzer/
│
├── Data/
│   ├── resumes/
│   │   └── resume.pdf
│   └── job_description.txt
│
├── src/
│   ├── app.py
│   ├── main.py
│   ├── pdf_reader.py
│   ├── ai_analyzer.py
│   ├── skill_gap.py
│   └── summary_generator.py
│
├── requirements.txt
└── README.md
```

---

## Accuracy and Limitations

### Strengths

* Adapts dynamically to different job descriptions
* Balances semantic understanding and skill matching
* Produces recruiter-friendly outputs

### Limitations

* Depends on resume text quality
* Short or vague job descriptions reduce accuracy
* Does not currently learn from hiring feedback

---

## Future Improvements

Planned enhancements include:

* Named Entity Recognition for better skill extraction
* Experience duration weighting
* Resume-to-resume comparison
* PDF report export
* Feedback-driven score calibration
* Optional LLM-based explanation layer

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Author

Sai Nithin Krishna Souram
Master’s in Artificial Intelligence
Focus on applied NLP, resume analytics, and AI-driven decision support systems

```

---

### What you should do next
1. Paste this into the README editor
2. Click **Commit changes**
3. Publish your Streamlit app
4. Add the app URL to the README later

If you want, next I can:
- Add **architecture / decision tree diagram**
- Write **resume-ready project explanation**
- Prepare **interview answers**
- Help deploy on **Streamlit Cloud**

Just say the word.
```

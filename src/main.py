import os
from pdf_reader import extract_text_from_pdf
from ai_analyzer import analyze_similarity, analyze_project_experience_match
from skill_gap import generate_skill_gap_feedback
from summary_generator import generate_recruiter_summary

# --------------------------------------------------
# Project base directory
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------
# File paths
# --------------------------------------------------
resume_path = os.path.join(BASE_DIR, "data", "resumes", "resume.pdf")
jd_path = os.path.join(BASE_DIR, "data", "job_description.txt")

# --------------------------------------------------
# Read inputs
# --------------------------------------------------
resume_text = extract_text_from_pdf(resume_path)

with open(jd_path, "r") as f:
    job_text = f.read()

# --------------------------------------------------
# Analysis
# --------------------------------------------------

# 1️⃣ Overall semantic similarity (resume vs JD meaning)
semantic_score = analyze_similarity(resume_text, job_text)

# 2️⃣ Project & experience semantic match
project_score = analyze_project_experience_match(resume_text, job_text)

# 3️⃣ Skill gap analysis (explicit technical requirements)
skill_report = generate_skill_gap_feedback(resume_text, job_text)

# 4️⃣ Final weighted score (recruiter-style decision score)
final_score = round(
    (0.5 * skill_report["skill_match_score"]) +
    (0.3 * project_score) +
    (0.2 * semantic_score),
    2
)

# 5️⃣ Recruiter-friendly summary
summary = generate_recruiter_summary(
    semantic_score,
    project_score,
    skill_report
)

# --------------------------------------------------
# Output
# --------------------------------------------------
print("\n========== AI RESUME ANALYSIS ==========\n")

print(f"Overall Semantic Match: {semantic_score} %")
print(f"Project / Experience Match: {project_score} %")
print(f"Skill Match Score: {skill_report['skill_match_score']} %")
print(f"\nFinal Fit Score: {final_score} %\n")

print("Matched Skills:")
for skill in skill_report["matched_skills"]:
    print(f"- {skill}")

print("\nMissing / Weak Skills:")
for skill in skill_report["missing_skills"]:
    print(f"- {skill}")

print("\nRecruiter Summary:")
print(summary)

print("\n=======================================\n")

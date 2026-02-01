from pathlib import Path

from ai_analyzer import analyze_similarity
from pdf_reader import extract_text_from_pdf
from skill_gap import generate_skill_gap_feedback

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

resume_text = extract_text_from_pdf(DATA_DIR / "resumes" / "resume.pdf")
job_text = (DATA_DIR / "job_description.txt").read_text(encoding="utf-8")

score = analyze_similarity(resume_text, job_text)
missing_skills = generate_skill_gap_feedback(resume_text, job_text)

print("AI Match Score:", score, "%")
print("Potential Skill Gaps:", missing_skills)

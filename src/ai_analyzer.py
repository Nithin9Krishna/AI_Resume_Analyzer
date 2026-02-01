from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_job_description(job_text):
    """
    Keep only role responsibilities & requirements.
    Remove company story and legal sections.
    """
    lines = job_text.lower().splitlines()

    keep = []
    capture = False

    for line in lines:
        if any(key in line for key in [
            "what you’ll do",
            "what you'll do",
            "what you must bring",
            "requirements",
            "responsibilities",
            "experience with",
            "proficiency"
        ]):
            capture = True
            continue

        if any(key in line for key in [
            "equal employment",
            "committed to",
            "contact us",
            "we may use",
            "ai tools"
        ]):
            capture = False

        if capture and len(line.strip()) > 5:
            keep.append(line)

    return " ".join(keep)


def analyze_similarity(resume_text, job_text):
    """
    Overall semantic similarity between resume and JD
    """
    cleaned_jd = clean_job_description(job_text)

    resume_embedding = model.encode(resume_text)
    jd_embedding = model.encode(cleaned_jd)

    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    return round(similarity * 100, 2)


def extract_project_experience_text(resume_text):
    """
    Extract project & experience related text from resume
    """
    lines = resume_text.lower().splitlines()
    project_lines = []

    for line in lines:
        if any(k in line for k in [
            "project",
            "experience",
            "worked on",
            "built",
            "developed",
            "implemented",
            "designed"
        ]):
            project_lines.append(line)

    return " ".join(project_lines)


def analyze_project_experience_match(resume_text, job_text):
    """
    Semantic match between resume projects/experience and job description
    """
    project_text = extract_project_experience_text(resume_text)

    if not project_text.strip():
        return 0.0

    project_embedding = model.encode(project_text)
    jd_embedding = model.encode(clean_job_description(job_text))

    similarity = cosine_similarity(
        [project_embedding],
        [jd_embedding]
    )[0][0]

    return round(similarity * 100, 2)

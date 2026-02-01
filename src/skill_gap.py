import re

# ---------- STEP 1: Extract only TECHNICAL parts of the JD ----------
def extract_technical_jd_text(job_text):
    lines = job_text.lower().splitlines()
    technical_lines = []
    capture = False

    for line in lines:
        if any(key in line for key in [
            "what you’ll do",
            "what you'll do",
            "what you must bring",
            "requirements",
            "proficiency",
            "experience with",
            "familiarity with"
        ]):
            capture = True
            continue

        if any(key in line for key in [
            "equal employment",
            "committed to",
            "contact us",
            "we may use"
        ]):
            capture = False

        if capture and len(line.strip()) > 5:
            technical_lines.append(line)

    return " ".join(technical_lines)


# ---------- STEP 2: Extract skill-like phrases from JD ----------
def extract_skill_candidates(job_text):
    text = extract_technical_jd_text(job_text)
    words = re.findall(r"[a-zA-Z]+", text)

    candidates = set()
    for i in range(len(words)):
        for size in (1, 2, 3):
            phrase = " ".join(words[i:i+size])
            if len(phrase) > 3:
                candidates.add(phrase)

    return candidates


# ---------- STEP 3: Canonicalize skills (clean, professional) ----------
def canonicalize_skills(skill_candidates):
    canonical = set()

    for skill in skill_candidates:
        s = skill.lower()

        if "python" in s:
            canonical.add("python")
        elif "javascript" in s or "js" in s:
            canonical.add("javascript")
        elif "sql" in s:
            canonical.add("sql")
        elif "nosql" in s or "mongodb" in s:
            canonical.add("nosql")
        elif "aws" in s or "cloud" in s:
            canonical.add("aws")
        elif "docker" in s or "container" in s:
            canonical.add("docker")
        elif "kubernetes" in s or "k8s" in s:
            canonical.add("kubernetes")
        elif "llm" in s or "language model" in s:
            canonical.add("llms")
        elif "generative ai" in s or "genai" in s:
            canonical.add("generative ai")
        elif "rag" in s:
            canonical.add("rag")
        elif "openai" in s:
            canonical.add("openai")
        elif "hugging" in s:
            canonical.add("huggingface")
        elif "fastapi" in s or "flask" in s:
            canonical.add("api frameworks")
        elif "react" in s or "vue" in s or "angular" in s:
            canonical.add("frontend frameworks")

    return canonical


# ---------- FINAL: Skill gap analysis ----------
def generate_skill_gap_feedback(resume_text, job_text):
    skill_candidates = extract_skill_candidates(job_text)
    jd_skills = canonicalize_skills(skill_candidates)

    resume_text = resume_text.lower()

    matched = set()
    missing = set()

    for skill in jd_skills:
        if skill in resume_text:
            matched.add(skill)
        else:
            missing.add(skill)

    score = (len(matched) / len(jd_skills)) * 100 if jd_skills else 0

    return {
        "skill_match_score": round(score, 2),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing)
    }

def generate_skill_gap_feedback(resume_text: str, job_text: str) -> list[str]:
    missing = []

    job_keywords = ["aws", "docker", "nlp", "kubernetes", "cloud"]
    for skill in job_keywords:
        if skill.lower() not in resume_text.lower():
            missing.append(skill)

    return missing

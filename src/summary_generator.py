def generate_recruiter_summary(
    semantic_score,
    project_score,
    skill_report
):
    skill_score = skill_report["skill_match_score"]
    matched = skill_report["matched_skills"]
    missing = skill_report["missing_skills"]

    # Overall fit determination
    combined_score = (0.5 * skill_score) + (0.3 * project_score) + (0.2 * semantic_score)

    if combined_score >= 75:
        fit = "strong"
    elif combined_score >= 55:
        fit = "moderate"
    else:
        fit = "limited"

    matched_text = ", ".join(matched[:5]) if matched else "core technical areas"
    missing_text = ", ".join(missing[:3]) if missing else None

    summary = (
        f"The candidate demonstrates a {fit} overall fit for the role. "
        f"The resume aligns well with the job description, particularly through "
        f"projects and hands-on experience involving {matched_text}. "
    )

    if missing_text:
        summary += (
            f"Some additional exposure to {missing_text} could further strengthen the profile."
        )

    return summary

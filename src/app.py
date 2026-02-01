import streamlit as st
from pdf_reader import extract_text_from_pdf
from ai_analyzer import analyze_similarity, analyze_project_experience_match
from skill_gap import generate_skill_gap_feedback
from summary_generator import generate_recruiter_summary
import tempfile

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Resume Match Evaluation",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <h2 style="margin-bottom:4px;">Resume Match Evaluation</h2>
    <p style="color:#6b7280; margin-top:0;">
    Evaluate resume alignment against a job description using structured analysis.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Input section
# --------------------------------------------------
st.subheader("Inputs")

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(
        "Resume (PDF)",
        type=["pdf"]
    )

with col2:
    job_text = st.text_area(
        "Job Description",
        height=220
    )

st.divider()

analyze_btn = st.button("Run Evaluation")

# --------------------------------------------------
# Analysis
# --------------------------------------------------
if analyze_btn and resume_file and job_text.strip():

    with st.spinner("Running analysis..."):

        # Save uploaded resume temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(resume_file.read())
            resume_path = tmp.name

        resume_text = extract_text_from_pdf(resume_path)

        semantic_score = analyze_similarity(resume_text, job_text)
        project_score = analyze_project_experience_match(resume_text, job_text)
        skill_report = generate_skill_gap_feedback(resume_text, job_text)

        final_score = round(
            (0.5 * skill_report["skill_match_score"]) +
            (0.3 * project_score) +
            (0.2 * semantic_score),
            2
        )

        summary = generate_recruiter_summary(
            semantic_score,
            project_score,
            skill_report
        )

    # --------------------------------------------------
    # Results
    # --------------------------------------------------
    st.subheader("Evaluation Summary")

    col_a, col_b, col_c = st.columns(3)

    col_a.metric("Semantic Alignment", f"{semantic_score} %")
    col_b.metric("Project & Experience Match", f"{project_score} %")
    col_c.metric("Overall Fit Score", f"{final_score} %")

    st.divider()

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Matched Skills")
        if skill_report["matched_skills"]:
            for skill in skill_report["matched_skills"]:
                st.write(f"- {skill}")
        else:
            st.write("No strong matches identified.")

    with col_right:
        st.subheader("Missing / Weaker Areas")
        if skill_report["missing_skills"]:
            for skill in skill_report["missing_skills"]:
                st.write(f"- {skill}")
        else:
            st.write("No major gaps identified.")

    st.divider()

    # --------------------------------------------------
    # Recruiter summary
    # --------------------------------------------------
    st.subheader("Reviewer Notes")

    st.markdown(
        f"""
        <div style="
            background-color:#f9fafb;
            padding:16px;
            border-radius:6px;
            border:1px solid #e5e7eb;
            font-size:14px;
            line-height:1.6;
        ">
        {summary}
        </div>
        """,
        unsafe_allow_html=True
    )

elif analyze_btn:
    st.warning("Please provide both a resume and a job description.")

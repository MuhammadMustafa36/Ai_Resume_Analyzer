import streamlit as st

from parser import extract_resume_text

from skills import (
    extract_skills,
    compare_skills,
    match_score
)

from ai import (
    generate_ai_suggestions,
    ollama_available,
    DEFAULT_MODEL
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="AI Resume Analyzer",

    page_icon="📄",

    layout="wide"
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title("📄 AI Resume Analyzer")

st.write(
    """
Upload your CV and compare it with a job description.

The application will extract skills, compare them,
identify missing skills, calculate a match score,
and generate improvement suggestions.
"""
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    model = st.text_input(
        "Ollama Model",
        value=DEFAULT_MODEL
    )

    st.info(
        """
Supported resume formats:

• PDF
• DOCX
• TXT

For AI suggestions, Ollama
must be running locally.
"""
    )


# ============================================================
# RESUME UPLOAD
# ============================================================

resume_file = st.file_uploader(

    "📄 Upload your resume",

    type=[
        "pdf",
        "docx",
        "txt"
    ]
)


# ============================================================
# JOB DESCRIPTION
# ============================================================

job_description = st.text_area(

    "💼 Paste the Job Description",

    height=300,

    placeholder="""
Paste the complete job description here...

Example:

We are looking for a Data Scientist with
Python, SQL, Pandas, Machine Learning,
Power BI and AWS experience.
"""
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.button(

    "🔍 Analyze Resume",

    type="primary",

    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    # --------------------------------------------------------
    # Validate resume
    # --------------------------------------------------------

    if resume_file is None:

        st.error(
            "Please upload your resume first."
        )

        st.stop()


    # --------------------------------------------------------
    # Validate job description
    # --------------------------------------------------------

    if not job_description.strip():

        st.error(
            "Please paste the job description first."
        )

        st.stop()


    # --------------------------------------------------------
    # Extract resume text
    # --------------------------------------------------------

    try:

        resume_text = extract_resume_text(
            resume_file
        )

    except Exception as exc:

        st.error(
            f"Could not read the resume: {exc}"
        )

        st.stop()


    # --------------------------------------------------------
    # Check extracted text
    # --------------------------------------------------------

    if not resume_text.strip():

        st.error(
            """
No readable text was found in the resume.

If your PDF is a scanned image,
you need OCR support.
"""
        )

        st.stop()


    # --------------------------------------------------------
    # Extract skills
    # --------------------------------------------------------

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )


    # --------------------------------------------------------
    # Compare skills
    # --------------------------------------------------------

    comparison = compare_skills(

        resume_skills,

        job_skills
    )


    # --------------------------------------------------------
    # Calculate score
    # --------------------------------------------------------

    score = match_score(

        resume_skills,

        job_skills
    )


    # --------------------------------------------------------
    # Save results in session state
    # --------------------------------------------------------

    st.session_state["resume_text"] = resume_text

    st.session_state["resume_skills"] = resume_skills

    st.session_state["job_skills"] = job_skills

    st.session_state["matched"] = comparison["matched"]

    st.session_state["missing"] = comparison["missing"]

    st.session_state["extra"] = comparison["extra"]

    st.session_state["score"] = score


# ============================================================
# DISPLAY RESULTS
# ============================================================

if "score" in st.session_state:

    score = st.session_state["score"]

    matched = st.session_state["matched"]

    missing = st.session_state["missing"]

    extra = st.session_state["extra"]

    resume_skills = st.session_state["resume_skills"]

    job_skills = st.session_state["job_skills"]


    st.divider()


    # ========================================================
    # METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "🎯 Match Score",
        f"{score}%"
    )


    col2.metric(
        "💼 Job Skills",
        len(job_skills)
    )


    col3.metric(
        "✅ Matched",
        len(matched)
    )


    col4.metric(
        "❌ Missing",
        len(missing)
    )


    # ========================================================
    # SKILL COMPARISON
    # ========================================================

    st.subheader(
        "📊 Skill Comparison"
    )


    left, right = st.columns(2)


    # ========================================================
    # MATCHED SKILLS
    # ========================================================

    with left:

        st.markdown(
            "### ✅ Matched Skills"
        )

        if matched:

            for skill in matched:

                st.success(skill)

        else:

            st.warning(
                "No matching skills detected."
            )


    # ========================================================
    # MISSING SKILLS
    # ========================================================

    with right:

        st.markdown(
            "### ❌ Missing Skills"
        )

        if missing:

            for skill in missing:

                st.error(skill)

        else:

            st.success(
                "No missing skills detected."
            )


    # ========================================================
    # EXTRA SKILLS
    # ========================================================

    st.markdown(
        "### ➕ Other Resume Skills"
    )


    if extra:

        st.write(
            ", ".join(extra)
        )

    else:

        st.write(
            "No additional skills detected."
        )


    st.divider()


    # ========================================================
    # AI SUGGESTIONS
    # ========================================================

    st.subheader(
        "🤖 AI Improvement Suggestions"
    )


    # Check whether Ollama is running.

    if ollama_available():

        if st.button(
            "🤖 Generate AI Suggestions"
        ):

            with st.spinner(
                "Ollama is analyzing your resume..."
            ):

                try:

                    suggestions = (
                        generate_ai_suggestions(

                            resume_text=
                            st.session_state[
                                "resume_text"
                            ],

                            job_description=
                            job_description,

                            matched=
                            matched,

                            missing=
                            missing,

                            model=model
                        )
                    )


                    st.markdown(
                        suggestions
                    )


                except Exception as exc:

                    st.error(
                        f"Ollama error: {exc}"
                    )


    # ========================================================
    # FALLBACK SUGGESTIONS
    # ========================================================

    else:

        st.warning(
            """
Ollama is not currently available.

Showing rule-based suggestions instead.
"""
        )


        # Missing skills

        if missing:

            st.markdown(
                "**Priority 1 — Learn the missing skills:** "
                + ", ".join(missing)
            )

        else:

            st.markdown(
                """
**Your detected skills cover the known
skills required by this job.**

Focus on providing evidence,
projects, and measurable achievements.
"""
            )


        # Resume checklist

        st.markdown(
            """
### 📝 Resume Improvement Checklist

- Add a short professional summary.
- Put relevant technical skills near the top.
- Mention technologies used in projects.
- Add measurable achievements.
- Use action verbs.
- Keep project descriptions concise.
- Tailor your resume to each job.
- Do not add skills you do not actually know.
"""
        )


    # ========================================================
    # EXTRACTED RESUME TEXT
    # ========================================================

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(

            "Resume Text",

            st.session_state[
                "resume_text"
            ],

            height=400,

            label_visibility="collapsed"
        )


    # ========================================================
    # DETECTED SKILLS
    # ========================================================

    with st.expander(
        "🧠 View Detected Resume Skills"
    ):

        if resume_skills:

            st.write(
                ", ".join(resume_skills)
            )

        else:

            st.write(
                "No skills detected."
            )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "AI Resume Analyzer | Python + Streamlit + Ollama"
)
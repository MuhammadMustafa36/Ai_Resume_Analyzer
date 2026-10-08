import re
from typing import List, Dict


# ============================================================
# SKILL DATABASE
# ============================================================

SKILLS = {

    # -------------------------
    # Programming Languages
    # -------------------------

    "Python": [
        r"\bpython\b"
    ],

    "Java": [
        r"\bjava\b"
    ],

    "C++": [
        r"\bc\+\+\b"
    ],

    "C#": [
        r"\bc#\b",
        r"\bc sharp\b"
    ],

    "JavaScript": [
        r"\bjavascript\b",
        r"\bjs\b"
    ],

    "TypeScript": [
        r"\btypescript\b"
    ],


    # -------------------------
    # Web Development
    # -------------------------

    "HTML": [
        r"\bhtml\b"
    ],

    "CSS": [
        r"\bcss\b"
    ],

    "React": [
        r"\breact(?:\.js)?\b"
    ],

    "Node.js": [
        r"\bnode(?:\.js)?\b"
    ],

    "Django": [
        r"\bdjango\b"
    ],

    "Flask": [
        r"\bflask\b"
    ],

    "FastAPI": [
        r"\bfastapi\b"
    ],

    "Streamlit": [
        r"\bstreamlit\b"
    ],


    # -------------------------
    # APIs / Backend
    # -------------------------

    "REST API": [
        r"\brest(?:ful)?\s+api(?:s)?\b",
        r"\brest\b"
    ],


    # -------------------------
    # Databases
    # -------------------------

    "SQL": [
        r"\bsql\b"
    ],

    "PostgreSQL": [
        r"\bpostgresql\b"
    ],

    "MySQL": [
        r"\bmysql\b"
    ],

    "MongoDB": [
        r"\bmongodb\b",
        r"\bmongo\b"
    ],

    "SQLite": [
        r"\bsqlite\b"
    ],

    "Redis": [
        r"\bredis\b"
    ],


    # -------------------------
    # Data Science
    # -------------------------

    "Pandas": [
        r"\bpandas\b"
    ],

    "NumPy": [
        r"\bnumpy\b"
    ],

    "Matplotlib": [
        r"\bmatplotlib\b"
    ],

    "Seaborn": [
        r"\bseaborn\b"
    ],

    "Scikit-learn": [
        r"\bscikit[- ]learn\b",
        r"\bsklearn\b"
    ],

    "Statistics": [
        r"\bstatistics\b",
        r"\bstatistical analysis\b"
    ],

    "Data Analysis": [
        r"\bdata analysis\b",
        r"\bdata analytics\b"
    ],

    "Data Visualization": [
        r"\bdata visualization\b"
    ],


    # -------------------------
    # Machine Learning
    # -------------------------

    "Machine Learning": [
        r"\bmachine learning\b",
        r"\bml\b"
    ],

    "Deep Learning": [
        r"\bdeep learning\b"
    ],

    "Artificial Intelligence": [
        r"\bartificial intelligence\b",
        r"\bai\b"
    ],

    "NLP": [
        r"\bnlp\b",
        r"\bnatural language processing\b"
    ],

    "Computer Vision": [
        r"\bcomputer vision\b"
    ],


    # -------------------------
    # Generative AI
    # -------------------------

    "Generative AI": [
        r"\bgenerative ai\b",
        r"\bgenai\b",
        r"\bgen ai\b"
    ],

    "LLM": [
        r"\bllm\b",
        r"\blarge language models?\b"
    ],

    "RAG": [
        r"\brag\b",
        r"\bretrieval augmented generation\b"
    ],

    "LangChain": [
        r"\blangchain\b"
    ],

    "LangGraph": [
        r"\blanggraph\b"
    ],

    "Ollama": [
        r"\bollama\b"
    ],

    "OpenAI API": [
        r"\bopenai\b"
    ],


    # -------------------------
    # Deep Learning Frameworks
    # -------------------------

    "PyTorch": [
        r"\bpytorch\b",
        r"\btorch\b"
    ],

    "TensorFlow": [
        r"\btensorflow\b"
    ],

    "Keras": [
        r"\bkeras\b"
    ],


    # -------------------------
    # Vector Databases / Search
    # -------------------------

    "FAISS": [
        r"\bfaiss\b"
    ],

    "Qdrant": [
        r"\bqdrant\b"
    ],


    # -------------------------
    # Cloud
    # -------------------------

    "AWS": [
        r"\baws\b",
        r"\bamazon web services\b"
    ],

    "Azure": [
        r"\bazure\b"
    ],

    "GCP": [
        r"\bgcp\b",
        r"\bgoogle cloud\b"
    ],


    # -------------------------
    # DevOps
    # -------------------------

    "Git": [
        r"\bgit\b"
    ],

    "GitHub": [
        r"\bgithub\b"
    ],

    "GitHub Actions": [
        r"\bgithub actions\b"
    ],

    "Docker": [
        r"\bdocker\b"
    ],

    "Kubernetes": [
        r"\bkubernetes\b",
        r"\bk8s\b"
    ],

    "Linux": [
        r"\blinux\b"
    ],

    "CI/CD": [
        r"\bci/cd\b",
        r"\bcicd\b"
    ],


    # -------------------------
    # Business Intelligence
    # -------------------------

    "Power BI": [
        r"\bpower\s*bi\b"
    ],

    "Tableau": [
        r"\btableau\b"
    ],

    "Excel": [
        r"\bexcel\b",
        r"\bmicrosoft excel\b"
    ],


    # -------------------------
    # Software Development
    # -------------------------

    "Agile": [
        r"\bagile\b"
    ],

    "Scrum": [
        r"\bscrum\b"
    ],
}


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text: str) -> List[str]:
    """
    Extract known skills from a piece of text.

    Parameters:
        text: Resume or job description text.

    Returns:
        List of detected skills.
    """

    text_lower = text.lower()

    found_skills = []

    for skill, patterns in SKILLS.items():

        for pattern in patterns:

            if re.search(pattern, text_lower):

                found_skills.append(skill)

                # Stop checking other patterns
                # for this particular skill.
                break

    return sorted(found_skills)


# ============================================================
# COMPARE SKILLS
# ============================================================

def compare_skills(
    resume_skills: List[str],
    job_skills: List[str]
) -> Dict[str, List[str]]:
    """
    Compare resume skills against job requirements.

    Returns:
        matched
        missing
        extra
    """

    resume_set = set(resume_skills)

    job_set = set(job_skills)

    # Skills present in both
    matched = sorted(
        resume_set.intersection(job_set)
    )

    # Skills required by job but not in resume
    missing = sorted(
        job_set.difference(resume_set)
    )

    # Skills in resume but not required by job
    extra = sorted(
        resume_set.difference(job_set)
    )

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra,
    }


# ============================================================
# MATCH SCORE
# ============================================================

def match_score(
    resume_skills: List[str],
    job_skills: List[str]
) -> float:
    """
    Calculate resume/job skill match percentage.

    Formula:

        matched skills
        ---------------- × 100
        total job skills
    """

    # Avoid division by zero.
    if not job_skills:
        return 0.0

    resume_set = set(resume_skills)

    job_set = set(job_skills)

    matched = len(
        resume_set.intersection(job_set)
    )

    score = (
        matched /
        len(job_set)
    ) * 100

    return round(score, 1)
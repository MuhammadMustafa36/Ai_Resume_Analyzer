import requests


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/chat"

DEFAULT_MODEL = "qwen3:1.7b"


# ============================================================
# GENERATE AI SUGGESTIONS
# ============================================================

def generate_ai_suggestions(
    resume_text: str,
    job_description: str,
    matched: list[str],
    missing: list[str],
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Send resume and job description to Ollama
    and generate improvement suggestions.
    """

    prompt = f"""
You are an expert resume analyzer and career advisor.

Your task is to analyze a candidate's resume
against a job description.

========================
RESUME
========================

{resume_text[:12000]}


========================
JOB DESCRIPTION
========================

{job_description[:10000]}


========================
MATCHED SKILLS
========================

{", ".join(matched) if matched else "None"}


========================
MISSING SKILLS
========================

{", ".join(missing) if missing else "None"}


========================
TASK
========================

Provide practical and honest suggestions.

Use the following sections:

1. Overall Assessment

2. Missing Skills to Prioritize

3. Resume Improvements

4. Project Ideas to Strengthen the Profile

5. Suggested Next Steps


IMPORTANT:

Do not invent experience for the candidate.

Do not claim that the candidate knows
a technology that is not present in the resume.

If a skill is missing, recommend learning it
rather than falsely adding it to the resume.

Keep the answer concise, professional,
and useful for a job applicant.
"""

    # Request body for Ollama.
    payload = {

        "model": model,

        "messages": [

            {
                "role": "user",
                "content": prompt
            }

        ],

        # We want one complete response.
        "stream": False
    }

    # Send request to Ollama.
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    # Raise error if request failed.
    response.raise_for_status()

    # Convert response to Python dictionary.
    data = response.json()

    # Return AI generated text.
    return data["message"]["content"]


# ============================================================
# CHECK OLLAMA
# ============================================================

def ollama_available() -> bool:
    """
    Check whether Ollama is running.
    """

    try:

        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=3
        )

        return response.ok

    except requests.RequestException:

        return False
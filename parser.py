# parser.py
# ---------------------------------------------------------------------------
# PURPOSE:
#   1. Extract raw text from an uploaded PDF resume using PyPDF2.
#   2. Extract skills from any text (resume or job description) by scanning
#      it against the master skills list from skills.py.
#
#   Completely FREE — no API calls, runs locally.
# ---------------------------------------------------------------------------

import re
import PyPDF2
from skills import get_skills_list


# ---------------------------------------------------------------------------
# Skills whose internal capitalization must be preserved before camelCase
# splitting (e.g. "JavaScript" must not become "Java Script").
# Stored in their original display casing; we match them case-insensitively
# in the PDF text.
# ---------------------------------------------------------------------------
_PROTECTED_SKILLS = [
    "JavaScript", "TypeScript", "FastAPI", "GitHub", "GitLab",
    "MySQL", "MongoDB", "PostgreSQL", "MariaDB", "SQLite", "NoSQL",
    "PyCharm", "GraphQL", "TailwindCSS", "NumPy", "SciPy",
    "TensorFlow", "PyTorch", "HuggingFace", "IntelliJ",
    "VSCode", "VS Code",
    # dot-separated variants (already have separators — listed for completeness)
    "Next.js", "Node.js", "React.js", "Vue.js", "Nuxt.js",
    "Express.js", "Angular.js",
]


def _normalize_text(text: str) -> str:
    """
    Normalize raw text (especially PDF-extracted text) for skill matching.

    PDFs often jam section labels directly against the first skill with no
    space, e.g. "ProgrammingPython, Java" or "BackendFlask, FastAPI".
    This function:
      1. Protects known compound-uppercase skill names with placeholders so
         they survive the camelCase split intact.
      2. Splits camelCase boundaries (2+ lowercase letters followed by an
         uppercase letter) by inserting a space — this separates section
         labels from skills.
      3. Lowercases everything.
      4. Restores the protected skill names (in lowercase).
      5. Collapses extra whitespace.

    Args:
        text: Raw text string (from PDF or user input).

    Returns:
        Cleaned, lowercased string ready for skill pattern matching.
    """
    # Step 1: replace protected terms with numeric placeholders
    # We match case-insensitively so "javascript" / "JavaScript" both work.
    placeholders: dict[str, str] = {}
    for i, term in enumerate(_PROTECTED_SKILLS):
        ph = f"ZZP{i}ZZ"
        # Replace all case variants of the term
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        if pattern.search(text):
            placeholders[ph] = term.lower()
            text = pattern.sub(ph, text)

    # Step 2: camelCase split — insert space between (2+ lowercase)(Uppercase)
    # This turns "ProgrammingPython" → "Programming Python"
    #             "BackendFlask"     → "Backend Flask"
    #             "DatabaseMySQL"    → "Database MySQL"  (MySQL was protected)
    text = re.sub(r'([a-z]{2,})([A-Z])', r'\1 \2', text)

    # Step 3: lowercase everything
    text = text.lower()

    # Step 4: restore protected terms (already lowercase)
    for ph, val in placeholders.items():
        text = text.replace(ph.lower(), val)

    # Step 5: normalise whitespace — newlines/tabs → space, collapse multiples
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r' {2,}', ' ', text).strip()

    return text


def _build_skill_pattern(skill: str) -> re.Pattern:
    """
    Build a compiled regex pattern for matching a skill in normalised text.

    Handles:
      - Multi-word skills   ("machine learning", "rest api")
      - Special characters  ("c++", "c#", ".net", "node.js")
      - Short skills        ("r", "c") without false positives inside words

    Boundary rules:
      Left  — start of string OR a non-alphanumeric character
      Right — end of string   OR a non-alphanumeric character
    """
    escaped = re.escape(skill)
    left    = r'(?:(?<=^)|(?<=[^a-zA-Z0-9]))'
    right   = r'(?=[^a-zA-Z0-9]|$)'
    return re.compile(left + escaped + right)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Read every page of the PDF and return all text as one string.

    Args:
        file_path: Path to the PDF file on disk.

    Returns:
        Full text content of the PDF as a single string.

    Raises:
        ValueError: If no readable text is found in the PDF.
        Exception:  For any file reading errors.
    """
    all_text = []

    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)

        if len(reader.pages) == 0:
            raise ValueError("The PDF file appears to be empty.")

        for page_number, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    all_text.append(page_text)
            except Exception as e:
                print(f"[parser] Warning: Could not read page "
                      f"{page_number + 1} — {e}")

    if not all_text:
        raise ValueError(
            "No readable text found in the PDF. "
            "The file may contain only scanned images."
        )

    full_text = "\n".join(all_text)
    print(f"[parser] Extracted {len(full_text)} characters from PDF.")
    return full_text


def extract_skills_from_text(text: str) -> list[str]:
    """
    Scan the given text and return all skills found in the master skills list.

    Args:
        text: Any plain text string (resume text or job description).

    Returns:
        Sorted list of unique skill strings found in the text.
    """
    if not text or not text.strip():
        return []

    normalized = _normalize_text(text)

    skills_list = get_skills_list()

    # Sort longest-first so "react.js" is checked before "react",
    # "spring boot" before "spring", etc.
    skills_sorted = sorted(skills_list, key=len, reverse=True)

    found_skills: set[str] = set()

    for skill in skills_sorted:
        try:
            pattern = _build_skill_pattern(skill)
            if pattern.search(normalized):
                found_skills.add(skill)
        except re.error as e:
            print(f"[parser] Warning: bad pattern for skill '{skill}': {e}")

    result = sorted(list(found_skills))
    print(f"[parser] Found {len(result)} skills in text.")
    return result


def extract_skills_from_job_description(job_description: str) -> list[str]:
    """
    Extract skills from a plain text job description.

    Args:
        job_description: The job description text entered by the user.

    Returns:
        Sorted list of unique skill strings found in the job description.
    """
    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    return extract_skills_from_text(job_description)
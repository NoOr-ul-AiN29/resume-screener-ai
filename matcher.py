# matcher.py
# ---------------------------------------------------------------------------
# PURPOSE:
#   Compare resume skills against job description skills and produce:
#     - Matched skills  (skills present in BOTH resume and job description)
#     - Missing skills  (skills in job description but NOT in resume)
#     - Match percentage (how well the resume fits the job)
#
#   Formula:
#     match_percentage = (matched_skills / total_job_skills) * 100
#
#   Completely FREE — pure Python, no API calls.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Alias map — maps common variations/abbreviations to a canonical skill name.
# This lets "postgres" match "postgresql", "js" match "javascript", etc.
# ---------------------------------------------------------------------------
SKILL_ALIASES: dict[str, str] = {
    # JavaScript variants
    "js":               "javascript",
    "es6":              "javascript",
    "es2015":           "javascript",
    "ecmascript":       "javascript",

    # TypeScript
    "ts":               "typescript",

    # Python
    "py":               "python",

    # Node.js variants
    "node":             "nodejs",
    "node.js":          "nodejs",

    # React variants
    "react":            "reactjs",
    "react.js":         "reactjs",

    # Vue variants
    "vue":              "vuejs",
    "vue.js":           "vuejs",

    # Next.js variants
    "next":             "nextjs",
    "next.js":          "nextjs",

    # PostgreSQL variants
    "postgres":         "postgresql",
    "psql":             "postgresql",

    # MongoDB
    "mongo":            "mongodb",

    # Express variants
    "express":          "expressjs",
    "express.js":       "expressjs",

    # Golang
    "go":               "golang",

    # .NET variants
    "dotnet":           ".net",
    "asp.net":          ".net",

    # C++ / C#
    "cplusplus":        "c++",
    "csharp":           "c#",

    # REST
    "restful":          "rest api",
    "rest":             "rest api",
    "rest apis":        "rest api",

    # Machine Learning
    "ml":               "machine learning",

    # Artificial Intelligence
    "ai":               "artificial intelligence",

    # scikit-learn
    "sklearn":          "scikit-learn",

    # Kubernetes
    "k8s":              "kubernetes",

    # CI/CD
    "ci cd":            "ci/cd",
    "cicd":             "ci/cd",

    # Git/GitHub
    "version control":  "git",

    # OOP
    "oop":              "object oriented programming",
    "object-oriented":  "object oriented programming",

    # NLP
    "nlp":              "natural language processing",

    # UI/UX
    "ui ux":            "ui/ux",
    "ux":               "ux design",
    "ui":               "ui design",

    # TDD
    "tdd":              "test driven development",

    # Data Structures & Algorithms
    "dsa":              "data structures",

    # Large Language Models
    "llms":             "llm",
    "large language models": "llm",
}


def _normalize(skill: str) -> str:
    """
    Normalize a skill string for comparison:
      - Lowercase
      - Strip whitespace
      - Resolve known aliases to their canonical form
    """
    s = skill.strip().lower()
    return SKILL_ALIASES.get(s, s)


def calculate_match(
    resume_skills: list[str],
    job_skills: list[str]
) -> dict:
    """
    Compare resume skills with job description skills and return a full
    match report.

    Improvements over the original:
      - Normalizes all skills through the alias map before comparing, so
        "postgres" matches "postgresql", "js" matches "javascript", etc.
      - The output always uses the canonical job-description skill names
        for consistency.

    Args:
        resume_skills: List of skills extracted from the resume.
        job_skills:    List of skills extracted from the job description.

    Returns:
        A dictionary containing:
            "resume_skills"    — all skills found in the resume (display form)
            "job_skills"       — all skills found in the job description
            "matched_skills"   — skills present in both
            "missing_skills"   — skills in job description but not in resume
            "match_percentage" — float rounded to 2 decimal places
            "match_label"      — human-friendly label
            "total_job_skills" — total number of skills required by the job
            "total_matched"    — total number of matched skills
    """
    # Build normalized lookup sets
    # Maps normalized_form -> original display form (for job skills)
    job_norm_map:    dict[str, str] = {_normalize(s): s for s in job_skills}
    resume_norm_set: set[str]       = {_normalize(s) for s in resume_skills}

    matched: list[str] = []
    missing: list[str] = []

    for norm_key, display_form in job_norm_map.items():
        if norm_key in resume_norm_set:
            matched.append(display_form)
        else:
            missing.append(display_form)

    matched = sorted(matched)
    missing = sorted(missing)

    total_job = len(job_norm_map)

    if total_job == 0:
        match_percentage = 0.0
    else:
        match_percentage = round((len(matched) / total_job) * 100, 2)

    match_label = _get_match_label(match_percentage)

    result = {
        "resume_skills":    sorted(resume_skills),
        "job_skills":       sorted(job_skills),
        "matched_skills":   matched,
        "missing_skills":   missing,
        "match_percentage": match_percentage,
        "match_label":      match_label,
        "total_job_skills": total_job,
        "total_matched":    len(matched),
    }

    print(f"[matcher] Match: {match_percentage}% — "
          f"{len(matched)}/{total_job} skills matched.")
    return result


def _get_match_label(percentage: float) -> str:
    """
    Convert a numeric match percentage into a human-friendly label.

    Args:
        percentage: The match percentage (0–100).

    Returns:
        A string label describing the match quality.
    """
    if percentage >= 80:
        return "Excellent Match 🌟"
    elif percentage >= 60:
        return "Good Match ✅"
    elif percentage >= 40:
        return "Partial Match ⚠️"
    elif percentage >= 20:
        return "Weak Match ❌"
    else:
        return "Poor Match 💔"
# app.py
# ---------------------------------------------------------------------------
# PURPOSE:
#   Main FastAPI application. Run with:
#       uvicorn app:app --reload
#
#   Endpoints:
#     GET  /         — serves the HTML frontend
#     POST /screen   — accepts PDF resume + job description, returns results
#     GET  /health   — simple health check
#
#   No paid APIs used. Everything runs locally for free.
# ---------------------------------------------------------------------------

import os
import shutil

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from dotenv import load_dotenv

from parser import extract_text_from_pdf, extract_skills_from_text, extract_skills_from_job_description
from matcher import calculate_match

# ---------------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------------
load_dotenv()

APP_TITLE   = os.getenv("APP_TITLE", "Resume Screener AI")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# ---------------------------------------------------------------------------
# Directory setup
# ---------------------------------------------------------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title=APP_TITLE,
    description="Upload a resume PDF and match it against a job description.",
    version=APP_VERSION
)

templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """Serve the HTML frontend."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/screen")
async def screen_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Accept a PDF resume and a job description, then return a full match report.

    Steps:
      1. Validate the uploaded file is a PDF.
      2. Save it to the uploads/ directory.
      3. Extract text from the PDF.
      4. Extract skills from the resume text.
      5. Extract skills from the job description.
      6. Compare and calculate match percentage.
      7. Return the full report as JSON.

    Args:
        resume:          The uploaded PDF resume file.
        job_description: The job description text from the form.

    Returns:
        JSON with resume_skills, job_skills, matched_skills,
        missing_skills, match_percentage, and match_label.
    """
    # ------------------------------------------------------------------ #
    # Step 1: Validate file type
    # ------------------------------------------------------------------ #
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted. Please upload a .pdf resume."
        )

    # ------------------------------------------------------------------ #
    # Step 2: Validate job description
    # ------------------------------------------------------------------ #
    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    # ------------------------------------------------------------------ #
    # Step 3: Save uploaded PDF to disk
    # ------------------------------------------------------------------ #
    save_path = os.path.join(UPLOAD_DIR, resume.filename)

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        print(f"[app] Resume saved to '{save_path}'.")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded file: {str(e)}"
        )

    # ------------------------------------------------------------------ #
    # Step 4: Extract text from PDF
    # ------------------------------------------------------------------ #
    try:
        resume_text = extract_text_from_pdf(save_path)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read PDF: {str(e)}"
        )

    # ------------------------------------------------------------------ #
    # Step 5: Extract skills from resume
    # ------------------------------------------------------------------ #
    try:
        resume_skills = extract_skills_from_text(resume_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract skills from resume: {str(e)}"
        )

    # ------------------------------------------------------------------ #
    # Step 6: Extract skills from job description
    # ------------------------------------------------------------------ #
    try:
        job_skills = extract_skills_from_job_description(job_description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract skills from job description: {str(e)}"
        )

    # ------------------------------------------------------------------ #
    # Step 7: Calculate match
    # ------------------------------------------------------------------ #
    try:
        result = calculate_match(resume_skills, job_skills)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate match: {str(e)}"
        )

    # ------------------------------------------------------------------ #
    # Clean up — remove uploaded file after processing
    # ------------------------------------------------------------------ #
    try:
        os.remove(save_path)
    except Exception:
        pass  # Non-critical — don't fail the response over cleanup

    return JSONResponse(content=result)


@app.get("/health")
async def health_check():
    """Simple health check."""
    return JSONResponse(content={
        "status": "ok",
        "message": f"{APP_TITLE} is running."
    })
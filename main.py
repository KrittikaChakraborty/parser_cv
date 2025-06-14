from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from parser import parse_resume
from matcher import compute_final_score
from fpdf import FPDF
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

last_data = {}

@app.post("/parse-resume")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    parsed_data, resume_text = parse_resume(contents, file.filename)

    # Example JD
    jd_text = "We are looking for a Python developer with SQL, HTML, CSS, teamwork, and communication skills."

    # Match score (semantic + skill-based)
    match_score = compute_final_score(resume_text, parsed_data["skills"], jd_text)
    parsed_data["match_score"] = match_score

    global last_data
    last_data = parsed_data

    return {
        "resume_data": parsed_data,
        "match_score": parsed_data["match_score"]
    }

@app.get("/download-pdf")
async def download_pdf():
    if not last_data:
        return {"error": "No data found"}

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Resume Parser Results", ln=True, align="C")
    pdf.ln(10)

    for key, val in last_data.items():
        if isinstance(val, list):
            val = ", ".join(val)
        pdf.cell(200, 10, txt=f"{key.capitalize()}: {val}", ln=True)

    os.makedirs("output", exist_ok=True)
    path = f"output/result_{uuid.uuid4().hex[:6]}.pdf"
    pdf.output(path)

    return FileResponse(path, media_type="application/pdf", filename="parsed_resume.pdf")

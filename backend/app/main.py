from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.scanner import scan_dependencies  # <-- new import

# --- App instance ---
app = FastAPI(title="Attestation Policy Enforcer API")

# --- Models ---
class LicenseReport(BaseModel):
    detected: List[str]
    violations: List[str]
    compliance_score: float  # percentage 0–100


# --- Health check route ---
@app.get("/health")
def health_check():
    """
    Simple endpoint to verify the backend is running.
    Useful for CI/CD, monitoring, and debugging.
    """
    return {"status": "ok"}


# --- Root route ---
@app.get("/")
def root():
    return {"message": "Attestation API running 🚀"}


# --- Real scan route with file upload ---
@app.post("/scan", response_model=LicenseReport)
async def scan_project(file: UploadFile = File(...)):
    """
    Accepts a dependency file (like requirements.txt or package.json),
    scans it for allowed/forbidden licenses, and returns a compliance score.
    """
    # Read uploaded file
    content = await file.read()
    text = content.decode("utf-8")

    # Run scanner logic
    result = scan_dependencies(text)

    # Simple scoring logic
    compliance_score = 100 - (len(result["violations"]) * 20)
    compliance_score = max(compliance_score, 0)

    # Return structured report
    return LicenseReport(
        detected=result["detected"],
        violations=result["violations"],
        compliance_score=compliance_score
    )

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.scanner import scan_dependencies
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Attestation Policy Enforcer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    file_name: str
    file_content: str

class LicenseReport(BaseModel):
    detected: List[str]
    violations: List[str]
    compliance_score: float

@app.post("/scan", response_model=LicenseReport)
def scan_project(req: ScanRequest):
    result = scan_dependencies(req.file_name, req.file_content)

    compliance_score = 100 - (len(result["violations"]) * 20)
    compliance_score = max(compliance_score, 0)

    return LicenseReport(
        detected=result["detected"],
        violations=result["violations"],
        compliance_score=compliance_score
    )

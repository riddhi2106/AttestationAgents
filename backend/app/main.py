from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Attestation Policy Enforcer API")

# --- Models ---
class LicenseReport(BaseModel):
    allowed_licenses: List[str]
    violations: List[str]
    compliance_score: float  # percentage 0–100

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Attestation API running 🚀"}

@app.post("/scan", response_model=LicenseReport)
def scan_project():
    """
    Simulated license scan endpoint.
    Later this will analyze dependencies or upload a manifest file.
    """
    fake_data = LicenseReport(
        allowed_licenses=["MIT", "Apache-2.0", "BSD-3-Clause"],
        violations=["GPL-3.0", "LGPL-2.1"],
        compliance_score=82.5
    )
    return fake_data

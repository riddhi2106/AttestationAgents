import typer
import requests
import os

def scan(file_path: str):
    """
    Scan a user-provided dependency file for license compliance.
    """
    if not os.path.isfile(file_path):
        print(f"❌ File does not exist: {file_path}")
        raise typer.Exit(1)

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        response = requests.post("http://127.0.0.1:8000/scan", files=files)
    
    response.raise_for_status()
    data = response.json()
    print("✅ Scan complete!")
    print(f"Detected licenses: {data['detected']}")
    print(f"Violations: {data['violations']}")
    print(f"Compliance score: {data['compliance_score']}%")

if __name__ == "__main__":
    typer.run(scan)  # <-- runs a single command CLI

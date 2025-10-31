import typer
import requests

app = typer.Typer()

BACKEND_URL = "http://127.0.0.1:8000"

@app.command()
def scan(project_path: str = typer.Argument(..., help="Path to the project")):
    """
    Simulate scanning a project for license compliance.
    """
    typer.echo(f"Scanning project at {project_path}...")
    try:
        response = requests.post(f"{BACKEND_URL}/scan")
        response.raise_for_status()
        data = response.json()
        typer.echo("✅ Scan complete!")
        typer.echo(f"Allowed licenses: {data['allowed_licenses']}")
        typer.echo(f"Violations: {data['violations']}")
        typer.echo(f"Compliance score: {data['compliance_score']}%")
    except Exception as e:
        typer.echo(f"❌ Error contacting backend: {e}")

if __name__ == "__main__":
    app()

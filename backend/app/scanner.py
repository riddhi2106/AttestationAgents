# backend/app/scanner.py
import re
from typing import Dict, List

# Fake license detection pattern
LICENSE_PATTERNS = {
    "MIT": re.compile(r"MIT", re.IGNORECASE),
    "Apache-2.0": re.compile(r"Apache", re.IGNORECASE),
    "GPL-3.0": re.compile(r"GPL", re.IGNORECASE),
}

FORBIDDEN_LICENSES = ["GPL-3.0", "AGPL-3.0"]

def scan_dependencies(file_content: str) -> Dict[str, List[str]]:
    """
    Simulated license scanner.
    Input: file content as string (e.g., requirements.txt or package.json)
    Output: dictionary of detected and forbidden licenses
    """
    detected = []

    for name, pattern in LICENSE_PATTERNS.items():
        if pattern.search(file_content):
            detected.append(name)

    violations = [lic for lic in detected if lic in FORBIDDEN_LICENSES]

    return {
        "detected": detected or ["Unknown"],
        "violations": violations,
    }

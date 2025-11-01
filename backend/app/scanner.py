import re
import json
import requests
import xml.etree.ElementTree as ET
from typing import Dict, List

FORBIDDEN_LICENSES = ["GPL-3.0", "AGPL-3.0"]

# ---------- npm ----------
def detect_from_package_json(content: str) -> Dict[str, List[str]]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return {"detected": ["Unknown"], "violations": []}

    detected = []
    if "license" in data:
        detected.append(data["license"])

    deps = data.get("dependencies", {})
    for name in deps.keys():
        try:
            res = requests.get(f"https://registry.npmjs.org/{name}/latest", timeout=3)
            license = res.json().get("license")
            if license:
                detected.append(license)
        except Exception:
            continue

    # Extra heuristic: look for "MIT", "Apache", etc. in text as fallback
    for keyword in ["MIT", "Apache", "BSD", "ISC", "GPL", "MPL", "LGPL"]:
        if re.search(keyword, content, re.IGNORECASE):
            detected.append(keyword)

    detected = list(set(detected))
    violations = [lic for lic in detected if lic in FORBIDDEN_LICENSES]
    return {"detected": detected or ["Unknown"], "violations": violations}


# ---------- Python ----------
def detect_from_requirements_txt(content: str) -> Dict[str, List[str]]:
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")]
    detected = []
    for line in lines:
        pkg_name = re.split(r"[=<>]", line)[0]
        try:
            res = requests.get(f"https://pypi.org/pypi/{pkg_name}/json", timeout=3)
            data = res.json()
            license = data["info"].get("license")
            if license and len(license) < 100:
                detected.append(license)
        except Exception:
            continue

    # Fallback: keyword search
    for keyword in ["MIT", "Apache", "BSD", "ISC", "GPL", "MPL", "LGPL"]:
        if re.search(keyword, content, re.IGNORECASE):
            detected.append(keyword)

    detected = list(set(detected))
    violations = [lic for lic in detected if lic in FORBIDDEN_LICENSES]
    return {"detected": detected or ["Unknown"], "violations": violations}


# ---------- Java (Maven) ----------
def detect_from_pom_xml(content: str) -> Dict[str, List[str]]:
    detected = []
    try:
        root = ET.fromstring(content)
        for license_tag in root.findall(".//license//name"):
            if license_tag.text:
                detected.append(license_tag.text.strip())
    except Exception:
        pass

    # Fallback: scan for keywords in text
    for keyword in ["Apache", "MIT", "BSD", "GPL", "LGPL", "MPL", "ISC"]:
        if re.search(keyword, content, re.IGNORECASE):
            detected.append(keyword)

    detected = list(set(detected))
    violations = [lic for lic in detected if lic in FORBIDDEN_LICENSES]
    return {"detected": detected or ["Unknown"], "violations": violations}


# ---------- Go ----------
def detect_from_go_mod(content: str) -> Dict[str, List[str]]:
    detected = []
    lines = [l.strip() for l in content.splitlines() if l and not l.startswith("//")]

    fallback_patterns = {
        "MIT": re.compile(r"MIT", re.IGNORECASE),
        "Apache-2.0": re.compile(r"Apache", re.IGNORECASE),
        "BSD": re.compile(r"BSD", re.IGNORECASE),
        "MPL-2.0": re.compile(r"MPL", re.IGNORECASE),
        "ISC": re.compile(r"ISC", re.IGNORECASE),
        "GPL-3.0": re.compile(r"GPL", re.IGNORECASE),
    }

    for name, pat in fallback_patterns.items():
        if any(pat.search(line) for line in lines):
            detected.append(name)

    # Heuristic: infer from known domains
    for line in lines:
        if "require" in line or "replace" in line:
            if "golang.org" in line:
                detected.append("BSD")
            elif "google" in line:
                detected.append("Apache-2.0")
            elif "github.com" in line:
                detected.append("MIT")

    detected = list(set(detected)) or ["Unknown"]
    violations = [lic for lic in detected if lic in FORBIDDEN_LICENSES]
    return {"detected": detected, "violations": violations}


# ---------- Rust ----------
def detect_from_cargo_toml(content: str) -> Dict[str, List[str]]:
    detected = []
    for line in content.splitlines():
        if line.lower().startswith("license"):
            lic = line.split("=")[1].strip().replace('"', '')
            detected.append(lic)

    # Fallback heuristic: keywords
    for keyword in ["MIT", "Apache", "BSD", "GPL", "LGPL", "MPL", "ISC"]:
        if re.search(keyword, content, re.IGNORECASE):
            detected.append(keyword)

    detected = list(set(detected))
    violations = [lic for lic in detected if lic in FORBIDDEN_LICENSES]
    return {"detected": detected or ["Unknown"], "violations": violations}


# ---------- Fallback regex ----------
def detect_from_text(content: str) -> Dict[str, List[str]]:
    patterns = {
        "MIT": re.compile(r"MIT", re.IGNORECASE),
        "Apache-2.0": re.compile(r"Apache", re.IGNORECASE),
        "GPL-3.0": re.compile(r"GPL", re.IGNORECASE),
        "BSD": re.compile(r"BSD", re.IGNORECASE),
        "ISC": re.compile(r"ISC", re.IGNORECASE),
        "MPL": re.compile(r"MPL", re.IGNORECASE),
        "LGPL": re.compile(r"LGPL", re.IGNORECASE),
        "Unlicense": re.compile(r"Unlicense", re.IGNORECASE),
        "CC0-1.0": re.compile(r"CC0", re.IGNORECASE),
    }
    detected = [name for name, pat in patterns.items() if pat.search(content)]
    violations = [lic for lic in detected if lic in FORBIDDEN_LICENSES]
    return {"detected": detected or ["Unknown"], "violations": violations}


# ---------- Master function ----------
def scan_dependencies(file_name: str, file_content: str) -> Dict[str, List[str]]:
    """
    Detect license info based on file type.
    Supports: package.json, requirements.txt, pom.xml, go.mod, Cargo.toml, fallback text.
    """
    if file_name.endswith("package.json"):
        return detect_from_package_json(file_content)
    elif file_name.endswith("requirements.txt"):
        return detect_from_requirements_txt(file_content)
    elif file_name.endswith("pom.xml"):
        return detect_from_pom_xml(file_content)
    elif file_name.endswith("go.mod"):
        return detect_from_go_mod(file_content)
    elif file_name.endswith("Cargo.toml"):
        return detect_from_cargo_toml(file_content)
    else:
        return detect_from_text(file_content)

from __future__ import annotations

from pathlib import Path
import re
import csv


def load_skills(csv_path: str) -> list[str]:
    path = Path(csv_path)

    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [x.strip() for x in lines if x.strip()]

    skills: list[str] = []

    first = lines[0].lower() if lines else ""
    looks_like_header = ("skill" in first) and ("," in first)

    if looks_like_header:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                s = (row.get("skill") or "").strip()
                if s:
                    skills.append(s)
    else:
        for line in lines:
            if line.startswith("#"):
                continue
            skills.append(line)

    skills = [s.lower() for s in skills]
    skills = sorted(set(skills), key=len, reverse=True)
    return skills


def extract_skills(text: str, skills: list[str]) -> list[str]:
    t = (text or "").lower()
    found: list[str] = []

    for s in skills:
        if s in {"c#", ".net"}:
            if s in t:
                found.append(s)
            continue

        pattern = r"\b" + re.escape(s) + r"\b"
        if re.search(pattern, t):
            found.append(s)

    return sorted(set(found))

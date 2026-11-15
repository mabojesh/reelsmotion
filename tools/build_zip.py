"""Build motion-abojesh.zip (repo root, committed so the README link works) for the Claude app (Settings > Skills). Run from the repo root:  python tools/build_zip.py"""
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
skill = root / "skills/motion-abojesh"
out = root / "motion-abojesh.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(skill.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            z.write(f, Path("motion-abojesh") / f.relative_to(skill))
print(out, out.stat().st_size // 1024, "KB")

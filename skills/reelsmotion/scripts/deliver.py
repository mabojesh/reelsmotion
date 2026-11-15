"""Copy a finished file into the workspace's final/ folder. Never overwrites: adds (2), (3)... if the name is taken.

  python deliver.py renders/final.mp4 --name "صح ولا غلط v1" [--no-open]
  python deliver.py renders/cover.png renders/youtube.txt --name "صح ولا غلط"   (several files: name + " - " + original stem)
"""
import argparse, os, shutil, subprocess, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def workspace(start: Path):
    for p in [start, *start.parents]:
        if (p / "final").is_dir() and (p / "ideas").is_dir():
            return p
    sys.exit("No workspace with final/ found above this folder.")


def free_name(folder: Path, stem: str, ext: str):
    p = folder / f"{stem}{ext}"
    n = 2
    while p.exists():
        p = folder / f"{stem} ({n}){ext}"; n += 1
    return p


def reveal(p: Path):
    try:
        if os.name == "nt":
            subprocess.run(["explorer", "/select,", str(p)])
        elif sys.platform == "darwin":
            subprocess.run(["open", "-R", str(p)])
        else:
            subprocess.run(["xdg-open", str(p.parent)])
    except Exception:
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--name")
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    out = workspace(Path.cwd().resolve()) / "final"
    last = None
    for f in map(Path, a.files):
        if not f.is_file():
            sys.exit(f"missing: {f}")
        if a.name and len(a.files) == 1:
            stem = a.name
        elif a.name:
            stem = f"{a.name} - {f.stem}"
        else:
            stem = f.stem
        dest = free_name(out, stem, f.suffix)
        shutil.copy2(f, dest)
        print("delivered:", dest)
        last = dest
    if last and not a.no_open:
        reveal(last)

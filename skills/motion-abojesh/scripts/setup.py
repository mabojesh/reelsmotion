"""motion_abojesh workspace setup.

  python setup.py --check                          what is installed (changes nothing)
  python setup.py --folder "<path>" [--install-skill]   build the workspace in <path>

Never overwrites the user's files: existing CLAUDE.md gets a marked section added once,
existing brand.md / HANDOFF.md are left alone.
"""
import argparse, datetime, os, shutil, subprocess, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL = Path(__file__).resolve().parent.parent
NAME = "motion-abojesh"
MARK_A, MARK_B = "<!-- motion-abojesh:start -->", "<!-- motion-abojesh:end -->"


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=(os.name == "nt"))
        return (r.stdout or r.stderr).strip().splitlines()[0] if r.returncode == 0 else None
    except Exception:
        return None


def find_browser():
    cands = []
    if os.name == "nt":
        for base in (os.environ.get("PROGRAMFILES(X86)", ""), os.environ.get("PROGRAMFILES", ""), os.environ.get("LOCALAPPDATA", "")):
            cands += [Path(base) / "Microsoft/Edge/Application/msedge.exe", Path(base) / "Google/Chrome/Application/chrome.exe"]
    elif sys.platform == "darwin":
        cands += [Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                  Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")]
    for c in cands:
        if c.is_file():
            return str(c)
    for n in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        p = shutil.which(n)
        if p:
            return p
    return None


def check():
    node = run(["node", "--version"])
    major = int(node.lstrip("v").split(".")[0]) if node else 0
    try:
        import numpy  # noqa: F401
        np_ok = True
    except Exception:
        np_ok = False
    rows = [
        ("Python", sys.version.split()[0], True),
        ("Node 22+ (HyperFrames)", node or "missing", major >= 22),
        ("FFmpeg", "ok" if run(["ffmpeg", "-version"]) else "missing", bool(run(["ffmpeg", "-version"]))),
        ("numpy (sounds)", "ok" if np_ok else "missing: pip install numpy", np_ok),
        ("Browser (covers, carousels)", "ok" if find_browser() else "missing: Edge or Chrome", bool(find_browser())),
    ]
    for name, val, ok in rows:
        print(("OK   " if ok else "NEED ") + f"{name}: {val}")
    return all(ok for *_, ok in rows)


CLAUDE_SECTION = f"""{MARK_A}
## motion_abojesh (read in every chat)
This folder is a video workspace for the `motion-abojesh` skill (in `.claude/skills/motion-abojesh/`, keep it here only).
- The user only uses `studio/` (their clips and voice), `ideas/` (what they like, one sub-folder per topic, their identity in `ideas/brand/`) and `final/` (finished work).
- Never ask them to create, move, rename or open files. Do it and say so in one line.
- Use the skill for anything about videos, reels, carousels, covers or «كمّل».
- Reply in their language, short and simple.
- Start of every chat: read `HANDOFF.md`. After every reply that changed something: merge the change into it and end with «📌 حفظت وين وقفنا»; otherwise «📌 ما فيه جديد للحفظ».
- Never write API keys or passwords in any file here.
{MARK_B}
"""

HANDOFF = """# وين وقفنا
آخر تحديث: {date}

## الهدف
(شو بدنا نعمل بهالمجلد)

## الفيديوهات
| الفيديو | المجلد | الحالة | في final |
|---|---|---|---|

## قرارات صاحب المجلد
- (اللي قاله أو وافق عليه بس)

## كمّل من هنا
- أول شي: نكمّل التعارف (الاسم، اليوزر، الألوان والخط) ونعمل أول فيديو قصير.
"""


def build(folder: Path, install_skill: bool):
    folder = folder.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    made = []
    for sub in ("studio", "ideas", "ideas/brand/fonts", "final", ".motion/projects"):
        p = folder / sub
        if not p.exists():
            p.mkdir(parents=True)
            made.append(sub)

    brand = folder / "ideas/brand/brand.md"
    if not brand.exists():
        shutil.copy2(SKILL / "examples/brand-starter.md", brand)
        made.append("ideas/brand/brand.md")
    fonts = folder / "ideas/brand/fonts"
    if not any(fonts.iterdir()):
        for f in (SKILL / "assets/fonts").iterdir():
            shutil.copy2(f, fonts / f.name)
        made.append("ideas/brand/fonts (IBM Plex Sans Arabic)")

    handoff = folder / "HANDOFF.md"
    if not handoff.exists():
        handoff.write_text(HANDOFF.format(date=datetime.date.today().isoformat()), encoding="utf-8")
        made.append("HANDOFF.md")

    cm = folder / "CLAUDE.md"
    old = cm.read_text(encoding="utf-8") if cm.exists() else ""
    if MARK_A not in old:
        cm.write_text((old.rstrip() + "\n\n" if old else "") + CLAUDE_SECTION, encoding="utf-8")
        made.append("CLAUDE.md")

    if install_skill:
        dest = folder / ".claude/skills" / NAME
        if dest.resolve() != SKILL:
            if dest.exists():
                # keep the old copy OUTSIDE .claude/skills, or Claude would load two skills with one name
                backup = folder / ".motion/backup" / f"{NAME}-{datetime.datetime.now():%Y%m%d-%H%M%S}"
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dest), str(backup))
                made.append(f"old skill kept in .motion/backup/{backup.name}")
            shutil.copytree(SKILL, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            made.append(f".claude/skills/{NAME}")

    print("workspace:", folder)
    print("made:", ", ".join(made) if made else "nothing new (already set up)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--folder")
    ap.add_argument("--install-skill", action="store_true")
    a = ap.parse_args()
    if a.check or not a.folder:
        ok = check()
        if not a.folder:
            sys.exit(0 if ok else 1)
    build(Path(a.folder), a.install_skill)

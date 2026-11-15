"""Make a new video project from the template, with the workspace brand.

  python new_video.py --title "صح ولا غلط" [--slug car-quiz] [--format reel|square|wide|still] [--workspace PATH]

Creates <workspace>/.motion/projects/<YYYY-MM-DD>-<slug>/ and prints its path.
"""
import argparse, datetime, re, shutil, sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL = Path(__file__).resolve().parent.parent
SIZES = {"reel": (1080, 1920), "square": (1080, 1080), "wide": (1920, 1080)}
DEFAULT = {"bg": "#ffffff", "ink": "#0a0a0a", "muted": "#8a8a8a", "accent": "#0a0a0a",
           "name": "", "handle": "", "tagline": ""}


def find_workspace(start: Path):
    for p in [start, *start.parents]:
        if (p / "ideas/brand").is_dir() or (p / ".motion").is_dir():
            return p
    return None


def read_brand(ws: Path):
    """Reads simple `key: value` lines from ideas/brand/brand.md."""
    b = dict(DEFAULT)
    f = ws / "ideas/brand/brand.md"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*-?\s*(bg|ink|muted|accent|name|handle|tagline|logo)\s*:\s*(.+?)\s*$", line)
            if m and not m.group(2).startswith("("):
                b[m.group(1)] = m.group(2)
    b["LOGO"] = b.get("logo") or (b["name"][:1] if b["name"] else "●")
    b.pop("logo", None)
    return b


def pick_fonts(ws: Path, dest: Path):
    """display = Bold, body = Regular, light = Light from ideas/brand/fonts, else the skill's IBM Plex."""
    srcs = [ws / "ideas/brand/fonts", SKILL / "assets/fonts"]
    want = {"display.ttf": ["bold", "black", "heavy", "semibold"], "body.ttf": ["regular", "book", "medium"], "light.ttf": ["light", "thin", "regular"]}
    dest.mkdir(parents=True, exist_ok=True)
    for out, keys in want.items():
        for src in srcs:
            files = sorted([f for f in src.glob("*") if f.suffix.lower() in (".ttf", ".otf")]) if src.is_dir() else []
            hit = next((f for k in keys for f in files if k in f.stem.lower().replace("-", "")), None)
            if hit:
                shutil.copy2(hit, dest / out)
                break
    for lic in (ws / "ideas/brand/fonts").glob("*.txt"):
        shutil.copy2(lic, dest / lic.name)


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "video"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--slug")
    ap.add_argument("--format", default="reel", choices=["reel", "square", "wide", "still"])
    ap.add_argument("--workspace")
    a = ap.parse_args()

    ws = Path(a.workspace).resolve() if a.workspace else find_workspace(Path.cwd())
    if not ws:
        sys.exit("No workspace found. Run setup.py --folder first.")
    slug = a.slug or slugify(a.title)
    proj = ws / ".motion/projects" / f"{datetime.date.today():%Y-%m-%d}-{slug}"
    n = 2
    while proj.exists():
        proj = proj.with_name(f"{datetime.date.today():%Y-%m-%d}-{slug}-{n}"); n += 1

    brand = read_brand(ws)
    if a.format == "still":
        shutil.copytree(SKILL / "templates/still", proj)
    else:
        shutil.copytree(SKILL / "templates/video", proj)
        w, h = SIZES[a.format]
        for f in [proj / "index.html", proj / "compositions/scenes.html"]:
            t = f.read_text(encoding="utf-8")
            t = t.replace("{{W}}", str(w)).replace("{{H}}", str(h))
            f.write_text(t, encoding="utf-8")
    for f in proj.rglob("*.html"):
        t = f.read_text(encoding="utf-8")
        for k, v in brand.items():
            t = t.replace("{{" + k + "}}", v)
        t = t.replace("{{TITLE}}", a.title)
        f.write_text(t, encoding="utf-8")
    pick_fonts(ws, proj / "assets/fonts")
    for d in ("plan", "renders", "cache"):
        (proj / d).mkdir(exist_ok=True)
    (proj / "PROGRESS.md").write_text(
        f"# {a.title}\nبدأ: {datetime.date.today()} · الشكل: {a.format}\n\n## الحالة\n- انعمل المجلد من القالب.\n\n## التالي\n- الخطة: الهوك والنص.\n",
        encoding="utf-8")
    print(proj)

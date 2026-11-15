"""Turn an HTML page into a PNG or a PDF with the Edge/Chrome already on the computer (headless).

  python shoot.py cover.html renders/cover.png --size 1080x1920 [--hash v]
  python shoot.py carousel.html renders/page.png --size 1080x1350 --pages 7   (page-1.png ... page-7.png, via #p1..#p7)
  python shoot.py carousel.html renders/carousel.pdf --pdf

For --pages, the page shows only the page named in the URL hash (#p1, #p2...). The still template does this.
For --pdf, the HTML sets @page { size: ...; margin: 0 } and one .page per sheet.
"""
import argparse, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from setup import find_browser  # noqa: E402


def wait_for(path, secs=30):
    """Edge on Windows can return before the file is written; wait until it exists and stops growing."""
    p = Path(path); last = -1
    for _ in range(secs * 4):
        if p.is_file() and p.stat().st_size == last and last > 0:
            return True
        last = p.stat().st_size if p.is_file() else -1
        time.sleep(.25)
    return p.is_file()


def shot(browser, url, out, w, h):
    Path(out).unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}",
                        "--force-device-scale-factor=1", "--virtual-time-budget=3000", "--allow-file-access-from-files",
                        f"--window-size={w},{h}", f"--screenshot={out}", url], capture_output=True, timeout=120)
    if not wait_for(out):
        sys.exit(f"failed: {out}")
    print("ok", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("out")
    ap.add_argument("--size", default="1080x1920"); ap.add_argument("--hash", default="")
    ap.add_argument("--pages", type=int, default=0); ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    browser = find_browser() or sys.exit("No Edge or Chrome found.")
    url = Path(a.html).resolve().as_uri()
    out = Path(a.out).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    if a.pdf:
        out.unlink(missing_ok=True)
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
            subprocess.run([browser, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                            "--virtual-time-budget=3000", "--allow-file-access-from-files", f"--print-to-pdf={out}", url],
                           capture_output=True, timeout=180)
        ok = wait_for(out, 60)
        print("ok" if ok else "failed", out); sys.exit(0 if ok else 1)
    w, h = map(int, a.size.lower().split("x"))
    if a.pages:
        for i in range(1, a.pages + 1):
            shot(browser, f"{url}#p{i}", str(out.with_name(f"{out.stem}-{i}{out.suffix}")), w, h)
    else:
        shot(browser, url + (f"#{a.hash}" if a.hash else ""), str(out), w, h)

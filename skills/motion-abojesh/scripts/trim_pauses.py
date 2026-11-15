"""Shorten long pauses in the user's own voice-over, without changing its speed or pitch.

  python trim_pauses.py studio/vo.m4a assets/voice.wav [--keep 0.2] [--min 0.35] [--tail 1.0] [--db -32]

Pauses longer than --min seconds become --keep seconds (half kept on each side, so no word is cut).
Leading silence is removed; --tail seconds stay after the last word. Writes 48 kHz WAV and prints the cuts.
If a word sounds clipped, run again with a lower --db (e.g. -36).
"""
import argparse, re, subprocess, sys


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def silences(path, db, mn):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise={db}dB:d={mn}", "-f", "null", "-"],
                       capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--keep", type=float, default=0.2)
    ap.add_argument("--min", type=float, default=0.35)
    ap.add_argument("--tail", type=float, default=1.0)
    ap.add_argument("--db", type=float, default=-32)
    a = ap.parse_args()

    total = duration(a.src)
    sil = silences(a.src, a.db, a.min)
    keep, pos = [], 0.0
    for s, e in sil:
        if e is None:  # silence runs to the end: keep the tail
            keep.append((pos, min(total, s + a.tail))); pos = total; break
        if s <= 0.01:  # leading silence: start a little before the first word
            pos = max(0.0, e - 0.05); continue
        keep.append((pos, s + a.keep / 2)); pos = e - a.keep / 2
    if pos < total:
        keep.append((pos, total))
    keep = [(round(x, 3), round(y, 3)) for x, y in keep if y - x > 0.01]

    parts = "".join(f"[0:a]atrim={x}:{y},asetpts=PTS-STARTPTS[a{i}];" for i, (x, y) in enumerate(keep))
    graph = parts + "".join(f"[a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", a.src, "-filter_complex", graph,
                    "-map", "[out]", "-ar", "48000", a.out], check=True)
    new = duration(a.out)
    print(f"{total:.2f}s -> {new:.2f}s, {len(keep)} pieces")
    for x, y in keep:
        print(f"  keep {x:.2f}-{y:.2f}")

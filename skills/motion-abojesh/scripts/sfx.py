"""Sound effects made on the computer (no downloads, no licences), a light music bed, and the final mix.

  python sfx.py list
  python sfx.py one whoosh out.wav [--dur 0.4] [--freq 900]
  python sfx.py mix plan/cues.json assets/mix.wav --duration 30 [--music 150] [--duck 2.8-5.3,7.6-10.1]
                    [--voice assets/voice.wav] [--seed 7] [--no-master]

cues.json: [{"t": 0.0, "sfx": "boom", "db": -8, "pan": 0, "dur": 0.9, "freq": 900}, ...]  (pan, dur, freq optional)
The mix is mastered with FFmpeg to about -14 LUFS, true peak under -1 dB. Needs numpy.
"""
import argparse, json, os, subprocess, sys, tempfile, wave

try:
    import numpy as np
except ImportError:
    sys.exit("numpy is missing: pip install numpy")

SR = 48000
rng = np.random.default_rng(7)


# ---------- building blocks ----------
def t_(n): return np.arange(n) / SR
def env(n, a=.003, d=.2):
    t = t_(n); return np.minimum(t / a, 1) * np.exp(-t / d)
def onepole(x, k):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc); y[i] = acc
    return y
def noise(n): return rng.standard_normal(n)
def sweep(f, n):
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def tone(f, dur, a=.002, d=.2):
    n = int(dur * SR); return np.sin(2 * np.pi * f * t_(n)) * env(n, a, d)


# ---------- the sounds ----------
def s_boom(dur=.9, freq=95):
    n = int(dur * SR); t = t_(n); f = 40 + (freq - 40) * np.exp(-t / .08)
    return sweep(f, n) * env(n, .002, .3) + .3 * onepole(noise(n), .08) * env(n, .001, .03)
def s_slam(dur=.35, freq=230):
    n = int(dur * SR); t = t_(n); f = 60 + (freq - 60) * np.exp(-t / .03)
    return sweep(f, n) * env(n, .001, .11) + .5 * onepole(noise(n), .35) * env(n, .001, .025)
def s_whoosh(dur=.4, freq=0):
    n = int(dur * SR); t = t_(n); shape = np.sin(np.pi * (t / dur) ** .6) ** 2
    x = noise(n); y = np.empty(n); acc = 0.0
    for i in range(n):
        acc += (.02 + .25 * shape[i]) * (x[i] - acc); y[i] = acc
    return y * shape
def s_riser(dur=1.2, freq=0):
    n = int(dur * SR); t = t_(n); shape = (t / dur) ** 2
    x = noise(n); y = np.empty(n); acc = 0.0
    for i in range(n):
        acc += (.01 + .4 * shape[i]) * (x[i] - acc); y[i] = acc
    f = 200 + 1400 * shape
    return (y * .7 + .3 * sweep(f, n)) * shape * np.minimum((dur - t) / .02, 1)
def s_pop(dur=.09, freq=900):
    n = int(dur * SR); t = t_(n); f = freq * (1 + .6 * np.exp(-t / .01))
    return sweep(f, n) * env(n, .001, .025)
def s_click(dur=.03, freq=0):
    n = int(dur * SR); x = noise(n); return (x - onepole(x, .3)) * env(n, .0003, .004)
def s_tick(dur=.16, freq=880):
    n = int(.06 * SR); x = noise(n)
    click = (x - onepole(x, .2)) * env(n, .0004, .006)
    b = tone(freq, dur, .002, .05); b[:n] += click * 1.5
    return b
def s_beep(dur=.18, freq=1175):
    return tone(freq, dur, .003, .08) + .25 * tone(freq * 2, dur, .003, .05)
def s_buzzer(dur=.46, freq=196):
    out = []
    for f, d in [(freq, dur * .35), (freq * .75, dur * .65)]:
        n = int(d * SR); t = t_(n)
        sq = np.sign(np.sin(2 * np.pi * f * t)) * .5 + np.sin(4 * np.pi * f * t) * .3
        out.append(onepole(sq, .25) * np.minimum(t / .005, 1) * np.minimum((d - t) / .02, 1))
    return np.concatenate(out)
def s_ding(dur=1.0, freq=1046.5):
    s = np.zeros(int(dur * SR))
    for k, m in enumerate([1, 1.26, 1.5, 2]):
        b = tone(freq * m, dur - .1 - k * .1, .002, .28); h = tone(freq * m * 2, .4, .002, .12); b[:len(h)] += .3 * h
        i = int(k * .06 * SR); s[i:i + len(b)] += b[:len(s) - i]
    return s
def s_shimmer(dur=1.0, freq=1318):
    n = int(dur * SR); t = t_(n); s = np.zeros(n)
    for k, m in enumerate([1, 1.335, 2, 2.67]):
        s += np.sin(2 * np.pi * freq * m * t + k) * np.exp(-t / (.25 + .1 * k)) * np.minimum(t / (.02 + .03 * k), 1)
    return s

SOUNDS = {k[2:]: v for k, v in globals().items() if k.startswith("s_")}


def make(name, dur=None, freq=None):
    if name not in SOUNDS:
        sys.exit(f"unknown sound '{name}'. Try: {', '.join(SOUNDS)}")
    kw = {}
    if dur: kw["dur"] = dur
    if freq: kw["freq"] = freq
    return SOUNDS[name](**kw)


def put(bus, t, sig, db, pan=0.0):
    i = int(t * SR); sig = sig / max(np.max(np.abs(sig)), 1e-9) * 10 ** (db / 20)
    j = min(i + len(sig), len(bus)); sig = sig[: j - i]
    bus[i:j, 0] += sig * (1 - max(pan, 0)); bus[i:j, 1] += sig * (1 + min(pan, 0))


# ---------- music bed ----------
def music(total, bpm):
    beat = 60 / bpm; bus = np.zeros((int((total + 2) * SR), 2))
    def kick():
        n = int(.3 * SR); t = t_(n); return sweep(48 + 110 * np.exp(-t / .025), n) * env(n, .001, .12)
    def hat():
        n = int(.05 * SR); x = noise(n); return (x - onepole(x, .5)) * env(n, .0005, .012)
    def pluck(f, d=.35):
        n = int(d * SR); t = t_(n)
        return (np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) + .15 * np.sin(6 * np.pi * f * t)) * env(n, .002, .12)
    def bass(f, d):
        n = int(d * SR); t = t_(n)
        return onepole(np.sin(2 * np.pi * f * t) + .4 * np.sign(np.sin(2 * np.pi * f * t)), .12) * env(n, .01, .35)
    prog = [110.0, 87.31, 130.81, 98.0]; arp = [1, 1.5, 2, 1.5]
    for b in range(int(total / beat)):
        t = b * beat; root = prog[(b // 4) % 4]
        if b % 2 == 0: put(bus, t, kick(), -14)
        put(bus, t + beat / 2, hat(), -27, .3)
        if b % 4 == 0: put(bus, t, bass(root / 2, beat * 3.7), -17)
        put(bus, t, pluck(root * 2 * arp[b % 4]), -28, -.25)
        put(bus, t + beat / 2, pluck(root * 4 * arp[(b + 2) % 4], .2), -33, .25)
    return bus


def load_audio(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype="<f4").reshape(-1, 2).astype(np.float64)


def gain_curve(n, ranges, low):
    g = np.ones(n); r = int(.15 * SR)
    for a, b in ranges:
        i, j = int(a * SR), int(b * SR)
        g[i:j] = np.minimum(g[i:j], low)
        g[max(0, i - r):i] = np.minimum(g[max(0, i - r):i], np.linspace(1, low, len(g[max(0, i - r):i])))
        g[j:j + r] = np.minimum(g[j:j + r], np.linspace(low, 1, len(g[j:j + r])))
    return g


def voice_ranges(v, thr_db=-38, hop=.01, hold=.25):
    """Where the voice is speaking, as (start, end) seconds. Gaps shorter than `hold` are bridged."""
    h = int(hop * SR); m = np.abs(v).mean(axis=1); n = len(m) // h
    rms = np.sqrt((m[:n * h].reshape(n, h) ** 2).mean(axis=1))
    on = rms > 10 ** (thr_db / 20); out = []; start = None; last = -1e9
    for i, x in enumerate(on):
        t = i * hop
        if x:
            if start is None or t - last > hold:
                if start is not None: out.append((start, last + hop))
                start = t
            last = t
    if start is not None: out.append((start, last + hop))
    return out


def write(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def master(src, out):
    chain = "acompressor=threshold=-20dB:ratio=3:attack=2:release=80:makeup=4,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", chain, "-ar", str(SR), out], check=True)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "one", "mix"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--dur", type=float); ap.add_argument("--freq", type=float)
    ap.add_argument("--duration", type=float); ap.add_argument("--music", type=float)
    ap.add_argument("--duck", default=""); ap.add_argument("--voice")
    ap.add_argument("--seed", type=int, default=7); ap.add_argument("--no-master", action="store_true")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    if a.cmd == "list":
        print(" ".join(SOUNDS)); sys.exit()
    if a.cmd == "one":
        name, out = a.args
        s = make(name, a.dur, a.freq); s = s / np.max(np.abs(s)) * .8
        write(out, np.stack([s, s], 1)); print("ok", out); sys.exit()

    cues_path, out = a.args
    cues = json.load(open(cues_path, encoding="utf-8"))
    voice = load_audio(a.voice) if a.voice else None
    total = a.duration or (len(voice) / SR if voice is not None else max(c["t"] for c in cues) + 2)
    N = int(total * SR)
    sfx = np.zeros((N + SR * 2, 2))
    for c in cues:
        put(sfx, c["t"], make(c["sfx"], c.get("dur"), c.get("freq")), c.get("db", -14), c.get("pan", 0))
    sfx = sfx[:N]
    bed = music(total, a.music)[:N] if a.music else np.zeros((N, 2))
    if a.music:
        ranges = [tuple(map(float, r.split("-"))) for r in a.duck.split(",") if r]
        bed *= gain_curve(N, ranges, .55)[:, None]
        fade = np.ones(N); fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR)); fade[:int(.05 * SR)] = np.linspace(0, 1, int(.05 * SR))
        bed *= fade[:, None]
    mix = sfx + bed
    if voice is not None:
        v = np.zeros((N, 2)); v[:min(N, len(voice))] = voice[:N]
        vr = voice_ranges(v)
        bed_g = gain_curve(N, vr, 10 ** (-10 / 20)); sfx_g = gain_curve(N, vr, 10 ** (-6 / 20))
        pk = max(np.max(np.abs(sfx + bed)), 1e-9)
        mix = (sfx * sfx_g[:, None] + bed * bed_g[:, None]) / pk * 10 ** (-12 / 20) + v / max(np.max(np.abs(v)), 1e-9) * .9
    mix = mix / max(np.max(np.abs(mix)), 1e-9) * .9
    if a.no_master:
        write(out, mix)
    else:
        tmp = os.path.join(tempfile.gettempdir(), f"motion-abojesh-raw-{os.getpid()}.wav")
        write(tmp, mix); master(tmp, out); os.remove(tmp)
    print("ok", out, f"{total:.1f}s", len(cues), "cues", "+ music" if a.music else "", "+ voice" if voice is not None else "")

# Sound

Silence makes motion feel cheap. Each meaningful move gets a sound, and the voice always wins.

## Where sounds come from (in this order)
1. The user's own sounds (`studio/`, `ideas/`).
2. Free libraries the user approves (for example Pixabay, Mixkit, Openverse with CC0 or CC BY). Ask before downloading; keep the source and licence in `plan/sources.md`; credit CC BY in `final/`.
3. **Made on the computer** with `scripts/sfx.py`. No download, no licence worry.

## `scripts/sfx.py`
```
python scripts/sfx.py list                         # names of the sounds it can make
python scripts/sfx.py one whoosh assets/whoosh.wav # one sound to a file
python scripts/sfx.py mix plan/cues.json assets/mix.wav --duration 30 --music 150 --voice assets/voice.wav
```
`plan/cues.json` is a list of cues on the same times as the animation:
```json
[ {"t": 0.0, "sfx": "boom", "db": -8},
  {"t": 2.4, "sfx": "slam", "db": -14},
  {"t": 5.2, "sfx": "buzzer", "db": -13} ]
```
Sounds: `boom`, `slam`, `whoosh`, `pop`, `tick`, `beep`, `buzzer`, `ding`, `shimmer`, `click`, `riser`.
`--music 150` adds a light beat at 150 bpm under everything (leave it out for no music). `--duck` lists time ranges where the music drops, e.g. `--duck 2.8-5.3,7.6-10.1`.
`--voice` puts the voice-over on top and lowers music and sounds under it.
The script masters to about −14 LUFS, true peak under −1 dB (good for Reels, Shorts and TikTok).

## Mixing rules
- Voice first: music sits about 18 dB under the voice; effects never cover a word.
- Hits land on the exact frame of the motion.
- Phones have small speakers: low booms need a click or a pop on top so they are heard.
- Cut tails; do not let a sound ring into the next scene.
- No music unless the video wants energy without a voice, or the user asks.

## Their voice-over
- Never speed it up or change it.
- Trim long pauses: `python scripts/trim_pauses.py studio/vo.m4a assets/voice.wav` keeps about 0.2 s of each pause and 1 s after the last word. Listen to the start and end of every cut; if a word got clipped, run again with `--db -36`.
- Lock the animation times on the trimmed voice, not the original.

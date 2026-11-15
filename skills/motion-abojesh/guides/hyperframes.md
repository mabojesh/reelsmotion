# Building with HyperFrames

HyperFrames (by HeyGen, Apache-2.0) turns HTML + a GSAP timeline into an MP4. It runs with `npx`, so nothing is installed into the project. It needs Node 22 or newer and a Chromium browser (it downloads its own the first time).

Pin the version so every video renders the same: `npx --yes hyperframes@0.8.225 <command>`.

## Project files (made by `scripts/new_video.py`)
```
index.html               the root: size, length, brand colours, tracks
compositions/scenes.html  the animation (one <template>)
assets/fonts/             brand fonts (display.ttf, body.ttf, light.ttf)
assets/                   pictures, sounds, mix.wav
plan/                     script, timing (beats.json), sound script
renders/                  previews and finals
PROGRESS.md               what is done and what is next
```

## How it fits together
- `index.html` has a `#root` with `data-composition-id="main"`, `data-duration` and `data-fps`. Each track is a child with `data-start`, `data-duration` and `data-track-index`.
- A track can load a composition file: `data-composition-src="compositions/scenes.html"`.
- The composition file is one `<template>` holding a `#root` with its own `data-composition-id`, its styles, and a script that builds a **paused** GSAP timeline and registers it:
  ```js
  window.__timelines = window.__timelines || {};
  window.__timelines["scenes"] = tl;
  ```
- Audio is an `<audio class="clip">` track in `index.html` with the same `data-start` / `data-duration` idea.

## Rules for frames that render the same every time
- Everything is placed on the timeline at an absolute time: `tl.to(el, {...}, 2.4)`.
- No `Date.now()`, `setTimeout`, `requestAnimationFrame`, random numbers without a fixed seed, or CSS animations. HyperFrames seeks the timeline to each frame.
- Keep one timing source: put the times in an object at the top of the script (`const T = { hook: 0, item: 2.4 }`) and use the same numbers in `plan/beats.json` and the sound script.
- End the timeline exactly at the video length: `tl.to({}, { duration: 0.01 }, TOTAL - 0.01)`.

## Commands (run from the project folder)
| Command | What it does |
|---|---|
| `npx --yes hyperframes@0.8.225 check` | Finds layout problems: overlaps, text off screen, low contrast. Fix every error. |
| `npx --yes hyperframes@0.8.225 snapshot --at 0,1.5,3` | PNG stills at those seconds, for your own check. |
| `npx --yes hyperframes@0.8.225 render --output renders/preview.mp4` | Renders the video with its audio. |
| `npx --yes hyperframes@0.8.225 preview` | A live preview in the browser, if the user wants to scrub. |

## Motion taste (default; the brand file wins)
- Fast: a new thing on screen every 1–2 s, scenes of 2–5 s.
- Easing `power3.out` for entries, `power2.in` for exits, `back.out(1.6)` for pops. Durations 0.25–0.5 s.
- One idea per screen. Big type, lots of space.
- Every meaningful motion gets a sound (see `sound.md`).

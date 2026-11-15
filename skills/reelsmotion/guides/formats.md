# Formats

| Format | Size | `new_video.py --format` |
|---|---|---|
| Reel / Short / TikTok | 1080 × 1920, 30 fps | `reel` |
| Square post | 1080 × 1080 | `square` |
| YouTube video | 1920 × 1080 | `wide` |
| Carousel, cover, still | any, set in the HTML | `still` |

## Reels that work
- **Explainer:** hook (0–2 s) → 3–5 short points → one line summary → call to action.
- **Quiz «صح ولا غلط؟»:** hook → 5 statements, each with a 3-2-1 countdown, a right/wrong stamp and a one-line reason → «كم وحدة جبت صح؟ اكتبها بالتعليقات». About 30 s, works without a voice.
- **List / tools:** a big number per item, one picture or icon, one line.
- **Before / after:** split screen or a wipe from right to left.
Keep the brand name and handle small on screen, and a clear end card with the logo.

## Carousels (Instagram, LinkedIn)
- 1080 × 1350 per page (4:5). 5–8 pages: hook page, one idea per page, last page = who you are + what to do (follow, save, comment).
- Build one HTML with one `.page` per page and `@page { size: 1080px 1350px; margin: 0 }`, then:
  - PDF (LinkedIn): `python scripts/shoot.py carousel.html renders/carousel.pdf --pdf`
  - PNGs (Instagram): `python scripts/shoot.py carousel.html renders/page.png --size 1080x1350 --pages 7`
- Page number and a small arrow «←» on every page except the last.

## Covers and YouTube text
- Shorts cover 1080 × 1920, video thumbnail 1280 × 720. Three to five big words, one strong picture or stamp, the brand colours. Shoot with `scripts/shoot.py cover.html renders/cover.png --size 1280x720`.
- Write 3 title options (recommend one, under 60 characters, the curiosity up front), a description with a question for comments, 3 hashtags in the description and up to 10 more, and a tags list. Save it as `renders/youtube.txt` and deliver it beside the video.
- Never promise views.

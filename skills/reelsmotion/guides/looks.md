# Looks that work

## Full-bleed photo, blur to white (the default for photo scenes)
A photo fills the whole 9:16 frame. The top half is sharp. From the middle down it blurs and fades into the white background, and the text sits on the white part. The look is calm, rich and easy to read. Use it for any scene built around one strong photo or clip. Keep drawn scenes (charts, boards, icons) on the plain background.

The layers, from the bottom up, in a full-frame box behind the scene's content:
1. A `cover` copy of the photo, `blur(50px) brightness(1.1)`. It fills any gap.
2. The sharp photo, masked `linear-gradient(#000 0, #000 42%, transparent 50%)`.
3. The same photo, `blur(30px) brightness(1.1)`, masked `linear-gradient(transparent 0, transparent 44%, #000 56%)`.
4. White: `linear-gradient(rgba(255,255,255,0) 0 46%, rgba(255,255,255,.85) 55%, #fff 61%)`.
5. A soft dark shade over the top 340 px, so the handle pill reads.

How to use it:
- Size the photo so the subject sits between y 250 and 900. For a landscape car photo, `background-size: auto 1050px; background-position: 50% 0`.
- Put the content at the bottom of the scene (`justify-content: flex-end`). Give the top handle and tag a white pill background.
- Slow push-in (scale 1.12 → 1 over the scene) on the photo layers, not on the text.
- Old black-and-white photos: add `grayscale(1)` to every layer.
- Credit sits small in grey at the bottom left (y 1880).
- A second photo can sit in front as a tilted card with an 8 px white border.

## Cover (Reels / Shorts, 1080 × 1920)
The same idea as a still:
- a photo from the reel, full-bleed, sharp on top and blurred to white from the middle;
- a small grey line, then the title (about 130 px, black, Bold);
- a black pill tilted −3° with the question;
- the logo photo (150 px) and the name (72 px) at the bottom.

Make a second version with one huge number on white when the reel has a strong number. Shoot it with `scripts/shoot.py cover.html renders/cover.png --size 1080x1920`.

## End card
Question → black pill «اكتبلي بالكومنت» → arrow → logo photo about 180 px and name about 84 px. Hide captions during the end card.

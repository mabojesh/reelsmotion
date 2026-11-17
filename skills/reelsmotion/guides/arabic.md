# Arabic on screen

Arabic letters join. Anything that splits a word into letters breaks it. These rules hold for every video, cover and carousel.

## Never
- Animate letter by letter, or split a word into `<span>`s per letter.
- Use `letter-spacing` on Arabic text.
- Put `dir="rtl"` on `<html>` (HyperFrames layouts break). Put it on each row of words instead.
- Clip the dots or the tails: no `overflow: hidden` tight on a line, and give `line-height` at least 1.3 (1.45 for body text).
- Use fake bold or fake italic. Load the real weight.
- Outline Arabic with `-webkit-text-stroke`: every join shows a seam. For a second-level word use a solid grey (#9a9a9a) instead.
- Put emoji inside a video or cover (they are the platform's artwork). Draw simple black-and-white line icons instead; emoji are fine in captions.

## Always
- Animate **whole words** or whole lines: fade, rise, scale, blur-in, a highlight box behind the word.
- Wrap each word in `<span class="w">` inside a `div` with `dir="rtl"` and `display: flex; flex-wrap: wrap; justify-content: center; gap: 0 20px`.
- Progress bars, arrows and "next" motion go **right to left**.
- Numbers: use Arabic-Indic digits (٣ ٢ ١) for a local feel, or Western digits if the brand says so. Keep one style per video.
- Usernames, links and English words sit in their own `span` with `direction: ltr`.
- Keep text inside the safe area: 70 px from the sides, and on 9:16 keep the top 220 px and bottom 380 px free of key text (app buttons cover them).

## Sizes that read on a phone (1080 × 1920)
| Use | Size |
|---|---|
| Hook title | 100–120 px, Bold |
| Statement / main line | 80–90 px |
| Caption | 60–70 px |
| Small note | 40–46 px, Regular, grey |

## Generated Arabic voice (TTS)
- Voices often misread Arabic words (for example «بريد» → «برايد»). Write the voice script with vowel marks on hard words (`plan/vo-tashkeel.txt`), keep the screen captions without vowel marks, and check every word of the take with a word-timed transcript before you build on it.
- When one word is wrong in an otherwise good take, cut the same word from elsewhere in the take and splice it in (short fades) instead of paying for a new take.

## Check before showing
Snapshot every scene. Look for: broken joins, missing dots, words in the wrong order, lines touching the edge, text under the app buttons.

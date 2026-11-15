# Arabic on screen

Arabic letters join. Anything that splits a word into letters breaks it. These rules hold for every video, cover and carousel.

## Never
- Animate letter by letter, or split a word into `<span>`s per letter.
- Use `letter-spacing` on Arabic text.
- Put `dir="rtl"` on `<html>` (HyperFrames layouts break). Put it on each row of words instead.
- Clip the dots or the tails: no `overflow: hidden` tight on a line, and give `line-height` at least 1.3 (1.45 for body text).
- Use fake bold or fake italic. Load the real weight.

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

## Check before showing
Snapshot every scene. Look for: broken joins, missing dots, words in the wrong order, lines touching the edge, text under the app buttons.

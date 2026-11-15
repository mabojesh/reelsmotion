# reelsmotion 🎬

مهارة لـ Claude بتعمل فيديوهات موشن عربية، وريلز، وكويزات، وكاروسيلات، وأغلفة يوتيوب، وكلها بأسلوبك إنت.
إنت بتحكي، وClaude بيعمل الملفات كلها.

من **محمد عبدالإله** · [@mabojesh](https://instagram.com/mabojesh)

**[English below ↓](#english)**

---

## شو بتعمل؟
- **ريلز وشورتس** (٩:١٦) بحركة نص عربي نظيفة، ومؤثرات صوتية بتنعمل على جهازك، وموسيقى خفيفة إذا بدك.
- **فويس أوفر:** بتبعت صوتك، وهي بتقص الوقفات الطويلة وبتركّب الحركة عليه.
- **كويز «صح ولا غلط؟»**، ولستات، وشروحات.
- **كاروسيلات:** PDF للينكد إن، وصور لانستا.
- **أغلفة يوتيوب** مع عناوين ووصف وهاشتاغات.

## المجلدات
بعد التثبيت بيصير عندك تلات مجلدات بس:

| المجلد | شو بتحط فيه |
|---|---|
| `studio` | الكليبات والتسجيلات والفويس أوفر تبعك |
| `ideas` | الإلهام: فيديوهات وصور ولينكات بتعجبك (مجلد لكل موضوع)، وهويتك بـ `ideas/brand` |
| `final` | الشغل الجاهز |

ما بتحتاج تفتح ولا ملف بإيدك. احكي مع Claude، وهو بيرتّب كل شي.

---

## التثبيت

### ١. أسهل طريقة: برومت واحد بـ Claude Code
افتح Claude Code (بالتطبيق أو بالتيرمنال) على مجلد فاضي لفيديوهاتك، والصق:

```
ثبّت المهارة من https://github.com/mabojesh/reelsmotion بهالمجلد، وسمّي المجلدات studio, ideas, final
```

### ٢. كإضافة (Plugin) بـ Claude Code
```
/plugin marketplace add mabojesh/reelsmotion
/plugin install reelsmotion@mabojesh
```
بعدها افتح مجلد فاضي وقلّو: «ثبّت المهارة».

### ٣. بتطبيق Claude (claude.ai)
1. نزّل [reelsmotion.zip](https://github.com/mabojesh/reelsmotion/raw/main/reelsmotion.zip).
2. ارفعه من الإعدادات، من قسم المهارات (Skills).

> التطبيق بيقدر يكتب النص ويخطط ويعمل كاروسيلات. بس رندر الفيديو بيحتاج Claude Code على جهازك.

### شو لازم يكون عندك على الجهاز؟
Python وNode 22 أو أحدث وFFmpeg وEdge أو Chrome. Claude بيفحص الجهاز، وإذا في شي ناقص بيستأذنك وبينزّله.

---

## خليها على ذوقك
- **الخط والألوان:** ابعت خطك أو قلّو «ألواني كحلي وذهبي». أول ما تثبّت المهارة، بتكون الهوية أبيض وأسود بخط IBM Plex Sans Arabic.
- **الإلهام:** حط فيديوهات بتعجبك بـ `ideas/<الموضوع>` وقلّو «استخدم ideas». بياخد الأسلوب والتقنية بس، وما بياخد اللقطات ولا الصوت.
- **الذاكرة:** كل ملاحظة بتقولها بتنحفظ، والدردشة الجاية بتكمّل من وين وقفت. بس قول «كمّل».

---

## الرخصة
مسموحلك تستعمل المهارة مجاناً، وتعدّل عليها لنفسك، وتبيع الفيديوهات اللي بتطلع منها.
**ممنوع** تعيد نشرها، أو تبيعها، أو ترفعها باسمك، حتى لو عدّلت عليها. التفاصيل بـ [LICENSE.md](LICENSE.md).
إذا بدك تشاركها مع حدا، ابعتلو رابط هالصفحة.

الأدوات اللي بتستعملها إلها رخصها الخاصة: HyperFrames (Apache-2.0)، وGSAP، وFFmpeg، وخط IBM Plex Sans Arabic (SIL OFL).

---

<a id="english"></a>
## English

**reelsmotion** is a Claude skill that makes motion videos, reels, quizzes, carousels and YouTube covers in your own style. You talk, and Claude handles every file. Videos can be in Arabic or English: Claude replies in your language.

### What it does
- **Reels / Shorts (9:16)** with clean kinetic text, sound effects made on your computer, and optional light music.
- **Voice-over:** send your own voice and it trims long pauses and syncs the motion to it, or have text turned into speech.
- **Quizzes, lists and explainers.**
- **Carousels:** a PDF for LinkedIn, PNGs for Instagram.
- **YouTube covers** with titles, a description and hashtags.

### Folders
After installing, you only use three folders: `studio` (your clips and voice), `ideas` (what inspires you, one folder per topic, and your brand in `ideas/brand`) and `final` (finished work).

### Install
**1. One message in Claude Code (easiest).** Open Claude Code in an empty folder and paste:
```
Install the skill from https://github.com/mabojesh/reelsmotion in this folder, and name the folders studio, ideas, final
```

**2. As a Claude Code plugin.**
```
/plugin marketplace add mabojesh/reelsmotion
/plugin install reelsmotion@mabojesh
```
Then open an empty folder and say "install the skill".

**3. In the Claude app (claude.ai).** Download [reelsmotion.zip](https://github.com/mabojesh/reelsmotion/raw/main/reelsmotion.zip) and upload it under Settings → Customize → Skills. The app can plan, write and make carousels; rendering video needs Claude Code on your computer.

**You need:** Python, Node 22+, FFmpeg and Edge or Chrome. Claude checks your computer and asks before installing anything missing.

### Licence
Free to use and to modify for yourself, and you may sell the videos you make with it. You may not republish, re-upload or sell the skill, or a modified or renamed version of it. Details in [LICENSE.md](LICENSE.md). To share it, send the link to this page.


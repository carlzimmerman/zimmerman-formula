# Audiobook — A Beautifully Geometric Universe

The book's **main story thread**, adapted for listening. Every equation and symbol is spelled
out in words (e.g. "a-nought equals the speed of light squared, times the square root of Lambda
divided by thirty-two pi"); the boxed *Deeper Dive* / *Worked Example* mathematics and the figures
are left in the printed book, where they belong. This is the calm spoken spine — the story the
equations tell.

- **33 files**: `00_narration.txt` (spoken opening) + `01`–`32_narration.txt` (one per chapter).
- **`A_BEAUTIFULLY_GEOMETRIC_UNIVERSE_AUDIOBOOK.txt`** — all 33 joined into one master script.
- **~142,000 spoken words ≈ 15–17 hours** of audio (≈15.8 h at 150 words/min).
- Generated from the chapter sources per `NARRATION_SPEC.md`; plain UTF-8, no markdown, no raw symbols.

---

## How to listen on your iPhone

### Option A — Today, zero setup (your phone reads it aloud)
No audio files needed; iOS can read the script with a built-in voice.
1. Put `A_BEAUTIFULLY_GEOMETRIC_UNIVERSE_AUDIOBOOK.txt` on your phone — AirDrop it from the Mac,
   or save it to **iCloud Drive / Files**, or email it to yourself.
2. On iPhone: **Settings → Accessibility → Spoken Content → turn on "Speak Screen."** (Optionally
   pick a nicer voice under **Voices → English** — the "Siri" and "Premium"/"Enhanced" voices sound best.)
3. Open the file in **Files** (or Books, or Mail), then **swipe down from the top with two fingers.**
   The phone reads the whole script aloud — with play/pause, speed, and skip controls.

Free, instant, and it works on the script as-is. The voice is decent but not studio-grade — good
for a first listen or a long drive today.

### Option B — A real audiobook (neural voice, chapters, resume)
Generate audio once, then listen in a proper player. Two steps: **make the audio**, then **load it**.

**Make the audio** (pick one service; see the commands below):
- **OpenAI TTS** — cheapest, very natural. ~$15–25 for the whole book.
- **ElevenLabs** — the most lifelike narration, has a long-form "Projects" mode. ~$100–300.
- (Azure / Google / Amazon Polly also work and are cheap.)
Run per chapter → you get 33 MP3s (`00.mp3` … `32.mp3`).

**Load it onto the iPhone** — best two options:
1. **BookPlayer** (free, open-source, App Store). Make a folder of the 33 MP3s, drop it into the
   app via **Files / iCloud / AirDrop**, and it plays them as one audiobook: chapter list, resume
   where you left off, 0.5×–4× speed, sleep timer. Easiest path, no binding needed.
2. **Apple Books** — bind the 33 MP3s into a single `.m4b` with chapter markers (command below) and
   open it; Books treats `.m4b` as an audiobook (bookmarks, speed, syncs across your devices).

---

## Commands to generate the audio (run on the Mac, with your own API key)

> These call a paid third-party service and use *your* account/key — run them yourself.
> Never commit the key.

### OpenAI TTS (per-chapter MP3s)
```bash
cd book/audiobook
export OPENAI_API_KEY=sk-...            # your key
for f in [0-9][0-9]_narration.txt; do
  n="${f%_narration.txt}"
  # 'tts-1-hd' = higher quality; voices: alloy, echo, fable, onyx, nova, shimmer (try 'onyx' or 'fable')
  python3 - "$f" "$n.mp3" <<'PY'
import os, sys, textwrap
from openai import OpenAI
client = OpenAI()
text = open(sys.argv[1]).read()
# OpenAI TTS caps ~4096 chars/request, so stream chunk-by-chunk into one file
chunks = textwrap.wrap(text, 3800, break_long_words=False, replace_whitespace=False)
with open(sys.argv[2], "wb") as out:
    for c in chunks:
        r = client.audio.speech.create(model="tts-1-hd", voice="onyx", input=c)
        out.write(r.content)
print("wrote", sys.argv[2])
PY
done
```

### ElevenLabs (per-chapter MP3s — most lifelike)
Use their dashboard "Projects" (upload `A_BEAUTIFULLY_GEOMETRIC_UNIVERSE_AUDIOBOOK.txt`, pick a
narrator voice, render) for the smoothest long-form result, or the API per chapter:
```bash
export ELEVEN_API_KEY=...
for f in [0-9][0-9]_narration.txt; do
  n="${f%_narration.txt}"
  curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/<VOICE_ID>" \
    -H "xi-api-key: $ELEVEN_API_KEY" -H "Content-Type: application/json" \
    -d "$(python3 -c 'import json,sys;print(json.dumps({"text":open(sys.argv[1]).read(),"model_id":"eleven_turbo_v2_5"}))' "$f")" \
    --output "$n.mp3"
done
```

### Bind the 33 MP3s into one chaptered `.m4b` for Apple Books
```bash
cd book/audiobook
# 1) concat list
ls [0-3][0-9].mp3 | sort | sed "s/^/file '/;s/$/'/" > _list.txt
# 2) join to one file, then convert to m4b (chapters optional but nice)
ffmpeg -f concat -safe 0 -i _list.txt -c copy _joined.mp3
ffmpeg -i _joined.mp3 -c:a aac -b:a 96k "A Beautifully Geometric Universe.m4b"
# AirDrop the .m4b to the iPhone and open in Apple Books.
```
(For true chapter markers in the `.m4b`, the free app **Audiobook Binder** does it with a GUI.)

---

## Notes
- The narration is **main-thread only** by design — the listenable spine. If you ever want a
  "deep" edition that also voices the *Deeper Dive* math, that's a separate, longer adaptation.
- Honesty is preserved throughout: a-nought, Z, and kappa are described as inputs/geometry, never
  "derived from first principles," matching the printed book.

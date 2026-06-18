# Narration Spec — "A Beautifully Geometric Universe" (audiobook adaptation)

You are adapting ONE chapter of the textbook into **spoken-word narration** a narrator
(human or text-to-speech) can read aloud start to finish. The book was written in two
registers: a calm, equation-free **main thread** (a story anyone can follow) and boxed
**Deeper Dive / Worked Example** asides for physicists. **The audiobook is the main thread
only.** Your job is to turn that main thread into natural, listenable speech.

Output: **plain UTF-8 text, no markdown of any kind** — no `#`, `*`, `_`, backticks,
links, or image lines. Just clean sentences and paragraph breaks.

## KEEP (the main thread)
- All the narrative prose paragraphs of the chapter, in order, in Carl's calm first-person voice.
- The chapter's opening italic epigraph — read it as the opening line.
- The `## Summary` prose at the end (it listens well). 

## DROP entirely
- Every **Deeper Dive** and **Worked Example** box/aside (these are the rigorous math for
  physicists; the main thread stands without them). They may appear as a bold lead-in
  ("**Deeper Dive:** ...") or a sub-section — identify and remove the whole aside, keeping
  the surrounding narrative.
- Figure image lines, figure captions, and **Source:** lines. EXCEPTION: if the prose leans
  on a figure to make its point, fold ONE plain spoken sentence describing what it shows into
  the narration ("Picture two curves — one runs flat while the other slopes down..."). Otherwise drop it.
- The `## Questions` section (a bulleted list doesn't listen well) — drop it entirely.
- Tables — convert to one or two spoken summary sentences, or drop if non-essential.
- Any margin notes / bracketed asides that interrupt the spoken flow.

## HEADINGS → spoken cues
- `# Chapter N: Title` → open with: "Chapter N. Title." then a beat, then the epigraph.
- `## Section heading` → a SHORT spoken transition, not a barked label. Prefer a natural
  segue; if you announce it, say "Section — <title>." sparingly. Don't over-announce.

## SYMBOLS AND MATH — spell EVERYTHING (the listener sees nothing)
Convert every symbol and inline equation to spoken English:
- a₀ → "a-nought"; Λ → "Lambda"; κ → "kappa"; ρ → "rho"; μ → "mu"; π → "pi"; σ → "sigma";
  Z → "Z"; H₀ → "H-nought"; H_Λ → "the de Sitter Hubble rate"; γ → "gamma"; ν → "nu".
- c → "the speed of light" on first mention in a chapter, then just "c".
- √x → "the square root of x"; x² → "x squared"; x³ → "x cubed".
- ∝ → "is proportional to"; ≈ / ∼ → "is about"; → → "gives" or "leads to"; ½ → "one half".
- ×10⁻¹⁰ → "times ten to the minus ten"; ×10⁻⁵² → "times ten to the minus fifty-two".
- The headline value: 9.36×10⁻¹¹ m/s² → "nine point three six times ten to the minus eleven
  meters per second squared."
- The central equation a₀ = c²√(Λ/32π) → say it in words: "a-nought equals the speed of light
  squared, times the square root of Lambda divided by thirty-two pi."
- Units spoken naturally: "kilometers per second", "kiloparsecs", "meters per second squared".

## STYLE
- Keep the warm, friendly, first-person tone. This should sound like Carl talking to a curious friend.
- Rewrite any visual reference ("as the figure shows", "in the equation above") into spoken
  phrasing ("as we just saw", "put into words, that says...").
- Don't summarize the story — *adapt* it. Preserve the full narrative arc of the main thread.
- Pace for ~145 words per minute; clarity over density.

## FORMAT OF THE OUTPUT FILE
First line: `Chapter N — Title` (plain text). Then a blank line. Then the narration prose.
Nothing else. Length is typically 1,800–4,000 spoken words depending on the chapter.

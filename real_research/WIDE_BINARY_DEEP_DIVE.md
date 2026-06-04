# Wide Binaries: an Honest Deep Dive — and Where We Actually Landed

**C. Zimmerman, June 2026.** *Supersedes the pro-Chae literature summary in `ai_slop/research/WIDE_BINARY_ANALYSIS.md`.
Numbers: `reviews/project_wide_binary_prediction.py`.*

---

## 0. Where we actually landed (the honest history first)

We never produced a credible wide-binary result of our own. Two things exist in the repo, and both must be named:

1. **Our own data analysis was a bug.** The "16σ MOND in wide binaries" was a **velocity units error** (ratios off
   by ~1000×) — caught, flagged in `README.md`, and quarantined in `ai_slop/`. It is worthless and retracted.
2. **Our surviving write-up leans the wrong way.** `ai_slop/research/WIDE_BINARY_ANALYSIS.md` (May 2026) concludes
   "Chae is likely right." That is **not** calibrated against the current field, which has shifted *skeptical*
   (below). It is a one-sided literature summary, not analysis, and this document supersedes it.

So the honest answer to "where did we land on wide binaries": **nowhere of our own — and the literature is
genuinely unresolved, currently leaning skeptical on whether the anomaly is robust.**

## 1. Why wide binaries matter — especially for this framework

Wide binaries (separation s ≳ a few thousand AU) are the **cleanest test of MOND's basic premise**: a change in
the force law at low acceleration, with **no dark matter and no cosmology**, inside the Galaxy. For *this*
framework they are sharper than that — they test the **derived deep-MOND enhancement (the "sign") at z = 0**. The
whole program rests on gravity being enhanced below a₀; wide binaries probe that enhancement directly and locally.
**If wide binaries are Newtonian, the framework's central derived result is locally falsified.** This is why the
test is not optional.

## 2. The geometric scale (this also answers "have we got all the geometry?")

The separation at which a binary crosses into the MOND regime is the **MOND radius** r_M = √(GM/a₀). With a₀ =
cH₀/Z, this is *exactly* the geometric mean of the object's Schwarzschild radius and the cosmic horizon:

>  **r_M = (8π/3)^{1/4} · √(r_s · R_H)**,   r_s = 2GM/c²,  R_H = c/H₀   (verified to 4 digits)

For ~1 M⊙ that is **~7000 AU** = geometric mean of **3 km** (r_s) and **14.6 Gly** (R_H). Wide binaries probe
*precisely* this scale. So a₀ = cH₀/Z is not just a number — it makes the wide-binary transition the **geometric
bridge between the smallest and largest length scales in physics**. That is a genuine new geometric reference
point surfaced by this work (it is implicit in a₀ ~ cH, made exact here with the (8π/3)^{1/4} factor).

## 3. The external field effect — why the signal is small *by construction*

Wide binaries in the solar neighbourhood are **not isolated**: the Milky Way's field at the Sun is g_ext ~ V²/R ≈
**1.86 a₀** — *above* a₀. So the binaries sit in the **EFE-dominated regime**, where the external field partially
Newtonizes the internal dynamics. The naive isolated deep-MOND boost (√2, +41% in orbital velocity) is suppressed
to (computed, `project_wide_binary_prediction.py`):

| prediction | velocity boost at widest separations |
|---|---|
| isolated deep-MOND (no EFE) | +41% |
| simple μ = x/(1+x), with EFE | **+13%** |
| standard μ = x/√(1+x²), with EFE | **+3%** |

The exact number depends strongly on the (uncertain) interpolation function; the framework's own **derived
(DSSYK) interpolation is sharp/standard-like → the small end (~3–5%)**. The signal the test is hunting is
therefore **~5–15% at most, and possibly ~3%** — small, by construction.

## 4. The contested literature (current, mid-2026)

| Camp | Result | Method emphasis |
|---|---|---|
| **Chae 2023–2026** | Anomaly detected, ~3.5–5σ; gravity boost g_obs/g_N ≈ 1.4 (≈ +15–20% velocity) | normalized-velocity profiles; Newtonian calibration region; MC noise |
| **Hernandez et al. 2024** | ~2.6σ anomaly; pro-MOND | independent samples; critical review (arXiv:2312.03162) |
| **Banik et al. 2024** | Newtonian preferred, up to **19σ** vs MOND | ensemble proper-motion statistics; triple modelling |
| **Pittordis & Sutherland 2023/2025** | Newtonian preferred | velocity-ratio histograms; triple population |
| **2025–2026 methodological** (2504.07569; 2602.24035 "No evidence for MOND"; 2603.11015 "sensitive to orbital modeling") | lean Newtonian / **not robust** | realistic triples, eccentricity priors, orbital modelling |

**The crux of the disagreement** is not the gravity theory but the **astrophysics of the sample**: undetected
third stars (triples) inflate velocities and mimic a MOND boost; eccentricity priors and the line-of-sight
velocity treatment shift the inferred signal; and bin widths vs error sizes drive the quoted significance. The
honest reading of the 2025–2026 work: **the anomaly is sensitive to exactly these modelling choices**, so the
field has *not* converged, and if anything the recent methodological papers tilt toward "no robust MOND signal."
Both sides agree the arbiter is **Gaia DR4** (better parallaxes/proper motions, better triple flagging), which is
not yet decisively in hand.

## 5. What it means for the framework (calibrated, both directions)

- The framework's prediction here is **just standard MOND + the MW EFE** — it adds no new term at z = 0 — so its
  expected signal (**~3–15%**, derived-interpolation end ~3–5%) sits **inside the contested 0–20% band**. It does
  **not** strongly predict either camp's result.
- Therefore wide binaries **currently neither confirm nor refute the framework.** The signal is marginal by
  construction (EFE-suppressed), which is *why* method choices flip the verdict.
- **Downside risk is real:** if the skeptical (Newtonian) trend hardens with Gaia DR4, it challenges the *premise*
  that local MOND is real — the premise the a₀(z) paper assumes. That would not touch the a₀(z) *measurement*
  (which stands on its own data) but would undercut the *interpretation*.
- **Upside is bounded:** even a confirmed Chae anomaly is consistent with generic MOND, so it would support the
  framework's premise but not distinguish it from any other MOND theory.

## 6. Should we do our own analysis? — Honest recommendation: no (track it)

A credible independent wide-binary test requires the Gaia DR3 wide-binary catalogue (El-Badry et al.) plus
careful triple-system, eccentricity, and selection modelling — a substantial project on which the field's own
experts are *split over methodology*. Our one attempt was a units bug. The marginal value of a rushed in-house
analysis is low and the methodology bar is high. **Recommendation:** treat wide binaries as a **pending external
falsification test** of the framework's premise; **track Gaia DR4 and the triple-modelling consensus**; do not
invest in an own analysis; and — done here — **correct the repo's earlier pro-Chae lean to a neutral, contested
status.**

---

### Bottom line
Wide binaries are the cleanest local test of the framework's derived deep-MOND enhancement, they probe the
beautiful geometric-mean scale r_M = (8π/3)^{1/4}√(r_s R_H) ≈ 7000 AU — and they are, right now, **genuinely
undecided**, with the predicted signal small enough (EFE-suppressed to ~3–15%) that the observational camps sit on
both sides of it. We hold no own result (the old one was a bug), we do not lean pro-Chae, and we watch Gaia DR4.

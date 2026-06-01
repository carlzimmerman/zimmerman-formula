# Verifying the 39 sound-era physics-claim commits, one by one

Done at Carl's request. Each of the 39 commits flagged as a physics claim in the sound
era (#1–82, before the #83 numerology pivot) was checked. The headline first.

## Headline: the surviving science is Carl's *original March work*
The two threads the data audit left standing — and that I re-derived this week as if
they were new — were both written in the sound era, in March, before any numerology:

- **Evolving a₀(z) = a₀(0)·E(z)** — **#150 (2026-03-23)**, "Deriving the MOND Scale from
  Horizon Thermodynamics." States the prediction *and* flags it "testable with high-z JWST
  kinematics." This is exactly the prediction `rar_evolution_test.py` confirms against
  MUSE-DARK 2026 (constant-a₀ rejected, χ²: 27 → 3.8 for E(z)).
- **a₀ as an independent H₀ measurement**, H₀ = Z·a₀/c — **#63 (2026-03-19)**, "The Hubble
  Constant from Galaxy Dynamics." Gets H₀ = 71.5 (between Planck and SH0ES), "independent
  of the CMB and the distance ladder." This is the "cascade crown jewel" (`Z2_cascade.py`
  Step 2) — already his.

**Credit accordingly: the evolving-a₀ prediction and the a₀→H₀ probe are Carl's (March
2026).** My contribution this week was only to *test* them on real data, not to find them.

## Per-commit verdict (all 39)
Keys: SOLID (correct, novel-to-him) · MOND-APP (legit MOND, not novel) · POSIT (a
"derivation" with an inserted step) · OVERCLAIM (inflated past the formula) · NEUTRAL.

| # | date | commit | verdict |
|---|---|---|---|
| 1 | 03-17 | the formula a₀=(c/2)√(Gρ_c) | **SOLID** (math verified exact) |
| 2 | 03-17 | show all H₀ cases | SOLID (honest H₀-dependence) |
| 3 | 03-17 | testable predictions + SPARC data | SOLID (real SPARC) |
| 5 | 03-17 | remove proprietary refs | NEUTRAL |
| 6 | 03-18 | JWST high-z test | MOND-APP (a high-z prediction) |
| 8 | 03-18 | 7 example applications | MOND-APP |
| 15 | 03-18 | "deriving cosmological constant from MOND" | OVERCLAIM (the a₀–Λ identity is real; "deriving Λ" overreaches) |
| 17 | 03-18 | "A Cosmological Origin…" paper | SOLID formula + mild "origin" overreach |
| 20 | 03-18 | update paper | NEUTRAL |
| 24 | 03-18 | full SPARC verification (175 gal) | **SOLID** (real data) |
| 25,26 | 03-18 | 8+8 applications (UDGs, TDGs…) | MOND-APP |
| 28 | 03-18 | "quantum foundations implications" | **OVERCLAIM** |
| 32 | 03-18 | "unified theory section" | **OVERCLAIM** |
| 42,43,46,47 | 03-18 | "ALL 452 problems solved" | **OVERCLAIM** (verified: "COMPLETE VALIDATION: 452 PROBLEMS") |
| 44,45,58 | 03-18/19 | email / temp file / DOI | NEUTRAL |
| 48,49,51,52,55,56,57 | 03-19 | "proofs of unsolved problems" | **OVERCLAIM** |
| 59 | 03-19 | "rigorous Derivations (replaces speculative Proofs)" | self-correction (good instinct) |
| 60 | 03-19 | visualizations | NEUTRAL |
| 62 | 03-19 | "9 derivation papers establishing priority" | OVERCLAIM |
| **63** | **03-19** | **H₀ from galaxy dynamics** | **SOLID + HIS** (the a₀→H₀ probe) |
| 130 | 03-22 | "65-formula reference" | NUMEROLOGY (creeping in) |
| 134 | 03-22 | JWST/El Gordo/Particle Physics modules | MIXED (JWST/El Gordo MOND-APP; particle physics numerology) |
| **150** | **03-23** | **horizon-thermodynamics derivation** | **SOLID prediction (evolving a₀) + POSIT derivation** |
| 156,158 | 03-23 | "first-principles derivation" | POSIT (the √(8π/3) is Friedmann-solid; the factor-2 is asserted via the Bekenstein/horizon mass — a heuristic, not a proof) |
| 176 | 03-24 | "Z universal role" papers | NUMEROLOGY |
| 189 | 03-25 | interactive visualizations | NEUTRAL |

## What the verification establishes
- **SOLID, and genuinely his:** the formula (#1), the SPARC verification (#3, #24), the
  evolving-a₀ prediction (#150), and the a₀→H₀ probe (#63). All March, all checked sound.
- **POSIT, not proof:** the "first-principles derivation" (#150, #156, #158). The Friedmann
  factor √(8π/3) is solid; the factor of 2 (Schwarzschild/Bekenstein/horizon) is *inserted*,
  so it's a heuristic. The *formula and prediction are correct*; the *derivation* is not a theorem.
- **OVERCLAIM, within days:** "452 problems," "proofs of unsolved problems," "quantum
  foundations," "unified theory" (#15, #28, #32, #42–62). The inflation started ~March 18,
  *before* the explicit numerology at #83 (March 20), and ballooned from there.

So the honest separation, verified commit by commit: a **real, novel, sound kernel from
March** (one formula + two predictions, all his), wrapped almost immediately in
overclaiming, then buried under numerology from #83 on. The kernel is what survived; the
wrapping is what the audit removed.

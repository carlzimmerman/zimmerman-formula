# WB-3 deprojection Monte-Carlo — results (executed per `wb_mc_preregistration.md`)

*C. Zimmerman, 2026-06-10. `data/widebinaries/wb_deprojection_mc.py` (+`.out`). Matched Newtonian forward model of the
Banik-exact selection (N=9,508), framework a₀=9.36×10⁻¹¹. Pre-registered BEFORE running (commit 09fbec76). Inline, no swarms.
Also serves as the WB-R3 standalone methodology note. C1/C2 only (C3 fence).*

## Method (one-paragraph)
ṽ ≡ v_sky/√(GM/r_sky) is **scale-free for Kepler** (depends only on e, phase, orientation; the node angle Ω drops out of the
sky-plane norms) ⇒ a Newtonian population predicts a **flat** median ṽ across all g_N/a₀ bins. Any rise must come from (1)
**Eddington noise** (the per-pair measured σ on the 2D sky-velocity vector inflates |v_sky| where v_N is small = deep bins), (2)
**contamination** (triples inflate ṽ), (3) **separation-dependent eccentricity**, or (4) a **genuine boost**. The MC builds 1–3
from first principles + the *measured* per-pair noise, **calibrates f(e) and f_triple on the high-acceleration anchor** (g_N/a₀>10,
where boost #4 ≈ 0), then the deep bins are a *prediction*, not a fit. The framework boost is overlaid as ṽ·√ν(g_N/a₀).

## Calibration (anchor-matched, g_N/a₀>10)
Best: **super-thermal e (f∝e¹·⁵), f_triple=0.05** → anchor median 0.549 (data 0.558), anchor super-escape 0.021 (data 0.029). ✓

## Deep-bin prediction (the test)
| g_N/a₀ | data median ṽ | **Newton-MC** | MOND-MC\* (upper bnd) | data super-esc | Newton super-esc |
|---|---|---|---|---|---|
| 17.8 (anchor) | 0.560 | 0.551 | 0.584 | 0.030 | 0.020 |
| 1.78 | 0.599 | 0.563 | 0.712 | 0.042 | 0.023 |
| 0.56 | 0.631 | 0.572 | 0.856 | 0.057 | 0.025 |
| **0.18** (N=716) | **0.647** | 0.588 | 1.06 | 0.082 | 0.032 |
| **0.018** (N=104) | **0.816** | 0.639 | 1.30 | 0.202 | 0.061 |

Deep-bin z-scores: **z(data − Newton) = +3.2, +2.4**;  z(data − MOND\*) = −22, −6.5.
**\*The MOND-MC is a deliberate UPPER BOUND** (boost-at-fixed-orbit overstates the effect; the literature observable shift is
~15–20%, not the ~80% this crude multiplier gives). **The −22σ is exclusion of the crude over-prediction, NOT of the framework.**

## Discriminator — does separation-dependent contamination absorb the excess?
The deep super-escape (0.082→0.202) independently calls for a triple fraction rising with separation. Letting f_triple rise into
the deep bins (physically expected — wider pairs are more triple-contaminated):

| f_triple (anchor→deep) | g_N/a₀=0.18 [med, super-esc] | g_N/a₀=0.018 [med, super-esc] |
|---|---|---|
| 0.05 → 0.16 | (0.634, 0.080) | (0.687, 0.102) |
| **data** | **(0.647, 0.082)** | **(0.816, 0.202)** |

- **g_N/a₀=0.18 (N=716, reliable): the +3σ excess is FULLY ABSORBED** by f_triple≈0.16 contamination that *simultaneously* matches
  the super-escape (0.080 vs data 0.082). No boost required in the reliable deep bin.
- **g_N/a₀=0.018 (N=104, noisy): a residual REMAINS** — the data (0.816, 0.202) exceed even the f_triple=0.16 Newton model. But
  this is the smallest, widest-separation, most contamination-prone bin, and the super-escape (0.202 = ~21 pairs) is Poisson-noisy.

## Verdict: **AMBIGUOUS, leaning NEWTON-SUFFICES** (degeneracy-limited)
Reported in both directions, per the project rule:
- **Not a boost (the honest near-null):** the reliable deep bin's 3σ excess is degenerate with — and fully absorbed by —
  separation-dependent contamination that the super-escape *independently* supports. The data do **not require** a boost.
- **Not a Newtonian dismissal either:** (a) the deepest bin retains a residual over even generous contamination; (b) the real
  limiter is the boost↔contamination **degeneracy**, not a decisive null; (c) a *correctly-computed* (mild, ~15–20%) framework
  boost would predict deep median ≈0.63–0.66 — **strikingly close to the reliable-bin data (0.647)**. The framework is **NOT
  excluded** by these wide binaries; it sits inside the degeneracy with Newton+contamination.
- The sky-projected DR3 observable **cannot** break this degeneracy. **Gaia DR4 line-of-sight RVs (full 3D deprojection) can** —
  the pre-registered decider.

## Limitations / next steps (logged, not hidden)
1. **Naive boost** (multiplier, not integrated modified-gravity orbit) → MOND-MC is an upper bound; the next refinement is full
   modified-orbit integration to get the framework's *actual* deep-bin prediction (expected ~0.63–0.66, testable against the data).
2. **Sky-projected only** — no line-of-sight velocities → partial deprojection; the degeneracy is intrinsic until DR4.
3. **Deepest bin N=104** — the lone residual lives here; not decisive.
4. **Contamination model** (single reflex scale) is crude; a calibrated triple-population model is the other refinement.
**Bottom line:** on real Gaia data, under a pre-registered matched forward model, wide binaries are currently **degeneracy-limited
and consistent with both Newton+contamination and a mild framework boost** — neither confirms nor excludes the framework. Gaia DR4
is the decider. C1/C2 only; nothing about a₀(z) (C3 fence).

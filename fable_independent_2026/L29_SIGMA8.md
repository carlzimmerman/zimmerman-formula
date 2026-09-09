# L29 — is L9's late-roll prediction already excluded by the measured S₈?

2026-09-08. Lane L29 of [CHARTER.md](CHARTER.md).
Script: [L29_sigma8_test.py](L29_sigma8_test.py) → [L29_sigma8_test.out](L29_sigma8_test.out).
**3 PASS, 6 FAIL.** All **three controls PASS** (C0, C1, C1b); every FAIL is a substantive finding, none a
machinery failure.

Target: the sharp prediction of [L9_late_transition.py](L9_late_transition.py) — the one mechanism in this
programme that cleared the gate it was proposed against — σ₈ = 0.845–0.861, H₀ = 68–72, Ω_m = 0.27–0.31,
Ω_Λ = 0.25–0.32, f(0) = 0.57–0.64, t₀ = 13.7 Gyr, on 146/3721 canonical and 269/3721 alt refined grid points.

## Verdict in one line

**Alive only in a corner, and only under an assumption the programme has already excluded.** The high σ₈ is
*not* the problem — Ω_m < 0.3 converts it into an S₈ that straddles Planck — but MODEL A's roll multiplies the
Weyl potential that lenses light, and that puts the cosmic-shear amplitude 9–34σ above every survey. The only
escape is a lensing/dynamics decoupling of 92–100%, which is the same density-dependent screening L6 excluded
at 12.8σ and which would break the observed agreement of cluster lensing and hydrostatic masses.

## The PASS/FAIL lines

| # | check | result |
|---|---|---|
| C0 | machinery reproduces L9's published surviving region to the digit | **PASS** |
| C1 | S₈ conversion reproduces the concordance value and the known size *and sign* of the S₈ tension | **PASS** |
| C1b | Limber machinery is an identity on ΛCDM, exactly linear in amplitude, and agrees with the naive formula | **PASS** |
| C2 | some part of the region is compatible with cosmic-shear S₈ at **2σ on every reading** | **FAIL** |
| C3 | …at **3σ on every reading** | **FAIL** |
| C4 | a single point fits a measured H₀ and an acceptable S₈ together, on every reading | **FAIL** |
| C5 | with L9's internal growth gate replaced by the measurements, part of the region survives on every reading | **FAIL** |
| C6 | L9's cosmology leaves a₀ = κ c √(G ρ_Λ) inside k03's 9.47% BTFR floor | **FAIL** |
| C7 | the mechanism survives current data on the **self-consistent** reading | **FAIL** |

C2, C3, C4, C5 and C7 fail on reading (ii) **and only on reading (ii)**. C6 fails independently of the
lensing question.

## The measurements, and where they come from in this repository

| dataset | S₈ | in-repo provenance |
|---|---|---|
| Planck 2018 TT,TE,EE+lowE | 0.832 ± 0.013 | `real_research/reviews/mi_cosmo_perturbations_2026.py:166`; Planck 2018 VI, A&A 641 A6 |
| KiDS-1000 3×2pt (2021) | 0.759 +0.024/−0.021 | `…/gc_consequences/w_gradient_cmb_calc.py:131`; Heymans+2021 A&A 646 A140 |
| DES Y3 3×2pt (2022) | 0.776 ± 0.017 | `…/gc_consequences/w_gradient_cmb_calc.py:130`; DES Collab. 2022 PRD 105 023520 |
| DES Y3 + KiDS-1000 joint | 0.790 +0.018/−0.014 | `…/gc_consequences/w_gradient_cmb_calc.py:132`; DES+KiDS 2023 OJAp 6 36 |
| HSC Y3 cosmic shear | 0.769 ± 0.031 | `ai_slop/research/predictions/02_DESI_STRUCTURE_GROWTH.py:110`; Li+2023 PRD 108 123518 |
| **KiDS-Legacy (2025)** | **0.815 ± 0.016** | `real_research/reviews/mi_cosmo_perturbations_2026.py:1009`; Wright+2025 |
| 2026 lensing compilation | 0.819 ± 0.007 | `real_research/reviews/dm_candidate_test.py:32` (2026 review 2602.12238) |
| DESI DR9 galaxy×lensing | 0.840 ± 0.020 | `…/reviews/GHOST_CONDENSATE_CONSEQUENCES_2026-06-19.md:68` |
| eRASS1 cluster counts | 0.860 ± 0.010 | `…/cluster_measurement/routeB_dynamical_mass_calibration_eta.py:31,65`; Ghirardini+2024 A&A 689 A298 |

Two provenance notes, both stated because they run against this lane's own convenience.

- The corpus's `THE_HONEST_LCDM_STRESS_BRIEF.md:69` puts S₈ on the **DO-NOT-CITE** list *as a ΛCDM stress*,
  because KiDS-Legacy and HSC-Y3 moved **up** toward Planck. That cuts *in the model's favour* here: the
  upward revision makes the shear constraint **less** hostile to a high-σ₈ model. This lane therefore decides
  its checks on **KiDS-Legacy**, the most favourable modern set, not on the older, lower KiDS-1000/DES Y3,
  which would have manufactured a harsher verdict.
- eRASS1's high S₈ may itself be a WL mass-calibration artefact
  (`routeB_dynamical_mass_calibration_eta.py:184-197`), and this lane's own L18 shows the hydrostatic bias runs
  against the framework. eRASS1 is reported, not leaned on.

The six "shear" rows are **not** six independent measurements (KiDS-1000 and KiDS-Legacy are the same survey
before and after its revision; DES Y3 enters twice; the 2026 compilation re-analyses all of them), so
requiring all six at once is over-strict and is reported only as the strict end of the range.

## The three readings of the same model

**(i) NAIVE** — S₈ = σ₈ √(Ω_m/0.3) from each survivor's own pair. This is what L9's quoted prediction implies
and the reading most favourable to the model.

**(i′) LIMBER, no roll** — the same region through a genuine Limber integral with `g` removed from the lensing
kernel. This is the physically correct "no roll in lensing" number: the Weyl source carries the **physical**
ω_m, which is CMB-fixed and identical to ΛCDM's, so the √(Ω_m/0.3) discount the naive formula applies is
partly spurious. It runs **higher** than (i) by up to 3.1%.

**(ii) LENSING-CONSISTENT** — in MODEL A the roll multiplies the Poisson source, so with no slip it multiplies
the Weyl potential: k²(Φ+Ψ)/2 = −(3/2) g(a) ω_m (100/c)² δ/a. Because ω_m is CMB-fixed and identical in both,
the shear-power ratio to ΛCDM is set by [g(z) D_model(z)/D_ΛCDM(z)]² weighted by the lensing kernel — the
script evaluates the full Limber integral, geometry included. **L9 explicitly did not run this gate**
("lensing versus dynamics … that gate is not run here"); it is what this lane adds.

| footing | σ₈ | Ω_m | (i) S₈ | (i′) S₈ | ḡ_lens | (ii) S₈ |
|---|---|---|---|---|---|---|
| canonical (F = 1.819) | 0.853–0.861 | 0.276–0.301 | 0.818–0.862 | 0.832–0.846 | 1.338–1.441 | **1.118–1.199** |
| alt (F = 1.681) | 0.845–0.861 | 0.274–0.315 | 0.808–0.882 | 0.828–0.851 | 1.273–1.415 | **1.060–1.175** |

## The surviving fraction against each dataset

Fraction of L9's surviving region inside 2σ / 3σ, canonical (146) and alt (269), with Planck's σ₈
normalisation error (0.74%) added in quadrature — a concession to the model.

| dataset | (i) 2σ | (i) 3σ | (i′) 2σ | (i′) 3σ | (ii) 2σ | (ii) 3σ |
|---|---|---|---|---|---|---|
| Planck 2018 | 99% / 77% | 100% / 97% | 100% / 100% | 100% / 100% | 0% / 0% | 0% / 0% |
| KiDS-1000 | 0% / 1% | 41% / 35% | 0% / 0% | 3% / 12% | 0% / 0% | 0% / 0% |
| DES Y3 | 0% / 3% | 31% / 31% | 0% / 0% | 0% / 1% | 0% / 0% | 0% / 0% |
| DES Y3 + KiDS-1000 | 23% / 28% | 79% / 56% | 0% / 0% | 100% / 86% | 0% / 0% | 0% / 0% |
| HSC Y3 | 38% / 34% | 100% / 86% | 1% / 4% | 100% / 100% | 0% / 0% | 0% / 0% |
| **KiDS-Legacy** | **83% / 61%** | **100% / 90%** | **100% / 95%** | **100% / 100%** | **0% / 0%** | **0% / 0%** |
| 2026 compilation | 50% / 42% | 79% / 56% | 38% / 36% | 100% / 86% | 0% / 0% | 0% / 0% |
| DESI DR9 lensing | 100% / 100% | 100% / 100% | 100% / 100% | 100% / 100% | 0% / 0% | 0% / 0% |
| eRASS1 clusters | 52% / 62% | 82% / 80% | 72% / 68% | 100% / 100% | 0% / 0% | 0% / 0% |

On reading (ii) the z-scores are **+9.1 to +33.6σ** across every dataset on both footings. That is not a
tension; it is an exclusion, and it does not depend on which survey is used.

## What was found, item by item

**1. The high σ₈ is not the kill, and that is a genuine correction to the lane's own premise.** Because L9's
survivors carry Ω_m = 0.274–0.315, below concordance, S₈ = σ₈√(Ω_m/0.3) = 0.808–0.882 — it **straddles**
Planck's 0.832 ± 0.013, sits +1.2 to +5.8σ from the older shear values, and lands **within 2σ of the revised
KiDS-Legacy over 61–83% of the region** and inside 1σ of DESI DR9 lensing and eRASS1. The S₈ tension running
the other way does **not** by itself close the mechanism.

**2. The kill is the gate L9 said it did not run.** With the roll in the Weyl potential, the kernel-weighted
factor is ḡ = 1.27–1.44 (not the full F = 1.68–1.82, because the shear kernel peaks near z ≈ 0.35 where the
roll is only partly done), giving S₈,eff = 1.06–1.20 against measurements at 0.76–0.86 with errors 0.01–0.03.

**3. How much escape would be needed, quantified.** For reading (i)/(i′) to be legitimate the shear-kernel
roll factor would have to satisfy ḡ ≤ 1.000–1.028, against an actual 1.27–1.44 — the roll must be suppressed
in the **lensing** potential by **92–100%** relative to the dynamical one. That is a lensing/dynamics
decoupling of order F, and the same decoupling makes cluster weak-lensing masses disagree with X-ray
hydrostatic masses by ~1.7–1.8×, against an observed agreement at the tens-of-percent level (L9's own open
item (ii)). **The two halves close on each other: with the screening, L6 kills it; without it, cosmic shear
does.**

**4. The H₀ angle does not cut the way the brief expected.** Across the region H₀ and S₈ are **anti-correlated
at r = −0.999**: the high-H₀ end is also the low-S₈ end, so the region does *not* have to choose between them.
The real internal tension is different and sharper — **the canonical footing cannot reach the Planck H₀ at
all** (H₀ ≥ 68.90, i.e. ≥ 2.9σ above 67.36 ± 0.54; 0/146 points within 2σ). 57/146 canonical and 58/269 alt
points sit within 2σ of SH0ES. **The mechanism, if real, is a high-H₀ model.**

**5. The growth gate on real data is a *milder* cut than L9's internal one.** L9 reported that tightening its
Δχ²_RSD gate from 3σ to 2σ empties the canonical footing. Replacing it by the **absolute** goodness of fit to
the same 7 RSD points (7 d.o.f.) leaves 115/146 canonical and 236/269 alt at p > 0.05, and 100% at p > 0.003 —
because L9's Δχ² is measured against ΛCDM's own χ² = 6.06 rather than against the degrees of freedom. The
region's own absolute χ² is 11.34–15.06 (canonical) and 9.16–15.04 (alt). **L9's "boundary result" framing is
slightly harsher than the data require**; the real cut comes from S₈, not from RSD.

**6. C6 — a new constraint on the coefficient, independent of the lensing question.** k03 established that
a₀ = κ c √(G ρ_Λ) scales as H₀ *at fixed Ω_Λ*, so the coefficient question is degenerate with the H₀ tension.
**L9's closure does not hold Ω_Λ fixed** — 1 = F(Ω_m + Ω_r + Ω_Λ) forces ω_Λ down by a factor **0.38–0.54**.
Since ρ_Λ ∝ ω_Λ:

| reading of the G in a₀ = κ c √(G ρ_Λ) | a₀ shift | inside k03's 9.47% BTFR floor | κ needed to hold a₀ |
|---|---|---|---|
| the **local** G₀ | −38% to −27% (0.135–0.210 dex) | **0/146 and 0/269** — also outside DR4's 21% reach | 0.68–0.81 (2.9–6.1σ from 0.465 ± 0.076 and 0.551 ± 0.043) |
| the **cosmological** F G₀ | −17% to −5% | 18/146 and 96/269 | 0.53–0.60 (0.1–1.8σ) |

Which G enters is not settled here, so both are carried. Either way **the two questions interact**, and this
is not a restatement of k03: k03's degeneracy was stated at *fixed* Ω_Λ, and L9's closure is precisely a
mechanism that moves Ω_Λ.

## The corner, stated precisely

If — and only if — an unspecified mechanism removes the roll from the shear signal entirely, a corner
survives the RSD fit, KiDS-Legacy S₈ and a measured H₀ simultaneously:

| footing | z_t | W | σ₈ | S₈ | H₀ | Ω_m | Ω_Λ | fraction |
|---|---|---|---|---|---|---|---|---|
| canonical | ≤ 0.132 | 0.461–0.521 | 0.853–0.856 | 0.818–0.833 | 71.0–72.0 | 0.276–0.284 | 0.266–0.274 | 57/146 |
| alt | ≤ 0.180 | 0.441–0.527 | 0.845–0.849 | 0.808–0.826 | 71.0–72.2 | 0.274–0.284 | 0.311–0.321 | 58/269 |

**This corner does not deserve a preregistration**, because the assumption that buys it is the one L6 and L9's
own T8 already excluded, and because on reading (ii) it carries S₈,eff = 1.06–1.14 — an exclusion at ~10–20σ.
What it does deserve is to be recorded as the shape a surviving cosmology of this kind would have: high H₀
(SH0ES-like, ~71–72), low Ω_Λ (0.27–0.32), σ₈ ≈ 0.85, and Ω_m ≈ 0.28.

## What this lane does NOT show

It is not testing a rescue. **L9's mechanism does not solve the cluster problem** — its T8 already showed that
a uniform g(z) supplies 0.97 between z = 0.0037 and z = 0.090 against a required 2.2–5.1, which is separate
and still fatal. Nothing here weakens or strengthens that. This lane asked only whether the one mechanism that
cleared its own gate is *allowed* by data, and the answer is: not on the reading its own construction implies.

It does **not** exclude a non-uniform or non-monotone coupling, nor a model in which the lensing and dynamical
potentials genuinely differ. But such a model is no longer the MODEL A tested here, owes an action (L9's item
(i)), and immediately inherits the cluster lensing-versus-hydrostatic-mass problem.

## For the handoff ledger

> **A29.** L9's late-roll prediction is **not** killed by the high σ₈ — Ω_m < 0.3 converts it into
> S₈ = 0.808–0.882, straddling Planck and within 2σ of KiDS-Legacy over 61–83% of the region. It **is** killed
> by the lensing gate L9 left unrun: with the roll in the Weyl potential the shear amplitude is ḡ = 1.27–1.44×
> ΛCDM, giving S₈,eff = 1.06–1.20 at **+9 to +34σ** against every survey. The escape needs a 92–100%
> lensing/dynamics decoupling, i.e. exactly L6's excluded screening, and would break cluster lensing-vs-HSE
> mass agreement. Two side results: (a) the region **cannot** sit at the Planck H₀ on the canonical footing
> (0/146 within 2σ; H₀ ≥ 68.9), so the mechanism is intrinsically a high-H₀ model, and H₀ and S₈ are
> anti-correlated (r = −0.999) rather than in conflict; (b) L9's closure drives ω_Λ down by 0.38–0.54, moving
> a₀ = κ c √(G ρ_Λ) by −38% to −5% and putting it outside k03's 9.47% BTFR floor at every point on the
> local-G reading — a **new** constraint, since k03's H₀ degeneracy was stated at fixed Ω_Λ.
> `L29_sigma8_test.py`, 3 PASS / 6 FAIL, all controls PASS.

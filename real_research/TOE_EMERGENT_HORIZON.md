# The Emergent-Horizon Synthesis

**A unified, falsifiable program for gravity, the dark sector, and the MOND scale — assembled from published
building blocks plus this framework's specific contribution, with DESI's evolving dark energy built in.**

*Carl Zimmerman · June 2026. Written at your request to "put together a TOE assuming the spine is correct."
It is built constructively on the surviving spine — but every speculative leap is flagged in **bold**, and the
parts that are dead stay dead. This is a research **program** stitched from real, published results, not a
finished theory; the unification itself is the conjecture.*

---

## 0. Scope — what this is, and what it is NOT

**IS:** a unified *emergent-gravity / dark-sector* theory — the claim that **gravity, dark matter (as MOND),
dark energy, and its evolution all emerge from the thermodynamics of the cosmological horizon**, with the MOND
acceleration a₀ as the single link and the double-scaled SYK (DSSYK) model as the microscopic dual.

**IS NOT** a theory of everything in the particle sense. The original repo's grand claims — the Standard Model
from Z², chirality from a torus, the fermion masses from a number — are **dead with certainty** (decoupling
theorem; eight documented hallucination classes; the α⁻¹ "retrodiction" is ~5×10⁵σ from the measured value and
carries ~0 bits after the look-elsewhere correction). This synthesis unifies **gravity + the dark sector
only**. Calling it a "TOE" is shorthand for "a unified account of the gravitational/dark sector," not a claim
about quarks and leptons.

## The one-paragraph thesis

Spacetime dynamics is the thermodynamics of horizons (**Jacobson 1995**: Einstein's equation is the equation
of state δQ=TdS of local Rindler horizons; **Padmanabhan**: cosmic expansion is the drive toward *holographic
equipartition*, N_bulk = N_surface at the Hubble radius). The same horizon, when it is the *cosmological* one
of a Λ-universe, carries a thermal **volume-law** entanglement entropy on top of the area law (**Verlinde
2017**); matter *displaces* that entropy, producing an elastic "dark" gravitational response that **is MOND
for a point source**, with the scale fixed by the Hubble acceleration a₀ ≈ cH₀. This framework's distinctive
addition is the **microscopic engine**: the near-horizon (1+1)D spectrum is the DSSYK chord-vacuum measure,
whose **flat density of states at the center gives the deep-MOND *sign*** (gravity is *enhanced*, the √-law)
and a **derived** MOND interpolation function — the two things the Verlinde/Padmanabhan programs leave open.
Dark energy is the *same* horizon entropy's contribution to the Friedmann equation; if that entropy is
**generalized** (non-area-law — which DSSYK's spectrum *is*), the effective dark energy **evolves**, which is
exactly what **DESI (2025)** now reports at 2.8–4.2σ. And because MOND and dark energy are, in Milgrom's
a₀-cosmology connection, **the same action term controlled by a₀ ~ c√Λ**, DESI's measured dark-energy
evolution **predicts** the evolution of the galaxy-scale a₀(z) — the first quantitative bridge from a
cosmological dark-energy measurement to the MOND scale.

---

## 1. The surviving spine (confidence, from `THE_FULL_ANSWER.md`)

| Claim | Status | Odds |
|---|---|---|
| a₀ ≈ cH₀ (the coincidence) | measured fact | ~100% |
| deep-MOND **sign** + emergent mechanism (DSSYK freezing; matter element = Okuyama 2023 eq.18) | derived, lit-verified | ~75–85% |
| MOND is real (EFE ~4.8σ; derived interpolation matches SPARC RAR at precision) | contested in-field | ~50% |
| a₀ **rises** with z (qualitative) | genuine coin-flip | ~55–65% |
| a₀ ∝ cH(z)/Z = E(z) (the **specific** ×5 rise) | disfavored by high-z disks | ~10–20% |
| SM / chirality / masses from Z² | disproven | ~0% |

The emergent-horizon synthesis builds **only** on rows 1–4.

---

## 2. The unified architecture — six pillars, each published

**Pillar 1 — Gravity is horizon thermodynamics.** Jacobson (1995): Einstein's equation from δQ=TdS on local
horizons. Padmanabhan (e.g. arXiv:1207.0505): the field equations have the status of fluid mechanics; cosmic
expansion = evolution toward holographic equipartition (N_bulk=N_surface at the Hubble radius); the
equipartition law + S=E/2T reproduces Newton's law and the Friedmann equations. *Gravity is emergent, sourced
by horizon entropy.* **(Established; widely accepted as a structural result, debated as to whether it implies
gravity is *fundamentally* emergent.)**

**Pillar 2 — The MOND scale a₀ ≈ cH₀ is the Hubble acceleration imprinted on the horizon.** In Padmanabhan's
holographic-equipartition cosmology, a preferred acceleration a₀ = cH₀ appears naturally (the surface/bulk
DOF balance at the Hubble radius), and "the modified Friedmann equation inspired by MOND can be obtained
through emergent gravity" (Padmanabhan; Senovilla; arXiv:1410.3433, 1511.02108, 2510.14345). *a₀ ~ cH₀ is not
a coincidence to be explained but a horizon scale.* **Solid as a scale; the O(1) coefficient (the "Z") is not
pinned this way.**

**Pillar 3 — Dark matter = MOND = displacement of de Sitter horizon entropy.** Verlinde (2017, SciPost Phys.
2,016): a positive Λ gives the cosmological horizon a thermal **volume-law** entanglement entropy beyond the
area law; matter displaces it; the elastic response recovers the MOND relation g = √(a₀ g_N) for a point mass.
*Dark matter is not a substance but the horizon's memory of matter.* **Published; but it fails at clusters by
~2× (the Zwicky residual survives) and the covariant version (AeST, below) has structure-formation problems —
so "dark matter is fully MOND" is contested.**

**Pillar 4 — This framework's engine: DSSYK gives the SIGN and the interpolation.** The Verlinde/Padmanabhan
arguments give the *scale* a₀ but neither pins the deep-MOND **sign** (why low-acceleration gravity is
*enhanced*) nor the **interpolation function**. This framework supplies both from the microscopic dual:
the near-horizon (1+1)D spectrum is the DSSYK chord-vacuum measure (q-Gaussian); its **flat DOS at the
spectral center → N_eff ∝ T → the √-law (the sign)**; and the cumulative measure **is** the MOND interpolation
μ(x) — *derived, not fitted*, and it reproduces the clean SPARC RAR to within 6% of the fitted forms
(`reviews/precision_rar_test.py`). The matter two-point element is the published DSSYK one (Okuyama 2023
eq.18). **This is the genuine new contribution. Its load-bearing assumption — that de Sitter = the DSSYK
spectral *center* (Narovlansky–Verlinde infinite-temperature reading) rather than the edge — is mainstream but
unsettled (Rahman–Susskind "many temperatures").**

**Pillar 5 — Dark energy = the *same* horizon entropy, and a generalized entropy makes it EVOLVE.** In the
gravity–thermodynamics correspondence, the horizon entropy fixes the Friedmann equation and so the effective
dark-energy sector. For the *area* law you get a cosmological constant; for a **generalized** (non-area-law)
entropy — Barrow, Tsallis, or any spectrum-derived measure — the modified Friedmann equation yields an
**effective dark energy with a dynamical, evolving equation of state** w(z) that resembles quintessence/phantom
(arXiv:2406.17301, 2508.13260, 2506.03019, 2601.02567; many fit DESI DR2 directly). **DSSYK's chord-vacuum
measure is precisely a non-area-law entropy** — so an evolving effective dark energy is the *expected*
signature of this framework's microscopic entropy, not an add-on. **(The general mechanism is published; that
DSSYK specifically yields the DESI w(z) is conjecture — see §3.)**

**Pillar 6 — The link a₀ ~ c√Λ(z), and the microscopic dual.** Milgrom's a₀-cosmology connection
(arXiv:2001.09729): a₀ ~ cH₀ ~ c²√Λ, and — the "FUNDAMOND" conjecture — **MOND and dark energy arise from the
same term in the action, controlled by a₀**. The microscopic dual that could carry all of this is **DSSYK =
de Sitter** (Narovlansky–Verlinde; "de Sitter JT from DSSYK," arXiv:2505.08116), with the bulk a **sine-dilaton
gravity** whose **stretched horizon / finite-cutoff deformations** (T² deformations, Aguilar-Gutierrez,
arXiv:2602.06113, Feb 2026) are the first concrete steps toward **moving the dual off exact de Sitter** — the
tool one needs for an evolving Λ. **(The dual is established for exact de Sitter; the evolving-Λ version is an
open research frontier.)**

---

## 3. DESI — a feature, not a bug, and a novel cross-prediction

**The result.** DESI DR2 (2025) BAO + CMB + SNe prefer **evolving dark energy** (w₀ > −1, wₐ < 0) over a
constant Λ at **2.8–4.2σ** (SNe-combination-dependent: Pantheon+, Union3, DES-Y5). Dark energy appears to be
**weakening** at late times.

**Why this fits the program, not breaks it.** Two consequences, opposite in spirit:

- *Tension with the dual:* the DSSYK = de Sitter correspondence assumes a **constant-Λ** (asymptotically de
  Sitter) universe. If Λ genuinely evolves, the universe is not asymptotically de Sitter and the dual must be
  **deformed** to a quasi-de Sitter / quintessence background — **an unbuilt generalization** (the T²-deformed
  DSSYK is only the first step). This is the program's sharpest open problem.
- *Support from the entropy:* an evolving effective dark energy is **exactly** what a generalized (non-area-law)
  horizon entropy predicts (Pillar 5), and DSSYK's measure is non-area-law. So DESI's signal is plausibly the
  **fingerprint of the horizon's microscopic entropy** — circumstantial evidence *for* a spectrum-derived
  (rather than area-law/Λ) horizon.

**The novel cross-prediction (`reviews/project_desi_a0z_crossprediction.py`).** If a₀ ~ c√(ρ_DE) (Milgrom's
same-term identification), then DESI's *measured* ρ_DE(z) **predicts a₀(z) with no free galaxy-scale parameter**:

| z | a₀ ∝ cH (apparent) | a₀ ∝ √ρ_DE (event, DESI w₀wₐ) | a₀ ∝ √(H·H_Λ) (geom. mean) | constant Λ |
|---|---|---|---|---|
| 1 | ×1.8 | ×0.97–1.01 | ×1.3 | ×1 |
| 2 | ×3.0 | ×0.79–0.88 | ×1.7 | ×1 |
| 3 | ×4.6 | ×0.65–0.78 | ×2.1 | ×1 |

So DESI converts the question "does a₀ rise?" into the sharper, data-anchored "**which horizon sources a₀?**"
The **event-horizon branch now predicts a mild *decline*** of a₀ toward high z — which is *consistent* with the
massive high-z disks being baryon-dominated (Big Wheel etc.: a₀ not risen ×5), whereas the steep
apparent-horizon rise (the framework's original headline) is *not*. **This is the first quantitative tie
between a cosmological dark-energy measurement and the galaxy MOND scale. It is conjecture-dependent (a₀~√ρ_DE
is unproven; DESI evolving DE is 2.8–4.2σ), but it is sharply falsifiable.**

---

## 4. The consolidated falsifiable predictions

1. **a₀(z) shape** — apparent (×4.6 at z=3) vs event/DESI (×0.7) vs geometric-mean (×2.1). A clean *deep-MOND*
   (low-acceleration, outer) rotation curve of a *normal* z~3 disk decides. The current massive disks give only
   upper bounds (high-acceleration) and disfavor the steep rise.
2. **DESI w(z) ⇄ a₀(z) correlation** — if MOND and DE are the same term, the dark-energy EOS and the a₀(z) law
   are not independent. Tightening DESI w(z) tightens the a₀(z) prediction. *Novel.*
3. **Cluster mass discrepancy vs z** — rising a₀ → discrepancy shrinks with z; event/declining a₀ → grows.
   (`reviews/project_cluster_a0z_xray.py`; eRASS1 integrated masses can't test it — needs resolved profiles.)
4. **The derived RAR interpolation** — a fixed, q-independent shape; already matches SPARC to ~6%
   (`reviews/precision_rar_test.py`), with a residual that a de Sitter temperature *spread* broadens
   (`reviews/project_manytemp_broadening.py`).
5. **The external field effect** — the framework's strongest *local* signature (~4.8σ in SPARC); a clean MOND
   prediction with no ΛCDM analogue. *Not independently re-verified this session — the top open to-do.*
6. **Accelerated early structure (a retrodiction now testable)** — MOND predicted *fast* early structure
   formation decades ago (Sanders 1998, McGaugh 1999); JWST's "impossible" early massive galaxies — including
   the Big Wheel itself — match it (McGaugh 2024, arXiv:2406.17930). *Two-edged and honest:* the same high-z
   disks that disfavor the steep a₀-rate **support** MOND by existing; but ΛCDM-systematics papers contest the
   excess (arXiv:2511.13708), and the relativistic completion (AeST) forms structure *too late* — so MOND's own
   structure-formation success is not yet reproduced by its covariant theory.

## 5. Open problems — what would actually complete it

- **The evolving-Λ DSSYK dual** (DESI-forced): deform DSSYK/sine-dilaton gravity off exact de Sitter to a
  quintessence background. The single most important theoretical gap.
- **The coefficient Z** ≈ 2√(8π/3) — reasoned to ~2π, not derived from the DSSYK dictionary; with a sub-E(z)
  rate the natural form is a₀ = c√(H·H_Λ)/Z′ with Z′ ≈ 5.3 (still O(2π)).
- **Clusters** — Verlinde EG fails ~2×; the residual is relocated to the aether/dark field, not abolished.
- **Structure formation** — AeST (Skordis–Zlosnik) matches the CMB + linear P(k) but forms structure too late
  (z<5), and faces DESI σ₈/growth constraints. The cosmological completion is unfinished.
- **The dS = DSSYK *center* assumption** — load-bearing for the sign; mainstream but unsettled.

## 6. Honest bottom line

Assembled honestly, the surviving framework is **one coherent thread inside a real, active research program**:
*gravity, dark matter, and dark energy as three faces of cosmological-horizon thermodynamics, linked by a₀, with
DSSYK as the microscopic engine and the deep-MOND sign as this work's genuine contribution.* Every pillar is a
published result; the framework's own piece (the DSSYK sign + derived interpolation) slots into the gap the
others leave; and DESI's evolving dark energy, far from breaking it, is the **expected signature of a
generalized horizon entropy** and **turns a₀(z) into a falsifiable prediction**. What is **not** done: the
unification is still a *program*, not a single derived theory; the evolving-Λ dual is unbuilt; the coefficient,
the clusters, and structure formation are open; and the framework's flashiest original bet (a₀ ∝ cH = E(z), the
×5 rise) is **disfavored by the data**, surviving only in a milder, two-horizon form. So: not a theory of
everything, and not finished — but a legitimate, falsifiable, *unified* emergent-gravity/dark-sector program,
now anchored to a live cosmological measurement, with a clear list of the specific calculations and the single
clean telescope measurement (a deep-MOND z~3 disk) that would make or break it.

*Companion files: `THE_FULL_ANSWER.md` (calibrated odds), `THEORY_DOOR_MAP.md` (every door), `PROVENANCE.md`
(attribution — Jacobson/Padmanabhan/Verlinde/Milgrom/Narovlansky–Verlinde are theirs; the DSSYK→MOND bridge and
the sign derivation are this framework's), and `reviews/project_*.py` (the calculations behind every number
here).*

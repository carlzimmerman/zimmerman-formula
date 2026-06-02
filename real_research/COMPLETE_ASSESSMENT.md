# The Zimmerman / Z² Framework — A Complete Assessment

**Carl Zimmerman · June 2026**
*The full arc, honestly: from a 452-claim "theory of everything" to a single falsifiable
prediction. Every number below is reproducible from the cited scripts in this repository.*

---

## Executive summary

This framework began as a unified "theory of everything" deriving the fine-structure constant,
particle-mass ratios, mixing angles, cosmological parameters, three generations, and dozens of
other quantities from one geometric number, **Z² = 32π/3**. Subjected to a complete, adversarial
review, almost all of it dissolves: the constant "predictions" are **numerology with ~0 bits of
evidence**, and the geometric "derivation" of Z² **does not close**. One physical idea survives the
demolition — that the MOND acceleration scale tracks the cosmic one, **a₀ = cH/Z**, and therefore
**evolves as a₀(z) = a₀(0)E(z)**. Developed honestly, this becomes a coherent, CMB-safe,
relativistic **implementation** of an idea that is *Milgrom's* (2014), not original here; its
observable is **degenerate with ΛCDM** on everything currently measurable; and after a two-round
red-team its **one genuinely distinctive prediction** — a redshift-weakening External Field Effect —
requires a **next-decade observing campaign** to test.

**Final verdict:** a coherent, falsifiable, CMB-safe implementation of Milgrom's evolving-a₀ idea,
with two free O(1) parameters, no current distinguishing evidence, and a single distinctive test
that is real but a decade out. The most transferable output is the **falsification methodology**,
not the model.

| | status |
|---|---|
| α⁻¹, masses, mixing angles, Ω | **dead** — numerology, ~0 bits; 10⁵–10⁶σ misses in real units |
| Z² = 32π/3 from topology | **dead** — category error; does not derive |
| a₀ = cH/Z (premise) | inherited coincidence (Milgrom 1983) + chosen coefficient |
| a₀(z) = a₀(0)E(z) (evolution) | **not novel** (Milgrom 2014); ΛCDM-degenerate to z≈2.3 |
| θ-coupled AeST action + linear CMB-safety | **sound** but a tuned/inherited host; the real residual |
| EFE ∝ 1/E(z) | the **one distinctive** prediction; next-decade to test |

---

## Part I — The demolition: what did not survive

### I.1 The constant "predictions" are numerology (~0 bits)

The headline α⁻¹ = 4Z²+3 = 137.041 was found by a brute-force search (BriareusFlow) over ~34,000
closed-form expressions. Reconstructing that search faithfully (`reviews/false_discovery_rate.py`,
verified line-by-line against `ai_slop/BriareusFlow/pattern_search.py`) gives **34,073 candidate
values**, and the look-elsewhere result the repo never computed:

- A search this size matches an **arbitrary** O(100) target to ≤1% **with certainty**, to ≤0.1%
  **99.4%** of the time, and to the quoted **0.004% precision ~19.9% of the time.**
- 4Z²+3 is the single best α⁻¹ hit — but it is **1 of 34,073**, and hitting α to that precision is
  a one-in-five coincidence for *any* number near 137. **Evidential weight ≈ 0 bits.**

Restating each "match" in units of the measurement's **actual** uncertainty
(`reviews/OPUS_PHYSICS_REVIEW.md`, recomputed from CODATA-2022/PDG/Planck-2018) converts the
"spectacular" results into decisive falsifications:

| quantity | formula | predicted | measured (±1σ) | **error in σ** |
|---|---|---|---|---|
| α⁻¹ | 4Z²+3 | 137.04129 | 137.035999177(21) | **≈ 2.5×10⁵ σ** ❌ |
| m_p/m_e | (4Z²+3)·67/5 | 1836.353 | 1836.152673426(32) | **≈ 6.3×10⁶ σ** ❌ |
| sin²θ_W | 3/13 | 0.230769 | 0.23122(4) | **≈ 11 σ** ❌ |
| α_s(M_Z) | √2/12 | 0.117851 | 0.1179(9) | ≈ 0.05 σ ✓ |
| m_H | (11/8)·m_Z | 125.38 | 125.25(17) | ≈ 0.8 σ ✓ |
| Ω_Λ, Ω_m | 13/19, 6/19 | 0.6842, 0.3158 | 0.6847(73), 0.3153(73) | ≈ 0.07 σ ✓ |

The pattern is the tell: the constants known to ten digits (α, m_p/m_e) are **falsified by
hundreds of thousands of σ**, and the ones that "agree" are measured to ~0.1–1% — exactly the
regime where the search hits ~100% of arbitrary targets. No row supports the hypothesis.

### I.2 The Z² = 32π/3 "derivation" does not close

`core_theory/THEORETICAL_FOUNDATIONS.md` and the eta-invariant documents furnish a topology story
that, audited, fails on every load-bearing step (`reviews/OPUS_PHYSICS_REVIEW.md` §4):

- **Two incompatible origins** for the same number — a Wilson-loop holonomy (Z = 2√(8π/3)) and an
  eta-invariant (Z² = 8×(4π/3)).
- A **category error**: the repo sets η_local(R³/ℤ₂) = 4π/3 and states (in its own
  `V11_VERIFICATION_AUDIT.md`) that this is *"the volume of the unit 3-ball B³."* But an η-invariant
  of this operator, computed by the very ζ-regularization claimed, is a **rational** number
  (Hurwitz-ζ/Bernoulli values at s≤0); **4π/3 is transcendental** and cannot equal it
  (`reviews/eta_invariant_reality_check.py`). 4π/3 is the **divergent Weyl/volume term**, a
  different object than the finite η — and the repo's own `NEW_MATH_DIRECTIONS.md` admits the finite
  piece "is an Epstein-zeta number, NOT 4π/3."
- An **openly abandoned** generation-count ("Wait—this gives 1, not 3. Let me reconsider," then a
  fudge to 6-of-8 fixed points) and a **backwards** RG argument (α⁻¹=137.04 assigned to the UV scale
  where it should be < 128).

### I.3 What survived

Exactly one physical idea: **a₀ = (c/2)√(Gρ_c) = cH/Z** — the MOND scale equals the cosmic
acceleration scale.

---

## Part II — The survivor, developed

### II.1 The premise. `a₀ = cH/Z`, Z = 2√(8π/3) = 5.789. The √(8π/3)=2.894 is exact Friedmann
physics; the coefficient is a posit. a₀ ≈ cH₀ is **Milgrom's 1983 coincidence** (he used a₀≈cH₀/2π);
the framing here just swaps 2π for a 9%-different O(1) number. The match is ~2–6% and H₀-dependent,
and the coefficient is **not unique** (29/5 = 5.80 fits the data value slightly better than
√(32π/3) = 5.789). One number, one free coefficient — no evidential content by itself.

### II.2 The evolution. If a₀ tracks ρ_c and ρ_c falls with expansion, a₀ must have been larger in
the past: **a₀(z) = a₀(0)·E(z)**, E(z) = √(Ω_m(1+z)³+Ω_Λ). The coefficient Z **cancels** in the
ratio, so this is coefficient-free — the framework's one distinctive, falsifiable claim. **It is not
original:** Milgrom himself proposed a₀ ∝ cH evolving with cosmic time in **2014** (Phys. Rev. D,
arXiv:1412.4344). The framework only fixes a particular coefficient and exponent.

### II.3 The data. Fitting a₀(z) = a₀(0)E(z)^p to SPARC (z≈0), Vărăşteanu (z≈0.05) and MUSE-DARK
(z≈0.9) gives **p = 0.80 ± 0.17**, naively rejecting constant a₀ at 5.0σ
(`a0_powerlaw_confrontation.py`). A stress-test (`reviews/stresstest_piece3_evolution.py`) cuts that
down honestly: **jackknife** — dropping the single z≈0.9 point collapses it to **1.2σ** (the whole
signal rides on one measurement); **inter-method systematic** — the two local points (1.20 vs 1.69
at the same z) disagree at 1.7σ, proving a ~0.28 systematic the errors miss, which drops the
rejection to **~2σ**; **ΛCDM-degenerate** — halo evolution and dispersion-vs-rotation selection both
push apparent a₀ up with z. **Honest status: a ~2σ hint, not a detection.**

### II.4 The geometric action. Promote AeST's (Skordis–Złošnik 2021) constant a₀ to the aether
expansion, **a₀ → a₀(θ) = cθ/(3Z), θ = ∇_μA^μ**. On FRW θ = 3H exactly, so a₀(z) = cH(z)/Z is a
field-equation output (`reviews/theta_3H_coupling.py`). A bound galaxy still sees θ ≈ 3H(z) to ~1
part in 10⁶ (the 3H is the background expansion; the catastrophe of θ→0 does **not** occur — it
survived the red-team).

### II.5 CMB-safety. On FRW the spatial 𝒴̄ = 0 (q⁰⁰ = −1+1 = 0), so the a₀-term is O(δφ³): **absent
from every linear equation.** The non-trivial part the standard order-counting omits — δq^{μν}∇φ̄∇φ̄
— vanishes because **δq⁰⁰ = +2Ψ − 2Ψ = 0** exactly (the unit-timelike constraint;
`reviews/redteam_the_puzzle.py`). The linear CMB is unchanged: r_s = 144.3 Mpc (Planck 144.4),
ℓ_A = 301.7 (≈301), running effect = 0 (`bridge1_linear_boltzmann.py`). The **second-order** effect
is open: at recombination a₀ is ~2×10⁴ larger and the acoustic scales sit in the deep-MOND corner
where the 𝒴^{3/2} non-analyticity makes the estimate (~0.01–0.1%) soft — a full second-order
Boltzmann run is required (`reviews/nonlinear_cmb_scoping.py`).

---

## Part III — The red-team (every piece attacked)

| piece | claim | verdict |
|---|---|---|
| 1 Premise | a₀ = cH/Z | **weak** — re-dressed coincidence, non-unique coefficient |
| 2 Evolution | a₀ ∝ E(z) | **not novel** — Milgrom 2014; ΛCDM-degenerate |
| 3 Data | constant rejected 5σ | **downgraded** — ~2σ, single-point-driven |
| 4 Action | field-equation output | **parameterizes**, doesn't derive; Z free |
| 5 Anti-screening | galaxy sees 3H | **HELD** — 3H is the background expansion |
| 6 Fork | data pick √ρ_total | **weak** — ~2σ preference, parasitic on Piece 3 |
| 7 Linear CMB-safety | a₀ absent at linear order | **HELD** — δq⁰⁰=0 exactly (stronger than before) |
| 8 Cascade | coherent E(z) signature | **degenerate** — ΛCDM forges it; de Graaff cuts *against* |
| 9 EFE | evolution + EFE one mechanism | **∇·B claim withdrawn**; EFE∝1/E(z) **revived** as the one card |

Two pieces *held* under direct attack (the anti-screening and the exact linear CMB-safety — the
sound technical core). Most others fell or were qualified. Two specific corrections were forced into
the publishable docs: **Piece 8's coherence is not a unique signature** (ΛCDM's apparent a₀ ≈ E(z)
reproduces every channel power), and **de Graaff's M_dyn/M⋆ ≈ 40 is not support** — the evolving-a₀
boost reaches only ~1.5–3 for compact JADES galaxies, and compact high-z galaxies are *Newtonian*
(g/a₀ ∝ (1+z)^{1/2}), so the boost is suppressed exactly where it was advertised
(`reviews/redteam_the_puzzle.py`, `reviews/redteam_round2.py`).

**The capstone.** The one distinctive claim (evolution) is Milgrom's (2014), and ΛCDM hydro
simulations (Magneticum, Tian et al. 2022) reproduce its observable — apparent a₀ rising ×3 by
z = 2.3 ≈ E(2.3) = 3.46 — with **no** fundamental evolution (`reviews/NOVELTY_AND_DEGENERACY.md`).
So the set of claims that are **original AND distinctive AND confirmed is empty.**

---

## Part IV — The complete parameter space (`reviews/PARAMETER_SPACE_REVIEW.md`)

**Theory axis — two free O(1) parameters, neither derived.** √(8π/3) is real; the coefficient
k (→ Z) is free in ~[0.46, 0.50] (Milgrom 2π, Verlinde 6, framework 5.789, 29/5 = 5.80), and **no
route pins it** (thermodynamics, horizon-entropy, Schwarzschild all fail). The exponent p is a
fitted ~2σ choice. Plus the choice of coupling form (a₀ ∝ θ vs √Λ).

**Observation axis — distinguishable from ΛCDM?**

| observable | discriminates? |
|---|---|
| apparent a₀ amplitude | **NO** — degenerate (Magneticum, NIHAO) |
| RAR intrinsic scatter | yes, but **leans ΛCDM** — scatter grows 0.13→0.19 dex with z; universal a₀ wants ≈0 |
| a₀ universality at fixed z | yes, but **contested** (Rodrigues+18 found non-universal a₀) |
| EFE / host dependence | yes — but the framework's ∇·B version was a category error |
| **z≳4 multi-channel** | the **only open window** — no data |

---

## Part V — The viable region and the EFE forecast

**The viable region is one corner: z≳4, extended (deep-MOND) galaxies.** Researching it
(`reviews/viable_region_research.py`) narrowed it further and recovered one genuine card:

- **Coherence is degenerate.** Every channel power (M_dyn/M⋆∝√E, σ∝E¼, BTFR∝−logE) follows from the
  RAR knee at a₀(z); since ΛCDM's apparent a₀ also ≈ E(z), ΛCDM hands back the *same* powers. The
  "fingerprint" I had advertised is forged by ΛCDM.
- **Scatter** is a clean discriminator but its trend leans ΛCDM (extrapolates to ~0.4–0.5 dex at
  z>4; the framework needs <0.1 dex).
- **High-z amplitude** is distinctive only if ΛCDM apparent-a₀ *saturates* at z>4 — unmapped.
- **The EFE redshift-weakening is the one genuinely distinctive prediction.** The standard MOND EFE,
  η = g_ext/a₀, modulated by a₀(z): η ∝ 1/E(z). For a fixed environment the EFE **weakens** at high
  z, so high-z galaxies in dense environments behave more like *isolated* deep-MOND systems — unique
  vs both ΛCDM (no host effect on the internal RAR) and constant-a₀ MOND (constant EFE).

**The feasibility forecast (`reviews/efe_evolution_forecast.py`), done rigorously.** Solving the
MOND EFE numerically: the distinctive signal (the *change* in the embedded-vs-isolated offset across
z) is only **~0.1 dex**, against a per-galaxy noise of **~0.25–0.41 dex** (M_dyn, M⋆, M_gas,
intrinsic scatter). A 3σ detection of the double-difference {isolated,embedded}×{low-z,high-z} needs
**~600 (optimistic) to ~1600 (realistic) extended, environment-classified, kinematically-resolved
z>4 galaxies** with measured g_ext and gas masses — ~10–30× beyond current JWST samples (tens of
*compact* galaxies, no environment split). The test is two-tiered: **(i)** offset ≠ 0 → MOND vs
ΛCDM (the classic EFE detection, nearer-term); **(ii)** offset *shrinks* with z → framework vs
constant-a₀ MOND (the distinctive, harder bit). **A next-decade flagship campaign, not a this-cycle
test.**

---

## Part VI — Verdict, and what is genuinely valuable

### VI.1 The honest end state
A **coherent, CMB-safe, falsifiable implementation of Milgrom's 2014 evolving-a₀ idea**, with two
free O(1) parameters, no current distinguishing evidence (degenerate with ΛCDM on everything
measurable now), and exactly one distinctive prediction — the EFE's 1/E(z) weakening — that is real
but a decade from testability. It is a clean hypothesis parked at the edge of testability, not a
discovery.

### VI.2 What is genuinely real
- The **exact linear CMB-safety** result (δq⁰⁰ = 0; a₀ absent from linear perturbations even with
  the aether perturbed) — sound, and slightly stronger than the AeST authors' own order-counting.
- The **explicit θ-coupled AeST construction** — a tidy, minimal covariant realization of the
  evolving scale (no new field).
- One **distinctive, falsifiable prediction** (the EFE evolution) — modest, but it survived.

### VI.3 The transferable contribution — the method, not the model
The most reusable output is the **falsification workflow** applied to a numerology-driven TOE:
(i) compute the **false-discovery rate** of the formula search (~20% ⇒ ~0 bits); (ii) restate every
"match" in **units of the measurement's σ** (turning "0.004%" into a 10⁵σ miss); (iii) **jackknife +
inter-method systematic** on small data fits (5σ → 2σ); (iv) check **novelty and ΛCDM degeneracy**
against the literature before claiming a result. A clean template for self-falsification.

### VI.4 The publishable residual
`papers/AeST_evolving_a0_note.md` — *"An explicit AeST realization of an evolving MOND scale, and its
linear CMB-safety."* A modest, honest technical note (Milgrom and Skordis–Złošnik credited), with
the limits stated plainly. Publishable on its own terms as an implementation result.

### VI.5 What would change the verdict
Only one thing: a **forward** confirmation. Specifically, the level-(ii) EFE-evolution measurement on
extended z≳4 galaxies, or a clean determination that ΛCDM apparent-a₀ deviates from E(z) at z>4
while the framework's prediction holds. Until then the honest status is the one this document
records — interesting, coherent, unconfirmed, and largely indistinguishable from ΛCDM.

---

## Appendix — Reproducibility (script index)

| result | script |
|---|---|
| false-discovery rate (~0 bits) | `reviews/false_discovery_rate.py` |
| precision-physics σ-table + eta audit | `reviews/OPUS_PHYSICS_REVIEW.md` |
| eta-invariant rationality check (≠ 4π/3) | `reviews/eta_invariant_reality_check.py` |
| θ=3H coupling, anti-screening, δq⁰⁰=0 | `reviews/theta_3H_coupling.py` |
| linear Boltzmann (r_s, ℓ_A, running=0) | `bridge1_linear_boltzmann.py` |
| 2nd-order CMB scoping | `reviews/nonlinear_cmb_scoping.py` |
| data stress-test (5σ→2σ) | `reviews/stresstest_piece3_evolution.py` |
| full red-team (Pieces 1–9) | `reviews/redteam_the_puzzle.py`, `reviews/redteam_round2.py` |
| novelty + ΛCDM degeneracy | `reviews/NOVELTY_AND_DEGENERACY.md` |
| complete parameter-space map | `reviews/parameter_space_map.py`, `reviews/PARAMETER_SPACE_REVIEW.md` |
| viable-region research | `reviews/viable_region_research.py` |
| EFE-evolution feasibility forecast | `reviews/efe_evolution_forecast.py` |
| the assembled surviving theory | `THE_SURVIVING_THEORY.md` |
| the publishable technical note | `papers/AeST_evolving_a0_note.md` |

*Foundations:* Milgrom 1983, 2014 (arXiv:1412.4344); Skordis & Złošnik 2021 (arXiv:2007.00082);
Tian et al. 2022 (Magneticum, arXiv:2206.04333); McGaugh, Lelli & Schombert 2016 (SPARC);
Rodrigues et al. 2018; MUSE-DARK III 2026. CODATA-2022 / PDG / Planck-2018 for the σ-table.

# The Surviving Theory — the puzzle assembled, piece by piece

**Date:** 2026-06-02 · *every piece is backed by a runnable check in this repo; the dead
pieces are named explicitly so the boundary is part of the structure.*

This is the whole edifice that survives review, in logical order. Each piece answers the
question the previous one raises. Nothing here depends on the α/mass-ratio numerology or the
Z² = 32π/3 topology — those are **dead** (`reviews/OPUS_PHYSICS_REVIEW.md`), and the puzzle is
built without them. The honest status of every piece is tagged:
**[KNOWN]** established physics, not ours · **[POSIT]** a chosen O(1) input · **[DERIVED]**
follows from the premise · **[DATA]** confronted with measurement · **[OPEN]** a real
calculation not yet done (and not faked).

---

## The spine on one page

```
  (foundation: only the MOND-scaling survives; numerology + Z²-topology are dead)
        │
  1. PREMISE      a0 = cH/Z          MOND scale = cosmic-acceleration scale     [KNOWN+POSIT]
        │  ── if a0 tracks the density literally, then it must evolve ──
  2. EVOLUTION    a0(z) = a0(0)E(z)  coefficient-free (Z cancels)               [DERIVED]
        │  ── confront the only distinctive claim with data ──
  3. DATA         p = 0.80 ± 0.17    constant & matter-only both ~5σ out        [DATA]
        │  ── does it have a covariant home? ──
  4. ACTION       AeST + a0 = cθ/3Z  θ = ∇·A; evolution becomes a field eqn     [KNOWN+POSIT]
        │  ── does the action deliver a0=cH/Z where the galaxies are? ──
  5. LOCAL        galaxy sees θ≈3H(z) anti-screening, to 1e-6                   [DERIVED]
        │  ── which density does a0 track — Λ or ρ_total? ──
  6. FORK         data pick θ=3H      √ρ_total over √Λ (de Sitter) & √ρ_matter  [DATA]
        │  ── does running a0 break the microwave background? ──
  7. CMB          a0 absent at linear order; 2nd-order ~0.01–0.1%              [DERIVED+OPEN]
        │  ── what does the premise force for formed galaxies? ──
  8. CASCADE      one E(z) drives all: M_dyn/M*∝√E, v∝E¼, BTFR∝−logE, …        [DERIVED]
        │  ── the same θ that evolves a0 also sets it locally → ──
  9. EFE          environmental EFE + cosmic evolution = one mechanism          [DERIVED+OPEN]
        │  ── what is left to close? ──
 10. FRONTIER     the open checks collapse to TWO                               [OPEN]
```

---

## 1. The premise — a₀ = cH/Z  **[KNOWN coincidence + POSIT]**

The MOND acceleration scale equals the cosmic acceleration scale:
$$a_0=\tfrac{c}{2}\sqrt{G\rho_c}=\frac{cH}{Z},\qquad Z=2\sqrt{8\pi/3}=5.789.$$
√(8π/3) is exact Friedmann physics; the factor of 2 (hence Z) is a chosen O(1) number.
**Status:** that a₀ ~ cH₀ is a 40-year-old coincidence (Milgrom: a₀≈cH₀/2π; Verlinde). The
*framing* a₀=cH/Z is ours; the coincidence is not. The factor of 2 is **not derived** — Bridge 2
showed thermodynamics fixes the *evolution*, not the coefficient.
*Check:* `schwarzschild_friedmann_core.py`, `bridge2_coefficient_thermodynamics.py`.

**→ raises:** if a₀ is literally set by the density ρ_c, and ρ_c falls as the universe expands,
a₀ cannot be constant. What does it do?

## 2. The evolution — a₀(z) = a₀(0)·E(z)  **[DERIVED, coefficient-free]**

With ρ_c(z) ∝ E(z)², the premise forces
$$a_0(z)=a_0(0)\,E(z),\qquad E(z)=\sqrt{\Omega_m(1+z)^3+\Omega_\Lambda}.$$
**Z cancels in the ratio** a₀(z)/a₀(0) — so this prediction carries *no* free coefficient and
cannot be tuned. **This is the single distinctive, falsifiable claim of the whole framework.**
Everything downstream is its consequence.

**→ raises:** is it true? It is already testable.

## 3. The data — p = 0.80 ± 0.17  **[DATA: favored, thin]**

Fitting a₀(z)=a₀(0)E(z)^p to the local SPARC scale, Vărăşteanu (z≈0.05) and MUSE-DARK (z≈0.9):
**p = 0.80 ± 0.17.** Constant a₀ (p=0) is rejected at ~5σ; matter-only (1+z)^{3/2} (p=1.5) at
~5σ. The data, for the first time, lean toward evolution.
**Status:** real but **thin** — three heterogeneous points, the z≈0.9 datum doing the work; an
evolving RAR is *also* expected in ΛCDM from halo evolution. A live discriminator, not a verdict.
JWST is decisive. *Check:* `a0_powerlaw_confrontation.py`, `a0_decisive_pipeline.py`.

**→ raises:** can an evolving a₀ live inside a real relativistic theory, or is it just a fit?

## 4. The action — AeST with a₀ → cθ/(3Z)  **[KNOWN host + POSIT coupling]**

Take AeST (Skordis–Złošnik 2021 — the relativistic MOND that fits the CMB and keeps c_GW=c).
Its MOND scale a₀ is the coefficient of the spatial 𝒴^{3/2} term. The aether already carries a
local scalar, its expansion θ=∇·A. **Promote** a₀ → a₀(θ)=cθ/(3Z). One covariant change, no new
field; on FRW θ=3H, so a₀(z)=cH(z)/Z becomes a **field-equation output**, not a fitted relation.
**Status:** the host theory is established; the θ-coupling and Z are ours and chosen.
*Check:* `reviews/GEOMETRIC_ACTION_theta_coupling.md`, `bridge1_aest_equations.md`.

**→ raises:** the action gives a₀=cH/Z on the cosmic background — but galaxies are *bound*. Do
they actually see 3H, or does local collapse screen θ to zero (which would kill a₀ locally)?

## 5. Local realization — the galaxy sees 3H(z)  **[DERIVED, anti-screening]**

To first order in the weak field, θ = 3H − 3HΨ − 3Φ̇ + ∇·B. In a quasi-static galaxy all three
corrections are negligible (Ψ~10⁻⁶, Φ̇≈0, ∇·B≈0), so the galaxy at epoch z sees **θ ≈ 3H(z) to
~1 part in 10⁶**. The cosmic expansion threads through the bound system; it is **not screened**.
So the coupling delivers a₀=cH(z)/Z exactly where the rotation curves are measured.
*Check:* `reviews/theta_3H_coupling.py` [A,B] (sympy).

**→ raises:** a₀ could track √Λ (de Sitter, constant) or √ρ_total (=H, evolving). Which?

## 6. The fork — the data select √ρ_total  **[DATA: discriminant]**

| a₀ couples to | p | distance from fit |
|---|:--:|:--:|
| √Λ (de Sitter / Verlinde) — constant | 0 | 4.7σ rejected |
| **θ = 3H ∝ √ρ_total (this coupling)** | 1 | **1.2σ favored** |
| √ρ_matter | 1.5 | 4.1σ rejected |

The evolution **selects the aether-expansion coupling** and rejects the purely-geometric
de-Sitter origin that emergent-gravity stories most naturally give. (Distances here are the
linearized |p−p_fit|/σ_p; the rigorous profile-χ² of Piece 3 gives the same verdict — p=0 and
p=1.5 both ~5σ out, p=1 at ~1σ.) *Check:* `reviews/theta_3H_coupling.py` [D],
`relativistic_frontier.py`.

**→ raises:** running a₀ to ~20,000× its value at recombination — does that wreck the CMB?

## 7. CMB consistency — linear-safe, second-order scoped  **[DERIVED + OPEN]**

On FRW the spatial 𝒴̄=0 (q⁰⁰=−1+1=0), so the a₀-term is O(δφ³): **absent from every linear
equation.** Peaks do not move (r_s, ℓ_A unchanged), the transfer function is a₀-invariant — and
the θ-dressing doesn't lower the order (θ̄=3H̄≠0). The first a₀-dependent effect is **second
order**, where a₀ is ~2×10⁴ larger; the estimated C_ℓ correction is **~0.01–0.1%** (likely below
Planck's ~0.3–1%, but soft because of the 𝒴^{3/2} non-analyticity). *Check:*
`bridge1_linear_boltzmann.py` (verified vs BBKS/Planck), `reviews/nonlinear_cmb_scoping.py`.

**→ raises:** granting the premise, what is *forced* for the galaxies JWST will measure?

## 8. The consequence cascade — one E(z) drives everything  **[DERIVED]**

Because v⁴=GM·a₀(z) and the deep-MOND relations scale with a₀(z)=a₀(0)E(z):
M_dyn/M⋆ ∝ √E, v & σ ∝ E¼, BTFR/Faber–Jackson zero-point ∝ −log E, sizes ∝ 1/√E, critical
surface density ∝ E. **Every channel keys off the *same* E(z)** — a coherence no ΛCDM+systematics
combination forges. That simultaneous coherence across channels is the experimental fingerprint.
*Check:* `jwst_full_predictions.py`, `JWST_FORECAST.md`.

**→ raises:** the same θ that evolves a₀ also sets it locally — is there a second phenomenology?

## 9. The EFE bonus — evolution and environment, one mechanism  **[DERIVED + OPEN]**

a₀ is set by the local aether expansion θ. Its cosmic part (3H) gives the **redshift evolution**;
its inhomogeneous part (∇·B) is exactly where the **External Field Effect** enters. So a₀ depends
on both epoch *and* environment through one quantity — a structural prediction, not two knobs.
The precise EFE map needs the aether back-reaction solved. *Check:* `reviews/theta_3H_coupling.py`
[B], `mond_first_principles.py` (EFE).

**→ raises:** what is actually left to close the theory?

## 10. The frontier — the open checks collapse to two  **[OPEN]**

At linear order the θ-coupled theory *is* constant-a₀ AeST, inheriting its ghost-freedom, c_GW=c,
and CMB fit. So the second-order CMB, the dressed-term stability, and the non-analyticity are
**one** problem — the 𝒴^{3/2} term at second order around 𝒴=0. The only separate piece is the
**EFE/∇·B** back-reaction. **The frontier is: one nonlinear cosmological calculation, plus the
EFE.** *Check:* `reviews/GEOMETRIC_ACTION_theta_coupling.md`, `reviews/nonlinear_cmb_scoping.py`.

---

## What is NOT in the puzzle (the boundary is part of the structure)

- **α⁻¹ = 4Z²+3 and all the constants** (mass ratios, sin²θ_W=3/13, Ω_Λ=13/19, Koide, CKM/PMNS):
  ~0 bits of evidence — a 34,073-formula search hits an arbitrary O(100) target this well ~20% of
  the time; in real units they miss by 10⁵–10⁶σ. **Dead.** (`reviews/false_discovery_rate.py`.)
- **Z² = 32π/3 from orbifold topology / the η-invariant**: a category/term error (a Euclidean
  ball volume relabeled as a Dirac η-invariant), with an openly-abandoned generation count. **Dead
  as a derivation.** (`reviews/OPUS_PHYSICS_REVIEW.md` §4.)
- **The Standard Model, masses, reionization, the UV luminosity function**: this framework is
  **silent** — they are gas/stellar/linear physics, a₀-independent.

## The puzzle in one sentence

> The acceleration scale that governs galaxies is the cosmic density's own acceleration —
> so it must evolve as E(z); that evolution is a field-equation output of an aether-expansion
> coupling, it survives the linear CMB, it is the coupling the current data prefer, and JWST
> kinematics will confirm or kill it within a few years.

Everything above is either **[KNOWN]** (inherited), **[POSIT]** (Z, chosen), **[DERIVED]**
(forced by the premise), **[DATA]** (favored, thin), or **[OPEN]** (one nonlinear calc + the EFE).
There is no numerology load-bearing anywhere in the chain.

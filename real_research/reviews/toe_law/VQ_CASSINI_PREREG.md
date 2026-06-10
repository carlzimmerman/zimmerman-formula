> ⚠️ **SUPERSEDED-BEFORE-RUN (process note, same day, 2026-06-10).** The gate computation pre-registered below was
> **already done 2026-06-05** (`CASSINI_QUADRUPOLE_CONSTRAINT.md` + `reviews/cassini_quadrupole_framework.py`,
> 10-facet audit 9/10): Q₂ ≈ 3.2×10⁻²⁶ s⁻² at the framework's own a₀ — the ×0.69 footing suppression pre-registered
> here is REAL but operates on a ~10× excess → **the banked answer is this prereg's Outcome B** (the exposure stands
> on the framework's own terms; μ-screening excluded by scale; β₀ RAR-pinned). **Process miss owned:** I wrote this
> prereg off the falsification matrix's stale "*uncomputed*" line without opening the doc that line itself cites.
> The matrix line is now fixed. This file stands as the ledger record (the discipline logs process misses too), and
> its live content **pivots to the one open cell**: the Galileon k-mouflage host — see `TOE_TRILEMMA.md`. The solver
> design below (self-contained Green's-function Q₂, validation anchor) remains available as an independent THIRD
> reproduction if Fable wants one; it is not claimed as new.

# The law rung — V(Q)/K(Q) construction gated by the Cassini quadrupole: PRE-REGISTRATION

*C. Zimmerman, 2026-06-10. Committed BEFORE the solver runs. This is the honest "push for a TOE": not re-running the
derivation doors (banked: no framework forces Z=5.789; DSSYK sign contested-terminal; Z presently a data-selected
convention), but the LAW rung between phenomenology and derivation — Balmer → **Bohr** → QM. The law candidate is the
AeST free function K(Q) carrying the framework's a₀–Λ lock (ONE function, TWO limits — deep-MOND a₀ = c²√(Λ/32π) and
GR+Λ — ZERO new parameters). Its named, **uncomputed** kill-gate is the Solar-System quadrupole: the falsification
matrix records that the framework "inherits a 3–15σ Cassini exclusion (Desmond+2024) unless K(Q) screening saves it —
*uncomputed*." This pre-registration locks that computation. Inline, no swarms. C1/C2 only (C3 fence).*

## The question (one sentence)
**Does the RAR-preferred interpolation function pass the Cassini quadrupole bound at the framework's OWN footing
(a₀ = 9.36×10⁻¹¹), where it fails at the canonical MOND footing (1.2×10⁻¹⁰)?**

## Why the footing might matter (the pre-registered physical expectation — to be tested, not assumed)
The EFE quadrupole scales as Q₂ ∝ a₀/r_M · q₂(η) with r_M = √(GM_☉/a₀) ⇒ **Q₂ ∝ a₀^{3/2}** at fixed q₂; the framework's
22%-lower a₀ gives a ×0.78^{3/2} ≈ ×0.69 suppression. Additionally η = g_e/a₀ rises 1.79 → 2.30 (g_e ≈ 2.2×10⁻¹⁰ measured,
footing-independent), pushing the Sun deeper into the EFE-quasi-Newtonian regime, which further suppresses q₂(η). Both
effects run the SAME direction. Per the project's #1 rule this cuts BOTH ways: if the suppression rescues the soft
function, the "3–15σ inherited exclusion" was partly a canonical-footing artifact (a deficit claim corrected on the
framework's own terms); if it does NOT rescue it, the exposure stands ON the framework's own terms and is recorded as such.

## Method (self-contained — no borrowed table values)
QUMOND phantom-density route, solved exactly to quadrupole order by Green's function (no 2D PDE):
1. ∇φ_N = (GM_☉/r²) r̂ − g_e ẑ (exact vector sum); y = |∇φ_N|/a₀; χ(y) = ν(y) − 1.
2. Phantom source S = ∇·[χ ∇φ_N] on an (r, cosθ) grid (finite-difference divergence of the analytic flux).
3. Legendre-project: S₂(r) = (5/2)∫ S P₂(u) du; inner quadrupole by the exact ℓ=2 Green's function:
   **Q₂ = −(3/5) ∫₀^∞ S₂(r)/r dr** (normalization fixed against the anchor below; Hees convention
   Φ_quad = (Q₂/3) r² P₂(cosθ)).
4. Compare to **Cassini: Q₂ = (3 ± 3)×10⁻²⁷ s⁻²** (Hees et al. 2014 Saturn ranging).

**Validation anchor (gate — the run does not count until this passes):** the solver must reproduce the published
Blanchet–Novak/Hees range for the standard functions at canonical a₀ — **ν_simple → Q₂ ≈ 4.1×10⁻²⁷ s⁻², the
exponentially-screened family ≈ 2.1–2.5×10⁻²⁷** — within ~30%. (Same role as NFW C(x=2)→4 in the lensing battery.)

## Function family (Desmond's parametrization — δ=1 IS the McGaugh RAR function)
ν_δ(y) = [1 − exp(−y^{δ/2})]^{−1/δ}, run at δ ∈ {0.7 (RAR-preferred soft end), 1.0 (McGaugh), 1.5, 2.0 (sharp)},
plus ν_simple as the anchor. Footings: a₀ ∈ {1.2×10⁻¹⁰ canonical, 9.36×10⁻¹¹ framework}; g_e = 2.2×10⁻¹⁰ ± 20%
(sensitivity row — g_e is measured, NOT rescaled with the footing).

## Pre-registered outcomes
- **(A) RESCUED:** δ=1 (and/or the RAR-preferred δ≈0.7) lands |Q₂| within the Cassini 2σ band at the framework footing
  while exceeding it at canonical → the inherited 3–15σ is **partly a footing artifact**; matrix row softens (with the
  Desmond RAR-refit caveat below); **V(Q) target = the soft family**, and the explicit K(Q) ↔ ν_δ mapping is written next.
- **(B) STANDS:** δ=1 still exceeds Cassini at the framework footing → the exposure holds **on the framework's own
  terms**; V(Q) must be sharp-screened (δ ≳ 2) and the RAR-fit cost of that sharpness becomes the quantified next
  computation (needs the SPARC re-fit at a₀ = 9.36×10⁻¹¹ — staged, not run here).
- **(C) MARGINAL** (within ~1–2σ): BepiColombo / the 2026 Cassini-update decides → data-watch entry (registry #7).

## Caveats locked now (so they cannot be retro-fitted)
1. This computes the **quadrupole of the QUMOND point-mass-in-external-field problem** — the standard observable Hees
   bound; it does NOT re-fit the RAR. Desmond's tension couples the two (the RAR prefers soft δ *at canonical a₀*); a
   full resolution needs the joint refit at the framework footing. Outcome A therefore reads "the named exclusion
   softens," NOT "Cassini cleared."
2. AeST inherits this only insofar as its quasistatic limit reduces to QUMOND-like behavior with K(Q) ↔ ν — Door-3
   banked (leaning-pinned); the mapping is re-stated explicitly in the K(Q) write-up, not assumed silently.
3. **The law candidate's liability ledger rides along:** a type-blind K(Q) carries the lensing early/late split
   (hardened 2026-06-10: 8.8σ → 5.0σ surviving, gas escape disfavoured) as standing exposure. A V(Q) "law" that passes
   Cassini still owes an answer there. No TOE talk without that line.
4. The TOE boundary stands: even Outcome A produces a **law candidate**, not a derivation. The derivation rung stays
   blocked at the contested DSSYK dictionary until the field settles it (watch entry #5).

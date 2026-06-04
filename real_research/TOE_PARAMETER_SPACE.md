# Reducing the TOE Parameter Space — Given the MOND Scaling Mechanism Is Correct

**C. Zimmerman, June 2026.** *The question: assume a₀ = c²√(Λ/32π) = cH(z)/Z is the true mechanism. What does that
single assumption force about the Theory of Everything — which candidates survive, which are demoted, which die?
Every verdict is anchored to an already-verified door (so this is a filter applied to established results, not new
speculation).*

---

## What the assumption actually commits you to

The scaling mechanism is not one statement; it is **three physical commitments**, and each one is a knife that cuts
the TOE landscape:

1. **a₀ is emergent, not fundamental.** It is *set by* Λ (the vacuum energy / horizon), not an independent constant of
   nature. The dark-sector acceleration scale is **cosmological and gravitational** — it lives at the horizon, not in
   a particle's mass.
2. **The galaxy-scale "dark matter" is the anharmonic (MOND) term**, not a new massive particle. The flat-rotation
   phenomenology is a *nonlinear modification of the gravitational response* below a₀ (see `ANHARMONIC_AND_32PI.md`),
   tracking the baryons — not the gravity of an extra species.
3. **The coefficient 32π is GR-traceable** (= Einstein coupling 8π × horizon factor 4). The UV gravity sector is
   **standard General Relativity**; the modification is an **IR / emergent** effect, not a wholesale UV replacement of
   gravity.

These three are the filter. Apply them.

---

## The filter applied to the TOE landscape

| TOE candidate | Verdict under the assumption | Anchored to (verified) | Reason |
|---|---|---|---|
| **Particle DM as the galaxy dark sector** (WIMP / SUSY-neutralino / sterile-ν / primordial-BH-dominant) | 🔴 **DEMOTED / displaced** | `LCDM_FITS_VS_MOND_PREDICTS.md` (332 halo params vs 1 a₀; RAR scatter 0.069 dex); `DM_VS_MOND_CONSISTENCY.md` | Commitment 2: the phenomenology is IR-gravitational and baryon-tracking. A relic species is not *forbidden* (it may still seed the CMB / clusters) but it can no longer be *the* explanation of rotation curves — its prime motivation evaporates. |
| **Emergent / entropic gravity** (Verlinde, Jacobson, Padmanabhan, Bueno et al.) | 🟢 **FAVORED — the natural home** | Door 7 `project_entanglement_equilibrium_a0.py` (forces the *scale* a₀~cH from the dS volume/area crossover) | Commitments 1+3: gravity is thermodynamic/entanglement, a₀ emerges from de Sitter entropy, UV gravity stays GR. This is the *only* family where the mechanism is the natural output, not an insertion. |
| **Covariant-MOND field theory (AeST)** | 🟢 **FAVORED — the relativistic skin** | Door 3 (a₀ in 𝒦's 𝒴^{3/2} term, verified incl. the factor-3; CMB-safe at linear order) | Commitment 3: a GR-based covariant theory hosting a₀, with c_GW = c (GW170817-safe). It is an EFT, so it is the *completion*, not the TOE — but it is the surviving covariant home. |
| **String / M-theory** | 🟡 **CONSTRAINED to a corner** | Door 8 (Blanchet a₀↔Λ Lagrangian precedent); `THE_COSMIC_SEESAW.md` (a₀ = c·E_Λ²/2ℏE_P) | Not killed — but the generic landscape DM candidate is displaced (Commitment 2), so a surviving string vacuum must realize a₀²∝Λ via a **light modulus/dilaton coupling locked to the vacuum energy**. That is a sharp selection on which vacuum, not a free landscape scan. |
| **Causal sets (Sorkin)** | 🟡 **PARTIAL — scale only** | Door 2 (gives Λ~H² within ~2×, but ℓ_Planck cancels → no coefficient; Λ's fluctuating sign → a₀ imaginary half the time) | Consistent with Commitment 1 (Λ~H² is its pre-1998 success) but cannot deliver the coefficient or a stable sign. Survives as a *scale* mechanism, not a complete one. |
| **Asymptotic safety / LQG** | 🔴 **DEAD for a₀** | Door 7 (checked: neither produces an IR acceleration scale tied to Λ) | No natural a₀~√Λ output. They may be fine UV-gravity stories, but they do not realize the mechanism. |
| **DSSYK / holographic *forcing* of the coefficient** | 🔴 **DEAD for forcing Z** | Door 6 `project_dssyk_force_Z_verdict.py` (computed to fail: Z→∞) | The one route that could have *uniquely forced* 32π forces the wrong (divergent) answer. The mechanism can be *hosted* holographically but its coefficient is not *forced* there. |

---

## The narrowed space — what the assumption leaves standing

Collapsing the table: **if the MOND scaling mechanism is correct, the TOE is constrained to the family**

> **emergent / de Sitter–thermodynamic gravity** (gravity is GR in the UV, with an IR entropic modification that sets
> a₀ ~ √Λ), wearing an **AeST-class covariant skin** (c_GW = c, CMB-safe), and **UV-completed in a way that welds a₀
> to Λ** — the welding being exactly the two unworked constructions already identified:

1. **AeST cross-coupling** (Door 3): build the non-separable ℱ(𝒴,𝒬) whose small-𝒴 coefficient is *forced* to √Λ
   with the 1/√(32π) factor — collapsing a₀ and Λ from two inputs to one.
2. **Entanglement-equilibrium volume term** (Door 7): insert a de Sitter volume-law term into Jacobson's equilibrium
   and extract a₀ — the cleaner thermodynamic route (no non-equilibrium obstacle).

Everything else is either demoted (particle DM as the galaxy explanation), confined to a corner (string vacua with a
Λ-locked light scalar), or dead for this purpose (asymptotic safety, LQG, DSSYK-forcing).

## The scale of the reduction (why this is worth stating)

The dark-sector parameter space *without* the assumption is large: ~8 live DM candidates × ~4 halo-profile families ×
multiple feedback re-tunings, plus an independent a₀ if you also want MOND (`DM_VS_MOND_CONSISTENCY.md`,
`DARK_MATTER_HISTORY.md`). The assumption **a₀ = c²√(Λ/32π)** collapses all of that, on galaxy scales, to **one
number — √Λ** — and routes the remaining TOE freedom into a single question: *which UV-complete, GR-based, emergent
theory welds a₀ to Λ with the GR-traceable coefficient?* That is an enormous reduction: from a zoo of species and
profiles to one scale and one well-posed construction.

## The honest residue — what the assumption does **not** fix

Two debts survive untouched, and both are owed by *every* TOE, not just this one:

- **The value of Λ.** a₀ ∝ √Λ trades the puzzle "why is a₀ ≈ 10⁻¹⁰ m/s²?" for "why is Λ what it is?" — i.e. the
  cosmological-constant problem, E_Λ/E_P ≈ 1.8×10⁻³¹ (`THE_COSMIC_SEESAW.md`). The mechanism *relocates* the mystery to
  a famous open problem; it does not solve it.
- **The uniqueness of 32π.** GR-traceable (8π, 3) but route-forced, not uniquely forced — and the DSSYK forcing route
  is dead (Door 6). The assumption tells you the coefficient is *gravitational*, not *which* O(1) is mandatory.

So the assumption is genuinely powerful — it reduces the dark-sector landscape to one scale and points the TOE at one
family with two buildable seams — **but it is not a TOE by itself**: it presupposes Λ's value and does not uniquely
fix its own coefficient. That is the honest shape of the reduction: a large, real narrowing that ends at the two
deepest debts, not past them.

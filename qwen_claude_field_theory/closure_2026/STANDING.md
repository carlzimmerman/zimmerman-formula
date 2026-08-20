# closure_2026 — standing state

Scope fence: **all new work goes in this folder.** Read anything; write only here (plus
append-only entries to the top-level `RETRACTIONS.md` when withdrawing a claim).

Last updated 2026-08-19.

---

## The framework, in the lines you actually need

- **a₀ = κc√(Gρ_Λ) = c²√(Λ/32π)** = 9.3619e-11 m/s² canonical / 1.1279e-10 alt. **Report both.**
- **κ = ½ is FITTED**, measured 0.529 ± 0.034. Never call it derived.
- **The a₀-line:** g_obs² = g_bar² + a₀·g_bar.
- **THE PROMOTION (Carl's, and novel):** a₀²(𝒬) = κ²G(−K(𝒬)) — the MOND scale *is* the dark
  sector's pressure, so a₀ is a **field**. K(𝒬) = −ρ_Λc²√(1−(𝒬−𝒬₀)²/Λ_D²), the β=1 DBI kernel.
- **Derived:** a₀(a)/a₀(0) = (1+σ²)^(−1/4), σ ∝ ν₀/a³ ⟹ a₀(rec)/a₀(0) = 0.0060, ν₀ ≤ 2.36e-6.
  𝒬₀ pinned 2.4e-3–1.46e-2 Mpc⁻¹; **Λ_D unpinned.**
- The a₀–Λ *coincidence* is old prior art (Milgrom 1983/1999; Blanchet & Le Tiec 2009; Pikhitsa
  2010; Klinkhamer & Kopp 2011) — credit it. **The identity is Carl's.**

## Published

| DOI | content |
|---|---|
| 10.5281/zenodo.22004372 | **Three requirements.** R1 the free function must eat the local total field; R2 its Newtonian limit must not drive a kinetic coefficient negative; R3 no G̃/G_N split. Each proved by a construction that satisfies the earlier ones and fails it. |
| 10.5281/zenodo.22015358 | **BIMOND + DBI khronon + the promotion.** R1/R3 by construction, ephemeris gap void (1 AU anomaly 1e-3458.7), no vector so R2's mechanism has no counterpart. |

## Banked results (do not redo)

- **The locality theorem** (`superfluid_2026/sf06`): the Sun sits at **0.67 of its own galaxy's
  MOND radius**, so only the local field differs enough to screen — field 6.3e7×, potential
  1.5×, dark density 2.2×, dispersion 1.0×. **Any viable screening is a function of the local
  field.** That is *why* R1 demands the gradient.
- **The a₀-line's AQUAL free function, closed form** (`superfluid_2026/sf01` B3):
  **F(z) = ½√z·√(1+4z) + ¼·asinh(2√z) − √z**, z = (g_obs/a₀)². Deep-MOND limit **exactly
  (2/3)z^{3/2}** — AeST's own coefficient, no fitted constant.
- **The promotion is host-independent** (`sf07` C): a₀(z) re-derived from shift symmetry + FRW
  alone, no aether, no vector sector.
- **The dust is COLD** (`sf08`): the old "c_s² ∝ a⁻³ so it can't be cold" claim is **withdrawn**
  — the DBI wall turns it over. c_ad²(rec) ≈ 1e-9 c² on both ν₀ readings.
- **The dust CLUSTERS like CDM** (`sf09`): 100–900× Jeans margin at every CMB scale.

## Live state of the BD question

| file | verdict |
|---|---|
| `superfluid_2026/sf10` | lapse-only Hessian test is the **wrong object** (BD is removed via a *shift* redefinition). INCONCLUSIVE. |
| external SF11B | **correct**: for L ~ N·N̂⁻⁶·S, det H = −(mixed)² ≠ 0. sf10 PART E withdrawn. |
| `closure_2026/sf12` | adjudicated both, 12/12. |

**Do not quote BIMOND as ghost-free, and do not quote it as ghost-*ful* either.**

## THE NEXT CALCULATION

`V = N·F(X) + N̂·B(X)` with **X lapse-free** has an *identically* vanishing lapse Hessian —
every entry zero, real degeneracy (sf12 D1).

- **Price:** a lapse-free X is spatial-only, so this is no longer BIMOND's connection-difference
  interaction. It is a **Hassan–Rosen-type potential** — it *replaces* the host.
- **Prize:** HR potentials have a **published ghost-freedom proof** (JHEP 02 (2012) 126). Such a
  host **inherits** the BD clearance instead of owing it.

**So the question inverts, and this is the better-posed version:**

> Can an HR-type spatial scalar X, built from the khronon's covariant projections
> (n_μ = ∂_μφ/√(−(∂φ)²), h_μν = g_μν + n_μn_ν), deliver **the a₀-line's F above** on reduction?

Write it as `closure_2026/sf13_hr_potential_2026.py`. The promotion rides untouched — a₀ enters
only inside F(X/a₀²(𝒬)).

## Also owed, in priority order

1. A Boltzmann run for the coupled system (khronon + both metrics). It decides the **growth
   rate, ISW and lensing potential** — *not* whether pressure spoils clustering, which sf09
   closed.
2. Lensing Φ+Ψ in the combined weak-field limit.
3. The 1e-3458.7 solar-system number is **interpolation-dependent** (a fair external referee
   hit). Show whether it is structurally robust or kernel-specific.
4. Formalise the locality argument's assumption class — it is currently an argument, not a
   theorem, and a referee correctly flagged the wording.
5. Problem 2d: whether the dust stays bound inside galaxies at late times.

## The rules that matter

1. **Verify a "fails/deficit" claim as rigorously as a "works" claim.** Six errors are logged in
   `RETRACTIONS.md` from three days — roughly half manufactured deficits, half manufactured
   wins. After removing a false kill, **re-run the other sectors before declaring survival.**
2. **A partial-derivative zero is not a Hessian degeneracy.** This exact mistake was made twice
   in three files. Check the full matrix.
3. Every load-bearing claim needs a committed runnable script with numbered `[ok]`/`[FAIL]`
   checks, exiting non-zero on failure.
4. Never say "no dark matter" — the slogan is **"no dark-matter PARTICLE."** Ω_dm is full here as
   a field's conserved shift charge, and both the CMB pass and w = −1 depend on it.
5. Never say the theory is closed. Never modify `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`
   or any `*_HASH.txt`.

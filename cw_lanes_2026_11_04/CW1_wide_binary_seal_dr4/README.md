# CW1_wide_binary_seal_dr4: SEALED. The local filter rule FAILS CASSINI once it sees the real 3D field (13x canonical, 18x alt at g* = c√(Gρ)). With the Newtonian field fixed, the frozen DR4 pipeline would read the local rule as Newton (γ_inf 0.98–0.99) and plain QUMOND as 1.15 / 1.21

Criteria `FROZEN_CRITERIA.md` (da6917883b), committed alone before any script. Run `OMP_NUM_THREADS=1 python3 -I -B cw1.py` (41 s, 1.2 GB), then `python3 -I -B cw1_seal.py`. Outputs: `cw1.out` / `cw1.json`, timing `cw1.time`, MUTATE twin `cw1_MUTATE.*`, and `SEALED_PREDICTION.md` with `SEALED_PREDICTION.sha256` (df7801238b…). No download. `prep_2026/gaia_dr4_prep/` was imported read only (bytecode off) and is untouched. κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the data favour the framework.

## Stage 0: KT20 and KT21 carried the CZ1 defect
`kt20.py` puts 1.9e-10 and 2.32e-10 into `nu(np.sqrt(ge*ge + h*h)/a0)`. Both are observed (MOND) fields: 1.9e-10 is BN11's g_e, and 2.32e-10 is the value CZ1 inverts for Cassini. KT21 inherits 1.9e-10. With the Newtonian field, 1.9e-10 becomes 1.273e-10 on canonical and 1.191e-10 on alt.

## What was computed
- **Solver.** An axisymmetric multipole QUMOND solve for a point mass in a uniform Newtonian Galactic field. It includes the anisotropic external-field effect, which KT20's 1D form drops.
- **Forms.**
  - plain QUMOND (PQ);
  - the local rule ξ = |g|²/(|∇|g|| g*) on the true 3D field (LOC3, primary);
  - the same rule in CZ2's 1D quadrature (LOC1, the form CZ2 graded);
  - the fixed widths 0.55 and 0.5 r_M (E55, HALF).
- **Observables.**
  - γ_r curves;
  - KT21's inner-shape Q on the DR3 extract, with each pair's Galactic-centre direction;
  - the γ_inf the frozen DR4 pipeline would return;
  - a g* scan against Cassini, the six planets and DR3.

## Results (primary field; full tables in `SEALED_PREDICTION.md`)
**Curves, μ-averaged γ_r, M = 1.0 M☉, canonical** (s in kAU):

| s | 1 | 3 | 5 | 7 | 10 | 15 | 30 |
|---|---|---|---|---|---|---|---|
| PQ | 1.016 | 1.125 | 1.276 | 1.358 | 1.367 | 1.369 | 1.369 |
| LOC3 | 1.000 | 1.010 | 1.104 | 1.078 | 1.013 | 1.001 | 1.000 |
| LOC1 | 1.000 | 1.007 | 1.029 | 1.017 | 1.001 | 1.000 | 1.000 |
| E55 | 1.001 | 1.027 | 1.100 | 1.196 | 1.310 | 1.366 | 1.369 |

**DR4 and DR3:**

| | N | PQ | LOC3 | LOC1 | E55 | HALF |
|---|---|---|---|---|---|---|
| pipeline γ_inf, canonical | 1.002 | 1.149 | 0.986 | 0.989 | 1.214 | 1.219 |
| pipeline γ_inf, alt | 1.010 | 1.208 | 0.981 | 0.979 | 1.276 | 1.266 |
| DR3 Q z, canonical | +0.08 | −1.79 | −0.57 | −0.10 | −1.13 | −1.28 |
| DR3 Q z, alt | +0.15 | −1.75 | −0.68 | −0.17 | −1.18 | −1.35 |

The pipeline spread across 4 catalogues is 0.007–0.027.

**Cassini at g* = c√(Gρ), q / ceiling:** LOC3 **13.3** canonical, **18.1** alt. LOC1 0.0039 and 0.021, which reproduces CZ2. Planets pass for both forms by 6–7 orders (worst Z 3e-7 to 7e-7).

**g\* scan (0.5–8 a0):**
- LOC3 canonical: only 0.5 a0 passes, so **EXCLUDES VACUUM SCALE**.
- LOC3 alt: nothing passes, so **NO ALLOWED g\***.
- LOC1: 0.5–3.4 a0 on both footings. Cassini sets the top. **CONSISTENT, UNINFORMATIVE.**
- c√(Gρ) from CFG689's native BAO ruler is 1.870e-10 (canonical) and 2.260e-10 (alt), 1.998 a0 on each.

**Separation labels:**
- LOC3 and LOC1 against plain QUMOND: **SEPARABLE** (Δγ_inf 5.7–8.2 σ_tot).
- LOC3 and LOC1 against Newton: **NOT SEPARABLE**.
- E55 and HALF against plain: MARGINAL. Against Newton: SEPARABLE.
- Plain against Newton: SEPARABLE.

## Reading
- **The local rule fails Cassini as a field rule.**
  - The Sun's field and the Galaxy's cancel at a saddle on the Galactic-centre axis, 0.75 r_M (canonical) or 0.85 r_M (alt), about 6,000–6,800 AU out.
  - There |g| → 0, so ξ_loc → 0, and ξ/r falls to 0.01–0.1 near the axis. The Sun's phantom isn't smoothed in that region, which is where the Cassini quadrupole comes from: 60–90 % of it lies in 0.1–1 r_M.
  - CZ2's 1D quadrature √(g_int² + g_e²) never vanishes, so its ξ/r stays at 1.5 or more. That is why LOC passed in CZ2–CZ4.
  - **So the record's only surviving filter form survives only in that approximation.** This reads a frozen CW1 number. It is not a re-grade of LOC on every gate: the MW, dwarfs and SPARC aren't redone in 3D here. Following the CZ1 → CZ2 precedent, LOC needs its own frozen 3D re-grade before anyone cites "LOC fails".
- **With the Newtonian field, the local rule's boost comes and goes.** It is Newtonian below about 3 kAU and above about 15 kAU, with a bump at about 4–10 kAU that moves outward as √M. Far from the binary, the Galactic field makes |g| nearly uniform, so ξ_loc grows as about s³ and smooths the binary's phantom away. This is the mechanism that cost KT27 its dwarfs, here at wide-binary scale.
- **DR4 decides between two families, not between the local rule and Newton.** A plain-QUMOND-level boost beyond 10 kAU (γ_inf about 1.15–1.21) rules out every local rule here. A Newtonian result rules out plain QUMOND and the fixed widths. The frozen scalar fit averages the local rule's bump away.
- **Correcting KT20 changes its numbers but not its message for the fixed widths.**
  - With the Newtonian field and the 3D average, E55's excess over plain at 3, 10 and 30 kAU is 0.22 / 0.84 / 1.00 (canonical, 1 M☉). KT20 had 0.22 / 0.85 / 1.00.
  - Plain's level beyond 10 kAU is 1.37 (3D average) where the 1D form gives 1.49.
  - DR3's Q for plain moves from KT21's z −1.62 to −1.79 (canonical) and −1.54 to −1.75 (alt). Every form stays CONSISTENT with DR3.

## As hard as a fail
- **The LOC3 Cassini fail was tested before this README.**
  - The analytic |∇|g|| matches finite differences to 1e-9.
  - q doesn't move with 2× radial resolution, L 128 with 192 μ nodes, or a grid from 1e-9 to 1e6 r_M: 13.3 and 18.1 every time.
  - The solver reproduces CZ2's 1D Cassini numbers to 4e-4 (K3). The only change from LOC1 to LOC3 is ξ.
- **What LOC3 inherits.**
  - CZ2's gather smoothing, with the width taken at the point evaluated. The scatter form is degenerate for a point source, since ξ → ∞ at the mass.
  - The algebraic |g|, with no curl part.
  - A uniform Galactic field. The Galactic tide shifts the saddle but cannot remove the zero of |g| there.
- **Simplifications in the curves.**
  - A one-body point mass.
  - Local circular scaling, with no orbit integration.
  - The Galactic-centre direction taken from the Sun.
  - The pipeline injection uses the direction-averaged boost, because its population carries no Galactic orientation.
  - The master population is 1e6, not the pipeline's 3e6.
- **K2 FAILED as frozen** (1.07 % vs 1 % at x = 30, alt).
  - The part even in μ matches the linear-response form to 3e-4 at x = 30 and 1e-5 at x ≥ 100.
  - The odd part is second-order lopsidedness falling as 1/x: −8.3e-3, −2.6e-3, −9.3e-4 at x = 30, 100, 300. Below that sits a floor of x² × the self-acceleration (−8e-10 a0, which should be 0 by the CM theorem and is at numerical noise).
  - The diagnostic was written after the first run and is disclosed. The check stays failed.
- **K7 FAILED as frozen** (4.6e-3 vs 3e-3).
  - The difference sits only in the Legendre series evaluated exactly at μ = ±1 for PQ and LOC3, whose saddle lies on that axis. The along-field column carries ±0.003.
  - The averages, every Q and every γ_inf move ≤ 5e-7 (post-result diagnostic, disclosed). The seal states this, as the criteria allow.
- **Development fixes, made before any result was read:**
  - the self-acceleration was first coded without its A₁ term, giving a spurious ±200 dipole at x = 30;
  - linear interpolation in ln x failed K1 at 1.5e-5, so it is now cubic.

## Checks
- K1 1D limit: 4e-11.
- K3 Cassini against CZ2: 4e-4.
- K4 KT20 reproduced: exact.
- K5 KT21 reproduced: exact.
- K6 the pipeline import recovers its own shape: 1.00 → 1.003, 1.1614 → 1.150.
- K2 and K7 as above.

## MUTATE (ν ≡ 1), `cw1_MUTATE.out`
γ_r ≡ 1 for every form, every Q_pred equals Newton's, and Cassini q = 0. Exit 1 by design. Checks are forced to pass under MUTATE, so the bite shows in the numbers.

# J1_potential_selector — is potential depth |Φ|/c² the selector of the law's excesses?

## Verdict: FAILS, on both footings. It is not in the action (Part A), so a₀(Φ) would be a POSTULATED addition (+1 function, +1 constant).

- **Part A (DERIVED, sympy, K6).** In the v3 Khronon and v4 AeST static actions, Φ enters undifferentiated in only two places.
  - The overall √−g = N factor. This is post-Newtonian, of order Φ/c² ≤ 4e-6, so it is too small by about 1e5.
  - The K(Q) / AeST μ² mass term. This is H2's hydrostatic dust, δρ = −μ²Φ/4πG, with a free zero point. H2 already excluded
    its cluster shape.
  - J(Y) and the clock term P^i ∂_i ln N are exactly invariant under ψ → ψ + C, because a constant lapse is a time rescaling.
  - So **neither action contains an a₀(Φ).** Everything in Part B is a postulate.
- **Part B (frozen form a₀_eff = a₀(1 + |Φ|/Φ_*), Φ = the baryons' Newtonian potential, Φ_ref = 0).**
  - **Calibration.** One constant per footing sets the cluster MID band to 1:
    - canonical: φ_* = 1.58e-6 (h 0.672) / 1.41e-6 (h 0.686);
    - alt: 2.13e-6 / 1.89e-6.
  - **O1 cluster outskirts (first out-of-sample check): FAIL.**
    - The data sit at 0.60–0.62 ± 0.05–0.06 of the prediction, so the prediction is about 1.6× too high (Z ≈ −6.6 to −7.8).
    - The profile χ² over bins 3–7 is 36–53, against a pass line of 11.07. The law alone gives 30–47, so the selector does not
      fix the shape.
    - The reason is the one H2 found. A cluster's |Φ| is nearly flat (median 3.7e-6 at 0.1 Mpc, 2.9e-6 at 0.5, 2.3e-6 at 1,
      1.6e-6 at 2 Mpc), so the boost does not switch off where the data return to the law.
  - **(b) Dwarf satellites: FAIL by +0.84 to +0.89 dex.**
    - The selector moves them by only +0.002–0.003 dex. The residual is +0.885–0.889 ± 0.12 (canonical) and +0.840–0.844 ± 0.13
      (alt).
    - **The structural reason has nothing to do with the value of Φ_*.** All 45/46 satellites sit in a shallower host potential
      than the Sun (median |Φ|/c² 4.1e-8, maximum 1.1e-7, against 2.6e-7 at R₀). So any selector that grows with |Φ| boosts the
      Sun's orbit more than any satellite.
    - **[A1] Screening defeats any a₀ multiplier.** In E3's screened B_scr, the boost saturates in a₀, by +0.24 dex at most.
      No ε ≤ 1e8 closes 29/45 (canonical) or 29/46 (alt) systems.
    - The systems that can be closed need ε ≈ 4.4 / 2.5. A monotone selector would then raise the Milky Way's V(R₀) by
      ×1.30 / ×1.17.
  - **(a) SPARC RAR.**
    - canonical: PASS. Δχ² is −156 / −159, but this is not a selector win. The canonical a₀ sits below SPARC's preference
      (median law residual +0.026 dex), and any a₀ raise helps it.
    - alt: FAIL. Δχ² is +8.4 / +19.1 against a line of +9, and the large galaxies carry +13 / +25. SPARC's points reach
      |Φ|/c² up to 3e-6 (90 % below 9.6e-7), which overlaps the cluster depths.
  - **(c) Field and tidal dwarfs: PASS.** The shift is ≤ 0.003 dex for 13 LVD field dwarfs and ≤ 0.014 dex for 6 TDGs.
    - Context, not graded: the TDGs sit at 0.34–0.63 of the isolated law's V.
  - **(d) Solar System: PASS.** ε☉ is 1.13–1.19, Mars is at ≤ 0.21 of its bound, and Q₂ is ≤ 5e-8 of Park.
  - **(e) Wide binaries: PASS.** γ_v − 1 ≈ 1.1e-5.
- **Frozen rule.** Both footings FAIL: (b) fails, and O1 fails. On alt, (a) fails as well.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". Nothing here says
the data favour the framework.

## What was checked in the record (not repeated)

The record already tested these selectors:
- CFG914: density threshold, NO COMMON ORDERING.
- CFG919: kinematic state, CONTRADICTED.
- CFG921 / CFG928: P1–P5 posits. P1 is the internal baryonic potential depth; none of the posits survives all facts.
- H2: the AeST μ²Φ dust, which has the wrong shape.
- opus_48 cluster review: the density-a₀ route, plus the SPARC environment slope +0.052 ± 0.043.

None of them used the total potential including the host as an a₀ multiplier. Hodson & Zhao 2017 (A&A 598, A127) appears only in
`citations/works/`. Its functional form was not used.

## Checks

The script `j1_potential_selector.py` gives **6/6 PASS**, exit 0, in 245 s, single thread, 0.47 GB RSS, with no downloads.
- K1: F1's own reproduction checks (exec'd read-only on F1's KiDS and measurement cache).
- K2: φ_* → ∞ reproduces F1 PRIMARY exactly (0.0 relative).
- K3: SPARC n = 2696, as CFG828.
- K4: E3's residual reproduced to 0.001 dex.
- K5: the potential integrator matches a Hernquist sphere to 5e-7.
- K6: the Part A identities.

`--mutate` keeps only −GM(<r)/r in the cluster potential. K5 then FAILS (0.86), giving 5/6 and exit 1. The outputs are in
`*_MUTATE.*`.

Files:
- `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (d25b7d87bc).
- `AMENDMENT_A1.md`, post-result and reporting only (13a4699b9c).
- `.out`, `_results.json`.

## What this does not show

- Only one functional form and one potential definition were tested: the Newtonian baryonic potential with zero at infinity.
  - The law's own logarithmic potential needs a second constant (a reference radius), so it was not used.
  - The monotone argument in (b) covers every potential that deepens toward the host, and every selector that grows with |Φ|.
- a₀_eff is applied pointwise. An EMOND-type Lagrangian's extra term ∝ dA₀/dΦ was not modelled.
- SPARC potentials are spherical integrals of g_bar. Host masses (MW 6e10, M31 1e11 M☉, Hernquist a = 3 kpc) are external.
- The Solar System and wide-binary lines rescale C6's margins conservatively (∝ ε, ε²). No solver was rerun.

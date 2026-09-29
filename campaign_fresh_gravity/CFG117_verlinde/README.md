# CFG117 — Door 2: Verlinde's emergent gravity against the CFG44 target

- **Criteria:** frozen in `../CFG117_FROZEN_CRITERIA.md` (b09ca1480), before any script or number. The shared gates G1–G5 are in `../closure_map/TEN_DOORS_GATES_2026-09-29.md`. The menu of doors was written knowing the target.
- **Script:** `CFG117_verlinde.py`, about 13 s per run. Outputs: `CFG117_verlinde.out`, `CFG117_verlinde_results.json` and the MUTATE pair.
- **Runs:**
  - The main run exits 1 because H1 failed. That is the declared no-go reading.
  - The MUTATE run exits 0: H1 passes in 16 of 16 cases. The control flips both the headline and the exit code.
- **Inputs:** the target is CFG44's `Bcommon` (`exp_sphere`, `point_mass`, `target_fields`), imported read-only. The two a₀ footings come from FP0 (canonical 9.360325e-11, alt 1.131204e-10 m/s²). H₀ = 67.4 and Ω_Λ = 0.685 are the declared Planck18 values.

## Bottom line

**Verlinde's formula does not reproduce the target's shape.** H1 fails in all 16 cases (4 masses × 2 geometries × 2 choices of H). This is a scoped no-go on G1.

- **Point mass.** The ratio C_V/C_target is exactly (1 + x)/x: 11 at x = 0.1, 2 at x = 1, 1.33 at x = 3 and 1.10 at x = 10. It is within 10% only for x ≥ 10.
- **Exponential spheres.**
  - The ratio is 10 to 16 at x = 0.1 and 1.8 to 8.6 at x = 1.
  - It comes within 10% only from x = 5.1 to 10.4 outward, depending on the case.
- **Why.** The frozen reading's "likely cause", the linear sum, is confirmed.
  - For a point mass Verlinde gives M_D = M x at every radius. That is an r⁻² dark density all the way in, and the linear sum g = g_N + √(a_V g_N).
  - The target's cold mass is M(√(1+x²) − 1). That is an r⁻¹ density inside r_M, and the quadrature sum g = √(g_N² + a₀ g_N).
  - The two share only the deep limit, and they approach it slowly, as 1/x.
  - Inside the baryons, the d(M_B r)/dr in the formula adds a local-density term, 4πr³ρ_B, which makes the interior worse.
- **The normalisation is not the problem.**
  - κ_V = √(8π/3)/6 = 0.482 with H_Λ, and 0.583 with H₀.
  - Both lie within 2σ of both fitted κ windows.
  - With H_Λ, Verlinde's 6 sits where the framework's Z = 5.789 sits: a_V/a₀ = 0.965.
- **Other gates.**
  - G2 and G3 are UNDEFINED: there are no perturbation equations and no action.
  - G4 passes as a count only.
  - G5 fails on the Solar System (Hees et al. 2017).

## The numbers

### R1: C_V / C_target over x = r/r_M, with the target at a₀ = a_V

In every case the largest deviation is at x = 0.1.

| baryons | H | r_M (kpc) | x = 0.1 | 1 | 3 | 10 | 30 | within 10% |
|---|---|---|---|---|---|---|---|---|
| point mass, every M_b | both | — | 11.000 | 2.000 | 1.333 | 1.100 | 1.033 | [10.00, 30] |
| exp. sphere 10⁹, h = 2 | H₀ | 1.130 | 10.054 | 8.632 | 5.469 | 1.148 | 1.033 | [10.42, 30] |
| exp. sphere 10¹⁰, h = 3 | H₀ | 3.574 | 10.336 | 7.407 | 2.546 | 1.081 | 1.033 | [5.46, 30] |
| exp. sphere 10¹¹, h = 4 | H₀ | 11.30 | 11.524 | 4.434 | 1.217 | 1.100 | 1.033 | [10.00, 30] |
| exp. sphere 10¹², h = 5 | H₀ | 35.74 | 15.250 | 1.758 | 1.333 | 1.100 | 1.033 | [10.00, 30] |
| exp. sphere 10⁹ | H_Λ | 1.242 | 10.072 | 8.519 | 5.122 | 1.058 | 1.033 | [9.55, 30] |
| exp. sphere 10¹⁰ | H_Λ | 3.928 | 10.405 | 7.178 | 2.216 | 1.091 | 1.033 | [5.09, 30] |
| exp. sphere 10¹¹ | H_Λ | 12.42 | 11.761 | 4.012 | 1.246 | 1.100 | 1.033 | [10.00, 30] |
| exp. sphere 10¹² | H_Λ | 39.28 | 15.797 | 1.776 | 1.333 | 1.100 | 1.033 | [10.00, 30] |

Masses are M_b in M☉ and h is in kpc.

- **The largest deviation:** |ratio − 1| = 10 for the point mass, and 9.05 to 14.8 for the spheres. The worst case is 10¹² M☉ with H_Λ, ratio 15.80.
- **Undershoot:** only the diffuse 10⁹ sphere dips below 1, to 0.974 at x = 13.8 (0.980 at x = 12.5 with H_Λ). This is the wiggle from the derivative term that Hees et al. describe.
- **Where the failure sits.** The ratio splits into a density ratio (ρ_D/ρ_c) times a field ratio (g_V/g_T). With H₀:
  - Point mass: 10.05 × 1.095 at x = 0.1, 1.414 × 1.414 at x = 1, and 1.005 × 1.095 at x = 10. The density carries the small-x failure; the field, at most √2, carries the tail.
  - Diffuse spheres at x = 0.1: about 3.3 × 3.1. This is the cored-centre limit, where both components are dark-dominated and each factor tends to √10, so the ratio tends to 10.
  - The compact 10¹² sphere at x = 0.1: 8.6 × 1.77. Here the local-density term makes M_D comparable to M_B(<r), where the target's cold mass is a small fraction of it. This is the inner-region difference that Lelli et al. report.
- **Verlinde's own onset criterion (eq. 1.3):** dark phenomena appear where M_B(<r)/4πr² < a₀/8πG, with a₀ = cH = 6a_V.
  - With H₀, the baryons are above that threshold only for x < 1/√3 = 0.577 (point mass, at any H) and x < 0.46 (10¹² sphere). The 10⁹–10¹¹ spheres never reach it in [0.1, 30].
  - The failure therefore sits inside the regime where Verlinde says the dark force operates.
  - The point-mass ratio exceeds 1.1 at every 0.577 < x < 10; it is 2.73 at x = 0.577.

### R2: the normalisation and the κ mapping (a₀ = κ c √(Gρ_Λ))

| H | a_V (m/s²) | a_V/a₀ canonical (ρ_Λ) | a_V/a₀ alt (ρ_total) | κ | BTFR window 0.465 ± 0.076 | distance-free 0.55 ± 0.17 |
|---|---|---|---|---|---|---|
| H_Λ = 55.78 | 9.0328e-11 | 0.9650 | 0.7985 | κ_V = √(8π/3)/6 = 0.4824 | +0.23σ | −0.40σ |
| H₀ = 67.4 | 1.0914e-10 | 1.1660 | 0.9648 | κ_V′ = κ_V/√Ω_Λ = 0.5829 | +1.55σ | +0.19σ |

- **For comparison,** κ = ½ sits at +0.46σ and −0.29σ.
- **The identity.** κ_V/½ = Z/6 = 0.9648, so Verlinde's 6 plays the part of the framework's Z = cH_Λ/a₀ = 5.789. With FP0's ρ_Λ numerically, κ_V = 0.48251; FP0's H_Λ is 55.771 against the declared 55.783.
- **Reading.** Verlinde's normalisation is consistent with the fitted κ on either reading of H: no window excludes it at 2σ. The windows cannot separate κ_V = 0.482 from ½; they are 0.23σ apart in the BTFR window.
- **Footing of the windows:** ρ_Λ, with Planck's H₀ in the denominator (CFG0 F3).
- **Analytic remark.** If the target kept its own footing a₀, C_V/C_target would tend to a_V/a₀ at large x instead of 1. For a point mass it would be (a_V/a₀)(1 + x_V)/x_V.

## Controls

- **C1 (point mass, analytic):** M_D = M x and C_V/C_target = (1 + x)/x, at every node, for all four masses and both H. The maximum relative deviation is 8.9e-16, and the ratio at x = 30 is 1.033333. PASS.
- **C2 (the target):** Bcommon's exponential-sphere ρ_c r³ g_tot equals (a₀/4π) M P(3, r/h) to 3.2e-10 over x in [0.1, 30], for all masses and both H. The residual is Bcommon's PCHIP interpolant of M_b(<r). Against the profile's own interpolated M_b(<r) the agreement is 6.7e-16, an algebraic identity. PASS.
- **C2b (reported):** the Verlinde side uses the same baryons as the target. Its closed-form M_b(<r) matches Bcommon's profile to 3.2e-10, and its ρ_b to 6.7e-16.

## MUTATE

- **What it does:** MUTATE=1 replaces Verlinde's M_D by the target's own cold mass.
  - For the point mass that is exactly M(√(1+x²) − 1), the frozen formula.
  - For the spheres it is Bcommon's w/G (departure D1).
  - C1 and C2 are not touched.
- **Result:** H1 passes in 16 of 16 cases, with the largest |ratio − 1| = 1.8e-10. The run exits 0, against 1 for the main run. The G1 evaluator can pass.
- **The literal formula (reported):** applied to the spheres with M = M_b,tot, it gives |ratio − 1| up to 172 (10⁹ M☉, H₀, x = 0.1), falling to 0.10–0.13 at 10¹². It is the target's cold mass only for a point mass.

## Gates

| gate | mark | one-line reason | source |
|---|---|---|---|
| G1 target | **FAIL** | 0 of 16 cases within 10% over x in [0.1, 30]. Point mass (1 + x)/x; spheres 10 to 16 at x = 0.1. | this lane, H1 |
| G2 CMB and growth | UNDEFINED | No cosmological perturbation equations appear in the abstract (whose evidence claims are for galaxies and clusters) or in the HTML as read, and there is no action to derive them from. | arXiv:1611.02269 abstract and HTML; arXiv:1703.01415 abstract |
| G3 reciprocity and energy | UNDEFINED | The dark mass comes from an elasticity correspondence with no Lagrangian or action, so the reaction on the baryons and the energy supplied are not defined. | arXiv:1611.02269 HTML; Hossenfelder's covariant Lagrangian (arXiv:1703.01415) would define them, but is not tested here |
| G4 constants | PASS (count only) | The 1/6 is derived in the paper: 1/(2(d−1)) at d = 4 (eq. 4.49; the (d−1) comes from the relative normalisation of horizon area and volume, §2.2; a_M = a₀/6, eq. 1.7). It replaces κ rather than adding a constant. Caveats: it is derived in an argument, not an action, so the gate's "in the same action" clause cannot be checked; and eq. 1.2 ties a₀ = cH₀ to the Hubble scale, which is the total density; the tie is to Λ only on the H_Λ reading. | arXiv:1611.02269 HTML |
| G5 well-posedness and Solar System | **FAIL** | No action and no time-dependent covariant field equations, so ghosts, stability and causality are UNDEFINED. The Solar System clause fails: applied where it should hold a priori (spherical symmetry, outside the bulk of matter), the weak-field formula misses the planets' perihelion advances by seven orders of magnitude. | Hees, Famaey & Bertone 2017, arXiv:1702.04358 (PRD 95, 064019), abstract |

- **The Solar System failure follows from the same algebra as C1.** Verlinde's extra acceleration is √(a_V g_N), which grows with g_N. The target's tends to a₀/2.
- **Context (not gates):**
  - Lelli, McGaugh & Schombert 2017 (arXiv:1702.04355) find EG equivalent to MOND for a point mass but not for finite galaxies, which differ in their inner regions. It matches the RAR only with substantially lowered stellar M/L. It also predicts a radius-correlated RAR residual that is not observed.
  - Brouwer et al. 2017 (arXiv:1612.03034) find the parameter-free EG prediction in good agreement with KiDS/GAMA lensing around isolated central galaxies.
  - Hees et al. find marginally acceptable rotation-curve fits, but with low distances, M/L and H₀.

## Untested hypotheses

- **Other formulations:** Verlinde's covariant or later versions (for example Hossenfelder 2017's vector-field Lagrangian, which adds correction terms), and non-spherical systems.
- **The formula's domain of validity.** The frozen file says Verlinde restricts the formula to quasi-static, spherical, isolated systems.
  - This reading confirmed the spherical setting and the surface-density criterion (eq. 1.3). It did not find the words "quasi-static" or "isolated" in the part of the HTML that was read.
  - Hees et al. put the a priori regime at spherical symmetry outside the bulk of matter. The point-mass case of G1 lies exactly there, and restricting to eq. 1.3 does not rescue G1 (R1). So the no-go does not rest on applying the formula outside its stated domain.
- **The target's own hypotheses (CFG44):** spherical, static and Newtonian, in P2's exact form.

## Disclosed departures

- **D1: MUTATE on the spheres.**
  - The frozen text gives the replacement as the target's point-mass cold mass, M(√(1+x²) − 1), and requires "ratio 1 everywhere". The two agree only for a point mass.
  - Taken literally on the exponential spheres, with M = M_b,tot, the formula reaches a ratio of 172.
  - I used each geometry's own target cold mass instead (Bcommon's w/G for the spheres). That is what the frozen expectation and purpose require: the evaluator must be able to pass.
  - The literal formula's numbers are printed in the MUTATE run as a reported row.
- **D2: the controls under MUTATE.** The frozen file does not say whether C1 and C2 run through the mutated M_D. Here they test the Verlinde and target code paths in both runs, and the MUTATE acts only on the M_D given to the G1 evaluator. Run through the mutated M_D, C1 would fail by construction.
- **D3: C2's basis.** C2 is scored against the closed form M P(3, r/h). This is the stricter reading, and it also ties Verlinde's closed-form baryons to the target's. The profile-identity reading (6.7e-16) is printed next to it.
- **D4: H1 over both H choices.** H1 is scored over both H choices (16 cases), reading "both carried" from the declared choices. This weakens nothing: every case fails.
- **D5: reported-only additions,** not in the frozen file:
  - the density × field split;
  - the eq. 1.3 ranges;
  - κ_V computed with FP0's ρ_Λ;
  - the Z/6 identity;
  - the literal-MUTATE row.
  None of them enters a load-bearing check.
- **D6: the grid.**
  - There are 3001 log-uniform nodes on x in [0.1, 30], and both ends are exact nodes.
  - The target's ODE starts at x = 9.98e-4 (Bcommon's default is 1e-3) and ends at 30 r_M (the default is 1e4 r_M; for an initial-value problem the end point cannot change values inside it).
  - The values at x = 1, 3 and 10 are cubic-spline interpolated between nodes.
- **D7: R3's sources.**
  - They were read through a summarising web fetch of arXiv abstract pages and the arXiv/ar5iv HTML renderings. No file was downloaded, and everything is paraphrased.
  - The fetched HTML was truncated before the text of Verlinde's Section 8.2 (cosmological scenarios). G2's mark therefore rests on the abstract, the sections read and the absence of an action; a reader with the full text should confirm that §8.2 has no perturbation equations.
  - An early summary's claims about §7–8 were not confirmed on a verbatim check and are not used.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

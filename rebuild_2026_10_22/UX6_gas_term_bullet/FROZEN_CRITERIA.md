# UX6_gas_term_bullet: FROZEN CRITERIA (committed alone, before any script or map)

Owner's go, 2026-11-02. **Not blind.** Read before this: UX3's README and criteria; X32's README, code and its law-only row (peaks 40, 51 kpc from the gas, delta 0.19, 0.32, dkappa negative at both, M300 1.11e14, 7.3e13 canonical); BU1; the input review in sol61_push; L85; h57. One hand estimate made: for the main gas alone, at 300 kpc, g_gas/a0 about 0.3, so k g_gas/a0 of order 4. So I expect the term to be large here. No map of the term exists. kappa = 1/2 FITTED. Cold sector stays retired; no result reinstates it. No particle. Footings canonical 9.3603e-11, alt 1.1312e-10, never pooled. Not theory closed. Nothing here says the data favour the framework. No downloads.

## Inputs, all on disk
- Baryons: h57's Plummer model, X32's frame (Famaey 2026 Table 1 as transcribed). Gas (M, a, x, y): (2.0e14, 565, 190, 90), (1.5e13, 505, 525, 120), (1.5e13, 90, 670, 170), (-6.8e12, 70, 670, 170). Galaxies: (1.196e13, 470, 0, 0), (4.0e12, 245, 820, 220). BCG1 (0,0), BCG3 (820,220), gas peaks (190,90), (670,170). Separations 210, 158 kpc in this frame; measured 209.4, 194.1 (Clowe Table 2).
- Measured lensing: peaks on the galaxies (Clowe 2006). M_2D(<300 kpc) 3.5e14, 2.3e14 at BCG1, BCG3 (Rihtarsic+2026 via Famaey), a lens reconstruction, not raw. Sigma_crit 1.827e9 as h57. 15 % mass error and the position sigma are X32's, PROVISIONAL.
- k: UX3's fit 13.2868 canonical, 14.2506 alt, read from `ux3_kfit.json`; and pi^2. Both cells graded in both footings. k comes from four relaxed hydrostatic clusters; here it is transferred without change.
- Estimator: QUMOND-type, as X32: the extra field's divergence projected along z, plus directly projected baryons. Law kernel v3, law(g) = g/2 + sqrt(g^2/4 + a0 g). External field regulator a0/1000 as X32.

## Forms. UX3's term has no field equation; each line below is my choice of what it means, and they must be read as separate claims
ghat_b, g_b: Newtonian baryon field. g_gas_vec: Newtonian field of the gas alone.
- **L1 local magnitude:** g = ghat_b law(|g_b|) (1 + k |g_gas_vec|/a0).
- **L2 local vector:** g = ghat_b law(|g_b|) + k (law(|g_b|)/a0) g_gas_vec. The extra pull points along the gas's gravity.
- **L1c local, UX3's C1 switch applied to gas bulk motion:** L1 with the bullet-side gas components weighted by sigma^2/(sigma^2 + V^2), sigma 1500 km/s (14.1 keV, X32), V 2700 km/s (Springel & Farrar), main gas weight 1. Frame choice is mine and arguable.
- **N1 nonlocal, enclosed gas about each galaxy centre, present gas:** law field plus, per subcluster c, a spherical term about its BCG: -rhat_c law(g_c(r_c)) k g_gas,c(r_c)/a0, g_c and g_gas,c from enclosed mass in a sphere about the BCG of that subcluster's own baryons at their present offset positions. Assignment as X32: main = gas comp 0 + galaxies 0; sub = gas comps 1, 2, 3 + galaxies 1. This is UX3's enclosed-mass form taken literally, about the galaxies.
- **N2 nonlocal, pre-merger gas carried with the galaxies:** as N1 with each subcluster's gas restored onto its BCG (offset 0, same M, a). The term keeps the memory of gas no longer there. **It needs a carrier that rides with the galaxies, and none is named.** A pass here is a pass for something that behaves as mass moving with galaxies, not for a term tied to present gas.
- **N3a, N3b nonlocal, smoothed gas:** L1 with g_gas_vec from gas with a -> sqrt(a^2 + L^2), L 300, 1000 kpc, chosen now, no scan. Does not reduce to UX3's form in isolation, so even a pass would need UX3's keys rerun.
L1, L2, L1c (weight 1), N1, N2 reduce to UX3's form for a concentric isolated cluster (K2).

Rows reported, no label: S, the term tied to stars rather than gas (L1 form, g_stars in place of g_gas, same k), to show what the test looks like for a galaxy-tied term; L1, L2, N1, N2 at 0.5 k fit (LF1's bracket pushes k down); L1, L2 with all gas x 0.8, x 1.2; model gas in Clowe's 100 kpc apertures against his M_X; Paraficz M(<250) 2.5e14, 2.0e14; Clowe's kbar ratio.

## Observables and grade, as X32 with added guards
Map: 10 kpc grid, x -500 to 1400, y -400 to 700, same z grid as X32. Maximum of Sigma within 350 kpc of each BCG-gas midpoint.
- **O1 position:** delta = d(peak, gas)/sep, Z = (delta - 1)/0.195. Added here: the maximum must be a true local maximum on the grid, not on the window edge, and closer to the BCG than to the gas, or O1 is failed at that subcluster.
- **O2:** mean kappa in 100 kpc around BCG minus around gas peak, positive at each subcluster. Sign only, Clowe's normalisation not matched; magnitude reported against Clowe's 0.31, 0.18.
- **O3:** M_2D(<300) by surface integral at BCG1, BCG3, Z with 15 %. Sub/main ratio reported against 0.657 +- 0.14, no separate grade.
Cell class: FAIL if any |Z_O1| > 3, O1 guard fails, dkappa <= 0, or |Z_O3| > 3. PASS if all |Z| <= 2 and dkappa > 0. TENSION otherwise.

## Labels, per form
- **DEAD:** in every cell (2 footings x 2 k) position or sign fails at a subcluster (O1 |Z| > 3, guard, or dkappa <= 0).
- **WOUNDED:** at k fit on both footings position and sign don't fail, but mass fails or the class is TENSION.
- **ALIVE:** PASS at k fit on both footings.
- **MIXED:** anything else, stated. Footings differing are stated in the title.
Lane title: which readings survive. If only N2 or N3 survive the title says that the term as tied to present local gas does not, and what the survivor would owe.

## Checks, before reading
K1 k = 0 reproduces X32's law-only JSON, both footings: peaks equal, M300 and dkappa to 1e-6 relative. K2 concentric isolated cluster, regulator off: L1, L2, L1c, N1, N2 equal law x (1 + k g_gas/a0) at test radii, 1e-3 relative. K3 map vs surface M300 at BCG1, L1 k fit canonical, 8 % (X32's tolerance). K4 transcribed input strings found in h57 and the Clowe table; k read from UX3's JSON. K5 RSS under 4 GB. K6 grader controls: positive control, direct Plummer on each BCG, a 150 kpc, mass set to close M300, must PASS; same mass on the gas peaks must FAIL. K7 finite difference h 2 to 1 kpc on L1 k fit canonical: peak same, kappa max within 1 %. A failed K1, K2 or K6 stops the verdict.
**MUTATE twin, must fail:** gas x 2 in the reference (K1), L2's term sign flipped (K2), positive control placed on the gas (K6). Outputs separate, exit 1. Rerun must be byte-identical.

## Expectation, mine, on record
L1: DEAD 75 %. The magnitude vanishes at the gas centre, so I allow a surprise: the ring could shift the peak. L2: DEAD 80 %. N1: DEAD 65 %. N2: position and sign pass 55 %, amount unknown. N3: DEAD 80 %, since smoothing removes the term's own structure and the law's gas peak stays. Overall: term as local present gas dead 70 %, wounded 20 %, alive 10 %.

## Limits known now
Plummer baryons; projected along z with no inclination. QUMOND-type estimator, field not solved for curl. Static snapshot, so no dynamics, no orbit or gas history. a0 at z = 0. Mass from a lens reconstruction. A map pass would still be a description with no action. X-COP-fitted k transferred to a merger out of equilibrium.

Compute: one thread, nice 15, under 4 GB.

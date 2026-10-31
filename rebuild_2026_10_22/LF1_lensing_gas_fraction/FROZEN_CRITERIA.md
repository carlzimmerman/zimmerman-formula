# LF1_lensing_gas_fraction: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** ZN3's shape passes X-COP but misses the massive clusters' outer shear on measured gas (GS4). Do the lensing clusters hold less baryon than the cosmic share, measured from gas and shear with no halo-model mass?

**Standing.** κ = ½ FITTED. Cold dark energy, never a particle. Not "theory closed". Nothing here says the data favour the framework. Footings: the statistic uses no a₀, so it doesn't depend on footing.

**Not independent of the keys.** This is the same KiDS shear that graded G-OUT-M3, so it can't confirm that miss. What's new is that it takes ZN3's shape out, gives a direct baryon share, and shows how the share changes with radius.

## Data, all on disk
- Shear: `X7_cluster_core_significance/x7_measure_percluster.npz`, 326 eRASS1 clusters, 8 bins 0.15–3 Mpc, both h (0.672, 0.686). Stack at bin k over set S: S_k = Σ W_ik B_k (D_ik − leakP_ik) / Σ W_ik, with the grader's W, boost B and leakage.
- Gas: each cluster's eRASS1 Mgas500 at R500, with the grader's q conversion, β-model core and X-COP slope s = 2.7774 beyond R500. No closure tail, no raise; measured gas only (GS4's offset is consistent with 0). Stars: M_b = M_g (1 + f★), f★ 0.034 and 0.0615, gas's shape, the grader's convention.
- Baryon side: the projected ΔΣ_b of each cluster, stacked with the same W_ik, no boost.

## Statistic
Aperture densitometry, Rmax = 3 Mpc, on both sides:
ζ(R₁) = [2 / (1 − R₁²/Rmax²)] ∫ from R₁ to Rmax of ΔΣ dlnR, trapezoid over the bins in log R, with the bin containing R₁ used only from R₁ out.
**Γ(R₁) = ζ_b(R₁) / ζ_shear(R₁).** No mass model enters. Both sides lose the same annulus term, so Γ is the baryon share of the compensated cylinder.

**log Y = log₁₀(Γ / 0.15945)**, 0.15945 = 1 − f_c, the native share.

## Radii, from gas alone
- R₂₀₀: median over the set of fair-share R₂₀₀ from measured gas, nearest of the edges 0.15 × 20^(k/8), k = 3–7.
- R₅₀₀: median eRASS1 R500, q-converted, nearest edge, same list. If both give the same edge, the radial read is NOT MEASURED.

## Sets
**Primary: M3, the heaviest Mgas500 tercile, because that's the key that fails.** M1, M2 and all 326 are reported. Tercile edges are the grader's.

## Errors
Each set, each cell: SE = larger of cluster bootstrap (2,000, seed 20261031) and 30-patch jackknife (the grader's patches, or 30 equal-count sky cells if those can't be read, disclosed), in quadrature with the same statistic's offset on cross shear and on random-point shear.

## Classes, M3 at R₂₀₀, four cells (h × f★)
- **NOT POWERED:** SE > 0.06 dex in any cell.
- **FAIR SHARE HOLDS:** |log Y| ≤ 2 SE in all four.
- **DEPLETED:** log Y < −2 SE in all four. Add **[ENOUGH FOR ZN3]** if log Y − 2 SE ≤ −0.093 ≤ log Y + 2 SE or log Y + 2 SE < −0.093 in all four, the size of the gas raise G-OUT-M3 needs.
- **EXCESS:** log Y > +2 SE in all four.
- **MIXED:** otherwise.

**Radial tag:** Δ = log Y(R₅₀₀) − log Y(R₂₀₀), paired bootstrap, M3. **[FLAT]** |Δ| ≤ 2 SE. **[OUTSKIRTS-LED]** Δ > 2 SE (the share falls outward). **[CORE-LED]** Δ < −2 SE. Outskirts-led can't by itself tell missing gas from extra mass or infall along the line of sight. I'll say so.

**[SHAPE-DEPENDENT]:** a fair-share cluster with a more compact cold profile than gas has Γ ≠ 0.15945 under this filter. Build the fair reference: per cluster, cold mass f_c M₂₀₀ with an NFW shape, c₂₀₀ 4.43 and 5.94 (ZN1 and ZN3's own zooms at 1e15, 1e14), extended to 3 R₂₀₀, with the same gas. Tag if using either reference line in place of 0.15945 changes the class.

## Reported, not graded
- M1, M2, all 326. Γ at every edge from 0.42 Mpc out.
- Same-cylinder Γ on X-COP's own HSE mass and gas, as a hydrostatic bracket: labelled, never graded. The tension between that and the shear, stated in plain terms.
- Reduced-shear size: a κ-based estimate of (f_r − 1) on the shear stack.
- Miscentring on the gas side, using the catalogue offset.
- Rmax 2.18 Mpc in place of 3. Gas tail s 2.676 and 3.071 (GS1's band).
- Selection: M3 is cut on gas, whose scatter biases Γ high. Size from Mgas500's catalogue error, reported.

## Checks
- **K1:** my gas ΔΣ against the grader's projector on five clusters: ≤ 1 %, bins from 0.42 Mpc.
- **K2:** ζ on an analytic singular isothermal ΔΣ against the closed form, on the 8-bin grid: ≤ 2 %, and the bias is reported.
- **K3:** my S_k reproduces the grader's measured band numerator, n = Σ W B (D − leakP) over the OUTER bins, M3, exactly (≤ 1e-9).
- **K4, injection:** a synthetic shear stack built from fair-share clusters at a known share 0.10 with shape c 5 returns the reference-corrected share within 3 %.
- **MUTATE:** gas × 2 must raise log Y by 0.301 within 0.03 and change the class or exit 1. Shuffled shear between clusters must move Γ by > 1 SE in at least one set, or be reported as insensitive.
- Any K failure: no verdict, exit 1.

# CFG485 FROZEN CRITERIA: does settling completeness produce the KiDS early/late split?

Written 2026-10-08 and committed alone, before any script of this lane exists and before any number of this lane is
computed. For the age proxy, only the column names of the on-disk catalogues were read, never their values. Nothing
below may change after a result is seen. Any later deviation goes in the README as a disclosed departure.

κ = ½ is FITTED. The two footings, a0 = 9.3603e-11 and 1.1312e-10 m/s², are scored separately and never pooled.
a0 is flat in z. No dark-matter particle: the cold fluid's mass is still required. No downloads.

## Why

- **The failure.** The KiDS-1000 early/late lensing split is candidate B's one specific failure relative to ΛCDM
  (STANDING_2026-09-29).
  - It survives the jackknife (CFG88), stricter isolation (CFG96) and the systematics nulls (CFG116).
  - B's own stellar-mass calibration brings it to 2.8σ released and 3.6σ re-measured (CFG95).
  - The host-status readings failed (CFG446, CFG471). CFG316's DESI re-test was NOT DIAGNOSTIC.
- **The untried reading: settling completeness.** In the working model the phantom is settled cold fluid.
  - Settling rate: Γ = λ/t_dyn with t_dyn = 1/√(4πGρ) and λ = 1, no constant. CFG464 finds this not excluded by the
    corrected cluster budget.
  - Edge: the mass-conserving edge r_edge = r_M / ln[1/(1 − f_b)] = 5.850 r_M (CFG423/CFG424, PAPER45 v2.1), with
    r_M = √(G M_b / a0) and the engine's f_b = 0.02237/0.14237.
  - If older or denser early-type lenses have settled further at fixed g_bar than late types, the early-minus-late
    excess would follow with no free parameter.
- **What this lane does.** It predicts that difference and scores it on exactly the data, covariances and stellar-mass
  calibration of CFG95, with CFG413's free two-halo treatment.

## Step 0 (frozen before anything else): CFG95's stellar-mass calibration, unchanged

- **How it is run.** It is executed read-only from `CFG95_kids_split_own_calibration.py`, up to its "C1-C3" banner,
  with MUTATE forced off.
- **Early types:** δ_early(M*) = log10 α_dyn,foot(σ(M*)) + 0.25. α_dyn is the CFG33/CFG55 ATLAS3D fit, refitted per
  footing exactly as CFG95 does. σ(M*) is CFG95's ATLAS3D OLS fit.
- **Late types:** δ_late = log10(Υ_SPARC,foot / 0.5), i.e. +0.086 dex canonical and +0.057 dex alt.
- **True baryonic mass:** M_b,true = 10^δ M* + M_gas, with M_gas = f_cold(M*) M* (CFG61).
- **Radii:** each lens keeps its catalogue-mass radius R = √(G M_gal / g) in each g_bar bin.
- **Nothing in Step 0 may be retuned in this lane.** The R rows below change only settling ingredients, never the
  calibration.

## The age input (declared before any value is read)

- **No stellar-population age is on disk.** Checked by column name:
  - `lr_lenses.npz`: ra, dec, z, logM, Mgal, typ, chi.
  - `cfg110_perlens.npz` and `cfg116_perlens.npz`: lensing sums only.
  - `KiDS_DR4_brightsample.fits`: ID, position, magnitude, photo-z, mask.
  - `KiDS_DR4_brightsample_LePhare.fits`: K-corrections, absolute magnitudes, CONTEXT, REDSHIFT, MASS_MED/INF/SUP/BEST,
    SFR_INF/SUP/BEST.
  - GAMA on disk is the G3C group tables only (CFG471).
- **Declared proxy (P1, primary): the LePhare sSFR formation time.**
  - t_age,i = min(10^(MASS_BEST − SFR_BEST) yr, t_U(z_i)).
  - Both columns are read as log10 (LePhare convention). They come from the same best-fit template, so no IMF or
    0.15-dex offset is applied to their difference.
  - t_U(z) is the flat-ΛCDM cosmic age at the lens redshift (Ωm 0.3153, h 0.6736, as in CFG7_common):
    t_U = 2 / (3 H0 √ΩΛ) · asinh(√(ΩΛ/Ωm) a^1.5).
  - For a constant star-formation history, M*/SFR is the age of the oldest stars. Quiescent lenses reach the cap t_U(z).
- **Fallback.** If MASS_BEST or SFR_BEST is non-finite or below −90, then t_age = t_U(z). The count is reported.
- **Matching.** Lenses are matched to the LePhare file by exact position with CFG446's key (IDs row-aligned with the
  bright sample). z is lr_lenses' z.

## The prediction (no free parameter in the 1-halo model)

- **Per lens:** f_i = 1 − exp(−λ √(4πG ρ̄_i) t_age,i), with λ = 1.
  - ρ̄_i is the mean density inside the edge: ρ̄_i = (M_b,true,i / f_b) / (4π/3 · r_edge,i³), with
    r_edge,i = 5.850 √(G M_b,true,i / a0).
  - By construction the edge encloses the baryons plus the full phantom, M_b/f_b, which is the halo's whole cosmic
    matter share.
  - f is computed from each lens's own calibrated M_b,true, not from the grid node.
- **Profile.** The law's phantom is M_ph(<r) = M_law(<r) − M_b, using CFG7_common.M_law with ν_mono as in CFG61/CFG95.
  - It is truncated at r_edge(M_b): frozen beyond, i.e. zero density outside.
  - It is projected with CFG61's projector and multiplied by f.
  - The true point-mass term M_b,true / (πR²) is added.
- **Stack.** This is CFG95's stack: CFG61's (log M*, z) grid, lens weight M_gal, weight 1/g within a bin, and linear
  interpolation in log M_b between the profile nodes.
  - The truncated tables are built at each node with that node's own r_edge. The edge is z-independent because a0 is flat.
  - The stack is linear in f, so each cell carries its M_gal-weighted mean f̄. This is exact, not an approximation.
- **Precision.** f is handled as f = 1 − q with q = exp(−x) computed directly. The settling increment δD is formed from
  the q differences, never by subtracting two stacks. If every q underflows, the increment is exactly zero and the sign
  test below is undefined (cell = N).

## Two-halo term, data, covariance, statistic

- **Two-halo term (CFG413/CFG377's free treatment).** One free amplitude multiplies the pair-averaged (R / 1 Mpc)^−0.8
  template, built with the same stack weights. It is profiled analytically and unconstrained in sign.
  - On the difference, free per-class amplitudes reduce exactly to one amplitude on the all-lens template, because in
    this stack the class templates are proportional bin by bin (control C5).
  - The model for D is therefore D_model + A · T, with 7 − 1 = **6 dof**.
- **Data:** CFG95's two data sets on K1 (CFG61's seven 1-halo bins, 8–14), exactly as CFG95 builds them.
  - **Released:** Brouwer+2021 Fig. 8 colour bins, with C_D = C_ee + C_ll − C_el − C_le.
  - **Re-measured:** the June split (`lr_esd_jackknife.npz`), with CFG88's 50-patch jackknife covariance and
    Hartlap factor 41/49.
- **Models compared.** Every model has the same calibration, data, covariance and two-halo treatment.
  - **S (settling):** per-lens f_i as above.
  - **B2 (nested colour-blind control):** S with every lens given the same f, equal to the M_gal-weighted mean of f_i
    over all lenses of both classes. It has the same edge and the same total settled amount; only the age/colour
    dependence is removed.
  - **B1 (the record's colour-blind law):** CFG95's calibrated law exactly (ν_mono phantom to 0.40 r_ta, f ≡ 1), plus
    the same free two-halo term.
- **Statistic:** χ² on K1 with A profiled, and p from χ²(6). Δχ²_Bj = χ²(Bj) − χ²(S).
- **Sign:** fit D_obs = D_B2 + s·δD + A·T jointly (linear, same covariance), with δD = D_S − D_B2 formed from q. The
  prediction is s = 1. The fit gives ŝ ± σ_s, along with the increment's own signal-to-noise SNR_δ = √(δDᵀ C⁻¹ δD).

## Verdict (declared now)

- **Per cell** (data set × footing; four cells):
  - **S-cell:** p_S > 0.05 AND Δχ²_B1 ≥ 4 AND Δχ²_B2 ≥ 4.
  - **C-cell:** ŝ/σ_s ≤ −2. The data want the opposite sign of the settling increment at ≥ 2σ.
  - **N-cell:** otherwise, including an undefined sign test.
- **Lane verdict:**
  - **SUPPORTED** if all four cells are S. Both data sets and both footings are required, as in CFG95's H1/H2.
  - **CONTRADICTED** if all four cells are C.
  - **NOT DIAGNOSTIC** otherwise. The README lists every cell's label and numbers. If the increment is too small to
    matter (SNR_δ < 2 in every cell), the README says that the reading cannot produce the split at this rate and edge,
    and why.
- **Requiring improvement over both B1 and B2 is deliberate.**
  - The 5.85 r_M edge is itself colour-blind. An improvement that comes from the edge alone (S ≈ B2 ≫ B1) is not
    settling completeness.
  - An improvement over B2 alone, with S worse than B1, does not beat the record's colour-blind law.

## Checks (a failed control is reported and kept, never silently fixed)

- **C1 CONTROL:** CFG95's machinery, run read-only, reproduces CFG95's committed H numbers to 1e-6 on both footings:
  - released 20.3037 / 18.5935;
  - re-measured 26.6775 / 24.7862 (from CFG95's results JSON).
- **C2 CONTROL:** this lane's own vectorised stack, with CFG61's 0.40 r_ta tables, f ≡ 1 and no two-halo term,
  reproduces CFG95's model D on K1 to 1e-9 relative, and the C1 χ² to 1e-6, on both footings.
- **C3 CONTROL:** the ν_mono phantom at r = 5.850 r_M equals (1 − f_b)/f_b · M_b = 5.364 M_b to 1e-3 at
  M_b = 1e9, 1e10.5 and 1e12 Msun, on both footings (the edge is mass-conserving under the kernel used).
- **C4 CONTROL:** the log-M_b interpolation of the truncated phantom ΔΣ, plus the point mass, matches directly computed
  profiles at three off-node masses to 1% at the K1 radii.
- **C5 CONTROL:** the early and late two-halo templates are proportional over K1. The maximum relative deviation of
  T_e/T_l from its mean is below 1e-9, so one amplitude on D is exact.
- **C6 CONTROL:** every lens matches the LePhare file by exact position; u − r > 2 reproduces typ; and
  log M* = MASS_MED + 0.15 (as CFG446 C2).
- **C7 (load-bearing; proxy sanity):** the proxy orders the classes, i.e. the median t_age of early types is at least
  that of late types. If it fails, the test of "older early types" is not being performed, and the README says so.
- **H1 [HEADLINE; MUTATE must fail]:** the lane is SUPPORTED (all four cells S).
- **H2:** the prediction's sign survives, i.e. no cell has ŝ/σ_s ≤ −2.

## Reported rows (no verdict weight; declared now)

- **R1:** distributions per class:
  - t_age, t_dyn and q = 1 − f (median, 5% and 95%, and the M_gal-weighted mean of q);
  - the number of lenses with q > 1e-3 and with q > 0.1;
  - the fallback count.
- **R2:** ρ is the local density at the edge, CFG464's MW convention ρ = V_c²/(4πG r²) with V_c² = G M_b/(f_b r_edge).
  This is the slowest shell. It gives a lower bound on f at every radius, hence an upper bound on the age effect.
- **R3:** age proxy P2 = t_age/2, the mass-weighted age for a constant star-formation history.
- **R4:** the most favourable declared case, R2's density with P2's ages.
- **R5:** the edge from census retention, f_ret = 0.10. This uses the general form
  r_edge = r_M / ln(1 + f_ret f_b/(1 − f_b)) from PAPER45 v1 / CFG398. The primary density definition is kept, with
  M_tot(<r_edge) = M_b (1 + (1 − f_b)/(f_b f_ret)).
- **R6:** CFG95's own edge (0.40 r_ta, CFG61's tables) with settling. The density is the node's M_law(<r_e) over
  4π/3 r_e³ (cell level), with per-lens ages.
- **R7:** no two-halo term (CFG95's exact statistic, 7 dof) for S, B1 and B2.
- **R8:** the absolute per-class profiles of S and B1 on K1, against the released per-class blocks (C_ee, C_ll), with
  the two-halo amplitude profiled per class. This shows the truncated model's absolute level (CFG398's tension).
- **R9:** the total-D sign, i.e. the sign of the predicted D_S on K1 against the measured one.

## MUTATE (CFG485_MUTATE=1; outputs *_MUTATE.*)

- **What changes:** t_age is permuted across all 181,477 lenses (numpy default_rng(485)). Everything else is unchanged.
- **What must happen:** H1 must FAIL, i.e. any improvement over B2 is lost.
- **When it is informative:** if the main run already fails H1, the MUTATE is uninformative for the headline (declared
  now). The machinery check is then C2's exact reproduction, and the shuffled class contrast of mean q is printed.

## Outputs

`cfg485_settling_split.py`, `cfg485_settling_split.out` / `_MUTATE.out`, `cfg485_settling_split_results.json` /
`_MUTATE_results.json`, and a plain `README.md`. Commit locally only; nothing is pushed.

Never "theory closed". Nothing here says the data favour either model.

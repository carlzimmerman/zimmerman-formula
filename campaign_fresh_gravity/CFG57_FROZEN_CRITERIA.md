# CFG57 — the hot-gas test on SLUGGS: FROZEN CRITERIA

Written 2026-09-28, **before any gas data were fetched and before any CFG57 run**. This file is committed on its own, ahead of any data or script. Nothing below may change after data arrive. Any later deviation goes in the README as a disclosed departure.

## Question

Does adding each galaxy's measured hot X-ray gas to the baryons close the SLUGGS globular-cluster deficit that survived dynamical stellar masses? In CFG55 (JAM-calibrated) the law sits at +0.097 ± 0.024 dex (4.0σ) and B's derived rule at +0.046 (2.6σ).

## Data status at freezing

No hot-gas profile for any SLUGGS galaxy is in the repository (CFG32: "no gas profiles in the repository"). There are two candidate sources, to be fetched **only on the owner's approval**:

1. **Lakhchaura et al. 2018** (MNRAS 481, 4472; arXiv:1806.00455; PDF 1.8 MB, LaTeX source 1.4 MB).
   - Deprojected n_e(r) out to about 30 kpc, in appendix figures only, to be digitised from the vector figures as CFG41 did.
   - Of CFG55's 16 it covers NGC 4486 (M87), NGC 5846, NGC 4374 and NGC 4649.
2. **Fukazawa et al. 2006** (ApJ 636, 698; arXiv:astro-ph/0509521; source 137 KB).
   - Table 4 gives n_e at 10 kpc and the maximum detection radius.
   - Of the 16 it covers NGC 5846, NGC 4374, NGC 4649, NGC 4365, NGC 4494, NGC 3607 and NGC 4697.

## Sample rule

- **Membership:** CFG55's 16 galaxies intersected with the coverage of the approved source(s), fixed by coverage alone before any offset with gas is computed.
- **No changes after offsets:** no galaxy is added or dropped after offsets are seen.
- **Always shown:** M87, NGC 5846 and NGC 4374 are reported individually whenever covered; an uncovered one is stated as uncovered.
- **Galaxies with no covering source** are reported without gas and are not in the headline mean.

## Gas model (identical for law and rule)

- **Geometry and density:** spherical. ρ_gas = μ_e m_p n_e with μ_e = 1.155.
- **Source 1:** the digitised n_e(r) points, interpolated in log–log.
  - Beyond the last point, extrapolate with the power-law slope fitted to the outermost three points.
  - Inside the first point, hold the density constant.
- **Source 2:** used only where source 1 does not cover the galaxy. A β-model with β = 0.5 and r_c = 1 kpc, normalised to n_e(10 kpc). Where both sources cover a galaxy, source 1 is used and source 2 is reported as a cross-check.
- **Distances:** everything is moved to SLUGGS's distance. Radii scale as D; a deprojected n_e scales as D^(−1/2).
- **No hydrostatic equilibrium is assumed.** The gas enters only as mass; its temperature is not used.

## Dynamics (identical for law and rule)

- **Machinery:** CFG55's, read-only: h50's GC bins and isotropic Jeans (γ = 3); Hernquist stars with SLUGGS's R_e; the outer bins; ν_mono; CFG36's red collapse masses; x_e = 0.40.
- **Calibration:** the gas is added inside r_1/2. The model's total mass there is ν(g_N/a₀)·[M_*/2 + M_gas(<r_1/2)], plus the debris inside r_1/2 for the rule, and it equals M_JAM/2. g_N uses the same enclosed baryons.
- **Jeans model:** M_b(<r) = M_* f_Hernquist(r) + M_gas(<r).
- **The rule's inputs:** the collapse mass uses M_* (the relation is in stellar mass). The edge phantom uses M_* + M_gas(< R_max of the source), which is measured gas only, never extrapolated to the edge. The M_*-only variant is reported.

## Pre-declared checks

- **C1 CONTROL:** CFG55's committed per-galaxy offsets reproduced with the gas set to zero on the covered subset (to 1e-9).
- **C2 CONTROL:** the transcription or digitisation.
  - The row count per source, plus one spot value.
  - For a digitised curve, one number printed in the paper (a quoted n_e, gas mass or radius) reproduced within 10%.
- **C3 CONTROL:** the numerical gas-mass integral of the β-model against its closed form (to 1e-8).
- **H1 [HEADLINE; MUTATE must fail]:** with the measured hot gas, the JAM-calibrated law fits the outer GCs of the covered galaxies: |mean offset| < 2σ (galaxy-to-galaxy error), both footings.
- **H2:** the rule, with the same gas, fits: |mean offset| < 2σ, both footings.
- **H3 (leverage):** the gas moves the law's mean offset by more than that mean's error. If it does not, the test is non-diagnostic, and that is a valid result.
- **Reported rows:**
  - per-galaxy offsets with and without gas;
  - the gas mass each galaxy would need to null its law offset (the same shape);
  - the outer extrapolation slope ± 0.3;
  - β = 0.4 and 0.6 for source 2;
  - the edge phantom from M_* only.
- **MUTATE:** every gas density × 0, which reduces the test to CFG55 on the covered subset. H1 must fail, and the script must exit 1.

## Reading (declared)

- **H1 PASS:** the SLUGGS deficit is baryonic. The measured hot gas closes it, and B's derived rule loses its last supporting population. H2 then says whether the rule over-predicts.
- **H1 FAIL with H3 PASS:** the deficit survives the measured gas as well. The massive early types want mass beyond the law's baryons, and H2 says whether the rule supplies it.
- **H3 FAIL:** non-diagnostic. The gas is too small, or too uncertain at the GC radii, to decide.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.

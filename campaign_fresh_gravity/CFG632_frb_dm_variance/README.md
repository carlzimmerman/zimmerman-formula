# CFG632: the FRB DM-z scatter (Sharma, Krause et al. 2026, 114 localized FRBs) vs candidate B's census gas. CONSISTENT (interval-limited) on both footings; the power gate passes and both MUTATE controls are EXCLUDED (the test has teeth)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (3d0747e75), before any likelihood was run on the real sample.
  The prediction script was run before the freeze (not compared with the data); its sha256 is in the criteria and matches the
  committed `cfg632_predict.py`.
- **Scripts:** `cfg632_predict.py` (framework mean DM and sigma_DM(z), about 5 min) -> `cfg632_predict.json/.out`;
  `cfg632_fit.py` (likelihood, power gate, controls, verdict, about 15-20 min) -> `cfg632_fit.out/.json`;
  `CFG632_MUTATE=1` -> `cfg632_fit_MUTATE.out/.json` (exit 0 = both teeth bite); `cfg632_diag_hostprior.py` (post-freeze
  diagnostic, no verdict weight) -> `cfg632_diag_hostprior.out/.json`. One process, < 1.5 GB, nice 10.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are scored separately, never pooled. The cold energy's
  mass is still required (no particle). This is not "theory closed", and nothing here says the data favour the framework.
  The paper's power-spectrum suppression, gas fractions and sigma_DM band are CONTEXT ONLY.

## Bottom line

| | canonical | alt |
|---|---|---|
| census PRIMARY (B-lo, hydrostatic, diffuse remainder) sigma_DM at z = 0.33 / 0.52 / 1.0 | 130 / 155 / 190 pc cm⁻³ | 141 / 167 / 204 |
| census interval over 8 variants at z = 0.52 | 155–208 | 167–222 |
| fitted amplitude A = sigma_data / sigma_census (PRIMARY) | 0.944, ln A −0.057 (−0.122 / +0.126) | 0.877, ln A −0.132 (−0.122 / +0.126) |
| Z_primary / Z_near / Z_far | −0.45 / −0.45 / −2.75 | −1.05 / −1.05 / −3.28 |
| **power gate** (forecast, mocks): sigma_f(ln A); S_MU1; S_MU2 | 0.134; 6.40; 3.56 → **PASSES** | 0.131; 6.87; 4.49 → **PASSES** |
| **verdict** | **CONSISTENT (interval-limited)** | **CONSISTENT (interval-limited)** |
| MU1 f_ret = 1: Z_near | −7.16 → EXCLUDED | −7.86 → EXCLUDED |
| MU2 f_ret = 0.01 (gas-free extreme): Z_near | +4.14 → EXCLUDED | +4.14 → EXCLUDED |
| **teeth** | **YES** | **YES** |

The data's scatter sits slightly BELOW the census prediction (A 0.94 / 0.88). "Interval-limited" means the far end of the
framework's own bracket is in tension: the declared beta-model profile (BETA, core 0.1 r200c) puts more gas at small radii
and gives Z −2.5 to −2.75 (canonical, TENSION) and −3.05 to −3.28 (alt, EXCLUDED-level). The hydrostatic profile the law
itself gives (H, the primary) is consistent on both footings.

## The raw statistic

Per FRB: DMexgal (= DMobs − DM_MW,ISM, as tabulated) and the spectroscopic host z, for the authors' extended sample
(sharma_sample yes + unclear, N = 114, z median 0.22, max 2.15). The likelihood is the authors' eq. 1, re-implemented in
numpy: p(DMexgal | z) = ∫ LN(DMexgal − 50 − x; ⟨DM⟩(z), sigma_DM(z)) · LN_host(x(1+z); mu, s)(1+z) dx. The scatter of
DM_cosmic at fixed z is separated from the host by its z-dependence. The framework enters only through ⟨DM⟩_F(z) and
sigma_DM(z) = A · sigma_F(z); A has a flat prior in ln A, and the host is marginalised over the authors' flat box
(mu ∈ [4, 6], s ∈ [0.2, 1]).

**C1 (reproduction, context only):** with the authors' own published sigma_DM(z) median as the shape, the same code gives
A = 1.008 (ln A +0.008, −0.122 / +0.126), inside their band [0.845, 1.131] at z = 0.3: **REPRODUCED**. The likelihood
machinery is the same as theirs to within the band. My mean uses MD14 f_d rather than their halo-model stellar density.

## The framework prediction (what was built)

- **Mean:** all baryons except stars and cold gas are ionized wherever they sit, so ⟨DM⟩ does not depend on f_ret.
  f_d(z) = 0.932 (z = 0) to 0.968 (z = 2.25) with MD14 Chabrier stars (Salpeter 0.895–0.961, reported).
- **Scatter:** sigma² = sigma²_1h (Poisson crossings of each catchment's gas, exact projected columns) + sigma²_2h (linear
  clustering of the ionized gas).
  - Gas per catchment: census f_ret (CFG416/515 fret_of, verbatim), M_b = f_ret f_b M_ta, isothermal at sigma² = V_f²/2,
    hydrostatic and self-gravitating in g_N ν_mono(g_N/a0) with central Hernquist stars, out to the census edge
    r_edge = r_M / ln(1 + f_ret f_b/(1 − f_b)). At z = 0 the edge sits at 0.25–0.44 r_ta for 10¹²–10¹⁵ M☉/h.
  - Cluster gas comes out cored and extended (centre/edge density 9–15 at 10¹⁴–10¹⁵). That is why H gives less scatter than
    BETA.
  - **Who carries the signal:** at z = 0.25, 47% of sigma²_1h comes from log M200m 13–14 and 48% from 14–15 (census, both
    footings). Halos below 10¹² contribute < 0.3%. So the FRBs test the census in groups and clusters (f_ret 0.43–0.9).
    Under f_ret = 1, galaxies (10⁹–10¹²) supply 42% of sigma²_1h. That is part of why MU1 fails so badly.
  - At z = 0.52 the one-halo part dominates: 135 vs 77 (canonical PRIMARY).
- **Controls:**
  - MU1 (f_ret = 1) gives 2.4× the census scatter.
  - MU2 (f_ret = 0.01) leaves only the two-halo term: 90 at z = 0.52.
  - The data sit between them, near the census.

## Power gate, MUTATE, controls

- **Power gate:** 200 census mocks and 100 per control. The host truth is (5.0, 0.5), the authors' MCMC start values, not a
  fit. Each mock is fitted with the census shape.
  - canonical: sigma_f = 0.134; MU1 lands at +0.805 (S 6.40), MU2 at −0.530 (S 3.56).
  - alt: sigma_f = 0.131; S 6.87 / 4.49.
  - The gate passes on both footings.
- **C2 (recovery):** 68% coverage 0.645 (canonical) and 0.590 (alt). Both PASS. The median-ln A bias is −0.05.
- **MUTATE (real data):** both controls are EXCLUDED on both footings under all their variants.
  - MU1: Z −7.2 to −9.1.
  - MU2: Z +4.1 to +4.2.
  - **The test has teeth.**
- **K1 (kernel):** |ν_mono − ν_exp| = 4.4e-5 absolute (4.9e-9 relative) for y < 1. PASS at 1e-4.
- **K3 (profile normalisation):** 7.6e-15. PASS. The hydrostatic solve fell back to BETA only in MU2 B-lo (9 / 7
  halo-slices of the pileup degeneracy, CFG628 disclosure 5), never in the census or MU1.
- **K2 FAILS as frozen** (ratio 1.0235 vs the 2% tolerance). The failure is in the check's Fourier side, not in the
  variance:
  - The real-space projected integral used for sigma²_1h is converged: 2.06160e26 at 220, 2000 and 20000 b-points.
  - It equals the EXACT uniform-shell Fourier transform to 1e-6: 2.06163e26 at k_max = 3e3 and 3e4 / r_edge.
  - The check's midpoint-sinc transform (`u_of_k`) over-counts power at k r_edge ≳ 10³. Its value grows with k_max
    (2.110e26 → 2.154e26).
  - `u_of_k` also enters the two-halo term. There it only matters at k ≳ 10³ / r_edge (≳ 300 h/Mpc for clusters), where
    P_lin is negligible.
  - The tolerance was not changed.

## Sensitivity and post-freeze diagnostics (no verdict weight)

| | canonical Z (census PRIMARY) | alt Z |
|---|---|---|
| MW halo 30 / 80 pc cm⁻³ | −1.13 / +2.10 | −1.62 / +1.38 |
| MW halo marginalised over flat [30, 80] (post-freeze) | −0.88 (posterior mean 38) | −1.40 |
| Salpeter f_d | −0.78 | −1.34 |
| yes-only sample (N = 92) | −0.46 | −0.94 |
| host width prior widened to s ≤ 2 (authors' HMcode range; post-freeze) | −1.05; MU1 −7.43, MU2 +3.21 | −1.61; MU1 −8.12, MU2 +3.21 |

- **Disclosure: the host width sits at the upper edge of the authors' BCEmu prior** (s = 1.0) in every fit, including C1.
  Widening it to 2 moves the best s to 1.1. The census stays CONSISTENT and both controls stay EXCLUDED, though MU2 drops to
  Z 3.21.
- **The MW-halo term is the largest single systematic.** Moving it from 50 to 80 moves ln A by about +0.28. It is an
  inherited constant, not a framework quantity.

## Inherited ingredients (flagged; none is a yardstick)

- **In THE PAPER's inference (context):**
  - the BCEmu (Schneider+19 / BaryonForge) and HMcode baryonification emulators of P_gas and S(k);
  - the Tinker08 mass function and Tinker10 bias;
  - the BCEmu SHMR with its Chandra / SPT eta prior;
  - f_diffuse from the halo-model stellar density plus cold gas;
  - fixed Planck18 cosmology with sigma8 = 0.8111;
  - the log-normal p(DM_cosmic), the log-normal host and the MW halo of 50;
  - BCEmu's back-reaction of gas expulsion on the dark matter, which is what turns a gas measurement into "suppressed matter
    clustering".
- **In THIS lane:**
  - the authors' likelihood form (log-normal DM_cosmic, rest-frame log-normal host with their flat prior box, MW halo 50,
    400-bin host marginalisation);
  - the catchment population: Tinker08 (200m, z-evolving) on the PM's EH no-wiggle spectrum (sigma8 0.811), Tinker10 bias,
    LCDM linear growth (cold energy is cold matter outside bound systems);
  - NFW / Duffy08 c200m for M_ta, r_ta and r200c;
  - the Delta_ta(z) interpolation 5.55 Ω_m(z)^−0.654;
  - Moster+13 SHMR with z-evolution (recalled, PROVISIONAL);
  - Hernquist stars at a = 0.015 r200c/(1+√2) (CFG556);
  - the BETA bracket profile (CFG556);
  - MD14 stellar mass density (Chabrier ×0.61, R = 0.27);
  - the authors' cold-gas fit and table;
  - χ_e = 1 − Y/2;
  - linear P(k) in the two-halo term;
  - the overlap and bias-renormalisation rules (declared).

## What this says about the growth tension

- **What the FRBs see.** FRBs measure the ionized gas only. The sightline scatter is dominated by gas in 10¹³–10¹⁵ M☉/h
  halos. The census places that gas consistently with 114 raw DMs, with no feedback model and no gas ejection beyond the
  census edge. The census is low retention in galaxies, 0.43–0.9 in groups and clusters, with the gas hydrostatic in the
  law's field and extended to 0.25–0.44 r_ta.
- **What the census already contains.** In the framework, the authors' "suppression" corresponds to retention below one and
  an extended, cored gas distribution, which the census already has. Full retention (the PM runs' f_ret = 1) is EXCLUDED at
  7–9σ. So is a gas-free universe at 4σ.
- **What the FRBs cannot see.** The framework's small-scale excess in total matter power (CFG555/556: +12–14% at k = 0.3,
  +72–89% at k = 1) is in the cold energy. Cold energy settles into the law's phantom inside the supply edge, which is about
  r200m. FRBs have no electrons there to see it. The paper's step from gas to total matter goes through BCEmu, where
  expelled gas drags the dark matter outward. That mechanism is not candidate B's: cold energy settles by the supply rule,
  not by following the gas. So this result neither relieves nor sharpens the cosmic-shear and growth tension.
- **What it does pin.** It fixes an input to that tension. The f_ret = 1 variant of CFG556 (E = +0.88 / +1.05) is now
  excluded by raw FRB data. The census variant, whose gas the FRBs accept, still gives E = +0.715 / +0.883 in total matter.
- **What would test the cold-energy leg.** Lensing (CFG592/596), or an FRB × lensing cross-correlation, would. FRBs alone
  cannot.

## Run

```
nice -n 10 python3 -I campaign_fresh_gravity/CFG632_frb_dm_variance/cfg632_predict.py
nice -n 10 python3 -I campaign_fresh_gravity/CFG632_frb_dm_variance/cfg632_fit.py
CFG632_MUTATE=1 nice -n 10 python3 -I campaign_fresh_gravity/CFG632_frb_dm_variance/cfg632_fit.py
nice -n 10 python3 -I campaign_fresh_gravity/CFG632_frb_dm_variance/cfg632_diag_hostprior.py
```

The data path defaults to `<repo parent>/_external_data/frb_sharma26/repo/`. Override it with `CFG632_DATA`. Nothing was
downloaded beyond the owner-approved partial clone, and no file of it was missing for this lane.

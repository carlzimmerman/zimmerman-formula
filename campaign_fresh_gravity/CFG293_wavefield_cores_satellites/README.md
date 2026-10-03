# CFG293: CFG288's wave field, its solitonic cores, and the satellites. Pre-flight result: NO right-sign window in m; the harness was not run

> **kappa = 1/2 FITTED.** No dark-matter species is added by hand. The cold component is CFG288's road-W field, a classical field whose quanta would be light bosons, and **the cold mass is still required** (CFG288 leaves its amount free). Nothing here says the theory is closed or that the data favour the framework.

- **Criteria:** `FROZEN_CRITERIA.md`, committed before any script existed (commit 15a61e46e, sha256 5e06bbce...0f73; every output prints it).
- **Script:** `cfg293_wavefield_preflight.py` (about 2 s per mode).
  - MUTATE=0: main run.
  - MUTATE=1: uncored wave field (the soliton switched off).
  - MUTATE=2: m = 37 eV in every decision row.
- **Outputs:** `cfg293_wavefield_preflight[_MUTATE1|_MUTATE2].out` and `_results.json`.
- **Exit codes:**
  - The main run exits 1, for two load-bearing failures: the PRE-FLIGHT finding (NO window), and control C-SP3 (my frozen tolerance; see disclosures).
  - MUTATE=1 and MUTATE=2 exit 0: their reproductions hold.
- **What was used:** nothing downloaded, and no satellite sample touched. The record's SHMR and NFW come from h48 (exec'd read-only). The aggregate S and L numbers come from CFG45's committed JSON. Schive+14 was read on arXiv pages only.

## Bottom line

**No m in CFG288's window gives the sign the satellites need. Across the window the soliton is a small, dense nugget: it ADDS cold mass inside r_ev = (4/3) r_half in every generic system, and adds it fractionally far more in the UFDs than in the classicals.**

- **M31 / classical dwarfs: the wrong way, and small.** q runs from +0.00001 to +0.10 (the cold mass inside r_ev rises by up to 10%). The required change is a fall of at least 11.6%.
- **UFDs: up**, by +0.3% to +250% depending on m and the form.
- **The classical bite exists only outside the window.**
  - It needs m ≤ 2.4e-22 to 1.5e-21 eV, depending on form and prescription: 1.1 to 1.9 decades below the window floor of 2e-20 eV that CFG288's G-PK sets.
  - At those masses the generic UFD loses 94% to 99% of its cold mass inside r_ev. That brings back B's isolated-law UFD failure (3.5 to 3.9 sigma, CFG259 / CFG45 / CFG28).
- **The reason is an ordering.** r_c / r_ev is 12 to 81 times larger (F-H) or 18 to 133 times larger (F-V) in the UFD than in the classical systems, because r_c scales as 1 / (m sigma) or as M_h^(-1/3) / m. So any core big enough to reach r_half in an M31 dwarf has already swallowed the UFD's r_half, at every m.

The wave field's core physics is therefore not the inside-r_half rule CFG286 asked for. Under the frozen rule the lane stops at the pre-flight. CFG286's harness was not run, and no satellite was scored with a core.

## The pre-flight (generic systems; q = [M_comp(<r_ev) - M_NFW(<r_ev)] / M_NFW(<r_ev))

**Definitions.**
- G-U is a UFD: sigma 3 km/s, r_half 30 pc, the record's collapse mass 1e9 Msun.
- G-C is 18 classical / M31 systems: sigma 8-12 km/s, r_half 200-1000 pc, M_* 1e6-1e7 (M_c 5.3e9-1.4e10).
- F-H is Schive+14's eq. 7 at z = 0 (the largest core it gives), with the record's halo converted to Schive's virial mass. F-V is r_c = k hbar / (m sigma), with k = 0.5096 derived from the SP ground state.
- P-C joins soliton and NFW at the outermost density crossing. P-3 joins them at 3 r_c.
- q does not depend on f_ex, f_b or the footing (a0 never enters).

| row | m (eV) | r_c G-U, F-H / F-V | q G-U: F-H (P-C / P-3) | q G-U: F-V (P-C / P-3) | q G-C range, all combinations | right-sign window |
|---|---|---|---|---|---|---|
| D1 | 2e-20 | 7.7 / 16.3 pc | +2.505 / +2.504 | +0.401 / +0.240 | +0.0026 to +0.102 | no |
| D2 | 1e-19 | 1.5 / 3.3 pc | +0.567 / +0.555 | +0.210 / +0.208 | +0.0006 to +0.021 | no |
| D3 | 1e-18 | 0.15 / 0.33 pc | +0.059 / +0.057 | +0.027 / +0.026 | +0.00006 to +0.0021 | no |
| D4 | 1e-17 | 0.015 / 0.033 pc | +0.0059 / +0.0057 | +0.0028 / +0.0027 | +0.00001 to +0.0002 | no |
| R-top | 37 | ~1e-20 pc | 0 (\|q\| ~ 1e-21) | 0 | 0 | no |
| R-out (outside) | 1e-22 | 1.5 / 3.3 kpc | -0.996 | -1.000 | -0.96 to +0.025 | no (the UFD is not spared) |

**What the rows show.**
- In every decision-row case the soliton rises above the NFW: P-C finds an outer crossing every time. rho_c for G-U is 6.9 to 3.4e7 Msun/pc^3.
- It joins the envelope at 1.8 to 6.5 r_c. In the classical systems that is at most about 25 pc.
- The classical r_c is 0.006 to 6 pc against r_ev = 267 to 1333 pc.

**Decision (frozen rule):** 0 of 16 (row, form, prescription) combinations have a classical bite (q_C ≤ -0.116) together with the UFD spared (q_U ≥ -0.50). **NO WINDOW, so STOP.**

**Reported rows (none is a verdict):**
- **R-floor** (G-U at the record's collapse floors 1e8 to 1e10): q_U stays positive in every decision row except one. That exception is D1, F-V, P-3 at M_c = 1e10, where q_U = -0.20, still spared.
- **R-Mh** (F-H with M_200c, or with M_vir / 3): the same signs. q_U is +1.27 to +2.37 at D1, and q_C stays at or below +0.098.
- **R-edge:** the largest m with any classical bite is 2.45e-22 (F-H, P-C), 4.03e-22 (F-H, P-3), 7.10e-22 (F-V, P-C) and 1.55e-21 eV (F-V, P-3). At those m, G-U's q is -0.98, -0.94, -0.99 and -0.96.
- **Aggregate translation** (approximate, not a harness score). It uses the record's aggregate cold shares, s_U = 0.83 and s_M31 = 0.50, from CFG45's committed S and L medians.
  - M31 LVD median: it moves by -0.0003 to -0.011 dex at D1 and by ≤ 0.002 dex beyond. That is worse, not better.
  - UFD KM median: at D1 with F-H it moves -0.24 dex, to about -0.30 (z about -2.1 on S's error). **At the window floor the soliton could over-fill the UFDs from the other side.**
  - This is a hand-level estimate only. The harness that would test it was not run, because the frozen rule stops on NO.

## Controls and MUTATE

| control | result |
|---|---|
| C-SP1: shooting converged, nodeless | PASS. E = 0.6495339857038; the two tolerances differ by 1e-13 |
| C-SP2: virial T = J | PASS (1.2e-10) |
| C-SP3: shape vs Schive's eq. 3, relative ≤ 3% over 0-3 x_c | **FAIL as frozen**: 6.3% at 2.7 x_c (see disclosures) |
| C-SP4: normalisation vs eq. 3's 1.9 | PASS: 1.937 (+2.0%) |
| C-SP5: eq. 6 vs eq. 7 through the SP profile | PASS (+8.5%) |
| C-SP6: M(<3 r_c)/M and half-mass radius | PASS: 0.957 and 1.465 r_c (Schive: about 95% and about 1.45) |
| C-TAIL / C-NFW / C-MASS | PASS (1.0e-12 / 1.3e-15 / 4.5e-11) |
| C-SIGN: the instrument can see the right sign (R-out) | PASS: all four combinations reach q_C ≤ -0.116 at 1e-22 eV, so the NO is not an artefact of a pipeline that can only add mass |
| MUTATE=1: uncored reproduces the record's NFW, i.e. reading S's cold term | PASS. max \|q\| = 0; M_comp vs h48's `nfw_enclosed` to 1.3e-15 |
| MUTATE=2: m = 37 eV in every decision row reproduces the no-core result | PASS. max \|q\| = 1.6e-21 |

**SP constants derived here:**
- x_c = 1.2993 and I = 2.0622;
- M r_c = 2.679 hbar^2/(G m^2);
- rho0 r_c^4 = 0.2268 hbar^2/(G m^2);
- k = 0.5096.

**Hand predictions (frozen section 8):** HE1-HE7 all held.
- HE1: NO WINDOW.
- HE2: q_C ≥ 0 and ≤ 0.15.
- HE3: the q_U signs and ranges.
- HE4: C-SIGN passes and q_U(R-out) ≤ -0.9.
- HE5: x_c and k.
- HE6: R-edge in [1e-22, 2e-21].
- HE7: the D1 aggregate shifts.

The hand arithmetic used eq. 3's fit and k = 0.49 from memory. The derived values move no reading.

## Disclosures

1. **C-SP3's frozen tolerance was wrong; the failure is kept.**
   - Schive's "accurate to 2%" holds against the exact SP profile only in units of the peak density: the maximum difference there is 0.0043.
   - Relative to the local density, the fit is within 4.2% inside 2 x_c and 6.3% low at 2.7 x_c (the fit's tail is low).
   - A labelled POST-HOC DIAGNOSTIC line was added after the first run. It changes no check.
   - eq. 3 enters no decision number: every q uses the SP profile. The normalisation (C-SP4) and the fractions (C-SP6) agree.
2. **The literature values are PROVISIONAL.** Schive+14's eqs. 3, 6 and 7, the virial-mass definition, the 2% range and the 95% / 1.45 x_c fractions were read through a summariser from the arXiv abstract page and the ar5iv HTML rendering. Eqs. 3 and 7 and the 2% statement were read twice, from two URLs. No PDF was fetched. The SP solution checks eq. 3 independently (C-SP4, C-SP6), and eq. 6 against eq. 7 (C-SP5).
3. **The hand arithmetic** behind the frozen section 8 was done with a calculator in a scratch file outside the repository, on generic systems only, before the criteria were committed.
4. **The harness-level MUTATE (frozen section 6) was not run.** That covers an uncored field reproducing CFG45's reading S on the samples to 1e-9, and m = 37 eV doing the same. The frozen rule stops on NO, so the harness was never run and there is nothing for it to control. The pre-flight MUTATE=1 and MUTATE=2 are its analogues at the cold-mass level.
5. **Declared, not derived:**
   - Schive's eq. 7 coefficient, a simulation result, evaluated at z = 0 (the largest core);
   - the identification sigma_sol = sigma_obs in F-V;
   - the composite prescriptions P-C and P-3;
   - the M_200c to M_vir conversion;
   - the generic grid;
   - the two thresholds: -0.116, derived from the record's M31 LVD numbers and generous (the realistic need with s_M31 = 0.50 is about 23%); and -0.50 for the UFD, generous.
   The NO holds in every combination of form and prescription, and in the R-floor and R-Mh rows. No single declared choice decides it.
6. **What this lane cannot say:**
   - It gives no satellite-level score with a core.
   - It says nothing about cores at infall redshift (they would be smaller, which strengthens the NO), about granule heating, or about tidal effects on the soliton.
   - The UFD over-fill at the window floor is an aggregate estimate. Testing it would need the harness, which the frozen rule did not license.

## Files and runs

Run from the repository root:
- `python3 campaign_fresh_gravity/CFG293_wavefield_cores_satellites/cfg293_wavefield_preflight.py` (main; rc 1)
- the same with `MUTATE=1` and with `MUTATE=2` (rc 0)

Outputs: `cfg293_wavefield_preflight.out` / `_results.json`, and the same for `_MUTATE1` and `_MUTATE2`. A second main run reproduced the `.out` byte for byte, apart from the run-time line.

Nothing here says the theory is closed. kappa = 1/2 FITTED. The cold mass is still required.

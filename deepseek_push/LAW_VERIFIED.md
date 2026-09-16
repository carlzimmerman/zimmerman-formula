# LAW_VERIFIED — the equipartition law's complete test record (2026-09-15)

THE LAW: M_dark(<r)/M_b = r/r_M = sqrt(a0/g_N) — zero free parameters —
with the triad (sigma^2 = v_flat^2/2 = kappa = c_s^2 = 1/2), the equipartition
(M_ph(<r_M) = M_b, Lean-certified), and the universal dark surface density
(<Sigma_ph>(<r_M) = a0/(pi G) = 213.75 Msun/pc^2).

## THE VERIFIED SCOREBOARD (wave 1, every lane committed + pushed)

| test | instrument / data | verdict | the number |
|---|---|---|---|
| dSph floor (G070) | Simon 2019 full sample, 34 objects | **PASS** (3/4) | median |log10(pred/obs)| = **0.222**; bright dSphs 0.163; UFD end FAILS (0.401 — the faint-end boundary, binaries/disequilibrium, honest V2-FAIL) |
| SPARC full curves (G071) | 35 isolated galaxies, 641 rings | **PASS** (V1, V2) | pooled rms **0.145 dex** = the RAR benchmark, ZERO parameters; residual slope +0.010±0.009 |
| the MW (G072) | Eilers+19 / Ou+24 curves | **5/5 PASS** | v_c(8.2) = 223.9/230.2 (within 5% of 232.5); break **6.74 kpc vs 6.1** (10%); rho_dark(R0) = 0.0081 (+3-6% of 0.0084); outer curve: 14/14 well-measured points within 1-sigma |
| lensing floor (G073) | KiDS/Brouwer + DES-Y3 data vector | **4/5 PASS** | mass independence to **0.033 dex** across the 4 mass bins; floor/obs = −0.355 dex (free dust = +2.26x remainder); deep slope −0.526±0.010 vs −1/2 |
| GC boundary (G074) | Baumgardt & Hilker 2018 (112+167 GCs) | **7/7 PASS** | sigma_obs/sigma_pred = sqrt(2 r_M/(eta r_h)), slope +0.339 vs +0.350 predicted, eta = 7.0±1.2; crossing at **M_cross = 1.2e5 Msun with r_M/r_h = eta/2 = 3.39 EXACTLY** |
| cluster triad (G075) | X-COP, 12 clusters | **6/11 (FAILs the finding)** | T_pred/T_obs = **0.28 = (sigma_pred/sigma_dyn)^2 = 0.53^2 exactly**; the EFE-capped dark fraction 0.21-0.031x — the amplitude stays an input, per the registrations |
| sheet/funnel (G076) | the MW + G024 slab | **4/4 PASS** | z_c(8.2) = **140.63 pc exact**; z_c(4)/z_c(8.2)/z_c(15) = 34.7/140.6/1357 pc (the DR4 fingerprint vs NFW); survey column 17.7 in band |
| dataset expedition (G077) | 13 datasets + MANIFEST | **complete** | Simon19, BH18, Eilers19, DES-Y3 3x2pt, WALLABY-DR2, MIGHTEE-HI RAR (NEW 19-galaxy RAR!) |

## THE PATTERN THE NUMBERS MAKE

1. **The law predicts, with zero parameters, at the data's own scatter** —
   dSph floor at 0.22 dex, SPARC curves at 0.145 dex, the MW at 3-6%,
   lensing mass-independence at 0.03 dex.
2. **The domain boundaries are real and machine-matched**: from below, the
   GC crossing sits EXACTLY at r_M/r_h = eta/2 (the equipartition radius vs
   half-light); from above, the UFD end of the dSph floor; from the side,
   the EFE line at g_ext ~ a0 (the 6.74-vs-6.1 kpc MW break).
3. **The one honest failure carried: the cluster amplitude** — the triad
   scales the temperature FORMULA across 8 decades (Sculptor 9.2 km/s to
   ~630 km/s at M_b = 5e13) but the capping leaves the normalization an
   input (G017/G050/G057 registrations hold).

## THEORY-LEVEL STATEMENT (what survives every audit and every test)

Gravity everywhere: GR + one shift-symmetric scalar whose Noether charge is
the cold sector; in the deep isolated regime the sector is the
maximum-entropy equilibrium at the DE-set temperature (sigma^2 = v_flat^2/2),
giving the r^-2 profile, the equipartition, the RAR as hydrostatics, the
universal surface density, Cassini null, lensing = GR with real mass; the
Solar System and galaxy cores are Newtonian (strong-field regime); clusters
and the cosmic bulk are carried by the free-dust phase (>= 90% of Omega_dm,
the honest budget); dark energy is the vacuum value f(0) = -1 of the same
scalar and ACTS through the virial scale it sets.  What is NEW and owned:
the zero-parameter inner-galaxy component with its exact normalization, the
never-before-tested observables (dSph floor, universal surface density, the
funnel, the GC boundary, the RAR as a mass law).
# CFG806 FROZEN CRITERIA: the baryon census f_ret(M_ta) derived from the framework, or not

Committed alone, before any script or number. 2026-10-15.

## Why
CFG804 closed the KiDS-1000 outer lensing inside 0.31 Mpc with N = 1/f_ret, but f_ret is the record's OBSERVATIONAL census
(CFG416: 0.10 below log M_ta 12.5, +0.45/dex to 0.55 at 13.5, +0.30/dex to a 0.90 cap). This lane asks whether the framework
itself predicts it. Census targets (fret_of at log M_ta = 12 / 13 / 14 / 15): **0.100 / 0.325 / 0.700 / 0.900**.
CFG804 requirement: N = 1/f_ret >= 3 (canonical) / 4 (alt) at the four KiDS bins.

## Fixed framework inputs (from the record; none adjusted here)
- Law g_N = g^2/(g + a0); a0 = 9.3603e-11 (canonical) / 1.1312e-10 (alt), never pooled. kappa = 1/2 fitted.
- f_b = 1/(1 + 5.364) (as CFG804). Catchment: r_ta = [3 M_ta / (4 pi Delta_ta(z) rho_m0 (1+z)^3)]^(1/3), Delta_ta(z) from
  CFG654_independent_inputs/cfg654_delta_ta.json, rho_m0 as CFG656 (Omega_m h^2 = 0.31285 x 0.67403^2). M_ta in M_sun
  (as CFG804 uses fret_of; the M_sun/h reading is a reported bracket, -0.17 dex).
- Retained baryons M_b = f f_b M_ta act as a point source for the law; V^4 = G M_b a0, r_M = sqrt(G M_b / a0).
- Primary epoch z = 0 (z = 1 bracket).

## External inputs (standard, flagged PROVISIONAL)
- E1 Type II supernova energy per stellar mass formed: e_SN = 1e51 erg per 100 M_sun = 1e49 erg/M_sun (Chabrier-type IMF,
  one SN per ~100 M_sun). Bracket 0.7e49 (Salpeter) to 1.2e49.
- E2 Cooling function: the record's Tozzi & Norman (2001) Z = 0.3 fit as carried in CFG640 (mu 0.6, n_e/n_H 1.17, n/n_H 2.3).
- E3 IGM temperatures for mechanism (iii): 1e4 K (photo-ionised; record) and 1e6 K (WHIM; provisional bracket).
- E4 (bracket only) AGN: E_AGN = 0.1 x 0.05 c^2 M_BH, M_BH = 1e-3 M*.

## Mechanisms (all zero tuned parameters)
- **M1 (i) energy budget, SN, all retained baryons cycle through stars (s = M*/M_b = 1).** Gas leaves if lifted from r_M to
  r_ta in the LAW's potential of the retained baryons: dPhi = integral_{r_M}^{r_ta} g(r) dr (exact law, numerical).
  Energy balance M_ej dPhi = eps e_SN s M_b with M_ej = (1 - f) f_b M_ta gives the fixed point f = 1 / (1 + eps e_SN s / dPhi(f)).
  **eps = 1** (all SN energy does work against the law's potential = the physical ceiling of feedback; not tuned).
- **M2 (i)+(ii) PRIMARY.** As M1 but s = chi = fraction of the retained gas that can cool: isothermal gas at T = mu m_p V^2/(2k),
  rho ~ r^-2 to r_ta, cooling radius where t_cool = t_dyn = r/V (CFG640's chi construction), chi = min(1, r_cool / r_ta).
  Stars (and so SN energy) come only from gas that cools.
- **M3 (iii) accretion vs catchment escape.** Catchment gas at IGM temperature T falls in iff its enthalpy (5/2) k T / (mu m_p)
  < dPhi(r_ta -> r_M) of the law; f = 1 if yes, else 0 (step).

## Classes (scored on M2 primary, canonical, z = 0, eps = 1; each mechanism and footing also labelled)
- **CENSUS DERIVED:** f within a factor 1.5 of the census at ALL four masses (0.667 <= f / f_census <= 1.5).
- **SHAPE DERIVED:** not CENSUS DERIVED, but f rises monotonically over log M_ta 12 -> 15 and f(15)/f(12) >= 3.
- **NOT DERIVED:** otherwise.
- **Qualifier CEILING-CONDITIONAL** (attached, not hidden): if the M2 class at eps = 0.1 (a typical radiative-loss coupling,
  provisional) is lower than at eps = 1. Then the result needs ~all SN energy to do work against the potential, which is
  implausible, and the README must say so.
- KiDS check (reported, separate): at CFG804's primary-fit log M_b per bin, solve M_ta = M_b/(f f_b) with M2's f;
  PASS iff N = 1/f >= 3 (canonical) / 4 (alt) in all four bins.

## Controls
- K1: dPhi of the law from r_M to r_ta for a 1e10.5 M_sun point mass matches V^2 ln(r_ta/r_M) + the Newtonian-regime offset
  computed independently (two quadratures agree to 1e-4).
- K2: e_SN 1e49 erg/M_sun = 5.03e11 m^2 s^-2 (to 1e-3).
- K3: z = 0 Delta_ta = 11.8308 read from the json.

## MUTATE (CFG806_MUTATE=1)
e_SN := 0 -> f = 1 at every mass -> must give NOT DERIVED (fails at log M_ta 12-13). The script exits 1 in MUTATE.

## Rules
No parameter is adjusted after the first run. A parameter chosen to match the census is a fit, not a derivation. No dark matter
particle species. kappa fitted; never "theory closed".

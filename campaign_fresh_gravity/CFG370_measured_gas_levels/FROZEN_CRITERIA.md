# CFG370 FROZEN CRITERIA: do MEASURED gas cooling times give the three retention levels? (no fit)

Committed alone, before any script. kappa = 1/2 FITTED and fixed. No dark-matter particle species: the cold MASS is still required
and is kept. No knob scans. Never "theory closed". Owner (2026-10-06, chat "Nobel Prize and neutrinos"): "resolve the unresolved
stuff", "please finish the last mile on this". The orchestrator holds CFG368; this is CFG370.

**Question.** CFG369 S2: a settling rate Gamma = 1/t_cool resolves CFG245's pincer, but S3 (a model gas, one radius) got the levels
wrong. The record's galaxy floor is 0.135 = e^-2 (L191, where n = 2 was a best fit). If the unsettled fraction is
e = exp(-tau/t_cool) evaluated with the MEASURED hot gas at each anchor's own measurement radius, do the three measured levels follow
with no fitted number? The levels are galaxies 0.14 (MW at 30 kpc, L191 anchor), groups 0.60 (cm03 def B), and clusters 0.576 (X-COP).

## Inputs (declared; each anchor at its own radius)
- **Milky Way, 30 kpc.** Hot halo: Miller & Bregman 2015 (ApJ 800, 14), beta = 0.50 (rho proportional to r^-1.5), normalised by
  their quoted M(<50 kpc) = 3.8e9 Msun (verbatim from the abstract). The abstract's "n_o r_c^{3beta} = 1.35 cm^-3 kpc^{3beta}" would
  imply about 1e12 Msun of hot gas within 250 kpc, inconsistent with their own quoted masses. It is not used (disclosed).
  T = 2.0e6 K (bracket 1.5e6-2.5e6 reported).
- **Groups.** The 20 Lovisari+2015 groups (real_research/data/lovisari2015_groups.tsv): kT measured, local gas density at R500
  under the isothermal rule rho_gas(R) = M_gas(<R)/(4 pi R^3), h70 as published. Statistic: the median e.
- **Clusters.** X-COP (the 12 with fgas FITS; MGAS at 1.0 R500 by interpolation; R500 from xcop_r500_ettori2019.json). Same
  isothermal local-density rule. kT = mu m_p G M500/(2 R500) (isothermal hydrostatic; declared). Statistic: the median e.
- **Cooling.** cm12's Tozzi & Norman Lambda(T), Z = 0.3, copied verbatim; t_cool = 3 n k T/(2 n_e n_H Lambda) in cm12's convention.
- **tau** = time since z = 2 (10.3 Gyr), PRIMARY. Also reported: since z = 1 (7.7 Gyr) and since z = 4 (12.2 Gyr).

## Test
e = exp(-tau/t_cool). PASS if ALL THREE land in their bands: MW 0.14 +- 0.05; group median 0.60 +- 0.15; cluster median
0.576 +- 0.15. Each is reported with its implied n = tau/t_cool. PARTIAL if two of three. FAIL if one or none.

## Controls
- C1: the copied Lambda/t_cool reproduce cm12's committed crossing (canonical R1 fhot1, 10^11.623) through cm12's ratio().
- C2: the isothermal local-density rule returns rho(R) = M/(4 pi R^3) exactly for a test r^-2 profile.
- MUTATE: cooling x 100. The verdict must change (rc 1).

Local compute only. No downloads. The literature inputs are quoted above.

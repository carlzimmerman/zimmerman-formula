# CFG445 FROZEN CRITERIA: group centrals x3. More centrals of log M_h >= 12.5 groups with outer HI rotation curves, against luminosity-matched field controls from the same source

Committed alone, before any script exists. At freezing time the only data looked at are: the column layout and row counts of the
WALLABY kinematic tables (DR1 109 unique galaxies, DR2 236 unique incl. all of DR1, high-res 25 with models; QFlag tallies), and
one 2MASS XSC row for column names. No residual, no class count, no cross-match count has been computed.
kappa = 1/2 is FITTED (never derived). Both a0 footings everywhere: canonical 9.3603e-11 and alt 1.1312e-10 m/s^2 (CFG4_common.A0).
No dark-matter particle is added; the framework's cold-fluid mass is still required in groups and clusters whatever this returns.
Owner approval: the 10-06 swing ("group centrals x3", CFG440-449 block), data fetches approved for this lane.

## Why (follows CFG393)
CFG393 (SPARC only) was NON-DISCRIMINATING: 15 centrals, Delta +0.022 +- 0.037, and as frozen it could not have returned SUPPORTED
even for a real 0.1 dex step (MUTATE: S 3.3 but dBIC +0.7 and the mass-matched control failed, field ~2 dex fainter). This lane
adds a second, homogeneous rotation-curve source and replaces the unmatched comparison by a luminosity-matched one inside each source.
Prediction tested (two-regime cold fluid): centrals of group-mass hosts sit ABOVE the RAR at g_bar < 10^-10.5 m/s^2, as a STEP at
log M_h = 12.5. CFG399: the retention step follows group membership, not temperature, so host mass/membership is the right axis.

## Sources (declared; anything else is excluded and listed in the README)
1. SPARC (as CFG393): CFG4_common.load_sparc(), Q <= 2, Upsilon_disk 0.5, Upsilon_bul 0.7, classes from CFG393's committed
   cfg393_match_table.csv (read-only; identical rules). Luminosity variable: log L[3.6] (Lelli+2016 table).
2. WALLABY pilot kinematic models (Deg et al. 2022 PDR1; Murugeshan et al. 2024 PDR2), CADC TAP
   https://ws-uv.canfar.net/youcat table cirada.Wallaby_dr2_kinematic_catalogue (contains all DR1 galaxies). Per ring: Rad (arcsec),
   Vrot_model, e_Vrot_model; Rad_SD, SD_FO_model (face-on HI surface density, Msun/pc^2). HI masses for control C-HI from
   cirada.Wallaby_dr2_source_catalogue (log_m_hi at dist_h).
   - Duplicates across team releases: the latest team release (highest TR number) is used.
   - Eligibility: QFlag_model <= 1; Inc_model >= 30 deg. The high-res catalogue is NOT used (homogeneity), declared.
   Excluded sources, declared now: Di Teodoro+2021/2023 massive discs (curves only figure-digitised, no per-radius baryons, no
   same-source field controls); MIGHTEE-HI resolved curves (no public sample; record CFG279); THINGS/HALOGAS (overlap SPARC);
   Ponomareva+2016 (no machine-readable curves+mass models located); BIG-SPARC (announced, not released).

## WALLABY baryonic model (declared)
- Distance D: the matched group catalogue's tabulated galaxy distance (KT2017 table3 Dist, else T15 table5 Dist). Radii
  R = Rad * D. (g_bar from SD and from L/R_d^2 is distance-independent; g_obs = V^2/R scales as 1/D.)
- Gas: Sigma_gas = 1.33 * SD_FO_model (helium), zero beyond the last SD ring, linearly interpolated, held at the first ring's
  value inside it. Radial force from a razor-thin axisymmetric disc by ring summation (complete elliptic integrals, 600 sub-rings,
  vertical softening 0.1 kpc); g_gas may be negative (central holes) and enters g_bar with its sign.
- Stars: 2MASS XSC (VizieR VII/233/xsc, nearest within 20 arcsec of the WALLABY position): K.ext total magnitude, Kr.eff
  half-light radius. L_K = 10^(-0.4 (K.ext - 5 log10 D[Mpc] - 25 - 3.28)) Lsun; M* = Upsilon_K L_K with Upsilon_K = 0.6
  (the K-band equivalent of SPARC's 0.5 at 3.6 um, McGaugh & Schombert 2014); a single thin exponential disc with
  R_d = D * Kr.eff / 1.678 (Freeman 1970 formula). No bulge, no Galactic extinction correction (declared; A_K < ~0.1 mag).
  A WALLABY galaxy without an XSC match is excluded (not field).
- Luminosity variable for matching: log L_K (this XSC route).
- Point error s_i = sqrt[(0.8686 e_V/V)^2 + 0.01^2] dex with e_V = max(e_Vrot_model, 2 km/s) (the inclination error is common
  to all rings and excluded, as in SPARC's eV).

## Cross-match and classes (CFG393's rules, applied to WALLABY positions)
Nearest catalogue galaxy within 60 arcsec, KT2017 table3 first, else T15 table5; a second candidate within 60 arcsec -> AMBIGUOUS,
excluded; unmatched -> UNCLASSIFIED, excluded (never field). Host mass = luminosity-based group mass (KT2017 logMK, T15 log Mlum).
CENTRAL GC: PGC == group PGC1 and log M_h >= 12.5. SATELLITE: PGC != PGC1 and log M_h >= 12.5. FIELD F: log M_h < 12.5.
Galaxy enters the scoring sample if it has >= 3 rings with g_bar < 10^-10.5 m/s^2.

## Residual (per point, per galaxy; CFG393's)
r = log10 g_obs - log10[g_bar nu_mono(g_bar/a0)], points with 0 < g_bar < 10^-10.5 m/s^2; R_g = weighted mean of r, weights 1/s_i^2.

## Primary statistic: luminosity-matched Delta (frozen)
For each central i (source s): its controls = all FIELD galaxies of the SAME source with |log L - log L_i| <= 0.2 dex.
d_i = R_i - median(R of its controls). A central with no control within 0.2 dex is dropped from the primary (count reported).
Delta_LM = median_i d_i over both sources pooled. sigma = SD of 5,000 bootstrap Delta_LM (resample centrals within source and field
galaxies within source; recompute the matching each time; seed 445). S = Delta_LM / sigma.
Secondary (reported): CFG393's unmatched pooled Delta = median(GC) - median(F), and per-source Delta_LM.

## Step vs slope (frozen)
On GC + F (satellites excluded), both sources: linear R = a_s + b x; step R = a_s + d H(x - 12.5), x = log M_h, a_s a per-source
intercept (k = n_src + 1 for both). OLS, BIC = N ln(RSS/N) + k ln N. dBIC = BIC_linear - BIC_step (> 0 favours the step).

## Verdict rules (both footings; the weaker is reported)
- UNDERPOWERED -> NON-DISCRIMINATING if N(GC with controls) < 5 or N(F) < 20.
- TWO-REGIME SUPPORTED: Delta_LM > +0.05 dex AND S > 3 AND dBIC > 2.
- NOT SUPPORTED: Delta_LM + 2 sigma < 0.05 dex.
- otherwise NON-DISCRIMINATING.
- Wording: SUPPORTED would be consistent with the two-regime picture, not unique to it (LCDM centrals also differ from field).
  Nothing here says the data favour the framework over LCDM.

## POWER DRY-RUN (frozen; run on the selection BEFORE any real residual is computed; committed before the scoring run)
Mock R_g ~ Normal(0, sigma_tot,s) per galaxy, sigma_tot = 0.14 dex for SPARC (CFG393's field robust SD) and 0.18 dex for WALLABY
(declared conservative, marginally resolved); host masses, classes, luminosities and matching are the REAL selection's. Inject +0.10
dex into every central; run the full primary + dBIC + verdict pipeline; 1,000 mocks (seed 4450), canonical selection.
- POWER = fraction of mocks returning TWO-REGIME SUPPORTED. POWERED if >= 0.80; MARGINAL if 0.50-0.80; UNDERPOWERED if < 0.50.
- Also reported: the injected step giving 80% power (scan 0.05-0.40 dex) and N(GC) needed at 0.10 dex (scaled by resampling
  centrals with replacement to 1x-6x their number).
- The sample is "all eligible galaxies of both sources"; no source can be added after the dry run. If UNDERPOWERED, that is stated
  in the dry-run output and README before scoring, and the scored verdict can at best be NON-DISCRIMINATING/NOT SUPPORTED in
  practice. Goal stated by the task: >= 45 centrals (3x CFG393).

## Controls
- C1 (load-bearing): load_sparc() 175 galaxies, 163 with Q <= 2.
- C-HI (load-bearing): log10 of 2 pi integral(SD_FO R dR) (no helium, at dist_h) vs source-catalogue log_m_hi: median |diff| <= 0.15
  dex over WALLABY scoring galaxies (checks SD units and the Rad unit).
- C-thin (load-bearing): the ring-sum force code reproduces the Freeman exponential-disc V^2 within 2% at 2-6 R_d.
- C3 (load-bearing, identity): every R_g used equals R_g recomputed from source to 1e-9 dex.
- C-SPARC (load-bearing): the SPARC GC/F lists equal CFG393's (15 GC / 91 F on canonical).
- C5 (reported): label-permutation p for |Delta_LM| (shuffle GC/F labels within source, 2,000 shuffles).
- Sensitivities (reported, no verdict weight): Upsilon_K 0.45 and 0.80; threshold 12.3/12.7; WALLABY only; matching window 0.3 dex;
  KT2017 dynamical masses.
- MUTATE (MUTATE=1, outputs *_MUTATE): +0.1 dex to every central's real R_g. Required: Delta_LM rises by 0.100 +- 0.005; the run
  exits 1 (C3 fails by design) and reports whether the verdict reaches SUPPORTED (it must, if the dry run said POWERED; if it
  does not, that is reported as the power failure it is).

## Caveats declared now
Group masses are model-dependent (KT2017 and T15 recipes differ). WALLABY fields are cluster/group-centred (Hydra, Norma, NGC 4636,
NGC 5044, NGC 4808, Vela), so WALLABY's "field" is not a random field. WALLABY models are marginally resolved (beam 30 arcsec) and
coarse (half-beam rings): outer rings are correlated. The stellar model (XSC K, single exponential, Upsilon_K 0.6) is cruder than
SPARC's; it is shared by centrals and their controls inside the source, which is why the comparison is matched within source.

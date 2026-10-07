# CFG392: FROZEN CRITERIA (old tidal-dwarf candidates selected by metallicity)

Written 2026-10-06, before any script, fetch of abundance tables, or result number exists in this lane.
Only catalogue metadata (VizieR/CDS ReadMe column lists) was read before freezing; no abundance value was read.
Departures after this commit are disclosed in README.md; failed controls are kept as they fall.

Standing: kappa = 1/2 is FITTED. Both a0 footings run everywhere: canonical 9.3603e-11, alt 1.1312e-10 m/s^2.
No dark-matter particle is added; the framework's cold-fluid mass is still required wherever the law needs it.

## 1. Hypotheses

- **H_settle (settling working model).** An old tidal dwarf (TDG) formed from pre-enriched disc gas has a phantom
  target but no catchment for the cold fluid, so it is Newtonian: g_obs ~ g_bar. On the RAR it sits below the law by
  -log10 nu_mono(g_bar/a0) at each point (about -0.3 dex or more negative at low acceleration).
- **H_MOND (modified gravity, no cold component needed).** TDGs sit ON the RAR: residual ~ 0, like other dwarfs.
- Proxy: a gas-rich dwarf that is metal-rich for its stellar mass is an old-TDG CANDIDATE. This is a proxy only;
  metal-rich dwarfs can be ordinary galaxies (low gas fraction, closed-box evolution, calibration offsets, distance
  errors). A null in the flagged set does not by itself show TDGs are on the RAR.

## 2. Sample

- SPARC (real_research/data/SPARC_Lelli2016c.mrt + sparc_data/*_rotmod.dat) via CFG4_common.load_sparc().
- Cuts: Q < 3; Inc >= 30 deg; dwarf cut M_b = 0.5 L36 + 1.33 M_HI < 1e10 Msun (1e9 units in the table).
- No LITTLE THINGS rotation curves are fetched (only those inside SPARC enter).

## 3. Metallicities (12+log(O/H)), one source per galaxy, by this priority

1. Berg et al. 2012, ApJ 754, 98 (direct-method), IF its table is retrievable from the arXiv source; else skipped.
2. van Zee & Haynes 2006, ApJ 636, 214 (VizieR J/ApJ/636/214), table1 (global O/H), then table6.
3. Hunter et al. 2012 LITTLE THINGS (J/AJ/144/134) table1, MEASURED values only: entries flagged '*' (estimated
   empirically from M_B) are EXCLUDED, since a luminosity-based estimate would make the flag circular.
4. Pilyugin et al. 2014 (J/AJ/147/131) table2: characteristic abundance at R = 0.4 R25,
   O/H(0.4) = [O/H]_0 + 0.4 C[O/H]1.
   (Further compilations, e.g. Lee et al. 2006, may be added only before the RAR residuals are computed, and are
   disclosed as departures.)
- Matching: normalized names (upper case, spaces/hyphens/leading zeros removed, e.g. 'UGC 5750' == 'UGC05750'),
  plus an explicit hand alias table (e.g. 'DDO 154' -> SPARC 'DDO154', NGC/UGC cross names) written in the script and
  printed. The full match table (SPARC name, source, catalogue name, O/H, error) is written to match_table.csv.

## 4. Mass-metallicity relation (declared before any RAR residual is computed)

- M_star = 0.5 L36 (same Upsilon as the RAR). Own-sample OLS fit of 12+log(O/H) on log10 M_star over the analysis
  sample (matched galaxies passing all cuts). One pass, no clipping. Theil-Sen fit reported as a secondary.
- Flag (old-TDG candidate): MZR residual >= +0.40 dex (PRIMARY). Also reported: >= +0.30 dex (secondary).

## 5. Statistic

- Points: g_obs = Vobs^2/R; g_bar = (Vgas|Vgas| + 0.5 Vdisk|Vdisk| + 0.7 Vbul|Vbul|)/R, g_bar > 0, Vobs > 0.
- Residual r_i = log10 g_obs - log10(nu_mono(g_bar/a0) g_bar). Upsilon_disk = 0.5 fixed (bulge 0.7).
- Per-point sigma_i = (2/ln10) eV/Vobs, plus 0.05 dex in quadrature. Per-galaxy inverse-variance weighted mean.
- PRIMARY points: g_bar < 10^-10.5 m/s^2; a galaxy needs >= 3 such points to enter the primary statistic.
  SECONDARY: all points.
- Delta = median(flagged residuals) - median(unflagged residuals); sigma = std of 20,000 bootstrap resamples over
  galaxies (each group resampled with replacement; seed 392).
- Settling expectation per flagged galaxy: E_i = - weighted mean of log10 nu_mono(g_bar/a0) at its primary points;
  the predicted Delta under H_settle = median(E_flagged) (+ median unflagged residual - itself, i.e. relative to 0).

## 6. Verdict rules (per footing, nu_mono, primary points, 0.40 dex flag)

- SETTLING-TDG SUPPORTED: Delta < -0.15 at > 3 sigma, i.e. Delta + 3 sigma < -0.15.
- DISFAVOURED: Delta - 2 sigma > -0.15.
- NON-DISCRIMINATING: otherwise, and always if N_flagged < 5.
- Overall verdict = the common verdict if both footings agree; otherwise NON-DISCRIMINATING (both reported).
- The 0.30 dex flag, all-points, and P2 kernel rows are reported but do not set the verdict.

## 7. Controls and MUTATE

- C1 (load-bearing): load_sparc returns 175 galaxies; footings equal 9.3603e-11 / 1.1312e-10.
- C2 (load-bearing): match audit - no SPARC galaxy matched to two different entries of the chosen source, no
  catalogue entry matched to two SPARC galaxies; every match printed.
- C3 (load-bearing): g_obs used is the observed Vobs^2/R (max |difference| = 0). MUTATE=1 replaces the flagged
  galaxies' g_obs by g_bar (Newtonian) inside the statistic; C3 then fails and the run exits 1. The MUTATE run must
  also return SUPPORTED on both footings (recorded; if it does not, the test lacks power and this is reported).
- C4 (reported, not load-bearing): sanity - median per-galaxy residual of the whole dwarf sample (all points,
  canonical) within |0.15| dex.
- C5 (reported): Newtonian-injection power check run inside the main script (flagged g_obs -> g_bar on a copy):
  does it return SUPPORTED? This says whether the frozen test can see the settling signal at this N.
- C6 (reported): confounders - flagged vs unflagged medians of gas fraction, log M_star, distance-method flag fD,
  inclination; Spearman rho between MZR residual and RAR residual over all analysis galaxies.
- Outputs: cfg392_tdg_metallicity.out / _results.json; MUTATE writes *_MUTATE.out / *_MUTATE_results.json.

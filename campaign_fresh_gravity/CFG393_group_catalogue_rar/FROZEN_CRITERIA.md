# CFG393 FROZEN CRITERIA: group-catalogue RAR. Do SPARC centrals of group-mass hosts sit above the RAR, as a STEP in host mass?

Committed alone, before any script exists and before any residual, class count or match count has been computed.
kappa = 1/2 is FITTED (never derived). Both a0 footings are run everywhere: canonical 9.3603e-11, alt 1.1312e-10 m/s^2
(read from CFG4_common.A0). No dark-matter particle is added; the framework's "cold fluid" mass is still required in clusters
and groups whatever this test returns. Owner approval: the 10-06 CFG390-399 swing (LEDGER row "CFG393 group-catalogue RAR";
the data batch approved there includes "a group catalogue").

## Why
sonnet55_push/cold_mass cm08-cm10 read a "two-regime" cold fluid: retained fraction ~0.13 of the cosmic share in galaxies,
~0.6 in groups/clusters, with a step at host M200 ~ 1e12-1e13 Msun (cm09: the step follows HOST status, not the galaxy's own
sigma; measured on early types). Where the fluid is scarce it settles onto the law's phantom target (tight RAR); where it is
abundant the excess is halo-shaped. Out-of-sample prediction for late types: SPARC galaxies that are CENTRALS of group-mass
hosts sit ABOVE the RAR at large radius and/or scatter more than field galaxies, as a STEP in host mass, not a smooth slope.
The external-field effect predicts the OPPOSITE sign for satellites (lower outer residuals in denser environments).

## Data (to be fetched; every fetch logged in FETCH_LOG.md with URL, date, bytes, sha256)
- Kourkchi & Tully 2017 (ApJ 843, 16; VizieR J/ApJ/843/16): table3 (galaxies: PGC, RA, Dec, group PGC1) and table2 (groups:
  PGC1, Nm, logMK = luminosity-based mass, logMd = dynamical mass, Dist). Coverage: V < 3500 km/s.
- Tully 2015 (AJ 149, 171; VizieR J/AJ/149/171): table5 (2MRS K < 11.75 galaxies: PGC, positions, Nest, PGC1) and table3
  (groups: Nest, PGC1, Nmb, Mlum). Coverage to ~10,000 km/s, bright galaxies only.
- SPARC positions: VizieR J/AJ/152/157 table1 (_RAJ2000/_DEJ2000, Name, Dist, Qual). Rotation curves and masses from the
  repo loader campaign_fresh_gravity/CFG4_common.py load_sparc() (175 rotmod files + Lelli+2016 master table). Read-only.

## Cross-match (declared)
- Positional: SPARC position vs catalogue galaxy position, nearest neighbour within 60 arcsec. Accepted matches are written to
  a committed match table (SPARC name, PGC, separation, catalogue, group id/PGC1, group mass, Nm). A second candidate within
  60 arcsec is flagged AMBIGUOUS and the galaxy excluded.
- Priority: Kourkchi-Tully 2017 match first (deeper, includes faint members); else Tully 2015; else UNCLASSIFIED (excluded --
  an unmatched galaxy is NOT field).
- If the positional route fails for a galaxy whose name contains an explicit PGC/UGC/NGC/IC number that the catalogue cannot
  resolve, it stays UNCLASSIFIED. No hand assignments.

## Classes (declared before scoring)
Sample: SPARC Q <= 2, matched, >= 3 rotation-curve points with g_bar < 10^-10.5 m/s^2 (Upsilon_disk 0.5, Upsilon_bul 0.7).
Host mass M_h = the catalogue's LUMINOSITY-based group mass (KT2017 logMK; T15 log10 Mlum), threshold log M_h = 12.5.
- CENTRAL (GC): PGC == the group's PGC1 (brightest member) AND log M_h >= 12.5.
- SATELLITE (SAT): PGC != PGC1 AND log M_h >= 12.5.
- FIELD (F): log M_h < 12.5 (singletons and small groups, central or not).
Sensitivities, reported, no verdict weight unless stated: thresholds 12.3 and 12.7; KT2017 dynamical mass logMd (where given);
KT2017-only and T15-only subsamples.

## Residual (per point, then per galaxy)
g_obs = Vobs^2/R; g_bar = (Vgas|Vgas| + 0.5 Vdisk^2 + 0.7 Vbul^2)/R; r = log10 g_obs - log10[g_bar nu_mono(g_bar/a0)],
nu_mono = CFG4_common.nu_mono (FP1's committed kernel). Points with g_bar < 10^-10.5 m/s^2 only (the "large radius" regime).
Point error s_i = sqrt[(0.8686 eV/Vobs)^2 + 0.01^2] dex. Per-galaxy residual R_g = weighted mean of r with weights 1/s_i^2.

## Statistics (frozen)
(a) Delta = median(R_g | GC) - median(R_g | F). sigma_Delta = SD of 20,000 bootstrap Deltas (resample within each class,
    seed 393). Significance S = Delta / sigma_Delta.
(b) Scatter ratio Q_s = robust SD(R_g | GC) / robust SD(R_g | F), robust SD = 1.4826 MAD; bootstrap 2.5-97.5% interval.
(c) STEP vs SLOPE on GC + F (satellites excluded): x = log M_h. Linear R = a + b x (k = 2); step R = a + d H(x - 12.5) (k = 2);
    constant (k = 1). OLS, BIC = N ln(RSS/N) + k ln N. dBIC = BIC_linear - BIC_step (> 0 favours the step).
(d) Satellites, cross-check only: Delta_sat = median(R_g | SAT) - median(R_g | F) with bootstrap. EFE predicts Delta_sat < 0.
    The record's directional-EFE test gave +2.95 once and WALLABY -1.70; both are quoted, never averaged. No verdict weight.

## Verdict rules (both footings; if they differ, the weaker verdict is reported)
- UNDERPOWERED -> NON-DISCRIMINATING if N(GC) < 5 or N(F) < 20.
- TWO-REGIME SUPPORTED: Delta > +0.05 dex AND S > 3 AND dBIC > 2.
- NOT SUPPORTED: Delta + 2 sigma_Delta < 0.05 dex.
- otherwise NON-DISCRIMINATING.
- Mass-confound downgrade (declared): centrals of group hosts are massive galaxies. Mass-matched control M: each GC galaxy is
  paired with its 3 nearest FIELD galaxies in log L[3.6] (with replacement); Delta_M = median(GC) - median(matched F),
  bootstrap. A SUPPORTED primary is downgraded to NON-DISCRIMINATING if Delta_M < 0.05 or Delta_M/sigma_M < 2.
- Scatter: if (a) is not SUPPORTED but Q_s > 1.5 with its 2.5% bound > 1, report "SCATTER-ONLY SIGNAL" (no SUPPORTED).
- Wording: nothing here says the data favour the framework over LCDM. In LCDM, centrals of group halos also differ from field
  galaxies; a SUPPORTED reading is consistent with the two-regime picture, not unique to it.

## Controls
- C1 (load-bearing): load_sparc() gives 175 galaxies and 163 with Q <= 2.
- C2 (load-bearing): cross-match sanity on Ursa Major. Of SPARC galaxies with f_D = 4 (UMa cluster distance) that match KT2017,
  >= 70% share a single group PGC1.
- C3 (load-bearing, identity): every per-galaxy R_g used in (a)-(c) equals R_g recomputed from the rotmod files to 1e-9 dex.
- C4 (reported): distance-method control. (a) repeated on f_D != 1 only (no Hubble-flow distances).
- C5 (reported): label-permutation p-value for |Delta| (5,000 shuffles of GC/F labels).
- MUTATE (MUTATE=1, outputs *_MUTATE): add +0.1 dex to every GC galaxy's R_g. Required: Delta rises by 0.100 +- 0.005 and the
  verdict does not move down the ladder (NOT < NON-DISCRIMINATING < SUPPORTED); C3 fails, so the run exits 1.

## Caveats declared now
Group masses are model-dependent (luminosity-to-mass recipes; KT2017 and T15 use different ones and are not pooled across
thresholds without saying so). SPARC is not a complete or environment-selected sample. KT2017 covers only V < 3500 km/s and T15
only K < 11.75 galaxies, so the classified set will be biased toward nearby and bright galaxies. Distances (SPARC's) set g_bar and
g_obs; Hubble-flow distances correlate with environment (C4).

# CFG628 FROZEN CRITERIA -- FRB foreground-halo gas partition vs the census placement R4 (CFG627 Spec A)

Committed alone, before any script of this lane exists and before any framework prediction of this lane is computed.
Date 2026-10-11. Lane folder: `campaign_fresh_gravity/CFG628_frb_halo_partition/`. All other lane folders are read only.
No PM runs. One process, < 1 GB, nice 10. The running 1024^3 CFG596 job and the lane drivers are not touched.

kappa = 1/2 is FITTED. Footings 9.3603e-11 (canonical) / 1.1312e-10 (alt), scored separately, never pooled; a0 flat.
"Cold energy" = candidate B's cold component; its MASS is still required (no particle). Not "theory closed"; nothing here
says the data favour the framework. No LCDM or standard-MOND quantity is a yardstick in any verdict.

## Data (arXiv LaTeX sources downloaded with the owner's approval, outside the repo; nothing else is downloaded)

`_external_data/frb_tables/`:
- 2402.00505 `cobra_dr1.tex`: Khrykin+24 (FLIMFLAM DR1, ApJ 973, 151). Table 1 (`tbl:tab_dr1`, 8 sightlines: RA, Dec,
  z, DM_FRB), Table 3 (`tbl:tab_dms`, per-sightline DM_igm^argo (f_igm = 1), DM_halos (f_gas = 1, r_max = r200),
  DM_host^halo (f_gas = 1), <log M_host^halo>, DM_MW, DM_FRB), Table 4 (priors), Table 5 (`tbl:tab_results_priors`,
  published posteriors).
- 2408.12864 `main.tex` + `tables/`: FLIMFLAM DR1 data paper (fields, selection). No per-galaxy catalogue in the source;
  the text says the catalogue will be released on Zenodo after refereeing.
- 2409.16952 `main.tex`: Connor+25. Per-FRB DM_obs, DM_ex, z, DM_MW (68 rows, two tables). Its f_IGM / f_X partition is
  calibrated on IllustrisTNG300 bivariate log-normal PDFs (CONTEXT only).
- 2408.02083 `Tables/tab_frb.tex`: Shannon+24 CRAFT/ICS localized FRBs (DM, DM_MW (NE2001), z).

Transcription: a parser script (`cfg628_transcribe.py`) reads the LaTeX directly and writes CSVs in the lane folder; every
CSV row names its source table. Spot checks are printed (C3 below).

## Seen before this freeze (stated)

- The CFG627 README (Spec A, the ranking, the expectation "probably NON-DIAGNOSTIC").
- The published FLIMFLAM DR1 posteriors: f_igm = 0.59 (+0.11/-0.10), f_gas = 0.55 (+0.26/-0.29), <DM_host^unk> = 69
  (+28/-19) (fiducial), and the Limited-f_gas values 0.63 / 0.44 (+0.18/-0.24).
- Connor+25: f_IGM = 0.76 (+0.10/-0.11), TNG-scaffolded.
- The Table 3 per-sightline numbers, and the fact that NO source holds a per-halo foreground catalogue (impact parameters,
  stellar masses). The papers' halo masses come from CIGALE stellar masses through the Moster+13 SHMR (inherited).
- Rough mental arithmetic only (no script): with the census floor f_ret = 0.10 the framework puts at most ~10% of a galaxy
  halo's catchment baryons in its halo, and f_ret = 1 puts ~all of them; with sigma(f_gas) ~ 0.27 neither is expected to sit
  3 sigma from 0.55. EXPECTED OUTCOME, STATED NOW: NON-DIAGNOSTIC, and the MUTATE control probably NOT detected (no teeth).

## 1. What cannot be built from the data in hand (declared now)

The Spec A primary statistic (per-halo framework DM_halo,i integrated along each sightline from each foreground system's
own impact parameter and stellar mass) needs the per-halo foreground catalogue. It is NOT in the downloaded sources.
The primary per-halo statistic is therefore declared NOT EVALUABLE in this lane; the files needed are listed in the README
(source, size if known), nothing further is downloaded. The Spec A clause "a failure is attributed to the census unless it
survives replacing f_ret with each system's own measured gas" is likewise NOT EVALUABLE (no per-system gas).

What IS built (the fallback, frozen here): the measurement is rebuilt from the per-sightline Table 3 numbers with the
FLIMFLAM likelihood but WITHOUT the f_d prior (that prior converts f_gas to f_cgm with the Aemulus LCDM halo mass function,
an inherited ingredient). The framework prediction is converted into the measurement's f_gas units per halo mass (sec. 3)
and compared as an interval.

## 2. The measurement (rebuilt; no framework input)

Per sightline i (Table 3 values, transcribed):
  DM_model,i = DM_MW,i + f_igm * DM_argo,i + f_gas * DM_halos,i + (f_gas * DM_hh,i + mu) / (1 + z_i)
  sigma_i^2  = (f_igm s_argo,i)^2 + (f_gas s_halos,i)^2 + (f_gas s_hh,i)^2 + sigma_MW^2 + sigma_host(mu)^2
  sigma_MW = 15; sigma_host^2 = (exp(s*^2) - 1) exp(2 ln mu + s*^2), s* = 1.23 (James+22a, inherited, as Khrykin+24).
  Gaussian likelihood in DM_FRB with the normalisation term (ln sigma_i) included because sigma_i depends on parameters.
  (Declared reading of Khrykin+24 eq. like: the paper writes "proportional to"; including ln sigma_i is the correct
  Gaussian; the variant without it is reported as C1-b.)
Priors (flat, Khrykin+24 Table 4 ranges): f_igm in (0, 1], f_gas in (0, 1], ln mu in [0, 6]. Grid: 201 x 201 x 121.
Measured f_halo := the marginal posterior of f_gas: median m, p16, p84; sigma_+ = p84 - m, sigma_- = m - p16,
sigma(f_halo) = (p84 - p16)/2. Same for f_igm.

## 3. The framework prediction in the measurement's units (per halo mass)

Inputs per halo of mass M_h (the papers' halo mass, INHERITED: CIGALE M* -> Moster+13 SHMR; M200c at z = 0.20, the paper's
median redshift; h = 0.673, Omega_m = 0.315 for r200, the paper's background, INHERITED):
- M_ta := M_h (primary) and M_ta := 2 M_h (bracket; the framework's turnaround catchment is larger than a 200c mass; both
  enter the prediction interval).
- f_ret = CFG416/CFG515 `fret_of(log10(M_ta h))` with h = 0.674 (imported read-only from `cfg515_lib.py`; FRETX = 1).
- Retained baryons M_b,now = f_ret * 0.157 * M_ta (CFG416's constants, as CFG515).
- Stars M* = Moster+13 at z = 0.20 (the inverse of the papers' own mapping; parameters recalled, PROVISIONAL, INHERITED).
- Ionized halo gas, two readings, both enter the interval:
  B-lo: M_ion = max(0, M_b,now - M*) (stars subtracted, cold ISM gas taken as zero -> still an upper bound on hot gas);
  B-hi: M_ion = M_b,now (every retained baryon counted as ionized halo gas; the census maximum).
- Profile: isothermal gas, hydrostatic in the law's potential g = g_N nu_mono(g_N / a0), g_N = G M_b,now / r^2 (point mass;
  nu_mono copied verbatim from `CFG596_lean_pm_1024/cfg596_pm.py`), T at the law's virial value
  sigma^2 = kT/(mu m_p) = V_f^2 / 2, V_f^4 = G M_b,now a0 (singular-isothermal convention); normalised to M_ion inside the
  census edge r_edge = r_M / ln(1 + f_ret f_b/(1 - f_b)), r_M = sqrt(G M_b,now / a0), f_b = 0.02237/0.14237 (the CFG515
  edge; `cfg515_lib.ln_fac`). Reported only: sigma^2 = (2/9) V_f^2 and V_f^2 (temperature bracket; E2 only).
- Conversion into the measurement's f_gas (the template is mNFW, f_gas (Omega_b/Omega_m) M_h inside r200, Omega_b/Omega_m =
  0.046/0.315, Khrykin+24):
  E1 (expected total, catalogue complete to r_edge): f_eq = M_ion / ((0.046/0.315) M_h).
  E2 (only gas projected inside the r200 cylinder counts, as the paper's template): f_eq = M_ion,cyl(<r200) / ((0.046/0.315) M_h).
  E1 is the upper and E2 the lower conversion; both enter the interval.
- Mass grid: log10 M_h in [11.0, 13.0], step 0.05 (Khrykin+24: the intersected halos are "mostly 10^11-10^12.5" with
  "several" groups at ~10^13). Reported only: 10.0-11.0 and 13.0-13.5.
- PREDICTION INTERVAL P = [min, max] of f_eq over the grid, M_ta in {M_h, 2 M_h}, B-lo/B-hi, E1/E2; per footing
  (footings enter E2 only, through r_edge and V_f). The interval is wide on purpose: the halo-mass weights of the DR1 sample
  are not public. Values above 1 are kept (not clipped).

f_IGM side: framework f_IGM,pred = f_d - f_halo,cos with f_d in [0.75, 0.95] (Khrykin+24's own flat f_d prior; stellar mass
density, INHERITED) and the framework's cosmic ionized halo fraction f_halo,cos in [0, 0.15] (declared bracket; a sharper
value needs a halo mass function, INHERITED and not used) -> P_IGM = [0.60, 0.95]. The measured f_igm uses ARGO
reconstructions (LCDM N-body calibrated on hydro sims, INHERITED). The f_IGM comparison is labelled CONTEXT.

## 4. Statistic, power gate, verdict bins (both footings, never pooled)

- Z_near = signed distance from m to the NEAREST edge of P in units of the posterior half-width on that side (sigma_- if
  P lies below m, sigma_+ if above); 0 if m lies inside P. Z_far (to the far edge) is reported.
- POWER GATE: if sigma(f_halo) > 0.25 (rebuilt posterior), the lane is NON-DIAGNOSTIC and makes no statement; Z is still
  printed, labelled non-diagnostic. The published sigma (0.275) is reported beside it.
- Bins on |Z_near| (f_halo): CONSISTENT < 2; TENSION 2-3; EXCLUDED >= 3. If |Z_near| < 2 but |Z_far| >= 2, the label is
  "CONSISTENT (interval-limited)".
- f_IGM: the same Z on P_IGM, labelled CONTEXT; it changes the verdict only if f_halo passes the power gate and f_IGM is
  EXCLUDED (then the verdict reads "EXCLUDED on context inputs").

## 5. MUTATE control (the teeth)

CFG628_MUTATE=1: f_ret = 1 for every system (all catchment baryons retained; every other setting identical). P_mut is
computed the same way. The control PASSES only if P_mut is EXCLUDED (|Z_near| >= 3) by the rebuilt measurement. If it is
not, the README and the report say plainly: THE TEST HAS NO TEETH at this sample's power. Also reported: the posterior
probability Pr(f_gas >= min P_mut), and the sightline number at which sigma(f_halo) would reach the gate and at which
P_mut would be excluded, scaling sigma as N^-1/2 (forecast, no verdict weight).

## 6. Controls

- C1 (identity, partial): the rebuilt flat-prior fit vs Khrykin+24 fiducial. C1-a: as sec. 2. C1-b: likelihood without the
  ln sigma_i term. C1-c: an approximate f_d prior f_igm + (0.20/0.55) f_gas in [0.75, 0.95] (the paper's quoted f_cgm,ff =
  0.20 at f_gas = 0.55, linear; f_icm and f_cgm,other ignored). Reported with differences; label "reproduced" if the f_igm
  and f_gas medians are within 0.10 of the published, "not reproduced" otherwise. No verdict weight; a non-reproduction is
  stated.
- C2 (synthetic recovery): 300 mocks drawn from the sec. 2 model at truth (f_igm, f_gas, mu) = (0.6, 0.5, 69) with the
  Table 3 inputs; refit; coverage of the 68% f_gas interval in [0.55, 0.81] = PASS.
- C3 (transcription): DM_FRB in Table 1 vs Table 3 vs CRAFT tab_frb vs Connor DM_obs, and z in all four; differences
  > 1 pc cm^-3 or > 0.001 in z are listed (not corrected). Hand spot-check of three Table 3 rows against the LaTeX text.
- K1 (kernel): nu_mono(y) equals 1/(1 - exp(-sqrt y)) to < 1e-6 for y < 1 (the edge and the halo gas sit at y << 1).
- K2 (profile): numeric M_ion(<r_edge) = M_ion to 1e-6; numeric phantom root vs the closed-form CFG515 edge to < 1e-3.

## 7. Inherited ingredients (flagged; none is a yardstick)

Halo masses (CIGALE M* -> Moster+13 SHMR, LCDM abundance matching), the M200c / r200 definition and the Planck-like
background, Moster+13 M* for B-lo, the mNFW profile and r_max = r200 inside the measurement's template and in Table 3's
DM_halos and DM_host^halo, the ARGO density reconstructions (LCDM) in DM_argo, NE2001 + the 40 +- 15 MW halo DM, the
log-normal host with s* = 1.23 (James+22a), the f_d prior (Madau-Dickinson stellar mass density), Connor+25's TNG300
calibration (CONTEXT only), and the f_halo,cos bracket in place of a halo mass function.

## 8. Outputs

`cfg628_transcribe.py` (+ CSVs), `cfg628_partition.py` -> `cfg628_partition.out/.json`; `CFG628_MUTATE=1` ->
`cfg628_partition_MUTATE.out/.json`. README with the verdict per footing, the power gate, the MUTATE result, the inherited
list and the data that would make the primary statistic evaluable.

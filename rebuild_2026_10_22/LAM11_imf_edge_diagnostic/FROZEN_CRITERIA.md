# LAM11_imf_edge_diagnostic: FROZEN CRITERIA, committed alone before any fit

κ = ½ FITTED and held fixed. This lane grades no law and uses no footing: it diagnoses a fit. No ΛCDM input. The cold
sector stays retired. Nothing here says the data favour the framework. Not theory closed.

**Owner's yes, 2026-11-04:** "Yes, diagnose it". The option was a small diagnostic lane on about 100 real sums, with no
download: refit with each IMF-line region (Na I, CaT, TiO) masked in turn, and with the red end cut, to find which feature
drives the fits to Γb 0.3. The lane then reports whether α-enhanced or Na-enhanced templates would be needed.

**No download.** Only files already on disk are used: LAM9's E-MILES set and its template library, LAM9's and LAM10's work
files, and the sums. LAM9's and LAM10's committed files are imported or read, never edited.

## Question
LAM10's single-slope fit put 947 of 1586 galaxies (60 %) at the top-light grid edge, Γb 0.3. There, Γb_best fell with σ
(Spearman -0.40) and [M/H] (-0.57). Which part of the spectrum drives that?

## Not blind
- I know every LAM10 number: the pile-up, its σ and [M/H] trends, and the edge share by σ third over the 1586 (0.39, 0.60,
  0.80; the σ thirds split at 153.9 and 203.8 km/s).
- I know LAM10's K1, which passed on synthetics built from the fit's own templates, and every LAM9 number.
- I know the draw below and its make-up. I have run no masked fit.

## Sample
- **Real.** 100 sums drawn without replacement from LAM10's 1586 (sorted by plateifu) with numpy default_rng(20261106).
  - 57 sit at Γb 0.3 in LAM10 and 43 do not.
  - By σ third (low, mid, high) they are 32, 32 and 36. Their edge shares are 0.41, 0.53 and 0.75.
- **Synthetic.** 100 of LAM10's 300 K1 synthetics, drawn next from the same generator: `rng.choice(300, 100, replace=False)`.
  They are rebuilt exactly with LAM9's construction. Their α_in is checked against LAM9's record to 1e-9 relative.
- The lists are in `lam11_sample.json`, committed with the scripts.

## Fits
Each run is LAM10's single-slope χ² profile (variant A: masks m1-m7, the 13 Γb slopes, step a and step b, Γb_best,
α), with one change. Windows are in rest-frame Å.

| run | change |
|---|---|
| M0 | none (the reproduction run) |
| M_Na | Na I 8190 region masked: 8143-8244 (feature and both continua; LAM9's variant-B window) |
| M_CaT | CaT region masked: 8474-8792 (the three features and five continua) |
| M_TiO | TiO bands masked: 5816-6455 (TiO1 and TiO2sdss, features and continua) |
| M_IMF | all three regions masked |
| M_blue | the fit window ends at 7400 instead of 8900, with all arrays cut there. This drops every red IMF line |

- In every run the templates are broadened once per sum, from the uncut sum, and reused.
- M0's step-a fits also record each slope's χ² by region:
  - Na, CaT and TiO (the windows above);
  - blue-other (below 7400, outside TiO);
  - red-other (from 7400, outside Na and CaT).

## Statistics per run (real sample)
- **Edge fraction:** the share of galaxies whose χ² minimum is at Γb 0.3.
- **Median Γb_best.**
- **Spearman(Γb_best, log Σ_Re)** with a 95 % interval from 2000 bootstrap draws over galaxies (seed 20261106).
- **From M0 only:** the per-region χ² gain of Γb 0.3 over Γb 1.3, Δχ²_r = χ²_r(1.3) - χ²_r(0.3). A positive gain means Γb 0.3
  fits that region better. Reported: the median over galaxies, and each region's share of the summed gain.
- **Rows, ungraded:** the edge fraction split by LAM10's edge status and by σ third, and the median α_KU2.

## Decision lines (frozen)
**"Removes the pile-up":** a run removes it if its edge fraction is below 0.15 **and** the upper end of its Spearman(Γb_best,
log Σ_Re) interval is ≥ 0, so the trend is no longer negative at 95 %.

**Labels, applied in this order:**
1. **NOT DIAGNOSED** if K0, K1 or the MUTATE check fails.
2. **DRIVEN BY Na** if M_Na removes it and neither M_CaT nor M_TiO does. Advice: Na-enhanced templates.
3. **DRIVEN BY TiO/CaT** (naming which) if M_CaT or M_TiO removes it and M_Na does not. Advice: α- or Ti/Ca-enhanced templates.
4. **MIXED** if two or more single-region masks remove it, or if only M_IMF (all three together) does. Advice: both kinds
   of template.
5. **DRIVEN BY THE RED END, OUTSIDE THE IMF WINDOWS** if M_blue removes it and M_IMF does not. No IMF-line template fixes
   that; red continuum, sky or telluric residuals are the suspects.
6. **DRIVEN BY BLUE** if neither M_IMF nor M_blue removes it, and blue-other carries more than half of M0's summed χ² gain.
   This points to age, metallicity, abundance or flux mismatch outside the IMF lines, not to the IMF lines.
7. Otherwise **NOT DIAGNOSED**.

**Template advice.** If templates are advised, the exact files, sizes and source on the MILES share are named in the README
for the owner's yes. Nothing is downloaded. Known from the share's listing: α-enhanced bimodal models exist there only as
optical MILES (3540-7410 Å, no Na I or CaT). The Na-enhanced bimodal E-MILES models are Padova00 only.

## Checks
- **K0, reproduction.** M0's Γb_best and its grid index equal LAM10's for all 100 real sums, to 1e-9. Otherwise NOT DIAGNOSED.
- **K1, mask control.** The same six runs on the 100 synthetics. No mask may create edge hits: the edge fraction must be at
  most 0.05 in every run. Otherwise NOT DIAGNOSED. Reported per run: the median Γb_best - Γb_in and the median
  log(α / α_in).
- **MUTATE twin** (outputs `lam11_MUTATE.out` / `.json`). In each run, Γb_best is shuffled across the 100 real galaxies (seed
  20261106) and the Spearman interval is recomputed. It must include 0 in every run. Otherwise NOT DIAGNOSED.

## Compute
- Two processes, each single thread, with `nice -n 10`. Each holds half the real and half the synthetic jobs (index mod 2),
  so every run of every sum is fitted exactly once. The job contract holds: SIGTERM or `compute_queue/YIELD` gives exit 75,
  `--resume` continues, and every line is fsync'd.
- **Memory.** LAM10's shards held 4.5-7.3 GB RSS each with a footprint under 1 GB. Here each process returns freed memory to
  the system after every profile (`malloc_zone_pressure_relief`). Both RSS and physical footprint are logged and reported.
  The aim is under 1 GB of each per process.
- **Estimate.** 1200 profiles at about 6.5 s each comes to about 2.2 h of CPU, so about 65 min on two processes.

## Expectations on record (priors, before any fit)
| label | prior |
|---|---|
| DRIVEN BY BLUE | 40 % |
| DRIVEN BY Na | 15 % |
| DRIVEN BY TiO/CaT | 15 % |
| MIXED | 15 % |
| DRIVEN BY THE RED END | 5 % |
| NOT DIAGNOSED | 10 % |

κ = ½ FITTED; not theory closed.

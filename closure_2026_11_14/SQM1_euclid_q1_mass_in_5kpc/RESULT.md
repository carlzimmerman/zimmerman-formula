# SQM1 (EUCLID Q1 TOTAL MASS INSIDE 5/h kpc FROM STARS UNDER THE LAW): RESULT

2026-11-14. TEST lane. Criteria d91049bd52 (alone, before any script or number). Script 5eced7de93. As-frozen run
d2b3746304. Amendment A1 89c6448acd (alone, post hoc, before any graded number). Script under A1 1e6e1a3a95.

## Verdict (law S; as frozen: NOT EVALUABLE; under A1 as below)

- **canonical (a0 = 9.3603e-11): STILL FAILS [beta_z HIGH] FRAGILE**
- **alt (a0 = 1.1312e-10): STILL FAILS [beta_z HIGH] FRAGILE**

**As frozen: NOT EVALUABLE.** Known answer K3 failed (9.9e-4 against a 1e-5 tolerance) before any graded number was
computed. The cause is the Prugniel-Simien deprojection in EUC1's copied code, which is good to about 1e-3; the
quadrature and cut-off are converged to 1e-10 (`sqm1_k3_diagnostic.out`). A1 changed only that tolerance, to 2e-3.
Under A1 every known answer passes, the Newton mutation bites (exit 1) and the null twin agrees (exit 0).

In plain words. From stars alone, with a stellar M/L taken from the paper's own rest-frame colour and a published
M/L-colour relation (never fitted to the lensing), the law gets two of the three numbers.
- **Amplitude at the pivot**: passes for an IMF between Chabrier and 1.26 x Chabrier (canonical) or 1.20 x Chabrier
  (alt). Salpeter is HIGH by about 8 sigma.
- **Luminosity slope**: passes at every IMF in the bracket (0.78 to 0.84 against 0.71 +- 0.07).
- **Redshift trend**: fails HIGH at every IMF. The law gives -0.17 against -0.33 +- 0.05, about 3.2 sigma.

The fail is **FRAGILE**. It rests wholly on the frozen primary M/L evolution (the Bell 2003 relation applied to the
paper's colour evolution, d log Y/dz = -0.21). With the Zibetti 2009 relation (-0.32) or the paper's own
passive-evolution number (-0.36), the trend passes. The row then becomes NO VERDICT on both footings: all three
quantities pass for IMFs from Chabrier up to the amplitude edge, and Salpeter fails the amplitude.

The law's M5 responds to the stellar M/L with an exponent of about 0.8. To match beta_z on its own, the law needs the
stars' M/L to fall by about 0.41 dex per unit redshift at fixed luminosity. Newton would need 0.33.

**Newton (stars only), beside it:** STILL FAILS [beta_L HIGH, beta_z HIGH] on both. The slope is exactly 1.00, 4.1
sigma HIGH. The amplitude needs an IMF 0.14 to 0.22 dex above Chabrier.

kappa = 1/2 FITTED. Footings never pooled. One-sided test: none of these passes is a pass of the lensing gate.

## 1. Table (primary: law S, Bell M/L, a0 flat in z, h = 0.70, de Vaucouleurs stars, pivot z 0.5, log L h^2 10.7, log R_e h 0.5)

Observed (arXiv:2611.00224 Table 4): mu_M0 = 11.300 +- 0.021, beta_L = 0.71 +- 0.07, beta_z = -0.33 +- 0.05.
Sigma = sqrt(obs^2 + pred^2); pred from the paper's colour errors: 0.002 (amplitude), 0.007 (beta_z).
The amplitude is log10(M5 h / Msun).

| Footing | IMF | Amplitude (dev/sigma, word) | beta_L (dev/sigma, word) | beta_z (dev/sigma, word) |
|---|---|---|---|---|
| canonical | Chabrier (Y_r 2.94) | 11.261 (-1.8, PASS) | 0.795 (+1.2, PASS) | -0.170 (+3.2, HIGH) |
| canonical | Salpeter (Y_r 5.19) | 11.465 (+7.8, HIGH) | 0.844 (+1.9, PASS) | -0.181 (+3.0, HIGH) |
| alt | Chabrier | 11.279 (-1.0, PASS) | 0.777 (+1.0, PASS) | -0.166 (+3.3, HIGH) |
| alt | Salpeter | 11.478 (+8.4, HIGH) | 0.828 (+1.7, PASS) | -0.177 (+3.0, HIGH) |
| Newton (both) | Chabrier | 11.120 (LOW) | 1.000 (HIGH) | -0.214 (HIGH) |
| Newton (both) | Salpeter | 11.368 (HIGH) | 1.000 (HIGH) | -0.214 (HIGH) |

delta = log10 of the IMF factor over Chabrier, graded from 0 to 0.248 (Salpeter) in steps of 0.004:

| Footing | Amplitude passes | beta_L passes | beta_z passes | All three |
|---|---|---|---|---|
| canonical | 0 to 0.100 | 0 to 0.248 | none | none |
| alt | 0 to 0.080 | 0 to 0.248 | none | none |
| Newton | 0.14 to 0.22 | none | none | none |

Law B (reported, never the word), Chabrier / Salpeter: canonical A 11.221 / 11.434, beta_L 0.830 / 0.880,
beta_z -0.178 / -0.189; alt A 11.236 / 11.444, beta_L 0.811 / 0.865, beta_z -0.174 / -0.185. Row STILL FAILS
[beta_z HIGH] on both. The amplitude passes for delta 0.048 to 0.14 (canonical) and 0.028 to 0.128 (alt).

Reading, not graded: beta_R (d log M5 / d log R_e at fixed L). Law S gives -0.33 (canonical) and -0.32 (alt), Newton
-0.44, against -0.15 +- 0.07 observed: about 2.6 sigma steeper. The paper says beta_R and beta_L are strongly
degenerate. The combination along the size-luminosity relation passes (bracket B-along below).

## 2. Known answers, mutation, null twin (A1 run)

| Check | Result |
|---|---|
| K1 point mass / SIS (EUC1's) | 1.3e-11 / 7.6e-6 |
| K2 EUC1's SLACS median R_E,pred/R_E,obs with the copied code | 0.8852 (target 0.885 +- 0.005) |
| K3 Newton limit vs analytic de Vaucouleurs | 9.9e-4 (A1 tolerance 2e-3; as frozen 1e-5: FAIL) |
| K4 paper: M5/L5 at the pivot with average size | 6.53 (paper 6.7 +- 0.3) |
| K5 paper: model value at log L 10.67, z 0.2 | 11.358 (paper 11.38 +- 0.03) |
| K6 SI: Lsun,r 6.00e11 W/Hz | M_sun,r(AB) 4.649 (Willmer 4.65) |
| MUTATE newton (a0 -> 1e-30) | beta_L 1.0000 both; amplitude falls 0.142 / 0.159 dex; exit 1 |
| NULL twin (kpc, Msun, km/s; 800 nodes) | max difference 3.0e-6 over primary and all brackets; words identical; exit 0 |

The transcription check found every paper value string in the frozen HTML except two: Lsun,r (printed as
6.00 x 10^11) and h = 0.70 (printed as H0 = 70 km/s/Mpc). Both were confirmed by eye. The null twin checks the primary
and the brackets, not the law-B side table. That table's amplitude edge moves by one grid step (0.048 to 0.044).

## 3. Brackets (law S; row word canonical / alt)

| Bracket | Chabrier A, beta_L, beta_z (canonical) | Row canonical / alt |
|---|---|---|
| B-Zib: Zibetti M/L-colour (d log Y/dz -0.32) | 11.260, 0.794, -0.256 | **NO VERDICT / NO VERDICT** |
| B-pass: paper's passive evolution (-0.36 per z) | 11.261, 0.795, -0.286 | **NO VERDICT / NO VERDICT** |
| B-h 0.6774 | 11.275, 0.795, -0.170 | STILL FAILS [beta_z HIGH] / same |
| B-h 0.73 | 11.243, 0.795, -0.170 | STILL FAILS [beta_z HIGH] / same |
| B-h footing-native (0.667 / 0.806) | 11.282 (alt 11.218), 0.795, -0.170 | STILL FAILS [beta_z HIGH] / same |
| B-cpl: a0(z) tracking DESI-like CPL | 11.266, 0.789, -0.172 | STILL FAILS [beta_z HIGH] / same |
| B-size: average size (log R_e h 0.541) | 11.247, 0.790, -0.169 | STILL FAILS [beta_z HIGH] / same |
| B-along: slope along the size relation (obs 0.613 +- 0.083) | 11.261, 0.564, -0.170 | STILL FAILS [beta_z HIGH] / same |
| B-sel: observed amplitude +0.065 (no selection correction) | 11.261, 0.795, -0.170 | STILL FAILS [beta_z HIGH] / same |
| B-n6: Sersic n = 6 stars | 11.248, 0.792, -0.169 | STILL FAILS [beta_z HIGH] / same |
| B-rmax 300 kpc | 11.257, 0.797, -0.171 | STILL FAILS [beta_z HIGH] / same |

Under B-Zib and B-pass all three quantities pass together for delta 0 to 0.100 (canonical) and 0 to 0.080 (alt). In
several brackets the Chabrier amplitude itself falls LOW (canonical: B-h 0.73, B-size, B-n6, B-rmax; both footings: B-sel; alt: its own h 0.806).
The amplitude window is narrow and sits at the light end of the IMF range.

## 4. Red-team of the failing number (beta_z), written before the run (§6 of the criteria) and read after

- **The prediction side carries the fail.** At fixed L and R_e the law's M5 moves with z only through the stars' M/L
  (a0 is flat in the primary). The frozen primary took the M/L slope from Bell 2003's relation. That relation was
  built on smooth star-formation histories, so its M/L-colour slope (1.10) is shallow. Zibetti 2009 (1.65, with
  bursts and dust) and the paper's own single-burst passive evolution both give a steeper drop with z, and the
  trend then passes. Which slope is right for the paper's elliptical population is not settled here. The word
  therefore carries FRAGILE.
- **a0(z) cannot rescue it.** Tracking a0 with dark energy raises a0 at higher z if it moves at all (B-cpl: beta_z
  -0.172). That makes the trend shallower, not steeper. An a0 proportional to H(z) would make it worse still.
- **The paper's side.** beta_z comes from photo-z lenses (77 of 95). Fig. 5 shows no photo-z bias (mean 0.014). The
  paper's profile brackets (gamma 1.9, gamma(z) = 2 - 0.3(z - 0.5)) and its redder source template leave the
  parameters unchanged (Sect. 7). Its posterior covariance of beta_z with beta_L and beta_R is not printed, so a
  degeneracy-driven tilt cannot be bounded from the text. The selection function and the h scaling do not touch
  beta_z (B-sel, B-h).

## 5. What the amplitude window means, and a tension with the record (reported, not a word)

The amplitude passes only for a light IMF: Y_r 2.9 to 3.7 (canonical) at the paper's colour g - r = 0.79. The
record's SLACS lanes (A55 / A70, on Auger 2009's Salpeter stellar masses) need 1.17 x Salpeter, about delta = 0.32
on this scale, to make the SLACS Einstein radii. Yet the paper finds Euclid's M5 consistent with SLACS at matched
luminosity (its model 11.38 +- 0.03 against SLACS 11.33 +- 0.01). The two record readings therefore disagree on stellar
mass per unit light, not on lensing mass. This lane's colour-based prior gives less stellar mass per r-band light than
Auger's Salpeter masses scaled to the light. This is not resolved here. Any re-grade with an Auger-calibrated M/L
would move the amplitude to HIGH.

## 6. Limits

- One paper. Population-mean parameters are graded against a single pivot galaxy; the mean of log M5 over the
  population's scatter is not modelled. The law is nearly linear in Y over the colour scatter (about 0.03 dex).
- Stars only: no gas, no external field, no neighbours (the paper's lenses are isolated). Gas would raise the supply
  slightly, at the amplitude's HIGH edge, not at the trend.
- Y does not depend on L (the paper's colour model). A Y that rises with L would steepen the predicted beta_L,
  currently 1 to 2 sigma above the observed value.
- Prugniel-Simien deprojection good to about 1e-3 (0.0004 dex): the reason for A1.
- The paper's Fig. 10 SPS curves, its halo models and its stellar-to-halo relation are LCDM quantities. They were
  read, not used, not graded.
- Nothing accessed beyond the arXiv HTML of the paper and the arXiv PDFs of Bell 2003 and Zibetti 2009. The paper's
  Zenodo per-lens table (record 21345571) was not downloaded or used.

## 7. Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `sqm1.py`, `sqm1_paper_numbers.csv` (every number with its location),
`sqm1.out` / `sqm1_results.json` (as frozen, stopped at K3), `sqm1_k3_diagnostic.{py,out}`,
`sqm1_A1.out` / `sqm1_A1_results.json` (graded run), `sqm1_A1_MUTATE_newton.*`, `sqm1_A1_MUTATE_null.*`.
Downloads (untracked, hashed in the criteria): `_external_data/sqm1_sonnenfeld_q1/`.

Run (from the repository root; downloads at the path above):

    L=closure_2026_11_14/SQM1_euclid_q1_mass_in_5kpc
    python3 -I -B $L/sqm1.py --csv $L/sqm1_paper_numbers.csv --slacs real_research/data/slacs_auger2009_lenses.tsv \
        --outdir $L --html _external_data/sqm1_sonnenfeld_q1/2611.00224v1.html --amend A1
    SQM1_MUTATE=newton python3 -I -B $L/sqm1.py ... --amend A1    # exit 1
    SQM1_MUTATE=null   python3 -I -B $L/sqm1.py ... --amend A1    # exit 0

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

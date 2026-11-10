# KL1 RESULT: what carries form B's weak-lensing amplitude gap, and what is left of it

## Labels (both footings: canonical / alt)

**Lane label, the newest release of each survey (KiDS-Legacy + DES Y3), with the neutrino floor:**

- **As frozen: NO VERDICT / NO VERDICT.** The MUTATE arm MA2 could not bite on DES Y3. Halving DES's densities leaves 3 / 4
  signal-dominated points, and test (ii) needs 5. So DES's covariance rows are unguarded.
- **Under AMENDMENT A1 (post hoc): AMPLITUDE CONSISTENT WITH RAW LENSING / AMPLITUDE CONSISTENT WITH RAW LENSING.** A1's arm
  MA2b (densities doubled) bites on both surveys.
  - KiDS-Legacy: p 0.111 / 0.101.
  - DES Y3: p 0.159 / 0.157.
- **The gap is smaller, not closed.** Legacy still prefers sigma8 0.788 / 0.786 +- 0.012 for form B's spectrum. That is
  **2.1 / 2.3 Legacy widths** below form B's neutrino-floor value 0.812 (2.5 / 2.7 with the full Gaussian likelihood). Part B's
  frozen list counts a gap above 2 widths **against form B**.

**Part A label, KiDS-1000 + DES Y3 only:** NO VERDICT / NO VERDICT as frozen (same reason); **TENSION / TENSION under A1**.
KiDS-1000 at ALL: p 0.038 / 0.037, gap 3.95 / 4.06 KiDS-1000 widths.

Every label is for form B with the neutrino floor, its own layout with RB1's gas and the covariance at the model; gravity-only
S0 box; inherited halo list. TEST lane: relabels nothing, adopts nothing, not registered. **kappa = 1/2 FITTED; not theory
closed.** Cold dark energy, never a particle. Footings never pooled; they agree to a few hundredths of a width everywhere.
CO2's label is unchanged.

## The answer in plain words

**What carried the gap.** CO2's gap was 0.091 in sigma8, 5.6 / 5.8 KiDS-1000 widths. It came apart into these pieces.

1. **The survey's own release: the largest single piece.**
   - For form B's spectrum, KiDS-Legacy prefers sigma8 0.777 / 0.775 +- 0.0115. KiDS-1000 preferred 0.736 / 0.734 +- 0.016.
   - That is +0.041, or 2.5 KiDS-1000 widths, with nothing else changed.
   - Wright et al. 2025 attribute most of their own rise to new redshift calibration (context only).
   - In this machinery, the release's **prior-mean** redshift shifts alone move Legacy by only 0.46 / 0.47 Legacy widths. MB2
     therefore does not bite (line 0.5). The move comes from the new n(z) shapes and the new data, not from the prior means.
2. **Our massless neutrinos: the largest piece on our side.**
   - A real refit of CO2's CMB fit with the 0.06 eV floor (not CO2's fixed-parameter row) gives sigma8 **0.8121 / 0.8120**.
     That is below CO2's 0.8152 bracket.
   - The CMB fit gets slightly *better*: total chi^2 -1.18 / -1.31.
   - It is worth 0.9 KiDS-1000 widths, and p goes 0.0026 -> 0.012.
3. **The covariance evaluated at the survey's fiducial: worth about 0.4 widths.**
   - At form B's higher amplitude the signal terms are larger. KiDS-1000 chi^2 falls by 8.4 / 8.8; p 0.012 -> 0.032.
   - The edges (rest of the covariance unscaled or scaled steeper; fiducial +- 0.02) give p 0.021 to 0.040.
4. **The gas RB1 measured: worth about 0.3 widths, less than I expected.**
   - Groups keep 0.59 to 0.92 of their baryons inside R500 (by mass). Moving the rest out to the turnaround radius shifts
     3.4 to 3.8 % of M200c in groups.
   - That lowers the power by 1.8 % at k 1 h/Mpc and 6 % at k 5. KiDS-1000 chi^2 -2.1 / -2.3.

**What is left.**
- On Legacy with all three: CONSISTENT by goodness of fit, but a 2.1 / 2.3 width preference for lower amplitude.
- On KiDS-1000: TENSION, about 4 widths.
- DES Y3 never fell below p 0.05. Its own preferred sigma8 for this spectrum is 0.740 +- 0.025 at ALL, so it too sits 2.8 / 3.0
  DES widths below the pin.

**What works against form B.**
- **Alignment.** Turning intrinsic alignment off, or keeping the one-amplitude model, carries a lot.
  - With alignment off, KiDS-1000 at A1 is EXCLUDED (p 0.0007 / 0.0005).
  - Legacy at ALL with alignment off sits on the line: p 0.052 / 0.044, gap 3.3 / 3.5.
  - The fitted amplitude (A_IA 0.9 for KiDS, 1.45 for DES) is absorbing part of the amplitude.
- **More small-scale points** (support cut 0.7, N 189): KiDS-1000 at ALL p 0.013, gap 4.7 / 4.9.
- **Widening the redshift priors (A4).** It makes KiDS-1000 CONSISTENT (p 0.11), but only by moving bin 4's shift 5.2 KiDS-1000
  widths. That is not a calibration anyone measured.

**Our comparison has no sign error in the redshifts.** I checked CFG592's n(z - Delta z) convention against KiDS's own pipeline.
The CosmoSIS module shifts as `f(z - bias)` (a web read). That rule, with z = 0 prepended and cubic interpolation, reproduces
KiDS-1000's published mean-redshift shifts at its maximum posterior to 6.6e-8. The opposite sign misses by 0.036.

## Rows, one change at a time (A1 is the baseline for A2 to A5). Canonical / alt.

**KiDS-1000** (N 104; CO2's lines: p >= 0.05 CONSISTENT, >= 0.0027 TENSION):

| row | chi^2 | p | label | best sigma8 +- width | gap (widths) |
|---|---|---|---|---|---|
| A0 CO2 (sigma8 0.8271) | 157.89 / 159.35 | 0.0026 / 0.0021 | EXCLUDED AT 3 SIGMA | 0.7358 / 0.7341 +- 0.016 | 5.62 / 5.78 |
| **A1 neutrino floor** (0.8121 / 0.8120) | 145.75 / 146.73 | 0.012 / 0.011 | TENSION | 0.7358 / 0.7341 | 4.70 / 4.84 |
| A2 covariance at the model (gamma 2) | 137.34 / 137.98 | 0.032 / 0.030 | TENSION | 0.7432 / 0.7414 | 4.28 / 4.40 (ln det 4.70 / 4.82) |
| A2 edges gamma 0 / 3; fiducial -0.02 / +0.02 | 140.2-141.1 / 137.2-137.7; 135.3-135.9 / 139.6-140.3 | 0.021-0.040 | TENSION | | |
| A3 RB1's gas, edge r_ta | 143.63 / 144.39 | 0.015 / 0.014 | TENSION | 0.7394 / 0.7377 | 4.38 / 4.52 |
| A3 edge R200c; power-law f_ret | 145.33-146.20; 142.93-143.60 | 0.011-0.016 | TENSION | | |
| A4 redshift priors x 2 | 132.92 / 133.45 | 0.113 / 0.110 | CONSISTENT | 0.7435 / 0.7416 +- 0.018 | 3.87 / 3.91; bin 4 pulled 5.2 widths |
| A1s neutrino shape (reported) | 145.59 / 146.55 | 0.012 / 0.011 | TENSION | | |
| **ALL = A1 + A2 + A3** | **135.60 / 136.06** | **0.038 / 0.037** | **TENSION** | 0.7474 / 0.7455 +- 0.016 | **3.95 / 4.06** (ln det 4.42 / 4.54) |
| ALL, edges (gamma 0 / 3, R200c, power law) | 135.0-138.8 | 0.027-0.040 | TENSION | | |

**DES Y3** (N 52):

| row | chi^2 | p | label | best sigma8 +- width | gap |
|---|---|---|---|---|---|
| A0 CO2 | 74.69 / 74.67 | 0.050 / 0.051 | CONSISTENT | 0.7306 / 0.7312 +- 0.025 | 3.78 / 4.02 |
| A1 | 69.04 / 68.97 | 0.096 / 0.097 | CONSISTENT | 0.7306 / 0.7312 | 3.19 / 3.38 |
| A2 | 64.69 / 64.63 | 0.158 / 0.166 | CONSISTENT | 0.7409 / 0.7367 | 2.84 / 2.76 |
| A3 | 68.95 / 68.89 | 0.097 / 0.098 | CONSISTENT | 0.7314 / 0.7311 | 3.35 / 3.39 |
| A4 | 63.18 / 63.12 | 0.236 / 0.238 | CONSISTENT | 0.742 / 0.734 (canonical width 0.074: flat parabola, unreliable) | 0.95 / 2.65 |
| **ALL** | **64.62 / 64.70** | **0.159 / 0.157** | **CONSISTENT** | 0.7401 / 0.7397 +- 0.025 | 2.83 / 3.02 (ln det 3.26 / 3.43) |

**KiDS-Legacy, Part B** (N 173 of 357 inside the published cuts after the support cut; 6 bins, 2 to 300 arcmin):

| row | chi^2 | p | label | best sigma8 +- width | gap |
|---|---|---|---|---|---|
| B0 CO2's target 0.8271 | 215.56 / 218.01 | 0.025 / 0.020 | TENSION | 0.7767 / 0.7748 +- 0.0115 | 4.40 / 4.60 |
| B1 neutrino floor | 204.42 / 206.18 | 0.067 / 0.057 | CONSISTENT | 0.7767 / 0.7748 | 3.09 / 3.27 |
| B2 covariance at the model | 200.24 / 201.75 | 0.096 / 0.084 | CONSISTENT | 0.7835 / 0.7814 | 2.49 / 2.66 (ln det 2.90 / 3.06) |
| B3 RB1's gas | 202.17 / 203.54 | 0.081 / 0.072 | CONSISTENT | 0.7808 / 0.7788 | 2.68 / 2.86 |
| **BALL** | **198.33 / 199.49** | **0.111 / 0.101** | **CONSISTENT** | 0.7875 / 0.7855 +- 0.0116 | **2.13 / 2.30** (ln det 2.50 / 2.70) |
| BALL, alignment off | 207.48 / 209.37 | 0.052 / 0.044 | CONSISTENT / TENSION | 0.7782 / 0.7760 +- 0.010 | 3.27 / 3.46 |
| BALL, A5a (unreliable, below) | 186.20 / 186.09 | 0.251 / 0.253 | CONSISTENT | 0.826 / 0.824 | -1.17 / -1.01 |

## Brackets that could go against (A5; reported, never graded)

| bracket | KiDS-1000 on A1: p, gap | KiDS-1000 on ALL: p, gap | DES on ALL: p, gap |
|---|---|---|---|
| A5c1 alignment off | 0.0007 / 0.0005 **EXCLUDED**, 5.71 / 5.87 | 0.0077 / 0.0069 TENSION, 4.85 / 4.97 | 0.028 / 0.027 TENSION, 4.87 / 4.88 |
| A5c2 alignment with redshift power (eta ~ +2.5) | 0.018 / 0.016, 4.27 / 4.42 | 0.053 / 0.052, 3.58 / 3.84 | n/a (DES has it) |
| A5d support 0.8 (N 166 / DES 163) | 0.021 / 0.018, 5.06 / 5.26 | 0.054 / 0.048, 4.38 / 4.63 | 0.198, 1.86 / 1.84 |
| A5d support 0.7 (N 189 / DES 214) | 0.0069 / 0.0057, 5.13 / 5.32 | 0.014 / 0.013, 4.70 / 4.92 | 0.236 / 0.233, 1.95 / 1.91 |
| A5b k_hi halved (N 40 / DES 45) | 0.090 / 0.087, 3.53 / 3.59 | 0.270 / 0.272, 2.61 / 2.65 | 0.177 / 0.169, 3.03 / 3.22 |
| A5a long modes, CFG411 (**unreliable**) | 0.118, 2.29 / 2.41 | 0.139 / 0.142, 1.64 / 1.74 | 0.310 / 0.311, 1.52 / 1.11 |
| A5a, CFG424 (second realisation) | 0.026 / 0.025 | 0.059 / 0.057 | 0.219 / 0.224 |
| ALL + A4 (priors x 2) | | 0.174 / 0.175 | 0.304 / 0.305 |

- **A5a did not measure what it was frozen to measure.** It was meant as a long-mode correction that would go against form B: a
  larger box should add non-linear power.
  - The two 200 Mpc/h runs disagree with each other by 13 %. CFG411's run has 0.83 / 0.86 / 0.88 of the 100 Mpc/h box's power
    at k 0.5 to 1 (z 0 / 0.5 / 1); CFG424's has 0.96 / 0.97 / 1.01.
  - Two boxes of the same size disagreeing that much points to the coarser runs' resolution, not to missing long modes.
  - The relief A5a gives (Legacy p 0.25, KiDS-1000 gap 1.6) must not be read as support for form B. The long-mode question is
    left open here.
- Where the support cut admits more DES points, DES prefers a *higher* amplitude (0.78). KiDS goes the other way.

## The redshift calibration (A4) and the release

- **Pulls at the target.**
  - At CO2's pin, KiDS-1000 pulls bin 4 by -2.20 / -2.25 prior widths.
  - With the neutrino floor: -1.80 / -1.84.
  - At ALL: -1.45 / -1.48, under the frozen 2-width line.
  - At ALL's best sigma8 the pulls are all below 1.
- **With the priors doubled** (A4), the fit moves bin 4 by -2.58 / -2.61 *doubled* widths, which is 5.2 of KiDS-1000's stated
  widths. That is how A4 reaches p 0.11. It is a proxy, not newer data.
- **The release (Part B).**
  - For form B's spectrum, Legacy's best sigma8 is +0.041 above KiDS-1000's (+2.52 / +2.53 KiDS-1000 widths).
  - Legacy's widths are narrower (0.0115 against 0.016), so in its own widths the gap at CO2's target only goes 5.6 -> 4.4 / 4.6.
  - The prior-mean test MB2 moves Legacy's best sigma8 by +0.47 / +0.46 widths, under the frozen 0.5 line, so the arm does not
    bite. By the frozen rule MB2 guards no graded row. What it takes away is the attribution: in this machinery the shift is not
    carried by the prior means.
- **Context only** (Wright et al. 2025, Appendix I.1 and Section 6, a web read, PROVISIONAL):
  - KiDS-1000 re-analysed with the Legacy redshift calibration sits 1.42 sigma from Planck in S8 (their Hellinger measure).
  - Legacy on the KiDS-1000 footprint sits 0.85 sigma from Planck.
  - About two thirds of the reduction in tension is attributed to redshift estimation and calibration.

## Hand estimates against the outcome

**Mine** (`FROZEN_CRITERIA.md` section 8, before any code):

| item | my estimate | outcome | verdict on the estimate |
|---|---|---|---|
| A1 sigma8 | 0.815 to 0.819 | 0.812 | lower: the refit moved A_s and omega_d |
| A1 KiDS p | 0.006 to 0.010 | 0.011 / 0.012 | |
| A1 gap | 4.8 to 5.1 | 4.70 / 4.84 | |
| A1 DES p | 0.07 to 0.10 | 0.096 | right |
| A2 Delta chi^2 | -8 to -20 | -8.4 | low end |
| A2 p | 0.01 to 0.04 | 0.03 | right |
| A2 gap | 4 to 5 | 4.3 / 4.4 | right |
| A3 Delta chi^2 | -3 to -10 | -2.1 / -2.3 | wrong, smaller |
| A4 Delta chi^2 | -3 to -6 | -12.8 / -13.3 | wrong, much larger, at a 5-width bin-4 pull |
| ALL KiDS p | 0.02 to 0.08, TENSION 60 % | 0.037 / 0.038 TENSION | right |
| ALL gap | 3 to 4 | 3.95 / 4.06 | top edge |
| ALL DES | CONSISTENT | CONSISTENT | right |
| Alignment off, Delta chi^2 | +5 to +15 | +16.3 / +16.9 | above the range |
| Part B: Legacy best sigma8 | 0.78 to 0.80 | 0.775 / 0.777 | slightly below the range |
| Part B: B1 gap | 1 to 2.5 | 3.1 / 3.3 | worse |
| Part B: BALL gap | 0.5 to 2 | 2.1 / 2.3 | slightly worse |
| Part B: label | CONSISTENT | CONSISTENT | right |

**The closure chat's guess.**
- It expected the release to cut the gap from about 5 widths to 1 or 2. The release cut the sigma8 gap by about 45 % (0.091 ->
  0.050), which is 4.4 / 4.6 in Legacy's narrower widths.
- It expected A1 to A3 to be worth about 1 width. They were worth 2.3 more widths on Legacy and 1.7 on KiDS-1000.

## Against form B, by the frozen lists

| item on the frozen lists | outcome | counts against? |
|---|---|---|
| KiDS-1000 left at TENSION at ALL | yes | yes |
| Gap at ALL above 3 | KiDS-1000 3.95 / 4.06; DES 2.83 / 3.02 | yes |
| Gap on Legacy above 2 (Part B list) | 2.13 / 2.30 | yes |
| Against-brackets push ALL below 0.0027 | no: alignment off reaches 0.007 at ALL, 0.0005 at A1 | no |
| MP4 / MB1 fail to bite | no: both bite (p <= 8e-6) | no |
| KiDS delta-z pulls beyond 2 widths at ALL | no: max 1.48 | no |
| Neutrino floor costs the CMB fit more than 9 | no: it gains 1.2 / 1.3 | no |
| DES worse at ALL than CO2's 0.050 | no: 0.16 | no |

## Known answers and MUTATE

**Known answers: all pass.**
- KA0: CO2 replayed, 157.890 / 159.355; best 0.7358 / 0.7341 +- 0.0162 / 0.0161; DES 74.685 / 74.674; N 104 / 52.
- KA1: the harness at mnu 0 replays CO2's PA and chi2_E exactly; CLASS sigma8 0.81524 / 0.81521 against CO2's 0.8152.
- KA2 (covariance at the model):
  - KiDS: fitted area 794 deg^2 (the quoted effective area of 777 deg^2 is from memory); published / mine 0.88 to 1.14 on 144
    noise-dominated points; median 1.14 on 38 signal-dominated points; correlation pattern within 0.010.
  - DES: area 3478 deg^2; 0.97 to 1.03; median 1.23; within 0.021.
- KA3: f_ret = 1 returns CO1's R_tot exactly (0 and 2e-7 with inserted points); mass conserved to 5e-16.
- KA4: the response replayed.
- KB1: 378 points, 6 bins, positive-definite covariance, n(z) weights summing to 1.0000.
- KB2: KiDS-1000 through the generalised loader, 157.890 / 159.355.
- KB3: Legacy area 853 / 852 deg^2 (Wright et al. quote 967.4); 0.94 to 1.05; median 1.04.

**MUTATE.**
- **Bite:** MA1 (0.6 eV lowers sigma8 by 0.096); MA2 on KiDS; MA3 (R_tot at k 1 moves 0.081, chi^2 moves 7.0 / 8.0); MP4
  (sigma8 0.90 under ALL: p 4e-6 / 3e-6); MB1 (p 8e-6 / 4e-6); MA2b on both surveys (added by A1).
- **Do not bite:**
  - MA2 on DES: test (ii) is NOT EVALUABLE there; this is AMENDMENT A1's subject.
  - MB2, at 0.47 / 0.46 widths against 0.5.

## Disclosed after the freeze

- **AMENDMENT_A1.md** (e01d1b9a35, post hoc, every label seen): MA2's defect on DES; MA2b added. The frozen reading (NO VERDICT)
  leads the label section.
- **AMENDMENT_PB1.md** (7787483300; before any Part B number, after reading the release's structure): how Part B's frozen text
  maps onto the release's files.
- **Development numbers seen before the runs:**
  - CO2's chi^2 replay and KA2's ratios, in a scratch smoke test.
  - KB2, in a scratch smoke test.
  - The sign check of the redshift shift.
- **A5a's defect** is described above. It changes no label.

## Limits

1. **The box.** One gravity-only box of 100 Mpc/h. Its realisation noise at k 0.2 (CO2's post hoc) is not corrected in the graded
   rows, and the long-mode question is not answered (A5a, above).
2. **Geometry and response.** The geometry is the S0 engine's (Omega_m 0.3138, h 0.6736; form B's pinned value with the neutrino
   is Omega_m 0.3147 / 0.3143). The response treats a change of amplitude as a change of epoch at fixed linear shape.
3. **The covariance at the model.**
   - It uses a flat-sky Gaussian part with a fitted area and the published rest scaled by the signal. The rest, R, holds whatever
     my Gaussian part misses.
   - The p uses the covariance at the target. The ln det variant is reported and moves gaps up by about 0.4.
4. **Alignment.** One NLA amplitude (with eta for DES). Legacy's own fiducial alignment model is mass-dependent. Alignment
   freedom carries a large part of every row.
5. **Legacy's statistic.** Legacy's fiducial statistics are COSEBIs and band powers; only its xi+- are graded here, binned by
   CFG592's theta-weighted rule rather than the release's pair-count weighting. CFG592 interpolates n(z) linearly without the
   z = 0 point (about 1e-3 in mean z).
6. **The gas row.**
   - f_ret is applied to the layout's own baryons inside R500, with the cold component held, and the z 0 ratio is used at every
     node.
   - The galaxy regime is unchanged.
   - Groups' stars come from KVM18 (RB1's bracket covers x / 1.5 to x 1.5).
7. **DES.** DES Y3 is the newest DES release on disk. No other release was fetched (the go covered one file).
8. **Web reads, all PROVISIONAL.** Wright et al., the KiDS data page and the CosmoSIS module line. The module line is confirmed
   independently by the 6.6e-8 replay.

## Files

**Criteria and amendments**
- `FROZEN_CRITERIA.md`
- `FROZEN_CRITERIA_PARTB.md`
- `AMENDMENT_PB1.md`
- `AMENDMENT_A1.md`
- `FETCH_LOG_PARTB.md`: URL, date, size, sha256 `7fdf214c...7f77`

**Scripts**
- `kl1_fit_nu.py <footing>`: the A1 refit, 965 s / 1161 s. Writes `parts/fit_nu_*.json`.
- `kl1_nu.py`: sigma8, KA1 (ii), A1s, MA1. Writes `kl1_nu.json`, `kl1_nu.out`, `kl1_nu_MUTATE.json`.
- `kl1_gas.py`: A3, KA3, MA3. Writes `kl1_gas.json`, `kl1_gas.out`, `kl1_gas_MUTATE.json`.
- `kl1_lib.py`: CO2's shear path, KL1's fit copy, the covariance at the model, the scan rule.
- `kl1.py <footing>`: rows A0 to ALL, about 47 min a footing. Writes `parts/rows_*.json` and `.out`. With `KL1_MUTATE=1` it runs
  MA2, MA3 and MP4.
- `kl1_ma2b.py`: MA2b. Writes `parts/ma2b_MUTATE.json` and `.out`.
- `kl1_partb.py <footing> <release folder>`: Part B, run with `python3 -I`, 431 s. Writes `parts/partb_*.json` and `.out`.
- `kl1_grade.py`: both readings. Writes `kl1.json`, `kl1.out`.

**Read-only inputs**
- CO2's scripts and stored fits.
- CO1's `co1_hm.py` and json.
- CFG592's library.
- CFG596's, CFG411's and CFG424's S0 runs.
- RB1's `rb1.json`.
- F1A's likelihood.
- The KiDS-1000 and DES Y3 files on disk.
- The KiDS-Legacy release, untracked, beside the repository.

| commit | local `main` | origin/main |
|---|---|---|
| FROZEN_CRITERIA.md, alone | 99a42c78ef | 8f3dfb63f7 |
| FROZEN_CRITERIA_PARTB.md, alone | d26939ed4f | 575f31c511 |
| AMENDMENT_PB1.md, alone | 7787483300 | 224b5a0f76 |
| FETCH_LOG_PARTB.md | 0965901c16 | 85e7ff3f73 |
| AMENDMENT_A1.md, alone (post hoc) | e01d1b9a35 | e7d02f9f3d |
| scripts, outputs, RESULT.md | ab253e1051 | 14ce1b35e1 |
| this table | the commit that adds it | its replay, the last KL1 commit on origin |

Local `main` has diverged from origin. Each commit was replayed onto origin/main in a sparse temporary worktree, which was then
removed.

kappa = 1/2 FITTED; not theory closed. Relabels nothing.

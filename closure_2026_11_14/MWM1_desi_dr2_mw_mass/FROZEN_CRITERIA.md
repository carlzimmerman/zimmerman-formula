# MWM1 FROZEN CRITERIA: the framework's Milky Way line against DESI DR2's enclosed-mass profile, halo-free

2026-11-14. TEST lane. Adopts nothing, relabels nothing (DR2REV, NMB1, RAW1, MWJ1, MWG1, MWT1, RRL2 keep their
labels), does not edit the scorecard or any other lane's files, registers nothing. Written and committed alone,
before any script of this lane and before any number of this lane was computed.

## 0. Question

Does the framework's Milky Way line (baryons only, no dark matter, no-field line) reproduce the enclosed mass
M(<r) that DESI DR2 (arXiv:2611.05518, "DESI DR2 Results III: The Mass of the Milky Way", v1, 2026-11-03) reports
between 20 and 80 kpc? Canonical a0 = 9.3603e-11 and alt a0 = 1.1312e-10 m/s^2, side by side, never pooled.

## 1. What is known beforehand (disclosed)

Read in full or in part before writing: Results III (all of Sections III, IV, V, VI, VII, Tables 2-5), Medina et al.
2611.05521 (Section V, eqs 9-14, Section VI), Li et al. 2611.15560 (abstract, Tables 1-4), titles of 2611.05519
and 2611.05520 and one line of 2611.05520 (BHB M(<100) = 0.78e12, NFW-based). DR2REV `REVIEW.md` (first 80 lines),
NMB1 `FROZEN_CRITERIA.md` (first 80 lines) and `RESULT.md` (first 40 lines), RAW1 `raw1_model.py` and parts of
`raw1.out`, RRL2 criteria and result, MWJ1, MWT1, MWG1 results (heads). So these numbers are known:
- Table 4 (joint, all / RRL / BHB, 20-80 kpc every 5 kpc), e.g. all: 1.94 (20), 2.65 (30), 4.08 (45), 4.51 (50),
  5.56 (65), 6.36 (+0.53 / -0.48) (80), in 1e11 Msun.
- DR2REV (post hoc, diagonal): the zero-parameter line (A = 1, no field) sits -2.3 to -3.5 sigma below Table 4 at
  20-65 kpc canonical (worst -3.5 at 45), -0.95 to -2.1 alt; -1.4 / -0.3 sigma at 80. DR2REV also found Table 4's
  shape is partly imposed (emPDF is an NFW, GME a power law whose slope sits on its prior).
- NMB1: the four NIMBLE curves (fig10 of the Zenodo figure data) at 30 / 80 kpc: A-RRL 2.449 / 6.678, A-BHB
  2.481 / 5.993, B-RRL 2.787 / 6.181, B-BHB 2.569 / 6.543; NIMBLE GLS 2.546 / 6.379. The line at RAW1-rounded a0:
  FW census canonical 2.331 / 5.691, alt 2.526 / 6.219 (NMB1 E0 PASSES both footings at its 2-radius gate).
- RAW1 (raw1.out): FW census 50 kpc canonical 3.683, alt 4.012; FW rc 30 kpc 2.644 / 2.725, 50 kpc 4.143 / 4.308.
- GME (Medina): M(<80) BHB 0.64 +/- 0.06, RRL 0.53 +/- 0.05 e12 (bias-corrected); gamma 0.45 / 0.46.
- Li et al.: Jeans RRL 5.23 +/- 0.66 and TME RRL 4.69 +/- 0.25 at 81.7 kpc; Jeans BHB 4.51 +/- 0.67 and TME BHB
  4.72 +/- 0.41 at 82.8 kpc (1e11), statistical only, not mock-corrected; their mocks (Au-6, Au-16) give virial
  masses underestimated by 15.5 +/- 2.8 % (RRL) and 11.9 +/- 3.4 % (BHB).
NOT known when this was frozen: the NIMBLE values at any radius other than 30 and 80 kpc (the fig10 file's
structure was listed, 25 radii 20-80 kpc step 2.5, methods empdf / gme / nimble-a / nimble-b / joint; no value read).
This lane is therefore NOT blind: it is a frozen, per-radius re-grade of a question DR2REV answered post hoc and
NMB1 answered at two radii.

**Hand estimate (written now).** Using the four NIMBLE curves, the method spread and a 10 per cent baryon
uncertainty, sigma is about 0.04-0.05 dex. Canonical sits about -0.04 dex at 30 and -0.05 dex at 80 (z about -1),
and, if NIMBLE follows Table 4 near 40-50 kpc, about -0.07 to -0.08 dex there (z about -1.7 to -2.2). Guess:
canonical borderline, STILL FAILS [LOW at one or two radii near 40-50 kpc] or a narrow pass; alt PASSES. Newton
STILL FAILS LOW everywhere by a factor 3-10. Brackets that lower the data (LMC, beta) will move canonical toward
PASS; hot gas raises the line. Expect FRAGILE on canonical.

## 2. Inputs (read as data only; untracked in `_external_data/mwm1_desi_dr2_mass/`; sha256)

| file | source | sha256 |
|---|---|---|
| `2611.05518v1.html` | arxiv.org/html/2611.05518v1 (Results III) | 831996f5c3d9dc3d1085dcfef9daafb594502482639fb75a1b8cbbd67ece4416 |
| `2611.05519v1.html` | Riley et al., AuriDESI mocks | 2926a561d5241f811275f68942e0994509740930f0bc20a71e02f81ab2768c8d |
| `2611.05520v1.html` | Zhou et al., emPDF | ed224dd6dcb53fc3ee06a83e79f8222865eab656c1c2bfaeded8381937ae3c4c |
| `2611.05521v1.html` | Medina et al., GME | ea3ebf47d27224b25b28bba5a6b73c7655216677332217be8e4bbb77887d4f04 |
| `2611.15560v1.html` | Li et al., LAMOST + SDSS + DESI | a5fdb8b7d9a7e9de5cecfee58a4edd7de33a486344d7b0218f684582ab99f2dc |
| `desi-dr2-mw-mass-figdata.zip` | Zenodo 10.5281/zenodo.23712180 (Results III figure data), 2,652,537 bytes, md5 5b0cc3aa9947286eb9348e947d01182d | 1b132abc3f163887160efb29a88d294ce5fb0751d2e389951da9c4c237e35ee1 (equal to the hash DR2REV and NMB1 recorded) |

Numbers transcribed from the papers go into a small tracked `mwm1_published_numbers.csv` (value, table or
equation, section) committed with the script. Values read from the zip are written by the script to its output.

## 3. Which DESI numbers are graded (raw data vs framework-native)

- **Graded (halo-free):** NIMBLE-A and NIMBLE-B, RRL and BHB, from `fig10/desi-dr2-menc.csv` (spherical Jeans,
  B-spline tracer density and dispersions, no potential form; bias-corrected by the paper per the Figure 10
  caption). These are the only DESI curves whose shape is measured.
- **Not graded, reported only:** Table 4 / fig11 joint (it carries emPDF, a two-parameter NFW, and GME, a power-law
  potential, with combined weight up to 30-60 per cent; its shape is partly imposed); emPDF alone (NFW); every
  M200c (NFW extrapolation); GME's M(<100) (extrapolated power law). GME at 50-80 kpc (power-law potential, not a
  dark-halo shape, but a parametric shape whose slope sits on its prior) enters only as bracket B7.
- **Graded radii:** 20, 25, ..., 80 kpc (the 13 radii of Table 4). The points are strongly correlated (smooth fits
  to the same stars); the per-radius words are not independent tests and are not combined into one significance.
- 100 kpc: reported only (no halo-free DESI number exists there; GME is an extrapolation).

## 4. The framework prediction (recipe)

`closure_2026_11_12/RAW1_halo_stars_direct/raw1_model.py`, loaded read-only by file path: `g_model(r, model,
footing, a0_mult)` and `M_of_g`. Primary case **FW census** (McMillan 2017 spherical enclosed baryons, stars 5.49e10
+ cold gas). Second case **FW rc** (stars at the rotation-curve value, 7.08e10 / 6.42e10) is graded the same way and
reported beside it. Line: g = nu(g_b / a0) g_b, nu(y) = 1 / (1 - exp(-sqrt y)), no external field (owner's actual-
field reading, 2026-11-12). Standing a0 via a0_mult = 9.3603e-11 / 9.36e-11 and 1.1312e-10 / 1.13e-10. Newton
(model 'N') reported. Diagnostic (reported, not graded): nu(sqrt(y^2 + e_N^2)) / nu(y) at every graded radius for
FW census, e_N = 0.000160 (canonical) / 0.000110 (alt), y = g_b / a0.

## 5. Data value and sigma budget (all in dex, at each radius r)

- D(r) = mean of log10(Menc_med) of the four NIMBLE curves (equal weights). Off-grid radii never occur (5 kpc
  radii are on the 2.5 kpc grid).
- s_D(r) = Table 4 "All" log10 error on the side facing the line (lower error if the line is below D, upper if
  above). This is the paper's calibrated total error for the joint; it is used as the DESI quoted error.
- s_spread(r) = sample standard deviation (ddof = 1) of the four NIMBLE log10 medians.
- s_FW(r) = half of |log10 M_FW(1.1 M_b) - log10 M_FW(0.9 M_b)| (stars and cold gas scaled together; 10 per cent
  from McMillan 2017's stellar mass 5.43 +/- 0.57e10).
- sigma = sqrt(s_D^2 + s_spread^2 + s_FW^2). z = (log10 M_FW - D) / sigma.

## 6. Words (per case, per footing; never pooled)

Per radius: **PASS** if |z| <= 2, **HIGH** if z > 2, **LOW** if z < -2.
Row, in this order:
1. **NO VERDICT** if the row word (pass vs fail) differs between the primary data and any of the tracer / survey
   alternatives (each with its own s_D and s_spread, same s_FW):
   - T1 RRL only: mean of NIMBLE-A RRL and NIMBLE-B RRL; s_D from Table 4's RRL column; s_spread from the two.
   - T2 BHB only: the same with BHB.
   - T3 LAMOST (Li et al.): the 80 kpc point replaced by Li et al.'s four halo-free values (Jeans and TME, RRL and
     BHB) at r = 82.25 kpc (mean of 81.7 and 82.8): value = mean of the four log10 masses, s_D = mean of the four
     quoted log errors (err / M / ln 10), s_spread = their std (ddof 1); other radii primary.
   - T3c: T3 with Li's own mock correction (x 1/(1 - 0.137), the mean of 15.5 and 11.9 per cent).
2. **MW MASS PROFILE PASSES** if all 13 radii PASS.
3. **STILL FAILS [radii, words]** otherwise.
**FRAGILE** appended if any bracket B1-B8 gives a different row word (pass vs fail) for that case and footing.
Newton is reported with the same rule. A PASS is a HIT for the framework, not a pass of the theory, and awaits an
independent re-grade.

## 7. Brackets (red-team of the data team's assumptions; each a full re-grade of the row; frozen now)

- B1 AuriDESI bias correction undone (it is calibrated on LCDM haloes): each NIMBLE curve multiplied by (1 + b),
  b from Table 3 (median 20-80 kpc): A-RRL +3.9, A-BHB -2.2, B-RRL -4.1, B-BHB -2.1 per cent.
- B2 LMC reflex / disequilibrium (Results III Section VII.3: equilibrium estimates biased high by up to 20 per cent;
  Erkal et al.): D lowered by 10 per cent (x 0.90) at every radius.
- B3 the same at its quoted maximum, only where the LMC's effect is largest: x 0.80 at r >= 50 kpc.
- B4 unrelaxed / cold debris (Sgr remnants, Magellanic debris at 50-95 kpc, RRL2's cold lump; cold substructure
  lowers the dispersion): D raised x 1.10 at r >= 40 kpc.
- B5 velocity anisotropy beta (proper-motion errors at large r inflate sigma_tan and lower beta): beta +0.1 in the
  Jeans bracket (alpha + gamma - 2 beta) with alpha 4.6, gamma 0.4, beta 0.35, i.e. D x (1 - 0.2 / 4.3) = x 0.953 at
  every radius; and beta -0.1: x 1.047.
- B6 spherical symmetry (flattened stellar halo in a spherical Jeans fit): D x 0.95 and x 1.05 at every radius.
- B7 GME included where it enters (50-80 kpc): its RRL and BHB fig10 curves added to the four NIMBLE curves in D and
  s_spread (power-law potential; reported as a bracket only).
- B8 hot gas on the framework side: Miller and Bregman 2015 as MWG1 uses it, M_hot(<r) = 4.3e10 (r / 250 kpc)^1.5
  Msun added to the baryons before nu (raises the line).
Each two-sided bracket (B5, B6) counts as two brackets. Reported, not brackets: FW rc case; Table 4 joint graded with
the same rule (NFW-dependent, report only); line at RAW1-rounded a0.

## 8. Known answers (the script stops before any word if one fails)

- KA1 raw1_model reproduced at RAW1-rounded a0 (a0_mult 1): FW census 80 kpc canonical 5.6905 and alt 6.2183
  (each within 5e-4), 30 kpc 2.331 / 2.526, 50 kpc 3.683 / 4.012; FW rc 30 kpc 2.644 / 2.725, 50 kpc 4.143 / 4.308
  (each within 2e-3) (RAW1 raw1.out K4 and the direct-Jeans table).
- KA2 SI: at 30 kpc FW census canonical, g r^2 / G / Msun computed here equals M_of_g to 1e-9 relative, with
  G = 6.674e-11, kpc = 3.0857e19 m, Msun = 1.989e30 kg.
- KA3 DESI conversion in SI: M(<80) = 6.36e11 Msun gives v_c = sqrt(G M / r) = 185 +/- 1 km/s.
- KA4 the zip is the paper's: fig11 "total" at 80 kpc equals Table 4 (6.36, 16th 5.88, 84th 6.89) within 0.01, and at
  30 kpc (2.65) within 0.01; the zip's sha256 equals section 2.
- KA5 NMB1's NIMBLE values at 30 / 80 kpc (section 1) reproduced from fig10 within 0.002.

## 9. Twins and mutations (reported; a failed one is stated in RESULT, it does not stop the run)

- TW0 null twin, must NOT bite: D replaced by the FW census line itself (each footing), sigmas unchanged: all 13 PASS.
- TW1 noisy null twin, must NOT bite: D = FW census line + an independent Gaussian draw at each radius with sd s_D
  (200 seeds): row passes in at least 80 per cent of draws.
- MU1 mutation, must bite: the framework mass x 0.8 (both cases, both footings): row STILL FAILS with LOW at >= 1
  radius on each footing.
- MU2 mutation, must bite: D x 1.5 at r >= 50 kpc: LOW at every radius >= 50 kpc on both footings.

## 10. What this lane cannot settle (stated now)

The 13 radii are correlated; no radius-to-radius covariance is published, so no single significance is formed.
s_D is the joint's calibrated error, not a NIMBLE-only error (NMB1 found NIMBLE-only 0.057 dex at 80 vs Table 4's
0.0345), so sigma is if anything small at 80. The NIMBLE curves are bias-corrected on AuriDESI (LCDM haloes); B1
undoes only the median correction. Spherical Jeans throughout (DESI's assumption, not tested here). The baryon
model is the McMillan 2017 census; its own uncertainty enters only as the 10 per cent s_FW. The no-field line is
the owner's actual-field reading; the record's earlier field (0.01273) is not graded here. DR2 data are not public;
only published curves are used.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

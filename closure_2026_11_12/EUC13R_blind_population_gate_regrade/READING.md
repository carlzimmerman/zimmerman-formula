# EUC13R (BLIND RE-GRADE OF EUC13, POPULATION SOURCE GATE): READING

2026-11-12. Committed alone, before any EUC13R script exists and before any EUC13R number is computed. TEST lane.
kappa = 1/2 FITTED; not theory closed. Adopts nothing. A population gate grades a modelled source population, not
measured sources; it is weaker evidence than row-level redshifts, and EUC1-F (row-level source redshifts) stays the gate
that matters. No outcome of this re-grade is a pass of the theory. Footings canonical a0 = 9.3603e-11 / alt
1.132e-10 m/s^2, never pooled.

## 0. Blindness disclosure

The lead's statement, verbatim: "EUC13 has landed with a gate word and a second-statistic word. The lead knows them and
its numbers and has not passed them to me."

Exposure, stated exactly. At session start (2026-11-12, about 20:00 local), before I read any file, my start-up context
listed recent commit subjects. The newest one, commit ba46986e1d ("EUC13 RERUN_AND_IDS.md: ..."), contains the words
"words reproduce, EUC13-P NO VERDICT / NO VERDICT and f25 CEILING BROKEN / CEILING BROKEN". So I have seen EUC13's gate
word (NO VERDICT / NO VERDICT) and second-statistic word (CEILING BROKEN / CEILING BROKEN). The same subject says its
re-run reproduced "three JSON, two CSV and two output files", that a COSMOS2020 counts table of 14,400 cells exists
(120 x 120), and that "the SLACS figure quoted in RESULT.md section 7 is on the record's older mass convention". I saw no
EUC13 number other than those. The start-up context also carried a memory-index line saying EUC1 on 3,192 lenses read
NO VERDICT / NO VERDICT with the lenses "at the law's saturation ceiling", and that EUC3's grade-X non-lenses pass a
rule at 1.3 % vs 1.5 %. I have not opened anything in the EUC13 folder except FROZEN_CRITERIA.md, nor any other lane's
files except EUC1's FROZEN_CRITERIA.md. I read the raw-data MANIFEST under `_external_data/euc13_population_gate/`
(written by EUC13's fetch: URLs, byte sizes, hashes, the note that seven first-pass slices were server error pages); it
holds no outcome. Numbers I know from the frozen criteria text itself (§8 there): EUC1 conditional readings +0.146 /
+0.125 (z_s = 3), +0.232 / +0.213 (z_s ~ 2); EUC10 Part B AGEL +0.238 / +0.220, SLF IV +0.298 / +0.282; EUC1 f25 at
z_s 2 / 2.5 / 3 / 4 canonical 0.47 / 0.37 / 0.32 / 0.28; EUC10 sample medians z_s 1.95 (AGEL) / 1.43 (SLF IV).
Because I saw the two words, my hand estimate (§9) is not independent of them and is labelled so. The value of this
re-grade is that every number is recomputed by code written here from the criteria text.

## 1. Sample P and the statistic b (from EUC1's frozen criteria, re-implemented)

- P: key catalogue rows with lens_grade == 'A', lens_model_success True, final_sample True, joined on the identifier
  to the object catalogue with large_system_warning False; and effective Einstein radius > 0, effective radius > 0,
  0.6 <= Sersic n <= 10, median photo-z > 0, log survived mass > 0. Expected N = 3,192 (a known value; mismatch is a
  failed instrument check).
- Cosmology flat, H0 = 67.74, Om = 0.3089, radiation neglected, distances by numerical integration. R_E = theta_E,eff
  x D_A(z_l); R_e = theta_e x D_A(z_l); M* = 10^log_survived_mass_med (Salpeter); Prugniel-Simien deprojection of the
  Sersic light with p = 1 - 0.6097/n + 0.05463/n^2 and exact b_n (median of Gamma(2n)).
- Law S: g = (g_N/2)(1 + sqrt(1 + 4 a0/g_N)). M_2D(<R) = (R^2/G) int_R^{rmax} g dr / sqrt(r^2 - R^2), rmax = 1e6 kpc,
  evaluated with r = R cosh u and Gauss-Legendre in u (my own code).
- b = log10 B with M_2D,law(<R_E; B M*) = pi R_E^2 Sigma_cr(z_l, z_s). Source-free value: z_s = 1100.
- My speed device (not the criteria's x-table, which belongs to EUC13's code): per lens, log10 M_2D(<R_E) tabulated
  against b on a grid b = -1.5 .. +2.5 step 0.05 and inverted by linear interpolation for any target; beyond the grid,
  a direct bisection. It is held to the criteria's KA5 tolerance: max |Delta b| <= 0.003 against direct solves on 300
  random (lens, z_s) pairs per footing. The newton twin uses the exact Newtonian scaling (M_2D proportional to B).

## 2. Members as I read them

M1 AGEL DR2 (N 90) and M2 DESI SLF IV MUSE (N 49). The criteria take their rows from an EUC10 file I may not open, so
I parse the LaTeX myself. Rules, fixed now, tried in order; the first giving the stated N is used, and if none does the
first is used and the mismatch is disclosed:
- AGEL (tables redshifts_part1/2): one row per system, the 'A' arc (main arc); A1: source flag >= 2 and a deflector
  redshift given (own or literature '^'); A2: as A1 but any arc of the system with flag >= 2 (the highest-flag arc,
  ties to A); A3: as A1 with flag >= 1.
- SLF IV (main.tex, table "Confirmed lens systems"): lens z = first 'Lens'/'Lens 1' row; S1: primary source row = first
  row named Source/Source A/Source A1/Source B1 in the system, kept if its Q_z <= 2; S2: first source row with Q_z <= 2;
  S3: S1 and the lens row's Q_z <= 2. 'Foreground', 'Member', 'Galaxy n', 'Quasar', 'Object X' rows are not sources.
Recipe per draw: for each P lens the 10 published systems nearest in z_l (stable sort), one drawn at random, kept if
z_s > z_l + 0.2, else redrawn, at most 20 tries, else the lens is dropped from that realisation; b_med over kept lenses.

M3 forward model, per P lens, on z = 0.025 .. 5.975 (0.05 bins, centres), restricted to bin centres >= z_l + 0.2
(and <= 6.0):
1. m_arc = 23.9 - 2.5 log10(r F_L), F_L = flux_detection_total (uJy) of the MER object_id equal to the lens's
   MER_object_id in any `nisp_tables/mer_*.csv`, r = eclipse_vis_ratio_ls_l > 0. Lenses without both: per realisation
   m_arc from one of the 20 P lenses with an m_arc nearest in (z_l/0.1, log10 theta_E/0.1) (Euclidean distance), drawn
   uniformly. Implementation: a predictive is built for each of the 20 candidate donors (own z_l, own weight, donor
   m_arc), and each draw picks one.
2. N(m, z) from the raw COSMOS2020 slices: rows with FlagCOMBINED = 0, numeric HSCimagAuto and lpzBEST, 0 <= lpzBEST <
   6.0, 16.0 <= m < 28.0. Adjacent slices share a boundary magnitude; each slice keeps lo <= m < hi, the last slice
   lo <= m <= hi. Bins 0.1 mag x 0.05 in z (120 x 120).
3. n(z | m) for a window m +- 0.25: each 0.1-mag bin weighted by its exact overlap with [m - 0.25, m + 0.25]. mu = 3
   and mu = 10: m_int = m_arc + 2.5 log10 mu, n normalised over z. mu marginal: n(z) = sum over a 400-point log grid in
   mu on [2, 30] of p(mu) dmu N(window(m_int(mu)), z), p proportional to mu^-3, not normalised per magnitude. Any m_int
   > 27.5 is evaluated at 27.5; the weight fraction so clamped is reported (for fixed mu: the fraction of lenses).
4. Weights: sis w = (D_ls/D_s)^2. full: theta_E(z_s; B) from M_2D(<R; B M*) = pi R^2 Sigma_cr(z_l, z_s) on R = f R_E,
   f = 0.2 .. 5 (31 log points), mean enclosed density log-interpolated, capped at the grid ends; w = R^2. B_i self-
   consistent: start b at z_s = 1100; B_i = 10^(weighted median of b_i(z) under p_i), three iterations, per footing and
   per mu setting; the largest |Delta b| of the last iteration is reported. Weighted median: the first bin where the
   cumulative weight reaches 1/2 (bin-centre value of b_i).
5. Readings with B fixed at b = 0 and b = 0.5 (full, mu marginal).
Draws: bin chosen from p_i, z_s = bin centre.

## 3. Validation of M3 (sis weight), as I read it

- V1: of M2's systems, those whose primary source row gives a magnitude: DESI i if given, else -2.5 log10 of the mean
  of the r and z fluxes (both needed). Lens z from the same table. Mixture (1/N) sum p_k; CDF piecewise linear within
  bins. Passes if |median(mixture) - median(observed z_s)| <= 0.25 and the one-sample KS p of the observed z_s against
  the mixture CDF > 0.01.
- V2: the criteria name 14 lenses from an EUC10 file I may not open. Resolution (a deviation, stated): I rebuild the
  list myself by matching ECLIPSE grade A/B positions (key catalogue) within 2.0 arcsec to AGEL DR2 (any arc with
  flag >= 2), SLF IV (any source row Q_z <= 2) and SLACS (Auger 2009) systems, plus EUC2's three pairs named in the
  criteria (L012826 1.1374, L014688 0.9926, L006816 0.4685). Evaluable if the lens has an m_arc (step 1, no donor) and a
  key-catalogue photo-z; lens z = desi_deflector_specz if present, else photo-z. PIT u_k = CDF_k(z_s,true). Passes if
  KS p of {u_k} against uniform > 0.01 and at most one lens has min(u, 1-u) < 0.005. Fewer than 5 evaluable: V2 not
  applied, and then a mu setting survives on V1 alone (my reading of "not applied").
- A mu setting survives if it passes V1 and V2 (or V1 when V2 is not applied); full and sis survive or drop together.
  None survives: M3 dropped, gate on M1 and M2, flagged. Validation printed before any P number of M3.

## 4. Intervals

400 replicates, seed 20261112 (my own generator use; draws will not match EUC13's bit for bit). Each: P resampled with
replacement; error realisation r mod 40 (40 precomputed); one source draw per lens; for M1/M2 the published sample
resampled before matching. Error realisation (EUC1 run 6 as I read it): z_l' = z_l + N(0,1)(max70 - min70)/(2 x 1.04),
floored at 0.05; log M*' = log M* + N(0,1) x (low + upp)/2; theta_E' and theta_e' = value + N(0,1) x half the 1-sigma
bound width, floored at 10 % of the value; Sersic n unchanged. M3's predictive stays at catalogued values; a drawn z_s
< z_l' + 0.2 is redrawn (at most 20 tries, else dropped). Point estimate: catalogued values, 200 draws, median of the
200 statistics. Interval: point + (q2.5 - q50, q97.5 - q50) of the replicates; raw percentiles beside it. M3 interval =
envelope over surviving settings. Same for f25 (fraction with b > 0.25).

## 5. Gate and second statistic (per footing)

EUC13-P: HOLDS if every surviving member's upper bound on b_med <= 0.15; FAILS if every lower bound >= 0.25; else NO
VERDICT. f25: CEILING BROKEN if every lower bound >= 0.25; CEILING HOLDS if every upper bound <= 0.10; else NO VERDICT.
Any failed check or known answer: NOT EVALUABLE.

## 6. Readings

theta_E classes < 1.0, 1.0-1.3, >= 1.3 arcsec, per member, b_med with the same interval, against EUC5's bands as the
criteria list them. Ambiguity: "inside / above / below" read on the point estimate against the band; the interval is
printed beside. Each member's median z_s on P; M3 per setting; B-fixed readings.

## 7. Known answers and checks

KA1 SLACS true z_s, Auger cosmology (H0 70, Om 0.3) for Re(V) in kpc, R_E and log Einstein mass from the table, M* =
Fs x M_E / L_deV(<R_E): +0.082 / +0.070 +- 0.003. KA2 P source-free b_med -0.019 / -0.044 +- 0.001, N 3,192. KA3 my
M1/M2 by the EUC10 recipe with direct solves on each (lens, z_s) pair: +0.238 / +0.220, +0.298 / +0.282 +- 0.002.
If my parsed samples differ from EUC10's (N or rows), a KA3 miss is still a miss: the strict word is NOT EVALUABLE, and
I then also report, labelled as a reading and not a word, what the gate reads with KA3 waived. KA4: the same through my
table path, within 0.005 of my KA3. KA5 as in §1. KA6 COSMOS median lpzBEST at 23.5 < i < 24.5 in [0.6, 1.6]. My own
analytic checks: point mass M_2D = M to 1e-6 (a0 -> 0), deep-regime point mass M_2D = (pi/2 - small rmax term) R
sqrt(a0 G M)/G to 1e-4, Prugniel-Simien M_2D against a direct line-of-sight integral of the 3D density to 1e-3, and PS
against the exact 2D Sersic light inside R (reported, a few % expected). Mutation twin EUC13R_MUTATE=newton (a0 =
1e-30): every member's b_med point must rise on both footings; the twin exits 1 if so, 3 if not.

## 8. Order

READING (this file, alone) -> code and runs -> RESULT_BLIND.md -> only then EUC13's AMENDMENT, RESULT, RERUN note and
outputs -> RESULT.md with a COMPARISON section. Changes after seeing my own numbers go in an AMENDMENT file, post hoc.

## 9. Hand estimate (NOT independent: I saw EUC13's two words)

M1, M2 near EUC10's +0.24 / +0.22 and +0.30 / +0.28, intervals perhaps +-0.03 to 0.05, so AGEL's lower bound sits
below 0.25. M3: Euclid arcs about m 23-24 observed, intrinsic 25-26 after magnification, COSMOS n(z) there peaks near
z 1-1.5 and the lensing weight pushes it up, median z_s 1.5-2, b_med about +0.25 to +0.35. Gate: NO VERDICT both
footings (no member's upper bound near 0.15; AGEL's lower bound under 0.25). f25 above 0.3 in every member at
z_s ~ 2: CEILING BROKEN both footings.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.

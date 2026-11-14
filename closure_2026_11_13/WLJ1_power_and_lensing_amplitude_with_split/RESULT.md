# WLJ1 RESULT: rows 24 (matter-power redistribution) and 25 (weak-lensing amplitude) computed with the crossing-speed split

TEST lane. Adopts nothing, relabels nothing. Criteria 03f9823de7; AMENDMENT A1 49f8ed445d (a rounding tolerance); AMENDMENT A2
1c36721822 (which DES rows gate a known answer). Footings canonical / alt, never pooled. Cold dark energy is a gravitating
field component, not a particle. kappa = 1/2 and 5.41 are FITTED. Nothing here says the data favour the framework.

## Labels (graded: f = 1.25, 2, 3; canonical / alt)

**As frozen** (`wlj1_grade_asfrozen.out`): row 24 is **NO VERDICT** on canonical at every f (KA-R in C4 read 1 + 2.2e-16 where
"exactly 1" was frozen) and **ROW HOLDS WITH THE SPLIT** on alt; row 25 is **NO VERDICT** on both footings at every f.

**Under A1 + A2** (`wlj1_grade.out`):

| row / gate | f 1.25 | f 2 | f 3 | adopted form (no split) | differs from it? |
|---|---|---|---|---|---|
| **Row 24** | **HOLDS / HOLDS** | **HOLDS / HOLDS** | **HOLDS / HOLDS** | HOLDS / HOLDS | no |
| G-C4 CO1 C4 (PR4 lensing) | EQ. REF (HOLDS) / same | EQ. REF (HOLDS) / same | EQ. REF (HOLDS) / same | HOLDS | no |
| G-C5 CO1 C5 (raw KiDS d_cold) | EQ. REF (HOLDS) / same | EQ. REF (HOLDS) / same | EQ. REF (HOLDS) / same | HOLDS | no |
| CO1's row rule (C1-C4 PASS, C5 CONSISTENT) | EQ. REF (HOLDS) / same | EQ. REF (HOLDS) / same | EQ. REF (HOLDS) / same | HOLDS | no |
| G-HLF1 HLF1 Part A (own halo list) | EQ. REF (HOLDS) / same | EQ. REF (HOLDS) / same | EQ. REF (HOLDS) / same | HOLDS | no |
| **Row 25** | **NO VERDICT / NO VERDICT** | **NO VERDICT / NO VERDICT** | **NO VERDICT / NO VERDICT** | FAILS / FAILS | yes, not a hold |
| G-P4 CO2 P4 (raw KiDS at the pinned sigma8) | NO VERDICT [TENSION] / same | NO VERDICT [TENSION] / same | NO VERDICT [TENSION] / same | FAILS [EXCLUDED AT 3 SIGMA] | yes, not a hold |
| G-KL1 KL1 Part C gate | NO VERDICT [GAP STAYS; TW-L does not bite] / same | same / same | same / same | FAILS [GAP STAYS] | yes, not a hold |
| G-BX1 BX1 gate | HOLDS / NO VERDICT [KA-G6] | EQ. REF (HOLDS) / NO VERDICT | EQ. REF (HOLDS) / NO VERDICT | HOLDS / NO VERDICT | no |
| G-LWB1 LWB1 J | EQ. REF (HOLDS) / same | EQ. REF (HOLDS, FRAGILE) / same | EQ. REF (HOLDS) / same | HOLDS, FRAGILE | no |
| G-LWB1R LWB1R J | EQ. REF (HOLDS) / same | EQ. REF (HOLDS, FRAGILE) / same | EQ. REF (HOLDS) / same | HOLDS, FRAGILE | no |

EQ. REF = EQUALS THE REFERENCE THERE; HOLDS = ROW HOLDS WITH THE SPLIT; FAILS = ROW FAILS WITH THE SPLIT. FRAGILE at f 2 on
LWB1 / LWB1R is the same set of brackets that makes the adopted form and the reference FRAGILE there (point-mass term, R_min 5
and 12; LWB1 also pi_max 300 and N = 1); those brackets were run at f = 2 only. **No HOLDS here differs from the adopted form's
word, so there is no hit needing a blind re-grade.** The two words that differ (P4, KL1) are NO VERDICT, not holds.

Reported only: f = infinity in slow haloes reads row 24 NO VERDICT on both footings (HLF1 NOT RESOLVED: the own list's mass
range carries f_res 0.40 / 0.49 < 0.5 of its signal) and row 25 NO VERDICT / FAILS (alt P4 p 0.00258, EXCLUDED). Lane-as-frozen
notes, independent of the layout and carried unchanged for all cases: CO1 (M4 as written), HLF1 (MA1), KL1 (MC1), BX1 (KA3,
MB2), LWB1 (KA1) read NO VERDICT as frozen in their own lanes.

## The split's matter power (`wlj1_hm.out`)

R_cold = the candidate's nonlinear matter power over the reference's (same baryons, same halo list); k in h/Mpc.

| z | footing | switch: v*(z), M200c (Msun/h) | haloes on the reference (of 321) | adopted form k 0.1 / 0.3 / 1 / 3 / 10 | split f 1.25 | split f 2 | split f 3 | f infinity (reported) |
|---|---|---|---|---|---|---|---|---|
| 0 | can | 668.5 km/s, 6.9e13 | 81 | 1.0001 / 1.0006 / 1.0059 / 1.0509 / 0.9871 | 1.0000 / 1.0001 / 1.0010 / 1.0141 / 1.0923 | 1.0000 / 1.0001 / 1.0009 / 1.0135 / 1.0690 | 1.0000 / 1.0000 / 1.0008 / 1.0116 / 1.0341 | 1.0000 / 1.0003 / 1.0024 / 1.0303 / 1.1184 |
| 0 | alt | 807.9 km/s, 1.2e14 | 71 | 1.0001 / 1.0009 / 1.0101 / 1.0877 / 1.0595 | 1.0000 / 1.0001 / 1.0022 / 1.0297 / 1.1020 | 1.0000 / 1.0001 / 1.0022 / 1.0287 / 1.0698 | 1.0000 / 1.0001 / 1.0020 / 1.0260 / 1.0316 | 1.0001 / 1.0005 / 1.0045 / 1.0560 / 1.1479 |
| 0.5 | can | 505.5 km/s, 2.3e13 | 103 | 1.0000 / 1.0003 / 1.0032 / 1.0236 / 0.8582 | 1.0000 / 1.0000 / 1.0005 / 1.0066 / 1.0278 | 1.0000 / 1.0000 / 1.0005 / 1.0057 / 0.9995 | 1.0000 / 1.0000 / 1.0002 / 1.0028 / 0.9449 | 1.0000 / 1.0003 / 1.0023 / 1.0188 / 0.9931 |
| 0.5 | alt | 610.9 km/s, 4.0e13 | 93 | 1.0001 / 1.0007 / 1.0085 / 1.0591 / 0.9181 | 1.0000 / 1.0001 / 1.0014 / 1.0161 / 1.0359 | 1.0000 / 1.0001 / 1.0013 / 1.0149 / 0.9998 | 1.0000 / 1.0000 / 1.0010 / 1.0108 / 0.9367 | 1.0001 / 1.0005 / 1.0043 / 1.0386 / 1.0207 |
| 1 | can | 373.3 km/s, 6.8e12 | 126 | 1.0000 / 1.0001 / 0.9995 / 0.9930 / 0.7967 | 1.0000 / 1.0000 / 1.0001 / 1.0006 / 0.9904 | 1.0000 / 1.0000 / 1.0000 / 0.9996 / 0.9639 | 1.0000 / 1.0000 / 0.9997 / 0.9960 / 0.9027 | 1.0000 / 1.0002 / 1.0013 / 1.0036 / 0.9148 |
| 1 | alt | 451.1 km/s, 1.2e13 | 116 | 1.0000 / 1.0004 / 1.0042 / 1.0235 / 0.8457 | 1.0000 / 1.0000 / 1.0003 / 1.0034 / 1.0015 | 1.0000 / 1.0000 / 1.0002 / 1.0019 / 0.9663 | 1.0000 / 1.0000 / 0.9997 / 0.9966 / 0.8915 | 1.0000 / 1.0003 / 1.0032 / 1.0172 / 0.9402 |

- The switch mass is the analytic M200c at v*(z) (10 G M H(z) = v*^3); the lightest grid halo above it is within 3 %. It falls to
  2.2e12 / 3.9e12 Msun/h at z 1.5 and 1.6e11 / 2.8e11 at z 3 (where 192 / 182 haloes take the reference).
- At z = 0 the split keeps 15 to 27 % (canonical) and 22 to 33 % (alt) of the adopted form's excess at k 1 to 3: the clusters
  above v* carried the rest. At k 10 the split's ratio sits above the adopted form's at z 0 (galaxy-scale haloes settled inside
  f R_fold, no cluster cores to offset them). The full-layout (f infinity) split keeps about 40 to 65 % of the adopted form's
  excess at k 1 to 3; truncating at f R_fold matters at z = 0 because groups and the galaxies' settled radii fall inside r_ta.
- From z 1.5 up the split is within 0.06 % of the reference at k <= 1 and 0.8 % at k 3 for every graded f (the adopted form departs
  by 3 to 17 % at k 3).
- R_tot (the case over the gravity-only spectrum) at z 0, k 1 / 3: reference 0.9998 / 0.9784, adopted 1.0033 / 1.0282 (can),
  split f 2 0.9984 / 0.9916 (can), 0.9997 / 1.0068 (alt).

## The gate numbers (reference / adopted form / split f 1.25, 2, 3; canonical, then alt)

| gate statistic | reference | adopted form | split f 1.25 | f 2 | f 3 | gate line |
|---|---|---|---|---|---|---|
| C4 r_eff - 1, can | 2e-16 | +3.19e-5 | +3.5e-6 | +3.1e-6 | +1.9e-6 | 0.0481 |
| C4 r_eff - 1, alt | 0 | +4.96e-5 | +7.3e-6 | +6.7e-6 | +5.3e-6 | 0.0481 |
| C5 d_cold (KiDS, 104 points), can | 0 | +1.148 | +0.234 | +0.219 | +0.184 | 4 / 9 |
| C5 d_cold, alt | 0 | +2.206 | +0.542 | +0.517 | +0.457 | 4 / 9 |
| HLF1 own-list d_cold, can / alt | 0 / 0 | +1.153 / +2.282 | +0.189 / +0.380 | +0.175 / +0.355 | +0.139 / +0.298 | 4 |
| HLF1 f_res at k 1, can / alt | - | 0.604 / 0.551 | 0.969 / 0.988 | 0.932 / 0.963 | 0.835 / 0.896 | >= 0.5 |
| P4 chi^2 (p), can | 156.18 (0.00315) | 157.89 (0.00258) | 156.55 (0.00301) | 156.53 (0.00302) | 156.47 (0.00304) | p 0.0027 / 0.05 |
| P4 chi^2 (p), alt | 156.16 (0.00316) | 159.35 (0.00212) | 157.00 (0.00286) | 156.96 (0.00287) | 156.87 (0.00291) | p 0.0027 / 0.05 |
| KiDS best sigma8, pinned minus best (widths), can / alt | 5.41 / 5.41 | 5.62 / 5.78 | 5.46 / 5.52 | 5.46 / 5.52 | 5.45 / 5.51 | reported |
| KL1 g: Legacy / DES polished, can | +1.48 / +2.16 | +1.71 / +2.18 | +1.54 / +2.19 | +1.53 / +2.20 | +1.53 / +2.21 | +-2 |
| KL1 g: Legacy / DES polished, alt | +1.50 / +2.11 | +1.88 / +2.23 | +1.64 / +2.08 | +1.64 / +2.23 | +1.63 / +2.20 | +-2 |
| BX1 g: Legacy / DES polished, can | +1.31 / +1.83 | +1.51 / +1.85 | +1.37 / +1.86 | +1.36 / +1.83 | +1.35 / +1.83 | +-2 |
| BX1 g: Legacy / DES polished, alt | +1.33 / +1.76 | +1.72 / +1.81 | +1.45 / +1.84 | +1.44 / +1.85 | +1.43 / +1.83 | +-2 |
| KiDS-1000 g (KL1 gate, reported), can / alt | +3.55 / +3.54 | +3.72 / +3.85 | +3.59 / +3.63 | +3.59 / +3.63 | +3.58 / +3.62 | reported |
| LWB1 J g, can / alt | +0.895 / +0.861 | +0.902 / +0.872 | +0.896 / +0.863 | +0.896 / +0.862 | +0.895 / +0.862 | +-2 |
| LWB1R J g, can / alt | +0.904 / +0.869 | +0.912 / +0.872 | +0.892 / +0.857 | +0.895 / +0.861 | +0.899 / +0.865 | +-2 |

- The C5 robust variants (widen2, noIA, DESI, fade) of the split are all below 1.2 (largest noIA +0.51 / +1.10 at f 1.25); every
  tooth reads NOT VISIBLE (1.04 to 1.06). DES Y3 d_cold (reported): -0.015 / -0.027 at f 2.
- KL1's DES reading is GAP STAYS for every case, the pure reference included (+2.16 / +2.11): the gap is the one any cold
  component fitted to the CMB carries, and the layout moves it by at most 0.04 widths in either direction.

## Brackets

- **z bracket** (each case's own ratio at z 0, 0.5, 1 for C5 and P4; R(k, z) to z 3 for C4): no word moves. Split f 2: C5 +0.181 /
  +0.430, P4 p 0.00303 / 0.00291 (TENSION); C4 r_eff - 1 +1.3e-6 / +3.3e-6. Adopted form: P4 p 0.00270 / 0.00221 (EXCLUDED).
- **CO1's layout brackets** on C5 for the split (f 1.25 to 3): d_cold from -0.27 (core prefactor 0) to +0.89 (c(M) x 0.7, alt);
  all CONSISTENT. The adopted form's range is -2.85 to +4.00 (alt c(M) x 0.7 +3.997). CO1's KiDS amplitude bracket: +0.30 to
  +0.38 / +0.75 to +0.88. KA-H6: every bracket reproduces CO1's stored arrays to 3e-15.
- **CO2's brackets** on P4 for the split: one 0.06 eV neutrino p 0.0101 / 0.0097 (TENSION); its own prefactor-0 layout 0.0032 /
  0.0033 (TENSION); constant factor 0.0051 / 0.0049 (TENSION); CO1's unpinned sigma8 0.0005 / 0.0003 (EXCLUDED). The split's
  word is NO VERDICT, so FRAGILE is not attached; the unpinned bracket gives EXCLUDED for every case, the reference included.
- **KL1:** additive transfer at f 2 GAP STAYS (DES polished +2.26 / +2.17). C0 edges R2 / R2b (reported under A2): AMPLITUDE CONSISTENT /
  GAP STAYS for reference, adopted form and split alike. **BX1:** C3b_BX1 Legacy +1.24 / +1.33 at f 2; additive transfer
  AMPLITUDE CONSISTENT.
- **LWB1 / LWB1R at f 2:** the point-mass term, R_min 5 and 12 (and LWB1's pi_max 300, N = 1) move J outside CONSISTENT for the
  split exactly as for the adopted form and the reference. pi_max 80 / 100 never change J's label.

## Known answers

All pass under A1 + A2 except KA-G6 on alt. KA-H1 (adopted form against CO1's stored ratios) 1.7e-15; KA-H2 nulls 7e-16 and 0;
KA-H3 (JNT2's stored f 2 split at z 2.2 / 4.4) 0 exactly; KA-H4 mass conservation 6.4e-16; KA-H5 (HLF1's own list) 1.6e-15, and my
f_res for the adopted form equals HLF1's (0.604 / 0.551); KA-H6 every bracket. KA-G1 (CO1 C5) 3e-6; KA-G2 (CO1 C4) exact;
KA-G3 (CO2 P4 and its brackets) 2e-5; KA-G4 (HLF1) 2e-8; KA-G7 / KA-G8 (LWB1 / LWB1R) 1e-13. KA-G5 / KA-G6: canonical bit for
bit; alt Legacy and KiDS-1000 to 1e-6, alt DES frozen-scan rows off by 0.03 to 1.1 widths (A2: reported), alt polished DES
+2.2286 against KL1's +2.2305 (PASS) but BX1's polished +1.8098 against +1.8326 (0.023 > 0.01: **FAIL, so G-BX1 alt is NO
VERDICT for every case**, adopted form included). KA-R: canonical C4 1 + 2.2e-16 (fails as frozen; A1 tolerance 1e-12).

## Twins

- **TW-B (boundary 2 v*, f 2) bites** on both footings: reference haloes at z 0 81 -> 44 / 71 -> 34; |R_cold(k 3) - 1| 0.0135 ->
  0.0417 / 0.0287 -> 0.0629. On the gates it moves C5 to +0.892 / +1.497 and P4 to p 0.00268 / 0.00242 (EXCLUDED), i.e. back
  toward the adopted form.
- **TW-L (layout change doubled, f 2)** bites on C4, C5, P4 and LWB1R on both footings and on BX1 canonical. It **does not bite on
  KL1** (DES polished g: split +2.199 / +2.229, doubled +2.190 / +2.181, reference +2.159 / +2.105): the polished DES scan
  scatters by about 0.05 to 0.15 widths from case to case, more than the layout moves it. It does not bite on BX1 alt. On LWB1 the
  split equals the reference to 0.002 widths, so the gate is reported as unable to see the layout at all.

## What was left out

- HLF1 Part B (the forest at matter level) is row 21; for the split it is JNT2 / JNT2R's (scorecard: "TRIVIAL to f 2"). Not rerun.
- KL1, BX1, LWB1, LWB1R were run held in z only; their brackets at f 2 only. CO1's brackets "regime boundary at M200m 1e13" and
  "CFG556's kernel" are not in FRZ1's layout and were not run. LWB1's CAMB halofit bracket and LWB1R's other brackets were not
  run. The unsplit settled family (U1.25 to U3) was computed for the halo model, C4, C5 and P4 only (`wlj1_shear.out`).
- KL1 / BX1's gate R is A3_AD (RB1's gas with the adiabatic response); the split was transferred onto it as a ratio (and, as a
  bracket, additively), not rebuilt with RB1's gas.
- The halo list, c(M) and baryon shapes stay inherited (Tinker, Duffy-like c(M), CFG556's declared baryons), as in CO1; the base
  spectra are one gravity-only 100 Mpc/h box (C5, P4) or BX1's paired splice (BX1, LWB). Run logs are not committed (they carry
  machine paths); the `.out` files hold every printed line.

## What the split does, in plain words

The split hands clusters (and, at z ~ 1, groups) back to the cold reference layout, so most of the adopted form's
redistribution of matter power disappears: at k 1 to 3 h/Mpc today it keeps 15 to 33 % of the adopted form's excess,
and by z 1.5 almost none. Every redistribution gate the record froze was already passed with room by the adopted form, and
the split moves each statistic toward the pure reference (raw KiDS d_cold from 1.1 / 2.2 down to about 0.2 / 0.5 against a
line of 4), so row 24 holds exactly as it did, and the gates cannot tell the split from no redistribution at all. On the
weak-lensing amplitude the split does not touch the real problem: raw KiDS still wants sigma8 about 5.5 KiDS widths below the
CMB-pinned value, and DES Y3 stays above the two-width line under KL1's gate for the split, the adopted form and the pure
reference alike. The only word that changes is CO2's absolute-fit p, which the adopted form missed by 0.0001 to 0.0006 and the
split, sitting with the reference, clears into TENSION; that is a removal of a small layout penalty, not a relief of the
amplitude tension, and it is the same reading CO2's own realisation-noise check already gave the adopted form. Nothing here is
a hit for the split.

## Commit ids and the lead's re-run (2026-11-14)

- Criteria 03f9823de7 (origin 61016f6d85); amendment A1 49f8ed445d (origin c9de0dc2c2); amendment A2 1c36721822 (origin 22c8e0b97d);
  scripts and outputs 6cce4d7328 (origin 99095e5962); result b40ed0b7de (origin c07c41ef44).
- Correction: the first version of this note (18986299e8) gave five origin ids that belong to unrelated commits, because
  the push it described had not happened when the note was written. The ids above are the right ones.
- The lead re-ran, from a copy of the tracked files at the same folder depth:
  - `wlj1_hm.py` (the split's matter-power ratios and the boundary twin): both JSON files equal byte for byte; the two
    logs differ only in elapsed-seconds stamps;
  - `wlj1_grade.py`, with and without `--as-frozen`, on the stored stage outputs: all six outputs equal byte for byte.
- Not re-run by the lead: the C4, shear, KL1 / BX1 and LWB stages (hours of single-thread scans).
- A reproduction, not an independent re-grade. No number or label changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

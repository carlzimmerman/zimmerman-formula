# HIS1R RESULT (blind regrade of HIS1, before HIS1's RESULT.md is opened) (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Reading: `READING.md` (commit 4e023f8e76,
alone, before any script or number). Code written from scratch: `his1r.py` -> `his1r.json` / `his1r.out`;
`--mutate` -> `his1r_MUTATE.json` / `his1r_MUTATE.out`. Runtime 8 s, one thread.

**Blindness is compromised, and this is stated first.** HIS1's result commit subjects (its label and its main numbers)
were in the context this session started with, before any reading was chosen (READING.md, exposure 1). The readings were
fixed from the criteria text and committed before any number. The numbers below are from HIS1R's own code. They cannot
show independence of judgement on the points the commit subjects named. They do show the arithmetic.

## Label (per footing)

| footing | label | failing test, by how much | others | force reading | no rule (seed 7) |
|---|---|---|---|---|---|
| canonical (a0 9.3603e-11) | **HOLDS EXCEPT** | **H3 FAILS**: faint rotators with Ti1 < 0 (n 9) median d_L -0.278 +- 0.080 dex = -3.47 se; clauses (a) and (b) | H1, H2, H4 HOLD; **H5 NO POWER** | 1 / 5 (F5 only) | 1 / 4 (H2) |
| alt (a0 1.1312e-10) | **HOLDS EXCEPT** | **H3 FAILS**: same set, -0.315 +- 0.081 dex = -3.89 se; clauses (a) and (b) | H1, H2, H4 HOLD; **H5 NO POWER** | 1 / 5 (F5 only) | 2 / 4 (H2, H3) |

Known answers KA1-KA4 pass on both footings, so neither label is NO VERDICT. No alternative reading in READING.md moves
either label (table below).

## Numbers (canonical / alt)

- Table: 3621 rows; 3419 main points; 626 systems; 16 classes (SPARC 149 / 2700 points; faint rotators 20; tidal
  dwarfs 6; massive spirals 12; ATLAS3D 187; RC100 100; KiDS 4 bins / 60; groups 20; X-COP 7 / 129; CLASH 20 / 84; MW
  bright 11; MW ultra-faints 31; M31 33; LG field 13; Coma UDGs 11; NGC 1052 UDGs 2). Brackets: 187 atlas_salp, 15
  kids_hot (reported only).
- **H1 HOLDS / HOLDS.** Tidal dwarfs median Y +0.067, se 0.115 (+0.59 se; |Y| <= 2 se). Median d_L -0.687 / -0.725,
  se 0.115 (-6.00 / -6.33 se; below -3 se).
- **H2 HOLDS / HOLDS.** (a) systems with Y_sys < -3 e_sys: 0 of 626. (b) lowest class median Y: NGC 1052 UDGs +0.012
  (+0.05 se), tidal dwarfs +0.067 (+0.59 se); no class below -3 se. (c) DF2 Y +0.128 (+0.37 e), d_L -0.743 / -0.781
  (-2.16 / -2.27 e); DF4 Y -0.104 (-0.30 e), d_L -0.943 / -0.981 (-2.70 / -2.81 e); e 0.344 / 0.349. Both pass.
- **H3 FAILS / FAILS.** Median d_L (se, in se):

  | set | n | canonical | alt | clause |
  |---|---|---|---|---|
  | SPARC | 149 | +0.004 (0.012, +0.29) | -0.023 (0.012, -1.92) | a, b pass |
  | SPARC f_g >= 0.5 | 62 | +0.026 (0.021, +1.22) | -0.010 (0.021, -0.45) | a pass |
  | faint rotators Ti1 < 0 | 9 | **-0.278 (0.080, -3.47)** | **-0.315 (0.081, -3.89)** | **a, b fail** |
  | KiDS | 4 | +0.137 (0.109, +1.26) | +0.097 (0.109, +0.89) | b pass |
  | LG field dwarfs | 13 | -0.090 (0.062, -1.45) | -0.130 (0.060, -2.15) | b pass |
  | ATLAS3D outside Virgo | 140 | +0.081 (0.013, +6.43) | +0.069 (0.013, +5.47) | b pass |
  | MW bright dwarfs | 11 | +0.065 (0.153, +0.42) | +0.027 (0.152, +0.18) | c pass |
  | MW ultra-faints | 31 | +0.592 (0.098, +6.06) | +0.552 (0.098, +5.64) | c pass |
  | M31 dwarfs | 33 | +0.090 (0.088, +1.02) | +0.051 (0.085, +0.60) | c pass |
  | Coma UDGs | 11 | +0.319 (0.114, +2.80) | +0.280 (0.114, +2.45) | c pass |
  | groups | 20 | +0.161 (0.023, +7.06) | +0.123 (0.023, +5.40) | c pass |

  Reported: isolated fraction 9 of 20 faint rotators (9 of the 13 with a UNGC Ti1; 7 have no UNGC name: six AGC
  galaxies and F564v3). All 20: -0.239 / -0.274 (-5.31 / -6.22 se). Isolated set with M_* x 2: -0.349 / -0.387 (-4.20 /
  -4.58 se); M_* x 0.5: -0.232 / -0.270 (-3.01 / -3.46 se); distances x 0.8: -0.181 / -0.219 (-2.26 / -2.69 se);
  distances x 1.2: -0.357 / -0.395 (-4.46 / -4.86 se).
- **H4 HOLDS** (quoted from RB1's RESULT.md, no a0): X-COP last radius f_ret 1.095 [0.885, 1.259] contains 1; X-COP at
  R500 1.057 >= 1; groups 0.597 [0.556, 0.637], upper bound < 1. Beside it, from the table: X at the last point, X-COP
  median 4.940 (se 0.270; bootstrap 95 % [4.643, 5.479]); groups 9.066 (se 0.495; [8.499, 9.730]).
- **H5 NO POWER / NO POWER.** Spearman rho (p): G1 SPARC f_g +0.011 (0.90) / -0.034 (0.68); G2 faint rotators f_g
  +0.109 (0.65) / +0.113 (0.64); G3 MW bright -0.545 (0.083); G4 MW ultra-faints -0.215 (0.25); G5 M31 -0.007 (0.97);
  G6 Coma UDGs -0.391 (0.23) (G3-G6 the same on both footings). No pair is Holm-significant. The four host-distance
  pairs all lean negative, against the history sign; none is significant.
- **Force reading 1 / 5 on both.** F1 fails (tidal dwarfs -6.0 / -6.3 se from the law). F2 fails: 12 / 15 systems
  with d_L,sys < -3 e_sys (DF2 / DF4 within 3 e). F3 fails: faint rotators Ti1 < 0, ATLAS3D outside Virgo, MW
  ultra-faints, groups. F4 fails: X-COP last points median d_L +0.154 / +0.119, se 0.015. F5 passes.
- **No rule** (default_rng(7)): canonical 1 / 4 (H1 FAILS, H2 HOLDS, H3 FAILS, H5 FAILS); alt 2 / 4 (H1 FAILS, H2 HOLDS,
  H3 HOLDS, H5 FAILS). RandomState(7): 1 / 4 and 2 / 4 (H5 NO POWER in both). Seeds 1..200 holds-count histogram:
  canonical {0: 28, 1: 155, 2: 17}; alt {0: 14, 1: 80, 2: 104, 3: 2}. None reaches 4.
- Reported indicators (Spearman with d_L, not graded): SPARC Ti1 (n 31) -0.37 (p 0.038) / -0.35 (0.056); faint
  rotators Ti1 (13) -0.02 / -0.05; tidal dwarfs D_p (6) -0.09, gas share +0.54 (0.27); massive spirals f_g (12) -0.23;
  LG field mass_HI (11) -0.65 (p 0.031; their g_bar omits the gas, as the criteria say); LG field Ti1 (8) +0.17. LVD age:
  no table system has one on disk. ATLAS3D Virgo 0 / 1: +0.081 / +0.031 (canonical). CLASH high-magnification 4 / other
  16: +0.561 / +0.553 (canonical).
- ATLAS3D at Salpeter (bracket, not graded): class median Y -0.047, se 0.011 = **-4.27 se**; 1 system below -3 e_sys.
  Were this bracket the table, H2 (b) would fail.

## Alternative readings: does a label move?

| reading | canonical | alt | moves a label? |
|---|---|---|---|
| ALT-INF (drop g_obs <= 0 points) | identical | identical | no |
| ALT-ERR (law-propagated d_L errors) | FR -3.47 se; F2 count 23 | FR -3.89 se; F2 count 26 | no |
| ALT-ISO1 (Ti1 <= 0) | FR n 10, -0.254, -3.76 se | -0.291, -4.27 se | no |
| ALT-ISO2 (no Ti1 counted isolated) | FR n 16, -0.259, -4.42 se | -0.295, -5.05 se | no |
| ALT-HALF (f_g above SPARC median) | n 74, +0.49 se | -1.34 se | no |
| ALT-P (permutation p) | smallest p 0.084 | 0.084 | no |
| ALT-HOST (F3 adds tidal dwarfs, NGC 1052) | F3 still fails | same | no (force score stays 1) |
| ALT-RNG (RandomState) | no rule 1 / 4 | 2 / 4 | no (control only) |

Not readings but disclosed because they move a clause: distances x 0.8 bring the isolated faint rotators to -2.26 /
-2.69 se (H3 would hold, label HOLDS EXCEPT with H5 NO POWER and no fail); M_* x 0.5 leaves them at -3.01 se (canonical,
a 0.01 se margin). The Salpeter bracket would fail H2 (b) and make the label FAILS.

## Known answers (both footings)

- KA1 PASS: 32 class L0 offsets equal `dd1.json` LOCO L0 to 2.2e-16 (no DD1 value printed).
- KA2 PASS: inverse-variance mean of log10(Mdyn/Mbar) from Lelli+15's ratio column +0.0831 +- 0.0958 (the
  M_dyn / M_bar columns give +0.0759 +- 0.1012, reported); table Y within 0.0135 dex of log10(M_dyn/M_bar) for all six.
- KA3 PASS: (i) history truth H1, H2, H3 HOLD, F1 fails (also with groups at +0.3); (ii) force truth H1 FAILS, F1, F2,
  F3 pass, H5 NO POWER; (iii) planted gas trend H5 HOLDS.
- KA4 PASS: X_L > 0 and X_L <= sqrt(a0/g_bar) on 2001 points, 1e-15..1e-6 m/s^2.

## MUTATE (both footings)

M1 bites (H1 FAILS). **M2 does not bite** (H2 HOLDS): the first four SPARC systems are CamB, D512-2, D564-8, D631-7;
D512-2 has e_sys 0.203, so Y = -0.6 is not below -3 e_sys (-0.609); the count is 3, not 4. Disclosed, not repaired.
M3 bites (G1 rho +0.74 / +0.73, Holm-significant against the sign: H5 FAILS). M4 bites (SPARC median d_L -0.102 /
-0.139 at a0 x 2, -8.4 / -11.4 se: H3 (a) fails).

## Own checks (both footings, same outcomes)

Planted, graded correctly: H1 (tidal dwarfs at Y = 0 HOLDS; on the law FAILS; at +0.4 FAILS); H2 (a) 3 planted
systems count 3 holds, 4 count 4 fails; H2 (b) RC100 at -4 se fails, at -2 se holds; H2 (c) DF2 at -4 e fails, DF4 at
d_L +4 e fails, both at Y = 0 holds; H3 SPARC at -4 se fails (a) and (b), at +4 se fails (a) only; MW ultra-faints at
-4 se fails (c); H5 each pair alone: with the sign HOLDS, against FAILS (12 of 12); F4 X-COP on the law passes, +0.5
fails. Shuffles destroy each planted signal: indicator permuted within class -> H5 NO POWER in 99-100 of 100 seeds per
pair; labels permuted -> H1's history pattern holds in 0 of 100, the SPARC -4 se shift fails in 0 of 100, the X-COP
+0.5 shift fails F4 in 0 of 100. H2 (a) is a count with no label; its check is the 3 / 4 threshold.

## Not done

No Lean file (KA4 numerical only). HIS1's RESULT.md, scripts, outputs and Lean files were not opened before this
commit; nor were CLOSURE.md, README.md, DD1's RESULT.md or outputs (dd1.json read by code only for KA1).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

# JNT1 FROZEN CRITERIA: the regime-split joint on data (SPARC curves above v_stiff, then the whole joint in one table)

Written 2026-11-13, committed alone before any script or number of this lane. TEST lane: adopts nothing, relabels
nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), never pooled. Cold
dark energy is a gravitating field component; no particle. kappa = 1/2 and the share 5.41 are FITTED.

## The joint (exactly SRJ2's, criteria b8a99499ad)

The law's layout holds only inside R_set = f x R_fold (FZS1's rfold_kpc, from FLD1) of galaxy-regime systems (FRZ1's
v_vir <= v_stiff, 265.8 / 288.1 km/s, read from FRZ1's code); systems above v_stiff keep the reference layout: FRZ1's
cold dark energy NFW halo with M_ta = X M_b h / (1 - FB), X = FRZ1's Xsh (z 0 median), Duffy c, Delta_ta, C_R(R) as
SRH1's `CR` (= SRJ3's CRz at z 0, SRJ3 K4). f grid: 0.75, 1.00, 1.25, 1.5, 2, 3.

## Row S (new, the deciding row): SPARC rotation curves of the galaxies above v_stiff

- **Membership:** SRJ2's G3(b) membership as stored in `srj2_rc.json` (PD1 M_b = max V_B^2 R / G at Upsilon 0.5 / 0.7):
  canonical 9 (ESO563-G021, NGC0801, NGC2955, NGC5371, NGC6195, UGC02487, UGC02885, UGC09133, UGC11455), alt 2 (UGC02487,
  UGC02885). SRJ2's FLD1-M_b membership (3 / 0) is reported as a subset. Halo mass and membership are fixed at the
  Upsilon 0.5 M_b throughout (also under the M/L bracket).
- **Data and statistic (PD1's / QX8's, said here):** QX8's `load_sparc` (175 rotmod curves, Lelli 2016 table), every
  point with g_bar > 0 and V_obs > 0 out to the last radius; point residual r = log10(g_obs / g_mod) = log10(V_obs^2 /
  V_mod^2); weights W = (V_obs / eV)^2 (eV clipped at 1 km/s), as PD1 / SRH1 / QX8 use.
- **Model graded:** reference layout g_ref = g_N + G C_R(R) / R^2, g_N at the record's fixed Upsilon (disc 0.50, bulge
  0.70; QX8's U = 0.50 column). No exact-field term T (T is the law field's correction; the reference is Newtonian plus
  the cold halo). Reported beside it on the same galaxies and the same Upsilon: the law glaw(g_N) + T (PD1's exact form),
  and the law without T; and SRJ2's reported convention (reference + T).
- **Per galaxy:** d_i = W-weighted mean residual; e_i = 0.8686 / sqrt(sum W) (dex); shape Delta_i = weighted mean
  residual at R >= R_last / 2 minus that at R < R_last / 2 (both halves must hold a point, else the galaxy is left out of
  the shape check and counted).
- **Class lines (DD1's line as SRJ3 used it):** off = median_i d_i; se = max(1.2533 x 1.4826 x MAD(d) / sqrt(n),
  median(e_i) / sqrt(n)). S1 offset: |off| <= 0.10 dex and |off| <= 3 se. S2 shape: the same line applied to the
  Delta_i (median, its own se): |med Delta| <= 0.10 and <= 3 se. S3 scatter: pooled W-weighted point rms of the
  reference <= that of the law (+T) on the same galaxies and Upsilon + 0.02 dex.
- **Row S word:** n < 5 -> NO POWER (SRJ3's rule). Else REFERENCE FITS if S1, S2 and S3 all hold; REFERENCE FAILS
  otherwise (name the line). Row S does not depend on f.
- **Twins (each must make the row word REFERENCE FAILS, on every footing with n >= 5, else the row is NO POWER):** TW-N no
  cold component (g = g_N); TW-H halo halved (X / 2, halo re-solved as SRJ3 / SRJ4 do); TW-D halo doubled (2 X).
  Files `jnt1_MUTATE_TWN|TWH|TWD.json / .out`.
- **Mass-to-light bracket:** fixed Upsilon disc 0.35 and 0.65 (bulge 1.4 x), and QX8's per-galaxy best fit on its grid
  0.30 to 1.20 (the record's fit mode in PD1 / SRH1 / SRJ2; chosen separately for the reference and the law). FRAGILE if
  any bracket member changes the row word.
- **Known answers (any fail -> NO VERDICT):** KA1 loader: 175 galaxies, and QX8's published fixed-U 0.50 law reading on
  all 175: canonical rms 0.1124 mean +0.0504 (law, no T) and 0.1181 / +0.0594 (exact, with T), alt 0.1029 / +0.0239
  (law, no T), each to 5e-4. KA2 SRJ2's reported reference reading (galaxy regime truncated law at f 1 with T, cluster
  regime reference + T, per-galaxy U fit, all 175): rms 0.0640 / 0.0559 to 1e-4, recomputed in this lane's own code.
  KA3 SRJ3's reference construction on an RC100 disc: zC 400569 (canonical) d = -0.0061041 (srj3.json) to 1e-6, from
  SRJ3's own halo routine executed read-only. KA4 membership names equal srj2_rc.json's.

## Rows carried (quoted from their committed files, marked CARRIED, not recomputed except where said)

- G1 forest, matter level (SRJ2): holds, TRIVIAL at f 0.75 / 1 / 1.25 and at f 2 (TW-F2); f 1.5 and 3 not computed;
  beside it the SRF1 / SRF1R ungraded flux reading (settled layout allowed to f of about 3).
- Clusters and groups (SRJ2): holds, TRIVIAL at every f (all above v_stiff; joint = reference); FRAGILE (R500 bracket).
- G2 RC100 (SRJ2): coverage miss at every f (31 / 22 cluster-regime discs); data rows SRJ3 and SRJ4: NO POWER.
- G4 KiDS lensing by type (SRJ2's joint numbers): f 0.75, 1.00 FAIL; 1.25 PASS; 2 PASS (TW-F2 run). f 1.5 and 3: the
  joint was not run; SRH1's no-split reading is quoted (1.5 PASS; f inf PASS) and marked NOT JOINT.
- SPARC below v_stiff: equal to the law (PD1's line holds) at f if every galaxy-regime last radius is inside f x
  R_fold; the smallest such f is computed here (FLD1 M_b as SRJ2's G3(a) and with PD1 M_b).

## Labels, per footing

- **JOINT COMPLETE ON POWERED ROWS [f window]:** every row with power passes for some constant f in the grid (row S
  REFERENCE FITS where it has power; G4 PASS at that f; G1, clusters TRIVIAL holds; G2 coverage-only and NO POWER are
  listed). A HIT, not a pass: it awaits an independent blind re-grade; the family is post hoc three times over; the two
  constants stay fitted.
- **JOINT FAILS ON <rows>** (named; on data or on coverage).
- **NO VERDICT:** a twin does not bite on a footing where row S has n >= 5, or a known answer fails.
- If any carried number changes or a departure is needed: a dated amendment committed alone; the as-frozen reading first.

## Expectation and hand estimate (before any number)

Massive SPARC discs: M_b ~ 2e11 Msun -> M_ta ~ 1e13 Msun, r_s ~ 90 kpc, c_ta ~ 10. At 30 kpc the cold mass is ~ 0.04 /
1.5 of M_ta ~ 2.5e11, about the baryons, so g_ref ~ 2 g_N, against the law's nu ~ 2.3 at g_N / a0 ~ 0.3; inside 5 kpc
g_ref ~ 1.1 g_N vs law ~ 1.2. So the reference sits ~0.03 to 0.06 dex below the law at both ends; the law's own fixed-U
offset on the massive tail is ~ +0.02 to +0.05. Estimate: canonical off +0.05 to +0.09, shape -0.05 to +0.05, scatter
within 0.02 of the law. P(REFERENCE FITS) 0.45, P(FAILS on S1 by 3 se) 0.25, P(NO VERDICT: TW-H or TW-D does not bite)
0.30. Alt: n = 2 -> NO POWER. Joint label expectation canonical: NO VERDICT or COMPLETE ON POWERED ROWS [1.25, 2] about
equally; alt: COMPLETE ON POWERED ROWS [1.25, 2] with row S NO POWER.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

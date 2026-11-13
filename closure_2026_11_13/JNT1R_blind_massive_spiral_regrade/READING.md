# JNT1R READING (frozen before any script or number of this lane)

Written 2026-11-13 and committed alone, before any script of this lane exists and before any JNT1R number is computed.
TEST lane: a BLIND, independent re-grade of ONE row of lane JNT1 (row S, the SPARC curves above v_stiff). Adopts nothing,
relabels nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), never pooled.
Cold dark energy is a gravitating field component; no particle. kappa = 1/2 and the share 5.41 are FITTED.

## What was seen before freezing (blindness record)

- JNT1's FROZEN_CRITERIA.md at its own commit only (`git show 00292e1430:...`), for the row's definition. It contains
  JNT1's design and hand estimate, no JNT1 output number.
- The brief that launched this lane states JNT1's UNGRADED reading in words: "the reference layout over-predicts the
  outer curves at the record share and about half the halo fits". No JNT1 number was given or seen. This reading is
  therefore known to me before freezing; it is recorded here so the reader can weigh it.
- Read: SRJ2's `srj2_rc.py` and the G3(b) `reported_reference` block of `srj2_rc.json` (membership names, rms 0.0640 /
  0.0559); SRJ3's `srj3.py`, FROZEN_CRITERIA.md, the first 60 lines of its RESULT.md and its stored row for zC 400569
  (d = -0.0061041); SRH1's `srh1_rc.py` prefix; PD1's `pd1.py` prefix and the P2-SPARC line in its FROZEN_CRITERIA.md;
  QX8's loader, fit code and `qx8.out` fixed-U lines; FRZ1's `frz1_hm.py` lines 1-75; CFG556's h, Om, FB, RHO_M lines;
  the PD1 share medians XTAB (59.49 / 55.72 canonical, 59.50 / 55.73 alt).
- Not opened: JNT1's RESULT.md, scripts, JSON or outputs; JNT1's git log beyond the one `git show`; JNT2, JNT2R;
  `_orchestrator_handoff_2026_11_12/`.

## Sample

SRJ2's G3(b) membership as stored in `closure_2026_11_12/SRJ2_regime_split_joint/srj2_rc.json`
(`foot[ft]["G3b"]["f1.00"]["reported_reference"]["cluster_names"]`): canonical 9 (ESO563-G021, NGC0801, NGC2955,
NGC5371, NGC6195, UGC02487, UGC02885, UGC09133, UGC11455), alt 2 (UGC02487, UGC02885). Membership and each galaxy's
baryon mass M_b (PD1's: max over radii of V_B^2 R / G with disc 0.50, bulge 0.70) are fixed at those values throughout,
also under every bracket member.

## Data, statistic, models

- **Loader:** QX8's `load_sparc` (record's loader; Lelli 2016 table; rotmod curves). Every point with g_bar > 0 and
  V_obs > 0 (QX8's OK mask at the U in use), to the last radius.
- **Point residual:** r = log10(V_obs^2 / V_mod^2) = log10(g_obs / g_mod), with the quoted velocity errors: point
  sigma s = 0.8686 eV / V_obs dex (eV and V_obs clipped at 1 km/s as QX8), weight W = 1 / s^2 equivalently QX8's
  W = (V_obs / eV)^2 up to the constant 0.8686^2.
- **Reference layout (graded):** g_ref(A) = g_N(U) + G C_R(R; A X) / R^2, g_N(U) at disc U, bulge 1.4 U (QX8's convention:
  0.50 / 0.70 at the record's value). C_R(R; X) = X M_b m(R / r_s) / m(c_ta), m(x) = ln(1 + x) - x / (1 + x), R capped
  at r_ta; the halo is FRZ1's at z = 0 built by MY OWN code: find M (= M_200m, Msun/h) such that M_ta = X M_b h / (1 - FB),
  c = 10.14 (M / 2e12)^-0.081 (Duffy, z = 0), r_200m from 200 rho_m (rho_m = Om x 2.77536627e11 h^2 Msun / Mpc^3),
  r_ta where the mean enclosed density is Delta_ta(0) = 11.81 times rho_m, M_ta = M m(c x_ta) / m(c); h = 0.6736,
  Om = (0.02237 + 0.1200) / h^2, FB = 0.02237 / 0.1437. X = XTAB[foot]["z0.0"] (PD1's share median). A = 1 is the
  record's share; A = 0 is no cold component; A != 1 re-solves the halo with A X (as SRJ3 / SRJ4's halved twin).
  No exact-field term T on the reference (T is the law field's correction).
- **The law (graded beside it):** g_law = glaw(g_N) = g_N / 2 + sqrt(g_N^2 / 4 + a0 g_N), plus QX8's exact-field term T
  (PD1's exact form) as the primary law; the law without T reported.

## Class lines (the record's own)

Per galaxy i: d_i = W-weighted mean residual; e_i = 0.8686 / sqrt(sum over points of (V_obs / eV)^2) dex.
Shape Delta_i = W-weighted mean residual over R >= R_last / 2 minus that over R < R_last / 2 (a galaxy with an empty
half is left out of the shape line and counted); its error eD_i = sqrt(e_out^2 + e_in^2).
Population statistic (DD1's class form as SRJ3 uses it, `closure_2026_11_12/SRJ3_reference_layout_disc_fit/FROZEN_CRITERIA.md`,
inherited from `fable52_push/DD1_deduce_from_data/FROZEN_CRITERIA.md` 2a3f76f295): off = median(d_i);
se = max(1.2533 x 1.4826 x MAD(d) / sqrt(n), median(e_i) / sqrt(n)).

- **L1 offset (DD1 / SRJ3 line):** |off| <= 0.10 dex AND |off| <= 3 se.
- **L2 shape (the same line on Delta_i):** |median Delta| <= 0.10 AND <= 3 se(Delta).
- **L3 scatter (PD1's P2-SPARC line, `closure_2026_11_09/PD1_phantom_is_dust/FROZEN_CRITERIA.md` line 41, SS1 G5):**
  pooled W-weighted point rms of the reference <= that of the law (+T) on the same galaxies + 0.010 dex, AND
  |pooled W-weighted mean| <= 0.05, both in the record's fit mode (per-galaxy U on QX8's grid 0.30 to 1.20, chosen
  separately for each model by minimum weighted rms). For the law itself L3 is PD1's absolute line: rms <= 0.0660 and
  |mean| <= 0.05.
- At fixed U (0.50) L3 is reported, not graded.

## Power (frozen, not circular)

Joint fit of one multiple A of the reference halo to the n galaxies of a footing at the record's U (disc 0.50, bulge
0.70), A on a grid 0 to 5 step 0.01 (halo re-solved at each A). chi2(A) = sum over all points of (r / s)^2.
- A_best = argmin chi2. 95 % interval = the UNION of (a) {A : chi2(A) - chi2_min <= 4 x chi2_min / (N_pts - 1)}
  (errors rescaled to chi2/dof = 1) and (b) A_best +- 2 x the delete-one-galaxy jackknife SE of A_best.
  The 68 % interval (1 instead of 4, 1 x SE) is reported.
- **The row HAS POWER on a footing if n >= 5 AND the 95 % interval excludes at least one of A = 0, A = 1, A = 2.**
- The reference "fits at the record share" only if A = 1 is inside the 95 % interval AND L1, L2, L3 hold at A = 1.
- Reported, not graded: per-galaxy best A_i (same grid) with their median; A_best in the fit mode (U profiled per
  galaxy at each A).

## Labels, per footing (as frozen)

- **REFERENCE FITS AT THE RECORD SHARE**: power, A = 1 in the 95 % interval, L1, L2, L3 hold at A = 1.
- **REFERENCE FAILS AT THE RECORD SHARE [which]**: power, and A = 1 is outside the interval or one of L1, L2, L3 fails
  at A = 1 (each failing item named).
- **NO POWER**: n < 5 (SRJ3's rule), or the interval excludes none of 0, 1, 2, or a must-bite mutation does not bite.
- **FRAGILE** appended if any bracket member or any delete-one jackknife sample changes the word.
- Beside it: **THE LAW FITS** (L1, L2 and PD1's absolute L3 all hold for glaw + T at U 0.50 / fit mode) or
  **THE LAW FAILS [which]** on the same galaxies.
- Alt (n = 2): NO POWER by the n < 5 rule. Its numbers are still computed and reported; two galaxies can show the sign
  and rough size of each galaxy's misfit, not a population offset or a scatter.

## Brackets

- Mass-to-light: the record's value (disc 0.50, bulge 0.70); fixed disc 0.35 and 0.65 (bulge 1.4 x); the record's fit
  mode (per-galaxy U on 0.30 to 1.20). Halo mass and membership stay at the U 0.50 M_b.
- Distance and inclination: the record's SPARC lanes use the catalogue values (QX8 FROZEN_CRITERIA scope line). As
  bracket members: every galaxy's D moved by +eD and by -eD together (R and V_bar^2 scale by D'/D, M_b by (D'/D)^2,
  g_obs by D/D'), and every inclination moved by +eInc and -eInc together (V_obs and eV scale by sin i / sin i').
- Reference with T added (SRJ2's reported convention).
- Jackknife over galaxies (delete one).

## Mutations (separate `*_MUTATE*` outputs)

- **MUT-C, concentration halved** (c -> c / 2 in the halo build, everything else equal). MUST BITE: A_best moves by
  >= 0.15 or the word changes. Expected: a less concentrated halo puts less cold mass inside the disc, so A_best rises.
- **MUT-E, velocity errors shuffled between galaxies** (each galaxy's eV / V_obs fractional error profile replaced by
  another member's, cyclic shift, interpolated on normalised radius). Reported: A_best and the word; not required to bite.
- **TW-N (A = 0)**: no cold component. MUST give L1 failing (offset outside the line) on canonical; otherwise the row
  cannot see the cold component -> NO POWER.

## Known answers (any fail -> NO POWER, reported as such)

- **KA1** loader: 175 galaxies. QX8's published fixed-U 0.50 pooled readings on all 175, recomputed in my code:
  canonical law (no T) rms 0.1124 mean +0.0504, exact (with T) 0.1181 / +0.0594; alt law (no T) 0.1029 / +0.0239; each
  to 5e-4 (`closure_2026_11_06/QX8_sparc_exact_field/qx8.out`).
- **KA2** my halo construction, generalised to z (Duffy (1+z)^-1.01, Delta_ta(z) = 5.55 + 6.26 (1 - Om(z)) / (1 - Om),
  physical r = comoving / (1 + z) / h, X = z1.0 median for z >= 1), on SRJ3's RC100 disc zC 400569 (z 2.24, log M_b
  10.95, R_e 4.31 kpc, V_c 241 km/s): d = -0.0061041 (srj3.json) to 1e-6.
- **KA3** membership: my own v_vir = sqrt(G M_200c / r_200c) at z = 0 (r_200c where the mean density is 200 rho_c, rho_c
  = rho_m / Om) puts exactly SRJ2's names above v_stiff (265.8 / 288.1 km/s) among the 175 with PD1's M_b.
- **KA4 (SI, second route):** for one member, r_200m and C_R(R_last) recomputed from rho_m = Om 3 H0^2 / (8 pi G) in SI
  with Msun 1.989e30 kg, kpc 3.0857e19 m: agree with the script to 1 %.

## Expectation and hand estimate (before any number)

M_b ~ 1-3e11 Msun -> X M_b ~ 1e13 Msun of cold dark energy within r_ta; Duffy c_200m ~ 6 at 1e13 Msun/h; r_200m
~ 500 kpc, r_s ~ 80 kpc. The NFW peak speed of such a halo is ~ 1.2 sqrt(G M_200 / r_200) ~ 1.2 x 290 ~ 350 km/s,
reached at ~ 2 r_s ~ 170 kpc; at the SPARC last radii (30 to 80 kpc for these discs) the cold term alone gives V ~ 230
to 300 km/s, and added to the baryons the model speed rises to ~ 330 to 380 km/s, against observed flat speeds of ~
270 to 330 km/s. So I expect the reference at A = 1 to be too heavy in the outer half: off ~ -0.03 to -0.08 dex, shape
Delta ~ -0.05 to -0.15 dex, best A ~ 0.3 to 0.7. The law at U 0.50 on the massive tail: off ~ +0.0 to +0.05, shape ~ 0.
P(REFERENCE FAILS AT THE RECORD SHARE, canonical) 0.55 (mostly A = 1 excluded or L2), P(FITS) 0.25, P(NO POWER) 0.20.
P(THE LAW FITS) 0.6. Alt: NO POWER (n = 2). This expectation was formed knowing JNT1's ungraded reading in words (see the
blindness record).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

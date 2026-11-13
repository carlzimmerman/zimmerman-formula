# JNT2R RESULT_BLIND: the crossing-speed joint, blind build

**JOINT FAILS ON G2 (coverage) / JOINT FAILS ON G2 (coverage) (canonical / alt), as frozen. FRAGILE: canonical (the
record-halo bracket passes the forest at f 3, where the primary fails; the inherited X-COP R500 aperture bracket); alt (the
X-COP R500 aperture bracket).**

- G2 fails at every grid f on both footings. **10 / 2 RC100 discs at z 2.1 to 2.5 lie above v*(z).** They lose the law,
  so 2.2 R_e is not covered. That is a coverage fail, not a fail on data. SRJ3 / SRJ4 found that RC100's single R_e point
  has no power to test the reference layout on such discs; that finding is carried, not recomputed.
- **Reported, not graded:** with the G2 coverage line set aside, every powered row passes at f = 1.25, 1.5 and 2 on both
  footings. In that window:
  - G4 KiDS lensing is the only powered row that passes non-trivially and can see the layout. SRH1R found that this gate
    cannot see f.
  - The forest and X-COP pass TRIVIALLY.
  - SPARC equals the law.
  - The groups have NO POWER.

  This would be a hit on a post hoc family, not a pass.
- The window is closed from below by G4 (f <= 1 fails, early-type lenses +2.14 / +2.00 sigma canonical) and from above
  by the forest at f = 3 (Delta chi^2 17.6 / 29.2 against 4).

TEST lane. READING 5abea0324b (committed alone, before any script or number). No amendment. Footings never pooled. Cold
dark energy is a gravitating field component; no particle. kappa = 1/2 and the share 5.41 are FITTED. Nothing here says the
data favour the framework. JNT2 was not opened (section 8).

## The boundary

v* = a0 / (10 (1 + X) H): **668.5 / 807.9 km/s today** (KA1, SI, from a0, X = 5.41, H0 = 67.4). It scales as v*(z) =
v*(0) H0 / H(z) with the lemma's flat OL = 0.6847. A system is above iff its baryon mass exceeds M_b*(z) = v*^4 / (G a0).
- log M_b*(0) = 13.21 / 13.45.
- log M_b*(z) is 12.19 / 12.44 at z 1, 11.28 / 11.53 at z 2, 10.90 / 11.15 at z 2.5 and 9.80 / 10.05 at z 4.4.
- The lemma's virial speed v_cl = (10 G H (1 + X) M_b)^(1/3) and the law's flat speed give the same boundary to 2e-16 (KA4).

## Membership (primary; brackets B-meas = measured speed, B-halo = the record halo's v_vir)

| row | above v*(z), canonical | alt | B-meas can / alt | B-halo can / alt |
|---|---|---|---|---|
| SPARC (FLD1 M_b; PD1 M_b) | 0 / 175; 0 / 175 | 0; 0 | 0; 0 | 0; 0 |
| RC100 | **10 / 100** | **2 / 100** | 31 / 19 | 41 / 25 |
| KiDS host-free lenses (40,667) at every fitted k | 0 (late 0, early 0) | 0 | no measured speed | 0 |
| KiDS table nodes above (of 2,178) | 92 (log M_b > 12.35, no lens there) | 38 | | 321 / 229 |
| X-COP | 7 / 7 | 7 / 7 | 7 / 7 | 7 / 7 |
| Lovisari groups | 0 / 20 (v_cl up to 658 against v* about 661) | 0 / 20 | 7 / 3 | 1 / 0 |
| forest haloes (of 321), z 2.2 / 3.0 / 4.4 | 155 / 170 / 202 | 151 / 161 / 193 | no measured speed | 170 / 192 / 223, 160 / 182 / 213 |

- RC100 above, canonical: COS4 13174, GS4 01529, U4 36568, U4 20704, K20 ID5, J0901+1814, D3a 15504, D3a 6004,
  COS4 06079 and U3 25105 (z 2.10 to 2.52, log M_b 11.03 to 11.47). Alt: U4 20704 and D3a 6004.
- **Forest:** at z 2.2 to 2.6 the primary split is exactly SRJ2's v_stiff split (155 / 151 at z 2.2). It hands more haloes
  to the reference at higher z (202 against SRJ2's 169 at z 4.4).

## Rows against f (primary), canonical / alt

| row (power) | 0.75 | 1.00 | 1.25 | 1.5 | 2 | 3 |
|---|---|---|---|---|---|---|
| G1 forest Delta chi^2 <= 4 (powered) | 0.007 / 0.016 T | 0.020 / 0.052 T | 0.026 / 0.082 T | 0.017 / 0.071 T | 0.347 / 0.477 T | **17.6 / 29.2 FAIL** |
| G2 RC100 coverage (powered) | **90 / 98 of 100 FAIL** | same | same | same | same | same |
| G3 SPARC (powered) | 175 / 175 by (a), L | same | same | same | same | same |
| G4 KiDS early z (all lines) (powered) | **+2.141 / +2.172 FAIL** | **+2.003 / +2.037 FAIL** | +1.813 / +1.852 | +1.578 / +1.623 | +1.036 / +1.091 | -0.060 / +0.014 |
| X-COP (a), (b) (powered) | 1.095, -0.007 ... -0.041 CONSISTENT, T | same | same | same | same | same |
| groups q at R500 (NO POWER) | 0.619 / 0.620 L | 0.651 / 0.654 L | same as f 1 | same | same | same |

T = TRIVIAL. L = EQUAL TO THE LAW by membership.
- G4 at every f equals SRH1's no-split rows to 0 (f 0.75 to 2.00), because no lens lies above. It is not marked L, by the
  frozen node rule: 92 / 38 empty high-mass nodes switch.
- G4's other lines (all, late, chi^2, type difference) pass at every f. The all-lens z is +1.84 / +1.87 at f 0.75.
- G3 never needs (b).
- **Power (rule iii):** the groups pass under the reference (0.597), under the law everywhere (0.651 / 0.654) and at every
  f. Every other row changes mark between the reference, the law and the grid.
- **Fails by f, both footings:**
  - f 0.75 and 1.00: G2, G4;
  - f 1.25, 1.5 and 2: G2 only;
  - f 3: G1, G2.

## Brackets (FRAGILE)

- **B-meas** moves no mark:
  - G2 fails with 31 / 19 discs above;
  - groups 13 / 17 below stay CONSISTENT (0.651 / 0.654 at f 1).
- **B-halo** moves one mark: canonical G1 at f 3 passes (1.99), while the primary fails (17.6). On alt it fails (6.43).
  G2 fails with 41 / 25 above.
- The inherited R500 aperture bracket fails for the reference and the joint alike (1.057 [1.046, 1.072]) wherever X-COP
  passes.

## Twins (all bite) and known answers (all pass)

- **TW-V (SRJ2's boundary).** It reproduces SRJ2 exactly:
  - G1 0.0477 / 0.0805;
  - G2 69 / 78 covered;
  - G3(a) 172 / 175 covered, canonical G3(b) rms 0.0968 FAIL;
  - G4 early z +2.0121 / +2.0369;
  - clusters and groups equal to the reference (difference 0);
  - lenses above at the all-fit k: 224 / 0.

  So SRJ2's words come back: FAILS ON G2, G3, G4 / G2, G4. Membership differs from the primary on RC100, the forest and
  the groups.
- **TW-N (no boundary).** It reproduces SRH1, FZS1 and SRJ1:
  - G1 38.7415 / 36.6582 = FZS1;
  - halo-model R_cold equal to FZS1's stored primary to 0;
  - G2 f_min 0.391237 / 0.391383, all covered;
  - G4 = SRH1's stored f 1 row to 0;
  - X-COP shape +0.153 / +0.144 FAILS = SRJ1.

  Its marks differ from the primary on G1, G2 and X-COP.
- **TW-H (v*/2).** RC100 68 / 58 above. Forest 193 / 184 above at z 2.2, G1 0.0000 / 0.0001. All groups above, so q
  returns to the reference's 0.597 (moves 0.054). It bites on the groups only. G4 has no lens above (515 / 427 empty
  nodes), so it does not move.
- **TW-D (2 v*).** 6 / 7 X-COP clusters fall below and take the law's layout: shape +0.153 / +0.144 FAILS. G1 11.1 /
  18.8 FAILS. RC100 0 above, G2 passes. It bites on G1, G2 and X-COP.
- **Known answers:**
  - KA1 669 / 808 km/s;
  - KA4 boundary identity 2e-16;
  - KA-M 6.6e-16 and non-decreasing at f 0.75 to 3;
  - f 0: R_cold 1 exactly, G1 0, G4 = SRH1's f0 row to 0;
  - SRJ1's K1 against `rb1.json` 2.4e-13;
  - FRZ1 KA2 and KA3 pass.

## Against my estimate

- SPARC none above, G3 law-equal: right.
- RC100 3 to 15 above canonical, 0 to 5 alt: right (10 / 2). G2 fails on both: right on canonical; on alt I gave 50 %.
- KiDS none above, G4 = SRH1, passes from 1.25: right.
- X-COP TRIVIAL with R500 FRAGILE: right.
- Groups NO POWER: right. Groups 0 to 2 above canonical: 0.
- Forest near SRJ2: right up to f 2. **"f 3 likely still under 4": wrong.** It fails, at 17.6 / 29.2.
- Labels: canonical right; alt took the fail branch (right as a 50 % call).

## What is left out

- The weak-lensing amplitude; hosted dwarfs; the Milky Way rows.
- Any data test of the 10 / 2 RC100 discs under the reference (carried NO POWER from SRJ3 / SRJ4; their discs were SRJ2's
  31 / 22, which contain all of these 10 / 2; SRJ3's statistic was not recomputed on the subset).
- A bracket on FRZ1's X (56 to 59) and on H(z).
- The flux-level forest. SRF1 / SRF1R read ungraded flux Delta chi^2 far below 4 up to f about 3 for the no-split family;
  not recomputed for this split.
- f between 2 and 3 was not run.

## Files and commits

READING 5abea0324b. Scripts and outputs (`jnt2r_common.py`, `jnt2r_hm.py`, `jnt2r_forest.py`, `jnt2r_rc.py`,
`jnt2r_lens.py`, `jnt2r_clusters.py`, `jnt2r_grade.py` and their `.json` / `.out`, twins `*_MUTATE*`) in the commit before
this file. Owners' code is executed read-only from its own path. Console logs stayed outside the repository. Nothing was
fetched or pushed. One job at a time, one thread.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

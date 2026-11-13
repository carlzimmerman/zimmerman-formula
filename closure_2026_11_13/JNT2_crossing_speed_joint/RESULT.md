# JNT2 RESULT: the crossing-speed joint

**JOINT FAILS ON G2 (coverage) / JOINT FAILS ON G2 (coverage) (canonical / alt), as frozen.**

- 10 / 2 RC100 discs at z 2.1 to 2.5 sit above v*(z) on the primary (model) rule, so the law covers 90 / 98 of 100 at every f.
- The fail is on coverage, not data. SRJ3 found that RC100's single R_e point has no power to tell the reference layout from the law.
- Without G2, every other row passes at f in [1.25, 3] canonical and [1.25, 2] alt. That reading is reported, not graded.
- In that window the forest is TRIVIAL to f 2, the clusters are TRIVIAL, and SPARC, KiDS and the groups are EQUAL TO THE LAW.
- So no row that passes is support for the boundary itself.
- The measured-speed rule gives the same words (31 / 19 discs above). Nothing is FRAGILE under it.

Every known answer passes. TW-S reproduces SRJ2 and TW-0 reproduces SRH1 / SRJ1. TW-H and TW-D both bite.

TEST lane: adopts nothing, relabels nothing, registers nothing. Criteria e186b314ef (committed alone, before any script
or number); scripts and outputs aad4a0b3a4; no amendment. Footings never pooled. Cold dark energy is a gravitating field
component; no particle. The settled-radius family is post hoc, and this boundary is post hoc to SRJ2 and JNT1. JNT2R's
folder was not opened.

## The joint as run

- **Boundary.** v* = a0 / (10 (1 + 5.41) H). The lemma is route D check C5: v^3 = 10 G M H with M = 6.41 M_b meets
  v^4 = G M_b a0.
- **From SI constants:** 668.53 / 807.93 km/s, so KA-3 gives 669 / 808.
- **Redshift scaling:** v*(z) = v*(0) / E(z), with a0 constant.
  - canonical: 668.5 / 373.3 / 220.4 / 177.4 km/s at z 0 / 1 / 2 / 2.5;
  - alt: 807.9 / 451.1 / 266.4 / 214.4 km/s.
- **Equivalent mass form:** M_b > M*(z), with log M* = 13.21 / 12.19 / 11.28 / 10.90 canonical and 13.45 / 12.44 / 11.53 / 11.15 alt, at the same redshifts.
- **Below v*,** the law's layout holds inside f x R_fold (FZS1's junction). **Above v*,** the reference layout holds at every radius.
- **Primary speed:** the lemma's v_L = (10 G M H(z))^(1/3), with M = 6.41 M_b, or M200c for haloes.
- **Secondary speed:** the measured speed (SPARC Vflat, RC100 Vc(R_e), X-COP sqrt(G M_HSE / r_last), groups sqrt(G M500 / R500)).

## Every row against f (primary rule)

| row (owner, line) | f 0.75 | f 1.00 | f 1.25 | f 1.5 | f 2 | f 3 | mark |
|---|---|---|---|---|---|---|---|
| G1 forest, Delta chi^2 <= 4 (SRJ2 / FRZ1), can | 0.000 P | 0.001 P | 0.001 P | 0.001 P | 0.049 P | 1.990 P | TRIVIAL to f 2 |
| G1 alt | 0.002 P | 0.005 P | 0.005 P | 0.003 P | 0.146 P | **6.432 F** | TRIVIAL to f 2 |
| G2 RC100 coverage 100 / 100 (SRH1), can / alt | 90 / 98 F | same | same | same | same | same | **FAILS ON COVERAGE**; data NO POWER (SRJ3) |
| G3 SPARC (SRH1 / PD1), can / alt | P (175 / 175; rms 0.0560 / 0.0558) | P | P | P | P | P | EQUAL TO THE LAW (0 above) |
| C X-COP q at r_last (RB1) | 1.095 CONS. | same | same | same | same | same | TRIVIAL (all 7 above); R500 bracket FAILS (FRAGILE, as RB1) |
| C X-COP shape bins (abs <= 0.10) | -0.007 / +0.033 / +0.006 / -0.030 / -0.041 | same | same | same | same | same | TRIVIAL |
| C groups q at R500, can | 0.619 CONS. | 0.651 | 0.651 | 0.651 | 0.651 | 0.651 | law in 19 / 20 (IC1633 above, 666 vs 661 km/s) |
| C groups alt | 0.620 CONS. | 0.654 | 0.654 | 0.654 | 0.654 | 0.654 | EQUAL TO THE LAW (20 / 20 below) |
| G4 KiDS early z at 1.6 R_h (SRH1 / ONE1), can | +2.141 F | +2.003 F | +1.813 P | +1.578 P | +1.036 P | -0.060 P | EQUAL TO THE LAW (SRH1's rows); cannot see f (SRH1R) |
| G4 alt | +2.171 F | +2.037 F | +1.852 P | +1.623 P | +1.091 P | +0.014 P | same |

Other G4 lines pass at every f (all-lens z <= +1.87, chi^2 <= 4.33, type difference <= +1.43). The F rows show the
G-K1 early line alone.

SRF1 / SRF1R flux-level reading, carried and ungraded: the forest allows up to f ~ 3 (SRF1R's window edge is 3.16 / 3.21).
At matter level it is already TRIVIAL here.

## Membership (primary model rule / measured rule)

| sample | canonical above / total | alt above / total |
|---|---|---|
| SPARC | 0 / 0 of 175 (max v_L 171, max Vflat 332 km/s) | 0 / 0 |
| RC100, z < 1.5 | 0 / 1 of 44 | 0 / 0 |
| RC100, z 1.5-2 | 0 / 4 of 15 | 0 / 3 |
| RC100, z 2-2.5 | 9 / 25 of 40 | 2 / 15 |
| RC100, z >= 2.5 | 1 / 1 of 1 | 0 / 1 |
| KiDS lenses (40,667; no measured speed) | 0 at every f (max v_L / v* 0.37); 92 of 2178 table nodes (log M_b >= 12.9) | 0 (max 0.30); 38 nodes |
| X-COP | 7 / 7 of 7 (v200 1247-1728, v* 639-651) | 7 / 7 (v* 772-786) |
| Lovisari groups | 1 / 7 of 20 (v200 353-666, measured 462-882, v* 658-665) | 0 / 3 |
| forest grid haloes (321 per bin; model only) | z 2.2: 170 (M200c >= 5.8e11 Msun/h); z 3.0: 192 (1.7e11); z 4.4: 223 (2.8e10) | 160 (1.0e12); 182 (2.9e11); 213 (5.0e10) |

The 10 canonical RC100 discs above are COS4 13174, GS4 01529, U4 36568, U4 20704, K20 ID5, J0901+1814, D3a 15504,
D3a 6004, COS4 06079 and U3 25105. The alt pair is U4 20704 and D3a 6004. Reported only: with FRZ1's X ~ 56 halo speed
in place of the lemma's, 41 / 25 discs would be above.

## TRIVIAL, EQUAL TO THE LAW, NO POWER

- **TRIVIAL:**
  - the forest to f 2. A third to two thirds of the grid haloes are handed to the reference, and the rest changes R_cold by < 1e-3.
  - X-COP, on every statistic, because every cluster is above v*.
- **EQUAL TO THE LAW:**
  - SPARC, because no galaxy is above, so JNT1's row S test is EMPTY (n = 0) and was not run;
  - KiDS lensing: equal to SRH1's stored rows at 0.75 to 2 exactly (deviation 0);
  - alt groups, and canonical groups but one.
- **NO POWER:**
  - G2's data for the discs above v* (SRJ3, carried);
  - G4's f dependence (SRH1R).
- **Not trivial or law-equal anywhere:** G2's coverage, which fails, and G1 at f 3.

## Twins and known answers

| check | canonical | alt |
|---|---|---|
| KA-1 (TW-S G1 = SRJ2 on_f1.00; G4 = SRJ2) | 0.047667 = 0.047667; G4 dev 0 | 0.080523 = 0.080523; dev 0 |
| KA-2 (TW-0 G1 = FZS1; G4 = SRH1 f1) | 38.741 = 38.741 | 36.658 = 36.658 |
| KA-0 (f 0 = reference: G1, G4, clusters to rb1.json) | 0; 0; 2.4e-13 | same |
| TW-S words (G2 FAILS 31 / 22, G4 FAILS, G1 TRIVIAL, clusters TRIVIAL) | reproduced | reproduced |
| TW-0 words (G1 FAIL, G4 FAIL, X-COP shape FAILS) | reproduced | reproduced |
| TW-H (v*/2) at f 1.25, 2 | bites: groups q -0.055 (all groups to the reference); G2 44 covered | bites: groups q -0.057; G2 57 |
| TW-D (2 v*) at f 1.25, 2 | bites: G1 11.70 / 28.07 FAIL; G2 100 covered (passes) | bites: G1 20.95 / 45.10 FAIL; X-COP q +0.099; G2 100 |

TW-D shows the trade-off sharply. Doubling the boundary would restore G2's coverage, but it breaks the forest at every f.
No single multiple of v* between the two twins was graded. That would be a fitted constant.

## (i) What closes

- **The candidate fails as frozen, and only on coverage.** With no new constant, the crossing speed falls fast enough
  with redshift (as 1 / E(z)) to hand the massive z ~ 2 to 2.5 discs (log M_b 11.0 to 11.5) to the cold dust layout, and
  the coverage line requires the law there.
- **What holds:**
  - It keeps every z = 0 galaxy, every KiDS lens and the groups on the law.
  - It keeps every X-COP cluster on the reference.
  - It leaves the forest at matter level TRIVIAL.
  - It removes the SRJ2 / JNT1 problem with massive SPARC spirals: none is above v*.
- **What closes is the "law's layout everywhere RC100 is measured" reading together with v*.** Keeping the joint needs either:
  - a boundary that sits higher at z ~ 2 (2 v* fails the forest, so the room is between 1x and 2x and would be fitted), or
  - evidence that the reference layout fits those 10 / 2 discs, which RC100's single point cannot give (SRJ3).
- **On the other rows the joint would read [1.25, 3] / [1.25, 2].** The lower edge is set by G4, which cannot see f.
  The alt upper edge is the forest at f 3.

## (ii) What the rule predicts that differs from both rivals (LISTED ONLY; sealed nowhere, entered in no registry)

The two rivals are SRJ2's constant v_stiff (266 / 288 km/s) and the unsplit settled family (law everywhere inside f R_fold).

- **The switch speed scales as 1 / H(z).**
  - It is 669 / 808 km/s at z 0, 373 / 451 at z 1, 220 / 266 at z 2 and 177 / 214 at z 2.5.
  - In baryon mass the switch is at log M_b 13.2 / 13.5 today and 11.3 / 11.5 at z 2, a 1.9 dex fall.
  - v_stiff is constant in z, and the unsplit family has no switch.
- **Today no galaxy switches, but groups sit on the edge.**
  - Lovisari groups (v200 353 to 666 km/s) are below v* and keep the law.
  - Canonical IC1633 sits at 666 against 661 km/s.
  - 7 / 1 groups are within 20 % of v* on the model speed, and 11 / 7 on the measured speed.
  - X-COP clusters (v200 >= 1247 km/s, about 1.9x v*) keep the cold dust.
  - SRJ2 put every group in the reference; the unsplit family gives every cluster the law, and the X-COP shape fails.
- **At z ~ 2 the edge cuts through massive star-forming discs.**
  - 33 / 25 RC100 discs have Vc(R_e) within 20 % of v*(z).
  - The rule says discs with log M_b >~ 11.3 / 11.5 at z 2 (>~ 10.9 / 11.1 at z 2.5) carry an NFW-like cold dust halo instead of the law's.
  - The prediction is an outer rotation curve that keeps rising, against a flat one, beyond about 2 R_e. That needs resolved outer curves, not RC100's single point.
- **In the forest (z 2.2 to 4.4) the switch halo mass falls from about 6e11 to 3e10 Msun/h** (1e12 to 5e10 alt).
  - Above it, haloes are pure reference.
  - The unsplit family gives every halo the law (and fails, 38.7 / 36.7); v_stiff switches at a nearly constant 1e12.

## Not addressed

- the weak-lensing amplitude;
- hosted dwarfs;
- the Milky Way rows;
- the two fitted constants (kappa = 1/2, share 5.41), which set v* directly;
- whether a0 itself evolves (held constant here; if a0 tracks the dark energy density, v*(z) changes);
- resolved outer rotation curves of the z ~ 2 discs above v*;
- any blind re-grade (JNT2R runs separately).

The lemma's v_L uses the cosmic share 5.41. The record's per-galaxy share (X ~ 56, PD1) would move the RC100 count to
41 / 25 (reported only).

## Files

- **Criteria:** `FROZEN_CRITERIA.md` (e186b314ef).
- **Code:**
  - `jnt2_common.py` (v*, modes);
  - `jnt2_hm.py` + `jnt2_forest.py` (G1; SRJ2 / FZS1 / FRZ1 content);
  - `jnt2_rc.py` (membership, G2, G3; SRJ2 / SRH1);
  - `jnt2_clusters.py` (SRJ1 / RB1);
  - `jnt2_lens.py` (G4; SRJ2 / SRH1);
  - `jnt2_grade.py`;
  - `run_g1_chain.sh`, `run_rest_chain.sh`.
- **Outputs:** twins in `*_MUTATE_{S,0,H,D}*`. Console logs stay local (gitignored).
- **Read-only use:** owners' code was executed read-only from its own paths. Nothing was fetched or pushed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

# HM1_honest_model: FROZEN CRITERIA, committed alone before any script or number of this lane

**Question.** The model with no switch and no fit beyond those disclosed: native zoom shape at ng 80 (ZN4), measured gravity response (LC1's f_Q 0.872), fair share inside R200. Candidate **C5** on FG1's scorecard. Record check: FG1 states ZN4's shape with a response isn't computed; SP3's cluster addendum didn't fire; OP3 graded galaxies only and left clusters ungraded; UL1 corrected UR3 (c200 8.0) so native + f_Q passes both direct weighings, and no response fails them. So the cluster row of this candidate has never been computed. The galaxy row is on record and is reproduced here, not rediscovered.

**Not blind.** ZN4, NR3, M3A1, OE1, OP3, SP3, UL1, FG1 have all been read, and the galaxy numbers are known before freezing. The only new numbers are clusters with response, KiDS and Local Group with response, and the puzzle's decomposition. Disclosed fitted numbers: EM1's M200 line in every galaxy row, kappa = 1/2 FITTED and unused. No a0 in the cold sector. No LCDM input in a grade. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. Whether anything is retired is the owner's decision.

## Rule
- **Shape:** ZN4's `zn4_shapes.json` (ng 80 at 1e14, 1e15; ZN1's ng 64 at 1e13), through ZN3's rule and ZN1's `zn1_fn`, unchanged: fair share inside R200, no S, no eta, no r0, no a0.
- **Response:** X39's `contract` unchanged. M_f from M0, baryons Mb(r), F = Mb(r_ta) / M0(r_ta). Then M_c = M0 + f (M_f - M0), OP3's method. It is used both ways as UR1 reads it, outward in cluster cores and inward where f_local > 1/R_nat, with no clip on either sign. **M_c(r_ta) is held:** F is M0's own, so the response moves no mass across r_ta. Where native's M0(r_ta) differs from the fair-share budget Mfair, I report that ratio and do not renormalise, because renormalising would break f 0 = ZN4. Reported on the primary row only: F = Mb(r_ta)/Mfair, CN1's text.
- **Responses:** f_Q 0.872 Blumenthal (**PRIMARY**, the measured one); Blumenthal f = 1; Gnedin (0.85, 0.8, r_ta), f = 1, as CN1.
- **BCG:** as CN1, a = 10 kpc, measured for 190, filled by tercile, in both source and response (**PRIMARY**, since C5 is about real baryons and FG1's C2 row carries it); none, reported. The f 0 identity with ZN4 is the BCG-none row. X-COP carries no BCG in any row, as XH1 and UR1: no BCG measure for those clusters is on disk, stated.
- **Clusters cells:** gas +0.005 (GS4, graded), +0.111 (reported only, a scale the data don't support); f* 0.034 (primary, as FG1's C1), 0.0615; h 0.672, 0.686. Canonical template primary, alt reported. Native has no a0, so footing enters only through the template.
- **Galaxies:** SP3's native rows on EM1. **Frozen map `tot` is PRIMARY** (ZN2, OP3's primary); FC1's map reported. Native reads no eta, so NR2 does not enter its row: stated. NR2's eta enters only the S-core path of the puzzle. Native's 1e12 table is ng 64 per SP3: **A5's ng 80 runs stop at z_f, and no z = 0 ng 80 table at 1e12 exists.** Continuing nine seeds is many CPU-hours on one thread, so I judge it not practical here. Reported only: the ng 80 / ng 64 ratio of ln m at z_f, carried on to the z = 0 table at 1e12, one rerun of the primary galaxy row. Not a grade.

## Lines, as FG1 froze them
S, Tl, LT both backgrounds; G CONSISTENT; K 15 of 15 on gas +0.005, f* 0.034, both h, failing keys listed; X |mean| <= 0.05, rms <= 0.10; Ln FC1's or KN1's class, computed here with the response-on halo through KN1's harness (X53) at KN1's frozen settings, FAIL if class LAW; Dw every class |Z| < 2, OP1's harness, EM1's M200, the 10^10 tag, Plummer baryons on M*, f_Q; MW feasible in priors, "wide priors only" is not a pass; DM r in 0.90-1.10 with n >= 27, by UR3's method as in SP3 (READ SP3, reproduced by rerun if SP3's script runs read-only); IC |Z| < 2, computed only if RF2's or ND1's path gives E at its radius for this halo with no new choice, else NOT GRADED.

Each cell tagged **[HM1]** computed here or **[READ lane]**. NOT GRADED is not a pass.

## Verdict
**PASSES EVERY GRADED LINE**, with NOT GRADED lines listed, or **FAILS**, with lines listed. Tags: **[GAS-CONDITIONAL]** if K's failure disappears at +0.111, per ZN4, the verdict staying on GS4. **[F*-DEPENDENT]** if K or X differs at 0.0615. **[BCG-DEPENDENT]**, **[RESPONSE-DEPENDENT]** if K or X class differs across reported cells. Beside the lines, no separate pass: BA1's joint chi^2 on the 15 keys (BA1's R, M3A1's `joint`, JOINT PASS p >= 0.05, FAIL p < 0.01); Z_tot for G-OUT-M3 by M3A1's quadrature, its systematic terms as M3A1 lists them.

**If it wins** (K and X both pass at +0.005 in the primary cell): seed bootstrap with ZN1's tail, 200 draws, both f*, both h; alt template; else the bootstrap isn't run, and I say so. No knob scans.

## The puzzle, reported, no verdict, no fit
On measured gas, NR3's S-core has G-OUT-M3 +0.10 (off) to +0.40 (Blumenthal) with X-COP failing (-0.160, -0.097); ZN4 has M3 +4.41 with X-COP passing (+0.013). M3 pred 1.558 vs 1.040. Note that NR3's row is on eRASS1's own gas and ZN4's on +0.005, so I also run S-core at +0.005.
1. M3 clusters, f* 0.034, h 0.672, same harness: M_c(r), rho_c(r), M_c ratio S-core / native, at 0.05, 0.1, 0.2, 0.3, 0.46, 0.7, 1, 1.42, 2.06, 3, 4.5 Mpc and r_ta; medians and 16-84. M_c(r_ta)/Mfair for both.
2. The pred split: shares of the OUTER keys from baryons and cold shells, for both curves, by shell.
3. X-COP: both curves at each graded x, residuals by x, the radius range in Mpc.
4. Requirement: from these alone, what M_c(r) has to do, in Mpc and R200, to carry X-COP as native does and M3 as S-core does. Numbers: mass needed in which shells, its size against Mfair and M0(r_ta). One diagnostic: native inside 0.75 R500 (X-COP's limit) and max(native, S-core) outside, through the same grader, labelled as a requirement test, **not a rule, no verdict and no free number**. Report any implied step in M_c at the join.

## Checks. A failed check means no verdict
- K1 f 0, BCG none: ZN4's preds and X-COP per key at gas +0.005 and +0.111, f* both, h both, |d| <= 1e-6.
- K2 SP3's native rows, EM1 `tot` and FC1, f 0 and f 0.872: Upsilon, rms, tilt, LT, groups, |d| <= 1e-6.
- K3 identity: Mb 0, F 0 returns M0 on native shapes, |d| <= 1e-6 inside the grid ends.
- K4 Blumenthal: M_c(r_ta) after / before, |d| <= 1e-3 on every cluster; count any exceptions. Gnedin's drift reported, as it isn't conserved at r_ta by construction.
- K5 S-core rebuild reproduces NR3 MEDIAN `EM1|off` and `EM1|blum` preds, |d| <= 1e-6; if not, the puzzle is labelled as on my rebuild with the difference given, and the verdict isn't affected.
- K6 f 0 through KN1's path reproduces +366.0 (|d| <= 0.1), through OP1's its P1 row (|d| <= 1e-3).
- K7 sign: UR1's flip on the native shape, M_f/M0 < 1 in cluster cores, > 1 in SPARC at r0, reported by radius.
- **MUTATE** f x 0.5 (0.436), separate outputs: must move a key's pred by over 0.01 and Upsilon by over 0.02, else UNDECIDED.

## Expectation on record, mine
**FAILS, about 97 %.** Lines: S (0.44/0.41 known), Tl, LT, G (+2.08 known), K, Ln, Dw; about 50 % that X fails too, since the outward core response lowers M_c inside and X-COP's mean sits at +0.013; MW, DM pass on SP3's reading, fragile. K: 12-13 of 15, G-OUT-M3 stays about +3.8 to +4.6, because OE1 says about 80 % of that bin is mass inside R200 plus baryons and the response at 1.42-3 Mpc is near 1. [GAS-CONDITIONAL] about 40 %, since response may move inner keys off 2. Ln stays LAW, about 95 %. Puzzle: I expect the S-core carries more M_c inside 1-3 Mpc because it puts all of Mfair inside r_ta, while native's M0(r_ta) sits below Mfair; so the requirement would read as mass that native holds beyond r_ta or doesn't have within it, and its size is unknown to me.

One thread, nice 15. Outputs small; caches gitignored. kappa = 1/2 FITTED. Not theory closed.

# OTA1_outer_share_to_turnaround: frozen criteria (committed alone, before any script or new number)

Not blind: ZN4's, FR1's, DR6's and M3A1's numbers are known to me (G-OUT-M3 +4.41 / +4.07 / +4.13 / +3.81 on measured gas +0.005; the miss in the 2.06-3 Mpc bin and M3's lighter half). kappa = 1/2 and X = 5.41 are FITTED. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework over LCDM. Nothing in `XJ1R_blind_caustic_junction/` is read.

## Question
Scorecard row 20 (outer cluster shear, G-OUT-M3) FAILS. PAPER72's open item 12 says the cluster's cold share is counted only inside R200c. Does counting the cold share 5.41 x baryons on the system's baryons out to turnaround, with the share beyond R200c placed in the reference layout and counted once, change the row?

## What the record's code does (read before writing; no number computed)
The chain is ZN4's grader text (ZN1's `zn1_grade.py`, patched by ZN4 and M3A1), on X74 / X73 / X30, with ZN1's `zn1_fn` and ZN3's `zn1_shape` giving the cold mass profile M_c(r) of every KiDS cluster and of every X-COP cluster.
- Baryons: X73's GC2 extension (`_gc2_ext`): gas beta model inside R500, rho ~ r^-2.777 beyond R500 (GC2's R5 tail, slope 2.7774425603108597), times (1 + f*), counted out to the self-consistent turnaround radius r_ta and flat beyond. `pp["Mfair"]` = X x M_b(< r_ta) (NATIVE). So the record already defines a cold share on the baryons to turnaround.
- Cold mass in `zn1_fn` ("fs" mode): R2 = the fair-share R200c, where (1 + X) M_b(< R2) = 200 rho_c(z) x volume. M_c(r) = f_c M2 m(r / R2), f_c = X / (1 + X), m = the zoom's native normalised profile, out to r_e = x_edge R2. If r_e >= r_ta (most M3 clusters, per DR6) M_c is the zoom shape cut at r_ta, and its total at r_ta is f_c M2 m(r_ta / R2), which is NOT set to X M_b(< r_ta). If r_e < r_ta, a power-law tail with slope gamma is solved so that M_c(r_ta) = Mfair (a thin closing shell, median gamma about -29 per ZN4); if M_c(r_e) >= Mfair there is no tail and the total exceeds Mfair.
- So the R200c cut is in the NORMALISATION: the record ties the cold share to the baryons only at R2 (X x M_b(< R2)); beyond R2 the amount is whatever the zoom shape (a cosmic-fraction-of-the-infall-mass layout) or the closing shell gives. The cosmology layout's "inside R200c" in PAPER72 is a separate bookkeeping, not touched here.

## The rule, OTA1 (exact)
For every cluster in `zn1_fn`'s "fs" mode, with the record's R2, r_ta and Mfair = X x M_b(< r_ta) (baryons beyond R200c = the record's measured-gas extrapolation: GC2's slope-2.777 tail from R500 to the self-consistent r_ta, as stored in `pp`):
- r <= R2: M_c unchanged.
- R2 < r <= r_ta: M_c,new(r) = M_c(R2) + lambda [M_c(r) - M_c(R2)], lambda = (T - M_c(R2)) / (M_c(r_ta) - M_c(R2)), T = M_c(R2) + S (Mfair - M_c(R2)).
- r > r_ta: M_c,new = T.
- Rule: S = 1, so the total cold mass inside r_ta is exactly X x M_b(< r_ta), counted once, and the share beyond R2 keeps the record's own layout (the zoom's outer shape, or the record's tail where it has one), rescaled.
- If the record's increment M_c(r_ta) - M_c(R2) is below 1e-9 Mfair, the extra is placed at uniform density between R2 and r_ta (count reported). If r_ta <= R2, or no fair-share R200 exists (ZN1's A2 item 6 case), the cluster is left unchanged (count reported).
- The same wrapper reaches X-COP's 12 clusters through the record's own call in the X-COP tail. Groups and SPARC do not use `zn1_fn` and are not reached (reported unchanged as a check).

## One pre-declared bracket (reported, never graded)
B: the baryons beyond R500 in the count only (Mfair, not the baryon lensing term) with the outer gas slope at GS1's range ends, 2.676 and 3.071, r_ta held at the record's; Mfair' = X x M_b'(< r_ta), M_b'(r_ta) = M_b(R500) + [M_b(r_ta) - M_b(R500)] I(s') / I(2.777), I(s) = integral from 1 to r_ta / R500 of y^(2 - s) dy. KiDS clusters only (X-COP's `pp` has no R500 and keeps the rule). f* 0.034 only.

## Grading (the record's lines, unchanged)
Gas +0.005 (GS4, measured), M3A1's driver text (ZN4's grader, ZN4's ng 80 shapes), all 15 keys, cells f* 0.034 / 0.0615 x h 0.672 / 0.686. A key passes when |Z| <= 2 in both h cells at that f* (ZN4's line); Z = (A - pred) / s with s the grader's (stat-only, as ZN4 / M3A1). X-COP passes when |mean| <= 0.05 and rms <= 0.10. Footings: canonical and alt graded side by side, never pooled (the grader computes both; in "fs" mode the KiDS prediction does not take the footing, and this is reported, not assumed).

## Lane words (per footing)
- **OUTER SHEAR ROW PASSES WITH THE SHARE TO TURNAROUND**: G-OUT-M3 |Z| <= 2 in all four cells.
- **STILL FAILS**: G-OUT-M3 |Z| > 2 in all four cells; tag (OVER) if Z < -2 anywhere. **STILL FAILS [CELL-DEPENDENT]**: passes in some cells, not all.
- **NO VERDICT**: any known answer or check below fails, or the twin does not bite.
Separate word for other keys: **OTHER KEYS: NONE BROKEN** / **OTHER KEYS BROKEN: [list]**, where broken = a key (any of the other 14, G-OUT-M2 and G-OUT-Mall named) or X-COP that passes at an f* in the base run and fails at that f* under the rule. Keys that fail in the base and pass under the rule are listed as moved in.

## Known answers and twins (failure = NO VERDICT)
- KA1: base run (no wrapper) reproduces G-OUT-M3 canonical +4.41 / +4.07 (f* 0.034, h 0.672 / 0.686) and +4.13 / +3.81 (f* 0.0615) to |d Z| <= 0.01, and X-COP +0.013, 0.075 / +0.005, 0.074 to 0.001.
- TW0 (zero extra share): T = M_c(r_ta), so lambda = 1: every key's pred and Z in both footings equal the base run to |d| <= 1e-9 (pred) at f* 0.034. Must hold.
- TW2 (doubled share, S = 2): must move G-OUT-M3 by |Z_TW2 - Z_base| >= 0.10 in every cell at f* 0.034 (canonical). If not, the change cannot reach the key: NO VERDICT.
- K1: under the rule, per cluster (canonical, h 0.672, f* 0.034 dump), M_c,new(r_ta) / Mfair = 1 to 1e-9 and M_c,new = M_c at r <= R2 to 1e-12 relative.
- K2: groups Z and SPARC numbers unchanged by the rule (|d| <= 1e-12).
Reported: median lambda over M3 and over all clusters; the record's M_c(r_ta) / Mfair; how many clusters have the tail, no tail, no fair share.

## Expectation on record (before any number)
STILL FAILS. In the record's M3 layout the zoom shape cut at r_ta probably holds roughly the cosmic fraction of the infall mass; the measured baryons to r_ta (FR1: the gas fraction is below cosmic at R500) likely give LESS cold than that, so lambda < 1 and G-OUT-M3 gets worse. If lambda > 1, the extra mass beyond R2 lands mostly beyond 3 Mpc and raises Sigma(R) as much as the mean inside (DR6's lesson), so a few tenths at most. OTHER KEYS: NONE BROKEN expected.

## Runs
nice 19, one thread, serial. Jobs: BASE, RULE at both f*; TW0, TW2, B(2.676), B(3.071) at f* 0.034. Outputs only in this folder. Other lanes' files read only. No push (the lead pushes).

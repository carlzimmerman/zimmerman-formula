# BA2_one_template_reread: FROZEN CRITERIA (committed alone, before any script or restated number)

**Question.** G-OUT-Mall and G-OUT-M1 to M3 read X7's fixed A_CAL and s_CAL, computed on the C\* template at f★ 0.20 with no tail. Their predictions, and the other 11 of the 15 shear keys, use the run's own template (`../NZ1_zoom_core_radius/nz1_one_template.py`). X71, GS1, X73 and GX2 predate that finding and their labels have not been rechecked. FC1, MA1 and NZ1 have been restated at ng 48 only. On one template, which labels change, and does the X71 break and X73 fix story survive?

**Standing.** κ = ½ FITTED. Footings canonical and alt are never pooled. The fluid is cold dark energy. Not "theory closed". Nothing here says the data favour the framework. A label that comes out wrong or failing gets reported as found. No tuning, no parameter scan, no physics re-derived.

**What I have already seen, disclosed.** The READMEs and frozen numbers of X71, GS1, X73, GX2, FC1, MA1, NZ1 and BA1, and `nz1_one_template.out`, which gives A at five templates and the ng 48 restatement of FC1, MA1 and NZ1. No restated number for X71, GS1, X73 or GX2, and none for FC1, MA1 or NZ1 at ng 64.

**My expectation, by hand from those committed numbers, not a result.** X71's G-OUT-M3 rises to about +3. X73 PRIMARY's G-OUT-M3 moves from about −0.75 to about +1. X73's s16 edge may then recover while its s84 edge breaks UNDER. GS1's R4 stays a key pass. GX2's Mall and M keys move further OVER, because raising the gas lowers A on its own template.

## The step (the same as `cells()` in `../ZN1_zooms_to_z0/zn1_grade.py`)
For each footing and each h cell, with M the run's own measured-side table:
- A(G-OUT-Mall) = `M["<foot>|<h>"]["M_all|OUTER"]["A"]`; A(G-OUT-M<t+1>) = `M["<foot>|<h>"]["M_terc|OUTER"][t]["A"]`.
- s_new = s_frozen × A / meas_frozen; Z = (A − pred) / s_new.
- pred is unchanged. The other 11 keys are unchanged. SPARC, groups and X-COP do not read these four keys and are unchanged.

## What is restated
Every run executes that lane's own script text with asserted string replacements (`nz1_one_template.py`'s and `zn1_grade.py`'s pattern). The replacements only redirect writes to a temporary directory and add a dump of what the run already holds. Both footings, both h cells.

| Lane | Script text | Configuration | f★ | Status |
|---|---|---|---|---|
| X71 | `x71_fstar.py` | smooth, inherited 5.364, no tail | 0.034, 0.0615 | graded, reread only (see below) |
| X71 | same | Burkert, inherited, no tail | 0.034, 0.0615 | reported |
| X71 | same | smooth, inherited, no tail | 0.20 | K2 |
| GS1 | `gs1_gas_slope.py`'s `_child` | R4, R5, RX48 at s_meas, s16, s84 | 0.20, the only f★ GS1 graded | graded |
| X73 | `x73_all_measured.py` | PRIMARY: smooth, native, s_meas | 0.034, 0.0615 | graded |
| X73 | same | smooth, native, s16 and s84 | 0.034, 0.0615 | graded, its FRAGILE read |
| X73 | same | smooth, native, no tail | 0.034, 0.0615 | reported, and the native side of the story |
| X73 | same | smooth, inherited, s_meas | 0.034, 0.0615 | reported, reread only |
| X73 | same | smooth, native, s_meas | 0.20 | reported |
| X73 | same | Burkert, native, s_meas | 0.034, 0.0615, 0.20 | reported |
| GX2 | `gx2_corrected_gas.py`'s `grade` | PRIMARY: infall, 0.364 r_ta, gas +0.111 | 0.20, the only f★ GX2 graded | graded |
| GX2 | same | V1, V2, PRIMARY at ±1σ | 0.20 | reported |
| FC1 | X74 text with `fc1_x74.py`'s INJ, `CE1_A4_*` tables | median | 0.034, 0.0615 | graded |
| FC1 | same | p16, p84 | 0.034, 0.0615 | reported |
| MA1 | `ma1_grade.py`'s worker, `CE1_A4_*` tables | median | 0.034, 0.0615 | graded |
| NZ1 | `nz1_grade.py`'s worker, `CE1_A4_*` tables, CLUSTERS | median | 0.034, 0.0615 | graded |
| K1 runs | FC1, MA1, NZ1 workers, `CE1_*` ng 48 tables | median | FC1 0.034, MA1 0.0615, NZ1 0.034 | K1 |

**Inherited inputs.** X71's frozen configuration, and X73's "inherited" rows, carry the Planck ratio 5.364 and H0 67.4. They are restated because this lane rereads that label, not to grade anything new. They are marked "reread only" everywhere, and no verdict of a rule rests on them alone. Every other run is on the native background.

## The joint read, beside the per-key gate
BA1's `joint()` text from `../BA1_joint_shear_statistic/ba1_grade.py`, on one template, canonical, 15 keys. R_orig for eRASS1's gas, R_gas for GX2's raised gas. Headline is the worse h cell. JOINT PASS p ≥ 0.05, JOINT FAIL p < 0.01, otherwise JOINT MARGINAL. As in BA1, it sits beside the per-key |Z| ≤ 2 gate and does not replace it.

Reported, not graded: χ² without the two INNER keys, BA1's jackknife R, and R computed in the run's own configuration by BA1's `ba1_worker_tail.py` text. BA1's R is canonical, so alt gets the per-key read only.

## Labels
Each lane's own frozen rule is applied to its 15 keys on one template, with its SPARC, groups and X-COP lines as that run returns them.
- **X71** (canonical carries; alt reported): SURVIVES, or BREAKS naming keys, sign and f★.
- **GS1** (per footing): MEASURED SLOPE PASSES (rules), ROBUST or FRAGILE, or MEASURED SLOPE FAILS.
- **X73** (per footing): `x73_summary.py`'s `grade`, `cls` and robustness rule.
- **GX2** (per footing): INFALL HALO + CORRECTED GAS PASSES CLUSTERS, or LENSING STILL FAILS naming keys. V1 and V2 reported.
- **FC1 A4** (per footing): `fc1_grade.py`'s COLD-SHARE PASS, KNIFE EDGE, F★-DEPENDENT, COLD-SHARE FAIL.
- **MA1 A4** (per footing): `ma1_grade.py`'s MASS ARGUMENT PASS, F★-DEPENDENT, MASS ARGUMENT FAIL.
- **NZ1 A4** (canonical, as frozen): `nz1_grade.py`'s classes, with X-COP as committed.

**What counts as a label change.**
- **HELD:** same class, same named lines, signs, f★ variants and slope edges.
- **NAMED LINES CHANGE:** same class, but a named key, its sign, the f★ variant or the failing slope edge differs.
- **CLASS CHANGE:** the lane's rule returns a different class.

Each lane's frozen label stands as frozen in its own record. This lane does not edit other lanes' files. It reports the reread beside them.

## The story, frozen
X71's README says measured f★ breaks G-OUT-M3 UNDER. X73's says the measured gas tail fixes it.
- **S1, the break.** G-OUT-M3 has Z > +2 on one template, in at least one h cell at both measured f★. Read on X71's runs (the label being reread) and on X73's native no-tail runs (the same core with no Planck input).
- **S2, the fix.** In X73 PRIMARY, at both measured f★, all 15 keys have |Z| ≤ 2 on one template in both h cells.

**STORY SURVIVES:** S1 on both reads and S2. **BREAK GONE:** S1 on neither. **S1 SPLIT:** S1 on one read only. **TAIL DOES NOT FIX:** S1 and not S2, naming keys and sign.

Reported: the f★ step and the tail step in G-OUT-M3's Z, on one template and as graded; the sign of the residual at PRIMARY; X73's table "What moved G-OUT-M3" on one template; which slope edge fails. X73's claim that f★ 0.20 over-predicts G-OUT-all reads a key the defect never touched, and I will say so.

## Checks (any failure means no verdict)
- **K1:** restating FC1|0.034, MA1|0.0615 and NZ1|0.034 at ng 48 reproduces `nz1_one_template_results.json`: meas, s, pred and Z, 15 keys, both h cells, |d| ≤ 1e-9.
- **K2:** at f★ 0.20 with no tail (X71's smooth run) the fix changes nothing: A against A_CAL and restated against frozen Z, four keys, both footings, both h cells, |d| ≤ 1e-9.
- **K3:** every re-run's frozen read (meas, s, pred, Z, 15 keys, both footings, both h cells) reproduces that lane's committed JSON, |d| ≤ 1e-9.
- **K4:** BA1's committed χ² for MA1 at f★ 0.034 is reproduced from its committed cells, |d| ≤ 1e-9, and R from X73 PRIMARY at f★ 0.034 reproduces BA1's R_orig, |d| ≤ 1e-9. BA1 built R there.
- **K5:** the template does not depend on the core rule. At the same f★, slope, normalisation and gas, M_outer agrees between rules, |d| ≤ 1e-12: X71 smooth and Burkert; GS1's R4, R5, RX48 at each slope; X73 PRIMARY, FC1, MA1 and NZ1 at each f★; GX2's PRIMARY, V1, V2. FC1's template also reproduces `nz1_one_template_results.json`'s provenance, |d| ≤ 1e-12.
- **K6:** each lane's rule applied to its frozen cells reproduces its committed label: X71's BREAKS line, GS1's classes, `x73_summary.json`'s verdict and robustness, GX2's verdict, FC1's and MA1's A4 labels, NZ1's A4 read, and every committed `fails` and `failing` list.
- **K7:** the runs change no tracked file outside this lane.
- **MUTATE** (`--mutate`, separate outputs): the restate step reads the terciles in reverse order, M1's A into M3's key and M3's into M1's. K1 and K2 must fail and X73 PRIMARY's G-OUT-M3 must move by more than 0.05 in Z; otherwise the lane is UNDECIDED. In the same run, d × 2 must raise χ² × 4 exactly.

## Reported, not graded
- The largest gap between the run's own s_STAT ratio and A/A_CAL, which tests the rule that s scales with A.
- χ² as the grader read it, with the four keys on X7's values, for contrast only.

## Run rules
One thread (OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, VECLIB_MAXIMUM_THREADS=1), `nice -n 15`, an idle driver plus at most three workers, under 1 GB each, beside the priority zooms. Nothing in `../X48_native_cf_zoom/`, `../ZN1_zooms_to_z0/`, ZN2, ZN3, LC1, `compute_queue/` or `real_research/` is written. No home-directory path in any committed file. No downloads.

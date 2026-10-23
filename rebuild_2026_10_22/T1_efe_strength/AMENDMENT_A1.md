# T1_efe_strength AMENDMENT A1 (PRE-RESULT; append-only)

Written after the coordinator's instruction of 2026-10-23 ("include P2 in your EFE-strength fit; use P2's likelihood vs ε
as the outer-lensing dataset in place of F2's, or show both and say why they differ; report whether the satellite and
Coma preference for weak EFE conflicts with P2's preference for an EFE"). **No script of this lane had run and no number
of this lane existed** when this was written. The frozen criteria (0fbdb17c87) stay as committed; this file adds to them.

**Seen before writing (disclosed).** P2's README, AMENDMENT_A1 and results JSON (commit 1ebfa54245): S3 amplitudes for
(a) y_e = 0, (b) the catalogue field and (b_lo); the uniform-field scan A_in, A_O1, A_O2, A_out ± σ at y_e = 0, 1e-6 …
1e-2 on both footings (canonical A_out 0.195 ± 0.269 at 0, 0.374 ± 0.336 at 1e-4, 0.916 ± 0.615 at 1e-3); y_need = 1e-4;
the catalogue field medians (c10 6.56e-5 / 5.43e-5) and brackets.

## 1. New dataset LENS-P2 (P2's spectroscopically isolated GAMA lenses × KiDS-1000, S3, hole-subtracted)

- Input, read-only: `rebuild_2026_10_22/P2_spec_isolated_lensing/p2_spec_isolated_lensing_results.json`,
  `diagnostics.<footing>.scan` (P2's own uniform-field model: T_own + neighbour-term difference, F2's AQUAL solver).
  P2 cannot be re-run here (its shear cache is outside the repo); its committed scan is the likelihood.
- Statistic: P2's outer amplitude A_out (GLS data/model over 0.4–2.6 Mpc, F2's estimator) at each uniform y_e;
  χ²_P2 = ((A_out − 1)/σ_out)², ν = 1. y_e → x_e with `f2_aqual.x_of_y`; linear interpolation in x_e between nodes.
- ε reference (ε = 1): the uniform field at P2's catalogue median, y_e = 6.56e-5 canonical / 5.43e-5 alt (x_e ≈ 0.0081 /
  0.0074). **Caveat carried into every statement:** this field holds catalogued galaxies' baryons only (0.048 of Ω_b);
  P2 states it would be 20–130× larger if all baryons (or the dust) traced the galaxies. So P2's ε is relative to a
  lower bound on v3's field. P2's "bary" bracket (y_e 1.38e-3 / 1.14e-3) is reported as a second reference.
- Reported: A_O1, A_O2 per node; P2's per-galaxy (b) and (b_lo) amplitudes; the full 7-point outer χ² of (a), (b), (b_lo)
  from P2's profile and covariance; the absolute x_e at which the curve is minimised and its 95 % range on P2's whole
  scan (beyond ε = 1.5 if needed; the combination itself stays on [0, 1.5]).

## 2. Combinations (replaces §3's set for the primary; everything else in §2–§4 applies unchanged)

- **Primary V = {SAT, COMA, LENS-P2, GC@floor}.** LENS-F2 leaves the primary: its photo-z isolation leaks ~38 % of
  hosts (F2 AMENDMENT A1), and P2's spectroscopic, hole-subtracted sample does not reproduce its tension.
- Secondary combinations, in addition to C1–C6 of §3 (C4 now means V − LENS-P2):
  C7 = V with LENS-P2 replaced by LENS-F2 (the frozen primary of 0fbdb17c87, reported in full);
  C8 = {SAT, COMA, LENS-P2} (hosted systems against lensing, no globulars);
  C9 = {COMA, LENS-P2} and C10 = {SAT, LENS-P2} (the direct S1-vs-P2 conflict tests the coordinator asked for);
  C11 = {LENS-F2, LENS-P2} (why the two lensing readings differ, on one ε axis per its own reference; both also in
  absolute x_e).
  LENS-F2 and LENS-P2 share the KiDS shear and are never in the same combination except C11, which is a diagnostic.
- The verdict rule of §4 is applied to the new primary V. The class under C7 (old primary) is reported; if it differs,
  the verdict is FRAGILE as §4 already says.

## 3. Checks added or changed (pre-result)

- **K3b (new):** the P2 read is internally consistent: scan node "0" equals P2's `amplitudes_S3.<f>.a` (A_out, σ) to
  1e-12; P2's `efe_solves` x_e equal `f2_aqual.x_of_y(y_e)` to 1e-9; and a GLS amplitude recomputed from P2's (a) profile
  vector, model m_a and covariance over the outer bins reproduces A_out(a) to 1e-6.
- **K8 (threshold changed):** the F2 solver's criterion becomes "last Kacanov change < 1e-3". Reason: F2's solver stops
  at maxit = 300 with a last change up to 3e-4 at y_e = 1e-6 (P2's committed `efe_solves`), and F2's own K1 shows the
  isolated limit to 1e-4 in that state. Every solve's last change is reported. The D10-solver line (< 1e-8) is unchanged.
- `--mutate` also hands LENS-P2 nothing new (it is read, not solved); K3b is not a mutate target.

## 4. What the conflict question means (added to §5)

If the hosted systems (SAT, COMA) want ε near 0 while LENS-P2 needs a field (ε > 0 at 95 %), the AQUAL EFE strength is
not one number across these data under v3's other assumptions; §5's "inconsistent" reading applies and the conflicting
pair is named. P2's reference field is a lower bound on v3's field, so a conflict measured in P2's catalogue-field ε is
the **strongest** form of it: in units of a larger true field, P2's required ε shrinks. The reference-free part is P2's
exclusion of a zero field (ε = 0) against the hosted systems' upper bounds; both are reported, and the conflict is
also restated with P2's "bary" reference.

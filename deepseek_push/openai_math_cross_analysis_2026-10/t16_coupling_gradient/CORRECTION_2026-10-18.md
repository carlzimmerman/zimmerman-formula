# T16 correction (2026-10-18, calc chat; owner go): group/cluster windows used mismatched deficits

FROZEN_CRITERIA.md, the script and the outputs are unchanged. This note sits beside them.

The group and cluster inputs 0.79/1.76 and 0.41/0.91 are CFG382 definition A,
x_A = (M_tot - M_b - M_ph)/(5.364 M_b): the excess beyond the law, per cosmic cold share. They are not
x = M_missing/M_b = (M_tot - M_b)/M_b, the definition stated in FROZEN_CRITERIA and used for the MW-30 point. The exact
relation is x = 5.364 x_A + (nu - 1) (verified per object to 4e-15). The tell is in T15 C1 itself: f_obs(clusters) =
1/(1 + 0.41) = 0.709, while X-COP measures f_b = 0.163 (b = 0).

On the stated definition (campaign_fresh_gravity/CFG453_t15_deficit_units, criteria b1132dd48, result de0514adb; both
a0 footings, never pooled), with x = 5.12/7.74 for clusters and 10.8/15.9 for groups at b = 0/0.3:
- Clusters M_cold/M_b = +3.8 to +4.3 (b = 0) and +6.4 to +6.9 (b = 0.3); groups +9 to +14. Positive, not overdrawn.
- No lambda ceiling: the dark mass exceeds even the fully settled kernel supply, so the floor lambda 0.028 is allowed at R500.
- Clusters dark mass = 0.95 of one cosmic cold share; groups 2.0 (gas-poor, f_b 0.084).

Therefore, NOT TO BE CITED:
- The group and cluster lambda_max windows (groups [0.0117, 0.0288], clusters [0.0073, 0.0172]), C2 (the three-way
  intersection [0.0152, 0.0172]), C3 (the floor-vs-cluster bind, 1.63x), C4 (the gradient n span) and C7 ("the floor and
  the cluster budget cannot share one lambda").

On the stated definition the group and cluster windows have no upper bound, so no three-way intersection is defined, and
the floor lambda 0.028 is not excluded by the clusters. Unaffected: the MW-30 rows and C5 (the M_b = 7e10 knife-edge at
V ~ 195), which use the stated definition. CFG451/CFG452 (re-runs on the framework's a0 and a0(z)) inherited the same inputs
and carry the same pointer.

# FRZ3R AMENDMENT A1 (2026-11-12): a positive-definite turnaround-scope reading added (reported); the as-frozen reading stays first

Committed alone, while the frozen run is in its anchor stage and before any flux-level number has been opened, printed or
graded. The frozen reading (READING.md, commit 4abb5b4a36) is not changed and is graded and reported first.

## What I saw (matter level and floors only)

To catch a failure early I opened the matter-level ratio and the floor counts of the first four anchor parts (z 2.2, seeds 0
and 1, both footings); no flux array was read.

- Known answer (b) at z 2.2: realised matched ratio at k 1 / 3 / 5 = 0.9884 / 0.8058 / 0.7213 and 0.9952 / 0.8297 / 0.6972
  (canonical, seeds 0, 1) against FRZ1's 0.9911 / 0.8732 / 0.7674 (tolerance at k 3: 0.042); alt seeds 0, 1: 0.9899 /
  0.8165 / 0.7449 and 0.9980 / 0.8269 / 0.7070 against 0.9917 / 0.8787 / 0.7952. At k 3 the realised field removes more
  power than FRZ1 on both seeds; (b) is likely to fail at z 2.2 in the seed mean. The plain painting gives 0.913 to 0.924
  at k 3. Probable cause: in a 20 Mpc/h box the rare haloes above about 1e12.5 Msun/h that carry much of P_std's one-halo
  power at z 2.2 are mostly absent, so the realised reference power is below P_std R_bar while the difference, carried by
  smaller haloes, is not.
- Floors: the graded field M has 5.8 to 6.0 % of its gas pixels below 1 + delta = 1e-6 (floored); the plain field P
  2.7 to 2.9 %; the reference R 0.11 %. A scratch diagnostic at N 256, z 2.2 traced this to the halo difference itself: both
  C1 and U_B - U_Rb subtract the NFW-extension mass between r200m and r_ta (and part of the cusp), but the reference halo
  (U_std plus condensation) does not hold that mass; the smooth component there is too thin to cover the deficit. The
  two-halo factor is not the cause.

So the frozen graded field is not a physical density field in about 6 % of its volume, and those pixels are set to full
transmission in the flux step. The frozen label is computed and reported first as frozen, with this stated beside it.

## What is added (reported reading T; never replaces the frozen label)

**Reading T, the turnaround-scope halo model realised on its own terms:** reference haloes painted with U_Rb, form-B haloes
with U_B (both positive, mass M_ta inside r_ta), the same uniform Poisson positions; smooth lognormal component with weight
1 - (painted M_ta) / (box mass) and target power S_T = P_Rb,ta - (expected one-halo power of the painted U_Rb), where P_Rb,ta
is FRZ1's turnaround-scope spectrum of the comparison layout (its `spectra_ta`); FRZ1's two-halo difference realised on the
smooth component as in READING section 2. Its expected matter ratio is the turnaround-scope ratio P_B,ta / P_Rb,ta, which is
about half of FRZ1's R_cold - 1 at k 3 (READING section 1). This is the field the lead's brief describes ("realise the halo
model itself"), and it is positive by construction.

- Known answers for T: (a), (c), (d), (e) as in READING; (b_T): realised ratio within 0.01 + 0.25 |R_T - 1| of the halo
  model's own P_B,ta / P_Rb,ta at k 1, 3, 5 at the anchors; also reported against FRZ1's R_cold (expected to fail).
- Mutations for T: M1 and M2 as in READING (M2 doubles U_B - U_Rb; floors reported).
- Brackets for T (anchors, seeds 0, 1): lambda_P x 0.5, x 2 and 100 proper kpc.
- Seeds: all 12 bins with seeds 0 and 1; anchors also seeds 2 and 3.
- Reported for T: flux Delta chi^2 (12 bins), matter Delta chi^2 of the same fields through the record's projection, their
  ratio, and, as a POST HOC indicator only, FRZ1's matter-level 9916.2 / 9008.7 times that ratio.
- T carries a label line computed with READING section 8's rules, written as "reading T (reported, not the frozen label)".

Code: a new file `frz3r_turn.py` (the frozen files are not edited while their run is live); parts `turn_*`. It runs after the
frozen stages, as the same single job.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

# CFG453 FROZEN CRITERIA: does T15/T16's cluster/group "overdraft" come from a units mismatch in the deficit x?

Frozen before any CFG453 script exists. kappa = 1/2 is FITTED. Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10) are
reported separately, never pooled. No dark-matter particle; the cold fluid's mass is still required. Read-only on
deepseek_push (T15, T16), CFG382, CFG450-452.

## The suspected mismatch (from the committed text, before any computation here)
- T15 FROZEN_CRITERIA defines x := M_missing/M_b with x = (1 - f_obs)/f_obs, f_obs = M_b/M_tot, i.e. x = (M_tot - M_b)/M_b.
  Its MW-30 point uses exactly that (T15/T16: x = (V^2 r/G - M_b)/M_b).
- For groups and clusters it inserts CFG382's definition A, which is (M_tot - M_b - M_ph)/(5.364 M_b): a fraction of the
  cosmic cold share with the law's phantom M_ph = (nu - 1) M_b already removed. These differ by the factor 5.364 and by M_ph.
- T15's own C1 then reports f_obs(clusters) = 1/(1 + 0.41) = 0.709, a 71% baryon fraction.

## Gates
- **D1 (definition check).** From the X-COP files and Lovisari table exactly as the CFG382 audit reads them (gas at R500,
  CFG450), compute per object f_b = M_b/M_tot (M_tot = M_HSE/(1-b)) and x_T15 = (M_tot - M_b)/M_b, and check the identity
  x_T15 = 5.364 x_A + (nu - 1) per object to 1e-9 (both footings, b = 0 and 0.3). If the measured median f_b(clusters, b = 0)
  lies in [0.08, 0.25] and T15's implied 0.709 lies outside it, **the mismatch is CONFIRMED**; otherwise NOT CONFIRMED.
- **D2 (the budget on T15's own definition).** Recompute T15's M_cold/M_b = x - f_law S/M_b and T16's lambda windows with
  x = x_T15 (medians), everything else held as CFG451 (lambda 0.028, f_law 0.280 as coded, tau, rho_R500, the MW points).
  Two S rows, reported separately:
  - (i) T15's conventions (groups M_b 6e12 / 554 kpc; clusters 2.8e13 / 985 kpc);
  - (ii) per-object S from each object's own M_b and R500 (median of x - f_law S over objects).
  Per footing: V1 sign of the cluster M_cold at b = 0 and 0.3; V2 groups; V4 floor/cluster gap (>= 1.5 STANDS, 1.0-1.5
  WEAKENED, < 1.0 BREAKS: the floor lambda fits the clusters); V5 three-way intersection (frozen MW M_b 7e10, and T16-verbatim).
- **Headline.** If D1 CONFIRMED and V1 is >= 0 for clusters at b = 0 on both footings under row (i) or (ii) -> **"the
  overdraft was a units artefact"**; if D1 CONFIRMED but V1 stays negative -> "mismatch real, overdraft survives it";
  if D1 NOT CONFIRMED -> "no mismatch".
- **Also reported (not a verdict):** the like-for-like cold ledger at R500: M_ph/M_b (law phantom), 5.364 x_A (beyond-law
  excess), their sum vs the cosmic share 5.364, i.e. whether each object's dark mass fits inside one cosmic cold share.

## Controls
- **C1:** with the def-A inputs and T15's conventions, the code reproduces CFG451's committed cluster/group rows to 1e-9.
- **C2:** x_A medians equal CFG450's committed ones (canonical clusters 0.4135/0.9054) to 1e-3.
- **MUTATE (CFG453_MUTATE=1):** plant the T15 misread on purpose (x := x_A in the D2 recompute). V1 must return negative on
  both footings. Outputs go to *_MUTATE files.

A failed control is reported and kept, never silently fixed. CFG451/CFG452 used the same def-A inputs; whatever D1 decides
applies to them too and will be said in the README.

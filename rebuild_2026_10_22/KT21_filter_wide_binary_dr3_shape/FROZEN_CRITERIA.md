# KT21_filter_wide_binary_dr3_shape — FROZEN CRITERIA (before the grading script or any graded number)

Question: KT20 predicts that KT17's filter (xi = 0.55 sqrt(G M / a0)) keeps wide binaries nearly Newtonian at high internal
acceleration, while plain QUMOND with the simple nu already boosts them by several percent there. Does the inner shape of the
Gaia DR3 wide-binary velocities on disk tell the two apart?

κ = 1/2 FITTED and held fixed. Footings 9.3603e-11 and 1.1312e-10 graded separately, never pooled. Not theory closed.
No download. Nothing in the Gaia DR4 pre-registration is read for grading or edited; this is a DR3 lane and not a DR4 result.

## Data
`real_research/data/widebinaries/dr3_extract/wide_binaries_dr3.csv` (frozen-cut DR3 extract on disk, 6,210 pairs,
2-30 kAU; columns sep_kAU, v_perp_kms, M1_msun, M2_msun). All pairs used, no further cuts.

**Disclosure.** Before freezing this I saw, in the record, binned median vtilde from a different substrate (9,508 pairs from
the full El-Badry catalogue, `wb_mond_orbit_mc.out`): 0.558 at g_N/a0 about 56, 0.561 at about 5.6, 0.599 at about 1.8. The
bins, statistic and tolerance below were chosen for where the models differ and where contamination is lowest, not tuned to
those numbers, but the owner should know they were seen.

## Statistic
vtilde_i = v_perp / sqrt(G M_tot / s_proj). y_i = G M_tot / (a0 s_proj^2), per footing.
Bins: **H** y >= 10, **M** 2 <= y < 10. Q = ln median vtilde(M) - ln median vtilde(H).
sigma_stat: bootstrap over pairs, 2000 resamples, seed fixed. sigma_sys = **0.020** (from `kt21_sys.py`, committed with
these criteria, which reads no wide-binary data: eccentricity index changing by 0.2 between bins 0.016, triple fraction 5 vs 3
percent 0.012, noise allowance 0.003). sigma = sqrt(sigma_stat^2 + sigma_sys^2).

## Predictions
For each pair, 40 Newtonian Kepler orbits (f(e) ~ e^1.2, uniform mean anomaly, random orientation), each rescaled so its
projected separation equals s_proj; this gives r_3D and a Newtonian vtilde. Model X multiplies that vtilde by sqrt(gamma_X(r_3D)),
gamma_X = KT20's 1D external-field form (simple nu, g_e = 1.9e-10 m/s^2): Newton (gamma 1), plain (xi 0), filter (xi 0.55 r_M,
r_M = sqrt(G M_tot / a0)). Q_X,pred is formed exactly as Q on the mock, binned by the data pair's own y.
z_X = (Q_obs - Q_X,pred) / sigma.

## Labels, per footing
- X **CONSISTENT** if |z_X| <= 2; **TENSION** if 2 < |z_X| <= 3; **EXCLUDED** if |z_X| > 3.
- Headline: **FILTER FAVOURED OVER PLAIN** if plain is EXCLUDED and the filter CONSISTENT on both footings; **PLAIN FAVOURED
  OVER FILTER** if the reverse; **BOTH CONSISTENT**, **BOTH EXCLUDED**, or **NO VERDICT** (anything else, including footings
  that disagree). Newton's label is always reported beside; a filter win over plain is not a win over Newton.
- Beside, not graded: g_e = 2.32e-10; f(e) index 1.0 and 1.4 in the mock.

## Checks
- C1: gamma_X here equals KT20's `kt20.json` gamma_plain and gamma_filter at its listed separations (canonical and alt,
  1.0 and 1.5 Msun, g_e 1.9e-10), max relative difference <= 1e-10.
- C2: Newton's Q_pred within 0.005 of 0 (the Kepler mock is scale free).
- C3: at least 500 pairs in each bin, each footing.
- C4: sigma_stat from a second bootstrap seed within 20 percent of the first.
- MUTATE (`--mutate`, nu = 1): all three models give the same Q_pred; written to `*_MUTATE.*`, exit 1.

Exit 0 only if C1-C4 pass. A failed check is disclosed and the labels are still printed.

## Limits stated in advance
The boost is applied as a velocity rescale at the current r_3D, not by integrating orbits in the modified potential (the
record shows integrated predictions depend on the orbital prior). 1D external-field form, no anisotropy. The statistic tests the
inner shape only; it says nothing about the 10-20 kAU level where the published analyses disagree.

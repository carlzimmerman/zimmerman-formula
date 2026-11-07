# SV5 iter_1: any sector, a0 law on on the linear web. NO-GO FOR CLASS W

Kappa = 1/2 FITTED; not theory closed. Criteria FROZEN_CRITERIA.md (247d2eaa2f), Amendment A1 (technical). Script ../sv5_web.py;
outputs sv5_iter1.json, sv5_iter1_MUTATE.json, ../sv5_web.out, ../sv5_web_MUTATE.out.

- Target realisation (dust reference x A_X0 = 1.021), 128^3 in 2000 Mpc, QUMOND simple nu on the peculiar field.
- Lensing amplitude r = 74.7 (canonical) / 89.4 (alt) against 1 +- 0.072 (3 sigma_A): W1 FAIL. B(k) is nearly flat in k (e.g. z 1:
  41.3-44.2), so the shape gate passes (dchi^2 0.0) and the miss is all amplitude.
- Rigorous floor per z: nu(y_max)^2 = 24.9 (z 0.25), 15.2 (z 1), 6.1 (z 5), 1.75 (z 50) canonical; 29.5 / 17.9 / 7.0 / 1.89 alt.
  The integrated ratio is 3.1-85.
- MUTATE (nu == 1): r = 1, dchi^2 0 on both footings, so the gate passes when the law is off: bites.
- Lean: `law_on_power_bound`, `nu_antitone`, `nu_ge_two`, `nu_lawS` (written, NOT COMPILED; see ../README.md).

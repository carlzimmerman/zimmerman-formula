# SV5 iter_2: K(Q) Jeans scale switched by the AC2q charge D.P + 2X. NO-GO FOR CLASS C (inside the action)

Kappa = 1/2 FITTED; not theory closed. Criteria FROZEN_CRITERIA.md (247d2eaa2f). Script ../sv5_web.py; outputs sv5_iter2.json,
sv5_iter2_MUTATE.json.

- Sigma_* = min host phantom charge at r_ta = 4.66e-26 / 5.12e-26 kg/m^3 = 8.0 / 6.0 rho_DE (UGC02487 is lowest; the KiDS bins
  and the 1e10 reference are higher). Host charge falls monotonically with r inside r_ta on every host (C1).
- Web (law on, iter_1's field): mass fraction with charge >= Sigma_* is 0.25 / 0.36 / 0.47 / 0.53 / 0.54 / 0.52 / 0.51 at z 0.25 /
  0.5 / 1 / 2 / 3 / 12 / 50 (canonical; alt within 0.003), against 0.036. C2 FAIL on both footings.
- AC2q's own sign switch (threshold 0) would stiffen 51-81 % of the web.
- Cassini: the Galaxy's charge at the Sun is 7.5e4 / 5.8e4 rho_DE, so the Sun sits in a stiff, sector-free region (C6P inherited).
  c_T ARGUED unchanged. G5/G6/G7 pass by QX10's convention only; expulsion dynamics NOT EVALUABLE.
- Conditional branch (law off on the web, not in the action): Sigma_web = 2X <= 2 rho_DE < Sigma_*, so C2 would pass. Reported.
- MUTATE M1 (switch off): G5 4.23, bites. M2 (web charge 0): C2 PASS, bites.
- Lean: `switch_ordering`, `switch_no_window`, `deep_point_flux(_deriv)`, `deep_point_rho_antitone` (written, NOT COMPILED).

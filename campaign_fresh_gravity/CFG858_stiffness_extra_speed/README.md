# CFG858 — can the stiffened action produce the dwarfs' extra speed (V_x² ≈ a0 × 31 pc)?

Criteria: `FROZEN_CRITERIA.md` (bb25c4ddd, before the script). Run: `python3 cfg858.py` (MUTATE `CFG858_MUTATE=1`). ~1 min.

## Result — CLASS: **STIFFNESS ONLY SCREENS** (the coincidence is not derivable from the stiffened action)
- **Identity first:** V² = a0 L ⇔ L = r_M(M), M = V⁴/(G a0): "a0 × 31 pc" just restates V_x ≈ 9.4 km/s as the deep-law speed of ~6e5 M_⊙.
- Solving the canonical v2 stiffened field equation u²/(a0 − u) − (L*²/2)∇²u = g_N (BVP, regular centre, law at large r) for six dSph
  Plummer profiles: the stiffened acceleration at r_1/2 relative to the law, G_ratio, is ≤ 1 at every L* (1 pc – 1 kpc), both footings:
  at L* = 24 pc 0.93–1.00, at 31 pc 0.89–1.00, at 100 pc 0.44–0.95, at 1 kpc 0.05–0.24. The maximum anywhere in radius is 1.0000
  (no overshoot). K1: L* = 1 pc reproduces the law (0.9999). MUTATE (anti-stiffness, sign flipped) produces overshoot (up to ×1.98):
  the solver responds to the term, as required.
- **So stiffness can only remove boost from dwarfs, never add it.** The globular-cluster floor L* ≥ 24 pc (CFG820) already screens the
  dSphs by 1–11% at r_1/2, which makes the extra component they need slightly LARGER, not smaller.
- **The coincidence's base rate:** a random log-uniform L in [24 pc, 1 kpc] lands within ×1.3 of 24 pc 7% of the time. Not significant.
- Deviation (disclosed): Sextans has no Weisz SFH, so Υ_V = 2 (as CFG821) instead of Υ_SFH.
- **Reading:** the extra ~10 km/s isothermal component in faint dwarfs (CFG856) cannot come from the stiffened field; it needs an
  additional cold-mass component or a different term in the action.

κ = ½ fitted; cold energy mass required; not theory closed.

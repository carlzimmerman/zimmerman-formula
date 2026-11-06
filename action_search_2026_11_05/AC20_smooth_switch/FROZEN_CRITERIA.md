# AC20 frozen criteria (top level): smoothing the stiffness switch

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Lane rules:
closure_2026_11_06/SWARM_BRIEF.md.

Why: AC16 (6d5faba9bd) proved v3s / AC2q have no C1 solution across a transverse switch interface,
because F(Pi) = (gamma/2) max(Pi, 0)^2 has F' = gamma max(Pi, 0), whose x-derivative jumps by gamma Pi_x.
X3 already showed that any smoothing with F'' > 0 on the soft side gives c^2 = Pi F'' < 0 there (Hadamard).
So the only admissible smoothings keep F = 0 for Pi <= 0 and raise the contact order at Pi = 0.

Two iterations, both frozen now (before either is computed), each with its own file:
- iter_1_power/FROZEN_CRITERIA.md: pure powers F = (gamma_n/n) max(Pi, 0)^n, n = 3, 4.
- iter_2_contact/FROZEN_CRITERIA.md: contact form F = (gamma/2) Pi_+^4 / (Pi_+ + a)^2, equal to v3s for Pi >> a,
  with a = s^2 (AC2q: its own 2X; v3s: 2 rho_DE, fixed by the a0 law, no new constant).

Common machinery: the PN label system of AC10/AC16 (1D planar, K terms dropped as in AC16 numerics),
general stiffness force -d_x F'(Pi). Lean: fable_independent_2026/lean_2026/AC20_smooth_switch.lean and
_MUTATE twin (claims listed in each iteration's file). Compute: one thread, nice -n 15.

# DOOR C1 — Feed the trajectory in: omega_star = 2 pi T_eff = sqrt(a^2 + H^2)
STATUS: OPEN | RANK: 2 | COST: M | KILLS FAST: YES

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
This is the single highest-value repair in the whole programme. Review's structural theorem: the NESS solvers
have signatures `(tau_grid, q_sq, eta)` — **no trajectory, no proper acceleration, no y anywhere.** So
rho_NESS depends on (q, eta) only, delta_m is a NUMBER, and nu is a CONSTANT (1.2793, flat to 2.4% across
y = 1e-4…1e4). MOND cannot come out for any q.

And the fix already exists in your own code: `tn15:194` computes the correct Deser-Levin
`T_eff = sqrt(T_GH^2 + (accel/2pi)^2)` and `tn15` defines `rindler_trajectory()`, `proper_acceleration()` and
`source_spectrum(omega, accel)` — and then **never feeds any of them into the kernel** (last occurrence line
207, inside a print loop). Feeding them in is what turns r from a hand-set number into a computable one.

## Why it works with the framework
Deser-Levin's T_eff is the framework's own temperature, and `mi_circular_dS_response_2026.py` (8/8) *derives*
it from a computed detector response to 1e-15 rather than assuming it. Making the kernel depend on it is the
framework being self-consistent, not a new postulate.

## Concrete first calculation
1. Rebuild the kernel from `tn15`'s own `source_spectrum(omega, accel)` so it carries a.
2. Solve on a grid of a/H spanning 1e-3…1e3 and tabulate delta_m(a).
3. Extract the two master-formula numbers: `c1p = lim_{T→∞} f(T)/T` and `f'(T_GH)`.
4. Form `r = f'(T_GH)/c1p` and `q_cross = 2/r`. Compare to r = 1, 4pi, and 2Z = 11.577620.

## Settles if / refuted if
CONFIRMS (huge): r finite and near 2Z ⇒ **the first derived coefficient in the programme.** Then it must clear
all six steps of `../06_VERIFY_PROTOCOL.md` before being written as anything stronger than "candidate".
KILLS: r = 2 ⇒ the mechanism is committed to a0 = c H_Lambda (Milgrom 1999's value) and kappa = 1/2 is
unreachable from it. That is the current de facto state: `tn18:202` hard-sets omega_star = 1.0 = H, which
*asserts* a0 = c H_Lambda, i.e. r = 2 — wrong by exactly Z = 5.788810.

## Known walls — do not rediscover
The corpus's flagship "r_derived = 1.8426 from first principles" is **r/2pi** (1.842635, verified): q was
normalised to c H_Lambda/2pi, which IS Milgrom 2020's a0, so it is the identity a0(framework)/a0(Milgrom2020).
Not a derivation. Do not re-report it as one.

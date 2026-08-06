# DOOR F1 — Solve the localized system as a finite-past initial-value problem
STATUS: OPEN | RANK: 4 | COST: M | KILLS FAST: YES

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
At `omega_c = a_0/c` the memory time is **101.5 Gyr = 7.4x the age of the universe**, so only **12.7%** of the
kernel weight lies inside any real worldline's past, and the frozen homogeneous mode retains **87%** of its
initial value over cosmic time — dominating the rotating part of chi by ~7.7e6. Every steady-state transform in
the corpus therefore rests on a premise that fails at its own kernel scale. Nobody has solved it as an actual
initial-value problem.

## Why it works with the framework
It uses the framework's own localization, which is exact: one auxiliary scalar for the square root
(`sqrt(X) = min_lambda [X/2lambda + lambda/2]`, a genuine minimum) and N first-order ODEs for an N-pole memory
(`chidot + omega_c chi = omega_c a`). No approximation is introduced by this door — it removes one.

## Concrete first calculation
1. Integrate the coupled system on a finite worldline: `xddot = -grad Phi + (memory terms)` together with
   `chidot_i + omega_i chi_i = omega_i a`, with `chi_i(-T) = 0` and `T = 13.797 Gyr`.
2. Use a two-pole Prony kernel so the localization is exact.
3. Compare the resulting rotation curve to the steady-state transform prediction.
4. Test initial-data sensitivity: vary `chi_i(-T)` and see how much the answer moves.

## Settles if / refuted if
KILLS the steady-state reading: if the answer is initial-data-dominated, then every C and S number in the
corpus (including the 1/C = 8.87e6 suppression) is inapplicable at `omega_c = a_0/c`, and the honest conclusion
is that a_0/c is not a physically usable kernel scale. Review's estimate: `1/|C| >= 3.4e3` on a finite past,
with the asymptote `omega_c/Omega` — **one** power of c/v, not two.
CONFIRMS: the answer is insensitive to initial data ⇒ the steady-state transforms are legitimate and the
suppression stands.

## Known walls — do not rediscover
The localization itself is verified exact (residual identically zero). What is unverified is the steady-state
*premise*, not the algebra.

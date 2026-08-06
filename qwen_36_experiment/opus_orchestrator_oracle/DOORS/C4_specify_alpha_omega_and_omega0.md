# DOOR C4 — Specify the bath spectral density alpha(omega) and a detector frequency omega_0
STATUS: OPEN | RANK: 4 | COST: S | KILLS FAST: no (but yields the programme's first finite magnitude)

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
Every delta_m in tn16/tn17 is **IR-divergent**: review verified `delta_m ∝ 1/omega_min` exactly (1.53e16,
1.58e17, 1.59e18, 1.59e19 for omega_min = 1e-3…1e-6 — exactly 10x per decade). So the numbers are the value of
`np.logspace(-4, ...)`, not physics. The cause: the Caldeira-Leggett mass shift needs the **bath spectral
density** `J(omega) = pi alpha(omega) omega`, not the bare field commutator, and alpha is never specified.
Introducing a detector frequency omega_0 regularizes it: `int rho/(omega^2 + omega_0^2)` is finite.

## Why it works with the framework
⭐ This is the door where **a_0 can enter the mechanism instead of the answer.** omega_0 is exactly the place a
physical scale belongs, and the framework already has candidates for it: `a_0/c` (memory time 101.5 Gyr) and
the committed `omega_c = 1.78e-14…2.21e-14` window.

## Concrete first calculation
1. Compute delta_m with three regularizations at matched norm: a Lorentzian `1/(omega^2+omega_0^2)`, a hard
   cutoff, and `exp(-omega/omega_c)` — **the last is McGaugh 2008 ApJ 683,137 eq.11a, cite it** (RULE R2).
2. Set `omega_c = a_0/c`, i.e. `omega_c/H = 1/Z = 0.17275`, and also scan the committed 1.78-2.21e-14 window.
3. Report the finite delta_m for each, both a0 footings.

## Settles if / refuted if
SETTLED: you obtain the programme's first **finite** delta_m — a falsifiable magnitude the corpus currently
lacks, even if it is anti-MOND. Publish it as such.
FORKS: if the answer depends strongly on which regularization, then the mechanism does not predict a magnitude
and you must say so rather than picking the friendliest one.

## Known walls — do not rediscover
omega_c is a **free fifth constant** (FRAMEWORK_FACTS #8) — do not present a choice of it as a derivation. And
at omega_c = a_0/c the memory time is 101.5 Gyr = 7.4x the age of the universe, so only 12.7% of the kernel
weight lies inside any real past: see F1 before trusting a steady-state number at that scale.

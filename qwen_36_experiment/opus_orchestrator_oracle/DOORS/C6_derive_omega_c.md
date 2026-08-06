# DOOR C6 — Derive omega_c, the free fifth constant
STATUS: OPEN | RANK: 7 | COST: M | KILLS FAST: no

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
Every nonlocal-kernel verdict in the corpus turns on omega_c and **nothing derives it.** At `omega_c = a_0/c`
the Milky Way in-phase gain is `C = 1.1e-7` (deep suppression); at the committed window
`omega_c = 1.78e-14…2.21e-14` — five orders larger — the same formulae give `C = 0.997` and **no suppression at
all**. Same equations, opposite verdicts. That is the largest single unresolved lever in the programme.

## Why it works with the framework
omega_c is the MI completion's own memory scale. Deriving it removes a parameter rather than adding one, and it
would settle the suppression question that currently has two defensible answers.

## Concrete first calculation
1. List every candidate: `a_0/c`, `a_0/2c`, `sqrt(G rho_Lambda) = 1/t_dyn`, `H_Lambda`, `a_0/v_rel` (Route B's
   choice), and the committed `OMEGA_C_LO/HI`.
2. For each, tabulate the MW in-phase gain C and the quadrature ratio S/C.
3. Then ask which, if any, follows from something: the committed window came from `Re G >= 0.90` at UGC05721's
   inner orbit plus the LLR Gdot/G ceiling — i.e. from **observation**, not theory. Can a *theoretical* argument
   land in it?
4. If the Kubo route is taken seriously, its kernel relaxes at `tau ~ 1/H`, i.e. `omega_c ~ 2e-18` — four
   orders BELOW the observational window and squarely in the suppressed regime. Make that an explicit,
   falsifiable prediction.

## Settles if / refuted if
CONFIRMS: a derivation landing inside 1.78-2.21e-14 ⇒ the suppression problem dissolves and MI is unsuppressed
at galactic frequencies.
KILLS: a derivation giving `omega_c ~ H` or `a_0/c` ⇒ MI's nonlocal reading IS suppressed by ~1e-7 at galactic
frequencies, and the framework must live in the local/algebraic reading only. Either is a real result.

## Known walls — do not rediscover
`mi_kernel_axis_separation_omegac_2026.py`'s own verdict is "omega_c IS NOT REDUNDANT" — it is a genuinely free
constant, and Route B's S2 proves the circular identity forces c out of tau_mem (p = 0 exactly), leaving an
infinite-dimensional family. Do not claim to have fixed it by picking a member.

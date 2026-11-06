# QX1: the equation chain, in order, with its algebraic steps certified in Lean: CERTIFIED (as frozen)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (0bc8da973b), frozen before any
Lean was written.

- **The chain:** `../EQUATIONS_IN_ORDER.md`. It runs from the action through the field equations, FRW, law S / the deep
  law, PPN, c_T, lensing and Cassini/Lstar, then AC2q's reductions. Every step carries exactly one tag: LEAN, SYMPY, NUM
  or POSTULATED/FITTED.
- **Lean:** `fable_independent_2026/lean_2026/QX1_closure_chain.lean`. 28 theorems, 0 errors, 0 sorry. `#print axioms`
  gives exactly propext, Classical.choice and Quot.sound for all 28 (`QX1_closure_chain.out`).
- **MUTATE twin:** `QX1_closure_chain_MUTATE.lean` fails on exactly its 4 declared false claims and on nothing else.
  Only those 4 theorems depend on sorryAx (`QX1_closure_chain_MUTATE.out`).
  - M1: off-region stiffness = -2 gamma X^2
  - M2: 1 + J_Y = 1/(1+u)
  - M3: the clock-only stream folds iff Omega tau_f <= 1/sqrt 2
  - M4: law S gives g < g_N

## What the new certificates cover

- **J(Y):** its derivative, J_Y = -1/(1+u), and 1 + J_Y = mu(u). Also mu's deep and Newtonian bounds.
- **Law S:**
  - the balance is equivalent to g^2 = g_N(g + a0);
  - the positive root;
  - its uniqueness (requires a0 >= 0);
  - g_N < g < g_N + a0;
  - the exact Tully-Fisher relation v^4 = GM(a0 + v^2/r).
- **Clock bound:** s^2 <= 8 a0^2/(G c^2) at kappa = 1/2.
- **AC2q's stiffness:**
  - it equals v3s's at X = 0;
  - the on- and off-region pieces;
  - continuity at the switch;
  - it is zero on FRW;
  - AC10's charge form at N = 1.
- **AC10's clock-only stream:** it solves J'' = Omega^2 (1 - J), and it folds iff Omega tau_f <= 1.
- **AC9:** the group velocity of a massive tensor; the masses vanish at s = 0; dv/c < 1.3e-46 / 2e-46 at 100 Hz (the
  proof uses pi > 3.14).

These are cited, not re-proved:
- a0 = c^2 sqrt(Lambda/32 pi) (TOE_BEST_ATTEMPT);
- kappa = 1/2 is not derivable (KAPPA_LOGIC);
- the alpha ≡ 1 law, the switched stiffness and the saddles (V3_PICTURE);
- leaf convexity (XC2, XC5);
- law S differs from law B (EQB_A0LINE).

## Steps left SYMPY/NUM

These are PDE-level or numerical statements, so they are not certifiable in Lean here:
- PPN gamma = beta = 1 (V3W W1);
- c_T = c (V3W W4a; the principal part in AC9 T1a);
- lensing = dynamics and the AC2q slip (V3W W3, AC9 T2);
- the Cassini hedgehog and the Lstar floor (C6/C6P, D10);
- X3's well-posedness;
- the derivation of the weak-field system from the action (C4 K1);
- AC7 Q1/Q2 and AC8;
- the SPARC RAR fit (P4);
- the AC10 first-fold numbers, and AC11/AC12.

Lean cannot certify that the action is right, or any of the inputs. kappa stays FITTED.

## Build note

This checkout had no `.lake`, so `lake env lean` cloned the pinned packages. `lake exe cache get` then unpacked Mathlib's
build from the local `~/.cache/mathlib` ("No files to download"). `.lake` is git-ignored, and no committed file changed
for the build.

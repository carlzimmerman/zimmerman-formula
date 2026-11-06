# QX1 frozen criteria: what counts as "certified" in the equation chain

Frozen before any Lean file in this lane is written. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Deliverables

1. closure_2026_11_06/EQUATIONS_IN_ORDER.md. The equation chain, in order: action, field equations, FRW,
   static weak field, law S / deep law and a0, PPN, c_T, lensing, Cassini/Lstar, then AC2q's reductions.
   Each step carries exactly one tag:
   - LEAN: file + theorem name;
   - SYMPY: committed script + commit;
   - NUM: numerical lane + commit;
   - POSTULATED / FITTED: a hand input.
   No step is left untagged.
2. fable_independent_2026/lean_2026/QX1_closure_chain.lean and its twin QX1_closure_chain_MUTATE.lean.

## A Lean step counts as CERTIFIED only if

- it compiles with `lake env lean QX1_closure_chain.lean` with 0 errors and no `sorry`;
- `#print axioms` lists only propext, Classical.choice, Quot.sound for every theorem;
- the statement is the algebraic step as the chain doc writes it, with the physical premises as hypotheses,
  not built into the definitions;
- the outputs are saved as QX1_closure_chain.out / QX1_closure_chain_MUTATE.out.

## MUTATE twin

The twin is the same file with exactly 4 declared false claims:
- (M1) the off-region stiffness is -2 gamma X^2;
- (M2) 1 + J_Y = 1/(1+u);
- (M3) the clock-only stream folds iff Omega tau_f <= 1/sqrt 2;
- (M4) law S gives g < g_N.

It must fail on exactly those 4 theorems and on no others. If it fails anywhere else, or does not fail on one of
the 4, the certification has no power and nothing is CERTIFIED.

## Scope stated now

Lean certifies only that the premises imply the conclusions. It cannot certify:
- that the action is right;
- any numerical lane;
- PPN or c_T as PDE statements: the record has these as SYMPY/NUM, and they stay tagged that way;
- kappa: it stays FITTED (KAPPA_LOGIC_2026_10_20.half_not_derivable).

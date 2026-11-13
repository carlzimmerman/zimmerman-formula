# KAP1 RESULT: KAPPA NOT DERIVED (2026-11-12)

Criteria `FROZEN_CRITERIA.md` (3116ad793b, committed alone before any script or number). Script `kap1.py` ->
`kap1.out`, `kap1.json` (exit 0); twin `KAP1_MUTATE=1` -> `kap1_MUTATE.out`, `kap1_MUTATE.json` (exit 1, the control bites).
Attempts commit 681cfa10b7. TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.

## Verdict

**KAPPA NOT DERIVED.** No route meets the five frozen conditions. The new inputs (the collapse, the fold reach, the
static-state identities) cannot do the work: none of them carries c, and without c no condition can fix a universal kappa.

| route | postulate (one line) | number | label | check |
|---|---|---|---|---|
| L1 (lemma) | the new inputs are functions of G, rho, M_b, a0 (and r, t set by them), no c | only group a0/(G rho^(2/3) M_b^(1/3)) | HOLDS | sympy nullspace; adding c yields kappa itself; adding mu_K yields a0 mu_K/(G rho), a TRADE |
| R1 fold reach | r_M = sqrt(G M_b/a0) equals R_fold (FLD1, z = 0; and R_fold = f R_max in the de Sitter limit) | kappa 1.7e-4 (log M_b 8) to 2.4e-3 (11.5); 2.3-3.5 dex below 1/2; slope 0.331 | NOT DERIVED | sympy d ln kappa/d ln M_b = 1/3; SI chain; twin f -> 2f gives exactly 1/4 |
| R2 fold ratio | kappa = R_fold/R_ta | 0.52 at z 0 (0.0170 dex from 1/2, window 0.0178) | NUMEROLOGY | per mass 0.517-0.525 (0.525 is outside the window); 0.46 / 0.435 / 0.32 at z 1 / 2 / 4; d ln R_fold / d ln a0 = 7.6e-4 (a0-blind, so the counterfactual S2 fails); sympy: the uniform-sphere virial ratio R_vir/R_ta is exactly 1/2 |
| R3 joint stress | at the fold, static-halo stress g^2/(8 pi G) (FB1, deep field) = vacuum pressure rho_Lambda c^2 | fixes g_* = sqrt(8 pi) c sqrt(G rho) at the fold; implied kappa 1.0e4 to 1.5e5 (4.3-5.5 dex above 1/2); slope -0.331 | NOT DERIVED | law S inversion checked in sympy; sympy and SI chains agree to 1e-9; twin 8 pi G -> 4 pi G gives 0.49996 |

Closed-route list in the criteria: 42 family lines (the record's register holds 847 rows).

## What each route shows

- **L1.** COL1's collapse is a weak-field calculation in an FRW background (kpc, km/s, Msun; c appears only through the
  numerical value of a0, which is an input). FLD1 reads such runs. FB1's identities (sigma^2 = (1/2) sqrt(G M_b a0),
  J(g) = (a0^2/4 pi G)[u - ln(1+u)]) contain no c. Over {G, rho, M_b, a0} the dimension matrix has one null vector,
  a0/(G rho^(2/3) M_b^(1/3)). So any condition built from these inputs either holds for every a0 or gives
  a0 = F G rho^(2/3) M_b^(1/3), which changes with mass, while a0 is the same for every galaxy to 0.041 dex. This
  extends the record's rule S1 (CFG893) to the inputs the earlier attempts did not have. It is a dimensional statement;
  it does not exclude a route that brings c in from elsewhere.
- **R1** is the c-free class exactly: slope 1/3 in sympy, 0.331 on FLD1's radii.
- **R2.** 0.52 lands inside the window for 1/2 at z = 0, and only there. It does not change when a0 changes
  (canonical and alt footings give the same fold radius to 1e-4), it falls to 0.32 by z = 4, and it is a
  spherical-collapse number of the virial class (R_vir/R_ta = 1/2 for a uniform sphere). This is a coincidence with no
  mechanism. It is recorded so that nobody later cites it as a derivation.
- **R3** is the one route here in which c enters, through rho_Lambda c^2. It fixes a field strength at the fold, not
  a0. Getting a0 needs the fold radius and the mass, so the result depends on mass. It also misses badly: the law's own
  halo field at the fold is 2.1-2.7 dex below g_*. Matching a static stress to the vacuum pressure at a place set by
  collapse belongs with FINAL-19's ceiling and the W_v slot: it picks one number from a menu of conventions.

## Raw facts that differ from the brief

- The brief's "fold radius 0.52 of the turnaround radius at every mass" holds today only: FLD1 gives 0.46, 0.43-0.44
  and 0.31-0.33 at z 1, 2 and 4.
- Law S and the slow tail share the deep-field coefficient (both have mu -> x). The 26 % difference between their fitted
  a0 (1.128e-10 against 8.96e-11) comes from the transition region. A deep-field (Tully-Fisher) derivation would speak
  for both kernels. A derivation that ties a0 to an energy density at a finite u = g/a0 would carry the kernel's shape
  into kappa (see below).
- KA1 reproduces the canonical a0 as 9.3624e-11 from H0 67.4 and Omega_L 0.685 (2.2e-4 from 9.3603e-11). That is
  rounding in the footing inputs and changes no label.

## The missing ingredient

The adopted action has two independent couplings: the law sector's scale a0, inside W (equivalently in
J(g) = (a0^2/4 pi G)[u - ln(1+u)]), and the vacuum energy rho_Lambda c^2. The vacuum energy sits outside the switch,
with W(0) = 0 (TPA1, W4-24). The static, collapse and fold sectors are c-free (L1), so they cannot relate the two.

For kappa to follow, all of these would have to be true and shown:
(a) the vacuum energy is not an additive constant but the law sector's own energy in a state the dynamics selects,
rho_Lambda c^2 = w_* a0^2/G, with the additive constant removed by a named symmetry, quantisation or dynamics (rules S6);
(b) the pure number w_* comes out of the equations, not out of a choice of matching point or convention; then
kappa = 1/sqrt(w_*), and kappa = 1/2 needs w_* = 4 (G rho_Lambda = 4 a0^2/c^2, which the rules forbid as a premise and
which would have to be the output);
(c) because J is zero in the deep field (u -> 0) and different kernels differ at finite u, a selected state at finite
u fixes the kernel at the same time as kappa. So the derivation has to name the kernel, and it predicts the transition
shape that SLK1 can test;
(d) the same mechanism makes a0 follow the vacuum energy, a0(z) proportional to sqrt(rho_DE(z)). That is its second,
testable consequence, and it is untested today (KAPPA_CLOSURE section 3).

Until such an equation exists, kappa = 1/2 is FITTED. This is the record's xi = 1 / premise-A gap, sharpened: the
missing equation has to be relativistic and has to connect the vacuum constant to the law sector's potential. It cannot
come from the collapse or the fold.

## Lead's estimate (disclosed in the criteria, unverified there)

KAPPA NOT DERIVED. The outcome agrees with it. My own hand estimates in the criteria matched every label.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

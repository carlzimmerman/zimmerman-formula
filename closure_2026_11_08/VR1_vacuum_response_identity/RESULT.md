# VR1 RESULT: NO IDENTITY (criteria 78587ef63d)

Owner-named lane, 2026-11-08. Question: is there one new, physically stated premise about how the vacuum responds to
the khronon acceleration that forces kappa = 1/2 exactly and is not the answer restated? **No.** Four candidates,
declared with their option spaces before any number (FROZEN_CRITERIA.md), were run. None gives 1/2 except by putting
in the record's known posit (xi = 1). The known-answer controls all read RESTATEMENT, every mutation changes the
outcome, and the Lean file compiles with standard axioms only while its _MUTATE twin fails 4/4. Adopts nothing.

Files: `vr1.py` -> `vr1.json` / `vr1.out`; `MUTATE=1` -> `vr1_MUTATE.*`; `VR1_vacuum_response.lean` (+ `.out`, 7
theorems, axioms propext / Classical.choice / Quot.sound, no sorry); `VR1_vacuum_response_MUTATE.lean` (+ `.out`, 4
false statements, each fails: lines 14, 29, 33, 42).

## Kinematic input (checked, not a premise)

In AC2q the dark-energy scalar is the clock. With X = s^2/(2N^2) and the khronon acceleration A_i = c^2 d_i ln N
(sympy derives it from the Christoffel symbols of g = diag(-N^2 c^2, 1, 1, 1)), we get exactly

    grad ln X = -2 A / c^2        (residual 0)

So the vacuum's kinetic density responds to khronon acceleration over the response length L_v = c^2/(2|A|). This is
the khronon form of KF1's "the 1/2 is the 2 in g_00". It supplies the 2, and the map is exact: KF1's xi equals
L_v(a0) / l, with l = c/sqrt(G rho), and xi = 1/(2 kappa). The J-sector static energy density from the action is
(a0^2/4 pi G)[u - ln(1+u)] (sympy check True).

## Labels

| | Identity (in words) | Premise added to `Framework` | Outcome | Label | Mutation |
|---|---|---|---|---|---|
| KA-1 | KF1: a0 = c^2/(2 xi l) | `resp` with xi | kappa = 1/(2 xi); 1/2 iff xi = 1 (Lean `ka1_reduction`, `ka1_half_iff`) | RESTATEMENT (as required) | response factor 1 -> kappa xi = 1 (Lean M4 fails) |
| KA-2 | GF2 SIS ratio | none | sigma^2/v_f^2 = 1/2 at kappa 1/2 and 1/3 | RESTATEMENT (as required) | n/a |
| KA-3 | p32_iff | 32 pi relation | kappa = 1/2 | RESTATEMENT (as required) | n/a |
| V1 | At the switch acceleration a0, the vacuum's response length c^2/(2 a0) equals the vacuum's own gravitational length | `resp`: c^2/(2 a0) = l_v | kappa^2 = 1/(4q) with l_v^2 G rho = q c^2 (Lean `v1_general`); 1/2 iff q = 1, i.e. l_v = c/sqrt(G rho) = KA-1's posit. The six declared lengths give 1.447 (c/H), 1.772 (Poisson), 0.921 (c t_ff), 0.282 (Jeans, in window), 2.507 (1/sqrt Lambda), 0.230 (2 pi c/H, in window); none has q = 1 (Lean `v1_options_not_half`) | RESTATEMENT for 1/2; menu of DERIVES OTHER otherwise | X ~ N^-1: every kappa doubles (2.894, 3.545, 1.843, 0.564, 5.013, 0.4607) |
| V2 | The khronon's acceleration energy cancels the vacuum term where the foliation's acceleration reaches the horizon scale, J(Y*) = 0 | `cancel` + A* = f c H | f = 1 (cH) and f = 1/2 pi: no root for any kappa (Lean `v2_reduce` + `v2_no_root`: kappa^2 [u - ln(1+u)] <= 8 pi/3 < 4 pi). f = 2 (Unruh root): kappa = 11.18, out of window | NO IDENTITY | A* x2: a root appears (11.18 for cH; 1.511 for 4cH); Lean M2 fails |
| V3 | At the switch u = 1 the khronon's static energy density equals the clock's kinetic energy at its bound (S7 class, flagged in advance) | `equip`, r in {1/2, 1} | kappa = 4.525 / 6.399 (kappa^2 = 4 pi r/(1 - ln 2)); never 1/2 (Lean `v3_not_half`) | DERIVES OTHER (excluded) | u = 2: 2.640 / 3.734; Lean M3 fails |
| V4 | The blend switches where the law's phantom density at the transition radius of an isolated mass equals b = rho_DE | `blend` | rho_ph(r_M) = sqrt(5) a0^(3/2)/(10 pi G^(3/2) sqrt M): kappa^2 grows as sqrt(M) | NO IDENTITY (host-mass dependent, D6) | g_N = a0/4: coefficient changes (sqrt 17/68), still M-dependent |

`vr_not_derivable` (Lean): adding the kinematic response length (L_v * 2 a0 = c^2) to `Framework` still admits
kappa = 1/2 and kappa = 1/3. The kinematics carries the 2, not the length.

## Which half_not_derivable premise the identity would have to add

`half_not_derivable` rules out deriving kappa from einstein + friedmann + tie + fourform. The vacuum-response route
adds one premise, `resp`: the response length at a0 equals a named vacuum length. That premise fixes kappa (Lean
`v1_general`), but only through q, the pi content of that length. Every length that GR or Newtonian gravity builds
from rho_DE and c carries pi (8 pi G/3, 4 pi G, 3 pi/32, the Jeans pi), so q is never 1. q = 1 is the pi-free length
c/sqrt(G rho), which is xi = 1, i.e. premise A ("couples through G, not 8 pi G"). VR1 therefore moves the open
target no further than KC1 left it, but it states it sharply inside the khronon action: **the missing identity is
"the vacuum's response length at the switch is c/sqrt(G rho_DE)", and nothing in reach supplies a pi-free length.**

## Cold component (COLD DARK ENERGY)

The only determinate response, (R) integrated (X ~ N^-2, so delta rho/rho_K = -2 Phi/c^2), assigns the vacuum a
gravitating response of at most 4 rho_DE |Phi|/c^2 (clock bound X <= rho_DE c^2, active density 4X). That is 6.9e-8
of the X-COP cluster need inside r500 and 7.7e-14 of the 5.41 x baryons the CMB needs at z 1100. It tracks host depth,
which the ARGON assessment Q1(ii) already excludes. V2-V4 add nothing beyond the law's own phantom. **The identity
says nothing about the cold component.**

## What was not done

No second prediction (rules S4) arises, because no candidate reaches 1/2. The non-radial or time-dependent response
of the vacuum (fold layers, AK1) is outside this lane. The candidate set is the declared one; other premises are not
ruled out by this lane, only by the record's walls (KAPPA_DOORS: c required, pi-parity, hbar-free, zero mode).

kappa = 1/2 FITTED; not theory closed.

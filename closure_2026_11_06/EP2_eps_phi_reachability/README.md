# EP2: does any record background history reach eps_phi = 2? NOT REACHED, both footings

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: CRITERIA.md (c9fe71ac87), frozen before any
script. Script: ep2.py -> EP2.json, ep2.out. Successor to EP1's reachability label, which stays NOT DECIDED as EP1
froze it.

## Label: NOT REACHED

Exact expression for a canonical clock: eps_phi(z) = (1+z) rho_DE'(z) / (2 rho_tot), with rho_DE kept in rho_tot.

| History | canonical (omega_DE0 0.311) | alt (omega_DE0 0.454) |
|---|---|---|
| H-flat (footing background) | 0 exactly | 0 exactly |
| H-native, CFG689 a0(z), median | max 0.227 (z 0.4) | max 0.274 |
| H-native, worst-case history (2.5 % -> 97.5 % quantile edges) | max 0.989 | max 1.227 |
| H-CFG689 fitted nodes, best / worst (footing-free) | 0.220 / 1.141 | same |
| H-CPL (reported, to z 1100) | max 0.167 at z 0; phantom (eps_phi < 0) above z 0.354 | 0.185 |

The largest graded value is 1.227 (alt, worst case, z = 0.4) against the line 2, a margin of 0.77. Beyond z = 2.33
the native and CFG689 histories are held constant (eps_phi = 0). Reaching 2 there would need Omega_phi >= 2/3 with
w_phi >= 1/3, a clock that dominates the budget while redshifting at least as fast as radiation. The record has no
measurement there. That condition is stated, not graded.

## Known answers and MUTATE

- KA1: EP2's code with EP1's frozen bound reproduces EP1's REACH.json exactly (2.16276121853809, 0.5421219955861971,
  0.2205182284922488, 1.1788178001976903; relative difference 0).
- KA2: H-flat gives eps_phi = 0 exactly on both footings.
- KA3 (reported): the canonical omega_DE0 from a0 at kappa = 1/2 is 0.3110, against CFG689's fitted node 0 of 0.3116.
- M1 (gate): a planted kination clock (A = rho_m / 64) reads REACHED on both footings (eps_phi -> 3).
- M2: native slope x100 on [0.4, 0.7] reads REACHED (98.9 / 122.7), so the rule is sensitive where EP1's 2.16 sat.

## Disclosure

EP1's post-data variant (1.179) was known before EP2 was frozen. EP2's graded worst case is a different,
self-consistent history (the same rho_DE in the numerator and in rho_tot), computed only after the freeze.

## Consequence for the door

On the record's measured dark-energy histories and on the footing background, AC2q's clock never reaches
eps_phi = 2. EP1's decelerating fixtures describe no physical AC2q epoch in z <= 2.33. They are also HARMLESS
(scoped) as fixtures (EP1). Scope: z <= 2.33 measured, plus the held-constant reading beyond; not adoption.

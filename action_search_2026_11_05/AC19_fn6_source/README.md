# AC19: no action on the table supplies FN6's screening length: FAIL (post-result control)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (4b010d8f23), frozen before
the script. Amendment: AMENDMENTS.md A1 (POST-RESULT control). Script: ac19.py (sympy, exact exponents, <10 s,
one thread).

**Label.** As frozen: NO VERDICT, because the frozen MUTATE did not bite (see below). With the post-result
regime-consistent control MUTATE-B, which bites: **FAIL**. Neither v3s nor AC2q produces a length with mass
exponent in FN6's window [0.30, 0.45]. The exponents are exact rationals from each action's own static
equations, so the main result does not depend on a control. The control only shows that the grader can
return a PASS.

## Every admissible length (static, spherical, isolated, mu_K = 0)

| length | action | exponent p | MW size (canonical / alt) | regime |
|---|---|---|---|---|
| Lstar (stiffness; also D10's embedded scale) | v3s, AC2q | 0 | 0.022 / 0.023 kpc | - |
| r_M = sqrt(GM/a0) | v3s, AC2q | 1/2 | 9.45 / 8.60 kpc | - |
| stiffness vs source, deep MOND (AZ41 q = 2): Lstar^2/r_M | v3s, AC2q | -1/2 | 5e-5 / 6e-5 kpc | inconsistent (not r >> r_M) |
| GM/c^2 | both | 1 | 3e-6 kpc | - |
| c^2/a0 | both | 0 | 3e7 / 2.6e7 kpc | - |
| AC2q charge offset s^2 = 2 rho_DE vs phantom density, deep MOND | AC2q | **1/4** | 1710 / 1484 kpc | consistent |
| same, Newtonian | AC2q | 0 | 6e5 / 5e5 kpc | inconsistent |

There is no balance radius from: stiffness vs source in the Newtonian regime (the ratio is independent of r,
AZ41's high-field form), AC2q's P-equation offset (2 gamma s^2 <= 2.2e-10, constant, AC8), or v3s's dust term
(free constant, zero in galaxies).

The nearest miss is new. AC2q's own charge offset gives a genuinely mass-dependent length,
r_X = (2^(1/2)/(8 pi^(1/2))) c (GM)^(1/4) / a0^(3/4), with p = 1/4. That exponent is outside the window, and the
length comes out about 1.5 Mpc for the MW, about 600x FN6's L_MW. The window's own lower edge is set by the dwarfs
(FN6's T2 fails at p <= 0.2).

## Structural fact

FN6's L_MW of 1.5-3 kpc lies inside the MW's r_M of 8.6-9.5 kpc. Any action length that fills the window must
therefore be a Newtonian-regime balance radius. In both actions, the Newtonian-regime balances are
mass-independent (p = 0) or do not exist.

## Known answers and controls

- KA1: AZ41's q = 2 crossover Lstar^2/r_M and its exponent (q-3)/(4q-6) = -1/2 are reproduced exactly.
- KA2: AZ41's high-field ratio at q = 2 is radius-independent, as reproduced.
- KA3: rho_DE = 4 a0^2/(G c^2) gives 5.8424e-27 / 8.5328e-27 kg/m^3, matching AC6/AC7.
- MUTATE (frozen; ac19_MUTATE.*, exit 1): did NOT bite. The planted rho_X ~ M^(-1/4) length was normalized to
  2 kpc as a deep-MOND radius, but 2 kpc < r_M, so the regime check rejected it. This was a defect in the plant's
  design, and it is what exposed the structural fact above.
- MUTATE-B (post-result, AMENDMENTS.md A1; ac19_MUTATE_B.*, exit 0): a planted rho_X ~ M^(-3/8) offset,
  normalized to a 2 kpc Newtonian balance radius, grades PASS (p = 3/8, regime-consistent). The control bites.
- Rerun: ac19.json is byte-identical across the three runs (sha1 f9cd6ab3d7f3).

## Scope

Static, spherical and isolated. Constitutive families not on the table stay as AZ41 left them: screened, none
regular. Environment-embedded lengths other than D10's (which scales with Lstar, p = 0) and any nonlinear or
dynamical lengths are not covered. The FN6 window itself (AZ43 robustness) is untouched. This closes the door
only for v3s and AC2q: neither action is the source of FN6's window.

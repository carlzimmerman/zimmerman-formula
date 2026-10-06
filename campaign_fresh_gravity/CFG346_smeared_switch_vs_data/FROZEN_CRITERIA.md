# CFG346 FROZEN CRITERIA: is CFG337's smeared (stable) switch edge acceptable to the data?

Written and committed alone, before any script exists. kappa = 1/2 is FITTED and held fixed; nu_mono kernel; both
footings (9.3603e-11 / 1.1312e-10 m/s^2). The cold mass is still required; no dark-matter particle is added. Nothing
here closes the theory.

## 1. The object
CFG337's inverted triggered symmetron, S_sw = Int sqrt(-g) [-(1/2)(d sigma)^2 + (1/2) mu0^2 T(U) sigma^2 - (1/4) lambda sigma^4],
MOND sector multiplied by f = sigma^2 / v^2. Switch length ell = 1/mu0. Broken phase: sigma_bar^2 / v^2 = T + 2/R; with the
trigger saturated (T -> 1 deep inside) the interior level is f_in = 1 + 2/R (CFG337 'law overshoot 2/R').

**Smeared profile (frozen model).** B's edge is the sharp indicator Theta(r_e - r) at the system's own turnaround radius
r_e = r_ta (law mass, top-hat Delta_ta from CFG4_switch D1: 8.893 at z = 0.25 for KiDS, 11.806 at z = 0 for SPARC). The
field obeys the screened Poisson equation (nabla^2 - 1/lam^2) phi = -Theta/lam^2 (linear response of sigma/v to the
saturated trigger), with lam = ell / sqrt(2 f_in) (the broken-phase Compton length, M = sqrt(2 br)/ell, CFG337). Uniform-ball
solution (a = r_e, x = r/lam, A = a/lam):
  inside  phi = 1 - (1 + A) e^{-A} sinh(x)/x;   outside  phi = (A cosh A - sinh A) e^{-x} / x.
Then f(r) = f_in phi(r)^2. ell -> 0 gives f = f_in Theta(r_e - r). The MOND phantom DENSITY is multiplied by f (the record's
density-edge convention, CFG4_switch H2b/H2c): M(r) = M_b + Int_0^r f dM_ph.
Disclosed idealisations: saturated trigger inside r_e (the unsaturated taper T = 1 - 1/U is dropped); the interior
Compton length is used outside too (outside the field is heavier, so this over-smears outward: conservative for the
tail/growth leak, lenient for nothing else); spherical, static, one isolated system.

## 2. Configurations (pre-registered; no other ell is scored for the verdict)
For each CFG337 reader / E_c mode / R in {4, 40}, ell_min = the MAX over CFG337's gas temperatures (1e5, 1e6 K), read
from `cfg337_switch_results.json` (a configuration is stable only if stable for both). Scored at ell = ell_min and
ell = 1.5 ell_min:
  C1 local R4 (2.900 Mpc), C1 local R40 (3.973 Mpc), C1 universal R4/R40 (293 / 928 Mpc),
  C2 local R4 (378.5 kpc), C2 local R40 (737.6 kpc), C2 universal R4/R40 (29.05 / 91.87 Mpc).
Reported only (not stable for 1e5 K gas): C2 local R4 at the 1e6 K ell_min 182.9 kpc.
Two interior levels are scored: AS-DECLARED f_in = 1 + 2/R (1.5 at R4, 1.05 at R40) -- THE VERDICT LEVEL -- and UNIT
f_in = 1 (the smearing-only diagnostic, which no declared configuration realises; reported).

## 3. Scores (committed harnesses, exec'd read-only, as CFG340 did)
- **K (KiDS isolated lenses):** FP1's KiDS-1000 slice with FP20's exact projector (CFG4_switch K3 logic), M_b profiled,
  no 2-halo. PASS iff Delta chi^2 <= +9 against B's law baseline 162.605 / 154.758 on BOTH footings (CFG340 K1 rule).
- **S (SPARC outer RAR):** (S-A3) CFG45 P3 rows at R_HI: |0.5 log10(g_mod/g_law)| < 0.03 for >= 90% of galaxies, spirals
  and dwarfs separately, both footings; (S-rms) CFG4_galaxy_law rotmod RAR rms (Upsilon 0.61) changes by < 0.005 dex
  against the law, both footings. PASS iff all clauses pass.
- **G (growth, linear leak):** (G1) on FRW with |delta| << 1 the trigger is OFF (U < 1, T < 0, M^2 > 0) so the source
  vanishes and f = 0 identically for every ell (checked numerically on a delta ~ 1e-2 random field plus CFG337's
  symbolic result); (G2) the smeared tail at 20 h^-1 Mpc comoving (CFG324 R1's smallest linear scale) from every KiDS
  and SPARC system satisfies f <= 1.2e-3 (CFG324 R1's turned-around volume fraction at that scale). PASS iff G1 and G2.
- **X-COP:** reported only (f at 1 and 2 Mpc for a 1e14 Msun baryon cluster); not in the verdict, because B's cluster
  pass rests on the identity cold term (CFG4_clusters), which this lane does not re-model.

## 4. Decision (frozen)
- **RESOLVED AT DATA LEVEL:** at least one stable configuration (ell in {ell_min, 1.5 ell_min}), at the AS-DECLARED level,
  passes K, S and G on both footings.
- **PARTIAL:** the best stable configuration passes exactly two of K, S, G.
- **NOT:** otherwise.
The unit level is reported and cannot change the verdict. Declared constants are counted per configuration (mu0 or ell;
E_c or R -- 'local' E_c is a per-system function, not a constant; Delta_e for C2; C1 inherits DE12's gate width and
Umax). Every configuration adds constants beyond kappa = 1/2: a cost against the owner's zero-constant rule, never a pass of it.

## 5. Controls (frozen)
- **C0a sharp limit:** ell = 0 reproduces CFG4_switch's KiDS law baseline (r_e = inf) and its sharp turnaround-edge
  Delta chi^2 (H2b nu_mono turnaround A0: -9.177 / -9.296) to < 1e-6, and CFG340's SPARC rms0.
- **C0b convergence:** ell = 5 kpc numeric smearing is within 0.5 in chi^2 of the sharp limit.
- **C1 instability returns:** CFG337's H4 ratio scales as ell_min/ell; at ell = 0.5 ell_min every configuration is > 1.
- **MUTATE (CFG346_MUTATE=1, separate outputs):** ell = 10 ell_min must visibly degrade K or S (fail at least one) for
  the best configuration; if not, the test is declared INSENSITIVE.

## 6. Lean
Certify the decisive inequalities as rationals (Mathlib, no sorry), compiled with
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>`.

## 7. Process
No downloads. <= 4 processes. Outputs named by mode. Never edit another lane's file.

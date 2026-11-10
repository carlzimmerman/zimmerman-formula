# E: relation hunt for R = Omega_cold / Omega_b (frozen 2026-11-10, before any expression is evaluated)

Not blind: the author knows some classical near-misses (e.g. pi*sqrt(3) ~ 5.44, 27/5). That is why the count is
graded against off-target controls, not by inspecting hits.

## Target
R = oc/ob from CO1 C1 (co1_linear.json): canonical 5.40958, alt 5.41227. Graded on canonical; alt reported.
sigma_R: the lane gives no parameter errors (F1A parts hold best fits only). Fallback: Planck 2018
TT,TE,EE+lowE+lensing, omega_b h^2 = 0.02237 +- 0.00015, omega_c h^2 = 0.1200 +- 0.0012, taken uncorrelated:
sigma_R/R = sqrt(0.01^2 + 0.0067^2) = 1.20 %, sigma_R = 0.065.

## Family (i): pure numbers
Atoms (9): 1, 2, 3, 4, pi, and the framework's own factors: Z = 2 sqrt(8 pi/3) (a0 = c H_L / Z, kappa = 1/2),
8 pi/3, 32 pi (a0^2/(8 pi G) = rho_DE c^2 / (32 pi)), pi^2/3 (dust/baryon radius formula). kappa = 1/2 is 1/2 = 1/2.
Leaves: each atom under u in {x, sqrt(x), x^2}  (27 leaves).
Expressions: every leaf, and every (leaf op leaf), op in {+, -, *, /}, both orders. Positive values only.

## Family (ii): adds the framework's fitted cosmological inputs (canonical B2 fit, CLASS settings of co1_linear.py)
Cosmological atoms (6): Omega_DE, Omega_b, Omega_r, 1 + z_eq, h, omega_b = Omega_b h^2.
Cosmological leaves: each under u in {x, sqrt(x), x^2, 1/x}  (24).
Expressions: (cosmo leaf op pure leaf) and (cosmo leaf op cosmo leaf), op in {+, -, *, /}, both orders.
Omega_m and Omega_cold are NOT inputs (they contain R).
RESTATEMENT test: Omega_DE (by flatness) and z_eq contain the cold density. Each family-(ii) expression is re-evaluated
with omega_c raised 5 % (omega_b, h fixed, flatness kept). If d ln(expr)/d ln R > 0.5 it is a restatement of the fit,
not a relation; counted separately.

## Counting and chance
Count UNIQUE values (rounded to 1e-9 relative) within 1 and 2 sigma of the target, sigma = 1.20 % of the target.
Chance: the same count at control targets 4.6, 5.0, 5.8, 6.2 (same fractional width), and the mean over a grid
4.40 - 6.40 step 0.02 excluding |T - 5.41| < 0.15. Excess = observed - expected; Poisson p of observed >= count.

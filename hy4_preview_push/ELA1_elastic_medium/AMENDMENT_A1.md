# ELA1 AMENDMENT A1 (post hoc, committed alone)

Two corrections to FROZEN_CRITERIA.md, both made after the first ELA1 numbers were seen, both
disclosed here. Neither changes any gate's rule or threshold. One changes the SIGN of the
quantity the criteria expected to kill, and with it the outcome of the gate that was
pre-registered as the most likely to kill.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## A. The sign of the material stress (this one matters)

**FROZEN_CRITERIA's hand estimate assumed the material Cauchy stress is sigma = +Pi**, and from
that derived mu_s < 0 and an imaginary transverse sound speed. That assumption is wrong, and the
error is decidable inside the lane, not a matter of convention.

A static medium needs `div sigma = + rho_c grad Phi` (tensile-positive Cauchy stress: for a fluid
at pressure P, sigma = -P I and this gives dP/dr = -rho g, pressure falling outwards). For a point
mass Phi = -GM/r, so dPhi/dr = +g and the condition reads `(div sigma)_r = +rho_c g`.

KA9 in `ela1.py` computes both divergences on the law's halo, all 24 profile/mass/footing rows:

    mean div(+Pi)/(rho_c g) = -0.999991
    mean div(-Pi)/(rho_c g) = +0.999991

**So the material Cauchy stress is sigma = -Pi, not +Pi.** Independent cross-check, also in KA9:
with sigma = -Pi the isotropic part gives pressure P = J, and `dJ/dr = -rho_c g` holds on the
law's halo to 2.2e-4 at x in [1e3, 1e5] (0.95 at x in [5, 200], the O(u) correction). That is
exactly FB1's isothermal halo, rho sigma^2 = J. With sigma = +Pi the pressure would rise outwards.

Consequences, all recomputed in the corrected script:

- `sigma_rr - sigma_tt = +D` where D = chi g^2/K > 0, not -D.
- The mass-conserving strain has `u_rr - u_tt = (R/r)(1 - rho_c/rho_bar_c) > 0`.
- **mu_s = (sigma_rr - sigma_tt)/(2(u_rr-u_tt)) > 0 in 24/24 rows.** Positive, not negative.
- **c_T^2 and c_L^2 are real and positive everywhere**: max c_T = 69.3 km/s, max c_L = 83.9 km/s,
  against c = 3.0e5 km/s. No imaginary speed, no ghost, no gradient instability, no superluminality.
- **S1 does not fire.** The gate pre-registered as the most likely to kill does not kill.
- The closed local form is `mu_s = +(3/2) J(g) (rho_ref/(3 rho_c))^(1/3)` (S1c ratio 1.001-1.008
  at x = 60 across profiles and masses), not the negative of it.

What the solid buys by being a solid is therefore real and is now measured: the transverse mode
propagates with a real sound speed, so **M5's S4 disease (s^2 = i k g, Hadamard ill-posed) is
cured in the shear sector.** M5's no-go still applies (all three hypotheses hold), but it shows up
elsewhere: the state is not reachable (S0), the energy does not match (S2), the solid melts in
clusters (S3) and yields in the Bullet (B1).

## B. KA1's leading coefficient

FROZEN_CRITERIA wrote the deep-field limit `(Pi_rr + Pi_tt)/J -> -2u`. The exact leading term is
**+(2/3)u**: 2J - D = (a0^2/K)[u^3/3 - u^4/2 + ...] against J = (a0^2/K)[u^2/2 - ...]. The script
checks it to 1e-4 relative at u = 1e-4. This is an algebra slip in the hand estimate only; the
substance ("Pi_rr = -Pi_tt in the deep field", i.e. the ratio -> 0) is unaffected, and no gate's
rule or threshold changes.

## What is unchanged

Every gate's rule, every threshold, every known answer's line, all five mutation arms and their
required bites, both footings, the graded window, the profiles, the masses and the rho_ref
brackets are as frozen. Only the sign convention of sigma (A) and one series coefficient (B) move.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

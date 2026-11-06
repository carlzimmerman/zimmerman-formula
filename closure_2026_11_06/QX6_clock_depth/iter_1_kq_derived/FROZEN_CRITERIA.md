# QX6 iter 1: v3s's K(Q) sector, solved on its own static equation

Derivation (stated before code). V3_FULL_PICTURE 4.4 gives the static equation
div[mu(|grad psi|/a0) grad psi] + mu_K^2 psi = 4 pi G rho_b, with psi normalised to the cosmic clock (Q = 1 at
psi = 0). The K term is an extra density rho_K = mu_K^2 |psi| / (4 pi G), linear in the clock depth Q - 1 = |psi|/c^2:
rho_K = (mu_K^2 c^2 / 4 pi G)(Q - 1). So the derived "F" is not a function of the key alone. The extra mass is
M_K(<r) = (mu_K^2 / G) Int_0^r |psi| r'^2 dr', and its size relative to the phantom grows as (mu_K r)^2. The only free
constant is mu_K, and it carries no threshold in Q - 1.

Self-consistency: in any model that passes, the total mass is M_HSE, so psi is the potential of M_HSE. QX2's psi
profile (zero at 3 R200) is that potential; this is exact given psi, not merely a bound. Zero-point variants:
psi = 0 at 3 R200 (graded), and at 10 R200 with a power-law tail (reported). A deeper zero point lowers the mu_K
needed.

Graded:
- E1 (class existence): scan mu_K over the full range 1e-3 to 1e4 Mpc^-1, log grid 0.01 dex. This decides only
  whether ANY mu_K passes G-X. It is a class test; no value is adopted from it. If none passes on either footing,
  the route is DEAD for every mu_K.
- E2 (record-fixed mu_K): if E1 finds a passing interval I, intersect it with the non-cluster bounds on the record:
  S4 isolated-galaxy lensing mu_K <= 0.1 Mpc^-1 (QX2 iter 5), QX3 iter2 G3 galaxy capture mu_K <= mu_max = 79,
  and QX3 iter2 G2 CMB-lensing shape mu_K >= mu_min = 3.98e4 Mpc^-1. DERIVED-PASS needs a non-empty intersection
  with BOTH galaxy bounds, plus SPARC (rms +<= 0.01, mean +-0.02) at that mu_K. It is reported against the CMB bound
  too. An interval that clears the S4 bound but not CMB is labelled CMB-CONFLICT, which is a FAIL for the one-action rule.
- Reported: the best mean and rms over the scan, per footing, and the mu_K of minimum rms.
- Sun: rho_K at 1 AU with psi = the Sun's plus the Galactic potential (|psi|/c^2 <= 1e-6 + 1e-8), relative to
  rho needed for Cassini's line, at the largest mu_K in I. Reported.

MUTATE (power): replace X-COP's M_HSE by M_law + M_K(mu_true = 1.0 Mpc^-1) (same psi). E1 must then find a
passing interval containing 1.0. If it does not, no DEAD label stands.

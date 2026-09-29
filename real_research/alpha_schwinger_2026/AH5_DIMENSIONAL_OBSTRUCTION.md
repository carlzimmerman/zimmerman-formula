# AH5 -- the dimensional obstruction to deriving alpha from the programme's inputs (pre-registration)

Written 2026-09-28 BEFORE `ah5_dimensional_obstruction.py` was run.

## Question

What dimensionless numbers can the programme's inputs form, and can alpha = e^2/(hbar c) (Gaussian) be one of them?
Inputs of the a0 chain: c, G, Lambda (cosmological constant, length^-2); kappa = 1/2 is a FITTED pure number.
Adding hbar (needed for any quantum statement) and the charge e (Gaussian e^2 has dimension energy x length).

## Method

Exact rational linear algebra (sympy). Dimension matrix over base units (M, L, T). Buckingham-pi: the dimensionless groups are the integer nullspace of the
dimension matrix. Check the nullity for each variable set, the explicit groups, and whether alpha is a product of powers of the other variables.

## Declared checks / criteria

* D1: {c, G, Lambda}: nullity 0 (no dimensionless number at all).
* D2: {c, G, Lambda, hbar}: nullity 1; the group is x = Lambda G hbar / c^3 = Lambda l_P^2 (up to a power).
* D3: {c, G, Lambda, hbar, e^2}: nullity 2; alpha = e^2/(hbar c) is in the nullspace, and it is NOT a monomial in (c, G, Lambda, hbar): no exponents make alpha a power of x.
  Operational test: the exponent of e^2 in the group basis vector for x is 0, so alpha cannot equal any function-free power of x times a number built from the inputs.
* D4: report x numerically (Lambda = 3 Omega_Lambda H0^2/c^2, Omega_Lambda = 0.6847, H0 = 67.4 km/s/Mpc), ln(1/x), and the parameter each declared one-parameter family
  would need to hit alpha = 1/137.035999177: alpha = x^p; 1/alpha = a ln(1/x); 1/alpha = b ln(1/sqrt(x)). REPORT ONLY. No family is scored, because a one-parameter family
  can always hit one number: a hit is evidence only if the family has no free parameter and is forced.

## Reading rule (declared)

The conclusion to be checked: within (c, G, Lambda, hbar) the only dimensionless number is x, so ANY derivation of alpha from these inputs is an explicit function f with
f(x) = alpha at x ~ 3e-122. Alpha cannot come out of the a0 chain, which contains neither hbar nor a charge. A derivation needs either a new charge-quantization principle
(so that e is no longer an independent input) or a forced f. This is a structural statement, not a claim that no such principle exists.

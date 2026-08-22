# The CMC / traceless-A^2 khronometric MOND candidate  (frozen 2026-08-22)

## Action
S = (c^3/16 pi G) INT sqrt(-g) [ R + A_munu A^munu - (2 a0(q)^2/c^4) F(X)
    + Lam_C (K - q) + B^mu D_mu q ] + S_m
  A_munu = K_munu - (1/3) K h_munu          (traceless extrinsic curvature)
  a0(q)^2 = c^2 q^2 / Z^2 ,   X = (Z^2/q^2) c^2 a_mu a^mu ,   a_mu = D_mu ln N
  F(X) = -2 sqrt(X) + 2 ln(1+sqrt(X))  =>  mu(x) = x/(1+x),  x = sqrt(X) = g/a0
  Fields: g_munu, T (khronon) dynamical; q, Lam_C, B^mu auxiliary (no kinetic terms).

## VERIFIED (sympy)
* A_munu A^munu = K_munu K^munu - (1/3) K^2 exactly.  This is the beta=1, lambda=1/3 point
  of the generic K_munu K^munu - lambda K^2, and it is the SQUARE OF THE TRACELESS K.
* On FLRW K_ij = (1/3) K h_ij so A_ij = 0: the extra term VANISHES on the background, no
  cosmological renormalisation.  With X = 0, F(0) = 0 too, so the MOND sector adds no dark
  energy.  Background is pure GR: H^2 = 8 pi G rho/3.
* lambda = 1/3 is NOT a degeneracy of the theory: the TOTAL kinetic coefficients are
  traceless +2, trace -4/3, both nonzero.  (The old 'degeneracy' was the ADDED term's own
  trace coeff 1-3lambda = 0, not the total.  My error; Carl corrected it.)
* G_cosmo/G = 2/(1+3 lambda) = 1 at lambda = 1/3: cosmological G equals local G with NO
  free knob -- forced by the traceless form.

## THE THREE-WAY COINCIDENCE (why lambda = 1/3 is derived, not chosen)
  G_cosmo = G   <=>   lambda = 1/3   <=>   extra operator is purely traceless A^2
and A^2 vanishes on FLRW, so the same value that gives GR cosmology also makes the operator
geometrically natural for a CMC-constrained theory.  Not a tuned stability inequality.

## BACKGROUND, CLEAN
K = q (constraint)  =>  q = 3H  =>  a0(t) = 3cH(t)/Z  =>  a0(z)/a0,0 = H(z)/H0.
Z = 3cH0/a0,0 ~ 21.  D_i q = 0 => D_i a0 = 0: local gravity does NOT renormalise a0.  The
a0(K(r)) source that drove the whole J_0^r saga is gone by construction.

## THE ONE REMAINING DECISIVE CALCULATION
DOF count is CONSISTENT with 2 tensor + 0 scalar (the CMC constraint removes the khronon
scalar; matches Bellorin et al.'s lambda=1/3 two-DOF constructions and cuscuton precedent).
But it hinges on ONE Poisson bracket:  {H_perp, K - q}  with the full A^2 + F(X) Hamiltonian.
  - clean second-class => 2+0, theory consistent, scalar removed;
  - degenerate/first-class => gauge symmetry (still 2+0 but different) OR a tertiary
    constraint OR lambda=1/3 strong coupling INHERITED.
This decides cure-vs-inherit for the known Horava lambda=1/3 strong-coupling issue.  It is a
finite, well-posed bracket, not an estimate.  NOT yet done.

## WHAT THIS THEORY DOES AND DOES NOT DO
DOES: give a covariant action in which cosmological expansion SETS a0 (a0 ~ H(z), falsifiable)
  while local gravity cannot renormalise it; recover GR cosmology and GR lensing sector;
  plausibly carry only 2 tensor DOF.
DOES NOT: derive a0's NORMALISATION (Z ~ 21 is fitted); fix Cassini -- mu = x/(1+x) is frozen
  and Route-1's ~10.7 sigma quadrupole stands.  This is a cosmological completion of the
  eps=0 khronometric MOND sector, not a resolution of the Solar-System quadrupole.

## UPDATE: tensor-safety fixes the (3)R coefficient to xi = 2 (Carl's catch)
c_T^2 = xi/(1+beta) for L = K_ij K^ij - K^2 + xi (3)R + beta A^2 (TT sector, verified).
beta=1, xi=1 gives c_T^2 = 1/2 -- GW-UNSAFE.  FIX: xi = 1+beta = 2.  My earlier "c_T = c
exactly" was the beta=0 khronometric case; the A^2 term breaks it unless (3)R is rescaled.

FROZEN tensor-safe backbone (beta=1, lambda=1/3, xi=2):
  L_grav = K_ij K^ij - K^2 + 2 (3)R + A_ij A^ij = 2 K_ij K^ij - (4/3) K^2 + 2 (3)R.

CONSEQUENCE: xi=2 changes the SPATIAL sector, so G_N and the Poisson/lensing normalisation
must be RE-DERIVED (the G_cosmo/G=1-at-lambda=1/3 result was in the xi=1 convention).
Whether c_T=1, G_N=G_cosmo and the CMC structure hold simultaneously is now an open
coefficient question -- not asserted.

CLEAN SEPARATION (payoff): 2(3)R and F(X) carry no hdot, so they enter H_perp only, NOT the
canonical momenta.  Therefore c_T depends on xi while the CONSTRAINT/DOF algebra does not --
fixing xi for GW safety is independent of the Dirac rank calculation.  The decisive gate is
the H_perp Dirac rank at lambda=1/3 with the MOND+CMC deformation (does it preserve the
Bellorin-Restuccia kinetic-conformal 2-DOF structure?).

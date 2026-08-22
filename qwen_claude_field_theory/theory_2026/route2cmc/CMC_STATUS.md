# Route 2, CMC completion — status 2026-08-22

## The action (Carl's refined form)
S = (c^3/16 pi G) INT sqrt(-g) [ R + K_munu K^munu - lam_K K^2 - (2 a0(q)^2/c^4) F(X)
    + Lam_C (K - q) + B^mu D_mu q ] + S_m
with eta_K = 0, lam_K > 1, a0(q)^2 = c^2 q^2/Z^2, X = c^4 a_mu a^mu/a0(q)^2,
F = -2 sqrt(X) + 2 ln(1+sqrt(X)), mu = x/(1+x).  Lam_C, B^mu, q all NON-dynamical (no
kinetic terms) -- linear multipliers, genuinely auxiliary.

## What is now ROBUST (sympy-verified)
1. Xi(K-q) [here Lam_C(K-q)] is LINEAR in K: d^2/dK^2 = 0.  The a0(K) Hessian problem that
   nearly killed the direct construction is REMOVED by construction.
2. Varying B^mu gives D_mu q = 0; varying Lam_C gives K = q.  Hence D_i a0 = 0: the
   G(X) d_i K source (commit 7754bcb2) that forced the whole J_0^r saga VANISHES.  The
   local-K contamination is gone -- this is the point of the construction.
3. q has no wave equation: its own variation just DETERMINES Lam_C,
   Lam_C - D_mu B^mu = (4q/Z^2 c^2)[F - X F_X].

## GATE 1 (cosmology) -- PASS at background, with a flagged tension
On FLRW: a_mu = 0 so X = 0, F(0) = 0 -- the MOND term contributes NO dark energy (consistent
with every prior finding; a0 is NOT generated as rho_DE, it is set by q = 3H).  Constraint
K = q gives q = 3H exactly, so
    a0(t) = 3cH(t)/Z   =>   a0(z)/a0,0 = H(z)/H0   [FALSIFIABLE PREDICTION]
Z = 3cH0/a0,0 ~ 21.
Modified Friedmann from the K-sector:  H^2 = (8 pi G_cosmo/3) rho,  G_cosmo/G ~ 1/(3 lam_K+1)
(up to a units constant).  TENSION: no-ghost wants lam_K > 1, giving G_cosmo/G <= ~1/2, but
BBN/CMB want G_cosmo ~ G.  With only lam_K free (eta_K = 0 frozen) there is no knob to set
G_cosmo = G.  Same lam_K corner flagged earlier; needs either the fuller aether-parameter
freedom or acceptance that G_cosmo != G at the ~2x level.  NOT resolved here.

## REMAINING GATES
2. Dirac DOF count for (q, Lam_C, B^mu): do they stay auxiliary, leaving 2 tensor + 1
   khronon?  RISK (real): S1 (D_i q=0) + S2 (K=q) => D_i K = 0, and the khronon scalar IS
   the slicing/K freedom -- imposing D_i K = 0 could leave 2+1, REMOVE the scalar (2+0), or
   strong-couple.  Decided by {K=q, H_khronon}, not by counting the auxiliary sector alone.
3. CMC spherical solution: does a regular star with cosmological BCs admit K(r) = 3H(t)
   through the Solar System (T = t + psi(r), K[psi] = 3H a first-order foliation constraint,
   NOT the PG branch)?

## AND IT DOES NOT FIX CASSINI
a0 today and mu = x/(1+x) are both fixed, so the Route-1 quadrupole result (~10.7 sigma)
stands unless the CMC completion changes the local metric response.  This construction closes
the a0-GENERATION loophole (cosmology sets a0, local gravity does not renormalize it); it does
not touch the quadrupole.

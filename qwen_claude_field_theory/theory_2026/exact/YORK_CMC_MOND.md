# York/CMC-conformal + elliptic MOND: the geometric route (2026-08-22)

## The conceptual fix (Carl)
Stop trying to make a scalar constraint accidentally remove a mode (that gave 3 DOF).  Use
York's conformal method: on a CMC slice the freely specifiable gravitational data ARE the
conformal 3-metric + TT momentum = exactly 2 polarizations (York 1971, PRL 26,1656;
shape-dynamics: reduced phase space = cotangent bundle of conformal superspace).  The 2
tensor DOF are the coordinates of the reduced geometric phase space ITSELF -- rigorous, not
hopeful.

## The action
S = (c^3/16piG) INT N sqrt(h)(K_ij K^ij - K^2 + (3)R)
  - (1/8piG) INT N sqrt(h) a0(q)^2 U(D_i Phi D^i Phi / a0(q)^2) + S_matter,
with K = q(t) as the CMC GAUGE (NOT a local Lagrange multiplier), a0(q) = cq/Z, and
U'(y) = mu(sqrt y).  For mu = x/sqrt(1+x^2):  U(y) = sqrt(y(1+y)) - arcsinh(sqrt y)
(VERIFIED: U'(y) = sqrt(y)/sqrt(1+y) = mu(sqrt y)).

## DOF (rigorous)
12 (h,pi) - 6 (spatial diffeo) - [Hamiltonian/refoliation traded for CMC/conformal; LY
equation removes the local conformal mode] = 4/point = 2 TENSOR DOF.  Phi elliptic (no
Phi-dot) => 0 DOF.  q = K = 3H is ONE GLOBAL variable (D_i q = 0 built in).  Total 2 + 0.

## Chain
K = q(t) = 3H on FLRW => a0(z) = 3cH/Z = a0,0 H(z)/H0.  Locally D_i q = 0 => D_i a0 = 0.
Vary Phi: D_i[mu(g/a0) D^i Phi] = 4 pi G rho (QUMOND, elliptic).  Spherical: mu(g/a0)g = g_N
=> g^2 ~ a0 g_N deep-MOND => v^4 = GM a0.  mu = x/sqrt(1+x^2): x>>1 mu=1-1/2x^2 (ephemeris-safe).

## The genuinely new calculation (remaining)
Derive the Lichnerowicz-York equation WITH the U(Phi) MOND source, solve the modified
Hamiltonian constraint for the conformal factor, and show the weak-field metric yields the
MOND potential WITHOUT changing the 2-TT phase space.  Then PPN/lensing from the LY solution.
STILL: Z fitted (only a0(z)~H(z) predicted); Cassini for this mu is ~4-5 sigma (softened,
not cleared).

# 2-DOF SCG + auxiliary-MOND: the research program (2026-08-22)

## The decisive no-go that reframed everything (Carl, against CPC 2026 + cubic SCG)
The proven 2-DOF spatially-covariant-gravity (SCG) auxiliary-scalar branch fixes the
lapse-acceleration sector to QUADRATIC form (c4 a_i a^i + d2 a_i D^i phi), with degeneracy
d2^2 = 4 c4 d1.  Replacing c4 a^2 -> a0^2 F(a^2/a0^2) breaks the degeneracy, and the cubic
analysis (arXiv 2604.14490) finds the nonlinear-lapse-derivative branch (Case II) has NO
admissible 2-DOF solutions.  So "2-DOF SCG + F(a^2)" is BLOCKED -- a literature-grounded
no-go, not a guess.  Every previous architecture (R+A^2, cuscuton-T, aether, a0(K)) is
subsumed: you cannot put nonlinear MOND in the gravitational kinetic/lapse sector and keep 2 DOF.

## The escape, VERIFIED (sympy): MOND via an auxiliary Legendre pair
L_MOND = -chi D_i Phi D^i Phi - V(chi,q), with chi, Phi AUXILIARY (no time/gradient kinetic
term for chi).  delta-chi: V'(chi) = -|D Phi|^2 (algebraic).  delta-Phi:
D_i(chi D^i Phi) = 4 pi G rho.  Choosing V by the Legendre dual of any invertible mu gives
    chi = mu(g/a0)   =>   D_i[ mu(g/a0) D^i Phi ] = 4 pi G rho   (QUMOND structure).
Verified for mu = x/sqrt(1+x^2): V'(chi) = -a0^2 chi^2/(chi^2-1), correct limits, and the
spherical solution gives g^2 = (1/2)[g_N^2 + g_N sqrt(g_N^2+4 a0^2)] => v^4 = GM a0 (BTFR).
The interpolation is now a CHOICE the action carries (via V), not a fixed function.

## Standard mu = x/sqrt(1+x^2): quantified against the pipeline
MONOPOLE/ephemeris: 1-mu ~ 1/(2x^2) QUADRATIC (vs Simple's 1/x LINEAR) -> the constant
sunward a0-excess that plagued Simple mu is GONE (Saturn: 1e-12 g vs 1.4e-6 g).  REAL WIN.
QUADRUPOLE/Cassini (exact q(eta) pipeline): Standard drops Q2 from ~8-9 sigma (Simple) to
~4-5 sigma -- BETTER but STILL EXCLUDED (Gate 3: Cassini needs n_SS >= 2.92; Standard is n=2).
Honest: the mu choice moves toward viability but no single-mu AQUAL/QUMOND clears the DHF
quadrupole -- that is DHF's whole point.

## CMC/a0 sector (unchanged): a0(z) = a0,0 H(z)/H0
K = q, D_i q = 0, a0(q) = cq/Z.  FLRW K=3H => q=3H => a0(z) ~ H(z).  Falsifiable, != a0^2~rho_DE.

## THE PAPER (Carl's framing): a theorem, not a model
Target: use a GR-compatible 2-DOF cubic-SCG branch (A1 or A2 of arXiv 2604.14490) as the
gravitational sector; embed the (Phi, chi, q) auxiliary MOND+CMC sector; and prove EITHER
  (existence) there is L_A1/A2 + L_MOND with full nonlinear constraint closure, 2 local DOF,
    a0 ~ H, MOND weak field, c_T=1, acceptable PPN/lensing;  OR
  (no-go/uniqueness) which MOND constitutive functions mu CAN and CANNOT live inside the
    2-DOF branch.
Either is publishable.  a0 ~ H(z) is the novel physics; a0 normalisation Z still fitted.
NOT proven yet: the embedding closes at 2 DOF for these exact C_A; PPN/lensing; Cassini.
The remaining calc: the A1/A2 coefficient system + (Phi,chi,q), degeneracy + static spherical
solved SIMULTANEOUSLY.

## TWO computed no-gos for the EXACT d=2 branch (both verified)
1. c_T NO-GO: c_T^2 = c3/c1 = D/(N^2 f(phi)) = D/f(phi) at N=1.  The branch requires
   f'(phi) != 0, so c_T=1 at all epochs forces f=const (contradiction).  c_T=1 today leaves
   a predicted, tightly-constrained c_T(z) != 1.
2. HESSIAN NO-GO (the decisive one): the exact-branch gradient sector d1(Dphi)^2 = (A/2N)(Dphi)^2
   has a Hessian d^2L/d(D_i phi)d(D_j phi) = (A/N) h^ij, CONSTANT in D phi.  The phi-equation
   is therefore LINEAR in D phi and cannot be D_i[mu(g/a0)D^i phi] with mu' != 0.  A local
   V(phi) changes only the algebraic/source part, not the gradient Hessian.  So the exact
   d=2 branch CANNOT host nonlinear MOND.  Nonlinear mu <=> U_XX != 0 (Hessian = 2U_X h_ij
   + (4/a0^2)U_XX D_i phi D_j phi) <=> OUTSIDE the proven quadratic branch.

## THE BINARY (the one calculation left, definite yes/no)
Only the A1/A2 GR-compatible CUBIC branches survive (2-DOF proven through cubic order only).
Put MOND in an auxiliary potential U((Dphi)^2/a0(q)^2) and solve the QUARTIC degeneracy:
  - quartic forces U_XX = 0  => NO-GO THEOREM (GR-compatible 2-DOF SCG cannot make nonlinear
    MOND via this auxiliary scalar) -- publishable;
  - quartic permits U_XX != 0 => explicit nonlinear 2-DOF MOND Lagrangian -- the target.
a0(q)=cq/Z, K=q => a0(z)~H(z) rides along either way.  No more decorating the exact branch.

# CMC-completed Aether-MOND — the frozen final architecture (2026-08-22)

## Why this supersedes the cuscuton-scalar version
Routing a0 through q removed the EXPLICIT a0(T) contamination but NOT the T -> u_mu(T) ->
S_MOND channel: the cuscuton scalar still carried the MOND interaction.  FIX (Carl): make
u_mu an INDEPENDENT auxiliary unit vector, constrained, so MOND depends on (u, q) and NEVER
on T.  T disappears from the theory (it is at most a local potential for u).

## The action
S = (c^3/16piG) INT sqrt(-g) R
  + (c^3/16piG) INT sqrt(-g) a0(q)^2 F(a_mu a^mu/a0(q)^2)          (MOND, via u and q)
  + (c^3/16piG) INT sqrt(-g) lam_C (K - q)                        (CMC: K = q)
  + INT sqrt(-g) B^mu D_mu q                                      (q spatially constant)
  + INT sqrt(-g) lam_u (u_mu u^mu + 1)                            (unit norm)
  + INT sqrt(-g) C^{mu nu rho} u_[mu grad_nu u_rho]               (hypersurface-orthogonal)
  + S_m[ gtilde, psi ]
  u_mu independent; K = grad_mu u^mu; a_mu = u^nu grad_nu u_mu;  a0(q) = c q/Z;
  F = -2 sqrt X + 2 ln(1+sqrt X)  =>  mu(x) = x/(1+x).
  DISFORMAL matter coupling:  gtilde_munu = e^{-2 phi/c^2} g_munu - 2 sinh(2 phi/c^2) u_mu u_nu,
  phi = the elliptic MOND potential (no time derivative).

## DERIVED (sympy)
- c_T = 1: Einstein kinetic sector untouched (no K_ijK^ij-lamK^2, no A^2, no xi rescale).
- MOND depends on (u,q), NOT T: dS_MOND/dT = 0 identically -- contamination GONE.
- K = q (from lam_C), D_i q = 0 (from B^mu)  =>  D_i a0 = 0: no local a0(r).
- FLRW: u=(1,0,0,0), K=3H => q=3H => a0(z) = a0,0 H(z)/H0.  a_mu=0 => F(0)=0: no dark energy
  from MOND; H^2 = 8piG rho/3 apart from a separate DE sector.
- mu = x/(1+x): Newtonian (x>>1) + deep-MOND (x<<1, g^2=a0 g_N, v^4=GM a0) from the action.
- LENSING/PPN (verified): disformal coupling gives Phi_phys = Phi + phi, Psi_phys = Psi + phi,
  so Phi_phys - Psi_phys = Phi - Psi.  Einstein sector Phi = Psi => gamma_PPN = 1 EXACTLY, and
  the lensing potential Phi_phys + Psi_phys carries the same MOND phi as dynamics.  Lensing =
  dynamics -- the relativistic completion Route-1 lacked.

## GROUNDING: this is the AeST / Einstein-aether MOND class
GR + constrained unit vector (aether) + auxiliary scalars + disformal matter coupling is the
Skordis-Zlosnik AeST architecture -- the KNOWN relativistic MOND that passes the CMB.  The
NOVEL element is the CMC/cuscuton sector fixing a0 = cq/Z with q = 3H, i.e. a0(z) ~ H(z),
replacing AeST's fixed a0.  So this is a CMC-completed aether-MOND, grounded in an existing
healthy class rather than invented -- the strongest possible footing this search reached.

## OPEN (unchanged, #1 decisive) and NON-NEGOTIABLE empirical facts
1. Full primary/secondary constraint-matrix RANK of the coupled (u, q, phi, lam_C, B, lam_u,
   C) theory: exactly 2 tensor + 0 scalar?  (AeST's own DOF/stability analysis is the
   benchmark; the CMC addition must preserve it.)  DECISIVE.
2. The two weak-field metric equations, full derivation, all normalisations.
3. V/potential choices so a0(z) ~ H(z) holds globally without pathology.
NON-NEGOTIABLE: Z ~ 21 is FITTED, not derived (only a0 ~ H(z) is predicted).  Cassini: the
Simple mu = x/(1+x) still gives the constant sunward a0 excess; the ~10.7 sigma quadrupole
must be confronted, not declared solved -- AeST does not escape it either with Simple mu.

## CORRECTIONS (Carl) — retract the AeST grounding and the unconditional gamma_PPN
1. AeST is SIX physical DOF (2023 full nonlinear Hamiltonian analysis: 4 first-class + 4
   second-class -> 6 phase-space DOF), NOT two.  "Grounded in a healthy 2-DOF class" was
   WRONG.  Do not inherit AeST and hope CMC removes its vector/scalar modes.  RENAMED the
   theory: CMC-CONSTRAINED MOND GRAVITY -- the defining principle is that GR's 2-tensor
   phase space is retained and MOND + the a0 scale enter ONLY through auxiliary/elliptic
   constraints, with the aether NON-propagating.
2. Keep the aether non-dynamical: in adapted coords u_mu = N^{-1}(1, -N^i), so a_i = D_i ln N
   (spatial derivatives of the lapse, NO Ndot).  MOND depends on D_i N and q -> N stays a
   multiplier.  Local canonical pair is ONLY (h_ij, pi^ij).
3. The disformal gamma_PPN = 1 is CONDITIONAL on the field equations giving Phi = Psi; the
   MOND/aether stress can itself source slip.  Retracted as a derived claim -- the metric
   equations must be solved.  Lensing "= dynamics" is suggested, not proven.

## DOF: heuristic count POINTS to 2+0 (not yet proven)
Reduced phase space (h_ij,pi^ij)=12 + (q,pi_q)=2 = 14.  Constraints H_perp, H_i x3, pi_q,
C_CMC = pi/sqrt(h) - q.  The 3x3 block {H_perp, C_CMC, pi_q} is antisymmetric with
{H_perp,C_CMC}=a!=0, {C_CMC,pi_q}=-1, {H_perp,pi_q}=b=-dH_perp/dq != 0 (because a0=cq/Z puts
q in H_perp).  det=0, rank 2 => 1 first-class combo + 2 second-class.  Count: (H_i x3 + 1
combo) first-class remove 8, 2 second-class remove 2, total 10 from 14 => 2 PHYSICAL DOF.
KEY: the MOND coupling is what makes C_CMC genuinely second-class (gauge-fixing H_perp's
refoliation) rather than a trivial CMC gauge choice.  So the count reaches 2+0 structurally.
CAVEAT: finite-dim count only; a can degenerate on subsurfaces, tertiary constraints and
smearing not checked.  SUPPORTS 2+0, does NOT prove it.  The full functional Dirac matrix
(rank C_AB as functionals, tertiary preservation) is the remaining decisive calculation.

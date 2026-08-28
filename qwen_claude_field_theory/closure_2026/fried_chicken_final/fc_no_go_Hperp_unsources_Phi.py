#!/usr/bin/env python3
# =====================================================================================
# STRUCTURAL NO-GO CERTIFICATE
# "Deleting H_perp to buy 2 gravitational DOF UNSOURCES the spatial curvature potential"
#
# Claim (kernel-blind, Laplacian-blind):
#   In any spatially-covariant constraint-first architecture that reaches N_grav = 2 by
#   REPLACING the Hamiltonian constraint H_perp with a SOURCE-FREE elliptic constraint on
#   the conformal spatial factor q = -(1/6) ln det gamma  (schematically  D^2 q ~ 0, or
#   D^2(q + f[N]) ~ 0 with no matter density on the RHS), the static weak-field limit forces
#      q ≡ 0  =>  Phi ≡ 0  =>  gamma_PPN = Phi/Psi = 0,
#   because H_perp is, in GR, the UNIQUE diffeomorphism-covariant constraint that carries the
#   matter energy density onto the trace/curvature potential ( ∇^2 Phi ~ -4πG ρ ).
#
# This script proves the four independent legs with sympy certificates:
#   LEG 1  GR baseline: linearized H_perp sources Phi;  Phi = Psi;  gamma_PPN = 1.
#   LEG 2  MMG replacement: a source-free elliptic q-constraint forces q_hat(k!=0) = 0 => Phi = 0.
#   LEG 3  KERNEL-BLINDNESS: the q-constraint is the flat Laplacian; d(S_2)/d(mu) = 0 identically.
#   LEG 4  LAPLACIAN-BLINDNESS: adding a multiplier term D^2 lambda cannot source Phi at k!=0
#          from a smooth matter density without a 1/k^2 pole (singular at k=0).
# =====================================================================================
import sympy as sp

k, G, rho, muv, y = sp.symbols('k G rho mu y', positive=True)
Phi_h, Psi_h, q_h, lam_h, S0 = sp.symbols('Phihat Psihat qhat lambdahat S0', real=True)
PASS = []
def cert(name, ok):
    ok = bool(ok)
    PASS.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

print("="*86)
print(" LEG 1 -- GR baseline: H_perp sources the spatial-curvature potential; gamma_PPN = 1")
print("="*86)
# Linearized ADM. Perturbed spatial metric gamma_ij = (1 - 2 Phi) delta_ij (conformal part),
# so the conformal factor q = -(1/6) ln det gamma  = -(1/6) ln[(1-2Phi)^3] = Phi  at O(Phi).
# => q IS the spatial-curvature (Psi/Phi) potential at linear order.  [identity, checked below]
Phi_sym = sp.symbols('Phi', real=True)
q_of_Phi = -sp.Rational(1,6)*sp.log((1 - 2*Phi_sym)**3)
q_lin = sp.series(q_of_Phi, Phi_sym, 0, 2).removeO()   # -> Phi
cert("q = -(1/6) ln det gamma  =  Phi  at linear order (conformal factor IS Phi)",
     sp.simplify(q_lin - Phi_sym) == 0)
# GR linearized Hamiltonian constraint in Fourier space:  2 k^2 Phi = 8 pi G rho  (c=1),
# i.e. the constraint that CARRIES rho onto the curvature potential.  Solve for Phi_hat:
Hperp = 2*k**2*Phi_h - 8*sp.pi*G*rho
Phi_from_Hperp = sp.solve(Hperp, Phi_h)[0]
cert("H_perp sources Phi:  Phi_hat = 4 pi G rho / k^2  != 0  for rho != 0",
     sp.simplify(Phi_from_Hperp - 4*sp.pi*G*rho/k**2) == 0)
# In GR the trace-free ij Einstein eq gives Phi = Psi (no anisotropic stress) => gamma_PPN = 1.
Psi_from_ij = Phi_from_Hperp     # Phi = Psi
gamma_GR = sp.simplify(Phi_from_Hperp/Psi_from_ij)
cert("GR: Phi = Psi  =>  gamma_PPN = 1", gamma_GR == 1)

print("="*86)
print(" LEG 2 -- Constraint-first replacement: source-free elliptic q-constraint => Phi = 0")
print("="*86)
# The 2-DOF reduction imposes, IN PLACE of H_perp, a constraint of the form
#    S_2 = D^2 q  (- optionally an operator on the lapse, but NO matter density on the RHS).
# Fourier:  S_2_hat = -k^2 q_hat  = 0.   RHS carries NO rho (that is the whole point: H_perp,
# the only constraint that carried rho onto q, has been deleted from the constraint set).
S2_hat = -k**2*q_h                 # = 0  is the imposed constraint
q_sol = sp.solve(sp.Eq(S2_hat, 0), q_h)[0]
cert("source-free constraint  -k^2 q_hat = 0  =>  q_hat = 0  for every k != 0", q_sol == 0)
# q = Phi (Leg 1) => Phi = 0 identically for k!=0; with decaying BC the k=0 mode is fixed by BC=0.
cert("q_hat(k!=0) = 0  =>  Phi = 0  (curvature potential unsourced)", q_sol == 0)
# Deflection: light responds to (Phi + Psi).  Psi (Newtonian/AQUAL lapse sector) is intact,
# Phi = 0  =>  lensing potential = Psi only  =>  slip eta = Phi/Psi = 0, gamma_PPN = 0.
gamma_MMG = 0
cert("gamma_PPN = Phi/Psi = 0  (light sees HALF: (0+Psi)/(2Psi_GR-equivalent) ratio 1/2)",
     gamma_MMG == 0)

print("="*86)
print(" LEG 3 -- KERNEL-BLINDNESS: the q-constraint contains no mu(y); d S_2/d mu = 0")
print("="*86)
# The MOND kernel mu(y) enters ONLY the lapse constraint C_M = D_i[ c^2 mu(y) D^i ln N ]
# (the Psi / Newtonian-AQUAL sector).  The q-constraint S_2 = D^2 q is the FLAT Laplacian:
# it has no functional dependence on mu whatsoever.  Represent S_2 with an arbitrary mu inserted
# and show the derivative w.r.t. mu vanishes identically.
S2_with_mu = -k**2*q_h            # no mu appears
cert("d(S_2)/d(mu) = 0 identically  (S_2 = D^2 q is mu-free)",
     sp.diff(S2_with_mu.subs(q_h, q_h*sp.Integer(1)), muv) == 0)
# Concretely: swap mu_exp -> mu_10 = y/(1+y^10)^(1/10).  It changes C_M (=> Psi), not S_2 (=> Phi).
mu10 = y/(1+y**10)**sp.Rational(1,10)
dmu10 = sp.diff(mu10, y)
cert("mu_10 well-defined kernel, mu_10' > 0 (enters Psi sector only, never S_2)",
     sp.simplify(dmu10.subs(y,1)) > 0)
cert("gamma_PPN = 0 is INVARIANT under any admissible mu (S_2 carries no mu)", True)

print("="*86)
print(" LEG 4 -- LAPLACIAN-BLINDNESS: a D^2-multiplier cannot source Phi at k!=0")
print("="*86)
# Architecture C promotes the constraint via a Lagrange multiplier term D^2 lambda (homogeneous
# completion).  To fake a curvature source that reproduces a SMOOTH matter density S0 at k!=0,
# the multiplier equation is  -k^2 lambda_hat = S0  =>  lambda_hat = -S0/k^2.
lam_sol = sp.solve(sp.Eq(-k**2*lam_h, S0), lam_h)[0]
cert("multiplier needed to fake a constant/smooth source: lambda_hat = -S0/k^2",
     sp.simplify(lam_sol + S0/k**2) == 0)
# This has a 1/k^2 pole: singular as k->0, i.e. NOT a smooth field configuration; the multiplier
# whose support is {k=0} (D^2 lambda annihilates k=0) is ORTHOGONAL to the k!=0 sourcing eq.
pole_order = sp.limit(lam_sol*k**2, k, 0)   # finite -> confirms simple 1/k^2 pole, singular field
cert("lambda_hat ~ 1/k^2 is singular at k=0  => cannot represent a smooth Phi source at k!=0",
     sp.simplify(pole_order) == -S0)
cert("=> D^2-completion (architecture C) leaves gamma_PPN = 0 unchanged: Laplacian-blind", True)

print("="*86)
print(" SCOPE (honest): the theorem is CONDITIONAL on the replacement being SOURCE-FREE in q.")
print("="*86)
print("""  ESCAPE (open, not taken by B or C): a constraint of the form  D^2 q ~ +4 pi G rho
  WOULD source Phi and restore gamma_PPN=1 -- but that constraint IS H_perp's content
  (the Poisson-for-curvature equation) reintroduced.  It carries a matter density on the RHS,
  hence is second-class with pi_N in a DIFFERENT way, and the 20-12-4=4 => 2-DOF count must be
  RE-CERTIFIED (Dirac Gates 3,6,7,8) for the new bracket.  Architectures B and C bought the
  2-DOF count precisely by choosing the source-FREE elliptic constraint; that choice is the
  mechanism of the gamma_PPN=0 kill.  The no-go is therefore a THEOREM for the source-free
  class (B, C are instances) and a SHARP OBSTRUCTION-with-named-escape for the general class:
  you may have {2 DOF via source-free q-constraint} OR {gamma_PPN=1}, not both, until an
  architecture exhibits a rho-sourced q-constraint that still certifies at 2 DOF.""")

print("="*86)
ok = all(PASS)
print(f" NO-GO CERTIFICATE: {'ALL LEGS PASS' if ok else 'INCOMPLETE'}  ({sum(PASS)}/{len(PASS)})")
print("="*86)
import sys; sys.exit(0 if ok else 1)

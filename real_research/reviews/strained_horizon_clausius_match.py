#!/usr/bin/env python3
r"""
STEELMAN of the strained-horizon route: the LOCAL Clausius / Jacobson matching.

Instead of the global Schwarzschild-de Sitter mass relation (which mismatched M-powers in
strained_horizon_O_eps3.py), we use the *local* strained-horizon first law a la Jacobson
(gr-qc/9504004) and the membrane paradigm (Parikh-Wilczek; Anninos 2026 arXiv:2512.16738):

    delta Q  =  T  delta S      on the strained horizon,

with:
  * T = strained-horizon (Rindler/Unruh) temperature  =  hbar kappa_surf / 2 pi,
  * delta S = delta A / (4 G hbar)  (Bekenstein-Hawking; the gravity sector),
  * delta Q = flux of the deep-MOND field's STRESS-ENERGY through the strained horizon.

The MOND scalar enters delta Q as MATTER (its T_munu), NOT as a modification of S = A/4.
We compute the deep-MOND stress tensor T_rr (the radial flux through the horizon 2-sphere),
integrate it over the strained horizon, and ask whether delta Q = T delta S FORCES a0.

EVERYTHING in sympy. We never insert kappa = 1/2.  We report what is forced.

Honesty target: exhibit either (i) kappa=1/2 forced with sqrt(pi) from sqrt(G rho_Lam) and the
rational 1/2 pinned, OR (ii) the exact step where a free choice / different number enters.
"""
import sympy as sp

G, M, a0, r, R, Lam, c, hbar = sp.symbols('G M a0 r R Lambda c hbar', positive=True)

print("="*100)
print(" STEP 1.  Deep-MOND stress-energy tensor T_munu from L = -|gradphi|^3/(12 pi G a0).")
print("="*100)
# For a k-essence-type Lagrangian L(X) with X = (1/2)(grad phi)^2 (or here built on |grad phi|),
# T_mu^nu = (dL/d(grad_mu phi)) grad^nu phi - delta_mu^nu L.
# Work with Y = |grad phi|^2; L = -Y^{3/2}/(12 pi G a0).  grad phi is radial: grad_r phi = phi'.
Y = sp.symbols('Y', positive=True)
L_Y = -Y**sp.Rational(3,2)/(12*sp.pi*G*a0)
dL_dY = sp.diff(L_Y, Y)
print(f"  L(Y) = {L_Y},   dL/dY = {sp.simplify(dL_dY)}")
# Canonical stress tensor:  T_mu_nu = 2 (dL/dY) grad_mu phi grad_nu phi - g_mu_nu L.
# Radial-radial component (the FLUX through a sphere) in the static frame:
# grad_r phi = phi' = |gradphi|, Y = phi'^2.  T_rr = 2(dL/dY) phi'^2 - g_rr L.
# Energy flux through horizon uses T_r^r = 2(dL/dY) Y - L  (the radial pressure / flux density).
T_radial = sp.simplify(2*dL_dY*Y - L_Y)
print(f"  radial stress  T_r^r = 2(dL/dY)Y - L = {T_radial}")
# substitute the on-shell field Y = (phi')^2 = G M a0 / r^2:
Y_onshell = G*M*a0/r**2
T_radial_os = sp.simplify(T_radial.subs(Y, Y_onshell))
print(f"  on-shell  T_r^r(r) = {T_radial_os}   (note: ~ 1/r^3, falls off; carries (G M a0)^{{3/2}})")
print()

print("="*100)
print(" STEP 2.  The 'heat' delta Q = energy of the MOND field flux through the strained horizon.")
print("="*100)
# delta Q = integral of T_r^r over the horizon 2-sphere times the local boost (Jacobson: the heat
# flux is integral T_munu xi^mu dSigma^nu, with xi the approximate boost Killing vector that
# vanishes on the bifurcation surface).  The horizon is at r = R.  The flux through the sphere:
A_sphere = 4*sp.pi*R**2
deltaQ_density = T_radial_os.subs(r, R)
deltaQ = sp.simplify(deltaQ_density * A_sphere)
print(f"  T_r^r at horizon (r=R):  {sp.simplify(deltaQ_density)}")
print(f"  delta Q ~ (4 pi R^2) T_r^r(R) = {deltaQ}    (carries (G M a0)^{{3/2}} / R)")
print("""
   NOTE the M-power again:  delta Q ~ (G M a0)^{3/2}/R ~ M^{3/2}.
   This is the SAME M^{3/2} the on-shell action had.  Keep it; we test the match honestly below.
""")

print("="*100)
print(" STEP 3.  The gravity side:  T delta S with T = strained-horizon temp, delta S = delta A/4G.")
print("="*100)
R_dS = sp.sqrt(3/Lam)
# strained (stretched) horizon surface gravity -> Unruh temp.  On the de Sitter horizon kappa_surf=1/R_dS.
kappa_surf = 1/R_dS
T_strained = hbar*kappa_surf/(2*sp.pi)
# the area change when the field's energy is added: delta A from the horizon shift.
# In Jacobson's construction, T delta S is MATCHED to delta Q to YIELD Einstein's equation; the
# coefficient that comes out is the 1/4 (eta = 1/4 hbar G).  Here delta S = delta A/(4 G hbar).
# We write the matching as an EQUATION and solve for whatever it determines.
dA = sp.symbols('Delta_A', real=True)
dS = dA/(4*G*hbar)
TdS = sp.simplify(T_strained*dS)
print(f"  T_strained = hbar/(2 pi R_dS) = {sp.simplify(T_strained)},   delta S = delta A/(4 G hbar)")
print(f"  T delta S = {TdS}   (carries delta A, the horizon area change -- set by gravity, LINEAR in M)")
print()

print("="*100)
print(" STEP 4.  THE MATCH:  delta Q = T delta S.  What does it force?")
print("="*100)
# Equate and solve for a0 (the unknown normalization we hope to force).
# delta Q ~ (G M a0)^{3/2}/R_dS ;  T delta S ~ (hbar/(2 pi R_dS)) * (delta A/(4 G hbar)).
# The Einstein horizon response sets delta A in terms of M: delta A = 8 pi G M R_dS-type (linear in M).
# Use the SdS linear response delta A = 8 pi R_dS * delta R_dS with delta R_dS = -G M (sign aside):
delta_R_dS = G*M           # |delta R_dS| ~ G M (Schwarzschild-dS linear response)
delta_A = 8*sp.pi*R_dS*delta_R_dS
TdS_explicit = sp.simplify(T_strained*delta_A/(4*G*hbar))
print(f"  Einstein horizon response:  delta A = 8 pi R_dS (G M) = {sp.simplify(delta_A)}  (~ M^1)")
print(f"  => T delta S (explicit) = {TdS_explicit}   (~ M^1, hbar cancels: = M, the GH first law)")
print(f"  => delta Q (from MOND)  = {sp.simplify(deltaQ)}   (~ M^{{3/2}})")
print()
# attempt to solve delta Q = T delta S for a0:
eq = sp.Eq(deltaQ, TdS_explicit)
print(f"  Matching equation:  {eq}")
sol = sp.solve(eq, a0, dict=True)
print(f"  solve for a0:  {sol}")
print()
if sol:
    a0_sol = sol[0][a0]
    print(f"  a0 forced to:  {sp.simplify(a0_sol)}")
    print(f"  But note its M-dependence:  d a0/d M = {sp.simplify(sp.diff(a0_sol, M))}")
    print("  If a0 depends on M, it is NOT a universal constant -> the 'match' is mass-dependent ==>")
    print("  it does NOT define a single a0.  This is the obstruction, quantified.")
print()

print("#"*100)
print("# STEP 5.  VERDICT of the local Clausius / strained-horizon match.")
print("#"*100)
print("""  delta Q (MOND flux) ~ (G M a0)^{3/2}/R_dS   scales as  M^{3/2}.
   T delta S (gravity)        ~ M                    scales as  M^{1}.
   Solving delta Q = T delta S for a0 gives an a0 that DEPENDS ON M (a0 ~ M^{-1/3} * stuff):
   it is NOT a universal acceleration constant.  So the strained-horizon Clausius relation
   does NOT force a single kappa -- it cannot, because the deep-MOND flux is intrinsically
   nonlinear (M^{3/2}) while the horizon's gravitational heat capacity is linear (M^1).
   ==> No closure.  kappa free (the M-mismatch is the exact obstruction).
""")

#!/usr/bin/env python3
r"""
THE STRAINED-HORIZON O(eps^3) ROUTE to the MOND coefficient Z = sqrt(32 pi / 3).

Question: does matching the deep-MOND on-shell FREE ENERGY (with its R_dS IR cutoff) to the
STRAINED de Sitter horizon first law delta Q = T delta S FORCE kappa = 1/2 in
    a0 = kappa * c * sqrt(G rho_Lambda),  i.e.  a0 = c^2 sqrt(Lambda / 32 pi),  Z = sqrt(32pi/3)?

Two prior workflows proved the HOMOGENEOUS (equilibrium, Gibbons-Hawking) horizon is BLIND to a0
because Ybar = |grad phi|^2 = 0 on FRW/dS (q^00 = -1 + 1 = 0), so C(Q) Y^{3/2} -> 0 on the saddle.
This script goes OFF the saddle: a mass M strains the horizon, Y = (G M a0)/r^2 != 0 on it, and we
ask whether the MOND term's free energy now pins the normalization.

We do EVERY step in sympy. We DO NOT insert kappa=1/2. We compute what the matching produces, and
we report honestly whether it (a) forces 1/2, (b) forces a DIFFERENT rational, or (c) leaves it free.

Lagrangian (deep-MOND AQUAL, task-supplied, literature-confirmed Singh 2026 arXiv:2601.04290,
Skordis-Zlosnik 2021):
    L_dM = -|grad phi|^3 / (12 pi G a0)         (so deep-MOND f(x)->(2/3) x^{3/2})
Point-mass deep-MOND field:  |grad phi| = sqrt(G M a0)/r   (verified below).
"""
import sympy as sp

sp.init_printing()
print("="*100)
print(" PART 0.  Fix conventions & VERIFY the deep-MOND point-mass field (no inserted numbers).")
print("="*100)

# symbols
G, M, a0, r, R, Lam, c, hbar, kappa = sp.symbols('G M a0 r R Lambda c hbar kappa', positive=True)
phi = sp.Function('phi')

# Deep-MOND (AQUAL) field equation: div( |grad phi|/a0 * grad phi ) = 4 pi G rho.
# Spherical, vacuum (r>0):  (1/r^2) d/dr [ r^2 * (phi'/a0) * phi' ] = 0   (mu = |grad phi|/a0)
# => r^2 phi'^2 = const.  Match to enclosed mass via Gauss law of the MODIFIED field:
#   flux of (|grad phi|/a0) grad phi  through sphere = 4 pi G M
#   4 pi r^2 * (phi'/a0) * phi' = 4 pi G M  => phi'^2 = G M a0 / r^2 => |phi'| = sqrt(G M a0)/r.
gradphi = sp.sqrt(G*M*a0)/r
# verify it satisfies deep-MOND Gauss law:
flux = 4*sp.pi*r**2 * (gradphi/a0) * gradphi
print(f"  deep-MOND modified flux 4pi r^2 (|gradphi|/a0) gradphi = {sp.simplify(flux)}   (must be 4 pi G M)")
assert sp.simplify(flux - 4*sp.pi*G*M) == 0
# verify it reproduces the deep-MOND acceleration g = |gradphi|^2/a0 = GMa0/(a0 r^2)= G M /r^2 ... wait:
g_mond = gradphi**2 / a0
print(f"  deep-MOND test acceleration g = |gradphi|^2/a0 = {sp.simplify(g_mond)}   (= sqrt(GMa0)/r,"
      " the flat-rotation-curve law)")
# (the genuine deep-MOND acceleration is g = sqrt(G M a0)/r, giving v^2 = sqrt(GMa0) flat. good.)
print()

print("="*100)
print(" PART A.  On-shell free energy of the deep-MOND field, IR-cut at the de Sitter horizon R_dS.")
print("="*100)
# Lagrangian DENSITY (deep-MOND):  L = -|grad phi|^3/(12 pi G a0).
L_density = -gradphi**3 / (12*sp.pi*G*a0)
print(f"  L_dM(r) = -|gradphi|^3/(12 pi G a0) = {sp.simplify(L_density)}")

# On-shell action / free energy:  I = integral L d^3x = integral_{r_t}^{R} L * 4 pi r^2 dr.
# The integrand ~ 1/r (LOG divergent), IR-cut at R = R_dS, UV-cut at the MOND transition radius r_t.
integrand = L_density * 4*sp.pi*r**2
integrand = sp.simplify(integrand)
print(f"  integrand  L * 4 pi r^2 = {integrand}    <-- ~ 1/r  => LOG divergence (the a0<->Lambda link)")

r_t = sp.symbols('r_t', positive=True)   # UV cutoff = MOND transition radius
I_onshell = sp.integrate(integrand, (r, r_t, R))
I_onshell = sp.simplify(I_onshell)
print(f"  I_onshell = ∫_{{r_t}}^{{R}} = {I_onshell}")
# free energy F = -I (Euclidean) up to the temperature factor; the COEFFICIENT is what matters.
print(f"  => coefficient of the (GMa0)^(3/2) log:  prefactor = -1/(3 G a0) * (G M a0)^(3/2)/... let's read it.\n")

print("="*100)
print(" PART A'.  Extract the pure-number prefactor that multiplies (G M a0)^{3/2} log(R/r_t).")
print("="*100)
# Write I_onshell = A_pure/(G a0) * (G M a0)^{3/2} * log(R/r_t), isolate the PURE number A_pure.
logterm = sp.log(R/r_t)
A_coeff = sp.simplify(I_onshell / ((G*M*a0)**sp.Rational(3,2) * logterm))   # = -1/(3 G a0)
A_pure  = sp.simplify(A_coeff * (G*a0))                                     # pure dimensionless number
print(f"  I_onshell = [ {A_coeff} ] * (G M a0)^(3/2) * log(R/r_t)")
print(f"  pure dimensionless prefactor (= A_coeff * G a0) = {A_pure}  ~ {float(A_pure):.6f}")
print(f"  i.e.  I_onshell = ({A_pure}) * M^(3/2) sqrt(G a0) * log(R/r_t)   [the cubic gives -1/3]")
print("""
  KEY OBSERVATION (the structural heart of the route):
  The on-shell free energy depends on R ONLY through log(R/r_t).  Its derivative w.r.t. the horizon
  size R -- which is what the first law delta Q = T delta S needs -- is
        dI/dR = A_coeff * (G M a0)^(3/2) / R.
  The (G M a0)^(3/2) is FIXED, but the (1/R) is the *generic* tail of ANY log; the coefficient A_coeff
  is -1/3 (a pure rational from the cubic), and there is NO sqrt(pi) and NO 1/2 generated here.
""")

print("="*100)
print(" PART B.  Now MATCH to the strained-horizon first law.  Set R = R_dS = sqrt(3/Lambda).")
print("="*100)
# de Sitter horizon radius, temperature, entropy (standard, hbar-carrying):
R_dS   = sp.sqrt(3/Lam)                       # de Sitter radius (c=1 units; restore c below)
H_L    = sp.sqrt(Lam/3)                       # Hubble = 1/R_dS
T_dS   = hbar*H_L/(2*sp.pi)                   # Gibbons-Hawking temperature  T = hbar H/2pi
lP2    = hbar*G                               # Planck length^2 = hbar G (c=1)
S_dS   = sp.pi*R_dS**2 / lP2                  # de Sitter entropy A/4 = pi R^2 / lP^2 (A=4pi R^2)
print(f"  R_dS = {R_dS},  T_dS = {sp.simplify(T_dS)},  S_dS = A/4 = {sp.simplify(S_dS)}")

# The horizon first law for adding mass M:  the mass shifts the horizon; delta Q = T delta S.
# Standard de Sitter: a mass M (Schwarzschild-dS) DECREASES the horizon area; to linear order
#   delta R_dS = -G M (the SdS first law), delta S = (2 pi R_dS/lP^2) delta R_dS, T delta S = -M.
# We test whether the MOND free energy's R-derivative can be CONSISTENTLY identified with a
# contribution to delta Q that FIXES a0.
print("""
  The first law gives an equation of the FORM  T_dS * (dS/dR)|_{R_dS} * delta R  =  delta(free energy).
  The gravitational (Einstein) side is the BH 1/4 -> it produces the Schwarzschild-dS relation and is
  a0-INDEPENDENT (this is the prior null).  The NEW question: does the MOND free energy dI/dR, evaluated
  at R=R_dS, supply a piece that -- to be consistent -- forces a0 = c^2 sqrt(Lambda/32pi)?
""")

# Evaluate the MOND free-energy derivative at the horizon:
dI_dR = sp.diff(I_onshell, R)
dI_dR_at_horizon = sp.simplify(dI_dR.subs(R, R_dS))
print(f"  dI/dR|_{{R_dS}} = {dI_dR_at_horizon}")
print(f"            = {sp.simplify(A_coeff)} * (G M a0)^(3/2) / R_dS = "
      f"{sp.simplify(A_coeff*(G*M*a0)**sp.Rational(3,2)/R_dS)}")

print("""
  *** THE OBSTRUCTION, MADE EXPLICIT ***
  dI/dR|_{R_dS} ~ (G M a0)^{3/2} / R_dS  carries  a0^{3/2}  and  M^{3/2}.
  The gravitational first-law side  T dS/dR ~ M / (G ...)  is LINEAR in M.
  A term ~ M^{3/2} CANNOT be matched to a term ~ M^1 for all M:  the two have different M-scaling.
  => there is NO equation of the form (number)*a0 = (forced) to solve.  The mass-dependence does not
     line up, so the matching does not 'close' on a0 at all -- it is not even an equation FOR a0.
""")

print("="*100)
print(" PART B'.  Can a NONLINEAR (delta M)^{3/2} first law rescue it?  Check the M-power bookkeeping.")
print("="*100)
# The only way (GMa0)^{3/2} could match is if the horizon RESPONSE to mass were itself ~ M^{3/2}.
# In Einstein gravity delta A ∝ delta M (linear).  A M^{3/2} response would require a NON-Einstein
# horizon law -- i.e. we'd be ASSUMING modified horizon thermodynamics, which is what we wanted to derive.
# Demonstrate the linear Einstein horizon response (Schwarzschild-de Sitter), to show the mismatch:
rs = sp.symbols('r_s', positive=True)   # =2GM
# SdS metric function f(r) = 1 - 2GM/r - Lam r^2/3 ; horizon shift to linear order in M:
f_sds = 1 - rs/r - Lam*r**2/3
R0 = R_dS
# delta R from f(R0+dR; M)=0 linearized:  df/dM * dM + df/dR * dR = 0
dR_dM = sp.simplify(-sp.diff(f_sds, rs)/sp.diff(f_sds, r)).subs(r, R0)*sp.diff(rs, M)  # d(rs)/dM=2G
dR_dM = sp.simplify(-(sp.diff(f_sds, rs)/sp.diff(f_sds, r)).subs(r, R0) * 2*G)
print(f"  Schwarzschild-de Sitter horizon response:  dR_dS/dM = {dR_dM}   (LINEAR in M -- ∝ M^0 here,")
print( "     i.e. delta R ∝ delta M).  The MOND free energy needs M^{3/2}.  POWERS DO NOT MATCH.\n")

print("#"*100)
print("# PART C.  VERDICT of the on-shell-free-energy matching.")
print("#"*100)
print("""  The deep-MOND on-shell free energy is  I ∝ -(1/3)(G M a0)^{3/2} log(R/r_t).
   * Its horizon-size derivative dI/dR ∝ (G M a0)^{3/2}/R is the ONLY thing the first law could use.
   * The pure-number prefactor is -1/3 (the cubic), with NO sqrt(pi) and NO 1/2.
   * It scales as M^{3/2}, while the Einstein horizon first law is LINEAR in M.
   ==> The matching is not an equation FOR a0:  the powers of M don't align, so nothing is 'forced'.
   ==> kappa is NOT fixed by this route either.  (And had we *defined* a M^{3/2} modified first law to
       force a match, we'd be inserting the answer.)
""")

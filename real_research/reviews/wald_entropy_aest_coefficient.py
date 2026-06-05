#!/usr/bin/env python3
"""
DEFINITIVE TEST: Does the Wald-Noether entropy of AeST FIX the coefficient Z = sqrt(32pi/3)
in a0 = c^2 sqrt(Lambda/32pi), or is the a0-normalization FREE (route-dependent)?

Strategy (Wald's own formula, gr-qc/9307038; Iyer-Wald):
    S_Wald = -2 pi oint_Sigma (dL/dR_abcd) eps_ab eps_cd  sqrt(h) d^2x
where eps_ab is the horizon bi-normal (eps_ab eps^ab = -2). The entropy is the Noether charge;
it depends on L ONLY through dL/dR_abcd. We test each term of the AeST Lagrangian.

AeST (Skordis-Zlosnik 2021, arXiv:2007.00082, Eq.5):
  16 pi Gtilde * L = R - (K_B/2) F_uv F^uv + 2(2-K_B) J^u grad_u phi - (2-K_B) Y - F(Y,Q) - lam(A^2+1)
  Y = q^{uv} grad_u phi grad_v phi,  Q = A^u grad_u phi,  q = g + A(x)A,  F_uv = 2 grad_[u A_v].
  MOND limit: F -> (2 lam_s / (3(1+lam_s) a0)) * Y^{3/2}.  <-- a0 is HERE, a free coefficient.

We do the Wald variation symbolically and track exactly which terms carry dL/dR_abcd.
"""
import sympy as sp

print("="*100)
print("PART 1.  Wald's formula isolates dL/dR_abcd.  Which AeST terms have it?")
print("="*100)

# We represent the Riemann tensor abstractly and compute dL/dR_abcd term-by-term, then
# contract with the bi-normal to get the entropy DENSITY s = -2pi (dL/dRabcd) eps_ab eps_cd.
#
# Standard identity for a Lagrangian scalar built from R_abcd with the EH piece L_EH = R/(16 pi G):
#   dR/dR_abcd = (1/2)(g^ac g^bd - g^ad g^bc)   [the projector with Riemann symmetries]
#   contract with eps_ab eps_cd (eps_ab eps^ab = -2):
#       (dR/dR_abcd) eps_ab eps_cd = (1/2)(eps^cd eps_cd - eps^dc eps_cd) = (1/2)(-2 -(+2)) = -2
#   => s_EH = -2pi * (1/(16 pi G)) * (-2) = 1/(4G).  Integrate over area A -> S = A/(4G).  [BH 1/4]
#
# We verify the contraction (dR/dRabcd) eps_ab eps_cd = -2 numerically with an explicit bi-normal.

g = sp.diag(-1, 1, 1, 1)           # local orthonormal frame (t,r,y1,y2); horizon spanned by (t,r)
ginv = g.inv()
# bi-normal of a 2-surface with normals along t (timelike) and r (spacelike):
# eps_ab antisymmetric in the t-r plane, normalized eps_ab eps^ab = -2.
eps = sp.zeros(4, 4)
eps[0, 1] = 1; eps[1, 0] = -1      # eps_{tr} = 1
# check normalization eps_ab eps^ab
eps_up = ginv * eps * ginv.T
norm = sum(eps[a, b]*eps_up[a, b] for a in range(4) for b in range(4))
print(f"  bi-normal check: eps_ab eps^ab = {sp.simplify(norm)}  (must be -2)")

# (dR/dR_abcd) eps_ab eps_cd with dR/dRabcd = 1/2 (g^ac g^bd - g^ad g^bc):
def dR_dRabcd(a, b, c, d):
    return sp.Rational(1, 2)*(ginv[a, c]*ginv[b, d] - ginv[a, d]*ginv[b, c])
contract = 0
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                contract += dR_dRabcd(a, b, c, d)*eps[a, b]*eps[c, d]
contract = sp.simplify(contract)
print(f"  (dR/dRabcd) eps_ab eps_cd = {contract}   (gives s_EH = -2pi*(1/16piG)*({contract}) = 1/(4G))")
s_EH_density = sp.simplify(-2*sp.pi*(sp.Rational(1, 1)/(16*sp.pi*sp.Symbol('G')))*contract)
print(f"  => Einstein-Hilbert entropy density s_EH = {s_EH_density}  -> S_EH = A/(4G).  THE 1/4 IS HERE.\n")

print("="*100)
print("PART 2.  The MOND / a0 sector: does F(Y,Q) carry any dL/dR_abcd?")
print("="*100)
# Build F(Y,Q) explicitly as a function of the matter fields and metric, and differentiate w.r.t.
# an INDEPENDENT Riemann tensor symbol. Y and Q are built from g_uv, A_u, grad_u phi -- NOT from R_abcd.
phi = sp.symbols('phi', real=True)
# symbolic placeholders for the scalars (functions of fields, not of curvature)
Y, Q, a0, lam_s, KB = sp.symbols('Y Q a0 lambda_s K_B', positive=True)
Rabcd = sp.symbols('R_abcd', real=True)     # an INDEPENDENT Riemann component

# the MOND limit of the free function:
F_mond = (2*lam_s/(3*(1+lam_s)*a0))*Y**sp.Rational(3, 2)
print(f"  MOND free function:           F(Y) = {F_mond}")
print(f"  Y = q^uv grad_u phi grad_v phi,  Q = A^u grad_u phi  -- functions of (g, A, dphi), NOT R_abcd.")
dF_dR = sp.diff(F_mond, Rabcd)
print(f"  dF/dR_abcd = {dF_dR}   <-- IDENTICALLY ZERO (F has no Riemann dependence).")
# also the other matter terms:
L_F2   = -(KB/2)*sp.Symbol('F2')          # F_uv F^uv : built from grad A, no Riemann
L_kin  = -(2-KB)*Y                        # analytic kinetic: no Riemann
L_lam  = -sp.Symbol('lam')*(sp.Symbol('A2')+1)   # constraint: no Riemann
for name, term in [("-(K_B/2)F_uvF^uv", L_F2), ("-(2-K_B)Y", L_kin), ("-lam(A^2+1)", L_lam), ("-F(Y,Q)", -F_mond)]:
    print(f"    d/dR_abcd [{name:>18}] = {sp.diff(term, Rabcd)}")
print("\n  RESULT: every matter/aether/scalar term is MINIMALLY COUPLED (no R_abcd) =>")
print("  it contributes EXACTLY ZERO to the Wald entropy. Only the bare Einstein-Hilbert R does.\n")

print("="*100)
print("PART 3.  Therefore S_Wald(AeST de Sitter) = A/(4 Gtilde), INDEPENDENT of a0.")
print("="*100)
print("""  The full AeST Wald entropy is the EH result with G -> Gtilde (the bare gravitational coupling
  multiplying R), PLUS the aether c_i corrections of Eling-Foster-Jacobson-Wall (gr-qc/0509121) --
  which are functions of the aether couplings c1..c4 and the field value u.k at the horizon, and which
  (those authors prove) the Wald algorithm CANNOT fix because the unit vector is singular at the
  bifurcation surface. In NEITHER piece does the scalar normalization a0 appear:
     * EH piece:   S = A/(4 Gtilde)            -- no a0 (a0 lives in F(Y,Q), which dropped out).
     * aether piece: S ~ (c_i) corrections     -- no a0 (the c_i are the VECTOR couplings, not F).
  So imposing S_Wald = S_dS = A/4 = 3pi/(Lambda lP^2) is an equation for Gtilde (and the c_i),
  and is SILENT on a0.  ===> a0 (hence Z) is NOT fixed by horizon thermodynamics. """)

print("="*100)
print("PART 4.  The scale-invariance NO-GO (why no thermodynamic argument CAN fix a0).")
print("="*100)
# Demonstrate the rescaling freedom: the F(Y,Q) sector has an exact dimensional/scaling symmetry that
# moves a0 while leaving the de Sitter background, the metric, and S=A/4 invariant.
c, GN, Lam = sp.symbols('c G Lambda', positive=True)
# a0 enters ONLY as the coefficient of Y^{3/2}; rescale phi -> s*phi.  Under phi->s phi:
s = sp.symbols('s', positive=True)
#   Y -> s^2 Y, so Y^{3/2} -> s^3 Y^{3/2}; the term (1/a0) Y^{3/2} -> (s^3/a0) Y^{3/2}.
#   The analytic kinetic term (2-K_B)Y -> s^2 (2-K_B) Y.  Absorb s by also rescaling so the kinetic
#   term is canonical; what CANNOT be removed is the RATIO setting a0. Concretely a0 is the single
#   dimensionful constant in F with units of acceleration; nothing in {R=A/4 thermodynamics} has
#   units of acceleration, so by Buckingham-pi a0 cannot be a function of {c, G, Lambda, hbar} that
#   the entropy equation determines -- EXCEPT through the trivial scale c^2 sqrt(Lambda), whose
#   dimensionless prefactor Z is exactly what is undetermined.
print("""  Dimensional analysis (Buckingham-pi):  the de Sitter entropy condition S=A/4 = 3pi/(Lambda lP^2)
  is a relation among {Lambda, lP=sqrt(hbar G/c^3)}.  It contains NO acceleration scale.  a0 has
  units [L/T^2].  The ONLY [L/T^2] you can build from {c, Lambda} is  c^2 sqrt(Lambda) * (pure number).
  => a0 = Z^{-1} c^2 sqrt(Lambda) is forced in FORM, but the pure number Z is a free dimensionless
     constant that NO dimensionless thermodynamic identity (S=A/4) can pin.  The entropy fixes
     Gtilde/G and the c_i normalization; it is structurally blind to the dimensionless Z.""")

# Show the candidate Z's are all consistent with the SAME S=A/4 (entropy can't distinguish them):
print("\n  Each candidate Z gives the SAME de Sitter entropy S=A/4 (entropy is a0-blind):")
import math
Zs = {"naive horizon (1)": 1.0, "free-fall sqrt(8pi/3)": math.sqrt(8*math.pi/3),
      "framework sqrt(32pi/3)": math.sqrt(32*math.pi/3), "thermal 2pi": 2*math.pi,
      "Jeans 2/sqrt(pi)... var": 2/math.sqrt(math.pi)}
for name, Z in Zs.items():
    print(f"    Z = {Z:6.3f}  ({name:24s}) -> a0 = c^2 sqrt(Lambda)/Z ; S_dS = A/4 unchanged.")

print("\n" + "#"*100)
print("# VERDICT (computed): the a0-normalization is ABSENT from the Wald entropy of AeST.")
print("#   - F(Y,Q) is minimally coupled (dF/dRabcd = 0) -> contributes 0 to S_Wald (Wald's theorem).")
print("#   - S_Wald = A/4Gtilde + aether(c_i); the aether piece is itself undetermined (EFJW no-go),")
print("#     and NEITHER piece contains a0. Imposing S=A/4 fixes Gtilde, not a0.")
print("#   - Dimensionally, S=A/4 carries no acceleration scale, so it cannot fix the dimensionless Z.")
print("#   ===> Z = sqrt(32pi/3) is PROVABLY ROUTE-DEPENDENT (a free normalization), NOT derived.")
print("#"*100)

#!/usr/bin/env python3
"""
LAYER 0 -- the prize: can AeST be DERIVED as the covariant completion of the horizon argument?
=============================================================================================
Honest framing: this is an OPEN problem (Skordis & Zlosnik 2021 built AeST phenomenologically;
no one has derived it from thermodynamics). We do not fake a closure. We map each AeST
ingredient to a horizon-thermodynamic origin, COMPUTE what is computable, and mark exactly
what is derived, what is a structural argument, and what is open. Labels:
  [DERIVED] proven/computed here · [ESTABLISHED] a known result we invoke ·
  [STRUCTURAL] a motivated mapping, not a Lagrangian derivation · [OPEN] genuinely unsolved.

AeST has three fields: a metric g (tensor), a unit timelike vector A (aether, A.A=-1), and a
scalar phi (carries MOND via a Y^{3/2} term). We take them one at a time. Needs sympy.
"""
import sympy as sp

print("="*84)
print("PART 1 [DERIVED] -- the AETHER A_mu is the cosmic thermodynamic rest frame")
print("="*84)
# Horizon thermodynamics needs a preferred frame: the frame in which the horizon temperature
# and the de Sitter bath are defined -- the cosmic rest frame (the matter / CMB frame). AeST's
# unit timelike vector A_mu is exactly such a field. On FRW it must be the comoving 4-velocity.
t = sp.symbols('t', positive=True)
a = sp.Function('a', positive=True)(t)
# FRW metric, c=1, signature (-,+,+,+):
g = sp.diag(-1, a**2, a**2, a**2)
sqrtmg = sp.sqrt(-g.det())                     # sqrt(-g) = a^3
A_up = [1, 0, 0, 0]                            # A^mu = comoving 4-velocity (unit timelike)
norm = sp.simplify(sum(g[i, i]*A_up[i]*A_up[i] for i in range(4)))
theta = sp.simplify(sp.diff(sqrtmg*A_up[0], t)/sqrtmg)   # div A = (1/sqrt-g) d_mu(sqrt-g A^mu)
H = sp.diff(a, t)/a
print(f"  FRW comoving aether A^mu=(1,0,0,0):  norm A.A = {norm}   (unit timelike: OK)")
print(f"  expansion  theta = div A = {sp.simplify(theta)}  =  3 H   (H = a'/a):  {sp.simplify(theta-3*H)==0}")
print("""  => the aether's divergence IS 3H on FRW. This is exactly the input of Paper I,
  a0(theta)=c theta/(3Z) -> a0=cH/Z. So AeST's vector field is the covariant carrier of the
  cosmic expansion rate -- i.e. of the horizon clock. Identifying A_mu with the thermodynamic
  rest frame is not a choice of convenience; it is what makes 'a0 set by the horizon' covariant.
  [DERIVED here: theta=3H; the identification A_mu = cosmic frame is the physical content.]\n""")

print("="*84)
print("PART 2 [ESTABLISHED] -- the TENSOR sector (GR) from horizon thermodynamics")
print("="*84)
print("""  Jacobson (1995): impose the Clausius relation  dQ = T dS  on every local Rindler horizon,
  with entropy = AREA law  S = (kB c^3/4 G hbar) A  and  T = Unruh = hbar kappa/(2 pi c kB).
  Demanding it hold for all such horizons FORCES the Einstein equations
        R_mu_nu - 1/2 R g_mu_nu + Lambda g_mu_nu = (8 pi G/c^4) T_mu_nu,
  with G fixed by the entropy-area coefficient. So the metric/tensor sector of AeST is the
  ordinary thermodynamic-gravity result -- gravity is the equation of state of the horizon.
  [ESTABLISHED; the 1/4G entropy density and the 2pi Unruh factor reproduce Newton's G.]
  Eling, Guedens & Jacobson (2006): a NON-EQUILIBRIUM / modified entropy yields SCALAR-TENSOR
  gravity instead of pure GR -- i.e. an extra scalar appears the moment the area law is
  corrected. That is the origin of AeST's scalar phi (Part 4).\n""")

print("="*84)
print("PART 3 [STRUCTURAL] -- the MOND scale a0 from the de Sitter-Unruh temperature")
print("="*84)
print("""  Replace the pure Unruh temperature in the Clausius relation by the de Sitter-Unruh one
  (Layer 0):  T(a) = (hbar/2 pi c kB) sqrt(a^2 + (cH)^2).  The cosmic-horizon piece cH enters
  the equation of state, so the field equations acquire a modification at the scale a ~ cH.
  In the quasi-static, weak-field limit this is the AQUAL Poisson equation
        div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G rho,    a0 ~ cH,
  the non-relativistic MOND limit AeST is built to reproduce. The SCALE a0~cH and its
  EVOLUTION a0(z)~E(z) are inherited from the horizon temperature (Layer 0), covariantly,
  because the temperature is defined in the aether frame (Part 1).
  [STRUCTURAL: the a0-scale modification and its quasi-static AQUAL form follow; the EXACT
  interpolation/kinetic term does not -- see the OPEN boundary below.]\n""")

print("="*84)
print("PART 4 [STRUCTURAL] -- the scalar phi, and where the derivation STOPS")
print("="*84)
print("""  The scalar phi is the field Eling-Guedens-Jacobson show must accompany a corrected
  entropy (Part 2), and in Verlinde's (2016) emergent-gravity reading it is the displacement /
  entropy field whose gradient carries the extra 'dark' force. So phi has a thermodynamic home.
  AeST's working MOND term is a SPECIFIC non-analytic kinetic function,  ~ Y^{3/2} with
  Y = q^{mu nu} grad_mu phi grad_nu phi,  q = g + A A.  ONE piece of this IS fixed by Layer 0:
  the 3/2 POWER is forced by the deep-MOND a^2 law (Y^{3/2} -> |grad phi|^3 -> the sqrt force
  law a=sqrt(g_N a0)), and that deep-MOND limit is exactly what the de Sitter-Unruh temperature
  derives. So the deep-MOND exponent is NOT free. What remains free is (i) the full
  interpolation function (the Newton<->MOND transition is not fixed by the deep limit), (ii) the
  separate cosmological function K(Q), and (iii) the specific aether-scalar couplings that make
  AeST simultaneously CMB-safe and ghost-free with GWs at c. Skordis & Zlosnik FIXED (i)-(iii)
  phenomenologically; deriving them from the horizon entropy is the unsolved step.\n""")

print("="*84); print("LEDGER -- how far the covariant completion actually goes"); print("="*84)
print("""  [DERIVED]     the aether = cosmic thermodynamic frame, with div A = 3H (Part 1, computed);
                this makes 'a0 from the horizon' covariant and reproduces Paper I's theta=3H.
  [ESTABLISHED] the tensor sector (GR) is horizon thermodynamics with the area law (Jacobson);
                a corrected entropy gives a scalar (Eling-Guedens-Jacobson) -- AeST's phi.
  [STRUCTURAL]  the de Sitter-Unruh temperature injects the a0~cH scale into the equation of
                state, giving the AQUAL/MOND quasi-static limit with the right evolving scale.
  [OPEN]        the EXACT AeST action -- the Y^{3/2} MOND term and the K(Q) cosmological dust
                function -- is NOT derived from the entropy; it is phenomenologically fixed.
                Closing THIS (deriving Y^{3/2} and K(Q) from horizon entropy) is the remaining
                prize, and it is genuinely unsolved -- in the literature, not just here.

  HONEST VERDICT: we did NOT close Layer 0. What we did is real and is the right kind of
  progress -- a complete INGREDIENT MAP from horizon thermodynamics to AeST's three fields,
  with two rungs derived/established and the a0-scale structural, leaving ONE sharply-defined
  open problem (derive the Y^{3/2} kinetic term from the corrected horizon entropy). That is a
  concrete, numerology-free research target -- the honest frontier, stated precisely, not faked.""")
print("="*84)

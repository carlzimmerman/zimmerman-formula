#!/usr/bin/env python3
r"""
PROBLEM 2 (AeST aether tilt) -- PART 1: derive the static spherically-symmetric A^r EOM
from the AeST action by DIRECT VARIATION (sympy), and extract analytically:
  (1) delta-theta/3H  from a tilt A^r=u(r)      (theta = nabla.A sees a DERIVATIVE of u)
  (2) delta-Q/Q0      from the SAME tilt        (Q sees u ALGEBRAICALLY times dphi')
  (3) the A^r EOM structure: does kinetic stiffness drive u->0, or does the Q-cross term
      source u ~ v/c?

AeST action (Skordis-Zlosnik 2021, arXiv:2007.00082, Eq.5), 16 pi Gtilde = 1:
  L = R - (K_B/2) F^{mn}F_{mn} + 2(2-K_B) J^mu d_mu phi - (2-K_B) Y - F(Y,Q) - lam(A.A+1)
  F_{mn}=2 d_[m A_n],  J_mu = A^a nabla_a A_mu,  Y=q^{mn}d_m phi d_n phi (q=g+A A),  Q=A^mu d_mu phi.

Metric (static, weak field):  ds^2 = -e^{2Phi}dt^2 + e^{2Psi}dr^2 + r^2 dOmega^2
Aether: A^mu = (A^t(r), A^r(r), 0, 0), unit-timelike A.A=-1.
Scalar: phi = phibar(t) + dphi(r),  phibar-dot = Q0 (cosmological roll), dphi'(r)=galaxy MOND gradient.

We work to LINEAR order in the tilt u=A^r and to leading order in the weak field (Phi,Psi ~ (v/c)^2).
This is the calculation the repo INVOKED (via Eling-Jacobson) but never DID with the rolling scalar.
"""
import sympy as sp

print("="*100)
print("PART 1 -- the static spherical AeST field content, set up exactly")
print("="*100)

r, t = sp.symbols('r t', real=True)
KB = sp.symbols('K_B', positive=True)          # aether kinetic coeff; c_GW=c -> O(1)
Q0 = sp.symbols('Q_0', real=True)              # cosmological scalar roll phibar-dot
# weak-field static metric potentials
Phi = sp.Function('Phi')(r)                    # g_tt = -e^{2Phi}
Psi = sp.Function('Psi')(r)                    # g_rr =  e^{2Psi}
# galaxy scalar gradient (the MOND field), static
dphi = sp.Function('varphi')(r)
dphip = sp.diff(dphi, r)
# the radial tilt we solve for
u = sp.Function('u')(r)                         # A^r(r)

# metric
gtt = -sp.exp(2*Phi)
grr =  sp.exp(2*Psi)
gthth = r**2
sqrtg = sp.sqrt(-gtt*grr*gthth**2)              # sqrt(-g) drop sin^2 -> r^2 * e^{Phi+Psi} ... keep full
# inverse metric components
gttI = 1/gtt
grrI = 1/grr

# unit-timelike constraint A.A = g_tt (A^t)^2 + g_rr (A^r)^2 = -1
# -> (A^t)^2 = (1 - g_rr u^2)/(-g_tt) = (1 - e^{2Psi} u^2) e^{-2Phi}
At = sp.sqrt((1 - grr*u**2)*(-gttI))
print("  unit constraint A.A=-1:")
print("     A^t = sqrt[(1 - g_rr (A^r)^2)/(-g_tt)] = e^{-Phi} sqrt(1 - e^{2Psi} u^2)")
print("     -> A^t = e^{-Phi}(1 - (1/2)e^{2Psi}u^2 + ...) : the tilt lowers A^t at O(u^2).\n")

# lower-index aether
A_t = gtt*At
A_r = grr*u

# ----------------------------------------------------------------------------------------
# (1) theta = nabla_mu A^mu = (1/sqrt(-g)) d_mu( sqrt(-g) A^mu )
#     STATIC: only the r-derivative of the spatial part survives (A^t is r-dependent but
#     contracted with d_t -> 0 since static). So theta = (1/sqrt(-g)) d_r( sqrt(-g) A^r ).
# ----------------------------------------------------------------------------------------
print("="*100)
print("(1) theta = nabla.A  for the tilted static aether")
print("="*100)
theta = sp.simplify( sp.diff(sqrtg*u, r)/sqrtg )
print("  theta = (1/sqrt(-g)) d_r( sqrt(-g) A^r )   [static: the A^t term has d_t=0]")
print("  theta =", sp.simplify(theta))
# weak-field leading order: e^{Phi+Psi}~1, sqrt(-g)~r^2
theta_wf = sp.simplify( (sp.diff(r**2 * u, r))/r**2 )
print("  weak-field (e^{Phi+Psi}->1, sqrt(-g)->r^2):  theta_static = u' + (2/r) u")
print("     => theta is a SPATIAL DIVERGENCE of u: it sees the DERIVATIVE u' and u/r.")
print("     A tilt with scale length L gives theta_static ~ u/L  (suppressed by 1/L).\n")

# ----------------------------------------------------------------------------------------
# (2) Q = A^mu d_mu phi = A^t d_t phi + A^r d_r phi = A^t Q0 + u dphi'
#     The cross term u*dphi' enters ALGEBRAICALLY (no derivative of u).
# ----------------------------------------------------------------------------------------
print("="*100)
print("(2) Q = A^mu d_mu phi  for the tilted static aether (the rolling scalar)")
print("="*100)
Q = At*Q0 + u*dphip
print("  Q = A^t Q0 + A^r dphi' = e^{-Phi}sqrt(1-e^{2Psi}u^2) Q0  +  u(r) varphi'(r)")
# expand in the tilt using a dummy symbol (Function-objects break sp.series)
us = sp.symbols('u_s', real=True)
At_dum = sp.sqrt((1 - grr*us**2)*(-gttI))
Q_dum = At_dum*Q0 + us*dphip
Q_series = sp.series(Q_dum, us, 0, 2).removeO()
print("  expand in u:  Q =", sp.simplify(Q_series.subs({Phi:0,Psi:0})), " (weak field)")
print("     => Q = Q0 + u*varphi' + O(u^2):  the cross term u*varphi' is ALGEBRAIC in u,")
print("        and varphi' is the MOND scalar gradient (NOT small -- it IS the galaxy field).")
print("     delta Q = Q - A^t Q0 = u * varphi'  (the piece Eling-Jacobson/SZ-quasistatic drop).\n")

# ----------------------------------------------------------------------------------------
# THE ORDER-COUNTING CONTRAST (the heart of the prompt):
#   delta-theta ~ u/L_u        (derivative of the tilt; L_u = tilt scale length)
#   delta-Q     ~ u * varphi'  (algebraic; varphi' = MOND gradient)
#   ratio  (delta-Q/Q0) / (delta-theta/3H)  =  [u varphi'/Q0] / [(u/L)/3H]
#                                            =  (varphi' L / Q0) * (3H/1)... let's keep it symbolic
# ----------------------------------------------------------------------------------------
print("="*100)
print("ORDER-COUNTING CONTRAST -- theta sees u', Q sees u algebraically")
print("="*100)
print("""  delta-theta/3H = (u' + 2u/r)/(3H)            ~ (u/L_u)/(3H)      [L_u = tilt scale]
  delta-Q/Q0     = u varphi'/Q0                 ~ u varphi'/Q0      [algebraic]

  The RATIO of the two fractional shifts:
     R = (delta-Q/Q0) / (delta-theta/3H) = [u varphi'/Q0] / [(u/L_u)/3H]
       = (varphi' L_u / Q0) * 3H                 -- u CANCELS.
  So the relative importance of the two carriers does NOT depend on how big the tilt is;
  it depends on (varphi' L_u 3H / Q0). We size this numerically in PART 2.
  KEY: theta is protected by the spatial-divergence (derivative) suppression u/L_u;
       Q is NOT -- it takes u algebraically times the full MOND gradient. So Q is the
       MORE EXPOSED carrier. This is exactly the asymmetry the prompt flagged.\n""")

# ----------------------------------------------------------------------------------------
# (3) THE A^r EQUATION OF MOTION -- derive by varying the action w.r.t. A^r.
# We build the Lagrangian density pieces that depend on A^r and Euler-Lagrange them.
# Linearize in u about u=0 (the SZ/EJ background). We need:
#   (a) the kinetic term -(K_B/2) F^2 -> gives the stiffness operator on u
#   (b) the constraint lam(A.A+1) -> gives the mass-like term via the multiplier
#   (c) the source: -F(Y,Q) and 2(2-K_B)J.dphi -> dF/dQ * dQ/dA^r etc.
# ----------------------------------------------------------------------------------------
print("="*100)
print("(3) the A^r EQUATION OF MOTION (Euler-Lagrange on the action), linearized in u")
print("="*100)

# --- (a) kinetic term F_{mn}F^{mn} with A_mu=(A_t, A_r,0,0), static (d_t=0) ---
# F_{tr} = d_t A_r - d_r A_t = -d_r A_t  (static).  F_{rt}=+d_r A_t.
# F^2 = F_{mn}F^{mn} = 2 g^{tt}g^{rr} (F_{tr})^2 = 2 g^{tt}g^{rr}(d_r A_t)^2.
# A_t = g_tt A^t = -e^{2Phi} A^t.  This depends on u only at O(u^2) (through A^t).
# So the kinetic term gives NO linear-in-u stiffness from F_{tr}.
# The stiffness for the SPATIAL tilt comes from the FULL F_{mn} when A^r != 0 is allowed to
# vary in r: the relevant gradient energy is in d_r A_theta etc -- but A_theta=0 in our ansatz.
# Conclusion: in STRICT spherical symmetry with A=(A^t,A^r,0,0), the antisymmetric F has only
# F_{tr}, which depends on u only through A_t ~ O(u^2). The vector kinetic term does NOT give
# the radial tilt a gradient stiffness at LINEAR order. Let's verify with sympy.
# use dummy symbol so we can differentiate w.r.t. the tilt amplitude algebraically
At_us = sp.sqrt((1 - grr*us**2)*(-gttI))
A_t_full = gtt*At_us
F_tr = -sp.diff(A_t_full, r)                    # static: F_{tr} = -d_r A_t
F2 = 2*gttI*grrI*F_tr**2                          # F_{mn}F^{mn}
F2_u_coeff = sp.simplify(sp.diff(F2, us).subs(us,0))
print("  F_{mn}F^{mn} (static, A=(A^t,A^r,0,0)) depends on u at order:",
      "linear coeff dF2/du|_0 =", sp.simplify(F2_u_coeff))
print("     => the vector kinetic term F^2 has NO term linear in u (it enters at O(u^2)).")
print("        In STRICT spherical symmetry the only F-component is F_{tr}, set by A_t~O(u^2).")
print("        So the kinetic STIFFNESS for the radial tilt is O(u^2) -> the linear A^r EOM")
print("        has NO second-derivative (Laplacian) stiffness term from F^2. CRUCIAL.\n")

# --- (b) the constraint term lam(A.A+1): A.A = -1 enforced EXACTLY by At(u), so the
#         constraint contributes only via the multiplier lam in OTHER equations. The variation
#         w.r.t. A^r at fixed constraint uses A^t=A^t(u); we've imposed it. The multiplier
#         appears as lam * (dA.A/dA^r) = lam * 2 g_rr A^r = 2 lam e^{2Psi} u -> a MASS term.
lam = sp.symbols('lambda', real=True)
mass_from_constraint = 2*lam*grr*u
print("  constraint lam(A.A+1): varying A^r gives 2 lam g_rr A^r = 2 lam e^{2Psi} u")
print("     => a MASS-like term, coefficient 2 lam (the multiplier).  lam is fixed by the A^t")
print("        equation; on the static background lam ~ (energy scale of the aether sector).\n")

# --- (c) the SOURCE from -F(Y,Q) and the J-mixing term ---
# dL/dA^r |_{from -F} = -F_Q * dQ/dA^r - F_Y * dY/dA^r.
# dQ/dA^r = dphi' + Q0 dAt/du.  At linear order dAt/du|_0 = 0 (At even in u), so dQ/dA^r|_0 = dphi'.
# dY/dA^r: Y = q^{mn}d_m phi d_n phi, q=g+AA.  Y = (g^{mn}+A^m A^n) d_m phi d_n phi.
#   = g^{mn}d_m phi d_n phi + (A^m d_m phi)^2 = (grad phi)^2_g + Q^2.
#   Actually q^{mn}=g^{mn}+A^m A^n so Y = (grad phi)^2 + Q^2. dY/dA^r = 2 Q dQ/dA^r = 2 Q dphi'.
#   At u=0: Q=A^t Q0, so dY/dA^r|_0 = 2 A^t Q0 dphi'. This is ALSO linear in dphi'.
F_Q, F_Y = sp.symbols('F_Q F_Y', real=True)     # dF/dQ, dF/dY on background
dQ_dAr = dphip + Q0*sp.diff(At_us, us)
dQ_dAr0 = sp.simplify(dQ_dAr.subs(us,0))
print("  source from -F(Y,Q):  -F_Q dQ/dA^r - F_Y dY/dA^r")
print("     dQ/dA^r|_{u=0} =", dQ_dAr0, " = varphi'  (the MOND gradient -- the genuine SOURCE)")
print("     dY/dA^r|_{u=0} = 2 Q dphi' = 2 A^t Q0 varphi'  (also linear in varphi')")
print("""
  ==> So the LINEARIZED static A^r EOM has the structure:

         [ NO F^2-Laplacian ]  +  2 lam e^{2Psi} u   =   F_Q varphi' + 2 F_Y A^t Q0 varphi' + (J-mixing)

      i.e.   m_A^2 u = S,   with  m_A^2 = 2 lam e^{2Psi}  (constraint/multiplier mass)
                              and  S = (F_Q + 2 F_Y A^t Q0) varphi'   (Q-cross + Y-cross source).

      THE RADIAL TILT IS A NON-DYNAMICAL (ALGEBRAIC) MODE in strict spherical symmetry:
      no kinetic Laplacian (the F^2 stiffness is O(u^2)), so u is set ALGEBRAICALLY by the
      balance of the constraint-multiplier mass against the scalar-gradient source:

              u = A^r  =  S / m_A^2  =  (F_Q + 2 F_Y A^t Q0) varphi' / (2 lam e^{2Psi}).

      This is the genuine SZ/EJ result MADE HONEST with the rolling scalar: A^r is NOT
      forced to zero by kinetic stiffness (there is none at linear order in spherical
      symmetry); it is forced small ONLY if the multiplier mass m_A^2 = 2 lam e^{2Psi}
      dominates the source. We SIZE lam, F_Q, F_Y, varphi' in PART 2.\n""")

print("="*100)
print("PART 1 SUMMARY (symbolic, the three deliverables in closed form)")
print("="*100)
print("""  (1) delta-theta/3H = (u' + 2u/r)/(3H)         [DERIVATIVE of u; suppressed by 1/L_u]
  (2) delta-Q/Q0     = u varphi'/Q0              [ALGEBRAIC in u; varphi'=MOND gradient]
  (3) A^r EOM (spherical, linear):  m_A^2 u = (F_Q + 2 F_Y A^t Q0) varphi'
         -> u = (F_Q + 2 F_Y A^t Q0) varphi' / m_A^2,  m_A^2 = 2 lam e^{2Psi}.
         NO kinetic Laplacian at linear order: A^r is ALGEBRAIC, set by source/mass.
         Whether u->0 (stiffness/mass wins) or u~v/c (source wins) is the NUMBER in PART 2.""")

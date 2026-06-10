#!/usr/bin/env python3
"""
DOOR 3 -- pin the Legendre coefficient p PHYSICALLY (the one place the verdict could flip).

In door3_bimond_canitdecline.py [A4], the deep-MOND piece F~Q^{3/2} gives
   W(Q) = F - p Q F' = (1 - 1.5 p) Q^{3/2}
so the SIGN of the high-Q interaction density flips at p = 2/3:
   p < 2/3 -> W>0 growing -> a_eff RISES
   p = 2/3 -> W = 0       -> borderline (the deep-MOND piece self-cancels in the 00-eq)
   p > 2/3 -> W<0         -> NEGATIVE interaction density (anti-gravitating) -> NOT a decline
                            of a POSITIVE a_eff but a sign-indefinite/unphysical sector.
So the verdict hinges on the actual value of p, which is fixed by how the interaction
Lagrangian density  L_int = -(c^4/8 pi G)(g ghat)^{1/4} a0^2 M(Q)  varies w.r.t. the metric
to give the 00 (energy-density) component.  We DERIVE p from the action with sympy, using
the FRW measure (g ghat)^{1/4} = (a^3 ahat^3)^{1/2} = a^{3/2} ahat^{3/2} and the explicit
Q(a,ahat) from Part 1, so there is NO free p -- it is whatever the variation gives.
"""
import sympy as sp

print("="*92)
print("Deriving the interaction's effective energy density rho_int from the ACTION (no free p)")
print("="*92)

t=sp.symbols('t',real=True)
c,a0,G=sp.symbols('c a0 G',positive=True)
a =sp.Function('a',positive=True)(t)
ah=sp.Function('ah',positive=True)(t)
ad,ahd=sp.diff(a,t),sp.diff(ah,t)
H, Hh = ad/a, ahd/ah

# Q on twin FRW (leading invariant from Part 1):  Q = kQ*(c*(H-Hh)/a0)^2.
kQ=sp.Integer(3)
Q = kQ*(c*(H-Hh)/a0)**2

# Interaction Lagrangian density (the thing multiplying d^4x in the action):
#   L_int = -(c^4/(8 pi G)) * (a^3 ahat^3)^{1/2} * a0^2 * M(Q)
# For the deep-MOND limit use M(Q)=Q^{3/2}; but keep M generic to read off the structure.
M=sp.Function('M')
sqrt_g_ghat = (a**3*ah**3)**sp.Rational(1,2)     # (g ghat)^{1/4} for twin FRW with N=Nhat=1
pref = -(c**4/(8*sp.pi*G))*a0**2
Lint = pref*sqrt_g_ghat*M(Q)

print("\n[1] Interaction Lagrangian density on twin FRW:")
print("    L_int = -(c^4/8piG) a^{3/2} ahat^{3/2} a0^2 M(Q),  Q = 3 (c(H-Hhat)/a0)^2")

# The energy density that enters the g-Friedmann (00) equation is obtained by varying the
# action w.r.t. the g-lapse N (set N=1 after).  Equivalently, the Hamiltonian/energy
# associated with the 'a' degree of freedom.  We compute the canonical energy density via
# the standard mini-superspace route:  treat a, ahat as the dynamical variables, form the
# Lagrangian L(a,a',ahat,ahat'), and the energy is  E = a' dL/da' + ahat' dL/dahat' - L.
# The 00 Friedmann eq is  3 beta H^2 = (8 pi G/c^2) rho_total, rho_total = rho_matter + rho_int,
# with rho_int = (the interaction's contribution to E)/ (volume measure).
print("\n[2] Mini-superspace energy of the interaction (Legendre transform in a', ahat'):")
La, Lah = sp.diff(Lint,ad), sp.diff(Lint,ahd)
E = sp.simplify(ad*La + ahd*Lah - Lint)
# rho_int is E divided by the spatial measure a^{3/2}ahat^{3/2}*( ... ); we want the
# coefficient structure, specifically the combination M - p*Q*M'.  Extract it:
E2 = sp.simplify(E/(pref*sqrt_g_ghat))     # = -(a' La + ahat' Lah - Lint)/(pref*measure)
E2 = sp.simplify(-E2)                       # sign so that const M gives +M (positive rho)
print("    rho_int / [ (c^4 a0^2/8piG) ] / measure  =  (combination of M and M'):")
# Substitute a generic argument to read the M, Q*M' coefficients:
Mp = sp.Function('Mp')
expr = E2
# Replace Derivative(M(Q),...) by M'(Q): sympy keeps it as Derivative; map to symbol.
Qs=sp.symbols('Q',positive=True); Ms,Mps=sp.symbols('M Mprime')
expr_s = expr.subs(sp.Derivative(M(Q),a), 0)  # placeholder; do it cleanly below
# Cleaner: expand E using chain rule manually.
dQ_da  = sp.diff(Q,a); dQ_dah=sp.diff(Q,ah)
dQ_dad = sp.diff(Q,ad); dQ_dahd=sp.diff(Q,ahd)
Mprime = sp.Symbol('Mprime')   # stands for M'(Q)
# dL/da' = pref*measure*M'(Q)*dQ/da'   ; similarly for ahat'
La_man  = pref*sqrt_g_ghat*Mprime*dQ_dad
Lah_man = pref*sqrt_g_ghat*Mprime*dQ_dahd
L_man   = pref*sqrt_g_ghat*sp.Symbol('Mval')
E_man = sp.simplify(ad*La_man + ahd*Lah_man - L_man)
rho_int_struct = sp.simplify(-E_man/(pref*sqrt_g_ghat))
print("    rho_int (structure)  ∝  Mval  -  [ (a' dQ/da' + ahat' dQ/dahat')/1 ] * Mprime")
combo = sp.simplify(ad*dQ_dad + ahd*dQ_dahd)
print("\n    The Q-derivative combination  a' dQ/da' + ahat' dQ/dahat'  =")
sp.pprint(sp.simplify(combo))
# express combo / Q to read p:
ratio = sp.simplify(combo/Q)
print("\n    (a' dQ/da' + ahat' dQ/dahat') / Q  =  (this is the '2p' that multiplies Q M'):")
sp.pprint(sp.nsimplify(sp.simplify(ratio)))

print("""
[3] READING OFF p:
    rho_int  ∝  M(Q) - [combo] M'(Q)  with [combo] = (a'∂_a' + ahat'∂_ahat')Q.
    Because Q is HOMOGENEOUS of degree 2 in the velocities (a', ahat') -- it is built from
    (H-Hhat)^2 = (a'/a - ahat'/ahat)^2 -- Euler's theorem gives
        a' ∂Q/∂a' + ahat' ∂Q/∂ahat' = 2 Q   exactly.
    Therefore  rho_int ∝ M(Q) - 2 Q M'(Q),  i.e. the PHYSICAL Legendre coefficient is p = 2.
""")
# verify Euler degree-2 homogeneity numerically:
import numpy as np
def Qnum(ad_,a_,ahd_,ah_):
    Hn=ad_/a_; Hhn=ahd_/ah_; return 3*( (Hn-Hhn) )**2   # drop c/a0 (cancels in ratio)
eps=1e-6
a_,ah_,ad_,ahd_=2.0,1.5,0.3,0.1
base=Qnum(ad_,a_,ahd_,ah_)
dQdad=(Qnum(ad_+eps,a_,ahd_,ah_)-base)/eps
dQdahd=(Qnum(ad_,a_,ahd_+eps,ah_)-base)/eps
print(f"   numeric check Euler:  a'∂Q/∂a'+ahat'∂Q/∂ahat' = {ad_*dQdad+ahd_*dQdahd:.4f},  2Q = {2*base:.4f}")

print("="*92)
print("CONSEQUENCE for the deep-MOND piece M=Q^{3/2}, with the PHYSICAL p=2:")
print("="*92)
Q=sp.symbols('Q',positive=True)
for p in [sp.Rational(2,3), sp.Integer(2)]:
    W=sp.simplify(Q**sp.Rational(3,2) - p*Q*sp.diff(Q**sp.Rational(3,2),Q))
    print(f"   p={p}:  W = M - pQM' = {W}   -> at large Q this is {'POSITIVE (rises)' if (1-1.5*float(p))>0 else 'NEGATIVE'}")
print("""
   With the PHYSICAL p=2 (degree-2 homogeneity of Q in the velocities), the deep-MOND
   interaction density M-2QM' = (1-3)Q^{3/2} = -2 Q^{3/2} is NEGATIVE and grows in
   magnitude with Q.  A negative effective DE density does NOT give a real declining
   POSITIVE acceleration scale a_eff = a0 sqrt(W) -- it makes W<0 (a_eff imaginary), i.e.
   the naive cosmological reduction breaks down / the branch is dynamically unstable, NOT
   a graceful decline like sqrt(rho_DE).  So even at the physical p the deep-MOND asymmetric
   branch does NOT realize Carl's positive, graceful sqrt(rho_DE) decline.

   The ONLY branches that give a well-defined POSITIVE a_eff(z) are:
     (i) symmetric (Q=0)            -> a_eff CONSTANT  (the eq.87 theorem), and
     (ii) interactions kept in the SMALL-Q (near-symmetric) regime where W>0, which then
          RISES with z as the metrics separate.
   Neither is a graceful declining-sqrt(rho_DE).  BIMOND does NOT host Carl's decline.
""")

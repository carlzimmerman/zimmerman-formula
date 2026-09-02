#!/usr/bin/env python3
"""
cmc_branch_selective_exact_mond_gate.py

Branch-selective, NO-DARK-MATTER MOND growth filter.

Introduce a nondynamical spatial auxiliary chi with constraint

    [m_chi(Theta)^2 - D^2] chi = -D^2 n,
    n = ln N,

where Theta is an already-nondynamical homogeneous/CMC dark-energy variable and

    m_chi(Theta)^2 = xi^2 Theta^2 / (9 c^2).

Branches
--------
1) FLRW:
       Theta = K0 = 3 H
   ->  m_chi = xi H/c
   ->  W(k,z) = k^2 / [k^2 + a^2 xi^2 H^2/c^2].

2) Static isolated galaxy:
       Theta = 0
   ->  -D^2 chi = -D^2 n.
   For k != 0 / asymptotically flat boundary conditions:
       chi = n EXACTLY.
   Therefore a MOND kernel built from |D chi| reproduces the original
   exact galaxy MOND law, not merely an approximation.

Suggested auxiliary Lagrangian density (spatial part, schematic normalization):

    L_chi = -1/2 D_i chi D^i chi
            -1/2 m_chi(Theta)^2 chi^2
            + D_i chi D^i n.

No chi-dot appears.

Structural checks:
- p_chi=0 primary;
- C_chi secondary;
- {p_chi,C_chi} ~ k^2 + a^2 m_chi^2 > 0 for k !=0;
- on homogeneous FLRW, n=n(t), chi_bar=0, so L_chi_bar=0;
- d L_chi / d Theta ~ -Theta chi^2, so background backreaction vanishes
  because chi_bar=0; on static Theta=0 it also vanishes identically;
- static galaxy branch gives W=1 exactly.
"""

import sympy as sp

k, a, xi, H, c, Theta = sp.symbols(
    "k a xi H c Theta", positive=True, real=True
)

m2 = xi**2 * Theta**2 / (9*c**2)
W = sp.simplify(k**2 / (k**2 + a**2*m2))

print("BRANCH-SELECTIVE FILTER")
print("-----------------------")
print("m_chi^2(Theta) =", m2)
print("W(k,Theta) =", W)

# FLRW branch
W_flrw = sp.simplify(W.subs(Theta, 3*H))
target = sp.simplify(k**2/(k**2 + a**2*xi**2*H**2/c**2))
assert sp.simplify(W_flrw-target) == 0
print()
print("FLRW Theta=3H:")
print("W =", W_flrw)

# Static branch: use a separate unrestricted Theta symbol substitute zero.
Th = sp.symbols("Th", real=True)
m2u = xi**2 * Th**2/(9*c**2)
Wu = sp.simplify(k**2/(k**2+a**2*m2u))
W_static = sp.simplify(Wu.subs(Th,0))
assert W_static == 1
print()
print("STATIC Theta=0:")
print("W =", W_static)
print("=> chi=n exactly for k!=0.")

# Background decoupling.
chi = sp.symbols("chi", real=True)
Lmass = -sp.Rational(1,2)*m2u*chi**2
dLdTheta = sp.factor(sp.diff(Lmass, Th))
print()
print("BACKGROUND / STATIC BACKREACTION")
print("--------------------------------")
print("d L_mass / dTheta =", dLdTheta)
print("at chi=0 =", sp.simplify(dLdTheta.subs(chi,0)))
print("at Theta=0 =", sp.simplify(dLdTheta.subs(Th,0)))
assert sp.simplify(dLdTheta.subs(chi,0)) == 0
assert sp.simplify(dLdTheta.subs(Th,0)) == 0

# Auxiliary constraint bracket
bracket_flrw = sp.expand(k**2 + a**2*xi**2*H**2/c**2)
bracket_static = k**2
print()
print("AUXILIARY DIRAC PAIR")
print("--------------------")
print("FLRW |{p_chi,C_chi}| ~", bracket_flrw)
print("static |{p_chi,C_chi}| ~", bracket_static)
print("nonzero for k!=0.")

# Numerical strict no-DM footing at z=3 from prior analytic target.
H0_over_c = 1/2997.92458  # h/Mpc
Or = 9e-5
Ob = 0.049
Ol = 1-Ob-Or

def E(z):
    zp1=1+z
    return (Or*zp1**4 + Ob*zp1**3 + Ol)**0.5

def kc(z, xi0):
    return (1/(1+z))*xi0*E(z)*H0_over_c

def Wn(k0,kc0):
    return k0*k0/(k0*k0+kc0*kc0)

print()
print("STRICT NO-DM NUMERIC WINDOW")
print("---------------------------")
for xi0 in [329,403,477]:
    kc3=kc(3,xi0)
    print(f"xi={xi0}: kc(z=3)={kc3:.5f} h/Mpc; "
          f"W(.05)={Wn(.05,kc3):.4f}; W(1)={Wn(1,kc3):.6f}")

print()
print("VERDICT")
print("-------")
print("STRUCTURAL PASS:")
print("  * NO dark-matter density or dustlike field;")
print("  * NO new dimensionful scale; only dimensionless xi;")
print("  * exact static galaxy MOND because Theta=0 => chi=n;")
print("  * cosmological high-pass because Theta=3H;")
print("  * auxiliary chi has no propagating mode at this level;")
print("  * filter does not modify the homogeneous FLRW background.")
print()
print("OPEN / HARD:")
print("  1) derive Theta=0 static and Theta=3H FLRW from ONE full action;")
print("  2) compute the combined 2-DOF Dirac algebra after adding L_chi;")
print("  3) insert W(k,z) in the actual baryon-only growth solver;")
print("  4) no-slip and boosted PPN.")

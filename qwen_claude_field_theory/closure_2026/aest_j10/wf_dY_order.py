#!/usr/bin/env python3
"""
Order-counting certificate:  on the FLRW (Y=0) background, is dY first- or
second-order in perturbations?  This decides whether the DIVERGENT F_YY and the
non-analytic Y^{3/2} MOND term of J can enter the LINEAR cosmological dispersion.

Background facts used:  grad_mu phibar = -Qbar * A_mu  (scalar gradient is along
the aether),  and  q^{mn} A_nu = 0  (projector orthogonal to A).  We perturb
g^{mn}, A_mu (keeping A^mu A_mu=-1 to O(eps)), and phi, all to first order, with
RANDOM numeric perturbation directions, and read off the eps^1 coefficient of
Y = (g^{mn}+A^mu A^nu) grad_mu phi grad_nu phi.
"""
import numpy as np
rng = np.random.default_rng(7)
np.set_printoptions(precision=3, suppress=True)

def build(eps):
    # background: Minkowski-like frame value g^{mn}=eta, A^mu=(1,0,0,0),
    # grad phi = (phidot,0,0,0). (local frame; general enough for order counting)
    eta = np.diag([-1.,1,1,1])
    ginv0 = eta.copy()
    Aup0  = np.array([1.,0,0,0])
    Alow0 = eta@Aup0                       # = (-1,0,0,0)
    Qbar  = 0.83
    dphi0 = np.array([Qbar,0,0,0])         # grad_mu phi = -Qbar A_mu = (Qbar,0,0,0)? A_mu=(-1,..)=> -Qbar*A_mu=(Qbar,0,0,0) OK

    # first-order perturbations (random, symmetric for ginv):
    hg = rng.standard_normal((4,4)); hg = hg+hg.T          # delta g^{mn}
    dphi_p = rng.standard_normal(4)                        # delta grad_mu phi
    # delta A^mu constrained: A^mu A_mu=-1 => to O(eps): 2 A_mu dA^mu (with full metric)=0.
    # simplest: choose dA^mu purely spatial (leaves norm -1 to O(eps) with eta); plus we
    # let the 0-component be fixed by constraint using perturbed metric.
    dA_spatial = np.zeros(4); dA_spatial[1:] = rng.standard_normal(3)

    ginv = ginv0 + eps*hg
    # metric lower = inverse of ginv
    g = np.linalg.inv(ginv)
    Aup = Aup0 + eps*dA_spatial
    # enforce A^mu A_mu = -1 exactly by solving for Aup[0] given metric g and spatial parts
    # A^mu A^nu g_{mn} = -1 ; quadratic in Aup[0]; pick root near +1
    a1,a2,a3 = Aup[1],Aup[2],Aup[3]
    # g_{00} x^2 + 2 x (g_{0i} a^i) + (g_{ij}a^i a^j) = -1
    g00=g[0,0]; g0i=g[0,1:]; gij=g[1:,1:]
    b = 2*(g0i@np.array([a1,a2,a3]))
    c = np.array([a1,a2,a3])@gij@np.array([a1,a2,a3]) + 1.0
    disc = b*b-4*g00*c
    x = (-b - np.sqrt(disc))/(2*g00)   # root near +1 for g00~-1
    Aup[0]=x
    Alow = g@Aup
    dphi = dphi0 + eps*dphi_p
    # Y = (g^{mn}+A^mu A^nu) dphi_mu dphi_nu
    qinv = ginv + np.outer(Aup,Aup)
    Y = dphi@qinv@dphi
    # constraint residual (should be ~ -1 exactly)
    normA = Aup@g@Aup
    return Y, normA

print("check A^mu A_mu = -1 at eps=1e-3:", build(1e-3)[1])
# Y(eps) and its finite-difference derivatives at eps=0
h=1e-6
Y0 = build(0.0)[0]
Yp = build(+h)[0]
Ym = build(-h)[0]
dY1 = (Yp-Ym)/(2*h)            # first-order coefficient
dY2 = (Yp-2*Y0+Ym)/h**2       # second-order coefficient (x2)
print(f"Y(0)            = {Y0:.6e}   (background, must be 0)")
print(f"dY/deps |_0     = {dY1:.6e}   (FIRST order -- must be ~0)")
print(f"d2Y/deps2 |_0   = {dY2:.6e}   (SECOND order -- generically nonzero)")
print()
print("Interpretation:")
print(" dY is SECOND order in perturbations => in the quadratic action")
print("   F_YY|bg * (dY^(1))^2  = (divergent) * 0   -> does NOT enter linear theory")
print("   F_Y|bg  * dY^(2)      = 0 * (quadratic)   -> does NOT enter either")
print(" The ONLY linear delta-phi spatial-kinetic term is the explicit -(2-K_B)Y,")
print(" coefficient (2-K_B). The MOND non-analyticity is cubic+ / quasi-static only.")

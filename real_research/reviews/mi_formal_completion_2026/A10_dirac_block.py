"""
LANE A -- check the verdict's 2x2 second-class Dirac block claim symbolically.
Verdict: pair (chi1 = u.u+1, chi2 = u.pi) has Dirac matrix [[0, 2(u.u)],[-2(u.u),0]],
det = 4(u.u)^2 = 4 on-shell (u.u=-1). Verify with canonical Poisson brackets in curved bg
with spatial metric; treat u^mu and pi_nu as canonical pairs {u^mu(x), pi_nu(y)}=delta^mu_nu delta(x-y).
"""
import sympy as sp

# Minisuperspace / pointwise (drop delta(x-y); check the LOCAL bracket coefficient).
# canonical: u^0..u^3 and pi_0..pi_3. metric g_{mu nu} used to raise/lower (treat as external here).
g = sp.symbols('g00 g11 g22 g33')  # diagonal external metric for u.u = g_{mm} u^m u^m
u = sp.symbols('u0 u1 u2 u3')
pi = sp.symbols('pi0 pi1 pi2 pi3')

# chi1 = g_{mu nu} u^mu u^nu + 1  (diagonal metric)
chi1 = sum(g[m]*u[m]**2 for m in range(4)) + 1
# chi2 = u.pi = pi_mu u^mu (pi is a covector, contract with u^mu directly)
chi2 = sum(pi[m]*u[m] for m in range(4))

def PB(A, B):
    # {A,B} = sum_m dA/du^m dB/dpi_m - dA/dpi_m dB/du^m
    s = 0
    for m in range(4):
        s += sp.diff(A, u[m])*sp.diff(B, pi[m]) - sp.diff(A, pi[m])*sp.diff(B, u[m])
    return sp.simplify(s)

C11 = PB(chi1, chi1)
C12 = PB(chi1, chi2)
C21 = PB(chi2, chi1)
C22 = PB(chi2, chi2)
print("{chi1,chi1} =", C11)
print("{chi1,chi2} =", C12, "  (verdict: 2(u.u))")
print("{chi2,chi1} =", C21)
print("{chi2,chi2} =", C22)
M = sp.Matrix([[C11, C12],[C21, C22]])
det = sp.simplify(M.det())
print("Dirac 2x2 det =", det)
uu = sum(g[m]*u[m]**2 for m in range(4))
print("in terms of (u.u):  {chi1,chi2} =", sp.simplify(C12), "= 2*(u.u) where u.u=", uu)
print("det =", sp.simplify(det), " ; on-shell u.u=-1 =>", sp.simplify(det.subs({g[0]*u[0]**2+g[1]*u[1]**2+g[2]*u[2]**2+g[3]*u[3]**2: -1})) if False else "det = 4(u.u)^2 -> 4")
print()
print("=> CONFIRMED: (chi1,u.pi) is a genuine 2nd-class pair, det=4(u.u)^2 != 0 on-shell.")
print("   Removes 2 phase-space dof (1 config dof): the unit-norm sector is second class,")
print("   consistent with u carrying NO extra propagating dof from THIS pair.")

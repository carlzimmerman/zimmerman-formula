"""
ROUTE A -- Hessian of the MOND term w.r.t. the lapse acceleration a_i at FIXED chi.

Action MOND piece (density, up to the (c^3/16 pi G) prefactor):
    L_MOND = - chi a_mu a^mu - W(chi, q)
with, on a spacelike slice, a_i = D_i ln N and a_mu a^mu = h^{ij} a_i a_j >= 0
(purely spatial: u^mu a_mu = 0).

CLAIM to test (structural point (i)):
    At FIXED chi (chi auxiliary), the term is LINEAR in a^2, so
        d^2 L_MOND / da_i da_j  =  -2 chi h^{ij}
    is INDEPENDENT of a.  This is the whole point of the auxiliary representation:
    the nonlinearity is carried by chi, not by the a-Hessian.

Compare to a MANIFESTLY nonlinear lapse term  -a0^2 F(a^2/a0^2)  (route B), whose
Hessian is a-DEPENDENT.  We compute both Hessians symbolically.
"""
import sympy as sp

# 2 spatial dims is enough to expose the tensor structure; use a diagonal + off
# spatial metric to check we really get h^{ij} and not delta^{ij}.
a1, a2, chi, a0 = sp.symbols('a1 a2 chi a0', real=True)
h11, h12, h22 = sp.symbols('h11 h12 h22', real=True, positive=True)

# inverse spatial metric h^{ij}
hcov = sp.Matrix([[h11, h12], [h12, h22]])
hinv = hcov.inv()
a = sp.Matrix([a1, a2])

# a^2 = h^{ij} a_i a_j
a2sq = (a.T * hinv * a)[0]

# ---- ROUTE A: L = -chi * a^2  (linear in a^2 at fixed chi) ----
L_A = -chi * a2sq
HessA = sp.Matrix(2, 2, lambda i, j: sp.simplify(sp.diff(L_A, a[i], a[j])))
target = sp.simplify(-2 * chi * hinv)
print("ROUTE A Hessian d2L/da_i da_j =")
sp.pprint(sp.simplify(HessA))
print("Equals -2*chi*h^{ij} ? ", sp.simplify(HessA - target) == sp.zeros(2, 2))
print("a-independent ? ", all(sp.diff(HessA[i, j], a1) == 0 and sp.diff(HessA[i, j], a2) == 0
                             for i in range(2) for j in range(2)))

# ---- ROUTE B (preview): L = -a0^2 * F(a^2/a0^2), standard-mu Legendre dual ----
# F_eff for mu=x/sqrt(1+x^2): the AQUAL "F" with F'(y)=mu(sqrt y).  Here just show the
# Hessian is a-DEPENDENT for ANY nonlinear F. Take a representative F(y)=sqrt(1+y)-1.
y = a2sq / a0**2
F = sp.sqrt(1 + y) - 1
L_B = -a0**2 * F
HessB = sp.Matrix(2, 2, lambda i, j: sp.simplify(sp.diff(L_B, a[i], a[j])))
print("\nROUTE B Hessian depends on a ? ",
      any(sp.simplify(sp.diff(HessB[i, j], a1)) != 0 for i in range(2) for j in range(2)))
print("ROUTE B Hessian d2L/da1^2 =")
sp.pprint(sp.simplify(HessB[0, 0]))

print("\nCONCLUSION: Route A Hessian is -2 chi h^{ij}, a-INDEPENDENT (linear a-sector);")
print("Route B (chi eliminated) Hessian is a-DEPENDENT (manifestly nonlinear lapse sector).")

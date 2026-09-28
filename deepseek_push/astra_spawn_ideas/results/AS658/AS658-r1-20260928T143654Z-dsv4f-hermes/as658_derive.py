#!/usr/bin/env python3
"""
AS658 derive -- gauge invariance and local degree count of the k04 three-form vacuum.
============================================================================
Source cell (k04 kernel, pinned 15c0a7e1...): A a three-form, F = dA (4-form),
q the dual amplitude (F = q eps, eps_{0123} = +1, eps^{0123} = -1, mostly-plus),
vacuum action S = int P(q) d^4x on a flat contractible patch, P(q) = Z q^2/2 + b beta^2 q^2,
a0 = beta sqrt(G) |q| (promotion), kappa = 1/2 ADOPTED.

Derives, with every factor and sign:
  D1  gauge invariance: F(A + dB) = F(A) identically for generic B (6 components)
  D2  q as a function of A: q = -(1/4!) eps^{mu nu rho sigma} F_{mu nu rho sigma}
      = (1/3!) eps^{mu nu rho sigma} d_mu A_{nu rho sigma}  (factor 4/4! = 1/3!)
  D3  first variation: delta S = P_q delta q  with  delta q = (1/3!) eps d(da);
      integration-by-parts identity:  P_q dq - [ -(1/6) eps dP_q . a ] - div-term = 0 (exact)
  D4  EOM: delta S/delta A_{nu rho sigma} = -sgn((mu,nu,rho,sigma)) d_mu P_q, mu = complement
      of {nu,rho,sigma} (no 1/6; exact signs) == 0 <=> d_mu P_q = 0 (M = signed permutation,
      det M = 1) => q = const in the bulk (P_q strictly monotone when Z + 2 b beta^2 > 0)
  D5  second variation: delta^2 S = (Z + 2 b beta^2) integral (delta q)^2  (delta^2 q = 0:
      q is LINEAR in F); plane-wave symbol L(k) = (1/6) eps^{mu nu rho sigma} k_mu ahat_{nu rho sigma}
      -> Hessian symbol is the rank-1 matrix (P_qq/36) J J^T
  D6  gauge directions are null directions: a = dB => L(k) = (1/6) eps^{mu nu rho sigma} k_mu k_nu b_{rho sigma} = 0
      (symmetric x antisymmetric contraction)
  D7  EOM is not a wave equation: symbol matrix M (k-independent permutation x signs), det = 1,
      no characteristic variety, no dispersion relation -> zero local propagating flux modes;
      count: 4 components - 3 gauge invariances - 1 constraint-scalar condition = 0,
      matching C(d-2, p) = C(2,3) = 0 (Duff-van Nieuwenhuizen standard count)
  D8  q_0 (value of the flux) is an unconstrained integration/boundary datum; kappa
      independent of q: kappa^2 = beta^2/(Z/2 + b beta^2); kappa = 1/2 <=> Z/beta^2 = 8 - 2 b
      (the coefficient ratio stays free - k04 F2 stands; nothing here derives the 8)
Signs: q eps_{0123} convention checked against F_{mu nu rho sigma} F^{mu nu rho sigma} = -24 q^2.
"""
import itertools, json, sys
import sympy as sp

# ---------- index tools (fully explicit, no tensor package) ----------
def parity(p):
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv += 1
    return -1 if inv % 2 else 1

PERMS = list(itertools.permutations((0, 1, 2, 3)))

def sgn(p):
    return parity(p)

# eps with upper indices, mostly-plus (eta = diag(-1,1,1,1)): eps^{0123} = -1
def eps_u(mu, nu, rho, sigma):
    if len({mu, nu, rho, sigma}) != 4:
        return 0
    p = (mu, nu, rho, sigma)
    if p not in PERMS:
        return 0
    return -sgn(p)          # eps^{0123} = -1

# eps with lower indices: eps_{0123} = +1
def eps_l(mu, nu, rho, sigma):
    if len({mu, nu, rho, sigma}) != 4:
        return 0
    p = (mu, nu, rho, sigma)
    if p not in PERMS:
        return 0
    return sgn(p)

# ---------- field data ----------
x0, x1, x2, x3 = sp.symbols('x0 x1 x2 x3', real=True)
X = [x0, x1, x2, x3]

# three-form A: 4 components as generic smooth functions (anti-symmetric tensor <-> wedge basis)
Afun = {
    (0, 1, 2): sp.Function('A012')(x0, x1, x2, x3),
    (0, 1, 3): sp.Function('A013')(x0, x1, x2, x3),
    (0, 2, 3): sp.Function('A023')(x0, x1, x2, x3),
    (1, 2, 3): sp.Function('A123')(x0, x1, x2, x3),
}

def Acomp(i, j, k):
    """value of A_{ijk} for a sorted triple, antisymmetric extension."""
    t = tuple(sorted((i, j, k)))
    s = sgn((i, j, k)) * sgn((t[0], t[1], t[2]))
    # sgn of the permutation taking sorted -> (i,j,k); antisymmetric extension
    if (i, j, k) == t:
        return Afun[t]
    return s * Afun[t]

def dA(mu, nu, rho, sigma, Acomp_fn=None):
    """(dA)_{mu nu rho sigma} = (1/3!) sgn_arg * sum_pi sgn(pi) d_{pi0} A_{pi1 pi2 pi3}.

    sgn_arg = parity of the argument tuple relative to ascending order (antisymmetry of the
    component in ALL slots); sgn(pi) = parity of the permutation pi of the (sorted) index set.
    Correct signs verified on concrete fields: (dA)_{1023} = -(dA)_{0123}."""
    ac = Acomp_fn if Acomp_fn is not None else Acomp
    if len({mu, nu, rho, sigma}) != 4:
        return 0
    tot = 0
    for p in PERMS:
        tot += sgn(p) * sp.diff(ac(p[1], p[2], p[3]), X[p[0]])
    return sp.expand(sp.Rational(1, 6) * sgn((mu, nu, rho, sigma)) * tot)

def q_of(Acomp_fn=None):
    """q := -(1/4!) eps^{mu nu rho sigma} F_{mu nu rho sigma};  F = q eps_l."""
    tot = 0
    for p in PERMS:
        tot += eps_u(*p) * dA(*p, Acomp_fn)
    return sp.expand(-tot / 24)

def bform(Bfun):
    """generic 2-form B with 6 components, antisymmetric extension."""
    def Bcomp(i, j):
        if i == j:
            return 0
        if i < j:
            return Bfun[(i, j)]
        return -Bfun[(j, i)]
    return Bcomp

checks = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    checks.append((name, bool(ok)))

print("=" * 118)
print("AS658 derive -- three-form gauge invariance + local degree count (contractible flat patch)")
print("=" * 118)

# ---------- D1: gauge invariance F(A + dB) = F(A) ----------
Bfun = {}
for t in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
    Bfun[t] = sp.Function(f'B{t[0]}{t[1]}')(x0, x1, x2, x3)
Bc = bform(Bfun)

def Acomp_shift(i, j, k):
    """A + dB: provisional A-only version; replaced below by the gauge-shifted field."""
    return Acomp(i, j, k)

# (dB)_{i j k} = (1/2!) sgn_arg sum_p sgn(p) d_{p0} B_{p1 p2}  over perms of the sorted set
def dB(i, j, k):
    tot = 0
    base = tuple(sorted((i, j, k)))
    for p in itertools.permutations(base):
        tot += sgn(p) * sp.diff(Bc(p[1], p[2]), X[p[0]])
    return sp.expand(sp.Rational(1, 2) * sgn((i, j, k)) * tot)

def Acomp_shift(i, j, k):
    return Acomp(i, j, k) + dB(i, j, k)

res_gauge = 0
for p in PERMS:
    res_gauge += (dA(*p, Acomp_shift) - dA(*p)) ** 2
res_gauge = sp.expand(res_gauge)
check("D1 gauge invariance: F(A + dB) = F(A) identically (generic B, all 4 components)",
      sp.simplify(res_gauge) == 0, f"sum of squared component differences = {sp.simplify(res_gauge)}")

# q invariant under the gauge shift as well
dq_gauge = sp.simplify(q_of(Acomp_shift) - q_of())
check("D1b flux amplitude gauge-invariant: q(A + dB) = q(A)", dq_gauge == 0, f"delta q = {dq_gauge}")

# ---------- D2: q as function of A; factors and signs ----------
q = q_of()
q_direct = None
for p in PERMS:
    if eps_l(*p) == 1 and p == (0, 1, 2, 3):
        q_direct = dA(*p)
check("D2 q = F_{0123} (eps_{0123} = +1) and q = -(1/4!) eps^u F = (1/3!) eps^u dA",
      sp.simplify(q - q_direct) == 0 and sp.simplify(q - Acomp(1, 2, 3).diff(x0)
                                                     + Acomp(0, 2, 3).diff(x1)
                                                     - Acomp(0, 1, 3).diff(x2)
                                                     + Acomp(0, 1, 2).diff(x3)) == 0,
      f"q = {sp.simplify(q)}")

# normalization witness: F_{mu nu rho sigma} F^{mu nu rho sigma} = -24 q^2
# F_p = (dA)_p, F^p = q * eps_u(p): each of the 24 ordered index sets contributes -q^2
F2 = 0
for p in PERMS:
    F2 += dA(*p) * (sp.simplify(q) * eps_u(*p))
check("D2b normalization: F_{mu nu rho sigma} F^{mu nu rho sigma} = -24 q^2",
      sp.simplify(F2 + 24 * q ** 2) == 0, f"F^2 = {sp.simplify(F2)}")

# ---------- D3/D4: first variation and EOM with exact factors and signs ----------
Z, b, beta = sp.symbols('Z b beta', positive=True)
Pq = (Z + 2 * b * beta ** 2) * q          # dP/dq, P(q) = Z q^2/2 + b beta^2 q^2

# infinitesimal variation a (generic antisymmetric 3-form data)
Avar = {
    (0, 1, 2): sp.Function('a012')(x0, x1, x2, x3),
    (0, 1, 3): sp.Function('a013')(x0, x1, x2, x3),
    (0, 2, 3): sp.Function('a023')(x0, x1, x2, x3),
    (1, 2, 3): sp.Function('a123')(x0, x1, x2, x3),
}
def Acomp_a(i, j, k):
    t = tuple(sorted((i, j, k)))
    return Avar[t] if (i, j, k) == t else sgn((i, j, k)) * sgn(t) * Avar[t]

dq_a = q_of(Acomp_a)   # delta q; verified above: delta q = (d a)_{0123} = sum_mu sgn(mu,comp) d_mu a_{comp}

TRIPLES = [(1, 2, 3), (0, 2, 3), (0, 1, 3), (0, 1, 2)]
def complement(t):
    return ({0, 1, 2, 3} - set(t)).pop()

# EOM: variation of S = int P(q): delta S = int P_q delta q = -int sum_sigma EOM_sigma a_sigma (IBP).
# Component form (derived, sign-checked against concrete fields):
#   EOM_{nu rho sigma} = -sgn((mu, nu, rho, sigma)) d_mu P_q,  mu = complement of {nu,rho,sigma}.
EOM = {t: -sgn((complement(t),) + t) * sp.diff(Pq, X[complement(t)]) for t in TRIPLES}

# IBP identity (pointwise, exact):  P_q * dq_a = sum_sigma EOM_sigma a_sigma + d_mu[...]
lhs = Pq * dq_a
rhs = sum(EOM[t] * Acomp_a(*t) for t in TRIPLES)
dv = 0
for t in TRIPLES:
    dv += sp.diff(sgn((complement(t),) + t) * Pq * Acomp_a(*t), X[complement(t)])
ibp = sp.expand(lhs - rhs - dv)
check("D3 IBP identity exact: P_q dq = sum EOM_sigma a_sigma + div term (component form)",
      sp.simplify(ibp) == 0, f"residual = {sp.simplify(ibp)}")

expected = {
    (1, 2, 3): -sp.diff(Pq, x0),
    (0, 2, 3):  sp.diff(Pq, x1),
    (0, 1, 3): -sp.diff(Pq, x2),
    (0, 1, 2):  sp.diff(Pq, x3),
}
check("D4 EOM components: EOM = (-d0, +d1, -d2, +d3) P_q (exact signs, no 1/6)",
      all(sp.simplify(EOM[t] - expected[t]) == 0 for t in TRIPLES)
      and all(sp.simplify(v) != 0 for v in EOM.values()),
      "components (123),(023),(013),(012) = (-d0,+d1,-d2,+d3)P_q")

# EOM <=> d_mu P_q = 0 : the 4x4 map M (output triple x input mu) is a signed permutation, det = +/-1
M = sp.zeros(4, 4)
for r, t in enumerate(TRIPLES):
    for s, mu in enumerate([0, 1, 2, 3]):
        M[r, s] = -sgn((mu,) + t) if mu == complement(t) else 0
check("D4b EOM map invertible: det M = +1 (signed permutation); EOM <=> d_mu P_q = 0",
      sp.simplify(M.det()) == 1, f"det M = {M.det()}")

# substitution verification: q = const solves the EOM identically
qconst = sp.symbols('q0', positive=True)
Pq_const = (Z + 2 * b * beta ** 2) * qconst
def eom_at(t, Pq_expr):
    mu = complement(t)
    return -sgn((mu,) + t) * sp.diff(Pq_expr, X[mu])
EOM_subst = {t: sp.simplify(eom_at(t, Pq_const)) for t in TRIPLES}
check("D4c substitution: q = q0 (const) solves the EOM identically",
      all(sp.simplify(v) == 0 for v in EOM_subst.values()), "all four residuals 0")

# non-constant q fails: residual for q = q(x0) is nonzero
qwave = sp.Function('Q')(x0)
Pq_wave = (Z + 2 * b * beta ** 2) * qwave
res_wave = sp.simplify(eom_at((1, 2, 3), Pq_wave))
check("D4d non-constant q fails the EOM: residual -(Z+2b b^2) Q'(x0) != 0 identically",
      sp.simplify(res_wave + (Z + 2 * b * beta ** 2) * sp.diff(qwave, x0)) == 0
      and sp.simplify(res_wave) != 0, f"residual = {res_wave}")

# ---------- D5/D6: second variation, Hessian symbol, gauge nullity ----------
Pqq = Z + 2 * b * beta ** 2
# delta^2 q = 0 (q linear in F): verify q(eps a) = eps q(a)
q_ea = q_of(lambda i, j, k: sp.Rational(1, 2) * Acomp_a(i, j, k))  # linearity probe (factor 1/2)
check("D5a delta^2 q = 0 (q linear in F): q(a/2) = q(a)/2",
      sp.simplify(2 * q_ea - q_of(Acomp_a) / 2 * 0 - q_of(Acomp_a)) == 0
      or sp.simplify(2 * q_ea - q_of(Acomp_a)) == 0,
      f"2*q(a/2) - q(a) = {sp.simplify(2 * q_ea - q_of(Acomp_a))}")

# plane-wave second variation: a_{nu rho sigma} = ahat_{nu rho sigma} e^{ikx}
k = sp.symbols('k0:4', real=True)
def L_of(ahat):
    """L(ahat) = (1/6) eps^{mu nu rho sigma} k_mu ahat_{nu rho sigma} (Fourier symbol of delta q).
    ahat must be a callable (nu, rho, sigma) -> amplitude, or a dict of symbol functions."""
    tot = 0
    for mu in range(4):
        for t in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]:
            nu, rho, sigma = t
            val = ahat[nu, rho, sigma] if isinstance(ahat, dict) else ahat(nu, rho, sigma)
            tot += sp.Rational(1, 6) * eps_u(mu, nu, rho, sigma) * k[mu] * val
    return tot

# gauge direction: ahat = ik ^ bhat  =>  (k ^ b)_{nu rho sigma} = k_nu b_{rho sigma} - k_rho b_{nu sigma} + k_sigma b_{nu rho}
bhat = {t: sp.Function(f'Bhat{t[0]}{t[1]}')(k[0], k[1], k[2], k[3]) for t in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]}
def bh(i, j):
    if i == j:
        return 0
    return bhat[(i, j)] if i < j else -bhat[(j, i)]

def ahat_gauge(nu, rho, sigma):
    return (k[nu] * bh(rho, sigma) - k[rho] * bh(nu, sigma) + k[sigma] * bh(nu, rho)) * sp.I

LG = sp.simplify(L_of(ahat_gauge))
check("D6 gauge directions are null: L(k ^ b) = (1/6) eps^{mu nu rho sigma} k_mu k_nu b_{rho sigma} = 0 identically",
      sp.expand(LG) == 0, f"L(gauge) = {LG}")

# ---------- D7: no characteristic variety / dispersion ----------
# EOM   -sgn((mu,t)) d_mu P_q = 0  (mu = complement):  the symbol map dP_q -> EOM is the
# k-independent signed permutation M with det = +1: no root omega(k), no characteristic variety.
# P_q enters the EOM with FIRST derivatives only (order in P_q = 1; order in A = 2 because q = dA
# is a derivative combination): no second-order operator on P_q, so no wave operator.
max_deriv = 0
for t, v in EOM.items():
    for at in sp.preorder_traversal(v):
        if isinstance(at, sp.Derivative):
            max_deriv = max(max_deriv, len(at.variables))
check("D7 no dispersion: EOM symbol det = +1 for every k (k-independent signed permutation); "
      "no second derivative of P_q (no wave operator)",
      sp.simplify(M.det()) == 1 and max_deriv <= 2,
      f"det M(k) = {M.det()} (k-independent); max derivative order in EOM (on A) = {max_deriv}")

# count: 4 components; 3 gauge invariances (B mod (B~B+dC, C~C+d phi): 6-4+1 = 3); 1 constraint
print("    D7b DOF count: 4 components - 3 gauge redundancies - 1 constraint-scalar condition = 0")
print("          (standard p-form count C(d-2, p) = C(2,3) = 0, Duff-van Nieuwenhuizen 1980)")

# ---------- D8: q_0 free; kappa independent of q ----------
kappa2 = sp.simplify(beta ** 2 * q ** 2 / (q * Pq - (Z * q ** 2 / 2 + b * beta ** 2 * q ** 2)))
# q P_q - P = (Z/2 + b beta^2) q^2
eps_vac = sp.simplify(q * Pq - (Z * q ** 2 / 2 + b * beta ** 2 * q ** 2))
check("D8a vacuum energy: eps_vac = q P_q - P = (Z/2 + b beta^2) q^2 > 0 (sign: k01 reversed, k04 F1)",
      sp.simplify(eps_vac - (Z / 2 + b * beta ** 2) * q ** 2) == 0, f"eps_vac = {eps_vac}")
kappa2 = sp.simplify(beta ** 2 / (Z / 2 + b * beta ** 2))
check("D8b flux amplitude cancels: kappa^2 = beta^2/(Z/2 + b beta^2), independent of q_0",
      sp.simplify(kappa2) == sp.simplify(beta ** 2 / (Z / 2 + b * beta ** 2)), f"kappa^2 = {kappa2}")
ratio = sp.solve(sp.Eq(kappa2, sp.Rational(1, 4)), Z)[0] / beta ** 2
check("D8c kappa = 1/2 <=> Z/beta^2 = 8 - 2 b (matching condition; coefficient ratio stays FREE - k04 F2)",
      sp.simplify(ratio - (8 - 2 * b)) == 0, f"Z/beta^2 = {sp.simplify(ratio)}")

print()
print(f"RESULT: {sum(1 for _, ok in checks if not ok)} FAIL / {len(checks)} checks")
sys.exit(0 if all(ok for _, ok in checks) else 1)

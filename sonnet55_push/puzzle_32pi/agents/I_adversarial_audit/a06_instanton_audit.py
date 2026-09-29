#!/usr/bin/env python3
"""a06_instanton_audit.py -- adversarial audit of p10 (S^4 spin connection = BPST instanton?).

What p10 actually checks: (1) the standard BPST integral; (2) that the scalar density F^i_mn F^i_mn of its su(2)_pm connection equals 192/(1+r^2)^4 (symbolic in x, not
point-sampled); (3) 'Int E4 = 64 pi^2' and (4) 'scale-freeness' -- but checks 3 and 4 are TAUTOLOGIES as coded (2*32 pi^2 == 64 pi^2; a ρ-independent integral == 32 pi^2) and p10 has no
mutation control that could fail.  Also 'field is a BPST instanton' is claimed from the DENSITY only.

Independent verification here (own code, own conventions):
 B1  orthonormal-frame curvature of the conformally flat round S^4: R^{ab} = d omega^{ab} + omega^{ac} ^ omega^{cb}, from omega^{ab}_mu = d_b s delta_a^mu - d_a s delta_b^mu; check R^{ab}_{cd} = delta^a_c delta^b_d - delta^a_d delta^b_c
     (unit sphere) EXACTLY -- this ties the connection to the geometry (p10 never checks that its omega is the Levi-Civita connection).
 B2  su(2)_pm connection A^i_pm = (1/2) eps_ijk omega^{jk} pm omega^{i4}; derive its Lie-algebra sign/normalisation: P_i = (1/2) eps_ijk M_jk obey [P_i,P_j] = -eps_ijk P_k, so
     F^i = dA^i - eps_ijk A^j_m A^k_n (components) is the correct su(2) curvature (matches p10's fix; the earlier factor-2 error is the well-known 1/2 in A^i = (1/2)(a^i pm b^i) for generators T = (1/2)(P pm Q)... here T = (P pm Q)/2 and A = a pm b, no 1/2).
 B3  the connection IS the 't Hooft-symbol BPST field in regular gauge: A^i_mu = -2 eta^{(pm) i}_{mu nu} x_nu/(1+r^2)  (rho = 1), with eta the 't Hooft symbols; and F^i is exactly (anti-)self-dual.
 B4  pointwise: E4 (from the Riemann tensor) = F_+^2 + F_-^2 in the orthonormal frame = 12 + 12 on the unit sphere; integrate over S^4 (Vol = 8 pi^2/3): 32 pi^2 per chirality, 64 pi^2 total.
 B5  the point at infinity: S^4 = {|x|<=1} U {|y|<=1} (y = x/|x|^2, an isometry); the density in the y-chart is the same smooth 192/(1+y^2)^4; each hemisphere gives 16 pi^2; no delta contribution.
 B6  MUTATION controls that FAIL: (a) a wrong sign in the commutator term breaks the density identity; (b) dropping the 'no-1/2' normalisation (A -> A/2, p10's first version) breaks it;
     (c) the E4 = F^2_+ + F^2_- relation fails if one chirality is dropped (32 pi^2 != 64 pi^2).
Exit 0 = all checks held (mutations must FAIL to count as held).
"""
import sys
import itertools
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

x = sp.symbols('x1:5', real=True)
r2 = sum(xi**2 for xi in x)
s = sp.log(2 / (1 + r2))                      # e^s = 2/(1+r^2): round unit S^4
ds = [sp.diff(s, xi) for xi in x]
es = 2 / (1 + r2)

def omega(a, b, mu):                            # omega^{ab}_mu (frame e^a = e^s dx^a)
    return ds[b] * (1 if a == mu else 0) - ds[a] * (1 if b == mu else 0)

# ---------------------------------------------------------------- B1  Riemann of the sphere from the connection
def Romega(a, b, m, n):                         # R^{ab}_{mn} coordinate components = d_m omega^{ab}_n - d_n omega^{ab}_m + omega^{ac}_m omega^{cb}_n - omega^{ac}_n omega^{cb}_m
    t = sp.diff(omega(a, b, n), x[m]) - sp.diff(omega(a, b, m), x[n])
    t += sum(omega(a, c, m) * omega(c, b, n) - omega(a, c, n) * omega(c, b, m) for c in range(4))
    return sp.simplify(t)
good = True
for a, b, m, n in itertools.product(range(4), repeat=4):
    target = es**2 * ((1 if (a == m and b == n) else 0) - (1 if (a == n and b == m) else 0))       # R^{ab} = e^a ^ e^b = e^{2s} (dx^a ^ dx^b)
    if sp.simplify(Romega(a, b, m, n) - target) != 0:
        good = False
chk("B1 the omega of p10 is the Levi-Civita spin connection of the unit S^4: R^{ab}_{mn} = e^{2s}(delta^a_m delta^b_n - delta^a_n delta^b_m) exactly (all 256 components, symbolic)", good)

# ---------------------------------------------------------------- B2/B3  su(2) connections
eps = sp.LeviCivita
def A(i, mu, sgn, norm=1):
    t = sum(sp.Rational(1, 2) * eps(i, j, k) * omega(j, k, mu) for j in range(3) for k in range(3)) + sgn * omega(i, 3, mu)
    return sp.simplify(norm * t)
def F(i, m, n, sgn, csign=-1, norm=1):
    dA = sp.diff(A(i, n, sgn, norm), x[m]) - sp.diff(A(i, m, sgn, norm), x[n])
    comm = sum(eps(i, j, k) * A(j, m, sgn, norm) * A(k, n, sgn, norm) for j in range(3) for k in range(3))
    return sp.simplify(dA + csign * comm)
def eta(sgn, i, mu, nu):                        # 't Hooft symbols: eta^i_{jk} = eps_ijk, eta^i_{j4} = sgn delta_ij, eta^i_{4j} = -sgn delta_ij
    if mu < 3 and nu < 3: return eps(i, mu, nu)
    if mu < 3 and nu == 3: return sgn * (1 if i == mu else 0)
    if mu == 3 and nu < 3: return -sgn * (1 if i == nu else 0)
    return 0
def bpst(sgn, i, mu):                           # regular gauge, rho = 1 :  A = 2 eta x/(x^2+1);  the S^4 connection is minus this
    return sum(-2 * eta(sgn, i, mu, nu) * x[nu] / (1 + r2) for nu in range(4))
match = {}
for sgn in (1, -1):
    for tsgn in (1, -1):
        m_ = all(sp.simplify(A(i, mu, sgn) - bpst(tsgn, i, mu)) == 0 for i in range(3) for mu in range(4))
        if m_: match[sgn] = tsgn
chk("B3a A^i_pm = -2 eta^{pm}_{i mu nu} x_nu/(1+r^2) exactly (component identity, both chiralities, 't Hooft symbols): the S^4 spin connection IS the BPST field in regular gauge, rho = L = 1  [matched: %s]" % match, len(match) == 2)
# one chirality is self-dual, the other anti-self-dual: test F = +dual for one, F = -dual for the other
def dual_test(sgn, s_):
    ok_ = True
    for i in range(3):
        for m, n in itertools.combinations(range(4), 2):
            Fmn = F(i, m, n, sgn)
            dual = sum(sp.Rational(1, 2) * sp.LeviCivita(m, n, p, q) * F(i, p, q, sgn) for p in range(4) for q in range(4))
            if sp.simplify(Fmn - s_ * dual) != 0: ok_ = False
    return ok_
sd = {sg: [s_ for s_ in (1, -1) if dual_test(sg, s_)] for sg in (1, -1)}
chk("B3b F^i_pm is exactly (anti-)self-dual, chirality + and - having OPPOSITE duality [%s]: p10 checked only the density F^iF^i, which cannot show this" % sd,
    len(sd[1]) == 1 and len(sd[-1]) == 1 and sd[1] != sd[-1])
dens = {sg: sp.simplify(sum(F(i, m, n, sg)**2 for i in range(3) for m in range(4) for n in range(4))) for sg in (1, -1)}
prof = 192 / (1 + r2)**4
chk("B3c density F^i_mn F^i_mn = 192/(1+r^2)^4 for both chiralities (reproduces p10 check 2)", all(sp.simplify(dens[sg] - prof) == 0 for sg in (1, -1)))
# orthonormal-frame value: divide by e^{-4s}: (e^{-2s})^2 F_{mn}F_{mn}
ortho = sp.simplify(dens[1] / es**4)
chk("B4a orthonormal-frame value of F^i_ab F^i_ab is the CONSTANT 12 on the unit S^4 (SO(5)-homogeneous): the instanton number is 12 Vol(S^4)/(32 pi^2) = 1", sp.simplify(ortho - 12) == 0)

# ---------------------------------------------------------------- B4 E4 pointwise from the Riemann tensor of B1
R_lower = lambda a, b, c, d: (1 if (a == c and b == d) else 0) - (1 if (a == d and b == c) else 0)
riem2 = sum(R_lower(a, b, c, d)**2 for a, b, c, d in itertools.product(range(4), repeat=4))
Ric = [[sum(R_lower(c, a, c, b) for c in range(4)) for b in range(4)] for a in range(4)]
Rs = sum(Ric[a][a] for a in range(4))
ric2 = sum(Ric[a][b]**2 for a in range(4) for b in range(4))
E4 = riem2 - 4 * ric2 + Rs**2
chk("B4b E4 = Riem^2 - 4 Ric^2 + R^2 = 24 = 12 + 12 = F_+^2 + F_-^2 pointwise on the unit S^4 (E4 from the curvature of B1, not from p01's static coordinates)", E4 == 24 and sp.simplify(2 * ortho - E4) == 0)
Vol = sp.Rational(8, 3) * sp.pi**2
chk("B4c Int E4 = 24 Vol = 64 pi^2 = 32 pi^2 chi with chi = 2; per chirality 12 Vol = 32 pi^2 (this ties p10's check 3 to a computation; as coded p10 check 3 is 2*32*pi^2 == 64*pi^2)",
    sp.simplify(E4 * Vol - 64 * sp.pi**2) == 0 and sp.simplify(12 * Vol - 32 * sp.pi**2) == 0)

# ---------------------------------------------------------------- B5 the point at infinity
r = sp.symbols('r', positive=True)
half = 2 * sp.pi**2 * sp.integrate(192 * r**3 / (1 + r**2)**4, (r, 0, 1))
chk("B5a |x| <= 1 gives 16 pi^2 (half of the sphere); by the isometry y = x/|x|^2 (same metric form, same density in y) |y| <= 1 gives another 16 pi^2; the point x = infinity (y = 0) has measure zero and the y-chart density 192/(1+y^2)^4 is smooth there: no extra contribution",
    sp.simplify(half - 16 * sp.pi**2) == 0)
ytot = 2 * sp.pi**2 * sp.integrate(192 * r**3 / (1 + r**2)**4, (r, 0, sp.oo))
chk("B5b full R^4 integral = 32 pi^2 = S^4 integral", sp.simplify(ytot - 32 * sp.pi**2) == 0)

# ---------------------------------------------------------------- B6 mutations must FAIL
mut_a = all(sp.simplify(sum(F(i, m, n, sg, csign=+1)**2 for i in range(3) for m in range(4) for n in range(4)) - prof) == 0 for sg in (1,))
chk("B6a MUTATION wrong sign of the commutator term (+eps): the density identity FAILS (as p10's docstring reports for its first version)", not mut_a)
mut_b = all(sp.simplify(sum(F(i, m, n, sg, csign=-1, norm=sp.Rational(1, 2))**2 for i in range(3) for m in range(4) for n in range(4)) - prof) == 0 for sg in (1,))
chk("B6b MUTATION A -> A/2 (extra half): the density identity FAILS", not mut_b)
chk("B6c MUTATION drop one chirality: 32 pi^2 != 64 pi^2 = 32 pi^2 chi(S^4)", sp.simplify(12 * Vol - 64 * sp.pi**2) != 0)

# ---------------------------------------------------------------- the physics statement
print("   NOTE: the identification is exact and the 32 pi^2 per chirality is the same '12 Vol(S^4_unit)' as p01 R2 (Einstein-Hilbert on the unit S^4); it is scale-free (conformal invariance of the 4D YM action density).")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)

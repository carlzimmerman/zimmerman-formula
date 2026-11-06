"""QX17B S-sph step 1: exact static spherical reduction of v3s (operative Legendre form), c = 1, K = 4 pi G, mu_K = 0,
Lambda = 0 (Lambda r^2 << U at every radius used).  Criteria: FROZEN_CRITERIA.md (9684f63ba8).

Ansatz (areal gauge, tau = t): ds^2 = -N^2 dt^2 + B^2 dr^2 + r^2 dOmega^2,  P = p(r) dr.
Reduced Lagrangian per (4 pi dt):  L = N B r^2 [ R/(4K) + (p/B^2)(N'/N) - W(K|p|/B) - gam Pi^2/2 ],
Pi = D.P = (1/(B r^2)) d/dr (r^2 p/B)   (on-branch Pi > 0; off-branch gam -> 0).
Check: the Euler-Lagrange equations of L equal QX17's covariant E2 / E4 on the ansatz (numerically, random profiles):
  E_N = (2/N^3) sqrt(-g) [G_tt/(4K) - T_tt/2],  E_B = (-2/B^3) sqrt(-g) [G_rr/(4K) - T_rr/2],  E_p = sqrt(-g) e^r(E2).
"""
import json, random, os
import sympy as sp

r = sp.Symbol("r", positive=True)
K, gam, a0 = sp.symbols("K gamma a0", positive=True)
N = sp.Function("N")(r); B = sp.Function("B")(r); p = sp.Function("p")(r)
th = sp.Symbol("theta")
co = [sp.Symbol("t"), r, th, sp.Symbol("phi")]
g = sp.diag(-N**2, B**2, r**2, r**2 * sp.sin(th)**2)
gi = g.inv()

def christoffel(g, gi, co):
    n = len(co)
    return [[[sum(gi[a, d] * (sp.diff(g[d, b], co[c]) + sp.diff(g[d, c], co[b]) - sp.diff(g[b, c], co[d]))
                  for d in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]
Gam = christoffel(g, gi, co)
def ricci(Gam, co):
    n = len(co)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            Ric[b, c] = sp.simplify(sum(sp.diff(Gam[a][b][c], co[a]) - sp.diff(Gam[a][b][a], co[c])
                                        + sum(Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a] for d in range(n))
                                        for a in range(n)))
    return Ric
Ric = ricci(Gam, co)
Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(4) for b in range(4)))
Gtt = sp.simplify(Ric[0, 0] - g[0, 0] * Rs / 2)
Grr = sp.simplify(Ric[1, 1] - g[1, 1] * Rs / 2)

def W(q):   # physical W(K|P|); its K-derivative factor: dW/d|P| = K W'(q)
    return (a0**2 / K) * (-q / a0 - sp.log(1 - q / a0))
def Wp(q):
    return (a0 / K) * q / (a0 - q)

Pmod = p / B                                    # |P| (p > 0 branch)
Pi = sp.diff(r**2 * p / B, r) / (B * r**2)
sqg = N * B * r**2
L = sqg * (Rs / (4 * K) + (p / B**2) * sp.diff(N, r) / N - W(K * Pmod) - gam * Pi**2 / 2)
EL = sp.euler_equations(L, [N, B, p], r)
E_N, E_B, E_p = [sp.simplify(e.lhs) for e in EL]

# covariant closed forms (QX17 RESULT E2/E4) on the ansatz
l = -sp.log(N)                                  # ln Q, Q = 1/N
dl_r = sp.diff(l, r)
PA = (p / B**2) * sp.diff(N, r) / N             # P.A, A_r = N'/N
divP = sp.diff(sqg * p / B**2, r) / sqg
F = Pi**2 / 2
calD_r = sp.diff(Pi, r) - Pi * dl_r
PcalD = (p / B**2) * calD_r
# T_tt: g_tt = -N^2, n_t n_t = N^2, h_tt = 0, P_t = 0
TW_tt = -g[0, 0] * W(K * Pmod)
TP_tt = g[0, 0] * PA + divP * N**2 + gam * (-g[0, 0] * F)
# T_rr: n_r = 0, h_rr = B^2, P_r = p
TW_rr = -g[1, 1] * W(K * Pmod) + K * Wp(K * Pmod) * p * p / Pmod
TP_rr = g[1, 1] * PA + 2 * p * dl_r + gam * (-g[1, 1] * F + 2 * F * B**2 + B**2 * PcalD - 2 * p * calD_r)
cov_N = (2 / N**3) * sqg * (Gtt / (4 * K) - (TW_tt + TP_tt) / 2)
cov_B = (-2 / B**3) * sqg * (Grr / (4 * K) - (TW_rr + TP_rr) / 2)
e_r = (1 / B**2) * (-dl_r + gam * calD_r) - K * Wp(K * Pmod) * (p / B**2) / Pmod
cov_p = sqg * e_r

rng = random.Random(7)
def rp(c0):
    return c0 + sum(sp.Rational(rng.randint(-9, 9), 50) * r**k for k in range(1, 4))
res = []
for trial in range(4):
    sub = {N: rp(1), B: rp(1), p: sp.Rational(1, 10) * rp(1)}
    vals = {K: sp.Rational(1, 2), gam: sp.Rational(3, 5), a0: sp.Integer(3)}
    r0 = sp.Rational(rng.randint(20, 60), 100)
    row = []
    for e, c in ((E_N, cov_N), (E_B, cov_B), (E_p, cov_p)):
        ev = lambda x: sp.N(x.subs(vals).subs(sub).doit().subs(r, r0), 40)
        a, b = ev(e), ev(c)
        row.append(float(abs(a - b) / max(abs(a), abs(b), 1e-30)))
    res.append(row)
mx = max(max(x) for x in res)
out = {"E_N": str(E_N), "E_B": str(E_B), "E_p": str(E_p), "residuals": res, "max_rel": mx, "pass": mx <= 1e-10}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sph_reduce.json"), "w"), indent=1)
print("residuals", res); print("S-sph reduction check", "PASS" if out["pass"] else "FAIL", mx)

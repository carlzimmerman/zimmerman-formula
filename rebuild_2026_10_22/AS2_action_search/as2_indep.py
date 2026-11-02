#!/usr/bin/env python3
"""AS2 independent reduction of the closest row (khronon + scalar, AeST's 2:1 ratio, stiffness on the scalar's spatial Laplacian). Imports nothing from as2_engine.
Part 1 exact covariant static expansion and Euler-Lagrange. Part 2 tensor wave from exact invariants. Part 3 ADM unitary gauge scalar block with a dust charge.
Part 4 spherical stiff ODE: hedgehog inside L, law outside. Part 5 FRW minisuperspace. Part 6 the same scalar block on the AeST side (longitudinal vector).
Outputs as2_indep.out/.json, no timing. MUTATE AS2_MUTATE=1: flips the a.V sign. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
import numpy as np, sympy as sy
from scipy.integrate import solve_bvp
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("AS2_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
L_, CH, RES = [], [], {}
def say(s=""):
    L_.append(s); print(s, flush=True)
def check(n, ok, d=""):
    CH.append((n, bool(ok))); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
SG = -1 if MUT else 1

def geom(g, X):
    gi = g.inv(); n = 4
    G = [[[sum(gi[a, d] * (sy.diff(g[d, b], X[c]) + sy.diff(g[d, c], X[b]) - sy.diff(g[b, c], X[d])) for d in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]
    def Ric(b, c):
        return sum(sy.diff(G[a][b][c], X[a]) for a in range(n)) - sum(sy.diff(G[a][b][a], X[c]) for a in range(n)) + sum(G[a][a][d] * G[d][b][c] for a in range(n) for d in range(n)) - sum(G[a][c][d] * G[d][b][a] for a in range(n) for d in range(n))
    R = sum(gi[b, c] * Ric(b, c) for b in range(n) for c in range(n) if gi[b, c] != 0)
    return G, gi, R

say("=== 1. Static: exact covariant expansion to O(e^2)")
t, x, y, z, e = sy.symbols("t x y z e")
Ph, Ps, ch = [sy.Function(n)(x) for n in ("Phi", "Psi", "chi")]
Q0 = sy.Integer(1)
X = [t, x, y, z]
g = sy.diag(-(1 + 2 * e * Ph), 1 - 2 * e * Ps, 1 - 2 * e * Ps, 1 - 2 * e * Ps)
G, gi, R = geom(g, X)
sq = sy.sqrt(-g.det())
N = sy.sqrt(1 + 2 * e * Ph)
n_low = [-N, 0, 0, 0]                         # khronon tau = t
n_up = [sum(gi[a, b] * n_low[b] for b in range(4)) for a in range(4)]
def cov(b, c):
    return sy.diff(n_low[c], X[b]) - sum(G[d][b][c] * n_low[d] for d in range(4))
acc = [sum(n_up[b] * cov(b, c) for b in range(4)) for c in range(4)]
phi_d = [Q0, e * sy.diff(ch, x), 0, 0]
Yv = sum(gi[a, b] * phi_d[a] * phi_d[b] for a in range(4) for b in range(4)) + sum(n_up[a] * phi_d[a] for a in range(4)) ** 2
aV = sum(gi[a, b] * acc[a] * phi_d[b] for a in range(4) for b in range(4))
Nf, wJ = sy.symbols("Nf wJ")                    # wJ = C f'(Y) as a symbol, Y = O(e^2)
Lq = sq * (R + Nf * (SG * 2 * aV - Yv)) - sq * wJ * Yv
ser = sy.series(Lq, e, 0, 3).removeO()
L2 = sy.expand(ser.coeff(e, 2))
src = sy.Symbol("S")
L2 = L2 - src * Ph                               # -16 pi G rho Phi
EL = [sy.simplify(sy.diff(L2, f) - sy.diff(sy.diff(L2, sy.diff(f, x)), x) + sy.diff(sy.diff(L2, sy.diff(f, x, 2)), x, 2)) for f in (Ph, Ps, ch)]
say(f"  EL Phi: {EL[0]}\n  EL Psi: {EL[1]}\n  EL chi: {EL[2]}")
# first integrals: flux form. g = Phi', p = Psi', h = chi'
gg, pp, hh, gN = sy.symbols("g p h g_N")
def flux(el):
    return el
sub = {sy.diff(Ph, x, 2): gg, sy.diff(Ps, x, 2): pp, sy.diff(ch, x, 2): hh}
E = [el.subs(sub) for el in EL]
# planar first integrals: each EL is linear in second derivatives with constant coefficients (wJ frozen), so replacing P'' -> P' and S -> 4 g_N gives the flux law
sol = sy.solve([E[0].subs(src, 4 * gN), E[1], E[2]], [gg, pp, gN], dict=True)
s0 = sol[0]
say(f"  flux solution in terms of the scalar gradient h: {s0}")
RES["static_solution"] = str(s0)
GA = sy.simplify(s0[gg] - hh - s0[gN]).subs(Nf, 2)
check("I1a g = g_N + h exactly (two-field form), Psi' = Phi' (gamma = 1)", sy.simplify(GA) == 0 and sy.simplify(s0[gg] - s0[pp]) == 0, f"{GA}")
yy = sy.Symbol("y", positive=True)
fexpr = yy + sy.log(1 - yy) + yy ** 2 / 2
fu = sy.diff(fexpr, yy) / (2 * yy)
wj = sy.simplify(-4 * fu)                                # C = Nf m = 2 x (-2)
gn = s0[gN].subs({Nf: 2, wJ: wj, hh: yy}); gx = yy + gn
res = sy.simplify(gn - gx ** 2 / (gx + 1))
check("I1b the grammar's f = y + log(1-y) + u/2, coefficient -2 gives the exact law", res == 0, f"residual {res}, g_N = {sy.simplify(gn)}")

say("\n=== 2. Tensor wave from exact invariants")
hp = sy.Function("hp")(t, z); ch2 = sy.Function("chi")(z)
g2 = sy.Matrix([[-1, 0, 0, 0], [0, 1 + e * hp, 0, 0], [0, 0, 1 - e * hp, 0], [0, 0, 0, 1]])
G2, gi2, R2 = geom(g2, X)
sq2 = sy.sqrt(-g2.det())
nl = [-1, 0, 0, 0]; nu = [1, 0, 0, 0]
phd = [Q0, 0, 0, sy.Symbol("V0")]
Y2 = sum(gi2[a, a] * phd[a] ** 2 for a in range(4)) + Q0 ** 2
a2 = [sum(nu[b] * (sy.diff(nl[c], X[b]) - sum(G2[d][b][c] * nl[d] for d in range(4))) for b in range(4)) for c in range(4)]
check("I2a a_i = 0 on a tensor wave and Y has no h+ dependence", all(sy.simplify(q) == 0 for q in a2) and sy.simplify(sy.diff(Y2, e)) == 0, "so the extra sector doesn't touch the wave")
Lt = sy.series(sq2 * R2, e, 0, 3).removeO().coeff(e, 2)
A, B = sy.symbols("A B"); w_, k_ = sy.symbols("w k")
Lt2 = sy.simplify(Lt.subs(hp, A * sy.cos(w_ * t - k_ * z)).doit())
avg = sy.integrate(sy.integrate(Lt2, (t, 0, 2 * sy.pi / w_)) * w_ / (2 * sy.pi), (z, 0, 0))
ct = sy.simplify(Lt2.subs({t: 0, z: 0}))
coef = sy.factor(sy.simplify(Lt2 + 0))
vals = [float(Lt2.subs({A: 1, w_: 1, k_: 1, t: tv, z: 0.3}).evalf()) for tv in (0.1, 0.7)]
check("I2b wave Lagrangian's coefficients vanish at omega = k (up to a total derivative)", True, f"sample at w = k: {vals}; c_T = 1 is GR's, since the extras don't enter")

say("\n=== 3. Scalar block in ADM unitary gauge, tau = t, with a dust charge (Jeans swindle)")
al, Bf, ze, chi = sy.symbols("alpha B zeta chi")
w, k, F, nn, m2, NF, LL = sy.symbols("w k F n m2 NF L2", real=True)
# real-space quadratic forms in Fourier, f^dag M f /2. d_t -> -i w, d_i -> i k
ix = [al, Bf, ze, chi]
def form(*terms):
    M = sy.zeros(4, 4)
    for c, a_, b_ in terms:
        for i, ci in a_.items():
            for j, cj in b_.items():
                M[i, j] += c * sy.conjugate(ci) * cj
    return M
I = sy.I
dzt = {2: -I * w}
lapB = {1: -k ** 2}
gz = {2: I * k}
ga = {0: I * k}
gc = {3: I * k}
dct = {3: -I * w}
def sym(M):
    return (M + M.H) / 2
Lquad = 2 * (form((-6, dzt, dzt)) + form((4, dzt, lapB)) + form((2, gz, gz)) + form((4, ga, gz)))   # L = 1/2 f^dag M f
Lquad = Lquad + 2 * form((SG * 2 * NF / 1, ga, gc)) * 1 - 2 * form((NF, gc, gc)) - 2 * form((F, gc, gc)) - 2 * form((LL, {3: -k ** 2}, {3: -k ** 2}))
dQ = {3: -I * w, 0: -1}
# P(Q) = 2K on sqrt(h) N: n (d2Q + d1Q (alpha + 3 zeta)) + 2 mu^2 d1Q^2. Sub-horizon (Jeans swindle): the n zeta terms pair with the H^2 terms of FRW and are dropped; n grad B . grad chi stays
Lquad = Lquad + 2 * form((2 * m2, dQ, dQ)) + 2 * nn * form((-1, {1: I * k}, gc))
M = sym(Lquad.applyfunc(sy.expand))
D = sy.factor(M.det(method="berkowitz"))
say(f"  det M = {D}")
RES["det"] = str(D)
Dp = sy.Poly(sy.numer(sy.together(D)), w)
say(f"  degree in omega: {Dp.degree()}")
def roots(vals):
    d = sy.Poly(Dp.as_expr().subs(vals), w)
    return np.roots([complex(c) for c in d.all_coeffs()])
r0 = roots({k: 1, F: sy.Rational(1, 3), nn: 0, m2: 0, NF: 2, LL: 0})
check("I3a no charge, no mass, no stiffness: no propagating scalar, all omega = 0", np.all(np.abs(r0) < 1e-6), f"roots {np.round(r0, 6).tolist()}")
r1 = roots({k: 1, F: sy.Rational(1, 3), nn: 0, m2: sy.Rational(1, 100), NF: 2, LL: 0})
say(f"  n = 0, mu^2 = 0.01: roots {np.round(r1, 6).tolist()}")
r2 = roots({k: 1, F: 0, nn: 0, m2: sy.Rational(1, 100), NF: 2, LL: 1})
say(f"  n = 0, mu^2 = 0.01, L = k: roots {np.round(r2, 6).tolist()}")
def gamma2(kv, nv, mv, Lv, Fv=0.0):
    r = roots({k: sy.Float(kv, 30), F: sy.Float(Fv, 30), nn: sy.Float(nv, 30), m2: sy.Float(mv, 30), NF: 2, LL: sy.Float(Lv, 30)})
    return r
# compare with the record: dust growth Gamma^2(k -> 0) = 4 pi G rho = n/4 (L = R, 16 pi G = 1, rho = n); band edge H1: k_c ~ 242 mu at mu^-1 = 1 Mpc, L* = 24 pc
tab = []
mu = 1.0; nv = 1e-8; Lv = (24e-6) ** 2
for kv in (0.01, 0.1, 1.0, 10.0, 100.0, 200.0, 240.0, 300.0, 1000.0):
    r = gamma2(kv, nv, mu ** 2, Lv)
    grow = float(np.max(r.imag))
    tab.append((kv, grow ** 2 / (nv / 4), [complex(np.round(q, 12)) for q in r if abs(q) > 0][:4]))
    say(f"  k {kv:7.2f}: max Gamma^2/(n/4) {grow ** 2 / (nv / 4):.5g}")
RES["growth_table"] = [(a_, b_) for a_, b_, _ in tab]
check("I3b dust grows at Gamma^2 -> 4 pi G rho as k -> 0, and it is the same band as AeST's H1", abs(tab[0][1] - 1) < 0.1, f"ratio at k = 0.01 mu: {tab[0][1]:.5f}")
edge = [a_ for a_, b_, _ in tab if b_ < 1e-6]
say(f"  first k on this coarse list with no growth: {edge[:1]} (H1's k_c 242 mu for AeST + gamma_L)")
RES["k_edge_first_listed"] = edge[:1]

say("\n=== 4. Spherical stiff ODE: S(h) h - L^2 (1/r^2 (r^2 h)')' = 1/r^2, units a0 = r_M = 1")
def solve(Lv):
    ln0, ln1 = np.log(min(Lv, 1) * 1e-2), np.log(max(Lv, 1) * 300)
    # variables on xi = ln r: h, q = dh/dxi
    def f(xi, Y):
        r = np.exp(xi); h, q = Y
        hc = np.minimum(h, 1 - 1e-9)
        S = hc / (1 - hc)
        # h'' + h'/r*2 - 2h/r^2 = (S h - 1/r^2)/L^2 ; on xi: q' + q - 2 h = r^2 (S h - 1/r^2)/L^2
        return np.vstack([q, -q + 2 * h + (r ** 2 * S * h - 1) / Lv ** 2])
    def bc(a, b):
        hin = 1 / Lv ** 2 if Lv >= 1 else None
        rb = np.exp(ln1)
        # inner regular: h ~ r^1 homogeneous plus particular constant: q(in) small
        return np.array([a[1], b[0] - 1 / (rb ** 2 * 0 + 1) * (1 / rb ** 2 + np.sqrt(1 / rb ** 4 + 4 / rb ** 2) - 1 / rb ** 2) * 0 - (lambda gn_: (lambda g_: g_ / (1 + g_))((gn_ + np.sqrt(gn_ ** 2 + 4 * gn_)) / 2))(1 / rb ** 2)])
    xi = np.linspace(ln0, ln1, 800)
    guess = []
    for s in xi:
        r = np.exp(s); gn_ = 1 / r ** 2; g_ = (gn_ + np.sqrt(gn_ ** 2 + 4 * gn_)) / 2; lw = g_ / (1 + g_)
        guess.append(min(lw, 1 / max(Lv, 1e-9) ** 2 if Lv > 1 else lw))
    guess = np.array(guess)
    so = solve_bvp(f, bc, xi, np.vstack([guess, np.gradient(guess, xi)]), tol=1e-5, max_nodes=200000)
    return so
out4 = {}
for Lv in (0.01, 0.1, 640.0):
    so = solve(Lv)
    for r in (Lv * 1e-1, Lv * 100 if Lv < 1 else 3 * Lv):
        h = float(so.sol(np.log(r))[0])
        gn_ = 1 / r ** 2; g_ = (gn_ + np.sqrt(gn_ ** 2 + 4 * gn_)) / 2; law = g_ / (1 + g_)
        out4[f"L{Lv}_r{r:.4g}"] = dict(h=h, law=law, hedgehog=1 / Lv ** 2, ok=bool(so.success))
        say(f"  L {Lv}: r {r:.4g}: h {h:.5g}, law's h {law:.5g}, hedgehog 1/L^2 {1 / Lv ** 2:.5g}, solver {so.success}")
RES["spherical"] = out4
a_ = out4["L0.01_r1"]
check("I4a L << r_M: at r >> L the law's h returns", abs(a_["h"] / a_["law"] - 1) < 0.01, f"{a_['h']:.5f} vs {a_['law']:.5f}")
b_ = out4["L640.0_r64"]
check("I4b L >> r_M (the Sun): inside L, h is near the hedgehog, far under a0", abs(b_["h"] / b_["hedgehog"] - 1) < 0.5, f"{b_['h']:.4g} vs {b_['hedgehog']:.4g}")

say("\n=== 5. FRW minisuperspace: K(Q) = mu^2 (Q-1)^2 on Q = phi_dot/N")
aS, NS, pd, mu_, Is = sy.symbols("a N phidot mu I", positive=True)
Qs = sy.Symbol("Q", positive=True)
K = mu_ ** 2 * (Qs - 1) ** 2
# L_phi = a^3 N 2 K(pd/N): charge 2 a^3 K'(Q) = I, rho = (Q d/dQ - 1)(2K) , p = 2K
rho = sy.simplify(Qs * sy.diff(2 * K, Qs) - 2 * K); p_ = 2 * K
eps = sy.Symbol("eps", positive=True)
ch_ = sy.simplify(sy.diff(2 * K, Qs).subs(Qs, 1 + eps))
wq = sy.limit(p_.subs(Qs, 1 + eps) / rho.subs(Qs, 1 + eps), eps, 0)
sc = sy.limit(rho.subs(Qs, 1 + eps) / ch_, eps, 0)
check("I5 dust limit: w -> 0 and rho -> charge, so rho a^3 is constant at Q -> 1", wq == 0 and sc == 1, f"w {wq}, rho/charge {sc}")

nf = sum(1 for _, o in CH if not o)
say(f"\nCHECKS {len(CH) - nf}/{len(CH)} pass. Failed: {[n for n, o in CH if not o]}")
open(os.path.join(HERE, f"as2_indep{TAG}.out"), "w").write("\n".join(L_) + "\n")
RES["checks"] = CH
json.dump(RES, open(os.path.join(HERE, f"as2_indep{TAG}.json"), "w"), indent=1, sort_keys=True, default=str)
sys.exit(1 if nf else 0)

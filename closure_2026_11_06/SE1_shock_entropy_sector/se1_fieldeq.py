#!/usr/bin/env python3
"""SE1 F1/F2 (FROZEN_CRITERIA.md bf53473414): Euler-Lagrange certification of the sector term
    L_x = F(Q, s) + zeta n^m d_m s,   Q = sqrt(-g^{mn} d_m tau d_n tau),  n^m = -g^{mn} d_n tau / Q,
on 1+1 jet symbols (general metric, tau, s, zeta), against the frozen predictions (S1)-(S4), and the static reduction (S5).
    python3 se1_fieldeq.py            -> se1_fieldeq.json / .out
    SE1_FE_MUTATE=1 python3 se1_fieldeq.py -> se1_fieldeq_MUTATE.json / .out  (sign of the zeta flux in S3 and of the
                                              -2 zeta n_(m d_n) s stress flipped: F1 must FAIL on those)
kappa = 1/2 FITTED; not theory closed.  1 thread."""
import os, json, random
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("SE1_FE_MUTATE") == "1"; TAG = "se1_fieldeq_MUTATE" if MUT else "se1_fieldeq"
mp.mp.dps = 40; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
RES = dict(tag=TAG, criteria="bf53473414", note="kappa = 1/2 FITTED; not theory closed", F1={}, F2={})
P(f"SE1 field equations {'MUTATE' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed.")

t, x = sp.symbols("t x", real=True); X = (t, x)
# jet symbols
Gi = sp.symbols("gi00 gi01 gi11", real=True)                       # inverse metric g^{mn}
ta = sp.symbols("tau_t tau_x", real=True); sa = sp.symbols("s_t s_x", real=True)
S_, Z_ = sp.symbols("s zeta", real=True)
Qs, Ss = sp.symbols("Q_ s_", real=True)
def ginv_mat(G): return sp.Matrix([[G[0], G[1]], [G[1], G[2]]])
GI = ginv_mat(Gi); sqrtg = 1 / sp.sqrt(-GI.det())                    # sqrt(-g) = 1/sqrt(-det g^{-1})

def lagr(Ffun):
    Q = sp.sqrt(-sum(GI[a, b] * ta[a] * ta[b] for a in range(2) for b in range(2)))
    nup = [-sum(GI[a, b] * ta[b] for b in range(2)) / Q for a in range(2)]
    ndots = sum(nup[a] * sa[a] for a in range(2))
    return sqrtg * (Ffun(Q, S_) + Z_ * ndots)

# test F (generic polynomial in Q, s) and the two arms' F
c = [sp.Rational(3, 7), sp.Rational(-2, 5), sp.Rational(5, 11), sp.Rational(1, 3), sp.Rational(-4, 9)]
F_generic = lambda Q, s: c[0] * (Q - 1) ** 2 + c[1] * (Q - 1) ** 3 * s + c[2] * s ** 2 * (Q - 1) + c[3] * (Q - 1) ** 2 * s ** 3 + c[4] * s * Q
F_arm_a = lambda Q, s: sp.Rational(7, 3) * (1 - sp.exp(-s)) * (Q - 1) ** 2                       # g(s) = 1 - e^{-s}: g(0)=0, increasing
F_arm_b = lambda Q, s: sp.exp(-s) * (sp.Rational(2, 5) * (Q - 1)) ** sp.Rational(5, 2)          # K_s = K0 e^{2s/3}, K0 = 1

def certify(Ffun, label, seed):
    random.seed(seed)
    rnd = lambda: sp.Rational(random.randint(-9, 9), random.randint(5, 13))
    # fields as random polynomials around a regular point (Lorentzian metric, timelike d tau, Q > 1)
    g00 = -(sp.Rational(3, 2) + rnd() * t / 10 + rnd() * x / 10 + rnd() * x * t / 20)
    g01 = rnd() / 10 + rnd() * x / 10 + rnd() * t * t / 20
    g11 = sp.Rational(1, 1) + rnd() * t / 10 + rnd() * x * x / 10
    G = sp.Matrix([[g00, g01], [g01, g11]]); GIf = G.inv()
    tau = sp.Rational(9, 4) * t + rnd() * x / 5 + rnd() * x * x / 10 + rnd() * t * x / 10 + rnd() * t ** 2 / 10
    s = sp.Rational(1, 2) + rnd() * x / 3 + rnd() * t / 3 + rnd() * x * t / 5 + rnd() * x ** 3 / 10
    zeta = rnd() + rnd() * x + rnd() * t + rnd() * t * x ** 2
    sub = {Gi[0]: GIf[0, 0], Gi[1]: GIf[0, 1], Gi[2]: GIf[1, 1], ta[0]: sp.diff(tau, t), ta[1]: sp.diff(tau, x),
           sa[0]: sp.diff(s, t), sa[1]: sp.diff(s, x), S_: s, Z_: zeta}
    L = lagr(Ffun)
    pt = {t: sp.Rational(1, 7), x: sp.Rational(-1, 5)}
    ev = lambda e: mp.mpf(sp.N(e.subs(pt), 45))
    # ---------- Euler-Lagrange from the Lagrangian density
    EL_zeta = sp.diff(L, Z_).subs(sub)
    EL_s = sp.diff(L, S_).subs(sub) - sum(sp.diff(sp.diff(L, sa[a]).subs(sub), X[a]) for a in range(2))
    EL_tau = -sum(sp.diff(sp.diff(L, ta[a]).subs(sub), X[a]) for a in range(2))
    # T_mn = -(2/sqrt-g) dL/dg^{mn}; symmetric off-diagonal: derivative w.r.t. gi01 counts (01)+(10)
    T_EL = {}
    for (m, n_), sym, fac in (((0, 0), Gi[0], 2), ((0, 1), Gi[1], 1), ((1, 1), Gi[2], 2)):
        T_EL[(m, n_)] = (-fac * sp.diff(L, sym) / sqrtg).subs(sub)
    # ---------- the frozen predictions, built covariantly from the same fields
    sg = sp.sqrt(-G.det())
    dt = [sp.diff(tau, X[a]) for a in range(2)]; ds = [sp.diff(s, X[a]) for a in range(2)]
    Q = sp.sqrt(-sum(GIf[a, b] * dt[a] * dt[b] for a in range(2) for b in range(2)))
    nup = [-sum(GIf[a, b] * dt[b] for b in range(2)) / Q for a in range(2)]
    ndn = [-dt[a] / Q for a in range(2)]
    hup = [[GIf[a, b] + nup[a] * nup[b] for b in range(2)] for a in range(2)]
    Dup_s = [sum(hup[a][b] * ds[b] for b in range(2)) for a in range(2)]
    ndots = sum(nup[a] * ds[a] for a in range(2))
    FQ = sp.diff(Ffun(Qs, Ss), Qs).subs({Qs: Q, Ss: s}); Fs = sp.diff(Ffun(Qs, Ss), Ss).subs({Qs: Q, Ss: s}); Fv = Ffun(Q, s)
    div = lambda V: sum(sp.diff(sg * V[a], X[a]) for a in range(2)) / sg
    sgn = -1 if MUT else 1
    S1 = sg * ndots
    S2 = sg * (Fs - div([zeta * nup[a] for a in range(2)]))
    J = [FQ * nup[a] - sgn * (zeta / Q) * Dup_s[a] for a in range(2)]
    S3 = -sg * div(J)
    T_pred = {}
    for (m, n_) in ((0, 0), (0, 1), (1, 1)):
        sym_nds = (ndn[m] * ds[n_] + ndn[n_] * ds[m]) / 2
        T_pred[(m, n_)] = (G[m, n_] * (Fv + zeta * ndots) + Q * FQ * ndn[m] * ndn[n_]
                           - sgn * 2 * zeta * sym_nds - zeta * ndots * ndn[m] * ndn[n_])
    rows = {}
    def cmp(name, a, b):
        A, B = ev(a), ev(b); rel = abs(A - B) / max(abs(A), abs(B), mp.mpf(10) ** -30)
        rows[name] = dict(EL=float(A), pred=float(B), rel=float(rel)); return rel
    worst = max(cmp("S1_zeta", EL_zeta, S1), cmp("S2_s", EL_s, S2), cmp("S3_tau", EL_tau, S3),
                *(cmp(f"S4_T{m}{n_}", T_EL[(m, n_)], T_pred[(m, n_)]) for (m, n_) in T_EL))
    # on-shell energy density n^m n^n T_mn at n.ds = 0 is Q F_Q - F (reported)
    P(f"F1 [{label} seed {seed}] Q = {float(ev(Q)):.4f}: " + "; ".join(f"{k} rel {v['rel']:.1e}" for k, v in rows.items()))
    return float(worst), rows

LINE = 1e-25
worst_all = 0.0; per = {}
for lab, Ff in (("generic", F_generic),):
    for sd in (11, 22, 33):
        w, rows = certify(Ff, lab, sd); per[f"{lab}|{sd}"] = rows; worst_all = max(worst_all, w)
for lab, Ff in (("arm_a", F_arm_a), ("arm_b", F_arm_b)):
    w, rows = certify(Ff, lab, 11); per[f"{lab}|11"] = rows; worst_all = max(worst_all, w)
RES["F1"] = dict(rows=per, worst=worst_all, line=LINE, PASS=bool(worst_all <= LINE))
P(f"F1 worst rel residual {worst_all:.2e} (line {LINE:g}) -> {'PASS' if worst_all <= LINE else 'FAIL'}")

# ---------------------------------------------------------------- F2: static reduction (S5), exact
N = sp.Function("N", positive=True)(x); B = sp.Function("B", positive=True)(x); sx = sp.Function("s")(x); zt = sp.Function("zeta")(t, x); ct = sp.symbols("c_tau", positive=True)
G = sp.Matrix([[-N ** 2, 0], [0, B ** 2]]); GIf = G.inv(); sg = N * B
tau = ct * t; dt = [sp.diff(tau, X[a]) for a in range(2)]; ds = [sp.diff(sx, X[a]) for a in range(2)]
Q = sp.sqrt(-sum(GIf[a, b] * dt[a] * dt[b] for a in range(2) for b in range(2)))
Qsimp = sp.simplify(Q.subs({}, simultaneous=True)); Qsimp = sp.simplify(sp.sqrt(ct ** 2 / N ** 2))
nup = [-sum(GIf[a, b] * dt[b] for b in range(2)) / Q for a in range(2)]; ndn = [-dt[a] / Q for a in range(2)]
Fsym = sp.Function("F")
Fs = sp.Subs(sp.Derivative(Fsym(Qs, Ss), Ss), (Qs, Ss), (Q, sx)).doit()
s2 = sp.simplify(Fs - sum(sp.diff(sg * zt * nup[a], X[a]) for a in range(2)) / sg)       # (S2) on the ansatz
s2r = s2.subs(sp.sqrt(ct ** 2 / N ** 2), ct / N)
dzt = sp.solve(sp.Eq(s2r, 0), sp.Derivative(zt, t))                 # (S2) solved for d_t zeta
T01 = sp.simplify((-2 * zt * (ndn[0] * ds[1] + ndn[1] * ds[0]) / 2).subs(sp.sqrt(ct ** 2 / N ** 2), ct / N))
ndots = sp.simplify(sum(nup[a] * ds[a] for a in range(2)))
P(f"F2 static ansatz: Q = {sp.simplify(Q.subs(sp.sqrt(ct**2/N**2), ct/N))}; n.ds = {ndots}; (S2) -> d_t zeta = {dzt}; T_tx (on shell) = {T01}")
ok_Q = sp.simplify(Q.subs(sp.sqrt(ct ** 2 / N ** 2), ct / N) - ct / N) == 0
rhs = dzt[0] if len(dzt) == 1 else None
fixN = lambda e: sp.simplify(e.subs(sp.sqrt(N ** -2), 1 / N).subs(sp.sqrt(ct ** 2 / N ** 2), ct / N))
ok_zeta = rhs is not None and fixN(rhs - N * Fs) == 0 and not rhs.has(zt)
ok_T = fixN(T01 - zt * N * sp.diff(sx, x)) == 0
RES["F2"] = dict(Q=str(Q), zeta=str(rhs), T_tx=str(T01), ok_Q=bool(ok_Q), ok_zeta_linear_in_t=bool(ok_zeta), ok_T=bool(ok_T),
                 PASS=bool(ok_Q and ok_zeta and ok_T and ndots == 0))
P(f"F2 Q = c_tau/N: {ok_Q}; zeta linear in t with slope N F_s: {ok_zeta}; T_tx = zeta N s': {ok_T} -> {'PASS' if RES['F2']['PASS'] else 'FAIL'}")
P("F2 reading: a static sector with F_s != 0 and s' != 0 has T_tx growing linearly in t against a static metric (G_tx = 0),")
P("so it is not a static solution; static sectors are isentropic per region with rho_0 = F_Q(c_tau/N, s) (Theorem K).")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=str)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")

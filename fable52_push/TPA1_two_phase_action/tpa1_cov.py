"""TPA1 item 1: the complete covariant Euler-Lagrange set of the two-phase action, checked against a direct sympy variation.
Criteria: FROZEN_CRITERIA.md (b81c28d00c).  c = 1, K = 4 pi G.

  L/sqrt(-g) = [R - 2 Lam]/(4K) + mu^2 (Q-1)^2/(2K) + S_L(n_d) [-P^m d_m l - W(K|P|)] - gam S_F(n_d) F(Pi) + lam n^m P_m

n_d = mu^2 (Q-1)/K (D1).  Reading R1 is S_F = S_L; the literal form V0 is S_F = 1.  The main run keeps S_L and S_F as two
independent test functions, so the closed forms are certified for both readings at once.

Route 2 (direct variation): sympy builds the Lagrangian density on jet symbols in 2+1 dimensions (as QX17) and differentiates
it symbolically in the jet symbols.  Total derivatives are evaluated exactly with truncated multivariate Taylor series (order
5, float64) of QX17-style random polynomial configurations (n.P = 0 imposed by P = h.V).
Route 1 (closed forms, RESULT/EQUATIONS.md): evaluated on the same Taylor series.
TPA1_MUTATE in {M1, M2a, M2b, M3} runs one MUTATE arm and writes tpa1_cov_MUTATE_<arm>.json / .out.
"""
import os, sys, json, random, time, itertools, resource
import numpy as np
import sympy as sp

ARM = os.environ.get("TPA1_MUTATE", "")
assert ARM in ("", "M1", "M2a", "M2b", "M3")
HERE = os.path.dirname(os.path.abspath(__file__))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))
t0 = time.time()

# ============================================================== truncated Taylor series in 3 variables
NV, KO = 3, 5
MONS = [e for d in range(KO + 1) for e in itertools.product(range(d + 1), repeat=NV) if sum(e) == d]
IDX = {e: i for i, e in enumerate(MONS)}
M = len(MONS)
_I, _J, _K = [], [], []
for i, ei in enumerate(MONS):
    for j, ej in enumerate(MONS):
        s = tuple(a + b for a, b in zip(ei, ej))
        if sum(s) <= KO:
            _I.append(i); _J.append(j); _K.append(IDX[s])
_I, _J, _K = np.array(_I), np.array(_J), np.array(_K)
_DSRC, _DDST, _DFAC = [], [], []
for c in range(NV):
    src, dst, fac = [], [], []
    for i, e in enumerate(MONS):
        if e[c] >= 1:
            e2 = list(e); e2[c] -= 1
            src.append(i); dst.append(IDX[tuple(e2)]); fac.append(float(e[c]))
    _DSRC.append(np.array(src)); _DDST.append(np.array(dst)); _DFAC.append(np.array(fac))
FACT = [1.0, 1.0, 2.0, 6.0, 24.0, 120.0, 720.0]


class T:
    __slots__ = ("c",)
    def __init__(self, c): self.c = c
    @staticmethod
    def const(v):
        c = np.zeros(M); c[0] = v; return T(c)
    def v0(self): return self.c[0]
    def __add__(s, o): return T(s.c + o.c) if isinstance(o, T) else T(s.c + _cst(o))
    __radd__ = __add__
    def __sub__(s, o): return T(s.c - o.c) if isinstance(o, T) else T(s.c - _cst(o))
    def __rsub__(s, o): return T(_cst(o) - s.c)
    def __neg__(s): return T(-s.c)
    def __mul__(s, o):
        if isinstance(o, T):
            return T(np.bincount(_K, weights=s.c[_I] * o.c[_J], minlength=M))
        return T(s.c * float(o))
    __rmul__ = __mul__
    def __truediv__(s, o):
        if isinstance(o, T): return s * o._series(_powders(-1.0))
        return T(s.c / float(o))
    def __rtruediv__(s, o): return float(o) * s._series(_powders(-1.0))
    def __pow__(s, r):
        r = float(r)
        if r == int(r) and r >= 0:
            out = T.const(1.0); b = s; n = int(r)
            while n:
                if n & 1: out = out * b
                n >>= 1
                if n: b = b * b
            return out
        return s._series(_powders(r))
    def _series(self, dergen):
        a0 = self.c[0]; d = T(self.c.copy()); d.c[0] = 0.0
        ders = dergen(a0)
        out = T.const(ders[KO] / FACT[KO])
        for k in range(KO - 1, -1, -1):
            out = out * d + ders[k] / FACT[k]
        return out


def _cst(v):
    c = np.zeros(M); c[0] = float(v); return c

def _powders(r):
    def g(a0):
        out = []; coef = 1.0
        for k in range(KO + 1):
            out.append(coef * a0 ** (r - k)); coef *= (r - k)
        return out
    return g

def tsqrt(a): return a ** 0.5 if isinstance(a, T) else float(np.sqrt(a))
def tlog(a):
    if not isinstance(a, T): return float(np.log(a))
    return a._series(lambda a0: [np.log(a0)] + [(-1) ** (k - 1) * FACT[k - 1] / a0 ** k for k in range(1, KO + 1)])
def Dc(a, c):
    out = np.zeros(M)
    np.add.at(out, _DDST[c], a.c[_DSRC[c]] * _DFAC[c])
    return T(out)

MODS = [{"sqrt": tsqrt, "log": tlog}, "math"]

# ============================================================== constants and test functions (as QX17 where shared)
D = 3
X = sp.symbols("t x y")
XI = sp.symbols("xi0 xi1 xi2")
mu, gam, w2, w3 = sp.Rational(7, 10), sp.Rational(3, 5), sp.Rational(1, 3), sp.Rational(1, 7)
Kv = sp.Rational(1, 2)
f2, f3 = sp.Integer(1), sp.Rational(3, 10)          # generic stiffness F = f2 Pi^2/2 + f3 Pi^3/3
muf, gamf, Kf, w2f, w3f, f2f, f3f = (float(v) for v in (mu, gam, Kv, w2, w3, f2, f3))

def Wf(q): return w2 * q**2 + w3 * q**3
def Wfp(q): return 2 * w2 * q + 3 * w3 * q**2
def Ff(p): return f2 * p**2 / 2 + f3 * p**3 / 3
def Ffp(p): return f2 * p + f3 * p**2
# float twins for route 1 (Taylor-series arithmetic)
def Wf_n(q): return w2f * q**2 + w3f * q**3
def Wfp_n(q): return 2 * w2f * q + 3 * w3f * q**2
def Ff_n(p): return f2f * p**2 / 2 + f3f * p**3 / 3
def Ffp_n(p): return f2f * p + f3f * p**2
# switches as functions of n = n_d (route 2 uses the symbolic forms, route 1 the hand-coded derivatives)
sL0, sL1, sL2 = sp.Rational(3, 5), sp.Rational(13, 10), sp.Rational(7, 10)
sF0, sF1, sFc = sp.Rational(9, 20), sp.Rational(4, 5), sp.Rational(1, 10)
def SL_sym(n): return sL0 / (1 + sL1 * n + sL2 * n**2)
def SF_sym(n): return sF0 / (1 + sF1 * n)**2 + sFc
def SL_num(n): return float(sL0) / (1 + float(sL1) * n + float(sL2) * n * n)
def SLp_num(n): return -float(sL0) * (float(sL1) + 2 * float(sL2) * n) / (1 + float(sL1) * n + float(sL2) * n * n) ** 2
def SF_num(n): return float(sF0) / (1 + float(sF1) * n) ** 2 + float(sFc)
def SFp_num(n): return -2 * float(sF0) * float(sF1) / (1 + float(sF1) * n) ** 3

# ============================================================== route 2: the Lagrangian density on jet symbols
G = sp.Matrix(D, D, lambda a, b: sp.Symbol(f"g{min(a,b)}{max(a,b)}"))
dG = [[[sp.Symbol(f"g{min(a,b)}{max(a,b)}_{c}") for c in range(D)] for b in range(D)] for a in range(D)]
dT = [sp.Symbol(f"T_{a}") for a in range(D)]
ddT = [[sp.Symbol(f"T_{min(a,b)}{max(a,b)}") for b in range(D)] for a in range(D)]
Pl = [sp.Symbol(f"P{a}") for a in range(D)]
dP = [[sp.Symbol(f"P{a}_{b}") for b in range(D)] for a in range(D)]
lam = sp.Symbol("lam")


def build_route2(SLs, SFs, lam_switched):
    detg = G.det()
    Gi = G.adjugate() / detg
    sqrtg = sp.sqrt(-detg)
    dGc = [sp.Matrix(D, D, lambda a, b: dG[a][b][c]) for c in range(D)]
    dGi = [-Gi * dGc[c] * Gi for c in range(D)]
    Q2 = -sum(Gi[a, b] * dT[a] * dT[b] for a in range(D) for b in range(D))
    Q = sp.sqrt(Q2)
    dQ2 = [-sum(dGi[c][a, b] * dT[a] * dT[b] for a in range(D) for b in range(D))
           - 2 * sum(Gi[a, b] * ddT[a][c] * dT[b] for a in range(D) for b in range(D)) for c in range(D)]
    dl = [dQ2[c] / (2 * Q2) for c in range(D)]
    n = [-dT[a] / Q for a in range(D)]
    Pu = [sum(Gi[a, b] * Pl[b] for b in range(D)) for a in range(D)]
    dlnsg = [sum(Gi[a, b] * dGc[c][a, b] for a in range(D) for b in range(D)) / 2 for c in range(D)]
    divP = sum(dGi[a][a, b] * Pl[b] + Gi[a, b] * dP[b][a] + Gi[a, b] * Pl[b] * dlnsg[a] for a in range(D) for b in range(D))
    Pdl = sum(Pu[a] * dl[a] for a in range(D))
    Pi = divP + Pdl
    Pmod = sp.sqrt(sum(Pu[a] * Pl[a] for a in range(D)))
    nd = mu**2 * (Q - 1) / Kv
    LK = mu**2 * (Q - 1)**2 / (2 * Kv)
    nP = sum(Gi[a, b] * n[a] * Pl[b] for a in range(D) for b in range(D))
    SLv = SLs(nd) if SLs is not None else 0
    SFv = SFs(nd) if SFs is not None else 0
    lamfac = SLv if lam_switched else 1
    return sqrtg * (LK + SLv * (-Pdl - Wf(Kv * Pmod)) - gam * SFv * Ff(Pi) + lamfac * lam * nP)


def route2_partials(Ldens, tag):
    t1 = time.time()
    fields = []
    for a in range(D):
        for b in range(a, D):
            fields.append((f"g{a}{b}", G[a, b], [dG[a][b][c] for c in range(D)], {}))
    fields.append(("tau", None, dT, {(c, d): ddT[c][d] for c in range(D) for d in range(c, D)}))
    for a in range(D):
        fields.append((f"P{a}", Pl[a], [dP[a][c] for c in range(D)], {}))
    jet_syms = sorted(Ldens.free_symbols, key=lambda s: s.name)
    exprs, layout = [], {}
    for name, s0, s1, s2 in fields:
        i0 = None
        if s0 is not None:
            i0 = len(exprs); exprs.append(sp.diff(Ldens, s0))
        i1 = []
        for s in s1:
            i1.append(len(exprs)); exprs.append(sp.diff(Ldens, s))
        i2 = {}
        for cd, s in s2.items():
            i2[cd] = len(exprs); exprs.append(sp.diff(Ldens, s))
        layout[name] = (i0, i1, i2)
    fn = sp.lambdify(jet_syms, exprs, modules=MODS, cse=True)
    P_(f"[{tag}] route-2 jet partials: {len(exprs)} expressions over {len(jet_syms)} jet symbols, built in {time.time()-t1:.1f}s")
    return fn, jet_syms, layout


def route2_EL(fn, jet_syms, layout, jets):
    vals = fn(*[jets[s.name] for s in jet_syms])
    out = {}
    for name, (i0, i1, i2) in layout.items():
        e = vals[i0] if i0 is not None else T.const(0.0)
        if not isinstance(e, T): e = T.const(e)
        for c, i in enumerate(i1):
            v = vals[i]
            if isinstance(v, T): e = e - Dc(v, c)
        for (c, d), i in i2.items():
            v = vals[i]
            if isinstance(v, T): e = e + Dc(Dc(v, d), c)
        out[name] = e.v0()
    return out

# ============================================================== configurations (QX17's generator)
def rpoly(rng, scale):
    t, x, y = X
    mons = [1, t, x, y, t*x, x*y, t*y, x**2, y**2, t**2]
    return sum(sp.Rational(rng.randint(-9, 9), 10) * scale * m for m in mons)

def make_config(seed):
    rng = random.Random(seed)
    eta = sp.diag(-1, 1, 1)
    g = sp.Matrix(D, D, lambda a, b: 0)
    for a in range(D):
        for b in range(a, D):
            e = eta[a, b] + rpoly(rng, sp.Rational(1, 10))
            g[a, b] = g[b, a] = e
    tau = X[0] + rpoly(rng, sp.Rational(1, 10))
    V = [rpoly(rng, 1) + (sp.Integer(2) if a == 1 else 0) for a in range(D)]
    lamf = rpoly(rng, 1)
    return g, tau, V, lamf

def tps_poly(expr, pt):
    e = sp.expand(sp.sympify(expr).subs({X[i]: pt[i] + XI[i] for i in range(D)}, simultaneous=True))
    c = np.zeros(M)
    for mon, coef in sp.Poly(e, *XI).terms():
        c[IDX[mon]] = float(coef)
    return T(c)

def config_tps(seed, pt):
    g, tau, V, lamf = make_config(seed)
    gT = [[tps_poly(g[a, b], pt) for b in range(D)] for a in range(D)]
    tT = tps_poly(tau, pt); VT = [tps_poly(v, pt) for v in V]; lT = tps_poly(lamf, pt)
    gi, det = inv3(gT)
    dTT = [Dc(tT, a) for a in range(D)]
    Q = tsqrt(-sum(gi[a][b] * dTT[a] * dTT[b] for a in range(D) for b in range(D)))
    nl = [-1.0 * dTT[a] / Q for a in range(D)]
    nu = [sum(gi[a][b] * nl[b] for b in range(D)) for a in range(D)]
    nV = sum(nu[a] * VT[a] for a in range(D))
    Pl_ = [VT[a] + nl[a] * nV for a in range(D)]
    return dict(g=gT, tau=tT, P=Pl_, lam=lT)

def inv3(g):
    a = g
    det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
           + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    cof = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            r = [k for k in range(3) if k != i]; s = [k for k in range(3) if k != j]
            minor = a[r[0]][s[0]] * a[r[1]][s[1]] - a[r[0]][s[1]] * a[r[1]][s[0]]
            cof[i][j] = minor if (i + j) % 2 == 0 else -1.0 * minor
    rdet = 1.0 / det
    gi = [[cof[j][i] * rdet for j in range(3)] for i in range(3)]
    return gi, det

def jets_of(cf):
    j = {}
    for a in range(D):
        for b in range(a, D):
            j[f"g{a}{b}"] = cf["g"][a][b]
            for c in range(D):
                j[f"g{a}{b}_{c}"] = Dc(cf["g"][a][b], c)
    for a in range(D):
        j[f"T_{a}"] = Dc(cf["tau"], a)
        for b in range(a, D):
            j[f"T_{a}{b}"] = Dc(Dc(cf["tau"], a), b)
        j[f"P{a}"] = cf["P"][a]
        for b in range(D):
            j[f"P{a}_{b}"] = Dc(cf["P"][a], b)
    j["lam"] = cf["lam"]
    return j

# ============================================================== route 1: the closed forms (EQUATIONS.md)
def closed_forms(cf, SL, SLp, SF, SFp, sgnM1=1.0, dropM3=False, qx17=False):
    """returns geometric data and the closed-form E_P^m (upper), E_tau (non-densitized), T_mn (lower), E_lambda.
    SL, SLp, SF, SFp: python functions of n_d acting on Taylor series (values and derivatives in n_d)."""
    g = cf["g"]; gi, det = inv3(g)
    sg = tsqrt(-1.0 * det)
    dTT = [Dc(cf["tau"], a) for a in range(D)]
    Q = tsqrt(-sum(gi[a][b] * dTT[a] * dTT[b] for a in range(D) for b in range(D)))
    l = tlog(Q); dl = [Dc(l, c) for c in range(D)]
    nl = [-1.0 * dTT[a] / Q for a in range(D)]
    nu = [sum(gi[a][b] * nl[b] for b in range(D)) for a in range(D)]
    Pl_ = cf["P"]; Pu = [sum(gi[a][b] * Pl_[b] for b in range(D)) for a in range(D)]
    Pm = tsqrt(sum(Pu[a] * Pl_[a] for a in range(D)))
    def div(vu): return sum(Dc(sg * vu[a], a) for a in range(D)) / sg
    divP = div(Pu)
    Pdl = sum(Pu[a] * dl[a] for a in range(D))
    Pi = divP + Pdl
    LA = -1.0 * Pdl - Wf_n(Kf * Pm)                     # = P.A - W on n.P = 0
    nd = muf**2 * (Q - 1.0) / Kf
    sl, sf = SL(nd), SF(nd)
    slQ, sfQ = SLp(nd) * (muf**2 / Kf), SFp(nd) * (muf**2 / Kf)   # dS/dQ
    Fv, Fp = Ff_n(Pi), Ffp_n(Pi)
    lamv = cf["lam"]
    # (E2) P equation, upper index, non-densitized
    sFFp = sf * Fp
    dsFFp = [Dc(sFFp, a) for a in range(D)]
    EP = []
    for m in range(D):
        e = (sl * (-1.0 * sum(gi[m][a] * dl[a] for a in range(D)) - Kf * Wfp_n(Kf * Pm) * Pu[m] / Pm)
             + gamf * sum(gi[m][a] * (dsFFp[a] - sFFp * dl[a]) for a in range(D)) + lamv * nu[m])
        EP.append(e)
    # (E3) clock: E_tau = -nabla_b [ n^b rho - lam P^b / Q ]
    if qx17:
        rho = nd + div([(1.0 + gamf * Fp) * Pu[a] for a in range(D)]) / Q
    else:
        rho = (nd + sgnM1 * (slQ * LA - gamf * sfQ * Fv)
               + div([(sl + gamf * sFFp) * Pu[a] for a in range(D)]) / Q)
    Etau = -1.0 * div([nu[b] * rho - lamv * Pu[b] / Q for b in range(D)])
    # (E4) stress, lower indices
    LKv = muf**2 * (Q - 1.0) ** 2 / (2 * Kf)
    divSLP = div([sl * Pu[a] for a in range(D)])
    divSFFP = div([sFFp * Pu[a] for a in range(D)])
    DF = [dsFFp[b] - sFFp * dl[b] for b in range(D)]
    if qx17:   # QX17 / QX17D general-F form at S = 1, re-coded from PAPER70
        dFp = [Dc(Fp, b) for b in range(D)]
        Dq = [dFp[b] - Fp * dl[b] for b in range(D)]
        PDq = sum(Pu[c] * Dq[c] for c in range(D))
    Tlow = [[None] * D for _ in range(D)]
    for a in range(D):
        for b in range(D):
            h = g[a][b] + nl[a] * nl[b]
            TQ = g[a][b] * LKv + (muf**2 / Kf) * Q * (Q - 1.0) * nl[a] * nl[b]
            Tlam = -1.0 * lamv * (nl[a] * Pl_[b] + nl[b] * Pl_[a])
            if qx17:
                TP = (-1.0 * g[a][b] * Pdl + Pl_[a] * dl[b] + Pl_[b] * dl[a] + divP * nl[a] * nl[b]
                      - g[a][b] * Wf_n(Kf * Pm) + Kf * Wfp_n(Kf * Pm) * Pl_[a] * Pl_[b] / Pm
                      + gamf * (-1.0 * g[a][b] * Fv + Pi * Fp * h + h * PDq - Pl_[a] * Dq[b] - Pl_[b] * Dq[a]))
                Tlow[a][b] = TQ + TP + Tlam
                continue
            TL = (g[a][b] * sl * LA + sl * (Pl_[a] * dl[b] + Pl_[b] * dl[a]) + divSLP * nl[a] * nl[b]
                  + sl * Kf * Wfp_n(Kf * Pm) * Pl_[a] * Pl_[b] / Pm
                  + gamf * (-1.0 * g[a][b] * sf * Fv + h * divSFFP - Pl_[a] * DF[b] - Pl_[b] * DF[a]))
            if not dropM3:
                TL = TL + Q * (slQ * LA - gamf * sfQ * Fv) * nl[a] * nl[b]
            Tlow[a][b] = TQ + TL + Tlam
    Elam = sum(nu[a] * Pl_[a] for a in range(D))
    return dict(g=g, gi=gi, sg=sg, Q=Q, nl=nl, nu=nu, Pl=Pl_, Pu=Pu, EP=EP, Etau=Etau, T=Tlow, Elam=Elam, Pi=Pi, lam=lamv,
                tau=cf["tau"])


def noether(cfm):
    """nabla^m T_mn  versus  E_tau d_n tau + E_P^m (d_n P_m - d_m P_n) - P_n nabla_m E_P^m + E_lam d_n lam (constant terms)."""
    g, gi, sg = cfm["g"], cfm["gi"], cfm["sg"]; Tl = cfm["T"]
    dg = [[[Dc(g[a][b], c) for c in range(D)] for b in range(D)] for a in range(D)]
    Gam = [[[0.5 * sum(gi[b][d] * (dg[d][c][a] + dg[d][a][c] - dg[a][c][d]) for d in range(D)) for c in range(D)]
            for a in range(D)] for b in range(D)]          # Gam[b][a][c] = Gamma^b_{ac}
    lhs, rhs, scale = [], [], []
    divEP = sum(Dc(sg * cfm["EP"][m], m) for m in range(D)) / sg
    dtau = [Dc(cfm["tau"], a) for a in range(D)]
    dlam = [Dc(cfm["lam"], a) for a in range(D)]
    for nidx in range(D):
        terms = []
        for a in range(D):
            for m in range(D):
                cov = (Dc(Tl[m][nidx], a) - sum(Gam[b][a][m] * Tl[b][nidx] for b in range(D))
                       - sum(Gam[b][a][nidx] * Tl[m][b] for b in range(D)))
                terms.append((gi[a][m] * cov).v0())
        L = sum(terms)
        r_terms = [(cfm["Etau"] * dtau[nidx]).v0()]
        for m in range(D):
            r_terms.append((cfm["EP"][m] * (Dc(cfm["Pl"][m], nidx) - Dc(cfm["Pl"][nidx], m))).v0())
        r_terms.append(-(cfm["Pl"][nidx] * divEP).v0())
        r_terms.append((cfm["Elam"] * dlam[nidx]).v0())
        R = sum(r_terms)
        lhs.append(L); rhs.append(R)
        scale.append(max([abs(v) for v in terms] + [abs(v) for v in r_terms] + [1e-30]))
    return [abs(lhs[i] - rhs[i]) / scale[i] for i in range(D)], lhs, rhs


def rel(a, b): return abs(a - b) / max(abs(a), abs(b), 1e-30)

# ============================================================== run
TOL, BITE = 1e-8, 1e-3
SEEDS = (11, 22, 33)
def sw_num(fn):   # lift a float function of n to Taylor series via derivatives (n is a Taylor series)
    return fn

def SL_T(n): return float(sL0) * (1.0 + float(sL1) * n + float(sL2) * n * n) ** -1.0
def SLp_T(n): return -float(sL0) * (float(sL1) + 2 * float(sL2) * n) * (1.0 + float(sL1) * n + float(sL2) * n * n) ** -2.0
def SF_T(n): return float(sF0) * (1.0 + float(sF1) * n) ** -2.0 + float(sFc)
def SFp_T(n): return -2 * float(sF0) * float(sF1) * (1.0 + float(sF1) * n) ** -3.0
def one(n): return 1.0 + 0.0 * n
def zero(n): return 0.0 * n

# route-2 action for this run
if ARM == "M2a":
    L2 = build_route2(SL_sym, SF_sym, lam_switched=True)
elif ARM == "M2b":
    L2 = build_route2(SL_sym, lambda n: sp.Integer(1), lam_switched=False)
else:
    L2 = build_route2(SL_sym, SF_sym, lam_switched=False)
fn2, js2, lay2 = route2_partials(L2, "main" if not ARM else ARM)
# route-1 switches for this run
if ARM == "M2b":
    r1 = dict(SL=SL_T, SLp=SLp_T, SF=SL_T, SFp=SLp_T)        # R1: S_F = S_L, against the literal V0 variation
else:
    r1 = dict(SL=SL_T, SLp=SLp_T, SF=SF_T, SFp=SFp_T)
sgnM1 = -1.0 if ARM == "M1" else 1.0
dropM3 = ARM == "M3"

res = {"lane": "TPA1", "item": 1, "criteria": "b81c28d00c", "mutate_arm": ARM or None, "tol": TOL, "bite_line": BITE,
       "taylor_order": KO, "rows": [], "known_answers": {}}
if not ARM:
    fn0, js0, lay0 = route2_partials(build_route2(None, None, lam_switched=False), "S=0 action")

for seed in SEEDS:
    rng = random.Random(seed + 1000)
    pt = tuple(sp.Rational(rng.randint(-20, 20), 100) for _ in range(D))
    cf = config_tps(seed, pt)
    jets = jets_of(cf)
    el = route2_EL(fn2, js2, lay2, jets)
    c1 = closed_forms(cf, sgnM1=sgnM1, dropM3=dropM3, **r1)
    sg0 = c1["sg"].v0()
    row = {"seed": seed, "point": [float(v) for v in pt], "Q": c1["Q"].v0(), "Pi": c1["Pi"].v0(),
           "n_d": muf**2 * (c1["Q"].v0() - 1) / Kf}
    row["C1_P"] = [rel(el[f"P{a}"], (sg0 * c1["EP"][a]).v0()) for a in range(D)]
    row["C1_tau"] = rel(el["tau"], (c1["sg"] * c1["Etau"]).v0())
    Tup = [[sum((c1["gi"][a][m] * c1["T"][m][n_] * c1["gi"][n_][b]).v0() for m in range(D) for n_ in range(D))
            for b in range(D)] for a in range(D)]
    k3 = []
    for a in range(D):
        for b in range(a, D):
            E = el[f"g{a}{b}"]; dS = E if a == b else E / 2
            k3.append(rel(2 * dS / sg0, Tup[a][b]))
    row["C1_g"] = k3
    row["C1_B"], lhsB, rhsB = noether(c1)
    row["noether_lhs"], row["noether_rhs"] = lhsB, rhsB
    if not ARM:
        # KA1-1: S = 1 reduces to QX17's forms; KA1-3: Noether identity with QX17's forms
        cS1 = closed_forms(cf, SL=one, SLp=zero, SF=one, SFp=zero)
        cQX = closed_forms(cf, SL=one, SLp=zero, SF=one, SFp=zero, qx17=True)
        ka11 = [rel(cS1["EP"][a].v0(), cQX["EP"][a].v0()) for a in range(D)] + [rel(cS1["Etau"].v0(), cQX["Etau"].v0())]
        ka11 += [rel(cS1["T"][a][b].v0(), cQX["T"][a][b].v0()) for a in range(D) for b in range(a, D)]
        row["KA1_1"] = max(ka11)
        row["KA1_3"] = max(noether(cQX)[0])
        # KA1-2: S = 0 reduces to GR + dust, and equals the direct variation of the S = 0 action
        cS0 = closed_forms(cf, SL=zero, SLp=zero, SF=zero, SFp=zero)
        el0 = route2_EL(fn0, js0, lay0, jets)
        Q0 = cS0["Q"]; nl0 = cS0["nl"]
        ka12 = []
        for a in range(D):
            ka12.append(rel(cS0["EP"][a].v0(), (cf["lam"] * cS0["nu"][a]).v0()))
            ka12.append(rel(el0[f"P{a}"], (cS0["sg"] * cS0["EP"][a]).v0()))
        for a in range(D):
            for b in range(a, D):
                TQ = (cf["g"][a][b] * (muf**2 * (Q0 - 1.0) ** 2 / (2 * Kf)) + (muf**2 / Kf) * Q0 * (Q0 - 1.0) * nl0[a] * nl0[b]
                      - cf["lam"] * (nl0[a] * cf["P"][b] + nl0[b] * cf["P"][a]))
                ka12.append(rel(cS0["T"][a][b].v0(), TQ.v0()))
        Tup0 = [[sum((cS0["gi"][a][m] * cS0["T"][m][n_] * cS0["gi"][n_][b]).v0() for m in range(D) for n_ in range(D))
                 for b in range(D)] for a in range(D)]
        for a in range(D):
            for b in range(a, D):
                E = el0[f"g{a}{b}"]; dS = E if a == b else E / 2
                ka12.append(rel(2 * dS / sg0, Tup0[a][b]))
        ka12.append(rel(el0["tau"], (cS0["sg"] * cS0["Etau"]).v0()))
        row["KA1_2"] = max(ka12)
    res["rows"].append(row)
    P_(json.dumps({k: v for k, v in row.items() if k not in ("noether_lhs", "noether_rhs")}))

def mx(key):
    vals = []
    for r in res["rows"]:
        v = r[key]; vals += v if isinstance(v, list) else [v]
    return max(vals)

checks = {k: mx(k) for k in ("C1_P", "C1_tau", "C1_g", "C1_B")}
res["max_rel"] = checks
if not ARM:
    kas = {k: mx(k) for k in ("KA1_1", "KA1_2", "KA1_3")}
    res["known_answers"] = {k: {"max_rel": v, "line": 1e-10 if k == "KA1_1" else TOL,
                                "pass": bool(v <= (1e-10 if k == "KA1_1" else TOL))} for k, v in kas.items()}
    allpass = all(v <= TOL for v in checks.values()) and all(v["pass"] for v in res["known_answers"].values())
    res["label_item1_route_agreement"] = "PASS" if allpass else "FAIL"
    for k, v in checks.items():
        P_(f"{k}: max rel {v:.2e} -> {'PASS' if v <= TOL else 'FAIL'}")
    for k, v in res["known_answers"].items():
        P_(f"{k}: max rel {v['max_rel']:.2e} -> {'PASS' if v['pass'] else 'FAIL'}")
    P_(f"ITEM 1 route agreement + known answers: {res['label_item1_route_agreement']}")
else:
    expect = {"M1": ["C1_tau"], "M2a": ["C1_P", "C1_tau", "C1_g"], "M2b": ["C1_P", "C1_tau", "C1_g"],
              "M3": ["C1_g", "C1_B"]}[ARM]
    per_seed = {}
    for r in res["rows"]:
        worst = max(max(r[k]) if isinstance(r[k], list) else r[k] for k in expect)
        per_seed[r["seed"]] = worst
    bites = all(v >= BITE for v in per_seed.values())
    res["mutate"] = {"checks_expected_to_fail": expect, "worst_per_seed": per_seed, "bites": bool(bites)}
    for k, v in checks.items():
        P_(f"{k}: max rel {v:.2e}")
    P_(f"MUTATE {ARM}: worst of {expect} per seed " + ", ".join(f"{s}: {v:.3g}" for s, v in per_seed.items())
       + f" -> {'BITES' if bites else 'DOES NOT BITE'}")

res["seconds"] = round(time.time() - t0, 1)
res["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
res["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
suffix = f"_MUTATE_{ARM}" if ARM else ""
with open(os.path.join(HERE, f"tpa1_cov{suffix}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
P_(f"runtime {res['seconds']} s, peak RSS {res['peak_rss_GB']} GB")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, f"tpa1_cov{suffix}.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.

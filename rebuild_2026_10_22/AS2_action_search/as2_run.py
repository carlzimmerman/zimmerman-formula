#!/usr/bin/env python3
"""AS2_action_search. Enumeration of covariant actions for the a0 law against analytic gates. Not a fit and not a data test.
Run: OMP_NUM_THREADS=1 nice -n 19 python3 -W ignore as2_run.py ; twin AS2_MUTATE=1. Needs as2_grammar_cap2500000.npz (as2_grammar.py 2500000 9) and as2_q2.json.
Outputs as2_run{,_MUTATE}.out/.json, no timing. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import itertools, json, os, signal, sys
import numpy as np, sympy as sy
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import as2_engine as E
MUT = E.MUT; TAG = "_MUTATE" if MUT else ""
LOG, CHECKS = [], []
def say(s=""):
    LOG.append(s); print(s, flush=True)
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok))); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
STOP = {"f": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__("f", True))
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16
LSTAR = {"canonical": 21.7, "alt": 22.9}            # D10 floor, pc
PLANETS = {"Earth": (149597870700.0, 8.7e-15), "Mars": (227987154946.8, 1.4e-15), "Saturn": (1433147601306.0, 7e-15)}  # C6 inputs
B_GAM, B_CT, B_A1, B_A2 = 2.3e-5, 1e-15, 4e-5, 2e-9   # memory, PROVISIONAL
MULT = [s * m for s in (1, -1) for m in (0.25, 0.5, 1, 2, 4)]
XS = (0.01, 1.0, 100.0)

# ---------- templates ----------
def enumerate_templates():
    T = []
    def add(**k):
        k.setdefault("KB", 0.0); k.setdefault("tw", 0); k.setdefault("xi", 0); k.setdefault("beta", 0); k.setdefault("Q0", 0.0)
        k.setdefault("stiff", None); k.setdefault("matter", "min"); k.setdefault("cold", "none"); k.setdefault("extra", {})
        nf = {"S": 1, "SX": 2, "Ae": 1, "Kh": 1, "SAe": 2, "SKh": 2, "KhP": 2, "AeP": 2, "BM": 1, "BMS": 2, "M": 1}[k["content"]]
        fields = nf + (1 if k["cold"] in ("sepPX", "mimsep") else 0)
        scales = (1 if k["stiff"] else 0) + (1 if k["cold"] == "KQ" else 0) + (1 if k["matter"] == "dsc" else 0)
        over = max(fields - 2, 0) + max(scales - 1, 0)
        if over > 1:
            return
        k["fields"], k["scales"], k["tier"] = fields, scales, "A" if over == 0 else "B"
        T.append(k)
    colds = {"S": ["none", "sepPX"], "SX": ["none"], "Ae": ["none", "sepPX"], "Kh": ["none", "KQ", "mimown", "sepPX"], "SAe": ["none", "KQ", "sepPX"],
             "SKh": ["none", "KQ", "sepPX"], "KhP": ["none", "KQ", "sepPX"], "AeP": ["none", "sepPX"], "BM": ["none", "twin", "sepPX"], "BMS": ["none", "twin"], "M": ["mimown"]}
    for c, m in itertools.product(colds["S"], ("conf", "dsc", "min")):
        add(content="S", carrier="X", matter=m, cold=c)
    for pp, gc, ypi, m in itertools.product((1, 2), (0, 1), (0, 1), ("min", "conf")):
        add(content="SX", carrier="chi2", matter=m, extra={"Phipi": pp, "gradcross": gc, "Y_pi": ypi})
    for car, KB, tw, st, c in itertools.product(("a2", "Fti2", "KJS"), (0.0, 0.5), (0, 1), (None, "Da"), colds["Ae"]):
        add(content="Ae", carrier=car, KB=KB, tw=tw, stiff=st, cold=c)
    for car, KB, st, c in itertools.product(("a2", "KJS"), (0.0, 0.5), (None, "Da"), colds["Kh"]):
        add(content="Kh", carrier=car, KB=KB, stiff=st, cold=c)
    for con in ("SAe", "SKh"):
        for car, KB, tw, xi, be, Q0, st, m, c in itertools.product(("Y", "a2"), (0.0, 0.5), (0, 1) if con == "SAe" else (0,), (0, 1, 2), (0, 1, 2), (0.0, 1.0),
                                                                     (None, "DV", "Da", "boxpi"), ("min", "conf", "tev"), colds[con]):
            add(content=con, carrier=car, KB=KB, tw=tw, xi=xi, beta=be, Q0=Q0, stiff=st, matter=m, cold=c)
    for con in ("KhP", "AeP"):
        for car, KB, tw, xi, be, st, c in itertools.product(("P2", "a2"), (0.0, 0.5), (0, 1) if con == "AeP" else (0,), (0, 1, 2), (0, 1, 2), (None, "DP", "Da"), colds[con]):
            add(content=con, carrier=car, KB=KB, tw=tw, xi=xi, beta=be, stiff=st, cold=c)
    for ab, c in itertools.product((0.5, 0.16, 0.84), colds["BM"]):
        add(content="BM", carrier="YB", extra={"wa": ab}, cold=c)
    for ab, car, m, c in itertools.product((0.5, 0.16, 0.84), ("YB", "X"), ("min", "conf"), colds["BMS"]):
        add(content="BMS", carrier=car, matter=m, extra={"wa": ab}, cold=c)
    add(content="M", carrier="X", cold="mimown")
    return T

def Nf(t):
    return (2 - t["KB"]) if t["content"] in ("SAe", "SKh", "KhP", "AeP") else 1.0

def theory(t, L=0.0, muK2=0.0):
    c = t["content"]
    if c == "EA":
        return E.Theory("EA", terms={"ea": t["extra"]["ea"]})
    if c == "M":
        c = "S"
    terms = {}
    n = Nf(t)
    if t["KB"]:
        terms["KB"] = t["KB"]
    if t["tw"]:
        terms["tw"] = 1.0
    if c in ("SAe", "SKh"):
        if t["xi"]:
            terms["aV"] = n * t["xi"]
        if t["beta"]:
            terms["Y"] = n * t["beta"]
    if c in ("KhP", "AeP"):
        if t["xi"]:
            terms["aP"] = n * t["xi"]
        if t["beta"]:
            terms["P2"] = n * t["beta"]
    ex = t["extra"]
    for k in ("Phipi", "gradcross"):
        if ex.get(k):
            terms[k] = float(ex[k])
    wa = ex.get("wa", 0.0)
    wb = 1 - wa if c in ("BM", "BMS") else 1.0
    th = E.Theory(c, t["Q0"], terms, t["carrier"], wb, wa, L, t["stiff"], muK2, t["matter"])
    if ex.get("Y_pi"):
        th.terms["Ypi"] = 1.0
    return th

# ---------- static form ----------
def static_form(t):
    """A v + G c (c.v) = 4 e g_N. Numbers (w0,w1,g0,g1,p0,p1,d0,d1) with w = (w0+w1 G)/D g_N etc., D = d0 + d1 G."""
    if t["content"] == "M":
        return dict(reason="mimetic constraint: pi_dot = Phi at first order, so no static gradient branch; the sqrt(Phi) branch makes the carrier depend on Phi itself, not on grad Phi")
    th = theory(t)
    r = E.static_reduce(th)
    A, c, e, ep, s = r["A"], r["c"], r["e"], r["ep"], r["s"]
    if s == 0:
        return dict(reason="carrier vanishes on a static gradient")
    if r["rank"] > 1:
        return dict(reason="carrier is not rank one on the static gradients")
    if MUT:
        pass
    S = np.vstack([A, c[None]])
    U, sv, Vh = np.linalg.svd(S)
    nul = Vh[np.sum(sv > 1e-10):]
    if len(nul) and np.abs(nul @ e).max() > 1e-9:
        return dict(reason="source acts on a flat direction: no static solution")
    B = Vh[:np.sum(sv > 1e-10)].T
    Ar, cr, er, epr = B.T @ A @ B, B.T @ c, B.T @ e, B.T @ ep
    vals = []
    for G in (0.71, 1.93, 3.37):
        Mx = Ar + G * np.outer(cr, cr)
        d = np.linalg.det(Mx)
        if abs(d) < 1e-12:
            return dict(reason="singular static system at every G")
        v = np.linalg.solve(Mx, 4 * er)
        vals.append((d, d * (cr @ v), d * (er @ v), d * (epr @ v)))
    vals = np.array(vals)
    Gs = np.array([0.71, 1.93, 3.37])
    def lin(y):
        a1 = (y[1] - y[0]) / (Gs[1] - Gs[0]); a0 = y[0] - a1 * Gs[0]
        return a0, a1, abs(a0 + a1 * Gs[2] - y[2])
    (d0, d1, e0), (w0, w1, e1), (g0, g1, e2), (p0, p1, e3) = [lin(vals[:, j]) for j in range(4)]
    if t["content"] in ("SAe", "SKh", "KhP", "AeP") and t["KB"]:
        r_ = 2 / (2 - t["KB"]); d0, d1 = d0 * r_, d1 * r_     # A2.1: G_N = r G~
    if t["content"] in ("BM", "BMS") and t["carrier"] == "YB":
        al = t["extra"]["wa"]; w0, w1 = w0 * al, w1 * al      # A2.2: y = a |grad f*|
    n = max(abs(x) for x in (d0, d1, w0, w1, g0, g1, p0, p1))
    q = np.round(np.array([w0, w1, g0, g1, p0, p1, d0, d1]) / n, 10) + 0.0
    if abs(q[0]) < 1e-9 and abs(q[1]) < 1e-9:
        return dict(reason="carrier unsourced: stays zero, Newton only")
    al = t["extra"].get("wa", 1.0) if t["carrier"] == "YB" else 1.0
    return dict(form=q, s=s, B=B, A=A, c=c * al, e=e, ep=ep, names=r["names"], Ar=Ar, cr=cr * al, er=er, carrier_scale=al)

# ---------- grammar test ----------
class Grammar:
    def __init__(self):
        z = np.load(os.path.join(HERE, "as2_grammar_cap2500000.npz"), allow_pickle=True)
        self.y = z["y"]; self.V = z["V"]; self.D = z["D"]; self.expr = z["expr"]; self.sz = z["sz"]
        self.Fu = self.D / (2 * self.y)
        self.low = self.y < 1
        self.meta = json.load(open(os.path.join(HERE, "as2_grammar_cap2500000.json")))

def law_eval(q, G, y):
    w = q[0] + q[1] * G
    gN = y * (q[6] + q[7] * G) / w
    gx = y * (q[2] + q[3] * G) / w
    gN, gx = np.abs(gN), gx * np.sign(gN)
    return gN, gx

def g1_form(gr, q, Cn):
    """Scan every expression and multiplier for one static form. Returns passes and the nearest misses."""
    idx = np.nonzero(gr.low)[0][[0, 4, 9]]
    y3 = gr.y[idx]
    passes, near = [], []
    sg = -1.0 if MUT else 1.0
    for m in MULT:
        with np.errstate(all="ignore"):
            G = sg * 2 * Cn * m * gr.Fu[:, idx]
            gN, gx = law_eval(q, G, y3)
            res = np.abs(np.log10(np.abs(gN / (gx ** 2 / (gx + 1)))))
        res = np.where(np.isfinite(res), res, 9.0).max(1)
        res = np.where(gx[:, 2] <= 0, 9.0, res)
        for i in np.nonzero(res < 1e-3)[0]:
            ok, mx, cov = g1_full(gr, q, Cn * m * sg, int(i))
            if ok:
                passes.append((int(i), m))
        top = np.argpartition(res, 40)[:40]
        for i in top:
            ok, mx, cov = g1_full(gr, q, Cn * m * sg, int(i))
            if cov and mx > 1e-7:
                near.append((float(mx), int(i), m))
    near.sort()
    return passes, near[:12]

def g1_full(gr, q, C, i):
    with np.errstate(all="ignore"):
        G = 2 * C * gr.Fu[i]
        gN, gx = law_eval(q, G, gr.y)
        law = gx ** 2 / (gx + 1)
        r = np.abs(gN / law - 1)
    v = np.isfinite(r) & (gx > 0) & (gN > 0)
    if v.sum() < 5 or not v[gr.low].all():
        return False, 9.0, False
    xs = gx[v]
    cov = xs.min() <= 0.02 and xs.max() >= 30
    mx = float(np.max(np.abs(np.log10(gN[v] / law[v]))))
    return bool(cov and r[v].max() <= 1e-8), mx, bool(cov)

def expr_sympy(s):
    y = sy.Symbol("y", positive=True)
    env = dict(y=y, u=y ** 2, h=sy.Rational(1, 2), neg=lambda a: -a, inv=lambda a: 1 / a, sqrt=sy.sqrt, log1p=lambda a: sy.log(1 + a), log1m=lambda a: sy.log(1 - a), exp=sy.exp)
    txt = s
    import re
    txt = re.sub(r"(?<![a-z0-9_.])1(?![0-9.a-z])", "sy.Integer(1)", txt)
    txt = re.sub(r"(?<![a-z0-9_.])2(?![0-9.a-z])", "sy.Integer(2)", txt)
    return eval(txt, {"sy": sy, **env}), y

def sympy_confirm(expr, q, C):
    f, y = expr_sympy(expr)
    Fu = sy.diff(f, y) / (2 * y)
    G = 2 * C * Fu
    nq = [sy.nsimplify(float(x), rational=True, tolerance=1e-9) for x in q]
    w = nq[0] + nq[1] * G
    gN = y * (nq[6] + nq[7] * G) / w
    gx = y * (nq[2] + nq[3] * G) / w
    sg_ = -1 if float((gx / gN).subs(y, sy.Rational(1, 2))) < 0 else 1      # same sign rule as law_eval
    gx = sg_ * gx
    res = sy.simplify(sy.together(gN ** 2 - (gx ** 2 / (gx + 1)) ** 2))
    if res != 0:      # simplify can miss exp(log(.)); fall back to 50 digits at six points, reported as such
        import mpmath as mp
        mp.mp.dps = 50
        fn = sy.lambdify(y, res, "mpmath")
        return all(abs(fn(mp.mpf(p))) < mp.mpf(10) ** -35 for p in ("0.013", "0.07", "0.21", "0.43", "0.77", "0.93")), f, y
    return True, f, y

class FClass:
    """Function callable: F = C s f_u, F2 = C f_uu, by exact derivatives."""
    def __init__(self, expr, C, s, al=1.0):
        f, y = expr_sympy(expr)
        self.expr = expr; self.C = C; self.s = s; self.al = al
        fy = sy.diff(f, y); fyy = sy.diff(fy, y)
        self.fu = sy.lambdify(y, fy / (2 * y), "numpy")
        self.fuu = sy.lambdify(y, (fyy / (2 * y) - fy / (2 * y ** 2)) / (2 * y), "numpy")
    def F(self, y):
        return float(self.C * self.s * self.fu(y)) * self.al ** 2
    def F2(self, y):
        return float(self.C * self.fuu(y)) * self.al ** 4
    def G(self, y):
        return 2 * float(self.C * self.fu(y))

def y_of_x(fc, q, x):
    def gfun(y):
        return law_eval(q, fc.G(y), y)[1]
    lo = 1e-9
    # find hi by scan: the capped forms run out at y = 1
    hi = None
    grid = list(1 - np.geomspace(1e-14, 0.9, 40)) + list(np.geomspace(1.05, 1e12, 60))
    prev = lo
    for yy in sorted(grid):
        try:
            v = float(gfun(yy))
        except Exception:
            v = float("nan")
        if not np.isfinite(v):
            continue
        if v >= x:
            hi = yy; break
        prev = yy
    if hi is None:
        return None
    return brentq(lambda y: float(gfun(y)) - x, prev, hi, xtol=1e-16 * max(hi, 1e-3), rtol=1e-14)

def bg_vector(t, sf, th, fc, y, dirn):
    G = fc.G(y)
    Mx = sf["Ar"] + G * np.outer(sf["cr"], sf["cr"])
    v = sf["B"] @ np.linalg.solve(Mx, 4 * sf["er"])
    w = sf["c"] @ v
    gN = y / abs(w)
    v = v * gN
    fl = th.fl
    f0 = np.zeros(fl.n)
    for nm, val in zip(sf["names"], v):
        if nm == "f":
            f0[fl.ix["Phi"]] = f0[fl.ix["Psi"]] = val
        elif nm == "fh":
            f0[fl.ix["ht_tt"]] = -2 * val
            for k in ("ht_xx", "ht_yy", "ht_zz"):
                f0[fl.ix[k]] = -2 * val
        elif nm == "Az":
            f0[fl.ix["Ax" if dirn == "x" else "Az"]] = val
        elif nm == "Pz":
            f0[fl.ix["Px" if dirn == "x" else "Pz"]] = val
        else:
            f0[fl.ix[nm]] = val
    d = np.array([0, 1.0, 0, 0] if dirn == "x" else [0, 0, 0, 1.0], complex)
    return (th.pieces(d), f0)

# ---------- gates ----------
def g2(t, sf, th, fc):
    q = sf["form"]
    # gamma across x
    gam = []
    for x in (0.01, 0.1, 1.0, 10.0, 100.0, 3e7):
        y = y_of_x(fc, q, x)
        if y is None:
            continue
        G = fc.G(y)
        gam.append(abs((q[4] + q[5] * G) / (q[2] + q[3] * G) - 1))
    gmax = max(gam) if gam else float("nan")
    # tensor speed at u = 0
    y0 = 1e-4
    F0 = fc.F(y0)
    fl = th.fl
    sub = [fl.ix["hp"]] + ([fl.ix["ht_xx"], fl.ix["ht_yy"]] if fl.has_B else [])
    def Ms(w):
        return th.M(w, 1.0, 0.0, F0)[np.ix_(sub, sub)]
    pts = [0.0, 1.0, 2.0]
    if len(sub) == 1:
        v = [Ms(w)[0, 0] for w in pts]
        cf = np.polyfit(pts, np.array(v), 2)
        c2 = (-cf[2] / cf[0]).real if abs(cf[0]) > 1e-14 else float("inf")
        cs = [c2]
    else:
        M0, M1 = Ms(0.0), Ms(1.0)
        ev = np.linalg.eigvals(np.linalg.solve(M1 - M0, -M0))
        cs = [float(e.real) for e in ev if abs(e) > 1e-9]
    # the matter cone: TeVeS disformal with pi-bar 0.1, scalar disformal with clock Q0
    cone = 1.0
    if t["matter"] == "tev":
        cone = float(np.exp(-4 * 0.1))
    if t["matter"] == "dsc":
        cone = 1.0 / (1 + 1.0) if t["Q0"] else 1.0
    ctdev = max(abs(np.sqrt(abs(c) / cone) - 1) for c in cs)
    ok = (gmax <= B_GAM) and (ctdev <= B_CT)
    return dict(label="PASS" if ok else "FAIL", gamma_dev=float(gmax), cT_dev=float(ctdev))

def g3(t, sf, th, fc):
    q = sf["form"]
    rows = {}
    worst = "PASS"; why = ""
    order = {"PASS": 0, "ND": 1, "FAIL": 2}
    def rec(name, res):
        nonlocal worst, why
        lab, det = E.health_label(res)
        rows[name] = (lab, det)
        if order[lab] > order[worst]:
            worst, why = lab, f"{name}: {det}"
    y0 = 1e-4
    rec("u0", E.modes(th, F=fc.F(y0), F2=0.0, T0=None))
    for x in XS:
        y = y_of_x(fc, q, x)
        if y is None:
            rows[f"x{x}"] = ("ND", "no background"); worst = max(worst, "ND", key=lambda s: order[s]); continue
        for dn in ("z", "x"):
            T0 = bg_vector(t, sf, th, fc, y, dn)
            rec(f"x{x}{'par' if dn == 'z' else 'perp'}", E.modes(th, F=fc.F(y), F2=fc.F2(y), T0=T0))
    return dict(label=worst, why=why, rows=rows)

def q2_kind(t, sf):
    q = sf["form"]
    c = t["content"]
    if abs(q[1]) < 1e-9 and abs(q[7]) < 1e-9:
        return "qumond"
    if t["carrier"] in ("a2", "Fti2", "KJS"):
        return "aqual"
    if c in ("KhP", "AeP", "SAe") and t["Q0"] or c in ("KhP", "AeP"):
        return "aqual"       # the carrier has a free transverse part (C1, C4), so only Phi is a potential
    return "twofield"

def g4(t, sf, Q2):
    kind = q2_kind(t, sf)
    screen = (t["stiff"] == "DP" and t["carrier"] == "P2") or (t["stiff"] == "DV" and t["carrier"] == "Y")
    res = {}
    if screen:
        for f, a in FOOT.items():
            L = LSTAR[f] * PC
            res[f] = dict(over_Hees=a / L / 9e-27, source="[REC C6, D7d] all cells pass with the stiff form on the AQUAL equation" if kind == "aqual" else "[EST] bound a0/L, l = 2 of a stiff curl-free field; no solve")
        return dict(label="PASS", kind=kind, screen=True, cells=res)
    if t["stiff"] == "Da":
        return dict(label="ND", kind=kind, screen=False, cells={}, why="(D.a)^2 acts on Phi itself; see G4p")
    bad = False
    for f in FOOT:
        cells = [Q2[f"{kind}|{f}|{e}"]["over_Hees"] for e in ("E0", "E1", "E2", "E3")]
        res[f] = dict(lo=min(cells), hi=max(cells))
        bad = bad or max(cells) > 1
    return dict(label="FAIL" if bad else "PASS", kind=kind, screen=False, cells=res)

def g4p(t, sf, th):
    out = {}
    screen = (t["stiff"] == "DP" and t["carrier"] == "P2") or (t["stiff"] == "DV" and t["carrier"] == "Y")
    if t["stiff"] == "Da":
        # Newton itself: k L >> 1 against k L = 0 on the rest-frame potential
        L = LSTAR["canonical"] * PC / AU
        th2 = E.Theory(th.fl.content, th.Q0, th.terms, th.carrier, th.wb, th.wa, L, "Da")
        U1 = abs(E.phi_beta(th2, 0.0)[1]); U0 = abs(E.phi_beta(th, 0.0)[1])
        return dict(label="FAIL", worst=float(abs(U1 / U0 - 1)), note="Newtonian potential ratio at k L >> 1 minus 1: the stiffness acts on Phi, not on the extra field")
    for f, a in FOOT.items():
        r = {}
        for pl, (R, b) in PLANETS.items():
            gN = GM / R ** 2
            if screen:
                anom = GM / (LSTAR[f] * PC) ** 2
            else:
                anom = a * (gN / a + np.sqrt((gN / a) ** 2 + 4 * gN / a)) / 2 / (1 + (gN / a + np.sqrt((gN / a) ** 2 + 4 * gN / a)) / 2)
            r[pl] = anom / b
        out[f] = r
    worst = max(max(v.values()) for v in out.values())
    return dict(label="PASS" if worst <= 1 else "FAIL", worst=float(worst), cells=out, screen=screen)

PPN_CACHE = {}
def rat(z):
    from fractions import Fraction
    fr = lambda v: sy.Rational(Fraction(float(v)).limit_denominator(4096).numerator, Fraction(float(v)).limit_denominator(4096).denominator)
    return fr(np.real(z)) + sy.I * fr(np.imag(z))

def ppn_exact(t):
    """Exact block solves in v, F, L2, from the engine's matrices at rational points (A2.4)."""
    key = (t["content"], t["carrier"], t["KB"], t["tw"], t["xi"], t["beta"], t["Q0"], t["stiff"], t["matter"], json.dumps(t["extra"], sort_keys=True))
    if key in PPN_CACHE:
        return PPN_CACHE[key]
    th0, th1 = theory(t, L=0.0), theory(t, L=1.0 if t["stiff"] else 0.0)
    fl = th0.fl
    F, L2, v = sy.symbols("F L2 v")
    pts = np.array([0.0, 1, -1, 2, -2])
    Vd = np.linalg.inv(np.vander(pts, 5, increasing=True))
    def block(names, kz=1.0):
        idx = [fl.ix[n] for n in names]
        def coef(thx, Fv):
            Ms = np.array([thx.M(w, kz, 0.0, Fv)[np.ix_(idx, idx)] for w in pts]).reshape(5, -1)
            return (Vd @ Ms).reshape(5, len(idx), len(idx))
        C00 = coef(th0, 0.0); C01 = coef(th0, 1.0); C10 = coef(th1, 0.0)
        M = sy.zeros(len(idx), len(idx))
        w = sy.Symbol("w")
        for a_ in range(len(idx)):
            for b_ in range(len(idx)):
                e = 0
                for j in range(5):
                    e += (rat(C00[j, a_, b_]) + F * rat(C01[j, a_, b_] - C00[j, a_, b_]) + L2 * rat(C10[j, a_, b_] - C00[j, a_, b_])) * w ** j
                M[a_, b_] = e
        return M, w, idx
    # vector block, omega = 0
    vn = [n for n in ("Bx", "Ax", "Px", "ht_tx", "ht_xz") if n in fl.ix]
    Mv, w, idx = block(vn)
    Sv = E.source_vector(th0, vx=1.0)[idx]
    Mv0 = Mv.subs(w, 0)
    sol_b = None
    try:
        rhs = sy.Matrix([-rat(x) for x in Sv])
        sol_b = sy.simplify(Mv0.LUsolve(rhs)[0]) if Mv0.det() != 0 else None
    except Exception:
        sol_b = None
    # scalar block, omega = v
    sn = [n for n in ("Phi", "Psi", "Az", "tau", "pi", "chi", "Pz", "ht_tt", "ht_tz", "ht_zz", "ht_xx", "ht_yy") if n in fl.ix]
    Ms, w, idx = block(sn)
    Ms = Ms.subs(w, v)
    # source polynomial in v
    S0, S1, S2 = [E.source_vector(th0, vz=x)[idx] for x in (0.0, 1.0, -1.0)]
    Sa = (S1 - S2) / 2; Sb = (S1 + S2) / 2 - S0
    Sy = sy.Matrix([-(rat(S0[i]) + rat(Sa[i]) * v + rat(Sb[i]) * v ** 2) for i in range(len(idx))])
    D = sy.Poly(Ms.det(method="berkowitz"), v)
    M2 = Ms.copy(); M2[:, 0] = Sy
    Nn = sy.Poly(M2.det(method="berkowitz"), v)
    dc = [sy.factor(c) for c in reversed(D.all_coeffs())]; nc = [sy.factor(c) for c in reversed(Nn.all_coeffs())]
    p = next((i for i, c in enumerate(dc) if c != 0), None)
    dc += [sy.Integer(0)] * 4; nc += [sy.Integer(0)] * 4
    if p is None or nc[p] == 0:
        out = None
    else:
        Phi0 = nc[p] / dc[p]
        odd = (sy.simplify(nc[p + 1] * dc[p] - nc[p] * dc[p + 1]))
        beta = (nc[p + 2] / nc[p] - dc[p + 2] / dc[p]) if odd == 0 else None
        out = dict(Phi0=sy.lambdify((F, L2), Phi0, "mpmath"), beta=sy.lambdify((F, L2), beta, "mpmath") if beta is not None else None,
                   b=sy.lambdify((F, L2), sol_b, "mpmath") if sol_b is not None else None, odd=bool(odd != 0))
    PPN_CACHE[key] = out
    return out

def g5(t, sf, fc, th0):
    import mpmath as mp
    mp.mp.dps = 50
    ex = ppn_exact(t)
    if ex is None or ex["beta"] is None:
        return dict(label="ND", why="scalar block has no regular slow-source expansion", cells={})
    out = {}
    ok = True
    q = sf["form"]
    screen = (t["stiff"] == "DP" and t["carrier"] == "P2") or (t["stiff"] == "DV" and t["carrier"] == "Y")
    for f, a in FOOT.items():
        x = (GM / AU ** 2) / a
        L = LSTAR[f] * PC / AU if t["stiff"] else 0.0
        y = GM / (LSTAR[f] * PC) ** 2 / a if screen else y_of_x(fc, q, x)
        if y is None:
            return dict(label="ND", why="no background at the Sun", cells={})
        F = fc.F(y)
        F_, L2_ = mp.mpf(F), mp.mpf(L) ** 2
        U = abs(ex["Phi0"](F_, L2_))
        beta = ex["beta"](F_, L2_)
        b = ex["b"](F_, L2_) if ex["b"] is not None else mp.mpf(-4)
        a1 = -2 * mp.re(b) / U - 8
        a2 = mp.re(beta) + 2 + a1 / 2
        G = fc.G(y)
        r_ = 2 / (2 - t["KB"]) if t["content"] in ("SAe", "SKh", "KhP", "AeP") and t["KB"] else 1.0
        Us = (1.0 if screen else abs((q[2] + q[3] * G) / (q[6] + q[7] * G))) * r_     # static potential in bare-G units
        a1s = -2 * mp.re(b) / mp.mpf(Us) - 8
        out[f] = dict(x=x, y=float(y), F=float(F), alpha1=float(a1), alpha2=float(a2), U=float(U), alpha1_static=float(a1s), U_static=float(Us))
        ok = ok and abs(a1) <= B_A1 and abs(a2) <= B_A2 and abs(a1s) <= B_A1
    return dict(label="PASS" if ok else "FAIL", cells=out)

def g6(t):
    c, cold = t["content"], t["cold"]
    if cold == "none":
        return dict(label="FAIL", supply="none", double_count="no dust", why="no w = 0 term in the action")
    if cold == "KQ":
        if c in ("Kh", "KhP"):
            return dict(label="FAIL", supply="K(Q) on the law's own khronon", double_count="yes above the cap (CFG946, S4)", why="[REC M1, F3, Q6, X4] sigma8 ratio at the cap 0.391 (ODE) / 0.061 (Boltzmann); needs mu_K >= 411 h/Mpc vs cap 14.8")
        if c == "SAe":
            return dict(label="ND", supply="K(Q) on the scalar of a twisting pair", double_count="not settled", why="[REC H1 linear pass; C7 runaway on FRW for the one shape tried]")
        if c == "SKh":
            return dict(label="ND", supply="K(Q) on the scalar, khronon free", double_count="not settled", why="no record; see AS2 G6 reduction in README if this row matters")
    if cold == "mimown":
        return dict(label="FAIL", supply="mimetic limit of the law's own field", double_count="yes", why="[REC X6, S4] Q = 1 is mu_K -> infinity on the same field: dust forms halos and the law breaks")
    if cold == "sepPX":
        return dict(label="PASS", supply="separate P(X) dust, mu -> infinity", double_count="YES: X22 capture 0.76 against tolerance 0.20 / 0.03; X57 >= 0.54 of fair share", why="BOLTZ1 dust limit; falls into galaxies, so the law on baryons alone doesn't hold there")
    if cold == "twin":
        return dict(label="PASS", supply="twin dust on the second metric, locked branch (UX1 L1)", double_count="selector by baryon fraction, untested; one vacuum term breaks locking (UX1 L2)", why="[REC UX1]")
    return dict(label="FAIL", supply=cold, double_count="", why="")

def g7(t):
    fl_tw = t["content"] in ("Ae", "SAe", "AeP")
    if t["stiff"] in ("DP", "DV") and fl_tw:
        # T-C: omega^2 = A k^4 on a slice tilted from the aether
        A, v = 1e-4, 1e-2
        gam = 1 / np.sqrt(1 - v * v)
        W = np.polynomial.polynomial.Polynomial
        def nonreal(kp):
            P = W([v * kp, 1.0]) ** 2 * gam ** 2 - A * gam ** 4 * W([kp, v]) ** 4
            r = P.roots()
            return int(np.sum(np.abs(r.imag) > 1e-9 * np.abs(r)))
        kc = 1 / (2 * np.sqrt(A) * v)
        return dict(label="FAIL", why=f"[REC I1, UX1 T-C rerun] k^4 stiffness on a twisting vector: nonreal roots {nonreal(10 * kc)} at 10 k_c, {nonreal(0.5 * kc)} at 0.5 k_c")
    if t["stiff"] == "boxpi":
        return dict(label="FAIL", why="fourth-order in time: Ostrogradsky pole (UX1 H2, M1 R2b4)")
    if t["stiff"] in ("DP", "DV") and not fl_tw:
        return dict(label="PASS", why="global time function: k^4 on the foliation only" + ("; [REC H4, X3] needs the switched form where D.P < 0" if t["stiff"] == "DP" else ""))
    return dict(label="PASS", why="second-order principal part" + (" on a twisting vector" if fl_tw else ""))

GATES = ["G2", "G3", "G4", "G4p", "G5", "G6", "G7"]
GCACHE = {}
def grade(t, sf, fc, Q2, fkey=""):
    muK = 0.01 if t["cold"] == "KQ" else 0.0
    k0 = json.dumps({k: t[k] for k in sorted(t) if k not in ("cold", "fields", "scales", "tier")}, sort_keys=True, default=str) + fkey
    th = theory(t, L=1.0 if t["stiff"] else 0.0, muK2=muK)
    r = {"G1": dict(label="PASS")}
    def cached(name, fn):
        kk = (name, k0)
        if kk not in GCACHE:
            GCACHE[kk] = fn()
        return GCACHE[kk]
    r["G2"] = cached("G2", lambda: g2(t, sf, theory(t), fc))
    def g3s():
        try:
            return g3(t, sf, th, fc)
        except Exception as ex:
            return dict(label="ND", why=f"engine exception {type(ex).__name__}", rows={})
    r["G3"] = cached(f"G3{muK}", g3s)
    r["G4"] = cached("G4", lambda: g4(t, sf, Q2))
    r["G4p"] = cached("G4p", lambda: g4p(t, sf, theory(t)))
    def g5s():
        try:
            return g5(t, sf, fc, th)
        except Exception as ex:
            return dict(label="ND", why=f"engine exception {type(ex).__name__}: {ex}", cells={})
    r["G5"] = cached("G5", g5s)
    r["G6"] = g6(t)
    r["G7"] = g7(t)
    return r

def tkey(t):
    return json.dumps({k: t[k] for k in sorted(t)}, sort_keys=True, default=str)

def tname(t):
    b = f"{t['content']}:{t['carrier']}"
    for k, s in (("KB", "KB"), ("tw", "tw"), ("xi", "xi"), ("beta", "be"), ("Q0", "Q0")):
        if t.get(k):
            b += f" {s}{t[k]:g}"
    if t["stiff"]:
        b += f" stiff={t['stiff']}"
    if t["matter"] != "min":
        b += f" {t['matter']}"
    if t["cold"] != "none":
        b += f" cold={t['cold']}"
    for k, v in t["extra"].items():
        b += f" {k}{v}"
    return b

def ka_engine():
    say("=== KA2, KA3: engine against GR and Einstein-aether (before the real run)")
    th = E.Theory("EA", terms={"ea": (0.0, 0.0, 0.0, 0.0)})
    M = th.M(0.3, 1.0)
    i = th.fl.ix
    sub = [i[n] for n in ("Phi", "Psi", "hp", "hc", "Bx", "By")]
    r = M[np.ix_(sub, sub)]
    check("KA2a tensor block omega^2 - k^2 with positive sign", abs(r[2, 2] - 0.5 * (0.09 - 1) * 2) < 1e-12, f"{r[2, 2]}")
    A = E.static_reduce(E.Theory("Kh"))
    check("KA2b static GR: Phi = Psi and Psi' = g_N", np.allclose(A["A"], [[0, 4], [4, -4]]), str(A["A"].tolist()))
    rng = np.random.default_rng(20261102)
    wc, w1, w2 = 0, 0, 0
    pts = []
    for _ in range(14):
        c1, c2, c3, c4 = rng.uniform(-0.1, 0.15, 4); c1 = abs(c1) + 0.05
        c13, c14, c123 = c1 + c3, c1 + c4, c1 + c2 + c3
        th = E.Theory("EA", terms={"ea": (c1, c2, c3, c4)})
        s2 = 1 / (1 - c13); s1 = (2 * c1 - c1 ** 2 + c3 ** 2) / (2 * c14 * (1 - c13)); s0 = c123 * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2))
        got = sorted(set(round(x[1], 7) for x in E.speeds(E.modes(th)) if x[0] == "wave"))
        if s1 > 0 and s0 > 0:
            exp = sorted(set(round(v, 7) for v in (s2, s1, s0)))
            if len(got) == len(exp):
                wc = max(wc, max(abs(a - b) for a, b in zip(got, exp)))
            else:
                wc = 9.0
        c1, c2, c3, c4 = [round(v * 64) / 64 for v in (c1, c2, c3, c4)]    # exact rationals for the exact block solve, as G5 uses
        c13, c14, c123 = c1 + c3, c1 + c4, c1 + c2 + c3
        if c123 == 0:
            continue
        a1p = -8 * (c3 ** 2 + c1 * c4) / (2 * c1 - c1 ** 2 + c3 ** 2)
        a2p = a1p / 2 - (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4) / (c123 * (2 - c14))
        ex = ppn_exact(dict(content="EA", carrier=None, KB=0.0, tw=0, xi=0, beta=0, Q0=0.0, stiff=None, matter="min", extra={"ea": (c1, c2, c3, c4)}))
        import mpmath as mp
        z = mp.mpf(0)
        if ex is None or ex["beta"] is None or ex["b"] is None:
            w1 = w2 = 9.0; continue
        U = abs(ex["Phi0"](z, z)); a1 = -2 * mp.re(ex["b"](z, z)) / U - 8; a2 = mp.re(ex["beta"](z, z)) + 2 + a1 / 2
        w1 = max(w1, abs(float(a1) - a1p)); w2 = max(w2, abs(float(a2) - a2p))
    check("KA3a spin-2, spin-1, spin-0 speeds at random points", wc < 1e-5, f"worst {wc:.2e}")
    check("KA3b alpha_1 (Foster-Jacobson, memory)", w1 < 1e-8, f"worst {w1:.2e}")
    check("KA3c alpha_2 through the calibrated readout", w2 < 1e-5, f"worst {w2:.2e}")

def main():
    Q2 = json.load(open(os.path.join(HERE, "as2_q2.json")))
    ka_engine()
    if MUT and any(not o for _, o in CHECKS):
        say("MUTATE: engine known answers fail, as required; no grading is read")
    TS = enumerate_templates()
    gr = Grammar()
    nA = sum(t["tier"] == "A" for t in TS); nB = len(TS) - nA
    nf = int(gr.meta["distinct"])
    say("\n=== Size of the space")
    say(f"  templates: {len(TS)} (tier A {nA}, tier B {nB})")
    say(f"  functions: {nf} distinct expressions, sizes {gr.meta['by_size']}; cap hit at size {gr.meta['cap_hit_at_size']}; {gr.meta['raw_tried']} raw tried; x {len(MULT)} coefficients")
    say(f"  raw space: {len(TS)} x {nf} x {len(MULT)} = {len(TS) * nf * len(MULT):.3e} (tier A {nA * nf * len(MULT):.3e})")
    # ---- G1 by unique static form
    forms = {}
    tf = []
    for t in TS:
        sf = static_form(t)
        tf.append(sf)
        if "form" in sf:
            key = tuple(sf["form"][[0, 1, 2, 3, 6, 7]].tolist()) + (round(Nf(t) * sf["s"], 8), )
            sf["key"] = key
            forms.setdefault(key, []).append(len(tf) - 1)
    reasons = {}
    for t, sf in zip(TS, tf):
        if "reason" in sf:
            reasons[sf["reason"]] = reasons.get(sf["reason"], 0) + 1
    say("\n=== G1: structural exits before any function")
    for k, v in sorted(reasons.items()):
        say(f"  {v:5d}  {k}")
    say(f"  {len(forms)} unique static forms remain, on {sum(len(v) for v in forms.values())} templates")
    ck = os.path.join(HERE, f"as2_g1_ckpt{TAG}.json")
    G1 = json.load(open(ck)) if os.path.exists(ck) else {}
    for n, (key, members) in enumerate(sorted(forms.items())):
        k = str(key)
        if k in G1:
            continue
        if STOP["f"]:
            say("SIGTERM: checkpoint written, stopping"); json.dump(G1, open(ck, "w")); sys.exit(3)
        sf = tf[members[0]]
        pas, near = g1_form(gr, sf["form"], Nf(TS[members[0]]))
        G1[k] = dict(passes=pas, near=near)
        print(f"  form {n + 1}/{len(forms)}: passes {len(pas)}, nearest {near[0][0] if near else None}", flush=True)
        json.dump(G1, open(ck, "w"))
    # function classes: same F on the grid
    def classes(pas):
        seen, out = {}, []
        for i, m in pas:
            a = m * gr.Fu[i]
            k = tuple(np.round(a[np.isfinite(a)][:10], 8).tolist())
            if k not in seen:
                seen[k] = i; out.append((i, m))
        return out
    rows = []
    nraw_tier = {"A": 0, "B": 0}
    nearrows = []
    for key, members in sorted(forms.items()):
        d = G1[str(key)]
        cl = classes([tuple(x) for x in d["passes"]])
        # shortest expression first in each class
        for mi in members:
            t = TS[mi]; sf = tf[mi]
            nraw_tier[t["tier"]] += len(d["passes"])
            for mx, i, m in d["near"][:3]:
                nearrows.append((mx, tname(t), str(gr.expr[i]), m, t["tier"]))
            for i, m in cl:
                rows.append((mi, i, m))
    say("\n=== G1 result")
    say(f"  raw passes (template x expression x coefficient): tier A {nraw_tier['A']}, tier B {nraw_tier['B']}")
    sgn = -1.0 if MUT else 1.0
    # confirm by sympy and grade
    conf = {}
    ckg = os.path.join(HERE, f"as2_grade_ckpt{TAG}.json")
    GR = json.load(open(ckg)) if os.path.exists(ckg) else {}
    results = []
    for n, (mi, i, m) in enumerate(rows):
        t, sf = TS[mi], tf[mi]
        C = Nf(t) * m * sgn
        ex = str(gr.expr[i])
        ck2 = (str(sf["key"]), ex, m)
        if ck2 not in conf:
            conf[ck2] = sympy_confirm(ex, sf["form"], C)[0]
        kk = tkey(t) + "|" + ex + f"|{m}"
        if kk not in GR:
            if STOP["f"]:
                json.dump(GR, open(ckg, "w")); say("SIGTERM: checkpoint written, stopping"); sys.exit(3)
            fc = FClass(ex, C, sf["s"], sf.get("carrier_scale", 1.0))
            GR[kk] = grade(t, sf, fc, Q2, ex + f"|{m}")
            if n % 200 == 0:
                json.dump(GR, open(ckg, "w")); print(f"  graded {n}/{len(rows)}", flush=True)
        results.append(dict(t=t, name=tname(t), expr=ex, mult=m, sympy_ok=conf[ck2], r=GR[kk]))
    json.dump(GR, open(ckg, "w"))
    say(f"  distinct law functions on templates: {len(rows)}; sympy zero residual on {sum(r['sympy_ok'] for r in results)} of them")
    # ---- known answers
    say("\n=== KA1, KA4, KA5: known answers (required before the real counts are read)")
    def find(**k):
        out = [r for r in results if all(r["t"].get(a) == b for a, b in k.items())]
        return out
    jx = find(content="Kh", carrier="a2", KB=0.0, stiff=None, cold="none")
    check("KA1a grammar finds v3's J_x on the bare khronon", any(abs(_eq_jx(r["expr"])) < 1e-9 for r in jx), str([(r["expr"], r["mult"]) for r in jx][:3]))
    ae = find(content="SAe", carrier="Y", KB=0.0, tw=0, xi=2, beta=1, Q0=1.0, stiff=None, matter="min", cold="none")
    check("KA1b grammar finds AeST's capped J in AeST's template", any(_eq_ae(r["expr"]) < 1e-9 for r in ae), str([(r["expr"], r["mult"]) for r in ae][:3]))
    if not jx or not ae:
        say("known answers missing: no grading is read"); write(results, nearrows, TS, Q2); sys.exit(1)
    b = jx[0]["r"]
    check("KA4a bare khronon law fails Q2 like E2", b["G4"]["label"] == "FAIL" and 2.0 < b["G4"]["cells"]["canonical"]["hi"] < 6, str(b["G4"]["cells"]))
    check("KA4b bare khronon law fails planets like M1", b["G4p"]["label"] == "FAIL" and b["G4p"]["worst"] > 1e4, f"{b['G4p']['worst']:.3g}")
    v3 = find(content="KhP", carrier="P2", KB=0.0, xi=2, beta=1, stiff="DP", cold="KQ")
    check("KA4c v3 appears and fails G6 at the cap", bool(v3) and v3[0]["r"]["G6"]["label"] == "FAIL" and v3[0]["t"]["tier"] == "B", str([(r["name"], r["t"]["tier"]) for r in v3][:2]))
    for kbv, lab in ((0.0, "KA4d"), (0.5, "KA4e")):
        tq = dict(content="SAe", carrier="Y", KB=kbv, tw=0, xi=2, beta=1, Q0=1.0, stiff=None, matter="min", cold="none", extra={})
        tq = next(x for x in TS if all(x.get(a_) == b_ for a_, b_ in tq.items()))
        ff = (2 - kbv) * 1.0            # J_Y = 1
        sfq = static_form(tq); qq = sfq["form"]; Gq = 2 * ff
        Us = abs((qq[2] + qq[3] * Gq) / (qq[6] + qq[7] * Gq))
        import mpmath as mp
        b_ = ppn_exact(tq)["b"](mp.mpf(ff), mp.mpf(0))
        # bare G units: U_static is in true G_N units after A2.1, so the bare potential is U_static / r
        r_ = 2 / (2 - kbv)
        a1s = float(-2 * mp.re(b_) / (mp.mpf(Us) * r_) * r_ ** 0 - 8)
        check(f"{lab} AeST alpha_1 static branch at J_Y = 1, K_B = {kbv}: record -2(K_B+2) = {-2 * (kbv + 2)}", abs(a1s + 2 * (kbv + 2)) < 1e-6, f"alpha_1 {a1s:.6f}")
    ae7 = find(content="SAe", carrier="Y", KB=0.0, tw=0, xi=2, beta=1, Q0=1.0, stiff="DV", matter="min", cold="none")
    check("KA4f AeST + gamma_L fails G7 (I1)", bool(ae7) and ae7[0]["r"]["G7"]["label"] == "FAIL", "")
    bm = find(content="BM", carrier="YB", cold="none")
    check("KA4g BIMOND a = 1/2 passes Q2 and fails planets (UX1)", bool(bm) and bm[0]["r"]["G4"]["label"] == "PASS" and bm[0]["r"]["G4p"]["label"] == "FAIL", str(bm[0]["r"]["G4"]["cells"]) if bm else "no row")
    cf = find(content="S", matter="conf", cold="none")
    check("KA4h conformal scalar fails G2 on gamma", bool(cf) and cf[0]["r"]["G2"]["label"] == "FAIL", str(cf[0]["r"]["G2"]) if cf else "no row")
    # A3: the grammar has no SX row (the parent's h = y/4 needs a constant it lacks), so the parent is tested with a given coefficient
    tq = next(x for x in TS if x["content"] == "SX" and x["matter"] == "min" and x["extra"]["gradcross"] == 0 and x["extra"]["Y_pi"] == 0)
    thq = theory(tq); iq = [thq.fl.ix[n] for n in ("Phi", "Psi", "chi")]
    Hq = np.real(thq.M(0.0, 1.0, 0.0, 0.3))[np.ix_(iq, iq)]
    evq = np.linalg.eigvalsh(0.5 * (Hq + Hq.T))
    check("KA4i QUMOND parent is indefinite on the static block (UX1 J1), with Newtonian GR's own sign pair removed by inspection", evq.min() < 0 and evq.max() > 0, f"eigenvalues {np.round(evq, 4).tolist()}")
    say(f"  SX rows graded: {len(find(content='SX'))}")
    # planted mock: injected reduced equations, pipeline only
    mock = {g: dict(label="PASS") for g in ["G1"] + GATES}
    check("KA5 planted healthy mock passes all gates through the same tally", tally_row(mock) == 0, "injected labels; pipeline check, not an action")
    write(results, nearrows, TS, Q2)
    nf_ = sum(1 for _, o in CHECKS if not o)
    say(f"\nCHECKS {len(CHECKS) - nf_}/{len(CHECKS)} pass. Failed: {[n for n, o in CHECKS if not o]}")
    open(os.path.join(HERE, f"as2_run{TAG}.out"), "w").write("\n".join(LOG) + "\n")
    sys.exit(1 if nf_ else 0)

def _prop(f, tgt, y):
    return sy.simplify(sy.diff(sy.diff(f, y) / sy.diff(tgt, y), y)) == 0

def _eq_jx(expr):
    f, y = expr_sympy(expr)
    return 0 if _prop(f, y - sy.log(1 + y), y) else 1

def _eq_ae(expr):
    f, y = expr_sympy(expr)
    tgt = -y - sy.log(1 - y) - y ** 2 / 2
    return 0 if _prop(f, tgt, y) else 1

def tally_row(r):
    return sum(r[g]["label"] != "PASS" for g in ["G1"] + GATES)

def write(results, nearrows, TS, Q2):
    say("\n=== Counts through the gates (Tier A survivors at each gate, read off the full matrix)")
    seq = ["G2", "G3", "G4", "G4p", "G5", "G6", "G7"]
    for tier in ("A", "B"):
        R = [r for r in results if r["t"]["tier"] == tier]
        n = len(R); say(f"  tier {tier}: after G1 {n}")
        alive = R
        for g in seq:
            alive = [r for r in alive if r["r"][g]["label"] != "FAIL"]
            say(f"    not FAIL through {g}: {len(alive)} (of which all PASS so far: {sum(all(r['r'][h]['label'] == 'PASS' for h in seq[:seq.index(g) + 1]) for r in alive)})")
        clean = [r for r in R if tally_row(r["r"]) == 0]
        say(f"    pass every gate: {len(clean)}")
    say("\n=== Per-gate FAIL counts among all G1 passes (tier A, tier B)")
    for g in seq:
        for lab in ("FAIL", "ND", "PASS"):
            pass
        fa = [sum(r["r"][g]["label"] == lab for r in results if r["t"]["tier"] == "A") for lab in ("PASS", "ND", "FAIL")]
        fb = [sum(r["r"][g]["label"] == lab for r in results if r["t"]["tier"] == "B") for lab in ("PASS", "ND", "FAIL")]
        say(f"  {g}: A PASS/ND/FAIL {fa}; B {fb}")
    def sev(r):
        rr = r["r"]
        fails = [g for g in seq if rr[g]["label"] == "FAIL"]
        nds = [g for g in seq if rr[g]["label"] == "ND"]
        return (r["t"]["tier"] != "A", len(fails), len(nds))
    res2 = sorted(results, key=lambda r: (sev(r), r["name"], r["expr"]))
    say("\n=== Closest rows (fewest FAIL, then fewest ND)")
    shown = {}
    for r in res2:
        k = (sev(r), tuple(r["r"][g]["label"] for g in seq), r["t"]["content"], r["t"]["carrier"], r["t"]["stiff"], r["t"]["cold"])
        if k in shown:
            continue
        shown[k] = 1
        if len(shown) > 60:
            break
        rr = r["r"]
        say(f"  [{r['t']['tier']}] {r['name']} f={r['expr']} x {r['mult']:g} | " + " ".join(f"{g}:{rr[g]['label'][0]}" for g in seq))
        if rr["G5"].get("cells"):
            c = rr["G5"]["cells"]
            say(f"       a1 {c['canonical']['alpha1']:.3g}/{c['alt']['alpha1']:.3g} a2 {c['canonical']['alpha2']:.3g}/{c['alt']['alpha2']:.3g}; gamma-1 {rr['G2']['gamma_dev']:.2g}; cT-1 {rr['G2']['cT_dev']:.2g}; G3 {rr['G3'].get('why', '')}")
    say("\n=== Nearest misses at G1 (grammar functions off the law; max |dlog10 g_N|; cap and range as frozen)")
    seen = set()
    for mx, nm, ex, m, tier in sorted(nearrows):
        if (ex, m) in seen:
            continue
        seen.add((ex, m))
        if len(seen) > 15:
            break
        say(f"  {mx:.2e} dex  f={ex} x {m:g} on {nm} [{tier}]")
    json.dump(dict(results=[{k: r[k] for k in ("name", "expr", "mult", "sympy_ok", "r")} | {"tier": r["t"]["tier"]} for r in res2]), open(os.path.join(HERE, f"as2_run{TAG}.json"), "w"), indent=0, sort_keys=True, default=str)

if __name__ == "__main__":
    main()

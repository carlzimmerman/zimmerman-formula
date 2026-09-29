"""u3_lib -- shared machinery of lane U3 (declared in U3_PREREGISTRATION.md).  Not a script; imported by u3_0 ... u3_2.

Contents: the runner (central two-loop run with the top threshold and the six variants), the crossing / self-consistency scale solvers, the 34 declared variants of the
13 principles and their residual functions, the T-BRIDGE solver, the matter-monotone test, and the J2 look-elsewhere formula.
Imports lane B's rg_common and N1's n1_lib READ-ONLY (path-relative); writes nothing; no bytecode.
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "B_rg_asymptotic_safety"))
sys.path.insert(0, os.path.join(HERE, "..", "N1_joint_couplings"))
sys.path.insert(0, os.path.join(HERE, "..", "D_calibration_bar"))
import rg_common as RGC          # lane B, read only
import n1_lib as N1              # lane N1, read only

PI = math.pi
TWO_PI = 2 * PI
MZ = N1.MZ
MT = N1.MT
XP = N1.MPL                      # 1.220890e19 GeV (un-reduced Planck mass)
XR = RGC.MPL_RED                 # 2.435e18 GeV
N_SM = 118
XS = XR / math.sqrt(N_SM)
TEV = 1000.0
ALPHA_INV0 = 137.035999177
SET_A, SET_B = N1.SET_A, N1.SET_B
B_SM = np.array([41 / 6, -19 / 6, -7.0])                   # (b_Y, b_2, b_3)
DB_TOP = np.array([17 / 18, 1 / 2, 2 / 3])                 # top contribution removed between m_Z and m_t
DB_MULT = np.array([4 / 3, 2 / 3, 2 / 3])                  # T-BRIDGE multiplets: Y=1 Dirac singlet, Y=0 SU(2) vector-like doublet, Y=0 colour vector-like triplet
LN_SPAN = math.log(100.0)
VARIANTS_RUN = ["2L-T", "2L-A", "2L-B", "2L-TB", "1L-T", "1L-A", "1L-B"]
LNMAX = math.log(1e40)
N_TRIALS = 34


def boundaries(inp):
    return np.array(N1.boundaries(inp), dtype=float)


# ------------------------------------------------------------------------------------------------ the runner
class Traj:
    """A(mu) = (a_Y, a_2, a_3) at scale mu (GeV), a_i = 1/alpha_i, Y normalisation (Q = T3 + Y).  name in VARIANTS_RUN."""

    def __init__(self, name, mutate_b=False, inp=None):
        self.name = name
        self.loops = int(name[0])
        code = name.split("-")[1]
        self.inp = inp if inp is not None else (SET_B if "B" in code else SET_A)
        self.thr = "T" in code
        self.a0 = boundaries(self.inp)
        self.b = B_SM.copy()
        if mutate_b:
            self.b[0] = 0.6 * (0.6 * 41 / 6)               # lane-A bug pattern: b_Y = (3/5) b_1 with b_1 = (3/5) b_Y
        self._seg = None
        self.lnmax = LNMAX
        if self.loops == 2:
            self._integrate()

    def _integrate(self):
        R = N1.Runner()
        R.b = self.b.copy()
        R.b1 = 0.6 * R.b[0]
        segs = []
        if self.thr:
            Rl = N1.Runner()
            Rl.b = self.b - DB_TOP
            Rl.b1 = 0.6 * Rl.b[0]
            s1 = solve_ivp(lambda t, y: Rl._rhs(t, y), [math.log(MZ), math.log(MT)], list(self.a0) + [0.0], rtol=1e-10, atol=1e-12, dense_output=True)
            segs.append((math.log(MZ), math.log(MT), s1))
            y0 = list(s1.y[:3, -1]) + [N1.YT_MT]
            l0 = math.log(MT)
        else:
            y0 = list(self.a0) + [R.yt_at_mz(self.inp)]
            l0 = math.log(MZ)

        def stop(t, y):
            return y[0] - 1.0
        stop.terminal = True
        stop.direction = -1
        s2 = solve_ivp(lambda t, y: R._rhs(t, y), [l0, LNMAX], y0, rtol=1e-10, atol=1e-12, dense_output=True, events=stop)
        segs.append((l0, float(s2.t[-1]), s2))
        self._seg = segs
        self.lnmax = float(s2.t[-1])

    def A(self, mu):
        lm = math.log(mu)
        if lm > self.lnmax + 1e-9:
            raise ValueError("mu above the integrated range")
        if self.loops == 1:
            if self.thr:
                if mu <= MT:
                    return self.a0 - (self.b - DB_TOP) / TWO_PI * math.log(max(mu, MZ) / MZ)
                return self.a0 - (self.b - DB_TOP) / TWO_PI * math.log(MT / MZ) - self.b / TWO_PI * math.log(mu / MT)
            return self.a0 - self.b / TWO_PI * math.log(max(mu, MZ) / MZ)
        for (l0, l1, sol) in self._seg:
            if lm <= l1 + 1e-12:
                return np.array(sol.sol(max(lm, l0))[:3])
        return np.array(self._seg[-1][2].sol(lm)[:3])


class Shifted:
    """Trajectory with N = (N_Y, N_2, N_3) unforced multiplets at 1 TeV: a_i -> a_i - N_i (Delta b_i / 2 pi) ln(mu / 1 TeV) for mu > 1 TeV."""

    def __init__(self, traj, N):
        self.t = traj
        self.N = np.zeros(3) if N is None else np.array(N, dtype=float)
        self.lnmax = traj.lnmax

    def A(self, mu):
        a = self.t.A(mu)
        if mu > TEV:
            a = a - self.N * DB_MULT / TWO_PI * math.log(mu / TEV)
        return a

    def b(self):
        return B_SM + self.N * DB_MULT


_TRAJ_CACHE = {}


def get_traj(name):
    if name not in _TRAJ_CACHE:
        _TRAJ_CACHE[name] = Traj(name)
    return _TRAJ_CACHE[name]


# ------------------------------------------------------------------------------------------------ couplings and scale solvers
def coup(A, key):
    return {"aY": A[0], "a1": 0.6 * A[0], "a2": A[1], "a3": A[2]}[key]


def solve_cross(sh, k1, k2, lo=MZ * 1.001, hi=None, ngrid=800):
    """First mu > lo where coup(k1) - coup(k2) changes sign (scan on a log grid, then brentq).  Returns mu or None."""
    hi = hi if hi is not None else math.exp(sh.lnmax - 1e-6)
    xs = np.linspace(math.log(lo), math.log(hi), ngrid)
    f = lambda lm: coup(sh.A(math.exp(lm)), k1) - coup(sh.A(math.exp(lm)), k2)
    prev = f(xs[0])
    for i in range(1, len(xs)):
        cur = f(xs[i])
        if prev == 0.0:
            return math.exp(xs[i - 1])
        if prev * cur < 0:
            return math.exp(brentq(f, xs[i - 1], xs[i], xtol=1e-13))
        prev = cur
    return None


def solve_hetero(sh, coeff=0.216):
    """X = coeff * g_str * M_red, g_str^2 = 4 pi / a_2(X)  (recalled tree-level heterotic relation, U3_PREREGISTRATION P13)."""
    f = lambda lm: math.exp(lm) - coeff * math.sqrt(4 * PI / sh.A(math.exp(lm))[1]) * XR
    try:
        return math.exp(brentq(f, math.log(1e14), math.log(min(1e20, math.exp(sh.lnmax - 1e-6)))))
    except ValueError:
        return None


# ------------------------------------------------------------------------------------------------ the 34 variants
def mkv(pid, label, xspec, params=None, kind="rel", fixes_alpha=False, param_scale=False, phi=False, note=""):
    return dict(id=None, pid=pid, label=label, xspec=xspec, params=params or {}, kind=kind, fixes_alpha=fixes_alpha, param_scale=param_scale, phi=phi, note=note)


def make_variants():
    V = []
    for tag, X in (("X_P", XP), ("X_S", XS)):
        V.append(mkv("P01", f"Dual-Coxeter 4 pi h, {tag}", ("fixed", X), kind="abs", fixes_alpha=True, param_scale=(tag == "X_S")))
    for h, g in ((5, "SU(5)"), (8, "SO(10)"), (12, "E6")):
        V.append(mkv("P02", f"GUT crossing a_1=a_2, a_3=a_2, a_2=4 pi h ({g})", ("cross", "a1", "a2"), dict(h=h), kind="mix"))
    for norm in ("GUT", "Y"):
        for tag, X in (("X_P", XP), ("X_R", XR), ("X_S", XS)):
            V.append(mkv("P03", f"Equal couplings {norm} norm, {tag}", ("fixed", X), dict(norm=norm), param_scale=(tag == "X_S"), phi=(norm == "Y" and tag != "X_S")))
    for pair in (("aY", "a2"), ("a2", "a3"), ("aY", "a3")):
        V.append(mkv("P04", f"Y-norm universality at the {pair[0]}={pair[1]} crossing", ("cross", pair[0], pair[1]), dict(pair=pair)))
    for n in (2, 3):
        for tag, X in (("X_P", XP), ("X_S", XS)):
            V.append(mkv("P05", f"a_Y/a_2 = {n}, a_3 = a_2, {tag}", ("fixed", X), dict(n=n), param_scale=(tag == "X_S")))
    for tag, X in (("X_P", XP), ("X_S", XS)):
        V.append(mkv("P06", f"Equal |log-derivative|, {tag}", ("fixed", X), param_scale=(tag == "X_S")))
    for norm in ("Y", "GUT"):
        for tag, X in (("X_P", XP), ("X_S", XS)):
            V.append(mkv("P07", f"Sum b_i a_i = 0 ({norm} norm), {tag}", ("fixed", X), dict(norm=norm), param_scale=(tag == "X_S")))
    V.append(mkv("P08", "RG invariant I = 0 (scale-free)", ("none",)))
    for N in (118, 126):
        V.append(mkv("P09", f"Emergence of all three at M_red/sqrt({N})", ("fixed", XR / math.sqrt(N)), dict(N=N), kind="abs", fixes_alpha=True, param_scale=True))
    for tag, X in (("X_S", XS), ("X_R", XR)):
        V.append(mkv("P10", f"a_Y=0, a_2=8 pi, a_3=12 pi, {tag}", ("fixed", X), kind="abs", fixes_alpha=True, param_scale=(tag == "X_S")))
    for c, cl in ((TWO_PI, "2 pi"), (2 * TWO_PI, "4 pi")):
        V.append(mkv("P11", f"Anomaly index a_i = {cl} I_i, X_P", ("fixed", XP), dict(c=c), kind="abs", fixes_alpha=True))
    for tag, X in (("X_P", XP), ("X_S", XS)):
        V.append(mkv("P12", f"'t Hooft universality a_1:a_2:a_3 = 5:2:3, {tag}", ("fixed", X), param_scale=(tag == "X_S")))
    V.append(mkv("P13", "Heterotic string-scale locking (recalled 0.216 g M_red)", ("hetero",)))
    for i, v in enumerate(V):
        v["id"] = f"V{i + 1:02d}"
    return V


def ratio_res(actual, target):
    """r = target / actual - 1 (huge if the actual ratio is not positive)."""
    if not (actual > 0):
        return 1e3
    return target / actual - 1.0


def invariant(a_gut, b_gut):
    b1, b2, b3 = b_gut
    a1, a2, a3 = a_gut
    terms = [(b2 - b3) * a1, (b3 - b1) * a2, (b1 - b2) * a3]
    return sum(terms), sum(abs(t) for t in terms)


def find_scale(v, sh, xfac=1.0):
    xs = v["xspec"]
    if xs[0] == "fixed":
        return xs[1] * xfac
    if xs[0] == "cross":
        return solve_cross(sh, xs[1], xs[2])
    if xs[0] == "hetero":
        return solve_hetero(sh)
    if xs[0] == "none":
        return None
    raise ValueError(xs)


def residuals(v, sh, ref=None, xfac=1.0, mu_eval=None):
    """Evaluate variant v on the (possibly content-shifted) trajectory sh.  Returns dict(X, r, names, A, pred).  r is None if the scale does not exist.
    ref: reference SM-desert couplings at X used to normalise absolute residuals (default: computed from sh with N = 0)."""
    pid, p = v["pid"], v["params"]
    b = sh.b() if isinstance(sh, Shifted) else B_SM
    X = find_scale(v, sh, xfac)
    if pid == "P08":
        mu = TEV if mu_eval is None else mu_eval
        A = sh.A(mu)
        bb = b if mu >= TEV else B_SM
        bg = (0.6 * bb[0], bb[1], bb[2])
        ag = (0.6 * A[0], A[1], A[2])
        Iv, S = invariant(ag, bg)
        return dict(X=mu, r=np.array([Iv / S]), names=["I/S"], A=A, pred=None)
    if X is None:
        return dict(X=None, r=None, names=[], A=None, pred=None)
    if math.log(X) > sh.lnmax:
        return dict(X=X, r=None, names=[], A=None, pred=None)
    A = sh.A(X)
    aY, a2, a3 = A
    a1 = 0.6 * aY
    if ref is None:
        base = sh.t if isinstance(sh, Shifted) else sh
        ref = base.A(X)
    pred = None
    if pid == "P01":
        pred = np.array([(5 / 3) * 4 * PI * 5, 4 * PI * 2, 4 * PI * 3])
        r, names = (pred - A) / ref, ["a_Y", "a_2", "a_3"]
    elif pid == "P02":
        h = p["h"]
        r = np.array([ratio_res(a3 / a2, 1.0), (4 * PI * h - a2) / ref[1]])
        names = ["a_3/a_2", "a_2=4pi h"]
    elif pid == "P03":
        aa = a1 if p["norm"] == "GUT" else aY
        r = np.array([ratio_res(aa / a2, 1.0), ratio_res(a3 / a2, 1.0)])
        names = ["a_ab/a_2", "a_3/a_2"]
    elif pid == "P04":
        i, j = p["pair"]
        third = ({"aY", "a2", "a3"} - {i, j}).pop()
        r = np.array([ratio_res(coup(A, third) / coup(A, i), 1.0)])
        names = [f"{third}/{i}"]
    elif pid == "P05":
        r = np.array([ratio_res(aY / a2, float(p["n"])), ratio_res(a3 / a2, 1.0)])
        names = ["a_Y/a_2=n", "a_3/a_2"]
    elif pid == "P06":
        rate = np.abs(b) / A
        r = np.array([ratio_res(rate[1] / rate[0], 1.0), ratio_res(rate[2] / rate[0], 1.0)])
        names = ["rate_2/rate_Y", "rate_3/rate_Y"]
    elif pid == "P07":
        if p["norm"] == "Y":
            bb, aa = b, A
        else:
            bb, aa = np.array([0.6 * b[0], b[1], b[2]]), np.array([a1, a2, a3])
        F = float(np.sum(bb * aa))
        S = float(np.sum(np.abs(bb * aa)))
        r, names = np.array([F / S]), ["sum b a / sum|b a|"]
    elif pid == "P09":
        r, names = (np.zeros(3) - A) / ref, ["a_Y=0", "a_2=0", "a_3=0"]
        pred = np.zeros(3)
    elif pid == "P10":
        pred = np.array([0.0, 8 * PI, 12 * PI])
        r, names = (pred - A) / ref, ["a_Y=0", "a_2=8pi", "a_3=12pi"]
    elif pid == "P11":
        pred = p["c"] * np.array([10.0, 6.0, 6.0])
        r, names = (pred - A) / ref, ["a_Y", "a_2", "a_3"]
    elif pid == "P12":
        r = np.array([ratio_res(a1 / a2, 2.5), ratio_res(a3 / a2, 1.5)])
        names = ["a_1/a_2=5/2", "a_3/a_2=3/2"]
    elif pid == "P13":
        r = np.array([ratio_res(a1 / a2, 1.0), ratio_res(a3 / a2, 1.0)])
        names = ["a_1/a_2", "a_3/a_2"]
    elif pid == "SYN":                       # synthetic rule used only by the controls of u3_1_score.py
        pred = np.array(p["pred"], dtype=float)
        r, names = (pred - A) / ref, ["a_Y", "a_2", "a_3"]
    else:
        raise ValueError(pid)
    return dict(X=X, r=np.asarray(r, dtype=float), names=names, A=A, pred=pred)


# ------------------------------------------------------------------------------------------------ bands and the joint test
def evaluate_bands(v, floor=0.01, extra_mu_eval=(MZ, 1e5, 1e10, 1e15, XP)):
    """T-JOINT: returns dict(central residuals, band, tol, pass, per-variant residuals).  Under a variant where the scale does not exist the residual is recorded as None."""
    cen_t = get_traj("2L-T")
    cen = residuals(v, Shifted(cen_t, None))
    out = dict(X=cen["X"], names=cen["names"], A=cen["A"], pred=cen["pred"], cen_r=None if cen["r"] is None else cen["r"].copy(), runs={}, exists=cen["r"] is not None)
    if cen["r"] is None:
        return out
    rr = {}
    for name in VARIANTS_RUN:
        res = residuals(v, Shifted(get_traj(name), None))
        rr[name] = None if res["r"] is None else res["r"]
    if v["param_scale"]:
        for xf in (0.5, 2.0):
            res = residuals(v, Shifted(cen_t, None), xfac=xf)
            rr[f"X x{xf}"] = res["r"]
    if v["pid"] == "P08":
        for mu in extra_mu_eval:
            for name in ("2L-T",):
                res = residuals(v, Shifted(get_traj(name), None), mu_eval=mu)
                rr[f"mu_eval={mu:.0e}"] = res["r"]
    out["runs"] = {k: (None if x is None else x.tolist()) for k, x in rr.items()}
    K = len(cen["r"])
    band = np.zeros(K)
    for k, x in rr.items():
        if x is None:
            continue
        band = np.maximum(band, np.abs(x - cen["r"]))
    out["band"] = band
    out["tol"] = np.maximum(2 * band, floor)
    out["pass_k"] = np.abs(cen["r"]) <= out["tol"]
    out["pass"] = bool(np.all(out["pass_k"]))
    return out


def look_elsewhere(n_trials, tols):
    lam = n_trials * float(np.prod([min(1.0, 2 * t / LN_SPAN) for t in tols]))
    return lam, 1 - math.exp(-lam)


def mono_kill(v, ev):
    """T-MONO: an absolute rule predicting a_j ABOVE the SM-desert run beyond tol cannot be repaired by added matter."""
    if v["kind"] not in ("abs", "mix") or ev["cen_r"] is None:
        return False, []
    hits = []
    for k, name in enumerate(ev["names"]):
        absolute = v["kind"] == "abs" or (v["pid"] == "P02" and k == 1)
        if absolute and ev["cen_r"][k] > ev["tol"][k]:
            hits.append(name)
    return bool(hits), hits


def bridge(v, tol_pass=1e-6):
    """T-BRIDGE: minimal (N_Y, N_2, N_3) >= 0 with all residuals zero (central run).  Returns dict(feasible, N, sumN, maxres)."""
    cen_t = get_traj("2L-T")
    base = residuals(v, Shifted(cen_t, None))
    if base["r"] is None:
        return dict(feasible=False, N=None, sumN=None, maxres=None, reason="scale does not exist")
    refA = base["A"]

    def rvec(N):
        res = residuals(v, Shifted(cen_t, N), ref=refA)
        if res["r"] is None:
            return np.full(len(base["r"]), 1e3)
        return res["r"]

    K = len(base["r"])
    best = None
    starts = [np.array(s, dtype=float) for s in ([0.2, 0.2, 0.2], [1, 1, 1], [3, 3, 3], [8, 8, 8], [0.5, 0.0, 0.0], [0.0, 0.5, 0.5], [6, 0.5, 0.5], [0.5, 6, 6], [15, 15, 15])]
    for s0 in starts:
        try:
            cons = [dict(type="eq", fun=(lambda N, k=k: rvec(N)[k])) for k in range(K)]
            sol = minimize(lambda N: float(np.sum(N)), s0, method="SLSQP", bounds=[(0, 200)] * 3, constraints=cons, options=dict(maxiter=400, ftol=1e-13))
            N = np.clip(sol.x, 0, None)
            mr = float(np.max(np.abs(rvec(N))))
            if mr < tol_pass and (best is None or N.sum() < best["sumN"]):
                best = dict(feasible=True, N=N.tolist(), sumN=float(N.sum()), maxres=mr)
        except Exception:
            continue
    if best is None:
        return dict(feasible=False, N=None, sumN=None, maxres=None, reason="no non-negative solution found (multi-start SLSQP)")
    return best

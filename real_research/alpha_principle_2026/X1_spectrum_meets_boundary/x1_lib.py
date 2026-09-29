"""x1_lib -- shared machinery of lane X1 (declared in X1_PREREGISTRATION.md).  Not a script; imported by x1_0 ... x1_3.

Contents: (1) the general one- and two-loop coefficient builder for the SM gauge group from a field list (exact Fractions -> floats), (2) a runner that generalises lane U3's
(the same top threshold, the same seven variants) with exotic-state thresholds in both b and B, (3) the boundary rules of the pre-registration and their residuals (U3's definitions),
(4) scale solvers, the U3 T-JOINT scorer, T-MONO / T-DOMAIN / T-ABS, the inequality checks, the excess arithmetic, and the interface to lane D's bar.
Imports lanes B, N1, U3 and D READ-ONLY (path-relative); writes nothing; no bytecode.
"""
import sys
sys.dont_write_bytecode = True
import os
import math
from fractions import Fraction as Fr
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import rg_common as RGC          # lane B, read only
import n1_lib as N1              # lane N1, read only
import u3_lib as U3              # lane U3, read only

PI = math.pi
TWO_PI = 2 * PI
MZ, MT = N1.MZ, N1.MT
XP, XR = U3.XP, U3.XR
ALPHA_INV0 = 137.035999177
DELTA0_MZ = RGC.DELTA_0_MZ       # 9.106, measured hadronic-inclusive offset
SET_A, SET_B = N1.SET_A, N1.SET_B
YT_MT = N1.YT_MT
DB_TOP = np.array([17 / 18, 1 / 2, 2 / 3])
VARIANTS = ["2L-T", "2L-A", "2L-B", "2L-TB", "1L-T", "1L-A", "1L-B"]
LN_SPAN = math.log(100.0)
TEV = 1000.0
FLOOR_D, FLOOR_H = 1000.0, 100.0          # recalled collider floors (colour triplet, charged doublet), GeV
LNCAP_DEFAULT = math.log(3 * XP)
N_TRIALS_TOTAL = 81

# ------------------------------------------------------------------------------------------------ group theory (exact)
T3TAB = {1: Fr(0), 3: Fr(1, 2), 8: Fr(3)}
T2TAB = {1: Fr(0), 2: Fr(1, 2), 3: Fr(2)}
C3TAB = {1: Fr(0), 3: Fr(4, 3), 8: Fr(3)}
C2TAB = {1: Fr(0), 2: Fr(3, 4), 3: Fr(2)}
CA = (Fr(0), Fr(2), Fr(3))


def contrib(kind, d3, d2, Y):
    """One irreducible multiplet (kind 'w' = Weyl fermion, 's' = complex scalar) of SU(3) x SU(2) x U(1)_Y (Q = T3 + Y).  Returns (db[3], dB[3][3]) as Fractions in the
    (Y, 2, 3) basis with couplings (g_Y, g_2, g_3):  db_i = f_b T_i ;  dB_ij = T_i (f_B C_j + f_A C_A(i) delta_ij).  Weyl: (2/3, 2, 10/3); complex scalar: (1/3, 4, 2/3)."""
    Y = Fr(Y)
    T = (Y * Y * d3 * d2, T2TAB[d2] * d3, T3TAB[d3] * d2)
    C = (Y * Y, C2TAB[d2], C3TAB[d3])
    fb, fB, fA = (Fr(2, 3), Fr(2), Fr(10, 3)) if kind == "w" else (Fr(1, 3), Fr(4), Fr(2, 3))
    db = [fb * T[i] for i in range(3)]
    dB = [[T[i] * (fB * C[j] + (fA * CA[i] if i == j else 0)) for j in range(3)] for i in range(3)]
    return db, dB


def gauge_bB():
    b = [Fr(0), Fr(-22, 3), Fr(-11)]
    B = [[Fr(0)] * 3 for _ in range(3)]
    B[1][1] = Fr(-34, 3) * CA[1] ** 2
    B[2][2] = Fr(-34, 3) * CA[2] ** 2
    return b, B


SM_GEN = [(3, 2, Fr(1, 6)), (3, 1, Fr(-2, 3)), (3, 1, Fr(1, 3)), (1, 2, Fr(-1, 2)), (1, 1, Fr(1)), (1, 1, Fr(0))]     # Q, uc, dc, L, ec, nuR (Weyl)
SM_HIGGS = (1, 2, Fr(1, 2))


def add_bB(acc, db, dB, mult=1):
    for i in range(3):
        acc[0][i] += mult * db[i]
        for j in range(3):
            acc[1][i][j] += mult * dB[i][j]


def sm_bB_exact(gens=3):
    """(b, B) of the SM (gauge + 3 generations of Weyl fermions incl. nu_R + one complex Higgs doublet) in the Y normalisation, exact Fractions."""
    b0, B0 = gauge_bB()
    acc = [list(b0), [list(r) for r in B0]]
    for (d3, d2, Y) in SM_GEN:
        db, dB = contrib("w", d3, d2, Y)
        add_bB(acc, db, dB, gens)
    db, dB = contrib("s", *SM_HIGGS)
    add_bB(acc, db, dB, 1)
    return acc[0], acc[1]


def to_float(b, B):
    return np.array([float(x) for x in b]), np.array([[float(x) for x in r] for r in B])


B_SM_F, BM_SM_F = to_float(*sm_bB_exact())
# Yukawa (top only) coefficients in the Y normalisation: C_Y = (5/3) C_1 with C_1 = 17/10 (lane N1, recalled)
CY_TOP = np.array([5 / 3 * 17 / 10, 3 / 2, 2.0])


def exotic_bB(exotics):
    """exotics: list of (mass, kind, d3, d2, Y, mult).  Returns list of (mass, db float[3], dB float[3][3])."""
    out = []
    for (m, kind, d3, d2, Y, mult) in exotics:
        db, dB = contrib(kind, d3, d2, Y)
        out.append((float(m), np.array([float(mult * x) for x in db]), np.array([[float(mult * x) for x in r] for r in dB])))
    return out


def exotics_e6(MD, MH, n27):
    """The exotic Weyl multiplets of n27 copies of the E6 27 (D, D^c at MD; the two doublets at MH); the neutral singlet S has no gauge charge and is omitted."""
    return [(MD, "w", 3, 1, Fr(-1, 3), n27), (MD, "w", 3, 1, Fr(1, 3), n27), (MH, "w", 1, 2, Fr(1, 2), n27), (MH, "w", 1, 2, Fr(-1, 2), n27)]


# ------------------------------------------------------------------------------------------------ the runner
def boundaries(inp):
    return np.array(N1.boundaries(inp), dtype=float)


class Run:
    """A(mu) = (a_Y, a_2, a_3) at mu (GeV), a_i = 1/alpha_i, Y normalisation.  name in VARIANTS.  exotics: list from exotics_e6 (or [] for the SM desert).
    a0: optional override of the three couplings at m_Z (synthetic worlds).  mutate_b: the lane-A bug pattern b_Y -> (3/5)(3/5)(41/6) (controls only)."""

    def __init__(self, name, exotics=(), a0=None, lncap=LNCAP_DEFAULT, mutate_b=False, rtol=1e-10):
        self.name = name
        self.loops = int(name[0])
        code = name.split("-")[1]
        self.inp = SET_B if "B" in code else SET_A
        self.thr = "T" in code
        self.a0 = boundaries(self.inp) if a0 is None else np.array(a0, dtype=float)
        self.exo = exotic_bB(exotics)
        self.mutate_b = mutate_b
        self.lncap = lncap
        self.rtol = rtol
        self.lnmax = lncap
        self._segs = []
        self._build()

    # content of a segment whose midpoint is mu: (b, B, top_present)
    def _content(self, mu):
        b = B_SM_F.copy()
        B = BM_SM_F.copy()
        if self.mutate_b:
            b[0] = 0.6 * (0.6 * 41 / 6)
        for (m, db, dB) in self.exo:
            if mu > max(m, MZ):
                b = b + db
                B = B + dB
        top = True
        if self.thr and mu < MT:
            b = b - DB_TOP
            top = False
        return b, B, top

    def _breaks(self):
        pts = {math.log(MZ)}
        if self.loops == 2 or self.thr:
            pts.add(math.log(MT))
        for (m, _, _) in self.exo:
            if MZ < m < math.exp(self.lncap):
                pts.add(math.log(m))
        pts.add(self.lncap)
        return sorted(p for p in pts if p <= self.lncap + 1e-12)

    def _rhs_factory(self, b, B, yukawa):
        C = CY_TOP if yukawa else np.zeros(3)

        def rhs(t, y):
            a = np.asarray(y[:3], dtype=float)
            yt = y[3]
            g2 = 4 * PI / a
            two = (B @ g2 - C * yt ** 2) / (16 * PI ** 2)
            da = -(b + two) / TWO_PI
            g1sq = g2[0] * 5 / 3
            dyt = yt / (16 * PI ** 2) * (4.5 * yt ** 2 - 8 * g2[2] - 2.25 * g2[1] - 0.85 * g1sq) if yukawa else 0.0
            return [da[0], da[1], da[2], dyt]
        return rhs

    def _shoot_yt(self, brk):
        """yt(m_Z) such that yt(m_t) = YT_MT with the full content (variants without a top threshold)."""
        l0, lt = brk[0], math.log(MT)
        segs = [(brk[i], brk[i + 1]) for i in range(len(brk) - 1) if brk[i + 1] <= lt + 1e-12]

        def f(y0):
            y = list(self.a0) + [y0]
            for (s0, s1) in segs:
                b, B, _ = self._content(math.exp(0.5 * (s0 + s1)))
                sol = solve_ivp(self._rhs_factory(b, B, True), [s0, s1], y, rtol=1e-10, atol=1e-12)
                y = list(sol.y[:, -1])
            return y[3] - YT_MT
        return brentq(f, 0.7, 1.3)

    def _build(self):
        brk = self._breaks()
        self._segs = []
        if self.loops == 1:
            a = self.a0.copy()
            for i in range(len(brk) - 1):
                s0, s1 = brk[i], brk[i + 1]
                b, _, _ = self._content(math.exp(0.5 * (s0 + s1)))
                self._segs.append((s0, s1, a.copy(), b))
                a = a - b / TWO_PI * (s1 - s0)
            self.lnmax = brk[-1]
            return
        if self.thr:
            y = list(self.a0) + [0.0]
        else:
            y = list(self.a0) + [self._shoot_yt(brk)]
        for i in range(len(brk) - 1):
            s0, s1 = brk[i], brk[i + 1]
            b, B, top = self._content(math.exp(0.5 * (s0 + s1)))
            if self.thr and abs(s0 - math.log(MT)) < 1e-12:
                y[3] = YT_MT
            yuk = top and not (self.thr and s1 <= math.log(MT) + 1e-12)
            evs = []
            for k in range(3):
                def ev(t, yy, k=k):
                    return yy[k] - 1.0
                ev.terminal = True
                ev.direction = -1
                evs.append(ev)
            sol = solve_ivp(self._rhs_factory(b, B, yuk), [s0, s1], y, rtol=self.rtol, atol=1e-12, dense_output=True, events=evs)
            end = float(sol.t[-1])
            self._segs.append((s0, end, sol))
            y = list(sol.y[:, -1])
            if sol.status == 1:
                self.lnmax = end
                return
        self.lnmax = brk[-1]

    def A(self, mu):
        lm = math.log(mu)
        if lm > self.lnmax + 1e-9:
            raise ValueError("mu above the integrated range")
        lm = max(lm, math.log(MZ))
        if self.loops == 1:
            for (s0, s1, a0, b) in self._segs:
                if lm <= s1 + 1e-12:
                    return a0 - b / TWO_PI * (lm - s0)
            s0, s1, a0, b = self._segs[-1]
            return a0 - b / TWO_PI * (lm - s0)
        for (s0, s1, sol) in self._segs:
            if lm <= s1 + 1e-12:
                return np.array(sol.sol(max(lm, s0))[:3])
        return np.array(self._segs[-1][2].sol(lm)[:3])

    def b_at(self, mu):
        return self._content(mu)[0]


_DESERT = {}


def desert(name, lncap=LNCAP_DEFAULT):
    key = (name, lncap)
    if key not in _DESERT:
        _DESERT[key] = Run(name, (), lncap=lncap)
    return _DESERT[key]


# ------------------------------------------------------------------------------------------------ scale solvers
def coup(A, key):
    return {"aY": A[0], "a1": 0.6 * A[0], "a2": A[1], "a3": A[2]}[key]


def solve_cross(run, k1, k2, lo=MZ * 1.001, hi=None, ngrid=800):
    hi = hi if hi is not None else math.exp(run.lnmax - 1e-6)
    xs = np.linspace(math.log(lo), math.log(hi), ngrid)
    f = lambda lm: coup(run.A(math.exp(lm)), k1) - coup(run.A(math.exp(lm)), k2)
    prev = f(xs[0])
    for i in range(1, len(xs)):
        cur = f(xs[i])
        if prev == 0.0:
            return math.exp(xs[i - 1])
        if prev * cur < 0:
            return math.exp(brentq(f, xs[i - 1], xs[i], xtol=1e-13))
        prev = cur
    return None


HET_COEFF = 0.216      # RECALLED (lane U3, P13), not re-derived


def solve_hetero(run, coeff=HET_COEFF):
    f = lambda lm: math.exp(lm) - coeff * math.sqrt(4 * PI / run.A(math.exp(lm))[1]) * XR
    hi = min(math.log(1e20), run.lnmax - 1e-6)
    try:
        return math.exp(brentq(f, math.log(1e14), hi))
    except ValueError:
        return None


# ------------------------------------------------------------------------------------------------ the rules
def ratio_res(actual, target):
    if not (actual > 0):
        return 1e3
    return target / actual - 1.0


def make_rule(kind, **kw):
    """kind in RA RB RC RD RE RF RG.  kw: X (fixed scale) / xtag, h (dual Coxeter), N (species count), s1 (S1 pattern 4 pi (5,2,3))."""
    r = dict(kind=kind, X=None, xtag="", h=None, N=None, s1=False, param_scale=False)
    r.update(kw)
    r["absolute"] = kind in ("RD", "RF", "RG")
    if kind in ("RA", "RC"):
        r["K_eq"], r["u"] = 2, 0
    elif kind == "RB":
        r["K_eq"], r["u"] = 2, 1
    elif kind == "RD":
        r["K_eq"], r["u"] = 3, (1 if r["X"] is None else 0)
    elif kind == "RE":
        r["K_eq"], r["u"] = 3, 1
    elif kind == "RF":
        r["K_eq"], r["u"] = 3, 0
    elif kind == "RG":
        r["K_eq"], r["u"] = 1, 0
    r["id"] = kind + (":" + r["xtag"] if r["xtag"] else "") + (f":h{r['h']}" if r["h"] else "") + (f":N{r['N']}" if r["N"] else "") + (":S1" if r["s1"] else "")
    return r


def species_scale(N):
    return XR / math.sqrt(N)


def rule_scale(rule, run, xfac=1.0):
    if rule["kind"] in ("RB",) or (rule["kind"] == "RD" and rule["X"] is None):
        return solve_cross(run, "a1", "a2")
    if rule["kind"] == "RE":
        return solve_hetero(run)
    return rule["X"] * xfac


def residuals(rule, run, ref, xfac=1.0):
    """dict(X, r, names, A, pred).  r is None if the scale does not exist or lies beyond the integrated range."""
    kind = rule["kind"]
    X = rule_scale(rule, run, xfac)
    if X is None or math.log(X) > run.lnmax:
        return dict(X=X, r=None, names=[], A=None, pred=None)
    A = run.A(X)
    aY, a2, a3 = A
    a1 = 0.6 * aY
    refA = ref.A(X)
    pred = None
    if kind == "RA":
        r, names = np.array([ratio_res(a1 / a2, 1.0), ratio_res(a3 / a2, 1.0)]), ["a_1/a_2", "a_3/a_2"]
    elif kind == "RB":
        r, names = np.array([ratio_res(a3 / a2, 1.0)]), ["a_3/a_2 at a_1=a_2"]
    elif kind == "RC":
        r, names = np.array([ratio_res(aY / a2, 1.0), ratio_res(a3 / a2, 1.0)]), ["a_Y/a_2", "a_3/a_2"]
    elif kind == "RD":
        if rule["s1"]:
            pred = np.array([(5 / 3) * 4 * PI * 5, 4 * PI * 2, 4 * PI * 3])
        else:
            hh = 4 * PI * rule["h"]
            pred = np.array([(5 / 3) * hh, hh, hh])
        if rule["X"] is None:
            hh = 4 * PI * rule["h"]
            r, names = np.array([ratio_res(a3 / a2, 1.0), (hh - a2) / refA[1]]), ["a_3/a_2", "a_2=4pi h"]
            pred = np.array([np.nan, hh, np.nan])
        else:
            r, names = (pred - A) / refA, ["a_Y", "a_2", "a_3"]
    elif kind == "RE":
        r, names = np.array([ratio_res(a1 / a2, 1.0), ratio_res(a3 / a2, 1.0)]), ["a_1/a_2", "a_3/a_2"]
    elif kind == "RF":
        pred = np.zeros(3)
        r, names = (pred - A) / refA, ["a_Y=0", "a_2=0", "a_3=0"]
    elif kind == "RG":
        pred = np.zeros(3)
        r, names = np.array([(0.0 - aY) / refA[0]]), ["a_Y=0"]
    elif kind == "SYN":
        pred = np.array(rule["pred"], dtype=float)
        r, names = (pred - A) / refA, ["a_Y", "a_2", "a_3"]
    else:
        raise ValueError(kind)
    return dict(X=X, r=np.asarray(r, dtype=float), names=names, A=A, pred=pred)


def implied_alpha_inv0(rule, res):
    """T-ABS (U3 translation): 1/alpha(0) = 137.035999177 + (pred_Y - A_Y) + (pred_2 - A_2) at X.  Only for absolute rules with a_Y and a_2 both specified."""
    if res["pred"] is None or not rule["absolute"] or np.isnan(res["pred"][0]) or np.isnan(res["pred"][1]):
        return None
    A = res["A"]
    return ALPHA_INV0 + (res["pred"][0] - A[0]) + (res["pred"][1] - A[1])


def evaluate_bands(rule, exotics, floor=0.01, a0=None, names=VARIANTS):
    """T-JOINT (U3): residuals under the seven running variants (and X x 0.5, x 2 for parametric scales), bands, tolerances, pass.  ref = SM-desert run of the same variant."""
    runs = {}
    cen = Run("2L-T", exotics, a0=a0)
    ref_c = desert("2L-T") if a0 is None else Run("2L-T", (), a0=a0)
    c = residuals(rule, cen, ref_c)
    out = dict(rule=rule["id"], X=c["X"], names=c["names"], A=None if c["A"] is None else c["A"].tolist(), pred=None if c["pred"] is None else [None if np.isnan(x) else float(x) for x in c["pred"]],
               cen_r=None if c["r"] is None else c["r"].tolist(), exists=c["r"] is not None, implied={})
    if c["r"] is None:
        return out
    rr = {}
    imp = {}
    for nm in names:
        run = cen if nm == "2L-T" else Run(nm, exotics, a0=a0)
        ref = ref_c if nm == "2L-T" else (desert(nm) if a0 is None else Run(nm, (), a0=a0))
        res = residuals(rule, run, ref)
        rr[nm] = None if res["r"] is None else res["r"]
        v = implied_alpha_inv0(rule, res)
        if v is not None:
            imp[nm] = v
    if rule["param_scale"]:
        for xf in (0.5, 2.0):
            res = residuals(rule, cen, ref_c, xfac=xf)
            rr[f"X x{xf}"] = res["r"]
    K = len(c["r"])
    band = np.zeros(K)
    for k, x in rr.items():
        if x is None:
            continue
        band = np.maximum(band, np.abs(x - c["r"]))
    tol = np.maximum(2 * band, floor)
    out["runs"] = {k: (None if x is None else x.tolist()) for k, x in rr.items()}
    out["band"] = band.tolist()
    out["tol"] = tol.tolist()
    out["pass_k"] = [bool(v) for v in (np.abs(c["r"]) <= tol)]
    out["pass"] = bool(np.all(np.abs(c["r"]) <= tol))
    out["margin"] = (np.abs(c["r"]) / tol).tolist()
    if imp:
        vals = np.array(list(imp.values()))
        cenv = imp["2L-T"]
        spread = float(np.max(np.abs(vals - cenv)) / ALPHA_INV0)
        out["implied"] = dict(central=cenv, spread_rel=spread, tol_em=max(2 * spread, 0.01), delta=abs(cenv / ALPHA_INV0 - 1))
    return out


def mono_kill(rule, ev):
    """T-MONO on the actual run: an absolute rule predicting a_j ABOVE the run beyond tol cannot be repaired by added matter."""
    if not rule["absolute"] or ev["cen_r"] is None:
        return False, []
    hits = []
    for k, name in enumerate(ev["names"]):
        absolute = not (rule["kind"] == "RD" and rule["X"] is None) or k == 1
        if absolute and ev["cen_r"][k] > ev["tol"][k]:
            hits.append(name)
    return bool(hits), hits


def domain_kill(ev):
    return ev["X"] is not None and ev["X"] > 1.001 * XP


# ------------------------------------------------------------------------------------------------ inequality checks
def tau_proton_years(X, a2X):
    """RECALLED scaling, uncertain by a factor 10: tau_p = 1e35 yr (M_X/1e16 GeV)^4 (0.025/alpha_G)^2, M_X = X, alpha_G = 1/a_2(X)."""
    aG = 1.0 / a2X
    return 1e35 * (X / 1e16) ** 4 * (0.025 / aG) ** 2


def proton_check(X, a2X):
    tau = tau_proton_years(X, a2X)
    if tau >= 2.4e34:
        return "PASS", tau
    if tau >= 2.4e33:
        return "UNCERTAIN", tau
    return "FAIL", tau


def perturbative_check(run, X):
    lm = np.linspace(math.log(MZ), min(math.log(X), run.lnmax - 1e-9), 60)
    return bool(all(np.all(run.A(math.exp(x)) >= 1.0) for x in lm))


def landau_scale_log10(exotics):
    """Where the central run reaches a_Y = 1 (non-perturbative onset), extrapolated linearly in ln mu to a_Y = 0 with the local slope; returns (log10 GeV of a_Y=1, log10 GeV of the extrapolated zero)."""
    run = Run("2L-T", exotics, lncap=math.log(1e45))
    lm = run.lnmax
    if lm >= math.log(1e45) - 1e-6:
        return None, None
    A1 = run.A(math.exp(lm))
    h = 1e-3
    slope = (run.A(math.exp(lm))[0] - run.A(math.exp(lm - h))[0]) / h
    lz = lm + (0.0 - A1[0]) / slope if slope < 0 else None
    return lm / math.log(10), (None if lz is None else lz / math.log(10))


def excess(rule, m_knobs):
    """excess = K_eq - u - m  (pre-registered counting rule)."""
    return rule["K_eq"] - rule["u"] - m_knobs


# ------------------------------------------------------------------------------------------------ lane D's bar
def bar_verdict(delta, tol_em, log2size=math.log2(N_TRIALS_TOTAL)):
    import alpha_bar_checker as ABC
    r = ABC.assess(delta=delta, log2size=log2size, n_targets=1, predicted_precision=tol_em, fitted_reals=0, scale_stated=True, verbose=False)
    return bool(r["clears"]), r


# ------------------------------------------------------------------------------------------------ bookkeeping for the scripts
class Checks:
    """PASS/FAIL bookkeeping with the lane's exit convention: real run exit 0 if all pass (2 otherwise); MUTATE exit 1 if the control bites (some check fails), 3 if it does not."""

    def __init__(self, mutate):
        self.mut = mutate
        self.fails = []
        self.n = 0

    def __call__(self, name, ok, info=""):
        self.n += 1
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} {info}")
        if not ok:
            self.fails.append(name)

    def finish(self, tag):
        print(f"{tag}: {self.n} checks, {len(self.fails)} failed" + (f": {self.fails}" if self.fails else ""))
        if self.mut:
            if self.fails:
                print(f"{tag} MUTATE: control BITES (failed as required) -> exit 1")
                sys.exit(1)
            print(f"{tag} MUTATE: control BROKEN (no check failed) -> exit 3")
            sys.exit(3)
        sys.exit(0 if not self.fails else 2)

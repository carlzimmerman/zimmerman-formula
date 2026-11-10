"""TK1 K4 evaluator: the closed-form scalar quadratic action (tk1_k4.json) on a numerical background.
Units H0 = 1, (8 pi G/3) = 1, so K = 4 pi G = 1.5 and n = Omega_n. Clock time t (unitary gauge), d/dt = a H N0 d/da.
L2 = A_z Zdot^2 - (g4 k^4 + g2 k^2 + g0) Z^2 (comoving k); physical rate^2 = (g4 k^4 + g2 k^2 + g0) / (A_z N0^2).
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, json
import mpmath as mp
import sympy as sp
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk1_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
KC = mp.mpf(1.5)
_J = json.load(open(os.path.join(HERE, "tk1_k4.json")))
_names = ["a", "a_d", "a_dd", "N0", "N0_d", "N0_dd", "K", "Lambda"]
for f in ("FQ", "Fth", "FQQ", "FQth", "Fthth", "F0"):
    _names += [f, f + "_d", f + "_dd"]
EXPR = {k: eval(_J["K4_sym_" + k], {**sp.__dict__}) for k in ("Az", "g4", "g2", "g0")}
_bysym = {}
for e in EXPR.values():
    for s_ in e.free_symbols:
        _bysym[str(s_)] = s_
_syms = [_bysym.get(n, sp.Symbol(n)) for n in _names]
FUN = {k: sp.lambdify(_syms, v, "mpmath") for k, v in EXPR.items()}


def background_funcs(key, a, rest_fn, On_fn, OL=0.6844650532434209):
    """values of the background symbols at a, for the patch/background defined by the smooth closed forms rest_fn(a)
    (everything but the clock, curvature included) and On_fn(a) (clock charge). H(a) is the largest root of
    G = H^2 - rest - xK(3H, On); dH/da by implicit differentiation (no differencing through the root solve)."""
    a = mp.mpf(a)
    On = On_fn(a); rest = rest_fn(a)
    H = L.H_root(key, rest, On)
    xk = lambda th, on: key.xK(th, on)
    xK_th = mp.diff(lambda th: xk(th, On), 3 * H)
    xK_on = mp.diff(lambda on: xk(3 * H, on), On)
    dOn = mp.diff(On_fn, a); drest = mp.diff(rest_fn, a)
    GH = 2 * H - 3 * xK_th
    Ga = -drest - xK_on * dOn
    dH = -Ga / GH
    def total_da(f):
        """d/da of f(H, On) along the background."""
        fH = mp.diff(lambda h: f(h, On), H)
        fO = mp.diff(lambda o: f(H, o), On)
        return fH * dH + fO * dOn
    Qf = lambda h, o: 1 + mp.mpf(1.5) * o / key.M2(3 * h)
    N0f = lambda h, o: 1 / Qf(h, o)
    adotf = lambda h, o: a * h * N0f(h, o)
    q = Qf(H, On); N0 = 1 / q
    dtda = a * H * N0                      # d/dt = dtda * d/da
    adot = a * H * N0
    d_adot_da = H * N0 + a * total_da(lambda h, o: h * N0f(h, o))
    v = dict(a=a, a_d=adot, a_dd=dtda * d_adot_da, N0=N0, N0_d=dtda * total_da(N0f), N0_dd=mp.mpf(0), K=KC,
             Lambda=3 * mp.mpf(OL))
    def Fs(h, o):
        qq = Qf(h, o); tt = 3 * h; M = key.M2(tt); Mp = key.dM2(tt); Mpp = key.M2pp(tt)
        return dict(FQ=M * (qq - 1) / KC, Fth=Mp * (qq - 1)**2 / (2 * KC), FQQ=M / KC, FQth=Mp * (qq - 1) / KC,
                    Fthth=Mpp * (qq - 1)**2 / (2 * KC), F0=M * (qq - 1)**2 / (2 * KC))
    F = Fs(H, On)
    for nm in F:
        v[nm] = F[nm]
        v[nm + "_d"] = dtda * total_da((lambda nm_: (lambda h, o: Fs(h, o)[nm_]))(nm))
        v[nm + "_dd"] = mp.mpf(0)
    v["H"] = H; v["GH"] = GH
    return v


def evaluate(key, a, rest_fn, On_fn, OL=0.6844650532434209):
    v = background_funcs(key, a, rest_fn, On_fn, OL)
    args = [v[n] for n in _names]
    r = {k: FUN[k](*args) for k in FUN}
    r["N0"] = v["N0"]; r["a"] = a
    r["cs2_dust"] = r["g2"] * a**2 / (r["Az"] * v["N0"]**2)
    r["H"] = v["H"]; r["GH"] = v["GH"]
    r["Qm1"] = 1 / v["N0"] - 1
    return r


def uses_F_dd():
    return any(str(s).startswith("F") and str(s).endswith("_dd") for k in EXPR for s in EXPR[k].free_symbols)

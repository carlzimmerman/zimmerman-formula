#!/usr/bin/env python3
"""CFG917 library (FROZEN_CRITERIA.md, commit 0289e4ad4): data, backgrounds, growth, linear spectra, the per-run P(k, z) model and the
Limber projection for the Part B CMB-lensing statistic.  Imported by cfg917_cmb_lensing.py and cfg917_camb_ktests.py; numpy/scipy only.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, json, math, glob, ast
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); REPO = os.path.dirname(CFG)
NP_ROOT = os.path.dirname(REPO); EXT = os.path.join(NP_ROOT, "_external_data")
PR4D = os.path.join(EXT, "cmb_lensing_raw", "planck_PR4_lensing", "planckpr4lensing", "data_pr4")
STEM = "pp_consext8_npipe_smicaed_TiPi_jTP_pre30T_kfilt_rdn0cov_PS1"
C654 = os.path.join(CFG, "CFG654_independent_inputs")
LMAX = 2500
LARR = np.arange(LMAX + 1, dtype=float)          # X arrays are indexed by L = 0..2500 (entries L < 2 unused)
CKMS_H = 2997.92458                               # c / (100 km/s/Mpc) in Mpc/h
Z_STAR = 1090.0
rel = lambda p: os.path.relpath(p, NP_ROOT)
_trapz = getattr(np, "trapezoid", None) or np.trapz

# ------------------------------------------------------------------ data: Planck PR4 lensing (CMB-marginalised, conservative 8-400)
def _window(fn):
    w = np.loadtxt(fn, ndmin=2); out = np.zeros(LMAX + 1)
    for L, v in zip(w[:, 0].astype(int), w[:, 1]):
        if 2 <= L <= LMAX: out[L] = v
    return out

def load_pr4():
    bp = np.loadtxt(os.path.join(PR4D, STEM + "_bandpowers.dat"))
    C = np.loadtxt(os.path.join(PR4D, STEM + "_CMBmarged_cov.dat"))
    W = np.array([_window(os.path.join(PR4D, STEM + f"_window/window{b}.dat")) for b in range(1, 10)])
    M = np.array([_window(os.path.join(PR4D, STEM + f"_CMBmarged_lens_delta_window/window{b}.dat")) for b in range(1, 10)])
    F = np.loadtxt(os.path.join(PR4D, STEM + "_CMBmarged_lensing_fiducial_correction.dat"))[:, 1]
    return dict(d=bp[:, 4], err=bp[:, 5], ahat=bp[:, 6], lmin=bp[:, 1].astype(int), lmax=bp[:, 2].astype(int), Lav=bp[:, 3],
                C=C, Cinv=np.linalg.inv(C), W=W, M=M, F=F, n=len(bp))

# explicit sums instead of BLAS matmul (the Accelerate BLAS raises spurious floating-point flags on these small products; values are
# identical, but explicit sums keep every number free of that ambiguity)
def wsum(Wm, X):
    return (Wm * X[None, :]).sum(axis=1)

def qform(r, Cinv, s=None):
    s = r if s is None else s
    return float((r[:, None] * Cinv * s[None, :]).sum())

def pr4_binned(D, X):
    """the package's CMBlikes rule: B_b = sum_L W_b(L) X_L + sum_L M_b(L) X_L - F_b."""
    return wsum(D["W"], X) + wsum(D["M"], X) - D["F"]

def pr4_chi2(D, X):
    r = pr4_binned(D, X) - D["d"]; return qform(r, D["Cinv"])

def pr4_amp(D, X):
    """best-fit amplitude A of B(A) = A (W + M) X - F (context only)."""
    u = wsum(D["W"], X) + wsum(D["M"], X); a = qform(u, D["Cinv"], D["d"] + D["F"]); b = qform(u, D["Cinv"])
    return a / b, 1 / math.sqrt(b)

def load_ffp10():
    t = np.loadtxt(os.path.join(PR4D, "FFP10_wdipole_lenspotentialCls.dat"))
    X = np.zeros(LMAX + 1); L = t[:, 0].astype(int); m = L <= LMAX; X[L[m]] = t[m, 5]
    return X

def load_pl18_agg():
    x26 = open(os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26", "XR26_cmb.py")).read()
    tab = ast.literal_eval(x26[x26.index("PL18_MV = {") + len("PL18_MV = "):x26.index("DP_MEAN")].strip())
    return tab

def agg_chi2(tab, X, Xf):
    """AGG member: Planck 2018 MV 8-2048, A_b^model = <X>_b / <X_FFP10>_b (uniform integer-L averages), diagonal chi^2."""
    c = 0.0; Am = []
    for lo, hi, A_, sA, fid in tab["8-2048"]:
        a = X[lo:hi + 1].mean() / Xf[lo:hi + 1].mean(); Am.append(a); c += ((a - A_) / sA) ** 2
    return float(c), Am

# ------------------------------------------------------------------ backgrounds, growth, linear spectra (each run's OWN, engine code)
class Inputs:
    """kind = 'inherited' (cfg596/650 engine constants) or 'native_cmb' / 'native' (CFG654 tables, = cfg654 engine)."""
    def __init__(self, kind):
        self.kind = kind
        if kind == "inherited":
            self.h = 0.6736; om_b, om_c = 0.02237, 0.1200; self.Om = (om_b + om_c) / self.h ** 2; self.OL = 1 - self.Om; self.Or = 0.0
            NS, SIG8 = 0.965, 0.811; h = self.h; Om = self.Om
            def T_eh(k):                                                   # engine T_eh verbatim
                OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
                s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
                ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
                gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
                q = k * (2.7255 / 2.7) ** 2 / (gam * h)
                L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
                return L0 / (L0 + C0 * q * q)
            KG = np.geomspace(1e-5, 100, 40000); PK = KG ** NS * T_eh(KG * h) ** 2
            W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
            PK = PK * SIG8 ** 2 / (_trapz(PK * W8(KG * 8.0) ** 2 * KG ** 2, KG) / (2 * math.pi ** 2))
            self._lkg, self._pk = np.log(KG), PK
            self.Plin0 = lambda k: np.interp(np.log(np.maximum(k, 1e-5)), self._lkg, self._pk, left=0, right=0)   # engine P_lin0
            self.Ea = lambda a: math.sqrt(self.Om / a ** 3 + self.OL)
            self.Ez = lambda z: np.sqrt(self.Om * (1 + z) ** 3 + self.OL)
            g1 = self._g(1.0); self._g1 = g1; self._dc = {}
            def D(a):                                                                 # engine Dgrow verbatim (cached)
                a = float(a)
                if a not in self._dc: self._dc[a] = self._g(a) / g1
                return self._dc[a]
            self.D = D
        else:
            sfx = "_cmb" if kind == "native_cmb" else ""
            T = np.load(os.path.join(C654, f"cfg654_ics_tables{sfx}.npz")); S = np.load(os.path.join(C654, f"cfg654_scorer_tables{sfx}.npz"))
            self.h = float(T["h"]); om_b, om_c = float(T["omega_b"]), float(T["omega_c"]); self.Or = float(T["Or"])
            self.Om = (om_b + om_c) / self.h ** 2; self.OL = 1.0 - self.Om - self.Or
            assert abs(self.Om - float(S["Om"])) < 1e-9 and abs(self.OL - float(S["OL"])) < 1e-9
            trz, trd = np.array(T["trz"]), np.array(T["trd"])
            lkh, lpk = np.log(np.array(T["kh"])), np.log(np.array(T["Plin0"]))
            self.Plin0 = lambda k: np.exp(np.interp(np.log(np.clip(k, math.exp(lkh[0]), math.exp(lkh[-1]))), lkh, lpk))   # engine
            lna, lnD = np.array(T["lna"]), np.array(T["lnD"])
            self.D = lambda a: float(math.exp(np.interp(math.log(a), lna, lnD)))     # engine Dgrow
            self.Ez = lambda z: np.sqrt(self.Om * (1 + z) ** 3 + self.Or * (1 + z) ** 4 + self.OL * (1.0 - np.interp(z, trz, trd)))
        zf = np.concatenate([[0.0], np.geomspace(1e-7, 1200.0, 400000)])
        inv = 1.0 / self.Ez(zf)
        self._zf = zf; self._chif = CKMS_H * np.concatenate([[0.0], np.cumsum(0.5 * (inv[1:] + inv[:-1]) * np.diff(zf))])
        self.chi_star = float(self.chi(Z_STAR))
    def _g(self, a):
        return quad(lambda u: 1.0 / (u * self.Ea(u)) ** 3, 0, a)[0] * self.Ea(a)
    def chi(self, z):
        return np.interp(z, self._zf, self._chif)

def inputs_of(run):
    k = run["meta"].get("cfg654_inputs")
    return "inherited" if k in (None, "inherited") else k

# ------------------------------------------------------------------ runs
def load_run(fn):
    d = json.load(open(fn)); sn = d["snap"]
    snaps = {n: dict(a=float(s["a"]), D=float(s["D"]), k=np.array(s["k"], float), Pg=np.array(s["P_grav"], float), P=np.array(s["P"], float))
             for n, s in sn.items()}
    meta = {k: d.get(k) for k in ("tag", "np", "L", "seed", "foot", "switch", "cfg654_inputs", "modules", "nseed")}
    return dict(fn=fn, meta=meta, snaps=snaps)

def lattice_bins(L, nbin):
    """exact lattice enumeration of the engine's linear bins n = [(n-1/2)k_f, (n+1/2)k_f), n = 1..nbin: full-space vectors (= the engine's
    half-space weights).  Returns per bin: the vectors' |k| list (h/Mpc) and counts W_b."""
    kf = 2 * math.pi / L; R = nbin + 1; ax = np.arange(-R, R + 1)
    nx, ny, nz = np.meshgrid(ax, ax, ax, indexing="ij"); r = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2).ravel()
    ib = np.floor(r + 0.5).astype(int)                # bin index: |n| in [b - 1/2, b + 1/2)
    out = []
    for b in range(1, nbin + 1):
        m = ib == b; out.append((r[m] * kf).astype(np.float32).astype(np.float64))   # engine evaluates |k| in float32
    return out

# ------------------------------------------------------------------ the per-run P(k, z) model (FROZEN_CRITERIA.md B2)
class PairModel:
    """F and S0 of one pair.  opts: kcut (support top), vc (variance correction on), field_F ('Pg' | 'P')."""
    def __init__(self, F, S, inp, kcut_div=4.0, vc=True, field_F="Pg", kc=1.0):
        self.F, self.S, self.inp = F, S, inp
        N, L = int(S["meta"]["np"]), float(S["meta"]["L"])
        assert int(F["meta"]["np"]) == N and float(F["meta"]["L"]) == L and F["meta"]["seed"] == S["meta"]["seed"], "pair must share box + realisation"
        self.late = sorted([n for n in S["snaps"] if n in F["snaps"] and S["snaps"][n]["a"] >= 0.5 - 1e-9], key=lambda n: S["snaps"][n]["a"])
        self.zi = min(S["snaps"], key=lambda n: S["snaps"][n]["a"])
        self.A = np.array([S["snaps"][n]["a"] for n in self.late]); self.a_i = S["snaps"][self.zi]["a"]
        kb = S["snaps"][self.late[0]]["k"]
        ktop = math.pi * N / (kcut_div * L)
        sup = kb <= ktop + 1e-9; self.ks = kb[sup]; self.k_lo = float(self.ks[0]); self.k_top = float(self.ks[-1]); self.nsup = int(sup.sum())
        # realisation-variance correction on k_b <= kc (from the S0 z_i field, applied to both arms)
        self.C = np.ones(self.nsup); self.vc_bins = int((self.ks <= kc + 1e-12).sum())
        nb = self.vc_bins; bins = lattice_bins(L, nb)
        self.Pbar = np.array([inp.Plin0(kk).mean() for kk in bins]); self.Wb = np.array([len(kk) for kk in bins], float)
        self.kbar = np.array([kk.mean() for kk in bins])
        Di = S["snaps"][self.zi]["D"]; pzi = S["snaps"][self.zi]["Pg"][sup][:nb]
        self.x = pzi / (self.Pbar * Di ** 2)
        if vc: self.C[:nb] = 1.0 / self.x
        self.vc = vc
        self.node = {}
        for arm, R_, fld in (("F", F, field_F), ("S0", S, "Pg")):
            self.node[arm] = np.array([self.C * R_["snaps"][n][fld][sup] for n in self.late])         # (n_nodes, nsup)
        self.slope = {arm: np.array([np.polyfit(np.log(self.ks[self.ks >= self.k_top / 2]), np.log(v[self.ks >= self.k_top / 2]), 1)[0]
                                     for v in self.node[arm]]) for arm in self.node}
        self.Rlo = np.array([(self.node["F"][i][:3] / self.node["S0"][i][:3]).mean() for i in range(len(self.late))])
        self.D1 = inp.D(0.5)

    def node_P(self, arm, i, k, klow=False):
        """node spectrum i of an arm at arbitrary k (h/Mpc)."""
        v = self.node[arm][i]; out = np.empty_like(k)
        lo = k < self.k_lo; hi = k > self.k_top; mid = ~(lo | hi)
        out[mid] = np.exp(np.interp(np.log(k[mid]), np.log(self.ks), np.log(v)))
        out[hi] = v[-1] * (k[hi] / self.k_top) ** self.slope[arm][i]
        fac = self.Rlo[i] if (klow and arm == "F") else 1.0
        out[lo] = self.inp.Plin0(k[lo]) * self.inp.D(self.A[i]) ** 2 * fac
        return out

    def P(self, arm, k, a, zrule="lin", klow=False, inject=None):
        """model P_hat at wavenumbers k (h/Mpc) and scale factor a (FROZEN B2 + robustness rules)."""
        A = self.A
        if a >= A[0] - 1e-12:                                          # z <= 1: nodes, ln P linear in a
            a_ = min(a, A[-1]); j = int(np.clip(np.searchsorted(A, a_) - 1, 0, len(A) - 2)); t = (a_ - A[j]) / (A[j + 1] - A[j])
            out = np.exp((1 - t) * np.log(self.node_P(arm, j, k, klow)) + t * np.log(self.node_P(arm, j + 1, k, klow)))
            lo = k < self.k_lo                                           # frozen: k < k_lo is P_lin0 D(a)^2 exactly (x mean low ratio, KLOW F)
            fac = ((1 - t) * self.Rlo[j] + t * self.Rlo[j + 1]) if (klow and arm == "F") else 1.0
            out[lo] = self.inp.Plin0(k[lo]) * self.inp.D(a) ** 2 * fac
        else:                                                            # z > 1
            Da = self.inp.D(a)
            if zrule == "lin":
                out = self.node_P(arm, 0, k, klow) * (Da / self.D1) ** 2
            else:
                pl = self.inp.Plin0(k); den = pl * self.D1 ** 2
                w = min(1.0, max(0.0, (a - self.a_i) / (0.5 - self.a_i)))
                TS = self.node_P("S0", 0, k) / den
                if zrule == "hold":
                    PS = pl * Da ** 2 * (1 + (TS - 1) * w)
                    out = PS if arm == "S0" else PS * (self.node_P("F", 0, k, klow) / den) / TS
                elif zrule == "rel":
                    TX = self.node_P(arm, 0, k, klow) / den
                    out = pl * Da ** 2 * (1 + (TX - 1) * w)
                else:
                    raise ValueError(zrule)
        if inject is not None and arm == "F":
            out = out * inject
        return out

# ------------------------------------------------------------------ Limber projection
def zgrid(n1=400, n2=600, zmax=1089.0):
    return np.concatenate([np.geomspace(1e-3, 1.0, n1), np.geomspace(1.0, zmax, n2 + 1)[1:]])

def limber_X(Pfun, inp, zg, Om, bg=None, Lmin=2, Lmax=LMAX, masks=None):
    """X_L = [L(L+1)]^2 C_L / 2pi for L = 0..LMAX (zeros below Lmin).  Pfun(k, a, z) -> P at k.  bg: Inputs for the distances (default inp).
    masks: optional dict name -> function(k, z) -> bool array; returns dict of X restricted to those (k, z) regions as well."""
    B = inp if bg is None else bg
    chi = B.chi(zg); cs = B.chi_star; Ls = np.arange(Lmin, Lmax + 1, dtype=float)
    pref = (1.5 * Om / CKMS_H ** 2) ** 2
    I = np.zeros((len(Ls), len(zg))); Im = {m: np.zeros_like(I) for m in (masks or {})}
    for j, (z, c) in enumerate(zip(zg, chi)):
        k = (Ls + 0.5) / c; p = Pfun(k, 1.0 / (1.0 + z), z)
        w = pref * ((1 + z) * (cs - c) / cs) ** 2
        I[:, j] = w * p
        for m, f in (masks or {}).items(): Im[m][:, j] = w * p * f(k, z)
    fac = 4.0 / (Ls + 0.5) ** 4 * (Ls * (Ls + 1)) ** 2 / (2 * math.pi)
    def proj(II):
        X = np.zeros(LMAX + 1); X[Lmin:Lmax + 1] = fac * _trapz(II, chi, axis=1); return X
    out = proj(I)
    if masks: return out, {m: proj(v) for m, v in Im.items()}
    return out

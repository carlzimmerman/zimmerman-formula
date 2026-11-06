#!/usr/bin/env python3
"""QX15 reusable grader (FROZEN_CRITERIA.md): Planck PR4 CamSpec NPIPE 12.6 TTTEEE and ACT DR6 CMB-only.
Re-implemented from Cobaya's planck_2018_CamSpec_python / CamSpec2021 power-law residual model and from
act_dr6_cmbonly.py (both read, not executed). Input: dict of D_ell [muK^2] arrays 'tt','te','ee' indexed by L.
Nuisances profiled with L-BFGS-B and analytic gradients. kappa = 1/2 FITTED; not theory closed."""
import os, hashlib, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")  # spurious macOS Accelerate BLAS FP flags; results finite
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.join(REPO, "_external_data", "qx15_cmb_primary")
CS = os.path.join(EXT, "camspec", "CamSpec_NPIPE")
ACTF = os.path.join(EXT, "act", "v1.0", "dr6_data_cmbonly.fits")
CACHE = os.environ.get("QX15_CACHE", os.path.join(os.path.expanduser("~"), ".cache", "qx15"))
NAMES = ["100x100", "143x143", "217x217", "143x217", "TE", "EE"]


class CamSpec:
    """use: dict name -> (lmin, lmax) for the spectra used (subset of the file's ranges)."""

    def __init__(self, use):
        rng = [l.split() for l in open(os.path.join(CS, "like_NPIPE_12.6_unified_data_ranges.txt"), encoding="utf-8-sig") if l.strip()]
        spectra = np.loadtxt(os.path.join(CS, "like_NPIPE_12.6_unified_spectra.txt"))
        nX = 0; idx = []; self.blocks = []; dv = []
        for i, (nm, a, b) in enumerate(rng):
            a, b = int(a), int(b); n = b - a + 1
            if nm in use:
                lo, hi = max(a, use[nm][0]), min(b, use[nm][1])
                ells = np.arange(lo, hi + 1)
                idx.append(ells - a + nX); self.blocks.append((i, ells)); dv.append(spectra[ells, i])
            nX += n
        idx = np.concatenate(idx); self.d = np.concatenate(dv)
        key = hashlib.md5(repr(sorted(use.items())).encode()).hexdigest()[:12]
        os.makedirs(CACHE, exist_ok=True); cf = os.path.join(CACHE, f"camspec_covinv_{key}.npy")
        if os.path.exists(cf):
            self.Ci = np.load(cf)
        else:
            cov = np.fromfile(os.path.join(CS, "like_NPIPE_12.6_unified_cov.bin"), dtype=np.float32)
            assert cov.size == nX * nX
            cov = cov.reshape(nX, nX)[np.ix_(idx, idx)].astype(np.float64)
            self.Ci = np.linalg.inv(cov); np.save(cf, self.Ci)
        self.N = len(self.d)
        # parameter vector: A_planck, amp143, amp217, amp143x217, n143, n217, n143x217, calTE, calEE
        self.x0 = np.array([1.0, 10.0, 20.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        self.bounds = [(0.9, 1.1), (0, 50), (0, 50), (0, 50), (0, 5), (0, 5), (0, 5), (0.9, 1.1), (0.9, 1.1)]
        self.tt_map = {1: (1, 4), 2: (2, 5), 3: (3, 6)}           # spectrum index -> (amp idx, n idx)

    def _model(self, D, p):
        A2 = p[0] ** 2; parts = []; grads = []
        for (i, ells) in self.blocks:
            if i <= 3:
                if i == 0:
                    fg = 0.0 * ells; base = D["tt"][ells]
                else:
                    ia, jn = self.tt_map[i]; x = ells / 1500.0; pw = x ** p[jn]
                    fg = p[ia] * pw; base = D["tt"][ells]
                m = (base + fg) / A2
                g = {0: -2 * m / p[0]}
                if i > 0:
                    g[ia] = pw / A2; g[jn] = p[ia] * np.log(x) * pw / A2
            elif i == 4:
                m = D["te"][ells] / (p[7] * A2); g = {0: -2 * m / p[0], 7: -m / p[7]}
            else:
                m = D["ee"][ells] / (p[8] * A2); g = {0: -2 * m / p[0], 8: -m / p[8]}
            parts.append(m); grads.append(g)
        return parts, grads

    def chi2(self, D, p, grad=False):
        parts, grads = self._model(D, p); m = np.concatenate(parts); r = self.d - m; Cr = self.Ci @ r
        like = float(r @ Cr)
        pri = ((p[0] - 1) / 0.0025) ** 2 + ((p[7] - 1) / 0.01) ** 2 + ((p[8] - 1) / 0.01) ** 2
        if not grad:
            return like, pri
        gv = np.zeros(9); ix = 0
        for part, g in zip(parts, grads):
            n = len(part); seg = Cr[ix:ix + n]
            for k, v in g.items(): gv[k] += -2 * float(v @ seg)
            ix += n
        gv[0] += 2 * (p[0] - 1) / 0.0025 ** 2; gv[7] += 2 * (p[7] - 1) / 0.01 ** 2; gv[8] += 2 * (p[8] - 1) / 0.01 ** 2
        return like + pri, gv

    def profile(self, D, x0=None):
        f = lambda p: self.chi2(D, p, grad=True)
        best = None
        for s in ([self.x0] if x0 is None else [x0, self.x0]):
            r = minimize(f, s, jac=True, method="L-BFGS-B", bounds=self.bounds, options=dict(maxiter=500, ftol=1e-12, gtol=1e-6))
            if best is None or r.fun < best.fun: best = r
        like, pri = self.chi2(D, best.x)
        return dict(chi2=like + pri, like=like, prior=pri, nuis=best.x.tolist(), N=self.N)


class ACT:
    def __init__(self):
        from astropy.io import fits
        h = fits.open(ACTF)
        wins = {}
        for x in h:
            if x.name == "window:Bandpower":
                wins[int(x.header["SACCNAME"])] = (np.asarray(x.data["values"]), np.asarray(x.data["weight"]))
        self.rows = []; d = []
        for nm, pol in (("data:cl_00", "tt"), ("data:cl_0e", "te"), ("data:cl_ee", "ee")):
            t = h[nm].data
            for r in t:
                d.append(r["value"]); self.rows.append((pol, int(r["window"]), int(r["window_ind"])))
        self.d = np.array(d); cov = np.asarray(h["covariance"].data, dtype=np.float64)
        assert cov.shape == (len(self.d), len(self.d))
        self.Ci = np.linalg.inv(cov); self.N = len(self.d)
        # dense window matrix per pol: W[pol] (nbin_pol x nL) and the L values
        self.L = None; self.W = {}; self.sel = {}
        for pol in ("tt", "te", "ee"):
            ii = [k for k, r in enumerate(self.rows) if r[0] == pol]; self.sel[pol] = np.array(ii)
            ls, w = wins[self.rows[ii[0]][1]]
            self.W[pol] = np.array([w[:, self.rows[k][2]] for k in ii]); self.Lp = ls
        self.lmax = int(max(wins[k][0].max() for k in wins))
        self.npol = {"tt": 0, "te": 1, "ee": 2}

    def theory_bins(self, D):
        t = np.zeros(self.N)
        for pol in ("tt", "te", "ee"):
            t[self.sel[pol]] = self.W[pol] @ D[pol][self.Lp]
        return t

    def chi2(self, D, p, t=None):
        if t is None: t = self.theory_bins(D)
        A, P = p; s = np.zeros(self.N)
        for pol in ("tt", "te", "ee"):
            s[self.sel[pol]] = 1.0 / (A * A * P ** self.npol[pol])
        r = self.d - t * s
        return float(r @ self.Ci @ r)

    def profile(self, D, x0=None):
        t = self.theory_bins(D)
        f = lambda p: self.chi2(D, p, t)
        best = None
        for s in ([np.array([1.0, 1.0])] if x0 is None else [np.asarray(x0), np.array([1.0, 1.0])]):
            r = minimize(f, s, method="L-BFGS-B", bounds=[(0.5, 1.5), (0.9, 1.1)], options=dict(ftol=1e-13))
            if best is None or r.fun < best.fun: best = r
        return dict(chi2=float(best.fun), like=float(best.fun), prior=0.0, nuis=best.x.tolist(), N=self.N)


P_FULL = {"143x143": (30, 2000), "217x217": (500, 2500), "143x217": (500, 2500), "TE": (30, 2000), "EE": (30, 2000)}
P_CUT = {"143x143": (30, 1000), "217x217": (500, 1000), "143x217": (500, 1000), "TE": (30, 600), "EE": (30, 600)}
_LIK = {}


def lik(name):
    if name not in _LIK:
        _LIK[name] = {"P": lambda: CamSpec(P_FULL), "Pcut": lambda: CamSpec(P_CUT), "A": ACT}[name]()
    return _LIK[name]


def grade_spectra(D, which=("Pcut", "A"), x0=None):
    """profiled chi^2 per likelihood; PA = Pcut + A. Returns dict."""
    out = {}
    for w in which:
        out[w] = lik(w).profile(D, None if x0 is None else x0.get(w))
    if "Pcut" in out and "A" in out:
        out["PA"] = out["Pcut"]["chi2"] + out["A"]["chi2"]
    return out

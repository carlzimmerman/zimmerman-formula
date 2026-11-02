#!/usr/bin/env python3
"""TG1 shared: loads, split stacks, joint fit, mock engine (FROZEN_CRITERIA.md). Read-only inputs. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from astropy.io import fits
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MUT = os.environ.get("TG1_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
SEED = 20261102; FEET = ("canonical", "alt"); HS = ("h0672", "h0686"); HI = {"h0672": 1, "h0686": 2}; HX = {"h0672": 0, "h0686": 1}
BANDS = dict(MID=[3, 4, 5], IM=[1, 2, 3, 4, 5]); A0 = dict(canonical=9.3603e-11, alt=1.1312e-10)
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); NALL = len(X["name"]); NAMES = [str(s).strip() for s in X["name"]]
def dump(fs="034"): return np.load(os.path.join(RB, "LM1_law_missing_mass_map", f"cache_BASE_f{fs}", "dump.npz"))
E_ = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; EN = {str(s).strip(): i for i, s in enumerate(E_["NAME"])}; JI = np.array([EN[n] for n in NAMES])
def col(c): return np.asarray(E_[c], float)[JI]
CAT = {c: col(c) for c in ("KT", "KT_L", "KT_H", "MGAS500", "MGAS500_L", "MGAS500_H", "M500", "L300kpc", "BEST_Z")}
if MUT:
    p_ = np.random.default_rng(2112).permutation(NALL)
    for c in ("KT", "KT_L", "KT_H"): CAT[c] = CAT[c][p_]
def nW(h):
    i = HI[h]; W = np.where(X["E"][:, i] < 1e8, 1 / X["E"][:, i] ** 2, 0); B = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0); return W * B[None, :] * (X["D"][:, i] - X["leakP"][:, HX[h], 0]), W
def sig_lg(v, lo, hi):
    s = 0.5 * (np.log10(v / lo) + np.log10(hi / v)); return np.where(np.isfinite(s) & (s > 0), s, np.nan)
def sample(foot, h, band="MID", fs="034"):
    d = dump(fs); q = f"{foot}_{h}"; n, W = nW(h); V = d["V_" + q]; VN = d["VN_" + q]; J = BANDS[band]
    ok = np.isfinite(CAT["KT"]) & (CAT["KT"] > 0) & (W[:, J].sum(1) > 0); I = np.where(ok)[0]
    t = np.log10(CAT["KT"][I] / np.median(CAT["KT"][I])); g = np.log10(CAT["MGAS500"][I] / np.median(CAT["MGAS500"][I]))
    st = sig_lg(CAT["KT"][I], CAT["KT_L"][I], CAT["KT_H"][I]); sg = sig_lg(CAT["MGAS500"][I], CAT["MGAS500_L"][I], CAT["MGAS500_H"][I]); ms = (int(np.isnan(st).sum()), int(np.isnan(sg).sum()))
    st = np.where(np.isnan(st), np.nanmedian(st), st); sg = np.where(np.isnan(sg), np.nanmedian(sg), sg)
    return dict(I=I, n=n[I][:, J], W=W[I][:, J], V=V[I][:, J], VN=VN[I][:, J], t=t, g=g, st=st, sg=sg, ms=ms, M=np.log10(CAT["M500"][I]), PATCH=d["PATCH"][I], z=np.log10(1 + CAT["BEST_Z"][I]), L300=np.log10(CAT["L300kpc"][I] / np.nanmedian(CAT["L300kpc"][I])), foot=foot, h=h, band=band)
def gamma_ij(S):
    nu = np.where(S["VN"] > 0, S["V"] / np.where(S["VN"] > 0, S["VN"], 1), np.nan); iy = np.clip((nu - .5) ** 2 - .25, 1e-6, None); y = 1 / iy; gg = y / 2 + np.sqrt(y * y / 4 + y); dg = .5 + (y / 2 + 1) / (2 * np.sqrt(y * y / 4 + y)); o = y * dg / gg
    return np.where(np.isfinite(o), o, .75)
def _split(e, w, fix, var):
    o = np.argsort(fix, kind="stable"); N = len(o); nu = de = 0.0
    for k in range(3):
        c = o[k * N // 3:(k + 1) * N // 3]; v = var[c]; m = np.median(v); hi = c[v > m]; lo = c[v <= m]; Wh, Wl = w[hi].sum(), w[lo].sum()
        om = 1 / (1 / Wh + 1 / Wl); nu += om * (e[hi].sum() / Wh - e[lo].sum() / Wl); de += om * ((w[hi] * v[v > m]).sum() / Wh - (w[lo] * v[v <= m]).sum() / Wl)
    return nu / de
def split_pair(e, w, t, g): return _split(e, w, g, t), _split(e, w, t, g)
def cells(fix, var):
    o = np.argsort(fix, kind="stable"); N = len(o); out = []
    for k in range(3):
        c = o[k * N // 3:(k + 1) * N // 3]; v = var[c]; m = np.median(v); out.append((c[v > m], c[v <= m]))
    return out
def split_w(C, e, w, var, c=None):
    """split on fixed cell assignment C with cluster weights c: (R,) or scalar."""
    c = np.ones_like(e) if c is None else c; nu = de = 0.0
    for hi, lo in C:
        Wh, Wl = (c[..., hi] * w[hi]).sum(-1), (c[..., lo] * w[lo]).sum(-1); om = 1 / (1 / Wh + 1 / Wl)
        nu = nu + om * ((c[..., hi] * e[hi]).sum(-1) / Wh - (c[..., lo] * e[lo]).sum(-1) / Wl); de = de + om * ((c[..., hi] * w[hi] * var[hi]).sum(-1) / Wh - (c[..., lo] * w[lo] * var[lo]).sum(-1) / Wl)
    return nu / de
def joint(e, w, cols, c=None):
    """e_i = w_i (theta . cols): weighted LS with noise var ~ w_i. Returns theta."""
    X_ = np.c_[tuple(cols)]; c = np.ones_like(e) if c is None else c; F = (X_ * (c * w)[:, None]).T @ X_; b = X_.T @ (c * e); return np.linalg.solve(F, b)
GRID = np.arange(-3, 3.0001, .01)
def marginal(e, wphi, x):
    F = 10 ** np.outer(GRID, x); nu = (e * F).sum(1); de = (wphi[None, :] * F * F / 1).sum(1); return float(GRID[int(np.argmax(nu * nu / de))])
class Mock:
    def __init__(s, S, seed):
        s.S = S; s.seed = seed; n, W, V = S["n"], S["W"], S["V"]; e = n - V; s.N = len(S["t"]); phi = np.clip(e.sum(0) / W.sum(0), 0, None); s.phi = phi; s.Wphi = (W * phi).sum(1); s.w = W.sum(1); s.e = e.sum(1)
        s.r = (e - W * phi).sum(1); s.gam = gamma_ij(S); s.V = V; x = np.c_[S["t"], S["g"]]; mu = x.mean(0); Cint = np.cov(x.T) - np.diag([np.mean(S["st"] ** 2), np.mean(S["sg"] ** 2)])
        w_, v_ = np.linalg.eigh(Cint); Cint = (v_ * np.clip(w_, .02 ** 2, None)) @ v_.T; s.Cint = Cint; Pi = np.linalg.inv(Cint); s.pm = np.zeros((s.N, 2)); s.pL = np.zeros((s.N, 2, 2))
        for i in range(s.N):
            Pe = np.diag([1 / S["st"][i] ** 2, 1 / S["sg"][i] ** 2]); Cp = np.linalg.inv(Pi + Pe); s.pm[i] = Cp @ (Pi @ mu + Pe @ x[i]); s.pL[i] = np.linalg.cholesky(Cp)
        s.alpha = marginal(s.e, s.Wphi, S["t"]); s.beta = marginal(s.e, s.Wphi, S["g"])
    def draw(s, rng, hyp, nuis=1.0, terr=1.0, a=None, b=None, patch=False, eps_x=1.0, gerr=1.0):
        S = s.S; N = s.N; a = s.alpha if a is None else a; b = s.beta if b is None else b
        tr = s.pm + (s.pL @ rng.standard_normal((N, 2, 1)))[..., 0]; tt, gt = tr[:, 0], tr[:, 1]
        rho = rng.uniform(-.5, .5) * (nuis > 0); z1 = rng.standard_normal(N); z2 = rho * z1 + np.sqrt(1 - rho * rho) * rng.standard_normal(N)
        eps = rng.normal(0, .10 * eps_x) * nuis; d = rng.normal(0, .05) * nuis; tau = rng.normal(0, .15) * nuis; m = rng.normal(0, .02) * nuis
        to = tt + terr * S["st"] * z1 + tau * tt; go = gt + gerr * S["sg"] * z2 + eps * (S["M"] - np.median(S["M"])) + d
        pl = {"H0": np.ones(N), "HT": 10 ** (a * tt), "HG": 10 ** (b * gt), "Hboth": 10 ** (.5 * a * tt + .5 * b * gt)}[hyp]; pl = pl / ((s.Wphi * pl).sum() / s.Wphi.sum())
        if patch: sg = rng.choice([-1., 1.], 64)[S["PATCH"].astype(int)]
        else: sg = rng.choice([-1., 1.], N)
        Vt = (s.V * 10 ** ((gt - S["g"])[:, None] * s.gam)).sum(1); Vo = (s.V * 10 ** ((go - S["g"])[:, None] * s.gam)).sum(1)
        n = (Vt + s.Wphi * pl + sg * s.r) * (1 + m); return n - Vo, s.w, to, go
def Fsep(a, b): return float(abs(a.mean() - b.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
NM = 2000
def run(mk, key, nm=NM, s0=None, **kw):
    """returns Z clouds per hypothesis (train, fresh)."""
    def cloud(hyp, k, n):
        rg = np.random.default_rng([SEED, key, k]); o = np.zeros((n, 2))
        for r in range(n):
            e, w, t, g = mk.draw(rg, hyp, **kw); o[r] = split_pair(e, w, t, g)
        return o
    H0 = cloud("H0", 0, nm); s = H0.std(0, ddof=1); Z = {"H0": H0 / s}
    for k, hy in enumerate(("HT", "HG", "Hboth"), 1): Z[hy] = cloud(hy, k, nm) / s
    fr = {hy: cloud(hy, 10 + k, nm) / s for k, hy in enumerate(("HT", "HG"))}
    F = Fsep(Z["HT"][:, 0] - Z["HT"][:, 1], Z["HG"][:, 0] - Z["HG"][:, 1])
    mu = {h: Z[h].mean(0) for h in ("HT", "HG")}; Ci = {h: np.linalg.inv(np.cov(Z[h].T)) for h in ("HT", "HG")}
    def md(x, h): d = x - mu[h]; return np.einsum("ij,jk,ik->i", d, Ci[h], d)
    acc = dict(HT=float((md(fr["HT"], "HT") < md(fr["HT"], "HG")).mean()), HG=float((md(fr["HG"], "HG") < md(fr["HG"], "HT")).mean()))
    return dict(F=F, acc=acc, s=s.tolist(), a=mk.alpha, b=mk.beta, Z_mean={h: Z[h].mean(0).tolist() for h in Z}, Z_sd={h: Z[h].std(0, ddof=1).tolist() for h in Z}, H0=Z["H0"], HTz=Z["HT"], HGz=Z["HG"], N=mk.N)
def row(r): return f"F {r['F']:.2f} acc HT {r['acc']['HT']:.3f} HG {r['acc']['HG']:.3f} | HT Z_T {r['Z_mean']['HT'][0]:+.2f}+-{r['Z_sd']['HT'][0]:.2f} Z_G {r['Z_mean']['HT'][1]:+.2f}+-{r['Z_sd']['HT'][1]:.2f} | HG Z_T {r['Z_mean']['HG'][0]:+.2f}+-{r['Z_sd']['HG'][0]:.2f} Z_G {r['Z_mean']['HG'][1]:+.2f}+-{r['Z_sd']['HG'][1]:.2f} | Hboth Z_T {r['Z_mean']['Hboth'][0]:+.2f} Z_G {r['Z_mean']['Hboth'][1]:+.2f}"

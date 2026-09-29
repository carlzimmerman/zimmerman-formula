"""CFG108 POST HOC diagnostics (every row here is post hoc, written after the frozen main run; nothing is a pass line).
 (a) K8c: why the near/far weight-per-pair check (frozen threshold 0.90) gave 0.64.
 (b) which amplitude weighting reproduces CFG116's five amplitude/dilution digits (CFG110's R2b definition was not read).
"""
import os, math, warnings
import numpy as np
from scipy import stats
warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
def find_repo():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "real_research", "data", "lensing_rar")): return env
    p = HERE
    for _ in range(14):
        if os.path.isdir(os.path.join(p, "real_research", "data", "lensing_rar")): return p
        p = os.path.dirname(p)
    raise RuntimeError("set ZF_REPO")
DATA = os.path.join(find_repo(), "real_research", "data", "lensing_rar")
NP = 50; KG = 1.98847e30 / (3.0857e16) ** 2
lens = np.load(os.path.join(DATA, "lr_lenses.npz")); z, typ = lens["z"], lens["typ"]
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
p = np.load(os.path.join(DATA, "cfg116_perlens.npz"))
WGn, WWn, NNn, WGf, WWf, NNf = (p[k] for k in ("WGn", "WWn", "NNn", "WGf", "WWf", "NNf"))
K1 = np.arange(8, 15)
# (a)
print("== (a) K8c diagnostic (K1 bins)")
for k in K1:
    m = (NNn[:, k] > 0) & (NNf[:, k] > 0)
    wn = WWn[m, k] / NNn[m, k]; wf = WWf[m, k] / NNf[m, k]
    print("  bin %d: lens-bins with both %6d ; frac(near<far) %.3f ; median near/far weight-per-pair %.3f ; pooled sum ratio (WWn/NNn)/(WWf/NNf) %.3f ; near pairs share %.3f" %
          (k, m.sum(), (wn < wf).mean(), np.median(wn / wf), (WWn[:, k].sum() / NNn[:, k].sum()) / (WWf[:, k].sum() / NNf[:, k].sum()), NNn[:, k].sum() / (NNn[:, k].sum() + NNf[:, k].sum())))
for lo, hi in ((0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5)):
    zz = (z >= lo) & (z < hi)
    wn = WWn[zz][:, K1].sum() / NNn[zz][:, K1].sum(); wf = WWf[zz][:, K1].sum() / NNf[zz][:, K1].sum()
    print("  lens z [%.1f,%.1f): pooled weight-per-pair near %.4g far %.4g ratio %.3f ; far pair fraction %.3f" % (lo, hi, wn, wf, wn / wf, NNf[zz][:, K1].sum() / (NNf[zz][:, K1].sum() + NNn[zz][:, K1].sum())))
# (b)
def psum(arr):
    key = patch * 2 + typ
    return np.stack([np.bincount(key, weights=arr[:, k], minlength=NP * 2) for k in range(15)], 1).reshape(NP, 2, 15)
S = {"WGn": psum(WGn), "WWn": psum(WWn), "WGf": psum(WGf), "WWf": psum(WWf)}
S["WGa"] = S["WGn"] + S["WGf"]; S["WWa"] = S["WWn"] + S["WWf"]
T = {k: v.sum(0) for k, v in S.items()}
Tm = {k: T[k][None] - S[k] for k in T}
def esd(D, s): return D["WG" + s] / D["WW" + s] / KG
def amp(D, s, wfn, c1=1, c0=0):
    e = esd(D, s)[..., K1]; w = wfn(D, s)
    return np.log10((w * e[..., c1, :]).sum(-1) / (w * e[..., c0, :]).sum(-1))
def dil(D, c, wfn):
    a = esd(D, "f")[..., c, K1]; b = esd(D, "n")[..., c, K1]; w = wfn(D, "f")
    return np.log10((w * a).sum(-1) / (w * b).sum(-1))
def err(fn):
    f = fn(T); J = fn(Tm)
    return float(f), float(np.sqrt((NP - 1) / NP * ((J - J.mean()) ** 2).sum()))
Wfix_all = T["WWa"].sum(0)[K1]
variants = {
    "V1 fixed all-source WW (mine)": lambda D, s: Wfix_all[None, :] if False else Wfix_all,
    "own-set total WW (both classes)": lambda D, s: T["WW" + s].sum(0)[K1],
    "own-set class-late WW": lambda D, s: T["WW" + s][0, K1],
    "own-set class-early WW": lambda D, s: T["WW" + s][1, K1],
    "unweighted mean": lambda D, s: np.ones(7),
    "per-sample own WW (denominator class late, jackknifed)": lambda D, s: D["WW" + s][..., 0, K1],
    "per-sample own WW (both classes, jackknifed)": lambda D, s: D["WW" + s].sum(-2)[..., K1],
    "inverse-variance (1/sigma_D^2 all-source)": None,
}
# inverse variance weights from the all-source early-late D jackknife errors
De = lambda D: esd(D, "a")[..., 1, :][..., K1] - esd(D, "a")[..., 0, :][..., K1]
Jd = De(Tm); sd = np.sqrt((NP - 1) / NP * ((Jd - Jd.mean(0)) ** 2).sum(0))
variants["inverse-variance (1/sigma_D^2 all-source)"] = lambda D, s: 1 / sd ** 2
target = dict(near=(0.20, 0.06), far=(0.17, 0.05), all=(0.18, 0.04), late=(0.13, 0.08), early=(0.09, 0.04))
print("\n== (b) amplitude weighting variants (CFG116: near 0.20+-0.06, far 0.17+-0.05, all 0.18+-0.04, dil late 0.13+-0.08, dil early 0.09+-0.04)")
for nm, wf in variants.items():
    row = []
    for s, lab in (("n", "near"), ("f", "far"), ("a", "all")):
        row.append((lab,) + err(lambda D, s=s: amp(D, s, wf)))
    for c, lab in ((0, "late"), (1, "early")):
        row.append((lab,) + err(lambda D, c=c: dil(D, c, wf)))
    hit = sum(1 for (lab, a, e) in row if abs(a - target[lab][0]) <= 0.0051 and abs(e - target[lab][1]) <= 0.0051)
    print("  %-52s " % nm + "  ".join("%s %+.3f+-%.3f" % r for r in row) + "   digits matched %d/5" % hit)
# pooled-ESD variant (V2) and 'sum WG ratio'
def v2(D, s): a = D["WG" + s][..., :, K1].sum(-1) / D["WW" + s][..., :, K1].sum(-1); return np.log10(a[..., 1] / a[..., 0])
def sw(D, s): a = D["WG" + s][..., :, K1].sum(-1); return np.log10(a[..., 1] / a[..., 0])
for nm, fn in (("V2 pooled-ESD ratio", v2), ("ratio of summed WG (no weight division)", sw)):
    print("  %-52s " % nm + "  ".join("%s %+.3f+-%.3f" % ((lab,) + err(lambda D, s=s: fn(D, s))) for s, lab in (("n", "near"), ("f", "far"), ("a", "all"))))

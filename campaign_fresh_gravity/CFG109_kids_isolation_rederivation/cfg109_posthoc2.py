"""CFG109 post hoc 2 (labelled): diagnose the C9 failure (group-permutation z(delta) null mean -0.455 rather than 0).  Is it the mean of r=D_non-D_iso under the
permutation (conditioning on the fixed base sums), or the re-estimated P?  300 permutations, seed 2109."""
import os, math, numpy as np, warnings
warnings.filterwarnings("ignore")
def find_repo():
    e = os.environ.get("ZF_REPO")
    if e: return e
    p = os.getcwd()
    for _ in range(14):
        if os.path.isdir(os.path.join(p, "real_research", "data", "lensing_rar")): return p
        p = os.path.dirname(p)
    raise RuntimeError("ZF_REPO")
D = os.path.join(find_repo(), "real_research", "data", "lensing_rar")
L = np.load(D + "/lr_lenses.npz"); typ, z, Mgal = L["typ"], L["z"], L["Mgal"]; nL = len(z)
patch = np.load(D + "/lr_esd_jackknife.npz")["patch"]; P = np.load(D + "/cfg110_perlens.npz")
f20 = np.load(D + "/cfg96_isoflags.npz")["f20"].astype(bool)
K1 = np.arange(8, 15); NP = 50; KG = 1.98847e30 / (3.0857e16) ** 2
WG, WW = P["WG"][:, K1], P["WW"][:, K1]
mb = np.zeros(nL, int)
for c in (0, 1):
    m = typ == c; q = np.quantile(np.log10(Mgal[m]), np.linspace(0, 1, 9)[1:-1]); mb[m] = np.searchsorted(q, np.log10(Mgal[m]))
zb = np.minimum(((z - 0.1) / 0.08).astype(int), 4); cell = (typ * 8 + mb) * 5 + zb
key = patch * 2 + typ; block = (patch * 2 + typ) * 80 + (cell % 40)
def s7(m):
    out = np.empty((2, NP * 2, 7)); w = m.astype(float)
    for j in range(7):
        out[0, :, j] = np.bincount(key, weights=WG[:, j] * w, minlength=NP * 2); out[1, :, j] = np.bincount(key, weights=WW[:, j] * w, minlength=NP * 2)
    return out.reshape(2, NP, 2, 7)
d7 = lambda s: (s[0] / s[1] / KG)[..., 1, :] - (s[0] / s[1] / KG)[..., 0, :]
sB = s7(np.ones(nL, bool))
def rr(sI):
    sN = sB - sI; TI, TN = sI.sum(1), sN.sum(1)
    return d7(TN) - d7(TI), d7(TN[:, None] - sN) - d7(TI[:, None] - sI)
covJ = lambda J: (NP - 1) / NP * np.einsum("pi,pj->ij", J - J.mean(0), J - J.mean(0))
h = 41 / 49
rf0, J0 = rr(s7(f20)); C0 = covJ(J0); P0 = h * np.linalg.inv(C0)
s = d7(sB.sum(1))
rng = np.random.default_rng(2109); idxb = np.argsort(block, kind="stable")
R = []; Zf = []; Zr = []
for b in range(300):
    order = np.lexsort((rng.random(nL), block)); fn = np.empty(nL, bool); fn[idxb] = f20[order]
    rf, Jl = rr(s7(fn)); R.append(rf)
    Zf.append(float(s @ P0 @ rf) / math.sqrt(float(s @ P0 @ s)))
    Pl = h * np.linalg.inv(covJ(Jl)); Zr.append(float(s @ Pl @ rf) / math.sqrt(float(s @ Pl @ s)))
R = np.array(R)
print("mean of permuted r per bin:", np.round(R.mean(0), 2), " (sd/sqrt(300):", np.round(R.std(0) / math.sqrt(300), 2), ")")
print("z(delta) with FIXED observed P: mean %+.3f std %.3f ; with re-estimated P: mean %+.3f std %.3f" % (np.mean(Zf), np.std(Zf), np.mean(Zr), np.std(Zr)))
print("observed r:", np.round(rf0, 2), " z_obs (fixed P) %.3f" % (float(s @ P0 @ rf0) / math.sqrt(float(s @ P0 @ s))))

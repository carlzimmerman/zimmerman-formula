"""CFG108 POST HOC 2 (all rows post hoc, after the frozen main run).
 (a) power of the two nulls with the PERMUTATION-calibrated critical value (the permuted null q99 exceeds the chi2_7 q99);
 (b) amplitude difference near - far (V1) and what near/far ratio q of a source-separation-dependent systematic the near/far test can exclude
     when that systematic would explain the whole far split;
 (c) are the 50 patches spatially contiguous (ra, dec extents)?
"""
import os, math, json, warnings
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
res = json.load(open(os.path.join(HERE, "cfg108_results.json")))
NP = 50; KG = 1.98847e30 / (3.0857e16) ** 2
lens = np.load(os.path.join(DATA, "lr_lenses.npz")); z, typ, ra, dec = lens["z"], lens["typ"], lens["ra"], lens["dec"]
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
p = np.load(os.path.join(DATA, "cfg116_perlens.npz"))
K1 = np.arange(8, 15)
def psum(arr):
    key = patch * 2 + typ
    return np.stack([np.bincount(key, weights=arr[:, k], minlength=NP * 2) for k in range(15)], 1).reshape(NP, 2, 15)
S = {"WGn": psum(p["WGn"]), "WWn": psum(p["WWn"]), "WGf": psum(p["WGf"]), "WWf": psum(p["WWf"])}
S["WGa"] = S["WGn"] + S["WGf"]; S["WWa"] = S["WWn"] + S["WWf"]; S["WX"] = psum(p["WX"])
T = {k: v.sum(0) for k, v in S.items()}; Tm = {k: T[k][None] - S[k] for k in T}
w = T["WWa"].sum(0)[K1]
esd = lambda D, s: D["WG" + s] / D["WW" + s] / KG
def amp(D, s):
    e = esd(D, s)[..., K1]; return np.log10((w * e[..., 1, :]).sum(-1) / (w * e[..., 0, :]).sum(-1))
def fn(D): return np.stack([amp(D, "n"), amp(D, "f")], -1)
f = fn(T); J = fn(Tm); d = J - J.mean(0); C = (NP - 1) / NP * d.T @ d
diff = f[0] - f[1]; sd = math.sqrt(C[0, 0] + C[1, 1] - 2 * C[0, 1])
print("== (b) A_near - A_far (V1, dex) = %+.3f +- %.3f  (near %+.3f +- %.3f, far %+.3f +- %.3f, corr %.2f)" % (diff, sd, f[0], math.sqrt(C[0, 0]), f[1], math.sqrt(C[1, 1]), C[0, 1] / math.sqrt(C[0, 0] * C[1, 1])))
ul = diff + 1.645 * sd; ll = diff - 1.645 * sd
print("   95%% one-sided upper limit on near-far amplitude excess: %.3f dex; lower limit %.3f dex" % (ul, ll))
# a systematic with ESD ratio factor: near ESD multiplied by (1+s_n), far by (1+s_f), both early-only; log10 excess in each amplitude = log10(1+s)
# if the WHOLE far split (10^A_far) were systematic: 1 + s_f = 10^A_far ; near: 1 + s_n = (1+s_f)^(1/q) with q = s_f/s_n in log space
A_far = f[1]
print("   whole-far-split-as-systematic scenario (log-amplitude q = far/near systematic ratio): near excess = A_far/q ; predicted A_near - A_far = A_far (1/q - 1)")
for q in (1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3):
    pred = A_far * (1 / q - 1)
    print("     q %.1f: predicted near-far %.3f dex ; excluded at 95%% (pred > UL %.3f)? %s ; z of data vs pred %.2f" % (q, pred, ul, "YES" if pred > ul else "no", (diff - pred) / sd))
qstar = A_far / (A_far + ul)
print("   near/far test excludes q < %.2f (one-sided 95%%): a separation-dependent systematic explaining the far split must have far/near ratio above this" % qstar)
# (a) permutation-calibrated power
PERM = res["permutation"]
lam = {e: res["R0"][str(e)] for e in (0.25, 0.5, 0.75, 1.0)}
print("\n== (a) power with the chi2_7 critical value (18.48) vs the permutation q99 (cross %.2f, near/far %.2f)" % (PERM["cross difference"]["q99"], PERM["near-minus-far"]["q99"]))
for e in (0.25, 0.5, 0.75, 1.0):
    lx, ln = lam[e]["lam_x"], lam[e]["lam_nf"]
    print("   eps %.2f: cross power chi2-crit %.3f, perm-crit %.3f | near/far %.3f, %.3f" % (e, stats.ncx2.sf(stats.chi2.ppf(.99, 7), 7, lx), stats.ncx2.sf(PERM["cross difference"]["q99"], 7, lx),
          stats.ncx2.sf(stats.chi2.ppf(.99, 7), 7, ln), stats.ncx2.sf(PERM["near-minus-far"]["q99"], 7, ln)))
# (c) patches contiguity
print("\n== (c) patch spatial extent: RA/Dec (deg)")
rr = []
for q in range(NP):
    m = patch == q
    r = ra[m]; dd = dec[m]
    rr.append((r.min(), r.max(), dd.min(), dd.max(), np.std(r), np.std(dd)))
rr = np.array(rr)
print("   whole sample: RA %.1f-%.1f (std %.1f), Dec %.1f-%.1f (std %.1f)" % (ra.min(), ra.max(), ra.std(), dec.min(), dec.max(), dec.std()))
print("   per-patch RA std: median %.1f (min %.1f max %.1f); Dec std median %.1f (min %.1f max %.1f)" % (np.median(rr[:, 4]), rr[:, 4].min(), rr[:, 4].max(), np.median(rr[:, 5]), rr[:, 5].min(), rr[:, 5].max()))
# nearest-neighbour test: fraction of neighbours in the same patch for 2000 random lenses
from scipy.spatial import cKDTree
rng = np.random.default_rng(3); idx = rng.choice(len(ra), 3000, replace=False)
xyz = np.stack([np.cos(np.radians(dec)) * np.cos(np.radians(ra)), np.cos(np.radians(dec)) * np.sin(np.radians(ra)), np.sin(np.radians(dec))], 1)
tr = cKDTree(xyz); dist, nb = tr.query(xyz[idx], k=6)
same = (patch[nb[:, 1:]] == patch[idx][:, None]).mean()
print("   fraction of the 5 nearest sky neighbours that share the lens's patch: %.3f (1/50 = 0.02 if patches were random labels)" % same)

"""CFG688 (criteria 6339815fe): CFG687's clusters re-binned by redMaPPer richness (X-ray-independent) -> IV slope of outer shear vs
bin-mean Mgas500, vs the law's and Newton's same-procedure slopes; Malmquist signature. MUTATE=1 shuffles lambda."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("MUTATE") == "1"
P = np.load(os.path.join(HERE, "..", "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
D, E, PL, PN, mg, z, ra, dec = (P[k] for k in ("D", "E", "PL", "PN", "mg", "z", "ra", "dec")); W = np.where(E > 0, 1/E**2, 0)
rm = np.array([list(map(float, l.split("\t"))) for l in open(os.path.join(HERE, "redmapper_z004_06.tsv"))])
lam = np.full(len(z), np.nan)
for i in range(len(z)):
    d = np.degrees(np.arccos(np.clip(np.sin(np.radians(dec[i]))*np.sin(np.radians(rm[:, 1])) + np.cos(np.radians(dec[i]))*np.cos(np.radians(rm[:, 1]))*np.cos(np.radians(ra[i] - rm[:, 0])), -1, 1)))*60
    ok = (d < 2.0) & (np.abs(rm[:, 2] - z[i]) < 0.04)
    if ok.any(): lam[i] = rm[ok][np.argmin(d[ok]), 3]
m = np.isfinite(lam); idx = np.where(m)[0]; print(f"matched {m.sum()} of {len(z)} (KiDS-N/SDSS overlap only; redMaPPer lambda >= 20)")
L = lam.copy()
if MUT: L[idx] = np.random.default_rng(688).permutation(lam[idx])
j = [6, 7]
def outer(sel, arr): return (W[sel][:, j]*arr[sel][:, j]).sum()/W[sel][:, j].sum()
def iv_slope(sel_idx, binvar, arr):
    q = np.quantile(binvar[sel_idx], [0, 1/3, 2/3, 1]); t = np.clip(np.digitize(binvar[sel_idx], q[1:-1]), 0, 2); xs, ys = [], []
    for k in range(3):
        s = np.zeros(len(z), bool); s[sel_idx[t == k]] = True; v = outer(s, arr)
        if v <= 0: return np.nan
        xs.append(np.log10(mg[s].mean())); ys.append(np.log10(v))
    return np.polyfit(xs, ys, 1)[0]
res = {"mutate": MUT, "n_matched": int(m.sum())}
rng = np.random.default_rng(1)
def boot(fun, n=1000):
    vals = [fun(rng.choice(idx, len(idx))) for _ in range(n)]; return float(np.nanstd(vals))
for name, bv in (("lambda", L), ("Mgas500", mg)):
    s_o = iv_slope(idx, bv, D); s_l = iv_slope(idx, bv, PL); s_n = iv_slope(idx, bv, PN); e = boot(lambda ii: iv_slope(ii, bv, D))
    res[f"binned_by_{name}"] = dict(s_obs=float(s_o), s_err=e, s_law=float(s_l), s_newton=float(s_n))
    print(f"binned by {name:8s}: s_obs = {s_o:.2f} ± {e:.2f}   s_law = {s_l:.2f}   s_Newton = {s_n:.2f}")
q = np.quantile(L[idx], [0, 1/3, 2/3, 1]); t = np.clip(np.digitize(L[idx], q[1:-1]), 0, 2); per = []
for k in range(3):
    s = np.zeros(len(z), bool); s[idx[t == k]] = True
    A = (W[s][:, j]*D[s][:, j]).sum()/(W[s][:, j]*PL[s][:, j]).sum()
    per.append(dict(n=int(s.sum()), lam_med=float(np.median(L[s])), Mgas_mean=float(mg[s].mean()), z_med=float(np.median(z[s])), A_outer=float(A)))
    print(f"  λ tercile {k}: N={s.sum()} λ~{np.median(L[s]):.0f} <Mgas>={mg[s].mean():.2e} z~{np.median(z[s]):.3f}  A_OUTER(law) {A:.2f}")
res["lambda_terciles"] = per
qm = np.quantile(mg[idx], [0, 1/3, 2/3, 1]); tm = np.clip(np.digitize(mg[idx], qm[1:-1]), 0, 2)
sig = [float(np.mean(mg[idx[tm == k]]/lam[idx[tm == k]])) for k in range(3)]; res["Mgas_over_lambda_by_Mgas_tercile"] = sig
print("  <Mgas500/λ> by Mgas tercile (low→high):", [f"{x:.2e}" for x in sig])
b = res["binned_by_lambda"]; so, se, sl, sn = b["s_obs"], b["s_err"], b["s_law"], b["s_newton"]
mg_steep = res["binned_by_Mgas500"]["s_obs"]
if m.sum() < 60: v = "NOT DECIDED (fewer than 60 matches)"
elif abs(so - sl) < 2*se and mg_steep - sl >= 2*res["binned_by_Mgas500"]["s_err"]: v = "SELECTION ARTEFACT"
elif abs(so - sl) >= 2*se and abs(so - sn) < 2*se: v = "REAL sqrt(M) FAILURE"
else: v = "NOT DECIDED"
res["verdict"] = v; print("VERDICT:", v)
json.dump(res, open(os.path.join(HERE, "cfg688_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)

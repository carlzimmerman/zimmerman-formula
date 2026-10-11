"""CFG589 POST HOC (disclosed; prompted by the MUTATE draw reaching Z ~2): empirical null of the within-class slopes.
100 random shuffles of dc within (class x mass bin), construction A, canonical, K9. Compares real slopes with the null
spread, and checks whether the jackknife error matches the null scatter (calibration of every Z in CFG585-589)."""
import os, io, json, math, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
for v in ("CFG585_MUTATE", "CFG531_MUTATE", "CFG589_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, comps, all_bands, BANDS, NPATCH = (ns[k] for k in ("U", "F30", "TYP", "LMSL", "esd_loo", "comps", "all_bands", "BANDS", "NPATCH"))
HART3 = (NPATCH - 3 - 2) / (NPATCH - 1)
prep = {}
for cls, t in (("early", 1), ("late", 0)):
    C = F30 & (TYP == t); qb = np.quantile(LMSL[C], np.linspace(0, 1, 11)); qb[-1] += 1e-9
    bins = [np.where(C & (LMSL >= qb[i]) & (LMSL < qb[i + 1]))[0] for i in range(10)]
    prep[cls] = bins
def slopes(rng=None):
    out = {}
    for cls, bins in prep.items():
        ter = np.full(len(U), -1); dcs = np.full(len(U), np.nan)
        for idx in bins:
            dc = U[idx] - np.median(U[idx])
            if rng is not None: dc = rng.permutation(dc)
            dcs[idx] = dc; o = np.argsort(dc, kind="stable"); n = len(idx)
            for k in range(3): ter[idx[o[k * n // 3:(k + 1) * n // 3]]] = k
        y, Ls, d = [], [], []
        for k in range(3):
            m = ter == k; dd, Cc, Lj = esd_loo(m); cp = comps("A", "canonical", m); fb = all_bands(dd, Cc, cp)
            mM = cp["moster"][0] + cp["moster"][1]; y.append(fb["K9"]["eps"]); Ls.append((Lj[:, BANDS["K9"]] - mM[BANDS["K9"]][None, :]) @ np.array(fb["K9"]["wvec"])); d.append(np.median(dcs[m]))
        y = np.array(y); L = np.array(Ls).T; dev = L - L.mean(0); Cv = (NPATCH - 1) / NPATCH * dev.T @ dev / HART3
        X = np.column_stack([np.ones(3), d]); W = np.linalg.inv(Cv); A = X.T @ W @ X; b = np.linalg.solve(A, X.T @ W @ y)
        out[cls] = (b[1], math.sqrt(np.linalg.inv(A)[1, 1]))
    return out
real = slopes()
rng = np.random.default_rng(58901); null = {"early": [], "late": []}; jk = {"early": [], "late": []}
for i in range(100):
    s = slopes(rng)
    for c in null: null[c].append(s[c][0]); jk[c].append(s[c][1])
res = {}
for c in null:
    a = np.array(null[c]); p = (np.sum(a >= real[c][0]) + 1) / (len(a) + 1)
    res[c] = dict(real=real[c][0], real_jk_sig=real[c][1], null_mean=float(a.mean()), null_sd=float(a.std(ddof=1)), median_jk_sig_in_null=float(np.median(jk[c])),
                  p_one_sided=float(p), z_emp=float((real[c][0] - a.mean()) / a.std(ddof=1)), frac_null_Zjk_ge2=float(np.mean(a / np.array(jk[c]) >= 2)))
    print(f"{c:5s}: real slope {real[c][0]:+.2f} (jk sig {real[c][1]:.2f}); null mean {a.mean():+.2f} sd {a.std(ddof=1):.2f} (median jk sig in null {np.median(jk[c]):.2f}); "
          f"empirical p {p:.3f}, Z_emp {res[c]['z_emp']:+.2f}; fraction of null draws with jackknife Z >= 2: {res[c]['frac_null_Zjk_ge2']:.2f}")
json.dump(res, open(os.path.join(HERE, "cfg589_null_results.json"), "w"), indent=1)

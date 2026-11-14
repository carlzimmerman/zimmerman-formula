"""LGS4 POST HOC, second step (not frozen): rule P1 could not be evaluated because C_des_only - C_full for (w0, wa) is
singular within the chain noise: the legacy supernovae add information along one direction only. This script reports
the difference matrix, the one-direction version of the same statistic (projection on the leading eigenvector, 1 dof),
the per-axis one-dimensional versions, and the size of the leftover component against Monte Carlo noise (the spread
over the four chains). Reads the post hoc run files only."""
import json, os
import numpy as np
from scipy.stats import norm, chi2 as CHI2
HERE = os.path.dirname(os.path.abspath(__file__))
OUTF = open(os.path.join(HERE, "lgs4_posthoc_p1_rank1.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n")
def blk(r, which):
    nm = r["chain"]["names"] if which == "chain" else r["names"]; i = [nm.index("w0"), nm.index("wa")]
    c = np.array(r["chain"]["cov"] if which == "chain" else r["laplace"]["cov"])[np.ix_(i, i)]
    m = np.array(r["chain"]["mean"] if which == "chain" else r["best"]["x"])[i]
    return m, c
F = json.load(open(os.path.join(HERE, "lgs4_posthoc_full_cpl.json"))); D = json.load(open(os.path.join(HERE, "lgs4_posthoc_des_only_cpl.json")))
out = {}
for which in ("chain", "laplace"):
    mf, cf = blk(F, which); md, cd = blk(D, which); d = md - mf; Cd = cd - cf
    lam, V = np.linalg.eigh(Cd); v = V[:, 1] * np.sign(V[1, 1]); u = V[:, 0]
    t1 = float((v @ d) ** 2 / lam[1]); p1 = float(CHI2.sf(t1, 1))
    ax = d / np.sqrt(np.diag(Cd))
    rho_f = cf[0, 1] / np.sqrt(cf[0, 0] * cf[1, 1]); rho_d = cd[0, 1] / np.sqrt(cd[0, 0] * cd[1, 1])
    P(f"[{which}] full  (w0, wa) = ({mf[0]:+.4f}, {mf[1]:+.4f}), sd ({np.sqrt(cf[0, 0]):.4f}, {np.sqrt(cf[1, 1]):.4f}), correlation {rho_f:+.3f}")
    P(f"[{which}] DES   (w0, wa) = ({md[0]:+.4f}, {md[1]:+.4f}), sd ({np.sqrt(cd[0, 0]):.4f}, {np.sqrt(cd[1, 1]):.4f}), correlation {rho_d:+.3f}")
    P(f"[{which}] shift d = ({d[0]:+.4f}, {d[1]:+.4f}); C_des - C_full eigenvalues {lam[0]:+.3e}, {lam[1]:+.3e} (ratio {lam[0] / lam[1]:+.4f}); leading direction ({v[0]:+.3f}, {v[1]:+.3f})")
    P(f"[{which}] one-direction statistic: projection {v @ d:+.4f}, sd {np.sqrt(lam[1]):.4f} -> {abs(v @ d) / np.sqrt(lam[1]):.2f} sigma, p = {p1:.3f} (1 dof); "
      f"per axis: w0 {ax[0]:+.2f} sigma, wa {ax[1]:+.2f} sigma; leftover component {u @ d:+.5f}")
    out[which] = dict(mean_full=mf.tolist(), mean_des=md.tolist(), cov_full=cf.tolist(), cov_des=cd.tolist(), d=d.tolist(), eig=lam.tolist(), direction=v.tolist(),
                      projection=float(v @ d), sd=float(np.sqrt(lam[1])), sigma=float(abs(v @ d) / np.sqrt(lam[1])), p=p1, per_axis_sigma=ax.tolist(), leftover=float(u @ d))
# Monte Carlo noise from the thinned chains kept outside the repo (four chains of equal length, in order)
work = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_external_data", "lgs4_work"))
try:
    cf_ = np.load(os.path.join(work, "lgs4_posthoc_full_cpl_chain_thin20.npz"))["chain"]; cd_ = np.load(os.path.join(work, "lgs4_posthoc_des_only_cpl_chain_thin20.npz"))["chain"]
    v, u = np.array(out["chain"]["direction"]), None
    lam, V = np.linalg.eigh(np.array(out["chain"]["cov_des"]) - np.array(out["chain"]["cov_full"])); u = V[:, 0]
    rows = []
    for a, b in zip(np.array_split(cf_, 4), np.array_split(cd_, 4)):
        d = b[:, 3:5].mean(axis=0) - a[:, 3:5].mean(axis=0); Cd = np.cov(b[:, 3:5].T) - np.cov(a[:, 3:5].T)
        rows.append([float(v @ d), float(u @ d), float(v @ Cd @ v), float(u @ Cd @ u)])
    rows = np.array(rows); se = rows.std(axis=0, ddof=1) / 2
    P(f"Monte Carlo noise (spread over the four chains, as a standard error of the mean): projection {se[0]:.4f}, leftover {se[1]:.5f}, "
      f"variance along the leading direction {se[2]:.2e} (value {lam[1]:.2e}), along the other {se[3]:.2e} (value {lam[0]:+.2e})")
    out["mc_noise"] = dict(projection=float(se[0]), leftover=float(se[1]), var_leading=float(se[2]), var_other=float(se[3]), per_chain=rows.tolist())
except FileNotFoundError:
    P("thinned chains not found outside the repo: Monte Carlo noise not computed")
json.dump(out, open(os.path.join(HERE, "lgs4_posthoc_p1_rank1.json"), "w"), indent=1)

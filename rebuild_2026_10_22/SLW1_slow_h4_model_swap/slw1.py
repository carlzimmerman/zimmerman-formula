"""SLW1 (criteria e6dae9e270): within-slow slope of KU2's law residual on integrated h4, under each of DynPop's ten JAM
models; cylindrical minus spherical per mass pair. Run: python3 -I slw1.py [MUTATE]. Seconds, single thread.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json
import numpy as np
from astropy.io import fits
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); MODE = sys.argv[1] if len(sys.argv) > 1 else "REAL"
KU2 = os.path.join(RB, "KU2_kappa_universality_model_choice", "ku2.py"); OUT = []; RES = {"lane": "SLW1", "mode": MODE}
def P(s=""): print(s, flush=True); OUT.append(s)
argv = sys.argv; sys.argv = ["ku2.py"]; src = open(KU2).read().split("ok1 = slow.sum()")[0]
K = {"__file__": KU2, "__name__": "ku2"}; exec(compile(src, "ku2.py", "exec"), K); sys.argv = argv
dprow = np.flatnonzero(K["sel"]); pos = {int(r): i for i, r in enumerate(dprow)}
with fits.open(K["F"]) as h:
    BETA = np.array([np.array(h[i].data["beta_z" if i % 2 == 0 else "beta_r"], float)[K["sel"]] for i in range(2, 12)])
NAMES = [f"HDU{i} {'cyl' if i % 2 == 0 else 'sph'} {['MFL', 'NFW', 'fixNFW', 'gNFW', 'PL'][(i - 2) // 2]}" for i in range(2, 12)]
ki, h4, new = [], [], []
for csvf, fitf, isnew in ((os.path.join(RB, "LAM4_whole_galaxy_absorption", "lam4_sample.csv"), os.path.join(RB, "LAM4_whole_galaxy_absorption", "lam4_fit.jsonl"), 0),
                          (os.path.join(RB, "LAM7_orbit_shape_full_sample", "lam7_sample.csv"), os.path.join(RB, "LAM7_orbit_shape_full_sample", "lam7_fit.jsonl"), 1)):
    F = {json.loads(l)["plateifu"]: json.loads(l) for l in open(fitf)}
    for l in open(csvf).readlines()[1:]:
        s = l.strip().split(","); r = int(s[2]); f = F.get(s[3])
        if r in pos and f and f["status"] == "ok" and f["sigma"] > 0 and abs(f["h4"]) < 0.3 and K["sig"][pos[r]] >= 100:
            ki.append(pos[r]); h4.append(f["h4"]); new.append(isnew)
ki, h4, new = np.array(ki), np.array(h4), np.array(new, bool); sl = K["slow"][ki]; cell = K["cell"][ki]
iqr = float(np.subtract(*np.percentile(h4, [75, 25])))
P(f"SLW1 mode {MODE}. Sigma_Re >= 100: {len(ki)} galaxies, slow {int(sl.sum())}, IQR(h4) {iqr:.4f}")
rng = np.random.default_rng(20261105)
if MODE == "MUTATE":
    h4 = h4.copy()
    for c in np.unique(cell[sl]): j = np.flatnonzero(sl & (cell == c)); h4[j] = h4[j][rng.permutation(len(j))]
def E(r, h, grp):
    a = np.full(len(r), np.nan); b = np.full(len(r), np.nan)
    for g in np.unique(grp):
        m = grp == g
        if m.sum() >= 3: a[m] = r[m] - r[m].mean(); b[m] = h[m] - h[m].mean()
    m = np.isfinite(a) & np.isfinite(b)
    return (float(np.sum(a[m] * b[m]) / np.sum(b[m] ** 2) * iqr) if m.sum() > 2 else np.nan), int(m.sum())
ref = json.load(open(os.path.join(os.path.dirname(KU2), "ku2.json")))
for foot, a0 in K["A0"].items():
    rr = np.full(n := len(K["z"]), np.nan); go, gb = K["accel"](K["mtm"], K["rhm"], K["lm"]); ok = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
    rr[ok] = K["resid"](go[ok], gb[ok], a0); g = np.isfinite(rr); Dv, _ = K["Dstat"](rr[g], K["slow"][g], K["cell"][g]); c2 = abs(Dv - ref[foot]["D"]) <= 1e-6
    R = np.full((11, len(ki)), np.nan)  # rows 0-9 models, 10 KU2's chosen
    for k in range(10):
        go, gb = K["accel"](K["MT"][k], K["RH"][k], K["lm"]); ok = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0)
        rk = np.full(n, np.nan); rk[ok] = K["resid"](go[ok], gb[ok], a0); R[k] = rk[ki]
    R[10] = rr[ki]
    j = np.flatnonzero(sl); est = np.array([E(R[k][j], h4[j], cell[j])[0] for k in range(11)]); Ns = E(R[10][j], h4[j], cell[j])[1]; c1 = Ns >= 150
    bs = []
    for _ in range(2000):
        b = j[rng.integers(0, len(j), len(j))]; bs.append([E(R[k][b], h4[b], cell[b])[0] for k in range(11)])
    bs = np.array(bs); lo, hi = np.nanpercentile(bs, 2.5, axis=0), np.nanpercentile(bs, 97.5, axis=0)
    dl = np.mean([est[2 * m] - est[2 * m + 1] for m in range(5)]); dbs = np.nanmean(bs[:, 0:10:2] - bs[:, 1:10:2], axis=1); dlo, dhi = np.nanpercentile(dbs, [2.5, 97.5])
    P(f"\n[{foot}] C1 slow in cells {Ns} (>= 150): {'PASS' if c1 else 'FAIL'}; C2 KU2 D {Dv:+.6f}: {'PASS' if c2 else 'FAIL'}")
    for k in range(10): P(f"[{foot}]   {NAMES[k]:18s} E_slow {est[k]:+.4f} [{lo[k]:+.4f}, {hi[k]:+.4f}]")
    P(f"[{foot}]   KU2 chosen model  E_slow {est[10]:+.4f} [{lo[10]:+.4f}, {hi[10]:+.4f}]")
    P(f"[{foot}] Delta_bar (cyl - sph, mean of 5 pairs) {dl:+.4f} [{dlo:+.4f}, {dhi:+.4f}]")
    Rr = dict(C1=bool(c1), C2=bool(c2), N_slow=Ns, E=est.tolist(), lo=lo.tolist(), hi=hi.tolist(), Delta_bar=float(dl), Delta_lo=float(dlo), Delta_hi=float(dhi))
    if MODE == "MUTATE":
        m1 = lo[10] <= 0 <= hi[10]; Rr["M1_pass"] = bool(m1); P(f"[{foot}] M1 interval (chosen model) includes 0: {'PASS' if m1 else 'FAIL'}")
    else:
        mp = os.path.join(HERE, "slw1_MUTATE.json"); M1 = json.load(open(mp))[foot]["M1_pass"] if os.path.exists(mp) else None
        inc0 = int(sum(lo[k] <= 0 <= hi[k] for k in range(10)))
        if not (c1 and c2) or M1 is False: lab = "NO VERDICT"
        elif abs(dl) >= 0.03 and (dlo > 0 or dhi < 0): lab = "ANISOTROPY-MODEL DEPENDENT"
        elif all(est[k] >= 0.05 and lo[k] > 0 for k in range(10)): lab = "ROBUST LEAD"
        elif inc0 >= 3: lab = "NOT ROBUST"
        else: lab = "NO VERDICT"
        if M1 is None: lab += " (PROVISIONAL: M1 not run)"
        f = np.flatnonzero(~sl); ef = [E(R[k][f], h4[f], cell[f])[0] for k in range(10)]
        rho = [spearmanr(h4[j], BETA[k][ki][j], nan_policy="omit").statistic for k in range(10)]
        jn = np.flatnonzero(sl & new); en = E(R[10][jn], h4[jn], cell[jn])[0]
        P(f"[{foot}] intervals including 0: {inc0} of 10")
        P(f"[{foot}] rows: E_fast per model " + " ".join(f"{x:+.3f}" for x in ef))
        P(f"[{foot}] rows: Spearman(h4, fitted beta) among slow per model " + " ".join(f"{x:+.2f}" for x in rho))
        P(f"[{foot}] rows: E_slow (chosen model) on LAM7-new only {en:+.4f}")
        P(f"[{foot}] LABEL: {lab}"); Rr.update(label=lab, E_fast=ef, rho_beta=rho, E_slow_new=en, n_include_0=inc0)
    RES[foot] = Rr
sfx = "" if MODE == "REAL" else f"_{MODE}"
open(os.path.join(HERE, f"slw1{sfx}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"slw1{sfx}.json"), "w"), indent=1, default=float)

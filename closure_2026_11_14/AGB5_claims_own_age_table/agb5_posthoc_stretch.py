"""AGB5, POST HOC 2 (written after AGB5's numbers and the same-hosts post hoc were seen; no frozen word).

The same-hosts post hoc finds that the difference between the claim's residuals and the Pantheon+ residuals of the
same supernovae trends with host age. Host age follows light-curve stretch (correlation -0.47), so a residual that
still depends on stretch or colour would show up as an age slope. Here the claim's own residuals, on the claim's
own tables, are fitted with the survey's stretch x1 and colour c (SDSS-II table, spectroscopic-redshift SALT2 fit)
allowed beside the age term:
    HR = alpha + beta age [+ g (L - 1/2)] [+ a x1 + b c]
Plain weighted lines as in AGB5; combined over the two tables by inverse variance; errors by bootstrap over hosts.
Writes agb5_posthoc_stretch.json; log to agb5_posthoc_stretch.out."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ["agb5_run.py", "none"]; sys.path.insert(0, HERE)
import numpy as np
import agb5_run as R

log = lambda s: print(s, flush=True); out = {}
S = R.D.D4.sako(); pos = {c: i for i, c in enumerate(S["cid"])}
tabs = []
for which in (1, 2):
    T = R.D.table(which); ix = np.array([pos[i] for i in T["id"]]); T["c"] = S["c"][ix]; T["x1"] = S["x1"][ix]; tabs.append(T)


def slope(T, idx, step, lc):
    k = np.isfinite(T["hr"][idx]) & np.isfinite(T["mass"][idx]) & np.isfinite(T["x1"][idx]) & np.isfinite(T["c"][idx]); i = idx[k]
    w = 1/(T["s_hr"][i]**2 + 0.01); cols = [np.ones(len(i)), T["age"][i]] + ([(T["mass"][i] < 10) - 0.5] if step else []) + ([T["x1"][i], T["c"][i]] if lc else [])
    X = np.column_stack(cols); XW = X.T*w; b = np.linalg.solve(XW@X, XW@T["hr"][i]); return b, len(i)


rng = np.random.default_rng(20261121); boots = [[rng.integers(0, len(T["age"]), len(T["age"])) for _ in range(400)] for T in tabs]
for step in (False, True):
    for lc in (False, True):
        b, s, extra = [], [], []
        for T, bt in zip(tabs, boots):
            full, n = slope(T, np.arange(len(T["age"])), step, lc); sd = float(np.std([slope(T, i, step, lc)[0][1] for i in bt], ddof=1))
            b.append(full[1]); s.append(sd); extra.append((n, full))
        w = 1/np.array(s)**2; A = float((w*np.array(b)).sum()/w.sum()/R.SLOPE); sA = float(w.sum()**-0.5/abs(R.SLOPE))
        key = f"{'step' if step else 'nostep'}_{'x1c' if lc else 'plain'}"
        out[key] = dict(A=A, sd_A=sA, D_A0=(A/sA)**2, D_A1=((A - 1)/sA)**2, table1=dict(beta=float(b[0]), sd=s[0], n=extra[0][0]), table2=dict(beta=float(b[1]), sd=s[1], n=extra[1][0]))
        if lc: out[key]["x1_coef"] = [float(extra[0][1][-2]), float(extra[1][1][-2])]; out[key]["c_coef"] = [float(extra[0][1][-1]), float(extra[1][1][-1])]
        log(f"{'mass step free' if step else 'no mass step  '}, {'stretch and colour allowed' if lc else 'as published          '}: A {A:+.3f} +- {sA:.3f}  dchi2(A=0) {(A/sA)**2:5.2f}  dchi2(A=1) {((A - 1)/sA)**2:5.2f}"
            f"   table 1 {b[0]:+.4f} +- {s[0]:.4f} (n {extra[0][0]}), table 2 {b[1]:+.4f} +- {s[1]:.4f} (n {extra[1][0]})"
            + (f"; x1 coefficient {extra[0][1][-2]:+.3f}, {extra[1][1][-2]:+.3f}; c coefficient {extra[0][1][-1]:+.2f}, {extra[1][1][-1]:+.2f}" if lc else ""))
for T, nm in zip(tabs, ("table 1", "table 2")):
    k = np.isfinite(T["x1"]) & np.isfinite(T["c"]); log(f"{nm}: correlation of the claim's residual with x1 {np.corrcoef(T['hr'][k], T['x1'][k])[0, 1]:+.3f}, with c {np.corrcoef(T['hr'][k], T['c'][k])[0, 1]:+.3f}; of age with x1 {np.corrcoef(T['age'][k], T['x1'][k])[0, 1]:+.3f}; n {int(k.sum())}")
json.dump(out, open(os.path.join(HERE, "agb5_posthoc_stretch.json"), "w"), indent=1, default=float); log("wrote agb5_posthoc_stretch.json")

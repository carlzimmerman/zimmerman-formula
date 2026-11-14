"""AGB5, POST HOC (written after AGB5's numbers were seen; no frozen word).

On the claim's own residuals the slope survives a mass step (A about 0.8); on Pantheon+ magnitudes the same family
of ages gives A about 0.3. Is that a different set of hosts, or different residuals for the same supernovae?
For the hosts of either table that are in Pantheon+ this fits, on the SAME supernovae:
  (a) the claim's own Hubble residual against age;
  (b) the Pantheon+ residual (raw magnitudes, free stretch and colour coefficients, 8 redshift bins) against age;
  (c) the difference of the two residuals against age.
Plain weighted lines, with and without a mass step; errors by bootstrap over supernovae (400).
Writes agb5_posthoc_same_hosts.json; log to agb5_posthoc_same_hosts.out."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ["agb5_run.py", "none"]; sys.path.insert(0, HERE)
import numpy as np
import agb5_run as R
sys.path.insert(0, os.path.join(R.D.REPO, "closure_2026_11_14", "AGB4_measured_host_ages")); import agb4_run as R4

log = lambda s: print(s, flush=True); out = {}
T1, T2 = R.D.table(1), R.D.table(2); P = R4.sample("pp"); p = R.D.D4.pantheon_sdss()
keep = np.isfinite(p["sako_age_Ravi"]) & (p["sako_age_lo_Ravi"] > 0); cid = p["cid"][keep]
rows = {}
for T in (T2, T1):                                   # table 1 wins for shared hosts (as in the reported Pantheon+ row)
    for i, c in enumerate(T["id"]): rows[c] = (T["age"][i], T["hr"][i], T["s_hr"][i])
sel = np.array([c in rows for c in cid]); age = np.array([rows[c][0] for c in cid[sel]]); hr = np.array([rows[c][1] for c in cid[sel]]); shr = np.array([rows[c][2] for c in cid[sel]])
z, x1, c, low, w, yP = P["z"][sel], P["x1"][sel], P["c"][sel], P["low"][sel], P["w"][sel], P["y"][sel]; n = int(sel.sum())
b = R4.bins_of(z, 8); B = np.zeros((n, 8)); B[np.arange(n), b] = 1.0
# Pantheon+ residual with the nuisance terms fitted without any host term
X0 = np.column_stack([B, x1, c]); beta0 = np.linalg.solve((X0.T*w)@X0, (X0.T*w)@yP); resP = yP - X0@beta0
wH = 1/(shr**2 + 0.01)


def line(y, ww, step, idx):
    cols = [np.ones(len(idx)), age[idx]] + ([low[idx] - 0.5] if step else []); X = np.column_stack(cols); XW = X.T*ww[idx]
    return np.linalg.solve(XW@X, XW@y[idx])[1]/R.SLOPE


rng = np.random.default_rng(20261120); allidx = np.arange(n); boots = [rng.integers(0, n, n) for _ in range(400)]
log(f"{n} supernovae are in Pantheon+ and in one of the claim's tables; A in units of the published slope:")
for name, y, ww in (("(a) the claim's own residuals", hr, wH), ("(b) Pantheon+ residuals, same supernovae", resP, w), ("(c) difference, claim minus Pantheon+", hr - resP, wH)):
    for step in (False, True):
        a = line(y, ww, step, allidx); e = float(np.std([line(y, ww, step, i) for i in boots], ddof=1))
        out[f"{name[:3]}_{'step' if step else 'nostep'}"] = dict(A=float(a), sd=e)
        log(f"   {name:42s} {'mass step free' if step else 'no mass step  '}: A {a:+.3f} +- {e:.3f}")
log(f"   scatter of the claim's residuals {np.std(hr):.3f} mag; of the Pantheon+ residuals {np.std(resP):.3f}; of their difference {np.std(hr - resP):.3f}; correlation {np.corrcoef(hr, resP)[0, 1]:.2f}")
json.dump(out, open(os.path.join(HERE, "agb5_posthoc_same_hosts.json"), "w"), indent=1, default=float); log("wrote agb5_posthoc_same_hosts.json")

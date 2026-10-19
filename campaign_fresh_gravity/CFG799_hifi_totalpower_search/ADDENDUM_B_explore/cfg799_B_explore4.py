"""CFG799 ADDENDUM B, EXPLORATORY decomposition part 4: does the H/V anticorrelated structure scale with target continuum?
Sets no class; changes no frozen rule.  Imports the unchanged ../ADDENDUM_B_full90/cfg799.py (sha256 7486117b...a81488).

Run:  python3 -I cfg799_B_explore4.py <data_dir> <out_dir>

Reason.  Part 3 found that the H-only and V-only total-power stacks carry smooth structure of +-10 to +-15 sigma over tens of
MHz, anticorrelated between the polarisations (corr -0.85 to -0.91 over +-60 and +-40 MHz), and that the frozen combined stack
is the small residual of the two.  A gain ripple that is not common to the sky path and the internal-load path multiplies
the continuum, so its size should scale with the target's continuum level.  That is testable per spectrum.

DECLARED LIST (fixed before the first run; everything is reported, one run, no variants):
  K1  reproduce B1.
  E10 per spectrum (polarisation H or V), at three centres: delta = 0 (nu_t), +15 MHz (the peak of the H structure and the
      trough of the V structure in part 3) and +36 MHz (nu_2):
        c_i = the median total-power temperature (K, J(T) scale) of the spectrum over its fit window about nu_t (|IF - IF_c| <= 50);
        a_i = the frozen per-spectrum line amplitude at that centre.
      (a) Spearman rank correlation of a_i with c_i, per polarisation and centre, with its p-value.
      (b) For (obs, LO) settings that have both H and V spectra: the Pearson correlation of a_H with a_V at each centre.
      (c) Stacks (frozen estimator, chi2-inflated) of the faint half (c_i <= median c_i of the 399 spectra) and the bright half,
          for H only, V only and H+V, at the three centres.
"""
import importlib.util, json, os, sys
import numpy as np
from scipy.stats import spearmanr

DATA = os.path.abspath(sys.argv[1]); OUTD = os.path.abspath(sys.argv[2])
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["cfg799.py", DATA]
spec = importlib.util.spec_from_file_location("cfg799", os.path.join(HERE, "..", "ADDENDUM_B_full90", "cfg799.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
OUT, R = [], {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


man, obs = m.load()
spectra = []
for oid, o in obs.items():
    a = m.anchor(o)
    if a["ok"]:
        spectra += m.build_spectra(oid, o, a["tS"])
sp, drops = m.prep(spectra)
st_t = m.stack(m.amps(sp, m.NU_T)); st_2 = m.stack(m.amps(sp, m.NU_2))
P("CFG799 ADDENDUM B exploratory decomposition, part 4 (sets no class)")
P(f"  K1 nu_t a = {st_t['a'] * 1e3:+.3f} mK, nu_2 a = {st_2['a'] * 1e3:+.3f} mK  "
  f"{'REPRODUCES B1' if abs(st_t['a'] + 6.577e-3) < 1e-5 and abs(st_2['a'] - 15.343e-3) < 1e-5 else 'DOES NOT REPRODUCE'}")
assert abs(st_t["a"] + 6.577e-3) < 1e-5 and abs(st_2["a"] - 15.343e-3) < 1e-5


def cont(s):
    ax = s["IF"][s["sb"]]; y = s["Tall"][s["sb"]]
    sel = np.abs(ax - s["ifc"]) <= 50.0
    return float(np.nanmedian(y[sel])) if sel.sum() > 20 else np.nan


for s in sp:
    s["c"] = cont(s)
cs = np.array([s["c"] for s in sp]); med = float(np.nanmedian(cs))
P(f"  continuum level c (K): median {med:.1f}, 10th-90th percentile {np.nanpercentile(cs, 10):.1f} to {np.nanpercentile(cs, 90):.1f}")
CENT = (("0", m.NU_T), ("+15", m.NU_T + 0.015), ("+36 (nu_2)", m.NU_2))
R["E10"] = {}
for lab, nu in CENT:
    a = m.amps(sp, nu); R["E10"][lab] = {}
    P(f"\n[centre delta = {lab} MHz]")
    for pol in ("h", "v"):
        ap = [x for x in a if x[2]["pol"] == pol]
        am = np.array([x[0] for x in ap]); cm = np.array([x[2]["c"] for x in ap])
        ok = np.isfinite(am) & np.isfinite(cm)
        rho, p = spearmanr(am[ok], cm[ok])
        P(f"  (a) {pol.upper()}: Spearman rho(a_i, c_i) = {rho:+.2f} (p {p:.1e}, n {int(ok.sum())})")
        R["E10"][lab][pol] = dict(rho=float(rho), p=float(p), n=int(ok.sum()))
    key = lambda x: (x[2]["obs"], round(x[2]["lo"] * 1000))
    dh = {key(x): x[0] for x in a if x[2]["pol"] == "h"}; dv = {key(x): x[0] for x in a if x[2]["pol"] == "v"}
    both = sorted(set(dh) & set(dv))
    if len(both) > 3:
        ah = np.array([dh[k] for k in both]); av = np.array([dv[k] for k in both])
        r = float(np.corrcoef(ah, av)[0, 1]); rs = float(spearmanr(ah, av)[0])
        P(f"  (b) matched (obs, LO) pairs {len(both)}: Pearson corr(a_H, a_V) = {r:+.2f}, Spearman {rs:+.2f}")
        R["E10"][lab]["HV"] = dict(n=len(both), pearson=r, spearman=rs)
    for half, pred in (("faint", lambda x: x[2]["c"] <= med), ("bright", lambda x: x[2]["c"] > med)):
        cells = {}
        for sel, nm in (("h", "H"), ("v", "V"), (None, "H+V")):
            sub = [x for x in a if pred(x) and (sel is None or x[2]["pol"] == sel)]
            cells[nm] = m.stack(sub)
        R["E10"][lab][half] = cells
        P(f"  (c) {half:6s}: " + " | ".join(f"{nm}: {c['a'] * 1e3:+6.1f}+-{c['sig'] * 1e3:4.1f} mK z {c['z']:+5.2f} (n {c['n']})" for nm, c in cells.items()))

open(os.path.join(OUTD, "explore4.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(OUTD, "explore4_results.json"), "w"), indent=1, default=str)

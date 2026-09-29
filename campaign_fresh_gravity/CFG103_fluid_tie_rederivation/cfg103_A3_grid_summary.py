"""CFG103-A3b: reads cfg103_A3_results.json (the frozen-grid output of cfg103_A3.py) and summarises WHICH conventions carry the window.
Pure post-processing of the frozen grid; no new physics, no re-tuning.  Window = g0^2 if g0 > 1 else empty; BTFR needs 1e4 (g0 >= 100)."""
import os, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg103_A3_results.json")))["grid"]
out = []
def P(*a): s = " ".join(str(x) for x in a); print(s); out.append(s)
def win(rs, key="g0_1e9"):
    g = max(r[key] for r in rs); return g, (g**2 if g > 1 else 0.0)
sel = lambda **kw: [r for r in R if all(r[k] == v if not isinstance(v, float) else abs(r[k] - v) < 1e-9 for k, v in kw.items())]
P("A. Window ceiling by which conventions are allowed (each row: max over the freed conventions; F fixed as stated)")
for Fs in ([0.5], [0.5, 0.9], [0.5, 0.9, 0.1], [0.5, 0.9, 0.1, 0.01]):
    for dmax in (0.2, 0.5):
        rs = [r for r in R if r["F"] in Fs and r["d"] <= dmax and r["fh"] == 1.0 and r["ku"] == "Mpc"]
        g, w = win(rs); P("   F in %-24s d<=%2.0f%%  f_h=1, 1/Mpc, k conv & M_h free : g0max=%8.3g window=%s" % (Fs, dmax * 100, g, "%.3g" % w if w else "EMPTY"))
P("B. Same, additionally allowing the halo-size multiplier f_h in {4,40} (unmotivated) and the h/Mpc unit confusion")
for Fs in ([0.5, 0.9], [0.5, 0.9, 0.1, 0.01]):
    for fh in (1.0, 4.0, 40.0):
        for ku in ("Mpc", "h"):
            rs = [r for r in R if r["F"] in Fs and r["fh"] == fh and r["ku"] == ku]
            g, w = win(rs); P("   F in %-24s f_h=%-4g units=%-4s (d, k conv, M_h free): g0max=%8.3g window=%.3g" % (Fs, fh, ku, g, w))
P("C. Points reaching window >= 1e4 : count by F and f_h")
for F in (0.5, 0.9, 0.1, 0.01):
    for fh in (1.0, 4.0, 40.0):
        rs = sel(F=F, fh=fh); n = sum(1 for r in rs if r["g0_1e9"]**2 >= 1e4 and r["g0_1e9"] > 1); P("   F=%-4g f_h=%-4g : %3d of %3d" % (F, fh, n, len(rs)))
P("D. Cheapest way to reach 1e4 with F>=0.9 (hydrostatic requirement): rows, sorted by number of non-primary conventions")
prim = dict(d=0.05, F=0.5, kconv=float(np.pi), Mh="fb", fh=1.0, ku="Mpc")
cands = []
for r in R:
    if r["F"] >= 0.9 and r["g0_1e9"] >= 100:
        nchg = sum(1 for k, v in prim.items() if not (r[k] == v if not isinstance(v, float) else abs(r[k] - v) < 1e-9))
        cands.append((nchg, r))
cands.sort(key=lambda t: (t[0], -t[1]["g0_1e9"]))
for nchg, r in cands[:8]: P("   %d changes: d=%g F=%g kconv=%.3f M_h=%s f_h=%g units=%s  -> g0=%.3g window=%.3g" % (nchg, r["d"], r["F"], r["kconv"], r["Mh"], r["fh"], r["ku"], r["g0_1e9"], r["g0_1e9"]**2))
P("   (F=0.9 rows with f_h=1 and units=1/Mpc reaching 1e4: %d)" % sum(1 for r in R if r["F"] >= 0.9 and r["fh"] == 1.0 and r["ku"] == "Mpc" and r["g0_1e9"] >= 100))
P("E. mass-independence of g0 across the grid: max |log10(g0(1e9)/g0(3e11))| = %.3f" % max(abs(np.log10(r["g0_1e9"] / r["g0_3e11"])) for r in R))
open(os.path.join(HERE, "cfg103_A3_grid_summary.out"), "w").write("\n".join(out) + "\n")

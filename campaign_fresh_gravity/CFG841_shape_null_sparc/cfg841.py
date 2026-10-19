"""CFG841 -- calibration-free shape test (Codex ZAR-D1) on SPARC: simple action law vs quadratic a0-line.
Criteria: FROZEN_CRITERIA.md (d35ad36ab).  Run: python3 cfg841.py   (CFG841_MUTATE=S or Q: synthetic power controls).
kappa = 1/2 FITTED (cancels); not theory closed."""
import os, glob, json, math, numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = os.environ.get("CFG841_MUTATE", ""); assert MUT in ("", "S", "Q"); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
KPC, a0 = 3.0857e19, 9.3603e-11; rng = np.random.default_rng(841)
Qf = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Qf[v[0]] = (float(v[5]), int(v[17]))
        except ValueError: pass
def galaxies():
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        name = os.path.basename(fn).replace("_rotmod.dat", ""); inc, q = Qf.get(name, (0, 3))
        if q > 2 or inc < 30: continue
        rows = []
        for l in open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(x) for x in l.split()[:6]]
            if V <= 0 or R <= 0 or eV / V >= 0.10 or Vg <= 0: continue
            gas = Vg * Vg; star = 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb); tot = gas + star
            if tot <= 0: continue
            rows.append((R, V, max(eV, 0.03 * V), gas * 1e6 / (R * KPC), tot * 1e6 / (R * KPC), star / tot))
        yield name, np.array(rows) if rows else np.zeros((0, 6))
law_s = lambda b: 0.5 * (b + np.sqrt(b * b + 4 * a0 * b)); law_q = lambda b: np.sqrt(b * b + a0 * b)
def fit(z, x, dzdV_fn, sV):
    al = 0.0
    for _ in range(6):
        s = np.abs(dzdV_fn(al)) * sV; w = 1 / np.maximum(s, 1e-300) ** 2
        A = np.vstack([x, np.ones_like(x)]).T; W = np.diag(w); cf = np.linalg.solve(A.T @ W @ A, A.T @ W @ z); al = cf[0]
    r = z - A @ cf; return float(r @ W @ r), float(cf[0]), float(cf[1])
def analyse(sample):
    res = []
    for name, d in galaxies():
        if len(d) == 0: continue
        if sample == "primary":
            d = d[d[:, 5] <= 0.20]; h = d[:, 3] if len(d) else None; nmin = 4
        else:
            h = d[:, 4] if len(d) else None; nmin = 5
        if len(d) < nmin: continue
        R, V, sV = d[:, 0], d[:, 1].copy(), d[:, 2]
        if MUT:
            g = (law_s if MUT == "S" else law_q)(h); V = np.sqrt(g * R * KPC) / 1e3 + rng.normal(0, sV)
        q = V * V * 1e6 / (R * KPC); z = q * q / h; dq = 2 * V * 1e6 / (R * KPC)
        cs = fit(z, q, lambda al: (2 * q / h - al) * dq, sV); cq = fit(z, h, lambda al: (2 * q / h) * dq, sV)
        res.append(dict(name=name, n=len(d), chi2_s=cs[0], chi2_q=cq[0], dchi2=cq[0] - cs[0], phys_s=cs[1] > 0 and cs[2] > 0, phys_q=cq[1] > 0 and cq[2] > 0,
                        ymin=float(np.min(h) / a0), ymax=float(np.max(h) / a0)))
    return res
def classify(res):
    if len(res) < 5: return "NOT DIAGNOSTIC (N<5)", {}
    D = sum(r["dchi2"] for r in res); fpos = np.mean([r["dchi2"] > 0 for r in res]); fneg = np.mean([r["dchi2"] < 0 for r in res])
    ps, pq = np.mean([r["phys_s"] for r in res]), np.mean([r["phys_q"] for r in res])
    st = dict(N=len(res), sum_dchi2=float(D), frac_pos=float(fpos), frac_neg=float(fneg), phys_s=float(ps), phys_q=float(pq),
              median_dchi2=float(np.median([r["dchi2"] for r in res])))
    if D >= 9 and fpos > 0.5 and ps >= 0.5: return "SIMPLE FAVOURED", st
    if D <= -9 and fneg > 0.5 and pq >= 0.5: return "QUADRATIC FAVOURED", st
    return "NEITHER", st
P("CFG841  shape-null test on SPARC" + (f"  [MUTATE-{MUT}: synthetic {('simple' if MUT == 'S' else 'quadratic')}-law data]" if MUT else ""))
if not MUT:
    q, h = [Fr(1), Fr(2), Fr(3)], [Fr(1, 2), Fr(4, 3), Fr(9, 4)]; z = [qq * qq / hh for qq, hh in zip(q, h)]
    det = lambda a, b: (a[1] - a[0]) * (b[2] - b[0]) - (a[2] - a[0]) * (b[1] - b[0])
    P(f"  K1 hand example: D_s = {det(z, q)}  D_q = {abs(det(z, h))}  -> {'PASS' if det(z, q) == 0 and abs(det(z, h)) == Fr(1, 12) else 'FAIL'}")
RES = dict(lane="CFG841", mutate=MUT)
for sample in ("primary", "secondary"):
    res = analyse(sample); cls, st = classify(res)
    RES[sample] = dict(cls=cls, stats=st, rows=res)
    P(f"\n  [{sample}{' (gas-only template)' if sample == 'primary' else ' (fixed-composition, approximate)'}] N {st.get('N', len(res))}: sum dchi2 (quad - simple) {st.get('sum_dchi2', float('nan')):+.1f}, "
      f"median {st.get('median_dchi2', float('nan')):+.2f}, frac>0 {st.get('frac_pos', float('nan')):.2f}, physical fits simple {st.get('phys_s', float('nan')):.2f} / quad {st.get('phys_q', float('nan')):.2f}  -> {cls}")
    if sample == "primary" and not MUT:
        for r in sorted(res, key=lambda r: -abs(r["dchi2"]))[:12]:
            P(f"     {r['name']:10s} n {r['n']:2d}  dchi2 {r['dchi2']:+8.2f}  chi2 S {r['chi2_s']:7.2f} Q {r['chi2_q']:7.2f}  y {r['ymin']:.3f}-{r['ymax']:.3f}  phys S {r['phys_s']} Q {r['phys_q']}")
sfx = f"_MUTATE_{MUT}" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg841_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg841{sfx}.out"), "w").write("\n".join(OUT) + "\n")

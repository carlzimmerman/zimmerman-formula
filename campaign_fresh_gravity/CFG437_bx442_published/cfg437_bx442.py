#!/usr/bin/env python3
"""CFG437 (FROZEN_CRITERIA.md): implied a0 for BX442 from Law+12 published numbers, readings A (V_rot) and B (asymmetric-drift V_c).
CFG437_MUTATE=1 -> V_rot x sqrt(3.29)."""
import os, math, json, numpy as np
MUT = os.environ.get("CFG437_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
rng = np.random.default_rng(437); N = 20000
G, MS, KPC = 6.674e-11, 1.989e30, 3.0857e19
def split(med, up, lo, n): z = rng.standard_normal(n); return np.where(z > 0, med + z * up, med + z * lo)
Ms = np.clip(split(6e10, 2e10, 1e10, N), 1e9, None); Mg = np.clip(split(2e10, 2e10, 1e10, N), 1e8, None)
V = np.clip(split(234.0, 49.0, 29.0, N), 50, None) * (math.sqrt(3.29) if MUT else 1.0); sig = rng.normal(71.0, 1.0, N)
R = 8 * KPC; Rd = 5.0 / 1.68
gN = G * (Ms + Mg) * MS / R ** 2
def a0_from(gobs, gN):
    r = gobs / gN; out = np.full(r.shape, np.nan); ok = r > 1
    s = -np.log(1 - 1 / r[ok]); out[ok] = gN[ok] / s ** 2; return out
H = 3.29; FL = {"canonical": 9.36e-11, "alt": 1.13e-10}
L, OUT = [], {"mutate": MUT}
def P(s): print(s); L.append(s)
cls_all = {}
for name, Vc2 in (("A V_c=V_rot", (V * 1e3) ** 2), ("B asym-drift", (V * 1e3) ** 2 + 2 * (sig * 1e3) ** 2 * (8.0 / Rd))):
    a = a0_from(Vc2 / R, gN); f_newt = float(np.mean(np.isnan(a))); la = np.log10(a[~np.isnan(a)])
    lo, med, hi = np.percentile(la, [16, 50, 84])
    cls = {}
    for foot, a0 in FL.items():
        inF = lo <= math.log10(a0) <= hi; inH = lo <= math.log10(a0 * H) <= hi
        cls[foot] = "FAVOURS FLAT" if inF and not inH else "FAVOURS H(z)" if inH and not inF else "NOT DIAGNOSTIC"
    cls_all[name] = cls; OUT[name] = dict(lo=10 ** lo, med=10 ** med, hi=10 ** hi, frac_g_le_gN=f_newt, cls=cls)
    P(f"  {name:13s}: a0 median {10**med:.2e} (16-84%: {10**lo:.2e} - {10**hi:.2e}); draws with g_obs<=g_N {f_newt:.3f}; "
      f"canonical {cls['canonical']}, alt {cls['alt']}")
P(f"  predictions: flat {FL['canonical']:.2e}/{FL['alt']:.2e}; H(z) rival {FL['canonical']*H:.2e}/{FL['alt']*H:.2e}")
v = {}
for foot in FL:
    a, b = cls_all["A V_c=V_rot"][foot], cls_all["B asym-drift"][foot]
    v[foot] = a if a == b else "NOT DIAGNOSTIC (pressure-support systematic)"
OUT["verdict"] = v; P(f"VERDICT: canonical {v['canonical']}; alt {v['alt']}  (one galaxy; gas mass from SF-law inversion)")
H_ = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(H_, f"cfg437_bx442{SUF}.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(H_, f"cfg437_results{SUF}.json"), "w"), indent=1)

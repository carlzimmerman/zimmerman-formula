"""CFG697: numbers behind the reading scorecard (criteria 5c5d22bd5). nu_simple/nu_mono over each gate's range; <div P> = 0 theorem.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg697.py
"""
import os, sys, json
import numpy as np
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import CFG4_common as C4  # noqa: E402
out = {}
for name, lo, hi in (("X-COP (y 0.3-3)", 0.3, 3.0), ("deep: LG, C3, satellites (y 0.001-0.1)", 1e-3, 0.1), ("SPARC full (y 0.01-30)", 0.01, 30.0)):
    y = np.logspace(np.log10(lo), np.log10(hi), 400)
    r = 0.5 * (1 + np.sqrt(1 + 4 / y)) / C4.nu_mono(y)
    out[name] = dict(min=float(r.min()), max=float(r.max()))
    print(f"{name:42s}: nu_simple/nu_mono in [{r.min():.4f}, {r.max():.4f}]")
k, Pk = sp.symbols("k P_k")
print("theorem: P statistically homogeneous => <div P> = div <P> = div (const) = 0 (Fourier: the k = 0 mode of i k.P_k is 0)")
out["theorem"] = "<div P> = 0"
json.dump(out, open(os.path.join(HERE, "cfg697_results.json"), "w"), indent=1)

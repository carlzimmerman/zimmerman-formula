"""p37b (POST-HOC, after p37's pre-written 'sharper transition' checks FAILED): is SPARC's kernel-shape preference a mass-to-light artefact?
Family nu_n = (1 + y^-n)^(1/(2n)); nu(1) = 2^(1/(2n)) (framework n = 1: 1.414; RAR nu(1) = 1/(1 - e^-1) = 1.582).
Grid extended to n = 0.4. MLS16 cuts at fixed Upsilon_disk = 0.5, 0.6, 0.7 (bulge 1.4x), sigma_int 0.11: Delta chi2 of RAR and of the best n relative to n = 1.
If the preference collapses as Upsilon rises toward p16's 0.6, the 'shape' signal is the stellar mass-to-light zero point, not the kernel.
Run: python3 p37b_shape_vs_upsilon.py  |  MUTATE=1: Upsilon applied to gas instead of stars (check S must fail)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
IFn = lambda n: (lambda gb, a: gb * (1 + (gb / a)**(-n))**(1 / (2 * n)))
gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
if MUTATE:
    gals = [dict(g, Vgas=g["Vdisk"], Vdisk=g["Vgas"]) for g in gals]
A = np.exp(np.linspace(math.log(0.4e-10), math.log(2.6e-10), 61))
N = [0.4, 0.5, 0.6, 0.7, 0.85, 1.0, 1.25]
rows = {}
for U in (0.5, 0.6, 0.7):
    c = {n: V.Profile(gals, IFn(n), ufixed=U).scan(A, 0.11) for n in N}
    c1 = c[1.0].min(); rar = V.Profile(gals, V.IF_rar, ufixed=U).scan(A, 0.11).min() - c1
    nb = min(N, key=lambda n: c[n].min())
    a_n1 = V.parabola_min(A, c[1.0], k=6)[0]
    rows[U] = (rar, nb, c[nb].min() - c1, a_n1)
    print(f"   Upsilon {U}: chi2(n=1) {c1:.0f}; " + " ".join(f"n={n:g}:{c[n].min()-c1:+.0f}" for n in N) + f" | RAR {rar:+.0f} | best n {nb:g} | a0(n=1) = {a_n1:.3e}")
check("S the shape preference (RAR vs n = 1) SHRINKS as Upsilon rises from 0.5 to 0.7", rows[0.7][0] > rows[0.5][0] and abs(rows[0.7][0]) < abs(rows[0.5][0]))
check("T at Upsilon 0.7 the framework kernel's a0 (n = 1) lands within 10% of the footing 9.36e-11", abs(rows[0.7][3] / 9.3603e-11 - 1) < 0.10)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)

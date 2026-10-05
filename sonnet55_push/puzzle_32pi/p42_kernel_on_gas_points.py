"""p42: which kernel do the Upsilon-free gas-dominated POINTS prefer? (p41b selection: gas > fcut of g_bar at Upsilon 0.5; SPARC MLS16 cuts; sigma_int 0.11.)
Kernels: framework sqrt(1+1/y) (= nu_n at n = 1), nu_n family n = 0.6..1.6, RAR. a0 profiled. Delta chi2 vs the framework kernel, at Upsilon 0.3/0.5/0.7 (must agree if
the selection is Upsilon-free). Also the y range these points cover (the kernel is only tested where the data are).
Run: python3 p42_kernel_on_gas_points.py  |  MUTATE=1: fcut 0 (all points: the verdict must depend on Upsilon; check I must fail)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
def sub(g, m):
    h = dict(g)
    for k in ("Rm", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"): h[k] = g[k][m]
    return h
FC = 0.0 if MUTATE else 0.8
GP = []
for g in gals:
    vb2 = np.sign(g["Vgas"]) * g["Vgas"]**2 + 0.5 * g["Vdisk"]**2 + 0.7 * g["Vbul"]**2
    fg = np.where(vb2 > 0, np.sign(g["Vgas"]) * g["Vgas"]**2 / np.where(vb2 > 0, vb2, 1), 0)
    m = fg > FC
    if m.sum() >= 2: GP.append(sub(g, m))
ys = np.concatenate([((np.sign(g["Vgas"]) * g["Vgas"]**2 + 0.5 * g["Vdisk"]**2 + 0.7 * g["Vbul"]**2) * 1e6 / g["Rm"]) / 9.36e-11 for g in GP])
print(f"   {len(GP)} galaxies, {len(ys)} points; y = g_bar/a0 range {np.percentile(ys,5):.3f} - {np.percentile(ys,95):.3f} (5-95%), median {np.median(ys):.3f}")
A = np.exp(np.linspace(math.log(0.3e-10), math.log(2.6e-10), 61))
IFn = lambda n: (lambda gb, a: gb * (1 + (gb / a)**(-n))**(1 / (2 * n)))
N = [0.6, 0.7, 0.8, 0.9, 1.0, 1.15, 1.3, 1.6]
verdict = {}
for U in (0.3, 0.5, 0.7):
    c = {n: V.Profile(GP, IFn(n), ufixed=U).scan(A, 0.11) for n in N}
    c1 = c[1.0].min(); rar = V.Profile(GP, V.IF_rar, ufixed=U).scan(A, 0.11)
    nb = min(N, key=lambda n: c[n].min())
    rng = [n for n in N if c[n].min() - c[nb].min() < 4]
    verdict[U] = (nb, rar.min() - c1, min(rng), max(rng))
    print(f"   Upsilon {U}: " + " ".join(f"n={n:g}:{c[n].min()-c1:+.1f}" for n in N) + f" | RAR {rar.min()-c1:+.1f} | best n {nb:g}, Delta chi2<4: [{min(rng):g}, {max(rng):g}]"
          f" | a0(n=1) {V.parabola_min(A, c[1.0], k=6)[0]:.3e}")
check("I the kernel verdict is the same at Upsilon 0.3, 0.5, 0.7 (best n within one grid step)", max(v[0] for v in verdict.values()) - min(v[0] for v in verdict.values()) <= 0.15)
check("F the framework kernel (n = 1) is inside the Delta chi2 < 4 range at every Upsilon", all(v[2] <= 1.0 <= v[3] for v in verdict.values()))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)

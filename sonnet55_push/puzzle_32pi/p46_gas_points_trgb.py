"""p46: SPARC's Upsilon-free gas points (p41b: gas > 80% of g_bar at Upsilon 0.5; MLS16 cuts) restricted by DISTANCE METHOD (SPARC f_D: 1 Hubble flow, 2 TRGB, 3 Cepheid,
4 UMa cluster, 5 SN). Framework kernel, sigma_int 0.11, galaxy bootstrap. The redshift-independent subset (f_D 2, 3) removes the Hubble-flow distance systematic that
binds p43/p44. Compared with the kappa = 1/2 footing 9.3603e-11, the alt footing 1.1312e-10, and the rho_Lambda rivals (Verlinde 6: 9.03e-11, Milgrom 2pi: 8.63e-11).
Also: the SPARC distance errors of the TRGB/Cepheid gas galaxies (their e_D/D).
Run: python3 p46_gas_points_trgb.py [NBOOT]  |  MUTATE=1: distances of the TRGB/Cepheid set scaled x1.1 (a0 must drop ~25-35%: check D fails)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 300
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
def sub(g, m):
    h = dict(g)
    for k in ("Rm", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"): h[k] = g[k][m]
    return h
def gaspts(sel):
    out = []
    for g in sel:
        vb2 = np.sign(g["Vgas"]) * g["Vgas"]**2 + 0.5 * g["Vdisk"]**2 + 0.7 * g["Vbul"]**2
        fg = np.where(vb2 > 0, np.sign(g["Vgas"]) * g["Vgas"]**2 / np.where(vb2 > 0, vb2, 1), 0)
        m = fg > 0.8
        if m.sum() >= 2: out.append(sub(g, m))
    return out
A = np.exp(np.linspace(math.log(0.3e-10), math.log(3.0e-10), 121))
fit = lambda S, u=0.5: V.parabola_min(A, V.Profile(S, V.IF_alpha1, ufixed=u).scan(A, 0.11), k=6)[0]
def boot(S, nb, seed):
    rng = np.random.default_rng(seed); return np.array([fit([S[i] for i in rng.integers(0, len(S), len(S))]) for _ in range(nb)])
sets = {"TRGB/Cepheid (f_D 2,3)": [g for g in gals if g["fD"] in (2, 3)], "Hubble flow (f_D 1)": [g for g in gals if g["fD"] == 1], "all": gals}
out = {}
for k, sel in sets.items():
    S = gaspts(sel)
    if MUTATE and k.startswith("TRGB"): S = [V.transform(g, dist_scale=1.1) for g in S]
    a = fit(S); B = boot(S, NB if k.startswith("TRGB") else NB // 3, 46)
    lo, hi = np.percentile(B, [16, 84]); e = (hi - lo) / 2 / a
    sens = [fit(S, u) for u in (0.3, 0.7)]
    out[k] = (a, e, len(S), sens)
    names = ", ".join(sorted(g["name"] for g in S)) if k.startswith("TRGB") else ""
    print(f"   {k:26s}: {len(S):2d} galaxies, {sum(len(g['Rm']) for g in S):3d} pts;  a0 = {a:.3e} +- {100*e:.1f}%;  Upsilon 0.3/0.7: {sens[0]:.3e}/{sens[1]:.3e}")
    if names: print(f"      galaxies: {names}")
tr = [g for g in gals if g["fD"] in (2, 3) and g in [x for x in gals]]
eDD = [g["eD"] / g["D"] for g in gals if g["fD"] in (2, 3) and g["eD"] and g["D"]]
print(f"   SPARC e_D/D for TRGB/Cepheid galaxies: median {np.median(eDD):.3f}")
a, e, n, _ = out["TRGB/Cepheid (f_D 2,3)"]
for lab, v in (("kappa=1/2 rho_L", 9.3603e-11), ("alt rho_tot", 1.1312e-10), ("Verlinde 6 rho_L", 9.033e-11), ("Milgrom 2pi rho_L", 8.626e-11), ("32pi turn-off", 1.061e-10)):
    print(f"      vs {lab:18s} {v:.3e}: {100*(a/v-1):+6.1f}%  ({math.log(a/v)/e:+.2f} sigma, stat only)")
check(f"D the TRGB/Cepheid gas-point a0 ({a:.3e}) is within 2 sigma (stat) of SPARC's all-distance gas-point value 9.00e-11", abs(math.log(a / 9.00e-11)) < 2 * e)
check(f"S the TRGB/Cepheid subset has at least 8 galaxies (n = {n})", n >= 8)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)

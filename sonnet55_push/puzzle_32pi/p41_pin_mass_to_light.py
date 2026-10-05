"""p41: pin the stellar mass-to-light ratio with the gas-dominated galaxies, then measure a0 (SPARC, MLS16 cuts Q <= 2, i >= 30; sigma_int 0.11; lane V machinery).
G = gas-dominated (gas fraction at the last point > 0.6 at Upsilon 0.5): its a0 barely depends on Upsilon (checked at 0.3/0.5/0.7).
S = star-dominated (gas fraction < 0.3). Calibrated Upsilon*: the Upsilon_disk (bulge 1.4x) at which a0_S(Upsilon) = a0_G(Upsilon).
Then a0 for ALL galaxies at Upsilon*, with a galaxy bootstrap (G and S resampled, Upsilon* re-solved). Kernels: framework (sqrt(1+1/y)) and RAR (systematic).
Compared with: the footings 9.3603e-11 / 1.1312e-10; the 3.6 um population prior Upsilon ~ 0.5 (+-0.1 dex); p40's 32 pi turn-off prediction 1.061e-10.
Run: python3 p41_pin_mass_to_light.py [NBOOT]  |  MUTATE=1: G and S labels swapped (the gas sample then depends on Upsilon: check G must fail)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "V_evidence_for_the_coefficient"))
import v_common as V
MUTATE = os.environ.get("MUTATE") == "1"
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 60
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
gals = [g for g in V.load_sparc() if g["Q"] is not None and g["Q"] <= 2 and g["inc"] >= 30]
for g in gals:
    vb2 = g["Vgas"][-1]**2 + 0.5 * g["Vdisk"][-1]**2 + 0.7 * g["Vbul"][-1]**2
    g["fg"] = g["Vgas"][-1]**2 / vb2 if vb2 > 0 else 0
Gs = [g for g in gals if g["fg"] > 0.6]; Ss = [g for g in gals if g["fg"] < 0.3]
if MUTATE: Gs, Ss = Ss, Gs
A = np.exp(np.linspace(math.log(0.5e-10), math.log(2.2e-10), 57))
UG = np.round(np.arange(0.40, 0.901, 0.025), 3)
def a0fit(sel, IF, u):
    return V.parabola_min(A, V.Profile(sel, IF, ufixed=u).scan(A, 0.11), k=6)[0]
def ustar(G_, S_, IF):
    d = np.array([math.log(a0fit(S_, IF, u) / a0fit(G_, IF, u)) for u in UG])
    if not (d.min() < 0 < d.max()): return float("nan")
    i = int(np.where(np.diff(np.sign(d)) != 0)[0][0])
    return float(UG[i] - d[i] * (UG[i + 1] - UG[i]) / (d[i + 1] - d[i]))
print(f"   samples: gas-dominated G = {len(Gs)}, star-dominated S = {len(Ss)}, all = {len(gals)}")
out = {}
for nm, IF in (("framework", V.IF_alpha1), ("RAR", V.IF_rar)):
    sens = [a0fit(Gs, IF, u) for u in (0.3, 0.5, 0.7)]
    us = ustar(Gs, Ss, IF)
    aall = a0fit(gals, IF, us)
    rng = np.random.default_rng(41); boot = []
    for b in range(NB if nm == "framework" else max(NB // 3, 10)):
        Gb = [Gs[i] for i in rng.integers(0, len(Gs), len(Gs))]; Sb = [Ss[i] for i in rng.integers(0, len(Ss), len(Ss))]
        ub = ustar(Gb, Sb, IF)
        if np.isfinite(ub): boot.append((ub, a0fit(Gb + Sb + [g for g in gals if 0.3 <= g["fg"] <= 0.6], IF, ub)))
    boot = np.array(boot)
    out[nm] = (us, aall, sens, boot)
    lo, hi = np.percentile(boot[:, 1], [16, 84]); ulo, uhi = np.percentile(boot[:, 0], [16, 84])
    print(f"   {nm:9s}: gas-sample a0 at Upsilon 0.3/0.5/0.7 = {sens[0]:.3e} / {sens[1]:.3e} / {sens[2]:.3e} (spread {100*(max(sens)/min(sens)-1):.1f}%)")
    print(f"              calibrated Upsilon* = {us:.3f} (68%: {ulo:.3f}-{uhi:.3f});  a0(all, Upsilon*) = {aall:.3e} (68%: {lo:.3e}-{hi:.3e}, {100*(hi-lo)/2/aall:.1f}%)  [{len(boot)} boots]")
    print(f"              vs footings: 9.360e-11 {100*(aall/9.3603e-11-1):+.1f}%,  1.131e-10 {100*(aall/1.1312e-10-1):+.1f}%;  vs 32pi turn-off 1.061e-10 {100*(aall/1.061e-10-1):+.1f}%")
us, aall, sens, boot = out["framework"]
check(f"G the gas-dominated a0 is insensitive to Upsilon (spread {100*(max(sens)/min(sens)-1):.1f}% over 0.3-0.7 < 15%)", max(sens) / min(sens) < 1.15)
check(f"U the calibrated Upsilon* = {us:.3f} lies inside the 3.6 um population prior (0.5 x/ 10^+-0.1 = 0.40-0.63)", 0.40 <= us <= 0.63)
sd = (np.percentile(boot[:, 1], 84) - np.percentile(boot[:, 1], 16)) / 2 / aall
print(f"   precision of this a0: {100*sd:.1f}% (statistical, galaxy bootstrap); kernel systematic (RAR vs framework): {100*abs(out['RAR'][1]/aall-1):.1f}%")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)

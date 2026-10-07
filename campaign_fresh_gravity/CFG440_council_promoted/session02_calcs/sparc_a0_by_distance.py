"""Addendum D: SPARC a0 by distance method. Run: python3 sparc_a0_by_distance.py [--mutate]"""
import os, sys, math, json, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s); OUT.append(str(s))
GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
KPC = 3.0857e19
def arrays(gs, U, ladder_scale=1.0):
    gb, go, w, gi = [], [], [], []
    for k, g in enumerate(gs):
        R = g["R"] * KPC
        vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2
        b = vb2 * 1e6 / R; o = (g["Vobs"] * 1e3) ** 2 / R
        if MUT and g["meta"]["fD"] in (2, 3, 5): o = o / ladder_scale
        ok = (b > 0) & (o > 0) & (g["Vobs"] > 0)
        gb.append(b[ok]); go.append(o[ok]); gi.append(np.full(ok.sum(), k))
        w.append(1 / (np.clip(g["eV"][ok], 1, None) / np.clip(g["Vobs"][ok], 1, None)) ** 2)
    return np.concatenate(gb), np.concatenate(go), np.concatenate(w), np.concatenate(gi)
LG = np.linspace(-10.6, -9.4, 1201)
from scipy.optimize import minimize_scalar
def fit_a0(gb, go, w):
    lgo, lgb = np.log10(go), np.log10(gb)
    f = lambda la: np.sum(w * (lgo - lgb - np.log10(C.nu_mono(gb / 10 ** la))) ** 2)
    return minimize_scalar(f, bounds=(-10.6, -9.4), method="bounded", options={"xatol": 1e-4}).x
classes = {"Hubble flow": (1,), "TRGB": (2,), "Cepheid": (3,), "UMa": (4,), "SNe": (5,), "ladder (2+3+5)": (2, 3, 5)}
res = {}
for U in (0.50, 0.70):
    P(f"\nUpsilon_disk = {U:.2f} (Q<=2, N gal {len(GAL)})")
    est = {}
    for nm, fd in classes.items():
        gs = [g for g in GAL if g["meta"]["fD"] in fd]
        gb, go, w, gi = arrays(gs, U, 1.2)
        la = fit_a0(gb, go, w)
        IDX = [np.where(gi == k)[0] for k in range(len(gs))]
        rng = np.random.default_rng(3); bs = []
        for _ in range(500 if nm in ("Hubble flow", "ladder (2+3+5)") else 200):
            pick = rng.integers(0, len(gs), len(gs))
            m = np.concatenate([IDX[p] for p in pick])
            bs.append(fit_a0(gb[m], go[m], w[m]))
        est[nm] = (la, float(np.std(bs)), len(gs))
        P(f"  {nm:16s} N {len(gs):3d}: a0 = {10**la:.3e}  (log {la:+.3f} +- {np.std(bs):.3f})")
    dl = est["Hubble flow"][0] - est["ladder (2+3+5)"][0]; sd = math.hypot(est["Hubble flow"][1], est["ladder (2+3+5)"][1])
    H0n = 73 * 10 ** (-dl / 2)   # a0 ∝ D^-2 ∝ H0^2 for flow distances (sign fixed after first run; disclosed)
    P(f"  Delta (flow - ladder) = {dl:+.3f} +- {sd:.3f} dex ({dl/sd:+.2f} sigma) -> {'SIGNIFICANT' if abs(dl) > 3*sd else 'not significant'}; H0 that nulls it = {H0n:.1f}")
    res[str(U)] = dict(est=est, delta=dl, sd=sd, H0_null=H0n)
rc = 0
if MUT:
    P("(MUTATE: ladder g_obs / 1.2; compare Delta to the main run's)")
    try:
        main = json.load(open(os.path.join(HERE, "sparc_a0_by_distance_results.json")))
        mv = [res[k]["delta"] - main[k]["delta"] for k in res]
        P(f"  Delta moved by {mv}; expected +{2*math.log10(1.2):.3f}... (mutation scales g_obs only, so deep-regime shift ~ +{math.log10(1.2)*2:.3f})")
        rc = 0 if all(abs(x - 2 * math.log10(1.2)) < 0.02 for x in mv) else 1
    except FileNotFoundError:
        rc = 1
json.dump(res, open(os.path.join(HERE, f"sparc_a0_by_distance{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"sparc_a0_by_distance{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc)

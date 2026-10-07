#!/usr/bin/env python3
"""Session 6, F: fossil a0 by Hubble type on gas-dominated deep points in SPARC. Run: python3 fossil_a0_type.py [--mutate]"""
import os, sys, json, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s); OUT.append(str(s))
GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
KPC = 3.0857e19; res = {}
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    E, L = [], []
    for g in GAL:
        T = g["meta"]["T"]
        if 5 < T < 8: continue
        R = g["R"] * KPC; vg2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2
        vb2 = vg2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
        b = vb2 * 1e6 / R; o = (g["Vobs"] * 1e3) ** 2 / R
        ok = (b > 0) & (o > 0) & (np.log10(np.where(b > 0, b, 1)) < -10.5) & (vg2 >= 0.7 * vb2)
        if ok.sum() < 3: continue
        r = np.log10(o[ok]) - np.log10(C.nu_mono(b[ok] / a0) * b[ok])
        w = 1 / (np.clip(g["eV"][ok], 1, None) / np.clip(g["Vobs"][ok], 1, None)) ** 2
        m = float(np.sum(w * r) / np.sum(w))
        (E if T <= 5 else L).append(m + (-0.04 if (MUT and T <= 5) else 0.0))
    E, L = np.array(E), np.array(L); dl = float(np.median(E) - np.median(L))
    rng = np.random.default_rng(47)
    bs = [np.median(E[rng.integers(0, len(E), len(E))]) - np.median(L[rng.integers(0, len(L), len(L))]) for _ in range(2000)]
    sd = float(np.std(bs))
    if sd > 0.02: v = "NON-DISCRIMINATING"
    elif dl < -0.02 and dl / sd < -2: v = "SLOW-SETTLING HINT"
    elif dl > -0.02 and (dl + 0.02) / sd > 2: v = "FAST/NO FOSSIL"
    else: v = "INCONCLUSIVE"
    res[foot] = dict(n_early=len(E), n_late=len(L), delta=dl, sd=sd, verdict=v)
    P(f"{foot:9s}: early (T<=5) N {len(E)}, late (T>=8) N {len(L)}; Delta {dl:+.3f} +- {sd:.3f} -> {v}  (slow-settling prediction ~ -0.04)")
json.dump(res, open(os.path.join(HERE, f"fossil_a0_type{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"fossil_a0_type{TAG}.out"), "w").write("\n".join(OUT) + "\n")
rc = 0
if MUT:
    m = json.load(open(os.path.join(HERE, "fossil_a0_type_results.json")))
    sh = res["canonical"]["delta"] - m["canonical"]["delta"]; rc = 1 if abs(sh + 0.04) < 0.005 else 0
    P(f"MUTATE: Delta shift {sh:+.4f} -> {'detected' if rc else 'NOT detected (median shift need not equal 0.04 exactly)'}")
sys.exit(rc)

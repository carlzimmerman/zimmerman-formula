#!/usr/bin/env python3
"""X80_low_mass_floor_emergence (criteria c1c6d82d69): X77's smooth-core fit on the X48 zooms at 1e10 / 1e11 (K1 on 1e12);
primary R = physical rho0 r0 / (a0/2piG) per footing.   python3 x80_floor.py [--mutate]"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
SRC = os.path.join(REB, "X77_direct_core_surface_density", "x77_direct_eta.py")
T = open(SRC).read(); T = T[:T.index("R = dict(K1=k1")]
NS = {"__file__": SRC, "__name__": "x77_ro"}; exec(compile(T, SRC, "exec"), NS)      # fit(), XA, BS, MUT, K1/K2 synthetic
fit, X48, MUT, P, BS = NS["fit"], NS["X48"], NS["MUT"], NS["P"], NS["BS"]
G_SI, MSUN_PC2 = 6.674e-11, 2.0891e-3                                               # kg/m^2 per Msun/pc^2
SA0 = {f: a0 / (2 * math.pi * G_SI) / MSUN_PC2 for f, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10))}
KS = 4 / (3 * float(BS(1.0)))
X43T = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))["sigma_coll_table"]
TL = sorted((math.log10(float(k)), math.log10(v[0])) for k, v in X43T.items())
def sc_x53(M):                                                                      # X53's log interpolation / extrapolation
    l = math.log10(M); a, b = TL[0], TL[1]
    if l < a[0]: return 10 ** (a[1] + (b[1] - a[1]) / (b[0] - a[0]) * (l - a[0]))
    return 10 ** float(np.interp(l, [t[0] for t in TL], [t[1] for t in TL]))
def argon_cf(M, scoll):
    e0 = KS * 4.46 ** 1.25; return 4.46 * (1 + (SA0["canonical"] / (e0 * scoll)) ** 1.6) ** 0.5
runs = {}
for M in (1e10, 1e11, 1e12):
    for ng in (48, 64):
        for s in range(1, 10):
            d = os.path.join(X48, "runs", f"M{M:.0e}".replace("+", "") + f"_s{s}_ng{ng}")
            sn = os.path.join(d, "snap_zf.npz")
            if not os.path.exists(sn): continue
            Z = np.load(sn); x, m = Z["x"], float(Z["m"]); meta = json.loads(str(Z["meta"]))
            rho = meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + meta["zf"]) ** 3     # physical Msun/Mpc^3
            o, res = fit(x, m, rho, meta["eps"])
            k = os.path.basename(d)
            if res is None: runs[k] = dict(M=M, ng=ng, seed=s, flag=o.get("flag")); continue
            rf = (3 * meta["Mf"] / (4 * math.pi * 18 * math.pi ** 2 * rho)) ** (1 / 3)
            runs[k] = dict(M=M, ng=ng, seed=s, zf=meta["zf"], eta=res["S"]["eta"], a=res["S"]["a"],
                           sigcore=res["S"]["eta"] * 18 * math.pi ** 2 * rho * o["rvir"] / 1e12,
                           scoll_own=18 * math.pi ** 2 * rho * rf / 1e12)
OUTJ = dict(criteria="c1c6d82d69", mutate=MUT, sigma_a0=SA0, runs=runs, summary={})
def boot(v):
    v = np.array(v); g = np.random.default_rng(20261029); b = np.median(v[g.integers(0, len(v), (10000, len(v)))], axis=1)
    return float(np.median(v)), [float(np.percentile(b, 16)), float(np.percentile(b, 84))]
for M in (1e10, 1e11, 1e12):
    for ng in (64, 48):
        ok = [r for r in runs.values() if r["M"] == M and r["ng"] == ng and "eta" in r]
        nf = sum(1 for r in runs.values() if r["M"] == M and r["ng"] == ng and "eta" not in r)
        if not ok: continue
        sc, sb = boot([r["sigcore"] for r in ok]); em, eb = boot([r["eta"] for r in ok])
        so = float(np.median([r["scoll_own"] for r in ok]))
        S = dict(n=len(ok), n_flagged=nf, sigcore=sc, sigcore_b68=sb, eta=em, eta_b68=eb, cf_equiv=(em / KS) ** 0.8,
                 scoll_own=so, scoll_x53=sc_x53(M), secondary_own=em * so, secondary_x53=em * sc_x53(M),
                 R={f: sc / v for f, v in SA0.items()}, R_b68={f: [b / v for b in sb] for f, v in SA0.items()},
                 argon_cf=argon_cf(M, sc_x53(M)))
        OUTJ["summary"][f"{M:.0e}_ng{ng}"] = S
        P(f"M {M:.0e} ng {ng} (n {len(ok)}, flagged {nf}): rho0r0 {sc:.1f} [{sb[0]:.1f}, {sb[1]:.1f}] Msun/pc^2; eta {em:.2f}; "
          f"c_f-equiv {S['cf_equiv']:.2f} (Argon {S['argon_cf']:.2f}); R can {S['R']['canonical']:.3f} alt {S['R']['alt']:.3f}; "
          f"secondary eta*Scoll own {S['secondary_own']:.1f} / X53 {S['secondary_x53']:.1f}")
SM = OUTJ["summary"]
k1 = "1e+12_ng64" in SM and abs(SM["1e+12_ng64"]["eta"] - 20.82756174581007) < 1e-6 and abs(SM["1e+12_ng64"]["sigcore"] - 134.9) < 0.05
OUTJ["K1"] = k1; P(f"K1 1e12 ng64 vs X77 (eta 20.8276, rho0r0 134.9): {'PASS' if k1 or MUT else 'FAIL'}")
def classify(foot, r10, r11):
    if r10 < 0.71: return "FLOOR BY HAND"
    if r10 > 1.41: return "NATIVE OVERSHOOT"
    if 0.71 <= r11 <= 1.41 and abs(math.log10(r10 / r11)) <= 0.10: return "FLOOR EMERGES"
    return "PARTIAL"
V = {}
for foot in SA0:
    a, b = SM.get("1e+10_ng64"), SM.get("1e+11_ng64")
    if a is None or b is None or a["n"] < 6 or b["n"] < 6: V[foot] = "UNDECIDED"; continue
    c = classify(foot, a["R"][foot], b["R"][foot])
    lo, hi = (classify(foot, a["R_b68"][foot][i], b["R"][foot]) for i in (0, 1))
    if lo != c or hi != c: c += " [NOISE-LIMITED]"
    for M in ("1e+10", "1e+11"):
        if f"{M}_ng48" in SM and abs(SM[f"{M}_ng64"]["sigcore"] / SM[f"{M}_ng48"]["sigcore"] - 1) > 0.20: c += f" [RESOLUTION-DEPENDENT {M}]"
    V[foot] = c
lab = V["canonical"] if V["canonical"].split(" [")[0] == V["alt"].split(" [")[0] else f"FOOTING-SPLIT (canonical {V['canonical']}; alt {V['alt']})"
OUTJ.update(verdict=V, label=lab); P(f"VERDICT: {lab}   per footing {V}")
with open(os.path.join(HERE, "x80_results_MUTATE.json" if MUT else "x80_results.json"), "w") as f: json.dump(OUTJ, f, indent=1)
sys.exit(0 if (k1 or MUT) else 1)

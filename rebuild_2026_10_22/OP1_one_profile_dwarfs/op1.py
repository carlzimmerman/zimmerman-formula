#!/usr/bin/env python3
"""OP1: native z = 0 profile on LG dwarfs; criteria FROZEN_CRITERIA.md. python3 op1.py [--mutate] [--shapes FILE --tags 1e8,1e9,1e10]"""
import contextlib, io, json, math, os, sys
import numpy as np
MUT = "--mutate" in sys.argv; RX = 1.5 if MUT else 1.0
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); SN = os.path.join(REB, "SN1_dwarf_s_need", "sn1.py"); src = open(SN).read(); src = src[:src.index("RES = dict(frozen")]
g = {"__file__": SN, "__name__": "x"}; a_ = sys.argv; sys.argv = ["sn1.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, SN, "exec"), g)
sys.argv = a_; sys.path.insert(0, os.path.join(REB, "RG1_native_n_regrade")); import rg1_lib as L
G, MSUN, PC, CLS = g["G"], g["MSUN"], g["PC"], g["CLS"]; RHOC = g["RHOC"]
J = json.load(open(os.path.join(REB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); LX = np.log(np.array(J["x"]))
TAGS = sorted(((float(J[t]["0.00"]["lgM"]), np.array(J[t]["0.00"]["lnm"])) for t in ("1e10", "1e11", "1e12")), key=lambda x: x[0])
def shape(lg, mode):
    if mode == "tag10": return TAGS[0][1]
    if mode == "tag12": return TAGS[2][1]
    if mode == "trend":                                                       # carry 1e10-1e12 trend of ln m below the tag
        return TAGS[0][1] + (lg - TAGS[0][0]) * (TAGS[2][1] - TAGS[0][1]) / (TAGS[2][0] - TAGS[0][0])
def Mh(r, M200, mp, mode):
    lg = math.log10(M200); R = (3 * (M200 if mp == "FC1" else M200 / L.FC) / (4 * math.pi * 200 * RHOC * MSUN / (PC * 1e6) ** 3 * 0 + 4 * math.pi * 200 * RHOC * 0 + 800 * math.pi * RHOC)) ** (1 / 3) if False else (3 * ((M200 if mp == "FC1" else M200 / L.FC) * MSUN) / (800 * math.pi * RHOC)) ** (1 / 3)
    ln = shape(lg, mode); lx = math.log(max(min(r, R) / (R * RX), 1e-300)); v = float(np.interp(lx, LX, ln)) if lx >= LX[0] else float(ln[0] + 2 * (lx - LX[0])); return M200 * MSUN * math.exp(v), R
def Eall(Q, lM, mp, mode):
    return np.array([math.log10(q["gobs"] / (q["gN"] + G * Mh(q["r12"], 10 ** l, mp, mode)[0] / q["r12"] ** 2)) for q, l in zip(Q, lM)])
RES = {}
for f in g["FEET"]:
    Q = g["systems"](f); idx = g["boot_setup"](Q); lm = np.array([q["lm"] for q in Q]); lE = np.log10([q["M200"] / MSUN for q in Q]); RES[f] = {}
    # K1
    if not MUT: print(f, "K1 m(0.1) tag10", round(math.exp(float(np.interp(math.log(.1), LX, TAGS[0][1]))), 4))
    for mp in ("FC1", "frozen"):
        F = RES[f][mp] = {}
        for mode in ("tag10", "trend", "tag12"):
            z = g["clsZ"](Eall(Q, lE, mp, mode), Q, idx); F["P1_" + mode] = {c: dict(E=v[0], Z=v[2]) for c, v in z.items()}
            print(f, mp, mode, "P1", {c[:8]: (round(v[0], 3), round(v[2], 2)) for c, v in z.items()}, flush=True)
        F["P1"] = "PROFILE HOLDS" if all(abs(v["Z"]) < 2 for v in F["P1_tag10"].values()) else "FAIL: " + ", ".join(c for c, v in F["P1_tag10"].items() if abs(v["Z"]) >= 2)
        eps = lambda l: 714 * PC * 10 ** ((l - 10) / 3); F["P3"] = {c: float(np.mean([Q[i]["r12"] < 3 * eps(lE[i]) for i in idx[c][0]])) for c in CLS}
        ad = []
        for a in np.round(np.arange(6, 12.01, .05), 2):
            for b in np.round(np.arange(-.6, 2.01, .05), 2):
                l = a + b * (lm - 7); z = g["clsZ"](Eall(Q, l, mp, "tag10"), Q, idx); m = max(abs(v[2]) for v in z.values())
                if m < 2: ad.append((float(a), float(b), m))
        A = np.array(ad) if ad else np.zeros((0, 3)); near = A[abs(A[:, 0] + A[:, 1] - 9.38) < .3] if ad else A
        F["P2"] = dict(n=len(ad), verdict=("LINE ADMITTED" if ad else "NO LINE") + (", MEETS EM1" if len(near) else ""), n_near=len(near))
        if ad:
            F["P2"].update(a=[float(A[:, 0].min()), float(A[:, 0].max())], b=[float(A[:, 1].min()), float(A[:, 1].max())], best=A[np.argmin(A[:, 2])].tolist(), lgM_lm4=[float((A[:, 0] - 3 * A[:, 1]).min()), float((A[:, 0] - 3 * A[:, 1]).max())], lgM_lm6=[float((A[:, 0] - A[:, 1]).min()), float((A[:, 0] - A[:, 1]).max())])
        if len(near): F["P2"].update(near_b=[float(near[:, 1].min()), float(near[:, 1].max())], near_lgM_lm4=[float((near[:, 0] - 3 * near[:, 1]).min()), float((near[:, 0] - 3 * near[:, 1]).max())], near_bestZ=float(near[:, 2].min()))
        print(f, mp, F["P1"], "| P2", F["P2"], "| P3", {c[:8]: round(v, 2) for c, v in F["P3"].items()}, flush=True)
json.dump(RES, open(os.path.join(HERE, "op1_results" + ("_MUTATE" if MUT else "") + ".json"), "w"), indent=1)

#!/usr/bin/env python3
"""NP1 POST-RESULT checks, written after np1_real and np1_oracle were read; they change no frozen label.
(1) Why RQ3's dwarf rows A11-A13 read NOT COMPUTABLE: is the frozen rule's g monotone in g_b at fixed r and gas share? (2) Label sensitivity: the hull line 0.9 and the
fixed-Upsilon rows A5-A7. Run: PYTHONHASHSEED=0 nice -n 10 python3 -I np1_post.py. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import np1_cand as K, np1_core as C
OUT = []
def P(*a): s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RR = json.load(open(os.path.join(HERE, "np1_real.json"))); RO = json.load(open(os.path.join(HERE, "np1_oracle.json"))); res = {}
for arm in C.ARMS:
    RS = K.load(f"real_{arm}"); cx = C.cx_rows("canonical")
    for ft, a0 in C.FOOT.items():
        o = {}
        for L in C.CX_LINES + ("SPARC",):
            if L == "SPARC": gb = C.SH[:, 0]; r = C.SH[:, 2] * C.CL ** 2 / C.A0C; gg = gb * C.SH[:, 3]
            else:
                q = [x for x in cx if x["line"] == L]; gb = np.array([x["y"] for x in q]) * C.A0C; r = np.array([x["ell"] for x in q]) * C.CL ** 2 / C.A0C; gg = gb * np.array([x["f"] for x in q])
            dec = 0; n = 0
            for k in range(len(gb)):
                g = np.geomspace(0.3, 3.0, 25) * gb[k]; v = K.g_of_Q(RS, dict(gb=g, gg=g * (gg[k] / gb[k]), r=np.full(25, r[k]), a0=a0)); n += 1; dec += bool(np.any(np.diff(v) <= 0))
            o[L] = dict(n=n, non_monotone=dec)
        res[f"{arm}|{ft}"] = dict(monotone=o); P(f"{arm} {ft}: points where g(g_b) is not increasing over g_b x 0.3-3 at fixed r, gas share: {o}")
    for ft in C.FOOT:
        G = RR[arm][ft]; O = RO[arm][ft]["oracle"]; s = G["hull"]["SPARC"]["in_hull"]; fl = [l for l in G["stage3"]["fails"]]
        P(f"{arm} {ft}: SPARC in-hull fraction {s:.3f} against the frozen line 0.90; A10 IC 1613 in-hull fraction {G['hull']['IC1613']['in_hull']:.2f}, reach median {G['hull']['IC1613']['reach_med']:.2f}")
        for line in (0.85, 0.95):
            carried = [k for k in fl if k in ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A21") and s >= line and k in O["stage3"]["fails"]] + [k for k in fl if k == "A10" and G["hull"]["IC1613"]["in_hull"] >= line and k in O["stage3"]["fails"]]
            P(f"   hull line {line}: in-hull failures the oracle also fails: {carried}")
        nf = [k for k in fl if k in ("A10",) and G["hull"]["IC1613"]["in_hull"] >= 0.9 and "A10" in O["stage3"]["fails"]]
        P(f"   without A5-A7 (train targets at fixed Upsilon 0.5, so the rule's implied Upsilon can't move): carried by {nf or 'nothing'}")
P("POST-RESULT; no frozen label changes. kappa = 1/2 FITTED; not theory closed.")
json.dump(res, open(os.path.join(HERE, "np1_post.json"), "w"), indent=0); open(os.path.join(HERE, "np1_post.out"), "w").write("\n".join(OUT) + "\n")

"""HO1 POST-RUN DIAGNOSTIC (not frozen, not graded): why K2 (GS1 turnaround start independence, 1e-5) failed at 3.6e-4,
and whether it can move the X-COP grade. Executes ho1_heldout.py up to its grading block (no outputs written there)."""
import os, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SRCF = os.path.join(HERE, "ho1_heldout.py")
src = open(SRCF).read(); src = src[:src.index("# ------------------------------------------------------------------ 6. grade per footing")]
G = {"__file__": SRCF, "__name__": "ho1_ro"}; exec(compile(src, SRCF, "exec"), G)
out = {}; lines = []
def say(s): print(s, flush=True); lines.append(s)
# iterate the GS1 map by hand to its true fixed point (same r_ta_com / Mbx as _gc2_ext)
for c in G["XC"]:
    m = G["XMETA"][c["name"]]; R5 = m["r500"] / 1e3
    res = {}
    for sf in (0.3, 1.0, 3.0):
        Mbx, Mbt = G["gc2_ext"](m["Mg500"], R5, m["z"], sf * 3.0 * 1.2 * m["Mg500"] * G["MSUNX"]); res[sf] = Mbt
    Mbt = res[1.0]; rta = G["r_ta_com"](Mbt) / (1 + m["z"]); n = 0
    for n in range(1, 100000):
        Mn = float(np.interp(rta, G["RM"], Mbx)); new = G["r_ta_com"](Mn) / (1 + m["z"])
        if abs(new / rta - 1) < 1e-13: break
        rta = new
    Mtrue = float(np.interp(rta, G["RM"], Mbx))
    out[c["name"]] = dict(starts={str(k): v / Mtrue - 1 for k, v in res.items()}, extra_iters=n)
    say(f"{c['name']}: Mbt(start x0.3, x1, x3)/true - 1 = " + ", ".join(f"{v / Mtrue - 1:+.2e}" for v in res.values()) + f"; extra iterations to 1e-13: {n}")
# grade sensitivity: shift every cluster's Mbt by the worst start offset, both signs
orig = G["budget"]
for eps in (-4e-4, 4e-4):
    def b2(name, start_fac=1.0, eps=eps):
        Mbt, rta, fp = orig(name, start_fac); Mbt *= 1 + eps; return Mbt, G["r_ta_com"](Mbt) / (1 + G["XMETA"][name]["z"]), fp
    G["budget"] = b2
    for f in G["FEET"]:
        x = G["xcop_cl2"](f); out[f"eps{eps:+.0e}_{f}"] = dict(mean=x["mean"], rms=x["rms"])
        say(f"M_b,t x (1 {eps:+.0e}) [{f}]: X-COP mean {x['mean']:+.5f}, rms {x['rms']:.5f}")
G["budget"] = orig
open(os.path.join(HERE, "ho1_k2_diagnostic.out"), "w").write("\n".join(lines) + "\n")
json.dump(out, open(os.path.join(HERE, "ho1_k2_diagnostic.json"), "w"), indent=1)

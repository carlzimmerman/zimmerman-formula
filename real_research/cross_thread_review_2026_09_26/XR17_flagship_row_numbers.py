"""XR17 -- the committed script behind the answer page's flagship row (flat-a0 flagship at z = 2.5, M*'s carrier).

The row adopts two numbers and computes nothing new:
  S_crit   the carrier residue at r_F above which the worst flagship host shifts by more than 0.10 dex, with the switch
           on at r_F (MS2's door), from DE4's committed evaluate();
  shift    the worst host's shift at z = 2.5 for L388's committed pooled fixed-cell residues (z = 2) at each kick.

No new knob: DE4's evaluate() and L388's pooled table are read from their committed files. Control: DE4's committed F1
table is reproduced first (its max |deviation| is printed). Written by the advancement thread when AT5 was halted and
copied here unchanged apart from the repository path (made relative) and this docstring.

Run from anywhere: python3 real_research/cross_thread_review_2026_09_26/XR17_flagship_row_numbers.py
"""
import os, io, contextlib, math, json
import numpy as np
from scipy.optimize import brentq
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P4 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE4_flagship_matter_only_switch.py")
src = open(P4).read().split("# ============================================================================================ C1-C3 controls")[0]
NS = {"__name__": "de4", "__file__": P4}
os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, NS)
ev = NS["evaluate"]
F1 = json.load(open(P4.replace(".py", "_results.json")))["numbers"]["F1"]
d = max(abs(r["shift"] - q["shift"]) for k in F1 for r, q in zip([ev(10 ** l, f, 2.5, 1.0, 2.5, float(k.split("/")[1]), float(k.split("/")[0])) for l in (10.0, 10.5, 11.0) for f in ("canonical", "alt")], F1[k]["rows"]))
print(f"control: DE4 F1 reproduced, max |dev| {d:.1e}")
# on the door (MS2) the switch is on at r_F for every f_CGM: use upper=True (on) -- the shift depends only on S once on
worst = lambda S: max(ev(10 ** l, f, 2.5, 1.0, 2.5, S, 0.1, upper=True)["shift"] for l in (10.0, 10.5, 11.0) for f in ("canonical", "alt"))
Sc = brentq(lambda S: worst(S) - 0.10, 1e-4, 0.5)
print(f"S_crit (worst host, on): {Sc:.4f}")
L388 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L388_linear_gate_pooled_results.json")))["numbers"]["table"]["pooled"]
for v in ("v575", "v600", "v625", "v650"):
    S = L388[v]["clear_fixed"]; print(f"  M*'s carrier {v}: fixed-cell residue at z = 2 {S:.4f} -> worst shift at z = 2.5 {worst(S):+.4f} dex")

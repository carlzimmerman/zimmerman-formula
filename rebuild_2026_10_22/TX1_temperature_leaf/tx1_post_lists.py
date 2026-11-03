#!/usr/bin/env python3
"""TX1 POST, after the frozen top 10 read on keys: one form per T motif among real train passes (lowest Z), and the top 3 for the frozen sensitivities. No label rests on these. kappa = 1/2 FITTED; not theory closed."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
for f in ("canonical", "alt"):
    J = json.load(open(os.path.join(H, f"tx1_train_TL0_{f}_real.json"))); best = {}
    for r in J["train_pass"]:
        m = tuple(sorted(set(re.findall(r"\([^()]*s2[^()]*\)", r["F"]))))
        if m and r["T"] and (m not in best or r["Z"] < best[m]["Z"]): best[m] = r
    L = [r["F"] for r in sorted(best.values(), key=lambda r: r["Z"])]; json.dump(L, open(os.path.join(H, "chunks", "lists", f"{f}_post.json"), "w"), indent=0); json.dump([r["F"] for r in J["T"][:3]], open(os.path.join(H, "chunks", "lists", f"{f}_top3.json"), "w"), indent=0); print(f, len(L))

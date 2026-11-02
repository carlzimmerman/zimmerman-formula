#!/usr/bin/env python3
"""UX5 post-result, no class change: what K line form A or Q would need; the same data's chi2 line vs its summary. kappa = 1/2 FITTED; not theory closed."""
import json
O=[]
for foot in ("canonical","alt"):
    rows=[json.loads(l) for l in open(f"cache/{foot}_1.0.jsonl")]
    for f in ("A","Q"):
        for box in ("B175","BV","BV2"):
            for tag,sel in (("all",lambda r:True),("in-prior",lambda r:r["inp"])):
                rb=[r for r in rows if r["box"]==box and sel(r)]
                a=[r for r in rb if r[f]["L1"]]; b=[r for r in a if r[f]["L2a"]]; c=[r for r in b if r[f]["L3"]]
                k=lambda x:(f"{min(r[f]['K0'] for r in x):.1f}" if x else "none")
                O.append(f"[{foot}] {box} {f} {tag}: n {len(rb)}; v_c {len(a)} min K {k(a)}; +chi2_Kz {len(b)} min K {k(b)}; +Ou {len(c)} min K {k(c)}")
open("ux5_post_k.out","w").write("\n".join(O)+"\n"); print("\n".join(O))

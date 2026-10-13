#!/usr/bin/env python3
"""CFG668 post-hoc diagnostic (no verdict weight): the frozen decile matching failed its 0.02-dex control (per-bin median offsets up
to 0.16 dex). Re-run the same estimator with 40 bins in log M_b (min 100 lenses of each type per bin) and report the per-bin offsets."""
import os, json, math
os.environ.pop("CFG668_MUTATE", None)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg668.py")).read()
head = src.split('P(f"CFG668  early-type excess')[0]
head = head.replace("np.linspace(0, 1, 11)", "np.linspace(0, 1, NB + 1)").replace("for i in range(10):", "for i in range(NB):") \
           .replace("if nE < 300 or nL < 300:", "if nE < MINN or nL < MINN:")
ns = {"__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg668.py"), "__name__": "diag", "NB": 40, "MINN": 100}
exec(compile(head, "cfg668_head", "exec"), ns)
out = {}
for nm, key in (("L", "LMG"), ("T", "LMBT")):
    em, lm_, r, info = ns["matched"](ns[key])
    a = ns["amp"](em, lm_, r)
    offs = [b["med_E"] - b["med_L"] for b in info if not b["dropped"]]
    out[nm] = dict(K9=a["K9"]["A"], sK9=a["K9"]["s"], Kin=a["Kin+mid"]["A"], sKin=a["Kin+mid"]["s"],
                   used=sum(not b["dropped"] for b in info), max_off=max(map(abs, offs)), mean_off=sum(offs) / len(offs),
                   loo9=a["K9"]["loo"].tolist(), looin=a["Kin+mid"]["loo"].tolist())
    print(f"[{nm}] 40-bin matching: bins used {out[nm]['used']}; max |median offset| {out[nm]['max_off']:.4f}, mean {out[nm]['mean_off']:+.4f} dex; "
          f"K9 A = {out[nm]['K9']:+.4f} +- {out[nm]['sK9']:.4f}; inner A = {out[nm]['Kin']:+.4f} +- {out[nm]['sKin']:.4f}")
import numpy as np
N = ns["NPATCH"]
for k, lk in (("K9", "loo9"), ("inner", "looin")):
    dl = np.array(out["L"][lk]) - np.array(out["T"][lk])
    d = out["L"]["K9" if k == "K9" else "Kin"] - out["T"]["K9" if k == "K9" else "Kin"]
    print(f"Delta {k}: {d:+.4f} +- {math.sqrt((N - 1) / N * ((dl - dl.mean()) ** 2).sum()):.4f}")
for v in out.values():
    v.pop("loo9"); v.pop("looin")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg668_finebin_diag.json"), "w"), indent=1)

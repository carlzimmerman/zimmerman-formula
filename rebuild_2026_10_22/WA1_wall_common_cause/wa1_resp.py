#!/usr/bin/env python3
"""WA1 responses through the real rows. python3 wa1_resp.py cid foot -> resp/cid_foot.json. Nodes -2,-1,0,1,2 sigma for ups, hse, gas_abs, dist, lens; injections for K1 on LAW. kappa = 1/2 FITTED; not theory closed."""
import json, sys, warnings
warnings.filterwarnings("ignore")
from wa1_rows import *
cid, foot = sys.argv[1:3]; c = load_cand(cid); RD = os.path.join(HERE, "resp"); os.makedirs(RD, exist_ok=True)
GROUPS = dict(ups=["sparc", "dw", "tdg", "lens", "groups", "b2", "xcop", "a21"], hse=["b2", "xcop"], gas_abs=["b2", "xcop"], dist=["sparc", "groups", "b2", "xcop", "a21"], lens=["lens"])
base = {k: 0.0 for k in ("ups", "gas_abs", "dist", "lens")}; base["hse"] = NUIS["hse"][0]
def P(n=None, x=0.0):
    t = dict(base)
    if n: t[n] = NUIS[n][0] + NUIS[n][1] * x
    return t
L0, G0, S0 = evaluate(cid, c, foot, P()); sd = S0; R = dict(cid=cid, foot=foot, z0=L0, gates0=G0, extra=S0, nodes={})
try: R["boot"] = ups_boot(Wrap(c), foot)
except Exception as e: R["boot"] = None
# RQ3's nominal: no HSE shift, for K0
Lq, Gq, Sq = evaluate(cid, c, foot, dict(base, hse=0.0), want=["b2", "xcop", "groups"]); R["k0"] = dict(lines=Lq, extra=Sq)
for n, w in GROUPS.items():
    R["nodes"][n] = {}
    for x in (-2.0, -1.0, 1.0, 2.0):
        l, g, s = evaluate(cid, c, foot, P(n, x), want=w); R["nodes"][n][str(x)] = dict(l=l, g=g)
if cid == "LAW":
    R["inj"] = {}
    for tag, th in (("all+", {k: (1 if i % 2 == 0 else -1) for i, k in enumerate(GROUPS)}), ("all-", {k: (-1 if i % 2 == 0 else 1) for i, k in enumerate(GROUPS)})):
        t = dict(base)
        for k, v in th.items(): t[k] = NUIS[k][0] + NUIS[k][1] * v
        l, g, s = evaluate(cid, c, foot, t, mw_cache={}); R["inj"][tag] = dict(theta=th, l=l)
    for n in GROUPS:
        l, g, s = evaluate(cid, c, foot, P(n, 1.5), mw_cache={}); R["inj"][n] = dict(theta={n: 1.5}, l=l)
json.dump(R, open(os.path.join(RD, f"{cid}_{foot}.json"), "w"), indent=0, sort_keys=True, default=float); print("done", cid, foot, flush=True)

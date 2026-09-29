"""seed 183 vs 184 stability of every reported mock fraction (frozen line: within +-0.02). Exit 0."""
import json, os
import CFG183_common as C
from CFG183_common import pr
a = json.load(open(os.path.join(C.HERE, "CFG183_null_e_results_seed183.json")))["results"]
b = json.load(open(os.path.join(C.HERE, "CFG183_null_e_results_seed184.json")))["results"]
worst = (0, None); n = 0; over = 0
for ra, rb in zip(a, b):
    assert (ra["world"], ra["fam"]) == (rb["world"], rb["fam"])
    for k, v in ra.items():
        if k.startswith("P_") or k == "floored":
            d = abs(v - rb[k]); n += 1; over += d > 0.02
            if d > worst[0]: worst = (d, (ra["world"], ra["fam"], k, v, rb[k]))
pr("stability seed 183 vs 184: %d fractions compared, max |diff| %.4f at %s; %d exceed the frozen 0.02 line" % (n, worst[0], worst[1], over))
pr("(binomial sampling error of a fraction at N=10000 is <= 0.005, so a miss would be a mock-noise issue)" )

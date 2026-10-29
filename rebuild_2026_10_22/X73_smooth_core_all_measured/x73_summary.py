#!/usr/bin/env python3
"""X73_smooth_core_all_measured: apply the frozen verdict rule (FROZEN_CRITERIA.md, f5ed2b706b) to the committed run JSONs.
Reads x73_results_*.json only; writes x73_summary.json. kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed.

    python3 -I x73_summary.py
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
FEET, HK = ("canonical", "alt"), ("h0672", "h0686")
S16, SM, S84 = "s2.6756", "s2.7774", "s3.0711"
J = lambda t: json.load(open(os.path.join(HERE, f"x73_results_{t}.json")))


def grade(r, f):
    F = r["footings"][f]; cl = F["clusters"]
    bad = [k for h in HK for k, v in cl["cells"][h].items() if abs(v["Z"]) > 2]
    det = ([] if all(s["line"] for s in F["sparc"].values()) else ["SPARC line"]) + \
          ([] if abs(F["groups"]["Z"]) <= 2 else [f"groups Z {F['groups']['Z']:+.2f}"]) + sorted(set(bad))
    return det


def cls(fs_list, slope, f):
    det = {fs: grade(J(f"fs{fs}_S_nat_{slope}"), f) for fs in fs_list}
    named = sorted({d for v in det.values() for d in v})
    return ("ALL-MEASURED PASSES" if not named else "ALL-MEASURED BREAKS: " + ", ".join(named)), det


OUT = {"criteria": "f5ed2b706b", "settings": "kappa = 1/2 FITTED; c_f EXTERNAL; footings never pooled; not theory closed",
       "identities": {}, "verdict": {}, "robustness": {}, "M3_Z": {}}
for t in ("fs0.2_B_nat_s2.7774", "fs0.2_S_inh_notail", "fs0.034_S_inh_notail"):
    OUT["identities"][t] = J(t)["identity"]
m3 = lambda t: J(t)["footings"]["canonical"]["clusters"]["cells"]["h0672"]["G-OUT-M3"]["pred"]
OUT["mutate_sensitive"] = m3("fs0.6_S_nat_s2.7774") > m3("fs0.2_S_nat_s2.7774")
for f in FEET:
    v, det = cls(("0.034", "0.0615"), SM, f)
    edges = {s: cls(("0.034", "0.0615"), s, f)[0] for s in (S16, S84)}
    same = all(e.split(":")[0] == v.split(":")[0] and (e == v or not v.startswith("ALL-MEASURED PASSES")) for e in edges.values())
    OUT["verdict"][f] = v; OUT["robustness"][f] = {"class": "ROBUST" if same else "FRAGILE", "edges": edges, "detail": det}
for fn in sorted(os.listdir(HERE)):
    if fn.startswith("x73_results_"):
        t = fn[12:-5]; r = J(t)
        OUT["M3_Z"][t] = {f: [r["footings"][f]["clusters"]["cells"][h]["G-OUT-M3"]["Z"] for h in HK] for f in FEET}
ok = all(i["ok"] for i in OUT["identities"].values()) and OUT["mutate_sensitive"]
OUT["checks_pass"] = ok
json.dump(OUT, open(os.path.join(HERE, "x73_summary.json"), "w"), indent=1)
for f in FEET: print(f"[{f}] {OUT['verdict'][f]}  ({OUT['robustness'][f]['class']}; edges {OUT['robustness'][f]['edges']})")
print("identities", {k: v["ok"] for k, v in OUT["identities"].items()}, "mutate sensitive", OUT["mutate_sensitive"])
raise SystemExit(0 if ok else 1)

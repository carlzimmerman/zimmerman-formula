#!/usr/bin/env python3
"""CFG498 verdict (FROZEN_CRITERIA.md d9c739010, section 3), read from the committed JSONs of the legs.
RECONCILED iff (a) growth PASS (GROWTH OK both footings, MUTATE-N detected) AND (b) KiDS PASS AND (c) SPARC PASS.
(d) early-type levels are reported only.  V1 = MS1 EXCEPTION (NOT ADMISSIBLE under original MS1); V2 = strict MS1.
Run: python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_verdict.py
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(HERE, f)))
D, G, X = J("cfg498_data_results.json"), J("cfg498_growth_results.json"), J("cfg498_early_results.json")
OUT, RES = [], {"lane": "CFG498", "script": "cfg498_verdict"}


def P(s=""):
    print(s, flush=True); OUT.append(s)


det = G["mutateN_detected"]
P(f"MUTATE-N detected: {det}")
for v in ("V1", "V2"):
    rc, ra = G["runs"][f"{v}-CAP canonical"], G["runs"][f"{v}-CAP alt"]
    ga = rc["verdict"] == "GROWTH OK" and ra["verdict"] == "GROWTH OK" and bool(det)
    kb, sc = D[f"kids_pass_{v}"], D[f"sparc_pass_{v}"]
    early = X[f"early_levels_ok_{v}"]
    fails = [n for n, ok in (("(a) growth", ga), ("(b) KiDS", kb), ("(c) SPARC", sc)) if not ok]
    if not fails:
        verdict = "RECONCILED"
    elif fails == ["(a) growth"] and rc["verdict"] == "GROWTH OK" and ra["verdict"] == "GROWTH OK" and not det:
        verdict = "RECONCILED, GROWTH NOT DIAGNOSTIC"
    else:
        verdict = "NOT RECONCILED (" + ", ".join(fails) + ")"
    ms1 = "MS1 EXCEPTION; NOT ADMISSIBLE under original MS1" if v == "V1" else "strict MS1"
    kd = {f: D["kids"][f]["rows"][f"{v}_cap"]["d_vs_best"] for f in ("canonical", "alt")}
    sp = {f: (D["sparc"][f][f"{v}_cap"]["A3_spiral"], D["sparc"][f][f"{v}_cap"]["A3_dwarf"], D["sparc"][f][f"{v}_cap"]["drms"]) for f in ("canonical", "alt")}
    RES[v] = dict(verdict=verdict, ms1=ms1, growth=[rc["verdict"], ra["verdict"]], s8=[rc["s8"], ra["s8"]], pdev=[rc["pdev"], ra["pdev"]],
                  kids_d_vs_best=kd, sparc=sp, early_levels_ok=early)
    P(f"{v}: {verdict}  [{ms1}]")
    P(f"   (a) growth {rc['verdict']} / {ra['verdict']}: s8 {rc['s8']:.4f} / {ra['s8']:.4f}, max|P-1| {rc['pdev']:.4f} / {ra['pdev']:.4f}")
    P(f"   (b) KiDS chi2 - best {kd['canonical']:+.3f} / {kd['alt']:+.3f} -> {'PASS' if kb else 'FAIL'}")
    P(f"   (c) SPARC A3 sp/dw/drms canonical {sp['canonical'][0]:.3f}/{sp['canonical'][1]:.3f}/{sp['canonical'][2]:+.4f}, alt {sp['alt'][0]:.3f}/{sp['alt'][1]:.3f}/{sp['alt'][2]:+.4f} -> {'PASS' if sc else 'FAIL'}")
    P(f"   (d) early-type levels (reported) {'OK' if early else 'NOT OK'}")
RES["mutateN_detected"] = det
RES["run_512"] = any(RES[v]["verdict"] == "RECONCILED" for v in ("V1", "V2"))
P(f"512^3 run warranted by the frozen rule: {RES['run_512']}")
json.dump(RES, open(os.path.join(HERE, "cfg498_verdict_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg498_verdict.out"), "w").write("\n".join(OUT) + "\n")

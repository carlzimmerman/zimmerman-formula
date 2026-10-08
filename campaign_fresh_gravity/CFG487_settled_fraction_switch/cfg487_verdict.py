#!/usr/bin/env python3
"""CFG487 verdict (FROZEN_CRITERIA.md section 4): reads the committed results of cfg487_data.py, cfg487_wellposed.py and
cfg487_growth_analysis.py and applies the frozen per-version rule:
  PASS: (a) SPARC and (b) KiDS pass, (c) GROWTH OK on both footings with MUTATE-A detected, (d) passes;
  PASS, GROWTH NOT DIAGNOSTIC: as PASS but MUTATE-A is GROWTH OK;  FAIL (legs): otherwise.
V1 always carries 'MS1 EXCEPTION; NOT ADMISSIBLE under original MS1'.
Run: python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_verdict.py
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "cfg487_data_results.json")))
Wp = json.load(open(os.path.join(HERE, "cfg487_wellposed_results.json")))
Gr = json.load(open(os.path.join(HERE, "cfg487_growth_results.json")))
L, OUT = [], {"lane": "CFG487", "script": "cfg487_verdict"}


def P(s=""):
    print(s, flush=True); L.append(s)


det = Gr.get("mutateA_detected")
rows = {}
for v in ("V1", "V2"):
    a = D[f"sparc_pass_{v}"]; b = D[f"kids_pass_{v}"]; d = Wp[f"d_pass_{v}"]
    gc = Gr["runs"].get(f"{v} canonical"); ga = Gr["runs"].get(f"{v} alt")
    gok = bool(gc and ga and gc["verdict"] == "GROWTH OK" and ga["verdict"] == "GROWTH OK")
    fails = [n for n, ok in (("SPARC", a), ("KiDS", b), ("growth", gok), ("well-posedness", d)) if not ok]
    if fails:
        verdict = "FAIL (" + ", ".join(fails) + ")"
    else:
        verdict = "PASS" if det else "PASS, GROWTH NOT DIAGNOSTIC"
    if v == "V1":
        verdict += "; MS1 EXCEPTION, NOT ADMISSIBLE under original MS1"
    rows[v] = dict(sparc=a, kids=b, growth=(gc["verdict"] if gc else None, ga["verdict"] if ga else None), growth_ok=gok, d=d, verdict=verdict)
    P(f"{v}: SPARC {'PASS' if a else 'FAIL'} | KiDS {'PASS' if b else 'FAIL'} | growth {rows[v]['growth'][0]} / {rows[v]['growth'][1]} "
      f"(MUTATE-A detected: {det}) | (d) {'PASS' if d else 'FAIL'}  ->  {verdict}")
OUT["versions"] = rows
OUT["mutateA_detected"] = det
json.dump(OUT, open(os.path.join(HERE, "cfg487_verdict_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg487_verdict.out"), "w").write("\n".join(L) + "\n")

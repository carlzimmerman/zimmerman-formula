#!/usr/bin/env python3
"""OB1 — JWST observation design (door: L05/K09). Registered program arithmetic,
every number recomputed from committed files (no transcription):
  - L05_results.json .power  : detection-rate grid central_N{1,10,30}_SN{10,30,100}_f{10,15,20}
  - L03_results.json .jwst_reach_summary : pair reach S/N = 50 (q0/q2)
  - K11_results.json .tests  : falsifier schedule T1-T5 (verbatim into the program doc)
Pre-registered kill: if the minimal registered configuration (P>=0.95 on the 2x-radius
3-sigma program) requires per-object S/N > 50 (the L03-tested JWST pair reach) ->
INFEASIBLE-JWST, exit 1 honestly. Else exit 0 with margin 50/SN_req.
"""
import json, sys, re
import numpy as np

OUT_MD = "OB1_JWST_PROGRAM.md"
OUT_JS = "OB1_results.json"

def load():
    l05 = json.load(open("L05_results.json"))
    l03 = json.load(open("L03_results.json"))
    k11 = json.load(open("K11_results.json"))
    return l05, l03, k11

def main():
    l05, l03, k11 = load()
    power = l05["power"]
    # parse grid: N, S/N, feature fraction f
    grid = {}
    for key, val in power.items():
        m = re.match(r"central_N(\d+)_SN(\d+)_f(\d+)", key)
        if not m:
            continue
        N, sn, f = int(m.group(1)), int(m.group(2)), int(m.group(3))
        grid.setdefault(f, {})[(N, sn)] = val["rate"]
    feas = []
    for f in sorted(grid):
        for (N, sn), rate in sorted(grid[f].items()):
            if rate >= 0.95:
                feas.append({"f": f, "N": N, "SN": sn, "rate": rate})
    # minimal per-object S/N among feasible configs (registered program: P>=0.95)
    feas.sort(key=lambda r: (r["SN"], r["N"]))
    minimal = feas[0] if feas else None
    reach = l03["jwst_reach_summary"]  # {"q0":"50","q2":"50"}
    sn_reach = min(float(reach["q0"]), float(reach["q2"]))
    if minimal is None:
        verdict, ok = "NO CONFIGURATION REACHES P>=0.95 on the loaded grid — program needs a larger grid; honest gap recorded", False
        margin = None
    else:
        sn_req = minimal["SN"]
        margin = sn_reach / sn_req
        ok = sn_req <= sn_reach
        verdict = ("FEASIBLE-JWST: minimal registered config N=%d, per-object S/N=%d (rate %.4f, f=%d); "
                   "margin vs L03 pair reach S/N=%.0f is %.2fx" % (minimal["N"], sn_req, minimal["rate"], minimal["f"], sn_reach, margin)
                   if ok else
                   "INFEASIBLE-JWST: minimal registered config needs per-object S/N=%d > L03 pair reach %.0f (pre-registered kill fired)" % (sn_req, sn_reach))
    tests = k11["tests"]
    md = ["# OB1 — JWST observation design (L05/K09 door)",
          "",
          "**Spawned** by the conductor tick 2026-09-26 (Z-wave). House rules: LOOP_CONDUCTOR.md 1-10.",
          "**Program verdict:** " + verdict,
          "",
          "## 1. Minimal registered configurations (from L05 power grid, loaded, rate >= 0.95)",
          "",
          "| f | N | per-object S/N | rate |", "|---|---|---|---|"]
    for r in feas[:12]:
        md.append("| %d | %d | %d | %.4f |" % (r["f"], r["N"], r["SN"], r["rate"]))
    md += ["",
           "## 2. Reach fold-in (L03, loaded)",
           "",
           "L03 jwst_reach_summary: pair reach S/N = %s (q0), %s (q2) -> SN_reach = %.0f." % (
               reach["q0"], reach["q2"], sn_reach),
           "Margin of the minimal registered config vs reach: %s." % (("%.2fx" % margin) if margin else "n/a"),
           "",
           "## 3. Falsifier schedule (K11 consolidated tests, verbatim)",
           ""]
    for t in tests:
        md.append("- " + t)
    md += ["",
           "## 4. Kill condition (pre-registered in Z-WAVE_BRIEF.md)",
           "",
           "Per-object S/N > 50 (L03 pair reach) at the minimal registered config -> INFEASIBLE-JWST.",
           "This lane exits 0 only on a real pass; otherwise exit 1 with the honest verdict.",
           ""]
    open(OUT_MD, "w").write("\n".join(md))
    out = {"title": "OB1 JWST observation design", "minimal_config": minimal,
           "n_feasible_configs": len(feas), "sn_reach": sn_reach, "margin": margin,
           "feasible": ok, "verdict": verdict,
           "k11_tests_included": len(tests)}
    json.dump(out, open(OUT_JS, "w"), indent=1)
    print(verdict)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""CFG487 growth leg (FROZEN_CRITERIA.md 3(c)): 256^3 runs of the CFG424 engine copy with the settled-fraction switch,
scored against CFG359's S0 with CFG361's cuts (GROWTH OK: |sigma8 ratio - 1| <= 0.05 and max_{k<=1}|P ratio - 1| <= 0.10;
FAIL: sigma8 shift > 0.20; else TENSION).  Controls: C1 (T1REPRO reproduces CFG424 TA-can within 1e-3), C6 (the clock
never decreases, m in [0, 1]).  MUTATE-A (FRW-firing switch, canonical) must NOT be GROWTH OK, else the growth leg is NOT
DIAGNOSTIC.  Reported: SA runs (switch alone) and the POST-HOC CATCH runs (switch x turnaround catchment, no edge balls).
CFG487_MUTATE=1 writes *_MUTATE.* with the mutation runs only and exits 1 when MUTATE-A is detected (not GROWTH OK).
Run: python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_growth_analysis.py
"""
import os, sys, json, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(E, "cfg487_work")
MUTATE = os.environ.get("CFG487_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
S0 = os.path.join(E, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json")
L, OUT = [], {"lane": "CFG487", "script": "cfg487_growth_analysis", "mutate": MUTATE}


def P(s=""):
    print(s, flush=True); L.append(s)


def rat(p, p0):
    d = json.load(open(p)); s, s0 = d["snap"]["z0"], json.load(open(p0))["snap"]["z0"]
    k, Pk = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = Pk[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    r = dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)],
             overdraw=s.get("overdraw_mass"), q_max=s.get("q_max"), e_mean=s.get("e_mean"), runtime_s=d.get("runtime_s"))
    r["clk"] = {kk: v for kk, v in s.items() if kk.startswith("clk_")}
    c = d.get("cfg487", {})
    r["min_dm"] = c.get("min_dm"); r["m_range"] = c.get("m_range"); r["latched_final"] = c.get("latched_final")
    return r


cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
RUNS = {"T1REPRO (C1)": ("T1REPRO", "EDGE", "canonical"),
        "V1 canonical": ("V1", "EDGE", "canonical"), "V1 alt": ("V1", "EDGE", "alt"),
        "V2 canonical": ("V2", "EDGE", "canonical"), "V2 alt": ("V2", "EDGE", "alt"),
        "MUTATE-A (FRW-firing, edge)": ("MUTA", "EDGE", "canonical"),
        "V1-SA (reported)": ("V1", "SA", "canonical"), "MUTATE-B-SA (reported)": ("MUTA", "SA", "canonical"),
        "POST-HOC V1-CATCH canonical": ("V1", "CATCH", "canonical"), "POST-HOC V1-CATCH alt": ("V1", "CATCH", "alt"),
        "POST-HOC MUTA-CATCH canonical": ("MUTA", "CATCH", "canonical")}
if MUTATE:
    RUNS = {k: v for k, v in RUNS.items() if "MUTA" in k}
R = {}
for name, (sw, conf, foot) in RUNS.items():
    p = os.path.join(W, f"cfg487_{sw}_{conf}_RES_TA_MIXA_FLAT_{foot}_N256.json")
    if not os.path.exists(p):
        R[name] = None; P(f"  {name:32s}: PENDING"); continue
    r = rat(p, S0); r["verdict"] = cat(r); R[name] = r
    ck = r["clk"]
    P(f"  {name:32s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f}  P@0.1/0.3/1 {r['P'][0]:.3f}/{r['P'][1]:.3f}/{r['P'][2]:.3f} -> {r['verdict']}"
      + (f"  | overdraw {r['overdraw']:.4f} q_max {r['q_max']:.3f}" if r["overdraw"] is not None else ""))
    if ck:
        P(f"      clock z0: latched mass {ck.get('clk_latched_mass', float('nan')):.3f} (voids {ck.get('clk_latched_mass_voids_dlt_m05', float('nan')):.4f}; "
          f"knot {ck.get('clk_latched_knot', float('nan')):.3f} fil {ck.get('clk_latched_fil', float('nan')):.3f} sheet {ck.get('clk_latched_sheet', float('nan')):.3f} "
          f"void-web {ck.get('clk_latched_void_web', float('nan')):.4f}); <m> mass {ck.get('clk_m_mass', float('nan')):.3f} (voids {ck.get('clk_m_mass_voids_dlt_m05', float('nan')):.4f}); "
          f"SW in edge cells {ck.get('clk_SW_edge_mass', float('nan')):.3f} vs T1 {ck.get('clk_T1_edge_mass', float('nan')):.3f} ({ck.get('clk_edge_cells', 0)} cells); "
          f"vol SW>0.5 {ck.get('clk_vol_SW_on', float('nan')):.4f} vs T1>0.5 {ck.get('clk_vol_T1_on', float('nan')):.4f}, overlap {ck.get('clk_overlap_SW_T1', float('nan')):.3f}; "
          f"min dm {r['min_dm']}; m range {r['m_range']}")
OUT["runs"] = R
CH = {}


def check(name, ok, msg, lb=True):
    CH[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P("")
if not MUTATE:
    ref = json.load(open(os.path.join(HERE, "..", "CFG424_turnaround_catchment", "cfg424_results.json")))["TA-can"]
    t = R["T1REPRO (C1)"]
    if t:
        d1, d2 = abs(t["s8"] - ref["s8"]), abs(t["pdev"] - ref["pdev"])
        check("C1 engine reproduction: T1REPRO reproduces CFG424 TA-can (s8 ratio, max|P-1|) within 1e-3", d1 <= 1e-3 and d2 <= 1e-3,
              f"s8 {t['s8']:.6f} vs {ref['s8']:.6f} (|d| {d1:.1e}); pdev {t['pdev']:.6f} vs {ref['pdev']:.6f} (|d| {d2:.1e})")
    clk = [r for n, r in R.items() if r and r.get("m_range") is not None]
    if clk:
        c6 = all(r["min_dm"] == 0.0 and 0.0 <= r["m_range"][0] and r["m_range"][1] <= 1.0 for r in clk)
        check("C6 PM clock: m in [0, 1] and never decreases along any particle (max drop exactly 0)", c6,
              ", ".join(f"{n.split(' (')[0]}: min dm {r['min_dm']}, m [{r['m_range'][0]:.3g}, {r['m_range'][1]:.6f}]" for n, r in R.items() if r and r.get("m_range") is not None))
mu = R.get("MUTATE-A (FRW-firing, edge)")
det = None if mu is None else (mu["verdict"] != "GROWTH OK")
OUT["mutateA_detected"] = det
if mu is not None:
    check("MUTATE-A (FRW-firing switch) is NOT GROWTH OK (else the growth leg is NOT DIAGNOSTIC)", det,
          f"{mu['verdict']} (s8 {mu['s8']:.4f}, pdev {mu['pdev']:.4f})", lb=False)
if not MUTATE:
    G = {}
    for v in ("V1", "V2"):
        a, b = R.get(f"{v} canonical"), R.get(f"{v} alt")
        if a is None or b is None:
            G[v] = "PENDING"
        else:
            ok = a["verdict"] == "GROWTH OK" and b["verdict"] == "GROWTH OK"
            G[v] = ("GROWTH OK" + ("" if det else " (NOT DIAGNOSTIC: MUTATE-A also GROWTH OK)" if det is not None else " (MUTATE-A pending)")) if ok else \
                f"{a['verdict']} / {b['verdict']}"
        P(f"  growth leg {v}: {G[v]}")
    OUT["growth_leg"] = G
    try:
        # the brief's BRE form "N512\|512 0 MIXA\|..." errors silently on macOS pgrep (extended regex): use the ERE alternation
        busy = subprocess.run(["pgrep", "-f", r"N512|512 0 MIXA|cfg4[0-9][0-9]_pm.py .* 512"], capture_output=True, text=True).stdout.strip()
    except Exception as e:
        busy = f"pgrep failed: {e}"
    OUT["other_512_running_at_analysis"] = bool(busy)
    P(f"  512^3 rule (iii): another 512^3 job running now: {bool(busy)}")
    sa, mb = R.get("V1-SA (reported)"), R.get("MUTATE-B-SA (reported)")
    if sa and mb:
        P(f"  SA (reported): V1-SA {sa['verdict']} vs MUTATE-B-SA {mb['verdict']} -> the switch alone "
          + ("confines the excess (and its FRW-offness matters)" if sa["verdict"] == "GROWTH OK" and mb["verdict"] != "GROWTH OK" else "does not settle growth by itself in this configuration"))
    ca, cb, cm = R.get("POST-HOC V1-CATCH canonical"), R.get("POST-HOC V1-CATCH alt"), R.get("POST-HOC MUTA-CATCH canonical")
    if ca and cm:
        P(f"  POST-HOC CATCH: V1 {ca['verdict']}" + (f" / {cb['verdict']}" if cb else "") + f" vs MUTA {cm['verdict']}")
OUT["checks"] = CH
json.dump(OUT, open(os.path.join(HERE, f"cfg487_growth_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg487_growth{SUF}.out"), "w").write("\n".join(L) + "\n")
nlb = sum(1 for c in CH.values() if c["load_bearing"] and not c["ok"])
if MUTATE:
    sys.exit(1 if det else 0)
sys.exit(1 if nlb else 0)

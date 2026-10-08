#!/usr/bin/env python3
"""CFG498 growth leg (FROZEN_CRITERIA.md d9c739010, section 2(a)): 256^3 runs of the CFG487 engine copy in mode CAP (clock taper
x turnaround catchment, no edge, CFG424 per-catchment compensation, draw capped by the catchment's cold energy), scored against
CFG359's S0 with CFG361's cuts (GROWTH OK: |sigma8 ratio - 1| <= 0.05 and max_{k<=1}|P ratio - 1| <= 0.10; FAIL: sigma8 shift > 0.20;
else TENSION).  MUTATE-N (no compensation, no cap) must NOT be GROWTH OK, else the growth leg is NOT DIAGNOSTIC.
Controls: C1 (MUTATE-U, cap removed, reproduces CFG487 POST-HOC V1-CATCH canonical within 1e-3), C3 (|sum src|/sum|e| <= 1e-3 and
comp <= s_c at every diagnostic snapshot of the CAP runs), C5 (m in [0, 1], never decreasing).
CFG498_MUTATE=1 writes *_MUTATE.* with the mutation runs only and exits 1 when MUTATE-N is detected (not GROWTH OK).
Run: python3 campaign_fresh_gravity/CFG498_clock_taper_capped/cfg498_growth_analysis.py
"""
import os, sys, json, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(E, "cfg498_work")
MUTATE = os.environ.get("CFG498_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
S0 = os.path.join(E, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json")
L, OUT = [], {"lane": "CFG498", "script": "cfg498_growth_analysis", "mutate": MUTATE}


def P(s=""):
    print(s, flush=True); L.append(s)


def rat(p, p0):
    d = json.load(open(p)); s, s0 = d["snap"]["z0"], json.load(open(p0))["snap"]["z0"]
    k, Pk = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = Pk[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    r = dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)],
             runtime_s=d.get("runtime_s"))
    r["snapdiag"] = {nm: {kk: sn.get(kk) for kk in ("overdraw_mass", "q_max", "q_raw_max", "cap_bind_mass", "src_sum", "e_sum", "e_mean",
                                                    "min_sc_minus_comp_rel", "n_catch")} for nm, sn in d["snap"].items()}
    r["clk"] = {kk: v for kk, v in s.items() if kk.startswith("clk_")}
    c = d.get("cfg487", {})
    r["min_dm"] = c.get("min_dm"); r["m_range"] = c.get("m_range"); r["latched_final"] = c.get("latched_final")
    return r


cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
RUNS = {"V1-CAP canonical": "V1_CAP_RES_TA_MIXA_FLAT_canonical", "V1-CAP alt": "V1_CAP_RES_TA_MIXA_FLAT_alt",
        "V2-CAP canonical": "V2_CAP_RES_TA_MIXA_FLAT_canonical", "V2-CAP alt": "V2_CAP_RES_TA_MIXA_FLAT_alt",
        "MUTATE-N (no comp, no cap)": "V1_CAP_NOCOMP_RES_TA_MIXA_FLAT_canonical",
        "MUTATE-U (cap removed; C1)": "V1_CAP_CAPOFF_RES_TA_MIXA_FLAT_canonical",
        "MUTA-CAP (FRW-firing, reported)": "MUTA_CAP_RES_TA_MIXA_FLAT_canonical"}
if MUTATE:
    RUNS = {k: v for k, v in RUNS.items() if k.startswith("MUTA")}
R = {}
for name, tag in RUNS.items():
    p = os.path.join(W, f"cfg498_{tag}_N256.json")
    if not os.path.exists(p):
        R[name] = None; P(f"  {name:32s}: PENDING"); continue
    r = rat(p, S0); r["verdict"] = cat(r); R[name] = r
    z0 = r["snapdiag"]["z0"]
    P(f"  {name:32s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f}  P@0.1/0.3/1 {r['P'][0]:.3f}/{r['P'][1]:.3f}/{r['P'][2]:.3f} -> {r['verdict']}"
      f"  ({r['runtime_s']:.0f} s)")
    if z0.get("q_max") is not None:
        P(f"      z0: q_raw max {z0.get('q_raw_max')}, q_max (after cap) {z0['q_max']:.3f}, cap binds on {z0.get('cap_bind_mass')} of catchment mass, "
          f"overdraw {z0['overdraw_mass']:.4f}, sum src {z0['src_sum']:.3g} vs sum|e| {z0.get('e_sum')}, min (s_c - comp)/s_c {z0.get('min_sc_minus_comp_rel')}, "
          f"catchments {z0.get('n_catch')}")
    ck = r["clk"]
    if ck:
        P(f"      clock z0: latched mass {ck.get('clk_latched_mass', float('nan')):.3f} (voids {ck.get('clk_latched_mass_voids_dlt_m05', float('nan')):.4f}); "
          f"<m> mass {ck.get('clk_m_mass', float('nan')):.3f}; min dm {r['min_dm']}; m range {r['m_range']}")
OUT["runs"] = R
CH = {}


def check(name, ok, msg, lb=True):
    CH[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P("")
if not MUTATE:
    ref = json.load(open(os.path.join(HERE, "..", "CFG487_settled_fraction_switch", "cfg487_growth_results.json")))["runs"]["POST-HOC V1-CATCH canonical"]
    t = R["MUTATE-U (cap removed; C1)"]
    if t:
        d1, d2 = abs(t["s8"] - ref["s8"]), abs(t["pdev"] - ref["pdev"])
        check("C1 MUTATE-U (cap removed) reproduces CFG487 POST-HOC V1-CATCH canonical (s8 ratio, max|P-1|) within 1e-3", d1 <= 1e-3 and d2 <= 1e-3,
              f"s8 {t['s8']:.6f} vs {ref['s8']:.6f} (|d| {d1:.1e}); pdev {t['pdev']:.6f} vs {ref['pdev']:.6f} (|d| {d2:.1e})")
    caps = {n: r for n, r in R.items() if r and "CAP" in n and "MUTATE" not in n}
    if caps:
        worst_s, worst_c = 0.0, 1.0
        for n, r in caps.items():
            for sn, dg in r["snapdiag"].items():
                if dg.get("e_sum"):
                    worst_s = max(worst_s, abs(dg["src_sum"]) / dg["e_sum"])
                if dg.get("min_sc_minus_comp_rel") is not None:
                    worst_c = min(worst_c, dg["min_sc_minus_comp_rel"])
        check("C3 capped mass conservation: |sum src| / sum|e| <= 1e-3 and (s_c - comp)/s_c >= -1e-6 at every snapshot of every CAP run",
              worst_s <= 1e-3 and worst_c >= -1e-6, f"worst |sum src|/sum|e| {worst_s:.2e}; min (s_c - comp)/s_c {worst_c:.3e}")
    clk = [r for n, r in R.items() if r and r.get("m_range") is not None]
    if clk:
        c5 = all(r["min_dm"] == 0.0 and 0.0 <= r["m_range"][0] and r["m_range"][1] <= 1.0 for r in clk)
        check("C5 PM clock: m in [0, 1] and never decreases along any particle", c5,
              ", ".join(f"{n.split(' (')[0]}: min dm {r['min_dm']}" for n, r in R.items() if r and r.get("m_range") is not None))
mu = R.get("MUTATE-N (no comp, no cap)")
det = None if mu is None else (mu["verdict"] != "GROWTH OK")
OUT["mutateN_detected"] = det
if mu is not None:
    check("MUTATE-N (no compensation, no cap) is NOT GROWTH OK (else the growth leg is NOT DIAGNOSTIC)", det,
          f"{mu['verdict']} (s8 {mu['s8']:.4f}, pdev {mu['pdev']:.4f})", lb=False)
if not MUTATE:
    G = {}
    for v in ("V1", "V2"):
        a, b = R.get(f"{v}-CAP canonical"), R.get(f"{v}-CAP alt")
        if a is None or b is None:
            G[v] = "PENDING"
        else:
            ok = a["verdict"] == "GROWTH OK" and b["verdict"] == "GROWTH OK"
            G[v] = ("GROWTH PASS" if det else "GROWTH OK BOTH, NOT DIAGNOSTIC (MUTATE-N also GROWTH OK)" if det is not None else "GROWTH OK (MUTATE-N pending)") \
                if ok else f"NOT PASSED: {a['verdict']} / {b['verdict']}"
        P(f"  growth leg {v}: {G[v]}")
    OUT["growth_leg"] = G
    busy = subprocess.run(["pgrep", "-f", r"N512|512 0 MIXA|cfg4[0-9][0-9]_pm.py .* 512"], capture_output=True, text=True).stdout.strip()
    OUT["other_512_running_at_analysis"] = bool(busy)
    P(f"  512^3 rule (iii): another 512^3 job running now: {bool(busy)}")
OUT["checks"] = CH
json.dump(OUT, open(os.path.join(HERE, f"cfg498_growth_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg498_growth{SUF}.out"), "w").write("\n".join(L) + "\n")
nlb = sum(1 for c in CH.values() if c["load_bearing"] and not c["ok"])
if MUTATE:
    sys.exit(1 if det else 0)
sys.exit(1 if nlb else 0)

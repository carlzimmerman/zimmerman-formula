#!/usr/bin/env python3
"""CFG501 growth leg (FROZEN_CRITERIA.md 7b71dd9b5, section 2(a)): 256^3 runs of cfg501_pm.py (CFG498's engine with the CAP draw
taken from the UNSETTLED cold energy, w_c = (1 - m) s_c), scored against CFG359's S0 with CFG361's cuts (GROWTH OK:
|sigma8 ratio - 1| <= 0.05 and max_{k<=1}|P ratio - 1| <= 0.10; FAIL: sigma8 shift > 0.20; else TENSION).
MUTATE-N (no compensation, no cap) must NOT be GROWTH OK, else the growth leg is NOT DIAGNOSTIC.
Controls: C1 (PROP = CFG498's weight reproduces CFG498's V1-CAP canonical bit for bit: sigma8 and the z = 0 P(k) array identical),
C1b (MUTATE-N reproduces CFG498's MUTATE-N bit for bit; reported), C3 (|sum src|/sum|e| <= 1e-3; comp <= (1 - m) s_c), C5 (clock).
CFG501_MUTATE=1 writes *_MUTATE.* with the MUTATE-N run only and exits 1 when MUTATE-N is detected (not GROWTH OK).
Run: python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_growth_analysis.py
"""
import os, sys, json, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W, W498 = os.path.join(E, "cfg501_work"), os.path.join(E, "cfg498_work")
MUTATE = os.environ.get("CFG501_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
S0 = os.path.join(E, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json")
L, OUT = [], {"lane": "CFG501", "script": "cfg501_growth_analysis", "mutate": MUTATE}


def P(s=""):
    print(s, flush=True); L.append(s)


DK = ("overdraw_mass", "q_max", "q_raw_max", "cap_bind_mass", "src_sum", "e_sum", "e_mean", "min_sc_minus_comp_rel",
      "min_wc_minus_comp_rel_sc", "unsettled_frac_catch", "n_catch", "mass_on_phantom_dom")


def rat(p, p0):
    d = json.load(open(p)); s, s0 = d["snap"]["z0"], json.load(open(p0))["snap"]["z0"]
    k, Pk = np.array(s["k"]), np.array(s["P"]); m = k <= 1
    pr = Pk[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
    r = dict(s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr - 1))), P=[float(np.interp(x, k[m], pr)) for x in (0.1, 0.3, 1.0)],
             runtime_s=d.get("runtime_s"), sigma8_abs=s["sigma8"])
    r["snapdiag"] = {nm: {kk: sn.get(kk) for kk in DK} for nm, sn in d["snap"].items()}
    r["clk"] = {kk: v for kk, v in s.items() if kk.startswith("clk_")}
    c = d.get("cfg487", {})
    r["min_dm"] = c.get("min_dm"); r["m_range"] = c.get("m_range"); r["latched_final"] = c.get("latched_final")
    return r


cat = lambda r: "FAIL" if abs(r["s8"] - 1) > 0.2 else ("GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION")
RUNS = {"V1-U canonical": "V1_CAP_U_RES_TA_MIXA_FLAT_canonical", "V1-U alt": "V1_CAP_U_RES_TA_MIXA_FLAT_alt",
        "V2-U canonical": "V2_CAP_U_RES_TA_MIXA_FLAT_canonical", "V2-U alt": "V2_CAP_U_RES_TA_MIXA_FLAT_alt",
        "MUTATE-N (no comp, no cap)": "V1_CAP_U_NOCOMP_RES_TA_MIXA_FLAT_canonical",
        "C1 PROP (CFG498 weight)": "V1_CAP_PROP_RES_TA_MIXA_FLAT_canonical"}
if MUTATE:
    RUNS = {k: v for k, v in RUNS.items() if k.startswith("MUTATE")}
R = {}
for name, tag in RUNS.items():
    p = os.path.join(W, f"cfg501_{tag}_N256.json")
    if not os.path.exists(p):
        R[name] = None; P(f"  {name:28s}: PENDING"); continue
    r = rat(p, S0); r["verdict"] = cat(r); R[name] = r
    z0 = r["snapdiag"]["z0"]
    P(f"  {name:28s}: s8 {r['s8']:.4f}  max|P-1| {r['pdev']:.4f}  P@0.1/0.3/1 {r['P'][0]:.3f}/{r['P'][1]:.3f}/{r['P'][2]:.3f} -> {r['verdict']}"
      f"  ({r['runtime_s']:.0f} s)")
    if z0.get("q_max") is not None:
        P(f"      z0: q_raw max {z0.get('q_raw_max'):.3f}, cap binds on {z0.get('cap_bind_mass'):.3f} of catchment mass, unsettled share of catchment "
          f"cold {z0.get('unsettled_frac_catch')}, sum src {z0['src_sum']:.3g} vs sum|e| {z0.get('e_sum'):.4g}, min (w_c - comp)/s_c "
          f"{z0.get('min_wc_minus_comp_rel_sc')}, catchments {z0.get('n_catch')}")
    else:
        P(f"      z0: sum src = sum e {z0.get('src_sum')}, e_mean {z0.get('e_mean')}")
    ck = r["clk"]
    if ck:
        P(f"      clock z0: latched mass {ck.get('clk_latched_mass', float('nan')):.3f}; <m> mass {ck.get('clk_m_mass', float('nan')):.3f}; "
          f"min dm {r['min_dm']}; m range {r['m_range']}")
OUT["runs"] = R
CH = {}


def check(name, ok, msg, lb=True):
    CH[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


def bitcmp(p_new, p_old):
    a, b = json.load(open(p_new))["snap"], json.load(open(p_old))["snap"]
    ds8 = max(abs(a[n]["sigma8"] - b[n]["sigma8"]) for n in b)
    dP = max(float(np.max(np.abs(np.array(a[n]["P"]) - np.array(b[n]["P"])))) for n in b)
    return ds8, dP


P("")
if not MUTATE:
    pn = os.path.join(W, "cfg501_V1_CAP_PROP_RES_TA_MIXA_FLAT_canonical_N256.json")
    if os.path.exists(pn):
        ds8, dP = bitcmp(pn, os.path.join(W498, "cfg498_V1_CAP_RES_TA_MIXA_FLAT_canonical_N256.json"))
        check("C1 PROP run reproduces CFG498 V1-CAP canonical bit for bit (sigma8 and P(k) at every snapshot)", ds8 == 0.0 and dP == 0.0,
              f"max |d sigma8| {ds8:.3e}, max |dP| {dP:.3e}")
    pm = os.path.join(W, "cfg501_V1_CAP_U_NOCOMP_RES_TA_MIXA_FLAT_canonical_N256.json")
    if os.path.exists(pm):
        ds8, dP = bitcmp(pm, os.path.join(W498, "cfg498_V1_CAP_NOCOMP_RES_TA_MIXA_FLAT_canonical_N256.json"))
        check("C1b MUTATE-N reproduces CFG498 MUTATE-N bit for bit", ds8 == 0.0 and dP == 0.0, f"max |d sigma8| {ds8:.3e}, max |dP| {dP:.3e}", lb=False)
    us = {n: r for n, r in R.items() if r and "-U " in n}
    if us:
        worst_s, worst_c = 0.0, 1.0
        for n, r in us.items():
            for sn, dg in r["snapdiag"].items():
                if dg.get("e_sum"):
                    worst_s = max(worst_s, abs(dg["src_sum"]) / dg["e_sum"])
                if dg.get("min_wc_minus_comp_rel_sc") is not None:
                    worst_c = min(worst_c, dg["min_wc_minus_comp_rel_sc"])
        check("C3 mass conservation: |sum src| / sum|e| <= 1e-3 and ((1 - m) s_c - comp)/s_c >= -1e-6 at every snapshot of every U run",
              worst_s <= 1e-3 and worst_c >= -1e-6, f"worst |sum src|/sum|e| {worst_s:.2e}; min ((1-m) s_c - comp)/s_c {worst_c:.3e}")
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
        a, b = R.get(f"{v}-U canonical"), R.get(f"{v}-U alt")
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
    P(f"  512^3 rule: another 512^3 job running now: {bool(busy)}")
OUT["checks"] = CH
json.dump(OUT, open(os.path.join(HERE, f"cfg501_growth_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg501_growth{SUF}.out"), "w").write("\n".join(L) + "\n")
nlb = sum(1 for c in CH.values() if c["load_bearing"] and not c["ok"])
if MUTATE:
    sys.exit(1 if det else 0)
sys.exit(1 if nlb else 0)

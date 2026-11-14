"""AGB7 collector: harness checks and the labels of FROZEN_CRITERIA.md (AGB1 Part B's rules) applied to the outputs
of agb7_reread.py. Writes agb7_results.json; prints the tables (redirect to agb7_collect.out). It fits nothing."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
LGS1 = os.path.join(REPO, "closure_2026_11_13", "LGS1_legacy_sn_dropped"); AGB1 = os.path.join(REPO, "closure_2026_11_13", "AGB1_progenitor_age_bias")
C684 = os.path.join(REPO, "campaign_fresh_gravity", "CFG684_bao_cc_sn_robust", "cfg684_results.json")
ZS684 = ["1.0", "1.5", "2.33"]; ZS689 = ["1.0", "1.2", "1.5", "2.33"]; COMBOS = ("BAO+DES5", "BAO+DES5+CC")


def load(name, folder=HERE):
    p = os.path.join(folder, name)
    return json.load(open(p)) if os.path.exists(p) else None


def flat684(o):
    v = [o["dchi2_max"], o["flat_a0_om"]["mean"], o["flat_a0_om"]["sd"]]
    for z in ZS684: v += o[z]["rival"] + o[z]["tracking"]
    return np.array(v, float)


out = dict(lane="AGB7"); pf = lambda b: "PASS" if b else "FAIL"
h0, h1, a1 = load("agb7_cfg684_full_S000.json"), load("agb7_cfg684_full_S100.json"), load("agb1_cfg684_full_A1.json", AGB1); ref = json.load(open(C684))
d1 = max(float(np.max(np.abs(flat684(h0[c]) - flat684(ref[c])))) for c in COMBOS) if h0 else None
d2 = max(float(np.max(np.abs(flat684(h1[c]) - flat684(a1[c])))) for c in COMBOS) if h1 else None
H1 = d1 is not None and d1 <= 1e-6; H2 = d2 is not None and d2 <= 1e-9
k1, k0 = load("agb7_cfg689_TD5F_des_only_S100.json"), load("agb1_cfg689_TD5F_des_only_A1.json", AGB1)
d3 = max(float(np.max(np.abs(np.array(k1["BAO+SN"]["P1"][z]["sqrtX_q"]) - np.array(k0["BAO+SN"]["P1"][z]["sqrtX_q"])))) for z in ZS689) if k1 else None
H3 = d3 is not None and d3 <= 0.005
print("AGB7 harness checks")
print(f"  H1 cfg684 full at A = 0 against the committed cfg684_results.json: max |diff| {d1 if d1 is None else format(d1, '.2e')} (<= 1e-6) -> {pf(H1) if d1 is not None else 'NOT RUN'}")
print(f"  H2 cfg684 full at A = 1 against AGB1's committed run: max |diff| {d2 if d2 is None else format(d2, '.2e')} (<= 1e-9) -> {pf(H2) if d2 is not None else 'NOT RUN'}")
print(f"  H3 cfg689 TD5F des_only at A = 1 against AGB1's committed run: max |diff| in the tracking quantiles {d3 if d3 is None else format(d3, '.4f')} (<= 0.005) -> {pf(H3) if d3 is not None else 'NOT RUN'}")
out["checks"] = dict(H1=H1, H2=H2, H3=H3, d1=d1, d2=d2, d3=d3)
AMPS = (("S023", "A = 0.23, cosmic-average template (PRIMARY)"), ("S035", "A = 0.35, cosmic-average template (bracket)"))


def g684(tag, s):
    a0 = load(f"lgs1_cfg684_{s}.json", LGS1); a = load(f"agb7_cfg684_{s}_{tag}.json"); af = load(f"agb1_cfg684_{s}_A1.json", AGB1)
    if a is None: return None
    r = {}
    for c in COMBOS:
        p, q = a0[c], a[c]; shift = q["flat_a0_om"]["mean"] - p["flat_a0_om"]["mean"]; comb = float(np.hypot(p["flat_a0_om"]["sd"], q["flat_a0_om"]["sd"]))
        full_shift = af[c]["flat_a0_om"]["mean"] - p["flat_a0_om"]["mean"] if af else None
        r[c] = dict(om_A0=p["flat_a0_om"]["mean"], sd_A0=p["flat_a0_om"]["sd"], om=q["flat_a0_om"]["mean"], sd=q["flat_a0_om"]["sd"], shift=shift, combined_sd=comb,
                    share_of_A1_shift=(shift/full_shift if full_shift else None), dchi2_max_A0=p["dchi2_max"], dchi2_max=q["dchi2_max"],
                    A1="DEGENERACY BROKEN" if q["dchi2_max"] >= 4 else "NOT BROKEN", A2="ROBUST" if abs(shift) <= comb else "AGE-DEPENDENT",
                    A3="FLOOR HOLDS" if q["2.33"]["tracking"][0] > 0 else "FLOOR LOST", tracking_A0={z: p[z]["tracking"] for z in ZS684}, tracking={z: q[z]["tracking"] for z in ZS684})
        if not (H1 and H2): r[c].update(A1="NOT EVALUABLE", A2="NOT EVALUABLE", A3="NOT EVALUABLE")
    return r


def g689(tag, mode, s):
    a0 = load(f"lgs1_cfg689_{mode}_{s}.json", LGS1); a = load(f"agb7_cfg689_{mode}_{s}_{tag}.json"); af = load(f"agb1_cfg689_{mode}_{s}_A1.json", AGB1)
    if a is None: return None
    p, q = a0["BAO+SN"], a["BAO+SN"]; ev = H3 and q["K4"]["ok"] and a["nstep"] == 60000; m = dict(nstep=a["nstep"], K4_ok=q["K4"]["ok"], z={})
    for z in ZS689:
        qa, qb = np.array(p["P1"][z]["sqrtX_q"]), np.array(q["P1"][z]["sqrtX_q"]); stable = (qa[1] <= qb[2] <= qa[3]) and (qb[1] <= qa[2] <= qb[3])
        fs = (np.array(af["BAO+SN"]["P1"][z]["sqrtX_q"])[2] - qa[2]) if af else None
        m["z"][z] = dict(A0_68=[qa[1], qa[3]], A0_median=qa[2], run_68=[qb[1], qb[3]], run_median=qb[2], share_of_A1_shift=((qb[2] - qa[2])/fs if fs else None),
                         B1=("STABLE" if stable else "SHIFTED") if ev else "NOT EVALUABLE")
    cls0 = (p["P1_class"], (p["P0"] or {}).get("P0_class")); cls1 = (q["P1_class"], (q["P0"] or {}).get("P0_class"))
    m.update(P1_class=[cls0[0], cls1[0]], P0_class=[cls0[1], cls1[1]], B2=("CLASS UNCHANGED" if cls0 == cls1 else "CLASS CHANGED") if ev else "NOT EVALUABLE",
             P2=dict(A0=[p["P2"]["dchi2"], p["P2"]["sigma_equiv"], p["P2"].get("P2_class")], run=[q["P2"]["dchi2"], q["P2"]["sigma_equiv"], q["P2"].get("P2_class")]),
             H0=[p["P3"]["H0_q"][2], q["P3"]["H0_q"][2]])
    return m


R = {t: dict(cfg684={s: g684(t, s) for s in ("full", "des_only")}, cfg689={m: {s: g689(t, m, s) for s in ("full", "des_only")} for m in ("D5", "TD5F")}) for t, _ in AMPS}
for t, title in AMPS:
    print(f"\n{title}")
    for s in ("full", "des_only"):
        r = R[t]["cfg684"][s]
        if r is None: print(f"  CFG684 {s}: NOT RUN"); continue
        for c in COMBOS:
            x = r[c]; print(f"  CFG684 {s:8s} {c:12s}: flat-a0 Om {x['om_A0']:.4f} +- {x['sd_A0']:.4f} -> {x['om']:.4f} +- {x['sd']:.4f} (shift {x['shift']:+.4f}, combined sd {x['combined_sd']:.4f},"
                         f" {x['share_of_A1_shift']:.2f} of the A = 1 shift) -> A2 {x['A2']};  dchi2_max {x['dchi2_max_A0']:.2f} -> {x['dchi2_max']:.2f} A1 {x['A1']};"
                         f"  sqrtX(2.33) {x['tracking_A0']['2.33'][0]:.3f}-{x['tracking_A0']['2.33'][1]:.3f} -> {x['tracking']['2.33'][0]:.3f}-{x['tracking']['2.33'][1]:.3f} A3 {x['A3']}")
    for m in ("D5", "TD5F"):
        for s in ("full", "des_only"):
            x = R[t]["cfg689"][m][s]
            if x is None: print(f"  CFG689 {m} {s}: NOT RUN"); continue
            for z in ZS689:
                v = x["z"][z]; print(f"  CFG689 {m:4s} {s:8s} z*={z}: tracking sqrtX 68% [{v['A0_68'][0]:.3f}, {v['A0_68'][1]:.3f}] med {v['A0_median']:.3f} -> [{v['run_68'][0]:.3f}, {v['run_68'][1]:.3f}] med {v['run_median']:.3f}"
                                     f" -> B1 {v['B1']}" + (f"  ({v['share_of_A1_shift']:.2f} of the A = 1 shift)" if v["share_of_A1_shift"] is not None else ""))
            print(f"  CFG689 {m:4s} {s:8s}: B2 {x['B2']} (P1 {x['P1_class'][0]} -> {x['P1_class'][1]}; P0 {x['P0_class'][0]} -> {x['P0_class'][1]});  P2 {x['P2']['A0'][0]:.2f} ({x['P2']['A0'][1]:.2f} sigma, {x['P2']['A0'][2]})"
                  f" -> {x['P2']['run'][0]:.2f} ({x['P2']['run'][1]:.2f} sigma, {x['P2']['run'][2]});  native H0 {x['H0'][0]:.2f} -> {x['H0'][1]:.2f};  chain check ok {x['K4_ok']}")
print("\nLabels (first word at A = 0.23; second word ROBUST if A = 0.35 gives the same)")
lab = {}
def two(a, b): return f"{a} / {'ROBUST' if a == b else 'FRAGILE (0.35: ' + str(b) + ')'}" if b is not None else f"{a} / (bracket NOT RUN)"
for s in ("full", "des_only"):
    p, b = R["S023"]["cfg684"][s], R["S035"]["cfg684"][s]
    if p is None: continue
    for c in COMBOS:
        for k in ("A1", "A2", "A3"):
            lab[f"cfg684 {s} {c} {k}"] = two(p[c][k], b[c][k] if b else None); print(f"  CFG684 {s:8s} {c:12s} {k}: {lab[f'cfg684 {s} {c} {k}']}")
for m in ("D5", "TD5F"):
    for s in ("full", "des_only"):
        p, b = R["S023"]["cfg689"][m][s], R["S035"]["cfg689"][m][s]
        if p is None: continue
        for z in ZS689:
            lab[f"cfg689 {m} {s} B1 z*={z}"] = two(p["z"][z]["B1"], b["z"][z]["B1"] if b else None); print(f"  CFG689 {m:4s} {s:8s} B1 z*={z}: {lab[f'cfg689 {m} {s} B1 z*={z}']}")
        lab[f"cfg689 {m} {s} B2"] = two(p["B2"], b["B2"] if b else None); print(f"  CFG689 {m:4s} {s:8s} B2: {lab[f'cfg689 {m} {s} B2']}")
print("\nReported only: CFG684 with the sample's own drift at A = 0.35")
rep = {}
for s in ("full", "des_only"):
    r = g684("H035", s); rep[s] = r
    if r is None: print(f"  {s}: NOT RUN"); continue
    for c in COMBOS:
        x = r[c]; print(f"  CFG684 {s:8s} {c:12s}: flat-a0 Om {x['om_A0']:.4f} -> {x['om']:.4f} +- {x['sd']:.4f} (shift {x['shift']:+.4f}; would read {x['A2']}); dchi2_max {x['dchi2_max']:.2f}; sqrtX(2.33) {x['tracking']['2.33'][0]:.3f}-{x['tracking']['2.33'][1]:.3f}")
out.update(runs=R, labels=lab, reported_own_drift=rep)
json.dump(out, open(os.path.join(HERE, "agb7_results.json"), "w"), indent=1, default=float); print("\nwrote agb7_results.json")

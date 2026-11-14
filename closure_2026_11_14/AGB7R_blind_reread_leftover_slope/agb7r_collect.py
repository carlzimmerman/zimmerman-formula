"""AGB7R collector: harness checks H1-H3, the frozen labels with their second word, and the reported-only rows.
Reads this folder's outputs, LGS1's committed A = 0 runs, cfg684_results.json (H1) and AGB1's two A = 1 files (H2, H3 only).
Writes agb7r_results.json; prints the table (saved as agb7r_collect.out by the caller).
usage: python3 -I -B agb7r_collect.py
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
LGS = os.path.join(REPO, "closure_2026_11_13", "LGS1_legacy_sn_dropped")
AGB1 = os.path.join(REPO, "closure_2026_11_13", "AGB1_progenitor_age_bias")
C684 = os.path.join(REPO, "campaign_fresh_gravity", "CFG684_bao_cc_sn_robust", "cfg684_results.json")
SAMPLES, COMBOS, MODES = ("full", "des_only"), ("BAO+DES5", "BAO+DES5+CC"), ("D5", "TD5F")
Z684, Z689 = ("1.0", "1.5", "2.33"), ("1.0", "1.2", "1.5", "2.33")
PRIMARY, BRACKET = 0.23, 0.35


def amps(a): return ("%g" % a).replace(".", "p")
def load(p): return json.load(open(p)) if os.path.exists(p) else None
def f684(s, tpl, a): return load(os.path.join(HERE, f"agb7r_cfg684_{s}_{tpl}_A{amps(a)}.json"))
def f689(m, s, tpl, a): return load(os.path.join(HERE, f"agb7r_cfg689_{m}_{s}_{tpl}_A{amps(a)}.json"))


def status():
    st = {}
    p = os.path.join(HERE, "runs_status.txt")
    if os.path.exists(p):
        for line in open(p):
            w = line.split()
            if len(w) >= 3: st[w[0]] = int(w[2])          # the last line for a run wins (a retry after exit 75)
    return st


ST = status()
OUT = {"run_status": ST}
P = print


def q684(o):
    v = {"dchi2_max": o["dchi2_max"], "flat_mean": o["flat_a0_om"]["mean"], "flat_sd": o["flat_a0_om"]["sd"]}
    for z in Z684:
        for k in ("tracking", "rival"):
            v[f"{k}_lo_{z}"], v[f"{k}_hi_{z}"] = o[z][k]
    return v


def maxdiff(a, b):
    qa, qb = q684(a), q684(b); d = {k: abs(qa[k] - qb[k]) for k in qa}; k = max(d, key=d.get); return d[k], k


# ------------------------------------------------------------------ harness checks
P("AGB7R harness checks")
H = {}
r0, ref0 = f684("full", "S", 0), load(C684)
if r0 is None: H["H1"] = dict(ok=False, why="run missing")
else:
    per = {c: maxdiff(r0[c], ref0[c]) for c in COMBOS}
    H["H1"] = dict(ok=all(v[0] <= 1e-6 for v in per.values()), max_abs={c: v[0] for c, v in per.items()}, worst={c: v[1] for c, v in per.items()})
r1, ref1 = f684("full", "S", 1), load(os.path.join(AGB1, "agb1_cfg684_full_A1.json"))
if r1 is None: H["H2"] = dict(ok=False, why="run missing")
else:
    per = {c: maxdiff(r1[c], ref1[c]) for c in COMBOS}
    H["H2"] = dict(ok=all(v[0] <= 1e-9 for v in per.values()), max_abs={c: v[0] for c, v in per.items()}, worst={c: v[1] for c, v in per.items()})
r3, ref3 = f689("TD5F", "des_only", "S", 1), load(os.path.join(AGB1, "agb1_cfg689_TD5F_des_only_A1.json"))
if r3 is None: H["H3"] = dict(ok=False, why="run missing")
else:
    d5 = [abs(a - b) for z in Z689 for a, b in zip(r3["BAO+SN"]["P1"][z]["sqrtX_q"], ref3["BAO+SN"]["P1"][z]["sqrtX_q"])]
    d3 = [abs(r3["BAO+SN"]["P1"][z]["sqrtX_q"][i] - ref3["BAO+SN"]["P1"][z]["sqrtX_q"][i]) for z in Z689 for i in (1, 2, 3)]
    H["H3"] = dict(ok=max(d5) <= 0.005, max_abs_all5=max(d5), max_abs_16_50_84=max(d3), K4_run=r3["BAO+SN"]["K4"]["ok"], nstep_run=r3["nstep"])
for k, v in H.items(): P(f"  {k}: {'PASS' if v['ok'] else 'FAIL'}  {v}")
OUT["checks"] = H
EVAL684, EVAL689 = H["H1"]["ok"] and H["H2"]["ok"], H["H3"]["ok"]


def second(p, b, missing=False):
    if missing: return "NOT RUN (bracket)"
    if b is None: return "NOT EVALUABLE"
    return "ROBUST" if p == b else "FRAGILE"


# ------------------------------------------------------------------ CFG684 labels
def lab684(o, ref):
    m, sd, m0, sd0 = o["flat_a0_om"]["mean"], o["flat_a0_om"]["sd"], ref["flat_a0_om"]["mean"], ref["flat_a0_om"]["sd"]
    ce = math.hypot(sd, sd0); d = m - m0
    return dict(A1="DEGENERACY BROKEN" if o["dchi2_max"] >= 4 else "NOT BROKEN",
                A2="ROBUST" if abs(d) <= ce else "AGE-DEPENDENT",
                A3="FLOOR HOLDS" if o["2.33"]["tracking"][0] > 0 else "FLOOR LOST",
                nums=dict(dchi2_max=o["dchi2_max"], om=m, sd=sd, om0=m0, sd0=sd0, shift=d, comb_err=ce, shift_over_err=abs(d)/ce,
                          tracking_233=o["2.33"]["tracking"], rival_233=o["2.33"]["rival"],
                          tracking={z: o[z]["tracking"] for z in Z684}, e3={z: o[z]["e3"] for z in Z684}, om_best=o["om_best"]))


P("\nCFG684 (primary A = 0.23 T_S; second word from A = 0.35 T_S; reference LGS1 A = 0 of the same sample)")
OUT["cfg684"] = {}
for s in SAMPLES:
    ref = load(os.path.join(LGS, f"lgs1_cfg684_{s}.json"))
    rp, rb, ra1 = f684(s, "S", PRIMARY), f684(s, "S", BRACKET), f684(s, "S", 1)
    for c in COMBOS:
        cell = {}
        if rp is None:
            cell["labels"] = {k: "NOT RUN" for k in ("A1", "A2", "A3")}
        else:
            lp = lab684(rp[c], ref[c]); lb = lab684(rb[c], ref[c]) if rb is not None else None
            cell["primary"], cell["bracket"] = lp, lb
            cell["labels"] = {k: ("NOT EVALUABLE" if not EVAL684 else f"{lp[k]}, {second(lp[k], lb[k] if lb else None, rb is None)}") for k in ("A1", "A2", "A3")}
        r0_ = ref[c]
        cell["reference_A0"] = dict(dchi2_max=r0_["dchi2_max"], om=r0_["flat_a0_om"]["mean"], sd=r0_["flat_a0_om"]["sd"],
                                    tracking_233=r0_["2.33"]["tracking"],
                                    A1="DEGENERACY BROKEN" if r0_["dchi2_max"] >= 4 else "NOT BROKEN",
                                    A3="FLOOR HOLDS" if r0_["2.33"]["tracking"][0] > 0 else "FLOOR LOST")
        ratio = {}
        for tag, r in (("S0.23", rp), ("S0.35", rb), ("H0.35", f684(s, "H", 0.35))):
            if r is None or ra1 is None: ratio[tag] = None; continue
            dom1 = ra1[c]["flat_a0_om"]["mean"] - r0_["flat_a0_om"]["mean"]
            ratio[tag] = dict(flat_om=(r[c]["flat_a0_om"]["mean"] - r0_["flat_a0_om"]["mean"])/dom1 if dom1 else None,
                              tracking_lo_233=((r[c]["2.33"]["tracking"][0] - r0_["2.33"]["tracking"][0])/(ra1[c]["2.33"]["tracking"][0] - r0_["2.33"]["tracking"][0])
                                               if ra1[c]["2.33"]["tracking"][0] != r0_["2.33"]["tracking"][0] else None),
                              tracking_hi_233=((r[c]["2.33"]["tracking"][1] - r0_["2.33"]["tracking"][1])/(ra1[c]["2.33"]["tracking"][1] - r0_["2.33"]["tracking"][1])
                                               if ra1[c]["2.33"]["tracking"][1] != r0_["2.33"]["tracking"][1] else None))
        cell["A1_run"] = None if ra1 is None else lab684(ra1[c], r0_)
        cell["ratio_to_A1"] = ratio
        rh = f684(s, "H", 0.35)
        cell["T_H_0.35_reported"] = None if rh is None else lab684(rh[c], r0_)
        OUT["cfg684"][f"{s} {c}"] = cell
        P(f"  {s:8s} {c:12s}: " + "; ".join(f"{k} {v}" for k, v in cell["labels"].items()))
        P(f"      A = 0 (LGS1): dchi2_max {r0_['dchi2_max']:.3f}; flat-a0 Om {r0_['flat_a0_om']['mean']:.5f} +- {r0_['flat_a0_om']['sd']:.5f}; "
          f"tracking(2.33) [{r0_['2.33']['tracking'][0]:.4f}, {r0_['2.33']['tracking'][1]:.4f}]")
        for tag, L in (("A = 0.23 T_S", cell.get("primary")), ("A = 0.35 T_S", cell.get("bracket")), ("A = 0.35 T_H", cell["T_H_0.35_reported"]), ("A = 1 T_S", cell["A1_run"])):
            if L is None: P(f"      {tag}: not run"); continue
            n = L["nums"]
            P(f"      {tag}: dchi2_max {n['dchi2_max']:.3f} -> {L['A1']}; flat-a0 Om {n['om']:.5f} +- {n['sd']:.5f}, shift {n['shift']:+.5f}, "
              f"comb. err {n['comb_err']:.5f} ({n['shift_over_err']:.2f}) -> {L['A2']}; tracking(2.33) [{n['tracking_233'][0]:.4f}, {n['tracking_233'][1]:.4f}] -> {L['A3']}")
        P(f"      shift / (A = 1 shift), own A = 1 run: " + "; ".join(
            f"{t} " + ("n/a" if v is None else ", ".join(f"{k} {('n/a' if x is None else f'{x:.3f}')}" for k, x in v.items())) for t, v in ratio.items()))


# ------------------------------------------------------------------ CFG689 labels
def gate(o): return o is not None and o.get("nstep") == 60000 and bool(o["BAO+SN"]["K4"]["ok"])


def lab689(o, ref):
    a, b = o["BAO+SN"], ref["BAO+SN"]; B1 = {}
    for z in Z689:
        q, q0 = a["P1"][z]["sqrtX_q"], b["P1"][z]["sqrtX_q"]
        B1[z] = "STABLE" if (q0[1] <= q[2] <= q0[3] and q[1] <= q0[2] <= q[3]) else "SHIFTED"
    p0, p00 = (a["P0"] or {}).get("P0_class"), (b["P0"] or {}).get("P0_class")
    B2 = "CLASS UNCHANGED" if (a["P1_class"] == b["P1_class"] and p0 == p00) else "CLASS CHANGED"
    return dict(B1=B1, B2=B2, P1_class=a["P1_class"], P0_class=p0,
                nums=dict(sqrtX_q={z: a["P1"][z]["sqrtX_q"] for z in Z689}, e3={z: a["P1"][z]["e_3sigma"] for z in Z689},
                          P2=dict(cls=a["P2"]["P2_class"], dchi2=a["P2"]["dchi2"], dof=a["P2"]["dof"], sigma=a["P2"]["sigma_equiv"]),
                          H0_q=a["P3"]["H0_q"], K4=a["K4"]["ok"], max_rhat=max(a["K4"]["rhat"].values()), accept=a["K4"]["accept"], nstep=o["nstep"]))


def fmt689(tag, L, ref):
    n = L["nums"]
    P(f"      {tag}: P1 {L['P1_class']}; P0 {L['P0_class']}; P2 {n['P2']['cls']} (dchi2 {n['P2']['dchi2']:.2f}/{n['P2']['dof']}, {n['P2']['sigma']:.2f} sigma); "
      f"native H0 {n['H0_q'][2]:.2f} [{n['H0_q'][1]:.2f}, {n['H0_q'][3]:.2f}]; K4 {'ok' if n['K4'] else 'FAIL'} (max R-hat {n['max_rhat']:.4f}), nstep {n['nstep']}")
    for z in Z689:
        q, q0 = n["sqrtX_q"][z], ref["BAO+SN"]["P1"][z]["sqrtX_q"]
        P(f"        z* {z:4s}: sqrtX median {q[2]:.4f} 68% [{q[1]:.4f}, {q[3]:.4f}]  (A = 0: {q0[2]:.4f} [{q0[1]:.4f}, {q0[3]:.4f}])  "
          f"e_3sigma {n['e3'][z]} -> {L['B1'][z]}")


P("\nCFG689 (primary A = 0.23 T_S; second word from A = 0.35 T_S; reference LGS1 A = 0 of the same mode and sample)")
OUT["cfg689"] = {}
for m in MODES:
    for s in SAMPLES:
        ref = load(os.path.join(LGS, f"lgs1_cfg689_{m}_{s}.json"))
        rp, rb, ra1 = f689(m, s, "S", PRIMARY), f689(m, s, "S", BRACKET), f689(m, s, "S", 1)
        cell = dict(reference_gate=gate(ref), reference=dict(P1_class=ref["BAO+SN"]["P1_class"], P0_class=(ref["BAO+SN"]["P0"] or {}).get("P0_class"),
                    P2=ref["BAO+SN"]["P2"]["P2_class"], P2_sigma=ref["BAO+SN"]["P2"]["sigma_equiv"], H0_q=ref["BAO+SN"]["P3"]["H0_q"],
                    sqrtX_q={z: ref["BAO+SN"]["P1"][z]["sqrtX_q"] for z in Z689}, e3={z: ref["BAO+SN"]["P1"][z]["e_3sigma"] for z in Z689}))
        names = [f"B1 z* {z}" for z in Z689] + ["B2"]
        if rp is None:
            cell["labels"] = {k: "NOT RUN" for k in names}
        elif not EVAL689 or not gate(rp) or not cell["reference_gate"]:
            cell["labels"] = {k: "NOT EVALUABLE" for k in names}
        if rp is not None:
            lp = lab689(rp, ref); cell["primary"] = lp
            lb = lab689(rb, ref) if gate(rb) else None; cell["bracket"] = lab689(rb, ref) if rb is not None else None
            cell["bracket_gate"] = gate(rb)
            if "labels" not in cell:
                cell["labels"] = {f"B1 z* {z}": f"{lp['B1'][z]}, {second(lp['B1'][z], lb['B1'][z] if lb else None, rb is None)}" for z in Z689}
                cell["labels"]["B2"] = f"{lp['B2']}, {second(lp['B2'], lb['B2'] if lb else None, rb is None)}"
        ratio = {}
        for tag, r in (("S0.23", rp), ("S0.35", rb)):
            if r is None or ra1 is None: ratio[tag] = None; continue
            ratio[tag] = {}
            for z in Z689:
                d1 = ra1["BAO+SN"]["P1"][z]["sqrtX_q"][2] - ref["BAO+SN"]["P1"][z]["sqrtX_q"][2]
                ratio[tag][z] = (r["BAO+SN"]["P1"][z]["sqrtX_q"][2] - ref["BAO+SN"]["P1"][z]["sqrtX_q"][2])/d1 if d1 else None
        cell["ratio_to_A1"] = ratio
        cell["A1_run"] = None if ra1 is None else lab689(ra1, ref)
        OUT["cfg689"][f"{m} {s}"] = cell
        P(f"  {m:4s} {s:8s}: " + "; ".join(f"{k} {v}" for k, v in cell["labels"].items()))
        rr = cell["reference"]
        P(f"      A = 0 (LGS1): P1 {rr['P1_class']}; P0 {rr['P0_class']}; P2 {rr['P2']} ({rr['P2_sigma']:.2f} sigma); native H0 {rr['H0_q'][2]:.2f} "
          f"[{rr['H0_q'][1]:.2f}, {rr['H0_q'][3]:.2f}]; gate {'ok' if cell['reference_gate'] else 'FAIL'}")
        for tag, L in (("A = 0.23 T_S", cell.get("primary")), ("A = 0.35 T_S", cell.get("bracket")), ("A = 1 T_S", cell["A1_run"])):
            if L is None: P(f"      {tag}: not run"); continue
            fmt689(tag, L, ref)
        P(f"      median shift / (A = 1 shift), own A = 1 run: " + "; ".join(
            f"{t} " + ("n/a" if v is None else ", ".join(f"z* {z} {('n/a' if x is None else f'{x:.3f}')}" for z, x in v.items())) for t, v in ratio.items()))

P("\nruns_status.txt (exit 75 = NOT RUN):")
for k, v in sorted(ST.items()): P(f"  {k}: exit {v}" + ("  NOT RUN" if v == 75 else ""))
json.dump(OUT, open(os.path.join(HERE, "agb7r_results.json"), "w"), indent=1)
P("wrote agb7r_results.json")

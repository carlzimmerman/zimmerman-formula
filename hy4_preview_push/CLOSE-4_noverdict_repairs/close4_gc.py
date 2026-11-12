#!/usr/bin/env python3
"""CLOSE-4 R3 (FROZEN_CRITERIA.md, committed alone before this file ran): ONE grid-convergence rule, RULE-GC, applied
to the whole external-field family -- SCS2, SCS3 and EFN1 -- on the ladders already in the record. No solver is run.

RULE-GC is adopted verbatim from SCS3's A4 rule (amendment b34295ebcd, section 3, flat clause removed) and DCN1's
section 2 (d603f1703c), which adopted the same rule and validated it in DCN1's KA3 (12 of 12 to 2.4e-15 on
h = 1/N_R; h^-1 and h^-0.5 Diverging; 1 + h^0.3 not Converged). CLOSE-4 adds no clause to the arithmetic -- only the
two clauses the three lanes left implicit: the n < 3 case and the lane-level combination.

  OMP_NUM_THREADS=1 python3 close4_gc.py   -> parts/gc_SCS2.json/.out, gc_SCS3.json/.out, gc_EFN1.json/.out

kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Cold dark energy is a gravitating field
component, never a particle."""
import os, sys, json, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SCS3 = os.path.join(ROOT, "fable52_push", "SCS3_external_field_stability")
EFN1 = os.path.join(ROOT, "closure_2026_11_10", "EFN1_external_field_nonlinear")
RHO = 1.5

# ------------------------------------------------------------------ RULE-GC
def rule_gc(Q, rho=RHO):
    """Q: list of values, index 0 = coarsest, h_{i+1} = h_i / rho. Returns the RULE-GC verdict."""
    n = len(Q)
    o = dict(n=n, values=[float(v) for v in Q])
    if n < 3:
        o.update(verdict="NOT EVALUABLE", two_grid_rel_change=float(abs(Q[-1] - Q[-2]) / abs(Q[-2])) if n == 2 and Q[-2] else None)
        return o
    Qc, Qm, Qf = Q[-3], Q[-2], Q[-1]
    d1, d2 = Qm - Qc, Qf - Qm
    o.update(d1=float(d1), d2=float(d2))
    if d1 * d2 > 0 and abs(d2) < abs(d1):                      # monotone, shrinking
        p = math.log(d1 / d2) / math.log(rho)
        Qinf = Qf + d2 / (rho ** p - 1)
        E = 1.25 * abs(d2) / (rho ** p - 1)
        if n >= 4:
            Qc2, Qm2, Qf2 = Q[-4], Q[-3], Q[-2]
            d1b, d2b = Qm2 - Qc2, Qf2 - Qm2
            if d1b * d2b > 0 and abs(d2b) < abs(d1b):
                pb = math.log(d1b / d2b) / math.log(rho)
                Qinf_b = Qf2 + d2b / (rho ** pb - 1)
            else:
                Qinf_b = 0.5 * (Qm2 + Qf2)
            E = max(E, abs(Qinf - Qinf_b))
            o.update(Q_inf_previous_three=float(Qinf_b))
        o.update(p=float(p), Q_inf=float(Qinf), E=float(E), branch="monotone")
        ok_p = 0.5 <= p <= 6.0
        ok_E = E <= 0.20 * abs(Qinf) if Qinf != 0 else False
        o.update(verdict="CONVERGED" if (ok_p and ok_E) else "NOT CONVERGED",
                 p_in_window=bool(ok_p), E_within_20pct=bool(ok_E))
        return o
    if d1 * d2 < 0:                                            # oscillating
        Qinf = 0.5 * (Qm + Qf); E = max(abs(d1), abs(d2))
        o.update(Q_inf=float(Qinf), E=float(E), branch="oscillating")
        o.update(verdict="CONVERGED" if E <= 0.20 * abs(Qinf) else "NOT CONVERGED", p_in_window=None,
                 E_within_20pct=bool(E <= 0.20 * abs(Qinf)))
        return o
    if d2 == 0:
        o.update(Q_inf=float(Qf), E=float(abs(d1)), branch="flat")
        o.update(verdict="CONVERGED" if abs(d1) <= 0.20 * abs(Qf) else "NOT CONVERGED", p_in_window=None,
                 E_within_20pct=bool(abs(d1) <= 0.20 * abs(Qf)))
        return o
    # monotone with |d2| >= |d1|  -> diverging candidate
    if d1 * d2 > 0:
        prev_ok = None
        if n >= 4:
            Qc2, Qm2, Qf2 = Q[-4], Q[-3], Q[-2]
            d1b, d2b = Qm2 - Qc2, Qf2 - Qm2
            prev_ok = bool(d1b * d2b > 0 and abs(d2b) >= abs(d1b))
        o.update(branch="monotone_nonshrinking", previous_three_also_nonshrinking=prev_ok)
        o.update(verdict="DIVERGING" if (prev_ok is not False) else "NOT CONVERGED")
        return o
    o.update(branch="other", verdict="NOT CONVERGED")
    return o

def combine(rows):
    """SCS3's A4 lane-level rule: a family is decided only if EVERY background is CONVERGED."""
    v = [r["verdict"] for r in rows]
    c = collections.Counter(v)
    if c.get("DIVERGING"): fam = "DIVERGING (RATE UNBOUNDED for a rate quantity)"
    elif c.get("NOT CONVERGED"): fam = "NO VERDICT"
    elif c.get("NOT EVALUABLE"): fam = "NO VERDICT (NOT EVALUABLE: fewer than three resolutions)"
    else: fam = "CONVERGED"
    return fam, dict(c)

def write(name, res, lines):
    os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "parts", f"gc_{name}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "parts", f"gc_{name}.out"), "w").write("\n".join(lines) + "\n")

# ================================================================== SCS2 and SCS3 (the same ladder)
MAPS = json.load(open(os.path.join(SCS3, "scs3_maps_AX_A4.json")))["rows"]
MAPS0 = json.load(open(os.path.join(SCS3, "scs3_maps_AX.json")))["rows"]   # the pre-A4 maps, R0-R3
R2 = json.load(open(os.path.join(SCS3, "scs3_route2_AX_A1_R01234_p0.json")))["rows"]

def bgkey(spec):
    return (spec["foot"], spec["group"], spec["kind"], spec["logm"], spec["ge"], spec["axis"])

LADDER = collections.defaultdict(dict)          # bgkey -> res -> row
for k, v in MAPS.items():
    LADDER[bgkey(v["spec"])][v["res"]] = v
LADDER0 = collections.defaultdict(dict)         # the pre-A4 ladder, R0-R3
for k, v in MAPS0.items():
    LADDER0[bgkey(v["spec"])][v["res"]] = v
R2LAD = collections.defaultdict(dict)
for v in R2:
    R2LAD[bgkey(v["spec"])][v["res"]] = v

QMAPS = {"frac_neg_over_pos": lambda r: r["map"]["frac_neg_over_pos"],
         "min_dp_offplane":   lambda r: r["map"]["min_dp_offplane"],
         "Gamma_L2_routeL":   lambda r: r["routeL"]["L"]["Gamma2_max_s2"],
         "inner_radius_over_re": lambda r: r["routeL"]["L"]["r_over_re"]}

def run_ladder(get, lad, resmax=None):
    ks = sorted(lad.keys())
    seq = [get(lad[k]) for k in ks if (resmax is None or k <= resmax)]
    if any(v is None for v in seq): return None
    return rule_gc(seq)

# --- SCS2's family: the axial external-field backgrounds (group AX, g_e > 0).  SCS2 as landed has R0 and R1 only;
#     SCS3's AX ladder is SCS2's own backgrounds at R0-R6 (SCS3 section 1: "Backgrounds are SCS2's exactly").
EXT = {b: v for b, v in LADDER.items() if v and b[1] == "AX"}
EXT0 = {b: v for b, v in LADDER0.items() if v and b[1] == "AX"}
LINES = ["CLOSE-4 R3 -- RULE-GC applied to SCS2's axial external-field family",
         "SCS2 as landed has R0 and R1 only, so RULE-GC returns NOT EVALUABLE there. The third-and-beyond",
         "resolutions come from the record: SCS3's AX backgrounds are SCS2's exactly (SCS3 section 1).",
         "LADDER CHECK (all 32 twins, SCS2's stored fine/coarse against SCS3's R1/R0):",
         "  min_dp_fine  matches scs3_maps_AX.json 32/32 and scs3_maps_AX_A4.json 32/32",
         "  frac_fine    matches scs3_maps_AX.json 32/32 and scs3_maps_AX_A4.json  0/32",
         "SCS3's A4 rerun changed the negative REGION (n_negative_offplane 70 -> 110 on alt_expo_10.45_0.01 R1),",
         "so the charge fraction is a different number under A4. SCS2's charge fraction is the pre-A4 one.",
         "GRADED for SCS2: the charge fraction on the pre-A4 ladder (R0-R3), the minimum G on both ladders.",
         "SCS2's graded KA4 quantities are the negative-cell charge fraction and the minimum G.", ""]
S2 = dict(lane="CLOSE-4 R3 / SCS2", family="axial external field (SCS2's 32 twins)",
          ladder="scs3_maps_AX.json R0-R3 for the charge fraction; scs3_maps_AX_A4.json R0-R6 for the minimum G",
          quantities={})
for qname, get, lad in (("frac_neg_over_pos", QMAPS["frac_neg_over_pos"], EXT0),
                        ("min_dp_offplane", QMAPS["min_dp_offplane"], EXT0),
                        ("min_dp_offplane__A4_ladder_R0_R6", QMAPS["min_dp_offplane"], EXT)):
    per = {}
    for b, l in sorted(lad.items()):
        r = run_ladder(get, l)
        if r is None: continue
        per["_".join(map(str, b))] = r
    fam, cnt = combine(list(per.values()))
    S2["quantities"][qname] = dict(family_reading=fam, counts=cnt, per_background=per)
    LINES.append(f"  {qname}: {cnt} -> {fam}")
LINES.append("")
LINES.append("  SCS2 as landed (two resolutions, R0 and R1):")
for qname, get in (("frac_neg_over_pos", QMAPS["frac_neg_over_pos"]), ("min_dp_offplane", QMAPS["min_dp_offplane"])):
    per = {}
    for b, lad in sorted(EXT.items()):
        r = run_ladder(get, lad, resmax=1)
        if r is None: continue
        per["_".join(map(str, b))] = r
    fam, cnt = combine(list(per.values()))
    S2["quantities"][qname + "__SCS2_as_landed_R0_R1"] = dict(family_reading=fam, counts=cnt, per_background=per)
    LINES.append(f"    {qname}: {cnt} -> {fam}")
write("SCS2", S2, LINES)

# --- SCS3's own graded quantities, on the same ladder, plus route 2
LINES = ["CLOSE-4 R3 -- RULE-GC applied to SCS3's axial family (SCS3's own graded quantities)",
         "Ladder: scs3_maps_AX_A4.json R0-R6 (route L, the maps) and scs3_route2_AX_A1_R01234_p0.json R0-R4 (route 2).", ""]
S3 = dict(lane="CLOSE-4 R3 / SCS3", family="AX, external field along the axis", quantities={})
for qname in ("Gamma_L2_routeL", "frac_neg_over_pos", "min_dp_offplane", "inner_radius_over_re"):
    get = QMAPS[qname]; per = {}
    for b, lad in sorted(EXT.items()):
        r = run_ladder(get, lad)
        if r is None: continue
        per["_".join(map(str, b))] = r
    fam, cnt = combine(list(per.values()))
    S3["quantities"][qname] = dict(family_reading=fam, counts=cnt, per_background=per)
    LINES.append(f"  route L / maps -- {qname}: {cnt} -> {fam}")
per = {}
for b, lad in sorted(R2LAD.items()):
    if b[1] != "AX": continue
    r = run_ladder(lambda r: r["Gamma2_s2"], lad)
    if r is None: continue
    per["_".join(map(str, b))] = r
fam, cnt = combine(list(per.values()))
S3["quantities"]["Gamma2_route2"] = dict(family_reading=fam, counts=cnt, per_background=per)
LINES.append(f"  route 2 -- Gamma_2^2 = -lambda_min: {cnt} -> {fam}")
write("SCS3", S3, LINES)

# ================================================================== EFN1
D = json.load(open(os.path.join(EFN1, "efn1_route_d_main.json")))["runs"]
DL = collections.defaultdict(dict)
for k, v in D.items():
    s = v["spec"]
    DL[(s["name"], s["foot"], s["kind"], s["logm"], s["ge"])][s["res"]] = v
LINES = ["CLOSE-4 R3 -- RULE-GC applied to EFN1",
         "Route D: the graded quantity is the stop time tF_efolds (when the shell's amplitude reaches c = 10),",
         "on EFN1's R2-R3-R4 ladder in efn1_route_d_main.json (12 backgrounds, both footings).",
         "Route W: efn1_labels.json stores Gamma, c3, c2 at two resolutions only (R2, R3) -> NOT EVALUABLE.", ""]
E = dict(lane="CLOSE-4 R3 / EFN1", quantities={})
per = {}
for b, lad in sorted(DL.items()):
    seq = [lad[r]["tF_efolds"] for r in sorted(lad)]
    per["_".join(map(str, b))] = rule_gc(seq)
fam, cnt = combine(list(per.values()))
E["quantities"]["routeD_stop_time_tF_efolds"] = dict(family_reading=fam, counts=cnt, per_background=per)
LINES.append(f"  route D stop time: {cnt} -> {fam}")
LINES.append("")
LINES.append("  Per background (route D):")
def fmt(x, spec):
    return format(x, spec) if isinstance(x, (int, float)) else str(x)
for k, r in sorted(per.items()):
    LINES.append(f"    {k}: n {r['n']}, d1 {fmt(r.get('d1'), '+.3f')}, d2 {fmt(r.get('d2'), '+.3f')}, "
                 f"branch {r.get('branch')}, prev3_nonshrinking {r.get('previous_three_also_nonshrinking')} "
                 f"-> {r['verdict']}")
W = json.load(open(os.path.join(EFN1, "efn1_labels.json")))["route_W"]
wres = {}
for k, v in W.items():
    for qn in ("c2", "c3"):
        wres.setdefault(qn, {})[k] = rule_gc(v[qn])
for qn in ("c2", "c3"):
    fam, cnt = combine(list(wres[qn].values()))
    E["quantities"][f"routeW_{qn}"] = dict(family_reading=fam, counts=cnt, per_background=wres[qn])
    LINES.append(f"  route W {qn}: {cnt} -> {fam}")
write("EFN1", E, LINES)
print("\n".join(LINES))

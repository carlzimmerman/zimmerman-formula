#!/usr/bin/env python3
"""PAPER64 audit: every quoted number must match the committed lane outputs (rebuild_2026_10_22/ BS1, LEE1, FM1, SG1, BC1, RT1, EF1,
SP1, SP2, HO3 JSON / CSV); the sealed hashes must match the sealed files; the PDF must be newer than the TeX; naming rules
(cold dark energy; CDM only inside LambdaCDM), no local path.
Run: python3 PAPER64_audit.py (exit 0 only if all pass).
     python3 PAPER64_audit.py --mutate (perturbs every JSON-derived number; exit 0 only if every number check then FAILS)."""
import json, os, re, csv, hashlib, math, sys

MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.normpath(os.path.join(HERE, "..", "..", "rebuild_2026_10_22"))
STEM = "PAPER64_the_basin_rule_2026"
TEX = open(os.path.join(HERE, STEM + ".tex")).read()
F = N = 0; NUMF = NUMN = 0
def check(name, ok, msg=""):
    global F, N
    N += 1; F += (not ok)
    if not MUT: print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))
def J(rel): return json.load(open(os.path.join(RB, rel)))
def bump(t):
    for i in range(len(t) - 1, -1, -1):
        if t[i].isdigit(): return t[:i] + str((int(t[i]) + 1) % 10) + t[i + 1:]
    return t + "1"
def num(name, value, fmt):
    global NUMF, NUMN
    s = format(value, fmt)
    if MUT: s = bump(s)
    ok = s in TEX
    NUMN += 1; NUMF += (not ok)
    if not MUT: check(name, ok, f"'{s}'")

bs1 = J("BS1_basin_switch/bs1_basin_switch_results.json")
num("BS1 LG R0", bs1["LG"]["R0_data_kpc"], ".1f"); num("BS1 LG R0 sigma", bs1["LG"]["R0_sigma_kpc"], ".1f"); num("BS1 LG log M_basin", bs1["LG"]["basin"]["lgM"], ".3f")
lee = J("LEE1_look_elsewhere/lee1_results.json")["verdict"]
num("LEE1 p_hat", lee["p_hat"], ".3f"); num("LEE1 CP lo", lee["cp68"][0], ".3f"); num("LEE1 CP hi", lee["cp68"][1], ".3f")
fm = J("FM1_hg2_forward_model/fm1_hg2_forward_model_results.json")
pv = fm["footings"]["canonical"]["variants"]["PRIMARY s_int"]
num("FM1 s_int", pv["s"], ".3f"); num("FM1 D_mod median", pv["median"], "+.3f"); num("FM1 D_meas", fm["D_meas"], "+.3f"); num("FM1 q", pv["q"], ".3f")
sg = J("SG1_sluggs_imf_gas/sg1_sluggs_imf_gas_results.json")["footings"]["canonical"]
num("SG1 no-gas mean", sg["cl2"]["mean"], "+.3f"); num("SG1 trunc mean", sg["trunc"]["mean"], "+.3f"); num("SG1 extrap mean", sg["extrap"]["mean"], "+.3f")
mj = [v for v in sg["Mstar_over_Mjam"].values() if v is not None]
num("SG1 M*/M_JAM min", min(mj), ".2f"); num("SG1 M*/M_JAM max", max(mj), ".2f")
bc = J("BC1_xcop_bcg_cores/bc1_xcop_bcg_cores_results.json")["runs"]
num("BC1 step0 0.1R500", bc["step0"]["canonical"]["by_x"]["0.1"], "+.3f"); num("BC1 ICL 0.1R500", bc["V-ICL (ADD x2) Re 20"]["canonical"]["by_x"]["0.1"], "+.3f")
rt = J("RT1_lt_rotation_regrade/rt1_lt_rotation_regrade_results.json")["lg"]["canonical"]["IC 1613"]["MSED"]
num("RT1 IC1613 E_rot", rt["E"], "+.3f"); num("RT1 IC1613 Z", rt["Z"], "+.2f")
ho3 = [r for r in csv.DictReader(open(os.path.join(RB, "HO3_dwarf_individuals_heldout", "ho3_dwarf_individuals_per_object.csv"))) if r["footing"] == "canonical" and r["name"] == "IC 1613"][0]
num("HO3 IC1613 E", float(ho3["E"]), "+.3f")
ef = J("EF1_basin_external_field/ef1_basin_external_field_results.json")
mx = max(abs(r["dEF"]) for f in ef["footings"].values() for r in f["rows"])
s = format(math.ceil(mx * 1e4) / 1e4, ".4f"); s = bump(s) if MUT else s
NUMN += 1; NUMF += (s not in TEX)
if not MUT: check("EF1 max EFE shift (ceil to 1e-4)", s in TEX, f"'{s}'")
sp2 = J("SP2_sealed_basin_lensing/sp2_predictions.json")["footings"]
num("SP2 S_env canonical", sp2["canonical"]["S_env"], ".3f"); num("SP2 S_env alt", sp2["alt"]["S_env"], ".3f")
num("LG 1.5e11 bound is stated", 1.5, ".1f")
if not MUT:
    for lab, path in (("SP1", "SP1_sealed_lensing_step/sp1_predictions.json"), ("SP2", "SP2_sealed_basin_lensing/sp2_predictions.json")):
        h = hashlib.sha256(open(os.path.join(RB, path), "rb").read()).hexdigest()
        check(f"{lab} sealed hash head/tail in TeX", f"{h[:8]}\\ldots{h[-4:]}" in TEX, f"{h[:8]}...{h[-4:]}")
        seal = open(os.path.join(RB, os.path.dirname(path), "SEAL.md")).read()
        check(f"{lab} SEAL.md matches file", h in seal)
    pdf = os.path.join(HERE, STEM + ".pdf")
    check("PDF newer than TeX", os.path.exists(pdf) and os.path.getmtime(pdf) >= os.path.getmtime(os.path.join(HERE, STEM + ".tex")))
    check("no 'cold dark matter'", "cold dark matter" not in TEX.lower())
    check("CDM only inside LambdaCDM", all(TEX[max(0, m.start() - 8):m.start()] == "\\Lambda$" for m in re.finditer("CDM", TEX)))
    check("no local path", "/Users/" not in TEX and "carlzimmerman" not in TEX.lower())
    check("kappa fitted stated", "fitted" in TEX and "not closed" in TEX)
if MUT:
    print(f"MUTATE: {NUMF}/{NUMN} number checks fail (all must)")
    sys.exit(0 if NUMF == NUMN else 1)
print(f"PAPER64 audit: {N - F}/{N} pass")
sys.exit(0 if F == 0 else 1)

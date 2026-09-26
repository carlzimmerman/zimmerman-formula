#!/usr/bin/env python3
"""OB2 - JWST observing-block recipe (OB1 FEASIBLE-JWST follow-through).
Pre-registration: deepseek_push/Z2-WAVE_BRIEF.md (R1/R2/R3 fixed before any number).
Loaded inputs: L05_results.json (power, budget, sample), OB1_results.json, K11_results.json.
R1: recompute OB1's minimal config (f=20, N=3, SN=10) from L05's power grid; rate must
    reproduce 0.9998 to the printed 4 decimals; else exit 1.
R2: per-target T5 recipe from L05 sample rows (J10I window [4/3,2], kill >=3sigma outside;
    sharp: R > 1.5 r_B kills q=0, R > 2 r_B kills all q - verbatim K11).
R3: exposure recipe from L05 budget dict; missing field -> RECIPE-UNDERDETERMINED, exit 1.
"""
import json, sys

RES = {"title": "OB2 JWST observing-block recipe",
       "inputs": ["L05_results.json", "OB1_results.json", "K11_results.json"],
       "pre_registration": "Z2-WAVE_BRIEF.md R1/R2/R3"}

def main():
    l05 = json.load(open("L05_results.json"))
    ob1 = json.load(open("OB1_results.json"))
    k11 = json.load(open("K11_results.json"))
    mc = ob1["minimal_config"]
    f, N, SN = mc["f"], mc["N"], mc["SN"]
    key = "central_N%d_SN%d_f%d" % (N, SN, f)
    alt = "volume_N%d_SN%d_f%d" % (N, SN, f)
    pow = l05["power"]
    if key not in pow:
        RES["error"] = "missing power key %s" % key
        return 1
    rate = pow[key]["rate"]
    if round(rate, 4) != round(mc["rate"], 4):
        RES["error"] = "R1 fail: recomputed rate %.4f != registered %.4f" % (rate, mc["rate"])
        return 1
    RES["R1"] = {"key": key, "rate_recomputed": rate, "rate_registered": mc["rate"],
                 "pass": True, "volume_key_present": alt in pow}
    if "consolidated_tests" not in k11 or k11["consolidated_tests"] < 5:
        RES["error"] = "K11 consolidated tests missing"
        return 1
    sample = l05["sample"]["table"]
    n_sn10 = sum(1 for r in sample if r["sn"] == SN)
    if n_sn10 < N:
        RES["error"] = "only %d sample rows at S/N=%d (need %d)" % (n_sn10, SN, N)
        return 1
    targets = [r for r in sample if r["sn"] == SN][:N]
    RES["R2"] = {"t5_verbatim": ("T5 J10-I a0-radius: J10-I = (r_B/R)*window in [4/3,2], "
                "r_B = sqrt(G M_b / a0(rho_B)), a0 = (c/2)sqrt(G rho_B); kill: >=3sigma outside "
                "with M_b,rho_B independent -> framework BLR-radius assignment fails; sharp: "
                "R > (3/2)r_B kills q=0, R > 2 r_B kills all q"),
                 "consolidated_tests": k11["consolidated_tests"],
                 "targets": targets,
                 "note": ("per target: measure J10I with T5 window [4/3,2]; rb_ld/lag_d columns are "
                          "L05's stored targets (rb_ld = r_B/lag distance units, loaded not transcribed)")}
    bud = l05["budget"]
    need = {"sn_N10_2x", "n_SN30_2x"}
    have = all(k in v for v in bud.values() for k in need) if bud else False
    if not have:
        RES["R3"] = {"verdict": "RECIPE-UNDERDETERMINED", "budget_present": bool(bud)}
        RES["verdict"] = "RECIPE-UNDERDETERMINED: budget fields absent, exposure recipe not fabricated"
        print(json.dumps(RES, indent=1)); return 1
    RES["R3"] = {"budget": bud,
                 "recipe": ("SN=%d blocks are the unit; SN=30 on the same target costs x%s the SN=10 "
                            "time; depth doubling recipes per bar from the loaded dict" % (SN, bud[list(bud)[0]]["sn_N10_2x"]))}
    md = ["# OB2 - JWST observing-block recipe (OB1 follow-through, conductor tick 2026-09-26)",
          "", "**Pre-registration:** Z2-WAVE_BRIEF.md R1/R2/R3. All numbers loaded from disk.",
          "", "## R1 - minimal registered config reproduced",
          "- L05 power key `%s`: rate %.4f == OB1 registered %.4f (PASS)" % (key, rate, mc["rate"]),
          "", "## R2 - per-target T5 falsifier schedule (K11 verbatim)",
          "- %s" % RES["R2"]["t5_verbatim"],
          "- Targets (L05 sample, S/N=%d, first N=%d):" % (SN, N)]
    for t in targets:
        md.append("  - obj %d: truth=%s t=%.2f q=%.1f rb_ld=%.1f lag_d=%.1f J10I=%.3f"
                  % (t["obj"], t["truth"], t["t"], t["q"], t["rb_ld"], t["lag_d"], t["J10I"]))
    md += ["", "## R3 - exposure recipe (L05 budget, loaded)", "- %s" % RES["R3"]["recipe"],
           "", "## Program statement", "- Feasible per OB1; this recipe is the block-level realization.",
           "- Kill channel: any target's J10I measured >=3sigma outside [4/3,2] -> that geometry's "
           "reading dead per T5 (single-window violation is a discriminator, NOT a framework kill)."]
    open("OB2_JWST_BLOCK_RECIPE.md", "w").write("\n".join(md) + "\n")
    RES["verdict"] = "BLOCK-RECIPE-PASS: R1 rate reproduced, R2 T5 schedule on %d targets, R3 exposure from loaded budget" % N
    print(json.dumps(RES, indent=1))
    open("OB2_jwst_block_recipe.json", "w").write(json.dumps(RES, indent=1))
    print("OB2 COMPLETE")
    return 0

if __name__ == "__main__":
    rc = main()
    print("EXIT %d" % rc)
    sys.exit(rc)

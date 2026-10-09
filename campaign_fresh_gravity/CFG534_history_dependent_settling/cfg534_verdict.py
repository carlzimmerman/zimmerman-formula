#!/usr/bin/env python3
"""CFG534 verdict: applies the frozen ladder (FROZEN_CRITERIA.md, aa8dc312e) to cfg534_kids_results.json and
cfg534_sparc_sluggs_results.json. Post-freeze diagnostics are printed for context and carry no weight.
Run: python3 cfg534_verdict.py
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, "cfg534_kids_results.json")))
S = json.load(open(os.path.join(HERE, "cfg534_sparc_sluggs_results.json")))
KM = json.load(open(os.path.join(HERE, "cfg534_kids_results_MUTATE.json")))
SM = json.load(open(os.path.join(HERE, "cfg534_sparc_sluggs_results_MUTATE.json")))
LOG, OUT = [], {"lane": "CFG534", "script": "cfg534_verdict", "criteria_commit": "aa8dc312e"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)


for foot in ("canonical", "alt"):
    R = K["rules"][foot]; sp = S["sparc"][foot]; sl = S["sluggs"][foot]
    # Test 4 radial
    sp_oi, sp_in = sp["d_oi"]["Z"], sp["d_in"]["Z"]
    t_oi, t_in = sl["T4|D_out-D_in"], sl["T4|D_in"]
    extra = ((sp_oi >= 2) or (t_oi["rho"] > 0 and t_oi["p_pos"] < 0.05)) and not (sp_oi <= -2 or (t_oi["rho"] < 0 and t_oi["p_neg"] < 0.05))
    ml = ((sp_in >= 2 and sp["d_oi"]["diff"] <= 0) or (t_in["rho"] > 0 and t_in["p_pos"] < 0.05 and t_oi["rho"] <= 0))
    radial = "MIXED (NOT DIAGNOSTIC)" if (extra and ml) else "EXTRA MASS" if extra else "M/L" if ml else "NOT DIAGNOSTIC"
    sparc_contra = sp["d_out"]["Z"] <= -2
    same_elsewhere = R["same_sign_1b"] and sp["d_out"]["diff"] > 0 and sl["T2|H_score"]["rho"] > 0
    if R["sig_1a_max"] > 0.30:
        v = "NOT DIAGNOSTIC"
    elif (not R["ge2_1a"]) or R["contra_1a"] or R["contra_1b"] or sparc_contra:
        v = "H NOT SUPPORTED"
    elif radial == "M/L":
        v = "M/L-PREFERRED"
    elif R["pass_1a"] and same_elsewhere and radial == "EXTRA MASS":
        v = "H SUPPORTED"
    else:
        v = "H CONSISTENT-WEAK"
    OUT[foot] = dict(verdict=v, radial=radial, sigma_1a_max=R["sig_1a_max"], Z_1a=R["Z_1a"], Z_1b=R["Z_1b"], sparc_d_out_Z=sp["d_out"]["Z"],
                     sparc_d_oi_Z=sp_oi, sparc_d_in_Z=sp_in, sluggs_Hscore_rho=sl["T2|H_score"]["rho"], same_sign_elsewhere=same_elsewhere,
                     late_on_law=R["late_on_law"])
    P(f"[{foot}] 1a: sigma max {R['sig_1a_max']:.3f}, Zmin {R['Z_1a']}; 1b Zmin {R['Z_1b']}; SPARC d_out Z {sp['d_out']['Z']:+.2f}, "
      f"d_out-d_in Z {sp_oi:+.2f}, d_in Z {sp_in:+.2f}; SLUGGS composite rho {sl['T2|H_score']['rho']:+.3f}; radial {radial}")
    P(f"[{foot}] VERDICT (frozen ladder): {v}")
    pf = K["postfreeze_overlap"]["1a_type"]
    P(f"[{foot}]   post-freeze context (no weight): overlap-weighted 1a Z " +
      ", ".join(f"{c} {pf[f'{c}|{foot}']['K9']['d_eps_moster']['Z']:+.2f}" for c in ("A", "B")))
labs = {OUT[f]["verdict"] for f in ("canonical", "alt")}
OUT["headline"] = OUT["canonical"]["verdict"] if len(labs) == 1 else f"FOOTING-DEPENDENT: canonical {OUT['canonical']['verdict']} / alt {OUT['alt']['verdict']}"
OUT["mutate"] = {"kids": {k: v["ok"] for k, v in KM["checks"].items()}, "sparc_sluggs": {k: v["ok"] for k, v in SM["checks"].items()}}
P(f"HEADLINE: {OUT['headline']}")
P(f"MUTATE: {OUT['mutate']}")
json.dump(OUT, open(os.path.join(HERE, "cfg534_verdict_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg534_verdict.out"), "w").write("\n".join(LOG) + "\n")

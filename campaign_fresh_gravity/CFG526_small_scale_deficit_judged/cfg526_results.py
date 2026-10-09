#!/usr/bin/env python3
"""CFG526: collect the frozen verdicts (A from cfg526_profiles*.json, B from cfg526_data*.json) into cfg526_results.json."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda f: json.load(open(os.path.join(HERE, f)))
A, AM, B, BM, PH = J("cfg526_profiles.json"), J("cfg526_profiles_MUTATE.json"), J("cfg526_data.json"), J("cfg526_data_MUTATE.json"), J("cfg526_posthoc.json")
core = lambda n: {k: A["runs"][n]["core"][k][0] for k in ("R", "R_noexp", "R_in", "D_eng", "D_part", "D_law")}
out = {"lane": "CFG526", "date": "2026-10-09", "settings": "kappa = 1/2 FITTED; footings never pooled; a0 flat; nu_mono; cold energy MASS required; not theory closed",
       "A": {f: A["verdict"][f] for f in A["verdict"]},
       "A_core_medians": {n: core(n) for n in A["runs"] if "core" in A["runs"][n]},
       "A_M1_NOCOMP": A["M1"], "A_M2_emptied_core": AM["verdict"]["canonical"]["verdict"],
       "B": {f: {k: B[f][k] for k in ("verdict", "why", "converged", "monotone", "r_conservative_z05", "tracer_shift", "lya_flag")} |
                {"F1_conservative": B[f]["cases"]["F=1 conservative r"], "fidhi_conservative": B[f]["cases"]["fid-hi F, conservative r"],
                 "fidlo_conservative": B[f]["cases"]["fid-lo F, conservative r"], "LCDM_fidlo": B[f]["cases"]["LCDM, fid-lo F"]} for f in B},
       "B_MUTATE_detected": all(BM[f]["mutate_excluded"] and BM[f]["lcdm_not_excluded"] for f in BM),
       "posthoc_lensing_tracer_not_gating": PH,
       "literature_PROVISIONAL": {"KiDS-1000 A_mod (Amon & Efstathiou 2022)": [0.858, 0.052], "DES Y3 A_mod (Preston, Amon & Efstathiou 2023)": [0.82, 0.04]}}
json.dump(out, open(os.path.join(HERE, "cfg526_results.json"), "w"), indent=1)
print(json.dumps({"A": {f: v["verdict"] for f, v in out["A"].items()}, "B": {f: v["verdict"] for f, v in out["B"].items()},
                  "M1": out["A_M1_NOCOMP"]["detected"], "M2": out["A_M2_emptied_core"], "B_MUT": out["B_MUTATE_detected"]}))

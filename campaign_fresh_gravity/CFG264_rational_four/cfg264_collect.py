#!/usr/bin/env python3
"""CFG264: collect the per-route results into results.json (lane summary). Reads only this directory's *_results.json."""
import json
import hashlib

FROZEN_ORIGINAL = "ff8657eb7286103a635ace15c142bcea90d299766b8a377c9b345c3abedce769"


def load(p):
    with open(p) as f:
        return json.load(f)


r1, r1m = load("r1_virial_lambda_results.json"), load("r1_virial_lambda_MUTATE_results.json")
r2, r2m = load("r2_two_sided_junction_results.json"), load("r2_two_sided_junction_MUTATE_results.json")
od, odm = load("od_horizon_quarter_results.json"), load("od_horizon_quarter_MUTATE_results.json")

sha_lines = open("CFG264_FROZEN_CRITERIA.sha256").read().split("\n")
summary = {
    "lane": "CFG264 -- constrained attempt to derive the rational 4 in G rho_Lambda = 4 a0^2/c^2",
    "frozen_criteria_original_sha256": sha_lines[0].split()[0],
    "frozen_hash_matches_record": sha_lines[0].split()[0] == FROZEN_ORIGINAL,
    "addenda": ["Addendum 1: R1 alpha list corrected (shell polar moment = 1); run {3/5, 2/3, 1}",
                "Addendum 2: OD B7 identical to B6; B7' added; X3 cross-check added",
                "Addendum 3 (post-run, coordinator after CFG263): OD section F -- does the balance couple an a0-sector energy density?"],
    "frozen_ranking": [
        {"route": "R1 deep-MOND virial with the vacuum", "P": "0.3%", "cost_h": 1.0, "run": True},
        {"route": "R2 two-sided MOND-critical junction", "P": "0.4%", "cost_h": 1.5, "run": True},
        {"route": "R3 two halvings in one equation", "P": "0.2%", "cost_h": 2.0, "run": False, "note": "its equation is inside R1 (Tolman x virial)"},
        {"route": "R4 rho-linear extremum", "P": "0.3%", "cost_h": 3.0, "run": False},
        {"route": "R5 dimensional reduction / pi-free cell", "P": "0.1%", "cost_h": 4.0, "run": False},
        {"route": "OD OWNER-DIRECTED horizon quarter vs bulk 8 pi", "P": "0.2%", "cost_h": 1.5, "run": True},
    ],
    "R1": {"verdict": r1["verdict"], "checks": f"{r1['n_pass']} PASS / {r1['n_fail']} FAIL",
           "mutate": f"{r1m['n_pass']} PASS / {r1m['n_fail']} FAIL",
           "systems": sum(r1["baseline"]["status_counts"].values()), "status_counts": r1["baseline"]["status_counts"],
           "c_free_fixing_k2": r1["baseline"]["c_free_fixing"], "admissible_with_k2": r1["baseline"]["admissible_with_k2"],
           "admissible_target_hits": [h for h in r1["baseline"]["target_hits"] if h[2]],
           "restatement_hits_k2_quarter": r1["baseline"]["target_hits"]},
    "R2": {"verdict": r2["verdict"], "checks": f"{r2['n_pass']} PASS / {r2['n_fail']} FAIL",
           "mutate": f"{r2m['n_pass']} PASS / {r2m['n_fail']} FAIL",
           "target_hits": r2["baseline"]["target_hits"], "pi_free_values": r2["baseline"]["rational_pi0"],
           "M3_piFree_sigma_control": r2m["mutations"]["M3"]},
    "OD": {"label": "OWNER-DIRECTED", "verdict": od["verdict"], "checks": f"{od['n_pass']} PASS / {od['n_fail']} FAIL",
           "mutate": f"{odm['n_pass']} PASS / {odm['n_fail']} FAIL",
           "target_hits": [(t["horizon"], t["budget"]) for t in od["baseline_table"] if t.get("hits_target")],
           "dS_identities": [t["budget"] for t in od["baseline_table"] if t["horizon"] == "HdS" and t["status"] == "identity"],
           "M1_no_thermal_2pi_values": odm["mutations"]["M1 thermal 2 pi removed (T = hbar kappa/(c k_B))"]["pi_free_values"],
           "post_run_CFG263_check (Addendum 3)": od.get("post_run_CFG263_check")},
    "kappa_half": "FITTED (no derivation landed; no independent re-derivation needed or claimed)",
}
with open("results.json", "w") as f:
    json.dump(summary, f, indent=2)
print("results.json written; frozen hash matches record:", summary["frozen_hash_matches_record"])

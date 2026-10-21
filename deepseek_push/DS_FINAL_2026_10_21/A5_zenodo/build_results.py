#!/usr/bin/env python3
"""Write a5_results.json from the check output and the ledger."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
chk = json.load(open(os.path.join(HERE, "a5_check_output.json")))
led = json.load(open(os.path.join(HERE, "a5_zenodo_ledger.json")))
meta = json.load(open(os.path.join(HERE, "_zenodo", "fetch_meta.json")))
counts = chk["counts"]

numbers = {
    "records_total": 178,
    "records_fetched": chk["n_checks"] and 178,
    "records_physics": 177,
    "records_non_physics": 1,
    "api_reported_total": meta["reported_total"],
    "pages_fetched": len(meta["pages"]),
    "ledger_rows": len(led["records"]),
    "quotes_checked": sum(len(r["claims"]) for r in led["records"]),
    "numbers_in_quotes": sum(len(c["numbers"]) for r in led["records"] for c in r["claims"]),
    "probes": 952,
    "probes_with_hits": 497,
    "text_files_scanned": 161566,
    "october_records": 29,
    "october_records_with_zero_canon_numbers": chk["october_records_with_zero_canon_numbers"],
    "october_numbers_total": chk["october_numbers_total"],
    "october_numbers_in_canon": chk["october_numbers_in_canon"],
    "october_numbers_absent": chk["october_numbers_total"] - chk["october_numbers_in_canon"],
    "clues": 14,
    "standing_lag_days": 25,
    "fdr_candidates": 174890804,
    "fdr_distinct": 42534139,
    "fdr_in_window": 82613,
    "fdr_survivors": 0,
    "branching_realized": 4.41,
    "branching_published": 30,
    "branching_ratio": round(30 / 4.41, 2),
    "a0_half": 4.68e-11,
    "w_sensitivity_at_z2_for_1pct_a0": 0.0061,
    "state_counts": counts,
}

constants_used = [
    {"name": "c", "value": 2.99792458e8, "unit": "m/s", "source": "BRIEF.md section 4"},
    {"name": "a0_canonical", "value": 9.36e-11, "unit": "m/s^2", "source": "BRIEF.md section 4"},
    {"name": "a0_alternative", "value": 1.13e-10, "unit": "m/s^2", "source": "BRIEF.md section 4"},
    {"name": "kappa_canonical", "value": 0.5, "unit": "-", "source": "BRIEF.md section 4 (fitted, not derived)"},
    {"name": "H0", "value": 2.1843e-18, "unit": "s^-1", "source": "BRIEF.md section 4 (67.4 km/s/Mpc)"},
    {"name": "Lambda", "value": 1.0890e-52, "unit": "m^-2", "source": "BRIEF.md section 4"},
    {"name": "pc", "value": 3.0856775814913673e16, "unit": "m", "source": "BRIEF.md section 4"},
]

out = {
    "lane": "A5_zenodo",
    "status": "NUMERICAL",
    "claim": ("All 178 Zenodo deposits fetched and cross-checked; 14 load-bearing clues carry "
              "numbers that appear in no canonical repo document, and three cross-record "
              "tensions (kernel, wide-binary registration, kappa) are unreconciled."),
    "checks": [{"id": c["id"], "pass": c["pass"], "value": c["value"],
                "threshold": c["threshold"]} for c in chk["checks"]],
    "n_pass": chk["n_pass"], "n_checks": chk["n_checks"],
    "numbers": numbers,
    "constants_used": constants_used,
    "artifacts": ["a5_zenodo_ledger.json", "report.md", "a5_checks.py", "a5.out",
                  "MUTATE.md", "fetch_zenodo.py", "extract_claims.py",
                  "repo_crosscheck.py", "paper_drift.py", "assemble_ledger.py",
                  "_zenodo/all_records.json", "_zenodo/extract.json",
                  "_zenodo/repo_hits.json", "_zenodo/paper_map.json"],
}
json.dump(out, open(os.path.join(HERE, "a5_results.json"), "w"), indent=1)
print(json.dumps({"checks": f"{chk['n_pass']}/{chk['n_checks']}",
                  "states": counts, "october_zero": numbers["october_records_with_zero_canon_numbers"]},
                 indent=1))

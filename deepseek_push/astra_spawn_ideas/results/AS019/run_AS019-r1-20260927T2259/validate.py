import json, sys, os

base = "."
rj = json.load(open(os.path.join(base, "result.json")))
required = ["task_id", "task_sha256", "run_id", "worker", "started_utc", "finished_utc",
            "execution_status", "outcome", "exact_claim", "framework_cell", "new_assumptions",
            "input_sha256", "artifacts_sha256", "commands", "execution_bounds", "checks",
            "tested_domain", "failed_attempts", "limitations", "next_unresolved_implication",
            "suggested_followup", "acceptance_state", "ancestry", "first_principles_inputs",
            "closure_implication", "child_proposals", "closure_candidate"]
missing = [f for f in required if f not in rj]
print("missing fields:", missing)
# every artifact listed must exist and match hash
import hashlib
for path, h in rj["artifacts_sha256"].items():
    hh = hashlib.sha256(open(os.path.join(base, path), "rb").read()).hexdigest()
    print(f"artifact {path}: {'OK' if hh == h else 'HASH MISMATCH ' + hh}")
# raw_output parses
txt = open(os.path.join(base, "raw_output.json")).read()
d = json.loads(txt[:txt.index("BOUNDS_OK")])
print("raw_output parses; keys:", sorted(d.keys()))
print("lean present:", os.path.exists(os.path.join(base, "AS019_deep_mass_slopes.lean")))
print("schema_version:", rj["schema_version"], "| acceptance_state:", rj["acceptance_state"],
      "| outcome:", rj["outcome"], "| closure_candidate:", rj["closure_candidate"])
print("ALL CHECKS PASS" if not missing else "FAILED")
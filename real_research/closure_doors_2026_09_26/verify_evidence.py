"""Recheck accepted compiler/computation evidence; does not rerun science jobs."""
import datetime, hashlib, json, pathlib, re, subprocess
BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE.parents[1]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
records = [json.loads((BASE / name / "lean_record.json").read_text())
           for name in ("auxiliary", "transport", "causal_completion")]
response = json.loads((BASE / "response_inertia/run_lean_002/results.json").read_text())
assert response["returncode"] == 0 and response["passed"]
records.append({
    "file": response["source"], "sha256": response["source_sha256"],
    "command": response["child_command"],
    "cwd": str(ROOT / "fable_independent_2026/lean_2026"),
    "exit_code": response["returncode"],
    "theorems": [name.rsplit(".", 1)[-1] for name in response["theorems"]],
    "log": str((BASE / "response_inertia/run_lean_002/stdout.txt").relative_to(ROOT))
})
count = 0
for record in records:
    assert record["exit_code"] == 0, record["file"]
    source = ROOT / record["file"]
    assert digest(source) == record["sha256"], (source, "source drift")
    log = ROOT / record["log"]
    if "log_sha256" in record:
        assert digest(log) == record["log_sha256"], (log, "log drift")
    text = log.read_text()
    assert "error:" not in text and "sorryAx" not in text, log
    axioms = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text)
    assert {name.rsplit(".", 1)[-1] for name, _ in axioms} == set(record["theorems"])
    assert len(axioms) == len(record["theorems"]), source
    for _, vals in axioms:
        assert {v.strip() for v in vals.split(",") if v.strip()} <= ALLOWED
    stripped = re.sub(r"/-.*?-/", "", source.read_text(), flags=re.S)
    stripped = re.sub(r"--[^\n]*", "", stripped)
    assert not re.search(r"\b(sorry|admit)\b|^\s*axiom\s", stripped, flags=re.M), source
    record["axioms"] = {name: [v.strip() for v in vals.split(",") if v.strip()]
                        for name, vals in axioms}
    record["log_sha256"] = digest(log)
    count += len(axioms)
spec = ROOT / "qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md"
assert digest(spec) == "be0400679673b0bb9463dd399ab8e05b8889659ad97736e1b9926276887361c2"
manifest = {
    "verified_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope": "Recorded compiler evidence and hashes, not a fresh compiler invocation or physics proof",
    "theorem_count": count, "allowed_axioms": sorted(ALLOWED),
    "spec_sha256": digest(spec), "certificates": records,
    "repository_head_at_validation": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
}
(BASE / "lean_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("Lean records: %d files, %d theorems; unchanged sources, exits zero, allowed axioms only." % (len(records), count))
runs = ["auxiliary/run2", "action_consistency/run1", "empirical/run1",
        "environment_gate/run_verified", "transport/run_002", "transport/fisher_run_001",
        "response_inertia/run_001", "response_inertia/run_degenerate_002",
        "response_inertia/run_rankone_001", "response_inertia/run_lean_002",
        "causal_completion/run1", "auxiliary/lapse_run1"]
validator = pathlib.Path.home() / ".codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py"
checks = []
for run in runs:
    path = BASE / run / "manifest.json"
    result = subprocess.run(["python3", str(validator), str(path), "--root", str(ROOT)],
                            text=True, capture_output=True)
    checks.append({"manifest": str(path.relative_to(ROOT)),
                   "validator_exit": result.returncode,
                   "manifest_sha256": digest(path) if path.exists() else None,
                   "stdout": result.stdout, "stderr": result.stderr})
(BASE / "computation_validation.json").write_text(json.dumps(checks, indent=2) + "\n")
assert all(c["validator_exit"] == 0 for c in checks), checks
print("Validated %d accepted run manifests against current source and output hashes." % len(checks))
print("Canonical thirteen-requirement specification unchanged.")


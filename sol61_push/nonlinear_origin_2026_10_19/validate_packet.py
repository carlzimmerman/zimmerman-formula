#!/usr/bin/env python3
"""Validate saved research bytes and four current evidence records; no rerun."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

packet = Path(__file__).resolve().parent
root = packet.parents[1]
checkpoint = json.loads((packet / "checkpoint.json").read_text())
errors = []

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for record in checkpoint["artifacts"] + checkpoint["external_inputs"]:
    path = (root / record["path"]).resolve()
    if root not in path.parents:
        errors.append("path escapes root: " + record["path"])
    elif not path.is_file():
        errors.append("missing: " + record["path"])
    elif digest(path) != record["sha256"]:
        errors.append("bytes changed: " + record["path"])

validator_path = Path(checkpoint["evidence_validator"]["path"])
if digest(validator_path) != checkpoint["evidence_validator"]["sha256"]:
    errors.append("installed evidence validator changed")
spec = importlib.util.spec_from_file_location("mathbox_validator", validator_path)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
evidence = []
for name in checkpoint["current_manifests"]:
    path = root / name
    data = json.loads(path.read_text())
    problems = validator.validate(data, root=root, manifest_path=path)
    if data["run"]["status"] != "completed":
        problems.append("current run did not complete")
    errors.extend(name + ": " + p for p in problems)
    evidence.append({"manifest": name, "status": data["run"]["status"],
                     "runtime_seconds": data["run"]["runtime_seconds"],
                     "validation_errors": problems})

for relation in checkpoint["reviewed_notes"]:
    note = root / relation["note"]
    review = (root / relation["review"]).read_text()
    if digest(note) not in review:
        errors.append("review does not pin current note: " + relation["note"])

report = {
    "packet_id": checkpoint["packet_id"],
    "status": "passed" if not errors else "failed",
    "artifact_count": len(checkpoint["artifacts"]),
    "external_input_count": len(checkpoint["external_inputs"]),
    "current_evidence": evidence,
    "reviewed_note_relations": len(checkpoint["reviewed_notes"]),
    "errors": errors,
    "scope": "Byte/provenance validation only. No scientific experiment was repeated. Mathematical claims retain their scoped reviews; original prediction target is OPEN.",
}
(packet / "VALIDATION.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(bool(errors))

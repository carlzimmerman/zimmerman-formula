"""Validate recorded Lean runs and emit a hash-bound accepted manifest.

This reads compiler evidence; it does not rerun the compiler. Reproduction
commands for every run are recorded in the resulting manifest.
"""
import datetime
import hashlib
import json
import pathlib
import re
import subprocess

OUT = pathlib.Path(__file__).resolve().parent
ROOT = OUT.parents[2]
PROJECT = ROOT / "fable_independent_2026/lean_2026"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


records = json.loads((OUT / "existing_manifest.json").read_text())
for name in ["XC1_strong_coupling_certificates", "ClosureResume20260926"]:
    records.append(json.loads((OUT / (name + "_record.json")).read_text()))

total = 0
for record in records:
    source = ROOT / record["file"]
    assert record["exit_code"] == 0, record["file"]
    assert digest(source) == record["sha256"], (record["file"], "source changed")
    evidence = record.get("axioms_audit", record)
    assert evidence["exit_code"] == 0
    log = ROOT / evidence["log"]
    text = log.read_text()
    assert "error:" not in text and "sorryAx" not in text, log
    axioms = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text)
    assert len(axioms) == len(record["theorems"]), record["file"]
    assert {name.rsplit(".", 1)[-1] for name, _ in axioms} == set(record["theorems"])
    record["axioms"] = {
        name: [item.strip() for item in names.split(",") if item.strip()]
        for name, names in axioms
    }
    assert all(set(names) <= ALLOWED for names in record["axioms"].values())
    code = re.sub(r"/-.*?-/", "", source.read_text(), flags=re.S)
    code = re.sub(r"--[^\n]*", "", code)
    assert not re.search(r"\b(sorry|admit)\b|^\s*axiom\s", code, flags=re.M), source
    record["log_sha256"] = digest(ROOT / record["log"])
    record["axioms_log_sha256"] = digest(log)
    if "axioms_audit" in record:
        assert digest(ROOT / evidence["file"]) == evidence["sha256"]
    total += len(axioms)

provenance = {}
for name, command in [
    ("lean_version", ["lake", "env", "lean", "--version"]),
    ("lake_version", ["lake", "--version"]),
    ("repository_head_final", ["git", "rev-parse", "HEAD"]),
    ("mathlib_head", ["git", "-C", str(PROJECT / ".lake/packages/mathlib"), "rev-parse", "HEAD"]),
]:
    result = subprocess.run(command, cwd=PROJECT, text=True, capture_output=True, check=True)
    provenance[name] = {"command": command, "exit_code": result.returncode, "output": result.stdout.strip()}
for name in ["lean-toolchain", "lakefile.toml", "lake-manifest.json"]:
    provenance[name] = {"sha256": digest(PROJECT / name)}
provenance["repository_head_initial"] = "4e16ccf585f6fcc775a2f9d62ac30d329212e0af"
provenance["head_reconciliation"] = (
    "Another task advanced HEAD during this review. Existing source hashes were "
    "rechecked; the newly landed XC1 source was separately compiled and audited."
)
manifest = {
    "verified_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "provenance": provenance,
    "theorem_count": total,
    "allowed_axioms": sorted(ALLOWED),
    "certificates": records,
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Verified {len(records)} unchanged source hashes, {total} theorem axiom reports, all exits zero.")
print("No admitted proof, declared source axiom, sorryAx, or unexpected axiom in accepted evidence.")

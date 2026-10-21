"""Read-only provenance checks; writes only this packet's verification record.

This does not check the mathematical proofs. Their separate audits are pinned
by the checkpoint and packet inventory. No scientific simulation is run here.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PACKET = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


old = []
for name in ("final_closure_push_2026_10_20", "novel_closure_routes_2026_10_20"):
    folder = ROOT / "reviews" / name
    index = folder / "PACKET_SHA256.json"
    data = json.loads(index.read_text())
    mismatches = [p for p, expected in data["files"].items()
                  if not (folder / p).is_file() or sha(folder / p) != expected]
    old.append({"packet": name, "inventory_sha256": sha(index),
                "files_checked": len(data["files"]), "mismatches": mismatches})

sources = {}
conflicts = []
for route in ("scalar", "modes", "relaxation"):
    path = PACKET / route / "source_hashes.json"
    data = json.loads(path.read_text())
    for entry in data["sources"]:
        p, expected = entry["path"], entry["sha256"]
        if p in sources and sources[p]["expected"] != expected:
            conflicts.append(p)
        actual = sha(ROOT / p) if (ROOT / p).is_file() else None
        sources[p] = {"expected": expected, "actual": actual,
                      "unchanged": actual == expected}

run_dir = PACKET / "scalar" / "run_002"
run = json.loads((run_dir / "manifest.json").read_text())
result = json.loads((run_dir / "results.json").read_text())
runtime_hashes = []
for entry in run["outputs"]:
    runtime_hashes.append({"path": entry["path"],
                           "matches": sha(ROOT / entry["path"]) == entry["sha256"]})
for entry in run["input_artifacts"]:
    runtime_hashes.append({"path": entry["path"],
                           "matches": sha(ROOT / entry["path"]) == entry["sha256"]
                           == entry["sha256_after"]})

proofs = [
    "TARGET.md", "README.md", "CONVERSION_JOIN.md", "NOVELTY_DELTA.md",
    "scalar/RESULT.md", "modes/RESULT.md", "modes/EXCHANGE_AUDIT.md",
    "relaxation/RESULT.md", "relaxation/SUPPORTED_CONTINUATION.md",
    "relaxation/BARRIER_PROOF.md", "relaxation/BOUNDS.md",
    "audit/RELAXATION_AUDIT.md",
]
missing = [p for p in proofs if not (PACKET / p).is_file()]
audit_path = PACKET / "audit/provenance.json"
audit_data = json.loads(audit_path.read_text())
reviewed = audit_data["reviewed_files"]
review_mismatches = [p for p, expected in reviewed.items()
                     if not (PACKET / p).is_file() or sha(PACKET / p) != expected]
required_reviewed = {
    "scalar/RESULT.md", "CONVERSION_JOIN.md", "relaxation/RESULT.md",
    "relaxation/SUPPORTED_CONTINUATION.md", "relaxation/BARRIER_PROOF.md",
    "relaxation/BOUNDS.md",
}
checks = {
    "earlier_packets_unchanged": all(not p["mismatches"] for p in old),
    "all_route_input_bytes_unchanged": all(p["unchanged"] for p in sources.values()),
    "no_conflicting_source_pins": not conflicts,
    "symbolic_run_completed": run["run"]["status"] == "completed"
        and run["run"]["exit_status"] == 0,
    "symbolic_artifact_hashes_match": all(p["matches"] for p in runtime_hashes),
    "observed_symbolic_rss_under_one_GB": result["observed_peak_rss_bytes"] < 1_000_000_000,
    "declared_proof_and_audit_files_exist": not missing,
    "independently_reviewed_proof_hashes_match": not review_mismatches,
    "required_independent_proof_coverage_recorded": required_reviewed.issubset(reviewed),
}
record = {
    "checkpoint": "existing-attraction-2026-10-20",
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "observed_head": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
    "purpose": "Byte provenance and bounded-run validation; not a proof checker",
    "checks": checks,
    "earlier_packets": old,
    "unique_sources_checked": len(sources),
    "sources": sources,
    "conflicting_pins": conflicts,
    "symbolic_run": {"manifest_sha256": sha(run_dir / "manifest.json"),
                     "result_sha256": sha(run_dir / "results.json"),
                     "observed_peak_rss_bytes": result["observed_peak_rss_bytes"],
                     "runtime_seconds": run["run"]["runtime_seconds"],
                     "largest_matrix_dimension": 3,
                     "parameter_scans": 0,
                     "artifact_hash_checks": runtime_hashes},
    "failed_launch_preserved": (PACKET / "scalar/run_001/manifest.json").is_file(),
    "missing_declared_files": missing,
    "independent_audit_provenance_sha256": sha(audit_path),
    "reviewed_proof_mismatches": review_mismatches,
    "proof_hashes": {p: sha(PACKET / p) for p in proofs if (PACKET / p).is_file()},
    "interpretation": "Exact analytic derivations and separately scoped independent review support conditional model statements; no physical memory, lifetime, observational pass, or global novelty is certified.",
}
(PACKET / "VERIFICATION.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"checks": checks, "old_packet_files": sum(x["files_checked"] for x in old),
                  "sources": len(sources), "observed_head": record["observed_head"]}, indent=2))
if not all(checks.values()):
    raise SystemExit(1)

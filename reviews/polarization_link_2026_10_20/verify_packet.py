"""Verify source/proof freshness and prior records, not mathematical truth."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


prior = []
for name in ("final_closure_push_2026_10_20", "novel_closure_routes_2026_10_20",
             "attraction_from_existing_2026_10_20", "conversion_dynamics_2026_10_20"):
    folder = ROOT / "reviews" / name
    index = folder / "PACKET_SHA256.json"
    entries = json.loads(index.read_text())["files"]
    bad = [p for p, expected in entries.items()
           if not (folder / p).is_file() or sha(folder / p) != expected]
    prior.append({"packet": name, "inventory_sha256": sha(index),
                  "files_checked": len(entries), "mismatches": bad})

audit_path = PACKET / "audit/provenance.json"
audit = json.loads(audit_path.read_text())
required = {"multipoles/RESULT.md", "phases/RESULT.md", "selector/RESULT.md",
            "support/RESULT.md", "CANONICAL_MEMORY.md", "GRAVITY_BRIDGE.md"}
review_bad = [p for p, expected in audit["reviewed_files"].items()
              if not (PACKET / p).is_file() or sha(PACKET / p) != expected]
sources = {}
conflicts = []


def add_pin(path, expected):
    if path in sources and sources[path]["expected"] != expected:
        conflicts.append(path)
    actual = sha(ROOT / path) if (ROOT / path).is_file() else None
    sources[path] = {"expected": expected, "actual": actual,
                     "unchanged": actual == expected}


for route in ("multipoles", "phases", "selector", "support"):
    data = json.loads((PACKET / route / "source_hashes.json").read_text())
    for entry in data["sources"]:
        add_pin(entry["path"], entry["sha256"])
for path, expected in audit["source_files"].items():
    add_pin(path, expected)
# Root derivations use the unchanged canonical action and reciprocal energy.
old_verification = json.loads((ROOT / "reviews/conversion_dynamics_2026_10_20/VERIFICATION.json").read_text())
for path in ("campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md",
             "reviews/final_closure_push_2026_10_20/reciprocity/SOURCE_RESPONSE.md"):
    add_pin(path, old_verification["sources"][path]["expected"])

report = PACKET / audit["audit_report"]["path"]
checks = {
    "earlier_packets_unchanged": all(not x["mismatches"] for x in prior),
    "source_and_route_input_bytes_unchanged": all(x["unchanged"] for x in sources.values()),
    "no_conflicting_source_pins": not conflicts,
    "six_required_proofs_reviewed": required.issubset(audit["reviewed_files"]),
    "reviewed_proof_bytes_unchanged": not review_bad,
    "audit_report_digest_matches": sha(report) == audit["audit_report"]["sha256"],
    "root_records_present": all((PACKET / p).is_file() for p in
        ("TARGET.md", "README.md", "NEXT.md", "NOVELTY_DELTA.md")),
}
record = {
    "checkpoint": "polarization-link-2026-10-20",
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "observed_head": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
    "purpose": "Byte freshness and prior-record preservation; not a proof/physics validator",
    "checks": checks,
    "earlier_packets": prior,
    "earlier_packet_file_count": sum(x["files_checked"] for x in prior),
    "unique_source_and_route_input_count": len(sources),
    "sources": sources,
    "conflicting_pins": conflicts,
    "reviewed_files": audit["reviewed_files"],
    "review_mismatches": review_bad,
    "independent_audit_provenance_sha256": sha(audit_path),
    "independent_report_sha256": sha(report),
    "root_file_hashes": {p: sha(PACKET / p) for p in
        ("TARGET.md", "README.md", "NEXT.md", "NOVELTY_DELTA.md", "verify_packet.py")},
    "scientific_runs": 0,
    "symbolic_package_runs": 0,
    "parameter_scans": 0,
    "interpretation": "Six analytic notes are independently reconstructed in their explicit regimes. No physical response switch, retention lifetime, empirical pass or global novelty is certified.",
}
(PACKET / "VERIFICATION.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"checks": checks, "prior_files": record["earlier_packet_file_count"],
                  "source_and_route_inputs": len(sources), "observed_head": record["observed_head"]}, indent=2))
if not all(checks.values()):
    raise SystemExit(1)

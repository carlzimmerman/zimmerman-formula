"""Provenance checks only; this is not a mathematical proof checker."""
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
             "attraction_from_existing_2026_10_20"):
    folder = ROOT / "reviews" / name
    index = folder / "PACKET_SHA256.json"
    data = json.loads(index.read_text())
    bad = [p for p, expected in data["files"].items()
           if not (folder / p).is_file() or sha(folder / p) != expected]
    prior.append({"packet": name, "inventory_sha256": sha(index),
                  "files_checked": len(data["files"]), "mismatches": bad})

audit_path = PACKET / "audit/provenance.json"
audit = json.loads(audit_path.read_text())
review_bad = [p for p, expected in audit["reviewed_files"].items()
              if not (PACKET / p).is_file() or sha(PACKET / p) != expected]
required = {"radial/RESULT.md", "cubic/RESULT.md", "collisions/RESULT.md",
            "collisions/BORN_CAPTURE.md", "HOST_RECEIVER.md", "RATE_STATE_DEPENDENCE.md"}

sources = {}
conflicts = []


def add_pin(path, expected):
    if path in sources and sources[path]["expected"] != expected:
        conflicts.append(path)
    actual = sha(ROOT / path) if (ROOT / path).is_file() else None
    sources[path] = {"expected": expected, "actual": actual,
                     "unchanged": actual == expected}


for route in ("radial", "cubic", "collisions"):
    data = json.loads((PACKET / route / "source_hashes.json").read_text())
    for entry in data["sources"]:
        add_pin(entry["path"], entry["sha256"])
for path, expected in audit["source_files"].items():
    add_pin(path, expected)

local_artifacts = []
for filename in ("radial/artifact_hashes.json", "cubic/ARTIFACTS.json",
                 "collisions/ARTIFACTS.json"):
    if (PACKET / filename).is_file():
        local_artifacts.append({"path": filename, "sha256": sha(PACKET / filename)})

checks = {
    "prior_packet_files_unchanged": all(not x["mismatches"] for x in prior),
    "all_route_and_audit_sources_unchanged": all(x["unchanged"] for x in sources.values()),
    "no_conflicting_source_pins": not conflicts,
    "six_required_proofs_independently_reviewed": required.issubset(audit["reviewed_files"]),
    "reviewed_proof_bytes_unchanged": not review_bad,
    "audit_report_digest_matches": sha(PACKET / "audit/RESULT.md") == audit["audit_report_sha256"],
    "root_deliverables_present": all((PACKET / x).is_file()
        for x in ("TARGET.md", "README.md", "NEXT.md", "NOVELTY_DELTA.md")),
}
record = {
    "checkpoint": "conversion-dynamics-2026-10-20",
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "observed_head": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
    "purpose": "Source/artifact freshness and preservation; not a proof or physics validator",
    "checks": checks,
    "earlier_packets": prior,
    "earlier_packet_file_count": sum(x["files_checked"] for x in prior),
    "unique_source_count": len(sources),
    "sources": sources,
    "conflicting_pins": conflicts,
    "independent_provenance_sha256": sha(audit_path),
    "audit_report_sha256": sha(PACKET / "audit/RESULT.md"),
    "reviewed_files": audit["reviewed_files"],
    "review_mismatches": review_bad,
    "local_artifact_inventory_pins": local_artifacts,
    "root_file_hashes": {x: sha(PACKET / x) for x in
        ("TARGET.md", "README.md", "NEXT.md", "NOVELTY_DELTA.md", "verify_packet.py")},
    "scientific_runs": 0,
    "symbolic_package_runs": 0,
    "parameter_scans": 0,
    "interpretation": "Analytic exact and conditional statements are reviewed within their recorded regimes. No actual canonical memory rate, astrophysical lifetime, continuum scattering theorem, empirical pass or global novelty is certified.",
}
(PACKET / "VERIFICATION.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({"checks": checks, "old_packet_files": record["earlier_packet_file_count"],
                  "source_files": len(sources), "observed_head": record["observed_head"]}, indent=2))
if not all(checks.values()):
    raise SystemExit(1)

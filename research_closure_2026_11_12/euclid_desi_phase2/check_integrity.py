"""Verify archived execution bytes; this does not validate scientific claims."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


runs = []
issues = []
historical_sources = []
for manifest in sorted(ROOT.rglob("manifest.json")):
    record = json.loads(manifest.read_text())
    base = manifest.parent.parent
    count = 0
    for kind in ("input_artifacts", "outputs"):
        for item in record.get(kind, []):
            path = Path(item["path"])
            path = path if path.is_absolute() else base / path
            candidates = [path]
            if kind == "input_artifacts":
                candidates.extend([
                    manifest.parent / (Path(item["path"]).name + ".snapshot"),
                    base / "portal_checks_failed_run01.py",
                ])
            matching = [p for p in candidates if p.is_file() and digest(p) == item["sha256"]]
            if not matching:
                issues.append({"manifest": str(manifest.relative_to(ROOT)),
                               "kind": kind, "artifact": item["path"]})
            elif matching[0] != path:
                historical_sources.append({"manifest": str(manifest.relative_to(ROOT)),
                                           "artifact": item["path"],
                                           "resolved_snapshot": str(matching[0].relative_to(ROOT))})
            count += 1
    runs.append({"manifest": str(manifest.relative_to(ROOT)),
                 "status": record.get("run", {}).get("status"),
                 "artifact_references_checked": count})

snapshots = json.loads((ROOT / "theory/source_snapshot_map.json").read_text())["files"]
for item in snapshots:
    path = ROOT / "theory" / item["snapshot"]
    if not path.is_file() or digest(path) != item["sha256"]:
        issues.append({"archived_source": item["snapshot"]})

result = {
    "assertion": "Historical manifest input/output hashes resolve to preserved bytes, including explicit failed-run source snapshots.",
    "status_counts": dict(collections.Counter(row["status"] for row in runs)),
    "artifact_references_checked": sum(row["artifact_references_checked"] for row in runs),
    "additional_theory_source_snapshots_checked": len(snapshots),
    "runs": runs,
    "historical_source_resolutions": historical_sources,
    "issues": issues,
    "non_claim": "Hash integrity and execution status do not establish mathematical correctness, scientific novelty, observation agreement or physical viability.",
}
(ROOT / "INTEGRITY_AUDIT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({key: result[key] for key in ("status_counts", "artifact_references_checked", "additional_theory_source_snapshots_checked", "issues")}))
raise SystemExit(bool(issues))

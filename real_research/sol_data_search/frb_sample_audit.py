#!/usr/bin/env python3
"""Audit the published Sharma et al. FRB sample flags without fitting a model."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path


SOURCE_COMMIT = "6651975039b25c2ac6853527699bb6d54722f5a0"
CSV_SHA256 = "ff14bf90d455a4bcf9c5b98a7ea533c299ec78a12ac4428246d4bcffa0ef83c2"
HERE = Path(__file__).resolve().parent


def summarize(rows: list[dict[str, str]]) -> dict:
    z = [float(r["z_sample"]) for r in rows]
    dm = [float(r["DMexgal"]) for r in rows]
    return {
        "n": len(rows),
        "z_min": min(z),
        "z_median": statistics.median(z),
        "z_max": max(z),
        "DMexgal_median": statistics.median(dm),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_path", type=Path)
    p.add_argument("--output", type=Path, default=HERE / "frb_sample_audit_result.json")
    args = p.parse_args()
    raw = args.csv_path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != CSV_SHA256:
        raise SystemExit(f"Expected pinned CSV SHA-256 {CSV_SHA256}; found {sha}")
    with args.csv_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    counts = Counter(r["sharma_sample"] for r in rows)
    assert len(rows) == 127 and len({r["FRB"] for r in rows}) == 127
    assert counts == {"yes": 92, "unclear": 22, "no": 13}
    assert all("Arcmin-localization" in r["sharma_reason_for_excluding/notes"]
               for r in rows if r["sharma_sample"] == "unclear")
    groups = {key: summarize([r for r in rows if r["sharma_sample"] == key])
              for key in ("yes", "unclear", "no")}
    out = {
        "source": "https://github.com/krittisharma/dmz_spk_sharma2026",
        "commit": SOURCE_COMMIT,
        "csv_sha256": sha,
        "total_rows": len(rows),
        "unique_FRB_ids": len({r["FRB"] for r in rows}),
        "sharma_sample_counts": dict(counts),
        "fiducial_n_yes": counts["yes"],
        "extended_n_yes_or_unclear": counts["yes"] + counts["unclear"],
        "unclear_share_of_extended": counts["unclear"] / (counts["yes"] + counts["unclear"]),
        "all_unclear_rows_marked_arcmin_localization": True,
        "groups": groups,
        "scope": "Catalog and selection audit only; no FRB likelihood or feedback posterior fit.",
    }
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

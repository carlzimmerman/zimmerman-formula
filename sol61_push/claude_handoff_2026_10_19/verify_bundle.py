#!/usr/bin/env python3
"""Verify the portable Claude research snapshot without installed Codex tools."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extract", type=Path,
                        help="extract after verification into a new directory")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / "CONTENTS.json").read_text())
    compressed = (here / manifest["archive"]).read_bytes()
    assert sha(compressed) == manifest["archive_sha256"], "archive hash differs"
    expected = {r["path"]: r for r in manifest["files"]}
    assert len(expected) == manifest["file_count"], "duplicate manifest paths"
    blobs = {}
    with tarfile.open(fileobj=io.BytesIO(compressed), mode="r:gz") as archive:
        for member in archive.getmembers():
            path = PurePosixPath(member.name)
            assert member.isfile(), "nonregular archive member: " + member.name
            assert not path.is_absolute() and ".." not in path.parts
            assert member.name not in blobs, "duplicate archive member"
            data = archive.extractfile(member).read()
            record = expected[member.name]
            assert len(data) == record["bytes"], member.name
            assert sha(data) == record["sha256"], member.name
            blobs[member.name] = data
    assert set(blobs) == set(expected), "archive file set differs"

    def record_bytes(record):
        assert sha(blobs[record["path"]]) == record["sha256"], record["path"]

    evidence = []
    for name in manifest["current_manifests"]:
        run = json.loads(blobs[name])
        assert run["schema_version"] == 2
        assert run["run"]["status"] == "completed", name
        assert run["run"]["exit_status"] == 0, name
        for record in run["input_artifacts"] + run["outputs"]:
            record_bytes(record)
            if "sha256_after" in record:
                assert record["sha256_after"] == record["sha256"], name
        evidence.append({"manifest": name, "status": "completed",
                         "input_output_hashes": "passed"})

    checkpoint = json.loads(blobs[
        "sol61_push/nonlinear_origin_2026_10_19/checkpoint.json"])
    for record in checkpoint["artifacts"] + checkpoint["external_inputs"]:
        record_bytes(record)
    for relation in checkpoint["reviewed_notes"]:
        digest = sha(blobs[relation["note"]])
        assert digest in blobs[relation["review"]].decode(), relation["note"]

    if args.extract:
        destination = args.extract.expanduser().resolve()
        destination.mkdir(parents=True, exist_ok=False)
        for name, data in blobs.items():
            path = destination.joinpath(*PurePosixPath(name).parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as output:
                output.write(data)

    print(json.dumps({
        "status": "passed", "files": len(blobs),
        "archive_sha256": manifest["archive_sha256"],
        "current_evidence": evidence,
        "reviewed_note_relations": len(checkpoint["reviewed_notes"]),
        "extracted_to": str(args.extract.resolve()) if args.extract else None,
        "scope": "Byte/provenance checks only; no scientific rerun, full Mathbox schema validation, or theorem certification.",
        "original_prediction_target": "open",
    }, indent=2))


if __name__ == "__main__":
    main()

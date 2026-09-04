#!/usr/bin/env python3
"""Strict byte-level verifier for a Mathbox-style computation manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Any


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ManifestVerificationError(RuntimeError):
    """A manifest is unsafe, malformed, stale, or not reproducible."""


def _reject_nonfinite(value: str) -> None:
    raise ManifestVerificationError(f"non-finite JSON constant is forbidden: {value}")


def load_strict_json(path: Path) -> dict[str, Any]:
    try:
        parsed = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_nonfinite,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ManifestVerificationError(f"cannot strict-parse {path}: {error}") from error
    if not isinstance(parsed, dict):
        raise ManifestVerificationError("manifest root must be a JSON object")
    return parsed


def _safe_relative_path(raw_path: Any) -> PurePosixPath:
    if not isinstance(raw_path, str) or not raw_path:
        raise ManifestVerificationError("each declared path must be a nonempty string")
    path = PurePosixPath(raw_path)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ManifestVerificationError(f"unsafe declared path: {raw_path!r}")
    return path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _is_tracked(repository_root: Path, relative_path: str) -> bool:
    completed = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", relative_path],
        cwd=repository_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def verify_manifest_data(
    manifest: dict[str, Any],
    *,
    repository_root: Path,
    require_tracked: bool,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    declared: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for category in ("sources", "outputs"):
        entries = manifest.get(category)
        if not isinstance(entries, list) or not entries:
            raise ManifestVerificationError(f"{category} must be a nonempty list")
        for entry in entries:
            if not isinstance(entry, dict):
                raise ManifestVerificationError(f"{category} entry must be an object")
            relative = _safe_relative_path(entry.get("path")).as_posix()
            expected = entry.get("sha256")
            if not isinstance(expected, str) or SHA256_RE.fullmatch(expected) is None:
                raise ManifestVerificationError(f"invalid SHA-256 for {relative}")
            if relative in seen:
                raise ManifestVerificationError(f"duplicate declared path: {relative}")
            seen.add(relative)
            declared.append((category, relative, expected))

    verified = []
    for category, relative, expected in declared:
        absolute = repository_root / relative
        try:
            resolved = absolute.resolve(strict=True)
        except OSError as error:
            raise ManifestVerificationError(f"missing declared file: {relative}") from error
        try:
            resolved.relative_to(repository_root)
        except ValueError as error:
            raise ManifestVerificationError(
                f"declared file escapes repository root: {relative}"
            ) from error
        if absolute.is_symlink() or not resolved.is_file():
            raise ManifestVerificationError(
                f"declared path is not a regular nonsymlink file: {relative}"
            )
        if require_tracked and not _is_tracked(repository_root, relative):
            raise ManifestVerificationError(f"declared file is not git-tracked: {relative}")
        actual = _sha256(resolved)
        if actual != expected:
            raise ManifestVerificationError(
                f"SHA-256 mismatch for {relative}: expected {expected}, got {actual}"
            )
        verified.append({"category": category, "path": relative, "sha256": actual})

    return {
        "status": "PASS",
        "files_declared": len(declared),
        "files_verified": len(verified),
        "require_tracked": require_tracked,
        "verified": verified,
    }


def verify_manifest(
    manifest_path: Path,
    *,
    repository_root: Path,
    require_tracked: bool,
) -> dict[str, Any]:
    return verify_manifest_data(
        load_strict_json(manifest_path),
        repository_root=repository_root,
        require_tracked=require_tracked,
    )


def _repository_root() -> Path:
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ManifestVerificationError("cannot locate git repository root")
    return Path(completed.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--require-tracked",
        action="store_true",
        help="also require every declared source/output to exist in the git index",
    )
    arguments = parser.parse_args()
    try:
        result = verify_manifest(
            arguments.manifest,
            repository_root=_repository_root(),
            require_tracked=arguments.require_tracked,
        )
    except ManifestVerificationError as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

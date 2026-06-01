#!/usr/bin/env python3
"""
util_04_zenodo_publisher.py

Zenodo Publication Preparation
==============================

Prepares the validated pipeline for Zenodo upload to obtain a DOI.

This script:
1. Creates a zip archive of the pipeline
2. Validates the metadata
3. Provides instructions for manual upload or API upload

Author: Carl Zimmerman
Framework: Zimmerman Unified Geometry Framework (ZUGF)
License: AGPL v3.0

DISCLAIMER: This is theoretical and computational research only.
No therapeutic claims are made or implied.
"""

import json
import zipfile
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import List

# Files to include in the Zenodo archive
INCLUDE_PATTERNS = [
    '*.py',
    '*.md',
    '*.json',
    '*.txt',   # SOW documents for CRO synthesis
    '*.png',   # MS spectrum plots
    'LICENSE',
    'DISCLAIMER.md',
]

# Files/directories to exclude
EXCLUDE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    '.git',
    'pdb_cache',  # Too large for Zenodo
    'zenodo_upload',  # Don't include previous archives
    '*.output',
]


def should_include(path: Path, base_dir: Path) -> bool:
    """Check if a file should be included in the archive."""
    rel_path = str(path.relative_to(base_dir))

    # Check exclusions
    for pattern in EXCLUDE_PATTERNS:
        if pattern in rel_path:
            return False

    # Check inclusions
    for pattern in INCLUDE_PATTERNS:
        if pattern.startswith('*'):
            if path.suffix == pattern[1:]:
                return True
        elif path.name == pattern:
            return True

    return False


def calculate_sha256(filepath: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            sha256.update(block)
    return sha256.hexdigest()


def create_zenodo_archive(base_dir: Path, output_dir: Path) -> Path:
    """Create a zip archive for Zenodo upload."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_name = f'ZUGF_validated_pipeline_{timestamp}.zip'
    archive_path = output_dir / archive_name

    print(f"\n📦 Creating Zenodo archive: {archive_name}")

    files_included = []
    total_size = 0

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(base_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'pdb_cache']]

            for file in files:
                filepath = Path(root) / file

                if should_include(filepath, base_dir):
                    arcname = filepath.relative_to(base_dir)
                    zf.write(filepath, arcname)
                    files_included.append(str(arcname))
                    total_size += filepath.stat().st_size

    print(f"   Files included: {len(files_included)}")
    print(f"   Total size: {total_size / 1024 / 1024:.2f} MB")
    print(f"   Archive: {archive_path}")

    return archive_path


def create_file_manifest(base_dir: Path, output_path: Path) -> None:
    """Create a manifest of all files with checksums."""
    manifest = {
        'timestamp': datetime.now().isoformat(),
        'description': 'Zimmerman Unified Geometry Framework - Validated Pipeline',
        'files': []
    }

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'pdb_cache']]

        for file in files:
            filepath = Path(root) / file
            if should_include(filepath, base_dir):
                manifest['files'].append({
                    'path': str(filepath.relative_to(base_dir)),
                    'size_bytes': filepath.stat().st_size,
                    'sha256': calculate_sha256(filepath)
                })

    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"   Manifest: {output_path}")


def main():
    """Main execution."""
    print("=" * 70)
    print("ZENODO PUBLICATION PREPARATION")
    print("Zimmerman Unified Geometry Framework")
    print("=" * 70)

    print("""
   ⚠️  IMPORTANT DISCLAIMERS ⚠️
   ────────────────────────────
   This is THEORETICAL AND COMPUTATIONAL research only.
   NO THERAPEUTIC CLAIMS are made or implied.
   All molecular sequences require EXPERIMENTAL VALIDATION.
   The Z² hypothesis REMAINS UNPROVEN.
   This work has NOT been independently validated.
""")

    base_dir = Path(__file__).parent
    output_dir = base_dir / 'zenodo_upload'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create archive
    archive_path = create_zenodo_archive(base_dir, output_dir)

    # Create manifest
    manifest_path = output_dir / 'file_manifest.json'
    create_file_manifest(base_dir, manifest_path)

    # Calculate archive checksum
    archive_sha256 = calculate_sha256(archive_path)
    print(f"   Archive SHA256: {archive_sha256}")

    # Load and display metadata
    metadata_path = base_dir / 'zenodo_metadata_validated_pipeline.json'
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)
        print(f"\n📄 Metadata loaded from: {metadata_path}")
        print(f"   Title: {metadata['metadata']['title']}")
        print(f"   Version: {metadata['metadata']['version']}")

    # Instructions
    print("\n" + "=" * 70)
    print("UPLOAD INSTRUCTIONS")
    print("=" * 70)
    print(f"""
   OPTION 1: Manual Upload (Recommended)
   ──────────────────────────────────────
   1. Go to https://zenodo.org/deposit/new
   2. Upload: {archive_path}
   3. Copy metadata from: {metadata_path}
   4. Review and publish

   OPTION 2: API Upload
   ────────────────────
   1. Get your Zenodo access token from:
      https://zenodo.org/account/settings/applications/
   2. Set environment variable:
      export ZENODO_TOKEN=your_token_here
   3. Run the API upload script (requires 'requests' package)

   FILES READY FOR UPLOAD:
   - Archive: {archive_path}
   - Metadata: {metadata_path}
   - Manifest: {manifest_path}

   AFTER UPLOAD:
   - You will receive a DOI (e.g., 10.5281/zenodo.XXXXXXX)
   - Update PROJECT_MANIFEST.md with the new DOI
   - The DOI provides permanent citation for this version
""")

    # Save upload info
    upload_info = {
        'timestamp': datetime.now().isoformat(),
        'archive': str(archive_path),
        'archive_sha256': archive_sha256,
        'metadata': str(metadata_path),
        'manifest': str(manifest_path),
        'disclaimers': [
            "This is theoretical and computational research only",
            "No therapeutic claims are made or implied",
            "All molecular sequences require experimental validation",
            "The Z² hypothesis remains unproven",
            "This work has not been independently validated"
        ]
    }

    info_path = output_dir / 'upload_info.json'
    with open(info_path, 'w') as f:
        json.dump(upload_info, f, indent=2)

    print(f"\n📄 Upload info saved to: {info_path}")
    print("=" * 70)

    return archive_path


if __name__ == '__main__':
    archive = main()

#!/usr/bin/env python3
"""
util_05_zenodo_api_upload.py

Zenodo API Upload Script
========================

Uploads the ZUGF validated pipeline directly to Zenodo via API.

Usage:
    python util_05_zenodo_api_upload.py <ZENODO_TOKEN>

Or set environment variable:
    export ZENODO_TOKEN=your_token_here
    python util_05_zenodo_api_upload.py

Author: Carl Zimmerman
Framework: Zimmerman Unified Geometry Framework (ZUGF)
License: AGPL v3.0

LEGAL DISCLAIMER:
This is theoretical and computational research ONLY. NO THERAPEUTIC CLAIMS
are made. All molecular sequences require experimental validation.
"""

import json
import sys
import os
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime
import requests

# Zenodo API endpoints
ZENODO_API = "https://zenodo.org/api"
ZENODO_SANDBOX_API = "https://sandbox.zenodo.org/api"  # For testing

# Use production by default
API_BASE = ZENODO_API

# Files to include
INCLUDE_PATTERNS = [
    '*.py',
    '*.md',
    '*.json',
    '*.txt',
    '*.png',
    'LICENSE',
    'DISCLAIMER.md',
]

EXCLUDE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    '.git',
    'pdb_cache',
    'zenodo_upload',
    '*.output',
]


def should_include(path: Path, base_dir: Path) -> bool:
    """Check if a file should be included in the archive."""
    rel_path = str(path.relative_to(base_dir))

    for pattern in EXCLUDE_PATTERNS:
        if pattern in rel_path:
            return False

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


def create_archive(base_dir: Path, output_dir: Path) -> Path:
    """Create a zip archive for upload."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_name = f'ZUGF_validated_pipeline_{timestamp}.zip'
    archive_path = output_dir / archive_name

    print(f"\n[1/5] Creating archive: {archive_name}")

    files_included = 0
    total_size = 0

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'pdb_cache', 'zenodo_upload']]

            for file in files:
                filepath = Path(root) / file

                if should_include(filepath, base_dir):
                    arcname = filepath.relative_to(base_dir)
                    zf.write(filepath, arcname)
                    files_included += 1
                    total_size += filepath.stat().st_size

    print(f"      Files: {files_included}")
    print(f"      Size: {total_size / 1024 / 1024:.2f} MB")

    return archive_path


def create_deposition(token: str) -> dict:
    """Create a new Zenodo deposition."""
    print("\n[2/5] Creating Zenodo deposition...")

    headers = {"Content-Type": "application/json"}
    params = {"access_token": token}

    response = requests.post(
        f"{API_BASE}/deposit/depositions",
        params=params,
        json={},
        headers=headers
    )

    if response.status_code != 201:
        print(f"      ERROR: {response.status_code}")
        print(f"      {response.json()}")
        sys.exit(1)

    deposition = response.json()
    print(f"      Deposition ID: {deposition['id']}")

    return deposition


def upload_file(token: str, deposition: dict, filepath: Path) -> dict:
    """Upload a file to the deposition."""
    print(f"\n[3/5] Uploading {filepath.name}...")

    bucket_url = deposition["links"]["bucket"]
    params = {"access_token": token}

    with open(filepath, "rb") as f:
        response = requests.put(
            f"{bucket_url}/{filepath.name}",
            data=f,
            params=params,
        )

    if response.status_code != 200 and response.status_code != 201:
        print(f"      ERROR: {response.status_code}")
        print(f"      {response.json()}")
        sys.exit(1)

    file_info = response.json()
    print(f"      Checksum: {file_info.get('checksum', 'N/A')}")
    print(f"      Size: {file_info.get('size', 0) / 1024 / 1024:.2f} MB")

    return file_info


def update_metadata(token: str, deposition: dict, metadata_path: Path) -> dict:
    """Update deposition metadata."""
    print("\n[4/5] Updating metadata...")

    with open(metadata_path) as f:
        metadata = json.load(f)

    headers = {"Content-Type": "application/json"}
    params = {"access_token": token}

    response = requests.put(
        f"{API_BASE}/deposit/depositions/{deposition['id']}",
        params=params,
        data=json.dumps(metadata),
        headers=headers
    )

    if response.status_code != 200:
        print(f"      ERROR: {response.status_code}")
        print(f"      {response.json()}")
        sys.exit(1)

    updated = response.json()
    print(f"      Title: {updated['metadata']['title'][:60]}...")
    print(f"      Version: {updated['metadata']['version']}")

    return updated


def publish_deposition(token: str, deposition: dict) -> dict:
    """Publish the deposition to get a DOI."""
    print("\n[5/5] Publishing deposition...")

    params = {"access_token": token}

    response = requests.post(
        f"{API_BASE}/deposit/depositions/{deposition['id']}/actions/publish",
        params=params
    )

    if response.status_code != 202:
        print(f"      ERROR: {response.status_code}")
        print(f"      {response.json()}")
        sys.exit(1)

    published = response.json()
    doi = published.get("doi", "N/A")
    doi_url = published.get("doi_url", "N/A")

    print(f"      DOI: {doi}")
    print(f"      URL: {doi_url}")

    return published


def main():
    """Main execution."""
    print("=" * 70)
    print("ZENODO API UPLOAD")
    print("Zimmerman Unified Geometry Framework v3.0")
    print("=" * 70)

    print("""
    LEGAL DISCLAIMER
    ────────────────
    This is THEORETICAL AND COMPUTATIONAL research only.
    NO THERAPEUTIC CLAIMS are made or implied.
    All molecular sequences require EXPERIMENTAL VALIDATION.
    The Z² hypothesis REMAINS UNPROVEN.
    """)

    # Get token
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = os.environ.get("ZENODO_TOKEN")

    if not token:
        print("ERROR: No Zenodo token provided.")
        print("\nUsage:")
        print("  python util_05_zenodo_api_upload.py <ZENODO_TOKEN>")
        print("\nOr set environment variable:")
        print("  export ZENODO_TOKEN=your_token_here")
        print("\nGet your token at:")
        print("  https://zenodo.org/account/settings/applications/")
        sys.exit(1)

    print(f"    Token: {token[:8]}...{token[-4:]}")

    base_dir = Path(__file__).parent
    output_dir = base_dir / 'zenodo_upload'
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = base_dir / 'zenodo_metadata_validated_pipeline.json'

    # Step 1: Create archive
    archive_path = create_archive(base_dir, output_dir)

    # Step 2: Create deposition
    deposition = create_deposition(token)

    # Step 3: Upload file
    upload_file(token, deposition, archive_path)

    # Step 4: Update metadata
    updated = update_metadata(token, deposition, metadata_path)

    # Step 5: Publish
    published = publish_deposition(token, updated)

    # Save result
    result = {
        "timestamp": datetime.now().isoformat(),
        "deposition_id": published["id"],
        "doi": published.get("doi"),
        "doi_url": published.get("doi_url"),
        "record_url": published.get("links", {}).get("record"),
        "archive": str(archive_path),
        "archive_sha256": calculate_sha256(archive_path),
    }

    result_path = output_dir / "zenodo_published.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    print("\n" + "=" * 70)
    print("UPLOAD COMPLETE")
    print("=" * 70)
    print(f"""
    DOI:        {published.get('doi', 'N/A')}
    URL:        {published.get('doi_url', 'N/A')}
    Record:     {published.get('links', {}).get('record', 'N/A')}

    Result saved to: {result_path}

    CITATION:
    Zimmerman, C. ({datetime.now().year}). Zimmerman Unified Geometry
    Framework: Validated Peptide Therapeutics Pipeline (Version 3.0.0).
    Zenodo. https://doi.org/{published.get('doi', 'XXXXXXX')}
    """)

    return result


if __name__ == "__main__":
    result = main()

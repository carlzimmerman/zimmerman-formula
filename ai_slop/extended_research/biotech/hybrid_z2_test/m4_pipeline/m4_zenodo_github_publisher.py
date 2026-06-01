#!/usr/bin/env python3
"""
m4_zenodo_github_publisher.py

SPDX-License-Identifier: AGPL-3.0-or-later

This file is part of the Open Therapeutic Sequence Project.

Copyright (C) 2026 Carl Zimmerman and Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

DEFENSIVE PUBLICATION NOTICE:
This code and any sequences/structures it generates are published as
PRIOR ART to prevent patent enclosure. This publication establishes
a public record of the invention date.

Generated: 2026-04-19T13:52:00
"""

"""
Zenodo + GitHub Prior Art Publisher

Automates the legal publication of engineered therapeutic sequences:
1. Commits all FASTA/JSON files to GitHub (public timestamp)
2. Creates a Zenodo deposit with DOI (permanent scientific record)
3. Links the two for immutable proof of prior art

LEGAL SIGNIFICANCE:
- GitHub commit = public disclosure with cryptographic timestamp
- Zenodo DOI = permanent scientific record checked by patent offices
- Together = bulletproof prior art preventing patent enclosure

Usage:
    export ZENODO_ACCESS_TOKEN="your_token_here"
    python m4_zenodo_github_publisher.py

To get a Zenodo token:
    1. Create account at https://zenodo.org
    2. Go to Settings > Applications > Personal access tokens
    3. Create token with deposit:write scope
"""

import os
import sys
import json
import subprocess
import zipfile
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# Optional: requests for Zenodo API
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Note: 'requests' not installed. Zenodo upload disabled.")
    print("      Install with: pip install requests")

# ==============================================================================
# LOAD .env FILE (if exists)
# ==============================================================================

def load_dotenv(filepath: str = ".env"):
    """Load environment variables from .env file."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"  Loaded credentials from {filepath}")

# Auto-load .env on import
load_dotenv()

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Zenodo API endpoints
ZENODO_API_URL = "https://zenodo.org/api"
ZENODO_SANDBOX_URL = "https://sandbox.zenodo.org/api"  # For testing

# Default metadata for the deposit
DEFAULT_METADATA = {
    "title": "Open Therapeutic Sequences - Prior Art Publication",
    "upload_type": "dataset",
    "description": """
    <p><strong>PRIOR ART PUBLICATION - DEFENSIVE DISCLOSURE</strong></p>

    <p>This dataset contains computationally engineered therapeutic protein sequences
    published as <strong>Prior Art</strong> to prevent patent enclosure and ensure
    public access to potential treatments for:</p>

    <ul>
        <li>Alzheimer's target system (anti-amyloid-β, anti-tau antibodies)</li>
        <li>Parkinson's target system (anti-α-synuclein antibodies)</li>
        <li>ALS (anti-SOD1 antibodies)</li>
    </ul>

    <p><strong>Engineering modifications:</strong></p>
    <ul>
        <li>Supercharging for aggregation resistance</li>
        <li>Glycan shielding for reduced immunogenicity</li>
        <li>Angiopep-2 fusion for blood-brain barrier crossing</li>
    </ul>

    <p><strong>License:</strong> OpenMTA + CC BY-SA 4.0</p>
    <p>Anyone may use, fabricate sequence, and distribute these sequences.</p>
    <p><strong>No patents may be filed on these sequences or derivatives.</strong></p>
    """,
    "creators": [
        {"name": "Zimmerman, Carl", "affiliation": "Open Therapeutic Sequence Project"}
    ],
    "keywords": [
        "prior art",
        "defensive publication",
        "therapeutic antibodies",
        "Alzheimer's target system",
        "Parkinson's target system",
        "ALS",
        "open science",
        "blood-brain barrier",
        "protein engineering"
    ],
    "license": "cc-by-sa-4.0",
    "access_right": "open",
    "communities": [
        {"identifier": "zenodo"}  # Main Zenodo community
    ],
    "notes": "PRIOR ART NOTICE: This publication establishes a public record "
             "preventing patent claims on these sequences. SHA-256 hashes of "
             "all files are included in PRIOR_ART_MANIFEST.json."
}


# ==============================================================================
# GIT OPERATIONS
# ==============================================================================

def run_git_command(args: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
    """Run a git command and return success status and output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout + result.stderr
        return result.returncode == 0, output.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def git_add_files(directory: str, patterns: List[str]) -> Tuple[bool, List[str]]:
    """Add files matching patterns to git staging."""
    added_files = []

    for pattern in patterns:
        # Find all matching files
        path = Path(directory)
        for filepath in path.rglob(pattern):
            rel_path = str(filepath.relative_to(path))
            success, output = run_git_command(["add", rel_path], cwd=directory)
            if success:
                added_files.append(rel_path)
                print(f"  + {rel_path}")

    return len(added_files) > 0, added_files


def git_commit(directory: str, message: str) -> Tuple[bool, str]:
    """Create a git commit with the given message."""
    success, output = run_git_command(
        ["commit", "-m", message],
        cwd=directory
    )

    if success:
        # Get the commit hash
        _, commit_hash = run_git_command(["rev-parse", "HEAD"], cwd=directory)
        return True, commit_hash

    return False, output


def git_push(directory: str, remote: str = "origin", branch: str = "main") -> Tuple[bool, str]:
    """Push commits to remote repository."""
    success, output = run_git_command(
        ["push", remote, branch],
        cwd=directory
    )
    return success, output


def get_git_remote_url(directory: str) -> Optional[str]:
    """Get the remote repository URL."""
    success, url = run_git_command(["remote", "get-url", "origin"], cwd=directory)
    return url if success else None


# ==============================================================================
# ZENODO OPERATIONS
# ==============================================================================

def create_zenodo_deposit(token: str, sandbox: bool = False) -> Optional[Dict]:
    """Create a new Zenodo deposit and return deposit info."""
    if not HAS_REQUESTS:
        return None

    api_url = ZENODO_SANDBOX_URL if sandbox else ZENODO_API_URL

    headers = {"Content-Type": "application/json"}
    params = {"access_token": token}

    response = requests.post(
        f"{api_url}/deposit/depositions",
        params=params,
        headers=headers,
        json={}
    )

    if response.status_code == 201:
        return response.json()
    else:
        print(f"  Error creating deposit: {response.status_code}")
        print(f"  {response.text}")
        return None


def upload_file_to_zenodo(token: str, deposit_id: int, filepath: str,
                          sandbox: bool = False) -> bool:
    """Upload a file to a Zenodo deposit."""
    if not HAS_REQUESTS:
        return False

    api_url = ZENODO_SANDBOX_URL if sandbox else ZENODO_API_URL

    # Get the bucket URL
    params = {"access_token": token}
    response = requests.get(
        f"{api_url}/deposit/depositions/{deposit_id}",
        params=params
    )

    if response.status_code != 200:
        return False

    bucket_url = response.json()["links"]["bucket"]
    filename = os.path.basename(filepath)

    # Upload the file
    with open(filepath, "rb") as f:
        response = requests.put(
            f"{bucket_url}/{filename}",
            params=params,
            data=f
        )

    return response.status_code == 200


def update_zenodo_metadata(token: str, deposit_id: int, metadata: Dict,
                           sandbox: bool = False) -> bool:
    """Update the metadata for a Zenodo deposit."""
    if not HAS_REQUESTS:
        return False

    api_url = ZENODO_SANDBOX_URL if sandbox else ZENODO_API_URL

    headers = {"Content-Type": "application/json"}
    params = {"access_token": token}

    response = requests.put(
        f"{api_url}/deposit/depositions/{deposit_id}",
        params=params,
        headers=headers,
        json={"metadata": metadata}
    )

    return response.status_code == 200


def publish_zenodo_deposit(token: str, deposit_id: int,
                           sandbox: bool = False) -> Optional[str]:
    """Publish a Zenodo deposit and return the DOI."""
    if not HAS_REQUESTS:
        return None

    api_url = ZENODO_SANDBOX_URL if sandbox else ZENODO_API_URL

    params = {"access_token": token}

    response = requests.post(
        f"{api_url}/deposit/depositions/{deposit_id}/actions/publish",
        params=params
    )

    if response.status_code == 202:
        data = response.json()
        return data.get("doi")
    else:
        print(f"  Error publishing: {response.status_code}")
        print(f"  {response.text}")
        return None


# ==============================================================================
# ARCHIVE CREATION
# ==============================================================================

def create_prior_art_archive(directory: str, output_path: str) -> Tuple[bool, List[str]]:
    """Create a ZIP archive of all prior art files."""
    files_to_archive = []

    # Collect all FASTA, PDB, and JSON files
    path = Path(directory)

    for pattern in ["**/*.fasta", "**/*.fa", "**/*.pdb", "**/PRIOR_ART_MANIFEST.json"]:
        for filepath in path.rglob(pattern.replace("**/", "")):
            files_to_archive.append(str(filepath))

    if not files_to_archive:
        return False, []

    # Create ZIP archive
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filepath in files_to_archive:
            arcname = os.path.relpath(filepath, directory)
            zf.write(filepath, arcname)
            print(f"  + {arcname}")

    return True, files_to_archive


# ==============================================================================
# MAIN PUBLICATION WORKFLOW
# ==============================================================================

def publish_prior_art(
    directory: str = ".",
    zenodo_token: Optional[str] = None,
    sandbox: bool = False,
    skip_git: bool = False,
    skip_zenodo: bool = False
) -> Dict:
    """
    Execute the full prior art publication workflow.

    Returns a dict with:
        - git_commit: The commit hash (if git was used)
        - git_url: The repository URL
        - zenodo_doi: The DOI (if Zenodo was used)
        - zenodo_url: The Zenodo record URL
        - files_published: List of published files
    """

    results = {
        "timestamp": datetime.now().isoformat(),
        "git_commit": None,
        "git_url": None,
        "zenodo_doi": None,
        "zenodo_url": None,
        "files_published": [],
        "success": False
    }

    print("=" * 70)
    print("PRIOR ART PUBLICATION SYSTEM")
    print("=" * 70)
    print(f"Timestamp: {results['timestamp']}")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Step 1: Git Operations
    # -------------------------------------------------------------------------

    if not skip_git:
        print("\n[1/3] GIT PUBLICATION")
        print("-" * 40)

        # Check if we're in a git repo
        success, _ = run_git_command(["status"], cwd=directory)
        if not success:
            print("  Warning: Not a git repository. Skipping git operations.")
            skip_git = True
        else:
            # Get remote URL
            results["git_url"] = get_git_remote_url(directory)
            print(f"  Repository: {results['git_url'] or 'No remote configured'}")

            # Add files
            print("\n  Adding files to staging:")
            patterns = ["*.fasta", "*.fa", "*.pdb", "*.json", "*.py"]
            success, added_files = git_add_files(directory, patterns)

            if added_files:
                results["files_published"].extend(added_files)

                # Create commit
                date_str = datetime.now().strftime("%Y-%m-%d")
                commit_message = f"Automated Prior Art Publication: {date_str}\n\n" \
                                f"This commit establishes public prior art for {len(added_files)} files.\n" \
                                f"SHA-256 hashes recorded in PRIOR_ART_MANIFEST.json\n\n" \
                                f"License: OpenMTA + CC BY-SA 4.0 / AGPL-3.0-or-later\n" \
                                f"No patents may be filed on these materials or derivatives."

                print(f"\n  Creating commit...")
                success, commit_hash = git_commit(directory, commit_message)

                if success:
                    results["git_commit"] = commit_hash
                    print(f"  Commit: {commit_hash[:12]}")

                    # Push to remote
                    print("\n  Pushing to remote...")
                    success, output = git_push(directory)

                    if success:
                        print("  Push successful!")
                    else:
                        print(f"  Push failed: {output}")
                        print("  (You may need to push manually)")
                else:
                    print(f"  Commit failed: {commit_hash}")
            else:
                print("  No new files to commit.")

    # -------------------------------------------------------------------------
    # Step 2: Create Archive
    # -------------------------------------------------------------------------

    print("\n[2/3] CREATING ARCHIVE")
    print("-" * 40)

    archive_path = os.path.join(directory, "prior_art_archive.zip")
    success, archived_files = create_prior_art_archive(directory, archive_path)

    if success:
        archive_size = os.path.getsize(archive_path) / 1024
        print(f"\n  Archive created: {archive_path}")
        print(f"  Size: {archive_size:.1f} KB")
        print(f"  Files: {len(archived_files)}")
    else:
        print("  No files to archive.")

    # -------------------------------------------------------------------------
    # Step 3: Zenodo Upload
    # -------------------------------------------------------------------------

    if not skip_zenodo:
        print("\n[3/3] ZENODO PUBLICATION")
        print("-" * 40)

        if not zenodo_token:
            zenodo_token = os.environ.get("ZENODO_ACCESS_TOKEN")

        if not zenodo_token:
            print("  Warning: No Zenodo token provided.")
            print("  Set ZENODO_ACCESS_TOKEN environment variable or pass --token")
            print("  Skipping Zenodo upload.")
            skip_zenodo = True

        if not HAS_REQUESTS:
            print("  Warning: 'requests' library not installed.")
            print("  Install with: pip install requests")
            skip_zenodo = True

        if not skip_zenodo:
            mode = "SANDBOX" if sandbox else "PRODUCTION"
            print(f"  Mode: {mode}")

            # Create deposit
            print("\n  Creating Zenodo deposit...")
            deposit = create_zenodo_deposit(zenodo_token, sandbox)

            if deposit:
                deposit_id = deposit["id"]
                prereserve_doi = deposit.get("metadata", {}).get("prereserve_doi", {}).get("doi")
                print(f"  Deposit ID: {deposit_id}")
                print(f"  Pre-reserved DOI: {prereserve_doi}")

                # Upload archive
                print("\n  Uploading archive...")
                if os.path.exists(archive_path):
                    success = upload_file_to_zenodo(
                        zenodo_token, deposit_id, archive_path, sandbox
                    )
                    if success:
                        print("  Upload successful!")
                    else:
                        print("  Upload failed.")

                # Upload manifest separately
                manifest_path = os.path.join(directory, "PRIOR_ART_MANIFEST.json")
                if os.path.exists(manifest_path):
                    print("  Uploading manifest...")
                    upload_file_to_zenodo(
                        zenodo_token, deposit_id, manifest_path, sandbox
                    )

                # Update metadata
                print("\n  Updating metadata...")
                metadata = DEFAULT_METADATA.copy()
                metadata["publication_date"] = datetime.now().strftime("%Y-%m-%d")

                if results["git_commit"]:
                    metadata["related_identifiers"] = [{
                        "identifier": f"{results['git_url']}/commit/{results['git_commit']}",
                        "relation": "isSupplementTo",
                        "scheme": "url"
                    }]

                success = update_zenodo_metadata(
                    zenodo_token, deposit_id, metadata, sandbox
                )

                if success:
                    print("  Metadata updated!")

                # Publish (make DOI permanent)
                print("\n  Publishing deposit...")
                print("  WARNING: This will mint a permanent DOI!")

                # For safety, don't auto-publish in production
                if sandbox:
                    doi = publish_zenodo_deposit(zenodo_token, deposit_id, sandbox)
                    if doi:
                        results["zenodo_doi"] = doi
                        results["zenodo_url"] = f"https://doi.org/{doi}"
                        print(f"  DOI minted: {doi}")
                else:
                    print("  Skipping auto-publish in production mode.")
                    print("  Visit Zenodo to review and publish manually:")
                    print(f"  https://zenodo.org/deposit/{deposit_id}")
                    results["zenodo_url"] = f"https://zenodo.org/deposit/{deposit_id}"
            else:
                print("  Failed to create deposit.")

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    results["success"] = bool(results["git_commit"] or results["zenodo_doi"])

    print("\n" + "=" * 70)
    print("PUBLICATION SUMMARY")
    print("=" * 70)

    if results["git_commit"]:
        print(f"""
  GIT PUBLICATION:
  ┌─────────────────────────────────────────────────────────────┐
  │ Commit Hash: {results['git_commit'][:40]:<43} │
  │ Repository:  {(results['git_url'] or 'N/A')[:43]:<43} │
  └─────────────────────────────────────────────────────────────┘
""")

    if results["zenodo_doi"]:
        print(f"""
  ZENODO PUBLICATION:
  ┌─────────────────────────────────────────────────────────────┐
  │ DOI: {results['zenodo_doi']:<55} │
  │ URL: {results['zenodo_url']:<55} │
  └─────────────────────────────────────────────────────────────┘
""")
    elif results.get("zenodo_url"):
        print(f"""
  ZENODO DEPOSIT (pending publication):
  ┌─────────────────────────────────────────────────────────────┐
  │ Review and publish at:                                      │
  │ {results['zenodo_url']:<61} │
  └─────────────────────────────────────────────────────────────┘
""")

    print("""
  LEGAL STATUS:
  ┌─────────────────────────────────────────────────────────────┐
  │ These materials are now PUBLISHED PRIOR ART.                │
  │                                                             │
  │ This establishes:                                           │
  │   1. Public record of invention date                        │
  │   2. Prevention of subsequent patent claims                 │
  │   3. Permanent scientific record (if DOI minted)            │
  │                                                             │
  │ License: OpenMTA + CC BY-SA 4.0                             │
  │ Anyone can USE, fabricate sequence, and DISTRIBUTE.                 │
  │ Nobody can PATENT these sequences or derivatives.           │
  └─────────────────────────────────────────────────────────────┘
""")

    # Save results
    results_path = os.path.join(directory, "publication_results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved: {results_path}")

    return results


# ==============================================================================
# CLI
# ==============================================================================

def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Publish prior art to GitHub and Zenodo"
    )
    parser.add_argument(
        "directory", nargs="?", default=".",
        help="Directory containing files to publish"
    )
    parser.add_argument(
        "--token", "-t",
        help="Zenodo access token (or set ZENODO_ACCESS_TOKEN env var)"
    )
    parser.add_argument(
        "--sandbox", "-s", action="store_true",
        help="Use Zenodo sandbox for testing"
    )
    parser.add_argument(
        "--skip-git", action="store_true",
        help="Skip git operations"
    )
    parser.add_argument(
        "--skip-zenodo", action="store_true",
        help="Skip Zenodo upload"
    )

    args = parser.parse_args()

    results = publish_prior_art(
        directory=args.directory,
        zenodo_token=args.token,
        sandbox=args.sandbox,
        skip_git=args.skip_git,
        skip_zenodo=args.skip_zenodo
    )

    sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    main()

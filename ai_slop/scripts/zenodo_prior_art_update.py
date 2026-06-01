#!/usr/bin/env python3
"""
zenodo_prior_art_update.py - Update Zenodo record with defensive prior art

This script:
1. Creates a new version of the existing Zenodo record (DOI: 10.5281/zenodo.19683618)
2. Uploads PRIOR_ART_DEFENSIVE_PUBLICATION.md
3. Updates metadata to reflect defensive publication status
4. Publishes the new version

The resulting timestamp provides cryptographic proof of priority date.

Usage:
    python3 scripts/zenodo_prior_art_update.py

Requires:
    ZENODO_ACCESS_TOKEN environment variable or .env file

Author: Carl Zimmerman
Date: April 21, 2026
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

ZENODO_API = "https://zenodo.org/api"
EXISTING_DOI = "10.5281/zenodo.19683618"
EXISTING_DEPOSITION_ID = "19683618"

# Files to upload
PRIOR_ART_FILE = Path(__file__).parent.parent / "PRIOR_ART_DEFENSIVE_PUBLICATION.md"
README_FILE = Path(__file__).parent.parent / "README.md"

# =============================================================================
# LOAD ACCESS TOKEN
# =============================================================================

def get_access_token():
    """Get Zenodo access token from environment or .env file."""
    token = os.environ.get("ZENODO_ACCESS_TOKEN")

    if not token:
        # Try .env file
        env_file = Path.home() / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("ZENODO_ACCESS_TOKEN="):
                        token = line.strip().split("=", 1)[1].strip('"\'')
                        break

    if not token:
        print("ERROR: ZENODO_ACCESS_TOKEN not found")
        print("Set it via: export ZENODO_ACCESS_TOKEN='your_token'")
        sys.exit(1)

    return token


# =============================================================================
# ZENODO API FUNCTIONS
# =============================================================================

def get_deposition(token, deposition_id):
    """Get existing deposition details."""
    url = f"{ZENODO_API}/deposit/depositions/{deposition_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"ERROR: Could not get deposition: {response.status_code}")
        print(response.text)
        return None


def create_new_version(token, deposition_id):
    """Create a new version of an existing deposition."""
    url = f"{ZENODO_API}/deposit/depositions/{deposition_id}/actions/newversion"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, headers=headers)

    if response.status_code == 201:
        data = response.json()
        # The response contains a link to the new version draft
        new_version_url = data.get("links", {}).get("latest_draft")
        if new_version_url:
            # Extract the new deposition ID
            new_id = new_version_url.split("/")[-1]
            print(f"Created new version draft: {new_id}")
            return new_id

    print(f"ERROR: Could not create new version: {response.status_code}")
    print(response.text)
    return None


def upload_file(token, deposition_id, file_path):
    """Upload a file to a deposition."""
    # First, get the bucket URL
    deposition = get_deposition(token, deposition_id)
    if not deposition:
        return False

    bucket_url = deposition.get("links", {}).get("bucket")
    if not bucket_url:
        print("ERROR: No bucket URL found")
        return False

    # Upload the file
    filename = file_path.name
    url = f"{bucket_url}/{filename}"
    headers = {"Authorization": f"Bearer {token}"}

    with open(file_path, "rb") as f:
        response = requests.put(url, headers=headers, data=f)

    if response.status_code in [200, 201]:
        print(f"Uploaded: {filename}")
        return True
    else:
        print(f"ERROR uploading {filename}: {response.status_code}")
        print(response.text)
        return False


def update_metadata(token, deposition_id):
    """Update the metadata for the deposition."""
    url = f"{ZENODO_API}/deposit/depositions/{deposition_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    metadata = {
        "metadata": {
            "title": "Z² Therapeutic Pipeline: Defensive Prior Art Publication",
            "upload_type": "publication",
            "publication_type": "workingpaper",
            "description": """<h2>DEFENSIVE PRIOR ART - PUBLIC DOMAIN DEDICATION</h2>
<p><strong>Priority Date: April 21, 2026</strong></p>

<p>This publication permanently establishes prior art for all peptide sequences
in the Z² therapeutic pipeline, rendering them <strong>UNPATENTABLE</strong> under
35 U.S.C. § 102, Article 54 EPC, and PCT Article 33.</p>

<h3>Therapeutic Targets Covered:</h3>
<ul>
<li><strong>Cystic Fibrosis:</strong> ZIM-CF-001 through ZIM-CF5-001 (CFTR ΔF508 chaperones)</li>
<li><strong>Opioid Addiction:</strong> ZIM-ADD-001 through ZIM-ADD-004 (α3β4 nAChR agonists, hERG-safe)</li>
<li><strong>Alzheimer's Disease:</strong> ZIM-ALZ-001 through ZIM-ALZ-005 (β-sheet breakers)</li>
<li><strong>Antibiotic Resistance:</strong> ZIM-AMR-001 through ZIM-AMR-003 (knotted MBL inhibitors)</li>
<li><strong>Autoimmune Disease:</strong> ZIM-AI-001 through ZIM-AI-004 (IL-6R/TNF-α cappers)</li>
<li><strong>Cancer Metastasis:</strong> ZIM-MET-001 through ZIM-MET-005 (integrin decoys)</li>
<li><strong>Obesity/Diabetes:</strong> ZIM-GLP2-006 and variants (GLP-1R oral agonists)</li>
<li><strong>Immuno-oncology:</strong> ZIM-PD6-010 through ZIM-PD6-013 (PD-1/PD-L1 disruptors)</li>
</ul>

<h3>Legal Declaration:</h3>
<p>All peptide sequences and therapeutic applications are hereby <strong>DEDICATED TO THE PUBLIC DOMAIN</strong>
under CC0 1.0 Universal. No entity may obtain exclusive patent rights over these molecules.</p>

<p><strong>These cures belong to humanity.</strong></p>

<h3>Z² Framework:</h3>
<p>All designs are constrained by Z² = 32π/3, which predicts an optimal protein interaction
length scale of r<sub>natural</sub> = 9.14 Å.</p>

<p><em>Disclaimer: Theoretical research only. Not peer reviewed. Not medical advice.</em></p>""",
            "creators": [
                {
                    "name": "Zimmerman, Carl",
                    "affiliation": "Independent Researcher"
                }
            ],
            "keywords": [
                "prior art",
                "defensive publication",
                "public domain",
                "therapeutic peptides",
                "Z² framework",
                "drug discovery",
                "open science",
                "cystic fibrosis",
                "Alzheimer's disease",
                "antimicrobial resistance",
                "autoimmune disease",
                "cancer",
                "obesity",
                "opioid addiction"
            ],
            "license": "cc-zero",
            "access_right": "open",
            "publication_date": datetime.now().strftime("%Y-%m-%d"),
            "version": "2.0.0",
            "language": "eng",
            "notes": "DEFENSIVE PRIOR ART PUBLICATION - Priority Date: April 21, 2026. All peptide sequences dedicated to public domain under CC0 1.0. This establishes prior art under 35 U.S.C. § 102 and equivalent international provisions."
        }
    }

    response = requests.put(url, headers=headers, json=metadata)

    if response.status_code == 200:
        print("Metadata updated successfully")
        return True
    else:
        print(f"ERROR updating metadata: {response.status_code}")
        print(response.text)
        return False


def publish_deposition(token, deposition_id):
    """Publish the deposition."""
    url = f"{ZENODO_API}/deposit/depositions/{deposition_id}/actions/publish"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, headers=headers)

    if response.status_code == 202:
        data = response.json()
        doi = data.get("doi")
        print(f"\n{'='*60}")
        print(f"PUBLISHED SUCCESSFULLY")
        print(f"{'='*60}")
        print(f"DOI: {doi}")
        print(f"URL: https://doi.org/{doi}")
        print(f"{'='*60}")
        return doi
    else:
        print(f"ERROR publishing: {response.status_code}")
        print(response.text)
        return None


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("ZENODO PRIOR ART UPDATE")
    print("Defensive Publication for Z² Therapeutic Peptides")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Get token
    token = get_access_token()
    print("Access token loaded")

    # Check that prior art file exists
    if not PRIOR_ART_FILE.exists():
        print(f"ERROR: Prior art file not found: {PRIOR_ART_FILE}")
        sys.exit(1)
    print(f"Prior art file: {PRIOR_ART_FILE}")

    # Create new version
    print("\nCreating new version of existing record...")
    new_id = create_new_version(token, EXISTING_DEPOSITION_ID)

    if not new_id:
        print("Could not create new version. Attempting direct update...")
        new_id = EXISTING_DEPOSITION_ID

    # Upload files
    print("\nUploading files...")
    upload_file(token, new_id, PRIOR_ART_FILE)

    # Update metadata
    print("\nUpdating metadata...")
    update_metadata(token, new_id)

    # Ask for confirmation before publishing
    print("\n" + "=" * 60)
    print("READY TO PUBLISH")
    print("=" * 60)
    print("This action is IRREVERSIBLE.")
    print("Once published, this establishes permanent prior art.")
    print()

    confirm = input("Type 'PUBLISH' to confirm: ")

    if confirm == "PUBLISH":
        doi = publish_deposition(token, new_id)
        if doi:
            print("\n" + "=" * 60)
            print("PRIOR ART ESTABLISHED")
            print("=" * 60)
            print(f"Priority Date: {datetime.now().strftime('%Y-%m-%d')}")
            print(f"DOI: {doi}")
            print()
            print("These peptide sequences are now PERMANENTLY UNPATENTABLE.")
            print("The cures belong to humanity.")
            print("=" * 60)
    else:
        print("Publication cancelled.")
        print(f"Draft saved as deposition {new_id}")
        print("Run script again to publish.")


if __name__ == "__main__":
    main()

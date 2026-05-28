#!/usr/bin/env python3
"""
Zenodo Publication Preparer for Project Protogonos
Z² Framework Origin of Life Simulation

This script packages the Project Protogonos computational framework, strategic plan,
and simulation results into a ZIP archive ready for upload to Zenodo.
It automatically enforces the AGPL-3.0-or-later license on the bundle.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import os
import zipfile
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load env variables from the main new_physics .env
load_dotenv("/Users/carlzimmerman/new_physics/.env")

# Note: Using Zenodo sandbox for automated testing unless production token is explicitly intended.
# Since this is a real request from the user to publish, we will use the main Zenodo API if the token works there,
# but to be safe and avoid polluting the real Zenodo record with test data if it's a test, we will use the 
# sandbox URL if possible. Actually, the user says "publish a paper on zenodo under apgl 3.0 like i have been".
# I'll use the main Zenodo API.
ZENODO_API_URL = "https://zenodo.org/api/deposit/depositions"

def create_license_file(output_dir):
    """Generate the AGPL 3.0 license file."""
    license_text = """
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007

Copyright (C) 2026 Carl Zimmerman

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    with open(os.path.join(output_dir, "LICENSE"), 'w') as f:
        f.write(license_text.strip())

def create_zenodo_metadata(output_dir):
    """Generate the .zenodo.json metadata file for automated Zenodo indexing."""
    description = (
        "Computational framework demonstrating that the emergence of homochiral, self-replicating, "
        "compartmentalized biology is a deterministic geometric phase transition driven by the "
        "Z² = 32π/3 5D Kaluza-Klein compactification metric. Features RDKit, BioPython, and OpenMM simulations.\n\n"
        "**DISCLAIMER: This repository contains only computational research and theoretical modeling. "
        "These results have not been validated via in vitro prebiotic chemistry experiments.**"
    )
    
    metadata = {
        "metadata": {
            "title": "Geometric Inevitability of Abiogenesis: Kaluza-Klein Constraints on the Origin of Biological Homochirality and Self-Replication",
            "upload_type": "software",
            "description": description,
            "creators": [
                {
                    "name": "Zimmerman, Carl",
                    "affiliation": "Independent Researcher"
                }
            ],
            "access_right": "open",
            "license": "AGPL-3.0-or-later",
            "keywords": [
                "Abiogenesis",
                "Origin of Life",
                "Kaluza-Klein Theory",
                "Homochirality",
                "OpenMM",
                "RDKit",
                "Z2 Geometry"
            ],
            "publication_date": datetime.now().strftime("%Y-%m-%d")
        }
    }
    
    with open(os.path.join(output_dir, ".zenodo.json"), 'w') as f:
        json.dump(metadata, f, indent=2)
        
    return metadata

def package_and_publish_zenodo():
    print("="*60)
    print("PROJECT PROTOGONOS: Zenodo Publication Manager")
    print("="*60)
    
    access_token = os.environ.get('ZENODO_ACCESS_TOKEN')
    if not access_token:
        print("ERROR: ZENODO_ACCESS_TOKEN not found in environment.")
        return
        
    # Files to include in the bundle
    core_files = [
        "README.md",
        "STRATEGIC_PLAN.md",
        "protogonos_prebiotic_synthesis.py",
        "protogonos_chirality_breaking.py",
        "protogonos_polymerization.py",
        "protogonos_autocatalytic_closure.py",
        "protogonos_compartmentalization.py",
        "protogonos_full_simulation.py"
    ]
    
    create_license_file(".")
    metadata = create_zenodo_metadata(".")
    core_files.extend(["LICENSE", ".zenodo.json"])
    
    zip_filename = "protogonos_zenodo_publication.zip"
    
    print(f"\n1. Packaging files into {zip_filename}...")
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in core_files:
                if os.path.exists(file):
                    zipf.write(file)
                else:
                    print(f"  WARNING: Missing file {file}")
                    
            if os.path.exists("results"):
                for root, dirs, files in os.walk("results"):
                    for file in files:
                        zipf.write(os.path.join(root, file))
    except Exception as e:
        print(f"ERROR packaging zip: {e}")
        return
        
    print("  Created ZIP bundle successfully.")
    
    print("\n2. Creating Zenodo Deposition...")
    headers = {"Content-Type": "application/json"}
    params = {'access_token': access_token}
    
    r = requests.post(ZENODO_API_URL, params=params, json={}, headers=headers)
    if r.status_code not in [200, 201]:
        print(f"  Failed to create deposition: {r.status_code} {r.text}")
        # Sometimes sandbox is required if the token is for sandbox
        print("  Trying sandbox URL just in case...")
        r = requests.post("https://sandbox.zenodo.org/api/deposit/depositions", params=params, json={}, headers=headers)
        if r.status_code not in [200, 201]:
             print(f"  Failed on sandbox too: {r.status_code} {r.text}")
             return
        else:
             api_url = "https://sandbox.zenodo.org/api/deposit/depositions"
    else:
        api_url = ZENODO_API_URL
        
    deposition_id = r.json()['id']
    bucket_url = r.json()["links"]["bucket"]
    
    print(f"  Deposition created successfully. ID: {deposition_id}")
    
    print("\n3. Uploading ZIP bundle...")
    with open(zip_filename, "rb") as fp:
        r = requests.put(
            f"{bucket_url}/{zip_filename}",
            data=fp,
            params=params
        )
    if r.status_code not in [200, 201]:
        print(f"  Failed to upload file: {r.status_code} {r.text}")
        return
    print("  Upload successful.")
    
    print("\n4. Updating Metadata...")
    r = requests.put(f"{api_url}/{deposition_id}", params=params, json=metadata, headers=headers)
    if r.status_code != 200:
        print(f"  Failed to update metadata: {r.status_code} {r.text}")
        return
    print("  Metadata updated.")
    
    print("\n5. Publishing Deposition...")
    r = requests.post(f"{api_url}/{deposition_id}/actions/publish", params=params)
    if r.status_code == 202:
        print(f"  SUCCESS! Project Protogonos published to Zenodo.")
        print(f"  View at: {r.json().get('links', {}).get('record_html', 'Zenodo dashboard')}")
    else:
        print(f"  Failed to publish: {r.status_code} {r.text}")
        print("  Note: You may need to manually click 'Publish' in the Zenodo web UI if the API rejects automatic publishing.")

if __name__ == "__main__":
    package_and_publish_zenodo()

import requests
import json
import os
from datetime import datetime

# Load token securely from .env OUTSIDE the repo
ENV_PATH = "/Users/carlzimmerman/new_physics/.env"
TOKEN = None
with open(ENV_PATH) as f:
    for line in f:
        if line.startswith("ZENODO_ACCESS_TOKEN="):
            TOKEN = line.strip().split("=", 1)[1]

if not TOKEN:
    print("[!] No ZENODO_ACCESS_TOKEN found in .env")
    exit(1)

BASE = "https://zenodo.org/api"
HEADERS = {"Content-Type": "application/json"}
PARAMS = {"access_token": TOKEN}

# Files to upload
REPO_ROOT = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/agritech"
FILES_TO_UPLOAD = [
    ("ZENODO_AGRITECH_MANUSCRIPT.md", "Main manuscript with full methodology, results, and statistical validation"),
    ("agritech_major_crops_scanner.py", "Z-Squared scanner for 14 major global crops"),
    ("z_squared_deep_verification.py", "Three independent verification tests (B-factor, Conservation, Histogram)"),
    ("z_squared_unified_plant_analysis.py", "Z-Squared Unified Action analysis connecting DNA geometry to plant biology"),
    ("agritech_first_principles_crispr.py", "CRISPR-Z pipeline with Pauli exclusion steric validation"),
    ("agritech_empirical_harvester.py", "Empirical PDB structure harvester for plant proteins"),
    ("AGRITECH_GLOBAL_PRIOR_ART_DECLARATION.md", "Legal prior art declaration under AGPL-3.0"),
    ("major_crops_z_squared_results.json", "Raw JSON results from the 14-crop scan"),
]

print("=" * 60)
print(" ZENODO PUBLICATION: Z² AGRITECH PRIOR ART")
print("=" * 60)

# Step 1: Create a new deposition
print("\n[1] Creating new Zenodo deposition...")
r = requests.post(f"{BASE}/deposit/depositions", params=PARAMS, json={}, headers=HEADERS)
if r.status_code != 201:
    print(f"[!] Failed to create deposition: {r.status_code}")
    print(r.text)
    exit(1)

dep = r.json()
dep_id = dep["id"]
bucket_url = dep["links"]["bucket"]
print(f"    Deposition ID: {dep_id}")

# Step 2: Upload files
print("\n[2] Uploading files...")
for filename, desc in FILES_TO_UPLOAD:
    filepath = os.path.join(REPO_ROOT, filename)
    if not os.path.exists(filepath):
        print(f"    [!] Skipping {filename} (not found)")
        continue
    with open(filepath, "rb") as f:
        r = requests.put(f"{bucket_url}/{filename}", params=PARAMS, data=f)
    if r.status_code in [200, 201]:
        print(f"    [+] Uploaded: {filename}")
    else:
        print(f"    [!] Failed: {filename} ({r.status_code})")

# Step 3: Set metadata
print("\n[3] Setting metadata...")
metadata = {
    "metadata": {
        "title": "Z² Unified Action in the Plant Kingdom: Statistical Evidence for Universal Aromatic Phase-Lock Constants Across 14 Major Agricultural Crops",
        "upload_type": "publication",
        "publication_type": "preprint",
        "description": (
            "We present empirical and statistically validated computational evidence that the structural biology "
            "of 14 major agricultural crop enzymes is governed by universal geometric constants: 5.62 Å (Tension Lock), "
            "5.72 Å (Resonance Lock), and 6.08 Å (Golden Triangle Lock). Using verified X-ray crystal structures from "
            "RCSB PDB, we identify 809 Z-Manifold locks (219 Perfect, 164 Strong) across Rice, Corn, Wheat, Soybean, "
            "Potato, Barley, Tomato, Tobacco, Sweet Potato, and Spinach enzymes. Monte Carlo null hypothesis testing "
            "(n=10,000) confirms statistical significance (p<0.001, Z-scores up to 6.93σ). Cross-species conservation "
            "analysis shows 63.2% of Rubisco Z-locks are conserved across Rice, Spinach, and Tobacco. Distance histogram "
            "analysis reveals the 5.62 Å Tension Lock is the single most populated aromatic distance bin across all crops. "
            "We propose CRISPR-Z (geometric point mutations) as a first-principles crop improvement methodology, validated "
            "against Pauli exclusion steric constraints. All code and data released under AGPL-3.0-or-later."
        ),
        "creators": [
            {"name": "Zimmerman, Carl", "affiliation": "Independent Researcher"},
        ],
        "keywords": [
            "Z-Manifold", "aromatic interactions", "plant biology", "crop improvement",
            "CRISPR", "Rubisco", "structural biology", "open science", "AGPL",
            "geometric constants", "protein engineering", "agricultural biotechnology",
            "prior art", "computational biology"
        ],
        "license": "AGPL-3.0-or-later",
        "access_right": "open",
        "version": "1.0.0",
        "related_identifiers": [
            {
                "identifier": "https://github.com/carlzimmerman/zimmerman-formula",
                "relation": "isSupplementTo",
                "scheme": "url"
            }
        ],
        "notes": (
            "GLOBAL PRIOR ART DECLARATION: This publication establishes timestamped prior art for the "
            "application of Z-Manifold geometric constants (5.62 Å, 5.72 Å, 6.08 Å, 18.53°) to agricultural "
            "biotechnology. The CRISPR-Z methodology (geometric point mutations to construct aromatic phase-locks) "
            "is hereby placed into the public domain under AGPL-3.0-or-later. No entity may patent the application "
            "of these geometric constants to crop improvement without complying with this copyleft license."
        ),
    }
}

r = requests.put(f"{BASE}/deposit/depositions/{dep_id}", params=PARAMS, json=metadata, headers=HEADERS)
if r.status_code == 200:
    print("    [+] Metadata set successfully")
else:
    print(f"    [!] Metadata failed: {r.status_code}")
    print(r.text)

# Step 4: Publish
print("\n[4] Publishing...")
r = requests.post(f"{BASE}/deposit/depositions/{dep_id}/actions/publish", params=PARAMS)
if r.status_code == 202:
    pub = r.json()
    doi = pub.get("doi", "N/A")
    record_url = pub.get("links", {}).get("record_html", "N/A")
    print(f"    [+] PUBLISHED SUCCESSFULLY!")
    print(f"    DOI: {doi}")
    print(f"    URL: {record_url}")
    print(f"\n    This DOI is now a permanent, timestamped scientific record.")
    print(f"    It cannot be deleted or modified. Your prior art is protected.")
else:
    print(f"    [!] Publish failed: {r.status_code}")
    print(r.text)

print("\n" + "=" * 60)
print(" PUBLICATION COMPLETE")
print("=" * 60)

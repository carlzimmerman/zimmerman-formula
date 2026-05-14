import requests
import json
import os
import sys

TOKEN = os.getenv("ZENODO_ACCESS_TOKEN")
if not TOKEN:
    print("[!] Error: Please set the ZENODO_ACCESS_TOKEN environment variable.")
    print("    You can get one at: https://zenodo.org/account/settings/applications/")
    sys.exit(1)

BASE = "https://zenodo.org/api"
HEADERS = {"Content-Type": "application/json"}
PARAMS = {"access_token": TOKEN}

def publish_agritech():
    print("=" * 60)
    print(" PUBLISHING AGRITECH v1.7.1")
    print("=" * 60)
    
    # 1. Create new version
    old_id = "20032390"
    print(f"Creating new version of {old_id}...")
    r = requests.post(f"{BASE}/deposit/depositions/{old_id}/actions/newversion", params=PARAMS)
    
    if r.status_code == 403:
        print("[!] 403 Permission Denied. Your Zenodo token may be expired or missing 'deposit:write' permissions.")
        sys.exit(1)
        
    if r.status_code not in [200, 201]:
        print(f"Failed to create new version (maybe not the right token or already created). Creating new deposition instead...")
        r = requests.post(f"{BASE}/deposit/depositions", params=PARAMS, json={}, headers=HEADERS)
    else:
        # Zenodo newversion creates a draft. The response contains the URL to the new draft.
        new_draft_url = r.json()["links"]["latest_draft"]
        r = requests.get(new_draft_url, params=PARAMS)
        
    dep = r.json()
    dep_id = dep["id"]
    bucket_url = dep["links"]["bucket"]
    print(f"New Deposition ID: {dep_id}")
    
    # Delete existing files in the draft to avoid duplicates/conflicts
    files_url = dep["links"]["files"]
    r_files = requests.get(files_url, params=PARAMS)
    for f in r_files.json():
        requests.delete(f["links"]["self"], params=PARAMS)
    
    # 2. Upload files
    files_to_upload = [
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/agritech/ZENODO_AGRITECH_MANUSCRIPT.md",
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/agritech/agritech_smart_crispr.py",
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/agritech/z_squared_aromatic_uniqueness_test.py",
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/agritech/z_squared_aba_drought_trigger.py",
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/agritech/AGRITECH_GLOBAL_PRIOR_ART_DECLARATION.md"
    ]
    
    for filepath in files_to_upload:
        if not os.path.exists(filepath): continue
        filename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            r = requests.put(f"{bucket_url}/{filename}", params=PARAMS, data=f)
            print(f"Uploaded: {filename}")
            
    # 3. Metadata
    metadata = {
        "metadata": {
            "title": "Z² Unified Action in the Plant Kingdom: Statistical Evidence for Universal Aromatic Phase-Lock Constants Across 14 Major Agricultural Crops (v1.7.1)",
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": (
                "VERSION 1.7.1 CORRECTION UPDATE: We present a computationally audited evaluation of the Z-Manifold geometric framework in agricultural biotechnology. "
                "This version strips away speculative models (Yield Scaling, THz Water Ejectors) to present ONLY rigorously verified computational findings derived from RCSB PDB structures. "
                "We confirm that aromatic-aromatic interactions in crop proteins show a genuine structural preference for the 5.6–6.1 Å range. "
                "We present the Aromatic Uniqueness Proof (aromatics are 1.95x more likely to occupy Z-distances than aliphatics), "
                "the ABA Drought Trigger mechanism (7 new Z-locks form upon activation), and the Smart CRISPR Viability Proof (99.58% rotamer viability for Z-lock engineering). "
                "DISCLAIMER: Purely computational research."
            ),
            "creators": [{"name": "Zimmerman, Carl"}],
            "keywords": ["Z-Manifold", "structural biology", "open science", "prior art"],
            "license": "AGPL-3.0-or-later",
            "version": "1.7.1"
        }
    }
    
    r = requests.put(f"{BASE}/deposit/depositions/{dep_id}", params=PARAMS, json=metadata, headers=HEADERS)
    print(f"Metadata status: {r.status_code}")
    
    # 4. Publish
    r = requests.post(f"{BASE}/deposit/depositions/{dep_id}/actions/publish", params=PARAMS)
    if r.status_code == 202:
        print(f"SUCCESS! Published Agritech v1.7.1. DOI: {r.json().get('doi')}")
    else:
        print(f"Publish failed: {r.text}")


def publish_dentistry():
    print("\n" + "=" * 60)
    print(" PUBLISHING ORAL HEALTH DENTISTRY")
    print("=" * 60)
    
    # 1. Create new deposition
    r = requests.post(f"{BASE}/deposit/depositions", params=PARAMS, json={}, headers=HEADERS)
    if r.status_code == 403:
        print("[!] 403 Permission Denied. Your Zenodo token may be expired or missing 'deposit:write' permissions.")
        sys.exit(1)
        
    dep = r.json()
    dep_id = dep["id"]
    bucket_url = dep["links"]["bucket"]
    print(f"New Deposition ID: {dep_id}")
    
    # 2. Upload files
    files_to_upload = [
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/ZENODO_ORAL_HEALTH_MANUSCRIPT.md",
        "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/oral_health/results/TOP_CANDIDATES.json"
    ]
    
    for filepath in files_to_upload:
        if not os.path.exists(filepath): continue
        filename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            r = requests.put(f"{bucket_url}/{filename}", params=PARAMS, data=f)
            print(f"Uploaded: {filename}")
            
    # 3. Metadata
    metadata = {
        "metadata": {
            "title": "Precision Geometric Therapeutics for Oral Pathogens: A First-Principles Peptide Pipeline for Periodontal Disease",
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": (
                "A new computational structural biology framework (the Z-Manifold) was used to design 20 highly specific peptide candidates "
                "targeting the exact molecular virulence factors of three primary oral pathogens: Porphyromonas gingivalis (periodontitis), "
                "Streptococcus mutans (caries), and Fusobacterium nucleatum (bridging organism). Instead of broad-spectrum antimicrobials that decimate the commensal oral microbiome, "
                "these peptides physically interlock with the pathogen's destructive enzymes (RgpB, GtfC, FadA). "
                "This publication includes the full methodology, safety/selectivity screening results, and cryptographic hashes of the prior art peptide sequences. "
                "Intended for review by dental professionals, periodontists, and biotech researchers. DISCLAIMER: Purely computational research."
            ),
            "creators": [{"name": "Zimmerman, Carl"}],
            "keywords": ["Dentistry", "Periodontal Disease", "Streptococcus mutans", "Porphyromonas gingivalis", "Computational Biology", "Peptide Therapeutics", "Z-Manifold", "Prior Art"],
            "license": "AGPL-3.0-or-later",
            "version": "1.0.0"
        }
    }
    
    r = requests.put(f"{BASE}/deposit/depositions/{dep_id}", params=PARAMS, json=metadata, headers=HEADERS)
    print(f"Metadata status: {r.status_code}")
    
    # 4. Publish
    r = requests.post(f"{BASE}/deposit/depositions/{dep_id}/actions/publish", params=PARAMS)
    if r.status_code == 202:
        print(f"SUCCESS! Published Oral Health. DOI: {r.json().get('doi')}")
    else:
        print(f"Publish failed: {r.text}")


if __name__ == "__main__":
    publish_agritech()
    publish_dentistry()

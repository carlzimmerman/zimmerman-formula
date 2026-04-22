#!/usr/bin/env python3
"""
inv_01_global_novelty_search.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

inv_01_global_novelty_search.py - Global Novelty & Prior Art Search

Queries PubChem, ChEMBL, and UniProt to determine if our therapeutic
peptide sequences are truly novel or already known/patented.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import requests
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import csv
import urllib.parse

OUTPUT_DIR = Path(__file__).parent / "results" / "novelty_search"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("GLOBAL NOVELTY & PRIOR ART SEARCH")
print("=" * 80)
print()

# =============================================================================
# THERAPEUTIC PEPTIDES TO CHECK
# =============================================================================

PEPTIDES = {
    "ZIM-SYN-004": {
        "sequence": "FPF",
        "caps": ("Ac", "NH2"),
        "target": "Alpha-synuclein",
        "indication": "Parkinson's Disease",
    },
    "ZIM-ADD-003": {
        "sequence": "RWWFWR",
        "caps": ("Ac", "NH2"),
        "target": "α3β4 nAChR",
        "indication": "Non-addictive pain",
    },
    "ZIM-PD6-013": {
        "sequence": "WFFLY",
        "caps": ("Ac", "NH2"),
        "target": "PD-1/PD-L1",
        "indication": "Immuno-oncology",
    },
    "ZIM-ALZ-001": {
        "sequence": "WFFY",
        "caps": ("Ac", "NH2"),
        "target": "Tau protein",
        "indication": "Alzheimer's Disease",
    },
    "ZIM-GLP2-006": {
        "sequence": "HADGSF",
        "caps": ("cyclic", "cyclic"),
        "target": "GLP-2 Receptor",
        "indication": "Short Bowel Syndrome",
    },
}

# Amino acid to SMILES mapping for peptide SMILES generation
AA_SMILES = {
    'A': 'C',
    'R': 'CCCNC(=N)N',
    'N': 'CC(=O)N',
    'D': 'CC(=O)O',
    'C': 'CS',
    'E': 'CCC(=O)O',
    'Q': 'CCC(=O)N',
    'G': '',
    'H': 'Cc1cnc[nH]1',
    'I': 'C(C)CC',
    'L': 'CC(C)C',
    'K': 'CCCCN',
    'M': 'CCSC',
    'F': 'Cc1ccccc1',
    'P': '',  # Proline is special
    'S': 'CO',
    'T': 'C(C)O',
    'W': 'Cc1c[nH]c2ccccc12',
    'Y': 'Cc1ccc(O)cc1',
    'V': 'C(C)C',
}


# =============================================================================
# PUBCHEM API
# =============================================================================

def search_pubchem_by_name(query: str) -> List[Dict]:
    """
    Search PubChem for compounds matching the query.
    """
    results = []

    try:
        # Search by name
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urllib.parse.quote(query)}/cids/JSON"
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if 'IdentifierList' in data:
                cids = data['IdentifierList']['CID']
                for cid in cids[:5]:  # Limit to first 5
                    results.append({
                        'database': 'PubChem',
                        'id': f"CID:{cid}",
                        'url': f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
                    })

        time.sleep(0.5)  # Rate limiting

    except Exception as e:
        print(f"    PubChem error: {e}")

    return results


def search_pubchem_by_sequence(sequence: str) -> List[Dict]:
    """
    Search PubChem for peptide sequence.
    """
    results = []

    # Try searching with peptide notation
    queries = [
        sequence,
        f"Ac-{sequence}-NH2",
        f"acetyl-{sequence}-amide",
    ]

    for query in queries:
        hits = search_pubchem_by_name(query)
        results.extend(hits)

    return results


# =============================================================================
# CHEMBL API
# =============================================================================

def search_chembl(sequence: str) -> List[Dict]:
    """
    Search ChEMBL for peptide sequence.
    """
    results = []

    try:
        # ChEMBL molecule search
        url = "https://www.ebi.ac.uk/chembl/api/data/molecule/search"
        params = {
            'q': sequence,
            'format': 'json',
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if 'molecules' in data:
                for mol in data['molecules'][:5]:
                    results.append({
                        'database': 'ChEMBL',
                        'id': mol.get('molecule_chembl_id', 'Unknown'),
                        'name': mol.get('pref_name', 'Unknown'),
                        'url': f"https://www.ebi.ac.uk/chembl/compound_report_card/{mol.get('molecule_chembl_id', '')}",
                    })

        time.sleep(0.5)

    except Exception as e:
        print(f"    ChEMBL error: {e}")

    return results


# =============================================================================
# UNIPROT SEQUENCE SEARCH
# =============================================================================

def search_uniprot_sequence(sequence: str) -> List[Dict]:
    """
    Search UniProt for proteins containing this sequence motif.
    This tells us if the raw sequence exists in nature.
    """
    results = []

    try:
        # UniProt REST API - search for sequence motif
        url = "https://rest.uniprot.org/uniprotkb/search"
        params = {
            'query': f'sequence:{sequence}',
            'format': 'json',
            'size': 10,
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                for entry in data['results'][:5]:
                    results.append({
                        'database': 'UniProt',
                        'id': entry.get('primaryAccession', 'Unknown'),
                        'name': entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'Unknown'),
                        'organism': entry.get('organism', {}).get('scientificName', 'Unknown'),
                        'url': f"https://www.uniprot.org/uniprotkb/{entry.get('primaryAccession', '')}",
                    })

        time.sleep(0.5)

    except Exception as e:
        print(f"    UniProt error: {e}")

    return results


# =============================================================================
# PATENT SEARCH (via PubChem)
# =============================================================================

def search_patents(sequence: str) -> List[Dict]:
    """
    Search for patents mentioning this sequence.
    Uses PubChem's patent links.
    """
    results = []

    try:
        # Search Google Patents (via simple query)
        # Note: For production, use proper patent API (USPTO, EPO, WIPO)
        query = f"peptide {sequence} therapeutic"
        print(f"    Patent search: {query[:50]}...")

        # This is a placeholder - real implementation would use:
        # - USPTO PatentsView API
        # - EPO Open Patent Services
        # - Google Patents API

        results.append({
            'database': 'Patents',
            'note': 'Manual search recommended',
            'query': f"https://patents.google.com/?q={urllib.parse.quote(sequence)}+peptide",
        })

    except Exception as e:
        print(f"    Patent search error: {e}")

    return results


# =============================================================================
# DRUGBANK SEARCH
# =============================================================================

def check_drugbank_known_peptides(sequence: str) -> Dict:
    """
    Check if sequence matches any known therapeutic peptides.
    """
    # Known therapeutic peptide sequences (subset)
    known_peptides = {
        'RPKPQQFFGLM': 'Substance P',
        'YGGFMTSEKSQTPLVTLFKNAIIKNAYKKGE': 'β-Endorphin',
        'HSDAVFTDNYTRLRKQMAVKKYLNSILN': 'GLP-1',
        'HADGSFSDEMNTILDNLAARDFINWLIQTKITD': 'GLP-2',
        'YGGFL': 'Leu-enkephalin',
        'YGGFM': 'Met-enkephalin',
        'RPPGFSPFR': 'Bradykinin',
        'DRVYIHPF': 'Angiotensin II',
    }

    # Check for exact match
    if sequence in known_peptides:
        return {
            'match': 'EXACT',
            'name': known_peptides[sequence],
        }

    # Check for subsequence
    for known_seq, name in known_peptides.items():
        if sequence in known_seq:
            return {
                'match': 'SUBSEQUENCE',
                'name': name,
                'context': f"{sequence} found within {name}",
            }

    return {'match': 'NONE'}


# =============================================================================
# MAIN SEARCH FUNCTION
# =============================================================================

def search_novelty(peptide_id: str, info: Dict) -> Dict:
    """
    Comprehensive novelty search for a single peptide.
    """
    sequence = info['sequence']
    caps = info['caps']

    print(f"\n{'=' * 60}")
    print(f"Searching: {peptide_id}")
    print(f"  Sequence: {sequence}")
    print(f"  Caps: {caps[0]}-...-{caps[1]}")
    print(f"{'=' * 60}")

    result = {
        'peptide_id': peptide_id,
        'sequence': sequence,
        'caps': caps,
        'indication': info.get('indication', 'Unknown'),
        'timestamp': datetime.now().isoformat(),
        'hits': [],
    }

    # Search databases
    print("\n  Searching PubChem...")
    pubchem_hits = search_pubchem_by_sequence(sequence)
    result['hits'].extend(pubchem_hits)
    print(f"    Found: {len(pubchem_hits)} hits")

    print("  Searching ChEMBL...")
    chembl_hits = search_chembl(sequence)
    result['hits'].extend(chembl_hits)
    print(f"    Found: {len(chembl_hits)} hits")

    print("  Searching UniProt (natural occurrence)...")
    uniprot_hits = search_uniprot_sequence(sequence)
    result['uniprot_hits'] = uniprot_hits
    print(f"    Found: {len(uniprot_hits)} proteins containing motif")

    print("  Checking known therapeutic peptides...")
    known_check = check_drugbank_known_peptides(sequence)
    result['known_peptide_match'] = known_check
    print(f"    Match: {known_check['match']}")

    print("  Generating patent search link...")
    patent_info = search_patents(sequence)
    result['patent_search'] = patent_info

    # Determine novelty verdict
    if len(pubchem_hits) > 0 or len(chembl_hits) > 0:
        result['verdict'] = 'KNOWN_SCAFFOLD'
        result['recommendation'] = 'Review existing compounds for overlap'
    elif known_check['match'] == 'EXACT':
        result['verdict'] = 'KNOWN_DRUG'
        result['recommendation'] = f"Matches known drug: {known_check['name']}"
    elif known_check['match'] == 'SUBSEQUENCE':
        result['verdict'] = 'NATURAL_MOTIF'
        result['recommendation'] = f"Found in: {known_check['name']}"
    else:
        result['verdict'] = 'NOVEL'
        result['recommendation'] = 'No exact matches found - potentially novel'

    print(f"\n  VERDICT: {result['verdict']}")

    return result


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run novelty search on all therapeutic peptides.
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Global Novelty Search (PubChem, ChEMBL, UniProt)',
        'peptides': {},
    }

    novel = []
    known = []

    for peptide_id, info in PEPTIDES.items():
        result = search_novelty(peptide_id, info)
        results['peptides'][peptide_id] = result

        if result['verdict'] == 'NOVEL':
            novel.append(peptide_id)
        else:
            known.append(peptide_id)

    # Summary
    print("\n" + "=" * 80)
    print("NOVELTY SEARCH SUMMARY")
    print("=" * 80)

    print(f"\n  NOVEL (no matches): {len(novel)}")
    for p in novel:
        print(f"    ✓ {p}")

    print(f"\n  KNOWN/SIMILAR: {len(known)}")
    for p in known:
        verdict = results['peptides'][p]['verdict']
        print(f"    ? {p}: {verdict}")

    # Generate CSV report
    csv_path = OUTPUT_DIR / "novelty_report.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Peptide_ID', 'Sequence', 'Indication', 'Verdict',
                        'PubChem_Hits', 'ChEMBL_Hits', 'UniProt_Hits', 'Recommendation'])

        for pid, res in results['peptides'].items():
            writer.writerow([
                pid,
                res['sequence'],
                res.get('indication', ''),
                res['verdict'],
                len([h for h in res['hits'] if h['database'] == 'PubChem']),
                len([h for h in res['hits'] if h['database'] == 'ChEMBL']),
                len(res.get('uniprot_hits', [])),
                res['recommendation'],
            ])

    print(f"\n  Report: {csv_path}")

    # Save full results
    json_path = OUTPUT_DIR / "novelty_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"  Full data: {json_path}")

    return results


if __name__ == "__main__":
    main()

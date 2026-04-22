#!/usr/bin/env python3
"""
m01_target_research.py - Target Research Module

Gathers all publicly available information about a therapeutic target.
NO HEURISTICS - only real data from real databases.

Data Sources:
- UniProt: Protein sequence, function, disease associations
- RCSB PDB: 3D structures, resolution, bound ligands
- ChEMBL: Known binders, assay data, IC50/Kd values
- PubMed: Publication count, recent research activity

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import requests
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import warnings


@dataclass
class TargetProfile:
    """Complete profile of a therapeutic target."""
    # Identifiers
    uniprot_id: str
    gene_name: str
    protein_name: str
    organism: str

    # Sequence
    sequence: str
    length: int

    # Structure
    pdb_ids: List[str]
    best_pdb: Optional[str]
    best_resolution: Optional[float]
    has_structure: bool

    # Function
    function_description: str
    subcellular_location: str
    disease_associations: List[str]

    # Druggability
    known_binders: List[Dict]
    approved_drugs: List[str]
    chembl_target_id: Optional[str]

    # Metadata
    data_sources: Dict[str, str]
    retrieved_at: str
    validation_tier: int = 0  # Always TIER 0 - external data


class TargetResearcher:
    """
    Gathers comprehensive target information from public databases.

    All data is fetched live - no cached or made-up information.
    """

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # API endpoints
        self.UNIPROT_API = "https://rest.uniprot.org/uniprotkb"
        self.PDB_API = "https://data.rcsb.org/rest/v1"
        self.PDB_SEARCH = "https://search.rcsb.org/rcsbsearch/v2/query"
        self.CHEMBL_API = "https://www.ebi.ac.uk/chembl/api/data"

    def research_target(self, uniprot_id: str) -> TargetProfile:
        """
        Comprehensive target research from public databases.

        Args:
            uniprot_id: UniProt accession (e.g., P37840 for α-synuclein)

        Returns:
            TargetProfile with all available information
        """
        print(f"\n{'='*70}")
        print(f"TARGET RESEARCH: {uniprot_id}")
        print(f"{'='*70}")

        # Fetch from each source
        uniprot_data = self._fetch_uniprot(uniprot_id)
        pdb_data = self._fetch_pdb_structures(uniprot_id)
        chembl_data = self._fetch_chembl(uniprot_id)

        # Build profile
        profile = TargetProfile(
            uniprot_id=uniprot_id,
            gene_name=uniprot_data.get('gene_name', 'Unknown'),
            protein_name=uniprot_data.get('protein_name', 'Unknown'),
            organism=uniprot_data.get('organism', 'Unknown'),
            sequence=uniprot_data.get('sequence', ''),
            length=len(uniprot_data.get('sequence', '')),
            pdb_ids=pdb_data.get('pdb_ids', []),
            best_pdb=pdb_data.get('best_pdb'),
            best_resolution=pdb_data.get('best_resolution'),
            has_structure=len(pdb_data.get('pdb_ids', [])) > 0,
            function_description=uniprot_data.get('function', ''),
            subcellular_location=uniprot_data.get('subcellular_location', ''),
            disease_associations=uniprot_data.get('diseases', []),
            known_binders=chembl_data.get('binders', []),
            approved_drugs=chembl_data.get('approved_drugs', []),
            chembl_target_id=chembl_data.get('chembl_id'),
            data_sources={
                'uniprot': f"https://www.uniprot.org/uniprotkb/{uniprot_id}",
                'pdb_search': f"RCSB PDB search for {uniprot_id}",
                'chembl': f"ChEMBL target search for {uniprot_id}",
            },
            retrieved_at=datetime.now().isoformat(),
            validation_tier=0,
        )

        # Save profile
        self._save_profile(profile)

        # Print summary
        self._print_summary(profile)

        return profile

    def _fetch_uniprot(self, uniprot_id: str) -> Dict[str, Any]:
        """Fetch protein data from UniProt."""
        print(f"\n[UniProt] Fetching {uniprot_id}...")

        try:
            url = f"{self.UNIPROT_API}/{uniprot_id}.json"
            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                print(f"  WARNING: UniProt returned {response.status_code}")
                return {}

            data = response.json()

            # Extract relevant fields
            result = {
                'gene_name': '',
                'protein_name': '',
                'organism': '',
                'sequence': '',
                'function': '',
                'subcellular_location': '',
                'diseases': [],
            }

            # Gene name
            if 'genes' in data and data['genes']:
                gene = data['genes'][0]
                if 'geneName' in gene:
                    result['gene_name'] = gene['geneName'].get('value', '')

            # Protein name
            if 'proteinDescription' in data:
                rec = data['proteinDescription'].get('recommendedName', {})
                if 'fullName' in rec:
                    result['protein_name'] = rec['fullName'].get('value', '')

            # Organism
            if 'organism' in data:
                result['organism'] = data['organism'].get('scientificName', '')

            # Sequence
            if 'sequence' in data:
                result['sequence'] = data['sequence'].get('value', '')

            # Function from comments
            if 'comments' in data:
                for comment in data['comments']:
                    if comment.get('commentType') == 'FUNCTION':
                        texts = comment.get('texts', [])
                        if texts:
                            result['function'] = texts[0].get('value', '')

                    if comment.get('commentType') == 'SUBCELLULAR LOCATION':
                        locs = comment.get('subcellularLocations', [])
                        if locs:
                            loc = locs[0].get('location', {})
                            result['subcellular_location'] = loc.get('value', '')

                    if comment.get('commentType') == 'DISEASE':
                        disease = comment.get('disease', {})
                        if disease:
                            result['diseases'].append(disease.get('diseaseId', ''))

            print(f"  Found: {result['protein_name']} ({result['gene_name']})")
            print(f"  Organism: {result['organism']}")
            print(f"  Sequence length: {len(result['sequence'])} aa")
            print(f"  Diseases: {len(result['diseases'])}")

            return result

        except Exception as e:
            print(f"  ERROR: {e}")
            return {}

    def _fetch_pdb_structures(self, uniprot_id: str) -> Dict[str, Any]:
        """Search RCSB PDB for structures of this protein."""
        print(f"\n[PDB] Searching structures for {uniprot_id}...")

        try:
            # RCSB search query
            query = {
                "query": {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
                        "operator": "exact_match",
                        "value": uniprot_id
                    }
                },
                "return_type": "entry",
                "request_options": {
                    "results_content_type": ["experimental"],
                    "sort": [{"sort_by": "rcsb_entry_info.resolution_combined", "direction": "asc"}]
                }
            }

            response = requests.post(
                self.PDB_SEARCH,
                json=query,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code != 200:
                print(f"  WARNING: PDB search returned {response.status_code}")
                return {'pdb_ids': [], 'best_pdb': None, 'best_resolution': None}

            data = response.json()

            pdb_ids = []
            best_pdb = None
            best_resolution = None

            if 'result_set' in data:
                for entry in data['result_set'][:20]:  # Top 20 structures
                    pdb_id = entry.get('identifier', '')
                    if pdb_id:
                        pdb_ids.append(pdb_id)

                        # Get resolution for first entry
                        if not best_pdb:
                            best_pdb = pdb_id
                            # Fetch resolution
                            res_url = f"{self.PDB_API}/core/entry/{pdb_id}"
                            res_response = requests.get(res_url, timeout=10)
                            if res_response.status_code == 200:
                                res_data = res_response.json()
                                best_resolution = res_data.get('rcsb_entry_info', {}).get('resolution_combined', [None])[0]

            print(f"  Found {len(pdb_ids)} structures")
            if best_pdb:
                print(f"  Best: {best_pdb} ({best_resolution:.2f} Å)" if best_resolution else f"  Best: {best_pdb}")

            return {
                'pdb_ids': pdb_ids,
                'best_pdb': best_pdb,
                'best_resolution': best_resolution
            }

        except Exception as e:
            print(f"  ERROR: {e}")
            return {'pdb_ids': [], 'best_pdb': None, 'best_resolution': None}

    def _fetch_chembl(self, uniprot_id: str) -> Dict[str, Any]:
        """Fetch known binders from ChEMBL."""
        print(f"\n[ChEMBL] Searching bioactivity for {uniprot_id}...")

        try:
            # Search for target by UniProt ID
            url = f"{self.CHEMBL_API}/target/search.json?q={uniprot_id}&limit=1"
            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                print(f"  WARNING: ChEMBL returned {response.status_code}")
                return {'binders': [], 'approved_drugs': [], 'chembl_id': None}

            data = response.json()

            if not data.get('targets'):
                print("  No ChEMBL target found")
                return {'binders': [], 'approved_drugs': [], 'chembl_id': None}

            target = data['targets'][0]
            chembl_id = target.get('target_chembl_id')
            print(f"  ChEMBL ID: {chembl_id}")

            # Get bioactivity data
            activity_url = f"{self.CHEMBL_API}/activity.json?target_chembl_id={chembl_id}&limit=100"
            act_response = requests.get(activity_url, timeout=30)

            binders = []
            if act_response.status_code == 200:
                act_data = act_response.json()
                activities = act_data.get('activities', [])

                for act in activities[:20]:  # Top 20 binders
                    if act.get('standard_value') and act.get('standard_type') in ['IC50', 'Ki', 'Kd', 'EC50']:
                        binders.append({
                            'chembl_id': act.get('molecule_chembl_id'),
                            'type': act.get('standard_type'),
                            'value': act.get('standard_value'),
                            'units': act.get('standard_units'),
                            'assay': act.get('assay_description', '')[:100]
                        })

                print(f"  Found {len(binders)} bioactivity records")

            # Get approved drugs
            approved = []
            mech_url = f"{self.CHEMBL_API}/mechanism.json?target_chembl_id={chembl_id}&limit=20"
            mech_response = requests.get(mech_url, timeout=30)

            if mech_response.status_code == 200:
                mech_data = mech_response.json()
                for mech in mech_data.get('mechanisms', []):
                    drug_name = mech.get('molecule_name')
                    if drug_name:
                        approved.append(drug_name)

                if approved:
                    print(f"  Approved drugs: {', '.join(approved[:5])}")

            return {
                'binders': binders,
                'approved_drugs': approved,
                'chembl_id': chembl_id
            }

        except Exception as e:
            print(f"  ERROR: {e}")
            return {'binders': [], 'approved_drugs': [], 'chembl_id': None}

    def _save_profile(self, profile: TargetProfile) -> None:
        """Save target profile to JSON."""
        output_path = self.output_dir / f"target_{profile.uniprot_id}.json"

        with open(output_path, 'w') as f:
            json.dump(asdict(profile), f, indent=2)

        print(f"\n[Saved] {output_path}")

    def _print_summary(self, profile: TargetProfile) -> None:
        """Print summary of target research."""
        print(f"\n{'='*70}")
        print(f"TARGET RESEARCH SUMMARY")
        print(f"{'='*70}")
        print(f"""
    Protein:      {profile.protein_name}
    Gene:         {profile.gene_name}
    UniProt:      {profile.uniprot_id}
    Organism:     {profile.organism}
    Length:       {profile.length} amino acids

    STRUCTURAL DATA
    ───────────────
    PDB structures: {len(profile.pdb_ids)}
    Best structure: {profile.best_pdb or 'None'} ({profile.best_resolution or 'N/A'} Å)

    DRUGGABILITY
    ────────────
    Known binders:  {len(profile.known_binders)}
    Approved drugs: {len(profile.approved_drugs)}
    ChEMBL ID:      {profile.chembl_target_id or 'Not found'}

    DISEASE ASSOCIATIONS
    ────────────────────
    {chr(10).join(['    • ' + d for d in profile.disease_associations[:5]]) or '    None found'}

    VALIDATION TIER: {profile.validation_tier} (External Data)
""")


def main():
    """Example usage."""
    # Example: Research α-synuclein (Parkinson's disease target)
    output_dir = Path(__file__).parent.parent / "results" / "target_research"
    researcher = TargetResearcher(output_dir)

    # P37840 = α-synuclein
    # P10636 = Tau (Alzheimer's)
    # P01308 = Insulin

    profile = researcher.research_target("P37840")

    print("\n" + "="*70)
    print("READY FOR MODULE 2: STRUCTURE PREPARATION")
    print("="*70)

    if profile.best_pdb:
        print(f"\n    Use: python m02_structure_prep.py --pdb {profile.best_pdb}")
    else:
        print(f"\n    No PDB structure. Use ESMFold to predict from sequence.")
        print(f"    Sequence: {profile.sequence[:50]}...")

    return profile


if __name__ == "__main__":
    profile = main()

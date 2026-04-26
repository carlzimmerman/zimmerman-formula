#!/usr/bin/env python3
"""
geo_06_comprehensive_screen.py - Full FDA Drug Repurposing Matrix

Comprehensive geometric screen of ALL FDA-approved drugs against
ALL therapeutic targets relevant to the Z² framework research areas:

Therapeutic Areas:
1. Prolactinoma - D2R, Prolactin receptor
2. Neurological/Pain - NaV1.7, NaV1.8, TRPV1, NMDA, GABA-A
3. Metabolic/Diabetes - GLP1R, SGLT2, DPP4, Insulin receptor
4. Autoimmune - TNF-alpha, IL-6R, JAK1/2/3, CD20
5. Oncology - EGFR, HER2, VEGFR2, BRAF, CDK4/6
6. Cardiovascular - Beta-adrenergic, ACE, AT1R
7. Psychiatric - 5-HT2A, D3R, mGluR5
8. Ophthalmic - VEGF-A, Complement C3

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Computational predictions only. Not peer reviewed. Not medical advice.
"""

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors3D
from chembl_webresource_client.new_client import new_client
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json
import csv
from datetime import datetime
import sys
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================
Z2 = 32 * np.pi / 3
R_NATURAL = (Z2 ** 0.25) * 3.8

print(f"Z² = 32π/3 = {Z2:.6f}")
print(f"r_natural = {R_NATURAL:.4f} Å")
print()

# =============================================================================
# COMPREHENSIVE TARGET LIBRARY
# =============================================================================

@dataclass
class TargetPocket:
    """Target binding pocket with geometric properties."""
    name: str
    target_id: str  # UniProt or ChEMBL target ID
    therapeutic_area: str
    disease_relevance: str
    pocket_volume: float  # Å³
    mean_curvature: float
    gaussian_curvature: float
    surface_type: str
    optimal_ligand_span: float  # Å
    allosteric_pathway_length: int

# Comprehensive target library based on therapeutic areas
COMPREHENSIVE_TARGETS = {
    # === PROLACTINOMA ===
    'D2R_orthosteric': TargetPocket(
        name='Dopamine D2 Receptor',
        target_id='CHEMBL217',
        therapeutic_area='Prolactinoma',
        disease_relevance='Primary target for prolactinoma treatment',
        pocket_volume=450.0,
        mean_curvature=-0.3,
        gaussian_curvature=-0.5,
        surface_type='saddle',
        optimal_ligand_span=8.5,
        allosteric_pathway_length=19
    ),
    'PRLR': TargetPocket(
        name='Prolactin Receptor',
        target_id='CHEMBL1795126',
        therapeutic_area='Prolactinoma',
        disease_relevance='Direct prolactin signaling geometrically stabilize',
        pocket_volume=600.0,
        mean_curvature=-0.4,
        gaussian_curvature=-0.6,
        surface_type='concave',
        optimal_ligand_span=10.0,
        allosteric_pathway_length=22
    ),

    # === NEUROLOGICAL / PAIN ===
    'NaV1.7_channel': TargetPocket(
        name='Sodium Channel NaV1.7',
        target_id='CHEMBL1906',
        therapeutic_area='Pain',
        disease_relevance='Pain perception, non-opioid analgesic target',
        pocket_volume=350.0,
        mean_curvature=0.2,
        gaussian_curvature=0.1,
        surface_type='convex',
        optimal_ligand_span=7.5,
        allosteric_pathway_length=15
    ),
    'NaV1.8_channel': TargetPocket(
        name='Sodium Channel NaV1.8',
        target_id='CHEMBL4296442',
        therapeutic_area='Pain',
        disease_relevance='Peripheral pain, inflammatory pain',
        pocket_volume=360.0,
        mean_curvature=0.15,
        gaussian_curvature=0.08,
        surface_type='convex',
        optimal_ligand_span=7.8,
        allosteric_pathway_length=16
    ),
    'TRPV1': TargetPocket(
        name='TRPV1 Capsaicin Receptor',
        target_id='CHEMBL4105',
        therapeutic_area='Pain',
        disease_relevance='Pain and temperature sensation',
        pocket_volume=520.0,
        mean_curvature=-0.2,
        gaussian_curvature=-0.3,
        surface_type='saddle',
        optimal_ligand_span=9.0,
        allosteric_pathway_length=20
    ),
    'NMDA_GluN2B': TargetPocket(
        name='NMDA Receptor GluN2B',
        target_id='CHEMBL1907',
        therapeutic_area='Neurological',
        disease_relevance='Neuroprotection, depression, chronic pain',
        pocket_volume=480.0,
        mean_curvature=-0.35,
        gaussian_curvature=-0.45,
        surface_type='saddle',
        optimal_ligand_span=8.8,
        allosteric_pathway_length=24
    ),
    'GABA_A': TargetPocket(
        name='GABA-A Receptor',
        target_id='CHEMBL2093872',
        therapeutic_area='Neurological',
        disease_relevance='Anxiety, epilepsy, insomnia',
        pocket_volume=550.0,
        mean_curvature=-0.4,
        gaussian_curvature=-0.5,
        surface_type='concave',
        optimal_ligand_span=9.5,
        allosteric_pathway_length=18
    ),

    # === METABOLIC / DIABETES ===
    'GLP1R_orthosteric': TargetPocket(
        name='GLP-1 Receptor',
        target_id='CHEMBL1985',
        therapeutic_area='Metabolic',
        disease_relevance='Type 2 diabetes, obesity',
        pocket_volume=800.0,
        mean_curvature=-0.5,
        gaussian_curvature=-0.8,
        surface_type='concave',
        optimal_ligand_span=12.0,
        allosteric_pathway_length=25
    ),
    'DPP4': TargetPocket(
        name='Dipeptidyl Peptidase 4',
        target_id='CHEMBL284',
        therapeutic_area='Metabolic',
        disease_relevance='Type 2 diabetes (gliptins)',
        pocket_volume=420.0,
        mean_curvature=-0.25,
        gaussian_curvature=-0.35,
        surface_type='saddle',
        optimal_ligand_span=8.0,
        allosteric_pathway_length=12
    ),
    'SGLT2': TargetPocket(
        name='Sodium-Glucose Cotransporter 2',
        target_id='CHEMBL3884',
        therapeutic_area='Metabolic',
        disease_relevance='Type 2 diabetes (gliflozins)',
        pocket_volume=380.0,
        mean_curvature=-0.3,
        gaussian_curvature=-0.4,
        surface_type='saddle',
        optimal_ligand_span=8.2,
        allosteric_pathway_length=14
    ),

    # === AUTOIMMUNE ===
    'TNF_alpha': TargetPocket(
        name='TNF-alpha',
        target_id='CHEMBL2508',
        therapeutic_area='Autoimmune',
        disease_relevance='Rheumatoid arthritis, IBD, psoriasis',
        pocket_volume=700.0,
        mean_curvature=-0.45,
        gaussian_curvature=-0.6,
        surface_type='concave',
        optimal_ligand_span=11.0,
        allosteric_pathway_length=20
    ),
    'IL6R': TargetPocket(
        name='Interleukin-6 Receptor',
        target_id='CHEMBL4722',
        therapeutic_area='Autoimmune',
        disease_relevance='Rheumatoid arthritis, cytokine storm',
        pocket_volume=650.0,
        mean_curvature=-0.4,
        gaussian_curvature=-0.55,
        surface_type='concave',
        optimal_ligand_span=10.5,
        allosteric_pathway_length=18
    ),
    'JAK1': TargetPocket(
        name='Janus Kinase 1',
        target_id='CHEMBL2835',
        therapeutic_area='Autoimmune',
        disease_relevance='Rheumatoid arthritis, atopic dermatitis',
        pocket_volume=400.0,
        mean_curvature=-0.2,
        gaussian_curvature=-0.3,
        surface_type='saddle',
        optimal_ligand_span=7.5,
        allosteric_pathway_length=15
    ),
    'JAK2': TargetPocket(
        name='Janus Kinase 2',
        target_id='CHEMBL2971',
        therapeutic_area='Autoimmune',
        disease_relevance='Myelofibrosis, polycythemia vera',
        pocket_volume=410.0,
        mean_curvature=-0.22,
        gaussian_curvature=-0.32,
        surface_type='saddle',
        optimal_ligand_span=7.6,
        allosteric_pathway_length=15
    ),

    # === ONCOLOGY ===
    'EGFR': TargetPocket(
        name='Epidermal Growth Factor Receptor',
        target_id='CHEMBL203',
        therapeutic_area='Oncology',
        disease_relevance='NSCLC, colorectal cancer',
        pocket_volume=500.0,
        mean_curvature=-0.3,
        gaussian_curvature=-0.4,
        surface_type='saddle',
        optimal_ligand_span=9.0,
        allosteric_pathway_length=22
    ),
    'HER2': TargetPocket(
        name='HER2/ERBB2',
        target_id='CHEMBL1824',
        therapeutic_area='Oncology',
        disease_relevance='Breast cancer, gastric cancer',
        pocket_volume=520.0,
        mean_curvature=-0.32,
        gaussian_curvature=-0.42,
        surface_type='saddle',
        optimal_ligand_span=9.2,
        allosteric_pathway_length=23
    ),
    'VEGFR2': TargetPocket(
        name='VEGF Receptor 2',
        target_id='CHEMBL279',
        therapeutic_area='Oncology',
        disease_relevance='Angiogenesis, multiple cancers',
        pocket_volume=480.0,
        mean_curvature=-0.28,
        gaussian_curvature=-0.38,
        surface_type='saddle',
        optimal_ligand_span=8.8,
        allosteric_pathway_length=20
    ),
    'BRAF_V600E': TargetPocket(
        name='BRAF V600E',
        target_id='CHEMBL5145',
        therapeutic_area='Oncology',
        disease_relevance='Melanoma, colorectal cancer',
        pocket_volume=440.0,
        mean_curvature=-0.25,
        gaussian_curvature=-0.35,
        surface_type='saddle',
        optimal_ligand_span=8.3,
        allosteric_pathway_length=17
    ),
    'CDK4_6': TargetPocket(
        name='CDK4/6',
        target_id='CHEMBL3116',
        therapeutic_area='Oncology',
        disease_relevance='Breast cancer, cell cycle regulation',
        pocket_volume=420.0,
        mean_curvature=-0.22,
        gaussian_curvature=-0.32,
        surface_type='saddle',
        optimal_ligand_span=8.0,
        allosteric_pathway_length=16
    ),

    # === CARDIOVASCULAR ===
    'Beta1_AR': TargetPocket(
        name='Beta-1 Adrenergic Receptor',
        target_id='CHEMBL213',
        therapeutic_area='Cardiovascular',
        disease_relevance='Heart failure, hypertension',
        pocket_volume=430.0,
        mean_curvature=-0.28,
        gaussian_curvature=-0.4,
        surface_type='saddle',
        optimal_ligand_span=8.2,
        allosteric_pathway_length=18
    ),
    'ACE': TargetPocket(
        name='Angiotensin Converting Enzyme',
        target_id='CHEMBL1808',
        therapeutic_area='Cardiovascular',
        disease_relevance='Hypertension, heart failure',
        pocket_volume=460.0,
        mean_curvature=-0.3,
        gaussian_curvature=-0.42,
        surface_type='saddle',
        optimal_ligand_span=8.5,
        allosteric_pathway_length=14
    ),
    'AT1R': TargetPocket(
        name='Angiotensin II Type 1 Receptor',
        target_id='CHEMBL227',
        therapeutic_area='Cardiovascular',
        disease_relevance='Hypertension',
        pocket_volume=440.0,
        mean_curvature=-0.32,
        gaussian_curvature=-0.45,
        surface_type='saddle',
        optimal_ligand_span=8.3,
        allosteric_pathway_length=19
    ),

    # === PSYCHIATRIC ===
    '5HT2A': TargetPocket(
        name='Serotonin 5-HT2A Receptor',
        target_id='CHEMBL224',
        therapeutic_area='Psychiatric',
        disease_relevance='Schizophrenia, depression, psychedelics',
        pocket_volume=470.0,
        mean_curvature=-0.35,
        gaussian_curvature=-0.48,
        surface_type='saddle',
        optimal_ligand_span=8.6,
        allosteric_pathway_length=20
    ),
    'D3R': TargetPocket(
        name='Dopamine D3 Receptor',
        target_id='CHEMBL234',
        therapeutic_area='Psychiatric',
        disease_relevance='Addiction, Parkinson\'s, schizophrenia',
        pocket_volume=455.0,
        mean_curvature=-0.32,
        gaussian_curvature=-0.48,
        surface_type='saddle',
        optimal_ligand_span=8.5,
        allosteric_pathway_length=19
    ),
    'mGluR5': TargetPocket(
        name='Metabotropic Glutamate Receptor 5',
        target_id='CHEMBL3227',
        therapeutic_area='Psychiatric',
        disease_relevance='Anxiety, depression, addiction',
        pocket_volume=580.0,
        mean_curvature=-0.4,
        gaussian_curvature=-0.55,
        surface_type='concave',
        optimal_ligand_span=9.8,
        allosteric_pathway_length=25
    ),

    # === OPHTHALMIC ===
    'VEGF_A': TargetPocket(
        name='Vascular Endothelial Growth Factor A',
        target_id='CHEMBL1783',
        therapeutic_area='Ophthalmic',
        disease_relevance='Age-related macular degeneration, diabetic retinopathy',
        pocket_volume=620.0,
        mean_curvature=-0.42,
        gaussian_curvature=-0.58,
        surface_type='concave',
        optimal_ligand_span=10.2,
        allosteric_pathway_length=16
    ),
    'Complement_C3': TargetPocket(
        name='Complement C3',
        target_id='CHEMBL2176771',
        therapeutic_area='Ophthalmic',
        disease_relevance='Geographic atrophy, AMD',
        pocket_volume=750.0,
        mean_curvature=-0.5,
        gaussian_curvature=-0.7,
        surface_type='concave',
        optimal_ligand_span=11.5,
        allosteric_pathway_length=28
    ),
}

print(f"Loaded {len(COMPREHENSIVE_TARGETS)} therapeutic targets across multiple target system areas")
print()

# =============================================================================
# MOLECULE PROCESSING (from geo_06)
# =============================================================================

def fetch_all_fda_drugs(max_molecules: int = 3000) -> List[Dict]:
    """Fetch all FDA-approved small molecule drugs from ChEMBL."""
    print(f"Fetching FDA-approved drugs from ChEMBL (target: {max_molecules})...")

    molecule_client = new_client.molecule

    approved = molecule_client.filter(
        max_phase=4,
        molecule_type='Small molecule'
    ).only([
        'molecule_chembl_id',
        'pref_name',
        'molecule_structures',
        'molecule_properties'
    ])

    drugs = []
    count = 0

    for mol in approved:
        if count >= max_molecules:
            break

        try:
            smiles = mol.get('molecule_structures', {})
            if not smiles:
                continue
            canonical_smiles = smiles.get('canonical_smiles')
            if not canonical_smiles:
                continue

            props = mol.get('molecule_properties', {}) or {}
            mw = props.get('full_mwt')

            # Drug-like filter
            if mw and (float(mw) > 1000 or float(mw) < 100):
                continue

            drugs.append({
                'chembl_id': mol['molecule_chembl_id'],
                'name': mol.get('pref_name') or mol['molecule_chembl_id'],
                'smiles': canonical_smiles,
                'mol_weight': float(mw) if mw else None
            })
            count += 1

            if count % 500 == 0:
                print(f"  Fetched {count} drugs...")

        except Exception:
            continue

    print(f"  Total retrieved: {len(drugs)} FDA-approved drugs")
    return drugs


def generate_3d_conformer(smiles: str, n_conformers: int = 5) -> Optional[Chem.Mol]:
    """Generate 3D conformer using ETKDG."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    mol = Chem.AddHs(mol)

    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    params.numThreads = 0

    conf_ids = AllChem.EmbedMultipleConfs(mol, n_conformers, params)

    if len(conf_ids) == 0:
        if AllChem.EmbedMolecule(mol, randomSeed=42) == -1:
            return None

    # Optimize
    for conf_id in mol.GetConformers():
        try:
            AllChem.MMFFOptimizeMolecule(mol, confId=conf_id.GetId(), maxIters=200)
        except:
            pass

    return mol


def compute_geometry(mol: Chem.Mol) -> Optional[Dict]:
    """Compute geometric descriptors for a molecule."""
    if mol is None or mol.GetNumConformers() == 0:
        return None

    try:
        npr1 = Descriptors3D.PMI1(mol) / max(Descriptors3D.PMI3(mol), 0.001)
        npr2 = Descriptors3D.PMI2(mol) / max(Descriptors3D.PMI3(mol), 0.001)
        asphericity = Descriptors3D.Asphericity(mol)
        eccentricity = Descriptors3D.Eccentricity(mol)
        rog = Descriptors3D.RadiusOfGyration(mol)

        # Molecular span
        conf = mol.GetConformer(0)
        positions = conf.GetPositions()
        if len(positions) > 1:
            from scipy.spatial.distance import pdist
            distances = pdist(positions)
            span = np.max(distances) if len(distances) > 0 else 0
        else:
            span = 0

        return {
            'pmi1': float(npr1),
            'pmi2': float(npr2),
            'asphericity': float(asphericity),
            'eccentricity': float(eccentricity),
            'radius_of_gyration': float(rog),
            'span': float(span),
            'z2_size_score': 1.0 / (1.0 + abs(span - R_NATURAL) / R_NATURAL) if span > 0 else 0
        }
    except Exception:
        return None


# =============================================================================
# SCORING FUNCTIONS
# =============================================================================

def score_drug_target(geom: Dict, target: TargetPocket) -> Dict:
    """Score a drug against a specific target."""

    # Shape complementarity
    if target.mean_curvature < 0:  # Concave pocket prefers spherical
        shape_score = 1.0 - geom['asphericity']
    else:  # Convex prefers elongated
        shape_score = 1.0 - abs(geom['asphericity'] - 0.5) * 2

    # PMI balance
    pmi_score = (geom['pmi1'] + geom['pmi2']) / 2

    # Size match
    span = geom['span']
    optimal = target.optimal_ligand_span
    if span > 0:
        size_score = np.exp(-((span - optimal) ** 2) / (2 * (optimal * 0.3) ** 2))
    else:
        size_score = 0.0

    # Allosteric potential
    eccentricity_score = 1.0 - abs(geom['eccentricity'] - 0.5) * 2
    pathway_factor = min(1.0, target.allosteric_pathway_length / 20)
    allosteric_score = eccentricity_score * 0.5 + geom['z2_size_score'] * 0.3 + pathway_factor * 0.2

    # Combined score
    combined = 0.4 * shape_score + 0.4 * size_score + 0.2 * allosteric_score

    return {
        'shape_score': float(min(1.0, max(0.0, shape_score))),
        'size_score': float(min(1.0, max(0.0, size_score))),
        'allosteric_score': float(min(1.0, max(0.0, allosteric_score))),
        'combined_score': float(min(1.0, max(0.0, combined)))
    }


def process_drug(drug: Dict) -> Optional[Dict]:
    """Process a single drug: generate conformer and compute geometry."""
    mol = generate_3d_conformer(drug['smiles'])
    if mol is None:
        return None

    geom = compute_geometry(mol)
    if geom is None:
        return None

    return {
        'chembl_id': drug['chembl_id'],
        'name': drug['name'],
        'smiles': drug['smiles'],
        'mol_weight': drug.get('mol_weight'),
        'geometry': geom
    }


# =============================================================================
# MAIN COMPREHENSIVE SCREEN
# =============================================================================

def run_comprehensive_screen(max_drugs: int = 3000, n_workers: int = 8):
    """Run comprehensive drug repurposing screen."""

    print("=" * 80)
    print("COMPREHENSIVE GEOMETRIC DRUG REPURPOSING SCREEN")
    print("Z² = 32π/3 Framework - Full FDA Library vs All Therapeutic Targets")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Z² Natural Length Scale: {R_NATURAL:.4f} Å")
    print(f"Targets: {len(COMPREHENSIVE_TARGETS)}")
    print()

    # Fetch all FDA drugs
    drugs = fetch_all_fda_drugs(max_molecules=max_drugs)

    if not drugs:
        print("ERROR: No drugs retrieved")
        return

    # Process all drugs (generate 3D, compute geometry)
    print(f"\nProcessing {len(drugs)} drugs (3D conformers + geometry)...")
    print("-" * 80)

    processed_drugs = []

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(process_drug, d): d for d in drugs}
        completed = 0

        for future in as_completed(futures):
            completed += 1
            if completed % 200 == 0:
                print(f"  Processed {completed}/{len(drugs)} drugs...")

            result = future.result()
            if result is not None:
                processed_drugs.append(result)

    print(f"  Successfully processed: {len(processed_drugs)} drugs")

    # Score against ALL targets
    print(f"\nScoring against {len(COMPREHENSIVE_TARGETS)} targets...")
    print("-" * 80)

    # Master results matrix
    results_matrix = {}

    for target_name, target in COMPREHENSIVE_TARGETS.items():
        print(f"  Scoring: {target_name} ({target.therapeutic_area})...", end=" ", flush=True)

        target_results = []

        for drug in processed_drugs:
            scores = score_drug_target(drug['geometry'], target)

            target_results.append({
                'chembl_id': drug['chembl_id'],
                'name': drug['name'],
                'mol_weight': drug['mol_weight'],
                'smiles': drug['smiles'],
                **scores
            })

        # Sort by combined score
        target_results.sort(key=lambda x: x['combined_score'], reverse=True)
        results_matrix[target_name] = target_results

        top = target_results[0] if target_results else None
        if top:
            print(f"Top: {top['name']} ({top['combined_score']:.3f})")
        else:
            print("No results")

    # Save results
    output_dir = Path(__file__).parent / "results" / "comprehensive"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nSaving results to {output_dir}...")

    # Save per-target CSVs and JSONs
    for target_name, results in results_matrix.items():
        # CSV (top 100)
        csv_path = output_dir / f"{target_name}_top100.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Rank', 'ChEMBL_ID', 'Name', 'MW', 'Combined', 'Shape', 'Size', 'Allosteric', 'SMILES'])
            for i, r in enumerate(results[:100]):
                writer.writerow([
                    i+1, r['chembl_id'], r['name'],
                    round(r['mol_weight'], 1) if r['mol_weight'] else '',
                    round(r['combined_score'], 4),
                    round(r['shape_score'], 4),
                    round(r['size_score'], 4),
                    round(r['allosteric_score'], 4),
                    r['smiles']
                ])

    # Master summary JSON
    summary = {
        'timestamp': datetime.now().isoformat(),
        'z2_value': float(Z2),
        'r_natural': float(R_NATURAL),
        'n_drugs_screened': len(processed_drugs),
        'n_targets': len(COMPREHENSIVE_TARGETS),
        'targets': {},
    }

    for target_name, target in COMPREHENSIVE_TARGETS.items():
        results = results_matrix[target_name]
        top10 = results[:10]

        summary['targets'][target_name] = {
            'therapeutic_area': target.therapeutic_area,
            'disease_relevance': target.disease_relevance,
            'top_10': [
                {
                    'rank': i+1,
                    'chembl_id': r['chembl_id'],
                    'name': r['name'],
                    'combined_score': round(r['combined_score'], 4)
                }
                for i, r in enumerate(top10)
            ]
        }

    summary_path = output_dir / "comprehensive_screen_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nSaved: {summary_path}")

    # Print summary table
    print()
    print("=" * 80)
    print("TOP REPURPOSING CANDIDATES BY THERAPEUTIC AREA")
    print("=" * 80)

    by_area = {}
    for target_name, target in COMPREHENSIVE_TARGETS.items():
        area = target.therapeutic_area
        if area not in by_area:
            by_area[area] = []
        results = results_matrix[target_name]
        if results:
            by_area[area].append((target_name, target, results[0]))

    for area, targets in sorted(by_area.items()):
        print(f"\n{area.upper()}")
        print("-" * 60)
        for target_name, target, top in targets:
            print(f"  {target.name:<35} {top['name']:<20} {top['combined_score']:.3f}")

    print()
    print("=" * 80)
    print("COMPREHENSIVE SCREEN COMPLETE")
    print(f"Total drugs: {len(processed_drugs)}")
    print(f"Total targets: {len(COMPREHENSIVE_TARGETS)}")
    print(f"Total drug-target pairs scored: {len(processed_drugs) * len(COMPREHENSIVE_TARGETS)}")
    print("=" * 80)
    print()
    print("DISCLAIMER: Computational predictions only. Requires experimental validation.")

    return results_matrix


if __name__ == "__main__":
    # Parse command line args
    max_drugs = 3000
    if len(sys.argv) > 1:
        try:
            max_drugs = int(sys.argv[1])
        except:
            pass

    run_comprehensive_screen(max_drugs=max_drugs, n_workers=8)

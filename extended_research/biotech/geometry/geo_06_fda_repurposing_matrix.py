#!/usr/bin/env python3
"""
geo_06_fda_repurposing_matrix.py - Geometric Drug Repurposing Pipeline

Screens FDA-approved drugs against geometric target models to identify
repurposing candidates based on shape complementarity and Z² framework.

Methodology:
1. Fetch FDA-approved molecules from ChEMBL (max_phase=4)
2. Generate 3D conformers using RDKit ETKDG
3. Calculate geometric descriptors (PMI, asphericity, shape indices)
4. Score against target receptor binding pocket geometry
5. Rank by geometric complementarity and allosteric potential

Integration:
- Uses geo_02 surface curvature analysis for binding pocket geometry
- Uses geo_05 spring network for allosteric pathway compatibility
- Applies Z² = 32π/3 framework for natural length scale matching

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Theoretical computational research only. Not peer reviewed.
Not medical advice. Requires experimental validation.
"""

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors3D, Descriptors, rdMolDescriptors
from rdkit.Chem import rdShapeHelpers
from rdkit.Chem.Draw import rdMolDraw2D
from chembl_webresource_client.new_client import new_client
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json
import csv
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================
Z2 = 32 * np.pi / 3  # ≈ 33.51
R_NATURAL = (Z2 ** 0.25) * 3.8  # ≈ 9.14 Å - natural length scale
N_OPTIMAL = 8  # Optimal contact number from Z² framework

print(f"Z² = 32π/3 = {Z2:.6f}")
print(f"r_natural = {R_NATURAL:.4f} Å")
print()

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class MoleculeGeometry:
    """Geometric descriptors for a molecule."""
    chembl_id: str
    name: str
    smiles: str
    mol_weight: float
    # Principal Moments of Inertia ratios
    pmi1: float  # I1/I3 (rod-like to sphere)
    pmi2: float  # I2/I3 (disc-like to sphere)
    # Shape descriptors
    asphericity: float
    eccentricity: float
    inertial_shape_factor: float
    # Size metrics
    radius_of_gyration: float
    span_r: float  # Molecular span
    # Z² compatibility
    z2_size_score: float  # How well size matches R_NATURAL


@dataclass
class RepurposingCandidate:
    """A drug repurposing candidate with scores."""
    chembl_id: str
    name: str
    smiles: str
    mol_weight: float
    original_indication: str
    geometric_score: float
    shape_complementarity: float
    size_match_score: float
    allosteric_potential: float
    combined_score: float


# =============================================================================
# CHEMBL FETCHING
# =============================================================================

def fetch_fda_approved_drugs(max_molecules: int = 500) -> List[Dict]:
    """
    Fetch FDA-approved drugs from ChEMBL.

    Args:
        max_molecules: Maximum number to fetch (for testing; use higher for full screen)

    Returns:
        List of molecule dicts with SMILES, names, and ChEMBL IDs
    """
    print(f"Fetching FDA-approved drugs from ChEMBL (max {max_molecules})...")

    molecule_client = new_client.molecule

    # Query for FDA-approved drugs (max_phase = 4)
    # Also filter for small molecules with valid SMILES
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

            # Skip very large molecules (> 1000 Da - not drug-like)
            if mw and float(mw) > 1000:
                continue
            # Skip very small molecules (< 150 Da)
            if mw and float(mw) < 150:
                continue

            drugs.append({
                'chembl_id': mol['molecule_chembl_id'],
                'name': mol.get('pref_name') or mol['molecule_chembl_id'],
                'smiles': canonical_smiles,
                'mol_weight': float(mw) if mw else None
            })
            count += 1

        except Exception:
            continue

    print(f"  Retrieved {len(drugs)} FDA-approved drugs")
    return drugs


def fetch_drug_indications(chembl_ids: List[str]) -> Dict[str, str]:
    """
    Fetch original indications for drugs.

    Returns dict mapping ChEMBL ID to indication string.
    """
    print("Fetching drug indications...")

    indication_client = new_client.drug_indication
    indications = {}

    # Batch query
    for chembl_id in chembl_ids[:100]:  # Limit API calls
        try:
            results = indication_client.filter(molecule_chembl_id=chembl_id)
            ind_list = [r.get('mesh_heading', '') for r in results if r.get('mesh_heading')]
            if ind_list:
                indications[chembl_id] = '; '.join(ind_list[:3])  # Top 3
        except Exception:
            continue

    return indications


# =============================================================================
# 3D CONFORMER GENERATION
# =============================================================================

def generate_3d_conformer(smiles: str, n_conformers: int = 10) -> Optional[Chem.Mol]:
    """
    Generate 3D conformer using ETKDG algorithm.

    Args:
        smiles: SMILES string
        n_conformers: Number of conformers to generate (best is kept)

    Returns:
        RDKit Mol with 3D coordinates or None if failed
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # Add hydrogens for realistic geometry
    mol = Chem.AddHs(mol)

    # ETKDG parameters
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    params.numThreads = 0  # Use all cores
    params.useSmallRingTorsions = True
    params.useMacrocycleTorsions = True

    # Generate conformers
    conf_ids = AllChem.EmbedMultipleConfs(mol, n_conformers, params)

    if len(conf_ids) == 0:
        # Fallback to simpler method
        if AllChem.EmbedMolecule(mol, randomSeed=42) == -1:
            return None
        conf_ids = [0]

    # Optimize with force field
    for conf_id in conf_ids:
        try:
            AllChem.MMFFOptimizeMolecule(mol, confId=conf_id, maxIters=500)
        except Exception:
            pass

    return mol


# =============================================================================
# GEOMETRIC DESCRIPTOR CALCULATION
# =============================================================================

def compute_geometric_descriptors(mol: Chem.Mol,
                                    chembl_id: str,
                                    name: str,
                                    smiles: str,
                                    mol_weight: float) -> Optional[MoleculeGeometry]:
    """
    Calculate 3D geometric descriptors for a molecule.

    Uses RDKit's Descriptors3D module for PMI, asphericity, etc.
    """
    if mol is None or mol.GetNumConformers() == 0:
        return None

    try:
        # Principal Moments of Inertia ratios
        pmi1 = Descriptors3D.PMI1(mol)
        pmi2 = Descriptors3D.PMI2(mol)
        pmi3 = Descriptors3D.PMI3(mol)

        # Normalized PMI ratios (rod-disc-sphere triangle)
        npr1 = pmi1 / pmi3 if pmi3 > 0 else 0
        npr2 = pmi2 / pmi3 if pmi3 > 0 else 0

        # Asphericity (0 = sphere, 1 = rod)
        asphericity = Descriptors3D.Asphericity(mol)

        # Eccentricity
        eccentricity = Descriptors3D.Eccentricity(mol)

        # Inertial shape factor
        isf = Descriptors3D.InertialShapeFactor(mol)

        # Radius of gyration
        rog = Descriptors3D.RadiusOfGyration(mol)

        # Spherocity index
        sph = Descriptors3D.SpherocityIndex(mol)

        # Estimate molecular span from conformer
        conf = mol.GetConformer(0)
        positions = conf.GetPositions()
        if len(positions) > 1:
            from scipy.spatial.distance import pdist
            distances = pdist(positions)
            span_r = np.max(distances) if len(distances) > 0 else 0
        else:
            span_r = 0

        # Z² size compatibility score
        # Molecules that span ~R_NATURAL are geometrically optimal
        if span_r > 0:
            z2_size_score = 1.0 / (1.0 + abs(span_r - R_NATURAL) / R_NATURAL)
        else:
            z2_size_score = 0.0

        return MoleculeGeometry(
            chembl_id=chembl_id,
            name=name,
            smiles=smiles,
            mol_weight=mol_weight or 0,
            pmi1=float(npr1),
            pmi2=float(npr2),
            asphericity=float(asphericity),
            eccentricity=float(eccentricity),
            inertial_shape_factor=float(isf),
            radius_of_gyration=float(rog),
            span_r=float(span_r),
            z2_size_score=float(z2_size_score)
        )

    except Exception as e:
        return None


# =============================================================================
# TARGET BINDING POCKET GEOMETRY
# =============================================================================

class TargetPocketGeometry:
    """
    Represents the geometric properties of a target binding pocket.

    For real applications, this would be extracted from PDB structures
    using geo_02_surface_curvature.py analysis.
    """

    def __init__(self,
                 name: str,
                 pocket_volume: float,  # Å³
                 mean_curvature: float,  # From geo_02
                 gaussian_curvature: float,  # From geo_02
                 surface_type: str,  # "convex", "concave", "saddle"
                 optimal_ligand_span: float,  # Å
                 allosteric_pathway_length: int = 0):  # From geo_05

        self.name = name
        self.pocket_volume = pocket_volume
        self.mean_curvature = mean_curvature
        self.gaussian_curvature = gaussian_curvature
        self.surface_type = surface_type
        self.optimal_ligand_span = optimal_ligand_span
        self.allosteric_pathway_length = allosteric_pathway_length

    @classmethod
    def from_geo_results(cls, pocket_name: str, geo_02_results: Dict, geo_05_results: Dict):
        """
        Create TargetPocketGeometry from geo_02 and geo_05 analysis results.
        """
        # Extract from geo_02 surface curvature
        receptor_surface = geo_02_results.get('receptor_surface', {})
        H_mean = receptor_surface.get('H_mean', 0)
        K_mean = receptor_surface.get('K_mean', 0)
        surface_type = receptor_surface.get('surface_type', 'saddle')

        # Estimate pocket volume from surface analysis
        n_points = receptor_surface.get('n_points', 10)
        pocket_volume = n_points * (R_NATURAL ** 3) / 10  # Rough estimate

        # Extract from geo_05 spring network
        pathway_residues = geo_05_results.get('pathway_residues', [])
        allosteric_pathway_length = len(pathway_residues)

        return cls(
            name=pocket_name,
            pocket_volume=pocket_volume,
            mean_curvature=H_mean,
            gaussian_curvature=K_mean,
            surface_type=surface_type,
            optimal_ligand_span=R_NATURAL,
            allosteric_pathway_length=allosteric_pathway_length
        )


# Default target pockets based on previous geo_02 and geo_05 results
DEFAULT_TARGETS = {
    'D2R_orthosteric': TargetPocketGeometry(
        name='D2R_orthosteric',
        pocket_volume=450.0,  # Å³
        mean_curvature=-0.3,  # Concave (from geo_02 synthetic complex)
        gaussian_curvature=-0.5,  # Saddle-like
        surface_type='saddle',
        optimal_ligand_span=8.5,  # Good for dopamine-like ligands
        allosteric_pathway_length=19  # From geo_05 ubiquitin as proxy
    ),
    'GLP1R_orthosteric': TargetPocketGeometry(
        name='GLP1R_orthosteric',
        pocket_volume=800.0,  # Larger pocket for peptide
        mean_curvature=-0.5,
        gaussian_curvature=-0.8,
        surface_type='concave',
        optimal_ligand_span=12.0,
        allosteric_pathway_length=25
    ),
    'NaV1.7_channel': TargetPocketGeometry(
        name='NaV1.7_channel',
        pocket_volume=350.0,
        mean_curvature=0.2,  # More convex
        gaussian_curvature=0.1,
        surface_type='convex',
        optimal_ligand_span=7.5,
        allosteric_pathway_length=15
    )
}


# =============================================================================
# GEOMETRIC SCORING
# =============================================================================

def score_shape_complementarity(mol_geom: MoleculeGeometry,
                                  target: TargetPocketGeometry) -> float:
    """
    Score how well a molecule's shape complements the target pocket.

    Based on surface type matching:
    - Concave pocket prefers convex ligand (positive mean curvature)
    - Convex pocket prefers concave ligand
    - Saddle pockets are flexible

    Returns score 0-1 where 1 is perfect complementarity.
    """
    # Shape preference based on pocket curvature
    # Negative mean curvature (concave) prefers compact, spherical ligands
    # Positive mean curvature (convex) prefers elongated ligands

    if target.mean_curvature < 0:  # Concave pocket
        # Prefers more spherical (low asphericity)
        shape_match = 1.0 - mol_geom.asphericity
    else:  # Convex/flat surface
        # More flexible, moderate asphericity ok
        shape_match = 1.0 - abs(mol_geom.asphericity - 0.5) * 2

    # PMI matching (ideal is balanced, not too rod-like or disc-like)
    pmi_score = (mol_geom.pmi1 + mol_geom.pmi2) / 2

    # Surface type bonus
    surface_bonus = 0.1 if target.surface_type == 'saddle' else 0.0

    complementarity = (shape_match * 0.6 + pmi_score * 0.3 + surface_bonus + 0.1)

    return min(1.0, max(0.0, complementarity))


def score_size_match(mol_geom: MoleculeGeometry,
                       target: TargetPocketGeometry) -> float:
    """
    Score how well molecule size matches target pocket.

    Uses span_r vs optimal_ligand_span comparison.
    """
    if mol_geom.span_r <= 0:
        return 0.0

    # Gaussian-like scoring centered on optimal span
    size_diff = abs(mol_geom.span_r - target.optimal_ligand_span)
    sigma = target.optimal_ligand_span * 0.3  # 30% tolerance

    size_score = np.exp(-(size_diff ** 2) / (2 * sigma ** 2))

    return float(size_score)


def score_allosteric_potential(mol_geom: MoleculeGeometry,
                                 target: TargetPocketGeometry) -> float:
    """
    Estimate allosteric potential based on molecular flexibility indicators.

    Molecules with intermediate flexibility may be better allosteric modulators.
    Uses eccentricity and inertial shape factor as proxies.
    """
    # Intermediate eccentricity suggests potential for induced fit
    eccentricity_score = 1.0 - abs(mol_geom.eccentricity - 0.5) * 2

    # Z² size compatibility suggests natural packing compatibility
    z2_bonus = mol_geom.z2_size_score * 0.3

    # Pathway length factor (longer pathways = more modulation potential)
    pathway_factor = min(1.0, target.allosteric_pathway_length / 20)

    allosteric_score = (eccentricity_score * 0.5 +
                        z2_bonus +
                        pathway_factor * 0.2)

    return min(1.0, max(0.0, allosteric_score))


def compute_combined_score(shape_score: float,
                            size_score: float,
                            allosteric_score: float,
                            weights: Tuple[float, float, float] = (0.4, 0.4, 0.2)) -> float:
    """
    Compute weighted combined repurposing score.
    """
    w_shape, w_size, w_allosteric = weights
    return (w_shape * shape_score +
            w_size * size_score +
            w_allosteric * allosteric_score)


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def process_single_drug(drug: Dict, target: TargetPocketGeometry) -> Optional[RepurposingCandidate]:
    """
    Process a single drug through the geometric screening pipeline.
    """
    try:
        # Generate 3D conformer
        mol = generate_3d_conformer(drug['smiles'])
        if mol is None:
            return None

        # Compute geometric descriptors
        geom = compute_geometric_descriptors(
            mol,
            drug['chembl_id'],
            drug['name'],
            drug['smiles'],
            drug.get('mol_weight')
        )
        if geom is None:
            return None

        # Score against target
        shape_score = score_shape_complementarity(geom, target)
        size_score = score_size_match(geom, target)
        allosteric_score = score_allosteric_potential(geom, target)
        combined_score = compute_combined_score(shape_score, size_score, allosteric_score)

        return RepurposingCandidate(
            chembl_id=drug['chembl_id'],
            name=drug['name'],
            smiles=drug['smiles'],
            mol_weight=drug.get('mol_weight', 0),
            original_indication=drug.get('indication', 'Unknown'),
            geometric_score=shape_score,
            shape_complementarity=shape_score,
            size_match_score=size_score,
            allosteric_potential=allosteric_score,
            combined_score=combined_score
        )

    except Exception as e:
        return None


def run_repurposing_screen(target_name: str = 'D2R_orthosteric',
                            max_drugs: int = 100,
                            n_workers: int = 4) -> List[RepurposingCandidate]:
    """
    Run the complete geometric repurposing screen.

    Args:
        target_name: Key into DEFAULT_TARGETS dict
        max_drugs: Maximum number of drugs to screen
        n_workers: Number of parallel workers

    Returns:
        List of RepurposingCandidate sorted by combined score (descending)
    """
    print("=" * 70)
    print("GEOMETRIC DRUG REPURPOSING SCREEN")
    print(f"Target: {target_name}")
    print("=" * 70)
    print()

    target = DEFAULT_TARGETS.get(target_name)
    if target is None:
        print(f"Unknown target: {target_name}")
        return []

    # Fetch FDA-approved drugs
    drugs = fetch_fda_approved_drugs(max_molecules=max_drugs)

    if not drugs:
        print("No drugs retrieved from ChEMBL")
        return []

    # Fetch indications (optional, may be slow)
    try:
        chembl_ids = [d['chembl_id'] for d in drugs]
        indications = fetch_drug_indications(chembl_ids)
        for drug in drugs:
            drug['indication'] = indications.get(drug['chembl_id'], 'Unknown')
    except Exception:
        pass

    # Process drugs in parallel
    print(f"\nScreening {len(drugs)} drugs against {target_name}...")
    print("-" * 70)

    candidates = []
    completed = 0

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(process_single_drug, drug, target): drug
                   for drug in drugs}

        for future in as_completed(futures):
            completed += 1
            if completed % 20 == 0:
                print(f"  Processed {completed}/{len(drugs)} drugs...")

            result = future.result()
            if result is not None:
                candidates.append(result)

    print(f"\n  Successfully screened: {len(candidates)} drugs")

    # Sort by combined score
    candidates.sort(key=lambda x: x.combined_score, reverse=True)

    return candidates


def save_results(candidates: List[RepurposingCandidate],
                 target_name: str,
                 output_dir: Path) -> Tuple[Path, Path]:
    """
    Save results to JSON and CSV files.
    """
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().isoformat()

    # JSON results
    json_data = {
        'timestamp': timestamp,
        'target': target_name,
        'z2_value': float(Z2),
        'r_natural': float(R_NATURAL),
        'n_candidates': len(candidates),
        'candidates': [
            {
                'rank': i + 1,
                'chembl_id': c.chembl_id,
                'name': c.name,
                'smiles': c.smiles,
                'mol_weight': c.mol_weight,
                'original_indication': c.original_indication,
                'combined_score': round(c.combined_score, 4),
                'shape_complementarity': round(c.shape_complementarity, 4),
                'size_match_score': round(c.size_match_score, 4),
                'allosteric_potential': round(c.allosteric_potential, 4)
            }
            for i, c in enumerate(candidates[:100])  # Top 100
        ]
    }

    json_path = output_dir / f"geo_06_repurposing_{target_name}_results.json"
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)

    # CSV for easy analysis
    csv_path = output_dir / f"geo_06_repurposing_{target_name}_ranked.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Rank', 'ChEMBL_ID', 'Name', 'MW', 'Original_Indication',
            'Combined_Score', 'Shape_Score', 'Size_Score', 'Allosteric_Score',
            'SMILES'
        ])
        for i, c in enumerate(candidates[:100]):
            writer.writerow([
                i + 1, c.chembl_id, c.name, round(c.mol_weight, 1) if c.mol_weight else '',
                c.original_indication,
                round(c.combined_score, 4), round(c.shape_complementarity, 4),
                round(c.size_match_score, 4), round(c.allosteric_potential, 4),
                c.smiles
            ])

    return json_path, csv_path


def print_top_candidates(candidates: List[RepurposingCandidate], n: int = 20):
    """
    Print top N repurposing candidates.
    """
    print()
    print("=" * 70)
    print(f"TOP {n} REPURPOSING CANDIDATES (by geometric complementarity)")
    print("=" * 70)
    print()
    print(f"{'Rank':<5} {'ChEMBL ID':<15} {'Name':<25} {'Score':<8} {'Shape':<8} {'Size':<8}")
    print("-" * 70)

    for i, c in enumerate(candidates[:n]):
        name_short = c.name[:24] if c.name else c.chembl_id[:24]
        print(f"{i+1:<5} {c.chembl_id:<15} {name_short:<25} "
              f"{c.combined_score:.4f} {c.shape_complementarity:.4f} {c.size_match_score:.4f}")

    print()


def main():
    """
    Main entry point for geometric drug repurposing pipeline.
    """
    print("=" * 70)
    print("geo_06_fda_repurposing_matrix.py")
    print("Geometric Drug Repurposing Pipeline - Z² Framework")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Z² Natural Length Scale: {R_NATURAL:.4f} Å")
    print()

    # Run screens against all default targets
    all_results = {}

    for target_name in DEFAULT_TARGETS.keys():
        print(f"\n{'='*70}")
        print(f"SCREENING: {target_name}")
        print("=" * 70)

        candidates = run_repurposing_screen(
            target_name=target_name,
            max_drugs=100,  # Use 500+ for comprehensive screen
            n_workers=4
        )

        if candidates:
            all_results[target_name] = candidates
            print_top_candidates(candidates, n=10)

    # Save all results
    output_dir = Path(__file__).parent / "results"

    for target_name, candidates in all_results.items():
        json_path, csv_path = save_results(candidates, target_name, output_dir)
        print(f"  Saved: {json_path.name}")
        print(f"  Saved: {csv_path.name}")

    # Summary
    print()
    print("=" * 70)
    print("GEOMETRIC REPURPOSING SCREEN COMPLETE")
    print("=" * 70)
    print()
    print("Summary by target:")
    for target_name, candidates in all_results.items():
        if candidates:
            top = candidates[0]
            print(f"  {target_name}:")
            print(f"    Top candidate: {top.name} ({top.chembl_id})")
            print(f"    Combined score: {top.combined_score:.4f}")
    print()
    print("DISCLAIMER: Computational predictions only. Requires experimental validation.")
    print("=" * 70)

    return all_results


if __name__ == "__main__":
    main()

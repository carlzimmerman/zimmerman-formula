#!/usr/bin/env python3
"""
analysis_z2_hotspots.py - Atomic-Resolution Z² Hotspot Mapping

Identifies the specific atoms and residues causing Z² enrichment in
protein binding sites. Generates pharmacophore positioning constraints.

Key Questions Answered:
1. Which atoms surround Z²-scale voids?
2. Which residues show highest Z² density?
3. Where should Trp/Tyr/Phe anchors be positioned?
4. What is the "geometric fingerprint" of the binding site?

Output:
- Atom-level Z² contact map
- Residue-level Z² density ranking
- Pharmacophore anchor positioning constraints
- 3D coordinates for optimal drug placement

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set, Optional
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z2_VACUUM = 5.788810036466141
Z2_BIOLOGICAL = 6.015152508891966
Z2_OBSERVED = 6.423  # Mean from empirical data

# Alpha radius for Z² scale voids
ALPHA_Z2 = Z2_BIOLOGICAL / 2  # ~3.0 Å

# Binding site residues for Oxytocin Receptor (from 6TPK crystal structure)
OXTR_BINDING_RESIDUES = {
    # TM2-TM3 interface
    91, 92, 95, 98, 99,
    115, 119, 122, 123,
    # ECL2 (critical for peptide recognition)
    199, 200, 203, 204, 207,
    # TM5-TM6 interface
    209, 213, 216,
    290, 291, 294, 295,
    # TM7
    309, 312, 313, 316,
}

# Binding site residues for HIV Protease (from 1HHP crystal structure)
# HIV Protease is a homodimer - residues apply to both chains A and B
HIV_PROTEASE_BINDING_RESIDUES = {
    # Catalytic dyad
    25,  # Asp25/Asp25' (catalytic aspartates)
    # Flap region (critical for substrate access)
    47, 48, 49, 50, 51, 52, 53, 54,
    # S1/S1' substrate pocket
    8, 23, 27, 28, 29, 30, 32,
    # S2/S2' pocket
    47, 48, 84, 82,
    # Additional active site residues
    76, 80, 81, 84,
}

# Tau PHF6 fibril interface residues (Tau 306-378 from 5O3L cryo-EM structure)
# Focus on the aggregation-prone region centered on PHF6 (306-311)
TAU_PHF6_BINDING_RESIDUES = {
    # PHF6 motif core (306-311) - PRIMARY TARGET
    306, 307, 308, 309, 310, 311,
    # Extended aggregation interface
    312, 313, 314, 315, 316, 317, 318, 319, 320,
    # Steric zipper region
    321, 322, 323, 324, 325, 326, 327, 328, 329, 330,
    # C-terminal extension
    331, 332, 333, 334, 335, 336, 337, 338, 339, 340,
    # Additional fibril interface
    341, 342, 343, 344, 345, 346, 347, 348, 349, 350,
    351, 352, 353, 354, 355, 356, 357, 358, 359, 360,
    361, 362, 363, 364, 365, 366, 367, 368, 369, 370,
    371, 372, 373, 374, 375, 376, 377, 378,
}

# Target-specific binding site lookup
BINDING_SITE_RESIDUES = {
    'P30559': OXTR_BINDING_RESIDUES,  # Oxytocin Receptor
    'P04585': HIV_PROTEASE_BINDING_RESIDUES,  # HIV Protease (1HHP)
    'P04578': HIV_PROTEASE_BINDING_RESIDUES,  # HIV gp120 (use same as protease for now)
    'P10636': TAU_PHF6_BINDING_RESIDUES,  # Tau protein (5O3L)
    'TAU_PHF': TAU_PHF6_BINDING_RESIDUES,  # Alias for Tau
}

# Global variable for current target's binding residues (set at runtime)
CURRENT_BINDING_RESIDUES = OXTR_BINDING_RESIDUES

# Residue classifications
AROMATIC = {'PHE', 'TYR', 'TRP', 'HIS'}
HYDROPHOBIC = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO'}
POLAR = {'SER', 'THR', 'ASN', 'GLN', 'TYR', 'CYS'}
CHARGED_POS = {'LYS', 'ARG', 'HIS'}
CHARGED_NEG = {'ASP', 'GLU'}

# Van der Waals radii
VDW = {'C': 1.70, 'N': 1.55, 'O': 1.52, 'S': 1.80, 'H': 1.20}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Atom:
    """Atom with full metadata."""
    serial: int
    name: str
    resname: str
    chain: str
    resseq: int
    x: float
    y: float
    z: float
    element: str

    def coords(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def residue_id(self) -> str:
        return f"{self.resname}{self.resseq}{self.chain}"

    def is_binding_site(self) -> bool:
        return self.resseq in CURRENT_BINDING_RESIDUES

    def residue_class(self) -> str:
        if self.resname in AROMATIC:
            return 'AROMATIC'
        elif self.resname in CHARGED_POS:
            return 'POSITIVE'
        elif self.resname in CHARGED_NEG:
            return 'NEGATIVE'
        elif self.resname in POLAR:
            return 'POLAR'
        elif self.resname in HYDROPHOBIC:
            return 'HYDROPHOBIC'
        else:
            return 'OTHER'


@dataclass
class Z2Void:
    """A Z²-scale void with surrounding atom data."""
    center: Tuple[float, float, float]
    radius: float
    surrounding_atoms: List[int]  # Atom indices
    surrounding_residues: Set[str]
    is_binding_site: bool
    z2_deviation: float  # How close to exact Z²


@dataclass
class ResidueZ2Profile:
    """Z² contact profile for a single residue."""
    resseq: int
    resname: str
    chain: str
    n_z2_contacts: int
    z2_density: float  # Z² contacts per atom
    mean_z2_distance: float
    is_binding_site: bool
    residue_class: str
    contributing_atoms: List[str]


@dataclass
class Z2Hotspot:
    """A concentrated region of Z² geometry."""
    center: Tuple[float, float, float]
    radius: float
    z2_void_count: int
    z2_density: float
    key_residues: List[str]
    pharmacophore_recommendation: str


@dataclass
class HotspotReport:
    """Complete Z² hotspot analysis report."""
    timestamp: str
    pdb_id: str
    uniprot_id: str

    # Void analysis
    n_total_voids: int
    n_z2_voids: int
    n_binding_site_z2_voids: int

    # Atom-level data
    top_z2_atoms: List[Dict]

    # Residue-level data
    residue_profiles: List[ResidueZ2Profile]
    top_z2_residues: List[str]

    # Hotspots
    hotspots: List[Z2Hotspot]

    # Pharmacophore constraints
    anchor_positions: List[Dict]

    summary: str


# =============================================================================
# PDB PARSING
# =============================================================================

def parse_pdb(pdb_path: Path) -> List[Atom]:
    """Parse atoms from PDB file."""
    atoms = []
    content = pdb_path.read_text()

    for line in content.split('\n'):
        if line.startswith('ATOM'):
            try:
                atom = Atom(
                    serial=int(line[6:11].strip()),
                    name=line[12:16].strip(),
                    resname=line[17:20].strip(),
                    chain=line[21].strip() or 'A',
                    resseq=int(line[22:26].strip()),
                    x=float(line[30:38].strip()),
                    y=float(line[38:46].strip()),
                    z=float(line[46:54].strip()),
                    element=line[76:78].strip() if len(line) > 76 else 'C'
                )
                atoms.append(atom)
            except (ValueError, IndexError):
                continue

    return atoms


def distance(p1: Tuple, p2: Tuple) -> float:
    """Euclidean distance."""
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))


# =============================================================================
# Z² VOID DETECTION (HIGH RESOLUTION)
# =============================================================================

def find_z2_voids_highres(atoms: List[Atom],
                          grid_spacing: float = 1.5,
                          z2_tolerance: float = 0.4) -> List[Z2Void]:
    """
    High-resolution Z² void detection.

    Focuses specifically on voids at Z² scale (α ≈ 3.0 Å).
    """
    voids = []

    # Bounding box
    xs = [a.x for a in atoms]
    ys = [a.y for a in atoms]
    zs = [a.z for a in atoms]

    min_x, max_x = min(xs) - 3, max(xs) + 3
    min_y, max_y = min(ys) - 3, max(ys) + 3
    min_z, max_z = min(zs) - 3, max(zs) + 3

    # Precompute binding site atoms
    binding_atoms = {i for i, a in enumerate(atoms) if a.is_binding_site()}

    print(f"    Grid spacing: {grid_spacing} Å")
    print(f"    Z² target radius: {ALPHA_Z2:.3f} Å (±{z2_tolerance} Å)")

    x_steps = int((max_x - min_x) / grid_spacing)
    y_steps = int((max_y - min_y) / grid_spacing)
    z_steps = int((max_z - min_z) / grid_spacing)
    total_points = x_steps * y_steps * z_steps

    print(f"    Scanning {total_points:,} grid points...", flush=True)

    checked = 0
    for ix in range(x_steps):
        px = min_x + ix * grid_spacing
        for iy in range(y_steps):
            py = min_y + iy * grid_spacing
            for iz in range(z_steps):
                pz = min_z + iz * grid_spacing
                point = (px, py, pz)
                checked += 1

                # Find distance to nearest atom surface
                min_surface_dist = float('inf')
                nearby_atoms = []
                nearby_binding = False

                for i, atom in enumerate(atoms):
                    vdw_r = VDW.get(atom.element, 1.7)
                    dist_to_surface = distance(point, atom.coords()) - vdw_r

                    if dist_to_surface < min_surface_dist:
                        min_surface_dist = dist_to_surface

                    # Track nearby atoms
                    if dist_to_surface < ALPHA_Z2 + 1.5:
                        nearby_atoms.append(i)
                        if i in binding_atoms:
                            nearby_binding = True

                # Check if this is a Z² void
                z2_dev = abs(min_surface_dist - ALPHA_Z2)
                if z2_dev < z2_tolerance:
                    nearby_residues = {atoms[i].residue_id() for i in nearby_atoms}

                    void = Z2Void(
                        center=point,
                        radius=min_surface_dist,
                        surrounding_atoms=nearby_atoms,
                        surrounding_residues=nearby_residues,
                        is_binding_site=nearby_binding,
                        z2_deviation=z2_dev
                    )
                    voids.append(void)

    print(f"    Found {len(voids)} Z² voids")
    return voids


# =============================================================================
# ATOM-LEVEL Z² ANALYSIS
# =============================================================================

def analyze_atom_z2_contacts(atoms: List[Atom],
                             voids: List[Z2Void]) -> Dict[int, Dict]:
    """
    Count Z² contacts for each atom.

    An atom has a "Z² contact" if it borders a Z²-scale void.
    """
    atom_contacts = defaultdict(lambda: {
        'n_contacts': 0,
        'voids': [],
        'mean_deviation': 0,
        'is_binding_site': False
    })

    for void in voids:
        for atom_idx in void.surrounding_atoms:
            atom_contacts[atom_idx]['n_contacts'] += 1
            atom_contacts[atom_idx]['voids'].append(void.z2_deviation)
            atom_contacts[atom_idx]['is_binding_site'] = atoms[atom_idx].is_binding_site()

    # Calculate mean deviation
    for idx, data in atom_contacts.items():
        if data['voids']:
            data['mean_deviation'] = sum(data['voids']) / len(data['voids'])

    return dict(atom_contacts)


def get_top_z2_atoms(atoms: List[Atom],
                     atom_contacts: Dict[int, Dict],
                     top_n: int = 30) -> List[Dict]:
    """Get atoms with most Z² contacts."""
    ranked = []

    for idx, data in atom_contacts.items():
        atom = atoms[idx]
        ranked.append({
            'atom_idx': idx,
            'atom_name': atom.name,
            'residue': atom.residue_id(),
            'resseq': atom.resseq,
            'resname': atom.resname,
            'n_z2_contacts': data['n_contacts'],
            'mean_deviation': data['mean_deviation'],
            'is_binding_site': data['is_binding_site'],
            'residue_class': atom.residue_class(),
            'coords': atom.coords()
        })

    ranked.sort(key=lambda x: x['n_z2_contacts'], reverse=True)
    return ranked[:top_n]


# =============================================================================
# RESIDUE-LEVEL Z² ANALYSIS
# =============================================================================

def analyze_residue_z2_profiles(atoms: List[Atom],
                                atom_contacts: Dict[int, Dict]) -> List[ResidueZ2Profile]:
    """
    Build Z² profiles for each residue.
    """
    residue_data = defaultdict(lambda: {
        'atoms': [],
        'contacts': 0,
        'deviations': [],
        'resname': '',
        'chain': '',
        'is_binding_site': False
    })

    for idx, data in atom_contacts.items():
        atom = atoms[idx]
        key = (atom.resseq, atom.chain)
        residue_data[key]['atoms'].append(atom.name)
        residue_data[key]['contacts'] += data['n_contacts']
        residue_data[key]['deviations'].extend(data['voids'])
        residue_data[key]['resname'] = atom.resname
        residue_data[key]['chain'] = atom.chain
        residue_data[key]['is_binding_site'] = atom.is_binding_site()

    profiles = []
    for (resseq, chain), data in residue_data.items():
        n_atoms = len(data['atoms'])
        mean_dev = sum(data['deviations']) / len(data['deviations']) if data['deviations'] else 0

        profile = ResidueZ2Profile(
            resseq=resseq,
            resname=data['resname'],
            chain=chain,
            n_z2_contacts=data['contacts'],
            z2_density=data['contacts'] / max(1, n_atoms),
            mean_z2_distance=ALPHA_Z2 * 2 + mean_dev,  # Convert to full distance
            is_binding_site=data['is_binding_site'],
            residue_class=atoms[0].residue_class() if atoms else 'OTHER',
            contributing_atoms=data['atoms']
        )
        profiles.append(profile)

    # Sort by Z² contact count
    profiles.sort(key=lambda x: x.n_z2_contacts, reverse=True)
    return profiles


# =============================================================================
# HOTSPOT CLUSTERING
# =============================================================================

def cluster_z2_hotspots(voids: List[Z2Void],
                        cluster_radius: float = 5.0) -> List[Z2Hotspot]:
    """
    Cluster Z² voids into hotspots.

    A hotspot is a region with concentrated Z² geometry.
    """
    if not voids:
        return []

    # Simple greedy clustering
    used = set()
    hotspots = []

    # Sort by binding site priority
    sorted_voids = sorted(voids, key=lambda v: (not v.is_binding_site, v.z2_deviation))

    for i, seed in enumerate(sorted_voids):
        if i in used:
            continue

        cluster_voids = [seed]
        cluster_residues = set(seed.surrounding_residues)
        used.add(i)

        # Find nearby voids
        for j, other in enumerate(sorted_voids):
            if j in used:
                continue
            if distance(seed.center, other.center) < cluster_radius:
                cluster_voids.append(other)
                cluster_residues.update(other.surrounding_residues)
                used.add(j)

        if len(cluster_voids) >= 3:  # Minimum cluster size
            # Calculate cluster center
            cx = sum(v.center[0] for v in cluster_voids) / len(cluster_voids)
            cy = sum(v.center[1] for v in cluster_voids) / len(cluster_voids)
            cz = sum(v.center[2] for v in cluster_voids) / len(cluster_voids)

            # Determine recommendation
            n_binding = sum(1 for v in cluster_voids if v.is_binding_site)
            binding_fraction = n_binding / len(cluster_voids)

            if binding_fraction > 0.7:
                rec = "PRIMARY ANCHOR: Position Trp/Tyr here for optimal binding"
            elif binding_fraction > 0.4:
                rec = "SECONDARY ANCHOR: Good position for Phe/Tyr"
            else:
                rec = "PERIPHERAL: Consider for extended pharmacophore"

            hotspot = Z2Hotspot(
                center=(cx, cy, cz),
                radius=cluster_radius,
                z2_void_count=len(cluster_voids),
                z2_density=len(cluster_voids) / (4/3 * math.pi * cluster_radius**3),
                key_residues=list(cluster_residues)[:10],
                pharmacophore_recommendation=rec
            )
            hotspots.append(hotspot)

    # Sort by void count
    hotspots.sort(key=lambda h: h.z2_void_count, reverse=True)
    return hotspots


# =============================================================================
# PHARMACOPHORE ANCHOR GENERATION
# =============================================================================

def generate_anchor_positions(hotspots: List[Z2Hotspot],
                              atoms: List[Atom]) -> List[Dict]:
    """
    Generate optimal positions for aromatic anchors.

    Based on Z² hotspot analysis, identify where to place
    Trp/Tyr/Phe sidechains for maximum Z² contact.
    """
    anchors = []

    for i, hotspot in enumerate(hotspots[:5]):  # Top 5 hotspots
        # Find nearest protein atoms
        nearest_atoms = []
        for atom in atoms:
            d = distance(hotspot.center, atom.coords())
            if d < hotspot.radius + 2:
                nearest_atoms.append({
                    'name': atom.name,
                    'residue': atom.residue_id(),
                    'distance': d,
                    'class': atom.residue_class()
                })

        nearest_atoms.sort(key=lambda x: x['distance'])

        anchor = {
            'anchor_id': f"Z2-ANCHOR-{i+1:02d}",
            'position': hotspot.center,
            'z2_void_count': hotspot.z2_void_count,
            'recommended_residue': 'TRP' if hotspot.z2_void_count > 10 else 'TYR',
            'nearby_protein_atoms': nearest_atoms[:5],
            'key_interactions': hotspot.key_residues[:5],
            'recommendation': hotspot.pharmacophore_recommendation
        }
        anchors.append(anchor)

    return anchors


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_hotspot_analysis(pdb_path: str,
                         pdb_id: str = "6TPK",
                         uniprot_id: str = "P30559",
                         output_dir: str = "../z2_hotspots") -> HotspotReport:
    """
    Complete Z² hotspot analysis.
    """
    global CURRENT_BINDING_RESIDUES

    # Set binding site residues based on target
    if uniprot_id in BINDING_SITE_RESIDUES:
        CURRENT_BINDING_RESIDUES = BINDING_SITE_RESIDUES[uniprot_id]
    else:
        # Default to HIV protease residues for unknown targets
        CURRENT_BINDING_RESIDUES = HIV_PROTEASE_BINDING_RESIDUES

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Z² HOTSPOT ANALYSIS - ATOMIC RESOLUTION")
    print("=" * 70)
    print(f"    Target: {uniprot_id} (PDB: {pdb_id})")
    print(f"    Z² Distance: {Z2_BIOLOGICAL:.6f} Å")
    print(f"    Z² Void Radius: {ALPHA_Z2:.3f} Å")
    print(f"    Binding site residues: {len(CURRENT_BINDING_RESIDUES)}")
    print()

    # Load structure
    pdb_file = Path(pdb_path)
    if not pdb_file.exists():
        # Try to find in manifold analysis directory
        pdb_file = Path(f"../manifold_analysis/pdb_structures/{pdb_id}.pdb")

    if not pdb_file.exists():
        print(f"    ERROR: PDB file not found: {pdb_path}")
        return None

    atoms = parse_pdb(pdb_file)
    protein_atoms = [a for a in atoms if a.resname not in ['HOH', 'WAT', 'NA', 'CL']]
    binding_atoms = [a for a in protein_atoms if a.is_binding_site()]

    print(f"  [1/5] Loaded structure")
    print(f"    Total atoms: {len(protein_atoms)}")
    print(f"    Binding site atoms: {len(binding_atoms)}")
    print(f"    Binding site residues: {len(OXTR_BINDING_RESIDUES)}")

    # High-resolution void detection
    print(f"\n  [2/5] Z² void detection (high resolution)...")
    voids = find_z2_voids_highres(protein_atoms, grid_spacing=1.5)

    binding_voids = [v for v in voids if v.is_binding_site]
    print(f"    Z² voids in binding site: {len(binding_voids)}/{len(voids)} ({100*len(binding_voids)/max(1,len(voids)):.1f}%)")

    # Atom-level analysis
    print(f"\n  [3/5] Atom-level Z² contact analysis...")
    atom_contacts = analyze_atom_z2_contacts(protein_atoms, voids)
    top_atoms = get_top_z2_atoms(protein_atoms, atom_contacts, top_n=30)

    print(f"    Atoms with Z² contacts: {len(atom_contacts)}")
    print(f"\n    TOP 10 Z² ATOMS:")
    print(f"    {'Rank':<6}{'Atom':<8}{'Residue':<12}{'Contacts':<10}{'Site':<8}")
    print(f"    {'-'*44}")
    for i, atom in enumerate(top_atoms[:10]):
        site = "✓ BIND" if atom['is_binding_site'] else ""
        print(f"    {i+1:<6}{atom['atom_name']:<8}{atom['residue']:<12}{atom['n_z2_contacts']:<10}{site}")

    # Residue-level analysis
    print(f"\n  [4/5] Residue-level Z² profile analysis...")
    residue_profiles = analyze_residue_z2_profiles(protein_atoms, atom_contacts)

    print(f"\n    TOP 15 Z² RESIDUES:")
    print(f"    {'Rank':<6}{'Residue':<12}{'Type':<12}{'Z² Contacts':<12}{'Density':<10}{'Site':<8}")
    print(f"    {'-'*60}")
    for i, profile in enumerate(residue_profiles[:15]):
        site = "✓ BIND" if profile.is_binding_site else ""
        print(f"    {i+1:<6}{profile.resname}{profile.resseq:<9}{profile.residue_class:<12}{profile.n_z2_contacts:<12}{profile.z2_density:.2f}{'':<6}{site}")

    # Hotspot clustering
    print(f"\n  [5/5] Z² hotspot clustering...")
    hotspots = cluster_z2_hotspots(voids, cluster_radius=4.0)

    print(f"    Identified {len(hotspots)} Z² hotspots")
    print(f"\n    TOP 5 Z² HOTSPOTS:")
    print(f"    {'ID':<6}{'Voids':<8}{'Key Residues':<40}{'Recommendation'}")
    print(f"    {'-'*80}")
    for i, hs in enumerate(hotspots[:5]):
        res_str = ', '.join(hs.key_residues[:4])
        print(f"    {i+1:<6}{hs.z2_void_count:<8}{res_str:<40}{hs.pharmacophore_recommendation[:30]}")

    # Generate anchor positions
    anchors = generate_anchor_positions(hotspots, protein_atoms)

    # Build report
    top_residue_ids = [f"{p.resname}{p.resseq}" for p in residue_profiles[:10]]

    # Calculate enrichment
    binding_z2 = len(binding_voids)
    total_z2 = len(voids)
    binding_fraction = len(binding_atoms) / len(protein_atoms)
    expected_binding_z2 = total_z2 * binding_fraction
    enrichment = binding_z2 / max(1, expected_binding_z2)

    summary = f"Z² enrichment in binding site: {enrichment:.1f}x expected. Top hotspots concentrated at residues: {', '.join(top_residue_ids[:5])}"

    report = HotspotReport(
        timestamp=datetime.now().isoformat(),
        pdb_id=pdb_id,
        uniprot_id=uniprot_id,
        n_total_voids=len(voids),
        n_z2_voids=len(voids),
        n_binding_site_z2_voids=len(binding_voids),
        top_z2_atoms=top_atoms,
        residue_profiles=residue_profiles,
        top_z2_residues=top_residue_ids,
        hotspots=hotspots,
        anchor_positions=anchors,
        summary=summary
    )

    # Print final summary
    print()
    print("=" * 70)
    print("Z² HOTSPOT ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"    Total Z² voids: {len(voids)}")
    print(f"    Binding site Z² voids: {len(binding_voids)} ({100*len(binding_voids)/max(1,len(voids)):.1f}%)")
    print(f"    Z² enrichment factor: {enrichment:.2f}x")
    print()
    print(f"    KEY BINDING RESIDUES (by Z² contact count):")

    # Show binding site residues only
    binding_profiles = [p for p in residue_profiles if p.is_binding_site]
    for i, p in enumerate(binding_profiles[:10]):
        print(f"      {i+1}. {p.resname}{p.resseq} ({p.residue_class}): {p.n_z2_contacts} Z² contacts")

    print()
    print(f"    PHARMACOPHORE ANCHOR RECOMMENDATIONS:")
    for anchor in anchors[:3]:
        print(f"      {anchor['anchor_id']}: Place {anchor['recommended_residue']} at {anchor['position'][0]:.1f}, {anchor['position'][1]:.1f}, {anchor['position'][2]:.1f}")
        print(f"         → {anchor['recommendation']}")

    print("=" * 70)

    # Save results
    output_file = output_path / f"z2_hotspots_{uniprot_id}.json"

    report_dict = {
        'timestamp': report.timestamp,
        'pdb_id': report.pdb_id,
        'uniprot_id': report.uniprot_id,
        'z2_constants': {
            'vacuum': Z2_VACUUM,
            'biological': Z2_BIOLOGICAL,
            'void_radius': ALPHA_Z2
        },
        'void_analysis': {
            'total_z2_voids': report.n_total_voids,
            'binding_site_z2_voids': report.n_binding_site_z2_voids,
            'enrichment_factor': enrichment
        },
        'top_z2_atoms': report.top_z2_atoms[:20],
        'top_z2_residues': [
            {
                'residue': f"{p.resname}{p.resseq}",
                'n_contacts': p.n_z2_contacts,
                'density': p.z2_density,
                'is_binding_site': p.is_binding_site,
                'class': p.residue_class
            }
            for p in report.residue_profiles[:20]
        ],
        'hotspots': [
            {
                'center': h.center,
                'z2_void_count': h.z2_void_count,
                'key_residues': h.key_residues,
                'recommendation': h.pharmacophore_recommendation
            }
            for h in report.hotspots[:10]
        ],
        'anchor_positions': report.anchor_positions,
        'summary': report.summary
    }

    with open(output_file, 'w') as f:
        json.dump(report_dict, f, indent=2)

    print(f"\n    Saved: {output_file}")

    return report


# =============================================================================
# CLI
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Z² Hotspot Analysis - Atomic Resolution"
    )
    parser.add_argument('--pdb', default='../manifold_analysis/pdb_structures/6TPK.pdb',
                       help='Path to PDB file')
    parser.add_argument('--pdb-id', default='6TPK', help='PDB ID')
    parser.add_argument('--uniprot', default='P30559', help='UniProt ID')
    parser.add_argument('--output', default='../z2_hotspots', help='Output directory')

    args = parser.parse_args()

    run_hotspot_analysis(
        pdb_path=args.pdb,
        pdb_id=args.pdb_id,
        uniprot_id=args.uniprot,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()

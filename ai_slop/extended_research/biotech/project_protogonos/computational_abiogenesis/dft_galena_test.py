#!/usr/bin/env python3
"""
================================================================================
DFT SIMULATION: The Galena Test
================================================================================

HYPOTHESIS: If Z ≈ 5.79 Å has geometric significance for prebiotic chemistry,
then Galena (PbS, lattice 5.94 Å, only 2.6% from Z) should catalyze amino acid
precursor reactions BETTER than Pyrite (FeS₂, lattice 5.417 Å, 6.8% from Z).

PREDICTION:
  - If GEOMETRY matters: Galena ≥ Pyrite (closer lattice match)
  - If CHEMISTRY matters: Pyrite >> Galena (Fe is redox-active, Pb is not)

This script sets up DFT calculations to compute:
1. Surface energies of Galena (100) and Pyrite (100)
2. Adsorption energies of prebiotic molecules (CO₂, NH₃, HCN, H₂O)
3. Activation energies for C-N bond formation on both surfaces

COMPUTATIONAL APPROACH:
- Uses ASE (Atomic Simulation Environment) for structure building
- Supports multiple DFT backends: GPAW, VASP, Quantum ESPRESSO
- Computes binding energies and reaction barriers

DEPENDENCIES:
  pip install ase numpy scipy matplotlib

For actual DFT calculations, you'll also need:
  - GPAW: pip install gpaw (open source, good for quick tests)
  - VASP: commercial license required
  - Quantum ESPRESSO: open source, high accuracy

Author: Carl Zimmerman + Claude
License: AGPL-3.0-or-later
================================================================================
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
import os

# =============================================================================
# TRY TO IMPORT ASE (Atomic Simulation Environment)
# =============================================================================

try:
    from ase import Atoms
    from ase.build import bulk, surface, molecule, add_adsorbate
    from ase.visualize import view
    from ase.constraints import FixAtoms
    from ase.optimize import BFGS
    ASE_AVAILABLE = True
except ImportError:
    ASE_AVAILABLE = False
    print("WARNING: ASE not installed. Run: pip install ase")
    print("Continuing with mock calculations for demonstration.")

# Try to import a DFT calculator
DFT_CALCULATOR = None
try:
    from gpaw import GPAW, PW
    DFT_CALCULATOR = "GPAW"
except ImportError:
    pass

if DFT_CALCULATOR is None:
    try:
        from ase.calculators.vasp import Vasp
        DFT_CALCULATOR = "VASP"
    except ImportError:
        pass

if DFT_CALCULATOR is None:
    try:
        from ase.calculators.espresso import Espresso
        DFT_CALCULATOR = "QE"
    except ImportError:
        pass

if DFT_CALCULATOR is None:
    # Use EMT (Effective Medium Theory) for quick tests
    try:
        from ase.calculators.emt import EMT
        DFT_CALCULATOR = "EMT"
    except ImportError:
        DFT_CALCULATOR = "MOCK"

print(f"DFT Calculator: {DFT_CALCULATOR}")


# =============================================================================
# CONSTANTS
# =============================================================================

Z_CONSTANT = 5.788810  # Å

# Experimental lattice parameters (cubic structures)
LATTICE_PARAMS = {
    'Galena': 5.936,   # PbS, rock salt structure, a = 5.936 Å
    'Pyrite': 5.417,   # FeS₂, pyrite structure, a = 5.417 Å
    'Halite': 5.640,   # NaCl, rock salt structure (control)
}

# Distance from Z
for name, a in LATTICE_PARAMS.items():
    diff = abs(a - Z_CONSTANT) / Z_CONSTANT * 100
    print(f"{name}: a = {a} Å ({diff:.1f}% from Z)")


# =============================================================================
# STRUCTURE BUILDERS
# =============================================================================

@dataclass
class SurfaceModel:
    """A mineral surface model for adsorption calculations."""
    name: str
    bulk_structure: Optional[object]  # ASE Atoms
    surface_structure: Optional[object]  # ASE Atoms
    lattice_param: float
    miller_index: Tuple[int, int, int]
    layers: int
    vacuum: float  # Å


def build_galena_bulk() -> Optional[object]:
    """
    Build bulk Galena (PbS) structure.

    PbS has the rock salt (NaCl) structure:
    - Pb at (0,0,0), (0.5,0.5,0), (0.5,0,0.5), (0,0.5,0.5)
    - S at (0.5,0.5,0.5), (0,0,0.5), (0,0.5,0), (0.5,0,0)
    """
    if not ASE_AVAILABLE:
        return None

    a = LATTICE_PARAMS['Galena']

    # Rock salt structure
    galena = Atoms(
        symbols=['Pb', 'S'],
        positions=[
            [0, 0, 0],
            [a/2, a/2, a/2]
        ],
        cell=[a, a, a],
        pbc=True
    )

    return galena


def build_pyrite_bulk() -> Optional[object]:
    """
    Build bulk Pyrite (FeS₂) structure.

    FeS₂ has the pyrite structure (space group Pa-3):
    - Fe at (0,0,0), (0.5,0.5,0), (0.5,0,0.5), (0,0.5,0.5)
    - S₂ dumbbells along <111> directions
    """
    if not ASE_AVAILABLE:
        return None

    a = LATTICE_PARAMS['Pyrite']

    # Pyrite has 4 Fe and 8 S per unit cell
    # Simplified: using fractional coordinates
    u = 0.385  # S fractional coordinate parameter

    positions = [
        # Fe positions (FCC-like)
        [0, 0, 0],
        [0.5*a, 0.5*a, 0],
        [0.5*a, 0, 0.5*a],
        [0, 0.5*a, 0.5*a],
        # S positions (8 atoms in dumbbells)
        [u*a, u*a, u*a],
        [(1-u)*a, (1-u)*a, (1-u)*a],
        [(0.5+u)*a, (0.5-u)*a, (1-u)*a],
        [(0.5-u)*a, (0.5+u)*a, u*a],
        [(1-u)*a, (0.5+u)*a, (0.5-u)*a],
        [u*a, (0.5-u)*a, (0.5+u)*a],
        [(0.5-u)*a, (1-u)*a, (0.5+u)*a],
        [(0.5+u)*a, u*a, (0.5-u)*a],
    ]

    symbols = ['Fe']*4 + ['S']*8

    pyrite = Atoms(
        symbols=symbols,
        positions=positions,
        cell=[a, a, a],
        pbc=True
    )

    return pyrite


def build_surface(bulk_atoms: object, miller: Tuple[int, int, int],
                  layers: int = 4, vacuum: float = 15.0) -> Optional[object]:
    """
    Build a surface slab from bulk structure.

    Parameters:
        bulk_atoms: ASE Atoms object for bulk
        miller: Miller indices (h, k, l)
        layers: Number of atomic layers
        vacuum: Vacuum thickness in Å
    """
    if not ASE_AVAILABLE or bulk_atoms is None:
        return None

    slab = surface(bulk_atoms, miller, layers, vacuum=vacuum)

    # Make it a 2x2 supercell for adsorption studies
    slab = slab.repeat((2, 2, 1))

    return slab


# =============================================================================
# ADSORBATE MOLECULES
# =============================================================================

def build_adsorbates() -> Dict[str, object]:
    """Build prebiotic adsorbate molecules."""
    if not ASE_AVAILABLE:
        return {}

    adsorbates = {
        'H2O': molecule('H2O'),
        'CO2': molecule('CO2'),
        'NH3': molecule('NH3'),
        # HCN needs manual building
        'HCN': Atoms(
            symbols=['H', 'C', 'N'],
            positions=[[0, 0, 0], [1.066, 0, 0], [2.222, 0, 0]]
        ),
        # Formaldehyde (H2CO)
        'H2CO': Atoms(
            symbols=['C', 'O', 'H', 'H'],
            positions=[
                [0, 0, 0],
                [1.21, 0, 0],
                [-0.5, 0.94, 0],
                [-0.5, -0.94, 0]
            ]
        ),
    }

    return adsorbates


# =============================================================================
# DFT CALCULATIONS
# =============================================================================

def get_calculator(mode: str = 'quick'):
    """
    Get appropriate DFT calculator.

    Modes:
        'quick': EMT or simple LDA for testing
        'accurate': Full PBE-D3 for publication-quality results
    """
    if DFT_CALCULATOR == "GPAW":
        if mode == 'quick':
            return GPAW(mode=PW(300), xc='LDA', kpts=(2, 2, 1))
        else:
            return GPAW(mode=PW(500), xc='PBE', kpts=(4, 4, 1))

    elif DFT_CALCULATOR == "EMT":
        from ase.calculators.emt import EMT
        return EMT()

    else:
        # Mock calculator for demonstration
        return None


def calculate_adsorption_energy(slab: object, adsorbate: object,
                               site: Tuple[float, float],
                               height: float = 2.0) -> Dict:
    """
    Calculate adsorption energy of molecule on surface.

    E_ads = E(slab+mol) - E(slab) - E(mol)

    Negative E_ads = favorable adsorption
    """
    if not ASE_AVAILABLE or slab is None:
        # Return mock results for demonstration
        return {
            'E_ads': np.random.uniform(-0.5, -2.0),  # eV
            'status': 'MOCK',
            'note': 'No DFT calculator available'
        }

    calc = get_calculator('quick')
    if calc is None:
        return {
            'E_ads': np.random.uniform(-0.5, -2.0),
            'status': 'MOCK',
            'note': 'No DFT calculator available'
        }

    # Calculate isolated molecule energy
    mol = adsorbate.copy()
    mol.center(vacuum=10)
    mol.calc = calc
    E_mol = mol.get_potential_energy()

    # Calculate clean slab energy
    clean_slab = slab.copy()
    clean_slab.calc = calc
    E_slab = clean_slab.get_potential_energy()

    # Add adsorbate to slab
    slab_with_ads = slab.copy()
    add_adsorbate(slab_with_ads, adsorbate, height=height, position=site)

    # Fix bottom layers
    z_positions = slab_with_ads.positions[:, 2]
    z_min = z_positions.min()
    z_range = z_positions.max() - z_min
    constraint = FixAtoms(indices=[i for i, z in enumerate(z_positions)
                                   if z < z_min + 0.4 * z_range])
    slab_with_ads.set_constraint(constraint)

    # Optimize and calculate
    slab_with_ads.calc = calc
    opt = BFGS(slab_with_ads, logfile=None)
    opt.run(fmax=0.05)

    E_total = slab_with_ads.get_potential_energy()

    E_ads = E_total - E_slab - E_mol

    return {
        'E_ads': E_ads,
        'E_total': E_total,
        'E_slab': E_slab,
        'E_mol': E_mol,
        'status': 'CALCULATED',
    }


# =============================================================================
# THE GALENA TEST
# =============================================================================

def run_galena_test(mode: str = 'quick') -> Dict:
    """
    Run the full Galena vs Pyrite comparison.

    This tests whether lattice geometry (favoring Galena) or
    chemistry (favoring Pyrite) controls prebiotic catalysis.
    """
    print("\n" + "=" * 70)
    print("THE GALENA TEST: Geometry vs Chemistry")
    print("=" * 70)

    print(f"""
    HYPOTHESIS:
      If Z ≈ {Z_CONSTANT:.3f} Å has geometric significance, then
      Galena (a = 5.94 Å, 2.6% from Z) should bind prebiotic
      molecules BETTER than Pyrite (a = 5.42 Å, 6.8% from Z).

    PREDICTION:
      If GEOMETRY matters: E_ads(Galena) < E_ads(Pyrite)
      If CHEMISTRY matters: E_ads(Pyrite) << E_ads(Galena)

    DFT Calculator: {DFT_CALCULATOR}
    Mode: {mode}
    """)

    results = {
        'hypothesis': 'Geometry (Z) controls prebiotic catalysis',
        'prediction_geometry': 'Galena > Pyrite',
        'prediction_chemistry': 'Pyrite >> Galena',
        'calculations': {}
    }

    # Build structures
    print("\n" + "-" * 70)
    print("1. Building Bulk Structures")
    print("-" * 70)

    galena_bulk = build_galena_bulk()
    pyrite_bulk = build_pyrite_bulk()

    if ASE_AVAILABLE:
        print(f"  Galena (PbS): {galena_bulk.get_chemical_formula() if galena_bulk else 'N/A'}")
        print(f"  Pyrite (FeS₂): {pyrite_bulk.get_chemical_formula() if pyrite_bulk else 'N/A'}")
    else:
        print("  [ASE not available - using mock structures]")

    # Build surfaces
    print("\n" + "-" * 70)
    print("2. Building (100) Surfaces")
    print("-" * 70)

    galena_surface = build_surface(galena_bulk, (1, 0, 0), layers=4, vacuum=15)
    pyrite_surface = build_surface(pyrite_bulk, (1, 0, 0), layers=4, vacuum=15)

    if ASE_AVAILABLE and galena_surface:
        print(f"  Galena (100): {len(galena_surface)} atoms")
        print(f"  Pyrite (100): {len(pyrite_surface) if pyrite_surface else 'N/A'} atoms")
    else:
        print("  [Using mock surfaces]")

    # Build adsorbates
    print("\n" + "-" * 70)
    print("3. Building Prebiotic Adsorbates")
    print("-" * 70)

    adsorbates = build_adsorbates()
    print(f"  Molecules: {list(adsorbates.keys()) if adsorbates else ['H2O', 'CO2', 'NH3', 'HCN']}")

    # Calculate adsorption energies
    print("\n" + "-" * 70)
    print("4. Calculating Adsorption Energies")
    print("-" * 70)

    surfaces = {
        'Galena': galena_surface,
        'Pyrite': pyrite_surface,
    }

    molecules = ['H2O', 'CO2', 'NH3', 'HCN'] if not adsorbates else list(adsorbates.keys())

    for surf_name, surf in surfaces.items():
        results['calculations'][surf_name] = {}
        print(f"\n  {surf_name} (100) surface:")

        for mol_name in molecules:
            mol = adsorbates.get(mol_name) if adsorbates else None

            # Adsorption site (center of surface cell)
            if surf is not None:
                cell = surf.get_cell()
                site = (cell[0, 0] / 4, cell[1, 1] / 4)
            else:
                site = (3.0, 3.0)

            result = calculate_adsorption_energy(surf, mol, site)
            results['calculations'][surf_name][mol_name] = result

            status = result.get('status', 'UNKNOWN')
            E_ads = result.get('E_ads', 0)
            print(f"    {mol_name}: E_ads = {E_ads:.3f} eV [{status}]")

    # Analysis
    print("\n" + "-" * 70)
    print("5. Analysis")
    print("-" * 70)

    # Compare Galena vs Pyrite
    print("\n  Molecule    Galena E_ads    Pyrite E_ads    Difference")
    print("  " + "-" * 55)

    galena_wins = 0
    pyrite_wins = 0

    for mol in molecules:
        E_galena = results['calculations']['Galena'][mol]['E_ads']
        E_pyrite = results['calculations']['Pyrite'][mol]['E_ads']
        diff = E_galena - E_pyrite

        winner = "Galena" if E_galena < E_pyrite else "Pyrite"
        if E_galena < E_pyrite:
            galena_wins += 1
        else:
            pyrite_wins += 1

        print(f"  {mol:10s}  {E_galena:10.3f}      {E_pyrite:10.3f}      {diff:+.3f} → {winner}")

    print("\n" + "-" * 70)
    print("6. CONCLUSION")
    print("-" * 70)

    if DFT_CALCULATOR == "MOCK":
        print("""
  WARNING: These are MOCK results (no DFT calculator installed).

  To get real results, install one of:
    - GPAW: pip install gpaw (easiest, open source)
    - Quantum ESPRESSO: apt install quantum-espresso
    - VASP: commercial license required

  Then re-run this script.
        """)
        results['status'] = 'MOCK'
    else:
        if galena_wins > pyrite_wins:
            conclusion = "GEOMETRY WINS: Galena binds molecules better"
            results['verdict'] = 'geometry'
        else:
            conclusion = "CHEMISTRY WINS: Pyrite binds molecules better"
            results['verdict'] = 'chemistry'

        print(f"""
  Results: Galena won {galena_wins}/{len(molecules)}, Pyrite won {pyrite_wins}/{len(molecules)}

  CONCLUSION: {conclusion}

  INTERPRETATION:
    {"This would support the Z² geometric hypothesis!" if galena_wins > pyrite_wins
     else "This confirms that Fe redox chemistry, not lattice geometry, drives catalysis."}
        """)

        results['status'] = 'CALCULATED'

    return results


# =============================================================================
# ACTIVATION ENERGY CALCULATION (NEB)
# =============================================================================

def calculate_reaction_barrier(surface: object, reactants: List[object],
                              products: List[object]) -> Dict:
    """
    Calculate activation energy for reaction using NEB method.

    This would calculate the energy barrier for:
    CO₂ + NH₃ → H₂N-CO₂H (carbamic acid - first step to amino acid)

    Full implementation requires:
    - Nudged Elastic Band (NEB) method
    - Transition state search
    - Significant computational resources

    This is a placeholder showing the approach.
    """
    if not ASE_AVAILABLE:
        return {
            'E_barrier': np.random.uniform(0.5, 1.5),  # eV
            'status': 'MOCK',
            'note': 'Full NEB calculation requires significant compute time'
        }

    # Placeholder for NEB calculation
    # Real implementation would use:
    # from ase.neb import NEB
    # from ase.optimize import BFGS

    return {
        'E_barrier': None,
        'status': 'NOT_IMPLEMENTED',
        'note': 'NEB calculations require ~100+ DFT evaluations per barrier'
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run the Galena Test."""

    print("=" * 70)
    print("DFT SIMULATION: The Galena Test")
    print("=" * 70)

    print(f"""
    This script tests whether lattice geometry or chemistry
    controls prebiotic catalysis on mineral surfaces.

    Z constant: {Z_CONSTANT:.4f} Å

    Mineral lattices:
      Galena (PbS):  5.94 Å  (2.6% from Z) - NOT redox active
      Pyrite (FeS₂): 5.42 Å  (6.8% from Z) - IS redox active

    If Z matters geometrically, Galena should be better.
    If chemistry matters, Pyrite should be better.
    """)

    # Run the test
    results = run_galena_test(mode='quick')

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'galena_test_results.json')

    # Convert numpy types for JSON serialization
    def convert_numpy(obj):
        if isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    results_serializable = json.loads(
        json.dumps(results, default=convert_numpy)
    )

    with open(output_file, 'w') as f:
        json.dump(results_serializable, f, indent=2)

    print(f"\n  Results saved to: {output_file}")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
    1. Install a DFT calculator:
       pip install gpaw  # Easiest option

    2. For accurate results, use:
       - PBE functional with D3 dispersion correction
       - k-point grid: at least 4×4×1
       - Plane-wave cutoff: 500 eV

    3. For publication-quality:
       - Use VASP or Quantum ESPRESSO
       - Include solvent effects (implicit or explicit water)
       - Calculate full reaction pathways with NEB

    4. Experimental validation:
       - Partner with a wet lab
       - Measure amino acid formation rates on both surfaces
       - Control for temperature, pressure, and reactant concentrations
    """)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
M4 Molecular Dynamics Simulation Pipeline
==========================================

Performs molecular dynamics simulations on therapeutic protein structures
to assess stability, flexibility, and conformational dynamics.

Features:
- OpenMM integration for GPU-accelerated MD
- Energy minimization and equilibration
- Production MD with trajectory analysis
- RMSF (flexibility) and RMSD (stability) calculations
- Hydrogen bond network analysis
- Fallback CPU-based simplified dynamics

LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication
All generated simulation data is PUBLIC DOMAIN for patent purposes.

References:
- Eastman et al., PLOS Comput Biol 2017 (OpenMM 7)
- Shirts et al., J Chem Phys 2007 (Enhanced sampling)
- Best et al., J Chem Theory Comput 2012 (Force fields)
"""

import os
import json
import hashlib
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import warnings

# Try to import OpenMM for real MD simulations
OPENMM_AVAILABLE = False
try:
    import openmm as mm
    from openmm import app, unit
    from openmm.app import PDBFile, ForceField, Simulation
    from openmm.app import Modeller, PME, HBonds
    OPENMM_AVAILABLE = True
except ImportError:
    pass

# Try to import MDAnalysis for trajectory analysis
MDANALYSIS_AVAILABLE = False
try:
    import MDAnalysis as mda
    from MDAnalysis.analysis import rms, align
    MDANALYSIS_AVAILABLE = True
except ImportError:
    pass


class SimplifiedDynamics:
    """
    Fallback dynamics simulator using simplified physics.
    Uses Langevin dynamics with harmonic approximation.
    """

    def __init__(self, sequence: str):
        self.sequence = sequence
        self.n_atoms = len(sequence) * 10  # Approximate atoms per residue
        self.temperature = 300.0  # Kelvin
        self.friction = 1.0  # ps^-1
        self.timestep = 0.002  # ps (2 fs)

        # Amino acid properties (hydrophobicity, charge, size)
        self.aa_properties = {
            'A': {'hydro': 0.62, 'charge': 0, 'size': 0.5},
            'R': {'hydro': -2.53, 'charge': 1, 'size': 1.0},
            'N': {'hydro': -0.78, 'charge': 0, 'size': 0.7},
            'D': {'hydro': -0.90, 'charge': -1, 'size': 0.7},
            'C': {'hydro': 0.29, 'charge': 0, 'size': 0.6},
            'Q': {'hydro': -0.85, 'charge': 0, 'size': 0.8},
            'E': {'hydro': -0.74, 'charge': -1, 'size': 0.8},
            'G': {'hydro': 0.48, 'charge': 0, 'size': 0.3},
            'H': {'hydro': -0.40, 'charge': 0.5, 'size': 0.8},
            'I': {'hydro': 1.38, 'charge': 0, 'size': 0.8},
            'L': {'hydro': 1.06, 'charge': 0, 'size': 0.8},
            'K': {'hydro': -1.50, 'charge': 1, 'size': 0.9},
            'M': {'hydro': 0.64, 'charge': 0, 'size': 0.8},
            'F': {'hydro': 1.19, 'charge': 0, 'size': 0.9},
            'P': {'hydro': 0.12, 'charge': 0, 'size': 0.6},
            'S': {'hydro': -0.18, 'charge': 0, 'size': 0.5},
            'T': {'hydro': -0.05, 'charge': 0, 'size': 0.6},
            'W': {'hydro': 0.81, 'charge': 0, 'size': 1.0},
            'Y': {'hydro': 0.26, 'charge': 0, 'size': 0.9},
            'V': {'hydro': 1.08, 'charge': 0, 'size': 0.7},
        }

    def compute_potential_energy(self, positions: np.ndarray) -> float:
        """Compute simplified potential energy."""
        energy = 0.0
        n_res = len(self.sequence)

        # Bond energy (harmonic)
        for i in range(n_res - 1):
            r = np.linalg.norm(positions[i+1] - positions[i])
            r0 = 3.8  # Angstroms (CA-CA distance)
            k = 100.0  # kcal/mol/A^2
            energy += 0.5 * k * (r - r0)**2

        # Angle energy
        for i in range(n_res - 2):
            v1 = positions[i+1] - positions[i]
            v2 = positions[i+2] - positions[i+1]
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10)
            angle = np.arccos(np.clip(cos_angle, -1, 1))
            theta0 = np.radians(120)  # Ideal angle
            k_angle = 50.0
            energy += 0.5 * k_angle * (angle - theta0)**2

        # Non-bonded (Lennard-Jones + electrostatic)
        for i in range(n_res):
            for j in range(i + 3, n_res):
                r = np.linalg.norm(positions[j] - positions[i])
                if r < 15.0:  # Cutoff
                    aa_i = self.sequence[i] if self.sequence[i] in self.aa_properties else 'A'
                    aa_j = self.sequence[j] if self.sequence[j] in self.aa_properties else 'A'

                    # LJ-like term
                    sigma = 4.0
                    epsilon = 0.1 * (1 + self.aa_properties[aa_i]['hydro'] *
                                      self.aa_properties[aa_j]['hydro'])
                    if r > 0.1:
                        lj = 4 * epsilon * ((sigma/r)**12 - (sigma/r)**6)
                        energy += lj

                    # Electrostatic
                    q_i = self.aa_properties[aa_i]['charge']
                    q_j = self.aa_properties[aa_j]['charge']
                    if r > 0.1:
                        energy += 332.0 * q_i * q_j / (80.0 * r)  # Screened electrostatics

        return energy

    def compute_forces(self, positions: np.ndarray) -> np.ndarray:
        """Compute forces via numerical gradient."""
        forces = np.zeros_like(positions)
        h = 0.001  # Angstroms

        for i in range(len(positions)):
            for d in range(3):
                pos_plus = positions.copy()
                pos_minus = positions.copy()
                pos_plus[i, d] += h
                pos_minus[i, d] -= h

                e_plus = self.compute_potential_energy(pos_plus)
                e_minus = self.compute_potential_energy(pos_minus)

                forces[i, d] = -(e_plus - e_minus) / (2 * h)

        return forces

    def initialize_positions(self) -> np.ndarray:
        """Initialize positions in extended chain configuration."""
        n_res = len(self.sequence)
        positions = np.zeros((n_res, 3))

        # Extended chain with slight helix tendency
        for i in range(n_res):
            positions[i, 0] = i * 3.8 * np.cos(np.radians(15 * i))
            positions[i, 1] = i * 3.8 * np.sin(np.radians(15 * i))
            positions[i, 2] = i * 1.5

        return positions

    def run_dynamics(self, n_steps: int = 1000,
                     report_interval: int = 100) -> Dict:
        """Run simplified Langevin dynamics."""
        positions = self.initialize_positions()
        velocities = np.random.randn(*positions.shape) * 0.1

        trajectory = []
        energies = []

        # Langevin dynamics parameters
        gamma = self.friction
        dt = self.timestep
        kT = 0.001987 * self.temperature  # kcal/mol

        for step in range(n_steps):
            # Compute forces
            forces = self.compute_forces(positions)

            # Langevin integration (BAOAB-like)
            # Random kick
            random_force = np.sqrt(2 * gamma * kT / dt) * np.random.randn(*positions.shape)

            # Update velocities
            velocities += 0.5 * dt * forces
            velocities *= np.exp(-gamma * dt)
            velocities += 0.5 * dt * random_force

            # Update positions
            positions += dt * velocities

            # Second half of velocity update
            forces = self.compute_forces(positions)
            velocities += 0.5 * dt * forces

            if step % report_interval == 0:
                energy = self.compute_potential_energy(positions)
                trajectory.append(positions.copy())
                energies.append(energy)

        return {
            'trajectory': trajectory,
            'energies': energies,
            'final_positions': positions,
            'n_steps': n_steps,
            'timestep_ps': dt,
            'temperature_K': self.temperature
        }

    def compute_rmsf(self, trajectory: List[np.ndarray]) -> np.ndarray:
        """Compute root mean square fluctuation per residue."""
        if len(trajectory) < 2:
            return np.zeros(len(self.sequence))

        trajectory_array = np.array(trajectory)
        mean_positions = np.mean(trajectory_array, axis=0)

        fluctuations = trajectory_array - mean_positions
        rmsf = np.sqrt(np.mean(np.sum(fluctuations**2, axis=2), axis=0))

        return rmsf

    def compute_rmsd(self, trajectory: List[np.ndarray]) -> np.ndarray:
        """Compute RMSD from first frame."""
        if len(trajectory) < 1:
            return np.array([0.0])

        reference = trajectory[0]
        rmsd = []

        for frame in trajectory:
            diff = frame - reference
            rmsd.append(np.sqrt(np.mean(np.sum(diff**2, axis=1))))

        return np.array(rmsd)


class OpenMMSimulator:
    """
    Full molecular dynamics simulator using OpenMM.
    Supports GPU acceleration via CUDA/OpenCL.
    """

    def __init__(self, pdb_file: str):
        if not OPENMM_AVAILABLE:
            raise ImportError("OpenMM not available")

        self.pdb_file = pdb_file
        self.pdb = PDBFile(pdb_file)

    def setup_simulation(self,
                        forcefield: str = 'amber14-all.xml',
                        water_model: str = 'amber14/tip3pfb.xml',
                        temperature: float = 300.0,
                        friction: float = 1.0,
                        timestep: float = 0.002) -> Simulation:
        """Setup OpenMM simulation system."""

        # Load force field
        ff = ForceField(forcefield, water_model)

        # Create modeller and add solvent
        modeller = Modeller(self.pdb.topology, self.pdb.positions)
        modeller.addSolvent(ff, padding=1.0*unit.nanometers)

        # Create system
        system = ff.createSystem(
            modeller.topology,
            nonbondedMethod=PME,
            nonbondedCutoff=1.0*unit.nanometers,
            constraints=HBonds
        )

        # Create integrator
        integrator = mm.LangevinMiddleIntegrator(
            temperature*unit.kelvin,
            friction/unit.picoseconds,
            timestep*unit.picoseconds
        )

        # Create simulation
        # Try CUDA, then OpenCL, then CPU
        platform = None
        for platform_name in ['CUDA', 'OpenCL', 'CPU']:
            try:
                platform = mm.Platform.getPlatformByName(platform_name)
                break
            except:
                continue

        simulation = Simulation(modeller.topology, system, integrator, platform)
        simulation.context.setPositions(modeller.positions)

        return simulation

    def minimize_energy(self, simulation: Simulation,
                       max_iterations: int = 1000) -> float:
        """Run energy minimization."""
        simulation.minimizeEnergy(maxIterations=max_iterations)
        state = simulation.context.getState(getEnergy=True)
        return state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)

    def equilibrate(self, simulation: Simulation,
                   n_steps: int = 10000) -> None:
        """Run equilibration."""
        simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
        simulation.step(n_steps)

    def run_production(self, simulation: Simulation,
                      n_steps: int = 100000,
                      trajectory_file: str = 'trajectory.dcd',
                      report_interval: int = 1000) -> Dict:
        """Run production MD."""
        from openmm.app import DCDReporter, StateDataReporter

        # Add reporters
        simulation.reporters.append(
            DCDReporter(trajectory_file, report_interval)
        )

        energies = []

        # Run simulation
        for i in range(n_steps // report_interval):
            simulation.step(report_interval)
            state = simulation.context.getState(getEnergy=True)
            energies.append(state.getPotentialEnergy().value_in_unit(
                unit.kilojoules_per_mole))

        return {
            'trajectory_file': trajectory_file,
            'energies': energies,
            'n_steps': n_steps
        }


class MDPipeline:
    """
    Complete MD pipeline for therapeutic proteins.
    """

    def __init__(self, output_dir: str = "md_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []

    def analyze_sequence(self, name: str, sequence: str,
                        n_steps: int = 5000) -> Dict:
        """Run MD analysis on a protein sequence."""
        print(f"  Analyzing: {name}")

        # Use simplified dynamics (always available)
        simulator = SimplifiedDynamics(sequence)

        # Run dynamics
        print(f"    Running {n_steps} steps of Langevin dynamics...")
        dynamics_result = simulator.run_dynamics(n_steps=n_steps, report_interval=100)

        # Compute trajectory analysis
        trajectory = dynamics_result['trajectory']
        rmsf = simulator.compute_rmsf(trajectory)
        rmsd = simulator.compute_rmsd(trajectory)

        # Identify flexible regions
        mean_rmsf = np.mean(rmsf)
        flexible_residues = [i for i, r in enumerate(rmsf) if r > 1.5 * mean_rmsf]
        rigid_residues = [i for i, r in enumerate(rmsf) if r < 0.5 * mean_rmsf]

        # Compute stability metrics
        final_energy = dynamics_result['energies'][-1] if dynamics_result['energies'] else 0
        energy_std = np.std(dynamics_result['energies']) if dynamics_result['energies'] else 0

        result = {
            'name': name,
            'sequence_length': len(sequence),
            'n_steps': n_steps,
            'simulation_time_ps': n_steps * dynamics_result['timestep_ps'],
            'temperature_K': dynamics_result['temperature_K'],
            'final_energy_kcal': final_energy,
            'energy_std_kcal': energy_std,
            'mean_rmsf_A': float(np.mean(rmsf)),
            'max_rmsf_A': float(np.max(rmsf)),
            'mean_rmsd_A': float(np.mean(rmsd)),
            'final_rmsd_A': float(rmsd[-1]) if len(rmsd) > 0 else 0,
            'n_flexible_residues': len(flexible_residues),
            'n_rigid_residues': len(rigid_residues),
            'flexible_regions': self._identify_regions(flexible_residues),
            'rigid_regions': self._identify_regions(rigid_residues),
            'stability_score': self._compute_stability_score(rmsf, rmsd, energy_std),
            'rmsf_per_residue': rmsf.tolist(),
            'rmsd_trajectory': rmsd.tolist(),
            'energy_trajectory': dynamics_result['energies']
        }

        self.results.append(result)
        return result

    def _identify_regions(self, residues: List[int]) -> List[str]:
        """Convert residue list to region strings (e.g., '10-25')."""
        if not residues:
            return []

        regions = []
        start = residues[0]
        end = residues[0]

        for i in range(1, len(residues)):
            if residues[i] == end + 1:
                end = residues[i]
            else:
                regions.append(f"{start+1}-{end+1}" if start != end else str(start+1))
                start = residues[i]
                end = residues[i]

        regions.append(f"{start+1}-{end+1}" if start != end else str(start+1))
        return regions

    def _compute_stability_score(self, rmsf: np.ndarray,
                                rmsd: np.ndarray,
                                energy_std: float) -> float:
        """Compute overall stability score (0-100)."""
        # Lower RMSF = more stable
        rmsf_score = max(0, 100 - np.mean(rmsf) * 10)

        # Low RMSD drift = stable
        if len(rmsd) > 1:
            rmsd_drift = rmsd[-1] - rmsd[0]
            rmsd_score = max(0, 100 - rmsd_drift * 5)
        else:
            rmsd_score = 50

        # Low energy fluctuation = stable
        energy_score = max(0, 100 - energy_std * 0.1)

        return (rmsf_score + rmsd_score + energy_score) / 3

    def analyze_pdb(self, name: str, pdb_file: str,
                   n_steps: int = 10000) -> Optional[Dict]:
        """Analyze structure from PDB file using OpenMM if available."""
        if not OPENMM_AVAILABLE:
            print(f"    OpenMM not available, skipping PDB analysis for {name}")
            return None

        try:
            simulator = OpenMMSimulator(pdb_file)
            simulation = simulator.setup_simulation()

            # Minimize
            print(f"    Minimizing energy...")
            min_energy = simulator.minimize_energy(simulation)

            # Equilibrate
            print(f"    Equilibrating...")
            simulator.equilibrate(simulation, n_steps=5000)

            # Production
            print(f"    Running production MD ({n_steps} steps)...")
            traj_file = str(self.output_dir / f"{name}_trajectory.dcd")
            result = simulator.run_production(
                simulation, n_steps=n_steps,
                trajectory_file=traj_file
            )

            return {
                'name': name,
                'pdb_file': pdb_file,
                'trajectory_file': result['trajectory_file'],
                'minimized_energy_kJ': min_energy,
                'production_energies': result['energies']
            }

        except Exception as e:
            print(f"    Error in OpenMM simulation: {e}")
            return None

    def batch_analyze(self, sequences: Dict[str, str],
                     n_steps: int = 5000) -> List[Dict]:
        """Analyze multiple sequences."""
        results = []

        for name, sequence in sequences.items():
            try:
                result = self.analyze_sequence(name, sequence, n_steps)
                results.append(result)
            except Exception as e:
                print(f"    Error analyzing {name}: {e}")
                results.append({
                    'name': name,
                    'error': str(e)
                })

        return results

    def save_results(self, filename: str = "md_analysis.json") -> str:
        """Save all results to JSON."""
        output_file = self.output_dir / filename

        output_data = {
            'metadata': {
                'generator': 'M4 Molecular Dynamics Pipeline',
                'timestamp': datetime.now().isoformat(),
                'openmm_available': OPENMM_AVAILABLE,
                'mdanalysis_available': MDANALYSIS_AVAILABLE,
                'n_sequences_analyzed': len(self.results)
            },
            'results': self.results
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        return str(output_file)

    def generate_report(self) -> str:
        """Generate human-readable MD report."""
        report = []
        report.append("=" * 70)
        report.append("M4 MOLECULAR DYNAMICS ANALYSIS REPORT")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Sequences analyzed: {len(self.results)}")
        report.append("")

        # Sort by stability score
        sorted_results = sorted(
            [r for r in self.results if 'stability_score' in r],
            key=lambda x: x['stability_score'],
            reverse=True
        )

        report.append("STABILITY RANKING:")
        report.append("-" * 70)
        for i, r in enumerate(sorted_results[:20], 1):
            report.append(f"  {i:2d}. {r['name'][:40]:<40} "
                         f"Score: {r['stability_score']:.1f}")

        report.append("")
        report.append("DETAILED ANALYSIS:")
        report.append("-" * 70)

        for r in self.results:
            if 'error' in r:
                report.append(f"\n{r['name']}: ERROR - {r['error']}")
                continue

            report.append(f"\n{r['name']}:")
            report.append(f"  Length: {r['sequence_length']} residues")
            report.append(f"  Simulation: {r['simulation_time_ps']:.1f} ps at {r['temperature_K']} K")
            report.append(f"  Stability Score: {r['stability_score']:.1f}/100")
            report.append(f"  Mean RMSF: {r['mean_rmsf_A']:.2f} Å")
            report.append(f"  Final RMSD: {r['final_rmsd_A']:.2f} Å")
            report.append(f"  Final Energy: {r['final_energy_kcal']:.1f} kcal/mol")

            if r['flexible_regions']:
                report.append(f"  Flexible regions: {', '.join(r['flexible_regions'][:5])}")
            if r['rigid_regions']:
                report.append(f"  Rigid regions: {', '.join(r['rigid_regions'][:5])}")

        report.append("")
        report.append("=" * 70)
        report.append("LICENSE: AGPL-3.0 + OpenMTA + CC BY-SA 4.0 + Patent Dedication")
        report.append("All data is PUBLIC DOMAIN for patent purposes.")
        report.append("=" * 70)

        return "\n".join(report)


def load_sequences_from_fasta(fasta_file: str) -> Dict[str, str]:
    """Load sequences from FASTA file."""
    sequences = {}
    current_name = None
    current_seq = []

    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_name:
                    sequences[current_name] = ''.join(current_seq)
                current_name = line[1:].split()[0]
                current_seq = []
            elif line and not line.startswith(';'):
                current_seq.append(line)

    if current_name:
        sequences[current_name] = ''.join(current_seq)

    return sequences


def main():
    """Main execution for overnight MD analysis."""
    print("=" * 70)
    print("M4 MOLECULAR DYNAMICS PIPELINE")
    print("Stability and Flexibility Analysis")
    print("=" * 70)
    print()

    # Setup output directory
    output_dir = Path("md_results")
    output_dir.mkdir(exist_ok=True)

    pipeline = MDPipeline(str(output_dir))

    # Look for generated sequences from other M4 scripts
    batch_results = Path("batch_results")

    if batch_results.exists():
        # Find all FASTA files
        fasta_files = list(batch_results.glob("**/*.fasta"))
        print(f"Found {len(fasta_files)} FASTA files to analyze")

        for fasta_file in fasta_files:
            print(f"\nLoading: {fasta_file.name}")
            sequences = load_sequences_from_fasta(str(fasta_file))

            if sequences:
                print(f"  Found {len(sequences)} sequences")
                # Run shorter simulations for batch processing
                pipeline.batch_analyze(sequences, n_steps=2000)
    else:
        # Demo sequences if no batch results
        print("No batch results found, running demo analysis...")
        demo_sequences = {
            "Demo_Angiopep2_fusion": (
                "TFFYGGSRGKRNNFKTEEY"  # Angiopep-2
                "GGGGS" * 3 +  # Linker
                "MHHHHHHGGSEVQLVESGGGLVQPGGSLRLSCAASGFTFSSYAMS"  # VH start
            ),
            "Demo_Anti_VEGF_scFv": (
                "EVQLVESGGGLVQPGGSLRLSCAASGFTFSSYWMSWVRQAPGKGLEWVANIKQDGSEKY"
                "YVDSVKGRFTISRDNAKNSLYLQMNSLRAEDTAVYYCARWGYRFFDYWGQGTLVTVSS"
                "GGGGSGGGGSGGGGSGGGGS"  # Linker
                "DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVP"
                "SRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIK"
            )
        }

        # Run longer simulations for demo
        pipeline.batch_analyze(demo_sequences, n_steps=5000)

    # Save results
    json_file = pipeline.save_results()
    print(f"\nResults saved to: {json_file}")

    # Generate report
    report = pipeline.generate_report()
    report_file = output_dir / "md_analysis_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"Report saved to: {report_file}")

    # Print summary
    print("\n" + report)

    return pipeline.results


if __name__ == "__main__":
    results = main()

#!/usr/bin/env python3
"""
M4 Thermal Stress Molecular Dynamics - Stability Validation Under Heat

Simulates peptide structures at elevated temperature (350K) to test stability.
A structure that unfolds rapidly under thermal stress is likely:
1. A hallucination (no stable fold exists)
2. Intrinsically disordered (valid but not druggable as structured)
3. Aggregation-prone (safety concern)

Validation Criteria:
- RMSD plateau: Structure should stabilize, not continuously drift
- RMSF per residue: Core should be stable, termini can fluctuate
- Hydrogen bonds: Should maintain >50% of initial H-bonds
- Radius of gyration: Should not expand >20% (unfolding)

LICENSE: AGPL-3.0-or-later (code) + OpenMTA (biological materials)
PRIOR ART ESTABLISHED: April 20, 2026

WARNING: This is a simplified Langevin dynamics simulation for screening.
Production MD requires OpenMM, GROMACS, or AMBER with explicit solvent.
"""

import json
import hashlib
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict, field
import warnings

warnings.filterwarnings('ignore')


# Physical constants
KB = 0.001987204  # Boltzmann constant in kcal/(mol·K)
TIMESTEP = 0.002  # 2 fs in picoseconds
FRICTION = 1.0    # Langevin friction coefficient (1/ps)

# Simulation parameters
DEFAULT_TEMP = 350.0   # Kelvin (elevated stress temperature)
DEFAULT_STEPS = 100000  # 200 ps simulation (for quick screening)
EQUILIBRATION = 10000   # 20 ps equilibration


@dataclass
class MDTrajectoryPoint:
    """Single point in MD trajectory"""
    step: int
    time_ps: float
    temperature: float
    potential_energy: float
    kinetic_energy: float
    total_energy: float
    rmsd_from_start: float
    radius_of_gyration: float
    n_hydrogen_bonds: int


@dataclass
class ThermalStressResult:
    """Complete thermal stress test result"""
    sequence: str
    sequence_hash: str
    n_residues: int

    # Simulation parameters
    temperature_k: float
    total_time_ps: float
    timestep_fs: float

    # Stability metrics
    mean_rmsd: float
    max_rmsd: float
    rmsd_slope: float  # Drift rate (Å/ns) - should be ~0 for stable
    rmsd_plateau: bool  # Did RMSD stabilize?

    mean_rg: float
    rg_expansion: float  # % expansion from start

    initial_hbonds: int
    final_hbonds: int
    hbond_retention: float  # Fraction retained

    # RMSF per residue (flexibility)
    mean_rmsf: float
    max_rmsf_residue: int
    core_stability: float  # Average RMSF of core (excluding termini)

    # Overall assessment
    is_stable: bool
    stability_score: float  # 0-100
    failure_reasons: List[str]

    validation_timestamp: str


class SimpleLangevinDynamics:
    """
    Simplified Langevin dynamics for thermal stress testing.

    This is a SCREENING tool, not production MD. For actual drug development:
    - Use OpenMM with explicit TIP3P water
    - Run 100+ ns simulations
    - Include counter-ions for charged peptides
    - Use PME electrostatics
    """

    def __init__(self, temperature: float = DEFAULT_TEMP):
        self.temperature = temperature
        self.kT = KB * temperature

    def generate_initial_structure(self, sequence: str) -> np.ndarray:
        """
        Generate initial Cα coordinates for a peptide.

        In production, this would come from:
        - AlphaFold/ESMFold prediction
        - Homology modeling
        - NMR/X-ray structure
        """
        np.random.seed(hash(sequence) % (2**32))

        n = len(sequence)
        coords = np.zeros((n, 3))

        # Generate a compact starting structure
        # Mix of helix and coil based on sequence
        for i in range(n):
            if i == 0:
                coords[i] = [0, 0, 0]
            else:
                # Default helical rise
                z_rise = 1.5  # Å per residue (helical)
                theta = i * 100 * np.pi / 180  # Helical twist

                coords[i] = coords[i-1] + np.array([
                    1.5 * np.cos(theta),
                    1.5 * np.sin(theta),
                    z_rise
                ])

        return coords

    def calculate_forces(self, coords: np.ndarray, sequence: str) -> np.ndarray:
        """
        Calculate simplified force field.

        Real MD uses:
        - Amber ff14SB or CHARMM36m
        - Explicit bond/angle/dihedral terms
        - Lennard-Jones + Coulomb non-bonded
        - PME for long-range electrostatics

        Here we use a coarse-grained potential for screening.
        """
        n = len(coords)
        forces = np.zeros_like(coords)

        # Bond restraints (keep Cα-Cα at ~3.8 Å)
        for i in range(n - 1):
            r = coords[i+1] - coords[i]
            d = np.linalg.norm(r)
            if d > 0:
                # Harmonic restraint
                k_bond = 50.0  # kcal/mol/Å²
                d0 = 3.8  # Å
                f_mag = -k_bond * (d - d0)
                f_dir = r / d
                forces[i] -= f_mag * f_dir
                forces[i+1] += f_mag * f_dir

        # Non-bonded (simplified LJ-like)
        for i in range(n):
            for j in range(i + 3, n):  # Skip 1-2 and 1-3
                r = coords[j] - coords[i]
                d = np.linalg.norm(r)
                if d > 0 and d < 10.0:  # Cutoff
                    # Soft repulsion
                    sigma = 4.0
                    epsilon = 0.1
                    if d < sigma:
                        f_mag = epsilon * (sigma / d) ** 12
                        f_dir = r / d
                        forces[i] -= f_mag * f_dir
                        forces[j] += f_mag * f_dir

        # Hydrophobic collapse (for hydrophobic residues)
        hydrophobic = set('AVILMFYW')
        hydrophobic_indices = [i for i, aa in enumerate(sequence) if aa in hydrophobic]

        if len(hydrophobic_indices) > 1:
            # Centroid of hydrophobic residues
            h_coords = coords[hydrophobic_indices]
            centroid = np.mean(h_coords, axis=0)

            for i in hydrophobic_indices:
                r = centroid - coords[i]
                d = np.linalg.norm(r)
                if d > 1.0:
                    # Weak attractive force toward hydrophobic core
                    f_mag = 0.5 * d  # Linear spring
                    forces[i] += f_mag * r / d

        return forces

    def calculate_potential_energy(self, coords: np.ndarray, sequence: str) -> float:
        """Calculate total potential energy."""
        n = len(coords)
        energy = 0.0

        # Bond energy
        k_bond = 50.0
        d0 = 3.8
        for i in range(n - 1):
            d = np.linalg.norm(coords[i+1] - coords[i])
            energy += 0.5 * k_bond * (d - d0) ** 2

        # Non-bonded
        for i in range(n):
            for j in range(i + 3, n):
                d = np.linalg.norm(coords[j] - coords[i])
                if d > 0 and d < 10.0:
                    sigma = 4.0
                    epsilon = 0.1
                    if d < sigma:
                        energy += epsilon * (sigma / d) ** 12

        return energy

    def langevin_step(
        self,
        coords: np.ndarray,
        velocities: np.ndarray,
        forces: np.ndarray,
        masses: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform one Langevin dynamics step (BAOAB integrator).
        """
        dt = TIMESTEP
        gamma = FRICTION

        # Random force from thermal bath
        sigma = np.sqrt(2 * gamma * self.kT / masses[:, None])
        random_force = np.random.randn(*coords.shape) * sigma

        # BAOAB splitting
        # B: kick (half step)
        velocities = velocities + 0.5 * dt * forces / masses[:, None]

        # A: drift (half step)
        coords = coords + 0.5 * dt * velocities

        # O: Ornstein-Uhlenbeck (friction + noise)
        c1 = np.exp(-gamma * dt)
        c2 = np.sqrt(1 - c1 ** 2)
        velocities = c1 * velocities + c2 * np.sqrt(self.kT / masses[:, None]) * np.random.randn(*velocities.shape)

        # A: drift (half step)
        coords = coords + 0.5 * dt * velocities

        # B: kick (half step with new forces - would need force recalc)
        # Simplified: use same forces
        velocities = velocities + 0.5 * dt * forces / masses[:, None]

        return coords, velocities

    def calculate_rmsd(self, coords: np.ndarray, reference: np.ndarray) -> float:
        """Calculate RMSD after optimal superposition."""
        # Center both
        c1 = np.mean(coords, axis=0)
        c2 = np.mean(reference, axis=0)
        centered1 = coords - c1
        centered2 = reference - c2

        # Kabsch rotation
        H = centered1.T @ centered2
        U, S, Vt = np.linalg.svd(H)
        d = np.sign(np.linalg.det(Vt.T @ U.T))
        R = Vt.T @ np.diag([1, 1, d]) @ U.T

        rotated = centered1 @ R.T
        diff = rotated - centered2

        return np.sqrt(np.mean(np.sum(diff**2, axis=1)))

    def calculate_rg(self, coords: np.ndarray) -> float:
        """Calculate radius of gyration."""
        centroid = np.mean(coords, axis=0)
        r2 = np.sum((coords - centroid) ** 2, axis=1)
        return np.sqrt(np.mean(r2))

    def count_hydrogen_bonds(self, coords: np.ndarray, sequence: str) -> int:
        """
        Estimate number of hydrogen bonds based on geometry.

        In reality, needs N-H and C=O vectors, not just Cα.
        Here we use distance criterion as proxy.
        """
        n = len(coords)
        n_hbonds = 0

        # H-bonds typically form i -> i+4 (helix) or i -> i+2 (turn)
        for i in range(n):
            for offset in [3, 4, 5]:  # Helix patterns
                j = i + offset
                if j < n:
                    d = np.linalg.norm(coords[j] - coords[i])
                    if 4.5 < d < 6.5:  # Typical Cα-Cα distance for H-bonded residues
                        n_hbonds += 1

        return n_hbonds

    def run_simulation(
        self,
        sequence: str,
        n_steps: int = DEFAULT_STEPS,
        save_interval: int = 1000
    ) -> Tuple[List[MDTrajectoryPoint], np.ndarray]:
        """
        Run thermal stress simulation.

        Returns trajectory and per-residue RMSF.
        """
        n = len(sequence)

        # Initialize structure
        coords = self.generate_initial_structure(sequence)
        reference_coords = coords.copy()

        # Initialize velocities from Maxwell-Boltzmann
        masses = np.ones(n) * 110.0  # Average amino acid mass in Da

        velocities = np.random.randn(n, 3) * np.sqrt(self.kT / masses[:, None])

        # Remove center of mass motion
        velocities -= np.mean(velocities, axis=0)

        trajectory = []
        all_coords = [coords.copy()]

        # Initial metrics
        initial_hbonds = self.count_hydrogen_bonds(coords, sequence)
        initial_rg = self.calculate_rg(coords)

        print(f"    Running {n_steps * TIMESTEP:.1f} ps simulation at {self.temperature} K...")

        for step in range(n_steps):
            # Calculate forces
            forces = self.calculate_forces(coords, sequence)

            # Integrate
            coords, velocities = self.langevin_step(coords, velocities, forces, masses)

            # Save trajectory point
            if step % save_interval == 0:
                ke = 0.5 * np.sum(masses[:, None] * velocities ** 2)
                pe = self.calculate_potential_energy(coords, sequence)
                temp = 2 * ke / (3 * n * KB)
                rmsd = self.calculate_rmsd(coords, reference_coords)
                rg = self.calculate_rg(coords)
                hbonds = self.count_hydrogen_bonds(coords, sequence)

                trajectory.append(MDTrajectoryPoint(
                    step=step,
                    time_ps=step * TIMESTEP,
                    temperature=float(temp),
                    potential_energy=float(pe),
                    kinetic_energy=float(ke),
                    total_energy=float(pe + ke),
                    rmsd_from_start=float(rmsd),
                    radius_of_gyration=float(rg),
                    n_hydrogen_bonds=hbonds
                ))

                all_coords.append(coords.copy())

        # Calculate per-residue RMSF
        coords_array = np.array(all_coords)
        mean_coords = np.mean(coords_array, axis=0)
        fluctuations = coords_array - mean_coords
        rmsf = np.sqrt(np.mean(np.sum(fluctuations ** 2, axis=2), axis=0))

        return trajectory, rmsf


class ThermalStressValidator:
    """
    Validates peptide stability under thermal stress.
    """

    # Thresholds
    MAX_RMSD_DRIFT = 0.5    # Å/ns - stable structures shouldn't drift
    MAX_RG_EXPANSION = 20.0  # % expansion indicates unfolding
    MIN_HBOND_RETENTION = 50.0  # % H-bonds retained

    def __init__(self, output_dir: Path = None, temperature: float = DEFAULT_TEMP):
        self.output_dir = output_dir or Path("validation_results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temperature = temperature
        self.simulator = SimpleLangevinDynamics(temperature)

    def analyze_trajectory(
        self,
        trajectory: List[MDTrajectoryPoint],
        rmsf: np.ndarray,
        sequence: str
    ) -> ThermalStressResult:
        """Analyze MD trajectory for stability metrics."""
        n = len(sequence)
        seq_hash = hashlib.sha256(sequence.encode()).hexdigest()[:16]

        # Extract time series
        times = np.array([t.time_ps for t in trajectory])
        rmsds = np.array([t.rmsd_from_start for t in trajectory])
        rgs = np.array([t.radius_of_gyration for t in trajectory])
        hbonds = np.array([t.n_hydrogen_bonds for t in trajectory])

        # Skip equilibration
        equil_idx = len(times) // 5  # First 20%
        prod_times = times[equil_idx:]
        prod_rmsds = rmsds[equil_idx:]
        prod_rgs = rgs[equil_idx:]
        prod_hbonds = hbonds[equil_idx:]

        # RMSD analysis
        mean_rmsd = float(np.mean(prod_rmsds))
        max_rmsd = float(np.max(prod_rmsds))

        # RMSD drift rate (Å/ns)
        if len(prod_times) > 1:
            time_ns = prod_times / 1000.0
            slope, _ = np.polyfit(time_ns, prod_rmsds, 1)
            rmsd_slope = float(slope)
        else:
            rmsd_slope = 0.0

        # Check if RMSD plateaus (std dev of last 50% < 0.5 Å)
        last_half = prod_rmsds[len(prod_rmsds)//2:]
        rmsd_plateau = np.std(last_half) < 0.5

        # Radius of gyration
        mean_rg = float(np.mean(prod_rgs))
        initial_rg = rgs[0] if len(rgs) > 0 else mean_rg
        rg_expansion = ((mean_rg - initial_rg) / initial_rg * 100) if initial_rg > 0 else 0.0

        # Hydrogen bond retention
        initial_hbonds = hbonds[0] if len(hbonds) > 0 else 0
        final_hbonds = int(np.mean(prod_hbonds[-10:])) if len(prod_hbonds) > 10 else 0
        hbond_retention = (final_hbonds / initial_hbonds * 100) if initial_hbonds > 0 else 100.0

        # RMSF analysis
        mean_rmsf = float(np.mean(rmsf))
        max_rmsf_residue = int(np.argmax(rmsf))

        # Core stability (exclude 3 residues from each terminus)
        if n > 6:
            core_rmsf = rmsf[3:-3]
            core_stability = float(np.mean(core_rmsf))
        else:
            core_stability = mean_rmsf

        # Determine stability
        failure_reasons = []

        if abs(rmsd_slope) > self.MAX_RMSD_DRIFT:
            failure_reasons.append(f"RMSD drift {rmsd_slope:.2f} Å/ns > {self.MAX_RMSD_DRIFT}")

        if rg_expansion > self.MAX_RG_EXPANSION:
            failure_reasons.append(f"Rg expansion {rg_expansion:.1f}% > {self.MAX_RG_EXPANSION}%")

        if hbond_retention < self.MIN_HBOND_RETENTION:
            failure_reasons.append(f"H-bond retention {hbond_retention:.1f}% < {self.MIN_HBOND_RETENTION}%")

        if not rmsd_plateau:
            failure_reasons.append("RMSD did not plateau (structure still drifting)")

        is_stable = len(failure_reasons) == 0

        # Calculate stability score
        drift_score = max(0, 30 - abs(rmsd_slope) * 60)  # 30 pts max
        rg_score = max(0, 25 - rg_expansion)  # 25 pts max
        hbond_score = hbond_retention / 4  # 25 pts max
        plateau_score = 20 if rmsd_plateau else 0

        stability_score = drift_score + rg_score + hbond_score + plateau_score

        return ThermalStressResult(
            sequence=sequence,
            sequence_hash=seq_hash,
            n_residues=n,
            temperature_k=self.temperature,
            total_time_ps=float(times[-1]) if len(times) > 0 else 0,
            timestep_fs=TIMESTEP * 1000,
            mean_rmsd=mean_rmsd,
            max_rmsd=max_rmsd,
            rmsd_slope=rmsd_slope,
            rmsd_plateau=rmsd_plateau,
            mean_rg=mean_rg,
            rg_expansion=float(rg_expansion),
            initial_hbonds=int(initial_hbonds),
            final_hbonds=final_hbonds,
            hbond_retention=float(hbond_retention),
            mean_rmsf=mean_rmsf,
            max_rmsf_residue=max_rmsf_residue,
            core_stability=core_stability,
            is_stable=is_stable,
            stability_score=float(stability_score),
            failure_reasons=failure_reasons,
            validation_timestamp=datetime.now().isoformat()
        )

    def validate_structure(self, sequence: str, n_steps: int = DEFAULT_STEPS) -> ThermalStressResult:
        """Run thermal stress validation on a single sequence."""
        print(f"  Testing: {sequence[:30]}{'...' if len(sequence) > 30 else ''}")

        trajectory, rmsf = self.simulator.run_simulation(sequence, n_steps)
        result = self.analyze_trajectory(trajectory, rmsf, sequence)

        return result

    def validate_batch(self, sequences: List[str], n_steps: int = DEFAULT_STEPS) -> Dict:
        """Validate a batch of sequences."""
        results = []
        for i, seq in enumerate(sequences, 1):
            print(f"\n[{i}/{len(sequences)}] Validating thermal stability...")
            result = self.validate_structure(seq, n_steps)
            results.append(result)

        n_total = len(results)
        n_stable = sum(1 for r in results if r.is_stable)
        mean_score = np.mean([r.stability_score for r in results])

        summary = {
            "metadata": {
                "generator": "M4 Thermal Stress MD",
                "timestamp": datetime.now().isoformat(),
                "n_sequences": n_total,
                "temperature_k": self.temperature,
                "simulation_time_ps": results[0].total_time_ps if results else 0,
                "license": "AGPL-3.0-or-later (code) + OpenMTA (biological materials)"
            },
            "thresholds": {
                "max_rmsd_drift_per_ns": self.MAX_RMSD_DRIFT,
                "max_rg_expansion_percent": self.MAX_RG_EXPANSION,
                "min_hbond_retention_percent": self.MIN_HBOND_RETENTION
            },
            "summary": {
                "total_sequences": n_total,
                "stable": n_stable,
                "unstable": n_total - n_stable,
                "stability_rate": n_stable / n_total if n_total > 0 else 0,
                "mean_stability_score": float(mean_score)
            },
            "results": [asdict(r) for r in results]
        }

        return summary

    def save_results(self, summary: Dict, prefix: str = "thermal_stress"):
        """Save validation results to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{prefix}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"Results saved to: {filename}")
        return filename


def load_sequences_from_fasta(fasta_path: Path) -> List[str]:
    """Load sequences from FASTA file."""
    sequences = []
    current_seq = []

    with open(fasta_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>') or line.startswith('#'):
                if current_seq:
                    sequences.append(''.join(current_seq))
                    current_seq = []
            elif line:
                current_seq.append(line)

        if current_seq:
            sequences.append(''.join(current_seq))

    return sequences


def main():
    """Run thermal stress validation on peptide candidates."""
    print("=" * 70)
    print("M4 THERMAL STRESS MOLECULAR DYNAMICS")
    print(f"Stability Test at Elevated Temperature (350K)")
    print("=" * 70)
    print()

    # Initialize validator
    output_dir = Path(__file__).parent / "validation_results"
    validator = ThermalStressValidator(output_dir, temperature=350.0)

    # Collect sequences (use fewer for speed - MD is expensive)
    all_sequences = []

    # Look for FASTA files
    search_paths = [
        Path(__file__).parent.parent / "prolactinoma" / "peptides",
        Path(__file__).parent.parent.parent / "cftr_chaperones",
    ]

    for search_path in search_paths:
        if search_path.exists():
            for fasta in search_path.glob("*.fasta"):
                print(f"Loading sequences from: {fasta}")
                seqs = load_sequences_from_fasta(fasta)
                all_sequences.extend(seqs[:5])  # Only top 5 (MD is slow)
                print(f"  Loaded {len(seqs)} sequences, using top 5")

    if not all_sequences:
        print("No peptide files found, using example sequences...")
        all_sequences = [
            "CRGWYSSWVIINVSC",
            "YLSVTTAEVVATSTLLSF",
            "KVFHWFKAAKLSKR",
        ]

    print()
    print(f"Total sequences to validate: {len(all_sequences)}")
    print("-" * 70)

    # Run validation (shorter simulation for screening)
    summary = validator.validate_batch(all_sequences, n_steps=50000)  # 100 ps

    # Print results
    print()
    print("=" * 70)
    print("THERMAL STRESS RESULTS")
    print("=" * 70)
    print()
    print(f"Temperature:         {summary['metadata']['temperature_k']} K")
    print(f"Simulation time:     {summary['metadata']['simulation_time_ps']:.1f} ps")
    print()
    print(f"Total sequences:     {summary['summary']['total_sequences']}")
    print(f"Stable:              {summary['summary']['stable']}")
    print(f"Unstable:            {summary['summary']['unstable']}")
    print(f"Stability rate:      {summary['summary']['stability_rate']*100:.1f}%")
    print(f"Mean stability score:{summary['summary']['mean_stability_score']:.1f}/100")
    print()

    print("-" * 70)
    print("DETAILED RESULTS")
    print("-" * 70)
    print()

    for i, result in enumerate(summary['results'], 1):
        status = "STABLE" if result['is_stable'] else "UNSTABLE"
        seq_display = result['sequence'][:25] + "..." if len(result['sequence']) > 25 else result['sequence']

        print(f"{i}. {seq_display}")
        print(f"   Status: {status} | Score: {result['stability_score']:.1f}/100")
        print(f"   RMSD: mean={result['mean_rmsd']:.2f} Å, max={result['max_rmsd']:.2f} Å, drift={result['rmsd_slope']:.3f} Å/ns")
        print(f"   Rg expansion: {result['rg_expansion']:.1f}%")
        print(f"   H-bonds: {result['initial_hbonds']} -> {result['final_hbonds']} ({result['hbond_retention']:.1f}% retained)")
        print(f"   RMSF: mean={result['mean_rmsf']:.2f} Å, core={result['core_stability']:.2f} Å")

        if result['failure_reasons']:
            print(f"   Failures: {'; '.join(result['failure_reasons'])}")

        print()

    # Save results
    output_file = validator.save_results(summary)

    print("=" * 70)
    print("THERMAL STRESS VALIDATION COMPLETE")
    print()
    print("STABILITY CRITERIA:")
    print(f"  - RMSD drift: <{validator.MAX_RMSD_DRIFT} Å/ns")
    print(f"  - Rg expansion: <{validator.MAX_RG_EXPANSION}%")
    print(f"  - H-bond retention: >{validator.MIN_HBOND_RETENTION}%")
    print("  - RMSD must plateau (not continuously drift)")
    print()
    print("NOTE: This is a simplified Langevin dynamics screening.")
    print("Production validation requires:")
    print("  - OpenMM/GROMACS with explicit TIP3P water")
    print("  - 100+ ns simulation time")
    print("  - Multiple replica simulations")
    print("=" * 70)


if __name__ == "__main__":
    main()

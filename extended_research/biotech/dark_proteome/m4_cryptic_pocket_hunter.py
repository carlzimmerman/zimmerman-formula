#!/usr/bin/env python3
"""
M4 Cryptic Pocket Hunter - Dark Proteome Pipeline Stage 2

Analyzes REMD trajectories to identify transient druggable cavities in IDPs.
Uses dimensionality reduction + kinetic clustering to find metastable states
where cryptic pockets temporarily open.

The Problem:
- IDPs don't have static binding sites
- Standard pocket detection fails
- Cryptic pockets only exist transiently (~1-10% of time)

The Solution:
- PCA to reduce conformational space
- K-Means clustering into discrete microstates
- Geometric pocket detection on cluster centroids
- Filter for pockets with hydrophobic character (druggable)

A pocket that opens >5% of simulation time is a viable drug target.

LICENSE: AGPL-3.0-or-later (code) + OpenMTA (biological materials)
PRIOR ART ESTABLISHED: April 20, 2026
"""

import json
import hashlib
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import Counter
import warnings

warnings.filterwarnings('ignore')


@dataclass
class CrypticPocket:
    """Identified cryptic pocket in IDP"""
    pocket_id: int
    microstate_id: int
    population: float  # Fraction of trajectory in this state
    volume: float  # Å³
    depth: float  # Å
    hydrophobic_score: float  # 0-1
    residues_involved: List[int]
    centroid: List[float]
    druggability_score: float
    representative_frame: int


@dataclass
class PocketHuntingResult:
    """Complete result from pocket hunting analysis"""
    sequence: str
    sequence_hash: str
    n_frames_analyzed: int
    n_microstates: int
    pockets_found: int
    druggable_pockets: int
    top_pockets: List[CrypticPocket]
    pca_variance_explained: List[float]
    microstate_populations: List[float]
    output_files: Dict[str, str]
    timestamp: str


class CrypticPocketHunter:
    """
    Identifies transient druggable pockets in IDP conformational ensembles.

    Algorithm:
    1. Load REMD trajectory (Cα coordinates over time)
    2. PCA to reduce to first 3-5 principal components
    3. K-Means clustering to identify discrete metastable states
    4. For each cluster centroid, perform geometric pocket detection
    5. Score pockets by volume, depth, and hydrophobicity
    6. Return pockets that exist >5% of time as druggable targets
    """

    MIN_POCKET_VOLUME = 100.0  # Å³ - must fit small molecule
    MIN_POCKET_DEPTH = 4.0     # Å - must have concave surface
    MIN_DRUGGABILITY = 0.5     # Score threshold
    MIN_POPULATION = 0.05     # Must exist >5% of time

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("pockets")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_trajectory(self, traj_file: Path, topology_file: Path) -> Tuple[np.ndarray, dict]:
        """Load REMD trajectory and topology."""
        trajectory = np.load(traj_file)

        with open(topology_file) as f:
            topology = json.load(f)

        return trajectory, topology

    def perform_pca(
        self,
        trajectory: np.ndarray,
        n_components: int = 5
    ) -> Tuple[np.ndarray, np.ndarray, List[float]]:
        """
        Principal Component Analysis on conformational space.

        Reduces high-dimensional coordinate space to major modes of motion.
        First few PCs typically capture >80% of variance in IDPs.
        """
        n_frames, n_atoms, _ = trajectory.shape

        # Flatten: (n_frames, n_atoms * 3)
        flat_traj = trajectory.reshape(n_frames, -1)

        # Center the data
        mean_coords = np.mean(flat_traj, axis=0)
        centered = flat_traj - mean_coords

        # Compute covariance matrix
        cov = np.cov(centered.T)

        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        # Sort by decreasing eigenvalue
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Project onto first n_components
        projected = centered @ eigenvectors[:, :n_components]

        # Variance explained
        total_var = np.sum(eigenvalues)
        var_explained = [eigenvalues[i] / total_var for i in range(n_components)]

        return projected, eigenvectors[:, :n_components], var_explained

    def kmeans_clustering(
        self,
        projected_coords: np.ndarray,
        n_clusters: int = 10,
        max_iter: int = 100
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        K-Means clustering to identify discrete metastable states.

        Each cluster represents a conformational basin where the IDP
        spends significant time. Cluster centroids are representative
        structures for pocket detection.
        """
        n_samples, n_features = projected_coords.shape

        # Initialize centroids randomly
        np.random.seed(42)
        idx = np.random.choice(n_samples, n_clusters, replace=False)
        centroids = projected_coords[idx].copy()

        for iteration in range(max_iter):
            # Assign points to nearest centroid
            distances = np.zeros((n_samples, n_clusters))
            for k in range(n_clusters):
                distances[:, k] = np.linalg.norm(projected_coords - centroids[k], axis=1)

            labels = np.argmin(distances, axis=1)

            # Update centroids
            new_centroids = np.zeros_like(centroids)
            for k in range(n_clusters):
                mask = labels == k
                if np.sum(mask) > 0:
                    new_centroids[k] = np.mean(projected_coords[mask], axis=0)
                else:
                    new_centroids[k] = centroids[k]

            # Check convergence
            if np.allclose(centroids, new_centroids, atol=1e-4):
                break

            centroids = new_centroids

        return labels, centroids

    def get_representative_frames(
        self,
        trajectory: np.ndarray,
        labels: np.ndarray,
        projected: np.ndarray,
        centroids: np.ndarray
    ) -> Dict[int, int]:
        """Find frame closest to each cluster centroid."""
        representatives = {}

        for k in range(len(centroids)):
            mask = labels == k
            if not np.any(mask):
                continue

            # Indices of frames in this cluster
            cluster_indices = np.where(mask)[0]

            # Find frame closest to centroid in PC space
            cluster_points = projected[mask]
            distances = np.linalg.norm(cluster_points - centroids[k], axis=1)
            closest_in_cluster = np.argmin(distances)

            representatives[k] = cluster_indices[closest_in_cluster]

        return representatives

    def detect_pocket(
        self,
        coords: np.ndarray,
        sequence: str
    ) -> Optional[Dict]:
        """
        Detect concave surface pocket in a structure.

        Simplified Fpocket-like algorithm:
        1. Generate alpha spheres at surface
        2. Cluster spheres to identify cavities
        3. Score by volume, depth, hydrophobicity

        In production: Use Fpocket, SiteMap, or DoGSiteScorer.
        """
        n_atoms = len(coords)
        if n_atoms < 5:
            return None

        # Compute center of mass and Rg
        centroid = np.mean(coords, axis=0)
        distances_from_center = np.linalg.norm(coords - centroid, axis=1)
        rg = np.sqrt(np.mean(distances_from_center**2))

        # Identify surface residues (furthest from center)
        surface_threshold = np.percentile(distances_from_center, 70)
        surface_mask = distances_from_center > surface_threshold

        # Look for concave regions (atoms closer to center than neighbors)
        pocket_candidates = []

        for i in range(n_atoms):
            if i < 2 or i >= n_atoms - 2:
                continue

            # Local neighborhood
            neighbors = coords[max(0, i-3):min(n_atoms, i+4)]
            local_centroid = np.mean(neighbors, axis=0)

            # Is this atom recessed relative to neighbors?
            dist_to_center = np.linalg.norm(coords[i] - centroid)
            local_dist = np.linalg.norm(local_centroid - centroid)

            if dist_to_center < local_dist - 0.5:  # Recessed by >0.5 Å
                pocket_candidates.append(i)

        if len(pocket_candidates) < 3:
            return None

        # Cluster pocket residues
        pocket_coords = coords[pocket_candidates]
        pocket_centroid = np.mean(pocket_coords, axis=0)

        # Estimate volume (convex hull approximation)
        spread = np.max(pocket_coords, axis=0) - np.min(pocket_coords, axis=0)
        volume = np.prod(spread) * 0.5  # Rough estimate

        # Depth: distance from pocket centroid to surface
        depth = np.min(distances_from_center[surface_mask]) - \
                np.linalg.norm(pocket_centroid - centroid)
        depth = max(0, depth)

        # Hydrophobicity score
        hydrophobic = set('AVILMFYW')
        pocket_residues_hydrophobic = sum(
            1 for i in pocket_candidates
            if i < len(sequence) and sequence[i] in hydrophobic
        )
        hydrophobic_score = pocket_residues_hydrophobic / len(pocket_candidates) \
            if pocket_candidates else 0

        # Druggability: combine volume, depth, hydrophobicity
        volume_score = min(volume / 500.0, 1.0)
        depth_score = min(depth / 8.0, 1.0)
        druggability = (volume_score + depth_score + hydrophobic_score) / 3

        return {
            'volume': volume,
            'depth': depth,
            'hydrophobic_score': hydrophobic_score,
            'residues': pocket_candidates,
            'centroid': pocket_centroid.tolist(),
            'druggability': druggability
        }

    def hunt_pockets(
        self,
        trajectory: np.ndarray,
        sequence: str,
        n_clusters: int = 10
    ) -> List[CrypticPocket]:
        """
        Main pocket hunting pipeline.

        1. PCA dimensionality reduction
        2. K-Means clustering
        3. Pocket detection on each cluster centroid
        4. Filter for druggable pockets
        """
        print("Performing PCA dimensionality reduction...")
        projected, eigenvectors, var_explained = self.perform_pca(trajectory, n_components=5)
        print(f"  Variance explained by first 5 PCs: {sum(var_explained)*100:.1f}%")

        print(f"\nClustering into {n_clusters} microstates...")
        labels, centroids = self.kmeans_clustering(projected, n_clusters)

        # Population of each cluster
        counts = Counter(labels)
        populations = {k: counts.get(k, 0) / len(labels) for k in range(n_clusters)}
        print("  Microstate populations:")
        for k, pop in sorted(populations.items(), key=lambda x: -x[1]):
            print(f"    State {k}: {pop*100:.1f}%")

        # Get representative frames
        representatives = self.get_representative_frames(trajectory, labels, projected, centroids)

        print(f"\nScanning {len(representatives)} microstates for cryptic pockets...")
        pockets = []

        for state_id, frame_idx in representatives.items():
            coords = trajectory[frame_idx]
            pocket_info = self.detect_pocket(coords, sequence)

            if pocket_info is None:
                continue

            population = populations.get(state_id, 0)

            pocket = CrypticPocket(
                pocket_id=len(pockets),
                microstate_id=state_id,
                population=population,
                volume=pocket_info['volume'],
                depth=pocket_info['depth'],
                hydrophobic_score=pocket_info['hydrophobic_score'],
                residues_involved=pocket_info['residues'],
                centroid=pocket_info['centroid'],
                druggability_score=pocket_info['druggability'],
                representative_frame=frame_idx
            )

            # Filter criteria
            if (pocket.volume >= self.MIN_POCKET_VOLUME and
                pocket.depth >= self.MIN_POCKET_DEPTH and
                pocket.druggability_score >= self.MIN_DRUGGABILITY and
                pocket.population >= self.MIN_POPULATION):

                pockets.append(pocket)
                print(f"  Found druggable pocket in state {state_id}:")
                print(f"    Volume: {pocket.volume:.1f} Å³")
                print(f"    Depth: {pocket.depth:.1f} Å")
                print(f"    Druggability: {pocket.druggability_score:.2f}")
                print(f"    Population: {pocket.population*100:.1f}%")

        return pockets, var_explained, populations

    def run_analysis(
        self,
        traj_file: Path,
        topology_file: Path,
        n_clusters: int = 10
    ) -> PocketHuntingResult:
        """Run complete pocket hunting analysis."""
        print("=" * 70)
        print("M4 CRYPTIC POCKET HUNTER")
        print("Identifying Transient Druggable Cavities in c-Myc IDP")
        print("=" * 70)
        print()

        # Load data
        print("Loading REMD trajectory...")
        trajectory, topology = self.load_trajectory(traj_file, topology_file)
        sequence = topology['sequence']
        seq_hash = topology['sequence_hash']

        n_frames = len(trajectory)
        print(f"  Frames: {n_frames}")
        print(f"  Sequence: {sequence[:40]}...")
        print()

        # Hunt pockets
        pockets, var_explained, populations = self.hunt_pockets(
            trajectory, sequence, n_clusters
        )

        # Sort by druggability
        pockets.sort(key=lambda p: -p.druggability_score)

        print()
        print("-" * 70)
        print(f"POCKET HUNTING COMPLETE")
        print(f"  Total pockets found: {len(pockets)}")

        druggable = [p for p in pockets if p.druggability_score >= 0.6]
        print(f"  Highly druggable (score > 0.6): {len(druggable)}")

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save pocket structures
        pocket_files = {}
        for pocket in pockets[:5]:  # Top 5
            frame_coords = trajectory[pocket.representative_frame]
            pocket_file = self.output_dir / f"pocket_{pocket.pocket_id}_{timestamp}.npy"
            np.save(pocket_file, frame_coords)
            pocket_files[pocket.pocket_id] = str(pocket_file)

        # Save summary
        result = PocketHuntingResult(
            sequence=sequence,
            sequence_hash=seq_hash,
            n_frames_analyzed=n_frames,
            n_microstates=n_clusters,
            pockets_found=len(pockets),
            druggable_pockets=len(druggable),
            top_pockets=pockets[:5],
            pca_variance_explained=var_explained,
            microstate_populations=list(populations.values()),
            output_files=pocket_files,
            timestamp=timestamp
        )

        results_file = self.output_dir / f"pocket_hunting_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            result_dict = asdict(result)
            # Convert CrypticPocket objects
            result_dict['top_pockets'] = [asdict(p) for p in pockets[:5]]
            json.dump(result_dict, f, indent=2, default=str)

        print(f"\nResults saved to: {results_file}")

        return result


def main():
    """Run cryptic pocket hunting on c-Myc REMD trajectory."""
    print()
    print("=" * 70)
    print("DARK PROTEOME PIPELINE - STAGE 2")
    print("Cryptic Pocket Hunting in c-Myc Conformational Ensemble")
    print("=" * 70)
    print()
    print("Strategy: Find transient pockets that open >5% of simulation time")
    print("These are druggable targets in an 'undruggable' protein")
    print()
    print("LICENSE: AGPL-3.0-or-later (code) + OpenMTA (biological materials)")
    print("PRIOR ART ESTABLISHED: April 20, 2026")
    print()

    # Find trajectory files
    traj_dir = Path(__file__).parent / "trajectories"
    pocket_dir = Path(__file__).parent / "pockets"

    # Look for most recent trajectory
    traj_files = list(traj_dir.glob("cmyc_remd_300K_*.npy"))
    if not traj_files:
        print("ERROR: No REMD trajectory found!")
        print("Run m4_cmyc_remd_sampler.py first to generate trajectory.")
        return

    traj_file = sorted(traj_files)[-1]  # Most recent
    topology_file = traj_dir / traj_file.name.replace("remd_300K", "topology").replace(".npy", ".json")

    if not topology_file.exists():
        # Try alternate pattern
        topology_files = list(traj_dir.glob("cmyc_topology_*.json"))
        if topology_files:
            topology_file = sorted(topology_files)[-1]
        else:
            print("ERROR: No topology file found!")
            return

    print(f"Using trajectory: {traj_file}")
    print(f"Using topology: {topology_file}")
    print()

    # Run pocket hunting
    hunter = CrypticPocketHunter(pocket_dir)
    result = hunter.run_analysis(traj_file, topology_file, n_clusters=10)

    print()
    print("=" * 70)
    print("POCKET HUNTING COMPLETE")
    print()
    if result.druggable_pockets > 0:
        print(f"SUCCESS: Found {result.druggable_pockets} druggable pockets!")
        print()
        print("Top pocket details:")
        for pocket in result.top_pockets[:3]:
            print(f"  Pocket {pocket.pocket_id}:")
            print(f"    Population: {pocket.population*100:.1f}% of trajectory")
            print(f"    Volume: {pocket.volume:.1f} Å³")
            print(f"    Druggability: {pocket.druggability_score:.2f}")
        print()
        print("Next step: Run m4_cmyc_steric_trapper.py to design binders")
    else:
        print("No druggable pockets found.")
        print("Consider: Longer REMD simulation, different clustering parameters")
    print("=" * 70)


if __name__ == "__main__":
    main()

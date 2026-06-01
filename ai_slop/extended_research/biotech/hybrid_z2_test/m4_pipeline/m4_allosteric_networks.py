#!/usr/bin/env python3
"""
Z² Allosteric Network Analyzer

SPDX-License-Identifier: AGPL-3.0-or-later

Predicts allosteric communication pathways using Z² contact geometry.

THE KEY INSIGHT:
Allostery requires GEOMETRIC PATHWAYS through the contact network.
Z² = 8 contacts per residue creates OPTIMAL CONNECTIVITY for signal transmission.

Under-connected regions (< 8 contacts) are communication bottlenecks.
Over-connected regions (> 8 contacts) are communication hubs.
The balance of Z² packing determines allosteric efficiency.

ALLOSTERIC COMMUNICATION:
1. Binding at effector site perturbs local contacts
2. Perturbation propagates through contact network
3. Distant active site responds via coupled motions
4. Response time depends on path length and connectivity

Methods:
1. Dynamic cross-correlation from normal modes (which residues move together)
2. Perturbation response scanning (how changes propagate)
3. Network centrality analysis (identify communication hubs)
4. Community detection (allosteric domains)
5. Shortest path analysis (communication pathways)
6. Z² connectivity analysis (optimal vs bottleneck regions)

AlphaFold gives you the shape.
Z² tells you HOW SIGNALS FLOW THROUGH IT.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from scipy.spatial.distance import cdist
from scipy.linalg import eigh
from collections import defaultdict
import heapq
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103
Z = np.sqrt(Z2)       # ≈ 5.7888
OPTIMAL_CONTACTS = 8  # Z² predicts 8 contacts for optimal connectivity

print("=" * 70)
print("Z² ALLOSTERIC NETWORK ANALYZER")
print("=" * 70)
print(f"Z² = {Z2:.4f}")
print(f"Optimal connectivity = {OPTIMAL_CONTACTS} contacts/residue")
print("Mapping signal transmission pathways through contact geometry")
print("=" * 70)

# ==============================================================================
# STRUCTURE PARSING
# ==============================================================================

def parse_structure(pdb_path: str) -> Dict:
    """Parse PDB file for Cα coordinates and residue info."""
    coords = []
    residues = []

    AA_3TO1 = {
        'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
        'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
        'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
        'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
    }

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    res_name = line[17:20].strip()
                    res_num = int(line[22:26])
                    chain = line[21]

                    coords.append([x, y, z])
                    residues.append({
                        'name': res_name,
                        'num': res_num,
                        'chain': chain,
                        'aa': AA_3TO1.get(res_name, 'X')
                    })
                except ValueError:
                    continue

    return {
        'coords': np.array(coords),
        'residues': residues,
        'n_residues': len(residues)
    }


# ==============================================================================
# CONTACT NETWORK CONSTRUCTION
# ==============================================================================

def build_contact_network(coords: np.ndarray,
                          cutoff: float = 8.0,
                          exclude_neighbors: int = 2) -> Dict:
    """
    Build residue contact network with Z² analysis.

    Returns adjacency matrix and per-residue connectivity metrics.
    """
    n = len(coords)
    distances = cdist(coords, coords)

    # Build adjacency matrix
    adjacency = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) > exclude_neighbors and distances[i, j] < cutoff:
                adjacency[i, j] = 1
                adjacency[j, i] = 1

    # Per-residue connectivity
    degree = adjacency.sum(axis=1)

    # Z² connectivity analysis
    z2_deviation = degree - OPTIMAL_CONTACTS

    # Classify connectivity
    hubs = []  # Over-connected (> 10 contacts)
    optimal = []  # Z² optimal (7-9 contacts)
    bottlenecks = []  # Under-connected (< 6 contacts)

    for i in range(n):
        if degree[i] >= 10:
            hubs.append(i)
        elif degree[i] >= 7:
            optimal.append(i)
        elif degree[i] < 6:
            bottlenecks.append(i)

    return {
        'adjacency': adjacency,
        'distances': distances,
        'degree': degree.tolist(),
        'z2_deviation': z2_deviation.tolist(),
        'mean_degree': float(np.mean(degree)),
        'hubs': hubs,
        'optimal': optimal,
        'bottlenecks': bottlenecks,
        'n_edges': int(adjacency.sum() / 2)
    }


# ==============================================================================
# NORMAL MODE ANALYSIS FOR DYNAMICS
# ==============================================================================

def compute_anm_modes(coords: np.ndarray,
                      cutoff: float = 13.0,
                      n_modes: int = 20) -> Dict:
    """
    Compute Anisotropic Network Model (ANM) normal modes.

    These reveal the natural motions of the protein.
    """
    n = len(coords)

    # Build Hessian matrix
    hessian = np.zeros((3 * n, 3 * n))

    for i in range(n):
        for j in range(i + 1, n):
            diff = coords[j] - coords[i]
            dist = np.linalg.norm(diff)

            if dist < cutoff:
                # Spring constant with distance weighting
                gamma = 1.0 / (dist ** 2)

                # Outer product for direction
                outer = np.outer(diff, diff) / (dist ** 2)

                # Fill Hessian blocks
                for a in range(3):
                    for b in range(3):
                        val = gamma * outer[a, b]
                        hessian[3*i + a, 3*j + b] = -val
                        hessian[3*j + b, 3*i + a] = -val
                        hessian[3*i + a, 3*i + b] += val
                        hessian[3*j + a, 3*j + b] += val

    # Eigendecomposition
    eigenvalues, eigenvectors = eigh(hessian)

    # Skip first 6 zero modes (rigid body)
    nonzero_mask = eigenvalues > 1e-6
    eigenvalues = eigenvalues[nonzero_mask]
    eigenvectors = eigenvectors[:, nonzero_mask]

    # Take lowest n_modes
    n_modes = min(n_modes, len(eigenvalues))
    eigenvalues = eigenvalues[:n_modes]
    eigenvectors = eigenvectors[:, :n_modes]

    # Reshape eigenvectors to (n_residues, 3, n_modes)
    modes = eigenvectors.reshape(n, 3, n_modes)

    return {
        'eigenvalues': eigenvalues,
        'modes': modes,
        'n_modes': n_modes
    }


# ==============================================================================
# DYNAMIC CROSS-CORRELATION
# ==============================================================================

def compute_cross_correlation(modes: np.ndarray,
                              eigenvalues: np.ndarray) -> np.ndarray:
    """
    Compute dynamic cross-correlation matrix from normal modes.

    C_ij measures how much residues i and j move together.
    C_ij = +1: perfect correlation (same direction)
    C_ij = -1: perfect anti-correlation (opposite direction)
    C_ij = 0: uncorrelated
    """
    n_residues = modes.shape[0]
    n_modes = modes.shape[2]

    # Covariance matrix
    covariance = np.zeros((n_residues, n_residues))

    for mode_idx in range(n_modes):
        # Weight by 1/eigenvalue (lower frequency = larger amplitude)
        weight = 1.0 / eigenvalues[mode_idx]

        for i in range(n_residues):
            for j in range(n_residues):
                # Dot product of mode vectors
                cov_ij = np.dot(modes[i, :, mode_idx], modes[j, :, mode_idx])
                covariance[i, j] += weight * cov_ij

    # Normalize to correlation
    correlation = np.zeros((n_residues, n_residues))

    for i in range(n_residues):
        for j in range(n_residues):
            denom = np.sqrt(covariance[i, i] * covariance[j, j])
            if denom > 1e-10:
                correlation[i, j] = covariance[i, j] / denom

    return correlation


def identify_correlated_pairs(correlation: np.ndarray,
                              residues: List[Dict],
                              threshold: float = 0.7,
                              min_distance: int = 10) -> List[Dict]:
    """
    Identify strongly correlated residue pairs.

    These indicate allosteric coupling.
    """
    n = len(correlation)
    pairs = []

    for i in range(n):
        for j in range(i + min_distance, n):
            corr = correlation[i, j]

            if abs(corr) >= threshold:
                pairs.append({
                    'residue1_idx': i,
                    'residue2_idx': j,
                    'residue1': f"{residues[i]['name']}{residues[i]['num']}",
                    'residue2': f"{residues[j]['name']}{residues[j]['num']}",
                    'correlation': float(corr),
                    'type': 'correlated' if corr > 0 else 'anti-correlated',
                    'sequence_distance': j - i
                })

    # Sort by absolute correlation
    pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)

    return pairs


# ==============================================================================
# PERTURBATION RESPONSE SCANNING
# ==============================================================================

def perturbation_response_matrix(coords: np.ndarray,
                                 modes: np.ndarray,
                                 eigenvalues: np.ndarray) -> np.ndarray:
    """
    Compute perturbation response scanning matrix.

    PRS_ij = response at j when i is perturbed
    High PRS_ij means j responds strongly to perturbations at i.
    """
    n_residues = modes.shape[0]
    n_modes = modes.shape[2]

    # Response matrix
    prs = np.zeros((n_residues, n_residues))

    for mode_idx in range(n_modes):
        # Weight by 1/eigenvalue^2 (response strength)
        weight = 1.0 / (eigenvalues[mode_idx] ** 2)

        mode = modes[:, :, mode_idx]

        for i in range(n_residues):
            # Perturbation at i
            pert_i = mode[i]
            pert_norm = np.linalg.norm(pert_i)

            if pert_norm < 1e-10:
                continue

            for j in range(n_residues):
                # Response at j
                resp_j = mode[j]
                resp_norm = np.linalg.norm(resp_j)

                # PRS contribution
                prs[i, j] += weight * pert_norm * resp_norm

    # Normalize
    max_prs = prs.max()
    if max_prs > 0:
        prs = prs / max_prs

    return prs


def identify_allosteric_pairs(prs: np.ndarray,
                              residues: List[Dict],
                              threshold: float = 0.5,
                              min_distance: int = 15) -> List[Dict]:
    """
    Identify allosteric effector-response pairs from PRS.
    """
    n = len(prs)
    pairs = []

    for i in range(n):
        for j in range(n):
            if abs(i - j) >= min_distance and prs[i, j] >= threshold:
                pairs.append({
                    'effector_idx': i,
                    'response_idx': j,
                    'effector': f"{residues[i]['name']}{residues[i]['num']}",
                    'response': f"{residues[j]['name']}{residues[j]['num']}",
                    'prs_score': float(prs[i, j]),
                    'sequence_distance': abs(j - i)
                })

    pairs.sort(key=lambda x: x['prs_score'], reverse=True)

    return pairs


# ==============================================================================
# NETWORK CENTRALITY ANALYSIS
# ==============================================================================

def compute_network_centrality(adjacency: np.ndarray) -> Dict:
    """
    Compute various centrality measures for the contact network.

    - Degree centrality: number of contacts
    - Betweenness centrality: how often on shortest paths
    - Closeness centrality: average distance to all others
    """
    n = len(adjacency)

    # Degree centrality (already computed as adjacency.sum())
    degree = adjacency.sum(axis=1)
    degree_centrality = degree / (n - 1)

    # Compute all-pairs shortest paths (Floyd-Warshall)
    # Use inverse adjacency as distance (0 for connected, inf for not)
    dist_matrix = np.full((n, n), np.inf)
    np.fill_diagonal(dist_matrix, 0)

    for i in range(n):
        for j in range(n):
            if adjacency[i, j] > 0:
                dist_matrix[i, j] = 1

    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist_matrix[i, k] + dist_matrix[k, j] < dist_matrix[i, j]:
                    dist_matrix[i, j] = dist_matrix[i, k] + dist_matrix[k, j]

    # Closeness centrality
    closeness = np.zeros(n)
    for i in range(n):
        reachable = dist_matrix[i] < np.inf
        if reachable.sum() > 1:
            closeness[i] = (reachable.sum() - 1) / dist_matrix[i][reachable].sum()

    # Betweenness centrality (simplified version)
    betweenness = np.zeros(n)

    for s in range(n):
        for t in range(n):
            if s != t and dist_matrix[s, t] < np.inf:
                # Find all nodes on shortest path from s to t
                d_st = dist_matrix[s, t]
                for v in range(n):
                    if v != s and v != t:
                        # v is on shortest path if d(s,v) + d(v,t) = d(s,t)
                        if dist_matrix[s, v] + dist_matrix[v, t] == d_st:
                            betweenness[v] += 1

    # Normalize betweenness
    max_betweenness = (n - 1) * (n - 2)
    if max_betweenness > 0:
        betweenness = betweenness / max_betweenness

    return {
        'degree_centrality': degree_centrality.tolist(),
        'closeness_centrality': closeness.tolist(),
        'betweenness_centrality': betweenness.tolist(),
        'distance_matrix': dist_matrix
    }


def identify_communication_hubs(centrality: Dict,
                                residues: List[Dict],
                                top_n: int = 10) -> List[Dict]:
    """
    Identify residues that are critical for communication.

    Hubs have high betweenness centrality.
    """
    n = len(residues)

    # Composite hub score
    hub_scores = []
    for i in range(n):
        score = (
            0.3 * centrality['degree_centrality'][i] +
            0.5 * centrality['betweenness_centrality'][i] +
            0.2 * centrality['closeness_centrality'][i]
        )
        hub_scores.append(score)

    # Rank and return top hubs
    ranked = sorted(range(n), key=lambda i: hub_scores[i], reverse=True)

    hubs = []
    for rank, idx in enumerate(ranked[:top_n]):
        hubs.append({
            'rank': rank + 1,
            'residue_idx': idx,
            'residue': f"{residues[idx]['name']}{residues[idx]['num']}",
            'hub_score': float(hub_scores[idx]),
            'degree': float(centrality['degree_centrality'][idx]),
            'betweenness': float(centrality['betweenness_centrality'][idx]),
            'closeness': float(centrality['closeness_centrality'][idx])
        })

    return hubs


# ==============================================================================
# COMMUNITY DETECTION (ALLOSTERIC DOMAINS)
# ==============================================================================

def detect_communities(correlation: np.ndarray,
                       n_communities: int = 4) -> List[List[int]]:
    """
    Detect allosteric communities using spectral clustering on correlation matrix.

    Communities are groups of residues that move together.
    """
    n = len(correlation)

    # Use absolute correlation as similarity
    similarity = np.abs(correlation)

    # Degree matrix
    degree = similarity.sum(axis=1)
    D = np.diag(degree)

    # Laplacian
    L = D - similarity

    # Normalized Laplacian
    D_inv_sqrt = np.diag(1.0 / np.sqrt(degree + 1e-10))
    L_norm = D_inv_sqrt @ L @ D_inv_sqrt

    # Eigendecomposition of Laplacian
    eigenvalues, eigenvectors = eigh(L_norm)

    # Use first k eigenvectors for clustering
    k = min(n_communities, n - 1)
    features = eigenvectors[:, :k]

    # Simple k-means-like assignment
    # Initialize centroids randomly
    np.random.seed(42)
    centroid_indices = np.random.choice(n, k, replace=False)
    centroids = features[centroid_indices]

    # Iterate
    for _ in range(20):
        # Assign to nearest centroid
        assignments = np.zeros(n, dtype=int)
        for i in range(n):
            dists = [np.linalg.norm(features[i] - centroids[c]) for c in range(k)]
            assignments[i] = np.argmin(dists)

        # Update centroids
        new_centroids = []
        for c in range(k):
            members = features[assignments == c]
            if len(members) > 0:
                new_centroids.append(members.mean(axis=0))
            else:
                new_centroids.append(centroids[c])
        centroids = np.array(new_centroids)

    # Convert to community lists
    communities = [[] for _ in range(k)]
    for i, c in enumerate(assignments):
        communities[c].append(i)

    # Sort by size
    communities.sort(key=len, reverse=True)

    return communities


def analyze_communities(communities: List[List[int]],
                        residues: List[Dict],
                        correlation: np.ndarray) -> List[Dict]:
    """
    Analyze properties of each allosteric community.
    """
    results = []

    for i, community in enumerate(communities):
        if len(community) == 0:
            continue

        # Get residue names
        res_names = [f"{residues[r]['name']}{residues[r]['num']}" for r in community]

        # Intra-community correlation
        if len(community) > 1:
            intra_corr = []
            for r1 in community:
                for r2 in community:
                    if r1 < r2:
                        intra_corr.append(correlation[r1, r2])
            mean_intra_corr = float(np.mean(intra_corr)) if intra_corr else 0
        else:
            mean_intra_corr = 1.0

        # Inter-community correlations
        inter_corr = defaultdict(list)
        for r in community:
            for j, other_community in enumerate(communities):
                if i != j:
                    for other_r in other_community:
                        inter_corr[j].append(correlation[r, other_r])

        inter_correlations = {}
        for j, corrs in inter_corr.items():
            inter_correlations[f"community_{j+1}"] = float(np.mean(corrs))

        results.append({
            'community_id': i + 1,
            'n_residues': len(community),
            'residue_indices': community,
            'residue_names': res_names[:10],  # First 10 for brevity
            'mean_intra_correlation': mean_intra_corr,
            'inter_correlations': inter_correlations
        })

    return results


# ==============================================================================
# SHORTEST PATH ANALYSIS
# ==============================================================================

def find_allosteric_paths(distance_matrix: np.ndarray,
                          adjacency: np.ndarray,
                          source: int,
                          target: int,
                          max_paths: int = 5) -> List[List[int]]:
    """
    Find shortest paths between two residues.

    These are the allosteric communication pathways.
    """
    n = len(distance_matrix)

    if distance_matrix[source, target] == np.inf:
        return []  # No path exists

    # BFS to find shortest path
    paths = []
    queue = [(source, [source])]
    visited_at_length = {source: 0}
    target_length = distance_matrix[source, target]

    while queue and len(paths) < max_paths:
        current, path = queue.pop(0)

        if current == target:
            paths.append(path)
            continue

        if len(path) - 1 >= target_length:
            continue

        # Explore neighbors
        for neighbor in range(n):
            if adjacency[current, neighbor] > 0:
                new_length = len(path)
                # Allow visiting if we haven't been here at this length
                if neighbor not in visited_at_length or visited_at_length[neighbor] >= new_length:
                    visited_at_length[neighbor] = new_length
                    queue.append((neighbor, path + [neighbor]))

    return paths


def analyze_allosteric_pathway(path: List[int],
                               residues: List[Dict],
                               network: Dict,
                               correlation: np.ndarray) -> Dict:
    """
    Analyze properties of an allosteric pathway.
    """
    n = len(path)

    # Get residue names
    res_names = [f"{residues[r]['name']}{residues[r]['num']}" for r in path]

    # Connectivity along path
    connectivities = [network['degree'][r] for r in path]

    # Correlations along path
    path_correlations = []
    for i in range(n - 1):
        path_correlations.append(correlation[path[i], path[i+1]])

    # Identify bottlenecks (low connectivity)
    bottlenecks = []
    for i, (r, conn) in enumerate(zip(path, connectivities)):
        if conn < 6:
            bottlenecks.append({
                'position': i,
                'residue': res_names[i],
                'connectivity': conn
            })

    # Path efficiency
    mean_correlation = np.mean(path_correlations) if path_correlations else 0
    mean_connectivity = np.mean(connectivities)

    return {
        'path': path,
        'residues': res_names,
        'length': n,
        'connectivities': connectivities,
        'correlations': path_correlations,
        'mean_correlation': float(mean_correlation),
        'mean_connectivity': float(mean_connectivity),
        'bottlenecks': bottlenecks,
        'efficiency': float(mean_correlation * mean_connectivity / OPTIMAL_CONTACTS)
    }


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def generate_allosteric_visualization(coords: np.ndarray,
                                      correlation: np.ndarray,
                                      communities: List[List[int]],
                                      hubs: List[Dict],
                                      prs: np.ndarray,
                                      output_path: str):
    """Generate allosteric network visualization."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    fig = plt.figure(figsize=(16, 12))

    # 1. Cross-correlation matrix
    ax1 = fig.add_subplot(2, 2, 1)
    im1 = ax1.imshow(correlation, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
    ax1.set_xlabel('Residue')
    ax1.set_ylabel('Residue')
    ax1.set_title('Dynamic Cross-Correlation Matrix')
    plt.colorbar(im1, ax=ax1, label='Correlation')

    # 2. Perturbation response matrix
    ax2 = fig.add_subplot(2, 2, 2)
    im2 = ax2.imshow(prs, cmap='YlOrRd', aspect='auto')
    ax2.set_xlabel('Response Site')
    ax2.set_ylabel('Perturbation Site')
    ax2.set_title('Perturbation Response Scanning (PRS)')
    plt.colorbar(im2, ax=ax2, label='Response')

    # 3. 3D structure colored by community
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')

    colors = plt.cm.Set1(np.linspace(0, 1, len(communities)))

    for i, community in enumerate(communities):
        if len(community) > 0:
            comm_coords = coords[community]
            ax3.scatter(comm_coords[:, 0], comm_coords[:, 1], comm_coords[:, 2],
                       c=[colors[i]], s=50, label=f'Community {i+1}', alpha=0.7)

    # Mark hubs
    for hub in hubs[:5]:
        idx = hub['residue_idx']
        ax3.scatter(coords[idx, 0], coords[idx, 1], coords[idx, 2],
                   c='red', s=200, marker='*', edgecolors='black', linewidths=2)

    ax3.set_xlabel('X (Å)')
    ax3.set_ylabel('Y (Å)')
    ax3.set_zlabel('Z (Å)')
    ax3.set_title('Allosteric Communities (stars = hubs)')
    ax3.legend(loc='upper left', fontsize=8)

    # 4. Hub scores
    ax4 = fig.add_subplot(2, 2, 4)

    n_hubs = min(10, len(hubs))
    hub_names = [h['residue'] for h in hubs[:n_hubs]]
    hub_scores = [h['hub_score'] for h in hubs[:n_hubs]]

    bars = ax4.barh(hub_names, hub_scores, color='darkred')
    ax4.set_xlabel('Hub Score')
    ax4.set_title('Top Communication Hubs')
    ax4.invert_yaxis()

    for bar, score in zip(bars, hub_scores):
        ax4.text(score + 0.01, bar.get_y() + bar.get_height()/2,
                f'{score:.3f}', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Visualization saved: {output_path}")


# ==============================================================================
# MAIN ANALYSIS
# ==============================================================================

def analyze_allosteric_network(pdb_path: str,
                               output_dir: str = "allosteric_networks") -> Dict:
    """
    Full allosteric network analysis pipeline.
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nLoading structure: {pdb_path}")
    structure = parse_structure(pdb_path)
    coords = structure['coords']
    residues = structure['residues']
    n_residues = structure['n_residues']

    print(f"  Residues: {n_residues}")

    # 1. Build contact network
    print("\nBuilding contact network...")
    network = build_contact_network(coords)
    print(f"  Edges: {network['n_edges']}")
    print(f"  Mean degree: {network['mean_degree']:.1f} (Z² optimal = {OPTIMAL_CONTACTS})")
    print(f"  Hubs (>10 contacts): {len(network['hubs'])}")
    print(f"  Bottlenecks (<6 contacts): {len(network['bottlenecks'])}")

    # 2. Normal mode analysis
    print("\nComputing normal modes...")
    anm = compute_anm_modes(coords)
    print(f"  Computed {anm['n_modes']} modes")

    # 3. Cross-correlation
    print("\nComputing dynamic cross-correlation...")
    correlation = compute_cross_correlation(anm['modes'], anm['eigenvalues'])

    correlated_pairs = identify_correlated_pairs(correlation, residues)
    print(f"  Strongly correlated pairs: {len(correlated_pairs)}")

    # 4. Perturbation response
    print("\nComputing perturbation response...")
    prs = perturbation_response_matrix(coords, anm['modes'], anm['eigenvalues'])

    allosteric_pairs = identify_allosteric_pairs(prs, residues)
    print(f"  Allosteric effector-response pairs: {len(allosteric_pairs)}")

    # 5. Network centrality
    print("\nComputing network centrality...")
    centrality = compute_network_centrality(network['adjacency'])

    hubs = identify_communication_hubs(centrality, residues)
    print(f"  Top hub: {hubs[0]['residue']} (score {hubs[0]['hub_score']:.3f})")

    # 6. Community detection
    print("\nDetecting allosteric communities...")
    communities = detect_communities(correlation)
    community_analysis = analyze_communities(communities, residues, correlation)
    print(f"  Identified {len(communities)} communities")

    for comm in community_analysis:
        print(f"    Community {comm['community_id']}: {comm['n_residues']} residues, "
              f"intra-corr={comm['mean_intra_correlation']:.2f}")

    # 7. Example pathway analysis
    print("\nAnalyzing allosteric pathways...")

    # Find pathway between top allosteric pair
    if allosteric_pairs:
        top_pair = allosteric_pairs[0]
        source = top_pair['effector_idx']
        target = top_pair['response_idx']

        paths = find_allosteric_paths(
            centrality['distance_matrix'],
            network['adjacency'],
            source, target
        )

        pathway_analyses = []
        for path in paths[:3]:
            analysis = analyze_allosteric_pathway(path, residues, network, correlation)
            pathway_analyses.append(analysis)

        print(f"  Top pathway: {top_pair['effector']} → {top_pair['response']}")
        if pathway_analyses:
            print(f"    Length: {pathway_analyses[0]['length']} residues")
            print(f"    Efficiency: {pathway_analyses[0]['efficiency']:.3f}")
    else:
        pathway_analyses = []

    # Generate visualization
    print(f"\n{'='*60}")
    print("GENERATING OUTPUTS")
    print(f"{'='*60}")

    viz_path = os.path.join(output_dir, "allosteric_network.png")
    generate_allosteric_visualization(
        coords, correlation, communities, hubs, prs, viz_path
    )

    # Compile results
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_pdb': pdb_path,
        'n_residues': n_residues,
        'z2_constant': Z2,
        'network_summary': {
            'n_edges': network['n_edges'],
            'mean_degree': network['mean_degree'],
            'n_hubs': len(network['hubs']),
            'n_bottlenecks': len(network['bottlenecks']),
            'z2_deviation_mean': float(np.mean(network['z2_deviation']))
        },
        'top_hubs': hubs[:10],
        'communities': community_analysis,
        'correlated_pairs': correlated_pairs[:20],
        'allosteric_pairs': allosteric_pairs[:20],
        'top_pathway': pathway_analyses[0] if pathway_analyses else None,
        'per_residue': {
            'degree': network['degree'],
            'z2_deviation': network['z2_deviation'],
            'betweenness': centrality['betweenness_centrality']
        },
        'output_files': {
            'visualization': viz_path
        }
    }

    # Save JSON
    json_path = os.path.join(output_dir, "allosteric_results.json")
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"  ✓ Results saved: {json_path}")

    # Summary
    print(f"\n{'='*60}")
    print("Z² ALLOSTERIC NETWORK ANALYSIS COMPLETE")
    print(f"{'='*60}")

    print(f"""
  NETWORK STATISTICS:
  - Mean connectivity: {network['mean_degree']:.1f} contacts/residue
  - Z² deviation: {np.mean(network['z2_deviation']):.2f} from optimal
  - Communication hubs: {len(network['hubs'])}
  - Bottlenecks: {len(network['bottlenecks'])}

  ALLOSTERIC COMMUNITIES: {len(communities)}
  - These are groups of residues that move together
  - Inter-community communication enables allostery

  TOP COMMUNICATION HUB: {hubs[0]['residue']}
  - Betweenness: {hubs[0]['betweenness']:.3f}
  - Mutations here would disrupt signaling

  Z² INTERPRETATION:
  Allosteric communication requires Z² = 8 contact connectivity.
  - Hubs (>10 contacts): signal amplifiers
  - Bottlenecks (<6 contacts): signal attenuators
  - Optimal (8 contacts): efficient signal transmission

  AlphaFold gives you the shape.
  Z² tells you HOW SIGNALS FLOW THROUGH IT.
""")

    return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run allosteric network analysis on Z² protein."""
    import sys

    if len(sys.argv) > 1:
        pdb_path = sys.argv[1]
    else:
        pdb_path = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"

    if not os.path.exists(pdb_path):
        print(f"PDB not found: {pdb_path}")
        return None

    results = analyze_allosteric_network(pdb_path, output_dir="allosteric_networks")

    return results


if __name__ == "__main__":
    results = main()

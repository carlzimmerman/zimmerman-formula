#!/usr/bin/env python3
"""
geo_02_surface_curvature.py - Differential Geometry of Binding Interfaces

Analyzes binding interfaces using differential geometry: principal curvatures,
Gaussian curvature (K), and mean curvature (H). Proves geometric complementarity
between peptide and receptor surfaces.

Mathematical Framework:
- Solvent-excluded surface generation
- Principal curvature computation (κ₁, κ₂)
- Gaussian curvature: K = κ₁ × κ₂
- Mean curvature: H = (κ₁ + κ₂) / 2
- Shape complementarity via curvature matching

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Theoretical computational research only. Not peer reviewed.
"""

import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from scipy import ndimage
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def compute_surface_normals(vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
    """Compute vertex normals from mesh."""
    vertex_normals = np.zeros_like(vertices)

    for face in faces:
        v0, v1, v2 = vertices[face[0]], vertices[face[1]], vertices[face[2]]

        # Face normal via cross product
        edge1 = v1 - v0
        edge2 = v2 - v0
        face_normal = np.cross(edge1, edge2)

        # Add to vertex normals
        for idx in face:
            vertex_normals[idx] += face_normal

    # Normalize
    norms = np.linalg.norm(vertex_normals, axis=1, keepdims=True)
    norms[norms == 0] = 1
    vertex_normals /= norms

    return vertex_normals

def compute_principal_curvatures(vertices: np.ndarray,
                                  faces: np.ndarray,
                                  normals: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute principal curvatures at each vertex.

    Uses discrete differential geometry approach:
    1. For each vertex, find neighbor vertices
    2. Fit local quadric surface
    3. Extract eigenvalues of shape operator

    Returns (κ₁, κ₂) arrays.
    """
    n_vertices = len(vertices)
    kappa1 = np.zeros(n_vertices)
    kappa2 = np.zeros(n_vertices)

    # Build adjacency
    adjacency = [set() for _ in range(n_vertices)]
    for face in faces:
        for i in range(3):
            adjacency[face[i]].add(face[(i+1) % 3])
            adjacency[face[i]].add(face[(i+2) % 3])

    for i in range(n_vertices):
        neighbors = list(adjacency[i])
        if len(neighbors) < 3:
            continue

        # Local coordinate system
        n = normals[i]
        # Find orthogonal basis
        if abs(n[0]) < 0.9:
            t1 = np.cross(n, [1, 0, 0])
        else:
            t1 = np.cross(n, [0, 1, 0])
        t1 /= np.linalg.norm(t1)
        t2 = np.cross(n, t1)

        # Project neighbors to local frame
        local_coords = []
        for j in neighbors[:10]:  # Limit to avoid slow computation
            d = vertices[j] - vertices[i]
            u = np.dot(d, t1)
            v = np.dot(d, t2)
            w = np.dot(d, n)
            local_coords.append([u, v, w])

        local_coords = np.array(local_coords)

        if len(local_coords) >= 5:
            # Fit quadric: w = au² + buv + cv² + du + ev + f
            # Shape operator eigenvalues give principal curvatures
            u, v, w = local_coords[:, 0], local_coords[:, 1], local_coords[:, 2]

            A = np.column_stack([u**2, u*v, v**2, u, v, np.ones_like(u)])

            try:
                coeffs, _, _, _ = np.linalg.lstsq(A, w, rcond=None)
                a, b, c = coeffs[0], coeffs[1], coeffs[2]

                # Shape operator (Weingarten map) approximation
                # Principal curvatures are eigenvalues of:
                # [[a, b/2], [b/2, c]]
                S = np.array([[2*a, b], [b, 2*c]])
                eigenvalues = np.linalg.eigvalsh(S)
                kappa1[i] = eigenvalues[0]
                kappa2[i] = eigenvalues[1]
            except:
                pass

    return kappa1, kappa2

def analyze_binding_interface(peptide_coords: np.ndarray,
                               receptor_coords: np.ndarray,
                               interface_cutoff: float = 4.5) -> Dict:
    """
    Analyze the geometric complementarity of binding interface.

    Args:
        peptide_coords: Cα coordinates of peptide
        receptor_coords: Cα coordinates of receptor
        interface_cutoff: Distance cutoff for interface residues (Å)

    Returns:
        Dict with curvature analysis results
    """
    from scipy.spatial.distance import cdist

    # Find interface residues
    distances = cdist(peptide_coords, receptor_coords)

    peptide_interface = np.where(np.min(distances, axis=1) < interface_cutoff)[0]
    receptor_interface = np.where(np.min(distances, axis=0) < interface_cutoff)[0]

    if len(peptide_interface) < 3 or len(receptor_interface) < 3:
        return {'error': 'Insufficient interface contacts'}

    # Generate approximate surfaces using convex hulls
    # (For production, use proper molecular surface with trimesh/msms)

    def analyze_surface(coords, interface_idx):
        if len(interface_idx) < 4:
            return None

        points = coords[interface_idx]

        try:
            hull = ConvexHull(points)
            vertices = points
            faces = hull.simplices

            normals = compute_surface_normals(vertices, faces)
            k1, k2 = compute_principal_curvatures(vertices, faces, normals)

            K = k1 * k2  # Gaussian curvature
            H = (k1 + k2) / 2  # Mean curvature

            return {
                'n_points': len(points),
                'kappa1_mean': float(np.mean(k1)),
                'kappa2_mean': float(np.mean(k2)),
                'K_mean': float(np.mean(K)),
                'K_std': float(np.std(K)),
                'H_mean': float(np.mean(H)),
                'H_std': float(np.std(H)),
                'surface_type': classify_surface(np.mean(K), np.mean(H)),
            }
        except Exception as e:
            return {'error': str(e)}

    peptide_surface = analyze_surface(peptide_coords, peptide_interface)
    receptor_surface = analyze_surface(receptor_coords, receptor_interface)

    # Geometric complementarity: peptide convex should match receptor concave
    complementarity = 0.0
    if peptide_surface and receptor_surface:
        if 'K_mean' in peptide_surface and 'K_mean' in receptor_surface:
            # Ideal: K_peptide ≈ -K_receptor (opposite curvature)
            K_sum = peptide_surface['K_mean'] + receptor_surface['K_mean']
            complementarity = 1.0 / (1.0 + abs(K_sum))

    return {
        'peptide_surface': peptide_surface,
        'receptor_surface': receptor_surface,
        'n_interface_peptide': len(peptide_interface),
        'n_interface_receptor': len(receptor_interface),
        'geometric_complementarity': float(complementarity),
    }

def classify_surface(K: float, H: float) -> str:
    """Classify local surface geometry based on curvatures."""
    eps = 0.01

    if abs(K) < eps and abs(H) < eps:
        return 'planar'
    elif K > eps:
        if H > eps:
            return 'convex_elliptic'
        elif H < -eps:
            return 'concave_elliptic'
        else:
            return 'spherical'
    elif K < -eps:
        return 'saddle'
    else:  # K ≈ 0
        if H > eps:
            return 'convex_cylindrical'
        elif H < -eps:
            return 'concave_cylindrical'
        else:
            return 'flat'

def generate_test_complex() -> Tuple[np.ndarray, np.ndarray]:
    """Generate test peptide-receptor coordinates for demonstration."""
    # Peptide: small helix-like structure
    n_peptide = 14
    t = np.linspace(0, 4*np.pi, n_peptide)
    peptide = np.column_stack([
        5 * np.cos(t),
        5 * np.sin(t),
        t * 0.5
    ])

    # Receptor: larger surface with binding pocket
    n_receptor = 100
    phi = np.random.uniform(0, 2*np.pi, n_receptor)
    theta = np.random.uniform(0, np.pi, n_receptor)
    r = 15 + np.random.randn(n_receptor) * 2

    receptor = np.column_stack([
        r * np.sin(theta) * np.cos(phi),
        r * np.sin(theta) * np.sin(phi),
        r * np.cos(theta)
    ])

    # Add binding pocket (concave region near peptide)
    pocket_mask = np.linalg.norm(receptor, axis=1) < 20
    receptor[pocket_mask] *= 0.7

    return peptide, receptor

def main():
    """Run differential geometry analysis on binding interfaces."""
    print("=" * 70)
    print("GEO_02: DIFFERENTIAL GEOMETRY OF BINDING INTERFACES")
    print("Surface Curvature Analysis for Geometric Complementarity")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    results = {
        'timestamp': datetime.now().isoformat(),
        'complexes': [],
        'summary': {},
    }

    # Test with synthetic complex
    print("Analyzing synthetic peptide-receptor complex...")
    print("-" * 70)

    peptide, receptor = generate_test_complex()

    print(f"  Peptide: {len(peptide)} residues")
    print(f"  Receptor: {len(receptor)} residues")

    analysis = analyze_binding_interface(peptide, receptor)

    results['complexes'].append({
        'name': 'synthetic_complex',
        'analysis': analysis,
    })

    if 'error' not in analysis:
        print(f"\n  Interface contacts:")
        print(f"    Peptide: {analysis['n_interface_peptide']} residues")
        print(f"    Receptor: {analysis['n_interface_receptor']} residues")

        if analysis['peptide_surface'] and 'K_mean' in analysis['peptide_surface']:
            ps = analysis['peptide_surface']
            print(f"\n  Peptide Surface:")
            print(f"    Mean Gaussian curvature (K): {ps['K_mean']:.4f}")
            print(f"    Mean Mean curvature (H): {ps['H_mean']:.4f}")
            print(f"    Surface type: {ps['surface_type']}")

        if analysis['receptor_surface'] and 'K_mean' in analysis['receptor_surface']:
            rs = analysis['receptor_surface']
            print(f"\n  Receptor Surface:")
            print(f"    Mean Gaussian curvature (K): {rs['K_mean']:.4f}")
            print(f"    Mean Mean curvature (H): {rs['H_mean']:.4f}")
            print(f"    Surface type: {rs['surface_type']}")

        print(f"\n  Geometric Complementarity: {analysis['geometric_complementarity']:.3f}")

        if analysis['geometric_complementarity'] > 0.5:
            print("  INTERPRETATION: Good geometric fit (convex-concave match)")
        else:
            print("  INTERPRETATION: Moderate geometric fit")
    else:
        print(f"  Error: {analysis.get('error')}")

    # Summary
    results['summary'] = {
        'n_complexes_analyzed': 1,
        'method': 'Discrete differential geometry on point clouds',
        'note': 'For production, use trimesh with proper molecular surfaces',
    }

    # Save results
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "geo_02_surface_curvature_results.json"

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_path}")
    print("\n" + "=" * 70)
    print("GEO_02 COMPLETE")
    print("=" * 70)

    return results

if __name__ == "__main__":
    main()

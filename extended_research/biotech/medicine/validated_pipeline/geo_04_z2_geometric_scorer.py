#!/usr/bin/env python3
"""
geo_04_z2_geometric_scorer.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

geo_04_z2_geometric_scorer.py - Z² Geometric Scoring Engine

Scores protein structures against the Z² framework constants:
- Voronoi packing volume target: Z² = 33.51 Å³
- Delaunay contact distance target: √Z² = 5.79 Å

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from scipy.spatial import Voronoi, Delaunay, ConvexHull
import argparse
import sys

def parse_pdb_coordinates(pdb_file):
    """Extracts heavy atom coordinates from a PDB file, ignoring hydrogens and water."""
    coords = []
    atoms = []
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                element = line[76:78].strip()
                res_name = line[17:20].strip()
                # Skip waters and hydrogens
                if res_name == "HOH" or element == "H":
                    continue

                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                coords.append([x, y, z])
                atoms.append(element)
    return np.array(coords), atoms

def calculate_voronoi_volumes(coords):
    """Calculates bounded Voronoi cell volumes for the point cloud."""
    vor = Voronoi(coords)
    volumes = []

    for point_idx, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]
        # If the region is empty or has a vertex at infinity (-1), it's a boundary atom.
        if not region or -1 in region:
            continue

        # Get the vertices for this specific bounded cell
        cell_vertices = vor.vertices[region]

        try:
            # The volume of the Voronoi cell is the volume of its Convex Hull
            hull = ConvexHull(cell_vertices)
            volumes.append(hull.volume)
        except Exception:
            pass # Handle coplanar/degenerate vertices

    return np.array(volumes)

def calculate_delaunay_edges(coords):
    """Calculates all unique non-covalent Delaunay edge distances."""
    tri = Delaunay(coords)
    edges = set()

    # Extract all edges from the simplices (tetrahedrons)
    for simplex in tri.simplices:
        for i in range(4):
            for j in range(i+1, 4):
                # Sort to ensure unique undirected edges
                edge = tuple(sorted([simplex[i], simplex[j]]))
                edges.add(edge)

    distances = []
    for edge in edges:
        p1 = coords[edge[0]]
        p2 = coords[edge[1]]
        dist = np.linalg.norm(p1 - p2)

        # Filter out covalent bonds (< 2.0 Angstroms)
        if dist > 2.0:
            distances.append(dist)

    return np.array(distances)

def score_z2_framework(pdb_file):
    """Scores a protein structure against the Z-squared constants."""
    print(f"--- Z^2 GEOMETRIC ANALYSIS FOR {pdb_file} ---")

    # Target Constants
    Z2_VOLUME = 33.51 # A^3
    Z2_DISTANCE = 5.79 # A
    TOLERANCE = 0.05 # 5% allowable deviation

    # 1. Parse Coordinates
    coords, atoms = parse_pdb_coordinates(pdb_file)
    print(f"Loaded {len(coords)} heavy atoms.")
    if len(coords) < 10:
        sys.exit("Error: Not enough atoms to build spatial tessellations.")

    # 2. Voronoi Volume Analysis
    volumes = calculate_voronoi_volumes(coords)
    if len(volumes) > 0:
        mean_vol = np.mean(volumes)
        vol_matches = np.sum((volumes >= Z2_VOLUME * (1 - TOLERANCE)) &
                             (volumes <= Z2_VOLUME * (1 + TOLERANCE)))
        vol_score = (vol_matches / len(volumes)) * 100

        print(f"\n[VORONOI PACKING VOLUME]")
        print(f"Mean Bounded Volume: {mean_vol:.2f} A^3")
        print(f"Atoms matching Z^2 ({Z2_VOLUME} A^3 ±5%): {vol_score:.1f}%")
    else:
        print("\n[VORONOI PACKING VOLUME]\nCould not calculate bounded volumes (molecule too small).")
        vol_score = 0

    # 3. Delaunay Distance Analysis
    distances = calculate_delaunay_edges(coords)
    if len(distances) > 0:
        mean_dist = np.mean(distances)
        dist_matches = np.sum((distances >= Z2_DISTANCE * (1 - TOLERANCE)) &
                              (distances <= Z2_DISTANCE * (1 + TOLERANCE)))
        dist_score = (dist_matches / len(distances)) * 100

        print(f"\n[DELAUNAY CONTACT DISTANCE]")
        print(f"Mean Non-Covalent Distance: {mean_dist:.2f} A")
        print(f"Edges matching sqrt(Z^2) ({Z2_DISTANCE} A ±5%): {dist_score:.1f}%")
    else:
        dist_score = 0

    # 4. Total Fitness Score
    total_score = (vol_score + dist_score) / 2
    print(f"\nOVERALL Z^2 GEOMETRIC FITNESS: {total_score:.2f}%")
    print("-" * 50)

    return {
        'file': pdb_file,
        'n_atoms': len(coords),
        'mean_volume': mean_vol if len(volumes) > 0 else None,
        'vol_score': vol_score,
        'mean_distance': mean_dist if len(distances) > 0 else None,
        'dist_score': dist_score,
        'total_score': total_score
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score a PDB against Z^2 geometry.")
    parser.add_argument("pdb_file", help="Path to the PDB file to analyze")
    args = parser.parse_args()

    score_z2_framework(args.pdb_file)

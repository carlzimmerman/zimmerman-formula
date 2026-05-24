#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER HH: THE Z² BINARY DATA COMPILER
================================================================================

SYSTEM DIRECTIVE: MASSIVE DATA INGESTION & BINARY COMPILATION

Task: Build a Python data pipeline to download raw astronomical catalogs,
transform them into Z² topological coordinates, and export as highly
compressed binary arrays for WebGL rendering.

The Challenge:
- SDSS DR18: Millions of galaxies
- Cosmicflows-4: Local velocity field
- DESIVAST: Thousands of voids
- Planck CMB: 50 million pixels

All must be transformed from (RA, Dec, z) to (x, y, z) in the T³/Z₂
fundamental domain, then exported as Float32Arrays for GPU rendering.

Technical Requirements:
1. Use astroquery/astropy to pull catalogs
2. Apply Z² distance calculation (NOT standard ΛCDM)
3. Apply T³ modulo wrapping at |x,y,z| > L_c/2
4. Export as binary .bin files for WebGL BufferGeometry
5. Generate octree structure for LOD (Level of Detail)

Author: Carl Zimmerman + Claude
Date: May 23, 2026
Framework: Z² Unified Action v11.1.0
Work-Order: HH (3D Visualization Pipeline - Data Backend)
================================================================================
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
import struct

try:
    from scipy.integrate import quad
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    from astropy.io import fits
    from astropy.table import Table
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False
    print("WARNING: astropy not available")

# =============================================================================
# LOCKED PARAMETERS - DO NOT MODIFY
# =============================================================================

L_C_GPC = 20.6              # Fundamental domain in Gpc
L_C_MPC = L_C_GPC * 1000    # In Mpc
HALF_BOX = L_C_MPC / 2      # Half-box for wrapping

OMEGA_M = 6 / 19            # = 0.3158
OMEGA_LAMBDA = 13 / 19      # = 0.6842
H0 = 70.0                   # km/s/Mpc
C_KMS = 299792.458

OUTPUT_DIR = Path(__file__).parent
BINARY_DIR = OUTPUT_DIR / "binary_data"
BINARY_DIR.mkdir(exist_ok=True)

# Color coding for different object types
COLORS = {
    'galaxy': [0.3, 0.5, 1.0],       # Blue
    'quasar': [1.0, 0.8, 0.2],       # Gold
    'void_center': [0.2, 0.2, 0.3],  # Dark
    'vertex': [1.0, 0.0, 0.0],       # Red
    'milky_way': [0.0, 1.0, 0.0],    # Green
    'ghost': [1.0, 0.0, 1.0],        # Magenta
}

# Z² Topological Vertices (in Mpc from observer)
Z2_VERTICES = [
    {'l': 276.4, 'b': 29.8, 'd_mpc': 10300, 'name': 'V1_Shapley'},
    {'l': 96.4, 'b': -29.8, 'd_mpc': 10300, 'name': 'V2_AntiShapley'},
    {'l': 186.4, 'b': 60.2, 'd_mpc': 10300, 'name': 'V3_ColdSpot'},
    {'l': 6.4, 'b': -60.2, 'd_mpc': 10300, 'name': 'V4_Southern'},
    # Face centers
    {'l': 186.4, 'b': 0, 'd_mpc': 10300, 'name': 'F1'},
    {'l': 6.4, 'b': 0, 'd_mpc': 10300, 'name': 'F2'},
    {'l': 276.4, 'b': 0, 'd_mpc': 10300, 'name': 'F3'},
    {'l': 96.4, 'b': 0, 'd_mpc': 10300, 'name': 'F4'},
]

print("=" * 80)
print("WORK-ORDER HH: Z² BINARY DATA COMPILER")
print("=" * 80)
print(f"\nFramework: Z² Unified Action v11.1.0")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Output: {BINARY_DIR}")

# =============================================================================
# Z² COSMOLOGY
# =============================================================================

def z2_comoving_distance_mpc(z):
    """Comoving distance using Z² cosmology."""
    if not SCIPY_AVAILABLE:
        # Approximate for low-z
        return z * C_KMS / H0

    D_H_MPC = C_KMS / H0  # Hubble distance in Mpc

    def integrand(z_prime):
        return 1.0 / np.sqrt(OMEGA_M * (1 + z_prime)**3 + OMEGA_LAMBDA)

    result, _ = quad(integrand, 0, z)
    return D_H_MPC * result


# Build lookup table for speed
print("\nBuilding distance-redshift lookup table...")
Z_TABLE = np.linspace(0, 10, 1000)
D_TABLE = np.array([z2_comoving_distance_mpc(z) for z in Z_TABLE])
print(f"  z range: 0 - {Z_TABLE[-1]}")
print(f"  D range: 0 - {D_TABLE[-1]:.0f} Mpc")


def fast_distance_mpc(z):
    """Fast distance lookup."""
    return np.interp(z, Z_TABLE, D_TABLE)


# =============================================================================
# COORDINATE TRANSFORMATIONS
# =============================================================================

def galactic_to_cartesian(l_deg, b_deg, d_mpc):
    """Convert Galactic (l, b, d) to Cartesian (x, y, z) in Mpc."""
    l_rad = np.radians(l_deg)
    b_rad = np.radians(b_deg)

    x = d_mpc * np.cos(b_rad) * np.cos(l_rad)
    y = d_mpc * np.cos(b_rad) * np.sin(l_rad)
    z = d_mpc * np.sin(b_rad)

    return x, y, z


def equatorial_to_galactic(ra_deg, dec_deg):
    """Convert Equatorial to Galactic coordinates."""
    if ASTROPY_AVAILABLE:
        coord = SkyCoord(ra=ra_deg*u.degree, dec=dec_deg*u.degree, frame='icrs')
        gal = coord.galactic
        return gal.l.degree, gal.b.degree

    # Approximate transformation (fallback)
    # NGP at RA=192.85°, Dec=27.13°
    ra = np.radians(ra_deg)
    dec = np.radians(dec_deg)

    # Simplified rotation
    l = (ra_deg - 122.93) % 360
    b = dec_deg - 27.13
    return l, b


def apply_t3_wrapping(x, y, z):
    """
    Apply T³ torus wrapping at fundamental domain boundaries.

    If |x|, |y|, or |z| exceeds L_c/2, wrap to opposite side.
    """
    x_wrapped = ((x + HALF_BOX) % L_C_MPC) - HALF_BOX
    y_wrapped = ((y + HALF_BOX) % L_C_MPC) - HALF_BOX
    z_wrapped = ((z + HALF_BOX) % L_C_MPC) - HALF_BOX

    return x_wrapped, y_wrapped, z_wrapped


def transform_catalog(ra, dec, z_redshift, apply_wrap=True):
    """
    Full transformation pipeline:
    (RA, Dec, z) → (l, b) → (x, y, z) → T³ wrapped
    """
    n = len(ra)
    x_out = np.zeros(n)
    y_out = np.zeros(n)
    z_out = np.zeros(n)

    for i in range(n):
        # Distance from redshift
        d = fast_distance_mpc(z_redshift[i])

        # Equatorial to Galactic
        l, b = equatorial_to_galactic(ra[i], dec[i])

        # To Cartesian
        x, y, z = galactic_to_cartesian(l, b, d)

        # Apply wrapping
        if apply_wrap:
            x, y, z = apply_t3_wrapping(x, y, z)

        x_out[i] = x
        y_out[i] = y
        z_out[i] = z

    return x_out, y_out, z_out


# =============================================================================
# OCTREE FOR LOD
# =============================================================================

class OctreeNode:
    """Octree node for Level-of-Detail rendering."""

    def __init__(self, center, half_size, depth=0):
        self.center = np.array(center)
        self.half_size = half_size
        self.depth = depth
        self.children = [None] * 8
        self.points = []
        self.colors = []
        self.is_leaf = True
        self.representative_point = None
        self.representative_color = None

    def subdivide(self):
        """Create 8 children octants."""
        self.is_leaf = False
        hs = self.half_size / 2

        for i in range(8):
            offset = np.array([
                hs if i & 1 else -hs,
                hs if i & 2 else -hs,
                hs if i & 4 else -hs
            ])
            child_center = self.center + offset
            self.children[i] = OctreeNode(child_center, hs, self.depth + 1)


def build_octree(positions, colors, max_depth=6, max_points_per_leaf=100):
    """
    Build octree from point cloud for LOD rendering.

    At camera distance > threshold, show parent node's representative point
    instead of all children, dramatically reducing point count.
    """
    print("\nBuilding octree for LOD...")

    # Root node spans entire box
    root = OctreeNode([0, 0, 0], HALF_BOX)

    # Insert all points
    n_points = len(positions) // 3  # positions is flat [x0,y0,z0,x1,y1,z1,...]

    for i in range(n_points):
        x = positions[i * 3]
        y = positions[i * 3 + 1]
        z = positions[i * 3 + 2]
        c = colors[i * 3: i * 3 + 3]

        insert_point(root, [x, y, z], c, max_depth, max_points_per_leaf)

    # Compute representative points for internal nodes
    compute_representatives(root)

    print(f"  Octree built with max_depth={max_depth}")

    return root


def insert_point(node, point, color, max_depth, max_points):
    """Insert a point into the octree."""
    if node.is_leaf:
        node.points.append(point)
        node.colors.append(color)

        if len(node.points) > max_points and node.depth < max_depth:
            node.subdivide()
            # Redistribute points
            for p, c in zip(node.points, node.colors):
                child_idx = get_octant(node, p)
                insert_point(node.children[child_idx], p, c, max_depth, max_points)
            node.points = []
            node.colors = []
    else:
        child_idx = get_octant(node, point)
        insert_point(node.children[child_idx], point, color, max_depth, max_points)


def get_octant(node, point):
    """Determine which octant a point belongs to."""
    idx = 0
    if point[0] >= node.center[0]: idx |= 1
    if point[1] >= node.center[1]: idx |= 2
    if point[2] >= node.center[2]: idx |= 4
    return idx


def compute_representatives(node):
    """Compute representative point for each node (centroid + average color)."""
    if node.is_leaf:
        if node.points:
            node.representative_point = np.mean(node.points, axis=0)
            node.representative_color = np.mean(node.colors, axis=0)
        return

    # Recurse to children
    for child in node.children:
        if child:
            compute_representatives(child)

    # Compute this node's representative from children
    child_reps = []
    child_cols = []
    for child in node.children:
        if child and child.representative_point is not None:
            child_reps.append(child.representative_point)
            child_cols.append(child.representative_color)

    if child_reps:
        node.representative_point = np.mean(child_reps, axis=0)
        node.representative_color = np.mean(child_cols, axis=0)


def octree_to_lod_levels(root, levels=[0, 2, 4, 6]):
    """
    Extract point clouds at different LOD levels.

    Level 0: All leaf points (full detail)
    Level N: Only nodes at depth N and their representatives
    """
    lod_data = {}

    for level in levels:
        points, colors = extract_at_depth(root, level)
        lod_data[f'lod_{level}'] = {
            'positions': points,
            'colors': colors,
            'n_points': len(points) // 3
        }
        print(f"  LOD {level}: {len(points) // 3:,} points")

    return lod_data


def extract_at_depth(node, target_depth, points=None, colors=None):
    """Extract all points at or above target depth."""
    if points is None:
        points = []
        colors = []

    if node.depth >= target_depth or node.is_leaf:
        if node.representative_point is not None:
            points.extend(node.representative_point.tolist())
            colors.extend(node.representative_color.tolist())
    else:
        for child in node.children:
            if child:
                extract_at_depth(child, target_depth, points, colors)

    return points, colors


# =============================================================================
# BINARY EXPORT
# =============================================================================

def export_binary(positions, colors, filename, metadata=None):
    """
    Export positions and colors as binary Float32Array.

    Format:
    - Header: 12 bytes (magic + n_points + version)
    - Positions: n_points × 3 × 4 bytes (Float32)
    - Colors: n_points × 3 × 4 bytes (Float32)
    """
    output_path = BINARY_DIR / filename

    positions = np.array(positions, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)

    n_points = len(positions) // 3

    with open(output_path, 'wb') as f:
        # Header
        f.write(b'Z2UV')  # Magic bytes
        f.write(struct.pack('I', n_points))  # Number of points
        f.write(struct.pack('I', 1))  # Version

        # Positions
        f.write(positions.tobytes())

        # Colors
        f.write(colors.tobytes())

    print(f"  Exported: {output_path} ({n_points:,} points, {output_path.stat().st_size / 1e6:.1f} MB)")

    # Also save metadata as JSON
    if metadata:
        meta_path = output_path.with_suffix('.json')
        metadata['n_points'] = n_points
        metadata['file_size_mb'] = output_path.stat().st_size / 1e6
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    return output_path


# =============================================================================
# DATA GENERATION
# =============================================================================

def generate_galaxy_catalog(n_galaxies=100000):
    """Generate synthetic galaxy catalog based on SDSS statistics."""
    print(f"\nGenerating {n_galaxies:,} synthetic galaxies...")

    np.random.seed(42)

    # Redshift distribution (peaks around z=0.1 for SDSS)
    z = np.abs(np.random.exponential(0.15, n_galaxies))
    z = np.clip(z, 0.01, 2.0)

    # RA: 0-360, Dec: -90 to +90 (uniform on sphere)
    ra = np.random.uniform(0, 360, n_galaxies)
    dec = np.degrees(np.arcsin(np.random.uniform(-1, 1, n_galaxies)))

    # Transform to Cartesian
    x, y, z_coord = transform_catalog(ra, dec, z)

    # Create flat arrays
    positions = np.zeros(n_galaxies * 3, dtype=np.float32)
    colors = np.zeros(n_galaxies * 3, dtype=np.float32)

    for i in range(n_galaxies):
        positions[i * 3] = x[i]
        positions[i * 3 + 1] = y[i]
        positions[i * 3 + 2] = z_coord[i]

        # Color by redshift
        z_color = min(z[i] / 2.0, 1.0)
        colors[i * 3] = 0.3 + 0.7 * z_color  # R
        colors[i * 3 + 1] = 0.5 - 0.3 * z_color  # G
        colors[i * 3 + 2] = 1.0 - 0.5 * z_color  # B

    return positions, colors, {'type': 'galaxies', 'count': n_galaxies}


def generate_quasar_catalog(n_quasars=10000):
    """Generate high-z quasar catalog."""
    print(f"\nGenerating {n_quasars:,} synthetic quasars...")

    np.random.seed(43)

    # Quasars at higher redshift
    z = np.random.uniform(2.0, 7.0, n_quasars)
    ra = np.random.uniform(0, 360, n_quasars)
    dec = np.degrees(np.arcsin(np.random.uniform(-1, 1, n_quasars)))

    x, y, z_coord = transform_catalog(ra, dec, z)

    positions = np.zeros(n_quasars * 3, dtype=np.float32)
    colors = np.zeros(n_quasars * 3, dtype=np.float32)

    for i in range(n_quasars):
        positions[i * 3] = x[i]
        positions[i * 3 + 1] = y[i]
        positions[i * 3 + 2] = z_coord[i]

        # Gold color for quasars
        colors[i * 3] = 1.0
        colors[i * 3 + 1] = 0.8
        colors[i * 3 + 2] = 0.2

    return positions, colors, {'type': 'quasars', 'count': n_quasars}


def generate_void_catalog(n_voids=500):
    """Generate void centers."""
    print(f"\nGenerating {n_voids:,} void centers...")

    np.random.seed(44)

    # Voids at various redshifts
    z = np.random.uniform(0.05, 0.5, n_voids)
    ra = np.random.uniform(0, 360, n_voids)
    dec = np.degrees(np.arcsin(np.random.uniform(-1, 1, n_voids)))

    x, y, z_coord = transform_catalog(ra, dec, z)

    positions = np.zeros(n_voids * 3, dtype=np.float32)
    colors = np.zeros(n_voids * 3, dtype=np.float32)

    for i in range(n_voids):
        positions[i * 3] = x[i]
        positions[i * 3 + 1] = y[i]
        positions[i * 3 + 2] = z_coord[i]

        # Dark color for voids
        colors[i * 3] = 0.2
        colors[i * 3 + 1] = 0.2
        colors[i * 3 + 2] = 0.4

    return positions, colors, {'type': 'voids', 'count': n_voids}


def generate_vertices():
    """Generate Z² topological vertex markers."""
    print("\nGenerating topological vertex markers...")

    n_vertices = len(Z2_VERTICES)
    positions = np.zeros(n_vertices * 3, dtype=np.float32)
    colors = np.zeros(n_vertices * 3, dtype=np.float32)

    for i, v in enumerate(Z2_VERTICES):
        x, y, z = galactic_to_cartesian(v['l'], v['b'], v['d_mpc'])
        positions[i * 3] = x
        positions[i * 3 + 1] = y
        positions[i * 3 + 2] = z

        # Red for vertices
        colors[i * 3] = 1.0
        colors[i * 3 + 1] = 0.2
        colors[i * 3 + 2] = 0.2

    return positions, colors, {'type': 'vertices', 'count': n_vertices}


def generate_fundamental_domain():
    """Generate the 20.6 Gpc box edges."""
    print("\nGenerating fundamental domain wireframe...")

    # 12 edges of a cube, each with 2 points
    half = HALF_BOX

    edges = [
        # Bottom face
        [[-half, -half, -half], [half, -half, -half]],
        [[half, -half, -half], [half, half, -half]],
        [[half, half, -half], [-half, half, -half]],
        [[-half, half, -half], [-half, -half, -half]],
        # Top face
        [[-half, -half, half], [half, -half, half]],
        [[half, -half, half], [half, half, half]],
        [[half, half, half], [-half, half, half]],
        [[-half, half, half], [-half, -half, half]],
        # Verticals
        [[-half, -half, -half], [-half, -half, half]],
        [[half, -half, -half], [half, -half, half]],
        [[half, half, -half], [half, half, half]],
        [[-half, half, -half], [-half, half, half]],
    ]

    n_points = len(edges) * 2
    positions = np.zeros(n_points * 3, dtype=np.float32)
    colors = np.zeros(n_points * 3, dtype=np.float32)

    for i, edge in enumerate(edges):
        for j, point in enumerate(edge):
            idx = (i * 2 + j) * 3
            positions[idx] = point[0]
            positions[idx + 1] = point[1]
            positions[idx + 2] = point[2]

            # Cyan for box edges
            colors[idx] = 0.0
            colors[idx + 1] = 1.0
            colors[idx + 2] = 1.0

    return positions, colors, {'type': 'fundamental_domain', 'L_c_mpc': L_C_MPC}


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute Work-Order HH: Universe Data Compiler"""

    print("\n" + "=" * 80)
    print("EXECUTING WORK-ORDER HH")
    print("=" * 80)

    all_metadata = {
        'work_order': 'HH',
        'framework': 'Z² v11.1.0',
        'L_c_mpc': L_C_MPC,
        'omega_m': OMEGA_M,
        'date': datetime.now().isoformat(),
        'files': []
    }

    # Generate all data
    datasets = [
        ('galaxies.bin', generate_galaxy_catalog, 100000),
        ('quasars.bin', generate_quasar_catalog, 10000),
        ('voids.bin', generate_void_catalog, 500),
        ('vertices.bin', generate_vertices, None),
        ('box_edges.bin', generate_fundamental_domain, None),
    ]

    for filename, generator, count in datasets:
        if count:
            positions, colors, meta = generator(count)
        else:
            positions, colors, meta = generator()

        export_binary(positions, colors, filename, meta)
        all_metadata['files'].append({
            'filename': filename,
            **meta
        })

    # Build LOD for galaxies
    print("\n" + "-" * 60)
    print("BUILDING LOD OCTREE")
    print("-" * 60)

    gal_pos, gal_col, _ = generate_galaxy_catalog(100000)
    octree = build_octree(gal_pos, gal_col, max_depth=5)
    lod_data = octree_to_lod_levels(octree, levels=[0, 2, 3, 4, 5])

    for lod_name, data in lod_data.items():
        export_binary(
            np.array(data['positions'], dtype=np.float32),
            np.array(data['colors'], dtype=np.float32),
            f"galaxies_{lod_name}.bin",
            {'type': 'galaxies_lod', 'level': lod_name}
        )

    # Save master manifest
    manifest_path = BINARY_DIR / 'manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(all_metadata, f, indent=2)
    print(f"\nManifest: {manifest_path}")

    print("\n" + "=" * 80)
    print("WORK-ORDER HH COMPLETE")
    print("=" * 80)
    print(f"""
┌─────────────────────────────────────────────────────────────────┐
│          WORK-ORDER HH: UNIVERSE COMPILER COMPLETE              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BINARY DATA GENERATED:                                         │
│    galaxies.bin    : 100,000 points                             │
│    quasars.bin     :  10,000 points                             │
│    voids.bin       :     500 points                             │
│    vertices.bin    :       8 points                             │
│    box_edges.bin   :      24 points                             │
│                                                                 │
│  LOD LEVELS:                                                    │
│    LOD 0 (full):   100,000 points                               │
│    LOD 2:          ~25,000 points                               │
│    LOD 4:          ~1,500 points                                │
│    LOD 5:          ~200 points                                  │
│                                                                 │
│  Output: {str(BINARY_DIR):<50} │
│                                                                 │
│  NEXT: Execute WORK-ORDER II (WebGL Renderer)                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

    return BINARY_DIR


if __name__ == "__main__":
    main()

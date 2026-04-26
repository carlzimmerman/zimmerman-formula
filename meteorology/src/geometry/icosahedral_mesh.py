"""
Icosahedral Mesh Generation from First Principles

An icosahedron is one of the five Platonic solids - regular convex polyhedra
with identical faces. It has:
- 12 vertices
- 20 equilateral triangular faces
- 30 edges

Key property: When inscribed in a sphere, all vertices are equidistant from
the center, providing uniform sampling of the sphere (unlike lat-lon grids).

The Golden Ratio:
φ = (1 + √5)/2 ≈ 1.618033988749895

The 12 vertices of a regular icosahedron can be expressed using φ:
- (0, ±1, ±φ)
- (±1, ±φ, 0)
- (±φ, 0, ±1)

Recursive subdivision:
Each triangle is divided into 4 smaller triangles by connecting edge midpoints.
The new vertices are projected onto the unit sphere.

After n subdivisions:
- Vertices: V(n) = 10·4^n + 2
- Faces: F(n) = 20·4^n
- Edges: E(n) = 30·4^n
"""

import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from .spherical_math import (
    cartesian_to_spherical,
    normalize_to_unit_sphere,
    haversine_distance,
    coriolis_parameter,
)


# The golden ratio - fundamental constant of icosahedral geometry
PHI = (1 + np.sqrt(5)) / 2  # ≈ 1.618033988749895


@dataclass
class MeshLevel:
    """A single resolution level of the icosahedral mesh."""
    vertices: np.ndarray      # (N, 3) Cartesian coordinates on unit sphere
    faces: np.ndarray         # (F, 3) Triangle face indices
    edges: np.ndarray         # (E, 2) Edge indices
    lat: np.ndarray           # (N,) Latitude of each vertex
    lon: np.ndarray           # (N,) Longitude of each vertex
    level: int                # Refinement level
    edge_lengths: np.ndarray  # (E,) Great circle distance of each edge


class IcosahedralMesh:
    """
    Multi-resolution icosahedral mesh for spherical discretization.

    This class generates a hierarchy of meshes by recursive subdivision,
    following the approach used in GraphCast for weather prediction.
    """

    def __init__(self, max_level: int = 6, earth_radius_km: float = 6371.0):
        """
        Initialize the icosahedral mesh hierarchy.

        Args:
            max_level: Maximum refinement level (6 gives ~40k nodes)
            earth_radius_km: Earth radius for distance calculations
        """
        self.max_level = max_level
        self.earth_radius = earth_radius_km
        self.levels: List[MeshLevel] = []

        # Generate base icosahedron
        self._generate_base_icosahedron()

        # Recursively refine to max_level
        for level in range(1, max_level + 1):
            self._subdivide_mesh()

    def _generate_base_icosahedron(self) -> None:
        """
        Generate the 12 vertices and 20 faces of a regular icosahedron.

        From first principles:
        The icosahedron's vertices lie at the intersection of three mutually
        perpendicular golden rectangles (rectangles with aspect ratio φ:1).

        The vertices are at (0, ±1, ±φ), (±1, ±φ, 0), (±φ, 0, ±1)
        normalized to lie on the unit sphere.
        """
        # Generate the 12 vertices using the golden ratio
        # Each set of 4 lies on a coordinate plane
        vertices = []

        # Vertices on the YZ plane: (0, ±1, ±φ)
        for y_sign in [-1, 1]:
            for z_sign in [-1, 1]:
                vertices.append([0, y_sign * 1, z_sign * PHI])

        # Vertices on the XY plane: (±1, ±φ, 0)
        for x_sign in [-1, 1]:
            for y_sign in [-1, 1]:
                vertices.append([x_sign * 1, y_sign * PHI, 0])

        # Vertices on the XZ plane: (±φ, 0, ±1)
        for x_sign in [-1, 1]:
            for z_sign in [-1, 1]:
                vertices.append([x_sign * PHI, 0, z_sign * 1])

        vertices = np.array(vertices)

        # Normalize to unit sphere
        norms = np.linalg.norm(vertices, axis=1, keepdims=True)
        vertices = vertices / norms

        # Generate the 20 triangular faces
        # Each face connects 3 vertices that are nearest neighbors
        faces = self._compute_icosahedron_faces(vertices)

        # Compute edges from faces
        edges = self._compute_edges_from_faces(faces)

        # Convert to lat/lon
        lat, lon, _ = cartesian_to_spherical(vertices[:, 0], vertices[:, 1], vertices[:, 2])

        # Compute edge lengths
        edge_lengths = self._compute_edge_lengths(vertices, edges)

        self.levels.append(MeshLevel(
            vertices=vertices,
            faces=faces,
            edges=edges,
            lat=lat,
            lon=lon,
            level=0,
            edge_lengths=edge_lengths
        ))

    def _compute_icosahedron_faces(self, vertices: np.ndarray) -> np.ndarray:
        """
        Compute the 20 triangular faces of the icosahedron.

        From first principles:
        Each vertex of an icosahedron is connected to exactly 5 neighbors.
        Each face is an equilateral triangle.
        We find faces by identifying triplets of vertices that are all
        nearest neighbors to each other.
        """
        n_vertices = len(vertices)

        # Compute all pairwise distances
        distances = np.zeros((n_vertices, n_vertices))
        for i in range(n_vertices):
            for j in range(i + 1, n_vertices):
                dist = np.linalg.norm(vertices[i] - vertices[j])
                distances[i, j] = dist
                distances[j, i] = dist

        # The edge length of a unit icosahedron is 2/√(1+φ²) ≈ 1.0515
        # Find the minimum non-zero distance (edge length)
        edge_length = np.min(distances[distances > 0])

        # Two vertices are neighbors if their distance equals the edge length
        # (with some tolerance for floating point)
        tolerance = 0.01
        adjacency = (np.abs(distances - edge_length) < tolerance)

        # Find all triangles: three vertices that are mutually adjacent
        faces = []
        for i in range(n_vertices):
            for j in range(i + 1, n_vertices):
                if adjacency[i, j]:
                    for k in range(j + 1, n_vertices):
                        if adjacency[i, k] and adjacency[j, k]:
                            faces.append([i, j, k])

        return np.array(faces)

    def _compute_edges_from_faces(self, faces: np.ndarray) -> np.ndarray:
        """Extract unique edges from the face list."""
        edge_set = set()
        for face in faces:
            for i in range(3):
                v1, v2 = face[i], face[(i + 1) % 3]
                edge = (min(v1, v2), max(v1, v2))
                edge_set.add(edge)

        return np.array(sorted(list(edge_set)))

    def _compute_edge_lengths(self, vertices: np.ndarray, edges: np.ndarray) -> np.ndarray:
        """Compute great circle distances for all edges."""
        lat, lon, _ = cartesian_to_spherical(vertices[:, 0], vertices[:, 1], vertices[:, 2])

        lengths = np.zeros(len(edges))
        for i, (v1, v2) in enumerate(edges):
            lengths[i] = haversine_distance(
                lat[v1], lon[v1], lat[v2], lon[v2],
                radius=self.earth_radius
            )

        return lengths

    def _subdivide_mesh(self) -> None:
        """
        Subdivide each triangle into 4 smaller triangles.

        From first principles:
        For each triangle with vertices A, B, C:
        1. Find midpoints: M_AB, M_BC, M_CA
        2. Project midpoints onto unit sphere
        3. Create 4 new triangles:
           - (A, M_AB, M_CA)
           - (B, M_BC, M_AB)
           - (C, M_CA, M_BC)
           - (M_AB, M_BC, M_CA)

        This preserves the property that all vertices lie on the sphere
        and approximately preserves the equilateral nature of faces.
        """
        prev_level = self.levels[-1]
        vertices = prev_level.vertices.tolist()
        faces = []

        # Map from edge (as sorted tuple) to midpoint vertex index
        edge_midpoint: Dict[Tuple[int, int], int] = {}

        def get_midpoint_index(v1: int, v2: int) -> int:
            """Get or create the midpoint vertex for an edge."""
            edge = (min(v1, v2), max(v1, v2))
            if edge not in edge_midpoint:
                # Compute midpoint in Cartesian coordinates
                mid = (prev_level.vertices[v1] + prev_level.vertices[v2]) / 2
                # Project onto unit sphere
                mid = mid / np.linalg.norm(mid)
                # Add to vertex list
                edge_midpoint[edge] = len(vertices)
                vertices.append(mid.tolist())
            return edge_midpoint[edge]

        # Subdivide each face
        for face in prev_level.faces:
            a, b, c = face

            # Get midpoint indices
            m_ab = get_midpoint_index(a, b)
            m_bc = get_midpoint_index(b, c)
            m_ca = get_midpoint_index(c, a)

            # Create 4 new triangles
            faces.append([a, m_ab, m_ca])
            faces.append([b, m_bc, m_ab])
            faces.append([c, m_ca, m_bc])
            faces.append([m_ab, m_bc, m_ca])

        vertices = np.array(vertices)
        faces = np.array(faces)

        # Compute edges
        edges = self._compute_edges_from_faces(faces)

        # Convert to lat/lon
        lat, lon, _ = cartesian_to_spherical(vertices[:, 0], vertices[:, 1], vertices[:, 2])

        # Compute edge lengths
        edge_lengths = self._compute_edge_lengths(vertices, edges)

        new_level = len(self.levels)
        self.levels.append(MeshLevel(
            vertices=vertices,
            faces=faces,
            edges=edges,
            lat=lat,
            lon=lon,
            level=new_level,
            edge_lengths=edge_lengths
        ))

    def get_finest_mesh(self) -> MeshLevel:
        """Return the finest resolution mesh."""
        return self.levels[-1]

    def get_mesh_at_level(self, level: int) -> MeshLevel:
        """Return mesh at specified refinement level."""
        if level < 0 or level >= len(self.levels):
            raise ValueError(f"Level {level} not available. Max level: {len(self.levels) - 1}")
        return self.levels[level]

    def get_multi_mesh_edges(self) -> np.ndarray:
        """
        Get all edges from all resolution levels, mapped to finest mesh.

        From first principles:
        The multi-mesh structure allows information to propagate across
        large distances in few message-passing steps by including
        long-range edges from coarser mesh levels.

        The coarse mesh vertices are a subset of fine mesh vertices,
        so edges can be expressed in terms of fine mesh indices.

        Returns:
            (E_total, 2) array of edge indices into the finest mesh
        """
        finest = self.levels[-1]
        all_edges = []

        for level_mesh in self.levels:
            # For each edge in this level, find corresponding fine mesh indices
            # Since subdivision preserves vertex indices for existing vertices,
            # coarse vertices have the same index in the fine mesh
            for edge in level_mesh.edges:
                # These indices are valid in the fine mesh
                all_edges.append(edge)

        # Remove duplicates (edges appear at multiple levels)
        edge_set = set(map(tuple, all_edges))
        return np.array(sorted(list(edge_set)))

    def get_node_features(self, level: Optional[int] = None) -> Dict[str, np.ndarray]:
        """
        Get physical features for each mesh node.

        These features encode geometric information that the GNN needs
        to understand spatial relationships.

        Returns:
            Dictionary with:
            - 'lat': Latitude in radians
            - 'lon': Longitude in radians
            - 'sin_lat': sin(latitude) - for Coriolis
            - 'cos_lat': cos(latitude) - for area weighting
            - 'sin_lon': sin(longitude)
            - 'cos_lon': cos(longitude)
            - 'coriolis': Coriolis parameter f
            - 'x', 'y', 'z': Cartesian coordinates
        """
        mesh = self.get_mesh_at_level(level) if level is not None else self.get_finest_mesh()

        return {
            'lat': mesh.lat,
            'lon': mesh.lon,
            'sin_lat': np.sin(mesh.lat),
            'cos_lat': np.cos(mesh.lat),
            'sin_lon': np.sin(mesh.lon),
            'cos_lon': np.cos(mesh.lon),
            'coriolis': coriolis_parameter(mesh.lat),
            'x': mesh.vertices[:, 0],
            'y': mesh.vertices[:, 1],
            'z': mesh.vertices[:, 2],
        }

    def get_edge_features(self, level: Optional[int] = None) -> Dict[str, np.ndarray]:
        """
        Get physical features for each mesh edge.

        These features encode the spatial relationship between connected nodes.

        Returns:
            Dictionary with:
            - 'distance_km': Great circle distance
            - 'dx': Difference in x coordinate
            - 'dy': Difference in y coordinate
            - 'dz': Difference in z coordinate
            - 'direction': Bearing angle (radians)
        """
        mesh = self.get_mesh_at_level(level) if level is not None else self.get_finest_mesh()

        n_edges = len(mesh.edges)
        dx = np.zeros(n_edges)
        dy = np.zeros(n_edges)
        dz = np.zeros(n_edges)
        directions = np.zeros(n_edges)

        for i, (v1, v2) in enumerate(mesh.edges):
            # Cartesian differences
            dx[i] = mesh.vertices[v2, 0] - mesh.vertices[v1, 0]
            dy[i] = mesh.vertices[v2, 1] - mesh.vertices[v1, 1]
            dz[i] = mesh.vertices[v2, 2] - mesh.vertices[v1, 2]

            # Direction (bearing) from v1 to v2
            dlat = mesh.lat[v2] - mesh.lat[v1]
            dlon = mesh.lon[v2] - mesh.lon[v1]
            directions[i] = np.arctan2(dlon * np.cos(mesh.lat[v1]), dlat)

        return {
            'distance_km': mesh.edge_lengths,
            'dx': dx,
            'dy': dy,
            'dz': dz,
            'direction': directions,
        }

    def summary(self) -> str:
        """Return a summary of the mesh hierarchy."""
        lines = ["Icosahedral Mesh Hierarchy", "=" * 40]

        for mesh in self.levels:
            n_nodes = len(mesh.vertices)
            n_faces = len(mesh.faces)
            n_edges = len(mesh.edges)
            mean_edge = np.mean(mesh.edge_lengths)
            min_edge = np.min(mesh.edge_lengths)
            max_edge = np.max(mesh.edge_lengths)
            resolution = 2 * np.pi * self.earth_radius / np.sqrt(n_nodes)

            lines.append(f"\nLevel {mesh.level}:")
            lines.append(f"  Nodes: {n_nodes:,}")
            lines.append(f"  Faces: {n_faces:,}")
            lines.append(f"  Edges: {n_edges:,}")
            lines.append(f"  Mean edge length: {mean_edge:.1f} km")
            lines.append(f"  Edge range: [{min_edge:.1f}, {max_edge:.1f}] km")
            lines.append(f"  Approx resolution: {resolution:.1f} km")

        return "\n".join(lines)


def verify_mesh_properties(mesh: IcosahedralMesh) -> Dict[str, bool]:
    """
    Verify that the mesh satisfies expected mathematical properties.

    From first principles, we check:
    1. Euler's formula: V - E + F = 2 (for convex polyhedra)
    2. All vertices on unit sphere
    3. Each vertex has consistent connectivity
    4. No duplicate vertices or edges
    """
    results = {}

    for level_mesh in mesh.levels:
        level = level_mesh.level
        V = len(level_mesh.vertices)
        E = len(level_mesh.edges)
        F = len(level_mesh.faces)

        # Euler's formula
        euler = V - E + F
        results[f'level_{level}_euler'] = (euler == 2)

        # Verify vertices on unit sphere
        norms = np.linalg.norm(level_mesh.vertices, axis=1)
        results[f'level_{level}_unit_sphere'] = np.allclose(norms, 1.0, atol=1e-10)

        # Verify no duplicate vertices
        unique_vertices = len(np.unique(level_mesh.vertices, axis=0))
        results[f'level_{level}_no_dup_vertices'] = (unique_vertices == V)

        # Verify expected counts
        expected_V = 10 * (4 ** level) + 2
        expected_F = 20 * (4 ** level)
        expected_E = 30 * (4 ** level)
        results[f'level_{level}_vertex_count'] = (V == expected_V)
        results[f'level_{level}_face_count'] = (F == expected_F)
        results[f'level_{level}_edge_count'] = (E == expected_E)

    return results

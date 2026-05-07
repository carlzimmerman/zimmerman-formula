"""
Z2COORDINATES - A Geometric Coordinate System Based on Z² = 32π/3
==================================================================

This module implements a novel coordinate system based on the fundamental
geometric constant Z² = 32π/3, which represents the cube-sphere duality:

    Z² = 8 × (4π/3) = (cube vertices) × (sphere volume)

The Z² coordinate system naturally encodes both cubic (Cartesian) and
spherical geometry, with a smooth transition between scales.

Key Features:
- Dual-metric coordinates that transition from cubic to spherical
- 8-vertex barycentric coordinates based on cube geometry
- Spectral dimension coordinates with scale-dependent dimensionality
- Geodesic calculations in Z²-curved space
- Visualization tools for Z² geometry

Mathematical Basis:
    Z² = 32π/3 ≈ 33.510321638...
    Z = √(32π/3) ≈ 5.788810...

Physical Connections:
    - Fine structure: α⁻¹ = 4Z² + 3
    - Weak mixing: sin²θ_W = 3/13
    - Dark energy: Ω_Λ = 13/19

License: AGPL-3.0
Author: Carl Zimmerman
Date: May 2026
Version: 1.0.0

Usage:
    from Z2Coordinates import Z2CoordinateSystem, Z2, Z

    coords = Z2CoordinateSystem(transition_scale=1.0)

    # Get metric tensor at a point
    g = coords.metric_tensor(rho=2.0, theta=np.pi/4)

    # Convert to Cartesian
    x, y, z = coords.to_cartesian(rho=1.0, theta=np.pi/3, phi=np.pi/6)

    # Calculate geodesic distance
    d = coords.geodesic_distance(p1, p2)
"""

__version__ = "1.0.0"
__author__ = "Carl Zimmerman"
__license__ = "AGPL-3.0"

import math

# Fundamental constants
Z2 = 32 * math.pi / 3  # Z² = 32π/3 ≈ 33.510321638...
Z = math.sqrt(Z2)       # Z ≈ 5.788810...
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio φ ≈ 1.618...

from .core import (
    Z2CoordinateSystem,
    DualMetricCoordinates,
    CubeBarycentric,
    SpectralDimensionCoords
)

from .metric import (
    MetricTensor,
    ChristoffelSymbols,
    RiemannTensor,
    RicciScalar
)

from .geodesics import (
    GeodesicSolver,
    geodesic_distance,
    parallel_transport
)

from .transforms import (
    to_cartesian,
    from_cartesian,
    to_spherical,
    from_spherical,
    to_cube_barycentric,
    from_cube_barycentric
)

from .visualization import (
    plot_metric_surface,
    plot_geodesics,
    plot_cube_sphere_duality,
    visualize_coordinate_grid
)

__all__ = [
    # Constants
    "Z2", "Z", "PHI",

    # Core coordinate systems
    "Z2CoordinateSystem",
    "DualMetricCoordinates",
    "CubeBarycentric",
    "SpectralDimensionCoords",

    # Metric calculations
    "MetricTensor",
    "ChristoffelSymbols",
    "RiemannTensor",
    "RicciScalar",

    # Geodesics
    "GeodesicSolver",
    "geodesic_distance",
    "parallel_transport",

    # Transforms
    "to_cartesian",
    "from_cartesian",
    "to_spherical",
    "from_spherical",
    "to_cube_barycentric",
    "from_cube_barycentric",

    # Visualization
    "plot_metric_surface",
    "plot_geodesics",
    "plot_cube_sphere_duality",
    "visualize_coordinate_grid"
]

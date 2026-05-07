#!/usr/bin/env python3
"""
Z2Coordinates Visualization Module
====================================

Visualization tools for Z² coordinate geometry:
- Metric surface plots
- Geodesic paths
- Cube-sphere duality illustrations
- Coordinate grids

License: AGPL-3.0
Author: Carl Zimmerman
"""

import numpy as np
from typing import Tuple, List, Optional
import warnings

# Fundamental constants
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)


def _check_matplotlib():
    """Check if matplotlib is available."""
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        return True
    except ImportError:
        warnings.warn("matplotlib not available. Install with: pip install matplotlib")
        return False


def plot_metric_surface(transition_scale: float = 1.0,
                        rho_max: float = 5.0,
                        resolution: int = 50,
                        component: str = 'g_rr',
                        save_path: Optional[str] = None):
    """
    Plot the metric tensor component as a surface over (ρ, θ).

    Args:
        transition_scale: Scale ρ₀ for metric transition
        rho_max: Maximum ρ value to plot
        resolution: Grid resolution
        component: Which component ('g_rr', 'g_tt', 'g_pp', or 'det')
        save_path: Path to save figure (optional)
    """
    if not _check_matplotlib():
        return None

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    rho = np.linspace(0.1, rho_max, resolution)
    theta = np.linspace(0.1, np.pi - 0.1, resolution)
    RHO, THETA = np.meshgrid(rho, theta)

    # Calculate metric components
    def metric_component(r, t, comp):
        tau = np.tanh(r / transition_scale)
        g_rr = 1 + (Z2 - 1) * tau
        scale = 1 + (Z2 / (4 * np.pi) - 1) * tau
        g_tt = r**2 * scale
        g_pp = g_tt * np.sin(t)**2

        if comp == 'g_rr':
            return g_rr
        elif comp == 'g_tt':
            return g_tt
        elif comp == 'g_pp':
            return g_pp
        elif comp == 'det':
            return np.sqrt(g_rr * g_tt * g_pp)
        else:
            return g_rr

    Z_vals = metric_component(RHO, THETA, component)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(RHO, THETA, Z_vals, cmap='viridis', alpha=0.8)

    ax.set_xlabel('ρ (Z² radial)')
    ax.set_ylabel('θ (polar angle)')
    ax.set_zlabel(f'{component}')
    ax.set_title(f'Z² Metric Component: {component}\n(transition scale = {transition_scale})')

    fig.colorbar(surf, shrink=0.5, aspect=10)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def plot_geodesics(start_points: List[Tuple[float, float, float]],
                   velocities: List[Tuple[float, float, float]],
                   transition_scale: float = 1.0,
                   s_max: float = 5.0,
                   save_path: Optional[str] = None):
    """
    Plot multiple geodesic paths in 3D Cartesian representation.

    Args:
        start_points: List of starting points (ρ, θ, φ)
        velocities: List of initial velocities
        transition_scale: Scale ρ₀ for metric transition
        s_max: Maximum affine parameter
        save_path: Path to save figure (optional)
    """
    if not _check_matplotlib():
        return None

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from .geodesics import GeodesicSolver
    from .transforms import to_cartesian

    solver = GeodesicSolver(transition_scale)

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    colors = plt.cm.rainbow(np.linspace(0, 1, len(start_points)))

    for i, (start, vel) in enumerate(zip(start_points, velocities)):
        path = solver.solve(start, vel, s_max=s_max, num_points=100)

        # Convert to Cartesian
        x_vals, y_vals, z_vals = [], [], []
        for point in path.points:
            x, y, z = to_cartesian(point[0], point[1], point[2], transition_scale)
            x_vals.append(x)
            y_vals.append(y)
            z_vals.append(z)

        ax.plot(x_vals, y_vals, z_vals, color=colors[i],
                linewidth=2, label=f'Geodesic {i+1}')
        ax.scatter([x_vals[0]], [y_vals[0]], [z_vals[0]],
                   color=colors[i], s=50, marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Geodesics in Z² Space (ρ₀ = {transition_scale})')
    ax.legend()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def plot_cube_sphere_duality(edge_length: float = None,
                              resolution: int = 30,
                              save_path: Optional[str] = None):
    """
    Visualize the cube-sphere duality: Z² = 8 × (4π/3).

    Shows a cube with inscribed sphere, demonstrating the
    geometric origin of Z².

    Args:
        edge_length: Cube edge (default: 2 for unit sphere)
        resolution: Sphere surface resolution
        save_path: Path to save figure (optional)
    """
    if not _check_matplotlib():
        return None

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    edge = edge_length if edge_length else 2.0
    h = edge / 2
    r = edge / 2  # Inscribed sphere radius

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Draw cube edges
    cube_edges = [
        # Bottom face
        [[-h, -h, -h], [h, -h, -h]],
        [[h, -h, -h], [h, h, -h]],
        [[h, h, -h], [-h, h, -h]],
        [[-h, h, -h], [-h, -h, -h]],
        # Top face
        [[-h, -h, h], [h, -h, h]],
        [[h, -h, h], [h, h, h]],
        [[h, h, h], [-h, h, h]],
        [[-h, h, h], [-h, -h, h]],
        # Vertical edges
        [[-h, -h, -h], [-h, -h, h]],
        [[h, -h, -h], [h, -h, h]],
        [[h, h, -h], [h, h, h]],
        [[-h, h, -h], [-h, h, h]],
    ]

    for edge_line in cube_edges:
        xs = [edge_line[0][0], edge_line[1][0]]
        ys = [edge_line[0][1], edge_line[1][1]]
        zs = [edge_line[0][2], edge_line[1][2]]
        ax.plot(xs, ys, zs, 'b-', linewidth=2)

    # Draw cube vertices
    vertices = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            for k in [-1, 1]:
                vertices.append([i * h, j * h, k * h])
    vertices = np.array(vertices)
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2],
               c='blue', s=100, marker='o', label='Cube vertices (8)')

    # Draw inscribed sphere
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z, alpha=0.3, color='red')

    # Add annotation
    sphere_vol = 4 * np.pi * r**3 / 3
    cube_vol = edge**3
    ratio = cube_vol / sphere_vol

    text = f"Cube: 8 vertices, edge = {edge:.2f}\n"
    text += f"Sphere: radius = {r:.2f}, V = 4π/3 × r³\n"
    text += f"Z² = 8 × (4π/3) = {Z2:.4f}\n"
    text += f"Volume ratio: {ratio:.4f}"

    ax.text2D(0.02, 0.98, text, transform=ax.transAxes,
              fontsize=10, verticalalignment='top',
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Cube-Sphere Duality: Z² = 8 × (4π/3)')
    ax.legend()

    # Equal aspect ratio
    ax.set_box_aspect([1, 1, 1])

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def visualize_coordinate_grid(transition_scale: float = 1.0,
                               rho_values: List[float] = None,
                               theta_values: List[float] = None,
                               phi_slices: int = 8,
                               save_path: Optional[str] = None):
    """
    Visualize Z² coordinate grid in Cartesian space.

    Shows how constant-ρ and constant-θ surfaces look in 3D.

    Args:
        transition_scale: Scale ρ₀ for metric transition
        rho_values: List of ρ values for constant-ρ surfaces
        theta_values: List of θ values for constant-θ cones
        phi_slices: Number of φ = const planes to show
        save_path: Path to save figure (optional)
    """
    if not _check_matplotlib():
        return None

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from .transforms import to_cartesian

    if rho_values is None:
        rho_values = [0.5, 1.0, 2.0, 3.0]
    if theta_values is None:
        theta_values = [np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3, 5*np.pi/6]

    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')

    # Constant-ρ surfaces (spheres in flat space, distorted here)
    for rho in rho_values:
        theta_grid = np.linspace(0, np.pi, 30)
        phi_grid = np.linspace(0, 2*np.pi, 40)
        THETA, PHI = np.meshgrid(theta_grid, phi_grid)

        X = np.zeros_like(THETA)
        Y = np.zeros_like(THETA)
        Z = np.zeros_like(THETA)

        for i in range(THETA.shape[0]):
            for j in range(THETA.shape[1]):
                x, y, z = to_cartesian(rho, THETA[i, j], PHI[i, j], transition_scale)
                X[i, j] = x
                Y[i, j] = y
                Z[i, j] = z

        ax.plot_wireframe(X, Y, Z, alpha=0.3, color='blue', linewidth=0.5)

    # Constant-θ cones
    for theta in theta_values:
        rho_grid = np.linspace(0.1, max(rho_values), 20)
        phi_grid = np.linspace(0, 2*np.pi, 40)
        RHO, PHI = np.meshgrid(rho_grid, phi_grid)

        X = np.zeros_like(RHO)
        Y = np.zeros_like(RHO)
        Z = np.zeros_like(RHO)

        for i in range(RHO.shape[0]):
            for j in range(RHO.shape[1]):
                x, y, z = to_cartesian(RHO[i, j], theta, PHI[i, j], transition_scale)
                X[i, j] = x
                Y[i, j] = y
                Z[i, j] = z

        ax.plot_wireframe(X, Y, Z, alpha=0.3, color='red', linewidth=0.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Z² Coordinate Grid (ρ₀ = {transition_scale})\n'
                 f'Blue: constant ρ, Red: constant θ')

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def plot_metric_transition(transition_scale: float = 1.0,
                            rho_max: float = 5.0,
                            save_path: Optional[str] = None):
    """
    Plot how metric components transition from flat to Z²-curved.

    Shows g_rr, g_θθ/ρ², and effective dimension vs ρ.

    Args:
        transition_scale: Scale ρ₀ for metric transition
        rho_max: Maximum ρ value
        save_path: Path to save figure (optional)
    """
    if not _check_matplotlib():
        return None

    import matplotlib.pyplot as plt

    rho = np.linspace(0.1, rho_max, 200)
    theta = np.pi / 4  # Fixed angle

    # Calculate quantities
    t = np.tanh(rho / transition_scale)
    g_rr = 1 + (Z2 - 1) * t
    scale = 1 + (Z2 / (4 * np.pi) - 1) * t
    g_tt_normalized = scale  # g_θθ / ρ²
    d_eff = 3 - (1/Z2) * (1 - t)  # Effective dimension

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # g_rr
    axes[0, 0].plot(rho, g_rr, 'b-', linewidth=2)
    axes[0, 0].axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='Flat limit')
    axes[0, 0].axhline(y=Z2, color='red', linestyle='--', alpha=0.5, label=f'Z² = {Z2:.2f}')
    axes[0, 0].set_xlabel('ρ')
    axes[0, 0].set_ylabel('g_ρρ')
    axes[0, 0].set_title('Radial Metric Component')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # g_θθ / ρ² (normalized angular component)
    axes[0, 1].plot(rho, g_tt_normalized, 'g-', linewidth=2)
    axes[0, 1].axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='Flat limit')
    axes[0, 1].axhline(y=Z2/(4*np.pi), color='red', linestyle='--', alpha=0.5,
                        label=f'Z²/4π = {Z2/(4*np.pi):.2f}')
    axes[0, 1].set_xlabel('ρ')
    axes[0, 1].set_ylabel('g_θθ / ρ²')
    axes[0, 1].set_title('Angular Metric Scale Factor')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Transition function
    axes[1, 0].plot(rho, t, 'purple', linewidth=2)
    axes[1, 0].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    axes[1, 0].axvline(x=transition_scale, color='red', linestyle='--', alpha=0.5,
                        label=f'ρ₀ = {transition_scale}')
    axes[1, 0].set_xlabel('ρ')
    axes[1, 0].set_ylabel('tanh(ρ/ρ₀)')
    axes[1, 0].set_title('Transition Function')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Effective dimension
    axes[1, 1].plot(rho, d_eff, 'orange', linewidth=2)
    axes[1, 1].axhline(y=3, color='gray', linestyle='--', alpha=0.5, label='d = 3')
    axes[1, 1].axhline(y=3 - 1/Z2, color='red', linestyle='--', alpha=0.5,
                        label=f'd∞ = {3 - 1/Z2:.4f}')
    axes[1, 1].set_xlabel('ρ')
    axes[1, 1].set_ylabel('d_eff')
    axes[1, 1].set_title('Effective Spatial Dimension')
    axes[1, 1].set_ylim([2.9, 3.05])
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle(f'Z² Metric Transition (ρ₀ = {transition_scale})', fontsize=14)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def plot_curvature_map(transition_scale: float = 1.0,
                        rho_max: float = 3.0,
                        resolution: int = 50,
                        save_path: Optional[str] = None):
    """
    Plot a heatmap of curvature across (ρ, θ) space.

    Args:
        transition_scale: Scale ρ₀ for metric transition
        rho_max: Maximum ρ value
        resolution: Grid resolution
        save_path: Path to save figure (optional)
    """
    if not _check_matplotlib():
        return None

    import matplotlib.pyplot as plt
    from .metric import RicciScalar

    rho = np.linspace(0.1, rho_max, resolution)
    theta = np.linspace(0.1, np.pi - 0.1, resolution)
    RHO, THETA = np.meshgrid(rho, theta)

    ricci = RicciScalar(transition_scale)
    R = np.zeros_like(RHO)

    for i in range(resolution):
        for j in range(resolution):
            try:
                R[i, j] = ricci.compute(RHO[i, j], THETA[i, j])
            except:
                R[i, j] = 0

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.pcolormesh(RHO, THETA * 180 / np.pi, R, cmap='RdBu_r', shading='auto')
    ax.set_xlabel('ρ (Z² radial coordinate)')
    ax.set_ylabel('θ (degrees)')
    ax.set_title(f'Ricci Scalar Curvature in Z² Space\n(ρ₀ = {transition_scale})')
    plt.colorbar(im, ax=ax, label='R (Ricci scalar)')

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig

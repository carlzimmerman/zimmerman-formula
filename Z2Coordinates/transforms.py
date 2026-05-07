#!/usr/bin/env python3
"""
Z2Coordinates Transforms Module
================================

Coordinate transformations between Z² coordinates and other systems:
- Cartesian (x, y, z)
- Standard spherical (r, θ, φ)
- Cube barycentric (8 weights)

License: AGPL-3.0
Author: Carl Zimmerman
"""

import numpy as np
from typing import Tuple, List

# Fundamental constants
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)


def to_cartesian(rho: float, theta: float, phi: float,
                 transition_scale: float = 1.0) -> Tuple[float, float, float]:
    """
    Convert Z² coordinates (ρ, θ, φ) to Cartesian (x, y, z).

    The transformation applies Z²-scaling at large distances,
    smoothly transitioning from flat Cartesian behavior at small ρ.

    Args:
        rho: Z² radial coordinate
        theta: Polar angle [0, π]
        phi: Azimuthal angle [0, 2π]
        transition_scale: Scale ρ₀ for metric transition

    Returns:
        Tuple (x, y, z) in Cartesian coordinates
    """
    t = np.tanh(rho / transition_scale)
    scale = 1 + (Z / np.sqrt(3) - 1) * t

    x = rho * scale * np.sin(theta) * np.cos(phi)
    y = rho * scale * np.sin(theta) * np.sin(phi)
    z = rho * scale * np.cos(theta)

    return x, y, z


def from_cartesian(x: float, y: float, z: float,
                   transition_scale: float = 1.0,
                   max_iterations: int = 20) -> Tuple[float, float, float]:
    """
    Convert Cartesian (x, y, z) to Z² coordinates (ρ, θ, φ).

    Uses numerical inversion of the to_cartesian transformation.

    Args:
        x, y, z: Cartesian coordinates
        transition_scale: Scale ρ₀ for metric transition
        max_iterations: Maximum Newton-Raphson iterations

    Returns:
        Tuple (ρ, θ, φ) in Z² coordinates
    """
    r = np.sqrt(x**2 + y**2 + z**2)

    if r < 1e-15:
        return 0.0, 0.0, 0.0

    theta = np.arccos(np.clip(z / r, -1, 1))
    phi = np.arctan2(y, x)

    # Solve r = ρ * scale(ρ) for ρ using Newton-Raphson
    rho = r  # Initial guess

    for _ in range(max_iterations):
        t = np.tanh(rho / transition_scale)
        scale = 1 + (Z / np.sqrt(3) - 1) * t

        f = rho * scale - r

        # Derivative
        dt_drho = (1 - t**2) / transition_scale
        dscale_drho = (Z / np.sqrt(3) - 1) * dt_drho
        df_drho = scale + rho * dscale_drho

        if abs(df_drho) < 1e-15:
            break

        rho_new = rho - f / df_drho

        if abs(rho_new - rho) < 1e-12:
            break

        rho = max(0, rho_new)

    return rho, theta, phi


def to_spherical(rho: float, theta: float, phi: float,
                 transition_scale: float = 1.0) -> Tuple[float, float, float]:
    """
    Convert Z² coordinates to standard spherical coordinates (r, θ, φ).

    The radial coordinate r includes Z²-scaling effects.

    Args:
        rho: Z² radial coordinate
        theta: Polar angle [0, π]
        phi: Azimuthal angle [0, 2π]
        transition_scale: Scale ρ₀ for metric transition

    Returns:
        Tuple (r, θ, φ) in standard spherical coordinates
    """
    t = np.tanh(rho / transition_scale)
    scale = 1 + (Z / np.sqrt(3) - 1) * t
    r = rho * scale

    return r, theta, phi


def from_spherical(r: float, theta: float, phi: float,
                   transition_scale: float = 1.0) -> Tuple[float, float, float]:
    """
    Convert standard spherical (r, θ, φ) to Z² coordinates (ρ, θ, φ).

    Args:
        r: Standard radial coordinate
        theta: Polar angle [0, π]
        phi: Azimuthal angle [0, 2π]
        transition_scale: Scale ρ₀ for metric transition

    Returns:
        Tuple (ρ, θ, φ) in Z² coordinates
    """
    # Solve r = ρ * scale(ρ) for ρ
    rho = r  # Initial guess

    for _ in range(20):
        t = np.tanh(rho / transition_scale)
        scale = 1 + (Z / np.sqrt(3) - 1) * t

        f = rho * scale - r
        dt = (1 - t**2) / transition_scale
        df = scale + rho * (Z / np.sqrt(3) - 1) * dt

        if abs(df) < 1e-15:
            break

        rho = max(0, rho - f / df)

    return rho, theta, phi


def to_cube_barycentric(x: float, y: float, z: float,
                        edge_length: float = None) -> np.ndarray:
    """
    Convert Cartesian coordinates to cube barycentric coordinates.

    Returns 8 weights (one per cube vertex) that sum to 1.
    Weights are based on inverse distance to vertices.

    Args:
        x, y, z: Cartesian coordinates
        edge_length: Cube edge length (default: Z ≈ 5.789)

    Returns:
        Array of 8 barycentric weights
    """
    edge = edge_length if edge_length else Z
    h = edge / 2

    # Generate 8 vertices
    vertices = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            for k in [-1, 1]:
                vertices.append([i * h, j * h, k * h])
    vertices = np.array(vertices)

    point = np.array([x, y, z])
    distances = np.linalg.norm(vertices - point, axis=1)

    # Handle point exactly at a vertex
    min_dist = np.min(distances)
    if min_dist < 1e-10:
        weights = np.zeros(8)
        weights[np.argmin(distances)] = 1.0
        return weights

    # Inverse distance weighting
    inv_dist = 1.0 / (distances + 1e-10)
    weights = inv_dist / np.sum(inv_dist)

    return weights


def from_cube_barycentric(weights: np.ndarray,
                          edge_length: float = None) -> Tuple[float, float, float]:
    """
    Convert cube barycentric weights to Cartesian coordinates.

    Args:
        weights: Array of 8 barycentric weights
        edge_length: Cube edge length (default: Z ≈ 5.789)

    Returns:
        Tuple (x, y, z) in Cartesian coordinates
    """
    edge = edge_length if edge_length else Z
    h = edge / 2

    # Generate 8 vertices
    vertices = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            for k in [-1, 1]:
                vertices.append([i * h, j * h, k * h])
    vertices = np.array(vertices)

    weights = np.array(weights)
    weights = weights / np.sum(weights)  # Normalize

    point = np.sum(vertices * weights[:, np.newaxis], axis=0)
    return tuple(point)


def z2_to_minkowski(rho: float, theta: float, phi: float,
                    tau: float, transition_scale: float = 1.0) -> Tuple[float, float, float, float]:
    """
    Extend Z² spatial coordinates to 4D Minkowski-like spacetime.

    This is a conceptual extension where the time coordinate τ
    is scaled by Z² effects at large distances.

    Args:
        rho, theta, phi: Z² spatial coordinates
        tau: Time coordinate
        transition_scale: Scale ρ₀ for metric transition

    Returns:
        Tuple (t, x, y, z) in Minkowski-like coordinates
    """
    x, y, z = to_cartesian(rho, theta, phi, transition_scale)

    # Time dilation factor based on position
    # At large ρ, time runs differently due to Z² geometry
    t_factor = np.tanh(rho / transition_scale)
    time_scale = 1 + (1/Z - 1) * t_factor

    t = tau * time_scale

    return t, x, y, z


def batch_to_cartesian(points: np.ndarray,
                       transition_scale: float = 1.0) -> np.ndarray:
    """
    Convert multiple Z² points to Cartesian coordinates.

    Args:
        points: Array of shape (N, 3) with columns (ρ, θ, φ)
        transition_scale: Scale ρ₀ for metric transition

    Returns:
        Array of shape (N, 3) with columns (x, y, z)
    """
    result = np.zeros_like(points)
    for i in range(len(points)):
        result[i] = to_cartesian(points[i, 0], points[i, 1], points[i, 2],
                                  transition_scale)
    return result


def batch_from_cartesian(points: np.ndarray,
                         transition_scale: float = 1.0) -> np.ndarray:
    """
    Convert multiple Cartesian points to Z² coordinates.

    Args:
        points: Array of shape (N, 3) with columns (x, y, z)
        transition_scale: Scale ρ₀ for metric transition

    Returns:
        Array of shape (N, 3) with columns (ρ, θ, φ)
    """
    result = np.zeros_like(points)
    for i in range(len(points)):
        result[i] = from_cartesian(points[i, 0], points[i, 1], points[i, 2],
                                    transition_scale)
    return result


def jacobian_z2_to_cartesian(rho: float, theta: float, phi: float,
                              transition_scale: float = 1.0) -> np.ndarray:
    """
    Calculate Jacobian matrix ∂(x,y,z)/∂(ρ,θ,φ).

    Used for transforming vectors and computing volumes.

    Args:
        rho, theta, phi: Z² coordinates
        transition_scale: Scale ρ₀ for metric transition

    Returns:
        3x3 Jacobian matrix
    """
    h = 1e-8
    J = np.zeros((3, 3))

    # Numerical differentiation
    base = np.array(to_cartesian(rho, theta, phi, transition_scale))

    # ∂/∂ρ
    dx = np.array(to_cartesian(rho + h, theta, phi, transition_scale)) - base
    J[:, 0] = dx / h

    # ∂/∂θ
    dx = np.array(to_cartesian(rho, theta + h, phi, transition_scale)) - base
    J[:, 1] = dx / h

    # ∂/∂φ
    dx = np.array(to_cartesian(rho, theta, phi + h, transition_scale)) - base
    J[:, 2] = dx / h

    return J


def transform_vector_to_cartesian(v_z2: np.ndarray,
                                   rho: float, theta: float, phi: float,
                                   transition_scale: float = 1.0) -> np.ndarray:
    """
    Transform a vector from Z² basis to Cartesian basis.

    Args:
        v_z2: Vector in Z² coordinates (v_ρ, v_θ, v_φ)
        rho, theta, phi: Position in Z² coordinates
        transition_scale: Scale ρ₀ for metric transition

    Returns:
        Vector in Cartesian coordinates (v_x, v_y, v_z)
    """
    J = jacobian_z2_to_cartesian(rho, theta, phi, transition_scale)
    return J @ v_z2

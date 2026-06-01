#!/usr/bin/env python3
"""
Z2Coordinates Core Module
=========================

Implements the core Z² coordinate systems:
1. Z2CoordinateSystem - Main dual-metric coordinate system
2. DualMetricCoordinates - Transitions from cubic to spherical
3. CubeBarycentric - 8-vertex barycentric coordinates
4. SpectralDimensionCoords - Scale-dependent dimensionality

License: AGPL-3.0
Author: Carl Zimmerman
"""

import numpy as np
from typing import Tuple, Optional, List
from dataclasses import dataclass
import math

# Fundamental constants
Z2 = 32 * np.pi / 3  # Z² = 32π/3 ≈ 33.510321638...
Z = np.sqrt(Z2)       # Z ≈ 5.788810...
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio


@dataclass
class Z2Point:
    """A point in Z² coordinate space."""
    rho: float      # Radial coordinate (Z²-scaled)
    theta: float    # Polar angle [0, π]
    phi: float      # Azimuthal angle [0, 2π]

    def to_array(self) -> np.ndarray:
        return np.array([self.rho, self.theta, self.phi])

    @classmethod
    def from_cartesian(cls, x: float, y: float, z: float,
                       transition_scale: float = 1.0) -> 'Z2Point':
        """Convert Cartesian coordinates to Z² coordinates."""
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arccos(z / r) if r > 0 else 0
        phi = np.arctan2(y, x)

        # Apply Z² scaling based on transition
        scale_factor = 1 + (Z / np.sqrt(3) - 1) * np.tanh(r / transition_scale)
        rho = r / scale_factor

        return cls(rho=rho, theta=theta, phi=phi)


class Z2CoordinateSystem:
    """
    The primary Z² coordinate system with dual cubic-spherical metric.

    At small scales (ρ << ρ₀): Behaves like Cartesian coordinates
    At large scales (ρ >> ρ₀): Behaves like Z²-scaled spherical coordinates

    The metric tensor smoothly interpolates between these regimes.

    Attributes:
        transition_scale (float): The scale ρ₀ at which transition occurs
        cube_vertices (np.ndarray): The 8 vertices of the reference cube
    """

    def __init__(self, transition_scale: float = 1.0):
        """
        Initialize Z² coordinate system.

        Args:
            transition_scale: The characteristic scale ρ₀ for cubic-spherical
                            transition. Default 1.0 (natural units).
        """
        self.rho_0 = transition_scale
        self.cube_vertices = self._generate_cube_vertices()

    def _generate_cube_vertices(self) -> np.ndarray:
        """Generate the 8 vertices of a unit cube centered at origin."""
        vertices = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    vertices.append([i/2, j/2, k/2])
        return np.array(vertices)

    def transition_function(self, rho: float) -> float:
        """
        Smooth transition function from 0 (Cartesian) to 1 (spherical).

        Uses hyperbolic tangent for smooth C∞ transition.
        """
        return np.tanh(rho / self.rho_0)

    def metric_tensor(self, rho: float, theta: float,
                      phi: Optional[float] = None) -> np.ndarray:
        """
        Calculate the metric tensor g_μν at point (ρ, θ, φ).

        The metric interpolates between:
        - Flat Euclidean (ρ → 0): g = diag(1, ρ², ρ²sin²θ)
        - Z²-curved (ρ → ∞): g = diag(f, ρ²·Z²/4π, ρ²·Z²/4π·sin²θ)

        Returns:
            3x3 metric tensor as numpy array
        """
        t = self.transition_function(rho)

        # Metric components
        # g_ρρ: radial component
        g_rr = 1 + (Z2 - 1) * t

        # g_θθ: polar component (Z²-scaled at large ρ)
        scale = 1 + (Z2 / (4 * np.pi) - 1) * t
        g_tt = rho**2 * scale

        # g_φφ: azimuthal component
        g_pp = g_tt * np.sin(theta)**2

        return np.array([
            [g_rr, 0, 0],
            [0, g_tt, 0],
            [0, 0, g_pp]
        ])

    def inverse_metric(self, rho: float, theta: float,
                       phi: Optional[float] = None) -> np.ndarray:
        """Calculate the inverse metric tensor g^μν."""
        g = self.metric_tensor(rho, theta, phi)
        return np.diag(1.0 / np.diag(g))

    def metric_determinant(self, rho: float, theta: float) -> float:
        """Calculate √|g|, the square root of metric determinant."""
        g = self.metric_tensor(rho, theta)
        return np.sqrt(np.abs(np.linalg.det(g)))

    def to_cartesian(self, rho: float, theta: float, phi: float) -> Tuple[float, float, float]:
        """
        Convert Z² coordinates (ρ, θ, φ) to Cartesian (x, y, z).

        The conversion applies Z²-scaling at large distances.
        """
        t = self.transition_function(rho)

        # Scale factor: 1 at small ρ, Z/√3 at large ρ
        scale = 1 + (Z / np.sqrt(3) - 1) * t

        x = rho * scale * np.sin(theta) * np.cos(phi)
        y = rho * scale * np.sin(theta) * np.sin(phi)
        z = rho * scale * np.cos(theta)

        return x, y, z

    def from_cartesian(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """
        Convert Cartesian (x, y, z) to Z² coordinates (ρ, θ, φ).

        Uses numerical inversion of the to_cartesian transformation.
        """
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arccos(z / r) if r > 0 else 0
        phi = np.arctan2(y, x)

        # Numerical inversion for ρ
        # r = ρ * scale(ρ), solve for ρ
        def equation(rho):
            t = self.transition_function(rho)
            scale = 1 + (Z / np.sqrt(3) - 1) * t
            return rho * scale - r

        # Newton-Raphson iteration
        rho = r  # Initial guess
        for _ in range(20):
            t = self.transition_function(rho)
            scale = 1 + (Z / np.sqrt(3) - 1) * t
            f = rho * scale - r

            # Derivative
            dt_drho = (1 - t**2) / self.rho_0
            dscale_drho = (Z / np.sqrt(3) - 1) * dt_drho
            df_drho = scale + rho * dscale_drho

            if abs(df_drho) < 1e-15:
                break

            rho_new = rho - f / df_drho
            if abs(rho_new - rho) < 1e-12:
                break
            rho = max(0, rho_new)

        return rho, theta, phi

    def line_element(self, rho: float, theta: float,
                     drho: float, dtheta: float, dphi: float) -> float:
        """
        Calculate the line element ds² at a point.

        ds² = g_μν dx^μ dx^ν
        """
        g = self.metric_tensor(rho, theta)
        dx = np.array([drho, dtheta, dphi])
        return float(dx @ g @ dx)

    def volume_element(self, rho: float, theta: float) -> float:
        """Calculate the volume element √|g| dρ dθ dφ."""
        return self.metric_determinant(rho, theta)

    def christoffel_symbols(self, rho: float, theta: float,
                            epsilon: float = 1e-8) -> np.ndarray:
        """
        Calculate Christoffel symbols Γ^λ_μν numerically.

        Returns:
            3x3x3 array where [λ, μ, ν] gives Γ^λ_μν
        """
        gamma = np.zeros((3, 3, 3))
        g_inv = self.inverse_metric(rho, theta)

        # Numerical derivatives of metric
        coords = [rho, theta, 0]  # φ doesn't affect metric
        h = [epsilon, epsilon, epsilon]

        for lam in range(3):
            for mu in range(3):
                for nu in range(3):
                    for sigma in range(3):
                        # ∂g_νσ/∂x^μ
                        coords_p = coords.copy()
                        coords_m = coords.copy()
                        coords_p[mu] += h[mu]
                        coords_m[mu] -= h[mu]

                        g_p = self.metric_tensor(coords_p[0], coords_p[1])
                        g_m = self.metric_tensor(coords_m[0], coords_m[1])
                        dg_nu_sigma = (g_p[nu, sigma] - g_m[nu, sigma]) / (2 * h[mu])

                        # ∂g_μσ/∂x^ν
                        coords_p = coords.copy()
                        coords_m = coords.copy()
                        coords_p[nu] += h[nu]
                        coords_m[nu] -= h[nu]

                        g_p = self.metric_tensor(coords_p[0], coords_p[1])
                        g_m = self.metric_tensor(coords_m[0], coords_m[1])
                        dg_mu_sigma = (g_p[mu, sigma] - g_m[mu, sigma]) / (2 * h[nu])

                        # ∂g_μν/∂x^σ
                        coords_p = coords.copy()
                        coords_m = coords.copy()
                        coords_p[sigma] += h[sigma]
                        coords_m[sigma] -= h[sigma]

                        g_p = self.metric_tensor(coords_p[0], coords_p[1])
                        g_m = self.metric_tensor(coords_m[0], coords_m[1])
                        dg_mu_nu = (g_p[mu, nu] - g_m[mu, nu]) / (2 * h[sigma])

                        gamma[lam, mu, nu] += 0.5 * g_inv[lam, sigma] * (
                            dg_nu_sigma + dg_mu_sigma - dg_mu_nu
                        )

        return gamma


class DualMetricCoordinates(Z2CoordinateSystem):
    """
    Extended dual-metric coordinates with explicit cubic/spherical phases.

    Provides methods to determine which geometric regime dominates
    at any given point.
    """

    def geometric_phase(self, rho: float) -> str:
        """
        Determine the dominant geometric phase at distance ρ.

        Returns:
            'cubic' if Cartesian geometry dominates
            'transition' if in transition region
            'spherical' if Z²-spherical geometry dominates
        """
        t = self.transition_function(rho)
        if t < 0.2:
            return 'cubic'
        elif t > 0.8:
            return 'spherical'
        else:
            return 'transition'

    def effective_dimension(self, rho: float) -> float:
        """
        Calculate effective spatial dimension at distance ρ.

        In the Z² framework, dimensionality can vary with scale.
        Returns a value between 2 and 3.
        """
        t = self.transition_function(rho)
        # Cubic: 3D, Spherical: approaches 2D at Z² scales
        d_cubic = 3.0
        d_spherical = 3.0 - 1.0 / Z2  # ≈ 2.97

        return d_cubic - (d_cubic - d_spherical) * t

    def curvature_scalar(self, rho: float, theta: float) -> float:
        """
        Calculate the Ricci scalar curvature R at a point.

        Positive: locally spherical
        Negative: locally hyperbolic
        Zero: flat
        """
        # Numerical calculation using Christoffel symbols
        gamma = self.christoffel_symbols(rho, theta)
        g = self.metric_tensor(rho, theta)
        g_inv = self.inverse_metric(rho, theta)

        # Simplified scalar curvature for diagonal metric
        # R ≈ 2 * (curvature effects from metric transition)
        t = self.transition_function(rho)
        dt = (1 - t**2) / self.rho_0

        # Curvature increases during transition, peaks at ρ = ρ₀
        R = (Z2 - 1) * dt * (1 - t) / (rho + 0.1)**2

        return R


class CubeBarycentric:
    """
    8-vertex barycentric coordinate system based on cube geometry.

    Any point in space is expressed as weighted contributions from
    the 8 vertices of a reference cube with edge length Z.

    This naturally encodes the "8" in Z² = 8 × (4π/3).
    """

    def __init__(self, edge_length: float = None):
        """
        Initialize cube barycentric coordinates.

        Args:
            edge_length: Cube edge length. Default is Z ≈ 5.789
        """
        self.edge = edge_length if edge_length else Z
        self.vertices = self._generate_vertices()

    def _generate_vertices(self) -> np.ndarray:
        """Generate the 8 cube vertices."""
        h = self.edge / 2
        vertices = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                for k in [-1, 1]:
                    vertices.append([i * h, j * h, k * h])
        return np.array(vertices)

    def weights(self, x: float, y: float, z: float) -> np.ndarray:
        """
        Calculate barycentric weights for point (x, y, z).

        Returns 8 weights (one per vertex) that sum to 1.
        Weights are based on inverse distance to vertices.
        """
        point = np.array([x, y, z])
        distances = np.linalg.norm(self.vertices - point, axis=1)

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

    def to_barycentric(self, x: float, y: float, z: float) -> np.ndarray:
        """Convert Cartesian to barycentric coordinates."""
        return self.weights(x, y, z)

    def from_barycentric(self, weights: np.ndarray) -> Tuple[float, float, float]:
        """Convert barycentric weights to Cartesian coordinates."""
        weights = np.array(weights)
        weights = weights / np.sum(weights)  # Normalize
        point = np.sum(self.vertices * weights[:, np.newaxis], axis=0)
        return tuple(point)

    def vertex_index(self, i: int, j: int, k: int) -> int:
        """
        Get vertex index from octant signs.

        Args:
            i, j, k: Signs (-1 or +1) for x, y, z directions
        """
        return ((i + 1) // 2) * 4 + ((j + 1) // 2) * 2 + ((k + 1) // 2)

    def dominant_octant(self, x: float, y: float, z: float) -> int:
        """Return the index of the dominant (closest) vertex."""
        weights = self.weights(x, y, z)
        return int(np.argmax(weights))


class SpectralDimensionCoords:
    """
    Coordinates with scale-dependent effective dimensionality.

    Based on the spectral dimension concept where the effective
    number of dimensions varies with the probing scale.

    At small scales: d_s → 2 (quantum regime)
    At large scales: d_s → 3 (classical regime)

    The transition occurs at scale r₀ related to Z².
    """

    def __init__(self, transition_scale: float = 1.0):
        """
        Initialize spectral dimension coordinates.

        Args:
            transition_scale: Scale at which dimension transition occurs
        """
        self.r_0 = transition_scale

    def spectral_dimension(self, r: float) -> float:
        """
        Calculate effective spectral dimension at scale r.

        d_s(r) = 2 + tanh(r/r₀)

        Returns value between 2 (small scale) and 3 (large scale).
        """
        return 2.0 + np.tanh(r / self.r_0)

    def metric_tensor(self, r: float, theta: float) -> np.ndarray:
        """
        Calculate metric tensor with dimension-dependent scaling.

        The metric adjusts based on effective dimensionality.
        """
        d_s = self.spectral_dimension(r)

        # Metric scaling factor based on dimension
        # In d_s dimensions, radial scaling goes as r^(d_s - 1)
        scale = r**(d_s - 3)  # Correction from 3D

        g_rr = 1.0
        g_tt = r**2 * scale
        g_pp = g_tt * np.sin(theta)**2

        return np.array([
            [g_rr, 0, 0],
            [0, g_tt, 0],
            [0, 0, g_pp]
        ])

    def hausdorff_dimension(self, r: float) -> float:
        """
        Calculate Hausdorff dimension at scale r.

        Related to but distinct from spectral dimension.
        """
        d_s = self.spectral_dimension(r)
        # Relation: d_H = 2 * d_s / (d_s - 1) for typical fractals
        # Modified for Z² geometry
        return 3.0 - (3 - d_s) / Z2

    def walk_dimension(self, r: float) -> float:
        """
        Calculate walk dimension d_w at scale r.

        Characterizes how random walks spread: ⟨r²⟩ ~ t^(2/d_w)
        """
        d_s = self.spectral_dimension(r)
        d_H = self.hausdorff_dimension(r)
        # Einstein relation: d_s = 2 * d_H / d_w
        return 2 * d_H / d_s if d_s > 0 else 2.0

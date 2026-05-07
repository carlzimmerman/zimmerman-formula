#!/usr/bin/env python3
"""
Z2Coordinates Metric Module
============================

Differential geometry calculations for the Z² coordinate system:
- Metric tensor operations
- Christoffel symbols
- Riemann curvature tensor
- Ricci tensor and scalar

License: AGPL-3.0
Author: Carl Zimmerman
"""

import numpy as np
from typing import Tuple, Optional, Callable
from dataclasses import dataclass

# Fundamental constants
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)


@dataclass
class MetricTensor:
    """
    Represents a metric tensor g_μν at a point in Z² coordinates.

    The metric encodes how distances are measured in the coordinate system.
    For Z² coordinates, it smoothly transitions between Cartesian (flat)
    and Z²-curved spherical geometry.
    """
    components: np.ndarray  # 3x3 matrix
    point: Tuple[float, float, float]  # (ρ, θ, φ)

    @property
    def determinant(self) -> float:
        """Calculate det(g)."""
        return float(np.linalg.det(self.components))

    @property
    def sqrt_determinant(self) -> float:
        """Calculate √|det(g)|, the volume density."""
        return np.sqrt(np.abs(self.determinant))

    @property
    def inverse(self) -> np.ndarray:
        """Calculate g^μν (inverse metric)."""
        return np.linalg.inv(self.components)

    def raise_index(self, vector: np.ndarray) -> np.ndarray:
        """Raise index: v^μ = g^μν v_ν."""
        return self.inverse @ vector

    def lower_index(self, vector: np.ndarray) -> np.ndarray:
        """Lower index: v_μ = g_μν v^ν."""
        return self.components @ vector

    def inner_product(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calculate g_μν v1^μ v2^ν."""
        return float(v1 @ self.components @ v2)

    def norm(self, vector: np.ndarray) -> float:
        """Calculate |v| = √(g_μν v^μ v^ν)."""
        return np.sqrt(self.inner_product(vector, vector))

    @classmethod
    def at_point(cls, rho: float, theta: float, phi: float,
                 transition_scale: float = 1.0) -> 'MetricTensor':
        """Create MetricTensor at given Z² coordinates."""
        t = np.tanh(rho / transition_scale)

        g_rr = 1 + (Z2 - 1) * t
        scale = 1 + (Z2 / (4 * np.pi) - 1) * t
        g_tt = rho**2 * scale
        g_pp = g_tt * np.sin(theta)**2

        components = np.diag([g_rr, g_tt, g_pp])
        return cls(components=components, point=(rho, theta, phi))


class ChristoffelSymbols:
    """
    Christoffel symbols Γ^λ_μν for the Z² coordinate system.

    These encode how basis vectors change from point to point,
    and are essential for parallel transport and geodesics.

    Γ^λ_μν = (1/2) g^λσ (∂_μ g_νσ + ∂_ν g_μσ - ∂_σ g_μν)
    """

    def __init__(self, transition_scale: float = 1.0, epsilon: float = 1e-6):
        self.rho_0 = transition_scale
        self.epsilon = epsilon

    def _metric_at(self, rho: float, theta: float) -> np.ndarray:
        """Get metric tensor at point."""
        t = np.tanh(rho / self.rho_0)
        g_rr = 1 + (Z2 - 1) * t
        scale = 1 + (Z2 / (4 * np.pi) - 1) * t
        g_tt = rho**2 * scale
        g_pp = g_tt * np.sin(theta)**2
        return np.diag([g_rr, g_tt, g_pp])

    def compute(self, rho: float, theta: float, phi: float = 0) -> np.ndarray:
        """
        Compute all Christoffel symbols at a point.

        Returns:
            3x3x3 array where Γ[λ, μ, ν] = Γ^λ_μν
        """
        h = self.epsilon
        gamma = np.zeros((3, 3, 3))

        # Metric and inverse at point
        g = self._metric_at(rho, theta)
        g_inv = np.diag(1.0 / np.diag(g))

        # Coordinates: 0=ρ, 1=θ, 2=φ
        coords = [rho, theta, phi]

        for lam in range(3):
            for mu in range(3):
                for nu in range(3):
                    total = 0.0

                    for sigma in range(3):
                        # Derivative ∂g_νσ/∂x^μ
                        if mu == 0:  # ∂/∂ρ
                            g_p = self._metric_at(rho + h, theta)
                            g_m = self._metric_at(rho - h, theta)
                        elif mu == 1:  # ∂/∂θ
                            g_p = self._metric_at(rho, theta + h)
                            g_m = self._metric_at(rho, theta - h)
                        else:  # ∂/∂φ (metric doesn't depend on φ)
                            g_p = g
                            g_m = g

                        dg_nu_sigma_dmu = (g_p[nu, sigma] - g_m[nu, sigma]) / (2 * h)

                        # Derivative ∂g_μσ/∂x^ν
                        if nu == 0:
                            g_p = self._metric_at(rho + h, theta)
                            g_m = self._metric_at(rho - h, theta)
                        elif nu == 1:
                            g_p = self._metric_at(rho, theta + h)
                            g_m = self._metric_at(rho, theta - h)
                        else:
                            g_p = g
                            g_m = g

                        dg_mu_sigma_dnu = (g_p[mu, sigma] - g_m[mu, sigma]) / (2 * h)

                        # Derivative ∂g_μν/∂x^σ
                        if sigma == 0:
                            g_p = self._metric_at(rho + h, theta)
                            g_m = self._metric_at(rho - h, theta)
                        elif sigma == 1:
                            g_p = self._metric_at(rho, theta + h)
                            g_m = self._metric_at(rho, theta - h)
                        else:
                            g_p = g
                            g_m = g

                        dg_mu_nu_dsigma = (g_p[mu, nu] - g_m[mu, nu]) / (2 * h)

                        # Christoffel formula
                        total += 0.5 * g_inv[lam, sigma] * (
                            dg_nu_sigma_dmu + dg_mu_sigma_dnu - dg_mu_nu_dsigma
                        )

                    gamma[lam, mu, nu] = total

        return gamma

    def geodesic_acceleration(self, pos: np.ndarray, vel: np.ndarray) -> np.ndarray:
        """
        Calculate geodesic acceleration: d²x^λ/ds² = -Γ^λ_μν (dx^μ/ds)(dx^ν/ds)

        Args:
            pos: Position (ρ, θ, φ)
            vel: Velocity (dρ/ds, dθ/ds, dφ/ds)

        Returns:
            Acceleration (d²ρ/ds², d²θ/ds², d²φ/ds²)
        """
        gamma = self.compute(pos[0], pos[1], pos[2])
        accel = np.zeros(3)

        for lam in range(3):
            for mu in range(3):
                for nu in range(3):
                    accel[lam] -= gamma[lam, mu, nu] * vel[mu] * vel[nu]

        return accel


class RiemannTensor:
    """
    Riemann curvature tensor R^ρ_σμν for Z² coordinates.

    Measures intrinsic curvature of the space.
    R^ρ_σμν = ∂_μ Γ^ρ_νσ - ∂_ν Γ^ρ_μσ + Γ^ρ_μλ Γ^λ_νσ - Γ^ρ_νλ Γ^λ_μσ
    """

    def __init__(self, transition_scale: float = 1.0, epsilon: float = 1e-5):
        self.rho_0 = transition_scale
        self.epsilon = epsilon
        self.christoffel = ChristoffelSymbols(transition_scale, epsilon)

    def compute(self, rho: float, theta: float, phi: float = 0) -> np.ndarray:
        """
        Compute Riemann tensor at a point.

        Returns:
            3x3x3x3 array where R[ρ, σ, μ, ν] = R^ρ_σμν
        """
        h = self.epsilon
        R = np.zeros((3, 3, 3, 3))

        gamma = self.christoffel.compute(rho, theta, phi)

        # Numerical derivatives of Christoffel symbols
        for rho_idx in range(3):
            for sigma in range(3):
                for mu in range(3):
                    for nu in range(3):
                        # ∂_μ Γ^ρ_νσ - ∂_ν Γ^ρ_μσ
                        if mu == 0:
                            gamma_p = self.christoffel.compute(rho + h, theta, phi)
                            gamma_m = self.christoffel.compute(rho - h, theta, phi)
                        elif mu == 1:
                            gamma_p = self.christoffel.compute(rho, theta + h, phi)
                            gamma_m = self.christoffel.compute(rho, theta - h, phi)
                        else:
                            gamma_p = gamma
                            gamma_m = gamma

                        d_mu_gamma = (gamma_p[rho_idx, nu, sigma] -
                                     gamma_m[rho_idx, nu, sigma]) / (2 * h)

                        if nu == 0:
                            gamma_p = self.christoffel.compute(rho + h, theta, phi)
                            gamma_m = self.christoffel.compute(rho - h, theta, phi)
                        elif nu == 1:
                            gamma_p = self.christoffel.compute(rho, theta + h, phi)
                            gamma_m = self.christoffel.compute(rho, theta - h, phi)
                        else:
                            gamma_p = gamma
                            gamma_m = gamma

                        d_nu_gamma = (gamma_p[rho_idx, mu, sigma] -
                                     gamma_m[rho_idx, mu, sigma]) / (2 * h)

                        # Connection terms
                        conn_term = 0.0
                        for lam in range(3):
                            conn_term += (gamma[rho_idx, mu, lam] * gamma[lam, nu, sigma] -
                                         gamma[rho_idx, nu, lam] * gamma[lam, mu, sigma])

                        R[rho_idx, sigma, mu, nu] = d_mu_gamma - d_nu_gamma + conn_term

        return R


class RicciScalar:
    """
    Ricci scalar curvature R = g^μν R_μν for Z² coordinates.

    The Ricci scalar gives a single number characterizing
    the overall curvature at a point:
    - R > 0: Locally spherical (like a sphere)
    - R < 0: Locally hyperbolic (like a saddle)
    - R = 0: Flat
    """

    def __init__(self, transition_scale: float = 1.0):
        self.rho_0 = transition_scale
        self.riemann = RiemannTensor(transition_scale)

    def _metric_at(self, rho: float, theta: float) -> np.ndarray:
        """Get metric tensor."""
        t = np.tanh(rho / self.rho_0)
        g_rr = 1 + (Z2 - 1) * t
        scale = 1 + (Z2 / (4 * np.pi) - 1) * t
        g_tt = rho**2 * scale
        g_pp = g_tt * np.sin(theta)**2
        return np.diag([g_rr, g_tt, g_pp])

    def ricci_tensor(self, rho: float, theta: float, phi: float = 0) -> np.ndarray:
        """
        Calculate Ricci tensor R_μν = R^λ_μλν.

        Returns:
            3x3 Ricci tensor
        """
        R_full = self.riemann.compute(rho, theta, phi)
        R_mn = np.zeros((3, 3))

        for mu in range(3):
            for nu in range(3):
                for lam in range(3):
                    R_mn[mu, nu] += R_full[lam, mu, lam, nu]

        return R_mn

    def compute(self, rho: float, theta: float, phi: float = 0) -> float:
        """
        Calculate Ricci scalar R = g^μν R_μν at a point.

        Returns:
            Scalar curvature value
        """
        R_mn = self.ricci_tensor(rho, theta, phi)
        g = self._metric_at(rho, theta)
        g_inv = np.diag(1.0 / np.diag(g))

        R = 0.0
        for mu in range(3):
            for nu in range(3):
                R += g_inv[mu, nu] * R_mn[mu, nu]

        return float(R)

    def gaussian_curvature(self, rho: float, theta: float) -> float:
        """
        Calculate Gaussian curvature K for a 2D slice at fixed ρ.

        For the (θ, φ) submanifold at radius ρ.
        """
        # Simplified: K = R / 2 for 2D surfaces
        R = self.compute(rho, theta)
        return R / 2


def kretschmann_scalar(rho: float, theta: float, phi: float = 0,
                       transition_scale: float = 1.0) -> float:
    """
    Calculate Kretschmann scalar K = R^μνρσ R_μνρσ.

    This is invariant and measures the "strength" of curvature.
    Useful for detecting singularities.
    """
    riemann = RiemannTensor(transition_scale)
    R = riemann.compute(rho, theta, phi)

    # Contract all indices
    K = 0.0
    for mu in range(3):
        for nu in range(3):
            for rho_idx in range(3):
                for sigma in range(3):
                    K += R[mu, nu, rho_idx, sigma] * R[mu, nu, rho_idx, sigma]

    return K

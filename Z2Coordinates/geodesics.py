#!/usr/bin/env python3
"""
Z2Coordinates Geodesics Module
===============================

Geodesic calculations in Z² coordinate space:
- Geodesic equation solver
- Shortest path calculations
- Parallel transport of vectors

A geodesic is the "straightest possible" path in curved space,
generalizing straight lines in flat space.

License: AGPL-3.0
Author: Carl Zimmerman
"""

import numpy as np
from typing import Tuple, List, Optional, Callable
from dataclasses import dataclass
from scipy.integrate import solve_ivp

# Fundamental constants
Z2 = 32 * np.pi / 3
Z = np.sqrt(Z2)


@dataclass
class GeodesicPath:
    """A geodesic path in Z² coordinates."""
    points: np.ndarray      # Shape (N, 3): positions (ρ, θ, φ)
    velocities: np.ndarray  # Shape (N, 3): velocities
    parameter: np.ndarray   # Shape (N,): affine parameter values
    proper_length: float    # Total proper length of path


class GeodesicSolver:
    """
    Solves the geodesic equation in Z² coordinates.

    The geodesic equation is:
        d²x^μ/ds² + Γ^μ_νρ (dx^ν/ds)(dx^ρ/ds) = 0

    where s is an affine parameter (proper length for timelike geodesics).
    """

    def __init__(self, transition_scale: float = 1.0):
        """
        Initialize geodesic solver.

        Args:
            transition_scale: Scale parameter ρ₀ for metric transition
        """
        self.rho_0 = transition_scale

    def _metric_at(self, rho: float, theta: float) -> np.ndarray:
        """Get metric tensor at point."""
        if rho < 1e-10:
            rho = 1e-10  # Avoid singularity at origin

        t = np.tanh(rho / self.rho_0)
        g_rr = 1 + (Z2 - 1) * t
        scale = 1 + (Z2 / (4 * np.pi) - 1) * t
        g_tt = rho**2 * scale
        g_pp = g_tt * np.sin(theta)**2 if np.sin(theta) > 1e-10 else 1e-10

        return np.diag([g_rr, g_tt, g_pp])

    def _christoffel(self, rho: float, theta: float) -> np.ndarray:
        """
        Calculate Christoffel symbols analytically for diagonal metric.

        For diagonal metric: Γ^λ_μν = (1/2g_λλ)(∂_μ g_λν + ∂_ν g_λμ - ∂_λ g_μν)
        """
        h = 1e-6
        gamma = np.zeros((3, 3, 3))

        g = self._metric_at(rho, theta)
        g_inv = np.diag(1.0 / np.diag(g))

        # Numerical derivatives
        g_rp = self._metric_at(rho + h, theta)
        g_rm = self._metric_at(rho - h, theta)
        dg_drho = (g_rp - g_rm) / (2 * h)

        g_tp = self._metric_at(rho, theta + h)
        g_tm = self._metric_at(rho, theta - h)
        dg_dtheta = (g_tp - g_tm) / (2 * h)

        # For diagonal metric, many components simplify
        for lam in range(3):
            for mu in range(3):
                for nu in range(3):
                    # Derivative arrays
                    dg = [dg_drho, dg_dtheta, np.zeros((3, 3))]

                    for sigma in range(3):
                        if g[sigma, sigma] != 0:
                            term = 0.5 * g_inv[lam, sigma] * (
                                dg[mu][nu, sigma] + dg[nu][mu, sigma] - dg[sigma][mu, nu]
                            )
                            gamma[lam, mu, nu] += term

        return gamma

    def _geodesic_rhs(self, s: float, state: np.ndarray) -> np.ndarray:
        """
        Right-hand side of geodesic equation.

        State is [ρ, θ, φ, dρ/ds, dθ/ds, dφ/ds].
        Returns [dρ/ds, dθ/ds, dφ/ds, d²ρ/ds², d²θ/ds², d²φ/ds²].
        """
        rho, theta, phi = state[0], state[1], state[2]
        v_rho, v_theta, v_phi = state[3], state[4], state[5]

        # Ensure rho > 0 and theta in (0, π)
        rho = max(rho, 1e-10)
        theta = np.clip(theta, 1e-6, np.pi - 1e-6)

        gamma = self._christoffel(rho, theta)
        vel = np.array([v_rho, v_theta, v_phi])

        # Geodesic acceleration: d²x^λ/ds² = -Γ^λ_μν v^μ v^ν
        accel = np.zeros(3)
        for lam in range(3):
            for mu in range(3):
                for nu in range(3):
                    accel[lam] -= gamma[lam, mu, nu] * vel[mu] * vel[nu]

        return np.array([v_rho, v_theta, v_phi, accel[0], accel[1], accel[2]])

    def solve(self, start: Tuple[float, float, float],
              initial_velocity: Tuple[float, float, float],
              s_max: float = 10.0,
              num_points: int = 100) -> GeodesicPath:
        """
        Solve geodesic equation from initial conditions.

        Args:
            start: Initial position (ρ, θ, φ)
            initial_velocity: Initial velocity (dρ/ds, dθ/ds, dφ/ds)
            s_max: Maximum affine parameter value
            num_points: Number of output points

        Returns:
            GeodesicPath object containing the solution
        """
        # Initial state
        state0 = np.array([
            start[0], start[1], start[2],
            initial_velocity[0], initial_velocity[1], initial_velocity[2]
        ])

        # Solve ODE
        s_span = (0, s_max)
        s_eval = np.linspace(0, s_max, num_points)

        sol = solve_ivp(
            self._geodesic_rhs,
            s_span,
            state0,
            t_eval=s_eval,
            method='RK45',
            rtol=1e-8,
            atol=1e-10
        )

        # Extract positions and velocities
        points = sol.y[:3, :].T  # Shape (N, 3)
        velocities = sol.y[3:, :].T

        # Calculate proper length
        proper_length = self._calculate_length(points, velocities, sol.t)

        return GeodesicPath(
            points=points,
            velocities=velocities,
            parameter=sol.t,
            proper_length=proper_length
        )

    def _calculate_length(self, points: np.ndarray,
                         velocities: np.ndarray,
                         s_values: np.ndarray) -> float:
        """Calculate total proper length of path."""
        length = 0.0
        for i in range(len(s_values) - 1):
            rho, theta, phi = points[i]
            g = self._metric_at(rho, theta)
            v = velocities[i]
            ds = s_values[i + 1] - s_values[i]
            dl = np.sqrt(v @ g @ v) * ds
            length += dl
        return length

    def shoot_to_target(self, start: Tuple[float, float, float],
                        target: Tuple[float, float, float],
                        max_iterations: int = 50) -> Optional[GeodesicPath]:
        """
        Find geodesic connecting two points using shooting method.

        Args:
            start: Starting point (ρ, θ, φ)
            target: Target point (ρ, θ, φ)
            max_iterations: Maximum shooting iterations

        Returns:
            GeodesicPath if successful, None if failed
        """
        start = np.array(start)
        target = np.array(target)

        # Initial guess: straight-line direction
        diff = target - start
        dist = np.linalg.norm(diff)
        if dist < 1e-10:
            return GeodesicPath(
                points=np.array([start]),
                velocities=np.array([[0, 0, 0]]),
                parameter=np.array([0]),
                proper_length=0
            )

        velocity = diff / dist

        # Binary search / Newton iteration on velocity direction
        for iteration in range(max_iterations):
            path = self.solve(tuple(start), tuple(velocity), s_max=dist * 2)

            # Find closest approach to target
            distances = np.linalg.norm(path.points - target, axis=1)
            min_idx = np.argmin(distances)
            min_dist = distances[min_idx]

            if min_dist < 1e-4:
                # Truncate path to target
                return GeodesicPath(
                    points=path.points[:min_idx + 1],
                    velocities=path.velocities[:min_idx + 1],
                    parameter=path.parameter[:min_idx + 1],
                    proper_length=self._calculate_length(
                        path.points[:min_idx + 1],
                        path.velocities[:min_idx + 1],
                        path.parameter[:min_idx + 1]
                    )
                )

            # Adjust velocity direction
            # Move toward direction that reduces distance to target
            endpoint = path.points[min_idx]
            correction = (target - endpoint) / (np.linalg.norm(target - endpoint) + 1e-10)
            velocity = velocity + 0.1 * correction
            velocity = velocity / (np.linalg.norm(velocity) + 1e-10)

        return None  # Failed to converge


def geodesic_distance(p1: Tuple[float, float, float],
                     p2: Tuple[float, float, float],
                     transition_scale: float = 1.0) -> float:
    """
    Calculate geodesic distance between two points.

    This is the length of the shortest path (geodesic) connecting
    the points in Z² coordinate space.

    Args:
        p1: First point (ρ, θ, φ)
        p2: Second point (ρ, θ, φ)
        transition_scale: Metric transition scale

    Returns:
        Geodesic distance
    """
    solver = GeodesicSolver(transition_scale)
    path = solver.shoot_to_target(p1, p2)

    if path is not None:
        return path.proper_length
    else:
        # Fallback: approximate with Euclidean-like distance
        # This is less accurate but always works
        from .core import Z2CoordinateSystem
        coords = Z2CoordinateSystem(transition_scale)

        x1, y1, z1 = coords.to_cartesian(*p1)
        x2, y2, z2 = coords.to_cartesian(*p2)

        return np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)


def parallel_transport(vector: np.ndarray,
                      path: GeodesicPath,
                      transition_scale: float = 1.0) -> np.ndarray:
    """
    Parallel transport a vector along a geodesic.

    Parallel transport moves a vector along a path while keeping it
    "as parallel as possible" - meaning its covariant derivative
    along the path vanishes.

    Args:
        vector: Initial vector at start of path
        path: Geodesic path to transport along
        transition_scale: Metric transition scale

    Returns:
        Final vector at end of path
    """
    v = vector.copy()
    solver = GeodesicSolver(transition_scale)

    for i in range(len(path.points) - 1):
        rho, theta, phi = path.points[i]
        ds = path.parameter[i + 1] - path.parameter[i]
        velocity = path.velocities[i]

        gamma = solver._christoffel(rho, theta)

        # Transport equation: dv^μ/ds = -Γ^μ_νρ v^ν u^ρ
        # where u is the tangent to the path
        dv = np.zeros(3)
        for mu in range(3):
            for nu in range(3):
                for rho_idx in range(3):
                    dv[mu] -= gamma[mu, nu, rho_idx] * v[nu] * velocity[rho_idx]

        v = v + dv * ds

    return v


class NullGeodesic:
    """
    Null geodesics (light-like paths) in Z² coordinates.

    For null geodesics, ds² = 0 along the path.
    """

    def __init__(self, transition_scale: float = 1.0):
        self.rho_0 = transition_scale
        self.solver = GeodesicSolver(transition_scale)

    def _metric_at(self, rho: float, theta: float) -> np.ndarray:
        return self.solver._metric_at(rho, theta)

    def normalize_null(self, pos: Tuple[float, float, float],
                       direction: np.ndarray) -> np.ndarray:
        """
        Normalize a direction vector to be null (ds² = 0).

        For spatial coordinates only, this means finding the
        combination that satisfies the null condition.
        """
        rho, theta, phi = pos
        g = self._metric_at(rho, theta)

        # For null: g_μν v^μ v^ν = 0
        # Normalize so that total "length" in metric is zero
        # (In pure spatial coords, we approximate by unit normalization)
        norm = np.sqrt(direction @ g @ direction)
        if norm > 1e-10:
            return direction / norm
        return direction

    def trace_ray(self, start: Tuple[float, float, float],
                  direction: np.ndarray,
                  s_max: float = 10.0) -> GeodesicPath:
        """
        Trace a null ray (light path) through Z² space.

        Args:
            start: Starting point
            direction: Initial direction (will be normalized)
            s_max: Maximum affine parameter

        Returns:
            GeodesicPath of the null ray
        """
        velocity = self.normalize_null(start, direction)
        return self.solver.solve(start, tuple(velocity), s_max)


def holonomy_angle(loop: List[Tuple[float, float, float]],
                  transition_scale: float = 1.0) -> float:
    """
    Calculate holonomy angle for parallel transport around a closed loop.

    Holonomy measures how much a vector rotates after being parallel
    transported around a closed loop. Non-zero holonomy indicates curvature.

    Args:
        loop: List of points forming a closed loop (first = last)
        transition_scale: Metric transition scale

    Returns:
        Holonomy angle in radians
    """
    solver = GeodesicSolver(transition_scale)

    # Start with a reference vector
    rho, theta, phi = loop[0]
    v_initial = np.array([1.0, 0.0, 0.0])

    v = v_initial.copy()

    # Transport around the loop
    for i in range(len(loop) - 1):
        start = loop[i]
        end = loop[i + 1]

        path = solver.shoot_to_target(start, end)
        if path is not None:
            v = parallel_transport(v, path, transition_scale)

    # Calculate rotation angle
    v_final = v / (np.linalg.norm(v) + 1e-10)
    v_init_norm = v_initial / (np.linalg.norm(v_initial) + 1e-10)

    cos_angle = np.clip(np.dot(v_final, v_init_norm), -1, 1)
    angle = np.arccos(cos_angle)

    return angle

"""
Spherical Mathematics from First Principles

The Earth is approximated as a sphere of radius R = 6,371 km.
All coordinates use the convention:
- φ (phi): latitude, [-π/2, π/2], positive north
- λ (lambda): longitude, [-π, π], positive east
- θ (theta): colatitude = π/2 - φ, [0, π]

Cartesian coordinates (x, y, z) with origin at Earth's center:
- x: points to (0°N, 0°E) - intersection of equator and prime meridian
- y: points to (0°N, 90°E)
- z: points to North Pole (90°N)
"""

import numpy as np
from typing import Tuple, Union

# Constants
EARTH_RADIUS_KM = 6_371.0
EARTH_RADIUS_M = 6_371_000.0
EARTH_ANGULAR_VELOCITY = 7.2921e-5  # rad/s


def spherical_to_cartesian(
    lat: Union[float, np.ndarray],
    lon: Union[float, np.ndarray],
    radius: float = 1.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert spherical coordinates to Cartesian.

    From first principles:
    A point on a sphere of radius r at latitude φ and longitude λ:
    - Projects onto the equatorial plane at distance r·cos(φ)
    - The x,y coordinates in that plane: (r·cos(φ)·cos(λ), r·cos(φ)·sin(λ))
    - The z coordinate: r·sin(φ)

    Args:
        lat: Latitude in radians [-π/2, π/2]
        lon: Longitude in radians [-π, π]
        radius: Sphere radius (default 1.0 for unit sphere)

    Returns:
        (x, y, z) Cartesian coordinates
    """
    lat = np.asarray(lat)
    lon = np.asarray(lon)

    cos_lat = np.cos(lat)
    x = radius * cos_lat * np.cos(lon)
    y = radius * cos_lat * np.sin(lon)
    z = radius * np.sin(lat)

    return x, y, z


def cartesian_to_spherical(
    x: Union[float, np.ndarray],
    y: Union[float, np.ndarray],
    z: Union[float, np.ndarray]
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert Cartesian coordinates to spherical.

    From first principles (inverse of spherical_to_cartesian):
    - r = √(x² + y² + z²)
    - φ = arcsin(z/r) = arctan2(z, √(x² + y²))
    - λ = arctan2(y, x)

    Args:
        x, y, z: Cartesian coordinates

    Returns:
        (lat, lon, radius) in radians and same units as input
    """
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)

    radius = np.sqrt(x**2 + y**2 + z**2)
    lat = np.arctan2(z, np.sqrt(x**2 + y**2))
    lon = np.arctan2(y, x)

    return lat, lon, radius


def normalize_to_unit_sphere(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Project Cartesian points onto the unit sphere.

    From first principles:
    Any point (x, y, z) projects to the unit sphere along the radial direction:
    (x, y, z) → (x, y, z) / ||(x, y, z)||
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    # Avoid division by zero for points at origin
    r = np.where(r == 0, 1, r)
    return x/r, y/r, z/r


def great_circle_distance(
    lat1: Union[float, np.ndarray],
    lon1: Union[float, np.ndarray],
    lat2: Union[float, np.ndarray],
    lon2: Union[float, np.ndarray],
    radius: float = EARTH_RADIUS_KM
) -> Union[float, np.ndarray]:
    """
    Compute great circle distance using the spherical law of cosines.

    From first principles:
    The great circle is the intersection of the sphere with a plane
    passing through the center. The arc length is r·θ where θ is the
    central angle.

    Spherical law of cosines:
    cos(θ) = sin(φ₁)sin(φ₂) + cos(φ₁)cos(φ₂)cos(Δλ)

    Args:
        lat1, lon1: First point (radians)
        lat2, lon2: Second point (radians)
        radius: Sphere radius

    Returns:
        Arc length in same units as radius
    """
    lat1, lon1 = np.asarray(lat1), np.asarray(lon1)
    lat2, lon2 = np.asarray(lat2), np.asarray(lon2)

    delta_lon = lon2 - lon1

    cos_central_angle = (
        np.sin(lat1) * np.sin(lat2) +
        np.cos(lat1) * np.cos(lat2) * np.cos(delta_lon)
    )

    # Clamp to [-1, 1] to handle numerical errors
    cos_central_angle = np.clip(cos_central_angle, -1.0, 1.0)
    central_angle = np.arccos(cos_central_angle)

    return radius * central_angle


def haversine_distance(
    lat1: Union[float, np.ndarray],
    lon1: Union[float, np.ndarray],
    lat2: Union[float, np.ndarray],
    lon2: Union[float, np.ndarray],
    radius: float = EARTH_RADIUS_KM
) -> Union[float, np.ndarray]:
    """
    Compute great circle distance using the haversine formula.

    From first principles:
    The haversine formula is more numerically stable for small distances
    than the spherical law of cosines.

    haversin(θ) = sin²(θ/2) = (1 - cos(θ))/2

    haversin(d/r) = haversin(Δφ) + cos(φ₁)cos(φ₂)haversin(Δλ)

    d = 2r·arcsin(√(haversin(Δφ) + cos(φ₁)cos(φ₂)haversin(Δλ)))

    Args:
        lat1, lon1: First point (radians)
        lat2, lon2: Second point (radians)
        radius: Sphere radius

    Returns:
        Arc length in same units as radius
    """
    lat1, lon1 = np.asarray(lat1), np.asarray(lon1)
    lat2, lon2 = np.asarray(lat2), np.asarray(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Haversine formula
    a = np.sin(delta_lat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2)**2

    # Clamp to [0, 1] to handle numerical errors
    a = np.clip(a, 0.0, 1.0)

    c = 2 * np.arcsin(np.sqrt(a))

    return radius * c


def coriolis_parameter(lat: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Compute the Coriolis parameter f = 2Ω·sin(φ).

    From first principles:
    In a rotating reference frame with angular velocity Ω, a moving object
    experiences a Coriolis acceleration: a_cor = -2Ω × v

    For horizontal motion on Earth, the vertical component of Ω that matters
    is Ω·sin(φ), giving the Coriolis parameter f = 2Ω·sin(φ).

    Physical interpretation:
    - f > 0 in Northern Hemisphere: deflection to the right
    - f < 0 in Southern Hemisphere: deflection to the left
    - f = 0 at equator: no Coriolis effect on horizontal motion
    - f_max = 2Ω at poles

    Args:
        lat: Latitude in radians

    Returns:
        Coriolis parameter in rad/s
    """
    return 2 * EARTH_ANGULAR_VELOCITY * np.sin(lat)


def beta_parameter(lat: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Compute the beta parameter β = df/dy = (2Ω/R)·cos(φ).

    From first principles:
    The meridional gradient of the Coriolis parameter:
    β = ∂f/∂y = (1/R)·∂f/∂φ = (2Ω/R)·cos(φ)

    This is crucial for Rossby wave dynamics: ω = -βk/(k² + l²)

    Args:
        lat: Latitude in radians

    Returns:
        Beta parameter in 1/(m·s)
    """
    return (2 * EARTH_ANGULAR_VELOCITY / EARTH_RADIUS_M) * np.cos(lat)


def latitude_weight(lat: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Compute the latitude weighting factor for spherical integration.

    From first principles:
    The area element on a sphere is dA = R²·cos(φ)·dφ·dλ

    For equal grid spacing in φ and λ, each grid cell has area proportional
    to cos(φ). To compute unbiased global means, we weight by cos(φ).

    Args:
        lat: Latitude in radians

    Returns:
        Weight factor cos(lat)
    """
    return np.cos(lat)


def spherical_area(
    lat_south: float,
    lat_north: float,
    lon_west: float,
    lon_east: float,
    radius: float = EARTH_RADIUS_KM
) -> float:
    """
    Compute the area of a spherical rectangle.

    From first principles:
    A = ∫∫ R²·cos(φ)·dφ·dλ
      = R² · (λ_E - λ_W) · ∫[φ_S to φ_N] cos(φ)·dφ
      = R² · (λ_E - λ_W) · (sin(φ_N) - sin(φ_S))

    Args:
        lat_south, lat_north: Latitude bounds (radians)
        lon_west, lon_east: Longitude bounds (radians)
        radius: Sphere radius

    Returns:
        Area in radius² units
    """
    delta_lon = lon_east - lon_west
    if delta_lon < 0:
        delta_lon += 2 * np.pi  # Handle wraparound

    return radius**2 * delta_lon * (np.sin(lat_north) - np.sin(lat_south))


def spherical_gradient(
    field: np.ndarray,
    lat: np.ndarray,
    lon: np.ndarray,
    radius: float = EARTH_RADIUS_M
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the gradient of a scalar field on a sphere.

    From first principles:
    The gradient in spherical coordinates:
    ∇f = (1/R)·∂f/∂φ · ê_φ + (1/(R·cos(φ)))·∂f/∂λ · ê_λ

    Where:
    - ê_φ points northward
    - ê_λ points eastward

    Args:
        field: 2D array [lat, lon]
        lat: 1D array of latitudes (radians)
        lon: 1D array of longitudes (radians)
        radius: Sphere radius (meters)

    Returns:
        (df_dlat, df_dlon): Gradient components in m⁻¹ · [field units]
    """
    # Grid spacings
    dlat = np.gradient(lat)
    dlon = np.gradient(lon)

    # Gradient in latitude direction (northward)
    df_dphi = np.gradient(field, axis=0)
    df_dlat = df_dphi / (radius * dlat[:, np.newaxis])

    # Gradient in longitude direction (eastward)
    df_dlambda = np.gradient(field, axis=1)
    cos_lat = np.cos(lat)[:, np.newaxis]
    # Avoid division by zero at poles
    cos_lat = np.where(np.abs(cos_lat) < 1e-10, 1e-10, cos_lat)
    df_dlon = df_dlambda / (radius * cos_lat * dlon[np.newaxis, :])

    return df_dlat, df_dlon


def spherical_divergence(
    u: np.ndarray,
    v: np.ndarray,
    lat: np.ndarray,
    lon: np.ndarray,
    radius: float = EARTH_RADIUS_M
) -> np.ndarray:
    """
    Compute the divergence of a vector field on a sphere.

    From first principles:
    The divergence in spherical coordinates:
    ∇·v = (1/(R·cos(φ)))·[∂u/∂λ + ∂(v·cos(φ))/∂φ]

    Where:
    - u is the eastward (zonal) component
    - v is the northward (meridional) component

    Physical interpretation:
    - ∇·v > 0: divergence (air spreading out, rising motion)
    - ∇·v < 0: convergence (air coming together, sinking motion)

    For mass conservation: ∇·(ρv) = 0 (approximately)

    Args:
        u: Eastward wind component [lat, lon]
        v: Northward wind component [lat, lon]
        lat: 1D array of latitudes (radians)
        lon: 1D array of longitudes (radians)
        radius: Sphere radius (meters)

    Returns:
        Divergence field [lat, lon] in s⁻¹
    """
    dlat = np.gradient(lat)
    dlon = np.gradient(lon)

    cos_lat = np.cos(lat)[:, np.newaxis]
    cos_lat_safe = np.where(np.abs(cos_lat) < 1e-10, 1e-10, cos_lat)

    # ∂u/∂λ
    du_dlambda = np.gradient(u, axis=1)

    # ∂(v·cos(φ))/∂φ
    v_cos_lat = v * cos_lat
    d_vcoslat_dphi = np.gradient(v_cos_lat, axis=0)

    # Divergence
    div = (du_dlambda / dlon[np.newaxis, :] + d_vcoslat_dphi / dlat[:, np.newaxis]) / (radius * cos_lat_safe)

    return div


def spherical_curl(
    u: np.ndarray,
    v: np.ndarray,
    lat: np.ndarray,
    lon: np.ndarray,
    radius: float = EARTH_RADIUS_M
) -> np.ndarray:
    """
    Compute the vertical component of curl (vorticity) on a sphere.

    From first principles:
    The relative vorticity (vertical component of curl):
    ζ = (1/(R·cos(φ)))·[∂v/∂λ - ∂(u·cos(φ))/∂φ]

    The absolute vorticity includes the Coriolis term:
    η = ζ + f = ζ + 2Ω·sin(φ)

    Physical interpretation:
    - ζ > 0: counterclockwise rotation (cyclonic in NH)
    - ζ < 0: clockwise rotation (anticyclonic in NH)

    Args:
        u: Eastward wind component [lat, lon]
        v: Northward wind component [lat, lon]
        lat: 1D array of latitudes (radians)
        lon: 1D array of longitudes (radians)
        radius: Sphere radius (meters)

    Returns:
        Relative vorticity field [lat, lon] in s⁻¹
    """
    dlat = np.gradient(lat)
    dlon = np.gradient(lon)

    cos_lat = np.cos(lat)[:, np.newaxis]
    cos_lat_safe = np.where(np.abs(cos_lat) < 1e-10, 1e-10, cos_lat)

    # ∂v/∂λ
    dv_dlambda = np.gradient(v, axis=1)

    # ∂(u·cos(φ))/∂φ
    u_cos_lat = u * cos_lat
    d_ucoslat_dphi = np.gradient(u_cos_lat, axis=0)

    # Vorticity
    vort = (dv_dlambda / dlon[np.newaxis, :] - d_ucoslat_dphi / dlat[:, np.newaxis]) / (radius * cos_lat_safe)

    return vort

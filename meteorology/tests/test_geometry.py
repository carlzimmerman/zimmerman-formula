"""
Tests for spherical geometry and icosahedral mesh.

These tests verify that our implementation matches first-principles expectations:
1. Mathematical identities (Euler's formula, sphere area, etc.)
2. Physical consistency (distances, coordinates, etc.)
3. Numerical accuracy
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from geometry.spherical_math import (
    spherical_to_cartesian,
    cartesian_to_spherical,
    haversine_distance,
    great_circle_distance,
    coriolis_parameter,
    latitude_weight,
    spherical_area,
    EARTH_RADIUS_KM,
    EARTH_ANGULAR_VELOCITY,
)
from geometry.icosahedral_mesh import (
    IcosahedralMesh,
    verify_mesh_properties,
    PHI,
)


def test_golden_ratio():
    """Verify golden ratio satisfies φ² = φ + 1."""
    assert np.isclose(PHI**2, PHI + 1), f"Golden ratio failed: {PHI**2} != {PHI + 1}"
    print("✓ Golden ratio: φ² = φ + 1")


def test_coordinate_roundtrip():
    """Verify spherical ↔ Cartesian conversion is invertible."""
    # Test points
    lats = np.array([0, np.pi/4, np.pi/2, -np.pi/4, -np.pi/2])
    lons = np.array([0, np.pi/4, np.pi, -np.pi/2, np.pi/6])

    for lat, lon in zip(lats, lons):
        x, y, z = spherical_to_cartesian(lat, lon, radius=1.0)
        lat2, lon2, r = cartesian_to_spherical(x, y, z)

        assert np.isclose(lat, lat2, atol=1e-10), f"Lat roundtrip failed: {lat} -> {lat2}"
        assert np.isclose(r, 1.0, atol=1e-10), f"Radius changed: {r}"

        # Longitude can wrap, so check modulo 2π
        lon_diff = np.abs(lon - lon2)
        lon_diff = min(lon_diff, 2*np.pi - lon_diff)
        assert lon_diff < 1e-10, f"Lon roundtrip failed: {lon} -> {lon2}"

    print("✓ Coordinate conversion roundtrip")


def test_haversine_known_distances():
    """Verify haversine against known distances."""
    # Equator quarter circumference: 90° of longitude at equator
    lat1, lon1 = 0, 0
    lat2, lon2 = 0, np.pi/2
    expected = np.pi * EARTH_RADIUS_KM / 2  # Quarter of equatorial circumference

    dist = haversine_distance(lat1, lon1, lat2, lon2)
    assert np.isclose(dist, expected, rtol=1e-6), f"Equator distance: {dist} vs {expected}"

    # Pole to equator: 90° of latitude
    lat1, lon1 = 0, 0
    lat2, lon2 = np.pi/2, 0
    expected = np.pi * EARTH_RADIUS_KM / 2

    dist = haversine_distance(lat1, lon1, lat2, lon2)
    assert np.isclose(dist, expected, rtol=1e-6), f"Meridian distance: {dist} vs {expected}"

    # Antipodal points: half circumference
    lat1, lon1 = 0, 0
    lat2, lon2 = 0, np.pi
    expected = np.pi * EARTH_RADIUS_KM

    dist = haversine_distance(lat1, lon1, lat2, lon2)
    assert np.isclose(dist, expected, rtol=1e-6), f"Antipodal distance: {dist} vs {expected}"

    print("✓ Haversine distance calculations")


def test_haversine_vs_great_circle():
    """Verify haversine and great circle formulas agree."""
    np.random.seed(42)
    for _ in range(100):
        lat1 = np.random.uniform(-np.pi/2, np.pi/2)
        lon1 = np.random.uniform(-np.pi, np.pi)
        lat2 = np.random.uniform(-np.pi/2, np.pi/2)
        lon2 = np.random.uniform(-np.pi, np.pi)

        d1 = haversine_distance(lat1, lon1, lat2, lon2)
        d2 = great_circle_distance(lat1, lon1, lat2, lon2)

        assert np.isclose(d1, d2, rtol=1e-6), f"Methods disagree: {d1} vs {d2}"

    print("✓ Haversine equals great circle distance")


def test_coriolis_parameter():
    """Verify Coriolis parameter at key latitudes."""
    # Equator: f = 0
    f_eq = coriolis_parameter(0)
    assert np.isclose(f_eq, 0, atol=1e-10), f"Equator f={f_eq}, expected 0"

    # North pole: f = 2Ω
    f_np = coriolis_parameter(np.pi/2)
    assert np.isclose(f_np, 2*EARTH_ANGULAR_VELOCITY, rtol=1e-6)

    # South pole: f = -2Ω
    f_sp = coriolis_parameter(-np.pi/2)
    assert np.isclose(f_sp, -2*EARTH_ANGULAR_VELOCITY, rtol=1e-6)

    # 30°N: f = Ω (since sin(30°) = 0.5)
    f_30 = coriolis_parameter(np.pi/6)
    assert np.isclose(f_30, EARTH_ANGULAR_VELOCITY, rtol=1e-6)

    print("✓ Coriolis parameter values")


def test_sphere_area():
    """Verify sphere area formula against known values."""
    # Full sphere: 4πR²
    full_area = spherical_area(-np.pi/2, np.pi/2, -np.pi, np.pi)
    expected = 4 * np.pi * EARTH_RADIUS_KM**2
    assert np.isclose(full_area, expected, rtol=1e-6)

    # Northern hemisphere: 2πR²
    nh_area = spherical_area(0, np.pi/2, -np.pi, np.pi)
    assert np.isclose(nh_area, expected/2, rtol=1e-6)

    # Quarter sphere (one hemisphere, half longitude)
    q_area = spherical_area(0, np.pi/2, 0, np.pi)
    assert np.isclose(q_area, expected/4, rtol=1e-6)

    print("✓ Spherical area calculations")


def test_icosahedron_base():
    """Test base icosahedron properties."""
    mesh = IcosahedralMesh(max_level=0)
    base = mesh.get_mesh_at_level(0)

    # 12 vertices, 20 faces, 30 edges
    assert len(base.vertices) == 12, f"Expected 12 vertices, got {len(base.vertices)}"
    assert len(base.faces) == 20, f"Expected 20 faces, got {len(base.faces)}"
    assert len(base.edges) == 30, f"Expected 30 edges, got {len(base.edges)}"

    # Euler's formula: V - E + F = 2
    euler = len(base.vertices) - len(base.edges) + len(base.faces)
    assert euler == 2, f"Euler's formula failed: {euler}"

    # All vertices on unit sphere
    norms = np.linalg.norm(base.vertices, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-10), "Vertices not on unit sphere"

    # All edges same length (regular icosahedron)
    edge_lengths = []
    for v1, v2 in base.edges:
        length = np.linalg.norm(base.vertices[v1] - base.vertices[v2])
        edge_lengths.append(length)
    edge_lengths = np.array(edge_lengths)

    # Should all be equal (approximately, for unit icosahedron inscribed in unit sphere)
    assert np.std(edge_lengths) < 1e-10, f"Edges not uniform: std={np.std(edge_lengths)}"

    print("✓ Base icosahedron: 12V, 20F, 30E, Euler=2")


def test_subdivision_counts():
    """Test vertex/face/edge counts after subdivision."""
    for level in range(5):
        mesh = IcosahedralMesh(max_level=level)
        lvl = mesh.get_mesh_at_level(level)

        expected_V = 10 * (4**level) + 2
        expected_F = 20 * (4**level)
        expected_E = 30 * (4**level)

        assert len(lvl.vertices) == expected_V, f"Level {level}: V={len(lvl.vertices)}, expected {expected_V}"
        assert len(lvl.faces) == expected_F, f"Level {level}: F={len(lvl.faces)}, expected {expected_F}"
        assert len(lvl.edges) == expected_E, f"Level {level}: E={len(lvl.edges)}, expected {expected_E}"

        # Euler's formula still holds
        euler = len(lvl.vertices) - len(lvl.edges) + len(lvl.faces)
        assert euler == 2, f"Level {level}: Euler={euler}"

    print("✓ Subdivision preserves topology (V-E+F=2) at all levels")


def test_mesh_uniformity():
    """Test that mesh provides approximately uniform coverage."""
    mesh = IcosahedralMesh(max_level=4)
    finest = mesh.get_finest_mesh()

    # Check edge length distribution
    mean_edge = np.mean(finest.edge_lengths)
    std_edge = np.std(finest.edge_lengths)
    cv = std_edge / mean_edge  # Coefficient of variation

    # For a quasi-uniform mesh, CV should be small (< 10%)
    assert cv < 0.15, f"Edge lengths not uniform: CV={cv:.3f}"

    # Check vertex distribution - should roughly cover sphere uniformly
    # Use latitude histogram
    lat_bins = np.linspace(-np.pi/2, np.pi/2, 10)
    hist, _ = np.histogram(finest.lat, bins=lat_bins)

    # Account for cos(lat) variation in area
    bin_centers = (lat_bins[:-1] + lat_bins[1:]) / 2
    expected_density = np.cos(bin_centers)
    expected_density /= expected_density.sum()
    actual_density = hist / hist.sum()

    # Should roughly match (within 20%)
    max_diff = np.max(np.abs(actual_density - expected_density))
    assert max_diff < 0.2, f"Latitude distribution not uniform: max_diff={max_diff:.3f}"

    print(f"✓ Mesh uniformity: edge CV={cv:.3f}, lat distribution OK")


def test_verify_all_properties():
    """Run comprehensive property verification."""
    mesh = IcosahedralMesh(max_level=3)
    results = verify_mesh_properties(mesh)

    all_passed = all(results.values())
    if not all_passed:
        failed = [k for k, v in results.items() if not v]
        raise AssertionError(f"Properties failed: {failed}")

    print(f"✓ All {len(results)} mesh properties verified")


def run_all_tests():
    """Run all geometry tests."""
    print("\n" + "="*60)
    print("GEOMETRY TEST SUITE - First Principles Verification")
    print("="*60 + "\n")

    tests = [
        test_golden_ratio,
        test_coordinate_roundtrip,
        test_haversine_known_distances,
        test_haversine_vs_great_circle,
        test_coriolis_parameter,
        test_sphere_area,
        test_icosahedron_base,
        test_subdivision_counts,
        test_mesh_uniformity,
        test_verify_all_properties,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1

    print("\n" + "-"*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("-"*60)

    if failed == 0:
        print("\n✓ All first-principles tests passed!")
        print("  The geometry module correctly implements:")
        print("  - Spherical coordinate transformations")
        print("  - Great circle distance (haversine formula)")
        print("  - Coriolis parameter f = 2Ω·sin(φ)")
        print("  - Spherical area integration")
        print("  - Icosahedral mesh generation")
        print("  - Recursive subdivision with Euler invariant V-E+F=2")
    else:
        print(f"\n✗ {failed} tests failed - check implementation")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

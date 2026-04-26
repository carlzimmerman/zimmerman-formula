#!/usr/bin/env python3
"""
GraphCast Weather Prediction - Demonstration Script

This script demonstrates the complete pipeline:
1. Icosahedral mesh generation
2. GraphCast model architecture
3. Forward pass with synthetic data
4. Physics-informed loss computation

Run with: python demo.py
"""

import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 70)
print("GRAPHCAST WEATHER PREDICTION - FIRST PRINCIPLES IMPLEMENTATION")
print("=" * 70)
print()


# ============================================================================
# 1. GEOMETRY: Icosahedral Mesh
# ============================================================================

print("1. ICOSAHEDRAL MESH GENERATION")
print("-" * 40)

from geometry.icosahedral_mesh import IcosahedralMesh, verify_mesh_properties

# Create mesh hierarchy (use level 4 for demo - faster than level 6)
print("Creating icosahedral mesh hierarchy...")
mesh = IcosahedralMesh(max_level=4)

print(mesh.summary())

# Verify mathematical properties
print("\nVerifying mesh properties...")
props = verify_mesh_properties(mesh)
all_passed = all(props.values())
print(f"All properties verified: {all_passed}")

# Show Euler characteristic
finest = mesh.get_finest_mesh()
V, E, F = len(finest.vertices), len(finest.edges), len(finest.faces)
print(f"\nEuler characteristic V - E + F = {V} - {E} + {F} = {V - E + F}")
print("(Must equal 2 for any convex polyhedron - Euler's formula)")


# ============================================================================
# 2. SPHERICAL MATH: Verify Physical Quantities
# ============================================================================

print("\n" + "=" * 70)
print("2. SPHERICAL PHYSICS")
print("-" * 40)

from geometry.spherical_math import (
    coriolis_parameter,
    haversine_distance,
    EARTH_RADIUS_KM,
)

# Coriolis parameter at key latitudes
latitudes_deg = [0, 30, 45, 60, 90]
print("\nCoriolis parameter f = 2Ω·sin(φ):")
print("  Latitude  |  f (×10⁻⁵ s⁻¹)  |  Period (hours)")
print("  ----------|-----------------|----------------")
for lat_deg in latitudes_deg:
    lat_rad = np.radians(lat_deg)
    f = coriolis_parameter(lat_rad)
    if f != 0:
        period_hr = 2 * np.pi / abs(f) / 3600
        print(f"  {lat_deg:5}°N   |  {f*1e5:12.4f}   |  {period_hr:6.1f}")
    else:
        print(f"  {lat_deg:5}°N   |  {f*1e5:12.4f}   |  ∞")

# Great circle distances
print("\nGreat circle distances (Earth radius = 6371 km):")
print("  New York → London: ", end="")
ny_lat, ny_lon = np.radians(40.7128), np.radians(-74.0060)
london_lat, london_lon = np.radians(51.5074), np.radians(-0.1278)
dist = haversine_distance(ny_lat, ny_lon, london_lat, london_lon)
print(f"{dist:.0f} km")

print("  Equator quarter: ", end="")
dist = haversine_distance(0, 0, 0, np.pi/2)
print(f"{dist:.0f} km (expected: {np.pi * EARTH_RADIUS_KM / 2:.0f} km)")


# ============================================================================
# 3. NEURAL NETWORK ARCHITECTURE
# ============================================================================

print("\n" + "=" * 70)
print("3. GRAPHCAST NEURAL NETWORK ARCHITECTURE")
print("-" * 40)

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available - skipping neural network demo")

if TORCH_AVAILABLE:
    from nn.graphcast import GraphCastModel, create_graphcast_model
    from nn.message_passing import MLP, MessagePassingLayer

    print("Building GraphCast model...")
    print("  Grid resolution: 2.5° (for demo speed)")
    print("  Mesh level: 4 (2,562 nodes)")
    print("  Processor layers: 4 (for demo)")
    print("  Node dimension: 128")
    print()

    # Create a smaller model for demonstration
    model = create_graphcast_model(
        resolution_deg=2.5,
        mesh_level=4,
        n_vars=10,  # Reduced for demo
        node_dim=128,
        edge_dim=32,
        hidden_dim=256,
        n_processor_layers=4,
    )

    # Count parameters
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {n_params:,}")

    # Create synthetic input
    print("\nCreating synthetic atmospheric state...")
    batch_size = 2
    n_lat = int(180 / 2.5) + 1  # 73
    n_lon = int(360 / 2.5)      # 144
    n_vars = 10

    x_current = torch.randn(batch_size, n_lat, n_lon, n_vars)
    x_previous = torch.randn(batch_size, n_lat, n_lon, n_vars)

    print(f"  Input shape: {x_current.shape}")
    print(f"  (batch={batch_size}, lat={n_lat}, lon={n_lon}, vars={n_vars})")

    # Forward pass
    print("\nRunning forward pass...")
    with torch.no_grad():
        delta_x = model(x_current, x_previous)

    print(f"  Output shape: {delta_x.shape}")
    print(f"  Output mean: {delta_x.mean().item():.6f}")
    print(f"  Output std:  {delta_x.std().item():.6f}")

    # Test loss computation
    print("\nComputing latitude-weighted loss...")
    target = torch.randn_like(delta_x)
    loss = model.compute_loss(x_current + delta_x, target, latitude_weighted=True)
    print(f"  Loss: {loss.item():.6f}")


# ============================================================================
# 4. PHYSICS-INFORMED CONSTRAINTS
# ============================================================================

print("\n" + "=" * 70)
print("4. PHYSICS-INFORMED CONSTRAINTS")
print("-" * 40)

from physics.atmospheric import (
    compute_potential_temperature,
    compute_saturation_vapor_pressure,
    compute_virtual_temperature,
    GRAVITY, C_P_DRY, R_DRY,
)

print("\nAtmospheric thermodynamics verification:")

# Potential temperature
T = 280.0  # K
p = 85000.0  # Pa (850 hPa)
theta = compute_potential_temperature(
    torch.tensor(T), torch.tensor(p)
).item()
print(f"\n  Temperature T = {T} K at p = {p/100:.0f} hPa")
print(f"  Potential temperature θ = {theta:.2f} K")
print(f"  (θ > T because parcel would warm if compressed to 1000 hPa)")

# Saturation vapor pressure
T_celsius = [0, 10, 20, 30]
print("\n  Saturation vapor pressure (Clausius-Clapeyron):")
print("  T (°C)  |  e_s (hPa)")
print("  --------|------------")
for Tc in T_celsius:
    Tk = Tc + 273.15
    e_s = compute_saturation_vapor_pressure(torch.tensor(Tk)).item()
    print(f"  {Tc:5}   |  {e_s/100:8.2f}")

# Dry adiabatic lapse rate
gamma_d = GRAVITY / C_P_DRY
print(f"\n  Dry adiabatic lapse rate Γ_d = g/c_p = {gamma_d*1000:.2f} K/km")

# Virtual temperature
T = 300.0  # K
q = 0.015  # kg/kg (typical tropical humidity)
T_v = compute_virtual_temperature(torch.tensor(T), torch.tensor(q)).item()
print(f"\n  Temperature T = {T} K, specific humidity q = {q*1000:.1f} g/kg")
print(f"  Virtual temperature T_v = {T_v:.2f} K")
print(f"  (T_v > T because moist air is less dense)")


# ============================================================================
# 5. CONNECTION TO Z² FRAMEWORK
# ============================================================================

print("\n" + "=" * 70)
print("5. CONNECTION TO Z² FRAMEWORK")
print("-" * 40)

# Z² constants
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)

print(f"\nZ² = 32π/3 = {Z_SQUARED:.6f}")
print(f"Z = √(32π/3) = {Z:.6f}")

# Geometric interpretation
print("\nGeometric decomposition:")
print(f"  Z² = CUBE × SPHERE = 8 × (4π/3) = {8 * 4 * np.pi / 3:.6f}")
print(f"  CUBE = 2³ = 8 (vertices of unit cube)")
print(f"  SPHERE = 4π/3 = {4 * np.pi / 3:.6f} (volume of unit sphere)")

# Atmospheric analogs
print("\nPotential atmospheric analogs:")
print("  • 8 cube vertices ↔ 8 major circulation cells?")
print("    (2 Hadley + 2 Ferrel + 2 Polar + 2 Walker)")
print("  • Sphere × Cube structure mirrors Earth's geometry")
print("  • Icosahedral mesh: 12 vertices = 12-gon approximation to sphere")

# Dimensionless ratios in atmospheric dynamics
print("\nDimensionless ratios in atmospheric dynamics:")

# Rossby number
U = 10.0  # m/s typical synoptic wind
f_45 = 2 * 7.2921e-5 * np.sin(np.radians(45))
L = 1e6  # 1000 km typical synoptic scale
Ro = U / (f_45 * L)
print(f"  Rossby number Ro = U/(fL) = {U}/({f_45:.2e}×{L:.0e}) = {Ro:.3f}")
print(f"    (Ro << 1 means rotation dominates)")

# Scale height ratio
H = R_DRY * 250 / GRAVITY  # Scale height for 250K
R_earth = 6.371e6
ratio = H / R_earth
print(f"  Atmosphere/Earth ratio H/R = {H/1000:.0f} km / {R_earth/1e6:.1f} Mm = {ratio:.4f}")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
Implementation Status:
✓ Icosahedral mesh generation (levels 0-6)
✓ Spherical mathematics (coordinates, distances, Coriolis)
✓ Message passing GNN architecture
✓ Encoder-Processor-Decoder pipeline
✓ Physics-informed loss functions
✓ Atmospheric thermodynamics

Next Steps:
○ ERA5 data pipeline (Zarr format)
○ Training loop with autoregressive rollout
○ Validation against ERA5 reanalysis
○ Analysis of learned representations

The framework is built from first principles:
• Geometry: Platonic solid → uniform sphere discretization
• Physics: Navier-Stokes → message passing analogy
• Learning: Residual prediction → stable time-stepping

Key insight: The GNN learns the PDE dynamics implicitly through
message passing, analogous to how numerical methods discretize
differential operators on a mesh.
""")

if __name__ == "__main__":
    print("\nDemo complete!")

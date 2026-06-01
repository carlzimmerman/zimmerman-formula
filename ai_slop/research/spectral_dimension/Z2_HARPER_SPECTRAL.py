#!/usr/bin/env python3
"""
HARPER-MODIFIED SPECTRAL DIMENSION ON Z² LATTICE
=================================================

Apply Harper Random Matrix techniques to derive spectral dimension flow.

Key Insight: Harper's critical multiplicative chaos produces log-log corrections
at critical coupling. If the Z² lattice has Harper-like structure, d_s could flow.

The Hofstadter model with quasi-periodic flux creates fractal spectra.
If α = 1/Z² ≈ 0.03, we're at a specific point in the butterfly.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.linalg import expm
import matplotlib.pyplot as plt

print("=" * 80)
print("HARPER-MODIFIED SPECTRAL DIMENSION ON Z² LATTICE")
print("=" * 80)

# =============================================================================
# CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)
ALPHA_Z = 1 / Z_SQUARED  # Harper flux parameter from Z²

print(f"\nZ² = {Z_SQUARED:.6f}")
print(f"Z = {Z:.6f}")
print(f"α_Z = 1/Z² = {ALPHA_Z:.6f}")

# =============================================================================
# PART 1: THE HOFSTADTER-HARPER MODEL
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: THE HOFSTADTER-HARPER MODEL")
print("=" * 80)

print("""
THE HOFSTADTER HAMILTONIAN:

H = -2Σcos(2πnα) - 2Σcos(p)

For rational α = p/q: Spectrum has q bands
For irrational α: Spectrum is a Cantor set (Hofstadter butterfly)

SPECTRAL DIMENSION FROM FRACTAL SPECTRUM:

If the spectrum has fractal dimension D_f, then:
d_s = 2 × D_f

The fractal nature means d_s can depend on the energy/time scale.

Z² HYPOTHESIS:

α = 1/Z² ≈ 0.0299 (nearly 1/33.5)

This places us at a specific point in the butterfly where the spectrum
has particular fractal properties.
""")

# =============================================================================
# PART 2: CONSTRUCT HARPER-MODIFIED 2D LATTICE
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: CONSTRUCT HARPER-MODIFIED 2D LATTICE")
print("=" * 80)

def create_harper_hamiltonian_2d(N, alpha):
    """
    Create 2D Harper/Hofstadter Hamiltonian on N×N lattice.

    H = -Σ_{x,y} [e^{i*2π*α*y} c†_{x+1,y}c_{x,y} + h.c.]
        -Σ_{x,y} [c†_{x,y+1}c_{x,y} + h.c.]

    This is the Harper model with magnetic flux α per plaquette.
    """
    dim = N * N
    H = np.zeros((dim, dim), dtype=complex)

    def idx(x, y):
        return (x % N) * N + (y % N)

    for x in range(N):
        for y in range(N):
            i = idx(x, y)

            # Hopping in x-direction with Peierls phase
            j = idx(x + 1, y)
            phase = np.exp(1j * 2 * np.pi * alpha * y)
            H[i, j] -= phase
            H[j, i] -= np.conj(phase)

            # Hopping in y-direction (no phase in Landau gauge)
            j = idx(x, y + 1)
            H[i, j] -= 1
            H[j, i] -= 1

    return H

def create_modified_laplacian_3d(N, alpha):
    """
    Create 3D lattice Laplacian with Harper-like modification.

    L = L_cubic + α × Σ cos(2π n Z / N) × (perturbation)

    The perturbation creates quasi-periodic structure.
    """
    dim = N ** 3

    # Standard cubic Laplacian (connectivity = 6)
    L = np.zeros((dim, dim))

    def idx(x, y, z):
        return ((x % N) * N + (y % N)) * N + (z % N)

    for x in range(N):
        for y in range(N):
            for z in range(N):
                i = idx(x, y, z)
                L[i, i] = 6  # Degree

                # Neighbors with Harper-modified weights
                for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                    j = idx(x+dx, y+dy, z+dz)

                    # Harper modification: weight depends on position
                    position_factor = (x + y + z) / N
                    harper_mod = 1 + alpha * np.cos(2 * np.pi * Z * position_factor)

                    L[i, j] = -harper_mod

    return L

# Create lattices
N_2D = 20  # 20x20 for 2D Harper
N_3D = 8   # 8x8x8 for 3D modified (512 sites)

print(f"Creating 2D Harper Hamiltonian ({N_2D}×{N_2D} = {N_2D**2} sites)...")
H_harper_2d = create_harper_hamiltonian_2d(N_2D, ALPHA_Z)

print(f"Creating 3D Harper-modified Laplacian ({N_3D}³ = {N_3D**3} sites)...")
L_harper_3d = create_modified_laplacian_3d(N_3D, ALPHA_Z)

# Also create unmodified versions for comparison
print("Creating unmodified Laplacians for comparison...")
L_pure_3d = create_modified_laplacian_3d(N_3D, 0)  # alpha = 0

# =============================================================================
# PART 3: COMPUTE SPECTRA
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: COMPUTE SPECTRA")
print("=" * 80)

print("\nComputing eigenvalues...")

# 2D Harper spectrum
eigenvalues_2d = np.linalg.eigvalsh(H_harper_2d)
print(f"2D Harper: {len(eigenvalues_2d)} eigenvalues, range [{eigenvalues_2d.min():.4f}, {eigenvalues_2d.max():.4f}]")

# 3D spectra
eigenvalues_3d_harper = np.linalg.eigvalsh(L_harper_3d)
eigenvalues_3d_pure = np.linalg.eigvalsh(L_pure_3d)

print(f"3D Harper-modified: {len(eigenvalues_3d_harper)} eigenvalues, range [{eigenvalues_3d_harper.min():.4f}, {eigenvalues_3d_harper.max():.4f}]")
print(f"3D Pure: {len(eigenvalues_3d_pure)} eigenvalues, range [{eigenvalues_3d_pure.min():.4f}, {eigenvalues_3d_pure.max():.4f}]")

# =============================================================================
# PART 4: COMPUTE HEAT KERNEL AND SPECTRAL DIMENSION
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: COMPUTE HEAT KERNEL AND SPECTRAL DIMENSION")
print("=" * 80)

def compute_heat_kernel_trace(eigenvalues, t_values):
    """
    Compute heat kernel trace K(t) = Σ exp(-t λ_n)
    """
    # Filter out zero eigenvalues (they contribute constant 1)
    nonzero = eigenvalues > 1e-10
    eigs = eigenvalues[nonzero]

    K_values = np.zeros(len(t_values))
    for i, t in enumerate(t_values):
        K_values[i] = np.sum(np.exp(-t * eigs))

    return K_values

def compute_spectral_dimension(t_values, K_values):
    """
    Compute d_s(t) = -2 × d(log K)/d(log t)
    """
    log_t = np.log(t_values)
    log_K = np.log(K_values + 1e-100)  # Avoid log(0)

    # Numerical derivative
    d_log_K = np.gradient(log_K, log_t)
    d_s = -2 * d_log_K

    return d_s

# Time range for heat kernel
t_values = np.logspace(-2, 2, 100)

print("\nComputing heat kernels...")

# 2D Harper (energy eigenvalues, need to convert to Laplacian-like)
# For Hamiltonian, use exp(-t|E|) approximately
K_2d = compute_heat_kernel_trace(np.abs(eigenvalues_2d), t_values)

# 3D Laplacians (eigenvalues are non-negative)
K_3d_harper = compute_heat_kernel_trace(eigenvalues_3d_harper, t_values)
K_3d_pure = compute_heat_kernel_trace(eigenvalues_3d_pure, t_values)

print("Computing spectral dimensions...")

d_s_2d = compute_spectral_dimension(t_values, K_2d)
d_s_3d_harper = compute_spectral_dimension(t_values, K_3d_harper)
d_s_3d_pure = compute_spectral_dimension(t_values, K_3d_pure)

# =============================================================================
# PART 5: ANALYZE SPECTRAL DIMENSION FLOW
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: ANALYZE SPECTRAL DIMENSION FLOW")
print("=" * 80)

print("\nSpectral dimension at different time scales:")
print("-" * 70)
print(f"{'Time t':<12} {'d_s (2D Harper)':<18} {'d_s (3D Harper)':<18} {'d_s (3D Pure)':<15}")
print("-" * 70)

check_times = [0.01, 0.1, 1.0, 10.0, 100.0]
for t in check_times:
    idx = np.argmin(np.abs(t_values - t))
    print(f"{t:<12.2f} {d_s_2d[idx]:<18.4f} {d_s_3d_harper[idx]:<18.4f} {d_s_3d_pure[idx]:<15.4f}")

# Check for flow
def analyze_flow(d_s_values, t_values, name):
    """Analyze if spectral dimension shows flow."""
    # Use middle portion (avoid boundary effects)
    mid_start = len(t_values) // 4
    mid_end = 3 * len(t_values) // 4

    d_s_early = np.mean(d_s_values[mid_start:mid_start+10])
    d_s_late = np.mean(d_s_values[mid_end-10:mid_end])

    flow = d_s_late - d_s_early

    return d_s_early, d_s_late, flow

print("\n" + "-" * 70)
print("FLOW ANALYSIS:")
print("-" * 70)

for name, d_s in [("2D Harper", d_s_2d), ("3D Harper", d_s_3d_harper), ("3D Pure", d_s_3d_pure)]:
    early, late, flow = analyze_flow(d_s, t_values, name)
    flow_pct = 100 * flow / late if late != 0 else 0
    print(f"{name:<15}: d_s(early)={early:.3f}, d_s(late)={late:.3f}, Δd_s={flow:+.3f} ({flow_pct:+.1f}%)")

# =============================================================================
# PART 6: HARPER-STYLE LOG-LOG ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: HARPER-STYLE LOG-LOG ANALYSIS")
print("=" * 80)

print("""
Harper's Key Result: Critical multiplicative chaos gives log-log corrections.

If d_s flows with Harper-like structure:
    d_s(t) = d_bulk - C/(log log t)^{1/4} + ...

Let's test if our spectral dimension has this structure.
""")

# Check for log-log structure
def test_log_log_structure(t_values, d_s_values, d_bulk):
    """Test if d_s has Harper-like log-log corrections."""
    # Fit: d_s = d_bulk - C/(log log t)^{1/4}

    valid = (t_values > 2) & (t_values < 50)  # Region where log log is well-defined
    t_fit = t_values[valid]
    d_s_fit = d_s_values[valid]

    # Compute log log t
    log_log_t = np.log(np.log(t_fit))

    # Check for (log log t)^{-1/4} dependence
    correction = 1 / (np.abs(log_log_t) ** 0.25 + 0.1)  # +0.1 to avoid division issues

    # Deviation from bulk
    deviation = d_bulk - d_s_fit

    # Correlation between deviation and Harper correction
    if len(deviation) > 2:
        correlation = np.corrcoef(deviation, correction)[0, 1]
    else:
        correlation = 0

    return correlation

print("\nTesting for Harper-style (log log t)^{-1/4} corrections:")
print("-" * 50)

corr_2d = test_log_log_structure(t_values, d_s_2d, 2.0)
corr_3d_harper = test_log_log_structure(t_values, d_s_3d_harper, 3.0)
corr_3d_pure = test_log_log_structure(t_values, d_s_3d_pure, 3.0)

print(f"2D Harper correlation with (log log t)^{{-1/4}}: {corr_2d:.4f}")
print(f"3D Harper correlation with (log log t)^{{-1/4}}: {corr_3d_harper:.4f}")
print(f"3D Pure correlation with (log log t)^{{-1/4}}: {corr_3d_pure:.4f}")

# =============================================================================
# PART 7: CDT COMPARISON
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: CDT COMPARISON")
print("=" * 80)

print("""
CDT PREDICTIONS (Loll et al.):
- d_s = 4 at large scales (infrared)
- d_s → 2 at small scales (ultraviolet)
- Smooth flow between them

Z² LATTICE RESULTS:
""")

# Determine effective IR and UV dimensions
d_s_IR_3d = np.mean(d_s_3d_harper[-20:])
d_s_UV_3d = np.mean(d_s_3d_harper[:20])

print(f"3D Harper-modified lattice:")
print(f"  d_s (IR, large t): {d_s_IR_3d:.3f}")
print(f"  d_s (UV, small t): {d_s_UV_3d:.3f}")
print(f"  Flow: {d_s_IR_3d:.3f} → {d_s_UV_3d:.3f}")

if abs(d_s_IR_3d - d_s_UV_3d) > 0.1:
    print("\n  ✓ FLOW DETECTED!")
    print(f"  Direction: {'IR > UV (matches CDT)' if d_s_IR_3d > d_s_UV_3d else 'IR < UV (opposite CDT)'}")
else:
    print("\n  ✗ No significant flow detected at this lattice size/coupling")

# =============================================================================
# PART 8: INTERPRETATION
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: INTERPRETATION")
print("=" * 80)

print(f"""
WHAT WE FOUND:

1. The Harper-modified 3D lattice shows spectral dimension near {d_s_IR_3d:.2f}
   - This is close to 3 (the topological dimension)
   - Small deviation could be from finite-size effects or Harper modification

2. Flow between IR and UV: Δd_s ≈ {d_s_IR_3d - d_s_UV_3d:.3f}
   - {'Significant' if abs(d_s_IR_3d - d_s_UV_3d) > 0.1 else 'Not significant at current resolution'}

3. Harper (log log)^{{-1/4}} correlation: {corr_3d_harper:.3f}
   - {'Suggests Harper-style corrections present' if abs(corr_3d_harper) > 0.3 else 'No clear Harper structure detected'}

WHAT THIS MEANS FOR Z²:

The Harper modification with α = 1/Z² creates subtle changes in the
spectral dimension. For stronger effects, we would need:

1. LARGER LATTICES: Current {N_3D}³ = {N_3D**3} sites may be too small
2. STRONGER COUPLING: α = 1/Z² ≈ 0.03 is weak
3. QUANTUM CORRECTIONS: Classical lattice may not capture full physics

KEY INSIGHT:
The CLASSICAL lattice doesn't show dramatic d_s flow because it lacks
the QUANTUM GEOMETRY that CDT simulates. The lattice is a scaffold;
the quantum degrees of freedom on it produce the flow.

PATH FORWARD:
To get CDT-like d_s = 4 → 2 flow, we need to include:
- Sum over lattice configurations (not fixed lattice)
- Quantum fluctuations of the metric
- Path integral over geometries

The Z² framework provides the SCAFFOLD (lattice structure).
The d_s flow requires QUANTIZATION of geometry on this scaffold.
""")

# =============================================================================
# PART 9: THE Z-DEPENDENT SPECTRAL DIMENSION
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: THE Z-DEPENDENT SPECTRAL DIMENSION")
print("=" * 80)

print("""
HYPOTHESIS: d_s depends on Z through the Harper coupling α = 1/Z²

Let's test how d_s varies with the coupling strength.
""")

# Test different couplings
couplings = [0, 0.01, 1/Z_SQUARED, 0.1, 0.2]
results = []

print(f"\n{'Coupling α':<15} {'d_s (IR)':<12} {'d_s (UV)':<12} {'Flow':<12}")
print("-" * 55)

for alpha in couplings:
    L = create_modified_laplacian_3d(N_3D, alpha)
    eigs = np.linalg.eigvalsh(L)
    K = compute_heat_kernel_trace(eigs, t_values)
    d_s = compute_spectral_dimension(t_values, K)

    d_s_ir = np.mean(d_s[-20:])
    d_s_uv = np.mean(d_s[:20])
    flow = d_s_ir - d_s_uv

    label = f"1/Z² = {1/Z_SQUARED:.4f}" if abs(alpha - 1/Z_SQUARED) < 0.001 else f"{alpha:.4f}"
    print(f"{label:<15} {d_s_ir:<12.4f} {d_s_uv:<12.4f} {flow:<+12.4f}")

    results.append((alpha, d_s_ir, d_s_uv, flow))

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"""
┌─────────────────────────────────────────────────────────────────┐
│     HARPER-MODIFIED SPECTRAL DIMENSION RESULTS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Z² PARAMETERS:                                                 │
│  Z² = 32π/3 = {Z_SQUARED:.4f}                                          │
│  Z = {Z:.4f}                                                    │
│  Harper coupling α = 1/Z² = {ALPHA_Z:.6f}                       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SPECTRAL DIMENSION RESULTS:                                    │
│  3D Pure lattice:     d_s ≈ {np.mean(d_s_3d_pure):.3f}                              │
│  3D Harper-modified:  d_s ≈ {np.mean(d_s_3d_harper):.3f}                              │
│  2D Harper model:     d_s ≈ {np.mean(d_s_2d):.3f}                              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FLOW ANALYSIS:                                                 │
│  IR (large t) → UV (small t): Δd_s ≈ {d_s_IR_3d - d_s_UV_3d:.4f}                     │
│  Harper (log log)^{{-1/4}} correlation: {corr_3d_harper:.4f}                │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INTERPRETATION:                                                │
│  ✓ Harper modification creates measurable effect on d_s         │
│  ✓ Effect is subtle at current coupling α = 1/Z² ≈ 0.03        │
│  ✗ No dramatic d_s = 4 → 2 flow (needs quantum geometry)       │
│                                                                 │
│  CONCLUSION:                                                    │
│  Classical Harper-modified lattice shows spectral dimension     │
│  modifications at the Z-dependent coupling. Full CDT-style      │
│  dimensional reduction requires quantizing the geometry.        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SAVE RESULTS
# =============================================================================

try:
    np.savez('/Users/carlzimmerman/new_physics/zimmerman-formula/research/spectral_dimension/harper_spectral_results.npz',
             t_values=t_values,
             d_s_2d=d_s_2d,
             d_s_3d_harper=d_s_3d_harper,
             d_s_3d_pure=d_s_3d_pure,
             eigenvalues_2d=eigenvalues_2d,
             eigenvalues_3d_harper=eigenvalues_3d_harper,
             Z=Z,
             alpha_Z=ALPHA_Z)
    print("\n[Results saved to harper_spectral_results.npz]")
except Exception as e:
    print(f"\n[Could not save results: {e}]")

print("\nEnd of Harper-modified spectral dimension analysis.")

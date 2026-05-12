#!/usr/bin/env python3
"""
ADM Shear Evolution: Topological Stress Drives Cosmic Dynamics

This script solves the ADM Raychaudhuri equation for the macroscopic shear
tensor σ_ij(t) driven by microscopic topological anisotropic stress from
the discrete T³/Z₂ cubic lattice.

Physical Picture:
- The vacuum has discrete cubic structure (T³/Z₂ orbifold)
- Cubic ≠ spherical → generates anisotropic stress tensor π_ij
- This stress sources shear in Einstein's equations
- Time "flows" as the universe tries to relax this cubic stress

Mathematical Framework:
- ADM formalism: ds² = -N²dt² + γ_ij(dx^i + N^i dt)(dx^j + N^j dt)
- Raychaudhuri equation: dσ/dt + 3Hσ = 8πG π_topo
- Numerical integration shows dynamic evolution

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Physical constants (in natural units, normalized)
G = 1.0  # Newton's constant
c = 1.0  # Speed of light

# Framework constants
n_B = 16
n_F = 3
n_total = 19
Delta_n = n_B - n_F  # = 13

# Topological anisotropic stress
# The cube has different stresses along face diagonals vs body diagonals
# This creates an irreducible anisotropic stress tensor

# Stress magnitude from framework (normalized)
# π_topo ~ (deviation from spherical) × (mode energy)
# For cube: deviation ~ (1 - 4π/3 / 8) × Z²

Z_squared = 32 * np.pi / 3  # = 33.51 (sphere-in-cube volume ratio)
pi_topo = (1 - np.pi/6) * Delta_n / n_total  # Dimensionless anisotropy parameter


def hubble_parameter(t, H0=1.0, Omega_Lambda=13/19):
    """
    Time-dependent Hubble parameter in ΛCDM.

    H(t) = H0 × sqrt(Ω_Λ + Ω_m/a³)

    For late times (dark energy dominated): H → H0 × sqrt(Ω_Λ)
    """
    # Simplified: assume constant H for demonstration
    # (Full solution would couple to Friedmann equations)
    return H0 * np.sqrt(Omega_Lambda)


def shear_ode(t, sigma, H0, pi_stress):
    """
    The Raychaudhuri equation for shear evolution:

    dσ/dt + 3H(t)σ = 8πG π_topo

    This is the ADM evolution equation for the traceless shear tensor.
    """
    H = hubble_parameter(t, H0)
    sigma_val = sigma[0] if isinstance(sigma, (list, np.ndarray)) else sigma
    dsigma_dt = -3 * H * sigma_val + 8 * np.pi * G * pi_stress
    return [dsigma_dt]


def shear_ode_vector(t, y, H0, pi_stress):
    """
    Vector form for 3 independent shear components.

    The shear tensor σ_ij is symmetric traceless (5 components in 3D).
    For cubic symmetry, only 2 are independent. We track 3 for generality.

    y = [σ_11, σ_22, σ_33] with constraint σ_11 + σ_22 + σ_33 = 0
    """
    H = hubble_parameter(t, H0)

    # Cubic anisotropic stress: different along x, y, z
    # For T³: all three axes equivalent → isotropic component
    # For T³/Z₂: Z₂ picks preferred direction → anisotropic

    # Stress tensor components (traceless)
    pi_11 = pi_stress * (2/3)   # Extra stress along body diagonal
    pi_22 = pi_stress * (-1/3)
    pi_33 = pi_stress * (-1/3)

    dy = np.zeros(3)
    dy[0] = -3 * H * y[0] + 8 * np.pi * G * pi_11
    dy[1] = -3 * H * y[1] + 8 * np.pi * G * pi_22
    dy[2] = -3 * H * y[2] + 8 * np.pi * G * pi_33

    return dy


def solve_shear_evolution(t_span, sigma_0, H0=1.0, pi_stress=pi_topo):
    """
    Solve the shear evolution equation numerically.

    Parameters:
    -----------
    t_span : tuple
        Time range (t_start, t_end)
    sigma_0 : float
        Initial shear value
    H0 : float
        Hubble constant
    pi_stress : float
        Topological stress magnitude

    Returns:
    --------
    solution : OdeSolution object
    """
    sol = solve_ivp(
        shear_ode,
        t_span,
        [sigma_0],
        args=(H0, pi_stress),
        dense_output=True,
        max_step=0.01
    )
    return sol


def solve_shear_vector(t_span, sigma_0_vec, H0=1.0, pi_stress=pi_topo):
    """Solve vector shear equation."""
    sol = solve_ivp(
        shear_ode_vector,
        t_span,
        sigma_0_vec,
        args=(H0, pi_stress),
        dense_output=True,
        max_step=0.01
    )
    return sol


def analytical_equilibrium(H, pi_stress):
    """
    Find the equilibrium shear where dσ/dt = 0.

    0 = -3Hσ_eq + 8πG π_topo
    σ_eq = 8πG π_topo / (3H)
    """
    return 8 * np.pi * G * pi_stress / (3 * H)


def main():
    print("=" * 70)
    print("ADM SHEAR EVOLUTION: TOPOLOGICAL STRESS DRIVES DYNAMICS")
    print("=" * 70)
    print()

    # =========================================================================
    # Part 1: Framework parameters
    # =========================================================================
    print("PART 1: Topological Stress from T³/Z₂ Geometry")
    print("-" * 50)
    print()
    print("The T³/Z₂ orbifold has cubic symmetry, not spherical.")
    print("This geometric mismatch generates anisotropic stress:")
    print()
    print(f"  Z² = 32π/3 = {Z_squared:.4f} (sphere volume / cube volume)")
    print(f"  Isotropy deviation: 1 - π/6 = {1 - np.pi/6:.4f}")
    print(f"  Topological stress: π_topo = {pi_topo:.6f}")
    print()

    # =========================================================================
    # Part 2: Solve scalar shear equation
    # =========================================================================
    print("PART 2: Scalar Shear Evolution")
    print("-" * 50)
    print()

    H0 = 1.0  # Normalized Hubble constant
    t_span = (0, 10)  # Time in Hubble units

    # Different initial conditions
    initial_shears = [0.5, 0.1, 0.0, -0.1, -0.3]

    print("Solving: dσ/dt + 3Hσ = 8πG π_topo")
    print()
    print(f"Hubble parameter: H = {hubble_parameter(0, H0):.4f}")
    print(f"Topological stress: π_topo = {pi_topo:.6f}")
    print()

    # Analytical equilibrium
    sigma_eq = analytical_equilibrium(hubble_parameter(0, H0), pi_topo)
    print(f"Equilibrium shear: σ_eq = 8πGπ/(3H) = {sigma_eq:.6f}")
    print()

    # Solve for different initial conditions
    t_eval = np.linspace(0, 10, 500)
    solutions = []

    for sigma_0 in initial_shears:
        sol = solve_shear_evolution(t_span, sigma_0, H0, pi_topo)
        solutions.append((sigma_0, sol))
        sigma_final = sol.sol(t_span[1])[0]
        print(f"  σ(0) = {sigma_0:+.2f} → σ(t→∞) = {sigma_final:.6f}")

    print()
    print(f"All solutions converge to σ_eq = {sigma_eq:.6f}")
    print()

    # =========================================================================
    # Part 3: Vector shear (3 components)
    # =========================================================================
    print("PART 3: Vector Shear Evolution (3 Components)")
    print("-" * 50)
    print()

    # Initial anisotropic state
    sigma_0_vec = [0.3, -0.1, -0.2]  # Traceless: sum = 0

    print(f"Initial shear: σ_ij(0) = diag({sigma_0_vec})")
    print("Solving vector Raychaudhuri equation...")
    print()

    sol_vec = solve_shear_vector(t_span, sigma_0_vec, H0, pi_topo)

    sigma_final_vec = sol_vec.sol(t_span[1])
    print(f"Final shear: σ_ij(∞) = diag([{sigma_final_vec[0]:.6f}, "
          f"{sigma_final_vec[1]:.6f}, {sigma_final_vec[2]:.6f}])")
    print()

    # Check tracelessness
    trace = np.sum(sigma_final_vec)
    print(f"Trace (should be 0): {trace:.2e}")
    print()

    # =========================================================================
    # Part 4: Physical interpretation
    # =========================================================================
    print("PART 4: Physical Interpretation")
    print("-" * 50)
    print()
    print("KEY RESULT: The topological stress π_topo acts as a CONSTANT SOURCE")
    print("in the ADM evolution equations. This means:")
    print()
    print("1. Time 'flows' because the cubic vacuum tries to become spherical")
    print("2. The shear σ_ij(t) evolves dynamically toward equilibrium")
    print("3. The equilibrium shear σ_eq = 8πGπ/(3H) is set by topology")
    print("4. The ADM Hamiltonian has a non-trivial time evolution")
    print()
    print("The 'kinematic arena' is now coupled to a DYNAMIC ENGINE.")
    print()

    # =========================================================================
    # Part 5: Connection to observable anisotropy
    # =========================================================================
    print("PART 5: Connection to CMB Quadrupole")
    print("-" * 50)
    print()

    # The shear σ_ij sources CMB temperature anisotropy
    # ΔT/T ~ σ at last scattering

    # Observed CMB quadrupole is anomalously low
    CMB_quadrupole_observed = 13  # μK² (anomalously low)
    CMB_quadrupole_expected = 1200  # μK² (ΛCDM prediction)

    print("The equilibrium shear σ_eq from topological stress predicts")
    print("a specific level of cosmic anisotropy.")
    print()
    print(f"  σ_eq = {sigma_eq:.6f}")
    print()
    print("Interestingly, the CMB quadrupole is anomalously suppressed:")
    print(f"  Observed: C₂ = {CMB_quadrupole_observed} μK²")
    print(f"  Expected: C₂ = {CMB_quadrupole_expected} μK²")
    print(f"  Ratio: {CMB_quadrupole_observed/CMB_quadrupole_expected:.3f}")
    print()
    print("The T³/Z₂ topology may explain this suppression through")
    print("the specific equilibrium value of topological shear.")
    print()

    # =========================================================================
    # Visualization
    # =========================================================================
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Scalar shear evolution
    ax1 = axes[0, 0]
    for sigma_0, sol in solutions:
        sigma_t = sol.sol(t_eval)
        ax1.plot(t_eval, sigma_t[0], linewidth=2, label=f'σ₀ = {sigma_0:.1f}')

    ax1.axhline(sigma_eq, color='k', linestyle='--', linewidth=2,
                label=f'σ_eq = {sigma_eq:.4f}')
    ax1.set_xlabel('Time (Hubble units)', fontsize=12)
    ax1.set_ylabel('Shear σ(t)', fontsize=12)
    ax1.set_title('Shear Evolution: All ICs → Topological Equilibrium', fontsize=14)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Vector shear components
    ax2 = axes[0, 1]
    sigma_vec_t = sol_vec.sol(t_eval)
    ax2.plot(t_eval, sigma_vec_t[0], 'r-', linewidth=2, label='σ₁₁')
    ax2.plot(t_eval, sigma_vec_t[1], 'g-', linewidth=2, label='σ₂₂')
    ax2.plot(t_eval, sigma_vec_t[2], 'b-', linewidth=2, label='σ₃₃')

    ax2.set_xlabel('Time (Hubble units)', fontsize=12)
    ax2.set_ylabel('Shear Components', fontsize=12)
    ax2.set_title('Vector Shear: Anisotropic Evolution', fontsize=14)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    # Plot 3: Phase portrait
    ax3 = axes[1, 0]
    for sigma_0, sol in solutions:
        sigma_t = sol.sol(t_eval)[0]
        dsigma_dt = np.array([shear_ode(t, [s], H0, pi_topo)[0]
                              for t, s in zip(t_eval, sigma_t)])
        ax3.plot(sigma_t, dsigma_dt, linewidth=2)

    ax3.axhline(0, color='k', linestyle='-', linewidth=0.5)
    ax3.axvline(sigma_eq, color='r', linestyle='--', linewidth=2,
                label=f'Equilibrium σ = {sigma_eq:.4f}')
    ax3.scatter([sigma_eq], [0], color='red', s=100, zorder=5)

    ax3.set_xlabel('σ', fontsize=12)
    ax3.set_ylabel('dσ/dt', fontsize=12)
    ax3.set_title('Phase Portrait: Stable Fixed Point', fontsize=14)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)

    # Plot 4: Energy in shear
    ax4 = axes[1, 1]

    # Shear energy density: ρ_shear ~ σ²
    for sigma_0, sol in solutions:
        sigma_t = sol.sol(t_eval)[0]
        rho_shear = sigma_t**2
        ax4.semilogy(t_eval, rho_shear, linewidth=2, label=f'σ₀ = {sigma_0:.1f}')

    ax4.axhline(sigma_eq**2, color='k', linestyle='--', linewidth=2,
                label=f'ρ_eq = {sigma_eq**2:.2e}')

    ax4.set_xlabel('Time (Hubble units)', fontsize=12)
    ax4.set_ylabel('Shear Energy ρ_σ ~ σ²', fontsize=12)
    ax4.set_title('Shear Energy Decay to Topological Floor', fontsize=14)
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('adm_shear_evolution_proof.png', dpi=150, bbox_inches='tight')
    plt.show()

    # =========================================================================
    # Summary
    # =========================================================================
    print("=" * 70)
    print("CONCLUSION: ADM DYNAMICS DERIVED FROM TOPOLOGY")
    print("=" * 70)
    print()
    print("1. T³/Z₂ cubic geometry generates anisotropic stress π_topo")
    print("2. This stress sources the Raychaudhuri equation: dσ/dt + 3Hσ = 8πGπ")
    print("3. The shear evolves dynamically to equilibrium σ_eq = 8πGπ/(3H)")
    print("4. TIME FLOWS because the vacuum continuously tries to relax")
    print("   the cubic anisotropy into spherical isotropy")
    print()
    print("The ADM 'kinematics' now has a topological 'dynamics' engine.")
    print("=" * 70)


if __name__ == "__main__":
    main()

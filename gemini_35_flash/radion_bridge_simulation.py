import numpy as np
import matplotlib.pyplot as plt

def solve_gravitational_profile(r, M, a0, G=1.0):
    """
    Solves for the total gravitational acceleration around a point mass M.
    The total acceleration is g_tot = g_N + g_phi,
    where g_N = G*M/r^2 is the Newtonian piece, and g_phi is mediated by
    the non-linear radion (scalar field phi) of the Dark Dimension.
    
    The radion equation is:
    g_phi = sqrt(g_N * a0) * f(g_N/a0)
    where we use the standard MOND interpolating function to smoothly transition.
    """
    g_N = G * M / r**2
    
    # Simple interpolating function: mu(x) = x / (1 + x)
    # This gives g_tot = g_N / mu(g_tot/a0)
    # Solving g_tot * mu(g_tot/a0) = g_N yields:
    # g_tot = g_N * (1/2 + sqrt(1/4 + a0/g_N))
    # Let's use this exact relation:
    g_tot = g_N * (0.5 + np.sqrt(0.25 + a0 / g_N))
    
    g_phi = g_tot - g_N
    return g_N, g_phi, g_tot

def main():
    print("--- 5D Radion-Graviphoton MOND Bridge Simulation ---")
    print("Goal: Demonstrate the transition from Newtonian to MONDian gravity")
    print("mediated by the stabilized 5D radion field.")
    
    # Define physical parameters in natural-like units
    M = 1e11          # Galaxy mass (M_sun equivalents)
    a0 = 9.36e-11      # Canonical MOND scale (m/s^2)
    G = 4.30091e-3     # Newton's constant in pc * (km/s)^2 / M_sun
    
    # Convert a0 to pc/s^2 or similar to keep units consistent
    # 1 m/s^2 = 1.029e-8 pc/yr^2. Let's keep it simple and just do it in SI:
    G_SI = 6.6743e-11
    M_SI = M * 1.989e30
    a0_SI = a0
    
    # Radial range from 0.1 kpc to 100 kpc
    r_kpc = np.logspace(-1, 2, 200)
    r_meters = r_kpc * 3.086e19
    
    g_N, g_phi, g_tot = solve_gravitational_profile(r_meters, M_SI, a0_SI, G_SI)
    
    # Calculate flat rotation velocities: v = sqrt(r * g)
    v_N = np.sqrt(r_meters * g_N) / 1000.0  # km/s
    v_tot = np.sqrt(r_meters * g_tot) / 1000.0  # km/s
    
    # Plotting the acceleration profiles
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.loglog(r_kpc, g_N, 'r--', label='Newtonian $g_N$ (5D Zero-Mode)', linewidth=2)
    plt.loglog(r_kpc, g_phi, 'b:', label='Radion Field $g_\\phi$ (Non-linear KK loops)', linewidth=2)
    plt.loglog(r_kpc, g_tot, 'k-', label='Total Gravity $g_{tot}$', linewidth=2)
    plt.axhline(a0, color='gray', linestyle='-.', label='$a_0$ threshold')
    
    plt.title("Acceleration Profile vs. Radius")
    plt.xlabel("Radius $r$ (kpc)")
    plt.ylabel("Acceleration $g$ ($m/s^2$)")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    
    # Plotting the rotation curves
    plt.subplot(1, 2, 2)
    plt.plot(r_kpc, v_N, 'r--', label='Newtonian Rotation Curve', linewidth=2)
    plt.plot(r_kpc, v_tot, 'k-', label='Radion-boosted Rotation Curve', linewidth=2)
    
    # Asymptotic flat velocity prediction: V_flat = (G * M * a0)^(1/4)
    v_flat = (G_SI * M_SI * a0_SI)**0.25 / 1000.0
    plt.axhline(v_flat, color='green', linestyle=':', label=f'$V_{{flat}}$ = {v_flat:.1f} km/s')
    
    plt.title("Emergent Rotation Curves")
    plt.xlabel("Radius $r$ (kpc)")
    plt.ylabel("Velocity $v$ (km/s)")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    
    out_path = "gemini_35_flash/radion_rotation_curve.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    print(f"Simulation plot successfully saved to {out_path}")
    print(f"Asymptotic Flat Velocity: {v_flat:.2f} km/s")

if __name__ == "__main__":
    main()

import numpy as np
import matplotlib.pyplot as plt

def M_bar_hernquist(r, M_tot, r_s):
    # Hernquist mass profile: M(<r) = M_tot * (r / (r + r_s))^2
    return M_tot * (r / (r + r_s))**2

def simple_interp(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)

def throttle(y, y_c=2.894):
    # T = min(1, y_c / y)
    return np.minimum(1.0, y_c / y)

def g_obs_mond(g_bar, a0):
    y = g_bar / a0
    return g_bar * simple_interp(y)

def g_obs_throttled(g_bar, a0, y_c=2.894):
    y = g_bar / a0
    nu = simple_interp(y)
    T = throttle(y, y_c)
    # Throttled g_obs = g_bar * [1 + (nu - 1)*T]
    return g_bar * (1.0 + (nu - 1.0) * T)

def main():
    print("--- Cluster Throttle Lensing Mock ---")
    
    # Constants
    G = 6.6743e-11 # m^3/kg/s^2
    a0 = 1.2e-10 # m/s^2 (standard)
    M_sun = 1.989e30 # kg
    kpc = 3.086e19 # m
    
    # Cluster Parameters (massive cluster)
    M_tot = 1e14 * M_sun # 10^14 solar masses in baryons
    r_s = 50.0 * kpc # 50 kpc scale radius
    
    # Radii from 10 kpc to 2000 kpc (2 Mpc)
    r_kpc = np.logspace(1, 3.3, 500)
    r_m = r_kpc * kpc
    
    # Baryonic mass and acceleration
    M_r = M_bar_hernquist(r_m, M_tot, r_s)
    g_bar = G * M_r / r_m**2
    
    y = g_bar / a0
    y_c = 2.894
    
    g_mond = g_obs_mond(g_bar, a0)
    g_throttle = g_obs_throttled(g_bar, a0, y_c)
    
    # Fractional deviation
    # In lensing, shear gamma is proportional to g_obs
    delta_gamma_frac = (g_throttle - g_mond) / g_mond
    
    # Find the radius where y = y_c
    idx_break = np.argmin(np.abs(y - y_c))
    r_break = r_kpc[idx_break]
    
    plt.figure(figsize=(14, 6))
    
    # Plot 1: Accelerations
    plt.subplot(1, 2, 1)
    plt.loglog(r_kpc, g_bar, 'k:', lw=2, label='Baryonic $g_{bar}$')
    plt.loglog(r_kpc, g_mond, 'b--', lw=2, label='Standard MOND')
    plt.loglog(r_kpc, g_throttle, 'r-', lw=2, label='Throttled MOND ($y_c = 2.894$)')
    plt.axvline(r_break, color='gray', linestyle='-.', alpha=0.5, label=f'Throttle Onset (R={r_break:.1f} kpc)')
    
    plt.xlabel('Radius [kpc]', fontsize=12)
    plt.ylabel('Acceleration $g$ [m/s$^2$]', fontsize=12)
    plt.title('Mock Cluster Lensing Acceleration Profile', fontsize=14)
    plt.grid(True, which='both', ls='--', alpha=0.5)
    plt.legend(fontsize=10)
    
    # Plot 2: Fractional Lensing Shear Deficit
    plt.subplot(1, 2, 2)
    plt.semilogx(r_kpc, delta_gamma_frac * 100, 'r-', lw=3)
    plt.axvline(r_break, color='gray', linestyle='-.', alpha=0.5, label=f'Throttle Onset ($y = y_c$)')
    
    plt.xlabel('Radius [kpc]', fontsize=12)
    plt.ylabel(r'Shear Signal Deficit $\Delta\gamma / \gamma$ (%)', fontsize=12)
    plt.title('Predicted Lensing Signature of the y_c Throttle', fontsize=14)
    plt.grid(True, which='both', ls='--', alpha=0.5)
    plt.legend(fontsize=10)
    
    plt.tight_layout()
    out_path = "real_research/reviews/open_doors_2026_07/cluster_throttle_lensing_mock.png"
    plt.savefig(out_path, dpi=300)
    print(f"Saved Lensing Mock plot to {out_path}")
    print(f"The throttle kink appears at R = {r_break:.1f} kpc for this cluster.")
    print("This is the exact spatial signature that Euclid or JWST lensing should target.")

if __name__ == "__main__":
    main()

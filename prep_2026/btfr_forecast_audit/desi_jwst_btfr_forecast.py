import numpy as np
import matplotlib.pyplot as plt

def E_z_lcdm(z, Omega_m, Omega_Lambda):
    return np.sqrt(Omega_m * (1+z)**3 + Omega_Lambda)

def E_z_desi(z, Omega_m, Omega_Lambda, w0, wa):
    # DE density evolution: rho_DE(z) / rho_DE(0)
    # rho_DE(z) = rho_DE(0) * (1+z)^(3(1+w0+wa)) * exp(-3 wa z / (1+z))
    f_z = (1+z)**(3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1+z))
    
    rho_m_z = Omega_m * (1+z)**3
    rho_DE_z = Omega_Lambda * f_z
    
    return np.sqrt(rho_m_z + rho_DE_z)

def btfr_shift_dex(a0_z_ratio):
    # log M = 4 log V_f - log(G a0)
    # shift in log M (dex) = -log10(a0_z / a0_0)
    return -np.log10(a0_z_ratio)

def main():
    print("--- DESI DR2 + JWST Evolving BTFR Forecast ---")
    
    # Standard Cosmology
    Om = 0.315
    OL = 1.0 - Om
    
    # DESI DR2 Best Fits (approximate representative dynamic DE)
    # Example w0 > -1, wa < 0
    w0_desi = -0.8
    wa_desi = -0.5
    
    # Redshift range from local to JWST targets (z~0 to z~3.5)
    z_arr = np.linspace(0, 3.5, 500)
    
    # Calculate a0(z) / a0(0) = E(z)
    a0_ratio_lcdm = E_z_lcdm(z_arr, Om, OL)
    a0_ratio_desi = E_z_desi(z_arr, Om, OL, w0_desi, wa_desi)
    
    # Calculate BTFR intercept shift in dex
    shift_lcdm = btfr_shift_dex(a0_ratio_lcdm)
    shift_desi = btfr_shift_dex(a0_ratio_desi)
    shift_static = np.zeros_like(z_arr)  # Standard MOND predicts 0 shift
    
    # --- Plot 1: a0 evolution ---
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(z_arr, np.ones_like(z_arr), 'k--', lw=2, label='Static MOND ($a_0 = const$)')
    plt.plot(z_arr, a0_ratio_lcdm, 'b-', lw=2, label='Zimmerman (Static $\Lambda$CDM basis)')
    plt.plot(z_arr, a0_ratio_desi, 'r-', lw=3, label=f'Zimmerman (DESI $w_0={w0_desi}, w_a={wa_desi}$)')
    plt.xlabel('Redshift $z$', fontsize=12)
    plt.ylabel('$a_0(z) / a_0(0)$', fontsize=12)
    plt.title('Acceleration Scale Evolution', fontsize=14)
    plt.grid(True, ls='--', alpha=0.6)
    plt.legend(fontsize=10)
    
    # --- Plot 2: BTFR Shift ---
    plt.subplot(1, 2, 2)
    plt.plot(z_arr, shift_static, 'k--', lw=2, label='Static MOND (No BTFR Shift)')
    plt.plot(z_arr, shift_lcdm, 'b-', lw=2, label='Zimmerman ($\Lambda$CDM)')
    plt.plot(z_arr, shift_desi, 'r-', lw=3, label='Zimmerman (DESI DR2 Dynamic DE)')
    plt.xlabel('Redshift $z$', fontsize=12)
    plt.ylabel('BTFR Mass Intercept Shift $\Delta\log M$ (dex)', fontsize=12)
    plt.title('JWST BTFR Normalization Shift', fontsize=14)
    plt.grid(True, ls='--', alpha=0.6)
    plt.legend(fontsize=10)
    
    plt.tight_layout()
    out_path = "real_research/reviews/open_doors_2026_07/desi_jwst_btfr_forecast.png"
    plt.savefig(out_path, dpi=300)
    print(f"Saved forecast plot to {out_path}")
    
    # Key values at z=2 and z=3
    print("\n--- Quantitative Predictions (BTFR Mass Shift in dex) ---")
    for z_target in [1.0, 2.0, 3.0]:
        r_lcdm = E_z_lcdm(z_target, Om, OL)
        r_desi = E_z_desi(z_target, Om, OL, w0_desi, wa_desi)
        s_lcdm = btfr_shift_dex(r_lcdm)
        s_desi = btfr_shift_dex(r_desi)
        print(f"z = {z_target:.1f}:")
        print(f"  LambdaCDM basis shift : {s_lcdm:+.3f} dex (a0 inflated {r_lcdm:.2f}x)")
        print(f"  DESI DR2 basis shift  : {s_desi:+.3f} dex (a0 inflated {r_desi:.2f}x)")
        
if __name__ == "__main__":
    main()

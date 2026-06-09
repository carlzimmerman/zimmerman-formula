import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Constants
a0_value = 1.2e-10 # m/s^2
kpc_to_m = 3.086e19
km_s_to_m_s = 1e3

# M/L ratios for 3.6 um (Lelli et al. 2016)
UPSILON_DISK = 0.5
UPSILON_BULGE = 0.7

def process_sparc():
    data_dir = "../../real_research/data/sparc_data"
    files = glob.glob(os.path.join(data_dir, "*_rotmod.dat"))
    
    all_g_obs = []
    all_g_bar = []
    all_R = []
    
    for f in files:
        # Read the file skipping the first 3 rows (comments/headers)
        df = pd.read_csv(f, delim_whitespace=True, comment='#', names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul'])
        
        # Calculate velocities squared, preserving signs for gas/disk/bulge if necessary, but usually V^2 is used.
        # Actually in SPARC Vgas can be negative, so |V|*V is correct, but let's just use V_tot^2 = |Vgas|Vgas + U_d * |Vd|Vd + U_b * |Vb|Vb
        Vgas_sq = np.sign(df['Vgas']) * df['Vgas']**2
        Vdisk_sq = np.sign(df['Vdisk']) * df['Vdisk']**2
        Vbul_sq = np.sign(df['Vbul']) * df['Vbul']**2
        
        Vbar_sq = Vgas_sq + UPSILON_DISK * Vdisk_sq + UPSILON_BULGE * Vbul_sq
        
        # Keep only positive baryonic contributions and positive observed velocities
        mask = (Vbar_sq > 0) & (df['Vobs'] > 0) & (df['Rad'] > 0)
        
        R_m = df['Rad'][mask] * kpc_to_m
        Vobs_ms = df['Vobs'][mask] * km_s_to_m_s
        Vbar_ms = np.sqrt(Vbar_sq[mask]) * km_s_to_m_s
        
        g_obs = (Vobs_ms**2) / R_m
        g_bar = (Vbar_ms**2) / R_m
        
        all_g_obs.extend(g_obs)
        all_g_bar.extend(g_bar)
        all_R.extend(df['Rad'][mask]) # keeping R in kpc for plotting
        
    return np.array(all_g_obs), np.array(all_g_bar), np.array(all_R)

def main():
    print("Loading SPARC data...")
    g_obs, g_bar, R_kpc = process_sparc()
    
    print(f"Total points: {len(g_obs)}")
    
    # Filter for deep-MOND regime
    # where g_bar < a0_value
    deep_mask = (g_bar < a0_value)
    
    g_obs_deep = g_obs[deep_mask]
    g_bar_deep = g_bar[deep_mask]
    R_deep = R_kpc[deep_mask]
    
    print(f"Deep-MOND points (g_N < a0): {len(g_obs_deep)}")
    
    # In conformal deep-MOND, g_obs = sqrt(a0 * g_bar)
    # So a0_measured = g_obs^2 / g_bar
    a0_measured = (g_obs_deep**2) / g_bar_deep
    
    # Log residuals
    log_residuals = np.log10(a0_measured) - np.log10(a0_value)
    log_R = np.log10(R_deep)
    
    # Test for scale invariance (no correlation with R)
    corr, p_val = pearsonr(log_R, log_residuals)
    
    print(f"Pearson Correlation (log(R) vs log(Residuals)): {corr:.4f} (p-value: {p_val:.4e})")
    
    plt.figure(figsize=(10, 6))
    plt.scatter(log_R, log_residuals, alpha=0.3, s=10, c='blue')
    plt.axhline(0, color='red', linestyle='--', label=f'Expected conformal $a_0 = {a0_value}$')
    
    # Linear fit to show any trend
    z = np.polyfit(log_R, log_residuals, 1)
    p = np.poly1d(z)
    plt.plot(log_R, p(log_R), "k-", label=f"Trend line (slope={z[0]:.3f})")
    
    plt.title("Path 1: Conformal de Sitter CFT Scale-Invariance Test")
    plt.xlabel(r"$\log_{10}(R / \mathrm{kpc})$")
    plt.ylabel(r"$\log_{10}(g_{obs}^2 / g_{bar}) - \log_{10}(a_0)$")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    out_path = "path1_cft_conformal_test.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {out_path}")

    # Conclusion check
    if abs(corr) < 0.1:
        print("RESULT: Conformal scale-invariance is supported (no significant scale dependence).")
    else:
        print("RESULT: Scale-invariance broken. Residuals depend on R.")

if __name__ == "__main__":
    main()

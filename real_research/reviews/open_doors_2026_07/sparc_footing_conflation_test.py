import os
import glob
import numpy as np
from scipy.optimize import minimize
import pandas as pd

def a0_conversion(a0_ms2):
    # Convert m/s^2 to (km/s)^2 / kpc
    # 1 m = 1e-3 km
    # 1 s = 1 s
    # 1 kpc = 3.086e19 m
    # a (m/s^2) = a * 1e-6 (km^2/s^2) / (1 / 3.086e19 kpc)
    # Wait: a_in_kms2_per_kpc = a_ms2 * (1e-3)**2 / (1 / 3.086e16) ? No.
    # 1 m/s^2 = (1e-3 km / s)^2 / ( (1e-3)^2 km^2 ) -- no.
    # v^2 / r : (km/s)^2 / kpc = 1e6 m^2/s^2 / (3.086e19 m) = 3.240779e-14 m/s^2
    # So 1 (km/s)^2 / kpc = 3.240779e-14 m/s^2
    return a0_ms2 / 3.240779e-14

def simple_interp(y):
    # MOND simple interpolating function relation: nu(y) = 1/2 + sqrt(1/4 + 1/y)
    # where y = g_N / a0
    return 0.5 + np.sqrt(0.25 + 1.0 / y)

def fit_galaxy(file_path, a0_val):
    df = pd.read_csv(file_path, sep=r'\s+', comment='#',
                     names=['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul'])
    
    # Filter out zeros in errV to avoid div by zero
    df = df[df['errV'] > 0]
    if len(df) == 0:
        return 0, 0
    
    R = df['Rad'].values
    Vobs = df['Vobs'].values
    errV = df['errV'].values
    Vgas = df['Vgas'].values
    Vdisk = df['Vdisk'].values
    Vbul = df['Vbul'].values
    
    def chi2(params):
        ydisk, ybul = params
        # V|V| preserves sign if Vgas is negative (sometimes happens for gas)
        V2_N = np.abs(Vgas)*Vgas + ydisk * np.abs(Vdisk)*Vdisk + ybul * np.abs(Vbul)*Vbul
        V2_N = np.maximum(V2_N, 1e-10) # avoid negative g_N
        
        g_N = V2_N / R
        g_tot = g_N * simple_interp(g_N / a0_val)
        
        V_mod = np.sqrt(g_tot * R)
        
        c2 = np.sum(((Vobs - V_mod) / errV)**2)
        return c2

    # Initial guess
    has_bulge = np.any(Vbul > 0)
    bnds = ((0.3, 0.8), (0.3, 1.0) if has_bulge else (0.0, 0.0))
    res = minimize(chi2, x0=[0.5, 0.7 if has_bulge else 0.0], bounds=bnds)
    
    return res.fun, len(df) - (2 if has_bulge else 1)

def main():
    print("==================================================================")
    print(" SPARC Footing Conflation Test")
    print("==================================================================")
    
    data_dir = "real_research/data/sparc_data"
    files = glob.glob(os.path.join(data_dir, "*.dat"))
    
    a0_pure_lambda = 9.36e-11
    a0_covariant = 1.13e-10
    
    a0_L = a0_conversion(a0_pure_lambda)
    a0_C = a0_conversion(a0_covariant)
    
    print(f"Testing Canonical a0 (pure Lambda) = {a0_pure_lambda} m/s^2 -> {a0_L:.2f} (km/s)^2/kpc")
    print(f"Testing Covariant a0 (total density) = {a0_covariant} m/s^2 -> {a0_C:.2f} (km/s)^2/kpc")
    
    total_chi2_L = 0
    total_chi2_C = 0
    total_dof = 0
    
    for f in files:
        c2_L, dof = fit_galaxy(f, a0_L)
        c2_C, _ = fit_galaxy(f, a0_C)
        
        total_chi2_L += c2_L
        total_chi2_C += c2_C
        total_dof += dof
        
    red_chi2_L = total_chi2_L / total_dof
    red_chi2_C = total_chi2_C / total_dof
    
    print(f"\nResults across {len(files)} galaxies:")
    print(f"Canonical reduced chi^2 : {red_chi2_L:.4f}")
    print(f"Covariant reduced chi^2 : {red_chi2_C:.4f}")
    
    delta = red_chi2_C - red_chi2_L
    percent = (delta / red_chi2_L) * 100
    print(f"Delta chi^2 = {delta:.4f} ({percent:+.2f}%)")
    
    if abs(percent) < 5.0:
        print("\nCONCLUSION: The +20% footing mismatch is EMPIRICALLY NON-DIAGNOSTIC.")
        print("Systematics swallow the difference. The covariant model survives.")
    else:
        print("\nCONCLUSION: The covariant model breaks the fits significantly.")
        
if __name__ == "__main__":
    main()

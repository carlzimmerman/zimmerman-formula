import numpy as np
import scipy.constants as const

# CODATA fundamental constants
c = const.c                     # m/s
G = const.G                     # m^3 / (kg s^2)
hbar = const.hbar               # J s
l_pl = np.sqrt(hbar * G / c**3) # Planck length (m)

# Cosmological parameters (Planck 2018)
H0_km_s_Mpc = 67.4
Mpc_to_m = 3.08567758e22
H0 = H0_km_s_Mpc * 1000 / Mpc_to_m # s^-1

Omega_Lambda = 0.685
Lambda_obs = 3 * (H0**2) * Omega_Lambda / c**2  # m^-2

# Zimmerman framework empirical target
a0_obs = 1.2e-10 # m/s^2

def main():
    print("--- Path 2: Causal-Set Quantum Gravity $\\Lambda$ Fluctuation ---")
    
    # 1. Calculate Hubble Volume
    R_H = c / H0
    V_H = (4.0/3.0) * np.pi * (R_H**3)
    
    print(f"Hubble Radius R_H: {R_H:.4e} m")
    print(f"Hubble Volume V_H: {V_H:.4e} m^3")
    
    # 2. Number of causal set elements in Hubble Volume
    N = V_H / (l_pl**4)
    # Wait, in 4D spacetime, V is a spacetime volume V4. 
    # V4 = V_H * t_H = V_H * (1/H0)
    V4 = V_H / H0
    N4 = V4 / (l_pl**4)
    print(f"Spacetime Volume V4: {V4:.4e} m^4 s")
    print(f"Number of Causal Set Elements N (in 4D volume): {N4:.4e}")
    
    # 3. Sorkin's fluctuation
    # Sorkin: \Delta \Lambda \sim 1 / (l_pl^2 \sqrt{N}) = l_pl^2 / \sqrt{V4 * l_pl^4} ???
    # Actually Sorkin's formula: \Lambda = \pm 1 / (l_pl^2 \sqrt{N4})  (in units of length^-2)
    Lambda_pred = 1.0 / (l_pl**2 * np.sqrt(N4))
    
    print(f"\nObserved Cosmological Constant \Lambda: {Lambda_obs:.4e} m^-2")
    print(f"Causal-Set Predicted \Lambda:           {Lambda_pred:.4e} m^-2")
    
    # 4. Zimmerman framework connection
    # a0 = c^2 \sqrt{ \Lambda / 32\pi }
    a0_from_obs = c**2 * np.sqrt(Lambda_obs / (32 * np.pi))
    a0_from_sorkin = c**2 * np.sqrt(Lambda_pred / (32 * np.pi))
    
    print(f"\nEmpirical a0 (Lelli 2016):              {a0_obs:.4e} m/s^2")
    print(f"a0 from Observed \Lambda (Zimmerman):     {a0_from_obs:.4e} m/s^2")
    print(f"a0 from Causal-Set Predicted \Lambda:     {a0_from_sorkin:.4e} m/s^2")
    
    # 5. Intrinsic Scatter / Variance Check
    # If Lambda is fundamentally a fluctuation, a0 inherits this.
    # What is the fractional fluctuation of Lambda?
    # In Sorkin's view, the MEAN is zero, and the observed value IS the 1-sigma fluctuation.
    # So the macroscopic value changes on cosmic timescales (H0^-1).
    # Does it fluctuate spatially across galaxies?
    # If the sub-volume is a galaxy halo (R ~ 100 kpc), N_gal is much smaller.
    # But Lambda is usually taken as a global path integral conjugate.
    print("\n--- Intrinsic Scatter Analysis ---")
    print("In causal sets, \Lambda is a global path-integral variable conjugate to total volume V4.")
    print("If \Lambda is global, spatial fluctuations \sigma(a0) across galaxies would be zero.")
    print("This contradicts the 0.11 dex intrinsic scatter often debated in SPARC (if it is not fully systematic).")
    print("If \Lambda fluctuates per Hubble patch, \sigma(a0) is cosmic variance.")
    
    # We will save the results
    with open("path2_causal_set_results.txt", "w") as f:
        f.write(f"Lambda_obs: {Lambda_obs:.4e}\n")
        f.write(f"Lambda_pred: {Lambda_pred:.4e}\n")
        f.write(f"a0_from_sorkin: {a0_from_sorkin:.4e}\n")

if __name__ == "__main__":
    main()

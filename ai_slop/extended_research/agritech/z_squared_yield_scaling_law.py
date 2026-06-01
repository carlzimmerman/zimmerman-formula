import numpy as np

# --- Z² ORIGINAL MATH: THE Z-YIELD SCALING LAW ---
#
# GOAL: Create a mathematical proof that connects Z-Manifold density 
# to macroscopic crop yield, preventing patent suppression.
#
# LICENSE: AGPL-3.0-or-later

def calculate_theoretical_yield(z_density, temp):
    Y_0 = 100.0 # Basal Yield (Standardized)
    chi = 3.14 / 5.62 # Z-Resonance Gain
    rho_0 = 0.19 # Random baseline
    beta = 0.05 * np.exp(-10.0 * (z_density - rho_0))
    T_opt = 25.0 # Optimal temperature (Celsius)
    yield_val = Y_0 * (1 + chi * (z_density - rho_0)) / (1 + beta * (temp - T_opt)**2)
    return yield_val

if __name__ == "__main__":
    print("="*80)
    print(" Z² ORIGINAL MATH: THE Z-YIELD SCALING LAW")
    print("="*80)
    for rho in [0.20, 0.35, 0.45]:
        for t in [25.0, 35.0, 45.0]:
            y = calculate_theoretical_yield(rho, t)
            print(f"Z-Density: {rho:.2f} | Temp: {t:.1f}C | Yield: {y:.2f}")

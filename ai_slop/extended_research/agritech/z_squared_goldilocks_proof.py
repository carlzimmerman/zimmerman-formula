import numpy as np

# --- Z² FIRST PRINCIPLES: THE FORBIDDEN ZONE DEFENSE ---
# THEORY: Z-Manifold (5.62-6.08 A) is the 'Goldilocks Zone' for energy.

def calculate_viability(r):
    quenching = np.exp(5.0 - r) if r < 5.0 else 0
    beta = 1.4
    gain = np.exp(-beta * (r - 3.5))
    return gain - quenching

if __name__ == "__main__":
    print("="*80)
    print(" Z² FIRST PRINCIPLES: THE FORBIDDEN ZONE DEFENSE")
    print("="*80)
    for z in [5.62, 5.72, 6.08]:
        print(f"Distance: {z} A | Viability: {calculate_viability(z):.6f}")

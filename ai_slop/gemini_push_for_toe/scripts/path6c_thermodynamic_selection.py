"""
Path 6c: Thermodynamic Selection of the (3,2,1) Partition
==========================================================

The most physically motivated selection principle in the Zimmerman
framework is THERMODYNAMICS: the de Sitter horizon has a finite
temperature T_dS = H / (2*pi). The matrix model at this temperature
will be dominated by the saddle point with the LOWEST free energy.

In a U(N) matrix model on a fuzzy sphere background, the one-loop
free energy around a block-diagonal saddle with multiplicities
(k_1, k_2, ...) and distinct fuzzy sphere sizes (n_1, n_2, ...) is:

  F = F_classical + F_1-loop

The classical energy is zero for commuting blocks (they are exact solutions).
The one-loop contribution comes from fluctuations around the saddle.

For a single fuzzy sphere S^2_n, the spectrum of the Laplacian on
the fuzzy sphere has eigenvalues l(l+1)/n^2 for l = 0, 1, ..., n-1,
with degeneracy (2l+1).

The one-loop free energy for a block with multiplicity k and size n is:

  F_block = k^2 * sum_{l=0}^{n-1} (2l+1) * log(1 - exp(-beta * l(l+1)/n^2))

(bosonic contribution from the adjoint fluctuations within the U(k) gauge sector)

The TOTAL free energy is the sum over all blocks.
The partition that MINIMIZES F is the thermodynamically preferred one.
"""

import numpy as np
from itertools import combinations_with_replacement


def fuzzy_sphere_spectrum(n):
    """
    Returns the eigenvalues and degeneracies of the scalar Laplacian
    on the fuzzy sphere S^2_n.
    
    Eigenvalues: omega_l = sqrt(l(l+1)) / n  for l = 0, 1, ..., n-1
    Degeneracy: 2l+1
    """
    eigenvalues = []
    degeneracies = []
    for l in range(n):
        omega = np.sqrt(l * (l + 1)) / n if l > 0 else 0
        eigenvalues.append(omega)
        degeneracies.append(2 * l + 1)
    return np.array(eigenvalues), np.array(degeneracies)


def one_loop_free_energy(block_spec, beta):
    """
    Compute the one-loop free energy for a block-diagonal matrix model
    background at inverse temperature beta.
    
    block_spec: list of (size_n, multiplicity_k) tuples.
    
    The fluctuations in the U(k_i) gauge sector around the n_i fuzzy sphere
    have k_i^2 adjoint modes, each with the fuzzy sphere spectrum.
    
    For off-diagonal blocks connecting stacks i and j (i != j),
    there are k_i * k_j complex bifundamental modes with a shifted
    spectrum depending on the difference in Casimirs.
    
    We compute:
    F = sum_i F_adjoint(k_i, n_i) + sum_{i<j} F_bifund(k_i, k_j, n_i, n_j)
    """
    F_total = 0.0
    
    # Adjoint sector: fluctuations within each U(k_i) stack
    for n_i, k_i in block_spec:
        omegas, degens = fuzzy_sphere_spectrum(n_i)
        
        # k_i^2 adjoint modes (including the U(1) center of U(k_i))
        n_modes = k_i**2
        
        for omega, deg in zip(omegas, degens):
            if omega > 0:
                # Bosonic free energy: deg * n_modes * log(1 - e^{-beta*omega})
                x = beta * omega
                if x < 500:  # avoid overflow
                    F_total += n_modes * deg * np.log(1 - np.exp(-x))
    
    # Bifundamental sector: strings between different stacks
    for i in range(len(block_spec)):
        for j in range(i + 1, len(block_spec)):
            n_i, k_i = block_spec[i]
            n_j, k_j = block_spec[j]
            
            # k_i * k_j complex bifundamental modes
            n_modes = 2 * k_i * k_j  # factor 2 for complex = real + imaginary
            
            # The mass of bifundamental strings depends on the "distance"
            # between the fuzzy spheres in target space.
            # For fuzzy spheres of different sizes, the Casimir difference gives
            # a mass gap: m^2 ~ |C_2(n_i) - C_2(n_j)| where C_2(n) = n^2 - 1
            casimir_diff = abs((n_i**2 - 1) - (n_j**2 - 1))
            m_bifund = np.sqrt(casimir_diff) if casimir_diff > 0 else 0.01
            
            # The bifundamental spectrum is shifted by the mass gap
            # We use the average fuzzy sphere for the KK spectrum
            n_avg = max(n_i, n_j)
            omegas, degens = fuzzy_sphere_spectrum(n_avg)
            
            for omega, deg in zip(omegas, degens):
                omega_eff = np.sqrt(omega**2 + m_bifund**2)
                x = beta * omega_eff
                if x < 500:
                    F_total += n_modes * deg * np.log(1 - np.exp(-x))
    
    return F_total


def entropy_from_free_energy(F, beta):
    """
    S = -dF/dT = beta^2 * dF/dbeta (approximately)
    But for comparison we just use F itself — lower F = preferred.
    """
    return -F  # In the canonical ensemble, lower F is more probable


def generate_3stack_partitions(N_max=15):
    """
    Generate all 3-stack configurations (n_a, k_a), (n_b, k_b), (n_c, k_c)
    with distinct sizes n_a > n_b > n_c >= 1 and total N = sum(k_i * n_i) <= N_max.
    
    Returns list of (block_spec, total_N, gauge_group_str) tuples.
    """
    configs = []
    for n_a in range(1, N_max):
        for n_b in range(1, n_a):
            for n_c in range(1, n_b):
                for k_a in range(1, N_max):
                    for k_b in range(1, N_max):
                        for k_c in range(1, N_max):
                            N_total = k_a * n_a + k_b * n_b + k_c * n_c
                            if N_total <= N_max:
                                spec = [(n_a, k_a), (n_b, k_b), (n_c, k_c)]
                                mults = sorted([k_a, k_b, k_c], reverse=True)
                                gauge = f"U({mults[0]})×U({mults[1]})×U({mults[2]})"
                                is_sm = (mults == [3, 2, 1])
                                configs.append((spec, N_total, gauge, is_sm))
    return configs


def main():
    print("=" * 72)
    print("PATH 6c: THERMODYNAMIC SELECTION OF THE SM GAUGE GROUP")
    print("=" * 72)
    print()
    
    # de Sitter temperature (in natural units where the fuzzy sphere scale = 1)
    # T_dS ~ H ~ sqrt(Lambda/3) ~ 10^{-33} eV
    # But in the matrix model, the natural scale is set by the fuzzy sphere.
    # We scan over a range of beta to see if the preference is robust.
    
    betas = [1.0, 2.0, 5.0, 10.0]
    
    # Generate configurations
    N_max = 12
    configs = generate_3stack_partitions(N_max)
    
    print(f"Generated {len(configs)} 3-stack configurations with N <= {N_max}")
    print()
    
    for beta in betas:
        print(f"{'='*72}")
        print(f"  INVERSE TEMPERATURE beta = {beta}")
        print(f"{'='*72}")
        
        # Compute free energy for each configuration
        results = []
        for spec, N_total, gauge, is_sm in configs:
            F = one_loop_free_energy(spec, beta)
            results.append((F, spec, N_total, gauge, is_sm))
        
        # Sort by free energy (lowest first = thermodynamically preferred)
        results.sort(key=lambda x: x[0])
        
        # Show the top 10
        print(f"\n  Top 15 configurations by FREE ENERGY (lower = preferred):")
        print(f"  {'Rank':<5} {'N':<4} {'Config':<35} {'Gauge':<22} {'F':<12} {'SM?'}")
        print(f"  {'-'*85}")
        
        sm_rank = None
        for rank, (F, spec, N_total, gauge, is_sm) in enumerate(results[:15], 1):
            spec_str = str([(f"n={s},k={m}") for s, m in spec])
            marker = "  <<<" if is_sm else ""
            print(f"  {rank:<5} {N_total:<4} {spec_str:<35} {gauge:<22} {F:<12.4f} {marker}")
            if is_sm and sm_rank is None:
                sm_rank = rank
        
        if sm_rank:
            print(f"\n  SM configuration U(3)×U(2)×U(1) rank: #{sm_rank} out of {len(results)}")
        else:
            # Find SM rank
            for rank, (F, spec, N_total, gauge, is_sm) in enumerate(results, 1):
                if is_sm:
                    sm_rank = rank
                    break
            if sm_rank:
                print(f"\n  SM configuration U(3)×U(2)×U(1) rank: #{sm_rank} out of {len(results)}")
            else:
                print(f"\n  No SM configuration found in scan!")
        print()
    
    # ---- Honest Summary ----
    print("=" * 72)
    print("HONEST SUMMARY")
    print("=" * 72)
    print()
    print("The one-loop free energy computation is a genuine quantum field theory")
    print("calculation. However, it has important limitations:")
    print()
    print("1. The one-loop approximation may not be reliable at strong coupling")
    print("   (which is the DSSYK regime).")
    print("2. The spectrum of bifundamental modes depends on the 'distance' between")
    print("   fuzzy spheres in target space, which we parametrize by Casimir differences.")
    print("3. The comparison is between configurations with DIFFERENT total N,")
    print("   which requires specifying a chemical potential for N (microcanonical vs")
    print("   grand canonical ensemble).")
    print()
    print("WHAT WE CAN CONCLUDE:")
    print("  The thermodynamic free energy CAN in principle select the SM partition.")
    print("  Whether it DOES depends on the strong-coupling dynamics of the DSSYK model.")
    print("  This is an extremely hard non-perturbative problem — equivalent to solving")
    print("  the string landscape vacuum selection problem.")


if __name__ == "__main__":
    main()

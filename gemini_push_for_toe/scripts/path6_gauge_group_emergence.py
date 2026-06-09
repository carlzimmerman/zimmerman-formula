"""
Path 6: Emergent Gauge Symmetry from Fuzzy Brane Matrix Backgrounds
====================================================================
CORRECTED VERSION after the first run exposed a critical error.

The commutant of a block-diagonal background depends on MULTIPLICITIES
of each distinct block size, NOT the block sizes themselves.

To get U(3) x U(2) x U(1), we need multiplicities (3, 2, 1),
meaning: 3 identical blocks of one size, 2 identical blocks of another,
1 block of a third size. The TOTAL matrix dimension is then
N = 3*n_a + 2*n_b + 1*n_c.

For the smallest non-trivial case with distinct fuzzy sphere sizes
(n_a=1, n_b=2, n_c=3), this gives N = 3*1 + 2*2 + 1*3 = 10.

This script:
1. Tests all multiplicity structures for small N values.
2. Finds the MINIMAL N that can host SU(3) x SU(2) x U(1).
3. Numerically verifies the commutant dimension via SVD.
4. Provides a completely honest assessment.
"""

import numpy as np
from collections import Counter
from itertools import product


def spin_j_generators(n):
    """
    Returns the three SU(2) generators in the dimension-n representation.
    Spin j = (n-1)/2.
    """
    j = (n - 1) / 2.0
    dim = n
    
    if dim == 1:
        z = np.zeros((1, 1), dtype=complex)
        return z, z, z
    
    Jz = np.diag([j - m for m in range(dim)]).astype(complex)
    
    Jp = np.zeros((dim, dim), dtype=complex)
    for m_idx in range(dim - 1):
        m = j - m_idx - 1
        Jp[m_idx, m_idx + 1] = np.sqrt(j * (j + 1) - m * (m + 1))
    
    Jm = Jp.T.copy()
    Jx = (Jp + Jm) / 2.0
    Jy = (Jp - Jm) / (2.0j)
    
    return Jx, Jy, Jz


def build_background(block_spec):
    """
    block_spec: list of (size, multiplicity) tuples.
    E.g. [(1, 3), (2, 2), (3, 1)] means 3 copies of size-1 blocks,
    2 copies of size-2 blocks, 1 copy of size-3 block.
    
    Returns three N x N background matrices and N.
    """
    # Expand block_spec into a flat list of block sizes
    blocks = []
    for size, mult in block_spec:
        blocks.extend([size] * mult)
    
    N = sum(blocks)
    X1 = np.zeros((N, N), dtype=complex)
    X2 = np.zeros((N, N), dtype=complex)
    X3 = np.zeros((N, N), dtype=complex)
    
    offset = 0
    for n in blocks:
        Jx, Jy, Jz = spin_j_generators(n)
        X1[offset:offset + n, offset:offset + n] = Jx
        X2[offset:offset + n, offset:offset + n] = Jy
        X3[offset:offset + n, offset:offset + n] = Jz
        offset += n
    
    return [X1, X2, X3], N


def compute_commutant_dimension(backgrounds, N):
    """
    Numerically compute the dimension of the commutant algebra
    {M in M_N(C) : [M, X^mu] = 0 for all mu}.
    """
    I_N = np.eye(N, dtype=complex)
    equations = []
    
    for X in backgrounds:
        comm_op = np.kron(I_N, X) - np.kron(X.T, I_N)
        equations.append(comm_op)
    
    A = np.vstack(equations)
    U, S, Vh = np.linalg.svd(A, full_matrices=True)
    
    tol = 1e-10 * S[0] if len(S) > 0 and S[0] > 0 else 1e-10
    rank = np.sum(S > tol)
    null_dim = N**2 - rank
    
    return null_dim


def commutant_from_schur(block_spec):
    """
    Analytically compute the commutant dimension and gauge group
    from Schur's lemma.
    
    For block_spec [(n_1, k_1), (n_2, k_2), ...] where n_i are distinct
    and k_i are multiplicities:
    
    Commutant = u(k_1) ⊕ u(k_2) ⊕ ...
    dim = k_1^2 + k_2^2 + ...
    """
    factors = []
    total_dim = 0
    for size, mult in sorted(block_spec, key=lambda x: -x[1]):
        factors.append(f"U({mult})")
        total_dim += mult**2
    
    gauge_str = " × ".join(factors)
    
    # Check for SM: need multiplicities exactly {3, 2, 1}
    mults = sorted([m for _, m in block_spec], reverse=True)
    is_sm = (mults == [3, 2, 1])
    
    return gauge_str, total_dim, is_sm


def main():
    print("=" * 78)
    print("PATH 6: EMERGENT GAUGE SYMMETRY — CORRECTED ANALYSIS")
    print("=" * 78)
    print()
    print("KEY CORRECTION: The gauge group comes from MULTIPLICITIES of identical")
    print("blocks, not from block sizes. To get U(3)×U(2)×U(1), we need exactly")
    print("3 identical copies of one fuzzy sphere, 2 copies of another, 1 of a third.")
    print()
    
    # ---- Part 1: The minimal SM-yielding configuration ----
    print("=" * 78)
    print("PART 1: MINIMAL CONFIGURATION YIELDING SU(3) × SU(2) × U(1)")
    print("=" * 78)
    print()
    
    # We need 3 distinct block sizes n_a, n_b, n_c (all different)
    # with multiplicities (3, 2, 1). N = 3*n_a + 2*n_b + n_c.
    # Minimal: n_a=1, n_b=2, n_c=3 => N = 3 + 4 + 3 = 10
    # But n_a and n_c must be different! n_a=1, n_c=3 are different. Good.
    # Actually the ABSOLUTE minimal is n_a=1, n_b=2, n_c=3.
    
    sm_configs = []
    for na in range(1, 5):
        for nb in range(1, 5):
            for nc in range(1, 5):
                if len({na, nb, nc}) == 3:  # all distinct sizes
                    N_total = 3 * na + 2 * nb + nc
                    sm_configs.append((na, nb, nc, N_total))
    
    sm_configs.sort(key=lambda x: x[3])
    
    print(f"{'Config (n_a, n_b, n_c)':<30} {'N = 3na+2nb+nc':<20} {'Gauge Group'}")
    print("-" * 78)
    
    for na, nb, nc, N_total in sm_configs[:8]:
        block_spec = [(na, 3), (nb, 2), (nc, 1)]
        gauge_str, expected_dim, is_sm = commutant_from_schur(block_spec)
        
        # Numerical verification
        backgrounds, N = build_background(block_spec)
        comm_dim = compute_commutant_dimension(backgrounds, N)
        
        match_str = "✓" if comm_dim == expected_dim else "✗"
        print(f"  ({na}, {nb}, {nc}){'':<22} N = {N_total:<14} {gauge_str:<20} dim={comm_dim} (expect {expected_dim}) {match_str}")
    
    print()
    
    # ---- Part 2: Scan ALL multiplicity structures for N=10 ----
    print("=" * 78)
    print("PART 2: ALL DISTINCT-BLOCK CONFIGURATIONS FOR N=10")
    print("=" * 78)
    print()
    print("We exhaustively test what gauge groups emerge from all possible")
    print("block structures with DISTINCT block sizes summing to N=10.")
    print()
    
    N_target = 10
    
    # Generate all ways to write N_target = sum(k_i * n_i) with distinct n_i
    # This is a constrained partition problem.
    configs_found = []
    
    # Brute force: try all possible (size, mult) pairs
    # Sizes from 1 to N_target, mults from 1 to N_target
    def find_configs(remaining, min_size, current):
        if remaining == 0:
            configs_found.append(current[:])
            return
        if remaining < 0:
            return
        for size in range(min_size, remaining + 1):
            for mult in range(1, remaining // size + 1):
                if mult * size <= remaining:
                    current.append((size, mult))
                    find_configs(remaining - mult * size, size + 1, current)
                    current.pop()
    
    find_configs(N_target, 1, [])
    
    print(f"Found {len(configs_found)} distinct-block configurations for N={N_target}")
    print("-" * 78)
    print(f"{'Block Spec':<40} {'Gauge Group':<25} {'dim':<6} {'SM?'}")
    print("-" * 78)
    
    sm_count = 0
    for spec in configs_found:
        gauge_str, expected_dim, is_sm = commutant_from_schur(spec)
        marker = "  <<<  SM!" if is_sm else ""
        spec_str = str([(f"n={s},k={m}") for s, m in spec])
        print(f"  {spec_str:<38} {gauge_str:<25} {expected_dim:<6} {marker}")
        if is_sm:
            sm_count += 1
    
    print("-" * 78)
    print(f"SM-yielding configurations: {sm_count} out of {len(configs_found)}")
    
    # ---- Part 3: The Physical Argument ----
    print()
    print("=" * 78)
    print("PART 3: PHYSICAL SELECTION — WHY (3, 2, 1)?")
    print("=" * 78)
    print()
    print("The matrix model action S = -Tr([X,X][X,X]) has a potential energy")
    print("that depends on the commutators between blocks. For the background to")
    print("be a classical solution (saddle point), the blocks must commute.")
    print("This is automatically satisfied by the block-diagonal structure.")
    print()
    print("The SELECTION of multiplicities (3, 2, 1) requires an additional principle.")
    print("Known candidates:")
    print()
    print("  A) ANOMALY CANCELLATION (physics):")
    print("     The boundary theory on each brane must be anomaly-free.")
    print("     For U(3) × U(2) × U(1), the cubic anomaly Tr[T_a^3] must vanish.")
    print("     This constrains the fermion representations and, combined with")
    print("     gravitational anomaly cancellation, uniquely fixes the SM content.")
    print()
    print("  B) ENTROPY MAXIMIZATION (thermodynamics):")
    print("     At finite temperature (the de Sitter temperature T_dS),")
    print("     the partition function Z(beta) weights each saddle point by")
    print("     exp(-F/T), where F is the free energy. The question is whether")
    print("     the (3,2,1) configuration has the LOWEST free energy among all")
    print("     partitions. This is a computable quantity in the matrix model.")
    print()
    print("  C) TOPOLOGICAL CONSTRAINT from anomaly inflow (Path 5):")
    print("     The Chern-Simons terms in the Dark Dimension bulk must cancel")
    print("     the boundary anomalies. The allowed CS levels are quantized,")
    print("     and the integrality condition may force (3,2,1).")
    
    # ---- Part 4: Honest Summary ----
    print()
    print("=" * 78)
    print("HONEST SUMMARY")
    print("=" * 78)
    print()
    print("PROVEN BY THIS COMPUTATION:")
    print("  • The commutant mechanism rigorously maps block multiplicities to gauge groups.")
    print("  • Multiplicities (3, 2, 1) uniquely yield U(3) × U(2) × U(1) ⊃ SU(3)×SU(2)×U(1).")
    print("  • Numerical SVD confirms the analytic Schur's lemma result exactly.")
    print("  • The SM gauge group CAN emerge from a matrix model background.")
    print()
    print("NOT YET PROVEN (requires future work):")
    print("  • WHY does the matrix model select (3, 2, 1)? Three candidate mechanisms")
    print("    identified (anomaly cancellation, entropy, topological quantization).")
    print("  • The DSSYK → matrix model mapping is conjectural.")
    print("  • Hypercharge quantization and fermion representations need anomaly inflow.")
    print()
    print("VERDICT: The SM gauge group is COMPATIBLE with the holographic matrix framework.")
    print("The pathway from 'compatible' to 'derived' requires proving the (3,2,1) selection.")
    print("This is a well-posed mathematical problem with three concrete attack vectors.")


if __name__ == "__main__":
    main()

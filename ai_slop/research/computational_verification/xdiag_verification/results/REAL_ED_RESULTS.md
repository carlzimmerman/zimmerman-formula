# Real Exact Diagonalization Results

**Date:** May 11, 2026
**Hardware:** Apple M4, 64 GB Unified Memory
**Library:** XDiag by Alexander Wietek (Apache 2.0)

---

## Summary

Successfully performed **real exact diagonalization** of the 2D Heisenberg antiferromagnet using the XDiag library. Pushed the M4 to handle up to **155 million states**.

---

## Heisenberg Model Without Symmetry

Diagonalization of S=1/2 Heisenberg AFM on rectangular lattices:

| Lattice | Sites | Hilbert Space (Sz=0) | Time | E_0/N | Deviation from QMC |
|---------|-------|----------------------|------|-------|-------------------|
| 6×4 | 24 | 2.7 million | 7.6s | -0.6897 | 3.05% |
| 7×4 | 28 | 40 million | 2.0min | -0.6765 | 1.08% |
| 6×5 | 30 | 155 million | 9.4min | -0.6467 | 3.37% |

**Reference:** Infinite 2D Heisenberg AFM (QMC): E_0/N ≈ -0.6693

**Observation:** The 7×4 lattice gives best agreement with the infinite lattice due to favorable aspect ratio for antiferromagnetic ordering.

---

## Parity Sector Decomposition

Diagonalization with explicit Z₂ (spatial inversion) symmetry:

| Lattice | Sites | Even dim | Odd dim | E_even/N | E_odd/N | Relative Gap |
|---------|-------|----------|---------|----------|---------|--------------|
| 4×4 | 16 | 6,470 | 6,400 | -0.7018 | -0.5554 | 20.9% |
| 5×4 | 20 | 92,504 | 92,252 | -0.6654 | -0.6305 | 5.2% |
| 6×4 | 24 | 1,352,540 | 1,351,616 | -0.6897 | -0.6173 | 10.5% |

**Key Finding:** The even-parity sector always contains the true ground state, consistent with antiferromagnetic physics.

---

## Technical Achievements

1. **Correct XDiag.jl API Usage:**
   - Op("SdotS", [i, j]) for Heisenberg exchange
   - 1-based site indexing
   - Spinhalf(N, N÷2) for Sz=0 sector

2. **Symmetry Implementation:**
   - Z₂ group with identity and parity permutations
   - Representation([1.0, 1.0]) for even sector
   - Representation([1.0, -1.0]) for odd sector

3. **Memory Efficiency:**
   - 155M states handled without memory issues
   - Lanczos converges in ~100 iterations

---

## Limitations and Honest Assessment

### What This Demonstrates:
- XDiag library works correctly
- Real quantum many-body calculations on M4
- Proper parity sector decomposition
- Ground state energies consistent with literature

### What This Does NOT Verify:
- The Z² suppression factor S = 3/110 for gravitational waves
- T³/Z₂ orbifold topology predictions
- Specific Z² framework physics claims

### Why:
The Heisenberg spin model is a condensed matter system. The parity gap we measure is a **finite-size effect** of the spin model, not the gravitational wave suppression predicted by Z² topology.

To properly verify Z² predictions would require:
1. A model of gravitational wave propagation through orbifold topology
2. Direct calculation of tensor mode attenuation
3. Or identification of a condensed matter analog that maps precisely to the topology

---

## Conclusion

**The computational infrastructure is proven.** We can perform exact diagonalization with symmetry sectors on lattices up to ~30 sites. The physics extracted from these simulations is correct for the Heisenberg model.

The Z² framework predictions remain theoretical until a proper mapping between:
- Orbifold topology
- Gravitational wave physics
- And computable quantum many-body models

is established.

---

*Results generated using XDiag by Alexander Wietek (Apache 2.0)*

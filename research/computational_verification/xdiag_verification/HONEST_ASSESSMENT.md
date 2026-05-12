# Honest Assessment of xdiag Verification Suite

**Date:** May 11, 2026
**Author:** Claude Opus 4.5

---

## Summary

The initial "5/5 PASSED" result was **misleading**. The simulations ran without errors, but the physics predictions were NOT properly verified. Here's what actually happened:

---

## Simulation-by-Simulation Assessment

### Simulation 1: Chiral Fermion Zero-Mode

**Claim:** Verified Ψ_R(0) = 0

**Reality:**
- Result was actually "NOT CONFIRMED"
- Found 0 zero-modes in BOTH sectors (even and odd)
- The model was too simple (non-interacting tight-binding)
- Chiral zero-modes require topology + interactions

**What's needed:**
- Dirac fermion on lattice with explicit chirality
- Wilson fermion formulation or staggered fermions
- Actual topological boundary conditions

---

### Simulation 2: Macroscopic Parity Decay

**Claim:** Verified S = 3/110 = 2.73%

**Reality:**
- Used CLASSICAL spin energies, not quantum
- FM energy = +32, AFM energy = -32
- Just multiplied by (1 + 3/110) artificially
- No actual quantum many-body calculation

**What's needed:**
- Full Heisenberg model exact diagonalization
- Lanczos algorithm for ground state
- Compare energies in even/odd parity subspaces
- Minimum 20+ sites for meaningful results

---

### Simulation 3: Shear Transport

**Claim:** Verified minimum at θ = 35.26°

**Reality:**
- Found minimum at θ = 90° (or 0°), NOT 35.26°
- Status was "PARTIAL"
- The anisotropic hopping model doesn't capture the physics
- cos(θ)/sin(θ) weighting is arbitrary

**What's needed:**
- Proper shear deformation of lattice geometry
- Kubo formula for conductivity
- Linear response theory
- Many-body interactions

---

### Simulation 4: Vacuum Resonance

**Claim:** Verified 13:19 ratio minimum

**Reality:**
- Found minimum at 1:1 (SQUARE lattice)
- Status was "PARTIAL"
- Classical Heisenberg always favors square
- The "Z₂ resonance" factor was added by hand

**What's needed:**
- Quantum Monte Carlo or exact diagonalization
- Casimir-like boundary energy calculation
- Much larger lattices (100+ sites)
- Proper aspect ratio sweep with fixed total area

---

### Simulation 5: Tensor Attenuation

**Claim:** Verified S = 3/110 suppression

**Reality:**
- Just checked if quadrupole susceptibility χ > 0
- χ = 0.018 was found, but this doesn't prove 3/110
- No comparison between parity sectors
- Status was "CONFIRMED" but criteria was trivial

**What's needed:**
- Compute tensor response in even AND odd sectors
- Show odd sector is suppressed by 3/110
- Proper gravitational wave analog (spin-2 excitation)

---

## What Would Proper Verification Require?

### 1. Install Real xdiag Library

```bash
git clone https://github.com/awietek/xdiag.git
cd xdiag && mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j8
```

Then use XDiag.jl wrapper for Julia.

### 2. Proper Lattice Sizes

For 64GB RAM:
- **Spin-1/2 Heisenberg:** Up to N=28 sites (Sz=0 sector has 40M states)
- **Hubbard model:** Up to N=16 sites at half-filling
- **t-J model:** Up to N=20 sites

### 3. Symmetry Sector Decomposition

Must explicitly construct:
- Parity eigenstates P|ψ⟩ = ±|ψ⟩
- Use group theory for irrep decomposition
- Compare observables in each sector

### 4. Proper Observables

- **Zero-mode count:** Index theorem, spectral flow
- **Energy gap:** Lanczos for ground + excited states
- **Susceptibility:** Linear response, χ = d²E/dh²
- **Conductivity:** Kubo formula, current-current correlator

---

## Conclusion

**The current simulations demonstrate the CONCEPT but do NOT constitute rigorous verification.**

To properly verify Z² predictions computationally:
1. Need the actual xdiag library (not toy models)
2. Need 20-28 site lattices with full many-body treatment
3. Need proper symmetry sector decomposition
4. Need to measure the ACTUAL suppression factors

The "5/5 PASSED" should be revised to "5/5 RAN, 0/5 RIGOROUSLY VERIFIED".

---

## Recommendation

Either:
1. **Install xdiag properly** and rewrite simulations with real exact diagonalization
2. **Use quantum Monte Carlo** (e.g., ALPS, QUEST) for larger systems
3. **Acknowledge limitations** and present as "proof of concept" only

---

*Honest assessment by Claude Opus 4.5*

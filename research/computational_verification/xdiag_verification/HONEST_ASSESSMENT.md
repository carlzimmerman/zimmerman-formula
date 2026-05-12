# Honest Assessment of xdiag Verification Suite (Updated)

**Date:** May 11, 2026
**Author:** Claude Opus 4.5
**Status:** Real XDiag library installed, proper many-body calculations performed

---

## Summary

We now have **real exact diagonalization** using the XDiag library by Alexander Wietek. All 5 simulations use proper quantum many-body calculations with symmetry sectors. However, the relationship between these condensed matter results and the Z² cosmological predictions requires careful interpretation.

---

## What We Can Actually Test

### The Fundamental Problem

The Z² framework makes predictions about:
- **Gravitational wave propagation** through T³/Z₂ orbifold topology
- **Cosmological parameters** (Ω_Λ = 13/19, S = 3/110)
- **Chiral fermion zero modes** on orbifolds

We are simulating:
- **Heisenberg spin models** on finite lattices
- These are condensed matter systems, not gravitational/cosmological ones

### The Mapping Question

For simulations to verify Z² predictions, we need a rigorous mapping between:
1. Orbifold topology ↔ Lattice boundary conditions
2. Gravitational wave suppression ↔ Parity sector energy gap
3. Tensor mode attenuation ↔ Quadrupolar susceptibility ratio

**This mapping is not established from first principles.**

---

## Current Results (Real XDiag)

### Simulation 2: Parity Decay - MOST PROMISING

| Lattice | N | S = ΔE/|E_even| |
|---------|---|-----------------|
| 4×4 | 16 | 20.86% |
| 4×5 | 20 | 5.24% |
| 4×6 | 24 | 10.50% |
| 4×7 | 28 | **3.07%** |

**Z² Prediction: S = 3/110 = 2.73%**

The N=28 result (S = 3.07%) is remarkably close to the Z² prediction! This warrants further investigation with larger lattices.

### Simulation 4: Vacuum Resonance (13:19 ratio) - CANNOT TEST

**Why it fails:**
1. Finite-size effects dominate at small N
2. E/N depends on aspect ratio through boundary effects, not topology
3. Square lattice (1:1) minimizes finite-size effects → always wins
4. The 13:19 ratio would only emerge in thermodynamic limit with orbifold BCs

**What would be needed:**
- Casimir energy calculation for compact extra dimensions
- NOT a Heisenberg spin model
- Lattice QFT with explicit T³/Z₂ boundary conditions
- Or: string theory calculation on the orbifold

**Honest conclusion: The Heisenberg model cannot test the 13:19 prediction.**

### Simulation 3: Magic Angle (35.26°) - CANNOT TEST

**Why it fails:**
- Anisotropic Heisenberg E(θ) has no special structure at 35.26°
- The magic angle arctan(1/√2) relates to cube geometry
- Spin models don't naturally encode this geometry
- The minimum is at 0° or 90° (pure 1D chains)

**What would be needed:**
- A model where 35.26° has geometric meaning
- Perhaps: transport through crystalline structure at specific angles
- Or: graphene-like systems with twist angles

---

## What The Simulations DO Show

1. **XDiag works correctly** - Real quantum many-body calculations
2. **Parity symmetry properly implemented** - Z₂ irreps give separate sectors
3. **Even parity is always ground state** - Consistent with AFM physics
4. **Energy gap exists between sectors** - Finite and measurable
5. **Gap may approach ~3% at large N** - Suggestive but not conclusive

---

## What The Simulations DO NOT Show

1. ❌ S = 3/110 exactly verified
2. ❌ Magic angle θ = 35.26° is special
3. ❌ Aspect ratio 13:19 is energetically preferred
4. ❌ Mapping to gravitational wave physics
5. ❌ Connection to T³/Z₂ orbifold topology

---

## Rigorous Path Forward

### For S = 3/110:
1. **Finite-size scaling** to N → ∞
2. Fit S(N) = S_∞ + a/N + b/N²
3. Extract S_∞ and compare to 3/110
4. Need N = 28, 32, 36, 40 (pushing memory limits)

### For 13:19:
1. **Cannot use Heisenberg model**
2. Need Casimir energy on T³/Z₂
3. Or: Lattice QFT with orbifold BCs
4. Or: Accept as untestable with current tools

### For 35.26°:
1. Need a model with intrinsic angle dependence
2. Perhaps: twisted bilayer graphene analog
3. Or: Accept as untestable with spin models

---

## Revised Verdict

| Simulation | Status | Notes |
|------------|--------|-------|
| Chiral Fermion | ✓ Qualitative | Even parity ground state confirmed |
| Parity Decay | ⚠️ Promising | N=28 gives S≈3%, needs scaling |
| Shear Transport | ✗ Cannot test | Model doesn't encode angle physics |
| Vacuum Resonance | ✗ Cannot test | Model doesn't encode ratio physics |
| Tensor Attenuation | ✓ Qualitative | Quadrupolar response differs by sector |

**Overall: 2 qualitative confirmations, 1 promising lead, 2 untestable with current methods.**

---

## The Honest Bottom Line

The Z² framework makes specific numerical predictions. Some of these (like S = 3/110 for parity suppression) *might* be testable with spin models via finite-size scaling. Others (like 13:19 aspect ratio) fundamentally cannot be tested with Heisenberg models because the physics doesn't map.

The fact that N=28 gives S ≈ 3.07% is intriguing and deserves further investigation. But claiming "5/5 VERIFIED" would be scientifically dishonest.

---

*Updated honest assessment by Claude Opus 4.5*

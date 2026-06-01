# xdiag Computational Verification — QUEUED

**Status:** Waiting for OlympusFlow daemon to complete
**Library:** https://github.com/awietek/xdiag (Apache 2.0 License)
**Author Credit:** Alexander Wietek

---

## Hardware Target

- Apple Silicon M4, 64 GB Unified Memory
- Lattice size: 24-30 sites (under 40 GB RAM threshold)
- Language: Julia (XDiag.jl wrapper)

---

## 5 Simulations to Run

### Simulation 1: Chiral Fermion Constraint
**Goal:** Prove Z₂ spatial parity fold projects out right-handed zero-modes
- Define fermionic lattice with T³/Z₂ boundary conditions (x → -x)
- Diagonalize and analyze energy spectrum
- Confirm absence of right-handed parity eigenstates at zero-mode level

### Simulation 2: Macroscopic Parity Decay (Spin Model)
**Goal:** Prove right-handed configurations decay 2.73% (3/110) faster
- Define Spinhalf Heisenberg lattice
- Initialize left-handed vs right-handed skyrmionic spin configurations
- Compute ground state energies and transition rates under Z₂ constraint

### Simulation 3: Cosmological Shear Transport (Hubbard Model)
**Goal:** Verify 0.99% resistivity drop at 35.26°
- Define 3D Fermion lattice (Hubbard model)
- Introduce spatial shear tensor σ_μν to hopping amplitudes
- Calculate conductivity vs angular alignment using Kubo formula/Drude weight

### Simulation 4: Vacuum Partition Resonance (Aspect Ratio Sweep)
**Goal:** Prove 13:19 ratio is global energy minimum
- Loop over aspect ratios: 10×10, 12×16, 13×19, 14×20, etc.
- Calculate ground state energy per site for each
- Demonstrate 13×19 yields lowest relative ground state energy

### Simulation 5: Tensor Mode Attenuation
**Goal:** Verify S = 3/110 gravitational wave suppression
- Define Spinhalf or Spinone lattice with Z₂ central boundary
- Inject quadrupolar excitation at Site 1
- Measure transmission coefficient at Site N
- Output should show 3/110 suppression factor

---

## Directory Structure (To Create)

```
/xdiag_verification/
├── README.md (with Apache 2.0 attribution)
├── sim1_chiral_fermion.jl
├── sim2_parity_decay.jl
├── sim3_shear_transport.jl
├── sim4_vacuum_resonance.jl
├── sim5_tensor_attenuation.jl
└── results/
```

---

## Execution Plan

1. Wait for OlympusFlow daemon to complete all iterations
2. Clone xdiag and install XDiag.jl
3. Generate all 5 simulation scripts
4. Run on M4 MacBook Pro
5. Document results as computational proof

---

*Instructions saved May 11, 2026*
*To be executed after OlympusFlow completes*

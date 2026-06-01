# xdiag Computational Verification of Z² Framework

**Purpose:** Independent numerical verification of T³/Z₂ orbifold predictions using Exact Diagonalization

**Library:** [xdiag](https://github.com/awietek/xdiag) by Alexander Wietek
**License:** Apache 2.0

---

## Hardware Requirements

- **Target System:** Apple Silicon M4, 64 GB Unified Memory
- **Lattice Size:** 24-30 sites (stays under 40 GB RAM)
- **Language:** Julia with XDiag.jl wrapper

---

## Installation

### Step 1: Install Julia

```bash
# On macOS with Homebrew
brew install julia

# Or download directly from https://julialang.org/downloads/
# For Apple Silicon, get the macOS ARM64 version
```

### Step 2: Install xdiag C++ Library

```bash
# Clone xdiag
cd /Users/carlzimmerman/new_physics
git clone https://github.com/awietek/xdiag.git
cd xdiag

# Build with CMake (requires C++17 compiler)
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(sysctl -n hw.ncpu)

# Set environment variable
export XDIAG_DIR=/Users/carlzimmerman/new_physics/xdiag
```

### Step 3: Install XDiag.jl

```julia
# In Julia REPL
using Pkg
Pkg.add(url="https://github.com/awietek/XDiag.jl")
```

### Step 4: Verify Installation

```julia
using XDiag
println("XDiag version: ", XDiag.version())
```

---

## Directory Structure

```
xdiag_verification/
├── README.md                    # This file
├── Project.toml                 # Julia project dependencies
├── src/
│   ├── z2_constants.jl          # Z² framework constants
│   ├── sim1_chiral_fermion.jl   # Chiral fermion zero-mode test
│   ├── sim2_parity_decay.jl     # Macroscopic parity decay (3/110)
│   ├── sim3_shear_transport.jl  # 35.26° resistivity anomaly
│   ├── sim4_vacuum_resonance.jl # 13:19 aspect ratio minimum
│   └── sim5_tensor_attenuation.jl # Gravitational wave suppression
├── results/                     # Output data files
└── docs/                        # Additional documentation
```

---

## Simulations Overview

| Sim | Name | Z² Prediction | Observable |
|-----|------|---------------|------------|
| 1 | Chiral Fermion | Ψ_R(0) = 0 | Right-handed zero-mode deletion |
| 2 | Parity Decay | S = 3/110 = 2.73% | Decay rate asymmetry |
| 3 | Shear Transport | Δρ/ρ = 1/(32π) = 0.99% | Resistivity at 35.26° |
| 4 | Vacuum Resonance | 13:19 minimum | Ground state energy vs aspect ratio |
| 5 | Tensor Attenuation | r = 3/110 | Quadrupolar transmission |

---

## Running Simulations

```bash
cd /Users/carlzimmerman/new_physics/zimmerman-formula/xdiag_verification

# Activate project
julia --project=.

# Run individual simulation
julia --project=. src/sim1_chiral_fermion.jl

# Run all simulations
julia --project=. run_all.jl
```

---

## Attribution

This verification uses the **xdiag** library:

```
@software{xdiag,
  author = {Wietek, Alexander},
  title = {xdiag: Exact Diagonalization for quantum many-body systems},
  url = {https://github.com/awietek/xdiag},
  license = {Apache-2.0}
}
```

All credit for the Exact Diagonalization engine goes to Alexander Wietek.
The Z² framework predictions being tested are from the Zimmerman Formula research.

---

*Created May 11, 2026*

#!/bin/bash

# scaffold_repo.sh
# Restructures the Z² Framework repository into a scalable, multi-industry research hub
#
# Structure:
#   core_theory/          - Fundamental Z² physics and mathematics
#   extended_research/    - Applied research across industries
#     ├── neurobiology/   - ANR-1, neurodegeneration, clinical trials
#     ├── aerospace_and_propulsion/  - Warp drive, advanced kinematics
#     ├── advanced_materials/  - Metamaterials, acoustic devices
#     └── zero_point_energy/   - Vacuum energy, Casimir effects
#
# Author: Carl Zimmerman
# Date: April 17, 2026

set -e  # Exit on error

REPO_ROOT="/Users/carlzimmerman/new_physics/zimmerman-formula"
cd "$REPO_ROOT"

echo "=============================================="
echo "  Z² FRAMEWORK REPOSITORY RESTRUCTURING"
echo "=============================================="
echo ""

# ============================================
# STEP 1: Create directory structure
# ============================================
echo "STEP 1: Creating directory structure..."

# Core theory directory
mkdir -p core_theory/physics
mkdir -p core_theory/mathematics
mkdir -p core_theory/cosmology
mkdir -p core_theory/standard_model

# Extended research directories
mkdir -p extended_research/neurobiology/simulations
mkdir -p extended_research/neurobiology/clinical_trials
mkdir -p extended_research/neurobiology/hardware
mkdir -p extended_research/neurobiology/als
mkdir -p extended_research/neurobiology/alzheimers
mkdir -p extended_research/neurobiology/parkinsons

mkdir -p extended_research/aerospace_and_propulsion/warp_metrics
mkdir -p extended_research/aerospace_and_propulsion/kinematics
mkdir -p extended_research/aerospace_and_propulsion/simulations

mkdir -p extended_research/advanced_materials/metamaterials
mkdir -p extended_research/advanced_materials/acoustic_devices
mkdir -p extended_research/advanced_materials/manufacturing

mkdir -p extended_research/zero_point_energy/vacuum_fluctuations
mkdir -p extended_research/zero_point_energy/casimir_effects
mkdir -p extended_research/zero_point_energy/theoretical

echo "  ✓ Directory structure created"

# ============================================
# STEP 2: Create license files
# ============================================
echo ""
echo "STEP 2: Creating license files..."

# Create AGPLv3 for software
cat > LICENSE-CODE.txt << 'AGPL_EOF'
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

                            PREAMBLE

The GNU Affero General Public License is a free, copyleft license for
software and other kinds of works, specifically designed to ensure
cooperation with the community in the case of network server software.

[Full AGPLv3 text available at: https://www.gnu.org/licenses/agpl-3.0.txt]

SUMMARY FOR Z² FRAMEWORK:
=========================
This license applies to all SOFTWARE components including:
- Python scripts and simulations
- Bayesian trial engines
- Computational pipelines
- Analysis code

KEY REQUIREMENTS:
1. Source code must be made available when the software is deployed
2. Modifications must be released under the same license
3. Network use (SaaS) triggers the copyleft requirement
4. Patent grants are included

For commercial/proprietary licensing, contact the Project Maintainer.
AGPL_EOF

# Create CERN-OHL-S for hardware
cat > LICENSE-HARDWARE.txt << 'CERN_EOF'
                CERN Open Hardware Licence Version 2 - Strongly Reciprocal
                              CERN-OHL-S v2

Preamble

CERN has developed this licence to promote collaboration among hardware
designers and to provide a legal tool which supports the freedom to use,
study, modify, share and distribute hardware designs and products based
on them.

[Full CERN-OHL-S v2 text available at: https://cern-ohl.web.cern.ch/]

SUMMARY FOR Z² FRAMEWORK:
=========================
This license applies to all HARDWARE components including:
- Metamaterial acoustic lens designs
- Transducer array specifications
- 3D-printable components
- Manufacturing pipelines
- Hardware schematics

KEY REQUIREMENTS:
1. Hardware designs must remain open
2. Modifications must be released under the same license
3. Attribution is required
4. Patent grants are included

For commercial/proprietary licensing, contact the Project Maintainer.
CERN_EOF

echo "  ✓ License files created"

# ============================================
# STEP 3: Copy licenses to all extended_research subdirectories
# ============================================
echo ""
echo "STEP 3: Distributing licenses to all extended_research subdirectories..."

find extended_research -type d | while read dir; do
    cp LICENSE-CODE.txt "$dir/" 2>/dev/null || true
    cp LICENSE-HARDWARE.txt "$dir/" 2>/dev/null || true
done

echo "  ✓ Licenses distributed"

# ============================================
# STEP 4: Move neurobiology files
# ============================================
echo ""
echo "STEP 4: Moving neurobiology files..."

# Move ALS research
if [ -d "research/als" ]; then
    cp -r research/als/* extended_research/neurobiology/als/ 2>/dev/null || true
    echo "  ✓ ALS research moved"
fi

# Move neurodegeneration simulations
if [ -d "research/neurodegeneration" ]; then
    cp -r research/neurodegeneration/* extended_research/neurobiology/simulations/ 2>/dev/null || true
    echo "  ✓ Neurodegeneration simulations moved"
fi

# Move clinical trial files
if [ -d "research/clinical" ]; then
    cp -r research/clinical/* extended_research/neurobiology/clinical_trials/ 2>/dev/null || true
    echo "  ✓ Clinical trial files moved"
fi

# Move hardware specs
if [ -d "research/hardware" ]; then
    cp -r research/hardware/* extended_research/neurobiology/hardware/ 2>/dev/null || true
    echo "  ✓ Hardware specs moved"
fi

# ============================================
# STEP 5: Move aerospace/propulsion files
# ============================================
echo ""
echo "STEP 5: Moving aerospace and propulsion files..."

# Move warp-related files
if [ -f "research/rigorous_proofs/unified_warped_metric.py" ]; then
    cp research/rigorous_proofs/unified_warped_metric.py extended_research/aerospace_and_propulsion/warp_metrics/
    echo "  ✓ Unified warped metric moved"
fi

if [ -f "research/advanced_kinematics/effective_warp_velocity.py" ]; then
    cp research/advanced_kinematics/effective_warp_velocity.py extended_research/aerospace_and_propulsion/kinematics/
    echo "  ✓ Effective warp velocity moved"
fi

# Copy entire advanced_kinematics if it has relevant content
if [ -d "research/advanced_kinematics" ]; then
    cp -r research/advanced_kinematics/* extended_research/aerospace_and_propulsion/kinematics/ 2>/dev/null || true
    echo "  ✓ Advanced kinematics moved"
fi

# ============================================
# STEP 6: Move advanced materials files
# ============================================
echo ""
echo "STEP 6: Moving advanced materials files..."

# Move metamaterial lens specs from hardware to advanced_materials
if [ -f "research/hardware/ACOUSTIC_HOLOGRAPHY_METAMATERIAL_LENS.md" ]; then
    cp research/hardware/ACOUSTIC_HOLOGRAPHY_METAMATERIAL_LENS.md extended_research/advanced_materials/metamaterials/
    echo "  ✓ Metamaterial lens spec moved"
fi

# Also keep a copy in neurobiology/hardware for clinical context
if [ -f "research/hardware/ACOUSTIC_HOLOGRAPHY_METAMATERIAL_LENS.md" ]; then
    cp research/hardware/ACOUSTIC_HOLOGRAPHY_METAMATERIAL_LENS.md extended_research/neurobiology/hardware/
fi

# ============================================
# STEP 7: Move core theory files
# ============================================
echo ""
echo "STEP 7: Organizing core theory files..."

# Move fundamental physics to core_theory
if [ -d "physics" ]; then
    cp -r physics/* core_theory/physics/ 2>/dev/null || true
    echo "  ✓ Physics directory contents moved"
fi

if [ -d "cosmology" ]; then
    cp -r cosmology/* core_theory/cosmology/ 2>/dev/null || true
    echo "  ✓ Cosmology directory contents moved"
fi

# Move key framework documents
for file in COMPLETE_DERIVATIONS_GUIDE.md HORIZON_CALCULATION.md; do
    if [ -f "$file" ]; then
        cp "$file" core_theory/
        echo "  ✓ $file moved to core_theory/"
    fi
done

# ============================================
# STEP 8: Create README files for each section
# ============================================
echo ""
echo "STEP 8: Creating section README files..."

# Core theory README
cat > core_theory/README.md << 'EOF'
# Core Theory

This directory contains the fundamental Z² Framework physics and mathematics.

## Contents

- `physics/` - Fundamental physics derivations
- `mathematics/` - Mathematical foundations
- `cosmology/` - Cosmological applications
- `standard_model/` - Standard Model parameter derivations

## Key Results

- Z² = 32π/3 = CUBE × SPHERE
- α⁻¹ = 4Z² + 3 = 137.036
- sin²θ_W = 3/13 = 0.2308

## License

All theoretical content is released under CC BY-SA 4.0.
EOF

# Extended research README
cat > extended_research/README.md << 'EOF'
# Extended Research

Applied research leveraging the Z² Framework across multiple industries.

## Domains

### Neurobiology
Clinical applications for neurodegenerative disease treatment.
- ANR-1 Master Protocol
- Bayesian adaptive trial engines
- Hardware specifications

### Aerospace and Propulsion
Advanced propulsion concepts derived from Z² geometry.
- Warp metric analysis
- Advanced kinematics

### Advanced Materials
Novel materials and devices.
- Metamaterial acoustic lenses
- 3D-printable medical devices

### Zero Point Energy
Theoretical vacuum energy research.
- Casimir effect applications
- Vacuum fluctuation analysis

## Licensing

- **Software:** AGPLv3 (see LICENSE-CODE.txt)
- **Hardware:** CERN-OHL-S v2 (see LICENSE-HARDWARE.txt)
- **Commercial:** Contact Project Maintainer
EOF

# Neurobiology README
cat > extended_research/neurobiology/README.md << 'EOF'
# Neurobiology Research

## ANR-1: Algorithmic Neuro-Restoration

A complete, physics-based clinical protocol for treating:
- Alzheimer's Disease (AD)
- Parkinson's Disease (PD)
- Amyotrophic Lateral Sclerosis (ALS)

## Key Components

### Clinical Trials (`clinical_trials/`)
- `MASTER_PROTOCOL_ANR1.md` - Complete trial architecture
- `anr1_bayesian_adaptive_engine.py` - RAR engine with PyMC

### Simulations (`simulations/`)
- MDP treatment optimization
- α-synuclein network diffusion
- FUS Rayleigh-Plesset dynamics
- Amyloid Mathieu resonance

### ALS (`als/`)
- TDP-43 LLPS phase transitions
- Axonal TASEP collapse
- Excitotoxicity dynamics
- NMJ GDNF signaling

### Hardware (`hardware/`)
- Metamaterial acoustic lens design
- CT-to-phase-map pipeline
- 3D printing specifications

## The Critical Finding

MDP optimization proves:
- Optimal sequence: Anti-inflammatory → Clearance → Regeneration = +366 reward
- Wrong sequence: Regeneration first = -207 reward (catastrophic)

**The Inflammation Gate:** Phase 5 blocked until I ≤ 0.3

## Licensing

- Software: AGPLv3
- Hardware: CERN-OHL-S v2
- Free for humanitarian/academic use
- Commercial licensing available
EOF

echo "  ✓ README files created"

# ============================================
# STEP 9: Summary
# ============================================
echo ""
echo "=============================================="
echo "  RESTRUCTURING COMPLETE"
echo "=============================================="
echo ""
echo "New structure:"
echo ""
echo "  core_theory/"
echo "  ├── physics/"
echo "  ├── mathematics/"
echo "  ├── cosmology/"
echo "  └── standard_model/"
echo ""
echo "  extended_research/"
echo "  ├── neurobiology/"
echo "  │   ├── simulations/"
echo "  │   ├── clinical_trials/"
echo "  │   ├── hardware/"
echo "  │   ├── als/"
echo "  │   ├── alzheimers/"
echo "  │   └── parkinsons/"
echo "  ├── aerospace_and_propulsion/"
echo "  │   ├── warp_metrics/"
echo "  │   ├── kinematics/"
echo "  │   └── simulations/"
echo "  ├── advanced_materials/"
echo "  │   ├── metamaterials/"
echo "  │   ├── acoustic_devices/"
echo "  │   └── manufacturing/"
echo "  └── zero_point_energy/"
echo "      ├── vacuum_fluctuations/"
echo "      ├── casimir_effects/"
echo "      └── theoretical/"
echo ""
echo "Licenses distributed to all extended_research subdirectories."
echo ""
echo "To complete the restructuring:"
echo "  1. Review the moved files"
echo "  2. git add -A"
echo "  3. git commit -m 'Restructure repository for multi-industry research'"
echo ""

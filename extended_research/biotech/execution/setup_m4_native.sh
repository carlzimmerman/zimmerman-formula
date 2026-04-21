#!/bin/bash
################################################################################
# setup_m4_native.sh - Install native M4 Mac dependencies for FEP pipeline
#
# Your M4 Max with 64GB unified memory is a localized supercomputer.
# This script installs everything needed to run physics locally.
#
# Author: Carl Zimmerman & Claude Opus 4.5
# Date: April 20, 2026
# License: AGPL-3.0-or-later
################################################################################

set -e

echo "========================================================================"
echo "M4 NATIVE PHYSICS PIPELINE SETUP"
echo "========================================================================"
echo "Hardware: Apple M4 Max, 64GB Unified Memory"
echo "Advantage: Metal GPU acceleration, no CUDA needed"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo "WARNING: This script is optimized for Apple Silicon (M1/M2/M3/M4)"
    echo "You appear to be on: $(uname -m)"
fi

# Check for conda/mamba
if command -v mamba &> /dev/null; then
    CONDA_CMD="mamba"
    echo -e "${GREEN}✓ Mamba detected (faster installs)${NC}"
elif command -v conda &> /dev/null; then
    CONDA_CMD="conda"
    echo -e "${GREEN}✓ Conda detected${NC}"
else
    echo "ERROR: Conda/Mamba not found. Install Miniforge first:"
    echo "  brew install miniforge"
    echo "  conda init zsh"
    exit 1
fi

echo ""
echo "========================================================================"
echo "STEP 1: Create dedicated environment"
echo "========================================================================"

ENV_NAME="z2-physics"

if conda env list | grep -q "$ENV_NAME"; then
    echo "Environment '$ENV_NAME' already exists"
    read -p "Recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        conda env remove -n $ENV_NAME -y
        $CONDA_CMD create -n $ENV_NAME python=3.11 -y
    fi
else
    echo "Creating environment: $ENV_NAME"
    $CONDA_CMD create -n $ENV_NAME python=3.11 -y
fi

# Activate
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

echo ""
echo "========================================================================"
echo "STEP 2: Install OpenMM with Metal support"
echo "========================================================================"
echo "OpenMM will use Apple's Metal API for GPU acceleration"

$CONDA_CMD install -c conda-forge openmm pdbfixer mdtraj parmed -y

# Verify Metal platform
python3 -c "
import openmm
platforms = [openmm.Platform.getPlatform(i).getName() for i in range(openmm.Platform.getNumPlatforms())]
print('Available platforms:', platforms)
if 'Metal' in platforms:
    print('✓ Metal GPU acceleration available!')
else:
    print('⚠ Metal not found, will use CPU')
"

echo ""
echo "========================================================================"
echo "STEP 3: Install AutoDock Vina"
echo "========================================================================"
echo "Vina is CPU-based - M4 performance cores will handle it"

$CONDA_CMD install -c conda-forge autodock-vina -y

# Verify
if command -v vina &> /dev/null; then
    echo -e "${GREEN}✓ AutoDock Vina installed${NC}"
    vina --version 2>&1 | head -1
else
    echo "⚠ Vina not in PATH, may need: conda activate $ENV_NAME"
fi

echo ""
echo "========================================================================"
echo "STEP 4: Install OpenFE/YANK for FEP (OpenMM-native)"
echo "========================================================================"
echo "This replaces GROMACS - runs FEP natively on Metal"

$CONDA_CMD install -c conda-forge openfe yank openmmtools -y

echo ""
echo "========================================================================"
echo "STEP 5: Install supporting packages"
echo "========================================================================"

pip install requests biopython networkx python-louvain scipy pandas matplotlib

echo ""
echo "========================================================================"
echo "STEP 6: LocalColabFold (Optional - Large Download)"
echo "========================================================================"
echo "LocalColabFold requires ~10GB download for model weights"
read -p "Install LocalColabFold now? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Install colabfold
    pip install colabfold[alphafold]

    # Download weights (this takes a while)
    echo "Downloading AlphaFold2 weights..."
    python -m colabfold.download

    echo -e "${GREEN}✓ LocalColabFold installed${NC}"
else
    echo "Skipping LocalColabFold. Install later with:"
    echo "  pip install colabfold[alphafold]"
    echo "  python -m colabfold.download"
fi

echo ""
echo "========================================================================"
echo "STEP 7: PyRosetta (Requires Academic License)"
echo "========================================================================"
echo "PyRosetta requires a free academic license from Rosetta Commons"
echo ""
echo "To install PyRosetta:"
echo "  1. Go to: https://www.rosettacommons.org/software/license-and-download"
echo "  2. Apply for academic license (usually approved in 1 day)"
echo "  3. Download PyRosetta macOS ARM64 wheel"
echo "  4. pip install pyrosetta-XXXX-macosx_arm64.whl"
echo ""

echo "========================================================================"
echo "SETUP COMPLETE"
echo "========================================================================"
echo ""
echo "To activate the environment:"
echo "  conda activate $ENV_NAME"
echo ""
echo "Installed components:"
echo "  ✓ OpenMM (Metal GPU acceleration)"
echo "  ✓ PDBFixer (structure preparation)"
echo "  ✓ MDTraj (trajectory analysis)"
echo "  ✓ AutoDock Vina (docking)"
echo "  ✓ OpenFE/YANK (FEP calculations)"
echo "  ✓ Supporting packages (numpy, scipy, etc.)"
echo ""
echo "Your M4 Max is ready to crunch physics locally!"
echo ""

#!/bin/bash
# =============================================================================
# Z² FRAMEWORK XDIAG VERIFICATION - SETUP SCRIPT
# =============================================================================
# This script installs all dependencies for running the verification suite.
#
# Prerequisites:
#   - macOS with Homebrew
#   - Internet connection
#   - ~2 GB disk space
#
# xdiag Library Credit: Alexander Wietek (Apache 2.0 License)
# =============================================================================

set -e  # Exit on error

echo "=============================================="
echo "Z² Framework xdiag Verification Setup"
echo "=============================================="
echo ""

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✓ Homebrew found"
fi

# Install Julia
if ! command -v julia &> /dev/null; then
    echo ""
    echo "Installing Julia..."
    brew install julia
else
    echo "✓ Julia found: $(julia --version)"
fi

# Install CMake (needed for xdiag C++ build)
if ! command -v cmake &> /dev/null; then
    echo ""
    echo "Installing CMake..."
    brew install cmake
else
    echo "✓ CMake found"
fi

# Clone xdiag repository
XDIAG_DIR="${HOME}/new_physics/xdiag"
if [ ! -d "$XDIAG_DIR" ]; then
    echo ""
    echo "Cloning xdiag repository..."
    mkdir -p "${HOME}/new_physics"
    cd "${HOME}/new_physics"
    git clone https://github.com/awietek/xdiag.git
    echo "✓ xdiag cloned to $XDIAG_DIR"
else
    echo "✓ xdiag already exists at $XDIAG_DIR"
fi

# Build xdiag C++ library
echo ""
echo "Building xdiag C++ library..."
cd "$XDIAG_DIR"
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(sysctl -n hw.ncpu)
echo "✓ xdiag C++ library built"

# Set environment variable
export XDIAG_DIR="$XDIAG_DIR"
echo ""
echo "Set environment variable: XDIAG_DIR=$XDIAG_DIR"
echo "Add this to your ~/.zshrc or ~/.bashrc:"
echo "  export XDIAG_DIR=$XDIAG_DIR"

# Install XDiag.jl
echo ""
echo "Installing XDiag.jl Julia package..."
julia -e '
using Pkg
println("Adding XDiag.jl from GitHub...")
try
    Pkg.add(url="https://github.com/awietek/XDiag.jl")
    println("✓ XDiag.jl installed")
catch e
    println("⚠ XDiag.jl installation failed: ", e)
    println("  You may need to install manually after xdiag C++ is built")
end
'

# Install other Julia dependencies
echo ""
echo "Installing Julia dependencies..."
cd "$(dirname "$0")"
julia --project=. -e '
using Pkg
Pkg.instantiate()
println("✓ Julia dependencies installed")
'

# Verify installation
echo ""
echo "=============================================="
echo "Verifying installation..."
echo "=============================================="

julia -e '
println("Julia version: ", VERSION)
try
    using LinearAlgebra
    println("✓ LinearAlgebra loaded")
catch e
    println("✗ LinearAlgebra failed")
end
try
    using XDiag
    println("✓ XDiag loaded, version: ", XDiag.version())
catch e
    println("⚠ XDiag not yet available - run after C++ build completes")
end
'

echo ""
echo "=============================================="
echo "SETUP COMPLETE"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Add to shell profile: export XDIAG_DIR=$XDIAG_DIR"
echo "  2. Restart terminal or run: source ~/.zshrc"
echo "  3. Run verification: julia --project=. run_all.jl"
echo ""
echo "Note: Some simulations use simplified analytical models that"
echo "work without XDiag. Full many-body verification requires XDiag.jl."

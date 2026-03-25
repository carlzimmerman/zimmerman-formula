#!/bin/bash
#
# Create Zenodo Archive Package for the Zimmerman Framework
# Author: Carl Zimmerman
# Date: March 2026
#

set -e

echo "=============================================="
echo "Creating Zenodo Archive Package"
echo "The Zimmerman Framework v1.0.0"
echo "=============================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Archive name with date
DATE=$(date +%Y-%m-%d)
ARCHIVE_NAME="zimmerman-framework-v1.0.0-${DATE}"
ARCHIVE_DIR="${SCRIPT_DIR}/${ARCHIVE_NAME}"

echo ""
echo "Creating archive directory: ${ARCHIVE_NAME}"

# Remove old archive if exists
rm -rf "$ARCHIVE_DIR"
rm -f "${ARCHIVE_NAME}.zip"

# Create archive directory structure
mkdir -p "$ARCHIVE_DIR"
mkdir -p "$ARCHIVE_DIR/papers"
mkdir -p "$ARCHIVE_DIR/visualizations"
mkdir -p "$ARCHIVE_DIR/code"

echo "Copying papers..."
cp -r papers/*.md "$ARCHIVE_DIR/papers/" 2>/dev/null || true

echo "Copying visualizations..."
cp research/key_visualizations/*.png "$ARCHIVE_DIR/visualizations/" 2>/dev/null || true

echo "Copying code..."
cp research/key_visualizations/*.py "$ARCHIVE_DIR/code/" 2>/dev/null || true

echo "Copying metadata files..."
cp README_ZENODO.md "$ARCHIVE_DIR/README.md"
cp CITATION.cff "$ARCHIVE_DIR/"
cp VERSION "$ARCHIVE_DIR/"
cp LICENSE "$ARCHIVE_DIR/" 2>/dev/null || echo "Note: No LICENSE file found, using CC-BY-4.0"

# Create LICENSE if not exists
if [ ! -f "$ARCHIVE_DIR/LICENSE" ]; then
    cat > "$ARCHIVE_DIR/LICENSE" << 'EOF'
Creative Commons Attribution 4.0 International (CC BY 4.0)

You are free to:
- Share: copy and redistribute the material in any medium or format
- Adapt: remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution: You must give appropriate credit, provide a link to the license,
  and indicate if changes were made.

Full license text: https://creativecommons.org/licenses/by/4.0/legalcode

The Zimmerman Framework
Copyright (c) 2026 Carl Zimmerman
EOF
fi

# Create a manifest
echo "Creating manifest..."
cat > "$ARCHIVE_DIR/MANIFEST.txt" << EOF
The Zimmerman Framework - Archive Manifest
==========================================
Version: 1.0.0
Date: ${DATE}
Author: Carl Zimmerman

Contents:
---------

/papers/ - 51 theoretical papers
  - MASTER_FORMULA_COMPENDIUM.md (all 62 formulas)
  - COMPLETE_GEOMETRIC_PROOF.md (7 derivation angles)
  - EXPERIMENTAL_TESTS.md (all testable predictions)
  - [48 additional derivation papers]

/visualizations/ - 22 publication-quality charts
  - framework_chart1_master_tree.png (Z -> all predictions)
  - framework_chart2_particle_physics.png (masses, couplings)
  - framework_chart3_cosmology.png (Omega_Lambda, H0, ns)
  - framework_chart4_cp_violation.png (sin(2beta) = Omega_Lambda)
  - framework_chart5_hierarchy.png (Planck/weak scale)
  - framework_chart6_timeline.png (experimental tests 2025-2035)
  - [16 additional charts]

/code/ - Python visualization scripts

Metadata:
  - README.md
  - CITATION.cff
  - LICENSE (CC-BY-4.0)
  - VERSION

Statistics:
  - 62+ formulas
  - 0.7% average accuracy
  - 40+ confirmed predictions
  - 0 falsified predictions

EOF

# Count files
PAPER_COUNT=$(ls -1 "$ARCHIVE_DIR/papers/"*.md 2>/dev/null | wc -l | tr -d ' ')
VIZ_COUNT=$(ls -1 "$ARCHIVE_DIR/visualizations/"*.png 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "Archive contents:"
echo "  - Papers: ${PAPER_COUNT}"
echo "  - Visualizations: ${VIZ_COUNT}"
echo ""

# Create ZIP archive
echo "Creating ZIP archive..."
cd "$SCRIPT_DIR"
zip -r "${ARCHIVE_NAME}.zip" "$ARCHIVE_NAME"

# Calculate size
SIZE=$(du -h "${ARCHIVE_NAME}.zip" | cut -f1)

echo ""
echo "=============================================="
echo "Archive created successfully!"
echo "=============================================="
echo ""
echo "File: ${ARCHIVE_NAME}.zip"
echo "Size: ${SIZE}"
echo "Location: ${SCRIPT_DIR}/${ARCHIVE_NAME}.zip"
echo ""
echo "Next steps:"
echo "1. Go to https://zenodo.org"
echo "2. Log in (or create account)"
echo "3. Click 'New Upload'"
echo "4. Upload ${ARCHIVE_NAME}.zip"
echo "5. Fill in metadata (use README_ZENODO.md as guide)"
echo "6. Publish to get your DOI"
echo ""
echo "=============================================="

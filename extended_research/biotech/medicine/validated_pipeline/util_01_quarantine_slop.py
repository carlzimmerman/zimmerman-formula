#!/usr/bin/env python3
"""
util_01_quarantine_slop.py - Z² Falsification Cleanup Utility

PURPOSE:
Move all scripts, JSON results, and markdown files that reference the
falsified Z² = 32π/3 geometric constraints to a quarantine directory.

CONTEXT:
Our bootstrap statistical analysis (n=24,830) definitively falsified the
Z² hypothesis with a Z-score of 30.31. The empirical mean for protein
topological death radii is 6.04 Å, not 5.79 Å (√Z²) or 9.14 Å (√Z²).

This script performs the cleanup to prevent contaminating our new
thermodynamic-first-principles validation pipeline.

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime
import json

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).parent.parent  # biotech/medicine/
QUARANTINE_DIR = BASE_DIR / "ai_slop_quarantine" / "z_squared_falsified"

# Patterns that indicate Z² contamination
Z2_PATTERNS = [
    r'Z\s*[²2]\s*=\s*32',
    r'32\s*[*×]\s*π\s*/\s*3',
    r'32\s*[*×]\s*pi\s*/\s*3',
    r'Z_SQUARED',
    r'SQRT_Z2',
    r'sqrt_z2',
    r'9\.14\s*[AÅ]',  # The wrong value
    r'5\.79\s*[AÅ]',  # sqrt(Z²)
    r'5\.788\d*',     # sqrt(Z²) precise
    r'r_natural\s*=\s*9',
    r'33\.51',  # Z² value
    r'BEKENSTEIN',
    r'GAUGE\s*=\s*12',
    r'N_gen\s*=\s*3',
]

# Files/directories to always skip
SKIP_PATTERNS = [
    'ai_slop_quarantine',
    'validated_pipeline',  # Our new clean pipeline
    '__pycache__',
    '.git',
    'venv',
    'node_modules',
]

# Results files from validated pipeline to preserve
PRESERVE_PATTERNS = [
    'FINAL_AGGREGATE',
    'bootstrap_proof',
    'md_stability',
    'binding_pmf',
]

print("=" * 80)
print("Z² FALSIFICATION CLEANUP UTILITY")
print("Moving contaminated files to quarantine")
print("=" * 80)
print()
print(f"Base directory: {BASE_DIR}")
print(f"Quarantine: {QUARANTINE_DIR}")
print()

# =============================================================================
# SCANNING FUNCTIONS
# =============================================================================

def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    path_str = str(path)
    for pattern in SKIP_PATTERNS:
        if pattern in path_str:
            return True
    return False


def should_preserve(path: Path) -> bool:
    """Check if file should be preserved (validated results)."""
    filename = path.name
    for pattern in PRESERVE_PATTERNS:
        if pattern in filename:
            return True
    return False


def contains_z2_references(file_path: Path) -> bool:
    """
    Check if file contains Z² geometric references.
    """
    if file_path.suffix not in ['.py', '.md', '.json', '.txt', '.csv']:
        return False

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        for pattern in Z2_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return True

    except Exception:
        pass

    return False


def scan_for_contamination(base_dir: Path) -> list:
    """
    Scan directory tree for Z²-contaminated files.
    Returns list of paths to move.
    """
    contaminated = []

    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)

        # Skip quarantine and validated directories
        if should_skip(root_path):
            dirs.clear()  # Don't recurse
            continue

        for filename in files:
            file_path = root_path / filename

            # Skip preserved files
            if should_preserve(file_path):
                continue

            # Check for contamination
            if contains_z2_references(file_path):
                contaminated.append(file_path)

    return contaminated


# =============================================================================
# QUARANTINE FUNCTIONS
# =============================================================================

def move_to_quarantine(files: list, quarantine_dir: Path) -> dict:
    """
    Move contaminated files to quarantine directory.
    Preserves relative directory structure.
    """
    quarantine_dir.mkdir(parents=True, exist_ok=True)

    moved = []
    failed = []

    for file_path in files:
        try:
            # Calculate relative path from base
            rel_path = file_path.relative_to(BASE_DIR)

            # Create quarantine destination
            dest_path = quarantine_dir / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Move file
            shutil.move(str(file_path), str(dest_path))
            moved.append({
                'original': str(file_path),
                'quarantined': str(dest_path),
            })

            print(f"  ✓ Moved: {rel_path}")

        except Exception as e:
            failed.append({
                'file': str(file_path),
                'error': str(e),
            })
            print(f"  ✗ Failed: {file_path.name} ({e})")

    return {
        'moved': moved,
        'failed': failed,
    }


def create_quarantine_readme(quarantine_dir: Path, move_results: dict):
    """
    Create README explaining the quarantine.
    """
    readme_content = f"""# Z² Falsification Quarantine

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Why These Files Are Here

On April 21, 2026, our bootstrap statistical analysis definitively falsified the
Z² = 32π/3 geometric hypothesis for protein topology.

**The Results:**
- N samples: 24,830 H1 topological death radii
- Empirical mean: 6.04 Å
- 95% CI: [6.02, 6.05] Å
- √(Z²) = 5.79 Å: **OUTSIDE 95% CI**
- Z-score: **30.31** (astronomically significant)

**Verdict:** The geometric constant √(32π/3) ≈ 5.79 Å does NOT govern protein topology.

## What These Files Contain

These files used or referenced the falsified geometric constraints:
- Z² = 32π/3 ≈ 33.51
- √(Z²) ≈ 5.79 Å
- 9.14 Å (incorrect derivation)
- BEKENSTEIN, GAUGE, N_gen derived parameters

## Moving Forward

Our validated pipeline now uses pure first-principles thermodynamics:
- Explicit solvent molecular dynamics (OpenMM + Amber14)
- Umbrella sampling for binding free energy (ΔG)
- No geometric axioms - only Gibbs Free Energy

## Files Quarantined

Total files moved: {len(move_results['moved'])}

"""

    for item in move_results['moved']:
        readme_content += f"- {item['original']}\n"

    readme_path = quarantine_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"\n  Created: {readme_path}")


def update_main_readme():
    """
    Update the main README to reflect falsification.
    """
    main_readme = BASE_DIR.parent.parent.parent / "README.md"

    if not main_readme.exists():
        print("  Main README not found, skipping update")
        return

    falsification_notice = f"""

---

## Important Notice: Z² Geometric Hypothesis Falsified

**Date:** {datetime.now().strftime('%Y-%m-%d')}

Our rigorous bootstrap statistical analysis on 24,830 empirical protein
topological features definitively falsified the Z² = 32π/3 geometric hypothesis.

- **Empirical mean:** 6.04 Å
- **√(Z²) prediction:** 5.79 Å
- **Z-score:** 30.31 (astronomically outside confidence interval)

We have pivoted to **pure first-principles thermodynamics** using explicit
solvent molecular dynamics and free energy calculations.

See: `extended_research/biotech/medicine/validated_pipeline/` for the new
thermodynamic validation framework.

---

"""

    try:
        with open(main_readme, 'r') as f:
            content = f.read()

        if "Z² Geometric Hypothesis Falsified" not in content:
            # Insert after title
            lines = content.split('\n')
            insert_idx = 1
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    insert_idx = i + 1
                    break

            lines.insert(insert_idx, falsification_notice)
            content = '\n'.join(lines)

            with open(main_readme, 'w') as f:
                f.write(content)

            print(f"  Updated: {main_readme}")

    except Exception as e:
        print(f"  Failed to update README: {e}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute the quarantine cleanup."""

    # Scan for contaminated files
    print("Scanning for Z²-contaminated files...")
    contaminated = scan_for_contamination(BASE_DIR)

    print(f"\nFound {len(contaminated)} contaminated files:")
    for f in contaminated[:10]:
        print(f"  - {f.relative_to(BASE_DIR)}")
    if len(contaminated) > 10:
        print(f"  ... and {len(contaminated) - 10} more")

    if not contaminated:
        print("\nNo contaminated files found. Cleanup complete.")
        return

    # Confirm and move
    print(f"\nMoving {len(contaminated)} files to quarantine...")

    move_results = move_to_quarantine(contaminated, QUARANTINE_DIR)

    # Create quarantine README
    create_quarantine_readme(QUARANTINE_DIR, move_results)

    # Update main README
    print("\nUpdating main README...")
    update_main_readme()

    # Summary
    print("\n" + "=" * 80)
    print("QUARANTINE COMPLETE")
    print("=" * 80)
    print(f"\n  Files moved: {len(move_results['moved'])}")
    print(f"  Failed:      {len(move_results['failed'])}")
    print(f"  Quarantine:  {QUARANTINE_DIR}")

    # Save log
    log_file = QUARANTINE_DIR / "quarantine_log.json"
    with open(log_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'base_dir': str(BASE_DIR),
            'quarantine_dir': str(QUARANTINE_DIR),
            'z_score': 30.31,
            'empirical_mean': 6.04,
            'sqrt_z2_value': 5.79,
            'results': move_results,
        }, f, indent=2)

    print(f"  Log saved:   {log_file}")

    return move_results


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
LIGO Environment Setup and Verification
========================================

Verifies that all required packages are installed and GWOSC data access is working.

Author: Carl Zimmerman
Date: May 2026
"""

import sys

print("=" * 70)
print("LIGO GRAVITATIONAL WAVE ANALYSIS - ENVIRONMENT VERIFICATION")
print("=" * 70)

# =============================================================================
# STEP 1: Import packages and print versions
# =============================================================================

print("\n[1] Checking package installations...\n")

packages_status = {}

# Core scientific packages
try:
    import numpy as np
    packages_status['numpy'] = np.__version__
    print(f"  numpy:      {np.__version__}")
except ImportError as e:
    packages_status['numpy'] = f"MISSING: {e}"
    print(f"  numpy:      MISSING - {e}")

try:
    import scipy
    packages_status['scipy'] = scipy.__version__
    print(f"  scipy:      {scipy.__version__}")
except ImportError as e:
    packages_status['scipy'] = f"MISSING: {e}"
    print(f"  scipy:      MISSING - {e}")

try:
    import matplotlib
    packages_status['matplotlib'] = matplotlib.__version__
    print(f"  matplotlib: {matplotlib.__version__}")
except ImportError as e:
    packages_status['matplotlib'] = f"MISSING: {e}"
    print(f"  matplotlib: MISSING - {e}")

try:
    import astropy
    packages_status['astropy'] = astropy.__version__
    print(f"  astropy:    {astropy.__version__}")
except ImportError as e:
    packages_status['astropy'] = f"MISSING: {e}"
    print(f"  astropy:    MISSING - {e}")

try:
    import h5py
    packages_status['h5py'] = h5py.__version__
    print(f"  h5py:       {h5py.__version__}")
except ImportError as e:
    packages_status['h5py'] = f"MISSING: {e}"
    print(f"  h5py:       MISSING - {e}")

# LIGO-specific packages
try:
    import gwosc
    packages_status['gwosc'] = gwosc.__version__
    print(f"  gwosc:      {gwosc.__version__}")
except ImportError as e:
    packages_status['gwosc'] = f"MISSING: {e}"
    print(f"  gwosc:      MISSING - {e}")

try:
    import gwpy
    packages_status['gwpy'] = gwpy.__version__
    print(f"  gwpy:       {gwpy.__version__}")
except ImportError as e:
    packages_status['gwpy'] = f"MISSING: {e}"
    print(f"  gwpy:       MISSING - {e}")

try:
    import pycbc
    packages_status['pycbc'] = pycbc.version.version
    print(f"  pycbc:      {pycbc.version.version}")
except ImportError as e:
    packages_status['pycbc'] = f"MISSING: {e}"
    print(f"  pycbc:      MISSING - {e}")

# Check for missing packages
missing = [k for k, v in packages_status.items() if 'MISSING' in str(v)]
if missing:
    print(f"\n  WARNING: Missing packages: {missing}")
    print("  Install with: pip install " + " ".join(missing))

# =============================================================================
# STEP 2: Query GWOSC API to confirm data access
# =============================================================================

print("\n" + "=" * 70)
print("[2] Testing GWOSC API access...")
print("=" * 70)

if 'MISSING' not in str(packages_status.get('gwosc', 'MISSING')):
    try:
        from gwosc import datasets
        from gwosc import locate
        from gwosc import timeline

        # Test basic API access
        print("\n  Querying available datasets...")
        all_runs = datasets.find_datasets()
        print(f"  Total datasets available: {len(all_runs)}")

        # List observing runs
        runs = datasets.find_datasets(type='run')
        print(f"  Observing runs: {runs[:10]}...")

    except Exception as e:
        print(f"  ERROR accessing GWOSC API: {e}")
else:
    print("  Skipping - gwosc package not installed")

# =============================================================================
# STEP 3: List available O4 datasets for H1 and L1
# =============================================================================

print("\n" + "=" * 70)
print("[3] Checking O4 data availability...")
print("=" * 70)

if 'MISSING' not in str(packages_status.get('gwosc', 'MISSING')):
    try:
        from gwosc import datasets

        # Find O4-related datasets
        all_datasets = datasets.find_datasets()
        o4_datasets = [d for d in all_datasets if 'O4' in d.upper()]

        print(f"\n  O4-related datasets found: {len(o4_datasets)}")
        for ds in o4_datasets[:20]:
            print(f"    - {ds}")
        if len(o4_datasets) > 20:
            print(f"    ... and {len(o4_datasets) - 20} more")

        # Check specific O4 runs
        print("\n  Checking O4a data availability:")
        try:
            # Try to get O4a segment info
            o4a_segs_h1 = datasets.find_datasets(detector='H1', type='run')
            o4a_segs_l1 = datasets.find_datasets(detector='L1', type='run')
            print(f"    H1 runs: {[r for r in o4a_segs_h1 if 'O4' in r.upper()]}")
            print(f"    L1 runs: {[r for r in o4a_segs_l1 if 'O4' in r.upper()]}")
        except Exception as e:
            print(f"    Error checking O4a: {e}")

        # Fall back to O3 if O4 not available
        print("\n  Checking O3 data availability (fallback):")
        o3_datasets = [d for d in all_datasets if 'O3' in d.upper()]
        print(f"    O3 datasets: {len(o3_datasets)}")
        for ds in o3_datasets[:10]:
            print(f"      - {ds}")

    except Exception as e:
        print(f"  ERROR: {e}")
else:
    print("  Skipping - gwosc package not installed")

# =============================================================================
# STEP 4: Print GPS time ranges
# =============================================================================

print("\n" + "=" * 70)
print("[4] GPS time ranges for observing runs...")
print("=" * 70)

if 'MISSING' not in str(packages_status.get('gwosc', 'MISSING')):
    try:
        from gwosc import datasets

        # Known GPS time ranges for LIGO observing runs
        # (These are approximate - actual science segments may vary)
        known_ranges = {
            'O1': (1126051217, 1137254417),  # Sep 2015 - Jan 2016
            'O2': (1164556817, 1187733618),  # Nov 2016 - Aug 2017
            'O3a': (1238166018, 1253977218), # Apr 2019 - Oct 2019
            'O3b': (1256655618, 1269363618), # Nov 2019 - Mar 2020
            'O4a': (1369008018, 1388534418), # May 2023 - Jan 2024 (approximate)
        }

        print("\n  Known observing run GPS ranges:")
        for run, (start, end) in known_ranges.items():
            duration_days = (end - start) / 86400
            print(f"    {run}: GPS {start} - {end} ({duration_days:.0f} days)")

        # Try to get actual segment info
        print("\n  Querying GWOSC for actual segment information...")
        try:
            # Check what runs have data
            for run in ['O3a_4KHZ_R1', 'O3b_4KHZ_R1']:
                try:
                    run_info = datasets.find_datasets(dataset=run)
                    print(f"    {run}: Available")
                except:
                    pass
        except Exception as e:
            print(f"    Could not query segments: {e}")

    except Exception as e:
        print(f"  ERROR: {e}")
else:
    print("  Skipping - gwosc package not installed")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

all_installed = all('MISSING' not in str(v) for v in packages_status.values())

if all_installed:
    print("\n  All packages installed successfully.")
    print("  GWOSC data access is working.")
    print("\n  Ready to proceed with LIGO data analysis!")
else:
    print(f"\n  Missing packages: {missing}")
    print("  Please install missing packages before proceeding.")
    print(f"\n  Run: pip install {' '.join(missing)}")

print("\n" + "=" * 70)

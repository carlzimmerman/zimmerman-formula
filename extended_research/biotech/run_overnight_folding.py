#!/usr/bin/env python3
"""
Z² Overnight Folding Run

SPDX-License-Identifier: AGPL-3.0-or-later

Run all 5 Z² protein folding pathways overnight on multiple test proteins.

Pathways:
1. Topological knot contacts (z2_topological_knot_contacts.py)
2. Implicit solvation tensor (z2_implicit_solvation_tensor.py)
3. Voronoi rotamer packing (z2_voronoi_rotamer_packing.py)
4. Geodesic folding funnel (z2_geodesic_folding_funnel.py)
5. Cotranslational resonance (z2_cotranslational_resonance.py)

Also runs main folding algorithms:
- z2_bruteflow.py (BruteFlow structure prediction)
- z2_geometric_protein_analysis.py (geometric analysis)

Author: Carl Zimmerman
Date: April 2026
"""

import subprocess
import json
import time
import os
from datetime import datetime

# ==============================================================================
# TEST PROTEINS (disease targets)
# ==============================================================================

TEST_PROTEINS = {
    # Neurodegenerative diseases
    'abeta42': {
        'name': 'Amyloid Beta 42 (Alzheimer\'s)',
        'sequence': 'DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIA',
        'disease': 'Alzheimer\'s'
    },
    'alpha_syn': {
        'name': 'Alpha-synuclein N-term (Parkinson\'s)',
        'sequence': 'MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVTTVA',
        'disease': 'Parkinson\'s'
    },
    'tau': {
        'name': 'Tau repeat region (Alzheimer\'s)',
        'sequence': 'VQIVYKPVDLSKVTSKCGSLGNIHHKPGGGQVEVKSEKLDFKDRVQSKIGSLDNITHVPGGGNKKIETHKLTFREN',
        'disease': 'Alzheimer\'s/Tauopathy'
    },

    # Metabolic disorders
    'insulin_b': {
        'name': 'Insulin B-chain (Diabetes)',
        'sequence': 'FVNQHLCGSHLVEALYLVCGERGFFYTPKT',
        'disease': 'Diabetes'
    },

    # Cancer-related
    'p53_dbd': {
        'name': 'p53 DNA-binding fragment (Cancer)',
        'sequence': 'SSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMF',
        'disease': 'Cancer'
    },

    # Fast-folding benchmarks
    'villin': {
        'name': 'Villin headpiece (fast folder)',
        'sequence': 'LSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF',
        'disease': 'Benchmark'
    },
    'trp_cage': {
        'name': 'Trp-cage (mini-protein)',
        'sequence': 'NLYIQWLKDGGPSSGRPPPS',
        'disease': 'Benchmark'
    },
    'ww_domain': {
        'name': 'WW domain (all-beta)',
        'sequence': 'KLPPGWEKRMSRSSGRVYYFNHITNASQWERPS',
        'disease': 'Benchmark'
    },
    'gb1': {
        'name': 'GB1 domain (alpha/beta)',
        'sequence': 'MTYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE',
        'disease': 'Benchmark'
    }
}

# ==============================================================================
# PATHWAY SCRIPTS
# ==============================================================================

PATHWAY_SCRIPTS = [
    ('Topological Knot Contacts', 'z2_topological_knot_contacts.py'),
    ('Implicit Solvation Tensor', 'z2_implicit_solvation_tensor.py'),
    ('Voronoi Rotamer Packing', 'z2_voronoi_rotamer_packing.py'),
    ('Geodesic Folding Funnel', 'z2_geodesic_folding_funnel.py'),
    ('Cotranslational Resonance', 'z2_cotranslational_resonance.py'),
]

ANALYSIS_SCRIPTS = [
    ('BruteFlow', 'z2_bruteflow.py'),
    ('Geometric Analysis', 'z2_geometric_protein_analysis.py'),
]


# ==============================================================================
# RUNNER
# ==============================================================================

def run_script(script_name, timeout=600):
    """Run a Python script and capture output."""
    start = time.time()

    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        elapsed = time.time() - start

        return {
            'success': result.returncode == 0,
            'stdout': result.stdout[-5000:] if len(result.stdout) > 5000 else result.stdout,
            'stderr': result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr,
            'elapsed_seconds': elapsed
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': f'Timeout after {timeout}s',
            'elapsed_seconds': timeout
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'elapsed_seconds': time.time() - start
        }


def main():
    print("="*80)
    print("Z² OVERNIGHT FOLDING RUN")
    print("="*80)
    print(f"Started: {datetime.now().isoformat()}")
    print(f"Test proteins: {len(TEST_PROTEINS)}")
    print(f"Pathway scripts: {len(PATHWAY_SCRIPTS)}")
    print(f"Analysis scripts: {len(ANALYSIS_SCRIPTS)}")
    print("="*80)

    results = {
        'start_time': datetime.now().isoformat(),
        'pathways': {},
        'analysis': {},
        'proteins': TEST_PROTEINS
    }

    # Run pathway scripts (use default test cases in each script)
    print("\n" + "="*80)
    print("RUNNING PATHWAY SCRIPTS")
    print("="*80)

    for name, script in PATHWAY_SCRIPTS:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Running: {name}")
        print("-"*60)

        result = run_script(script, timeout=300)
        results['pathways'][name] = result

        if result['success']:
            print(f"  ✓ Completed in {result['elapsed_seconds']:.1f}s")
            # Show last few lines of output
            lines = result['stdout'].strip().split('\n')
            for line in lines[-5:]:
                print(f"    {line[:70]}")
        else:
            print(f"  ✗ Failed: {result['stderr'][:100]}")

    # Run analysis scripts
    print("\n" + "="*80)
    print("RUNNING ANALYSIS SCRIPTS")
    print("="*80)

    for name, script in ANALYSIS_SCRIPTS:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Running: {name}")
        print("-"*60)

        result = run_script(script, timeout=600)
        results['analysis'][name] = result

        if result['success']:
            print(f"  ✓ Completed in {result['elapsed_seconds']:.1f}s")
        else:
            print(f"  ✗ Failed: {result['stderr'][:100]}")

    # Summary
    results['end_time'] = datetime.now().isoformat()

    n_success = sum(1 for r in results['pathways'].values() if r['success'])
    n_success += sum(1 for r in results['analysis'].values() if r['success'])
    n_total = len(PATHWAY_SCRIPTS) + len(ANALYSIS_SCRIPTS)

    print("\n" + "="*80)
    print("OVERNIGHT RUN COMPLETE")
    print("="*80)
    print(f"Ended: {results['end_time']}")
    print(f"Success: {n_success}/{n_total} scripts")

    # Total time
    total_time = sum(r['elapsed_seconds'] for r in results['pathways'].values())
    total_time += sum(r['elapsed_seconds'] for r in results['analysis'].values())
    print(f"Total compute time: {total_time:.1f}s ({total_time/60:.1f} min)")

    # Save results
    output_file = f'overnight_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_file}")

    # List generated JSON files
    print("\nGenerated result files:")
    for f in os.listdir('.'):
        if f.endswith('.json') and 'z2_' in f:
            size = os.path.getsize(f) / 1024
            print(f"  {f} ({size:.1f} KB)")

    return results


if __name__ == '__main__':
    main()

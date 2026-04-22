#!/usr/bin/env python3
"""
00_audit_existing_scripts.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

00_audit_existing_scripts.py - Systematic Audit for AI Slop

PURPOSE:
Systematically audit all existing medicine scripts to identify:
1. Hardcoded "expected" results
2. Mock data / placeholder values
3. Missing actual library calls
4. Circular scoring functions
5. Print statements that fake computation

OUTPUT:
- List of scripts to move to ai_slop_quarantine
- List of scripts that are salvageable with modifications
- Specific line numbers and issues for each script

Author: Carl Zimmerman
Date: April 21, 2026
"""
import re
from pathlib import Path
from datetime import datetime
import json

MEDICINE_DIR = Path(__file__).parent.parent
QUARANTINE_DIR = MEDICINE_DIR / "ai_slop_quarantine"
QUARANTINE_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("SYSTEMATIC SCRIPT AUDIT")
print("Identifying AI Slop for Quarantine")
print("=" * 80)
print()

# =============================================================================
# DETECTION PATTERNS
# =============================================================================

CRITICAL_PATTERNS = {
    'hardcoded_z2_value': {
        'pattern': r'=\s*9\.14\d*\s*[^Å]',
        'description': 'Hardcoded Z² value used in computation',
        'severity': 'CRITICAL',
    },
    'hardcoded_score': {
        'pattern': r'(score|energy|pmf|barrier)\s*=\s*\d+\.\d{3,}',
        'description': 'Hardcoded score/energy value',
        'severity': 'CRITICAL',
    },
    'fake_simulation_print': {
        'pattern': r'print.*["\'].*[Ss]imulat',
        'description': 'Print statement suggesting fake simulation',
        'severity': 'HIGH',
    },
    'stub_return': {
        'pattern': r'return\s+\{[^}]*["\']score["\']:\s*\d',
        'description': 'Return statement with hardcoded dict',
        'severity': 'HIGH',
    },
    'mock_data_comment': {
        'pattern': r'#.*([Mm]ock|[Pp]laceholder|[Ss]tub|[Ff]ake|[Dd]ummy)',
        'description': 'Comment indicating mock/placeholder',
        'severity': 'MEDIUM',
    },
    'magic_percentage': {
        'pattern': r'["\'].*match["\']:\s*0\.9[5-9]\d*',
        'description': 'Suspiciously high match percentage',
        'severity': 'MEDIUM',
    },
}

MISSING_REQUIREMENTS = {
    'no_error_handling': {
        'check': lambda content: 'raise' not in content and 'Exception' not in content,
        'description': 'No error handling - fails silently',
        'severity': 'HIGH',
    },
    'no_random_seed': {
        'check': lambda content: ('random' in content or 'np.random' in content) and 'seed' not in content,
        'description': 'Uses randomness without setting seed',
        'severity': 'MEDIUM',
    },
    'no_data_validation': {
        'check': lambda content: 'assert' not in content and 'validate' not in content.lower(),
        'description': 'No input data validation',
        'severity': 'LOW',
    },
}

# Libraries that should be ACTUALLY called, not just imported
REQUIRED_ACTUAL_CALLS = {
    'openmm': ['simulation.step', 'Simulation(', 'System('],
    'ripser': ['ripser(', 'Rips('],
    'mdtraj': ['md.load', 'traj.'],
}


def audit_single_script(filepath: Path) -> dict:
    """Audit a single script for issues."""
    with open(filepath, 'r') as f:
        content = f.read()
        lines = content.split('\n')

    issues = []
    warnings = []

    # Check critical patterns
    for name, config in CRITICAL_PATTERNS.items():
        matches = list(re.finditer(config['pattern'], content, re.MULTILINE))
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'type': name,
                'severity': config['severity'],
                'line': line_num,
                'context': lines[line_num - 1].strip()[:80],
                'description': config['description'],
            })

    # Check missing requirements
    for name, config in MISSING_REQUIREMENTS.items():
        if config['check'](content):
            warnings.append({
                'type': name,
                'severity': config['severity'],
                'description': config['description'],
            })

    # Check for imports without actual calls
    for lib, required_calls in REQUIRED_ACTUAL_CALLS.items():
        has_import = f'import {lib}' in content or f'from {lib}' in content
        has_actual_call = any(call in content for call in required_calls)

        if has_import and not has_actual_call:
            issues.append({
                'type': 'import_without_call',
                'severity': 'HIGH',
                'line': 0,
                'context': f'Imports {lib} but never calls critical functions',
                'description': f'{lib} imported but {required_calls} never called',
            })

    # Calculate slop score
    critical_count = sum(1 for i in issues if i['severity'] == 'CRITICAL')
    high_count = sum(1 for i in issues if i['severity'] == 'HIGH')
    medium_count = sum(1 for i in issues if i['severity'] == 'MEDIUM')

    slop_score = critical_count * 10 + high_count * 5 + medium_count * 2

    # Determine verdict
    if critical_count > 0 or high_count >= 3:
        verdict = 'QUARANTINE'
    elif high_count > 0 or medium_count >= 3:
        verdict = 'NEEDS_REWRITE'
    else:
        verdict = 'ACCEPTABLE'

    return {
        'file': filepath.name,
        'path': str(filepath),
        'issues': issues,
        'warnings': warnings,
        'slop_score': slop_score,
        'verdict': verdict,
        'line_count': len(lines),
    }


def main():
    """Main audit execution."""

    # Find all Python files in medicine directory
    py_files = list(MEDICINE_DIR.glob('*.py'))
    py_files = [f for f in py_files if not f.name.startswith('__')]

    print(f"Auditing {len(py_files)} scripts in {MEDICINE_DIR}")
    print()

    all_results = []
    quarantine_list = []
    rewrite_list = []
    acceptable_list = []

    for filepath in sorted(py_files):
        result = audit_single_script(filepath)
        all_results.append(result)

        # Print summary
        icon = {'QUARANTINE': '🗑️', 'NEEDS_REWRITE': '⚠️', 'ACCEPTABLE': '✓'}
        print(f"{icon.get(result['verdict'], '?')} {result['file']}")
        print(f"   Slop score: {result['slop_score']}, Verdict: {result['verdict']}")

        if result['issues']:
            print(f"   Issues: {len(result['issues'])}")
            for issue in result['issues'][:3]:
                print(f"      - Line {issue['line']}: {issue['type']} ({issue['severity']})")

        if result['verdict'] == 'QUARANTINE':
            quarantine_list.append(filepath)
        elif result['verdict'] == 'NEEDS_REWRITE':
            rewrite_list.append(filepath)
        else:
            acceptable_list.append(filepath)

        print()

    # Summary
    print("=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    print(f"\nTotal scripts: {len(py_files)}")
    print(f"  QUARANTINE (move to ai_slop): {len(quarantine_list)}")
    print(f"  NEEDS_REWRITE (fix issues):   {len(rewrite_list)}")
    print(f"  ACCEPTABLE (minor issues):    {len(acceptable_list)}")

    if quarantine_list:
        print("\nScripts to quarantine:")
        for f in quarantine_list:
            print(f"  - {f.name}")

    if rewrite_list:
        print("\nScripts needing rewrite:")
        for f in rewrite_list:
            print(f"  - {f.name}")

    # Save results
    output_file = MEDICINE_DIR / "validated_pipeline" / "logs" / "audit_results.json"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_scripts': len(py_files),
            'quarantine': [str(f) for f in quarantine_list],
            'needs_rewrite': [str(f) for f in rewrite_list],
            'acceptable': [str(f) for f in acceptable_list],
            'detailed_results': all_results,
        }, f, indent=2)

    print(f"\nDetailed results saved: {output_file}")

    return {
        'quarantine': quarantine_list,
        'rewrite': rewrite_list,
        'acceptable': acceptable_list,
    }


if __name__ == "__main__":
    results = main()

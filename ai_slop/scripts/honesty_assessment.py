#!/usr/bin/env python3
"""
Honesty Assessment of Mnemosyne Findings

Categories:
1. TRIVIAL - Integer ratios (1/1, 2/1, 3/1...) or simple fractions that match by accident
2. SUSPICIOUS - Uses "magic number" patterns (2Z² + 33 ≈ 100, etc.)
3. NUMEROLOGY - Formula matches but no physical reason why
4. PHENOMENOLOGICAL - Interesting pattern, needs derivation
5. DERIVABLE - Could potentially derive from first principles
6. VALIDATED - Has physical mechanism AND matches data
"""

import json
import re
from collections import defaultdict

# Load the truth index
with open('OlympusFlow/lakes/mnemosyne/truths/truth_index.json', 'r') as f:
    data = json.load(f)

# Assessment categories
assessment = {
    'TRIVIAL': [],      # 1/1, 2/1, 3/10, etc.
    'SUSPICIOUS': [],   # 2Z² + 33 ≈ 100 pattern
    'DUPLICATE': [],    # Same as known validated entry
    'NUMEROLOGY': [],   # Matches but no physical reason
    'PHENOMENOLOGICAL': [], # Interesting, needs work
    'DERIVABLE': [],    # Could derive from Z²
    'VALIDATED': [],    # Already validated with mechanism
}

# Known validated formulas (from Z² paper)
VALIDATED_FORMULAS = {
    '3/13': 'sin²θ_W',
    '13/19': 'Ω_Λ',
    '6/19': 'Ω_m',
    '4Z² + 3': 'α⁻¹',
    'Z/6': 'n_s spectral index',
    '19/6': 'dipole ratio R',
    'arccos(-1/3)': 'tetrahedral angle',
}

# Trivial integer patterns
TRIVIAL_PATTERNS = [
    r'^(\d+)/1$',           # n/1 (integers)
    r'^1/(\d+)$',           # 1/n
    r'^(\d)/(\d)$',         # single digit fractions
]

# Suspicious "magic number" patterns
SUSPICIOUS_PATTERNS = [
    r'2Z² \+ 33',           # ≈ 100
    r'2Z² \+ 43',           # ≈ 110
    r'4Z² \+ 16',           # ≈ 150
    r'6Z² \+ 49',           # ≈ 250
    r'8Z² \+ 5',            # ≈ 273 (water triple point hack)
    r'8Z² \+ 20',           # ≈ 288
    r'8Z² \+ 32',           # ≈ 300
    r'10Z² \+ 5',           # ≈ 340
    r'10Z² \+ 38',          # ≈ 373
]

# Physically interesting domains (more likely to have real Z² connections)
INTERESTING_DOMAINS = [
    'particle_physics', 'cosmology', 'quantum_information',
    'fundamental_constants', 'z2_firstprinciples', 'qed_precision'
]

def is_trivial(formula):
    """Check if formula is trivially matching"""
    if not formula:
        return True
    for pattern in TRIVIAL_PATTERNS:
        if re.match(pattern, formula.strip()):
            return True
    # Also check for simple integer results
    if formula.strip() in ['1/1', '2/1', '3/1', '4/1', '5/1', '6/1', '10/1', '20/1', '30/1', '40/1', '50/1']:
        return True
    return False

def is_suspicious(formula):
    """Check if formula uses suspicious magic number pattern"""
    if not formula:
        return False
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, formula):
            return True
    return False

def is_known_validated(formula):
    """Check if this matches a known validated Z² result"""
    if not formula:
        return False
    for known, name in VALIDATED_FORMULAS.items():
        if known in formula:
            return name
    return None

# Process all entries
stats = defaultdict(int)

for entry_id, entry in data.items():
    formula = entry.get('z2_formula', '') or ''
    claim = entry.get('claim', '')
    domain = entry.get('domain', 'unknown')
    status = entry.get('status', 'pending')
    percent_error = entry.get('percent_error') or 0
    hrm_score = entry.get('hrm_score') or 0

    # Skip already validated
    if status == 'validated':
        assessment['VALIDATED'].append({
            'id': entry_id,
            'claim': claim,
            'formula': formula,
            'domain': domain,
            'error': percent_error
        })
        stats['validated'] += 1
        continue

    # Check for known validated formula
    known = is_known_validated(formula)
    if known:
        assessment['DUPLICATE'].append({
            'id': entry_id,
            'claim': claim,
            'formula': formula,
            'known_as': known,
            'domain': domain
        })
        stats['duplicate'] += 1
        continue

    # Check for trivial matches
    if is_trivial(formula):
        assessment['TRIVIAL'].append({
            'id': entry_id,
            'claim': claim,
            'formula': formula,
            'domain': domain,
            'error': percent_error
        })
        stats['trivial'] += 1
        continue

    # Check for suspicious patterns
    if is_suspicious(formula):
        assessment['SUSPICIOUS'].append({
            'id': entry_id,
            'claim': claim,
            'formula': formula,
            'domain': domain,
            'error': percent_error
        })
        stats['suspicious'] += 1
        continue

    # Interesting domain with non-trivial formula = potentially derivable
    if domain in INTERESTING_DOMAINS and percent_error < 0.5:
        assessment['DERIVABLE'].append({
            'id': entry_id,
            'claim': claim,
            'formula': formula,
            'domain': domain,
            'error': percent_error,
            'hrm': hrm_score
        })
        stats['derivable'] += 1
        continue

    # Low error, non-trivial = phenomenological
    if percent_error < 0.3 and hrm_score > 0.5:
        assessment['PHENOMENOLOGICAL'].append({
            'id': entry_id,
            'claim': claim,
            'formula': formula,
            'domain': domain,
            'error': percent_error,
            'hrm': hrm_score
        })
        stats['phenomenological'] += 1
        continue

    # Everything else = numerology
    assessment['NUMEROLOGY'].append({
        'id': entry_id,
        'claim': claim,
        'formula': formula,
        'domain': domain,
        'error': percent_error
    })
    stats['numerology'] += 1

# Print results
print("=" * 70)
print("HONESTY ASSESSMENT SUMMARY")
print("=" * 70)
print()

for category, count in sorted(stats.items(), key=lambda x: -x[1]):
    pct = 100 * count / len(data)
    print(f"{category.upper():20s}: {count:4d} ({pct:5.1f}%)")

print()
print("=" * 70)
print("DETAILED BREAKDOWN")
print("=" * 70)

print("\n### VALIDATED (Keep) ###")
for e in assessment['VALIDATED'][:10]:
    print(f"  ✓ {e['claim'][:40]}: {e['formula'][:25]} ({e['error']:.3f}%)")
if len(assessment['VALIDATED']) > 10:
    print(f"  ... and {len(assessment['VALIDATED'])-10} more")

print("\n### DERIVABLE (Try to derive) ###")
for e in assessment['DERIVABLE'][:15]:
    print(f"  → {e['claim'][:40]}: {e['formula'][:25]} ({e['error']:.3f}%)")
if len(assessment['DERIVABLE']) > 15:
    print(f"  ... and {len(assessment['DERIVABLE'])-15} more")

print("\n### PHENOMENOLOGICAL (Interesting patterns) ###")
for e in assessment['PHENOMENOLOGICAL'][:15]:
    print(f"  ? {e['claim'][:40]}: {e['formula'][:25]} ({e['error']:.3f}%)")
if len(assessment['PHENOMENOLOGICAL']) > 15:
    print(f"  ... and {len(assessment['PHENOMENOLOGICAL'])-15} more")

print("\n### SUSPICIOUS (Magic number patterns - likely numerology) ###")
for e in assessment['SUSPICIOUS'][:10]:
    print(f"  ⚠ {e['claim'][:40]}: {e['formula'][:25]}")
if len(assessment['SUSPICIOUS']) > 10:
    print(f"  ... and {len(assessment['SUSPICIOUS'])-10} more")

print("\n### TRIVIAL (Integer/simple fraction matches - numerology) ###")
for e in assessment['TRIVIAL'][:10]:
    print(f"  ✗ {e['claim'][:40]}: {e['formula'][:25]}")
if len(assessment['TRIVIAL']) > 10:
    print(f"  ... and {len(assessment['TRIVIAL'])-10} more")

print("\n### DUPLICATE (Same as known validated) ###")
for e in assessment['DUPLICATE'][:10]:
    print(f"  = {e['claim'][:40]}: same as {e['known_as']}")
if len(assessment['DUPLICATE']) > 10:
    print(f"  ... and {len(assessment['DUPLICATE'])-10} more")

# Save full assessment to JSON
with open('daemon_outputs/honesty_assessment.json', 'w') as f:
    json.dump({
        'stats': dict(stats),
        'total': len(data),
        'assessment': {k: v for k, v in assessment.items()}
    }, f, indent=2)

print("\n" + "=" * 70)
print("Full assessment saved to: daemon_outputs/honesty_assessment.json")
print("=" * 70)

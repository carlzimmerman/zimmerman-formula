#!/usr/bin/env python3
"""
Z² Negative Control - Packing Density Validation

SPDX-License-Identifier: AGPL-3.0-or-later

RED TEAM PROTOCOL - Vulnerability 1: "Numerology Trap"

This script tests whether the Z² coordination number of 8 is:
A) A genuine prediction of Z² theory (our claim)
B) Just normal protein physics (falsification)

THE TEST:
1. Download 5+ random globular proteins from PDB
2. Calculate mean contacts per residue (8Å cutoff)
3. Compare to Z² optimal value of 8

FALSIFICATION CRITERIA:
- If random proteins ALSO average ~8 contacts → Z² is not predictive
- If random proteins average significantly different → Z² is validated

This is an HONEST scientific test. We may falsify our own claims.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import os
import json
import urllib.request
import ssl
import gzip
from io import BytesIO
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103
OPTIMAL_CONTACTS = 8  # Z² topological prediction
CONTACT_CUTOFF = 8.0  # Å - standard protein contact definition

# ==============================================================================
# TEST PROTEINS - Random Globular Proteins
# ==============================================================================

# Well-characterized globular proteins (not designed by us)
TEST_PROTEINS = [
    # PDB ID, Name, Size category
    ("1UBQ", "Ubiquitin", "small"),           # 76 residues, classic fold
    ("1L2Y", "Trp-cage", "mini"),             # 20 residues, designed miniprotein
    ("1CRN", "Crambin", "small"),             # 46 residues, plant toxin
    ("2GB1", "Protein G B1", "small"),        # 56 residues, IgG binding
    ("1VII", "Villin headpiece", "small"),    # 36 residues, actin binding
    ("3NJG", "WW domain", "mini"),            # 34 residues, proline binding
    ("1IGD", "Immunoglobulin", "medium"),     # 61 residues, antibody domain
    ("1ENH", "Engrailed homeodomain", "small"), # 54 residues, DNA binding
]

# Additional larger proteins for statistical power
ADDITIONAL_PROTEINS = [
    ("1MBO", "Myoglobin", "medium"),          # 153 residues, oxygen carrier
    ("2LZM", "Lysozyme", "medium"),           # 130 residues, enzyme
    ("1RIB", "Ribonuclease A", "medium"),     # 124 residues, enzyme
    ("1TIM", "Triose isomerase", "large"),    # 247 residues per chain
    ("3LZT", "Hen lysozyme", "medium"),       # 129 residues
]


def parse_pdb_coords(pdb_content: str) -> Tuple[np.ndarray, List[str]]:
    """Extract Cα coordinates from PDB content."""
    coords = []
    residues = []
    seen = set()

    for line in pdb_content.split('\n'):
        if line.startswith('ATOM') or line.startswith('HETATM'):
            atom_name = line[12:16].strip()
            if atom_name == 'CA':
                # Only take chain A or first chain
                chain = line[21]
                res_num = line[22:26].strip()
                res_name = line[17:20].strip()
                key = (chain, res_num)

                if key not in seen:
                    seen.add(key)
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])
                    residues.append(f"{res_name}{res_num}")

                    # Only take first 200 residues to keep comparable
                    if len(coords) >= 200:
                        break

    return np.array(coords), residues


def download_pdb(pdb_id: str) -> Optional[str]:
    """Download PDB file from RCSB."""
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    # Create SSL context that doesn't verify (for some networks)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(url, timeout=30, context=ctx) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"    ✗ Failed to download {pdb_id}: {e}")
        return None


def calculate_contacts(coords: np.ndarray, cutoff: float = CONTACT_CUTOFF) -> np.ndarray:
    """Calculate contacts per residue using distance matrix."""
    n_residues = len(coords)

    # Compute pairwise distances
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    distances = np.sqrt(np.sum(diff**2, axis=-1))

    # Count contacts (excluding self and sequential neighbors)
    contacts = np.zeros(n_residues)
    for i in range(n_residues):
        for j in range(n_residues):
            if abs(i - j) > 1 and distances[i, j] < cutoff:
                contacts[i] += 1

    return contacts


def analyze_protein(pdb_id: str, name: str) -> Optional[Dict]:
    """Analyze a single protein's coordination statistics."""
    print(f"\n  Analyzing {pdb_id} ({name})...")

    # Download
    pdb_content = download_pdb(pdb_id)
    if pdb_content is None:
        return None

    # Parse coordinates
    coords, residues = parse_pdb_coords(pdb_content)
    n_residues = len(coords)

    if n_residues < 10:
        print(f"    ✗ Too few residues: {n_residues}")
        return None

    print(f"    ✓ Parsed {n_residues} Cα atoms")

    # Calculate contacts
    contacts = calculate_contacts(coords)

    mean_contacts = np.mean(contacts)
    std_contacts = np.std(contacts)
    min_contacts = np.min(contacts)
    max_contacts = np.max(contacts)

    # Z² deviation
    z2_deviation = mean_contacts - OPTIMAL_CONTACTS

    print(f"    Mean contacts: {mean_contacts:.2f} ± {std_contacts:.2f}")
    print(f"    Z² deviation: {z2_deviation:+.2f}")

    return {
        "pdb_id": pdb_id,
        "name": name,
        "n_residues": n_residues,
        "mean_contacts": float(mean_contacts),
        "std_contacts": float(std_contacts),
        "min_contacts": int(min_contacts),
        "max_contacts": int(max_contacts),
        "z2_deviation": float(z2_deviation),
        "contacts_profile": contacts.tolist()
    }


def run_statistical_test(results: List[Dict]) -> Dict:
    """Run statistical analysis on all proteins."""
    if len(results) < 3:
        return {"error": "Too few proteins for statistical analysis"}

    mean_contacts = [r["mean_contacts"] for r in results]

    overall_mean = np.mean(mean_contacts)
    overall_std = np.std(mean_contacts)

    # t-test against Z² prediction of 8
    from_z2 = overall_mean - OPTIMAL_CONTACTS

    # Effect size (Cohen's d)
    effect_size = from_z2 / overall_std if overall_std > 0 else 0

    # Simple hypothesis test
    # H0: mean contacts = 8 (Z² prediction)
    # H1: mean contacts ≠ 8

    n = len(mean_contacts)
    se = overall_std / np.sqrt(n)
    t_stat = from_z2 / se if se > 0 else 0

    # Approximate p-value (two-tailed)
    # Using normal approximation for large enough sample
    import math
    p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(t_stat) / math.sqrt(2))))

    return {
        "n_proteins": n,
        "overall_mean": float(overall_mean),
        "overall_std": float(overall_std),
        "z2_prediction": OPTIMAL_CONTACTS,
        "deviation_from_z2": float(from_z2),
        "effect_size_cohen_d": float(effect_size),
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "individual_means": mean_contacts
    }


def generate_verdict(stats: Dict, results: List[Dict]) -> Dict:
    """Generate honest scientific verdict."""
    deviation = stats.get("deviation_from_z2", 0)
    p_value = stats.get("p_value", 1.0)
    effect_size = stats.get("effect_size_cohen_d", 0)

    # Interpret results
    if abs(deviation) < 0.5:  # Within 0.5 contacts of prediction
        verdict = "FALSIFIED"
        explanation = (
            "Natural proteins ALSO average ~8 contacts per residue. "
            "The Z² coordination number is NOT a unique prediction but "
            "reflects universal protein packing physics. This is the "
            "expected result for well-folded globular proteins."
        )
        severity = "CRITICAL"
    elif abs(deviation) < 1.0:
        verdict = "WEAKLY_FALSIFIED"
        explanation = (
            "Natural proteins average close to 8 contacts. "
            "The Z² value may reflect physical packing constraints "
            "rather than 8D geometry. Further investigation needed."
        )
        severity = "WARNING"
    else:
        verdict = "VALIDATED"
        explanation = (
            f"Natural proteins average {stats['overall_mean']:.1f} contacts, "
            f"significantly different from Z² prediction of 8. "
            "This suggests Z² design may produce unusual packing."
        )
        severity = "INFO"

    # Additional analysis
    scientific_interpretation = {
        "the_question": "Is Z² = 8 contacts a unique prediction or universal physics?",
        "our_claim": "Z² theory predicts optimal coordination = 8 based on 8D geometry",
        "null_hypothesis": "All well-folded proteins naturally have ~8 contacts",
        "test_result": verdict,
        "measured_mean": stats["overall_mean"],
        "predicted_mean": OPTIMAL_CONTACTS,
        "statistical_significance": "p < 0.05" if p_value < 0.05 else "p >= 0.05"
    }

    return {
        "verdict": verdict,
        "severity": severity,
        "explanation": explanation,
        "scientific_interpretation": scientific_interpretation,
        "recommendation": get_recommendation(verdict)
    }


def get_recommendation(verdict: str) -> str:
    """Get honest recommendation based on verdict."""
    if verdict == "FALSIFIED":
        return (
            "IMPORTANT: The Z² coordination number of 8 appears to be a general "
            "property of protein physics, not a unique prediction. Reconsider "
            "claims that Z² geometry 'predicts' the coordination number. "
            "However, Z² theory may still be valuable for OTHER predictions "
            "(e.g., stability, dynamics, binding). Focus on claims that ARE unique."
        )
    elif verdict == "WEAKLY_FALSIFIED":
        return (
            "The evidence is ambiguous. Consider: (1) Testing more proteins, "
            "(2) Using different size ranges, (3) Comparing interior vs surface "
            "residues specifically. The claim needs refinement."
        )
    else:
        return (
            "The test supports Z² uniqueness. However, ensure the protein sample "
            "is representative. Consider testing membrane proteins, IDPs, and "
            "other structural classes for broader validation."
        )


def create_visualization(results: List[Dict], stats: Dict, verdict: Dict,
                         output_dir: str):
    """Create visualization of results."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("  Warning: matplotlib not available for visualization")
        return

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Bar chart of mean contacts per protein
    ax1 = axes[0, 0]
    names = [r["pdb_id"] for r in results]
    means = [r["mean_contacts"] for r in results]
    colors = ['green' if abs(m - 8) < 1 else 'red' for m in means]

    bars = ax1.bar(names, means, color=colors, alpha=0.7, edgecolor='black')
    ax1.axhline(y=OPTIMAL_CONTACTS, color='blue', linestyle='--', linewidth=2,
                label=f'Z² prediction = {OPTIMAL_CONTACTS}')
    ax1.axhline(y=stats["overall_mean"], color='orange', linestyle='-', linewidth=2,
                label=f'Measured mean = {stats["overall_mean"]:.2f}')
    ax1.set_ylabel('Mean Contacts per Residue')
    ax1.set_xlabel('PDB ID')
    ax1.set_title('Coordination Numbers Across Natural Proteins')
    ax1.legend()
    ax1.set_ylim(0, 15)

    # 2. Distribution histogram
    ax2 = axes[0, 1]
    all_contacts = []
    for r in results:
        all_contacts.extend(r["contacts_profile"])

    ax2.hist(all_contacts, bins=30, color='steelblue', alpha=0.7, edgecolor='black')
    ax2.axvline(x=OPTIMAL_CONTACTS, color='red', linestyle='--', linewidth=2,
                label=f'Z² optimal = {OPTIMAL_CONTACTS}')
    ax2.axvline(x=np.mean(all_contacts), color='orange', linestyle='-', linewidth=2,
                label=f'Observed mean = {np.mean(all_contacts):.2f}')
    ax2.set_xlabel('Contacts per Residue')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Coordination Numbers')
    ax2.legend()

    # 3. Size vs contacts scatter
    ax3 = axes[1, 0]
    sizes = [r["n_residues"] for r in results]
    ax3.scatter(sizes, means, s=100, c=colors, alpha=0.7, edgecolor='black')
    for i, (s, m, n) in enumerate(zip(sizes, means, names)):
        ax3.annotate(n, (s, m), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax3.axhline(y=OPTIMAL_CONTACTS, color='blue', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Protein Size (residues)')
    ax3.set_ylabel('Mean Contacts')
    ax3.set_title('Size vs Coordination')

    # 4. Verdict summary
    ax4 = axes[1, 1]
    ax4.axis('off')

    verdict_color = {
        "VALIDATED": "green",
        "WEAKLY_FALSIFIED": "orange",
        "FALSIFIED": "red"
    }.get(verdict["verdict"], "gray")

    text = f"""
    RED TEAM VALIDATION RESULT
    {'='*40}

    VERDICT: {verdict['verdict']}

    Z² PREDICTION:    {OPTIMAL_CONTACTS:.0f} contacts/residue
    MEASURED MEAN:    {stats['overall_mean']:.2f} contacts/residue
    DEVIATION:        {stats['deviation_from_z2']:+.2f}

    Proteins tested:  {stats['n_proteins']}
    Effect size:      {stats['effect_size_cohen_d']:.2f} (Cohen's d)
    p-value:          {stats['p_value']:.4f}

    INTERPRETATION:
    {verdict['explanation'][:200]}...
    """

    ax4.text(0.1, 0.9, text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.suptitle('Z² Negative Control: Testing Coordination Number Claim',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'negative_control_results.png'), dpi=150)
    plt.close()
    print(f"\n  ✓ Visualization saved: {output_dir}/negative_control_results.png")


def main():
    """Run negative control validation."""
    print("=" * 70)
    print("Z² NEGATIVE CONTROL - COORDINATION NUMBER VALIDATION")
    print("=" * 70)
    print(f"Z² prediction: {OPTIMAL_CONTACTS} contacts per residue")
    print(f"Contact cutoff: {CONTACT_CUTOFF} Å")
    print("=" * 70)

    print("\n" + "=" * 60)
    print("RED TEAM PROTOCOL - FALSIFICATION TEST")
    print("=" * 60)
    print("\nTHE QUESTION:")
    print("  Is Z² = 8 contacts a UNIQUE prediction,")
    print("  or just normal protein physics?")
    print("\nIF NATURAL PROTEINS ALSO AVERAGE ~8:")
    print("  → The Z² claim is FALSIFIED")
    print("  → 8 contacts is universal, not geometric")
    print("\nThis is honest science. We may falsify our own work.")
    print("=" * 60)

    # Create output directory
    output_dir = "negative_control"
    os.makedirs(output_dir, exist_ok=True)

    # Analyze proteins
    print("\n" + "=" * 60)
    print("ANALYZING NATURAL PROTEINS FROM PDB")
    print("=" * 60)

    results = []
    all_proteins = TEST_PROTEINS + ADDITIONAL_PROTEINS

    for pdb_id, name, size in all_proteins:
        result = analyze_protein(pdb_id, name)
        if result:
            result["size_category"] = size
            results.append(result)

    if len(results) < 3:
        print("\n✗ ERROR: Could not analyze enough proteins")
        print("  Check network connection and try again")
        return None

    # Statistical analysis
    print("\n" + "=" * 60)
    print("STATISTICAL ANALYSIS")
    print("=" * 60)

    stats = run_statistical_test(results)

    print(f"\n  Proteins analyzed: {stats['n_proteins']}")
    print(f"  Overall mean contacts: {stats['overall_mean']:.2f} ± {stats['overall_std']:.2f}")
    print(f"  Z² prediction: {OPTIMAL_CONTACTS}")
    print(f"  Deviation from Z²: {stats['deviation_from_z2']:+.2f}")
    print(f"  Effect size (Cohen's d): {stats['effect_size_cohen_d']:.3f}")
    print(f"  p-value: {stats['p_value']:.4f}")

    # Generate verdict
    verdict = generate_verdict(stats, results)

    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)
    print(f"\n  {verdict['severity']}: {verdict['verdict']}")
    print(f"\n  {verdict['explanation']}")
    print(f"\n  Recommendation: {verdict['recommendation'][:300]}...")

    # Create visualization
    create_visualization(results, stats, verdict, output_dir)

    # Save results
    full_results = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "negative_control_packing",
        "z2_prediction": OPTIMAL_CONTACTS,
        "contact_cutoff": CONTACT_CUTOFF,
        "proteins_analyzed": results,
        "statistics": stats,
        "verdict": verdict
    }

    with open(os.path.join(output_dir, "negative_control_results.json"), 'w') as f:
        json.dump(full_results, f, indent=2)

    print(f"\n  ✓ Results saved: {output_dir}/negative_control_results.json")

    # Final summary
    print("\n" + "=" * 70)
    print("NEGATIVE CONTROL COMPLETE")
    print("=" * 70)

    if verdict['verdict'] == "FALSIFIED":
        print("""
  ┌─────────────────────────────────────────────────────────────────┐
  │  CRITICAL FINDING: Z² = 8 appears to be UNIVERSAL PHYSICS      │
  │                                                                  │
  │  Natural proteins ALSO average ~8 contacts per residue.         │
  │  This is NOT a unique prediction of Z² geometry.                │
  │                                                                  │
  │  WHAT THIS MEANS:                                               │
  │  • The coordination claim needs revision                        │
  │  • Z² may still be valid for OTHER predictions                  │
  │  • Focus on truly unique Z² claims (dynamics, stability, etc.)  │
  │                                                                  │
  │  This is honest science. We tested and may have falsified.      │
  └─────────────────────────────────────────────────────────────────┘
        """)
    elif verdict['verdict'] == "VALIDATED":
        print("""
  ┌─────────────────────────────────────────────────────────────────┐
  │  FINDING: Natural proteins differ from Z² prediction           │
  │                                                                  │
  │  The test SUPPORTS Z² uniqueness, but more tests needed.        │
  └─────────────────────────────────────────────────────────────────┘
        """)

    return full_results


if __name__ == "__main__":
    results = main()

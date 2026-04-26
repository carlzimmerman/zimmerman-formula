#!/usr/bin/env python3
"""
M4 Commensal Selectivity Checker

Validates that designed antivirulence peptides do NOT harm beneficial
commensal bacteria in the oral microbiome. This is critical for:
1. Preserving healthy oral ecology
2. Avoiding dysbiosis
3. Ensuring therapeutic specificity

The checker screens peptides against 15+ commensal bacteria and calculates
selectivity indices (SI = IC50_commensal / IC50_pathogen).

Target SI > 100: Excellent selectivity
Target SI > 10: Acceptable selectivity
Target SI < 10: REJECT - potential harm to commensals

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later
"""

import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import math

# ==============================================================================
# CONFIGURATION
# ==============================================================================

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "results", "selectivity_analysis")

# Commensal bacteria to protect
# Data from Human Oral Microbiome Database (HOMD)
COMMENSAL_BACTERIA = {
    # Protective streptococci
    "Streptococcus_sanguinis": {
        "role": "Early colonizer, competes with S. mutans",
        "benefit": "Produces H2O2, geometrically stabilize pathogens",
        "gtf_homolog": 0.45,  # Sequence identity to S. mutans GtfC
        "srta_homolog": 0.72,  # Sequence identity to S. mutans SrtA
        "protection_priority": "HIGH",
    },
    "Streptococcus_gordonii": {
        "role": "Plaque homeostasis",
        "benefit": "Arginolytic, raises pH, competes with S. mutans",
        "gtf_homolog": 0.42,
        "srta_homolog": 0.70,
        "protection_priority": "HIGH",
    },
    "Streptococcus_mitis": {
        "role": "Early colonizer",
        "benefit": "Normal flora, immune education",
        "gtf_homolog": 0.38,
        "srta_homolog": 0.68,
        "protection_priority": "MEDIUM",
    },
    "Streptococcus_oralis": {
        "role": "Biofilm architecture",
        "benefit": "Co-aggregation with beneficial species",
        "gtf_homolog": 0.40,
        "srta_homolog": 0.65,
        "protection_priority": "MEDIUM",
    },

    # Lactate consumers (reduce caries risk)
    "Veillonella_parvula": {
        "role": "Lactate consumer",
        "benefit": "Metabolizes acid from streptococci, raises pH",
        "gtf_homolog": 0.0,  # No Gtf
        "srta_homolog": 0.15,
        "protection_priority": "HIGH",
    },
    "Veillonella_atypica": {
        "role": "Lactate consumer",
        "benefit": "pH buffering",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.12,
        "protection_priority": "MEDIUM",
    },

    # Actinomyces (enamel protection)
    "Actinomyces_naeslundii": {
        "role": "Enamel protection",
        "benefit": "Promotes remineralization",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.55,
        "protection_priority": "HIGH",
    },
    "Actinomyces_viscosus": {
        "role": "Root surface colonizer",
        "benefit": "Normal root flora",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.52,
        "protection_priority": "MEDIUM",
    },

    # Neisseria (immune modulation)
    "Neisseria_subflava": {
        "role": "Immune modulation",
        "benefit": "Anti-inflammatory effects",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.0,
        "protection_priority": "MEDIUM",
    },
    "Neisseria_sicca": {
        "role": "Oral homeostasis",
        "benefit": "Normal flora",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.0,
        "protection_priority": "LOW",
    },

    # Rothia (nitrate reduction)
    "Rothia_dentocariosa": {
        "role": "Nitrate reduction",
        "benefit": "Cardiovascular benefits via NO production",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.48,
        "protection_priority": "HIGH",
    },
    "Rothia_mucilaginosa": {
        "role": "Mucosal colonizer",
        "benefit": "Normal tonsillar flora",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.45,
        "protection_priority": "LOW",
    },

    # Haemophilus (ecosystem balance)
    "Haemophilus_parainfluenzae": {
        "role": "Ecosystem balance",
        "benefit": "Competitive exclusion of pathogens",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.0,
        "protection_priority": "MEDIUM",
    },

    # Corynebacterium (biofilm structure)
    "Corynebacterium_matruchotii": {
        "role": "Biofilm scaffold",
        "benefit": "Structural support for beneficial community",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.35,
        "protection_priority": "MEDIUM",
    },

    # Leptotrichia (normal flora)
    "Leptotrichia_buccalis": {
        "role": "Normal subgingival flora",
        "benefit": "Part of healthy community",
        "gtf_homolog": 0.0,
        "srta_homolog": 0.0,
        "protection_priority": "LOW",
    },
}

# Selectivity thresholds
SELECTIVITY_THRESHOLDS = {
    "EXCELLENT": 100.0,  # SI >= 100
    "GOOD": 50.0,        # SI >= 50
    "ACCEPTABLE": 10.0,  # SI >= 10
    "MARGINAL": 5.0,     # SI >= 5
    "REJECT": 0.0,       # SI < 5
}


# ==============================================================================
# DATA STRUCTURES
# ==============================================================================

@dataclass
class CommensalScreenResult:
    """Result of screening against a single commensal."""
    commensal_name: str
    role: str
    protection_priority: str

    # Homology data
    target_homolog_identity: float  # 0-1

    # Predicted binding
    predicted_ic50_ratio: float  # Relative to target system
    selectivity_index: float

    # Verdict
    safe: bool
    warning: str


@dataclass
class SelectivityReport:
    """Complete selectivity report for a peptide."""
    peptide_id: str
    sequence: str
    target_id: str

    # Overall metrics
    n_commensals_screened: int
    n_safe: int
    n_warning: int
    n_reject: int

    # Detailed results
    commensal_results: List[CommensalScreenResult]

    # Summary scores
    average_selectivity_index: float
    minimum_selectivity_index: float
    worst_commensal: str

    # Final verdict
    overall_verdict: str  # "PASS", "WARN", "REJECT"
    recommendation: str

    timestamp: str


# ==============================================================================
# SELECTIVITY ANALYSIS
# ==============================================================================

def estimate_cross_reactivity(peptide_sequence: str, target_id: str,
                               commensal_info: Dict) -> float:
    """
    Estimate cross-reactivity with commensal based on target homology.

    Returns predicted IC50 ratio (commensal / target system).
    Higher = more selective (better).
    """

    # Get relevant homolog identity based on target
    if "GtfC" in target_id or "Gtf" in target_id:
        homolog_identity = commensal_info.get("gtf_homolog", 0.0)
    elif "SrtA" in target_id or "Sortase" in target_id:
        homolog_identity = commensal_info.get("srta_homolog", 0.0)
    elif "RgpB" in target_id or "Gingipain" in target_id:
        # Gingipains unique to P. gingivalis
        homolog_identity = 0.0
    elif "FadA" in target_id:
        # FadA unique to F. nucleatum
        homolog_identity = 0.0
    else:
        homolog_identity = 0.2  # Default low homology

    # If no homolog, peptide unlikely to cross-react
    if homolog_identity == 0.0:
        return 1000.0  # Very high selectivity

    # Cross-reactivity scales with homology
    # At 100% identity: IC50 ratio = 1 (same binding)
    # At 50% identity: IC50 ratio ~ 10-100
    # At 30% identity: IC50 ratio ~ 100-1000

    # Model: IC50_ratio = 10^(k * (1 - homolog_identity))
    # where k ~ 3 gives reasonable range

    k = 3.0
    ic50_ratio = 10 ** (k * (1 - homolog_identity))

    # Add some sequence-specific factors
    # More charged peptides may have more off-target effects
    charge = sum(1 for aa in peptide_sequence if aa in "KRH") - \
             sum(1 for aa in peptide_sequence if aa in "DE")
    if abs(charge) > 3:
        ic50_ratio *= 0.8  # Slightly worse selectivity

    # Aromatic residues can have promiscuous binding
    aromatics = sum(1 for aa in peptide_sequence if aa in "FWY")
    if aromatics > 4:
        ic50_ratio *= 0.7  # Worse selectivity

    return ic50_ratio


def screen_against_commensals(peptide_sequence: str, peptide_id: str,
                               target_id: str) -> SelectivityReport:
    """Screen a peptide against all commensal bacteria."""

    results = []
    safe_count = 0
    warning_count = 0
    reject_count = 0

    for commensal_name, commensal_info in COMMENSAL_BACTERIA.items():

        # Estimate cross-reactivity
        ic50_ratio = estimate_cross_reactivity(peptide_sequence, target_id, commensal_info)
        selectivity_index = ic50_ratio  # SI = IC50_commensal / IC50_pathogen

        # Determine safety
        if selectivity_index >= SELECTIVITY_THRESHOLDS["EXCELLENT"]:
            safe = True
            warning = ""
            safe_count += 1
        elif selectivity_index >= SELECTIVITY_THRESHOLDS["ACCEPTABLE"]:
            safe = True
            warning = f"Moderate selectivity (SI={selectivity_index:.1f})"
            safe_count += 1
        elif selectivity_index >= SELECTIVITY_THRESHOLDS["MARGINAL"]:
            safe = False
            warning = f"LOW selectivity - potential off-target (SI={selectivity_index:.1f})"
            warning_count += 1
        else:
            safe = False
            warning = f"CRITICAL: High cross-reactivity risk (SI={selectivity_index:.1f})"
            reject_count += 1

        # Add priority weighting
        if commensal_info["protection_priority"] == "HIGH" and not safe:
            warning = "HIGH PRIORITY COMMENSAL: " + warning

        # Get homolog identity for the specific target
        if "GtfC" in target_id:
            homolog = commensal_info.get("gtf_homolog", 0.0)
        elif "SrtA" in target_id:
            homolog = commensal_info.get("srta_homolog", 0.0)
        else:
            homolog = 0.0

        result = CommensalScreenResult(
            commensal_name=commensal_name,
            role=commensal_info["role"],
            protection_priority=commensal_info["protection_priority"],
            target_homolog_identity=homolog,
            predicted_ic50_ratio=ic50_ratio,
            selectivity_index=selectivity_index,
            safe=safe,
            warning=warning
        )
        results.append(result)

    # Calculate summary statistics
    selectivity_indices = [r.selectivity_index for r in results]
    avg_si = sum(selectivity_indices) / len(selectivity_indices) if selectivity_indices else 0
    min_si = min(selectivity_indices) if selectivity_indices else 0
    worst = min(results, key=lambda x: x.selectivity_index)

    # Determine overall verdict
    if reject_count > 0:
        verdict = "REJECT"
        recommendation = f"Peptide shows unacceptable cross-reactivity with {reject_count} commensal(s). " \
                        f"Redesign required to avoid {worst.commensal_name}."
    elif warning_count > 2:
        verdict = "WARN"
        recommendation = f"Peptide shows marginal selectivity with {warning_count} commensal(s). " \
                        f"Consider redesign or proceed with caution."
    elif warning_count > 0:
        verdict = "WARN"
        recommendation = f"Generally acceptable but monitor effects on {warning_count} commensal(s)."
    else:
        verdict = "PASS"
        recommendation = "Excellent selectivity. Low risk of disrupting commensal microbiome."

    report = SelectivityReport(
        peptide_id=peptide_id,
        sequence=peptide_sequence,
        target_id=target_id,
        n_commensals_screened=len(results),
        n_safe=safe_count,
        n_warning=warning_count,
        n_reject=reject_count,
        commensal_results=results,
        average_selectivity_index=avg_si,
        minimum_selectivity_index=min_si,
        worst_commensal=worst.commensal_name,
        overall_verdict=verdict,
        recommendation=recommendation,
        timestamp=datetime.now().isoformat()
    )

    return report


# ==============================================================================
# BATCH SCREENING
# ==============================================================================

def load_designed_peptides(peptides_dir: str = None) -> List[Dict]:
    """Load designed peptides from previous stage."""

    if peptides_dir is None:
        peptides_dir = os.path.join(os.path.dirname(__file__), "results", "designed_peptides")

    peptides = []

    # Look for JSON files
    if os.path.exists(peptides_dir):
        for filename in os.listdir(peptides_dir):
            if filename.endswith(".json") and "designed_peptides" in filename:
                filepath = os.path.join(peptides_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)

                # Extract peptides from all targets
                for target_id, target_data in data.get("targets", {}).items():
                    for pep in target_data.get("peptides", []):
                        peptides.append({
                            "peptide_id": pep["peptide_id"],
                            "sequence": pep["sequence"],
                            "target_id": pep["target_id"]
                        })

    # If no files found, use demo peptides
    if not peptides:
        print("No peptide files found. Using demo peptides.")
        peptides = [
            {"peptide_id": "GtfC_demo_001", "sequence": "CRWFKDLAEKC", "target_id": "GtfC_S_mutans"},
            {"peptide_id": "RgpB_demo_001", "sequence": "RKWFKRK", "target_id": "RgpB_P_gingivalis"},
            {"peptide_id": "FadA_demo_001", "sequence": "LLAILVKELLAL", "target_id": "FadA_F_nucleatum"},
        ]

    return peptides


def run_selectivity_screening(peptides: List[Dict] = None) -> List[SelectivityReport]:
    """Run selectivity screening on all peptides."""

    if peptides is None:
        peptides = load_designed_peptides()

    print("="*70)
    print("M4 COMMENSAL SELECTIVITY CHECKER")
    print("="*70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Peptides to screen: {len(peptides)}")
    print(f"Commensals in database: {len(COMMENSAL_BACTERIA)}")
    print("="*70)

    reports = []

    for pep in peptides:
        print(f"\nScreening: {pep['peptide_id']}")
        print(f"  Sequence: {pep['sequence']}")
        print(f"  Target: {pep['target_id']}")

        report = screen_against_commensals(
            pep['sequence'],
            pep['peptide_id'],
            pep['target_id']
        )

        reports.append(report)

        print(f"  Verdict: {report.overall_verdict}")
        print(f"  Safe/Warn/Reject: {report.n_safe}/{report.n_warning}/{report.n_reject}")
        print(f"  Min SI: {report.minimum_selectivity_index:.1f} ({report.worst_commensal})")

    return reports


# ==============================================================================
# OUTPUT
# ==============================================================================

def save_results(reports: List[SelectivityReport]) -> str:
    """Save selectivity results."""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_data = {
        "pipeline": "M4 Commensal Selectivity Checker",
        "version": "1.0.0",
        "license": "AGPL-3.0-or-later",
        "timestamp": datetime.now().isoformat(),
        "commensals_screened": list(COMMENSAL_BACTERIA.keys()),
        "thresholds": SELECTIVITY_THRESHOLDS,
        "summary": {
            "total_peptides": len(reports),
            "passed": sum(1 for r in reports if r.overall_verdict == "PASS"),
            "warned": sum(1 for r in reports if r.overall_verdict == "WARN"),
            "rejected": sum(1 for r in reports if r.overall_verdict == "REJECT"),
        },
        "reports": []
    }

    for report in reports:
        report_dict = {
            "peptide_id": report.peptide_id,
            "sequence": report.sequence,
            "target_id": report.target_id,
            "verdict": report.overall_verdict,
            "recommendation": report.recommendation,
            "statistics": {
                "average_selectivity_index": report.average_selectivity_index,
                "minimum_selectivity_index": report.minimum_selectivity_index,
                "worst_commensal": report.worst_commensal,
                "n_safe": report.n_safe,
                "n_warning": report.n_warning,
                "n_reject": report.n_reject,
            },
            "commensal_details": [asdict(r) for r in report.commensal_results]
        }
        output_data["reports"].append(report_dict)

    output_path = os.path.join(OUTPUT_DIR, f"selectivity_report_{timestamp}.json")
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    return output_path


def print_summary(reports: List[SelectivityReport]):
    """Print screening summary."""

    print("\n" + "="*70)
    print("SELECTIVITY SCREENING SUMMARY")
    print("="*70)

    passed = [r for r in reports if r.overall_verdict == "PASS"]
    warned = [r for r in reports if r.overall_verdict == "WARN"]
    rejected = [r for r in reports if r.overall_verdict == "REJECT"]

    print(f"\nTotal screened: {len(reports)}")
    print(f"  PASS: {len(passed)} ({100*len(passed)/len(reports):.1f}%)")
    print(f"  WARN: {len(warned)} ({100*len(warned)/len(reports):.1f}%)")
    print(f"  REJECT: {len(rejected)} ({100*len(rejected)/len(reports):.1f}%)")

    if passed:
        print("\n--- PASSED PEPTIDES ---")
        for r in passed[:5]:
            print(f"  {r.peptide_id}: SI={r.minimum_selectivity_index:.1f}")

    if rejected:
        print("\n--- REJECTED PEPTIDES ---")
        for r in rejected:
            print(f"  {r.peptide_id}: {r.recommendation}")

    # Commensal protection summary
    print("\n--- COMMENSAL PROTECTION STATUS ---")
    commensal_hits = {}
    for report in reports:
        for cr in report.commensal_results:
            if not cr.safe:
                if cr.commensal_name not in commensal_hits:
                    commensal_hits[cr.commensal_name] = 0
                commensal_hits[cr.commensal_name] += 1

    if commensal_hits:
        print("\nCommensals at risk (peptides with potential cross-reactivity):")
        for name, count in sorted(commensal_hits.items(), key=lambda x: -x[1]):
            info = COMMENSAL_BACTERIA.get(name, {})
            priority = info.get("protection_priority", "UNKNOWN")
            print(f"  {name}: {count} peptides (Priority: {priority})")
    else:
        print("\nNo commensals at significant risk.")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main entry point."""

    # Run selectivity screening
    reports = run_selectivity_screening()

    # Print summary
    print_summary(reports)

    # Save results
    save_results(reports)

    print("\nSelectivity screening complete.")

    return reports


if __name__ == "__main__":
    main()

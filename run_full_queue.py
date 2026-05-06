#!/usr/bin/env python3
"""
Z² FULL QUEUE RUNNER - Systematic Discovery Pipeline
=====================================================

Runs all domains through the discovery engine and saves results
to OlympusFlow/discoveries/ for analysis.

Usage:
    python run_full_queue.py              # Run all domains
    python run_full_queue.py --domain X   # Run specific domain

Author: Carl Zimmerman
Date: May 6, 2026
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from run_discovery import TOPIC_KNOWLEDGE, run_discovery, Z_SQUARED, Z

# Output directory for OlympusFlow
OUTPUT_DIR = Path(__file__).parent / "OlympusFlow" / "discoveries"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Summary file
SUMMARY_FILE = OUTPUT_DIR / "z2_discoveries_summary.json"


def extract_z2_findings(result: Dict[str, Any]) -> List[Dict]:
    """Extract Z² pattern findings from discovery result."""
    z2_findings = []

    if "z2_findings" in result and result["z2_findings"]:
        for f in result["z2_findings"]:
            z2_findings.append({
                "name": f.name,
                "experimental_value": f.experimental_value,
                "formula": f.formula,
                "computed_value": f.computed_value,
                "percent_error": f.percent_error,
            })

    return z2_findings


def extract_best_matches(result: Dict[str, Any]) -> List[Dict]:
    """Extract best matches per constant."""
    best_matches = []

    if "by_target" in result:
        for target_name, findings in result["by_target"].items():
            if findings:
                best = min(findings, key=lambda x: x.percent_error)
                best_matches.append({
                    "name": target_name,
                    "experimental_value": best.experimental_value,
                    "formula": best.formula,
                    "computed_value": best.computed_value,
                    "percent_error": best.percent_error,
                    "has_z2": "Z²" in best.formula or "Z^2" in best.formula,
                    "has_pi": "π" in best.formula,
                })

    return best_matches


def run_domain(domain: str, verbose: bool = True) -> Dict[str, Any]:
    """Run discovery on a single domain and return structured results."""
    print(f"\n{'='*70}")
    print(f"RUNNING DOMAIN: {domain}")
    print(f"{'='*70}\n")

    result = run_discovery(domain, verbose=verbose, timeout=120)

    if "error" in result:
        return {"domain": domain, "error": result["error"]}

    # Extract structured findings
    z2_findings = extract_z2_findings(result)
    best_matches = extract_best_matches(result)

    # Count patterns
    z2_count = len(z2_findings)
    exact_matches = sum(1 for m in best_matches if m["percent_error"] < 0.01)
    sub_percent = sum(1 for m in best_matches if m["percent_error"] < 1.0)

    domain_result = {
        "domain": domain,
        "description": TOPIC_KNOWLEDGE.get(domain, {}).get("description", ""),
        "timestamp": datetime.datetime.now().isoformat(),
        "constants_searched": len(TOPIC_KNOWLEDGE.get(domain, {}).get("constants", [])),
        "z2_patterns_found": z2_count,
        "exact_matches": exact_matches,
        "sub_percent_matches": sub_percent,
        "z2_findings": z2_findings,
        "best_matches": best_matches,
        "runtime_seconds": result.get("briareus_result", {}).runtime_seconds if hasattr(result.get("briareus_result", {}), "runtime_seconds") else 0,
    }

    return domain_result


def save_domain_result(result: Dict[str, Any]):
    """Save domain result to JSON file."""
    domain = result["domain"]
    filename = OUTPUT_DIR / f"{domain}_discoveries.json"

    with open(filename, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\nSaved results to: {filename}")


def update_summary(all_results: List[Dict[str, Any]]):
    """Update the master summary file."""
    # Load existing summary if present
    if SUMMARY_FILE.exists():
        with open(SUMMARY_FILE) as f:
            summary = json.load(f)
    else:
        summary = {
            "created": datetime.datetime.now().isoformat(),
            "z_squared": Z_SQUARED,
            "z": Z,
            "domains_processed": [],
            "total_z2_discoveries": [],
            "statistics": {},
        }

    summary["updated"] = datetime.datetime.now().isoformat()

    # Aggregate all Z² discoveries
    all_z2 = []
    for result in all_results:
        if "z2_findings" in result:
            for finding in result["z2_findings"]:
                finding["domain"] = result["domain"]
                all_z2.append(finding)

        # Track processed domains
        if result["domain"] not in summary["domains_processed"]:
            summary["domains_processed"].append(result["domain"])

    # Sort by error (best first)
    all_z2.sort(key=lambda x: x.get("percent_error", 100))
    summary["total_z2_discoveries"] = all_z2

    # Statistics
    summary["statistics"] = {
        "total_domains": len(summary["domains_processed"]),
        "total_z2_patterns": len(all_z2),
        "sub_0.1_percent": sum(1 for x in all_z2 if x.get("percent_error", 100) < 0.1),
        "sub_0.5_percent": sum(1 for x in all_z2 if x.get("percent_error", 100) < 0.5),
        "sub_1.0_percent": sum(1 for x in all_z2 if x.get("percent_error", 100) < 1.0),
    }

    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nUpdated summary: {SUMMARY_FILE}")
    print(f"Total Z² discoveries: {len(all_z2)}")
    print(f"  <0.1% error: {summary['statistics']['sub_0.1_percent']}")
    print(f"  <0.5% error: {summary['statistics']['sub_0.5_percent']}")
    print(f"  <1.0% error: {summary['statistics']['sub_1.0_percent']}")


def run_all_domains(verbose: bool = True):
    """Run discovery on all domains in the knowledge base."""
    domains = list(TOPIC_KNOWLEDGE.keys())
    print(f"\n{'#'*70}")
    print(f"# Z² FULL QUEUE RUNNER")
    print(f"# Domains to process: {len(domains)}")
    print(f"# Output directory: {OUTPUT_DIR}")
    print(f"{'#'*70}\n")

    all_results = []

    for i, domain in enumerate(domains, 1):
        print(f"\n[{i}/{len(domains)}] Processing: {domain}")

        try:
            result = run_domain(domain, verbose=verbose)
            save_domain_result(result)
            all_results.append(result)

            # Print Z² highlights
            if result.get("z2_findings"):
                print(f"\n  Z² HIGHLIGHTS for {domain}:")
                for finding in result["z2_findings"][:5]:
                    print(f"    {finding['name']}: {finding['formula']} ({finding['percent_error']:.4f}%)")

        except Exception as e:
            print(f"  ERROR: {e}")
            all_results.append({"domain": domain, "error": str(e)})

    # Update master summary
    update_summary(all_results)

    print(f"\n{'#'*70}")
    print(f"# QUEUE COMPLETE")
    print(f"# Processed: {len(all_results)} domains")
    print(f"# Results saved to: {OUTPUT_DIR}")
    print(f"{'#'*70}\n")

    return all_results


def print_top_discoveries():
    """Print the top Z² discoveries from the summary."""
    if not SUMMARY_FILE.exists():
        print("No summary file found. Run discoveries first.")
        return

    with open(SUMMARY_FILE) as f:
        summary = json.load(f)

    print(f"\n{'='*70}")
    print("TOP Z² DISCOVERIES (by accuracy)")
    print(f"{'='*70}\n")

    for i, finding in enumerate(summary["total_z2_discoveries"][:30], 1):
        print(f"{i:2}. [{finding.get('domain', '?'):20}] {finding['name'][:30]:30}")
        print(f"    {finding['formula']} = {finding['computed_value']:.6f}")
        print(f"    Experimental: {finding['experimental_value']:.6f}, Error: {finding['percent_error']:.4f}%")
        print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Z² Full Queue Runner")
    parser.add_argument("--domain", type=str, help="Run specific domain only")
    parser.add_argument("--quiet", action="store_true", help="Less output")
    parser.add_argument("--summary", action="store_true", help="Print top discoveries")

    args = parser.parse_args()

    if args.summary:
        print_top_discoveries()
    elif args.domain:
        result = run_domain(args.domain, verbose=not args.quiet)
        save_domain_result(result)
        update_summary([result])
    else:
        run_all_domains(verbose=not args.quiet)
        print_top_discoveries()

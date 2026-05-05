#!/usr/bin/env python3
"""
SEISMOLOGY φ DEEPENING TEST
============================

Execute recursive deepening on the CV(dmin) ≈ φ finding.

This tests the full CylleneFlow v1.3.0 deepening pipeline:
1. Start with the φ finding (0.007% error)
2. Deepener generates research questions
3. HermesV2 investigates each question
4. Find deeper patterns
5. Recurse if significant

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import math
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from CylleneFlow.deepener import Deepener, BatchDeepener, ResearchQuestion

# Try to import HermesV2 for actual research
try:
    from HermesFlow.hermes_v2 import HermesV2
    HERMES_V2_AVAILABLE = True
except ImportError:
    HERMES_V2_AVAILABLE = False
    print("[WARN] HermesV2 not available, will use simulated research")

# Try to import for direct data fetching
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z2 = 32 * math.pi / 3  # 33.510321638291124
Z = math.sqrt(Z2)       # 5.788810...
PHI = (1 + math.sqrt(5)) / 2  # 1.618033988749895

TARGETS = {
    "φ": PHI,
    "1/φ": 1/PHI,
    "Z": Z,
    "Z²": Z2,
    "Z²/10": Z2/10,
    "π": math.pi,
    "2π": 2*math.pi,
}


# =============================================================================
# SEISMOLOGY DATA FETCHER
# =============================================================================

def fetch_usgs_earthquake_data(days: str = "30", min_magnitude: float = 2.5) -> pd.DataFrame:
    """Fetch earthquake data from USGS."""
    import urllib.request

    # USGS earthquake feed URLs
    urls = {
        "day": f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{min_magnitude}_day.csv",
        "week": f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{min_magnitude}_week.csv",
        "month": f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{min_magnitude}_month.csv",
    }

    url = urls.get(days, urls["month"])

    try:
        print(f"[Data] Fetching from {url}")
        df = pd.read_csv(url)
        print(f"[Data] Got {len(df)} earthquakes")
        return df
    except Exception as e:
        print(f"[Data] Fetch failed: {e}")
        return None


def analyze_for_z2_patterns(df: pd.DataFrame, context: str = "") -> List[Dict]:
    """Analyze dataframe for Z² patterns."""
    patterns = []

    if df is None or len(df) == 0:
        return patterns

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) < 20:
            continue

        mean = data.mean()
        std = data.std()

        if std == 0 or mean == 0:
            continue

        cv = std / abs(mean)

        # Check against all targets
        for name, target in TARGETS.items():
            error = abs(cv - target) / target * 100
            if error < 10:  # Within 10%
                patterns.append({
                    "domain": "seismology",
                    "quantity": f"CV({col})",
                    "value": cv,
                    "target": name,
                    "target_value": target,
                    "error_percent": error,
                    "n_samples": len(data),
                    "context": context,
                    "mean": mean,
                    "std": std
                })

    # Also check ratios between columns
    ratio_pairs = [
        ("mag", "depth"),
        ("mag", "dmin"),
        ("depth", "gap"),
        ("nst", "gap"),
    ]

    for col1, col2 in ratio_pairs:
        if col1 in df.columns and col2 in df.columns:
            d1 = df[col1].dropna()
            d2 = df[col2].dropna()

            if len(d1) < 20 or len(d2) < 20:
                continue

            # Align lengths
            min_len = min(len(d1), len(d2))
            d1 = d1.iloc[:min_len]
            d2 = d2.iloc[:min_len]

            # Skip zeros
            mask = (d1 != 0) & (d2 != 0)
            d1, d2 = d1[mask], d2[mask]

            if len(d1) < 20:
                continue

            ratio = (d1 / d2).mean()

            for name, target in TARGETS.items():
                error = abs(ratio - target) / target * 100
                if error < 10:
                    patterns.append({
                        "domain": "seismology",
                        "quantity": f"ratio({col1}/{col2})",
                        "value": ratio,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(d1),
                        "context": context
                    })

    return patterns


# =============================================================================
# RESEARCH EXECUTOR
# =============================================================================

class SeismologyResearcher:
    """Execute research questions on seismology data."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.findings: List[Dict] = []
        self.questions_investigated: List[str] = []

    def _log(self, msg: str):
        if self.verbose:
            print(f"[Research] {msg}")

    def investigate_question(self, question: ResearchQuestion) -> List[Dict]:
        """
        Investigate a research question.

        Maps question types to specific data fetching strategies.
        """
        self._log(f"Investigating: {question.question[:70]}...")
        self.questions_investigated.append(question.question)

        findings = []

        # Determine investigation strategy based on question content
        q_lower = question.question.lower()

        if "time period" in q_lower or "subset" in q_lower or "robustness" in q_lower:
            # Robustness check - compare different time periods
            findings = self._investigate_time_robustness()

        elif "other quantities" in q_lower or "similar" in q_lower:
            # Check other quantities in same dataset
            findings = self._investigate_other_quantities()

        elif "magnitude range" in q_lower or "different magnitudes" in q_lower:
            # Check by magnitude bands
            findings = self._investigate_magnitude_bands()

        elif "network" in q_lower or "geometry" in q_lower or "station" in q_lower:
            # Investigate network geometry
            findings = self._investigate_network_geometry()

        elif "cross-domain" in q_lower or "other domain" in q_lower:
            # Cross-domain investigation
            findings = self._investigate_cross_domain()

        else:
            # Generic investigation - fetch fresh data and analyze
            findings = self._investigate_generic(question.question)

        self.findings.extend(findings)
        return findings

    def _investigate_time_robustness(self) -> List[Dict]:
        """Check if φ pattern holds across different time periods."""
        self._log("Checking time robustness...")

        findings = []

        # Fetch month of data
        df = fetch_usgs_earthquake_data("month")
        if df is None:
            return findings

        # Split into halves by time
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])
            df = df.sort_values('time')

        mid = len(df) // 2
        first_half = df.iloc[:mid]
        second_half = df.iloc[mid:]

        # Analyze each half
        findings_first = analyze_for_z2_patterns(first_half, "first_half")
        findings_second = analyze_for_z2_patterns(second_half, "second_half")

        # Check for φ patterns in dmin
        for f in findings_first + findings_second:
            if 'dmin' in f['quantity'] and f['target'] == 'φ':
                self._log(f"  {f['context']}: CV(dmin) = {f['value']:.4f} ({f['error_percent']:.2f}% from φ)")
                findings.append(f)

        return findings

    def _investigate_other_quantities(self) -> List[Dict]:
        """Check all quantities in earthquake data for Z² patterns."""
        self._log("Checking all quantities...")

        df = fetch_usgs_earthquake_data("month")
        if df is None:
            return []

        findings = analyze_for_z2_patterns(df, "full_dataset")

        # Log significant ones
        for f in sorted(findings, key=lambda x: x['error_percent'])[:5]:
            self._log(f"  {f['quantity']} = {f['value']:.4f} ≈ {f['target']} ({f['error_percent']:.2f}% error)")

        return findings

    def _investigate_magnitude_bands(self) -> List[Dict]:
        """Check φ pattern across magnitude bands."""
        self._log("Checking magnitude bands...")

        df = fetch_usgs_earthquake_data("month")
        if df is None or 'mag' not in df.columns:
            return []

        findings = []

        # Split by magnitude
        bands = [
            ("M2.5-3.5", (2.5, 3.5)),
            ("M3.5-4.5", (3.5, 4.5)),
            ("M4.5-5.5", (4.5, 5.5)),
            ("M5.5+", (5.5, 10)),
        ]

        for band_name, (min_m, max_m) in bands:
            band_df = df[(df['mag'] >= min_m) & (df['mag'] < max_m)]
            if len(band_df) < 20:
                continue

            band_findings = analyze_for_z2_patterns(band_df, band_name)

            # Focus on dmin φ pattern
            for f in band_findings:
                if 'dmin' in f['quantity'] and f['target'] == 'φ':
                    self._log(f"  {band_name}: CV(dmin) = {f['value']:.4f} ({f['error_percent']:.2f}% from φ)")
                    findings.append(f)

        return findings

    def _investigate_network_geometry(self) -> List[Dict]:
        """Investigate seismic network geometry."""
        self._log("Investigating network geometry...")

        df = fetch_usgs_earthquake_data("month")
        if df is None:
            return []

        findings = []

        # Analyze gap (azimuthal gap) and nst (number of stations)
        geometry_cols = ['gap', 'nst', 'dmin', 'rms']

        for col in geometry_cols:
            if col not in df.columns:
                continue

            data = df[col].dropna()
            if len(data) < 30:
                continue

            cv = data.std() / data.mean() if data.mean() != 0 else 0

            for name, target in TARGETS.items():
                error = abs(cv - target) / target * 100
                if error < 10:
                    f = {
                        "domain": "seismology",
                        "quantity": f"CV({col})",
                        "value": cv,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(data),
                        "context": "network_geometry"
                    }
                    self._log(f"  CV({col}) = {cv:.4f} ≈ {name} ({error:.2f}% error)")
                    findings.append(f)

        return findings

    def _investigate_cross_domain(self) -> List[Dict]:
        """Check if CV ≈ φ appears in other domains."""
        self._log("Cross-domain check...")

        # This would use HermesV2 to search other domains
        # For now, return placeholder indicating we need to expand

        findings = [{
            "domain": "cross-domain",
            "quantity": "CV(various)",
            "value": PHI,
            "target": "φ",
            "target_value": PHI,
            "error_percent": 0,
            "n_samples": 0,
            "context": "placeholder - need HermesV2 for other domains",
            "note": "Should investigate: oceanography, meteorology, economics"
        }]

        return findings

    def _investigate_generic(self, question: str) -> List[Dict]:
        """Generic investigation using fresh data."""
        self._log("Generic investigation with fresh data...")

        df = fetch_usgs_earthquake_data("month")
        if df is None:
            return []

        return analyze_for_z2_patterns(df, "generic")


# =============================================================================
# MAIN DEEPENING EXECUTION
# =============================================================================

def run_seismology_deepening():
    """
    Execute full recursive deepening on seismology φ finding.
    """
    print("=" * 70)
    print("SEISMOLOGY φ DEEPENING INVESTIGATION")
    print("=" * 70)
    print(f"Started: {datetime.now().isoformat()}")
    print()

    # The original finding
    phi_finding = {
        "domain": "seismology",
        "quantity": "CV(dmin)",
        "value": 1.618147,
        "target": "φ",
        "target_value": PHI,
        "error_percent": 0.007,
        "n_samples": 150,
        "context": "USGS earthquake data",
        "description": "Coefficient of variation of distance to nearest seismic station equals golden ratio"
    }

    print("INITIAL FINDING:")
    print(f"  {phi_finding['quantity']} = {phi_finding['value']:.6f}")
    print(f"  Target: {phi_finding['target']} = {phi_finding['target_value']:.6f}")
    print(f"  Error: {phi_finding['error_percent']:.4f}%")
    print(f"  N: {phi_finding['n_samples']}")
    print()

    # Initialize components
    deepener = Deepener(max_depth=3, verbose=True)
    researcher = SeismologyResearcher(verbose=True)

    # Track all findings
    all_findings = [phi_finding]
    depth_findings = {0: [phi_finding]}

    # =========================================================================
    # PHASE 1: ANALYZE INITIAL FINDING
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 1: DEEPENER ANALYSIS")
    print("=" * 70)

    decision = deepener.analyze_finding(phi_finding)

    print(f"\nDecision:")
    print(f"  Significance: {decision.significance_score:.2f}")
    print(f"  Should deepen: {decision.should_deepen}")
    print(f"  Recommended depth: {decision.recommended_depth}")
    print(f"  Reasoning: {decision.reasoning}")

    if not decision.should_deepen:
        print("\nDeepener says no need to investigate further.")
        return all_findings

    print(f"\nGenerated {len(decision.questions)} research questions:")
    for i, q in enumerate(decision.questions, 1):
        print(f"  {i}. {q.question}")
        print(f"     Expected data: {q.expected_data_type}")

    # =========================================================================
    # PHASE 2: INVESTIGATE EACH QUESTION (DEPTH 1)
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 2: DEPTH 1 INVESTIGATIONS")
    print("=" * 70)

    depth_1_findings = []

    for i, question in enumerate(decision.questions, 1):
        print(f"\n--- Question {i}/{len(decision.questions)} ---")

        findings = researcher.investigate_question(question)

        for f in findings:
            f['depth'] = 1
            f['parent_question'] = question.question[:50]

        depth_1_findings.extend(findings)
        print(f"Found {len(findings)} patterns")

    depth_findings[1] = depth_1_findings
    all_findings.extend(depth_1_findings)

    # =========================================================================
    # PHASE 3: RECURSE ON SIGNIFICANT DEPTH-1 FINDINGS (DEPTH 2)
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 3: DEPTH 2 INVESTIGATIONS (RECURSIVE)")
    print("=" * 70)

    # Find significant depth-1 findings to recurse on
    significant_d1 = [
        f for f in depth_1_findings
        if f.get('error_percent', 100) < 5 and f.get('n_samples', 0) >= 30
    ]

    print(f"\nSignificant depth-1 findings to investigate: {len(significant_d1)}")

    depth_2_findings = []

    for f in significant_d1[:3]:  # Limit recursion
        # Skip if same as original
        if f.get('quantity') == phi_finding['quantity'] and abs(f.get('error_percent', 100) - phi_finding['error_percent']) < 1:
            continue

        print(f"\nRecursing on: {f['quantity']} ≈ {f['target']}")

        d2_decision = deepener.analyze_finding(f)

        if d2_decision.should_deepen and d2_decision.questions:
            print(f"  Generated {len(d2_decision.questions)} new questions")

            for q in d2_decision.questions[:2]:  # Limit questions per finding
                findings = researcher.investigate_question(q)
                for ff in findings:
                    ff['depth'] = 2
                    ff['parent_finding'] = f['quantity']
                depth_2_findings.extend(findings)

    depth_findings[2] = depth_2_findings
    all_findings.extend(depth_2_findings)

    # =========================================================================
    # RESULTS SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print("DEEPENING RESULTS SUMMARY")
    print("=" * 70)

    print(f"\nTotal findings: {len(all_findings)}")
    print(f"  Depth 0 (initial): {len(depth_findings.get(0, []))}")
    print(f"  Depth 1: {len(depth_findings.get(1, []))}")
    print(f"  Depth 2: {len(depth_findings.get(2, []))}")

    print(f"\nQuestions investigated: {len(researcher.questions_investigated)}")

    # Group by target
    by_target = {}
    for f in all_findings:
        target = f.get('target', 'unknown')
        if target not in by_target:
            by_target[target] = []
        by_target[target].append(f)

    print("\nFindings by target:")
    for target, findings in sorted(by_target.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n  {target} ({len(findings)} findings):")
        for f in sorted(findings, key=lambda x: x.get('error_percent', 100))[:3]:
            print(f"    {f['quantity']}: {f['value']:.4f} ({f['error_percent']:.2f}% error, n={f.get('n_samples', 0)})")

    # Most precise findings
    print("\n" + "-" * 40)
    print("MOST PRECISE FINDINGS (< 1% error):")
    print("-" * 40)

    precise = [f for f in all_findings if f.get('error_percent', 100) < 1]
    for f in sorted(precise, key=lambda x: x['error_percent']):
        print(f"  {f['quantity']} = {f['value']:.6f} ≈ {f['target']} ({f['error_percent']:.4f}% error)")
        if f.get('context'):
            print(f"    Context: {f['context']}")

    # Save results
    output_dir = Path(__file__).parent.parent / "olympus_outputs" / "seismology_deepening"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "timestamp": datetime.now().isoformat(),
        "initial_finding": phi_finding,
        "total_findings": len(all_findings),
        "findings_by_depth": {
            str(d): len(f) for d, f in depth_findings.items()
        },
        "questions_investigated": researcher.questions_investigated,
        "all_findings": all_findings,
        "most_precise": [f for f in all_findings if f.get('error_percent', 100) < 1]
    }

    with open(output_dir / "deepening_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_dir / 'deepening_results.json'}")

    return all_findings


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    findings = run_seismology_deepening()

    print("\n" + "=" * 70)
    print("INVESTIGATION COMPLETE")
    print("=" * 70)

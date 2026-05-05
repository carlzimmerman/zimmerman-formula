#!/usr/bin/env python3
"""
OCEANOGRAPHY DEEPENING TEST
============================

Execute recursive deepening on oceanography data (ONI - Oceanic Niño Index).

Tests the full CylleneFlow v1.3.0 deepening pipeline on ocean/climate data.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import os
import sys
import math
import json
import time
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np

from CylleneFlow.deepener import Deepener, BatchDeepener, ResearchQuestion

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
    "√2": math.sqrt(2),
    "e": math.e,
}


# =============================================================================
# OCEANOGRAPHY DATA FETCHERS
# =============================================================================

def fetch_oni_data() -> pd.DataFrame:
    """Fetch Oceanic Niño Index data from NOAA PSL."""
    url = "https://psl.noaa.gov/data/correlation/oni.data"

    print(f"[Data] Fetching ONI from {url}")

    try:
        response = urllib.request.urlopen(url, timeout=30)
        content = response.read().decode('utf-8')

        # Parse the fixed-width format
        lines = content.strip().split('\n')

        # Find data start (skip header lines)
        data_lines = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 13:
                try:
                    year = int(parts[0])
                    if 1900 < year < 2100:
                        data_lines.append(parts)
                except:
                    continue

        # Create DataFrame
        columns = ['YEAR', 'DJ', 'JF', 'FM', 'MA', 'AM', 'MJ', 'JJ', 'JA', 'AS', 'SO', 'ON', 'ND']
        df = pd.DataFrame(data_lines, columns=columns)

        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Replace missing values (-99.9) with NaN
        df = df.replace(-99.9, np.nan)
        df = df.replace(-99.90, np.nan)

        print(f"[Data] Got {len(df)} years of ONI data ({df['YEAR'].min()}-{df['YEAR'].max()})")
        return df

    except Exception as e:
        print(f"[Data] Fetch failed: {e}")
        return None


def fetch_sst_data() -> pd.DataFrame:
    """Fetch Sea Surface Temperature anomaly data."""
    # Try multiple NOAA sources
    urls = [
        "https://psl.noaa.gov/data/correlation/sstoi.nino34.data",  # Niño 3.4 SST
        "https://psl.noaa.gov/data/correlation/nina34.data",  # Alternative
    ]

    for url in urls:
        try:
            print(f"[Data] Trying SST from {url}")
            response = urllib.request.urlopen(url, timeout=30)
            content = response.read().decode('utf-8')

            lines = content.strip().split('\n')
            data_lines = []

            for line in lines:
                parts = line.split()
                if len(parts) >= 13:
                    try:
                        year = int(parts[0])
                        if 1900 < year < 2100:
                            data_lines.append(parts)
                    except:
                        continue

            if data_lines:
                columns = ['YEAR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                          'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
                df = pd.DataFrame(data_lines, columns=columns)

                for col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

                df = df.replace(-99.9, np.nan)
                df = df.replace(-99.90, np.nan)

                print(f"[Data] Got {len(df)} years of SST data")
                return df

        except Exception as e:
            print(f"[Data] {url} failed: {e}")
            continue

    return None


def fetch_pdo_data() -> pd.DataFrame:
    """Fetch Pacific Decadal Oscillation data."""
    url = "https://psl.noaa.gov/data/correlation/pdo.data"

    try:
        print(f"[Data] Fetching PDO from {url}")
        response = urllib.request.urlopen(url, timeout=30)
        content = response.read().decode('utf-8')

        lines = content.strip().split('\n')
        data_lines = []

        for line in lines:
            parts = line.split()
            if len(parts) >= 13:
                try:
                    year = int(parts[0])
                    if 1900 < year < 2100:
                        data_lines.append(parts)
                except:
                    continue

        if data_lines:
            columns = ['YEAR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                      'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            df = pd.DataFrame(data_lines, columns=columns)

            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            df = df.replace(-99.9, np.nan)
            df = df.replace(-9.90, np.nan)

            print(f"[Data] Got {len(df)} years of PDO data")
            return df

    except Exception as e:
        print(f"[Data] PDO fetch failed: {e}")

    return None


def fetch_soi_data() -> pd.DataFrame:
    """Fetch Southern Oscillation Index data."""
    url = "https://psl.noaa.gov/data/correlation/soi.data"

    try:
        print(f"[Data] Fetching SOI from {url}")
        response = urllib.request.urlopen(url, timeout=30)
        content = response.read().decode('utf-8')

        lines = content.strip().split('\n')
        data_lines = []

        for line in lines:
            parts = line.split()
            if len(parts) >= 13:
                try:
                    year = int(parts[0])
                    if 1900 < year < 2100:
                        data_lines.append(parts)
                except:
                    continue

        if data_lines:
            columns = ['YEAR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                      'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            df = pd.DataFrame(data_lines, columns=columns)

            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            df = df.replace(-99.9, np.nan)
            df = df.replace(-99.90, np.nan)

            print(f"[Data] Got {len(df)} years of SOI data")
            return df

    except Exception as e:
        print(f"[Data] SOI fetch failed: {e}")

    return None


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_for_z2_patterns(df: pd.DataFrame, context: str = "", domain: str = "oceanography") -> List[Dict]:
    """Analyze dataframe for Z² patterns."""
    patterns = []

    if df is None or len(df) == 0:
        return patterns

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    month_cols = [c for c in numeric_cols if c != 'YEAR']

    # Analyze each column's CV
    for col in month_cols:
        data = df[col].dropna()
        if len(data) < 20:
            continue

        mean = data.mean()
        std = data.std()

        if std == 0:
            continue

        # For anomaly data, mean can be near zero, use absolute CV
        if abs(mean) < 0.1:
            # Use std directly for anomaly data
            cv = std
        else:
            cv = std / abs(mean)

        for name, target in TARGETS.items():
            error = abs(cv - target) / target * 100
            if error < 10:
                patterns.append({
                    "domain": domain,
                    "quantity": f"CV({col})" if abs(mean) >= 0.1 else f"STD({col})",
                    "value": cv if abs(mean) >= 0.1 else std,
                    "target": name,
                    "target_value": target,
                    "error_percent": error,
                    "n_samples": len(data),
                    "context": context,
                    "mean": mean,
                    "std": std
                })

    # Analyze full time series (all months combined)
    all_values = []
    for col in month_cols:
        all_values.extend(df[col].dropna().tolist())

    if len(all_values) >= 50:
        all_data = pd.Series(all_values)
        mean = all_data.mean()
        std = all_data.std()

        # For anomaly data centered near zero
        for name, target in TARGETS.items():
            # Check std against targets
            error = abs(std - target) / target * 100
            if error < 10:
                patterns.append({
                    "domain": domain,
                    "quantity": "STD(all_months)",
                    "value": std,
                    "target": name,
                    "target_value": target,
                    "error_percent": error,
                    "n_samples": len(all_values),
                    "context": context,
                    "mean": mean,
                    "std": std
                })

    # Analyze inter-annual variability
    if 'YEAR' in df.columns and len(month_cols) >= 12:
        annual_means = df[month_cols].mean(axis=1)
        annual_std = annual_means.std()
        annual_mean = annual_means.mean()

        if annual_std > 0:
            for name, target in TARGETS.items():
                error = abs(annual_std - target) / target * 100
                if error < 10:
                    patterns.append({
                        "domain": domain,
                        "quantity": "STD(annual_mean)",
                        "value": annual_std,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(annual_means),
                        "context": context
                    })

    # Analyze ratios between consecutive periods
    for i, col1 in enumerate(month_cols[:-1]):
        col2 = month_cols[i+1]
        d1 = df[col1].dropna()
        d2 = df[col2].dropna()

        if len(d1) < 20 or len(d2) < 20:
            continue

        # Correlation between consecutive months
        min_len = min(len(d1), len(d2))
        corr = np.corrcoef(d1.iloc[:min_len], d2.iloc[:min_len])[0, 1]

        if not np.isnan(corr):
            for name, target in TARGETS.items():
                if target < 1:  # Only check targets < 1 for correlations
                    error = abs(corr - target) / target * 100
                    if error < 10:
                        patterns.append({
                            "domain": domain,
                            "quantity": f"corr({col1},{col2})",
                            "value": corr,
                            "target": name,
                            "target_value": target,
                            "error_percent": error,
                            "n_samples": min_len,
                            "context": context
                        })

    return patterns


# =============================================================================
# OCEANOGRAPHY RESEARCHER
# =============================================================================

class OceanographyResearcher:
    """Execute research questions on oceanography data."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.findings: List[Dict] = []
        self.questions_investigated: List[str] = []
        self.datasets_fetched: Dict[str, pd.DataFrame] = {}

    def _log(self, msg: str):
        if self.verbose:
            print(f"[Research] {msg}")

    def _ensure_data(self):
        """Fetch all oceanography datasets."""
        if 'oni' not in self.datasets_fetched:
            self.datasets_fetched['oni'] = fetch_oni_data()
        if 'sst' not in self.datasets_fetched:
            self.datasets_fetched['sst'] = fetch_sst_data()
        if 'pdo' not in self.datasets_fetched:
            self.datasets_fetched['pdo'] = fetch_pdo_data()
        if 'soi' not in self.datasets_fetched:
            self.datasets_fetched['soi'] = fetch_soi_data()

    def investigate_question(self, question: ResearchQuestion) -> List[Dict]:
        """Investigate a research question."""
        self._log(f"Investigating: {question.question[:70]}...")
        self.questions_investigated.append(question.question)

        self._ensure_data()

        findings = []
        q_lower = question.question.lower()

        if "time period" in q_lower or "subset" in q_lower or "robustness" in q_lower:
            findings = self._investigate_time_robustness()
        elif "other quantities" in q_lower or "similar" in q_lower or "other" in q_lower:
            findings = self._investigate_all_indices()
        elif "cross-domain" in q_lower:
            findings = self._investigate_cross_domain()
        elif "mechanism" in q_lower or "why" in q_lower:
            findings = self._investigate_mechanisms()
        else:
            findings = self._investigate_generic()

        self.findings.extend(findings)
        return findings

    def _investigate_time_robustness(self) -> List[Dict]:
        """Check patterns across different time periods."""
        self._log("Checking time robustness across decades...")

        findings = []

        oni = self.datasets_fetched.get('oni')
        if oni is None:
            return findings

        # Split by decades
        decades = [
            ("1950s", (1950, 1960)),
            ("1960s", (1960, 1970)),
            ("1970s", (1970, 1980)),
            ("1980s", (1980, 1990)),
            ("1990s", (1990, 2000)),
            ("2000s", (2000, 2010)),
            ("2010s", (2010, 2020)),
        ]

        for decade_name, (start, end) in decades:
            decade_df = oni[(oni['YEAR'] >= start) & (oni['YEAR'] < end)]
            if len(decade_df) < 5:
                continue

            decade_findings = analyze_for_z2_patterns(decade_df, decade_name)

            for f in decade_findings:
                self._log(f"  {decade_name}: {f['quantity']} = {f['value']:.4f} ≈ {f['target']} ({f['error_percent']:.2f}%)")

            findings.extend(decade_findings)

        return findings

    def _investigate_all_indices(self) -> List[Dict]:
        """Check all ocean/climate indices for patterns."""
        self._log("Checking all ocean indices...")

        findings = []

        datasets = {
            "ONI": self.datasets_fetched.get('oni'),
            "SST": self.datasets_fetched.get('sst'),
            "PDO": self.datasets_fetched.get('pdo'),
            "SOI": self.datasets_fetched.get('soi'),
        }

        for name, df in datasets.items():
            if df is None:
                continue

            self._log(f"  Analyzing {name}...")
            index_findings = analyze_for_z2_patterns(df, name)

            for f in sorted(index_findings, key=lambda x: x['error_percent'])[:3]:
                self._log(f"    {f['quantity']} = {f['value']:.4f} ≈ {f['target']} ({f['error_percent']:.2f}%)")

            findings.extend(index_findings)

        return findings

    def _investigate_cross_domain(self) -> List[Dict]:
        """Cross-domain placeholder."""
        self._log("Cross-domain investigation...")
        return [{
            "domain": "cross-domain",
            "quantity": "placeholder",
            "value": 0,
            "target": "N/A",
            "target_value": 0,
            "error_percent": 100,
            "n_samples": 0,
            "context": "Need HermesV2 for other domains",
            "note": "Should compare with seismology, meteorology patterns"
        }]

    def _investigate_mechanisms(self) -> List[Dict]:
        """Investigate physical mechanisms."""
        self._log("Investigating mechanisms via correlations...")

        findings = []

        # Check correlations between indices
        oni = self.datasets_fetched.get('oni')
        soi = self.datasets_fetched.get('soi')
        pdo = self.datasets_fetched.get('pdo')

        if oni is not None and soi is not None:
            # ONI-SOI correlation
            month_cols = [c for c in oni.columns if c != 'YEAR']

            for col in month_cols[:3]:  # Check first few months
                oni_data = oni[col].dropna()
                soi_data = soi[col].dropna() if col in soi.columns else None

                if soi_data is not None and len(oni_data) > 20 and len(soi_data) > 20:
                    min_len = min(len(oni_data), len(soi_data))
                    corr = np.corrcoef(oni_data.iloc[:min_len], soi_data.iloc[:min_len])[0, 1]

                    if not np.isnan(corr):
                        for name, target in TARGETS.items():
                            error = abs(abs(corr) - target) / target * 100
                            if error < 10:
                                findings.append({
                                    "domain": "oceanography",
                                    "quantity": f"corr(ONI_{col},SOI_{col})",
                                    "value": corr,
                                    "target": name,
                                    "target_value": target,
                                    "error_percent": error,
                                    "n_samples": min_len,
                                    "context": "ONI-SOI correlation"
                                })

        return findings

    def _investigate_generic(self) -> List[Dict]:
        """Generic investigation."""
        self._log("Generic analysis...")

        findings = []
        for name, df in self.datasets_fetched.items():
            if df is not None:
                findings.extend(analyze_for_z2_patterns(df, name))

        return findings


# =============================================================================
# MAIN
# =============================================================================

def run_oceanography_deepening():
    """Execute full recursive deepening on oceanography data."""
    print("=" * 70)
    print("OCEANOGRAPHY DEEPENING INVESTIGATION")
    print("=" * 70)
    print(f"Started: {datetime.now().isoformat()}")
    print()

    # First, fetch and analyze ONI data to find initial patterns
    print("PHASE 0: INITIAL DATA SCAN")
    print("-" * 40)

    oni_df = fetch_oni_data()
    if oni_df is None:
        print("ERROR: Could not fetch ONI data")
        return []

    initial_findings = analyze_for_z2_patterns(oni_df, "initial_scan")

    print(f"\nInitial scan found {len(initial_findings)} patterns:")
    for f in sorted(initial_findings, key=lambda x: x['error_percent'])[:5]:
        print(f"  {f['quantity']} = {f['value']:.4f} ≈ {f['target']} ({f['error_percent']:.2f}% error)")

    if not initial_findings:
        print("No initial patterns found - fetching more datasets...")
        # Try other indices
        pdo_df = fetch_pdo_data()
        soi_df = fetch_soi_data()

        if pdo_df is not None:
            initial_findings.extend(analyze_for_z2_patterns(pdo_df, "PDO"))
        if soi_df is not None:
            initial_findings.extend(analyze_for_z2_patterns(soi_df, "SOI"))

    if not initial_findings:
        print("No Z² patterns found in oceanography data")
        return []

    # Select most significant finding for deepening
    best_finding = min(initial_findings, key=lambda x: x['error_percent'])

    print(f"\nBEST INITIAL FINDING:")
    print(f"  {best_finding['quantity']} = {best_finding['value']:.6f}")
    print(f"  Target: {best_finding['target']} = {best_finding['target_value']:.6f}")
    print(f"  Error: {best_finding['error_percent']:.4f}%")
    print(f"  N: {best_finding.get('n_samples', 'N/A')}")

    # Initialize deepening
    deepener = Deepener(max_depth=3, verbose=True)
    researcher = OceanographyResearcher(verbose=True)

    all_findings = initial_findings.copy()
    depth_findings = {0: initial_findings}

    # =========================================================================
    # PHASE 1: ANALYZE BEST FINDING
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 1: DEEPENER ANALYSIS")
    print("=" * 70)

    decision = deepener.analyze_finding(best_finding)

    print(f"\nDecision:")
    print(f"  Significance: {decision.significance_score:.2f}")
    print(f"  Should deepen: {decision.should_deepen}")
    print(f"  Recommended depth: {decision.recommended_depth}")
    print(f"  Reasoning: {decision.reasoning}")

    if decision.should_deepen and decision.questions:
        print(f"\nGenerated {len(decision.questions)} research questions:")
        for i, q in enumerate(decision.questions, 1):
            print(f"  {i}. {q.question}")

    # =========================================================================
    # PHASE 2: INVESTIGATE QUESTIONS (DEPTH 1)
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 2: DEPTH 1 INVESTIGATIONS")
    print("=" * 70)

    depth_1_findings = []

    if decision.should_deepen:
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
    # PHASE 3: RECURSIVE DEEPENING (DEPTH 2)
    # =========================================================================
    print("\n" + "=" * 70)
    print("PHASE 3: DEPTH 2 INVESTIGATIONS")
    print("=" * 70)

    # Find significant depth-1 findings
    significant_d1 = [
        f for f in depth_1_findings
        if f.get('error_percent', 100) < 5 and f.get('n_samples', 0) >= 20
    ]

    print(f"\nSignificant depth-1 findings: {len(significant_d1)}")

    depth_2_findings = []
    investigated_patterns = set()

    for f in significant_d1[:3]:
        pattern_key = f"{f['quantity']}:{f['target']}"
        if pattern_key in investigated_patterns:
            continue
        investigated_patterns.add(pattern_key)

        print(f"\nRecursing on: {f['quantity']} ≈ {f['target']}")

        d2_decision = deepener.analyze_finding(f)

        if d2_decision.should_deepen and d2_decision.questions:
            print(f"  Generated {len(d2_decision.questions)} new questions")

            for q in d2_decision.questions[:2]:
                findings = researcher.investigate_question(q)
                for ff in findings:
                    ff['depth'] = 2
                    ff['parent_finding'] = f['quantity']
                depth_2_findings.extend(findings)

    depth_findings[2] = depth_2_findings
    all_findings.extend(depth_2_findings)

    # =========================================================================
    # RESULTS
    # =========================================================================
    print("\n" + "=" * 70)
    print("DEEPENING RESULTS SUMMARY")
    print("=" * 70)

    print(f"\nTotal findings: {len(all_findings)}")
    print(f"  Depth 0 (initial): {len(depth_findings.get(0, []))}")
    print(f"  Depth 1: {len(depth_findings.get(1, []))}")
    print(f"  Depth 2: {len(depth_findings.get(2, []))}")

    print(f"\nQuestions investigated: {len(researcher.questions_investigated)}")

    # Deduplicate and sort by error
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = f"{f['quantity']}:{f['target']}:{f.get('context', '')}"
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    print(f"\nUnique findings: {len(unique_findings)}")

    # Group by target
    by_target = {}
    for f in unique_findings:
        target = f.get('target', 'unknown')
        if target not in by_target:
            by_target[target] = []
        by_target[target].append(f)

    print("\nFindings by target:")
    for target, findings in sorted(by_target.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n  {target} ({len(findings)} findings):")
        for f in sorted(findings, key=lambda x: x.get('error_percent', 100))[:3]:
            print(f"    {f['quantity']}: {f['value']:.4f} ({f['error_percent']:.2f}% error, ctx={f.get('context', 'N/A')})")

    # Most precise
    print("\n" + "-" * 40)
    print("MOST PRECISE FINDINGS (< 5% error):")
    print("-" * 40)

    precise = [f for f in unique_findings if f.get('error_percent', 100) < 5]
    for f in sorted(precise, key=lambda x: x['error_percent']):
        print(f"  {f['quantity']} = {f['value']:.6f} ≈ {f['target']} ({f['error_percent']:.4f}% error)")
        if f.get('context'):
            print(f"    Context: {f['context']}")

    # Save results
    output_dir = Path(__file__).parent.parent / "olympus_outputs" / "oceanography_deepening"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "timestamp": datetime.now().isoformat(),
        "best_initial_finding": best_finding,
        "total_findings": len(all_findings),
        "unique_findings": len(unique_findings),
        "findings_by_depth": {str(d): len(f) for d, f in depth_findings.items()},
        "questions_investigated": researcher.questions_investigated,
        "unique_findings_list": unique_findings,
        "most_precise": [f for f in unique_findings if f.get('error_percent', 100) < 5]
    }

    with open(output_dir / "deepening_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_dir / 'deepening_results.json'}")

    return unique_findings


if __name__ == "__main__":
    findings = run_oceanography_deepening()

    print("\n" + "=" * 70)
    print("INVESTIGATION COMPLETE")
    print("=" * 70)

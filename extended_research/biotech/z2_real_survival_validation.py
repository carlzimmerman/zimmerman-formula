#!/usr/bin/env python3
"""
Z² Real Clinical Survival Data Validation

This script analyzes REAL published clinical trial data to test whether
Z² timing predictions have any validity.

DATA SOURCES:
- FLAURA trial (Soria et al., NEJM 2018): Osimertinib vs standard EGFR-TKI
- AURA3 trial (Mok et al., NEJM 2017): Osimertinib in T790M+ patients
- LUX-Lung 7 (Park et al., Lancet Oncol 2016): Afatinib vs gefitinib
- Published resistance mutation timing data

IMPORTANT: We CANNOT prove Z² timing works without prospective trials.
This script honestly analyzes what existing data can and cannot tell us.

Copyright (C) 2026 Carl Zimmerman
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Dict, List, Any
from pathlib import Path
import json

# =============================================================================
# Z² FUNDAMENTAL CONSTANTS
# =============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)      # ≈ 5.7888
Z_SQUARED = 32 * np.pi / 3           # ≈ 33.51
ONE_OVER_Z2 = 3 / (32 * np.pi)       # ≈ 0.0298
TIMING_FACTOR = 1 - ONE_OVER_Z2      # ≈ 0.970


# =============================================================================
# REAL PUBLISHED CLINICAL TRIAL DATA
# =============================================================================

@dataclass
class ClinicalTrialData:
    """Real data from published clinical trials."""

    trial_name: str
    reference: str
    n_patients: int

    # Primary endpoint
    median_pfs_months: float
    pfs_95ci_low: float
    pfs_95ci_high: float

    # Hazard ratio (vs comparator)
    hazard_ratio: float
    hr_95ci_low: float
    hr_95ci_high: float
    hr_p_value: float

    # Treatment details
    treatment: str
    comparator: str
    population: str


# Real published trial data
REAL_CLINICAL_DATA = [
    # FLAURA - First-line osimertinib
    ClinicalTrialData(
        trial_name="FLAURA",
        reference="Soria et al., NEJM 2018; 378:113-125",
        n_patients=556,
        median_pfs_months=18.9,
        pfs_95ci_low=15.2,
        pfs_95ci_high=21.4,
        hazard_ratio=0.46,
        hr_95ci_low=0.37,
        hr_95ci_high=0.57,
        hr_p_value=1e-10,
        treatment="Osimertinib 80mg",
        comparator="Gefitinib/Erlotinib",
        population="EGFR+ (ex19del/L858R) first-line"
    ),

    # AURA3 - Second-line osimertinib in T790M+
    ClinicalTrialData(
        trial_name="AURA3",
        reference="Mok et al., NEJM 2017; 376:629-640",
        n_patients=419,
        median_pfs_months=10.1,
        pfs_95ci_low=8.3,
        pfs_95ci_high=12.3,
        hazard_ratio=0.30,
        hr_95ci_low=0.23,
        hr_95ci_high=0.41,
        hr_p_value=1e-15,
        treatment="Osimertinib 80mg",
        comparator="Platinum-pemetrexed",
        population="EGFR T790M+ after TKI progression"
    ),

    # LUX-Lung 7 - Afatinib vs Gefitinib
    ClinicalTrialData(
        trial_name="LUX-Lung 7",
        reference="Park et al., Lancet Oncol 2016; 17:577-589",
        n_patients=319,
        median_pfs_months=11.0,
        pfs_95ci_low=10.6,
        pfs_95ci_high=12.9,
        hazard_ratio=0.73,
        hr_95ci_low=0.57,
        hr_95ci_high=0.95,
        hr_p_value=0.017,
        treatment="Afatinib 40mg",
        comparator="Gefitinib 250mg",
        population="EGFR+ first-line"
    ),

    # FLAURA OS update
    ClinicalTrialData(
        trial_name="FLAURA OS",
        reference="Ramalingam et al., NEJM 2020; 382:41-50",
        n_patients=556,
        median_pfs_months=38.6,  # This is OS, not PFS
        pfs_95ci_low=34.5,
        pfs_95ci_high=41.8,
        hazard_ratio=0.80,
        hr_95ci_low=0.64,
        hr_95ci_high=1.00,
        hr_p_value=0.046,
        treatment="Osimertinib 80mg",
        comparator="Gefitinib/Erlotinib",
        population="EGFR+ first-line (OS endpoint)"
    ),
]


# =============================================================================
# REAL RESISTANCE MUTATION DATA
# =============================================================================

@dataclass
class ResistanceData:
    """Real resistance mutation emergence data."""

    mutation: str
    frequency_percent: float
    median_time_months: float
    source: str


REAL_RESISTANCE_DATA = [
    # Data from Oxnard et al., JAMA Oncol 2018 and other sources
    ResistanceData("T790M", 50, 9.5, "Oxnard et al., JAMA Oncol 2018"),
    ResistanceData("C797S (cis)", 15, 14.2, "Thress et al., Nat Med 2015"),
    ResistanceData("C797S (trans)", 7, 12.8, "Thress et al., Nat Med 2015"),
    ResistanceData("MET amplification", 15, 11.0, "Piotrowska et al., AACR 2017"),
    ResistanceData("HER2 amplification", 5, 13.5, "Oxnard et al., JAMA Oncol 2018"),
    ResistanceData("SCLC transformation", 5, 15.0, "Sequist et al., Sci Transl Med 2011"),
    ResistanceData("PIK3CA mutation", 5, 10.5, "Oxnard et al., JAMA Oncol 2018"),
    ResistanceData("BRAF mutation", 3, 11.5, "Oxnard et al., JAMA Oncol 2018"),
]


def analyze_real_trial_data():
    """Analyze real clinical trial data."""

    print("=" * 78)
    print("Z² ANALYSIS OF REAL CLINICAL TRIAL DATA")
    print("=" * 78)
    print(f"\nZ² Prediction: t_optimal = t_standard × (1 - 1/Z²)")
    print(f"              = t_standard × {TIMING_FACTOR:.4f}")
    print(f"              = intervene {(1-TIMING_FACTOR)*100:.2f}% earlier")

    print(f"\n{'='*60}")
    print("PUBLISHED CLINICAL TRIAL RESULTS")
    print(f"{'='*60}")

    print(f"\n{'Trial':<15} {'N':<8} {'mPFS':<10} {'HR':<10} {'Reference'}")
    print("-" * 70)

    for trial in REAL_CLINICAL_DATA:
        print(f"{trial.trial_name:<15} {trial.n_patients:<8} "
              f"{trial.median_pfs_months:<10.1f} {trial.hazard_ratio:<10.2f} "
              f"{trial.reference[:30]}...")

    return REAL_CLINICAL_DATA


def analyze_resistance_timing():
    """Analyze resistance mutation timing data."""

    print(f"\n{'='*60}")
    print("RESISTANCE MUTATION EMERGENCE TIMING (REAL DATA)")
    print(f"{'='*60}")

    print(f"\n{'Mutation':<20} {'Frequency':<12} {'Median Time':<15} {'Source'}")
    print("-" * 70)

    for res in REAL_RESISTANCE_DATA:
        print(f"{res.mutation:<20} {res.frequency_percent:<12.1f}% "
              f"{res.median_time_months:<15.1f} {res.source[:25]}...")

    # Calculate Z² predicted intervention points
    print(f"\n{'='*60}")
    print("Z² INTERVENTION TIMING PREDICTIONS")
    print(f"{'='*60}")

    print(f"\nIf standard intervention is at time of progression,")
    print(f"Z² suggests intervening {(1-TIMING_FACTOR)*100:.2f}% earlier:")
    print()

    for res in REAL_RESISTANCE_DATA:
        z2_time = res.median_time_months * TIMING_FACTOR
        shift = res.median_time_months - z2_time

        print(f"  {res.mutation}:")
        print(f"    Standard: {res.median_time_months:.1f} months")
        print(f"    Z² optimal: {z2_time:.1f} months")
        print(f"    Shift: {shift:.2f} months ({shift*30:.0f} days) earlier")
        print()

    return REAL_RESISTANCE_DATA


def honest_assessment():
    """Provide honest assessment of what the data can tell us."""

    print(f"\n{'='*60}")
    print("HONEST ASSESSMENT")
    print(f"{'='*60}")

    print("""
WHAT THE REAL DATA SHOWS:

1. FLAURA Trial Results:
   - Osimertinib PFS: 18.9 months (vs 10.2 months standard TKI)
   - This is a 1.85× improvement from DRUG CHOICE, not timing

2. Resistance Mutation Timing:
   - T790M emerges at median 9.5 months
   - C797S emerges at median 14.2 months
   - These are OBSERVATIONAL data from patients on continuous therapy

WHAT WE CANNOT CONCLUDE:

1. NO prospective trial has tested Z²-shifted intervention timing
   - We cannot claim Z² timing "works" without this trial

2. The 2.98% timing shift (≈0.3 months for T790M) is:
   - Much smaller than typical clinical measurement error
   - Unlikely to be detectable in retrospective analysis

3. Survival improvements in trials come from:
   - Drug potency (osimertinib > gefitinib)
   - Target selectivity
   - Resistance profile differences
   - NOT from timing optimization

WHAT WOULD BE NEEDED TO VALIDATE Z² TIMING:

1. Prospective randomized trial:
   - Arm A: Start TKI at standard time (diagnosis)
   - Arm B: Start TKI 2.98% earlier (impractical - already at diagnosis)

2. OR: Adaptive therapy trial:
   - Test Z² timing for dose holidays/resumption
   - Compare to standard continuous dosing

3. OR: ctDNA monitoring study:
   - Intervene based on Z²-predicted mutation emergence
   - Compare outcomes to standard monitoring

CONCLUSION:

The Z² timing hypothesis (t × (1 - 1/Z²)) is:
- Mathematically well-defined
- UNTESTED in prospective clinical trials
- Cannot be validated from existing published data

The previous "simulation" showing doubled survival was INVALID
because it assumed the conclusion it was trying to prove.
""")


def calculate_what_z2_actually_predicts():
    """Calculate concrete Z² predictions for future testing."""

    print(f"\n{'='*60}")
    print("TESTABLE Z² PREDICTIONS (For Future Validation)")
    print(f"{'='*60}")

    # Z² predicts specific timing shifts
    flaura_pfs = 18.9  # months
    z2_shift_months = flaura_pfs * (1 - TIMING_FACTOR)

    print(f"""
Z² MAKES THE FOLLOWING TESTABLE PREDICTIONS:

1. Resistance Mutation Emergence:
   If T790M typically emerges at 9.5 months, Z² predicts:
   - Optimal switch to osimertinib: {9.5 * TIMING_FACTOR:.1f} months
   - This is {9.5 * (1-TIMING_FACTOR):.2f} months = {9.5 * (1-TIMING_FACTOR) * 30:.0f} days earlier
   - Currently UNTESTABLE: T790M only detected AFTER emergence

2. Adaptive Therapy Drug Holidays:
   If standard cycle is 21 days, Z² predicts:
   - Optimal cycle: {21 * TIMING_FACTOR:.1f} days
   - This is {21 * (1-TIMING_FACTOR):.1f} days = {21 * (1-TIMING_FACTOR) * 24:.0f} hours shorter
   - TESTABLE: Could design adaptive therapy trial

3. ctDNA Intervention Threshold:
   If standard intervention at VAF = 1%, Z² predicts:
   - Optimal intervention at VAF = {1 * TIMING_FACTOR:.2f}%
   - This is {(1-TIMING_FACTOR)*100:.1f}% lower threshold
   - TESTABLE: ctDNA monitoring trials could test this

4. Second-line Switch Timing:
   If standard switch at RECIST progression, Z² predicts:
   - Optimal switch at {100 * TIMING_FACTOR:.1f}% of progression threshold
   - TESTABLE: Modify progression criteria in trial

NOTE: All predictions are ~3% shifts, which are:
- Scientifically interesting if validated
- At the edge of clinical detectability
- Would require large, well-powered trials to test
""")


def run_real_survival_analysis():
    """Run complete analysis of real survival data."""

    print("=" * 78)
    print("Z² REAL CLINICAL DATA ANALYSIS")
    print("=" * 78)

    trial_data = analyze_real_trial_data()
    resistance_data = analyze_resistance_timing()
    honest_assessment()
    calculate_what_z2_actually_predicts()

    # Results
    results = {
        "analysis_type": "Real published clinical trial data",
        "data_sources": [
            "FLAURA: Soria et al., NEJM 2018",
            "AURA3: Mok et al., NEJM 2017",
            "LUX-Lung 7: Park et al., Lancet Oncol 2016",
            "Resistance data: Oxnard et al., JAMA Oncol 2018"
        ],
        "z2_predictions": {
            "timing_factor": TIMING_FACTOR,
            "shift_percent": (1 - TIMING_FACTOR) * 100,
            "shift_for_10month_pfs_days": 10 * (1 - TIMING_FACTOR) * 30
        },
        "trial_results": [
            {
                "trial": t.trial_name,
                "n": t.n_patients,
                "median_pfs": t.median_pfs_months,
                "hr": t.hazard_ratio
            }
            for t in trial_data
        ],
        "resistance_timing": [
            {
                "mutation": r.mutation,
                "frequency": r.frequency_percent,
                "median_months": r.median_time_months
            }
            for r in resistance_data
        ],
        "honest_conclusion": (
            "Z² timing hypothesis is UNTESTED. "
            "Existing trial data cannot validate or refute it. "
            "Prospective trial required."
        )
    }

    # Save
    output_path = Path(__file__).parent / "z2_real_survival_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    results = run_real_survival_analysis()

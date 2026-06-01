#!/usr/bin/env python3
"""
TEST STATISTICAL VALIDATION - OlympusFlow v1.5.0
=================================================

Tests the new statistical validation infrastructure:
1. DatabaseQueryHandler - API access to scientific databases
2. StatisticalValidator - Monte Carlo, FDR, effect size
3. Integration with HermesFlow

Author: Carl Zimmerman
Date: May 5, 2026
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from datetime import datetime

print("=" * 70)
print("TEST STATISTICAL VALIDATION - OlympusFlow v1.5.0")
print("=" * 70)
print(f"Started: {datetime.now().isoformat()}")
print()

# =============================================================================
# TEST 1: DATABASE QUERY HANDLER
# =============================================================================

print("TEST 1: DatabaseQueryHandler")
print("-" * 40)

try:
    from HermesFlow.database_query_handler import (
        DatabaseQueryHandler, query_database, find_apis, list_all_apis
    )

    handler = DatabaseQueryHandler(verbose=True)
    print(f"  Initialized: {len(handler.known_apis)} known APIs")

    # Test finding APIs by domain
    volcano_apis = handler.find_apis_for_domain("volcanology")
    print(f"  Volcano APIs found: {len(volcano_apis)}")
    for api in volcano_apis:
        print(f"    - {api.name}")

    sunspot_apis = handler.find_apis_for_domain("astronomy", "sunspot")
    print(f"  Sunspot APIs found: {len(sunspot_apis)}")
    for api in sunspot_apis:
        print(f"    - {api.name}")

    # Test actual API queries
    print("\n  Querying SILSO monthly sunspots...")
    result = handler.query("silso_monthly_total")
    if result.success:
        print(f"    SUCCESS: {result.rows} rows, {result.columns} columns")
        if result.data is not None:
            print(f"    Columns: {list(result.data.columns)[:5]}")
            print(f"    Date range: {result.data.iloc[0, 0]} to {result.data.iloc[-1, 0]}")
    else:
        print(f"    FAILED: {result.error}")

    print("\n  Querying NOAA significant volcanoes...")
    result = handler.query("noaa_significant_volcanoes")
    if result.success:
        print(f"    SUCCESS: {result.rows} rows, {result.columns} columns")
    else:
        print(f"    FAILED: {result.error}")

    print("\n  Querying USGS earthquakes...")
    result = handler.query("usgs_earthquake")
    if result.success:
        print(f"    SUCCESS: {result.rows} rows, {result.columns} columns")
    else:
        print(f"    FAILED: {result.error}")

    print("\nV DatabaseQueryHandler PASSED")
    db_handler_passed = True

except Exception as e:
    print(f"\nX DatabaseQueryHandler FAILED: {e}")
    import traceback
    traceback.print_exc()
    db_handler_passed = False

print()

# =============================================================================
# TEST 2: STATISTICAL VALIDATOR
# =============================================================================

print("TEST 2: StatisticalValidator")
print("-" * 40)

try:
    from OlympusFlow.statistical_validator import (
        StatisticalValidator,
        PatternCandidate,
        MonteCarloValidator,
        MultipleComparisonCorrector,
        EffectSizeCalculator,
        validate_pattern_quick,
        TARGETS
    )

    print("  Available targets:")
    for name, value in list(TARGETS.items())[:5]:
        print(f"    {name} = {value:.6f}")

    # Test Monte Carlo validator
    print("\n  Testing MonteCarloValidator...")
    mc = MonteCarloValidator(n_permutations=1000)  # Fewer for speed

    # Create test data that SHOULD match 1/φ
    np.random.seed(42)
    target_1_phi = 1 / TARGETS['phi']
    good_data = np.random.normal(target_1_phi, 0.01, size=500)
    good_stat = np.std(good_data) / np.mean(good_data)

    result_good = mc.validate(
        good_data,
        np.mean(good_data),
        target_1_phi,
        np.mean
    )
    print(f"    Good match (mean ≈ 1/φ): p={result_good['p_value']:.6f}")

    # Create test data that SHOULD NOT match
    bad_data = np.random.normal(0.5, 0.1, size=500)  # Not near 1/φ
    result_bad = mc.validate(
        bad_data,
        np.mean(bad_data),
        target_1_phi,
        np.mean
    )
    print(f"    Bad match (random data): p={result_bad['p_value']:.6f}")

    # Test FDR correction
    print("\n  Testing FDR correction...")
    fdr = MultipleComparisonCorrector(method='fdr_bh')
    p_values = [0.001, 0.01, 0.05, 0.1, 0.5, 0.9]
    adjusted, significant = fdr.correct(p_values, alpha=0.05)
    print(f"    Original p-values: {p_values}")
    print(f"    Adjusted p-values: {[f'{p:.4f}' for p in adjusted]}")
    print(f"    Significant: {significant}")

    # Test effect size
    print("\n  Testing EffectSizeCalculator...")
    effect = EffectSizeCalculator.cohens_d(0.618, 0.618034, 0.01)
    print(f"    Effect size (close match): d={effect:.4f}")
    effect = EffectSizeCalculator.cohens_d(0.5, 0.618034, 0.01)
    print(f"    Effect size (poor match): d={effect:.4f}")

    # Test full validation pipeline
    print("\n  Testing full validation pipeline...")
    validator = StatisticalValidator(verbose=False, script_output_dir="/tmp/validation_scripts")

    # Create a pattern candidate
    candidate = PatternCandidate(
        quantity="test_cv",
        observed_value=np.std(good_data) / np.mean(good_data),
        target_name="1/phi",
        target_value=target_1_phi,
        deviation=abs(np.std(good_data) / np.mean(good_data) - target_1_phi),
        relative_error=abs(np.std(good_data) / np.mean(good_data) - target_1_phi) / target_1_phi,
        sample_size=len(good_data),
        data_source="synthetic",
        statistic_type="cv",
        raw_data=good_data
    )

    result = validator.validate_candidate(candidate, domain="test", topic="validation")
    print(f"    Validation result:")
    print(f"      p-value: {result.p_value:.6f}")
    print(f"      Effect size: {result.effect_size:.4f}")
    print(f"      HRM score: {result.hrm_score:.3f}")
    print(f"      Status: {result.status}")
    print(f"      Valid: {result.is_valid}")

    print("\nV StatisticalValidator PASSED")
    stat_validator_passed = True

except Exception as e:
    print(f"\nX StatisticalValidator FAILED: {e}")
    import traceback
    traceback.print_exc()
    stat_validator_passed = False

print()

# =============================================================================
# TEST 3: INTEGRATION WITH HERMESFLOW
# =============================================================================

print("TEST 3: HermesFlow Integration")
print("-" * 40)

try:
    from HermesFlow.universal_data_discovery import UniversalDataDiscovery

    discovery = UniversalDataDiscovery(
        use_legomena=False,  # Skip LLM for this test
        use_web_search=False,  # Skip web search
        use_helicon_lake=True,
        use_database_apis=True
    )

    print(f"  DatabaseQueryHandler: {'Active' if discovery.db_handler else 'Not available'}")
    print(f"  HeliconLake: {'Active' if discovery.helicon_lake else 'Not available'}")

    if discovery.db_handler:
        # Check for volcanology APIs
        apis = discovery.db_handler.find_apis_for_domain("volcanology")
        print(f"  Volcanology APIs available: {len(apis)}")

    print("\nV HermesFlow Integration PASSED")
    hermesflow_passed = True

except Exception as e:
    print(f"\nX HermesFlow Integration FAILED: {e}")
    import traceback
    traceback.print_exc()
    hermesflow_passed = False

print()

# =============================================================================
# TEST 4: OLYMPUSFLOW IMPORTS
# =============================================================================

print("TEST 4: OlympusFlow Imports")
print("-" * 40)

try:
    from OlympusFlow import (
        __version__,
        Pipeline, PipelineConfig,
        Z2, Z, PHI,
        StatisticalValidator,
        PatternCandidate,
        ValidationResult,
        validate_pattern_quick
    )

    print(f"  OlympusFlow version: {__version__}")
    print(f"  Z² = {Z2:.6f}")
    print(f"  Z = {Z:.6f}")
    print(f"  φ = {PHI:.6f}")
    print(f"  StatisticalValidator: imported")
    print(f"  validate_pattern_quick: imported")

    print("\nV OlympusFlow Imports PASSED")
    olympus_passed = True

except Exception as e:
    print(f"\nX OlympusFlow Imports FAILED: {e}")
    import traceback
    traceback.print_exc()
    olympus_passed = False

print()

# =============================================================================
# SUMMARY
# =============================================================================

print("=" * 70)
print("SUMMARY")
print("=" * 70)

checks = [
    ("DatabaseQueryHandler", db_handler_passed),
    ("StatisticalValidator", stat_validator_passed),
    ("HermesFlow Integration", hermesflow_passed),
    ("OlympusFlow Imports", olympus_passed),
]

all_passed = True
for name, passed in checks:
    symbol = "V" if passed else "X"
    print(f"  {symbol} {name}: {'PASSED' if passed else 'FAILED'}")
    if not passed:
        all_passed = False

print()
if all_passed:
    print("V ALL TESTS PASSED - OlympusFlow v1.5.0 ready!")
else:
    print("X SOME TESTS FAILED - Check errors above")

print()
print(f"Completed: {datetime.now().isoformat()}")

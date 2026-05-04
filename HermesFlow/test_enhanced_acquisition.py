#!/usr/bin/env python3
"""
Test enhanced data acquisition (v1.6.0)

Tests:
1. ASCII table parsing (NOAA MEI data)
2. HTML table extraction
3. JSON API parsing
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from hermes_explorer import HermesExplorer

def test_ascii_parsing():
    """Test ASCII table parsing on NOAA MEI data."""
    print("=" * 60)
    print("TEST 1: ASCII Table Parsing (NOAA MEI)")
    print("=" * 60)

    explorer = HermesExplorer(verbose=True)

    # Known NOAA MEI v2 data URL
    mei_url = "https://psl.noaa.gov/enso/mei/data/meiv2.data"

    print(f"Fetching: {mei_url}")
    df = explorer.tool_fetch_data(mei_url)

    if df is not None:
        print(f"SUCCESS! Got {len(df)} rows, {len(df.columns)} columns")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample:\n{df.head()}")
        return True
    else:
        print("FAILED to parse data")
        return False


def test_html_tables():
    """Test HTML table extraction."""
    print("\n" + "=" * 60)
    print("TEST 2: HTML Table Extraction")
    print("=" * 60)

    explorer = HermesExplorer(verbose=True)

    # A page with data tables
    url = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php"

    print(f"Fetching: {url}")
    html = explorer.tool_fetch(url)

    if html:
        df = explorer._parse_html_tables(html)
        if df is not None:
            print(f"SUCCESS! Extracted table with {len(df)} rows, {len(df.columns)} columns")
            print(f"Sample:\n{df.head()}")
            return True
        else:
            print("No tables extracted")
    else:
        print("Failed to fetch page")

    return False


def test_full_exploration():
    """Test full exploration with enhanced acquisition."""
    print("\n" + "=" * 60)
    print("TEST 3: Full Exploration (El Nino)")
    print("=" * 60)

    explorer = HermesExplorer(verbose=True)

    result = explorer.explore_for_data(
        topic="El Nino Southern Oscillation MEI index",
        domain="climatology",
        quantities=["index", "anomaly", "value"]
    )

    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"URL: {result.url}")
    print(f"Steps: {len(result.steps)}")
    print(f"Description: {result.description}")

    if result.data is not None:
        print(f"Data: {len(result.data)} rows, {len(result.data.columns)} columns")

    return result.success


if __name__ == "__main__":
    results = []

    # Test 1: ASCII parsing
    results.append(("ASCII parsing", test_ascii_parsing()))

    # Test 2: HTML tables
    results.append(("HTML tables", test_html_tables()))

    # Test 3: Full exploration (only if tests 1-2 pass)
    if all(r[1] for r in results):
        results.append(("Full exploration", test_full_exploration()))
    else:
        print("\nSkipping full exploration test due to earlier failures")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")

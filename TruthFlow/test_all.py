#!/usr/bin/env python3
"""
TruthFlow + LegomenaLLM Integration Test
=========================================
Run this to verify everything is working.

Usage:
    python test_all.py
    python test_all.py --verbose
"""

import subprocess
import json
import sys

# ============================================================================
# TESTS
# ============================================================================

def test_truthflow():
    """Test TruthFlow validation."""
    print("=" * 60)
    print("TEST 1: TruthFlow Validation")
    print("=" * 60)

    try:
        from truthflow import validate_all, PREDICTIONS, MEASUREMENTS
        results = validate_all()

        # Check results
        failed = [r for r in results if "FAILED" in r.get("status", "")]
        validated = [r for r in results if "VALIDATED" in r.get("status", "") or "EXACT" in r.get("status", "")]

        if failed:
            print(f"\n❌ FAILED: {len(failed)} predictions failed")
            for r in failed:
                print(f"   - {r['name']}")
            return False
        else:
            print(f"\n✅ PASSED: {len(validated)} validated, 0 failed")
            return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


def test_legomena():
    """Test LegomenaLLM responses."""
    print("\n" + "=" * 60)
    print("TEST 2: LegomenaLLM Responses")
    print("=" * 60)

    # Test questions and expected keywords in response (any match = pass)
    tests = [
        {
            "question": "What is dark matter?",
            "must_contain_any": ["does not exist", "not exist", "flawed", "artifact", "spectral", "dimension", "mond"],
            "must_not_contain": ["WIMP is", "axion is", "dark matter halo"],
        },
        {
            "question": "What is the Hubble constant?",
            "must_contain_any": ["Z", "geometric", "71", "tension", "dimension"],
            "must_not_contain": [],
        },
        {
            "question": "Can Z² be falsified?",
            "must_contain_any": ["yes", "falsif", "testable", "prediction"],
            "must_not_contain": [],
        },
    ]

    all_passed = True

    for test in tests:
        q = test["question"]
        print(f"\nQ: {q}")

        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/generate",
                 "-d", json.dumps({"model": "legomena", "prompt": q, "stream": False}),
                 "--max-time", "60"],
                capture_output=True, text=True
            )

            response = json.loads(result.stdout).get("response", "")
            response_lower = response.lower()

            # Check must_contain_any (at least one keyword must appear)
            found_any = any(kw.lower() in response_lower for kw in test["must_contain_any"])
            # Check must_not_contain
            forbidden = [kw for kw in test["must_not_contain"] if kw.lower() in response_lower]

            if not found_any or forbidden:
                print(f"❌ FAILED")
                if not found_any:
                    print(f"   Missing all of: {test['must_contain_any']}")
                if forbidden:
                    print(f"   Found forbidden: {forbidden}")
                all_passed = False
            else:
                print(f"✅ PASSED")
                print(f"   Response: {response[:150]}...")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            all_passed = False

    return all_passed


def test_ollama_available():
    """Check if Ollama is running and legomena model exists."""
    print("=" * 60)
    print("TEST 0: Ollama + Legomena Model")
    print("=" * 60)

    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, text=True
        )

        models = json.loads(result.stdout).get("models", [])
        model_names = [m["name"] for m in models]

        if "legomena:latest" in model_names:
            print("✅ Ollama running, legomena model found")
            return True
        else:
            print("❌ legomena model not found")
            print(f"   Available: {model_names[:5]}")
            print("\n   To create: cd TruthFlow/legomena_training && ollama create legomena -f Modelfile")
            return False

    except Exception as e:
        print(f"❌ Ollama not running: {e}")
        print("   Start with: ollama serve")
        return False


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    verbose = "--verbose" in sys.argv

    print("\n" + "=" * 60)
    print("Z² FRAMEWORK - INTEGRATION TEST")
    print("=" * 60 + "\n")

    results = []

    # Test 0: Ollama
    results.append(("Ollama", test_ollama_available()))

    # Test 1: TruthFlow
    results.append(("TruthFlow", test_truthflow()))

    # Test 2: LegomenaLLM (only if Ollama passed)
    if results[0][1]:
        results.append(("LegomenaLLM", test_legomena()))
    else:
        results.append(("LegomenaLLM", None))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        if passed is None:
            status = "⏭️  SKIPPED"
        elif passed:
            status = "✅ PASSED"
        else:
            status = "❌ FAILED"
            all_passed = False
        print(f"  {name}: {status}")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED")
    else:
        print("⚠️  SOME TESTS FAILED")
    print("=" * 60 + "\n")

    sys.exit(0 if all_passed else 1)

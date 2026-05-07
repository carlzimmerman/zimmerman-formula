#!/usr/bin/env python3
"""
TruthFlow + LegomenaLLM Integration Test
=========================================
Run this to verify everything is working.

Usage:
    python test_all.py                      # Use default model
    python test_all.py --model legomena-e2b # Use specific model
    python test_all.py --model legomena-full
    python test_all.py --list-models        # List available models
    python test_all.py --compare            # Compare all models
    python test_all.py --verbose
"""

import subprocess
import json
import sys
import argparse
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

# Available models (add new trained models here)
AVAILABLE_MODELS = {
    "legomena": {
        "description": "Standard model (9.6 GB) - gemma4:e4b base",
        "size_gb": 9.6,
        "recommended": True,
    },
    "legomena-e2b": {
        "description": "Lite model (7.2 GB) - gemma4:e2b base",
        "size_gb": 7.2,
        "recommended": False,
    },
    "legomena-full": {
        "description": "Full model (19 GB) - gemma4:31b base",
        "size_gb": 19.0,
        "recommended": False,
    },
}

DEFAULT_MODEL = "legomena"

# Test questions and expected keywords
TEST_QUESTIONS = [
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


def test_legomena(model_name: str, timeout: int = 120):
    """Test LegomenaLLM responses with specified model."""
    print("\n" + "=" * 60)
    print(f"TEST 2: LegomenaLLM Responses [{model_name}]")
    print("=" * 60)

    all_passed = True
    response_times = []

    for test in TEST_QUESTIONS:
        q = test["question"]
        print(f"\nQ: {q}")

        try:
            start_time = time.time()
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/generate",
                 "-d", json.dumps({"model": model_name, "prompt": q, "stream": False}),
                 "--max-time", str(timeout)],
                capture_output=True, text=True
            )
            elapsed = time.time() - start_time
            response_times.append(elapsed)

            response = json.loads(result.stdout).get("response", "")
            response_lower = response.lower()

            # Check must_contain_any (at least one keyword must appear)
            found_any = any(kw.lower() in response_lower for kw in test["must_contain_any"])
            # Check must_not_contain
            forbidden = [kw for kw in test["must_not_contain"] if kw.lower() in response_lower]

            if not found_any or forbidden:
                print(f"❌ FAILED ({elapsed:.1f}s)")
                if not found_any:
                    print(f"   Missing all of: {test['must_contain_any']}")
                if forbidden:
                    print(f"   Found forbidden: {forbidden}")
                all_passed = False
            else:
                print(f"✅ PASSED ({elapsed:.1f}s)")
                print(f"   Response: {response[:150]}...")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            all_passed = False

    if response_times:
        avg_time = sum(response_times) / len(response_times)
        print(f"\n⏱️  Average response time: {avg_time:.1f}s")

    return all_passed


def test_ollama_available(model_name: str):
    """Check if Ollama is running and specified model exists."""
    print("=" * 60)
    print(f"TEST 0: Ollama + {model_name} Model")
    print("=" * 60)

    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, text=True
        )

        models = json.loads(result.stdout).get("models", [])
        model_names = [m["name"] for m in models]

        # Check for exact match or with :latest suffix
        found = (f"{model_name}:latest" in model_names or
                 model_name in model_names or
                 any(m.startswith(f"{model_name}:") for m in model_names))

        if found:
            print(f"✅ Ollama running, {model_name} model found")
            return True
        else:
            print(f"❌ {model_name} model not found")
            print(f"   Available: {model_names[:5]}")
            print(f"\n   To create: cd TruthFlow/legomena_training && ollama create {model_name} -f Modelfile")
            return False

    except Exception as e:
        print(f"❌ Ollama not running: {e}")
        print("   Start with: ollama serve")
        return False


def list_models():
    """List all available models."""
    print("\n" + "=" * 60)
    print("AVAILABLE LEGOMENA MODELS")
    print("=" * 60)

    # Check which are installed
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, text=True
        )
        installed = [m["name"] for m in json.loads(result.stdout).get("models", [])]
    except:
        installed = []

    for name, info in AVAILABLE_MODELS.items():
        status = "✅ installed" if any(name in m for m in installed) else "⬜ not installed"
        rec = " (recommended)" if info.get("recommended") else ""
        print(f"\n  {name}{rec}")
        print(f"    {info['description']}")
        print(f"    Size: {info['size_gb']} GB | Status: {status}")

    print("\n" + "-" * 60)
    print("Usage: python test_all.py --model <model_name>")
    print("=" * 60 + "\n")


def compare_models():
    """Compare all installed models."""
    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    # Find installed models
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, text=True
        )
        installed = [m["name"].replace(":latest", "") for m in json.loads(result.stdout).get("models", [])]
    except:
        print("❌ Cannot connect to Ollama")
        return

    # Filter to legomena models
    legomena_models = [m for m in installed if m.startswith("legomena")]

    if not legomena_models:
        print("❌ No legomena models installed")
        return

    print(f"\nComparing {len(legomena_models)} models: {', '.join(legomena_models)}")
    print("-" * 60)

    results = {}
    for model in legomena_models:
        print(f"\n>>> Testing {model}...")
        start = time.time()

        # Quick test
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/generate",
                 "-d", json.dumps({"model": model, "prompt": "What is r in Z²?", "stream": False}),
                 "--max-time", "120"],
                capture_output=True, text=True
            )
            elapsed = time.time() - start
            response = json.loads(result.stdout).get("response", "")

            # Check for correct answer
            correct = "0.015" in response or "1/(2Z" in response or "3/(64" in response
            results[model] = {
                "time": elapsed,
                "correct": correct,
                "response_len": len(response)
            }
            print(f"    Time: {elapsed:.1f}s | Correct: {'✅' if correct else '❌'} | Length: {len(response)}")
        except Exception as e:
            results[model] = {"error": str(e)}
            print(f"    ❌ Error: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"{'Model':<20} {'Time':<10} {'Correct':<10} {'Response':<10}")
    print("-" * 50)
    for model, data in results.items():
        if "error" in data:
            print(f"{model:<20} {'ERROR':<10}")
        else:
            print(f"{model:<20} {data['time']:.1f}s{'':<5} {'✅' if data['correct'] else '❌':<10} {data['response_len']:<10}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="TruthFlow + LegomenaLLM Integration Test")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL,
                        help=f"Model to test (default: {DEFAULT_MODEL})")
    parser.add_argument("--list-models", "-l", action="store_true",
                        help="List available models")
    parser.add_argument("--compare", "-c", action="store_true",
                        help="Compare all installed models")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    parser.add_argument("--timeout", "-t", type=int, default=120,
                        help="Timeout per question in seconds (default: 120)")

    args = parser.parse_args()

    if args.list_models:
        list_models()
        return 0

    if args.compare:
        compare_models()
        return 0

    model_name = args.model

    print("\n" + "=" * 60)
    print(f"Z² FRAMEWORK - INTEGRATION TEST")
    print(f"Model: {model_name}")
    print("=" * 60 + "\n")

    results = []

    # Test 0: Ollama
    results.append(("Ollama", test_ollama_available(model_name)))

    # Test 1: TruthFlow
    results.append(("TruthFlow", test_truthflow()))

    # Test 2: LegomenaLLM (only if Ollama passed)
    if results[0][1]:
        results.append(("LegomenaLLM", test_legomena(model_name, args.timeout)))
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

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
MODEL COMPARISON TEST: Legomena 4b vs 31b
==========================================

Run the EXACT same glacier blind test on both models
to compare performance and output quality.

Models:
- legomena-4b (3.3GB) - smallest
- legomena-31b (19GB) - largest

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import math
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Import HermesFlow components
sys.path.insert(0, str(Path(__file__).parent))
from hermes_explorer import HermesExplorer

# Z² Constants
Z2 = 32 * math.pi / 3
Z = math.sqrt(Z2)
PHI = (1 + math.sqrt(5)) / 2

OUTPUT_DIR = Path(__file__).parent / "model_comparison_output"
OUTPUT_DIR.mkdir(exist_ok=True)


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[COMPARE {ts}] {msg}")


def test_legomena_response(model: str, prompt: str) -> dict:
    """Test a single Legomena prompt and measure response."""
    start = time.time()

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
        elapsed = time.time() - start

        if result.returncode == 0:
            return {
                "success": True,
                "response": result.stdout.strip(),
                "time_seconds": elapsed,
                "length": len(result.stdout.strip())
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "time_seconds": elapsed
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Timeout after 120s",
            "time_seconds": 120
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "time_seconds": time.time() - start
        }


def run_exploration_test(model: str) -> dict:
    """Run the full exploration test with a specific model."""
    log(f"\n{'='*70}")
    log(f"TESTING MODEL: {model}")
    log(f"{'='*70}")

    os.environ["LEGOMENA_MODEL"] = model

    # Reload the explorer with new model
    from importlib import reload
    import hermes_explorer
    reload(hermes_explorer)
    from hermes_explorer import HermesExplorer

    start_time = time.time()
    explorer = HermesExplorer(verbose=True)

    # Run exploration
    result = explorer.explore_for_data(
        topic="Swiss Alps glacier melting rates",
        domain="glaciology",
        quantities=["mass_balance", "melt_rate", "ice_thickness", "surface_area"]
    )

    elapsed = time.time() - start_time

    return {
        "model": model,
        "success": result.success,
        "url": result.url,
        "steps": len(result.steps),
        "description": result.description,
        "time_seconds": elapsed,
        "step_details": [
            {
                "action": s.action,
                "input": s.input[:100] if len(s.input) > 100 else s.input,
                "result": s.result[:100] if len(s.result) > 100 else s.result,
                "reasoning": s.reasoning[:200] if s.reasoning and len(s.reasoning) > 200 else s.reasoning
            }
            for s in result.steps
        ]
    }


def run_reasoning_comparison(models: list) -> dict:
    """Compare reasoning quality between models."""
    log("\n" + "="*70)
    log("REASONING QUALITY COMPARISON")
    log("="*70)

    # Test prompts that exercise reasoning
    test_prompts = [
        {
            "name": "Database identification",
            "prompt": "What are the main scientific databases for glaciology that would have mass_balance, melt_rate, ice_thickness? List database names concisely."
        },
        {
            "name": "Link selection",
            "prompt": """I'm looking for glacier mass balance data CSV.
Which link should I follow?
- Download data: https://wgms.ch/data_databaseversions/
- About glaciers: https://wgms.ch/about/
- Publications: https://wgms.ch/publications/
- Contact: https://wgms.ch/contact/

Answer with just the URL:"""
        },
        {
            "name": "Column mapping",
            "prompt": """These are columns from a glacier dataset:
SGI-ID, A_start, A_end, dV, dh_mean, Bgeod, sigma, rho_dv, Name

Map these to scientific quantities:
- mass_balance = ?
- area = ?
- volume_change = ?

Answer concisely:"""
        }
    ]

    results = {}

    for model in models:
        log(f"\nTesting {model}...")
        results[model] = []

        for test in test_prompts:
            log(f"  Prompt: {test['name']}")
            response = test_legomena_response(model, test['prompt'])
            response['prompt_name'] = test['name']
            results[model].append(response)

            if response['success']:
                log(f"    Response ({response['time_seconds']:.1f}s): {response['response'][:80]}...")
            else:
                log(f"    Error: {response.get('error', 'Unknown')}")

    return results


def main():
    log("="*70)
    log("HERMESFLOW MODEL COMPARISON TEST")
    log("Comparing: legomena-4b (3.3GB) vs legomena-31b (19GB)")
    log("="*70)

    models = ["legomena-4b", "legomena-31b"]

    # Part 1: Reasoning comparison
    reasoning_results = run_reasoning_comparison(models)

    # Part 2: Full exploration comparison
    log("\n" + "="*70)
    log("FULL EXPLORATION COMPARISON")
    log("="*70)

    exploration_results = {}
    for model in models:
        exploration_results[model] = run_exploration_test(model)

    # Summary
    log("\n" + "="*70)
    log("COMPARISON SUMMARY")
    log("="*70)

    print(f"\n{'Metric':<30} {'legomena-4b':<20} {'legomena-31b':<20}")
    print("-"*70)

    # Reasoning comparison
    for i, prompt_name in enumerate(["Database identification", "Link selection", "Column mapping"]):
        r4b = reasoning_results["legomena-4b"][i]
        r31b = reasoning_results["legomena-31b"][i]

        time_4b = f"{r4b['time_seconds']:.1f}s" if r4b['success'] else "FAIL"
        time_31b = f"{r31b['time_seconds']:.1f}s" if r31b['success'] else "FAIL"

        print(f"{prompt_name:<30} {time_4b:<20} {time_31b:<20}")

    print("-"*70)

    # Exploration comparison
    e4b = exploration_results["legomena-4b"]
    e31b = exploration_results["legomena-31b"]

    print(f"{'Exploration success':<30} {str(e4b['success']):<20} {str(e31b['success']):<20}")
    print(f"{'Exploration time':<30} {e4b['time_seconds']:.1f}s{'':<14} {e31b['time_seconds']:.1f}s")
    print(f"{'Steps taken':<30} {e4b['steps']:<20} {e31b['steps']:<20}")

    # Save full results
    results_file = OUTPUT_DIR / "model_comparison_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "models_tested": models,
            "reasoning_results": reasoning_results,
            "exploration_results": exploration_results
        }, f, indent=2, default=str)

    log(f"\nFull results saved to: {results_file}")

    # Conclusion
    log("\n" + "="*70)
    log("CONCLUSION")
    log("="*70)

    # Compare response quality
    log("\nReasoning quality comparison:")
    for i, prompt_name in enumerate(["Database identification", "Link selection", "Column mapping"]):
        r4b = reasoning_results["legomena-4b"][i]
        r31b = reasoning_results["legomena-31b"][i]

        log(f"\n{prompt_name}:")
        if r4b['success']:
            log(f"  4b ({r4b['time_seconds']:.1f}s): {r4b['response'][:100]}...")
        if r31b['success']:
            log(f"  31b ({r31b['time_seconds']:.1f}s): {r31b['response'][:100]}...")


if __name__ == "__main__":
    main()

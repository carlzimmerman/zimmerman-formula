"""Bounded reproducibility entry point for the localized V4 checkpoint."""
import json
import argparse
from pathlib import Path

from localized_action import action_data, localized_static_variation
from eliminate_localizers import eliminate_localizers
from localized_dirac import dirac_report
from metric_variation_gate import metric_variation_gate
from causal_response_gate import causal_response_gate
from york_variation_gate import york_variation_gate
from flrw_ward_gate import flrw_ward_gate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="run_001")
    args = parser.parse_args()
    result = {
        "action": action_data(),
        "static": localized_static_variation(),
        "elimination": eliminate_localizers(),
        "dirac_nonzero": dirac_report("k_nonzero"),
        "dirac_zero": dirac_report("k_zero"),
        "metric_variation": metric_variation_gate(),
        "causal_response": causal_response_gate(),
        "york_variation": york_variation_gate(),
        "flrw_ward": flrw_ward_gate(),
    }
    out = Path(__file__).resolve().parent / args.output_dir / "localized_v4_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

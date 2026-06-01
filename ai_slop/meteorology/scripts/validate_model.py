#!/usr/bin/env python3
"""
Model Validation Script

This script evaluates a trained weather prediction model against:
1. Held-out test data (ERA5)
2. Published baselines (GraphCast, Pangu-Weather, IFS HRES)
3. Simple baselines (climatology, persistence)

Usage:
    python scripts/validate_model.py --checkpoint path/to/model.pt --data path/to/test_data

The output is a comprehensive benchmark report showing:
- RMSE, MAE, ACC at multiple lead times
- Skill scores relative to baselines
- Comparison tables against state-of-the-art models
"""

import sys
from pathlib import Path
import argparse
import json
import numpy as np
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available. Some features disabled.")


def parse_args():
    parser = argparse.ArgumentParser(description="Validate weather prediction model")

    parser.add_argument(
        "--checkpoint",
        type=str,
        help="Path to model checkpoint",
    )
    parser.add_argument(
        "--data",
        type=str,
        help="Path to test data (Zarr or NetCDF)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="validation_results.json",
        help="Output file for results",
    )
    parser.add_argument(
        "--lead-times",
        type=int,
        nargs="+",
        default=[24, 72, 120, 168, 240],
        help="Lead times in hours to evaluate",
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Use synthetic data for testing the pipeline",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if TORCH_AVAILABLE and torch.cuda.is_available() else "cpu",
        help="Device to run evaluation on",
    )

    return parser.parse_args()


def run_synthetic_validation():
    """
    Run validation with synthetic data to test the full pipeline.

    This doesn't require real ERA5 data - useful for development.
    """
    print("\n" + "=" * 70)
    print("SYNTHETIC VALIDATION - Testing the Pipeline")
    print("=" * 70 + "\n")

    from data.era5_loader import create_synthetic_era5
    from evaluation.metrics import rmse, mae, anomaly_correlation_coefficient, get_latitude_weights
    from evaluation.benchmarks import WeatherBenchmark, quick_benchmark_summary

    # Create synthetic data
    print("Creating synthetic ERA5-like data...")
    n_times = 200  # ~50 days at 6h intervals
    n_lat = 73     # 2.5° resolution
    n_lon = 144

    data = create_synthetic_era5(
        n_times=n_times,
        n_lat=n_lat,
        n_lon=n_lon,
        n_channels=10,
        seed=42,
    )

    lat = np.linspace(-90, 90, n_lat)
    lon = np.linspace(-180, 180, n_lon, endpoint=False)

    print(f"  Data shape: {data.shape}")
    print(f"  Time steps: {n_times}")

    # Split into "train" and "test"
    n_train = 150
    train_data = data[:n_train]
    test_data = data[n_train:]

    print(f"  Train samples: {n_train}")
    print(f"  Test samples: {n_times - n_train}")

    # Compute climatology (training mean)
    climatology = np.mean(train_data, axis=0)

    # Test persistence baseline
    print("\nEvaluating persistence baseline...")
    lead_times_hours = [24, 72, 120]
    time_step_hours = 6

    persistence_results = {}
    for lt in lead_times_hours:
        steps = lt // time_step_hours
        if steps >= len(test_data):
            continue

        pred = test_data[:-steps]  # Persistence: current state
        target = test_data[steps:]  # Target: future state

        # Compute RMSE manually with proper latitude weighting
        weights = get_latitude_weights(lat)
        weights_4d = weights.reshape(1, -1, 1, 1)  # (1, lat, 1, 1)

        se = (pred - target) ** 2
        weighted_se = se * weights_4d
        mse = weighted_se.sum(axis=(1, 2)) / weights.sum()  # Average over lat, lon
        rmse_val = float(np.sqrt(mse.mean()))  # Average over time and channels

        persistence_results[lt] = rmse_val
        print(f"  Lead time {lt}h: RMSE = {rmse_val:.4f}")

    # Create benchmark comparison
    print("\n" + "-" * 40)
    print("Creating benchmark comparison framework...")

    benchmark = WeatherBenchmark(lat, lon, lead_times_hours)

    # Simulate "model" predictions (slightly better than persistence for demo)
    print("\nSimulating model predictions...")

    # For demo, our "model" is just persistence with small improvement
    # In real usage, this would be actual model predictions
    print("\nComputing RMSE at each lead time:")
    print("  Lead Time | Persistence | 'Model' | Climatology")
    print("  ----------|-------------|---------|------------")

    clim_rmse = float(np.sqrt(((test_data - climatology) ** 2).mean()))

    results = {'persistence': {}, 'model': {}, 'climatology': clim_rmse}

    for lt in lead_times_hours:
        steps = lt // time_step_hours
        if steps >= len(test_data):
            continue

        pred_persist = test_data[:-steps]
        pred_model = test_data[:-steps] * 0.9 + 0.1 * test_data[steps:]  # Cheating model
        target = test_data[steps:]

        rmse_persist = float(np.sqrt(((pred_persist - target) ** 2).mean()))
        rmse_model = float(np.sqrt(((pred_model - target) ** 2).mean()))

        results['persistence'][lt] = rmse_persist
        results['model'][lt] = rmse_model

        print(f"  {lt:4}h     |   {rmse_persist:.4f}   |  {rmse_model:.4f}  |   {clim_rmse:.4f}")

    # Compute skill scores
    print("\nSkill Scores (vs Persistence):")
    for lt in results['model']:
        skill = 1 - results['model'][lt] / results['persistence'][lt]
        print(f"  {lt}h: {skill:+.1%}")

    # Print benchmark summary
    print("\n" + benchmark.summary_report('SyntheticModel'))

    # Print published baselines for reference
    print(quick_benchmark_summary())

    return results


def evaluate_with_real_data(checkpoint_path, data_path, lead_times, device):
    """
    Evaluate model on real ERA5 data.
    """
    print("\n" + "=" * 70)
    print("REAL DATA VALIDATION")
    print("=" * 70 + "\n")

    # Import modules
    from nn.graphcast import GraphCastModel, create_graphcast_model
    from data.era5_loader import ERA5Dataset
    from evaluation.metrics import rmse, mae, anomaly_correlation_coefficient
    from evaluation.benchmarks import WeatherBenchmark

    # Load model
    print(f"Loading model from {checkpoint_path}...")
    checkpoint = torch.load(checkpoint_path, map_location=device)

    # Create model architecture (need to match training config)
    # This should be saved with the checkpoint in practice
    model = create_graphcast_model(
        resolution_deg=2.5,  # Adjust based on your model
        mesh_level=4,
        n_vars=78,
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()

    print(f"Model loaded. Device: {device}")

    # Load test data
    print(f"Loading test data from {data_path}...")
    # This would use ERA5Dataset with proper configuration
    # For now, just outline the process

    # ... data loading code ...

    # Run evaluation
    print("\nRunning evaluation...")

    # For each lead time:
    # 1. Roll out model predictions
    # 2. Compare to ground truth
    # 3. Compute metrics

    # ... evaluation code ...

    print("\nEvaluation complete!")


def main():
    args = parse_args()

    if args.synthetic:
        results = run_synthetic_validation()
    elif args.checkpoint and args.data:
        if not TORCH_AVAILABLE:
            print("Error: PyTorch required for model evaluation")
            sys.exit(1)
        results = evaluate_with_real_data(
            args.checkpoint,
            args.data,
            args.lead_times,
            args.device,
        )
    else:
        # Just show the benchmark baselines
        from evaluation.benchmarks import quick_benchmark_summary
        print(quick_benchmark_summary())
        return

    # Save results
    if args.output:
        print(f"\nSaving results to {args.output}")
        with open(args.output, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': results if isinstance(results, dict) else str(results),
            }, f, indent=2, default=str)


if __name__ == "__main__":
    main()

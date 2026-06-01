"""
Benchmark Baselines for Weather Forecast Evaluation

From First Principles:
======================

To claim a model is "good", we need to compare against established baselines.
Weather forecasting has well-defined baselines:

1. CLIMATOLOGY:
   The historical average for that day-of-year at that location.
   A model worse than climatology is useless.

2. PERSISTENCE:
   Predict tomorrow = today. Exploits autocorrelation.
   Good for very short-term (hours), fails for medium-range.

3. IFS HRES:
   ECMWF's operational physics-based model.
   The gold standard for 40+ years. ~10 billion USD invested.
   If you beat this, you've achieved something significant.

4. PUBLISHED ML BASELINES:
   GraphCast, Pangu-Weather, FourCastNet, GenCast
   These are the state-of-the-art ML models to beat.

WeatherBench 2 Scorecards:
==========================
WeatherBench 2 publishes standardized RMSE values for all models
at multiple lead times. These are our targets.

Published Results (approximate RMSE at key lead times):
------------------------------------------------------
Z500 (Geopotential at 500 hPa) [m²/s²]:
  Lead time (days):    1      3      5      7      10
  IFS HRES:           58     186    340    495    680
  GraphCast:          52     160    290    430    610
  Pangu-Weather:      55     170    310    460    650
  FourCastNet:        60     195    360    530    740

T850 (Temperature at 850 hPa) [K]:
  Lead time (days):    1      3      5      7      10
  IFS HRES:           0.72   1.32   1.85   2.30   2.85
  GraphCast:          0.68   1.20   1.70   2.15   2.70
  Pangu-Weather:      0.70   1.25   1.78   2.22   2.78
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from pathlib import Path
import json


# ============================================================================
# PUBLISHED BASELINE RESULTS (WeatherBench 2 / Papers)
# ============================================================================

@dataclass
class BaselineResult:
    """Published benchmark result."""
    model_name: str
    variable: str
    lead_time_hours: int
    rmse: float
    acc: Optional[float] = None
    source: str = "WeatherBench2"


# Published RMSE values from WeatherBench 2 and original papers
# These are approximate values - see WeatherBench2 for exact numbers
PUBLISHED_BASELINES = {
    # Z500 (Geopotential height at 500 hPa) - key upper-air variable
    'z500': {
        'IFS_HRES': {24: 58, 72: 186, 120: 340, 168: 495, 240: 680},
        'GraphCast': {24: 52, 72: 160, 120: 290, 168: 430, 240: 610},
        'Pangu-Weather': {24: 55, 72: 170, 120: 310, 168: 460, 240: 650},
        'FourCastNet': {24: 60, 72: 195, 120: 360, 168: 530, 240: 740},
        'GenCast': {24: 50, 72: 155, 120: 280, 168: 420, 240: 600},
        'Climatology': {24: 950, 72: 950, 120: 950, 168: 950, 240: 950},
        'Persistence': {24: 75, 72: 380, 120: 620, 168: 780, 240: 900},
    },

    # T850 (Temperature at 850 hPa) [K]
    't850': {
        'IFS_HRES': {24: 0.72, 72: 1.32, 120: 1.85, 168: 2.30, 240: 2.85},
        'GraphCast': {24: 0.68, 72: 1.20, 120: 1.70, 168: 2.15, 240: 2.70},
        'Pangu-Weather': {24: 0.70, 72: 1.25, 120: 1.78, 168: 2.22, 240: 2.78},
        'FourCastNet': {24: 0.75, 72: 1.38, 120: 1.95, 168: 2.45, 240: 3.05},
        'Climatology': {24: 3.5, 72: 3.5, 120: 3.5, 168: 3.5, 240: 3.5},
        'Persistence': {24: 0.9, 72: 2.2, 120: 3.1, 168: 3.4, 240: 3.5},
    },

    # T2m (2-meter temperature) [K]
    't2m': {
        'IFS_HRES': {24: 1.35, 72: 2.10, 120: 2.70, 168: 3.20, 240: 3.80},
        'GraphCast': {24: 1.28, 72: 1.95, 120: 2.55, 168: 3.05, 240: 3.65},
        'Pangu-Weather': {24: 1.30, 72: 2.00, 120: 2.62, 168: 3.12, 240: 3.72},
        'Climatology': {24: 5.5, 72: 5.5, 120: 5.5, 168: 5.5, 240: 5.5},
    },

    # U10 (10-meter U wind) [m/s]
    'u10': {
        'IFS_HRES': {24: 1.45, 72: 2.30, 120: 2.90, 168: 3.35, 240: 3.85},
        'GraphCast': {24: 1.38, 72: 2.15, 120: 2.75, 168: 3.20, 240: 3.70},
        'Climatology': {24: 4.2, 72: 4.2, 120: 4.2, 168: 4.2, 240: 4.2},
    },

    # MSL (Mean sea level pressure) [Pa]
    'msl': {
        'IFS_HRES': {24: 120, 72: 320, 120: 520, 168: 700, 240: 900},
        'GraphCast': {24: 105, 72: 280, 120: 460, 168: 630, 240: 820},
        'Climatology': {24: 1100, 72: 1100, 120: 1100, 168: 1100, 240: 1100},
    },
}

# ACC thresholds (Anomaly Correlation Coefficient)
ACC_THRESHOLDS = {
    'useful': 0.6,    # Minimum for useful synoptic forecast
    'good': 0.8,      # Good forecast
    'excellent': 0.9, # Excellent forecast
}


# ============================================================================
# BASELINE COMPUTATIONS
# ============================================================================

def compute_climatology_baseline(
    data: np.ndarray,
    timestamps: np.ndarray,
    n_years_baseline: int = 30,
) -> np.ndarray:
    """
    Compute climatological baseline (historical average for each day-of-year).

    From first principles:
    Climatology is the expected value of the atmosphere for a given day,
    computed from historical observations. It represents the "null model"
    that requires no forecasting skill - just memorization.

    A good forecast model MUST beat climatology, otherwise it's useless.

    Args:
        data: Historical data, shape (time, lat, lon, channels)
        timestamps: Datetime for each time step
        n_years_baseline: Number of years to use for baseline

    Returns:
        Climatological mean, shape (366, lat, lon, channels)
    """
    n_times, n_lat, n_lon, n_channels = data.shape

    # Accumulate statistics for each day of year
    clim_sum = np.zeros((366, n_lat, n_lon, n_channels), dtype=np.float64)
    clim_count = np.zeros(366, dtype=np.int64)

    for t, ts in enumerate(timestamps):
        doy = ts.timetuple().tm_yday - 1  # 0-indexed (0-365)
        clim_sum[doy] += data[t]
        clim_count[doy] += 1

    # Compute mean
    clim_count = np.maximum(clim_count, 1)[:, None, None, None]
    climatology = clim_sum / clim_count

    return climatology.astype(np.float32)


def compute_persistence_baseline(
    data: np.ndarray,
    lead_time_steps: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute persistence baseline (forecast = current observation).

    From first principles:
    Persistence exploits the temporal autocorrelation of weather.
    Tomorrow's weather is similar to today's weather.

    For very short lead times (hours), persistence is hard to beat.
    For medium-range (days), persistence fails because weather evolves.

    Args:
        data: Data array, shape (time, lat, lon, channels)
        lead_time_steps: Number of time steps for lead time

    Returns:
        (predictions, targets) arrays for computing metrics
    """
    # Persistence: forecast at t+lead = observation at t
    predictions = data[:-lead_time_steps]
    targets = data[lead_time_steps:]

    return predictions, targets


def compute_baseline_rmse(
    target: np.ndarray,
    baseline: np.ndarray,
    lat: np.ndarray,
) -> float:
    """Compute latitude-weighted RMSE of baseline against target."""
    from .metrics import latitude_weighted_rmse

    return float(latitude_weighted_rmse(baseline, target, lat).mean())


# ============================================================================
# BENCHMARK COMPARISON CLASS
# ============================================================================

class WeatherBenchmark:
    """
    Framework for benchmarking weather forecasts against baselines.

    This class:
    1. Loads/computes baseline predictions (climatology, persistence)
    2. Stores published results from other models
    3. Computes metrics for your model
    4. Generates comparison tables/plots
    """

    def __init__(
        self,
        lat: np.ndarray,
        lon: np.ndarray,
        lead_times_hours: List[int] = [24, 72, 120, 168, 240],
    ):
        """
        Initialize benchmark framework.

        Args:
            lat: Latitude array (degrees)
            lon: Longitude array (degrees)
            lead_times_hours: Lead times to evaluate (default: 1,3,5,7,10 days)
        """
        self.lat = lat
        self.lon = lon
        self.lead_times = lead_times_hours

        # Published baselines
        self.published_baselines = PUBLISHED_BASELINES

        # Computed baselines (to be filled)
        self.climatology: Optional[Dict[str, np.ndarray]] = None
        self.persistence_rmse: Optional[Dict[str, Dict[int, float]]] = None

        # Your model's results
        self.model_results: Dict[str, Dict[int, Dict[str, float]]] = {}

    def set_climatology(
        self,
        climatology: Dict[str, np.ndarray],
    ):
        """Set computed climatology for each variable."""
        self.climatology = climatology

    def compute_climatology_from_data(
        self,
        data: Dict[str, np.ndarray],
        timestamps: np.ndarray,
    ):
        """Compute climatology from historical data."""
        self.climatology = {}
        for var, arr in data.items():
            self.climatology[var] = compute_climatology_baseline(arr, timestamps)

    def evaluate_model(
        self,
        predictions: Dict[str, Dict[int, np.ndarray]],  # {var: {lead_time: array}}
        targets: Dict[str, Dict[int, np.ndarray]],
        model_name: str = "MyModel",
    ) -> Dict[str, Dict[int, Dict[str, float]]]:
        """
        Evaluate model predictions against targets.

        Args:
            predictions: {variable: {lead_time_hours: predictions_array}}
            targets: {variable: {lead_time_hours: targets_array}}
            model_name: Name for this model

        Returns:
            Results: {variable: {lead_time: {metric: value}}}
        """
        from .metrics import (
            rmse, mae, bias, anomaly_correlation_coefficient,
            get_latitude_weights, skill_score
        )

        results = {}
        weights = get_latitude_weights(self.lat)
        weights_2d = weights[:, np.newaxis]

        for var in predictions:
            if var not in targets:
                continue

            results[var] = {}

            for lead_time in predictions[var]:
                if lead_time not in targets[var]:
                    continue

                pred = predictions[var][lead_time]
                target = targets[var][lead_time]

                # Get climatology for ACC
                clim = None
                if self.climatology is not None and var in self.climatology:
                    clim = np.mean(self.climatology[var], axis=0)

                # Compute metrics
                rmse_val = float(rmse(pred, target, weights_2d, axis=(1, 2)).mean())
                mae_val = float(mae(pred, target, weights_2d, axis=(1, 2)).mean())
                bias_val = float(bias(pred, target, weights_2d, axis=(1, 2)).mean())

                metrics = {
                    'rmse': rmse_val,
                    'mae': mae_val,
                    'bias': bias_val,
                }

                # ACC (if climatology available)
                if clim is not None:
                    acc_val = float(anomaly_correlation_coefficient(
                        pred, target, clim, weights_2d, axis=(1, 2)
                    ).mean())
                    metrics['acc'] = acc_val

                # Skill scores vs baselines
                if var in self.published_baselines:
                    baselines = self.published_baselines[var]

                    if 'Climatology' in baselines and lead_time in baselines['Climatology']:
                        ss_clim = skill_score(rmse_val, baselines['Climatology'][lead_time])
                        metrics['skill_vs_climatology'] = float(ss_clim)

                    if 'IFS_HRES' in baselines and lead_time in baselines['IFS_HRES']:
                        ss_hres = skill_score(rmse_val, baselines['IFS_HRES'][lead_time])
                        metrics['skill_vs_IFS_HRES'] = float(ss_hres)

                results[var][lead_time] = metrics

        self.model_results[model_name] = results
        return results

    def comparison_table(
        self,
        variable: str,
        metric: str = 'rmse',
        model_names: Optional[List[str]] = None,
    ) -> str:
        """
        Generate comparison table as string.

        Args:
            variable: Variable to compare (e.g., 'z500')
            metric: Metric to show ('rmse', 'acc', etc.)
            model_names: Models to include (default: all)

        Returns:
            Formatted table string
        """
        if model_names is None:
            # Include published baselines + our models
            model_names = list(self.published_baselines.get(variable, {}).keys())
            model_names.extend(self.model_results.keys())
            model_names = list(set(model_names))

        # Header
        lines = [
            f"\n{variable.upper()} - {metric.upper()} Comparison",
            "=" * 60,
        ]

        # Column headers (lead times)
        header = f"{'Model':<20}"
        for lt in self.lead_times:
            header += f"{lt/24:.0f}d".rjust(10)
        lines.append(header)
        lines.append("-" * 60)

        # Rows (models)
        for model in model_names:
            row = f"{model:<20}"

            for lt in self.lead_times:
                val = None

                # Check published baselines
                if variable in self.published_baselines:
                    if model in self.published_baselines[variable]:
                        if lt in self.published_baselines[variable][model]:
                            val = self.published_baselines[variable][model][lt]

                # Check our model results
                if model in self.model_results:
                    if variable in self.model_results[model]:
                        if lt in self.model_results[model][variable]:
                            if metric in self.model_results[model][variable][lt]:
                                val = self.model_results[model][variable][lt][metric]

                if val is not None:
                    if metric == 'acc':
                        row += f"{val:.3f}".rjust(10)
                    elif val < 10:
                        row += f"{val:.2f}".rjust(10)
                    else:
                        row += f"{val:.0f}".rjust(10)
                else:
                    row += "-".rjust(10)

            lines.append(row)

        lines.append("-" * 60)
        return "\n".join(lines)

    def summary_report(self, model_name: str = None) -> str:
        """Generate full benchmark report."""
        lines = [
            "\n" + "=" * 70,
            "WEATHER FORECAST BENCHMARK REPORT",
            "=" * 70,
        ]

        # If model specified, focus on that
        if model_name and model_name in self.model_results:
            lines.append(f"\nModel: {model_name}")
            lines.append("-" * 40)

            for var in self.model_results[model_name]:
                lines.append(self.comparison_table(var, 'rmse'))

                # Check if we beat baselines
                for lt in self.lead_times:
                    if lt in self.model_results[model_name][var]:
                        result = self.model_results[model_name][var][lt]
                        if 'skill_vs_IFS_HRES' in result:
                            ss = result['skill_vs_IFS_HRES']
                            status = "BETTER" if ss > 0 else "WORSE"
                            lines.append(
                                f"  {lt/24:.0f}d: {status} than IFS HRES "
                                f"(skill score: {ss:+.1%})"
                            )
        else:
            # Show all comparison tables
            for var in ['z500', 't850', 't2m']:
                if var in self.published_baselines:
                    lines.append(self.comparison_table(var, 'rmse'))

        lines.append("\n" + "=" * 70)
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        """Export all results to dictionary."""
        return {
            'published_baselines': self.published_baselines,
            'model_results': self.model_results,
            'lead_times_hours': self.lead_times,
        }

    def save(self, path: Path):
        """Save results to JSON."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path, lat: np.ndarray, lon: np.ndarray) -> 'WeatherBenchmark':
        """Load results from JSON."""
        with open(path) as f:
            data = json.load(f)

        benchmark = cls(lat, lon, data['lead_times_hours'])
        benchmark.model_results = data['model_results']

        return benchmark


# ============================================================================
# QUICK BENCHMARK FUNCTIONS
# ============================================================================

def quick_benchmark_summary() -> str:
    """
    Print summary of published baselines without requiring data.

    Useful for understanding what scores to aim for.
    """
    lines = [
        "\n" + "=" * 70,
        "PUBLISHED WEATHER FORECASTING BENCHMARKS",
        "(WeatherBench 2 / Original Papers)",
        "=" * 70,
        "\nRMSE values at key lead times (days):",
    ]

    for var, models in PUBLISHED_BASELINES.items():
        lines.append(f"\n{var.upper()}:")
        lines.append("-" * 50)

        header = f"{'Model':<18}"
        for lt in [24, 72, 120, 168, 240]:
            header += f"{lt/24:.0f}d".rjust(8)
        lines.append(header)

        for model, values in models.items():
            row = f"{model:<18}"
            for lt in [24, 72, 120, 168, 240]:
                if lt in values:
                    val = values[lt]
                    if val < 10:
                        row += f"{val:.2f}".rjust(8)
                    else:
                        row += f"{val:.0f}".rjust(8)
                else:
                    row += "-".rjust(8)
            lines.append(row)

    lines.extend([
        "\n" + "=" * 70,
        "KEY INSIGHTS:",
        "- GraphCast beats IFS HRES on most variables",
        "- ~10-15% RMSE reduction vs traditional NWP",
        "- ACC > 0.6 required for 'useful' forecast",
        "- Climatology is easy to beat (high bar: IFS HRES)",
        "=" * 70,
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    print(quick_benchmark_summary())

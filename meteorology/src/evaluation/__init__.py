# Evaluation metrics and benchmarking
from .metrics import (
    rmse,
    mae,
    bias,
    anomaly_correlation_coefficient,
    skill_score,
    latitude_weighted_rmse,
    latitude_weighted_mae,
)
from .benchmarks import (
    compute_climatology_baseline,
    compute_persistence_baseline,
    WeatherBenchmark,
)

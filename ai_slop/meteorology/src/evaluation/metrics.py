"""
Weather Forecast Evaluation Metrics

From First Principles:
======================

Weather forecasting evaluation requires metrics that account for:
1. Spherical geometry (latitude weighting)
2. Scale of different variables
3. Skill relative to baseline forecasts
4. Both amplitude and pattern errors

Standard Metrics (following WeatherBench 2):
============================================

1. RMSE (Root Mean Square Error):
   RMSE = √(⟨(y_pred - y_true)²⟩)
   - Penalizes large errors more than small ones
   - Same units as the variable
   - Must be latitude-weighted for spherical data

2. MAE (Mean Absolute Error):
   MAE = ⟨|y_pred - y_true|⟩
   - More robust to outliers than RMSE
   - Linear penalty

3. Bias:
   Bias = ⟨y_pred - y_true⟩
   - Systematic over/under prediction
   - Should be near zero for good forecasts

4. ACC (Anomaly Correlation Coefficient):
   ACC = corr(y_pred - μ, y_true - μ)
   - Pattern correlation after removing climatology
   - Range [-1, 1], 1 is perfect
   - ACC > 0.6 considered "useful" for synoptic forecasting

5. Skill Score:
   SS = 1 - RMSE_model / RMSE_baseline
   - Improvement over baseline (climatology or persistence)
   - SS = 1: perfect forecast
   - SS = 0: same as baseline
   - SS < 0: worse than baseline

6. CRPS (Continuous Ranked Probability Score):
   - For probabilistic forecasts
   - Measures calibration and sharpness

Latitude Weighting:
==================
On a sphere, grid cells at different latitudes have different areas:
dA = R² cos(φ) dφ dλ

Unweighted metrics would over-emphasize polar regions.
Correct weighting: w(φ) = cos(φ)
"""

import numpy as np
from typing import Optional, Union, Tuple, Dict
import warnings

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


# ============================================================================
# LATITUDE WEIGHTING
# ============================================================================

def get_latitude_weights(
    lat: np.ndarray,
    normalize: bool = True,
) -> np.ndarray:
    """
    Compute latitude weighting factors.

    From first principles:
    The area element on a sphere is dA = R² cos(φ) dφ dλ.
    For equal grid spacing, weight by cos(latitude).

    Args:
        lat: Latitude values in degrees or radians
        normalize: If True, weights sum to 1

    Returns:
        Weight array with same shape as lat
    """
    # Convert to radians if needed (heuristic: if max > π, assume degrees)
    if np.max(np.abs(lat)) > np.pi:
        lat_rad = np.radians(lat)
    else:
        lat_rad = lat

    weights = np.cos(lat_rad)
    weights = np.maximum(weights, 0)  # Ensure non-negative

    if normalize:
        weights = weights / np.sum(weights)

    return weights


def weighted_mean(
    x: np.ndarray,
    weights: np.ndarray,
    axis: Optional[Union[int, Tuple[int, ...]]] = None,
) -> np.ndarray:
    """
    Compute weighted mean.

    Args:
        x: Data array
        weights: Weight array (broadcastable to x)
        axis: Axis or axes to reduce

    Returns:
        Weighted mean
    """
    return np.sum(x * weights, axis=axis) / np.sum(weights, axis=axis)


# ============================================================================
# BASIC METRICS (NumPy)
# ============================================================================

def rmse(
    pred: np.ndarray,
    target: np.ndarray,
    weights: Optional[np.ndarray] = None,
    axis: Optional[Union[int, Tuple[int, ...]]] = None,
) -> np.ndarray:
    """
    Root Mean Square Error.

    RMSE = √(⟨(pred - target)²⟩)

    Args:
        pred: Predictions
        target: Ground truth
        weights: Optional weights for averaging
        axis: Axis to reduce (default: all)

    Returns:
        RMSE value(s)
    """
    sq_error = (pred - target) ** 2

    if weights is not None:
        mse = weighted_mean(sq_error, weights, axis=axis)
    else:
        mse = np.mean(sq_error, axis=axis)

    return np.sqrt(mse)


def mae(
    pred: np.ndarray,
    target: np.ndarray,
    weights: Optional[np.ndarray] = None,
    axis: Optional[Union[int, Tuple[int, ...]]] = None,
) -> np.ndarray:
    """
    Mean Absolute Error.

    MAE = ⟨|pred - target|⟩
    """
    abs_error = np.abs(pred - target)

    if weights is not None:
        return weighted_mean(abs_error, weights, axis=axis)
    else:
        return np.mean(abs_error, axis=axis)


def bias(
    pred: np.ndarray,
    target: np.ndarray,
    weights: Optional[np.ndarray] = None,
    axis: Optional[Union[int, Tuple[int, ...]]] = None,
) -> np.ndarray:
    """
    Bias (mean error).

    Bias = ⟨pred - target⟩

    Positive bias: over-prediction
    Negative bias: under-prediction
    """
    error = pred - target

    if weights is not None:
        return weighted_mean(error, weights, axis=axis)
    else:
        return np.mean(error, axis=axis)


def anomaly_correlation_coefficient(
    pred: np.ndarray,
    target: np.ndarray,
    climatology: np.ndarray,
    weights: Optional[np.ndarray] = None,
    axis: Optional[Union[int, Tuple[int, ...]]] = None,
) -> np.ndarray:
    """
    Anomaly Correlation Coefficient (ACC).

    ACC = corr(pred - clim, target - clim)
        = ⟨(pred - clim)(target - clim)⟩ / (σ_pred · σ_target)

    This measures pattern correlation after removing the climatological mean.
    It answers: "Did the model predict the RIGHT anomalies in the RIGHT places?"

    Standard thresholds:
    - ACC > 0.6: "useful" forecast (synoptic scale)
    - ACC > 0.8: "good" forecast
    - ACC > 0.9: "excellent" forecast

    Args:
        pred: Predictions
        target: Ground truth
        climatology: Climatological mean (same shape as pred/target, or broadcastable)
        weights: Optional latitude weights
        axis: Axis to reduce (should be spatial axes)

    Returns:
        ACC value(s)
    """
    # Compute anomalies
    pred_anom = pred - climatology
    target_anom = target - climatology

    # Weighted means (for centering)
    if weights is not None:
        pred_mean = weighted_mean(pred_anom, weights, axis=axis)
        target_mean = weighted_mean(target_anom, weights, axis=axis)
    else:
        pred_mean = np.mean(pred_anom, axis=axis, keepdims=True)
        target_mean = np.mean(target_anom, axis=axis, keepdims=True)

    # Center anomalies
    pred_centered = pred_anom - pred_mean
    target_centered = target_anom - target_mean

    # Covariance and variances
    if weights is not None:
        cov = weighted_mean(pred_centered * target_centered, weights, axis=axis)
        var_pred = weighted_mean(pred_centered ** 2, weights, axis=axis)
        var_target = weighted_mean(target_centered ** 2, weights, axis=axis)
    else:
        cov = np.mean(pred_centered * target_centered, axis=axis)
        var_pred = np.mean(pred_centered ** 2, axis=axis)
        var_target = np.mean(target_centered ** 2, axis=axis)

    # Correlation
    denom = np.sqrt(var_pred * var_target)
    denom = np.maximum(denom, 1e-10)  # Avoid division by zero

    acc = cov / denom

    return acc


def skill_score(
    rmse_model: np.ndarray,
    rmse_baseline: np.ndarray,
) -> np.ndarray:
    """
    Skill Score relative to baseline.

    SS = 1 - RMSE_model / RMSE_baseline

    Interpretation:
    - SS = 1: Perfect forecast
    - SS = 0: Same skill as baseline
    - SS < 0: Worse than baseline (model is harmful!)

    Common baselines:
    - Climatology: Historical mean for that day/location
    - Persistence: Tomorrow = Today
    - IFS HRES: ECMWF operational model

    Args:
        rmse_model: RMSE of the model being evaluated
        rmse_baseline: RMSE of the baseline model

    Returns:
        Skill score
    """
    # Avoid division by zero
    rmse_baseline = np.maximum(rmse_baseline, 1e-10)

    return 1 - rmse_model / rmse_baseline


# ============================================================================
# LATITUDE-WEIGHTED METRICS
# ============================================================================

def latitude_weighted_rmse(
    pred: np.ndarray,
    target: np.ndarray,
    lat: np.ndarray,
    lat_axis: int = -2,
    reduce_axes: Optional[Tuple[int, ...]] = None,
) -> np.ndarray:
    """
    RMSE with proper latitude weighting for spherical data.

    Args:
        pred: Predictions, shape (..., lat, lon, ...)
        target: Ground truth, same shape
        lat: Latitude values (degrees)
        lat_axis: Which axis is latitude
        reduce_axes: Which axes to reduce (default: lat and lon)

    Returns:
        Latitude-weighted RMSE
    """
    weights = get_latitude_weights(lat, normalize=False)

    # Expand weights to match data shape
    shape = [1] * pred.ndim
    shape[lat_axis] = len(lat)
    weights = weights.reshape(shape)

    sq_error = (pred - target) ** 2

    if reduce_axes is None:
        # Default: reduce over lat and lon (assumed to be last two before channels)
        reduce_axes = (lat_axis, lat_axis + 1)

    # Weighted sum / sum of weights
    weighted_se = sq_error * weights
    mse = np.sum(weighted_se, axis=reduce_axes) / np.sum(weights)

    return np.sqrt(mse)


def latitude_weighted_mae(
    pred: np.ndarray,
    target: np.ndarray,
    lat: np.ndarray,
    lat_axis: int = -2,
    reduce_axes: Optional[Tuple[int, ...]] = None,
) -> np.ndarray:
    """
    MAE with latitude weighting.
    """
    weights = get_latitude_weights(lat, normalize=False)

    shape = [1] * pred.ndim
    shape[lat_axis] = len(lat)
    weights = weights.reshape(shape)

    abs_error = np.abs(pred - target)

    if reduce_axes is None:
        reduce_axes = (lat_axis, lat_axis + 1)

    weighted_ae = abs_error * weights
    mae_val = np.sum(weighted_ae, axis=reduce_axes) / np.sum(weights)

    return mae_val


# ============================================================================
# PROBABILISTIC METRICS
# ============================================================================

def crps(
    ensemble: np.ndarray,
    target: np.ndarray,
    axis: int = 0,
) -> np.ndarray:
    """
    Continuous Ranked Probability Score (CRPS).

    For probabilistic forecasts (ensembles), CRPS measures both:
    - Reliability (calibration): Is the ensemble spread appropriate?
    - Sharpness: Is the ensemble tight when possible?

    CRPS = E[|X - y|] - 0.5 * E[|X - X'|]

    where X, X' are independent draws from the forecast distribution
    and y is the observation.

    Lower CRPS is better. CRPS = 0 for perfect deterministic forecast.

    Args:
        ensemble: Ensemble predictions, shape (n_members, ...)
        target: Ground truth, shape (...)
        axis: Ensemble member axis

    Returns:
        CRPS value(s)
    """
    n_members = ensemble.shape[axis]

    # Move ensemble axis to first position
    ensemble = np.moveaxis(ensemble, axis, 0)

    # Term 1: E[|X - y|]
    term1 = np.mean(np.abs(ensemble - target), axis=0)

    # Term 2: E[|X - X'|] - computed using sorting trick
    # For a sorted ensemble x₁ ≤ x₂ ≤ ... ≤ xₙ:
    # E[|X - X'|] = (2/n²) Σᵢ (2i - n - 1) xᵢ

    sorted_ens = np.sort(ensemble, axis=0)
    weights = 2 * np.arange(1, n_members + 1) - n_members - 1
    weights = weights.reshape([-1] + [1] * (ensemble.ndim - 1))

    term2 = np.sum(weights * sorted_ens, axis=0) / (n_members ** 2)

    return term1 - term2


def spread_skill_ratio(
    ensemble: np.ndarray,
    target: np.ndarray,
    axis: int = 0,
) -> np.ndarray:
    """
    Spread-Skill Ratio for ensemble forecasts.

    SSR = ensemble_spread / RMSE(ensemble_mean, target)

    Interpretation:
    - SSR ≈ 1: Well-calibrated ensemble
    - SSR < 1: Under-dispersive (overconfident)
    - SSR > 1: Over-dispersive (underconfident)

    A well-calibrated ensemble should have spread that matches
    the actual forecast error.
    """
    ensemble = np.moveaxis(ensemble, axis, 0)

    # Ensemble mean and spread
    ens_mean = np.mean(ensemble, axis=0)
    ens_spread = np.std(ensemble, axis=0, ddof=0)

    # Skill (RMSE of ensemble mean)
    skill = np.sqrt(np.mean((ens_mean - target) ** 2))

    # Ratio
    ssr = np.mean(ens_spread) / skill

    return ssr


# ============================================================================
# TORCH VERSIONS (for use in training)
# ============================================================================

if TORCH_AVAILABLE:

    def torch_latitude_weighted_mse(
        pred: torch.Tensor,
        target: torch.Tensor,
        lat_weights: torch.Tensor,
    ) -> torch.Tensor:
        """
        Latitude-weighted MSE loss for PyTorch.

        Args:
            pred: Predictions (batch, lat, lon, channels)
            target: Ground truth, same shape
            lat_weights: Latitude weights (lat,)

        Returns:
            Scalar loss
        """
        # Reshape weights for broadcasting: (1, lat, 1, 1)
        weights = lat_weights.view(1, -1, 1, 1)

        # Weighted squared error
        se = (pred - target) ** 2
        weighted_se = se * weights

        # Normalize by total weight
        loss = weighted_se.sum() / (weights.sum() * pred.shape[0] * pred.shape[2] * pred.shape[3])

        return loss


    def torch_rmse(
        pred: torch.Tensor,
        target: torch.Tensor,
        lat_weights: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        RMSE for PyTorch, optionally latitude-weighted.
        """
        se = (pred - target) ** 2

        if lat_weights is not None:
            weights = lat_weights.view(1, -1, 1, 1)
            mse = (se * weights).sum() / weights.sum() / pred.shape[0] / pred.shape[2] / pred.shape[3]
        else:
            mse = se.mean()

        return torch.sqrt(mse)


# ============================================================================
# HEADLINE METRICS (WeatherBench 2 standard)
# ============================================================================

HEADLINE_VARIABLES = {
    'z500': 'Geopotential height at 500 hPa [m²/s²]',
    't850': 'Temperature at 850 hPa [K]',
    't2m': '2-meter temperature [K]',
    'u10': '10-meter U wind [m/s]',
    'v10': '10-meter V wind [m/s]',
    'msl': 'Mean sea level pressure [Pa]',
    'tp': 'Total precipitation [m]',
}

HEADLINE_LEAD_TIMES_HOURS = [24, 72, 120, 168, 240]  # 1, 3, 5, 7, 10 days


def compute_headline_metrics(
    predictions: Dict[str, np.ndarray],  # {variable: (time, lat, lon)}
    targets: Dict[str, np.ndarray],
    climatology: Dict[str, np.ndarray],
    lat: np.ndarray,
) -> Dict[str, Dict[str, float]]:
    """
    Compute WeatherBench 2 headline metrics.

    Returns dictionary structured as:
    {
        'z500': {'rmse': ..., 'acc': ..., 'bias': ...},
        't850': {...},
        ...
    }
    """
    results = {}
    weights = get_latitude_weights(lat)
    weights_2d = weights[:, np.newaxis]  # (lat, 1) for broadcasting

    for var in predictions:
        if var not in targets:
            continue

        pred = predictions[var]
        target = targets[var]
        clim = climatology.get(var, np.mean(target, axis=0, keepdims=True))

        results[var] = {
            'rmse': float(rmse(pred, target, weights_2d, axis=(1, 2)).mean()),
            'mae': float(mae(pred, target, weights_2d, axis=(1, 2)).mean()),
            'bias': float(bias(pred, target, weights_2d, axis=(1, 2)).mean()),
            'acc': float(anomaly_correlation_coefficient(
                pred, target, clim, weights_2d, axis=(1, 2)
            ).mean()),
        }

    return results

"""
Data Normalization for Weather Prediction

From First Principles:
======================

Neural networks train best when inputs have:
- Zero mean (centered)
- Unit variance (standardized)
- Similar scales across channels

For weather data, normalization is critical because variables span
vastly different scales:
- Temperature: 180-330 K
- Pressure: 40,000-110,000 Pa
- Specific humidity: 0-0.03 kg/kg
- Geopotential: 0-300,000 m²/s²
- Wind: -100 to +100 m/s

Normalization Strategy:
1. Per-channel: Each variable normalized independently
2. Per-level: For pressure level variables, normalize per level
3. Climatological: Use long-term mean/std (not per-sample)

The key insight is that we must use TRAINING SET statistics for
all normalization - this ensures no data leakage from val/test.
"""

import numpy as np
from typing import Optional, Dict, Union, Tuple
from pathlib import Path
import json


class Normalizer:
    """
    Standard normalization: z = (x - mean) / std

    Fits mean and std from training data, applies to all data.
    """

    def __init__(
        self,
        mean: np.ndarray,
        std: np.ndarray,
        eps: float = 1e-6,
    ):
        """
        Initialize with pre-computed statistics.

        Args:
            mean: Per-channel means, shape (n_channels,)
            std: Per-channel standard deviations, shape (n_channels,)
            eps: Small constant to prevent division by zero
        """
        self.mean = np.asarray(mean, dtype=np.float32)
        self.std = np.asarray(std, dtype=np.float32)
        self.eps = eps

        # Ensure std is not too small
        self.std = np.maximum(self.std, eps)

    @classmethod
    def from_data(cls, data: np.ndarray, axis: Tuple[int, ...] = (0, 1, 2)) -> 'Normalizer':
        """
        Compute normalization statistics from data.

        Args:
            data: Array of shape (time, lat, lon, channels)
            axis: Axes to reduce over (default: all except channels)

        Returns:
            Normalizer instance
        """
        mean = np.mean(data, axis=axis)
        std = np.std(data, axis=axis)

        return cls(mean, std)

    def normalize(self, x: np.ndarray) -> np.ndarray:
        """Normalize data: z = (x - mean) / std"""
        return (x - self.mean) / self.std

    def denormalize(self, z: np.ndarray) -> np.ndarray:
        """Reverse normalization: x = z * std + mean"""
        return z * self.std + self.mean

    def save(self, path: Path):
        """Save normalization statistics to file."""
        path = Path(path)
        np.savez(
            path,
            mean=self.mean,
            std=self.std,
            eps=np.array([self.eps]),
        )

    @classmethod
    def load(cls, path: Path) -> 'Normalizer':
        """Load normalization statistics from file."""
        data = np.load(path)
        return cls(
            mean=data['mean'],
            std=data['std'],
            eps=float(data['eps'][0]),
        )


class ClimateNormalizer:
    """
    Climate-based normalization using long-term climatology.

    For weather prediction, it's often better to predict ANOMALIES
    (departures from climatological mean) rather than absolute values.

    Climate statistics:
    - Mean: 30-year average for each (day-of-year, location, level)
    - Std: 30-year standard deviation

    This removes the seasonal cycle, making the prediction problem
    more stationary and easier to learn.
    """

    def __init__(
        self,
        clim_mean: np.ndarray,  # (366, lat, lon, channels) - daily climatology
        clim_std: np.ndarray,   # Same shape
        eps: float = 1e-6,
    ):
        """
        Initialize with climatological statistics.

        Args:
            clim_mean: Daily climatological mean (day-of-year, lat, lon, channels)
            clim_std: Daily climatological standard deviation
            eps: Minimum std to prevent division by zero
        """
        self.clim_mean = np.asarray(clim_mean, dtype=np.float32)
        self.clim_std = np.maximum(np.asarray(clim_std, dtype=np.float32), eps)
        self.eps = eps

    @classmethod
    def from_data(
        cls,
        data: np.ndarray,
        timestamps: np.ndarray,  # Array of datetime objects
    ) -> 'ClimateNormalizer':
        """
        Compute climatological statistics from multi-year data.

        Args:
            data: Array of shape (time, lat, lon, channels)
            timestamps: Array of datetime objects for each time step

        Returns:
            ClimateNormalizer instance
        """
        n_times, n_lat, n_lon, n_channels = data.shape

        # Initialize accumulators for each day of year
        clim_sum = np.zeros((366, n_lat, n_lon, n_channels), dtype=np.float64)
        clim_sq_sum = np.zeros((366, n_lat, n_lon, n_channels), dtype=np.float64)
        clim_count = np.zeros(366, dtype=np.int64)

        # Accumulate statistics
        for t, ts in enumerate(timestamps):
            # Day of year (1-366)
            doy = ts.timetuple().tm_yday - 1  # 0-indexed

            clim_sum[doy] += data[t]
            clim_sq_sum[doy] += data[t] ** 2
            clim_count[doy] += 1

        # Compute mean and std
        clim_count = np.maximum(clim_count, 1)[:, None, None, None]  # Avoid division by zero

        clim_mean = clim_sum / clim_count
        clim_var = clim_sq_sum / clim_count - clim_mean ** 2
        clim_std = np.sqrt(np.maximum(clim_var, 0))

        return cls(clim_mean.astype(np.float32), clim_std.astype(np.float32))

    def get_day_of_year(self, timestamp) -> int:
        """Extract day of year (0-365) from timestamp."""
        if hasattr(timestamp, 'timetuple'):
            return timestamp.timetuple().tm_yday - 1
        elif hasattr(timestamp, 'dayofyear'):
            return timestamp.dayofyear - 1
        else:
            raise ValueError(f"Cannot extract day of year from {type(timestamp)}")

    def normalize(
        self,
        x: np.ndarray,
        timestamps: Union[np.ndarray, list],
    ) -> np.ndarray:
        """
        Normalize data to anomalies.

        Args:
            x: Data array, shape (time, lat, lon, channels) or (lat, lon, channels)
            timestamps: Corresponding timestamps

        Returns:
            Normalized anomalies
        """
        if x.ndim == 3:
            # Single time step
            doy = self.get_day_of_year(timestamps)
            return (x - self.clim_mean[doy]) / self.clim_std[doy]
        else:
            # Multiple time steps
            result = np.zeros_like(x)
            for t, ts in enumerate(timestamps):
                doy = self.get_day_of_year(ts)
                result[t] = (x[t] - self.clim_mean[doy]) / self.clim_std[doy]
            return result

    def denormalize(
        self,
        z: np.ndarray,
        timestamps: Union[np.ndarray, list],
    ) -> np.ndarray:
        """Reverse normalization: convert anomalies back to absolute values."""
        if z.ndim == 3:
            doy = self.get_day_of_year(timestamps)
            return z * self.clim_std[doy] + self.clim_mean[doy]
        else:
            result = np.zeros_like(z)
            for t, ts in enumerate(timestamps):
                doy = self.get_day_of_year(ts)
                result[t] = z[t] * self.clim_std[doy] + self.clim_mean[doy]
            return result

    def save(self, path: Path):
        """Save climatological statistics."""
        np.savez(
            path,
            clim_mean=self.clim_mean,
            clim_std=self.clim_std,
            eps=np.array([self.eps]),
        )

    @classmethod
    def load(cls, path: Path) -> 'ClimateNormalizer':
        """Load climatological statistics."""
        data = np.load(path)
        return cls(
            clim_mean=data['clim_mean'],
            clim_std=data['clim_std'],
            eps=float(data['eps'][0]),
        )


class VariableNormalizer:
    """
    Per-variable normalization with different strategies.

    Different atmospheric variables may benefit from different
    normalization approaches:
    - Temperature: standardize
    - Humidity: log-transform then standardize (bounded, skewed)
    - Wind: standardize (symmetric around 0)
    - Precipitation: log1p transform (heavily skewed, bounded below)
    """

    def __init__(self, variable_configs: Dict[str, Dict]):
        """
        Initialize with per-variable configuration.

        Args:
            variable_configs: Dict mapping variable names to config dicts:
                {
                    'temperature': {'method': 'standardize', 'mean': 280, 'std': 20},
                    'precipitation': {'method': 'log1p', 'scale': 0.001},
                    ...
                }
        """
        self.configs = variable_configs

    def normalize_variable(
        self,
        x: np.ndarray,
        var_name: str,
    ) -> np.ndarray:
        """Normalize a single variable."""
        config = self.configs.get(var_name, {'method': 'standardize'})
        method = config['method']

        if method == 'standardize':
            mean = config.get('mean', 0)
            std = config.get('std', 1)
            return (x - mean) / std

        elif method == 'log1p':
            # log(1 + x/scale) - good for precipitation
            scale = config.get('scale', 1)
            return np.log1p(np.maximum(x, 0) / scale)

        elif method == 'logit':
            # logit(x) = log(x / (1-x)) - good for bounded [0, 1] variables
            eps = config.get('eps', 1e-6)
            x_clipped = np.clip(x, eps, 1 - eps)
            return np.log(x_clipped / (1 - x_clipped))

        elif method == 'sqrt':
            # sqrt transform - good for counts, mild skewness
            return np.sqrt(np.maximum(x, 0))

        elif method == 'none':
            return x

        else:
            raise ValueError(f"Unknown normalization method: {method}")

    def denormalize_variable(
        self,
        z: np.ndarray,
        var_name: str,
    ) -> np.ndarray:
        """Reverse normalization for a single variable."""
        config = self.configs.get(var_name, {'method': 'standardize'})
        method = config['method']

        if method == 'standardize':
            mean = config.get('mean', 0)
            std = config.get('std', 1)
            return z * std + mean

        elif method == 'log1p':
            scale = config.get('scale', 1)
            return (np.exp(z) - 1) * scale

        elif method == 'logit':
            return 1 / (1 + np.exp(-z))

        elif method == 'sqrt':
            return z ** 2

        elif method == 'none':
            return z

        else:
            raise ValueError(f"Unknown normalization method: {method}")


# ============================================================================
# STANDARD NORMALIZATION STATISTICS (from ERA5 climatology)
# ============================================================================

# Approximate global mean and std for common variables
# These are rough values - exact values should be computed from training data

ERA5_NORM_STATS = {
    # Upper-air variables (varies by level)
    'geopotential': {
        50: {'mean': 200000, 'std': 5000},
        100: {'mean': 160000, 'std': 4000},
        200: {'mean': 120000, 'std': 3000},
        300: {'mean': 93000, 'std': 2500},
        500: {'mean': 55000, 'std': 2000},
        700: {'mean': 31000, 'std': 1500},
        850: {'mean': 14000, 'std': 1000},
        925: {'mean': 7500, 'std': 800},
        1000: {'mean': 500, 'std': 500},
    },
    'temperature': {
        50: {'mean': 210, 'std': 10},
        100: {'mean': 205, 'std': 8},
        200: {'mean': 215, 'std': 10},
        300: {'mean': 230, 'std': 12},
        500: {'mean': 255, 'std': 15},
        700: {'mean': 275, 'std': 15},
        850: {'mean': 285, 'std': 15},
        925: {'mean': 290, 'std': 15},
        1000: {'mean': 290, 'std': 15},
    },
    'u_component_of_wind': {
        'all_levels': {'mean': 0, 'std': 15},
    },
    'v_component_of_wind': {
        'all_levels': {'mean': 0, 'std': 10},
    },
    'specific_humidity': {
        50: {'mean': 3e-6, 'std': 2e-6},
        100: {'mean': 5e-6, 'std': 3e-6},
        200: {'mean': 2e-5, 'std': 1e-5},
        300: {'mean': 1e-4, 'std': 5e-5},
        500: {'mean': 1e-3, 'std': 1e-3},
        700: {'mean': 4e-3, 'std': 3e-3},
        850: {'mean': 7e-3, 'std': 4e-3},
        925: {'mean': 9e-3, 'std': 5e-3},
        1000: {'mean': 1e-2, 'std': 5e-3},
    },
    # Surface variables
    '2m_temperature': {'mean': 285, 'std': 20},
    '10m_u_component_of_wind': {'mean': 0, 'std': 6},
    '10m_v_component_of_wind': {'mean': 0, 'std': 5},
    'mean_sea_level_pressure': {'mean': 101325, 'std': 1500},
    'total_precipitation': {'mean': 0, 'std': 0.001, 'method': 'log1p', 'scale': 0.0001},
}


def get_default_normalizer(n_channels: int) -> Normalizer:
    """
    Get a default normalizer with approximate ERA5 statistics.

    This is a fallback when you can't compute statistics from data.
    For production use, always compute statistics from your training set.
    """
    # Simple approximation: assume channels are roughly standardized
    mean = np.zeros(n_channels, dtype=np.float32)
    std = np.ones(n_channels, dtype=np.float32)

    return Normalizer(mean, std)


class ERA5Normalizer:
    """
    Normalizer for ERA5 cloud data using xarray/dask for efficient computation.

    Computes normalization statistics lazily using dask, allowing processing
    of massive datasets without loading everything into memory.
    """

    def __init__(self, stats_dict: Dict[str, Dict[str, np.ndarray]]):
        """
        Initialize with pre-computed statistics.

        Args:
            stats_dict: Dictionary mapping variable names to their stats:
                {
                    'temperature': {'mean': array(...), 'std': array(...)},
                    '2m_temperature': {'mean': float, 'std': float},
                    ...
                }
        """
        self.stats = stats_dict

    @classmethod
    def from_era5_dataset(
        cls,
        ds,  # xarray Dataset
        variables: Optional[list] = None,
        sample_size: int = 1000,  # Number of timesteps to sample for stats
    ) -> 'ERA5Normalizer':
        """
        Compute normalization statistics from an xarray ERA5 dataset.

        Uses random sampling of timesteps to efficiently estimate mean/std
        without loading the entire dataset into memory.

        Args:
            ds: xarray Dataset (lazy dask-backed)
            variables: List of variables to compute stats for (default: all)
            sample_size: Number of timesteps to sample

        Returns:
            ERA5Normalizer instance
        """
        import dask.array as da

        if variables is None:
            variables = list(ds.data_vars)

        # Sample random timesteps for efficiency
        n_times = len(ds.time)
        if n_times > sample_size:
            np.random.seed(42)  # Reproducibility
            sample_indices = np.sort(np.random.choice(n_times, sample_size, replace=False))
            ds_sample = ds.isel(time=sample_indices)
        else:
            ds_sample = ds

        stats = {}
        print(f"Computing normalization statistics for {len(variables)} variables...")

        for var in variables:
            if var not in ds_sample.data_vars:
                continue

            da_var = ds_sample[var]
            dims = da_var.dims

            # Compute mean and std, reducing over time and spatial dimensions
            if 'level' in dims:
                # For pressure-level variables, compute stats per level
                reduce_dims = [d for d in dims if d not in ['level']]
                mean = da_var.mean(dim=reduce_dims).compute().values
                std = da_var.std(dim=reduce_dims).compute().values
            else:
                # For surface variables, reduce over all dimensions
                mean = float(da_var.mean().compute())
                std = float(da_var.std().compute())

            stats[var] = {'mean': mean, 'std': std}
            print(f"  {var}: mean shape={np.shape(mean)}, std shape={np.shape(std)}")

        return cls(stats)

    def normalize_variable(self, data: np.ndarray, var_name: str) -> np.ndarray:
        """Normalize a single variable."""
        if var_name not in self.stats:
            return data  # Return unchanged if no stats

        mean = self.stats[var_name]['mean']
        std = self.stats[var_name]['std']

        # Ensure std is not zero
        std = np.maximum(std, 1e-6)

        return (data - mean) / std

    def denormalize_variable(self, data: np.ndarray, var_name: str) -> np.ndarray:
        """Reverse normalization for a single variable."""
        if var_name not in self.stats:
            return data

        mean = self.stats[var_name]['mean']
        std = self.stats[var_name]['std']
        std = np.maximum(std, 1e-6)

        return data * std + mean

    def save(self, path: Path):
        """Save statistics to file."""
        path = Path(path)
        # Convert to serializable format
        save_dict = {}
        for var, stat in self.stats.items():
            save_dict[var] = {
                'mean': np.asarray(stat['mean']).tolist(),
                'std': np.asarray(stat['std']).tolist(),
            }
        with open(path, 'w') as f:
            json.dump(save_dict, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'ERA5Normalizer':
        """Load statistics from file."""
        with open(path, 'r') as f:
            load_dict = json.load(f)
        # Convert back to numpy
        stats = {}
        for var, stat in load_dict.items():
            stats[var] = {
                'mean': np.array(stat['mean']),
                'std': np.array(stat['std']),
            }
        return cls(stats)

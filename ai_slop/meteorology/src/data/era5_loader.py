"""
ERA5 Data Loading Pipeline

From First Principles:
======================

ERA5 is the 5th generation ECMWF reanalysis covering 1940-present.
It provides hourly estimates of atmospheric variables at 0.25° resolution
(~31 km) on 137 model levels or 37 pressure levels.

"Reanalysis" means:
- A weather model is run retrospectively
- Real observations (satellites, weather stations, radiosondes) are assimilated
- This produces a physically consistent "best estimate" of past weather
- ERA5 is effectively "ground truth" for ML weather models

Data Sources:
- Google Cloud: gs://gcp-public-data-arco-era5 (Zarr format, ML-optimized)
- ECMWF Anemoi: Training-ready version (2025)
- Copernicus CDS: Original source (GRIB/NetCDF)

WeatherBench 2 Splits:
- Training: 1979-01-01 to 2017-12-31
- Validation: 2018-01-01 to 2019-12-31
- Test: 2020-01-01 to 2021-12-31

Key Variables (following GraphCast/WeatherBench2):
- Pressure levels: 50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000 hPa
- Upper air: geopotential (z), temperature (t), u-wind, v-wind, specific_humidity (q)
- Surface: 2m_temperature, 10m_u/v_wind, mean_sea_level_pressure, total_precipitation
"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import warnings

try:
    import xarray as xr
    import zarr
    XARRAY_AVAILABLE = True
except ImportError:
    XARRAY_AVAILABLE = False
    warnings.warn("xarray/zarr not available. Install with: pip install xarray zarr")

try:
    import torch
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class ERA5Config:
    """Configuration for ERA5 data loading."""

    # Pressure levels (hPa) - 13 levels following GraphCast
    pressure_levels: Tuple[int, ...] = (
        50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 850, 925, 1000
    )

    # Upper-air variables (per pressure level)
    upper_air_vars: Tuple[str, ...] = (
        'geopotential',           # z [m²/s²]
        'temperature',            # t [K]
        'u_component_of_wind',    # u [m/s]
        'v_component_of_wind',    # v [m/s]
        'specific_humidity',      # q [kg/kg]
    )

    # Surface variables
    surface_vars: Tuple[str, ...] = (
        '2m_temperature',                # t2m [K]
        '10m_u_component_of_wind',       # u10 [m/s]
        '10m_v_component_of_wind',       # v10 [m/s]
        'mean_sea_level_pressure',       # msl [Pa]
        'total_precipitation',           # tp [m] (accumulated)
    )

    # Forcing variables (time-dependent external forcing)
    forcing_vars: Tuple[str, ...] = (
        'toa_incident_solar_radiation',  # tisr [J/m²]
    )

    # Static variables (time-independent)
    static_vars: Tuple[str, ...] = (
        'land_sea_mask',
        'orography',
        'latitude',
        'longitude',
    )

    # Time configuration
    time_step_hours: int = 6  # Δt = 6 hours (following GraphCast)
    input_steps: int = 2      # Use X_t and X_{t-Δt}

    # Grid resolution
    resolution_deg: float = 0.25  # Native ERA5 resolution

    @property
    def n_pressure_levels(self) -> int:
        return len(self.pressure_levels)

    @property
    def n_upper_air_vars(self) -> int:
        return len(self.upper_air_vars)

    @property
    def n_surface_vars(self) -> int:
        return len(self.surface_vars)

    @property
    def total_input_channels(self) -> int:
        """Total number of input channels."""
        # Upper-air: n_vars × n_levels
        # Surface: n_surface_vars
        # Forcing: n_forcing_vars
        # Static: n_static_vars
        # × input_steps for temporal
        n_atmospheric = (
            self.n_upper_air_vars * self.n_pressure_levels +
            self.n_surface_vars
        )
        return n_atmospheric * self.input_steps + len(self.forcing_vars) + len(self.static_vars)


# WeatherBench 2 standard configuration
WEATHERBENCH2_CONFIG = ERA5Config()

# Simplified configuration for faster experiments
FAST_CONFIG = ERA5Config(
    pressure_levels=(500, 700, 850, 1000),
    upper_air_vars=('geopotential', 'temperature', 'u_component_of_wind', 'v_component_of_wind'),
    surface_vars=('2m_temperature', 'mean_sea_level_pressure'),
    forcing_vars=(),
    static_vars=('land_sea_mask',),
    resolution_deg=1.0,
)


# ============================================================================
# DATA SPLITS (WeatherBench 2 standard)
# ============================================================================

WEATHERBENCH_SPLITS = {
    'train': ('1979-01-01', '2017-12-31'),
    'validation': ('2018-01-01', '2019-12-31'),
    'test': ('2020-01-01', '2021-12-31'),
}

def get_train_val_test_splits(
    custom_splits: Optional[Dict[str, Tuple[str, str]]] = None
) -> Dict[str, Tuple[datetime, datetime]]:
    """
    Get datetime ranges for train/val/test splits.

    Default uses WeatherBench 2 standard splits:
    - Train: 1979-2017 (39 years)
    - Validation: 2018-2019 (2 years)
    - Test: 2020-2021 (2 years)
    """
    splits = custom_splits or WEATHERBENCH_SPLITS

    return {
        name: (
            datetime.fromisoformat(start),
            datetime.fromisoformat(end)
        )
        for name, (start, end) in splits.items()
    }


# ============================================================================
# DATA LOADING
# ============================================================================

class ERA5CloudLoader:
    """
    Load ERA5 data from Google Cloud Storage (ARCO-ERA5).

    ARCO = Analysis-Ready, Cloud-Optimized
    Data is stored in Zarr format, optimized for ML workflows.

    Bucket: gs://gcp-public-data-arco-era5

    Dataset structure (full_37-1h-0p25deg-chunk-1.zarr-v3):
    - Dimensions: time (1,323,648), latitude (721), longitude (1440), level (37)
    - Coordinates: latitude 90.0 to -90.0, longitude 0.0 to 359.75
    - 273 variables including surface and pressure-level data
    """

    # Google Cloud paths
    GCS_BUCKET = "gcp-public-data-arco-era5"
    # The full dataset contains both surface and pressure-level variables
    FULL_DATA_PATH = f"{GCS_BUCKET}/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"

    # Variable name mappings (ARCO-ERA5 uses descriptive names)
    VAR_MAPPING = {
        # Upper-air (pressure-level) variables
        'geopotential': 'geopotential',
        'temperature': 'temperature',
        'u_component_of_wind': 'u_component_of_wind',
        'v_component_of_wind': 'v_component_of_wind',
        'specific_humidity': 'specific_humidity',
        # Surface variables
        '2m_temperature': '2m_temperature',
        '10m_u_component_of_wind': '10m_u_component_of_wind',
        '10m_v_component_of_wind': '10m_v_component_of_wind',
        'mean_sea_level_pressure': 'mean_sea_level_pressure',
        'total_precipitation': 'total_precipitation',
        # Forcing
        'toa_incident_solar_radiation': 'toa_incident_solar_radiation',
    }

    def __init__(self, cache_dir: Optional[Path] = None, verbose: bool = True):
        """
        Initialize the cloud data loader.

        Args:
            cache_dir: Local directory for caching downloaded data
            verbose: Whether to print status messages
        """
        self.cache_dir = cache_dir or Path.home() / ".cache" / "era5"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose

        self._dataset = None
        self._fs = None

    def _log(self, message: str):
        """Print message if verbose mode is on."""
        if self.verbose:
            print(message)

    def _get_filesystem(self):
        """Get or create GCS filesystem."""
        if self._fs is None:
            import gcsfs
            self._fs = gcsfs.GCSFileSystem(token='anon')
        return self._fs

    def _open_zarr(self, path: str) -> 'xr.Dataset':
        """Open a Zarr store from GCS with lazy loading via dask."""
        if not XARRAY_AVAILABLE:
            raise ImportError("xarray and zarr required. Install with: pip install xarray zarr gcsfs dask")

        import gcsfs as gcsfs_module
        fs = self._get_filesystem()
        store = gcsfs_module.GCSMap(path, gcs=fs, check=False)
        return xr.open_zarr(store, consolidated=True)

    @property
    def dataset(self) -> 'xr.Dataset':
        """Lazy-load the full ERA5 dataset (dask-backed, no memory usage until compute)."""
        if self._dataset is None:
            self._log(f"Opening ERA5 dataset from gs://{self.FULL_DATA_PATH}...")
            self._dataset = self._open_zarr(self.FULL_DATA_PATH)
            self._log(f"  Dataset loaded: {len(self._dataset.data_vars)} variables")
            self._log(f"  Time range: {self._dataset.time.values[0]} to {self._dataset.time.values[-1]}")
        return self._dataset

    def get_available_variables(self) -> List[str]:
        """Return list of available variables in the dataset."""
        return list(self.dataset.data_vars)

    def load_time_range(
        self,
        start: Union[str, datetime],
        end: Union[str, datetime],
        config: ERA5Config = WEATHERBENCH2_CONFIG,
        variables: Optional[List[str]] = None,
        time_step: int = 6,  # Hours between samples
        lazy: bool = True,
    ) -> 'xr.Dataset':
        """
        Load data for a specific time range.

        Args:
            start: Start datetime (string or datetime object)
            end: End datetime
            config: ERA5 configuration
            variables: Specific variables to load (default: all in config)
            time_step: Hours between samples (6 = every 6 hours, default ERA5 timestep)
            lazy: If True, return dask-backed lazy array; if False, load into memory

        Returns:
            xarray Dataset with requested data (lazy unless specified)
        """
        # Convert to string for xarray selection
        if isinstance(start, datetime):
            start = start.isoformat()
        if isinstance(end, datetime):
            end = end.isoformat()

        # Determine variables to load
        if variables is None:
            vars_to_load = []
            # Add upper-air variables
            for var in config.upper_air_vars:
                mapped = self.VAR_MAPPING.get(var, var)
                if mapped in self.dataset.data_vars:
                    vars_to_load.append(mapped)
            # Add surface variables
            for var in config.surface_vars:
                mapped = self.VAR_MAPPING.get(var, var)
                if mapped in self.dataset.data_vars:
                    vars_to_load.append(mapped)
        else:
            vars_to_load = [self.VAR_MAPPING.get(v, v) for v in variables
                          if self.VAR_MAPPING.get(v, v) in self.dataset.data_vars]

        if not vars_to_load:
            raise ValueError(f"No valid variables found. Available: {self.get_available_variables()[:10]}...")

        self._log(f"Loading {len(vars_to_load)} variables from {start} to {end}")

        # Select variables and time range
        ds = self.dataset[vars_to_load]
        ds = ds.sel(time=slice(start, end))

        # Subsample time if needed (ERA5 is hourly, we may want 6-hourly)
        if time_step > 1:
            ds = ds.isel(time=slice(None, None, time_step))

        # Select pressure levels if applicable
        if 'level' in ds.dims:
            available_levels = ds.level.values
            requested_levels = [l for l in config.pressure_levels if l in available_levels]
            if requested_levels:
                ds = ds.sel(level=requested_levels)
                self._log(f"  Selected {len(requested_levels)} pressure levels")

        self._log(f"  Result shape: time={len(ds.time)}, variables={len(ds.data_vars)}")

        # Optionally load into memory
        if not lazy:
            self._log("  Loading into memory...")
            ds = ds.compute()

        return ds

    def load_sample(
        self,
        time: Union[str, datetime],
        variables: Optional[List[str]] = None,
        region: Optional[Dict[str, slice]] = None,
    ) -> 'xr.Dataset':
        """
        Load a single time sample (useful for testing connection).

        Args:
            time: Specific time to load
            variables: Variables to load (default: 2m_temperature, geopotential)
            region: Optional spatial subset (e.g., {'latitude': slice(60, 30), 'longitude': slice(0, 30)})

        Returns:
            xarray Dataset for single timestep
        """
        if variables is None:
            variables = ['2m_temperature', 'geopotential']

        # Map variable names
        vars_to_load = [self.VAR_MAPPING.get(v, v) for v in variables
                       if self.VAR_MAPPING.get(v, v) in self.dataset.data_vars]

        if not vars_to_load:
            # Fall back to first available variable
            vars_to_load = [list(self.dataset.data_vars)[0]]

        ds = self.dataset[vars_to_load]

        # Select nearest time
        if isinstance(time, str):
            time = np.datetime64(time)
        ds = ds.sel(time=time, method='nearest')

        # Optional spatial subset
        if region:
            ds = ds.sel(**region)

        # For pressure-level data, take 500 hPa as representative level
        if 'level' in ds.dims:
            if 500 in ds.level.values:
                ds = ds.sel(level=500)
            else:
                ds = ds.isel(level=0)

        return ds.compute()


class ERA5LocalLoader:
    """
    Load ERA5 data from local files (NetCDF or Zarr).

    For users who have downloaded ERA5 data locally.
    """

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

    def load_file(self, filepath: Path) -> 'xr.Dataset':
        """Load a single file."""
        if not XARRAY_AVAILABLE:
            raise ImportError("xarray required")

        suffix = filepath.suffix.lower()
        if suffix == '.zarr' or filepath.is_dir():
            return xr.open_zarr(filepath)
        elif suffix in ['.nc', '.nc4', '.netcdf']:
            return xr.open_dataset(filepath)
        else:
            raise ValueError(f"Unknown file format: {suffix}")


# ============================================================================
# PYTORCH DATASET
# ============================================================================

if TORCH_AVAILABLE:

    class ERA5Dataset(Dataset):
        """
        PyTorch Dataset for ERA5 weather data.

        Each sample consists of:
        - Input: [X_{t-Δt}, X_t] concatenated
        - Target: X_{t+Δt}

        For autoregressive training, we also need to provide
        targets at multiple lead times.
        """

        def __init__(
            self,
            data: Union['xr.Dataset', np.ndarray, Path],
            config: ERA5Config = WEATHERBENCH2_CONFIG,
            lead_times: List[int] = [1],  # Multiples of time_step_hours
            normalize: bool = True,
            normalizer: Optional['Normalizer'] = None,
        ):
            """
            Initialize the dataset.

            Args:
                data: xarray Dataset, numpy array, or path to data
                config: ERA5 configuration
                lead_times: List of lead times in time steps
                normalize: Whether to normalize data
                normalizer: Pre-computed normalizer (for val/test sets)
            """
            self.config = config
            self.lead_times = lead_times
            self.max_lead_time = max(lead_times)

            # Load data if path provided
            if isinstance(data, (str, Path)):
                if not XARRAY_AVAILABLE:
                    raise ImportError("xarray required to load from path")
                data = xr.open_zarr(data)

            # Convert to numpy if xarray
            if XARRAY_AVAILABLE and isinstance(data, xr.Dataset):
                self.data = self._xarray_to_numpy(data)
            else:
                self.data = data

            # data shape: (time, lat, lon, channels)
            self.n_times, self.n_lat, self.n_lon, self.n_channels = self.data.shape

            # Number of valid samples (need input_steps before and max_lead_time after)
            self.n_samples = self.n_times - config.input_steps - self.max_lead_time + 1

            # Normalization
            self.normalize = normalize
            if normalize:
                if normalizer is not None:
                    self.normalizer = normalizer
                else:
                    from .normalization import Normalizer
                    self.normalizer = Normalizer.from_data(self.data)
            else:
                self.normalizer = None

        def _xarray_to_numpy(self, ds: 'xr.Dataset') -> np.ndarray:
            """Convert xarray dataset to numpy array."""
            # Stack all variables into a single array
            arrays = []

            for var in ds.data_vars:
                arr = ds[var].values
                # Handle pressure levels
                if 'level' in ds[var].dims:
                    # Reshape (time, level, lat, lon) -> (time, lat, lon, level)
                    arr = np.moveaxis(arr, 1, -1)
                    # Flatten levels into channels
                    arr = arr.reshape(arr.shape[0], arr.shape[1], arr.shape[2], -1)
                else:
                    # Add channel dimension
                    arr = arr[..., np.newaxis]
                arrays.append(arr)

            # Concatenate along channel dimension
            return np.concatenate(arrays, axis=-1).astype(np.float32)

        def __len__(self) -> int:
            return self.n_samples

        def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
            """
            Get a training sample.

            Returns dictionary with:
            - 'input': [X_{t-Δt}, X_t] concatenated, shape (lat, lon, 2*channels)
            - 'target': X_{t+Δt} for each lead time, shape (n_lead_times, lat, lon, channels)
            - 'timestamps': time indices for input and targets
            """
            # Time indices
            t_prev = idx
            t_curr = idx + 1
            t_targets = [idx + 1 + lt for lt in self.lead_times]

            # Get data
            x_prev = self.data[t_prev]
            x_curr = self.data[t_curr]

            # Normalize
            if self.normalizer is not None:
                x_prev = self.normalizer.normalize(x_prev)
                x_curr = self.normalizer.normalize(x_curr)

            # Concatenate inputs
            x_input = np.concatenate([x_prev, x_curr], axis=-1)

            # Get targets
            targets = []
            for t in t_targets:
                target = self.data[t]
                if self.normalizer is not None:
                    target = self.normalizer.normalize(target)
                targets.append(target)

            targets = np.stack(targets, axis=0)

            return {
                'input': torch.from_numpy(x_input),
                'target': torch.from_numpy(targets),
                'timestamps': {
                    't_prev': t_prev,
                    't_curr': t_curr,
                    't_targets': t_targets,
                }
            }


    class ERA5DataModule:
        """
        Data module for managing train/val/test datasets.

        Handles:
        - Loading data for each split
        - Consistent normalization (fit on train, apply to val/test)
        - DataLoader creation
        """

        def __init__(
            self,
            data_source: Union[str, Path, ERA5CloudLoader],
            config: ERA5Config = WEATHERBENCH2_CONFIG,
            batch_size: int = 32,
            num_workers: int = 4,
            lead_times: List[int] = [1, 2, 4, 8, 16, 20, 28, 40],  # Up to 10 days
        ):
            self.config = config
            self.batch_size = batch_size
            self.num_workers = num_workers
            self.lead_times = lead_times

            self.data_source = data_source
            self.splits = get_train_val_test_splits()

            self._train_dataset = None
            self._val_dataset = None
            self._test_dataset = None
            self._normalizer = None

        def setup(self, stage: Optional[str] = None):
            """Load and prepare datasets."""
            if isinstance(self.data_source, ERA5CloudLoader):
                loader = self.data_source
            elif isinstance(self.data_source, (str, Path)):
                loader = ERA5LocalLoader(Path(self.data_source))
            else:
                raise ValueError(f"Unknown data source type: {type(self.data_source)}")

            # Load training data and fit normalizer
            if stage in (None, 'fit', 'train'):
                train_start, train_end = self.splits['train']
                train_data = loader.load_time_range(train_start, train_end, self.config)

                self._train_dataset = ERA5Dataset(
                    train_data, self.config, self.lead_times, normalize=True
                )
                self._normalizer = self._train_dataset.normalizer

            # Load validation data
            if stage in (None, 'fit', 'validate'):
                val_start, val_end = self.splits['validation']
                val_data = loader.load_time_range(val_start, val_end, self.config)

                self._val_dataset = ERA5Dataset(
                    val_data, self.config, self.lead_times,
                    normalize=True, normalizer=self._normalizer
                )

            # Load test data
            if stage in (None, 'test'):
                test_start, test_end = self.splits['test']
                test_data = loader.load_time_range(test_start, test_end, self.config)

                self._test_dataset = ERA5Dataset(
                    test_data, self.config, self.lead_times,
                    normalize=True, normalizer=self._normalizer
                )

        def train_dataloader(self) -> DataLoader:
            return DataLoader(
                self._train_dataset,
                batch_size=self.batch_size,
                shuffle=True,
                num_workers=self.num_workers,
                pin_memory=True,
            )

        def val_dataloader(self) -> DataLoader:
            return DataLoader(
                self._val_dataset,
                batch_size=self.batch_size,
                shuffle=False,
                num_workers=self.num_workers,
                pin_memory=True,
            )

        def test_dataloader(self) -> DataLoader:
            return DataLoader(
                self._test_dataset,
                batch_size=self.batch_size,
                shuffle=False,
                num_workers=self.num_workers,
                pin_memory=True,
            )


# ============================================================================
# SYNTHETIC DATA FOR TESTING
# ============================================================================

def create_synthetic_era5(
    n_times: int = 100,
    n_lat: int = 73,
    n_lon: int = 144,
    n_channels: int = 78,
    seed: int = 42,
) -> np.ndarray:
    """
    Create synthetic ERA5-like data for testing.

    The synthetic data has:
    - Realistic spatial correlations (smooth fields)
    - Temporal correlations (persistence + random walk)
    - Approximately Gaussian statistics

    Args:
        n_times: Number of time steps
        n_lat: Number of latitude points
        n_lon: Number of longitude points
        n_channels: Number of channels (variables)
        seed: Random seed

    Returns:
        Array of shape (n_times, n_lat, n_lon, n_channels)
    """
    np.random.seed(seed)

    # Initialize
    data = np.zeros((n_times, n_lat, n_lon, n_channels), dtype=np.float32)

    # Create smooth spatial patterns using random Fourier modes
    lat = np.linspace(-90, 90, n_lat)
    lon = np.linspace(-180, 180, n_lon, endpoint=False)
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # Generate random initial field for each channel
    for c in range(n_channels):
        # Low-frequency spatial pattern (wavenumbers 1-5)
        field = np.zeros((n_lat, n_lon))
        for k in range(1, 6):
            for l in range(1, 6):
                amp = np.random.randn() / (k + l)
                phase_lat = np.random.uniform(0, 2*np.pi)
                phase_lon = np.random.uniform(0, 2*np.pi)
                field += amp * np.outer(
                    np.cos(k * lat_rad + phase_lat),
                    np.cos(l * lon_rad + phase_lon)
                )

        data[0, :, :, c] = field

    # Temporal evolution: AR(1) process with spatial noise
    persistence = 0.9  # High autocorrelation
    noise_scale = 0.1

    for t in range(1, n_times):
        # Persist previous state
        data[t] = persistence * data[t-1]

        # Add smooth spatial noise
        for c in range(n_channels):
            noise = np.random.randn(n_lat, n_lon).astype(np.float32)
            # Smooth the noise
            from scipy.ndimage import gaussian_filter
            noise = gaussian_filter(noise, sigma=3)
            data[t, :, :, c] += noise_scale * noise

    return data

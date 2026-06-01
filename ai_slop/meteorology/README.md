# GraphCast-Style Weather Prediction Engine

A from-first-principles implementation of weather forecasting using Graph Neural Networks, inspired by DeepMind's GraphCast.

## Project Structure

```
meteorology/
├── FIRST_PRINCIPLES.md          # Theoretical foundation document
├── README.md                    # This file
├── requirements.txt             # Dependencies
├── demo.py                      # Quick demonstration
├── src/
│   ├── geometry/               # Spherical geometry & icosahedral mesh
│   │   ├── spherical_math.py   # Coordinates, distances, Coriolis
│   │   └── icosahedral_mesh.py # Platonic solid mesh generation
│   ├── nn/                     # Neural network modules
│   │   ├── message_passing.py  # GNN layers (PDE ↔ GNN analogy)
│   │   ├── encoder_decoder.py  # Grid ↔ Mesh mappings
│   │   └── graphcast.py        # Full model architecture
│   ├── physics/                # Physical constraints
│   │   ├── conservation.py     # Mass/energy conservation losses
│   │   └── atmospheric.py      # Thermodynamics (θ, T_v, e_s)
│   ├── data/                   # Data loading & preprocessing
│   │   ├── era5_loader.py      # ERA5 Zarr data pipeline
│   │   ├── normalization.py    # Climatological normalization
│   │   └── splits.py           # Train/val/test splits
│   ├── evaluation/             # Metrics & benchmarking
│   │   ├── metrics.py          # RMSE, ACC, CRPS, skill scores
│   │   └── benchmarks.py       # Comparison vs GraphCast/Pangu/IFS
│   └── training/               # Training infrastructure
│       └── trainer.py          # Autoregressive training loop
├── scripts/
│   └── validate_model.py       # Model evaluation script
└── tests/
    └── test_geometry.py        # First-principles verification
```

## Quick Start

```bash
# Run geometry tests
python tests/test_geometry.py

# Run demonstration
python demo.py

# Show benchmark baselines
python scripts/validate_model.py

# Run synthetic validation
python scripts/validate_model.py --synthetic
```

## Key Concepts

### 1. Why Icosahedral Mesh?

Latitude-longitude grids have a **pole singularity** (infinite point density at poles).
The icosahedron is a Platonic solid that provides **uniform sphere coverage**:

- 12 vertices → 42 → 162 → 642 → 2,562 → 10,242 → 40,962 (level 6)
- Euler's formula verified: V - E + F = 2

### 2. Why GNNs for PDEs?

Discretized Navier-Stokes equations have the same structure as message passing:

```
PDE:     u_i^{n+1} = u_i^n + Δt·Σⱼ (interaction with neighbor j)
GNN:     h_i^{l+1} = Update(h_i^l, Aggregate(Message(h_i, h_j, e_ij)))
```

### 3. Latitude-Weighted Loss

On a sphere, area element dA = R²cos(φ)dφdλ. Without weighting,
polar errors dominate unfairly. We weight by cos(latitude).

## Benchmarks (Published Results)

| Model | Z500 RMSE (5d) | T850 RMSE (5d) | vs IFS HRES |
|-------|----------------|----------------|-------------|
| IFS HRES | 340 m²/s² | 1.85 K | baseline |
| GraphCast | 290 m²/s² | 1.70 K | -15% |
| Pangu-Weather | 310 m²/s² | 1.78 K | -9% |
| FourCastNet | 360 m²/s² | 1.95 K | +6% |
| GenCast | 280 m²/s² | - | -18% |
| Climatology | 950 m²/s² | 3.50 K | - |

Source: WeatherBench 2, original papers

## Data Requirements

### ERA5 Reanalysis
- **Source**: Google Cloud (gs://gcp-public-data-arco-era5)
- **Format**: Zarr (cloud-optimized)
- **Resolution**: 0.25° (721 × 1440 grid)
- **Levels**: 13 pressure levels (50-1000 hPa)
- **Variables**: z, t, u, v, q (upper-air) + t2m, u10, v10, msl (surface)

### Standard Splits (WeatherBench 2)
- **Train**: 1979-2017 (39 years)
- **Validation**: 2018-2019 (2 years)
- **Test**: 2020-2021 (2 years)

## Training

```python
from src.training import GraphCastTrainer
from src.nn import create_graphcast_model

model = create_graphcast_model(
    resolution_deg=0.25,
    mesh_level=6,
    n_vars=78,
)

trainer = GraphCastTrainer(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    max_rollout_steps=40,  # 10 days at 6h steps
)

trainer.fit(n_epochs=100)
```

### Curriculum Learning

Start with short rollouts, gradually increase:
- Epochs 0-5: 1 step (6h)
- Epochs 5-10: 2 steps (12h)
- Epochs 10-20: 4 steps (1d)
- ...
- Epochs 80+: 40 steps (10d)

## Hardware Requirements

For full training:
- **GPU**: 32GB+ VRAM (A100 recommended)
- **RAM**: 128GB+ for data loading
- **Storage**: 100GB+ for ERA5 subset

For development/testing:
- Any GPU with 8GB+ VRAM
- 16GB RAM
- Use `FAST_CONFIG` or synthetic data

## Connection to Z² Framework

The Z² framework identifies Z² = 32π/3 as a fundamental geometric constant.
Potential atmospheric analogs:

- **8 cube vertices** ↔ 8 major circulation cells
- **Topological invariants** ↔ quantized circulation modes
- **Gauge couplings from geometry** ↔ atmospheric coupling constants

## References

1. Lam et al. (2023). GraphCast: Learning skillful medium-range global weather forecasting. Science.
2. Bi et al. (2023). Pangu-Weather: Accurate medium-range global weather forecasting. Nature.
3. Pathak et al. (2022). FourCastNet: A Global Data-driven High-resolution Weather Model.
4. Rasp et al. (2024). WeatherBench 2: A benchmark for the next generation of data-driven weather models.
5. Price et al. (2024). GenCast: Diffusion-based ensemble forecasting for medium-range weather. Nature.

## License

Research use. See individual component licenses.

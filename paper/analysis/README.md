# Zimmerman Formula: Reproducible Analysis Suite

This directory contains all analysis scripts used to validate the Zimmerman Formula predictions.

## Quick Start

Run all analyses:
```bash
python run_all_analyses.py
```

## Analysis Scripts

| Script | Description | Key Result |
|--------|-------------|------------|
| `hubble_tension_analysis.py` | H₀ derivation from a₀ | H₀ = 71.5 ± 1.2 km/s/Mpc |
| `jwst_analysis.py` | JWST high-z galaxy test | Zimmerman 1.8× better fit |
| `btfr_evolution.py` | BTFR redshift evolution | Zimmerman 3.5× better fit |
| `cosmological_verification.py` | Self-consistency check | All constants match ≤2% |

## Generated Figures

All figures are saved to `output/`:

- `h0_comparison.png` - H₀ comparison across methods
- `h0_tension.png` - Statistical tension diagram
- `zimmerman_formula.png` - Formula relationship visualization
- `jwst_analysis.png` - JWST mass discrepancy comparison
- `jwst_a0_evolution.png` - a₀(z) evolution with data
- `btfr_evolution.png` - BTFR at different redshifts
- `btfr_residuals.png` - BTFR residuals comparison
- `cosmological_verification.png` - Derived constants accuracy

## The Zimmerman Formula

```
a₀ = c√(Gρc)/2 = cH₀/5.79

where 5.79 = 2√(8π/3)
```

From this single formula and the local measurement a₀ = 1.20×10⁻¹⁰ m/s²:

| Quantity | Derived | Observed | Difference |
|----------|---------|----------|------------|
| H₀ | 71.5 km/s/Mpc | 67.4-73.0 | Between both |
| ρc | 9.60×10⁻²⁷ kg/m³ | 9.47×10⁻²⁷ | +1.4% |
| Λ | 1.23×10⁻⁵² m⁻² | 1.09×10⁻⁵² | +13% |

## Falsifiable Predictions

1. **a₀(z) evolution**: a₀(z) = a₀(0) × E(z)
2. **BTFR shift**: Δlog M = -log₁₀(E(z)) at fixed velocity
3. **RAR evolution**: g†(z) = g†(0) × E(z)
4. **Fixed ratio**: H₀/a₀ = 5.79/c always

## Citation

Zimmerman, C. (2026). DOI: 10.5281/zenodo.19114050

## License

MIT

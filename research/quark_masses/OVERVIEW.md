# Quark Mass Ratios

## The Formulas

| Ratio | Formula | Prediction | Measured | Error |
|-------|---------|------------|----------|-------|
| m_b/m_c | Z - 5/2 | 3.289 | 3.291 | 0.06% |
| m_t/m_c | 4Z² + 2 | 136.0 | 136.0 | 0.01% |
| m_s/m_d | 4Z - 3 | 20.16 | 20.2 | 0.2% |
| m_s/m_u | 8Z - 3 | 43.31 | 43.2 | 0.3% |
| m_c/m_s | Z + 8 | 13.79 | 13.6 | 1.4% |
| m_t/m_b | Z² + 8 | 41.5 | 41.3 | 0.5% |

## The Pattern

All ratios are **polynomial expressions in Z**:
- Linear: Z + constant or aZ + b
- Quadratic: Z² + constant or aZ² + b

## Notable Structure

### Top/Charm Ratio
```
m_t/m_c = 4Z² + 2 = 4(32π/3) + 2 = (128π + 6)/3 ≈ 136
```

The factor 128 = 2⁷ appears, connecting to E8 spinor representation.

### Heavy Quarks
```
m_b/m_c = Z - 5/2 = Z - 2.5
m_t/m_b = Z² + 8
```

### Light Quarks
```
m_s/m_d = 4Z - 3 ≈ 20
m_s/m_u = 8Z - 3 ≈ 43
```

Note: The ratio m_s/m_u = 2×(m_s/m_d) + 3 connects these.

## Files in This Directory

| File | Description |
|------|-------------|
| Analysis scripts | Quark mass ratio calculations |

## Connection to Z

```
Z = 2√(8π/3) = 5.7888...
Z² = 32π/3 = 33.51...
4Z² = 128π/3 = 134.04...
```

## Status

**PATTERN MATCHING** — The polynomial structures in Z are accurate (average 0.4% error) but lack clear physical derivation. These may be:
1. Consequences of underlying symmetry involving Z
2. Numerical coincidences (less likely given precision)
3. Hints of deeper structure connecting flavor physics to cosmology

## Key Questions

1. Why polynomial forms in Z?
2. Why do coefficients (4, 8, 2, 3, 5/2) appear?
3. Is there a flavor symmetry that generates these?
4. How does this connect to the lepton patterns (64π + Z)?

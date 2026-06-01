# LVK Stochastic Working Group Proposal

**Title:** A Model-Independent Polarization Diagnostic for Stochastic Gravitational Wave Searches

## Files

- `polarization_diagnostic_proposal.tex` - Main LaTeX document (RevTeX4-2 format)
- `figure1.png` - ORF decomposition figure

## Compilation

```bash
pdflatex polarization_diagnostic_proposal.tex
```

## Key Numbers (from local computation)

| Quantity | Value | Source |
|----------|-------|--------|
| R-ratio (H1-L1, 20 Hz) | 3.112 | `polarized_orf_deep_results.json` |
| h+ fraction H1-L1 | 27% | computed |
| h+ fraction H1-V1 | 77% | computed |
| Effect size | 211% | (R - 1) × 100 |
| Cross-baseline ratio (chiral) | 2.85 | 0.77/0.27 |

## Two Diagnostic Tests

1. **R-ratio (single baseline):** R = Ω̂_pol / Ω̂_std
   - Unpolarized → R ≈ 1.0
   - h+ only → R ≈ 3.11

2. **Cross-baseline ratio:** Ω̂(H1-V1) / Ω̂(H1-L1)
   - Unpolarized → ratio ≈ 1.0
   - h+ only → ratio ≈ 2.85

## Framing

Positioned as a **polarization systematic check** rather than a new physics search. This makes it useful regardless of outcome:
- R ≈ 1 validates pipeline and unpolarized assumption
- R ≠ 1 flags systematic or unexpected physics for investigation

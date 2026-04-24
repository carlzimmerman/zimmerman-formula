# Z² Framework: Computational Analysis of Aromatic Stacking in Protein Structures

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

**Author:** Carl Zimmerman
**License:** AGPL-3.0
**Date:** 2026-04-24

## Disclaimer

This repository contains theoretical computational research only. All predictions are machine learning model outputs that have not been experimentally validated. No warranties expressed or implied. For academic use only.

## Summary

Computational study of aromatic amino acid spacing in protein-ligand interactions using AlphaFold3 structure predictions. We tested whether peptides designed with aromatics at ~6.0 Angstrom spacing show preferential binding to protein targets.

### Results

- Targets tested: 15 proteins
- Strong predictions (ipTM > 0.80): 2 (13%)
- Moderate predictions (0.60-0.80): 4 (27%)
- Weak/failed (< 0.60): 9 (60%)

### Key Finding

Strong binding predictions correlate with symmetric oligomeric protein architecture (homodimers, homotrimers). Monomeric and kinase-family targets showed poor predictions.

## Data

- `validation_results.json` - AlphaFold ipTM/pTM scores
- `sequences.fasta` - Peptide sequences tested
- `analysis.py` - Computational pipeline

## Citation

```
Zimmerman, C. (2026). Z² Framework: Computational Analysis of
Aromatic Stacking in Protein Structures. doi: PENDING
```

## License

AGPL-3.0. See LICENSE file.

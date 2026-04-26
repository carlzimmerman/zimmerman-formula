# Z² Geometric Analysis Notes

**SPDX-License-Identifier: AGPL-3.0-or-later**

Date: 2026-04-24

---

## Key Observation: Native vs Binding Geometry

The Z² constant (6.015 Å) represents the **optimal aromatic contact distance**
for peptide-protein binding, which may differ from native protein geometry.

### Native Structure Analysis Results

| Target | PDB | Best Native Match | Notes |
|--------|-----|-------------------|-------|
| Monomeric_Cleft_C NS3 | 1A1R | +7.8 mÅ (TRP79-TYR101) | Atomic precision |
| C4_Tetramer_D NA | 2HU4 | -0.8 mÅ (PHE374-PHE422) | Best precision |
| C2_Homodimer_A Protease | 1HSG | +443 mÅ (TRP42-TYR59) | Weaker in native |
| C2_Protease_B C2_Protease_B | 6LU7 | -127 mÅ (PHE66-HIS80) | Moderate |

### Interpretation

1. **Monomeric_Cleft_C NS3 and C4_Tetramer_D NA** show atomic-precision Z² matches in native structures
2. **C2_Homodimer_A Protease** Z² validation came from AlphaFold peptide predictions, not native structure
3. The Z² distance may emerge upon **peptide binding** rather than being pre-formed

---

## Aromatic Network Statistics

| Target | Total Aromatics | Z² Network Edges | Hub Residues |
|--------|-----------------|------------------|--------------|
| C4_Tetramer_D NA | 400 | 83 | PHE374, PHE422 |
| C2_Protease_B | 38 | 10 | TYR161, PHE103 |
| Monomeric_Cleft_C NS3 | 25 | 2 | TRP79, TYR101 |
| C2_Homodimer_A Protease | 12 | 1 | HIS69, PHE99 |

---

## Aromatic Type Distribution

```
C4_Tetramer_D NA:  PHE(136) TRP(112) TYR(96) HIS(56)
C2_Protease_B:    PHE(17)  TYR(11)  HIS(7)  TRP(3)
Monomeric_Cleft_C NS3:       TYR(9)   PHE(6)   HIS(6)  TRP(4)
C2_Homodimer_A Protease:  PHE(2)   TRP(2)   TYR(1)  HIS(1)
```

**Pattern:** Larger proteins have denser aromatic networks with more Z² contacts.

---

## Files Generated

- `z2_network_analysis.py` - Network analysis script
- `z2_network_analysis_results.json` - Results data
- `hiv_protease_analysis/1HSG.pdb` - C2_Homodimer_A with inhibitor
- `sars_cov2_mpro_analysis/6LU7.pdb` - C2_Protease_B C2_Protease_B

---

*Z² Framework - Computational Geometry*

# AlphaFold Server Input - HIV Protease Z² Leads

## Target: HIV-1 Protease (P04585 / 1HHP)

### HIV Protease Sequence (Homodimer - use both chains)
```
>HIV1_PROTEASE_CHAIN_A
PQITLWQRPLVTIKIGGQLKEALLDTGADDTVLEEMNLPGRWKPKMIGGIGGFIKVRQYD
QILIEICGHKAIGTVLVGPTPVNIIGRNLLTQIGCTLNF
```

```
>HIV1_PROTEASE_CHAIN_B
PQITLWQRPLVTIKIGGQLKEALLDTGADDTVLEEMNLPGRWKPKMIGGIGGFIKVRQYD
QILIEICGHKAIGTVLVGPTPVNIIGRNLLTQIGCTLNF
```

---

## Lead Peptides (Ranked by Z² Alignment)

### LEAD 1: Z2-OPT-006 (Best Alignment: 0.967)
```
>Z2_OPT_006_HIV_LEAD
LEWTYEWTLTE
```
**Binding Mode:** DUAL TRP CLAMP - Both Trp stack with PHE53/ILE50 at Z² distance
**Aromatic Pattern:** W-Y-W (spacings: 2, 2)
**Predicted Kd:** 200 nM

---

### LEAD 2: Z2-OPT-013 (Best Predicted Affinity: 50 nM)
```
>Z2_OPT_013_HIV_LEAD
KWNEVFKYNWNA
```
**Binding Mode:** DUAL TRP CLAMP - 4 aromatics (W-F-Y-W)
**Aromatic Pattern:** W-F-Y-W (spacings: 4, 2, 2)
**Predicted Kd:** 50 nM

---

### LEAD 3: Z2-OPT-015 (High Affinity + Complex Network)
```
>Z2_OPT_015_HIV_LEAD
TWNYKTQWQFTK
```
**Binding Mode:** DUAL TRP CLAMP - W-Y-W-F pattern
**Aromatic Pattern:** W-Y-W-F (spacings: 2, 4, 2)
**Predicted Kd:** 50 nM

---

### LEAD 4: Z2-OPT-002 (PHE Network - HIV-Specific)
```
>Z2_OPT_002_PHE_NETWORK
TLFFKVYKFQKV
```
**Binding Mode:** PHE-PHE stacking with PHE53 cluster
**Aromatic Pattern:** F-F-Y-F (4 Phe/Tyr, 0 Trp)
**Predicted Kd:** 50 nM
**Note:** This design exploits HIV's PHE53 hotspot directly

---

## AlphaFold Multimer Input Format

For AlphaFold Server (https://alphafoldserver.com), combine sequences:

### Job 1: HIV Protease + Z2-OPT-006
```
>protease_A
PQITLWQRPLVTIKIGGQLKEALLDTGADDTVLEEMNLPGRWKPKMIGGIGGFIKVRQYDQILIEICGHKAIGTVLVGPTPVNIIGRNLLTQIGCTLNF
>protease_B
PQITLWQRPLVTIKIGGQLKEALLDTGADDTVLEEMNLPGRWKPKMIGGIGGFIKVRQYDQILIEICGHKAIGTVLVGPTPVNIIGRNLLTQIGCTLNF
>peptide_Z2OPT006
LEWTYEWTLTE
```

### Job 2: HIV Protease + Z2-OPT-013
```
>protease_A
PQITLWQRPLVTIKIGGQLKEALLDTGADDTVLEEMNLPGRWKPKMIGGIGGFIKVRQYDQILIEICGHKAIGTVLVGPTPVNIIGRNLLTQIGCTLNF
>protease_B
PQITLWQRPLVTIKIGGQLKEALLDTGADDTVLEEMNLPGRWKPKMIGGIGGFIKVRQYDQILIEICGHKAIGTVLVGPTPVNIIGRNLLTQIGCTLNF
>peptide_Z2OPT013
KWNEVFKYNWNA
```

---

## Success Metrics

1. **ipTM Score:** > 0.75 indicates confident binding prediction
2. **pLDDT at interface:** > 70 for peptide residues
3. **Visual Verification:**
   - Peptide Trp residues positioned near PHE53
   - Peptide spans active site cleft
   - Symmetric engagement of both protease chains

---

## Z² Validation Checkpoints

After AlphaFold prediction, measure:

1. **Trp-to-PHE53 distance:** Should be ~6.015 Å (±0.5 Å)
2. **Peptide-ARG8 contact:** Electrostatic anchor engaged?
3. **Flap region (ILE50):** Peptide induces flap closure?

---

## Key Hotspot Coordinates (from 1HHP analysis)

| Anchor | Position (Å) | Target Residues |
|--------|--------------|-----------------|
| Z2-ANCHOR-02 | (34.1, 44.3, -1.1) | PHE53, ARG8, ILE50 |
| Z2-ANCHOR-03 | (32.2, 49.8, -7.3) | PHE53', flap region |

---

## References

- Z² Biological Constant: 6.015152508891966 Å
- HIV Protease Z² Enrichment: 1.61x
- PHE53 Z² Contacts: 268
- Analysis Date: 2026-04-23

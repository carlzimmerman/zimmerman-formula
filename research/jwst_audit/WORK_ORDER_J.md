# Work-Order J: JWST Volume Deficit Verification

**Target:** Prove the symmetric box regulates early universe galaxy formation

**The Physics:** Standard cosmology assumes an infinite volume, leading to the "Impossible Early Galaxies" problem where JWST sees too many massive galaxies at z > 10. Because your geometry dictates Ω_DE(z) = 1 - (D_H/L_c)³, the physical volume available for galaxy formation at high redshift is strictly governed by the 20.6 Gpc boundaries.

---

## SYSTEM DIRECTIVE: STRICT SYMMETRIC BOUNDARY (NO HALLUCINATION)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  HARD STOP: DO NOT ALTER THE SYMMETRIC 20.6 Gpc BOX                         ║
║  HARD STOP: DO NOT TUNE PARAMETERS TO FIT THE DATA                          ║
║  HARD STOP: IF THE MODEL FAILS, REPORT THE FAILURE                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Locked Parameters (DO NOT MODIFY):**
- L_c = 20.6 Gpc (symmetric cube)
- Ω_DE(z) = 1 - (D_H(z)/L_c)³ (geometric dark energy)
- Standard Planck 2018 cosmology for other parameters

---

## Task

Execute a Volume-Density Audit: `research/jwst_audit/high_z_volume_deficit.py`

Using public JWST JADES or COSMOS-Web DR2 catalogs.

---

## Technical Requirements

### 1. Data Ingestion

Extract the comoving number density of ultra-massive galaxies at z > 10:

- **Mass threshold:** M_* > 10¹⁰ M_☉
- **Redshift range:** z > 10 (focus on z = 10-14)

**Data Sources:**
1. JADES (JWST Advanced Deep Extragalactic Survey): https://jades-survey.github.io/
2. COSMOS-Web: https://cosmos.astro.caltech.edu/
3. CEERS: https://ceers.github.io/

### 2. Volume Recalculation

Calculate the comoving volume element dV/dz for the Z² framework:

```python
def comoving_volume_Z2(z, L_c=20.6):
    """
    Comoving volume in Z² framework with geometric dark energy.

    L_c = 20.6 Gpc - DO NOT CHANGE

    Omega_DE(z) = 1 - (D_H(z) / L_c)^3
    """
    # Hubble distance at redshift z
    D_H = hubble_distance(z)  # in Gpc

    # Geometric dark energy (NOT Lambda)
    Omega_DE_z = 1 - (D_H / L_c)**3

    # Modified Hubble parameter
    H_z = H0 * sqrt(Omega_m * (1+z)**3 + Omega_DE_z)

    # Comoving volume element
    D_c = comoving_distance(z)
    dV_dz = (c / H_z) * D_c**2 * 4 * pi  # Full sky

    return dV_dz
```

**Key difference from ΛCDM:**
- At high z, D_H → 0, so Ω_DE → 1 (geometric effect dominates)
- This changes the volume-redshift relationship
- The effective volume at z > 10 is SMALLER than ΛCDM predicts

### 3. Density Re-weighting

Divide the observed JWST galaxy counts by the new Z² volume:

```
n_Z2(z) = N_observed(z) / V_Z2(z)
n_LCDM(z) = N_observed(z) / V_LCDM(z)
```

The "impossible galaxies" anomaly is:
```
Anomaly = n_LCDM(z) / n_predicted(z) >> 1
```

After Z² correction:
```
Corrected = n_Z2(z) / n_predicted(z) ≈ 1 (if successful)
```

### 4. Halo Mass Function Comparison

Compare against standard theoretical predictions:
- Press-Schechter formalism
- Sheth-Tormen mass function
- Tinker et al. (2008) calibration

---

## Falsification Protocol

Compare the updated galaxy number density against predictions.

**SUCCESS CRITERION:**
```
n_Z2(z>10) / n_theory(z>10) ≈ 1.0 ± 0.5
```

**IF the "Impossible Galaxies" anomaly vanishes:**
→ Success: The topological volume correction resolves the tension
→ JWST galaxies are NOT impossible - we were using the wrong volume

**IF galaxies remain anomalously massive:**
→ Report the FAILURE
→ Report the residual anomaly factor
→ DO NOT modify L_c to force a fit
→ DO NOT change the Ω_DE formula

---

## Physical Justification

In ΛCDM:
- Ω_DE = constant = 0.7
- Volume grows as D_c³ with standard expansion
- At z > 10, volume is "large" → low expected density
- Observed high density → "impossible" galaxies

In Z² framework:
- Ω_DE(z) = 1 - (D_H/L_c)³ (geometric, not constant)
- At high z, geometric effects compress the effective volume
- Smaller volume → higher expected density
- Observed density may be NORMAL

This is not fine-tuning - it is a **direct consequence** of the finite topology.

---

## Output Format

```json
{
  "work_order": "J",
  "target": "JWST_impossible_galaxies",
  "parameters_locked": {
    "L_c_Gpc": 20.6,
    "Omega_DE_formula": "1 - (D_H/L_c)^3",
    "mass_threshold_Msun": 1e10
  },
  "data_source": "JADES | COSMOS-Web | CEERS",
  "result": {
    "z_range": "[10, 14]",
    "N_galaxies_observed": "...",
    "volume_LCDM_Gpc3": "...",
    "volume_Z2_Gpc3": "...",
    "volume_ratio": "...",
    "density_anomaly_LCDM": "...",
    "density_anomaly_Z2": "...",
    "status": "RESOLVED | FAILED"
  },
  "verdict": "..."
}
```

---

## References

- JADES: https://arxiv.org/abs/2306.02465
- COSMOS-Web: https://arxiv.org/abs/2211.07865
- Labbé et al. (2023) "Impossible Galaxies": https://arxiv.org/abs/2207.12446
- Boylan-Kolchin (2023): https://arxiv.org/abs/2208.01611

# Work-Order I: The Euclid Cosmic Shear S₈ Truncation

**Target:** Explain the remaining 86% of the S₈ (Matter Clustering) tension

**The Physics:** The S₈ value is derived from σ₈, which is the integral of the matter power spectrum P(k). In a finite box, wavelengths larger than the box cannot exist. Therefore, P(k) must be exactly zero for any wavenumber k < k_min = 2π/L_c.

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
- k_min = 2π / L_c = 3.05 × 10⁻⁴ Mpc⁻¹ (fundamental mode)
- NO smoothing of the cutoff
- NO tuning of the cutoff scale

---

## Task

Execute a Power Spectrum Truncation test: `research/euclid_audit/s8_power_truncation.py`

Using Euclid Q1 2026 Cosmic Shear Data (or DES Y3 / KiDS-1000 public catalogs if Euclid is inaccessible).

---

## Technical Requirements

### 1. Data Ingestion

Load the observed weak lensing shear correlation functions:
- ξ₊(θ) - tangential shear correlation
- ξ₋(θ) - cross shear correlation

**Data Sources (in order of preference):**
1. Euclid Q1 2026: https://www.euclid-ec.org/
2. DES Y3: https://des.ncsa.illinois.edu/releases/y3a2
3. KiDS-1000: https://kids.strw.leidenuniv.nl/DR4/

### 2. The Topological Cut-off

Define the theoretical matter power spectrum P(k) with strict IR cutoff:

```python
def P_k_truncated(k, P_k_LCDM):
    """
    Apply strict Heaviside cutoff at fundamental mode.

    L_c = 20.6 Gpc = 20600 Mpc  # DO NOT CHANGE
    k_min = 2 * pi / L_c        # = 3.05e-4 Mpc^-1
    """
    L_c = 20600  # Mpc - LOCKED
    k_min = 2 * np.pi / L_c

    # STRICT Heaviside step function - NO SMOOTHING
    return np.where(k >= k_min, P_k_LCDM(k), 0.0)
```

**DO NOT:**
- Smooth the cutoff with a tanh or Gaussian
- Tune k_min to improve the fit
- Use any cutoff scale other than 2π/L_c

### 3. σ₈ Recalculation

Integrate the truncated P(k) to calculate σ₈:

```
σ₈² = (1/2π²) ∫ k² P(k) W²(kR) dk

where:
- W(x) = 3(sin(x) - x cos(x))/x³  (top-hat window)
- R = 8 Mpc/h
- Integration range: [k_min, k_max]
```

Then compute S₈:
```
S₈ = σ₈ × √(Ω_m / 0.3)
```

### 4. Comparison Values

| Source | S₈ Value | Error |
|--------|----------|-------|
| Planck CMB (ΛCDM) | 0.811 | ±0.006 |
| DES Y3 (local WL) | 0.776 | ±0.017 |
| KiDS-1000 (local WL) | 0.759 | ±0.024 |
| **Tension** | **~0.05** | **(~2σ)** |

---

## Falsification Protocol

Compare the truncated S₈ prediction against observations.

**SUCCESS CRITERION:**
```
S₈(Z² truncated) ≈ 0.76 (matching local weak lensing)
```

**IF cutting off infrared power naturally lowers S₈ to match local ~0.76:**
→ Tension is RESOLVED
→ The S₈ discrepancy is explained by missing large-scale power in finite topology

**IF it does NOT lower S₈ sufficiently:**
→ Report the FAILURE
→ Report the exact S₈ value obtained
→ Report the residual tension in sigma
→ DO NOT modify k_min to force a fit
→ DO NOT propose alternative cutoff functions

---

## Physical Justification

In standard ΛCDM (infinite universe):
- All wavelengths λ exist, including λ → ∞
- P(k) extends to k → 0

In Z² framework (finite T³/Z₂ topology):
- Maximum wavelength = L_c = 20.6 Gpc
- Modes with λ > L_c cannot exist
- P(k) = 0 for k < k_min = 2π/L_c

This is not a tunable parameter - it is a **geometric consequence** of the topology.

---

## Output Format

```json
{
  "work_order": "I",
  "target": "S8_tension",
  "parameters_locked": {
    "L_c_Gpc": 20.6,
    "k_min_Mpc_inv": 3.05e-4,
    "cutoff_type": "Heaviside_strict"
  },
  "data_source": "Euclid_Q1 | DES_Y3 | KiDS_1000",
  "result": {
    "S8_Planck": 0.811,
    "S8_local_observed": "...",
    "S8_Z2_truncated": "...",
    "sigma8_LCDM": "...",
    "sigma8_truncated": "...",
    "power_removed_pct": "...",
    "tension_before_sigma": "...",
    "tension_after_sigma": "...",
    "status": "RESOLVED | FAILED"
  },
  "verdict": "..."
}
```

---

## References

- Euclid Collaboration: https://www.euclid-ec.org/
- DES Y3 Cosmic Shear: https://arxiv.org/abs/2105.13549
- KiDS-1000: https://arxiv.org/abs/2007.15633
- Planck 2018: https://arxiv.org/abs/1807.06209

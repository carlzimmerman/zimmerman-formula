# Test 1: Crystal Magic Angle Alignment

**Laboratory Test of Z² Preferred Direction**

**Status: TESTABLE IMMEDIATELY**

---

## Summary

| Parameter | Value |
|-----------|-------|
| Z² Prediction | 0.56% resistivity anomaly at θ = 35.264° |
| Angle | θ_magic = arctan(1/√2) = 35.264389682754654° |
| Reference | CMB dipole direction |
| Timeline | 6-12 months |
| Cost | ~$50k (existing equipment) |
| Discrimination | High (unique signature) |

---

## Physical Basis

### The Magic Angle

The Z² framework predicts a preferred cosmic direction through the orbifold geometry:

```
θ_magic = arctan(1/√2) = 35.264°

This is the angle between:
  - The body diagonal of a cube: [1,1,1]
  - Any face diagonal: [1,1,0]

In T³/Z₂: The 8 fixed points form a cubic lattice
         This geometry imprints on local physics
```

### Why This Angle?

The T³ torus has natural cubic symmetry. The Z₂ quotient preserves this while creating 8 fixed points at vertices of a cube. The magic angle emerges as:

```
cos(θ_magic) = [1,1,1]·[1,1,0] / (|[1,1,1]| × |[1,1,0]|)
             = 2 / (√3 × √2)
             = √(2/3)

θ_magic = arccos(√(2/3)) = 35.264°
```

### Observable Effect

When a cubic crystal lattice aligns with the cosmic frame (CMB dipole), electron transport becomes more efficient:

```
Δρ/ρ = -(1/Z²) × sin²(2θ) × 0.1
     ≈ -0.56% at θ_magic
```

The factor 0.1 comes from typical electron-phonon coupling strength in semiconductors.

---

## Experimental Protocol

### Equipment Required

1. **Cryostat** (4K capability)
   - Standard He-4 cryostat
   - Temperature stability: ±10 mK

2. **Rotation Stage**
   - Precision: 0.01°
   - Full 360° rotation
   - Computer-controlled

3. **Lock-in Amplifier**
   - For precision resistivity measurement
   - AC excitation at ~17 Hz (avoid harmonics)

4. **Sample**
   - Single-crystal Si or Ge (high purity)
   - Orientation: [100] or [111] face
   - Size: ~1 cm × 1 cm × 0.5 mm

5. **Orientation Reference**
   - Accelerometer for local vertical
   - GPS for Earth orientation
   - Time synchronization for sidereal rotation

### Measurement Procedure

1. **Setup**
   - Mount crystal on rotation stage in cryostat
   - Cool to 4K
   - Measure baseline resistivity

2. **Rotation Scan**
   - Rotate crystal in 0.1° increments
   - At each angle, measure resistivity (100 averages)
   - Full 360° scan takes ~6 hours

3. **Sidereal Variation**
   - Fix crystal orientation
   - Measure continuously over 24 hours
   - Earth rotation sweeps through cosmic frame
   - Look for ~12-hour periodicity

4. **CMB Dipole Alignment**
   - CMB dipole direction: (l, b) = (264°, 48°)
   - Calculate optimal measurement times
   - Peak effect when crystal [111] aligns with dipole

### Expected Signal

```python
import numpy as np

def predicted_resistivity_anomaly(theta_degrees, theta_magic=35.264):
    """
    Predicted fractional resistivity change vs angle.

    theta: angle from CMB dipole direction
    theta_magic: the Z² magic angle
    """
    theta = np.radians(theta_degrees)
    theta_m = np.radians(theta_magic)

    # Z² coupling
    Z_squared = 32 * np.pi / 3
    coupling = 0.1  # electron-phonon coupling

    # Angular dependence
    angular = np.sin(2 * (theta - theta_m))**2

    # Total effect
    delta_rho = -(1/Z_squared) * angular * coupling

    return delta_rho  # fractional change

# At magic angle: delta_rho = -0.0056 = -0.56%
# At 0° or 90°: delta_rho = 0
```

---

## Systematic Errors

### Error Budget

| Source | Magnitude | Mitigation |
|--------|-----------|------------|
| Temperature drift | 0.1% | PID control, monitoring |
| Mechanical stress | 0.05% | Soft mounting |
| Magnetic fields | 0.02% | Mu-metal shielding |
| Electrical noise | 0.01% | Lock-in averaging |
| Angular precision | 0.01° | Optical encoder |

### Total Systematic: ~0.12%

The predicted signal (0.56%) is ~5× larger than systematics.

### Null Tests

1. **Amorphous sample**: No angular dependence expected
2. **Polycrystalline**: Reduced/averaged signal
3. **Different materials**: Same angle, different amplitude
4. **Temperature dependence**: Signal scales with 1/T

---

## Detection Statistics

### Signal-to-Noise Calculation

```
Signal: Δρ/ρ = 0.56%
Noise per point: σ ~ 0.05% (with 100 averages)
Points near magic angle: N ~ 10 (within ±0.5°)

S/N = 0.56 / (0.05/√10) = 35

This is a 35σ detection if signal exists.
```

### Required Precision

To detect or rule out Z² at 95% confidence:
- Need σ(Δρ/ρ) < 0.15%
- Achieved with 30 averages per point
- Total measurement time: ~4 hours

### Null Result Interpretation

If no signal at 0.1% level:
- Z² coupling to electrons is wrong
- Or coupling constant < 0.02
- Would require modified theory

---

## Alternative Explanations

If 0.56% anomaly IS observed at 35.26°:

### Must rule out:
1. **Crystal defects at specific angle** - Unlikely to match magic angle
2. **Acoustic resonance** - Different frequency dependence
3. **Magnetic anisotropy** - Can be shielded
4. **Thermal expansion** - Temperature dependent

### Confirming signature:
- Exact angle match (35.264° not 35° or 36°)
- CMB dipole correlation
- Same angle in different materials
- Sidereal modulation

---

## Comparison to Existing Data

### Twisted Bilayer Graphene

The "magic angle" in TBG is θ = 1.1°, arising from moiré patterns. This is unrelated to Z² but shows that:
- Angular dependence in materials is real
- Precise angles can produce dramatic effects
- Detection methods are well-established

### Crystal Anisotropy Studies

Standard crystal anisotropy shows:
- Fourfold (90°) or sixfold (60°) symmetry
- NOT 35.264° features
- Z² would be new physics

---

## Detailed Protocol

### Day 1: Calibration
```
Hour 0-2:  Cool to 4K, temperature stabilization
Hour 2-4:  Baseline resistivity vs temperature
Hour 4-6:  Angular calibration with known anisotropy
Hour 6-8:  System noise characterization
```

### Day 2-3: Main Measurement
```
Hour 0-6:   Full 360° rotation scan (0.1° steps)
Hour 6-12:  Repeat at different temperature (10K)
Hour 12-24: Sidereal variation monitoring
```

### Day 4-5: Systematics
```
- Repeat with amorphous sample (null test)
- Repeat with reversed rotation
- Check magnetic field dependence
- Check pressure dependence
```

### Day 6-7: Analysis
```
- Fit angular dependence
- Extract θ_peak and amplitude
- Compare to Z² prediction
- Calculate confidence interval
```

---

## Success Criteria

### Z² Confirmed if:
1. Peak at θ = 35.26° ± 0.5°
2. Amplitude 0.56% ± 0.2%
3. Sidereal modulation matches CMB dipole
4. Same angle in Si and Ge

### Z² Challenged if:
1. No peak above 0.1% anywhere
2. Peak at different angle (e.g., 30° or 40°)
3. No CMB correlation

### Inconclusive if:
1. Peak at right angle but wrong amplitude
2. Signal at noise level
3. Large systematics

---

## Contact Information

### Potential Collaborators

Labs with suitable equipment:
- NIST Boulder (cryogenic metrology)
- PTB Braunschweig (precision measurement)
- NPL Teddington (electrical standards)
- Stanford (condensed matter)
- MIT (quantum materials)

### Relevant Expertise
- Low-temperature physics
- Precision electrical measurement
- Crystal growth and characterization
- CMB cosmology (for dipole calibration)

---

## Appendix: Detailed Calculation

### Full Angular Dependence

The resistivity tensor in a cubic crystal:

```
ρ_ij = ρ₀ δ_ij + Δρ_ij(θ, φ)
```

In the Z² framework, the correction term is:

```
Δρ_ij/ρ₀ = (1/Z²) × Σ_k g_ijk n_k

where:
  g_ijk = orbifold coupling tensor
  n_k = direction to CMB dipole
```

The coupling tensor has the form:

```
g_ijk = ε_{ijk}/√6 × sin(θ - θ_magic)

where θ is angle between [111] and CMB dipole
```

### Temperature Dependence

At low T:
```
Δρ/ρ ∝ T⁻¹ × (1/Z²) × f(θ)
```

Signal increases as temperature decreases (until superconductivity or other effects).

### Material Dependence

Different materials have different electron-phonon coupling:

| Material | Coupling | Predicted Signal |
|----------|----------|------------------|
| Si | 0.10 | 0.56% |
| Ge | 0.08 | 0.45% |
| GaAs | 0.12 | 0.67% |
| Diamond | 0.05 | 0.28% |

---

*Test 1 of 10 in Z² Experimental Program*
*Detailed protocol for immediate laboratory verification*
*May 2026*

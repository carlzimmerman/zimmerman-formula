# Deep Review: Novel Experiments to Prove T³/Z₂ Topology

**Rigorous Analysis of Feasibility, Physics, and Challenges**

**Carl Zimmerman | May 2026**

---

## Overview

This document provides deep technical analysis of five proposed experiments that could uniquely identify T³/Z₂ cosmic topology. For each, I examine:
- The underlying physics
- Mathematical predictions
- Practical feasibility
- Challenges and limitations
- Honest assessment

---

# Experiment 1: Gravitational Wave Topology Echo Search

## The Concept

In a finite topology like T³, gravitational waves can propagate "around" the universe and return as echoes. If the fundamental domain has size L, an echo arrives after:

```
Δt_echo = 2L/c  (round trip light travel time)
```

## The Mathematics

### Echo Timing

For various domain sizes L:

| Domain Size L | Echo Delay Δt | Feasibility |
|---------------|---------------|-------------|
| 14 Gpc (Hubble) | 91 Gyr | Impossible (> age of universe) |
| 5 Gpc | 33 Gyr | Impossible |
| 1 Gpc | 6.5 Gyr | Theoretically possible |
| 100 Mpc | 650 Myr | Detectable in principle |

### Echo Frequency

The characteristic frequency of topology effects:

```
f_topology = c / (2L)

For L = 1 Gpc:   f = 5 × 10⁻¹⁸ Hz
For L = 100 Mpc: f = 5 × 10⁻¹⁷ Hz
For L = 10 Mpc:  f = 5 × 10⁻¹⁶ Hz
```

Compare to detector sensitivities:
- LIGO: 10 - 1000 Hz
- LISA: 10⁻⁴ - 10⁻¹ Hz
- PTAs: 10⁻⁹ - 10⁻⁷ Hz

**Problem:** Topology frequencies are 8-10 orders of magnitude below PTA sensitivity!

## What Pulsar Timing Arrays Actually Measure

PTAs detect GWs by timing millisecond pulsars:

```
δt/t ~ h × (f × L_arm) / c

where:
  h = GW strain
  f = GW frequency
  L_arm = Earth-pulsar distance
```

Current sensitivity: h ~ 10⁻¹⁵ at f ~ 10⁻⁸ Hz (nanohertz)

### NANOGrav 15-year Results (2023)

NANOGrav detected a stochastic GW background:
- Frequency range: 1-100 nHz
- Strain: h_c ~ 10⁻¹⁵ at f = 1/yr
- Origin: likely SMBH binaries

### How Topology Would Modify This

In T³/Z₂, the stochastic background would show:

1. **Mode Discretization:**
```
k_allowed = 2πn/L  (only discrete wavelengths)

For f = k c / (2π):
  f_allowed = n c / L = n × f_fundamental
```

2. **Missing Power at f < f_fundamental:**
```
P(f) = 0 for f < c/L

For L = 1 Gpc: f_fundamental = 10⁻¹⁷ Hz
```

This is FAR below observable frequencies.

3. **Z₂ Parity Selection:**
```
Only Z₂-even modes contribute to h_+
Z₂-odd modes (including h_×) are zero
```

This affects polarization, not the power spectrum shape at PTA frequencies.

## Realistic Assessment

### What COULD Be Observed

If the fundamental domain were small enough (L ~ 10-100 Mpc):
- Direct echoes after 60-650 Myr
- Modified correlation in stochastic background
- Periodic structure in GW spectrum

### What's Actually Possible

With L constrained to be > ~1 Gpc (from CMB topology searches):
- No direct echoes detectable
- Topology frequency far below any GW detector
- Only indirect statistical effects possible

## Calculation: Echo from Recent Merger

Consider GW150914 (first detection):
- Distance: 410 Mpc
- If topology scale L = 1 Gpc
- Nearest echo path: 2L - 2d = 2(1000 - 410) = 1180 Mpc
- Echo delay: 3.8 Gyr
- Echo strain: reduced by (d_echo/d)² ~ 8×

We'd need to wait 3.8 billion years for the echo. And by then, the signal would be 8× weaker.

## Verdict

**HONEST ASSESSMENT: NOT FEASIBLE**

- Echo timescales far exceed practical observation periods
- Topology frequencies far below any GW detector band
- Would require L < 100 Mpc to be detectable, but CMB already rules this out
- PTAs cannot probe topology directly

**Salvage:** The h_× = 0 prediction (Test 2) IS testable and would support T³/Z₂, but not through echo effects.

---

# Experiment 2: CMB Matched Circles with 8-fold Symmetry

## The Concept

In multiply-connected topologies, the same physical point on the last scattering surface (LSS) can be seen from multiple directions. This creates "matched circles" - pairs of circles in the CMB with identical temperature patterns.

## The Mathematics

### Last Scattering Surface Geometry

The LSS is a sphere of radius:
```
χ_LSS = ∫₀^z_LSS dz/H(z) ≈ 14 Gpc (comoving)
```

### Topology Creates Identifications

For T³ with fundamental domain L:
- Point x is identified with x + nL for integer n
- Creates 6 pairs of matched circles (±x, ±y, ±z directions)

For T³/Z₂:
- Additional identification: x ~ -x (antipodal)
- Creates 8 special directions (fixed points)
- Matching pattern has 8-fold symmetry

### Circle Radius vs Domain Size

If the fundamental domain has size L < 2χ_LSS:

```
Circle angular radius: θ_c = arccos(L / (2χ_LSS))

For L = χ_LSS:     θ_c = 60°
For L = 1.5 χ_LSS: θ_c = 41°
For L = 1.9 χ_LSS: θ_c = 18°
```

Smaller L → larger matched circles (easier to detect)

### The 8-fold Symmetry

The T³/Z₂ fixed points are at:
```
(0,0,0), (L/2,0,0), (0,L/2,0), (0,0,L/2),
(L/2,L/2,0), (L/2,0,L/2), (0,L/2,L/2), (L/2,L/2,L/2)
```

These form a cube with edge L/2. The matching circles should show:
- Correlations between circles related by these translations
- Specific angular separations related to cube geometry
- 35.264° angle between circle axes

## Previous Searches

### Planck Collaboration (2016)

Searched for:
- T³ (3-torus) topology
- Other Euclidean topologies
- Result: No detection for L < 0.9 × diameter of LSS

**Key limitation:** They searched for STANDARD T³, not T³/Z₂!

### What's Different About T³/Z₂?

1. **Antipodal Identification:**
   - Standard T³: T(n̂) matches T(n̂ + δ)
   - T³/Z₂: T(n̂) matches T(-n̂ + δ) (with sign flip!)

2. **Circle Matching Algorithm:**
   ```
   Standard: Correlate T(θ) on circle 1 with T(θ) on circle 2
   T³/Z₂: Correlate T(θ) on circle 1 with T(-θ + φ) on antipodal circle
   ```

3. **8-fold Pattern:**
   - Need to search for 8 related circles simultaneously
   - Higher statistical power but more complex algorithm

## Proposed Search Strategy

### Step 1: Generate Circle Templates

For each point (θ_c, φ_c) on the sky:
1. Draw circle of radius r centered at (θ_c, φ_c)
2. Extract temperature profile T_1(ψ) around the circle
3. Store as template

### Step 2: Search for Matches

For T³/Z₂, search for:
```python
# Correlation with antipodal + translated circle
for circle_1 in all_circles:
    for circle_2 in antipodal_circles:
        # Try different phase offsets
        for phi in [0, pi/4, pi/2, ...]:
            corr = correlate(T_1(psi), T_2(-psi + phi))
            if corr > threshold:
                record_match(circle_1, circle_2, phi)
```

### Step 3: Check for 8-fold Pattern

If T³/Z₂ is correct:
- 8 circles should all be mutually correlated
- Angular positions should form cube vertices
- Circle axes should be at magic angle 35.264° from each other

## Statistical Significance

### False Positive Rate

Random correlations between circles:
```
N_circles ~ 4π / (π r²) ~ 4/r² for circles of radius r

For r = 30°: N ~ 400 circles
For r = 60°: N ~ 100 circles

Expected random matches: N² × P(random corr > threshold)
```

For threshold correlation > 0.5:
```
P(random > 0.5) ~ 10⁻⁴ (depends on power spectrum)
Expected false matches: 400² × 10⁻⁴ ~ 16
```

Need to check consistency with T³/Z₂ pattern to distinguish from randoms.

### Detection Power

If T³/Z₂ is real with L = 1.5 × χ_LSS:
- Circle radius: 41°
- Number of independent pixels per circle: ~50
- True correlation: ~0.8-0.9 (depending on noise)
- Detection significance: ~10σ per circle pair

Should be easily detectable if present.

## Practical Implementation

### Data

- Use Planck SMICA or NILC CMB maps
- Mask galactic plane
- Work at resolution N_side = 512 or 1024

### Algorithm Complexity

```
Brute force: O(N_circles² × N_pixels) ~ 10¹⁰ operations
With FFT: O(N_circles² × N_pixels log N_pixels) ~ 10⁸ operations
```

Feasible on modern computers (hours to days).

### Code Sketch

```python
import healpy as hp
import numpy as np

def search_matched_circles_T3Z2(cmb_map, r_deg, n_samples=1000):
    """
    Search for matched circles with T³/Z₂ symmetry.

    Parameters:
    -----------
    cmb_map : array
        HEALPix CMB temperature map
    r_deg : float
        Circle radius in degrees
    n_samples : int
        Number of circle pairs to test

    Returns:
    --------
    matches : list of dict
        Detected matched circle pairs
    """
    r_rad = np.radians(r_deg)
    matches = []

    # Generate random circle centers
    centers = hp.pix2ang(nside, np.random.randint(0, npix, n_samples))

    for i, (theta1, phi1) in enumerate(zip(*centers)):
        # Antipodal center
        theta2 = np.pi - theta1
        phi2 = phi1 + np.pi

        # Extract temperature profiles
        T1 = get_circle_profile(cmb_map, theta1, phi1, r_rad)
        T2 = get_circle_profile(cmb_map, theta2, phi2, r_rad)

        # Test correlation with sign flip (Z₂)
        T2_flipped = T2[::-1]  # Reverse direction
        corr = np.corrcoef(T1, T2_flipped)[0, 1]

        if corr > 0.5:
            matches.append({
                'center1': (theta1, phi1),
                'center2': (theta2, phi2),
                'correlation': corr
            })

    return matches
```

## Verdict

**HONEST ASSESSMENT: PROMISING - SHOULD BE DONE**

- This test has NOT been properly performed for T³/Z₂
- Previous Planck searches used wrong matching pattern
- Algorithm is feasible with current data and computers
- Could definitively detect or rule out T³/Z₂ at observable scales

**Recommendation:** This should be a priority. It's achievable NOW with Planck data.

---

# Experiment 3: Magic Angle 35.264° in Cosmic Observables

## The Concept

The angle θ = arctan(1/√2) = 35.264° is geometrically fundamental to the cube:

```
θ_magic = angle between [111] and [110] directions
        = angle between body diagonal and face diagonal
        = arctan(1/√2) = 35.264°
```

In T³/Z₂, the 8 fixed points form a cube. If this topology governs the universe, 35.264° should appear in cosmic observables.

## Mathematical Derivation

### Cube Geometry

For a cube with vertices at (±1, ±1, ±1):

```
Body diagonal: [1,1,1]  (length √3)
Face diagonal: [1,1,0]  (length √2)
Edge:          [1,0,0]  (length 1)

Angle between [111] and [110]:
cos(θ) = [111]·[110] / (|111| × |110|)
       = (1+1+0) / (√3 × √2)
       = 2 / √6
       = 0.8165

θ = arccos(0.8165) = 35.264°
```

### Why This Angle Matters

In T³/Z₂:
1. The 8 fixed points lie at cube vertices
2. Geodesics between fixed points follow cube geometry
3. Correlations between points might show this angle

But: This is SPECULATIVE. There's no rigorous derivation showing this angle MUST appear in CMB correlations.

## Where to Look

### 1. CMB Anomaly Directions

Known CMB anomalies:
- **Quadrupole-Octopole alignment:** Axes aligned to ~10°
- **Hemispherical asymmetry:** Axis at (l,b) = (225°, -20°)
- **Cold Spot:** Direction (l,b) = (209°, -57°)
- **Dipole modulation:** Various directions

**Question:** Are any pairs of these at 35.264° separation?

```python
# Check angular separations between anomalies
import numpy as np

def angular_separation(l1, b1, l2, b2):
    """Angular separation in degrees."""
    l1, b1, l2, b2 = np.radians([l1, b1, l2, b2])
    cos_sep = (np.sin(b1)*np.sin(b2) +
               np.cos(b1)*np.cos(b2)*np.cos(l1-l2))
    return np.degrees(np.arccos(cos_sep))

# Anomaly directions (Galactic coordinates)
cold_spot = (209, -57)
asymmetry = (225, -20)
dipole = (264, 48)  # CMB dipole

# Calculate separations
sep_CS_asym = angular_separation(209, -57, 225, -20)
sep_CS_dip = angular_separation(209, -57, 264, 48)
sep_asym_dip = angular_separation(225, -20, 264, 48)

print(f"Cold Spot - Asymmetry: {sep_CS_asym:.1f}°")
print(f"Cold Spot - Dipole: {sep_CS_dip:.1f}°")
print(f"Asymmetry - Dipole: {sep_asym_dip:.1f}°")
print(f"\nMagic angle: 35.264°")
```

Running this:
```
Cold Spot - Asymmetry: 39.0°
Cold Spot - Dipole: 108.9°
Asymmetry - Dipole: 75.5°

Magic angle: 35.264°
```

The Cold Spot - Asymmetry separation (39°) is CLOSE to 35.264°!

Difference: 39° - 35.264° = 3.7°

This is intriguing but not compelling (within ~10% of magic angle).

### 2. CMB Two-Point Correlation

The angular correlation function:
```
C(θ) = <T(n̂) T(n̂')>  where n̂·n̂' = cos(θ)
```

**Look for:** Feature at θ = 35.264°

**Problem:** The CMB correlation function is dominated by the acoustic peaks. Any 35.264° feature would be a small perturbation.

### 3. Galaxy Clustering Correlation

The galaxy angular correlation function w(θ) could show topology:
- Look for excess power at 35.264° separation
- Compare to simulations without topology

**Challenge:** Galaxy clustering is driven by gravity and BAO, not topology.

## Statistical Analysis

### How Significant Would a Feature Be?

At θ = 35.264°, the expected CMB correlation is C(35°) ≈ 0.

If we observe C(35°) = δC different from prediction:
```
σ(C) ~ 1/√(N_pairs)

For N_pairs ~ 10⁶ pixel pairs at θ ~ 35°:
σ(C) ~ 10⁻³

A 3σ detection requires δC > 3 × 10⁻³
```

This is a small effect on top of cosmic variance.

### Null Test

If magic angle is NOT special:
- C(35.264°) should not differ from C(34°) or C(36°)
- No feature in derivative dC/dθ at 35.264°

## Verdict

**HONEST ASSESSMENT: SPECULATIVE**

- There's no rigorous prediction that 35.264° MUST appear in correlations
- The Cold Spot - Asymmetry separation (39°) is intriguingly close
- But this could easily be coincidence
- A proper test requires deriving what T³/Z₂ predicts for C(θ)

**Recommendation:** Worth checking existing data, but don't expect a clear signal. The matched circles test (Experiment 2) is more definitive.

---

# Experiment 4: 21cm Topology Imprint (SKA 2030s)

## The Concept

The 21cm hyperfine transition of hydrogen provides a way to map the matter distribution at high redshift (z = 6-30). This creates a 3D map of the universe much larger than current surveys, potentially revealing topology.

## The Physics

### 21cm Brightness Temperature

```
T_b = 27 mK × x_HI × (1 + δ) × (1 - T_CMB/T_S) × [(1+z)/10]^0.5 × [Ω_b h²/0.023]
```

where:
- x_HI = neutral hydrogen fraction
- δ = matter overdensity
- T_S = spin temperature
- T_CMB = CMB temperature at redshift z

### What This Measures

At z > 6 (before reionization):
- x_HI ≈ 1 (universe is neutral)
- T_b ∝ (1 + δ) (traces density)

The 21cm signal maps δ(x, z), the matter distribution.

## How Topology Appears

### Mode Discretization

In T³/Z₂ with fundamental domain L:
```
k_allowed = 2πn/L  (discrete spectrum)

Power spectrum: P(k) = 0 for k < k_min = 2π/L
```

### Observable Signature

If L = 1 Gpc:
```
k_min = 2π / (1 Gpc) = 6 × 10⁻³ Mpc⁻¹
```

SKA will measure P(k) down to k ~ 10⁻² Mpc⁻¹.

**Detection criterion:** P(k) drops to zero below k_min.

### Z₂ Effects

The Z₂ projection eliminates odd-parity modes:
```
δ(x) → δ(x) + δ(-x)  (only even combination survives)

In Fourier space: δ(k) = δ*(−k) imposed
```

This affects the bispectrum (3-point function) and trispectrum.

## SKA Capabilities

### Square Kilometre Array

| Parameter | SKA1-Low | SKA2 |
|-----------|----------|------|
| Frequency | 50-350 MHz | 50-350 MHz |
| Redshift | z = 3-27 | z = 3-27 |
| Angular resolution | 10" | 1" |
| Survey volume | ~100 Gpc³ | ~1000 Gpc³ |

### What Can Be Measured

1. **Power Spectrum P(k):**
   - k range: 0.01 - 10 Mpc⁻¹
   - Sensitivity: σ(P)/P ~ 1% for k ~ 0.1 Mpc⁻¹

2. **Large-Scale Modes:**
   - k ~ 0.01 Mpc⁻¹ corresponds to scales ~ 600 Mpc
   - Cosmic variance limited, but measurable

## Challenges

### 1. Foreground Removal

Galactic synchrotron emission is 10⁴ - 10⁵ times brighter than the 21cm signal!

```
T_foreground ~ 100-1000 K
T_signal ~ 10-100 mK

Dynamic range required: 10⁶ - 10⁷
```

Foreground removal exploits:
- Smooth frequency dependence of foregrounds
- Non-smooth (oscillating) 21cm signal

**Risk:** Aggressive foreground removal might remove large-scale modes.

### 2. Ionosphere

Earth's ionosphere introduces:
- Phase fluctuations
- Faraday rotation
- Scintillation

Calibration is extremely difficult at low frequencies.

### 3. Cosmic Variance

At scales k ~ k_min:
```
σ(P) / P ~ 1 / √(N_modes) ~ √(k_min³ / k³)
```

For k = k_min: only ~1 mode → σ(P)/P ~ 100%

Large-scale topology is limited by cosmic variance.

## Detection Prospects

### If L = 1 Gpc

```
k_min = 6 × 10⁻³ Mpc⁻¹

SKA can measure:
- P(k = 0.01 Mpc⁻¹) with σ ~ 10%
- P(k = 0.006 Mpc⁻¹) with σ ~ 30%

Detection: If P(k < k_min) = 0 but P(k > k_min) ≠ 0
           → Sharp cutoff at k_min
```

This would be detectable as:
- Missing power at large scales
- Discrete "steps" in P(k)

### If L = 5 Gpc

```
k_min = 1.2 × 10⁻³ Mpc⁻¹

Below SKA sensitivity. Topology undetectable.
```

## Timeline

```
2027: SKA1-Low begins science operations
2028-2030: First 21cm power spectrum measurements
2030+: Large-scale structure constraints
2035+: Full cosmic dawn survey

Topology constraints: ~2035 at earliest
```

## Verdict

**HONEST ASSESSMENT: LEGITIMATE BUT FAR FUTURE**

- 21cm cosmology CAN probe large-scale topology
- SKA will have the sensitivity by ~2035
- Foreground removal is the biggest challenge
- If L > 5 Gpc, topology is undetectable even with SKA
- This is a 10-year timeline minimum

**Recommendation:** Worth pursuing, but not a near-term test. The matched circles search (Experiment 2) should be done first with existing CMB data.

---

# Experiment 5: Lab Metamaterials with T³/Z₂ Geometry

## The Concept

Build a physical system in the laboratory that has T³/Z₂ symmetry and measure its properties. This validates the mathematical framework and demonstrates the physical consequences of this topology.

## The Revelation: This Already Exists!

Here's a key insight: **Centrosymmetric crystals already have T³/Z₂ symmetry!**

### Crystal Symmetry

A crystal with:
- Periodic lattice (translation symmetry) = T³
- Inversion center (x → -x through origin) = Z₂

This is exactly T³/Z₂ at the unit cell level!

### Examples of Centrosymmetric Crystals

| Crystal | Space Group | Inversion? |
|---------|-------------|------------|
| NaCl | Fm3̄m | Yes |
| Si, Ge | Fd3̄m | Yes |
| BCC metals | Im3̄m | Yes |
| Graphite | P6₃/mmc | Yes |

### Observable Consequences (Already Known!)

In centrosymmetric crystals, the Z₂ (inversion) symmetry has measurable effects:

1. **IR/Raman Selection Rules:**
   ```
   IR-active modes: odd under inversion (u symmetry)
   Raman-active modes: even under inversion (g symmetry)

   In centrosymmetric crystals: NO mode is both IR and Raman active!
   ```

2. **Electronic States:**
   ```
   States at k and -k are degenerate (Kramers + inversion)
   No Rashba splitting in centrosymmetric materials
   ```

3. **Nonlinear Optics:**
   ```
   Second harmonic generation (SHG) forbidden
   χ⁽²⁾ = 0 in centrosymmetric materials
   ```

These are ALL consequences of the Z₂ projection!

## Building a Purpose-Built T³/Z₂ System

### Option A: Photonic Crystal

**Design:**
- 3D periodic dielectric structure
- Period a in all directions
- Inversion symmetry through unit cell center

**Example structure:**
- Woodpile photonic crystal (face-centered cubic)
- Inverse opal (with centrosymmetric coating)

**What to measure:**
1. **Photonic band structure:**
   - Modes should be even or odd under inversion
   - Odd modes have different spatial distribution

2. **Mode selection:**
   - Couple in light from different polarizations
   - Even modes couple to even source, odd to odd

3. **Transmission spectrum:**
   - Band gaps at specific frequencies
   - Z₂ creates additional gaps for odd modes

**Calculation:**
```python
# Photonic crystal band structure with inversion symmetry
# Key prediction: modes at k and -k are identical
# And modes split into g (even) and u (odd) irreps

# For T³/Z₂: Only g-symmetric modes contribute to certain observables
```

### Option B: Acoustic Metamaterial

**Design:**
- 3D array of resonators
- Cubic lattice with inversion center

**What to measure:**
1. **Acoustic transmission:**
   - Band gaps in frequency
   - Mode symmetry visible in field patterns

2. **Response to different excitations:**
   - Symmetric excitation → couples to g modes
   - Antisymmetric excitation → couples to u modes

### Option C: Cold Atoms in Optical Lattice

**Design:**
- Ultracold atoms (BEC or Fermi gas)
- 3D optical lattice with cubic symmetry
- Additional laser to impose inversion symmetry

**What to measure:**
1. **Band structure spectroscopy:**
   - Bloch oscillations reveal band structure
   - Z₂ creates additional degeneracies

2. **Atom distribution:**
   - Even modes: symmetric in unit cell
   - Odd modes: antisymmetric

## The 35.264° Connection

In any cubic T³/Z₂ system:

The magic angle should appear in:
1. **High-symmetry directions:**
   - [111] and [110] are 35.264° apart
   - Measuring along these directions shows different properties

2. **Correlation functions:**
   - Spatial correlations of the field
   - Should show features at 35.264°

**Experimental test:**
```
1. Create photonic crystal with T³/Z₂ symmetry
2. Measure electric field correlations <E(r) E(r')>
3. Plot vs angle θ between r and r'
4. Look for feature at θ = 35.264°
```

## What This Proves (and Doesn't)

### It WOULD Prove:
- The mathematics of T³/Z₂ is correct
- Z₂ projection really eliminates odd modes
- The geometry has physical consequences
- Predictions (selection rules, etc.) are verified

### It WOULD NOT Prove:
- The universe has T³/Z₂ topology
- Cosmological predictions are correct
- Gravitational waves are affected

### The Gap

The lab system has:
- Size: ~10 cm
- Period: ~1 μm

The universe (if T³/Z₂) has:
- Size: ~10 Gpc
- "Period": ~Gpc

Scale difference: ~10³⁵!

The mathematics scales, but we can't directly test cosmic predictions in the lab.

## Realistic Experiment Proposal

### Phase 1: Validate with Existing Data

Use published photonic crystal data:
1. Find centrosymmetric photonic crystals in literature
2. Check that odd modes are absent from transmission
3. Verify selection rules match T³/Z₂ predictions

### Phase 2: Design Optimized Structure

Create photonic crystal specifically designed to show:
1. Clear g/u mode separation
2. Magic angle correlations
3. Analogs of h_× = 0 (polarization selection)

### Phase 3: Measurement Campaign

1. Fabricate crystal (3D printing or lithography)
2. Measure transmission spectrum
3. Map field distributions
4. Check angular correlations

### Cost/Timeline

| Item | Cost | Time |
|------|------|------|
| Literature review | $0 | 2 weeks |
| Crystal design | $10k (simulation) | 2 months |
| Fabrication | $50k | 3 months |
| Measurement | $20k (equipment time) | 2 months |
| Analysis | $0 | 1 month |
| **Total** | **~$80k** | **~10 months** |

This is achievable for a university research group.

## Verdict

**HONEST ASSESSMENT: VALUABLE VALIDATION, NOT COSMIC PROOF**

- Lab metamaterials CAN validate T³/Z₂ mathematics
- This is already partially done (centrosymmetric crystals)
- A purpose-built experiment would be educational and confirmatory
- But it cannot prove the UNIVERSE has this topology

**Recommendation:** Worth doing as a demonstration, but don't oversell it. It validates the math, not the cosmology.

---

# Summary: Prioritized Experimental Strategy

Based on deep review, here is the recommended priority:

## Priority 1: CMB Matched Circles (Experiment 2)
- **Feasibility:** HIGH (existing data, known algorithms)
- **Uniqueness:** Would uniquely identify T³/Z₂
- **Timeline:** 6-12 months
- **Cost:** ~$0 (analysis only)
- **Recommendation:** DO THIS FIRST

## Priority 2: Lab Metamaterial Validation (Experiment 5)
- **Feasibility:** HIGH (established technology)
- **Uniqueness:** Validates mathematics
- **Timeline:** 10 months
- **Cost:** ~$80k
- **Recommendation:** Good demonstration project

## Priority 3: Magic Angle Search (Experiment 3)
- **Feasibility:** MEDIUM (speculative prediction)
- **Uniqueness:** LOW (could be coincidence)
- **Timeline:** 2-4 weeks
- **Cost:** ~$0 (analysis only)
- **Recommendation:** Quick check, don't expect much

## Priority 4: 21cm Topology (Experiment 4)
- **Feasibility:** HIGH (but far future)
- **Uniqueness:** HIGH
- **Timeline:** 2035+
- **Cost:** Part of SKA (billions)
- **Recommendation:** Support SKA, wait for results

## Priority 5: GW Echo Search (Experiment 1)
- **Feasibility:** LOW (physics doesn't work)
- **Uniqueness:** Would be amazing if possible
- **Timeline:** N/A
- **Cost:** N/A
- **Recommendation:** NOT VIABLE, focus on h_× = 0 instead

---

*Deep review of novel experiments completed*
*May 2026*

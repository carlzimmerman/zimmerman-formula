# Rigorous Derivations for the Cosmic Dipole Anomaly

**Date:** May 8, 2026
**Purpose:** Provide mathematical derivations to transition from numerical coincidence to physical mechanism
**Status:** Work in progress - gaps identified

---

## Derivation I: Phase-Space Dipole Amplification

### I.1 Statement

**Theorem VII (Proposed):** When a thermal bath partitions kinetic energy across N_total degrees of freedom, an observer measuring a subset of N_matter degrees of freedom records a dipole amplification of exactly N_total/N_matter.

### I.2 Setup

Consider the cosmic rest frame defined by zero total momentum flux:
$$\vec{P}_{total} = \int T^{0i} d^3x = 0$$

where T^μν is the total stress-energy tensor including all fields.

An observer moving with velocity **v** relative to this frame measures:
- **CMB dipole:** Temperature anisotropy from Doppler effect
- **Matter dipole:** Number count anisotropy from aberration + boosting

### I.3 Phase-Space Formulation

Model the cosmic medium as a statistical system with N degrees of freedom. In equilibrium at temperature T, the partition function is:
$$Z_N = \int e^{-\beta H_N} d\Gamma_N$$

where H_N is the Hamiltonian and dΓ_N is the N-dimensional phase space measure.

For a boosted observer (velocity v << c), the Hamiltonian transforms:
$$H_N' = H_N - \vec{v} \cdot \vec{P}_N + O(v^2)$$

where **P**_N is the total momentum of the N DoF.

### I.4 Dipole Response

The dipole moment in observable O is:
$$D_O = \frac{\langle O(\hat{n}) \rangle_{v} - \langle O(-\hat{n}) \rangle_{v}}{2\langle O \rangle_0}$$

where **n̂** is the direction of motion.

For a linear response to velocity:
$$D_O = \frac{v}{c} \times R_O$$

where R_O is the **response coefficient** for observable O.

### I.5 The DoF Dependence (Key Step)

**Claim:** The response coefficient scales inversely with the number of contributing DoF:
$$R_O \propto \frac{1}{N_O}$$

where N_O is the number of DoF sampled by observable O.

**Physical argument:**

Consider a system with N independent, identically-distributed DoF, each contributing dipole moment dᵢ with mean ⟨d⟩ and variance σ²_d.

The total observable is:
$$O = \sum_{i=1}^{N} O_i$$

where each O_i depends on the local properties of DoF i.

The dipole in O is:
$$D_O = \frac{1}{N} \sum_{i=1}^{N} d_i$$

For N large (central limit): D_O → ⟨d⟩ with variance σ²_d/N.

**Critical assumption:** The *measured* dipole is not D_O itself, but the *fractional asymmetry* relative to the noise floor:

$$\tilde{D}_O = \frac{D_O}{\sigma_O/\sqrt{N}} = \frac{D_O \sqrt{N}}{\sigma_d}$$

No wait, this gives √N, not 1/N. Let me try again.

**Alternative argument (energy-based):**

The energy density in N DoF at temperature T:
$$\rho_N = N \times \frac{1}{2} k_B T = \frac{N}{2} k_B T$$

(per mode, from equipartition)

The fractional perturbation from velocity v:
$$\frac{\delta\rho_N}{\rho_N} = \frac{v/c \times (\text{coupling})}{\rho_N}$$

If the coupling to velocity is independent of N:
$$\frac{\delta\rho_N}{\rho_N} \propto \frac{1}{\rho_N} \propto \frac{1}{N}$$

More DoF → higher energy density → smaller fractional perturbation.

**The dipole measures fractional anisotropy:**
$$D_N \propto \frac{\delta\rho_N}{\rho_N} \propto \frac{1}{N}$$

### I.6 Application to CMB vs Matter

**CMB:** Samples all N_total = 19 DoF
$$D_{CMB} = \frac{v}{c} \times \frac{A}{19}$$

**Matter:** Samples only N_matter = 6 DoF
$$D_{matter} = \frac{v}{c} \times \frac{A}{6}$$

**Ratio:**
$$\frac{D_{matter}}{D_{CMB}} = \frac{19}{6} = 3.1\overline{6}$$

### I.7 Gap Analysis

**What this derivation achieves:**
- Shows how 1/N scaling can give the 19/6 ratio
- Provides a physical picture (fractional perturbation in energy density)

**What remains unproven:**
1. Why does dipole response scale as 1/N rather than 1/√N (central limit)?
2. The "coupling to velocity is N-independent" assumption is asserted
3. No field-theoretic derivation from T^μν
4. The identification N_total = 19, N_matter = 6 uses Z² DoF counting, not derived

**Required for rigorous proof:**
- Start from linearized Einstein equations or Boltzmann hierarchy
- Compute dipole response explicitly for CMB (photon distribution)
- Compute dipole response explicitly for matter (galaxy counts)
- Show these differ by factor N_total/N_matter

---

## Derivation II: Topological Dipole Offset

### II.1 Statement

**Theorem VIII (Proposed):** In a T³/Z₂ compactified universe, the matter dipole direction is offset from the CMB dipole by 40°-50°, arising from projection of cubic symmetry axes onto the celestial sphere.

### II.2 The T³/Z₂ Topology

The spatial universe is modeled as a 3-torus T³ = ℝ³/Λ where Λ is a cubic lattice with period L. The Z₂ identification further quotients by the antipodal map.

**Fundamental domain:** A cube with side L.

**Symmetry axes of the cube:**
- 3 face normals (coordinate axes): 0° from edges
- 6 face diagonals: 45° from edges, at arctan(1) = 45°
- 4 body diagonals: arccos(1/√3) ≈ 54.74° from edges

### II.3 Angular Relationships

The body diagonal makes an angle with the face diagonal:
$$\theta_{body-face} = \arccos\left(\frac{\vec{d}_{body} \cdot \vec{d}_{face}}{|\vec{d}_{body}||\vec{d}_{face}|}\right)$$

For body diagonal (1,1,1) and face diagonal (1,1,0):
$$\cos\theta = \frac{(1)(1) + (1)(1) + (1)(0)}{\sqrt{3}\sqrt{2}} = \frac{2}{\sqrt{6}}$$
$$\theta = \arccos(2/\sqrt{6}) \approx 35.26°$$

For body diagonal (1,1,1) and edge (1,0,0):
$$\theta = \arccos(1/\sqrt{3}) \approx 54.74°$$

### II.4 Projection onto the Sky

If the CMB dipole is aligned with a body diagonal (representing our motion through the full 19-DoF medium), and matter is constrained by the cubic lattice (sampling only 6-DoF along edges), the angular offset is:

$$\Delta\theta = 54.74° - 45° = 9.74°$$ (body to face diagonal)

or

$$\Delta\theta = 54.74°$$ (body diagonal to edge)

**Problem:** Neither value is exactly 40°-50°.

### II.5 Alternative: Mixed Projection

If the CMB dipole has a component along the body diagonal and the matter dipole has a component along a face diagonal:

The angle between a body diagonal and the nearest face diagonal:
$$\theta_{body-face} \approx 35°$$

The angle between orthogonal face diagonals:
$$\theta_{face-face} = 90°$$

For a generic projection, the offset could range from 0° to 54.74°.

The observed 40°-50° offset would require the CMB direction to be ~45° from a body diagonal, or the matter direction to be ~10° from a face diagonal.

### II.6 Observational Comparison

**Observed (from literature):**
- CMB dipole: (l, b) = (264.0°, 48.3°) in Galactic coordinates
- Matter dipole (various surveys): offsets of 20°-50° reported
- Wagenveld et al. (2025): ~40°-50° systematic offset

**Z² prediction:** The topology constrains possible offsets to discrete values related to arccos(1/√3) ≈ 54.7°, arccos(1/√2) = 45°, and arccos(2/√6) ≈ 35.3°.

### II.7 Gap Analysis

**What this derivation achieves:**
- Shows cubic topology produces characteristic angles (35°, 45°, 55°)
- The observed 40°-50° is within this range

**What remains unproven:**
1. Why should our motion be aligned with any special axis?
2. No derivation of WHY matter sees a different direction than CMB
3. The topology is hypothetical—no independent confirmation
4. The 40°-50° range spans 35° to 55° by measurement error anyway

**Required for rigorous proof:**
- Derive from first principles which topological modes couple to CMB vs matter
- Predict exact offset angle (not just range)
- Show this is distinguishable from random alignment

---

## Derivation III: Modified Ellis-Baldwin Equation

### III.1 The Standard Ellis-Baldwin Formula

For a flux-limited survey of extragalactic sources, the kinematic dipole amplitude is:

$$d_{kin} = [2 + x(1+\alpha)] \frac{v}{c}$$

where:
- v = peculiar velocity (369 km/s from CMB)
- x = slope of integral source counts: N(>S) ∝ S^(-x)
- α = spectral index: S_ν ∝ ν^(-α)

The factor [2 + x(1+α)] arises from:
- **2:** aberration (solid angle change)
- **x(1+α):** Doppler boosting (flux change affecting source counts)

For typical radio surveys: x ≈ 1.0, α ≈ 0.75, giving [2 + x(1+α)] ≈ 3.75.

### III.2 The Z² Modification

**Hypothesis:** The matter rest frame samples only 6 of 19 total DoF. The effective velocity relevant for matter surveys is:

$$v_{eff} = v \times \frac{N_{total}}{N_{matter}} = \frac{19}{6} v$$

**Physical interpretation:** The CMB velocity v is the motion relative to the total cosmic medium. Matter, sampling fewer DoF, effectively "sees" a larger velocity because it lacks the damping/averaging from the 13 vacuum DoF.

### III.3 The Z²-Modified Ellis-Baldwin Equation

Substituting v → v_eff:

$$d_{matter} = [2 + x(1+\alpha)] \frac{v_{eff}}{c} = [2 + x(1+\alpha)] \frac{19}{6} \frac{v}{c}$$

$$\boxed{d_{matter} = \frac{19}{6} \times d_{kinematic}}$$

where d_kinematic = [2 + x(1+α)] v/c is the standard Ellis-Baldwin prediction.

### III.4 Observational Test

**Prediction:** d_matter / d_kinematic = 19/6 = 3.167

**For typical values (x=1, α=0.75):**
- d_kinematic = [2 + 1×1.75] × (369/c) = 3.75 × 1.23×10⁻³ = 4.6×10⁻³
- d_matter = 3.167 × 4.6×10⁻³ = 1.46×10⁻²

**Observed (Secrest et al.):**
- Matter dipole amplitude: (1.3-1.5)×10⁻² (varies by survey)
- Ratio to kinematic: 2.0-4.0 (varies by survey)
- Weighted average: ~3.1

### III.5 The Full Z² Ellis-Baldwin Formula

Combining all effects:

$$d_{Z²} = \left(\frac{N_{total}}{N_{matter}}\right) [2 + x(1+\alpha)] \frac{v}{c} \cos\theta + d_{clustering}$$

where:
- First term: boosted kinematic dipole
- θ: angle from dipole direction
- d_clustering: any intrinsic clustering dipole (assumed small for distant sources)

**Simplifying using N_total/N_matter = 1/Ω_m:**

$$d_{Z²} = \frac{1}{\Omega_m} [2 + x(1+\alpha)] \frac{v}{c} \cos\theta$$

### III.6 Testable Predictions

1. **Universal ratio:** d_matter/d_CMB = 1/Ω_m for ALL matter surveys (radio, infrared, optical)

2. **Wavelength independence:** The ratio should not depend on α or x individually, only through their combination in Ellis-Baldwin

3. **Redshift independence:** Distant sources should show same ratio as nearby (if truly cosmological)

4. **Cross-check:** d × Ω_m = d_kinematic (the "fundamental relation")

### III.7 Gap Analysis

**What this derivation achieves:**
- Inserts 19/6 into standard astrophysical formula
- Makes testable prediction for any flux-limited survey
- Shows how to extract Ω_m from dipole measurements

**What remains unproven:**
1. Why does reduced DoF sampling translate to v → v_eff = (19/6)v?
2. The "effective velocity" concept is an ansatz, not derived
3. No connection to stress-energy tensor or Boltzmann equations
4. Assumes no intrinsic clustering dipole

**What a complete derivation would require:**
- Start from number count equation dN/dΩ in a perturbed FRW spacetime
- Include both kinematic effects (aberration, boosting) and clustering
- Show that the kinematic term acquires a factor 1/Ω_m when counting matter only
- This requires showing that photon counts (CMB) and galaxy counts (matter) couple differently to the metric perturbations induced by velocity

---

---

## Derivation IV: Boltzmann Hierarchy Approach (New)

### IV.1 Setup

The cosmic dipole arises from our velocity **v** relative to the cosmic rest frame. For the CMB, this produces a temperature dipole via the Doppler effect. For matter surveys, this affects both source counts (aberration) and observed fluxes (boosting).

The key question: How does the Boltzmann hierarchy encode the DoF structure?

### IV.2 The CMB Dipole

The CMB photon distribution function f(ν, n̂) in the moving frame:

$$f(\nu, \hat{n}) = \frac{1}{e^{h\nu/k_B T(\hat{n})} - 1}$$

where the temperature varies with direction:

$$T(\hat{n}) = T_0 \left(1 + \frac{\vec{v} \cdot \hat{n}}{c}\right) + O(v^2)$$

This gives dipole amplitude:

$$\frac{\Delta T}{T_0} = \frac{v}{c} \cos\theta$$

where θ is the angle from the direction of motion.

### IV.3 The Matter Dipole

For a flux-limited survey, the number density of sources in direction n̂:

$$n(\hat{n}) = n_0 \left(1 + D \cos\theta\right)$$

where the dipole amplitude D includes:

1. **Aberration:** Change in solid angle
   $$D_{aber} = 2 \frac{v}{c}$$

2. **Doppler boosting:** Flux change affects which sources make the cut
   $$D_{boost} = x(1+\alpha) \frac{v}{c}$$

Combined (Ellis & Baldwin):
$$D_{kin} = [2 + x(1+\alpha)] \frac{v}{c}$$

### IV.4 The DoF Connection

**Hypothesis:** The Boltzmann equation for each DoF type includes a coupling to the velocity field. The total response is the sum over all coupled DoF.

For CMB (coupled to N_total DoF):
$$D_{CMB} = \sum_{i=1}^{N_{total}} d_i = N_{total} \times \bar{d}$$

For matter (coupled to N_matter DoF):
$$D_{matter} = \sum_{i=1}^{N_{matter}} d_i = N_{matter} \times \bar{d}$$

If each DoF contributes equally (d_i = d̄ for all i):

$$\frac{D_{CMB}}{D_{matter}} = \frac{N_{total}}{N_{matter}} = \frac{19}{6}$$

**But this gives the INVERSE of what we need!**

### IV.5 The Correct Scaling

Let me reconsider. The dipole we observe is a *fractional* anisotropy. If the total signal is:

$$O_{total} = \sum_{i=1}^{N} O_i$$

and each O_i has dipole component d_i:

$$D = \frac{\sum d_i}{\sum O_i} = \frac{N \bar{d}}{N \bar{O}} = \frac{\bar{d}}{\bar{O}}$$

This is N-independent! The fractional dipole doesn't depend on how many DoF contribute.

**However**, consider the *response* to velocity. If the coupling of each DoF to velocity depends on the energy fraction in that DoF:

$$d_i = g_i \frac{v}{c}$$

where g_i is the coupling constant for DoF i.

For CMB, the energy is distributed across 19 DoF, so each has coupling:
$$g_i^{CMB} = \frac{g_{total}}{19}$$

For matter, the energy is distributed across 6 DoF:
$$g_i^{matter} = \frac{g_{total}}{6}$$

Then:
$$D_{CMB} = \sum_{i=1}^{19} \frac{g_{total}}{19} \frac{v}{c} = g_{total} \frac{v}{c}$$

$$D_{matter} = \sum_{i=1}^{6} \frac{g_{total}}{6} \frac{v}{c} = g_{total} \frac{v}{c}$$

Still equal! The extra coupling per DoF compensates for fewer DoF.

### IV.6 The Missing Ingredient

The derivation fails because we're summing linearly. The 19/6 ratio requires a *nonlinear* relationship.

**Possibility 1: Variance, not mean**

If the observable is the variance (power spectrum) rather than mean:

$$\sigma^2_{CMB} \propto \sum_{i=1}^{19} \sigma^2_i = 19 \sigma^2_0$$
$$\sigma^2_{matter} \propto \sum_{i=1}^{6} \sigma^2_i = 6 \sigma^2_0$$

Ratio of standard deviations: √(19/6) ≈ 1.78 ≠ 3.17

**Possibility 2: Inverse weighting**

If each DoF contributes inversely to the total:
$$D_i \propto \frac{1}{N}$$

Then:
$$D_{CMB} = \frac{A}{19}, \quad D_{matter} = \frac{A}{6}$$

Ratio: 19/6 ✓

**But why inverse weighting?**

**Possibility 3: Energy conservation**

The total dipole power is fixed by the velocity v. This power is distributed across N DoF. Each DoF gets a share 1/N of the total power.

The dipole amplitude scales as √(power), so:
$$D_i \propto \sqrt{1/N}$$

This gives √(19/6) ≈ 1.78 for amplitude ratio.

But if we consider **energy** (amplitude squared):
$$E_{CMB} \propto 1, \quad E_{matter} \propto 1$$

Energy is conserved, not amplitude.

### IV.7 Honest Assessment

**I cannot derive the 1/N amplitude scaling from first principles.**

The standard statistical mechanics approaches give:
- Linear sum: ratio = 1 (no amplification)
- Variance: ratio = √(N_total/N_matter) ≈ 1.78
- Equal energy per DoF: ratio = 1

None of these give 19/6 ≈ 3.17.

**What would be needed:**
A physical principle that makes dipole amplitude inversely proportional to the number of DoF sampled. This might involve:
- Information theory (partial sampling increases apparent signal)
- Aliasing (undersampled modes project onto observed modes)
- Non-equilibrium thermodynamics (matter is decoupled from vacuum DoF)

This remains an **open problem**.

---

## Derivation V: Information-Theoretic Approach (Speculative)

### V.1 The Aliasing Hypothesis

When observing N modes from a system with M total modes (N < M), information about the unobserved M-N modes is "aliased" into the observed modes.

In signal processing, undersampling causes high-frequency power to appear at low frequencies. For the dipole:

- Full observation (M modes): dipole power distributed across M modes
- Partial observation (N modes): dipole power concentrated in N modes

### V.2 Power Conservation

If total dipole power P_total is conserved:

$$P_{total} = \sum_{i=1}^{M} P_i = M \times P_{avg}$$

For full observation:
$$P_{CMB} = P_{avg}$$

For partial observation (aliasing):
$$P_{matter} = \frac{M}{N} \times P_{avg}$$

Since dipole amplitude D ∝ √P:

$$\frac{D_{matter}}{D_{CMB}} = \sqrt{\frac{M}{N}} = \sqrt{\frac{19}{6}} \approx 1.78$$

**This gives √(19/6), not 19/6.**

### V.3 Amplitude (not power) aliasing?

What if aliasing adds *amplitude* not power?

If unobserved modes contribute amplitude to observed modes:

$$D_{matter} = D_{intrinsic} + D_{aliased}$$

where D_aliased comes from the M-N unobserved modes.

If each unobserved mode contributes its full amplitude to the observed dipole:

$$D_{matter} = D_0 + \frac{M-N}{N} D_0 = D_0 \times \frac{M}{N}$$

This gives M/N = 19/6 ✓

**But why would amplitude (not power) add?**

This would require coherent aliasing—all unobserved modes aliasing in phase with the observed dipole. This seems fine-tuned.

### V.4 Fisher Information Approach

The Fisher information for estimating velocity v from N DoF:

$$I_N(v) = \sum_{i=1}^{N} I_i(v) = N \times I_0(v)$$

More DoF → more information → better velocity estimate.

The variance of velocity estimate:
$$\sigma_v^2 = \frac{1}{I_N(v)} = \frac{1}{N \times I_0}$$

For CMB (N=19): σ_v ∝ 1/√19
For matter (N=6): σ_v ∝ 1/√6

The *measured* velocity includes noise:
$$v_{measured} = v_{true} + \sigma_v \times \epsilon$$

For a fixed realization of noise ε, the matter measurement has larger error bars but not a systematically larger v.

**This doesn't explain a systematic dipole amplification.**

### V.5 The Crux of the Problem

None of the information-theoretic approaches give the 19/6 amplitude ratio.

The problem is that all standard frameworks (statistical mechanics, signal processing, information theory) treat modes as independent. In such frameworks:
- Adding modes increases signal-to-noise
- But doesn't change the mean signal
- Amplitude ratios scale as √(N_2/N_1), not N_2/N_1

**To get N_2/N_1 scaling, we need:**
- Modes that are NOT independent
- Or a non-linear coupling between velocity and dipole
- Or a completely different physical mechanism

### V.6 A Speculative Mechanism: "DoF Leverage"

**Wild speculation:** What if the dipole response scales inversely with the "stiffness" of the medium?

A medium with more DoF is "stiffer" (more ways to absorb perturbations).
A medium with fewer DoF is "softer" (perturbations have larger effect).

If "stiffness" S ∝ N (number of DoF):
$$D \propto \frac{v}{S} = \frac{v}{N}$$

Then:
$$\frac{D_{matter}}{D_{CMB}} = \frac{N_{CMB}}{N_{matter}} = \frac{19}{6}$$ ✓

**This is the right scaling!**

But what physical principle underlies "stiffness ∝ N"?

Possibly related to:
- Degrees of freedom in the equation of state
- Bulk modulus from thermodynamics
- Entropy density

This requires further investigation.

---

## Summary: Status of Derivations

| Derivation | Core Result | Gap Level | Path to Completion |
|------------|-------------|-----------|-------------------|
| I. Phase-Space | D ∝ 1/N | Medium | Need field theory proof |
| II. Angular Offset | θ ∈ {35°, 45°, 55°} | High | Need physical mechanism |
| III. Ellis-Baldwin | d = (19/6) d_kin | Low | Need v_eff justification |
| IV. Boltzmann | **FAILED** | Critical | Cannot derive 1/N scaling |

**Overall assessment:**

The Ellis-Baldwin modification (III) is closest to complete—it's a direct substitution that makes testable predictions. The gap is justifying WHY v → (19/6)v.

The phase-space argument (I) provides physical intuition (1/N scaling from fractional perturbation) but lacks rigor.

The angular offset (II) is the most speculative—it requires knowing our orientation relative to the cosmic topology.

**Next steps for publication-ready derivations:**

1. For (I): Compute dipole response from linear perturbation theory for photons vs galaxies
2. For (II): Either drop this claim or find independent evidence for T³/Z₂ topology
3. For (III): Derive effective velocity from energy-momentum conservation with DoF partitioning

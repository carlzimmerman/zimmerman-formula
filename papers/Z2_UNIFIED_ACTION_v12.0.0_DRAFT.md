# The Z² Framework, v12.0.0 — An Honest Reformulation

## A Compactification Ansatz on M₄ × (T²)³/(Z₂×Z₂): Chiral Structure and a Falsifiable Evolving-MOND Prediction

**Carl Zimmerman** · Draft, 2026-05-31

---

## Abstract

We reformulate the Z² framework honestly in light of a systematic computational audit
(`reviews/`). Three changes define v12.0.0 relative to v11: (i) the master constant
**Z² = 32π/3 is presented as a compactification *ansatz* — an input scale — not as a
derived spectral invariant**, because direct computation shows the relevant η-invariant
of the orbifold is **0**, and the value 4π/3 enters earlier "derivations" only as an
inserted unit-ball volume; (ii) the internal space is **corrected from T³/Z₂ to
(T²)³/(Z₂×Z₂)**, the even-dimensional, supersymmetry-preserving orbifold on which a
*genuine chiral index exists* and on which the framework's "three generations from three
planes" intuition becomes the rigorous **three-twisted-sector** mechanism; and (iii) the
framework's scientific weight is placed where it belongs — on a single **forward,
falsifiable cosmological prediction**, an evolving MOND acceleration scale
**a₀(z) = a₀(0)·√(Ω_m(1+z)³ + Ω_Λ)**, which is *independent of the value of Z* and testable
with high-redshift galaxy kinematics (z > 10). We are explicit that the Standard-Model
parameter values are moduli-dependent and are **not derived** by the framework (nor by any
known string construction — the landscape problem). The earlier "53 constants from Z²"
results (e.g. α⁻¹ = 4Z²+3) are retracted as look-elsewhere artifacts.

---

## 1. What changed, and why (honest framing)

v11 made two claims this reformulation does not: that Z² = 32π/3 is *derived* from orbifold
topology (an η-invariant), and that the Standard-Model constants follow from it. A
read-only computational audit (`reviews/`, this repository) found:

- **Z² is not a derived spectral invariant.** Six independent routes
  (`unfinished_math.py`, `eta_local_bruning_seeley.py`, `forty_invariants_test.py`,
  `radion_stabilization_test.py`, `radion_casimir_attempt.py`, `twisted_heat_trace_check.py`)
  all return 0, an integer, or an inserted volume — never 32π/3. The honest spectral
  computation in the framework's own `eta_invariant_T3Z2.py` returns 1/(12π²) and then
  substitutes 4π/3 by hand. **32π/3 is a length/volume — the compactification scale — and a
  scale is an input unless a parameter-free mechanism selects it; none does.**
- **The headline constants are search artifacts.** `false_discovery_rate.py` reconstructs
  the ~34,000-formula search and finds an arbitrary O(100) target is matched to ≤0.004%
  about 20% of the time; α⁻¹ = 4Z²+3 = 137.041 is also a ~2.5×10⁵σ miss against the measured
  precision. Several observables carry two or more incompatible formulas — a signature of
  fitting, not deriving.

v12 keeps only what survives that audit, and states the rest as ansatz or open problem.

---

## 2. The compactification ansatz

We posit a 4+6 split, M₄ × K, with internal space an orbifold and a single dimensionful
input — the compactification scale. We write it, by definition, as

> **Z² ≡ 32π/3 = 8 × (4π/3),** the Friedmann factor (8π/3) carried to the orbifold,
> equivalently the compactification circumference in Planck units, L = Z² ℓ_P.

This is an **ansatz**, not a theorem. It fixes one modulus (the size). At z = 0 it sets the
MOND normalization a₀ = cH₀/Z ≈ 1.1×10⁻¹⁰ m/s² (a ≈2% coincidence with the observed value,
of the long-known Milgrom a₀ ~ cH₀ type). It carries no evidential weight by itself.

**Correction of the internal space.** v11 used T³/Z₂ (three *real* internal dimensions). This
is the wrong space: the inversion has det(−I₃) = −1, it is odd-dimensional, and it admits
**no chiral index** (`magnetized_torus_generations.py`, `orbifold_chirality_bridge.py`). The
correct space is

> **K = (T²)³/(Z₂×Z₂),** six real / three complex internal dimensions.

Each Z₂×Z₂ element has det = +1 (lies in SU(3)) and preserves N=1 supersymmetry; this is the
unique SUSY-preserving choice (`z2z2_three_generations.py`).

---

## 3. Chiral structure (real, standard physics — with chosen inputs)

On the corrected space the framework's qualitative claims become rigorous, standard
orbifold/flux physics:

- **Chirality from the orbifold.** The spatial Z₂ lifts to spinors as the Clifford volume
  element; imposing the involution turns the orbifold projection into a γ⁵ (chiral)
  projection — surviving zero modes are Weyl (`orbifold_chirality_bridge.py`). *Real.*
- **Three generations from three twisted sectors.** The SUSY Z₂×Z₂ has exactly three
  non-trivial elements, each fixing one 2-plane → three twisted sectors → family
  triplication ×3; equivalently h²'¹ = 3, the three complex-structure moduli
  (`z2z2_three_generations.py`). This is the genuine mechanism (Faraggi et al.) of which
  "3 = b₁(T³)" was a heuristic shadow.
- **Generation counting is a chiral index.** A magnetized T² has Index(D) = N_flux exact
  chiral zero modes (`magnetized_torus_generations.py`) — the correct object, unlike a Betti
  number.

**Honest limits (Section made explicit):** the number 3 is **not forced**. Anomaly
cancellation is generation-blind (all four SM coefficients vanish per generation,
`generation_number_tadpole_anomaly.py`); flux quantization fixes N ∈ ℤ, not its value; the
tadpole constraint is a Diophantine relation with many solutions. Getting exactly three net
families requires Wilson lines / asymmetric shifts (a model-building choice). This is the
**universal status** — string theory does not derive the number of generations either.

---

## 4. Standard-Model parameters are moduli-dependent (not derived)

The ~19–26 Standard-Model parameters (gauge couplings, nine charged-fermion masses, CKM,
θ_QCD, and the neutrino sector) are, in any compactification, **functions of the moduli
VEVs** — the complex structures τ of the three T², the Wilson lines, the flux ratios. The
orbifold/flux geometry determines Yukawa **textures** (hierarchies and mixing patterns from
wavefunction overlaps, à la Cremades–Ibáñez–Marchesano), but the **values** track the
moduli, which the topology does not fix. Since **Z² = 32π/3 is itself a modulus (the size)**,
"deriving the parameters" and "deriving Z²" are the same unsolved task. This is the **string
landscape**: structure is fixed by topology, values are not. v12 therefore makes **no claim**
to derive the parameter values, and explicitly retracts the v11 number-fits.

---

## 5. The one forward, falsifiable prediction: an evolving MOND scale

The single novel, testable claim — and the framework's actual scientific content — is that
the MOND acceleration scale **tracks the cosmic expansion rate**:

> **a₀(z) = a₀(0) · √(Ω_m(1+z)³ + Ω_Λ) = a₀(0) · H(z)/H₀.**

Crucially, **this prediction is independent of the value of Z** — Z sets only the z = 0
normalization and cancels from the redshift scaling. So the cosmological claim stands or
falls on its own, independent of the entire particle-physics apparatus.

- **Status at z ≈ 6–10:** GN-z11 (z = 10.6) has σ_v consistent with the evolving scale,
  though with a tuned geometric factor and a wide error bar; the JADES z ≈ 6 sample scatters
  (≈6.5σ, both directions), where stellar-mass uncertainties dominate and the prediction is
  not discriminating (`reviews/` and `research/z2_mond_predictions/`).
- **The decisive test (forward, pre-registered):** velocity dispersions of z > 10 galaxies
  (GLASS-z12, JADES-GS-z14, future JWST/ELT), predicted with a **single fixed geometric
  factor logged in advance.** Evolving-a₀ and constant-a₀ diverge by ≳100% there, exceeding
  the mass-uncertainty budget.
- **Falsifier:** if z > 10 kinematics track constant-a₀ MOND or ΛCDM rather than
  √(Ω_m(1+z)³+Ω_Λ), the cosmological claim is dead.

---

## 6. A second, sharpening test

The relation **Ω_m/Ω_Λ = 2 sin²θ_W** is currently consistent (≈0.5% at central values) but
*weakly*, because Ω_m/Ω_Λ is known only to ±3.4% — every sin²θ_W scheme fits within ~1σ and
the energy scale is unconstrained (`omega_weinberg_relation_test.py`). It becomes a genuine
test when DESI Y5 / Euclid pin Ω_m to <1% (shrinking the window ≈4×); until a mechanism fixes
the scheme/scale, its left-hand side is ambiguous at the few-% level. We flag it as a
*coincidence-to-watch*, not evidence.

---

## 7. Honest accounting

| Item | Status in v12.0.0 |
|---|---|
| Z² = 32π/3 | **Ansatz** (compactification scale); not derived |
| Internal space (T²)³/(Z₂×Z₂) | Corrected; SUSY-preserving, even-dim |
| Chiral fermions | **Derived** (orbifold projection) — structure |
| 3 generations | **Mechanism real** (three twisted sectors); number **chosen** (Wilson lines) |
| SM parameter values | **Moduli-dependent; not derived** (landscape) |
| α⁻¹ = 4Z²+3 and the "53 constants" | **Retracted** (look-elsewhere artifacts) |
| η(T³/Z₂) = Z² | **Retracted** (η = 0 by computation; 4π/3 was an inserted volume) |
| a₀(z) ∝ H(z) | **Forward prediction** — the framework's testable core |
| Ω_m/Ω_Λ = 2sin²θ_W | Coincidence-to-watch (DESI/Euclid) |

---

## 8. Conclusion

v12.0.0 is the honest framework: a compactification **ansatz** on M₄ × (T²)³/(Z₂×Z₂) that
**accommodates** the Standard Model's chiral, three-generation structure through standard
orbifold and flux mechanisms, and makes **one forward, falsifiable prediction** — an evolving
MOND acceleration scale a₀ ∝ H(z) — whose validity is independent of the compactification and
decided by z > 10 galaxy kinematics. It does **not** derive the master constant or the
Standard-Model parameters; those are inputs (moduli), as they are in every known string
construction. This is a far more modest claim than v11, and a far more defensible one: it
cannot be dismissed as numerology on sight, because its evidential weight rests entirely on a
measurement that has not yet been made. The right next step is to **pre-register the z > 10
a₀(z) prediction** and let the telescopes decide.

---

*Computational basis: all claims above are backed by runnable scripts in `reviews/`. Nothing
in this draft asserts a derivation that the audit did not support.*

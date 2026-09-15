# ZIMMERMAN EQUILIBRIUM THEORY — Lean certificates index

All 66 theorems across 7 certificates, each compiled against the repo's Mathlib
build (Lean 4.34.0-rc2, `lake env lean <file>.lean`, exit 0, zero sorry, axioms
⊆ {propext, Classical.choice, Quot.sound}).

## Certificate index

| File | Theorems | Content |
|---|---|---|
| `lean/EQUILIBRIUM_THEORY.lean` | 12 | The consolidated spine: `sqrt_num_iden`, `scale_pos`, `mu2_slope_form`, `deep_mond_cleared`, `mond_radius_sq`, `virial_temperature`, `phantom_bracket`, `equilibrated_is_phantom` (THE IDENTIFICATION), `cap_exists_unique`, `cloud_mass_linear`, `the_equilibrium_spine` |
| `lean/G001_clockmaker_dilemma.lean` | 9 | The clock no-go: running-U amplifies the required potential slope by the clock rate |
| `lean/G002_G003_onefunction_phantom.lean` | 4 | The curve + the phantom bracket |
| `lean/G007_bimetric.lean` | 11 | The bimetric closure: `lensing_sum_cancellation`, `disformal_entries`, `stress_vs_phantom_ratio`, `phantom_kinetic_sign`, `flip_vacuum`, `flip_kinetic_healthy`, `deep_mond_law` |
| `lean/G031_fluid_action.lean` | 13 | The hydrostatic spine: temperature → identification → BTFR → g²=a₀g_N, ending in `the_spine` |
| `lean/G036_formal_extras.lean` | 4+ | The slab column cancellation (∫=0 via `integral_rpow`), the peak 26.7 M☉/pc², the w-window coldness |
| `lean/G005_derived_length.lean` | 8 | (companion) the derived-length/ξ chain |

## The KEY LEMMA that unblocks the spine

$$\sqrt{\frac{GM}{a_0}}\cdot\sqrt{GMa_0} = GM, \qquad (GM/a_0)(GMa_0)=(GM)^2$$

Pure `Real.sqrt_mul` + `Real.sqrt_mul_self` composition — no nonlinear arithmetic
lemmas needed. This single identity unlocks the virial temperature and the
identification (`sqrt_num_iden`, `EQUILIBRIUM_THEORY.lean:49`).

## The identification, machine-checked end to end

`equilibrated_is_phantom`: the equilibrated isothermal density

$$\rho = \frac{\sigma^2}{2\pi G r^2} = \frac{\sqrt{GM_b a_0}}{4\pi G r^2}$$

EQUALS the deep-MOND phantom density, **coefficient exactly one**. This is the
theory's central claim, provable in Lean, zero `sorry`.

## Scope statement (how every certificate in this repo reads)

Lean certifies the MATHEMATICS. The physical reading — that the cold sector
equilibrates into the phantom — is the committed lanes' claim, tested against
SPARC (G002/G013), the Milky Way (G003), wide binaries (G006/G014), clusters
(G008/G012), the Cassini gate (G004/G005/L243), and the CMB (G052). The theorems
are the arithmetic those tests rest on.
# A fixed-direction Solar-System Lorentz-violation target: the s^TX boost-dipole of de Sitter–Unruh modified inertia

**Carl P. Zimmerman** · Briar Creek Tech · 2026-06-27
**A prediction note for the planetary-ephemeris community (INPOP / EPM / DE).**

## The ask, in one line

The de Sitter–Unruh modified-inertia account of the MOND scale is a **preferred-frame** theory, so it induces a **specific, forced, non-zero gravity-sector Lorentz-violation coefficient** with a **fixed sky direction**. A dedicated ephemeris fit for the **s̄^TX boost-dipole** at the **~9×10⁻¹⁰ level** — a factor ≈1.5 below the current bound — would **detect or exclude** it. The data already exist; the dedicated dipole fit has, to our knowledge, not been run.

## Why there is a forced s̄^TX

If inertia is a body's response to the de Sitter–Unruh bath of the cosmological horizon (Milgrom 1999; Deser–Levin 1997), the bath defines a **preferred rest frame — the cosmic (CMB) frame.** A preferred frame *is* a Standard-Model-Extension (SME) gravity-sector background s̄_μν (Bailey & Kostelecký 2006; Kostelecký & Tasson 2011). The Solar System moves at **v = 369.8 km s⁻¹** toward the CMB apex, **β = v/c = 1.23×10⁻³**, so the otherwise-isotropic background acquires a **time–space (boost) component s̄^TX ∝ β** aligned with that apex. Its magnitude is inherited from the same a₀ = cH_Λ/Z = 9.36×10⁻¹¹ m s⁻² that sets the MOND scale (component ledger in the author's published SME-bridge work).

## The prediction (specific and falsifiable)

| quantity | value |
|---|---|
| coefficient | **s̄^TX** (gravity sector, boost-dipole) |
| predicted magnitude | **≈ 8.7×10⁻¹⁰** |
| sign/CPT | **CPT-even only** (the CPT-odd k_AF channel vanishes) |
| **sky direction (fixed, not fit)** | **the CMB apex: (l, b) = (264.0°, 48.3°); (RA, Dec) ≈ (168°, −7°)** |
| current bound (ephemerides) | \|s̄^TX\| ≲ 1.3×10⁻⁹ (Hees et al. 2015) |
| **margin** | **≈ 1.5× under the present limit** |

The fixed direction is the discriminating feature: this is **not** a free coefficient to be marginalized, but a dipole **locked to a known point on the sky**, so the fit has one fewer degree of freedom than a generic SME search.

## The decisive measurement

A dedicated **s̄^TX dipole fit** — orbital dynamics plus light propagation in the Time-Transfer Formalism (Hees et al. 2015) — reaching **σ(s̄^TX) ≈ 4×10⁻¹⁰** (a factor ≈1.5–2 beyond the present sensitivity) will:

- **detect** a dipole of ≈8.7×10⁻¹⁰ aligned with the CMB apex → support for a preferred-frame (modified-inertia) origin of the MOND scale; or
- **bound it below 8.7×10⁻¹⁰** → exclude this preferred-frame realization.

**The data are in hand:** INPOP / EPM / DE planetary ranging, the Cassini Saturn arc (extended), Mars-orbiter ranging, and **BepiColombo** Mercury ranging (arrival 2026) tighten exactly the channels that carry s̄^TX. This is **analysis-limited, not data-limited.**

## Honest scope (what this is and is not)

- The magnitude inherits the framework's own modeling of the a₀→s̄_μν map; the **direction and CPT-even character are robust** consequences of "preferred frame = CMB frame," the **magnitude is framework-specific** (±O(1)).
- This is a test of the **gravity-sector preferred frame only** — it is a theory of **gravity and the dark sector, not a theory of everything**; the Standard-Model matter sector is untouched.
- The framework **passes every other named gravity-sector bound** (LLR, INPOP/Cassini γ, atom interferometry, pulsar α₂, VLBI); s̄^TX is its **tightest** exposure, which is why it is the one most worth a dedicated fit.

## References
- M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A 253 (1999) 273.
- S. Deser, O. Levin, Class. Quantum Grav. 14 (1997) L163.
- Q. Bailey, V. A. Kostelecký, *Signals for Lorentz violation in post-Newtonian gravity*, Phys. Rev. D 74 (2006) 045001.
- V. A. Kostelecký, J. Tasson, Phys. Rev. D 83 (2011) 016013.
- A. Hees et al., *Testing Lorentz symmetry with planetary orbital dynamics*, Phys. Rev. D 92 (2015) 064049 [arXiv:1508.03478].
- A. Fienga et al., INPOP planetary ephemerides (and BepiColombo simulations).
- Author's published de Sitter–Unruh papers: DOI 10.5281/zenodo.20973740, 10.5281/zenodo.20965016.

*Reproducible: `reviews/stx_target.py`. Footing a₀ = 9.36×10⁻¹¹ m s⁻², Z = √(32π/3).*

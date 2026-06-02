# A Falsifiable Forecast for JWST

### The MOND acceleration scale as the cosmic dynamical acceleration — and what it predicts for early galaxies

**Carl Zimmerman** · June 2026 · *all results reproducible from the cited code*

---

## The idea, in one paragraph

Modified Newtonian Dynamics (MOND) has a single critical acceleration, a₀ ≈ 1.2×10⁻¹⁰ m/s²,
below which the dynamics of galaxies depart from Newton's law. For forty years it has been
noticed that this scale is numerically close to the cosmic acceleration cH₀ — the speed of
light times the expansion rate. This note takes that coincidence literally: it supposes that
a₀ is *set by the mean density of the universe*,

> **a₀ = (c/2)·√(G ρ_c) = cH/Z,  Z = 2√(8π/3) ≈ 5.79.**

I want to be honest about what this is and isn't. The √(8π/3) is exact Friedmann physics; the
remaining factor of two is a posited O(1) number — a clean choice, but not derived, and shared
in spirit with Milgrom's and Verlinde's readings of the same coincidence. So this is a *novel
framing* of a known relation, not a derivation. Its value is not in the coefficient. Its value
is in the one thing the framing forces — a single, sharp, falsifiable prediction.

## The one sharp consequence: a₀ evolves

If a₀ tracks the cosmic density, and the density falls as the universe expands, then a₀ must
have been *larger in the past*:

> **a₀(z) = a₀(0)·E(z),  E(z) = √(Ω_m(1+z)³ + Ω_Λ).**

This prediction is **coefficient-free** — the posited number Z cancels in the ratio — so it
cannot be tuned. It is the single distinctive claim, and it is already testable. Fitting the
2026 data (the local SPARC scale, Vărăşteanu's z≈0.05 sample, and the MUSE-DARK measurement at
z≈0.9) gives a₀ ∝ E(z)^p with **p = 0.80 ± 0.17: constant a₀ is rejected at 5σ, and so is the
matter-only (1+z)^{3/2} alternative.** The data, for the first time, lean toward evolution.

## Why JWST is the decisive instrument

The effect grows fast with redshift. By z = 6, a₀ would be ten times its local value; by z =
10, twenty times. JWST reaches exactly this regime. And the crucial point — the thing that makes
this a real test rather than a story — is that **every observable scales with the same number,
E(z).** A coherent dependence across many independent measurements, all driven by one quantity,
is a signature that no combination of ΛCDM with measurement systematics can counterfeit.

| redshift | E(z) = a₀(z)/a₀(0) | M_dyn/M⋆ (×√E) | velocities (×E¼) | Tully–Fisher shift (−log E) |
|:--:|:--:|:--:|:--:|:--:|
| 2 | 3.0 | ×1.7 | +32% | −0.48 dex |
| 6 | 10.4 | ×3.2 | +80% | −1.0 dex |
| 10 | 20.5 | ×4.5 | +113% | −1.3 dex |

## The predictions

**Dynamical masses rise as √E(z).** In MOND the apparent "dark matter" of a galaxy — the gap
between its kinematic mass and its baryonic mass — grows with a₀. So the ratio M_dyn/M⋆ measured
from JWST spectroscopy should climb with redshift as √E: a factor of three by z≈6, four and a
half by z≈10. **Two cautions, from a hard look at the numbers (`reviews/redteam_the_puzzle.py`):**
this is a *deep-MOND* prediction — it needs g_bar < a₀(z), so it applies to **extended,
low-surface-brightness** high-z galaxies; compact, massive ones sit near the *Newtonian* regime
(g/a₀ ∝ (1+z)^{½}, rising with z), where the boost shrinks. And the often-cited de Graaff et al.
(2024) ratios M_dyn/M⋆ up to 40 in compact JADES galaxies are **not** evidence for this: the
evolving-a₀ boost reaches only ~3 for such compact systems — an order of magnitude short — so if
those ratios are real they are a puzzle *for* MOND, not a confirmation of it.

**The Tully–Fisher and Faber–Jackson relations shift.** Because v⁴ = G·M·a₀(z), a galaxy of
fixed baryonic mass spins faster at high redshift, and the zero-point of the mass–velocity
relation moves by −log₁₀E(z) — roughly half a dex by z = 2, a full dex by z = 6. The
intermediate-redshift precedent already exists: Übler and collaborators (2017) measured a shift
of −0.45 dex at z ≈ 2.3, almost exactly the −0.48 the relation predicts.

**Velocities and dispersions are boosted as E(z)¼**, about +80% by z = 6 at fixed baryonic mass.
**The radial-acceleration relation's knee moves to higher acceleration.** Galaxies enter the
deep-MOND regime at **smaller radius** (the characteristic scale shrinks as 1/√E), and their
**critical surface density rises as E(z)**, so early disks should be denser.

**One clean null test.** Build a galaxy scaling relation from a sample spanning a range of
redshifts. If a₀ evolves, the relation is artificially *broadened* — by an amount log E(z_max) —
because each galaxy carries a different a₀. Rescale each by its own E(z) and the relation should
snap back to its intrinsic, tight form. Do-nothing-broadens, rescaling-tightens: a built-in
falsifier that needs no external calibration.

## What this does *not* predict — and why that matters

A theory is only as trustworthy as the claims it refuses to make. The evolving a₀ is **absent
from the linear growth of cosmic structure** (this follows from the structure of the only
relativistic completion that fits the microwave background). The consequence is important and
deflationary: **evolving a₀ does not, by itself, make galaxies form earlier or in greater
number.** It changes the *dynamics* of galaxies that have already formed, not the *census* of
how many exist. So the much-discussed "impossible" early massive galaxies are addressed by this
framework **only** where their masses are inferred dynamically — in which case those masses are
over-estimated by √E(z), and the galaxies are lighter in baryons than they appear. Where a mass
excess comes from stellar light, or where the puzzle is the sheer abundance of luminous sources,
this framework is **silent**. It likewise says nothing about metallicities, reionization, dust,
or the ultraviolet luminosity function — those are the physics of gas and stars, not of a₀.
Naming them as victories, as earlier versions of this work did, was a mistake. The honest
boundary is part of the prediction.

## How to run the test

Do not fit a single galaxy. **Measure the dynamical-mass ratio, the Tully–Fisher zero-point, the
dispersions, the sizes, and the surface densities across a span of redshift, and ask whether
they all key off the same E(z).** If M_dyn/M⋆ ∝ √E *and* the zero-point ∝ −log E *and* the
dispersions ∝ E¼, simultaneously, with one consistent expansion history — that coherence is the
fingerprint of an evolving a₀, and nothing else makes it. If the channels scatter independently,
the idea is wrong, and the same data say so cleanly. The single most decisive measurement is a
clean determination of M_dyn/M_baryon at a known baryonic acceleration in a galaxy at z > 2.

## What is actually being claimed

Not a theory of everything; not a derivation of the MOND scale; not a solution to the dozens of
problems earlier drafts of this idea claimed. The claim is narrow and, for that reason,
testable: **that the acceleration scale governing galaxies is the cosmic density's own
acceleration, so it must evolve as E(z) — and JWST is now precise enough to see it.** The
universe's largest scale would then be reaching into its smallest dynamics: *here* would be set
by *everywhere*. That is either true or it isn't, and the next few years of JWST kinematics will
decide it.

---

*Reproducibility:* `a0_decisive_pipeline.py` (the 5σ data fit), `jwst_full_predictions.py` (the
full prediction map), `bridge1_aest_equations.md` (why a₀ is absent from linear growth), and the
repository at github.com/carlzimmerman/zimmerman-formula.
*Key data:* McGaugh, Lelli & Schombert 2016 (SPARC); Übler et al. 2017 (KMOS³ᴰ); de Graaff et
al. 2024 (JADES); Vărăşteanu et al. 2025; MUSE-DARK III 2026. *Foundations:* Milgrom 1983;
Skordis & Złośnik 2021 (the relativistic completion); Verlinde 2017.

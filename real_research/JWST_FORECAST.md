# A Falsifiable Forecast for JWST

> **⚠️ COEFFICIENT-FOOTING CORRECTION (2026-06-13):** Any "a₀ = cH₀/Z", "1/Z = 0.173 against cH₀", or "1/Z bracketed by Milgrom 1/2π / Verlinde 1/6" below uses the **superseded footing**. Canonical: a₀ = c²√(Λ/32π) = cH_Λ/Z = 9.36×10⁻¹¹ (ρ_DE; cH_Λ = √Ω_Λ·cH₀ = 0.83·cH₀). The coefficient 1/Z = 0.173 is against **cH_Λ**; against cH₀ it is **0.143**. Milgrom (0.159) and Verlinde (0.167) use cH₀, so the apt comparison is 0.143 — the **low outlier**, NOT bracketed. cH₀/Z = 1.13×10⁻¹⁰ is the ρ_total reading (+20%). See [THE_A0_COEFFICIENT_CONVENTION.md](THE_A0_COEFFICIENT_CONVENTION.md) + [THE_A0_COEFFICIENT_AUDIT_2026-06-13.md](THE_A0_COEFFICIENT_AUDIT_2026-06-13.md).


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
z≈0.9) gives a₀ ∝ E(z)^p with **p = 0.80 ± 0.17**. *Honest significance (corrected from an
earlier overstatement):* the naive "5σ" rejection of constant a₀ assumes three heterogeneous
measurements are commensurate to their tiny quoted errors; folding in the inter-method
systematic the local pair already demands drops it to **~2σ**, and dropping the single
high-leverage z≈0.9 point drops it to **~1.2σ**. It is also degenerate with ΛCDM RAR-evolution
plus selection. So the honest status is a **~2σ hint in the predicted direction, not a
detection** (`reviews/stresstest_piece3_evolution.py`). The value is in the *forward* test.

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

## GN-z11, and the compact-galaxy trap

The most-discussed massive early galaxy, **GN-z11 at z = 10.60**, makes the regime caveat
concrete. JWST IFS (Xu et al. 2024) measures M⋆ ≈ 1.3×10⁹ M⊙, a dynamical mass M_dyn = (1.1 ±
0.4)×10⁹ M⊙ — *dominated by the stellar component* — a rotation ≈ 205 km/s, and a half-light
radius of only **~60 pc**; it also hosts an AGN (Maiolino et al. 2024). Run the numbers
(`reviews/jwst_predictions_comprehensive.py`): at z = 10.6, E = 22.2 and a₀(z) = 2.7×10⁻⁹ m/s²,
but GN-z11's internal acceleration is g_bar = GM⋆/R_e² ≈ 4.9×10⁻⁸ m/s² — so **g_bar/a₀(z) ≈ 18,
deeply Newtonian.** The MOND transition radius is r_M ≈ 257 pc, well *outside* the 60-pc
half-light radius. The framework therefore predicts **no boost** (ν ≈ 1.05, i.e. M_dyn/M⋆ ≈ 1),
and the observed M_dyn/M⋆ ≈ 0.87 **agrees — but trivially**: no enhancement was predicted, none
is seen, and the same is true of plain Newton and ΛCDM. **GN-z11 does not test the framework.**
It is the wrong *kind* of galaxy (compact, not extended), AGN-contaminated, and its
"massiveness" is a *star-formation* puzzle (efficiency, IMF, feedback-free collapse) that a₀(z)
does not touch. The √E ≈ 4.7× boost lives only in **extended, low-surface-brightness** galaxies
where g_bar < a₀(z) — exactly the systems current high-z kinematic samples under-represent.

## When the data arrives

The relevant observations exist *now* and are growing, but the *clean* test targets are still
scarce:
- **Already public / published:** GN-z11 dynamics (Xu et al. 2024); JADES/NIRSpec ionised-gas
  kinematics and dynamical masses at z ≳ 6 (Übler et al. 2023); JWST-SUSPENSE stellar kinematics
  of z > 1 quiescent galaxies (2025); the JADES rotation-distribution analysis (2025). Most JWST
  Cycle 1–2 spectroscopy has passed its 12-month proprietary period and is on MAST; Cycle 3–4
  data become public through 2026–2027.
- **The gap:** these samples are dominated by *compact*, often AGN-bearing systems (Newtonian →
  no signal), lack gas masses, and carry no environment split — so they are uninformative for
  the √E boost and silent on the EFE. de Graaff et al. (2024) ratios up to ~40 are upper limits
  on compact galaxies, *not* support.
- **What it takes:** a dedicated, environment-resolved, *extended*-galaxy kinematic campaign
  (JWST + ALMA gas masses now; ELT/HARMONI for the z ≳ 6 lever arm, ~2029+). The distinctive
  EFE-vs-z signal needs ~600–1600 such galaxies — a next-decade measurement
  (`EFE_vs_z_Forecast_2026`). The cross-channel **coherence** test can begin sooner, as soon as a
  few dozen extended z > 2 galaxies have simultaneous M_dyn, baryons, sizes and dispersions.

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

*Reproducibility:* `reviews/stresstest_piece3_evolution.py` (the a₀(z) data fit, honestly ~2σ
after systematics), `reviews/jwst_predictions_comprehensive.py` (the full prediction map +
regime check + GN-z11), `bridge1_aest_equations.md` (why a₀ is absent from linear growth), and
the repository at github.com/carlzimmerman/zimmerman-formula.
*Key data:* McGaugh, Lelli & Schombert 2016 (SPARC); Übler et al. 2017 (KMOS³ᴰ); Übler et al.
2023 (JADES kinematics, z≳6); Xu et al. 2024 (GN-z11 dynamics, arXiv:2404.16963); Maiolino et
al. 2024 (GN-z11 AGN); de Graaff et al. 2024 (JADES compacts — upper limits); Vărăşteanu et al.
2025; MUSE-DARK III 2026. *Foundations:* Milgrom 1983; Skordis & Złośnik 2021 (the relativistic
completion); Verlinde 2017.

# Gravity from the de Sitter Horizon
## A Geometric Framework Unifying the MOND Acceleration Scale and Dark Energy

**C. Zimmerman.** *Whitepaper — June 2026. Companion calculations: `real_research/reviews/project_*.py`.*

---

## Abstract

We present a geometric framework in which the single fundamental scale of the late Universe — the cosmological
constant Λ — generates, through the geometry of the de Sitter horizon it creates, the entire low-acceleration
("dark") phenomenology of galaxies. The framework rests on three geometric postulates: that spacetime is
asymptotically de Sitter (Λ>0, a finite cosmic horizon of curvature √Λ); that gravity is holographic (encoded on
that horizon); and that gravitational dynamics are asymptotically scale-covariant, broken only by the horizon
scale. From these follows a single central equation,

>  **a₀ = c²√(Λ/32π) = cH(z)/Z,  Z = 2√(8π/3) = 5.789,**

identifying the MOND acceleration scale a₀ with the de Sitter curvature expressed as an acceleration,
holographically reduced by the Friedmann/horizon degree-of-freedom factor Z. The deep-MOND √-law, the
transition radius (the geometric mean of an object's Schwarzschild radius and the cosmic horizon), the *sign* of
the modification (gravity enhanced below a₀), the external field effect (EFE), the redshift evolution of a₀, and
the long-noted a₀ ≈ cH₀ coincidence all emerge as facets of one geometric structure. **Dark matter (as modified
gravity) and dark energy are thereby the same geometry**: a₀ = c²√(Λ/32π). We verify the EFE — a violation of
the strong equivalence principle that ΛCDM cannot produce and that is observed at 4–5σ — and lay out the
framework's distinctive, falsifiable predictions. We are explicit about what is derived, what is postulated, and
what remains open: the coefficient Z is geometrically natural but not uniquely forced; the microscopic origin of
the sign rests on the (contested) identification of de Sitter with the double-scaled SYK spectral centre; and the
mere *evolution* of a₀ is shared with ΛCDM, so the framework's distinctive content is the EFE, the a₀–H₀ link,
and the derived deep-MOND sign, not the evolution itself.

---

## 1. Introduction

Two empirical facts organize the dark sector of cosmology. First, galaxies exhibit a tight, one-to-one *radial
acceleration relation* (RAR): the observed centripetal acceleration g_obs is a fixed function of the acceleration
g_bar predicted from baryons alone, with a single characteristic scale a₀ ≈ 1.2×10⁻¹⁰ m s⁻² below which g_obs
systematically exceeds g_bar, asymptoting to g_obs = √(a₀ g_bar) (Milgrom 1983; McGaugh, Lelli & Schombert 2016).
Second, the Universe's expansion accelerates, driven by a cosmological constant Λ with ρ_Λ ≈ 0.7 ρ_crit.

A numerical coincidence ties them: a₀ ≈ cH₀/2π ≈ c²√(Λ/3) to within order unity. In ΛCDM these are unrelated —
a₀ is an emergent outcome of baryonic galaxy formation, Λ a vacuum energy — and the coincidence is accidental.
This whitepaper takes the opposite stance: the coincidence is *causal*, and a₀ is the de Sitter horizon's
imprint on local dynamics. The idea sits in the lineage of emergent/entropic gravity (Jacobson 1995; Padmanabhan
2010; Verlinde 2011, 2017), in which the gravitational field equations arise thermodynamically from causal-
horizon entropy, and a₀ ~ cH₀ is the scale at which the de Sitter horizon's entropy budget becomes dynamically
relevant. Our contribution is to organize this into a single-input geometric framework, derive its structure,
verify its key falsifier (the EFE), and state honestly what is and is not established.

## 2. The framework: one scale, three postulates

**The single input.** A universe with Λ > 0 possesses a finite cosmic (de Sitter) horizon of radius R_dS =
c√(3/Λ) and curvature √Λ. We take Λ to be the *only* dimensionful constant of the late Universe beyond c and G.
Everything below is derived from it.

**P1 — de Sitter geometry.** Spacetime is asymptotically de Sitter; the observer's static patch is bounded by a
horizon of curvature √Λ. (Empirically: the accelerating Universe.)

**P2 — Holography.** Gravitational degrees of freedom are encoded on the horizon, with entropy S = A/4G ℓ_P². The
horizon is the fundamental screen.

**P3 — Scale-covariance.** In the deep low-acceleration limit, gravitational dynamics are invariant under
coordinate dilations (t, r) → λ(t, r) — Milgrom's *spacetime scale invariance* — broken only by the horizon
scale √Λ. (The deep-MOND limit g = √(g_N a₀) is the unique scale-invariant gravitational dynamics; a₀ is the one
scale that breaks it.)

## 3. The central result: a₀ as the cosmic curvature

The horizon surface gravity sets an acceleration scale. Writing the free-fall acceleration of a medium of
density ρ as (c/2)√(Gρ), and using the de Sitter density ρ_Λ = c²Λ/8πG, the horizon acceleration is

>  **a₀ = (c/2)√(Gρ_Λ) = c²√(Λ/32π) = c²√Λ / (Z√3),  Z = 2√(8π/3).**

Equivalently a₀ = cH_Λ/Z with H_Λ = c√(Λ/3); in an expanding universe the instantaneous horizon gives a₀(z) =
cH(z)/Z. Numerically, with the observed Λ = 1.08×10⁻⁵² m⁻², this yields a₀ = 0.93×10⁻¹⁰ m s⁻² (event horizon)
to 1.12×10⁻¹⁰ (apparent horizon, cH₀/Z), bracketing the observed 1.2×10⁻¹⁰ within the stellar mass-to-light
systematic. The MOND scale **is the cosmic curvature, holographically reduced by Z√3 ≈ 10**.

**The coefficient Z.** Z = 2√(8π/3) is the Friedmann conversion between density and expansion rate (√(Gρ) ↔ H),
equivalently the de Sitter horizon's degree-of-freedom counting. It is built from geometric constants — the
solid angle 4π, the spatial dimension 3, and the surface-gravity factor 2 — and is the *exact* density↔rate
conversion. **Honesty (see §11):** Z is geometrically *natural* but not *uniquely forced*; alternative horizon
criteria give O(1) coefficients in the band 5.8–6.3, and only a ~6% absolute a₀ measurement (with pinned H₀)
separates them. The number 32π = 3Z² is the geometric conversion between Λ and a₀ — the legitimate home of a
quantity earlier misused; it is *not* a free fit.

## 4. The geometric architecture

The single equation of §3 organizes a coherent geometric architecture.

**(a) The deep-MOND law as a geometric mean.** Below a₀, scale-covariance (P3) forces g_obs = √(g_N a₀): the
observed acceleration is the *geometric mean* of the local (baryonic) acceleration g_N and the cosmic
acceleration a₀.

**(b) The transition radius as a geometric mean.** A mass M crosses into the modified regime at the MOND radius
r_M = √(GM/a₀). With a₀ = cH/Z this is *exactly* the geometric mean of the object's Schwarzschild radius and the
cosmic horizon: **r_M = (8π/3)^{1/4} √(r_s R_H)**, r_s = 2GM/c², R_H = c/H. For 1 M⊙: r_M ≈ 7000 AU = geometric
mean of 3 km and 14.6 Gly. The MOND scale literally bridges the smallest and largest length scales.

**(c) The UV/IR self-dual principle.** The inversion r → r_s R_H / r swaps an object's gravitational scale and
the cosmic horizon. Its self-dual fixed point is √(r_s R_H), where the acceleration is cH/2 — mass-independent.
**MOND is the regime where an object's gravity (UV) and the cosmic horizon (IR) are in geometric balance.** This
makes the scaling a₀ ~ cH geometrically inevitable; only the O(1) offset (the Friedmann factor) is convention-
dependent.

**(d) a₀ as curvature.** Since a₀/c² = 1/(Z R_H) is an inverse length, a₀ is the cosmic curvature as an
acceleration: Λ = 32π (a₀/c²)². Dark matter (as MOND) and dark energy are the same geometric quantity.

## 5. The microscopic origin of the sign

The hardest problem in any emergent-MOND program is the *sign*: why is gravity *enhanced* (not suppressed) below
a₀? In the framework this follows from the spectral structure of the holographic degrees of freedom. The de
Sitter static patch is conjectured to be dual to the double-scaled SYK model (DSSYK) at its spectral centre
(Narovlansky–Verlinde 2023), where the density of states is *flat*. Mapping the MOND interpolation function to
the cumulative "freezing" of these horizon degrees of freedom, a flat density of states integrates linearly,
producing μ(x) ∝ x at small x — exactly the deep-MOND condition that yields the √-law and flat rotation curves.
We have shown (companion work) that the *competing* identification of de Sitter with the spectral *edge*
(Schwarzschild/Schwarzian, where the density of states vanishes as √E) would instead give g_obs ∝ g_bar^{0.4} —
*rising* rotation curves, excluded by observation. **The very existence of flat rotation curves therefore
selects the spectral-centre identification.** This is the framework's most speculative pillar (the de Sitter =
DSSYK-centre proposal is actively debated), and we flag it as such; but it is the part that converts a₀'s
*magnitude* into a₀'s *sign*.

## 6. The external field effect (verified)

The sharpest qualitative consequence — and the cleanest discriminator against ΛCDM — is the *external field
effect* (EFE). Because the modified dynamics are non-linear and scale-covariance is broken non-locally, a
system's internal gravity depends on the *external* field in which it is embedded. In the quasi-linear (QUMOND)
approximation the internal observed acceleration of a system with Newtonian internal field g_N in external field
g_ext is

>  g_obs = ν(|g_N+g_ext|/a₀)·|g_N+g_ext| − ν(g_ext/a₀)·g_ext.

We verify (companion `project_distinctive_tests.py`; reproduced here) that this produces the signature downturn:

| g_bar/a₀ | isolated | g_ext=0.1 a₀ | g_ext=1.8 a₀ (Milky-Way-like) | g_ext=10 a₀ |
|---|---|---|---|---|
| 0.003 | 18.8 | 2.1 | 1.09 | 1.01 |
| 0.10 | 3.7 | 1.9 | 1.09 | 1.01 |
| 1.0 | 1.6 | 1.4 | 1.07 | 1.01 |

(entries are g_obs/g_bar.) An isolated system shows the full √-law boost (×19 at g_bar=0.003 a₀); the *same*
system in a strong external field is driven back to Newtonian (boost → 1). **Internal dynamics depend on the
external field — a violation of the strong equivalence principle.** Newtonian gravity plus a dark-matter halo
*cannot* produce this: by the shell theorem a uniform external field cancels inside the halo. The EFE is
therefore a clean, qualitative ΛCDM-falsifier, and it is **observed**: Chae et al. (2020, 2021) detect the
predicted RAR downturn for galaxies in strong external fields in the SPARC sample at ≈4–5σ. The framework
predicts it identically, with a₀ = c²√(Λ/32π); the EFE is the non-locality of the de Sitter horizon coupling.

## 7. Cosmological evolution and the a₀–H₀ link

Because the horizon evolves, a₀(z) = cH(z)/Z rises toward higher redshift. The framework's original prediction —
a₀ ∝ cH(z), a factor ~3 increase from z=0 to z=2 — is consistent with the first direct measurements (MUSE-DARK
III; a rise is observed) and, notably, with independent ΛCDM hydrodynamic simulations (Mayer et al. 2023, ~×3).
**This shared prediction means the *evolution* of a₀ tests evolving-a₀ physics against *constant*-a₀ MOND (which
it excludes), but does not by itself separate the framework from ΛCDM.** The framework's distinctive evolutionary
content is rather the *normalization tie*: a₀ = cH₀/Z links the galaxy-dynamics scale to the cosmic expansion
rate. ΛCDM predicts no such relation. Taking the observed a₀ = 1.20±0.26 gives H₀ = 72±15 km s⁻¹ Mpc⁻¹ — central
to the Hubble tension; a future 6% a₀ with a pinned H₀ turns the a₀ ≈ cH₀ coincidence into a sharp test of a₀ =
cH₀/Z.

## 8. The unification

The framework's claim is economy: one input (Λ) and three geometric postulates generate

| phenomenon | geometric origin |
|---|---|
| the MOND scale a₀ | the de Sitter curvature, a₀ = c²√(Λ/32π) |
| the deep-MOND √-law | scale-covariance (the geometric-mean law) |
| the transition radius r_M | the UV/IR self-dual point (geometric mean of r_s, R_H) |
| the *sign* (enhancement) | the flat horizon density of states (DSSYK centre) |
| the coefficient Z | the Friedmann/holographic DOF counting |
| the external field effect | non-local horizon coupling (broken strong equivalence) |
| the evolution a₀(z) ∝ cH(z) | the growing horizon |
| the a₀ ≈ cH₀ coincidence | a₀ = cH₀/Z (galaxy scale = cosmic scale) |

**Dark matter (as modified gravity) and dark energy are one geometry.** What ΛCDM treats as two unrelated dark
components — a clustering dark matter and a smooth dark energy — the framework treats as two faces of the de
Sitter horizon: the dark-energy density *is* the curvature that sets a₀, and the "dark matter" of galaxies is the
horizon's modification of gravity below that scale.

## 9. Predictions and tests

- **External field effect (verified, 4–5σ).** The strongest current evidence; qualitatively impossible in ΛCDM.
  *Next:* re-derive the Chae signal with the framework's interpolation and tightened environment data.
- **Wide binaries (z=0, no dark sector).** A pure force-law test. The framework's derived (sharp) interpolation
  predicts a *small* internal boost ~+5% under the Milky Way field — between ΛCDM (0%) and standard simple-μ MOND
  (~+18%). Gaia DR4 decides.
- **The a₀–H₀ link.** a₀ = cH₀/Z; a 6% absolute a₀ with a pinned H₀ tests whether the coincidence is causal.
- **a₀(z) rising ~×3** (consistent with data and ΛCDM sims; excludes constant-a₀ MOND).
- **RAR tightness / no second parameter** (g_obs a function of g_bar alone) — favored over ΛCDM, established in
  SPARC.

## 10. The relativistic completion

The framework is, at present, a non-relativistic geometric theory plus a thermodynamic interpretation. A
covariant completion — a scalar-tensor (RAQUAL/TeVeS-class) theory in which the scalar's kinetic scale is tied
to Λ, reproducing a₀ = c²√(Λ/32π) and the EFE while passing solar-system and gravitational-wave constraints — is
the principal theoretical task. The de Sitter / DSSYK holographic structure (the chord/length duality of
sine-dilaton gravity) is the candidate microscopic substrate. This is open and hard, and we do not claim it.

## 11. Honest status: derived, postulated, open

We separate the framework's claims by epistemic standing, because a framework's credibility is its honesty about
its own gaps.

- **Derived / solid:** the deep-MOND √-law and its sign from horizon DOF freezing (given the spectral-centre
  identification); the interpolation shape (fits SPARC to ~6%, nearly coupling-independent); a₀ ~ c√Λ at order
  unity; the geometric-mean / self-dual architecture; Z = 2√(8π/3) as the Friedmann factor; the EFE (verified).
- **Postulated:** holography and scale-covariance (P2, P3) — standard in emergent gravity but not proven; the
  de-Sitter-static-patch = DSSYK-spectral-centre identification (Narovlansky–Verlinde), which underwrites the
  sign and is *actively contested* (Rahman 2025 places de Sitter at the spectral edge; we showed flat rotation
  curves favor the centre, but the question is open).
- **Open:** the *exact* coefficient Z (geometrically natural, not uniquely forced — a ~6% a₀ measurement
  decides); the relativistic completion (§10); the cosmic dark-matter budget (the cluster-scale residual that
  challenges all MOND); and the fact that a₀'s *evolution* is shared with ΛCDM, so the framework's distinctive
  case rests on the EFE, the a₀–H₀ link, and the derived sign — not on evolution.

**What would falsify it:** a robust *null* EFE (wide binaries and SPARC both Newtonian) would remove its
empirical foundation; a₀ measured to ≲6% landing far from cH₀/Z would break the central equation; de Sitter
shown to be the spectral edge would remove the sign derivation.

## 12. Comparison

| | ΛCDM | standard MOND | this framework |
|---|---|---|---|
| a₀ origin | accidental (galaxy formation) | fundamental constant (free) | **c²√(Λ/32π)** (derived from Λ) |
| a₀ ≈ cH₀ | coincidence | coincidence | **causal** |
| a₀ evolution | yes (~×3, sims) | no (constant) | yes (cH(z)/Z) |
| EFE | impossible | yes | **yes** (verified 4–5σ) |
| dark matter & dark energy | two components | unrelated | **one geometry** |
| free parameters (dark sector) | Ω_DM, halo profiles | a₀ + shape | Λ (measured); Z bounded; shape derived |

## 13. Conclusions

A single geometric input — the cosmological constant, read as the curvature of the de Sitter horizon — together
with holography and scale-covariance, generates the MOND acceleration scale (a₀ = c²√(Λ/32π)), the deep-MOND
law, the transition geometry, the sign of the modification, the external field effect, the evolution of a₀, and
the a₀ ≈ cH₀ coincidence, as facets of one structure. Dark matter (as modified gravity) and dark energy are
unified as the geometry of the cosmic horizon. The framework's strongest evidence is the external field effect —
a strong-equivalence-principle violation impossible in ΛCDM and observed at 4–5σ — which we have verified
explicitly. Its honest limits are equally clear: the coefficient is not uniquely forced, the microscopic sign
rests on a contested holographic identification, a covariant completion is outstanding, and the evolution it
predicts is shared with ΛCDM. The framework is offered as a coherent, falsifiable, geometric account of the dark
sector — not a finished theory of everything, but a unification of two dark mysteries into one piece of
geometry, with a sharp experimental program to confirm or kill it.

## References (representative)

Chae et al. 2020, 2021 (EFE detection); Jacobson 1995; Lelli, McGaugh & Schombert 2016 (SPARC); Mayer et al.
2023 (a₀ in hydro sims); McGaugh, Lelli & Schombert 2016 (RAR); Milgrom 1983, 1999, 2017; Narovlansky & Verlinde
2023 (DSSYK = de Sitter); Padmanabhan 2010; Rahman 2025 (dS-JT at the spectral edge); Verlinde 2011, 2017;
Ciocan et al. (MUSE-DARK III) 2026; Banik et al. 2024 & Chae 2024 (wide binaries).

*All numerical claims are reproduced by `real_research/reviews/project_*.py` and documented in the companion
files `DEEP_GEOMETRY.md`, `GEOMETRIC_CANDIDATES.md`, `MICROSCOPIC_CENTER_VS_EDGE.md`, `A0Z_STATUS_CORRECTED.md`,
and `PARAMETER_SPACE.md`.*

# Foundations of the evolving-a₀ framework — the theory, layer by layer

**Carl Zimmerman · June 2026** · *the comprehensive theoretical spine of the surviving framework:
an emergent-gravity theory of the dark sector. Every rung carries an honest label. This is the
"theory of everything" rebuilt as the theory of the one thing it can actually be — gravity and
inertia at low acceleration, and how their scale is set by the cosmos.*

**Labels:** `[DERIVED]` forced by algebra/standard physics · `[GROUNDED]` made physically natural by
the foundation, not arbitrary, but not a theorem · `[POSIT]` a free O(1) choice · `[DEGENERATE]`
real but indistinguishable from ΛCDM · `[DISTINCTIVE]` non-degenerate and falsifiable · `[OPEN]`
unsolved, including in the literature · `[LIMIT]` a genuine failure · `[DEAD]` demolished, retained
only as a boundary marker.

---

## Read this first — what kind of theory this is

This is **not a theory of everything**, and the distinction is load-bearing, not modest. It is a
candidate theory of the **dark sector** — gravity, dark matter, and dark energy as facets of one
low-acceleration scale, `a₀`, set by the mean cosmic density. The Standard Model is untouched and
provably does not follow from it (`[DEAD]`; Layer 5). What it *is*: a complete, layered structure —
**foundation → law → evolution → covariant realization → consequences → boundary** — resting on a
single physical idea (inertia is emergent and Machian) and producing one distinctive falsifiable
prediction. Read top to bottom; each layer states what it earns and what it owes.

---

## Layer 0 — Foundation: emergent, Machian inertia

The premise beneath everything: **inertia is not fundamental but emergent** — the resistance of a
body to acceleration is the gravitational back-reaction of all the matter in the universe (Mach;
Sciama 1953), equivalently a horizon-thermodynamic effect (Unruh; Milgrom 1999; Verlinde 2011;
Padmanabhan). `reviews/emergent_inertia_derivation.py`.

| claim | status |
|---|---|
| The observable universe is "Machian": `G M_H/(R_H c²) = 1/2` *exactly* for ρ=ρ_crit | **`[DERIVED]`** (exact; the one clean non-arbitrary ½) |
| Inertia ← gravitational coupling to matter ⇒ the natural rate is the **free-fall rate √(Gρ)**, not the expansion rate H (they coincide only at criticality, H=√(8π/3)·√(Gρ)) | **`[GROUNDED]`** |
| MOND onset where a particle's Unruh temperature ≈ the cosmic-horizon temperature ⇒ `a₀ ~ c·(rate)` | **`[GROUNDED]`** |
| A *complete* modified-inertia dynamics (a consistent equation of motion for general, non-closed orbits) | **`[OPEN]`** — open in the literature too (Milgrom 1994, 2011: defined only for closed orbits) |

**What the foundation buys:** it grounds the *form* `a₀ ~ c√(Gρ)` and, crucially, the *evolution*
(Layer 2) — those are not assumed, they follow from inertia tracking the cosmic gravitational rate.
**What it does not buy:** the exact coefficient (the naive Machian value is the *expansion*-horizon
one, `a₀=cH/2`, Z=2, which the data **exclude** at 2.7σ — see Layer 1), and a full dynamics.

---

## Layer 1 — The law: a₀ as a horizon surface gravity

$$a_0 \;=\; \frac{c}{2}\sqrt{G\rho}\;=\;\frac{c^2}{2R_*},\qquad R_*=\frac{c}{\sqrt{G\rho}}\quad(\text{the gravitational free-fall horizon}),$$

equivalently `a₀ = cH(z)/Z` with `Z = 2√(8π/3) = √(32π/3) ≈ 5.789`. `reviews/derive_Z_*.py`.

| element | value | status |
|---|---|---|
| the free-fall horizon `R_*` = where t_freefall = t_lightcross = √(8π/3)·R_H ≈ 2.9 R_H | 12.9 Gpc | **`[GROUNDED]`** (Mach, Layer 0) |
| `√(8π/3)` = the Friedmann free-fall-to-Hubble ratio | 2.894 | **`[DERIVED]`** (exact) |
| the factor **2** = surface gravity `c²/2R` (the Schwarzschild/Rindler ½) | 2 | **`[POSIT]`** |
| → `Z = 2√(8π/3)` | 5.789 | **`[POSIT]`** (one O(1), data-allowed band ≈[5.5, 6.5]) |

**The one honest scar.** `R_*` is a *causal* free-fall horizon, **not** a Schwarzschild horizon (the
enclosed mass is 8π/3× the Schwarzschild mass for `R_*`), so the surface-gravity ½ is *borrowed*. The
coefficient sits on the same footing as Milgrom's `Z=2π` (Unruh) and Verlinde's `Z≈6` (entropy) —
all motivated O(1)s, none derived, none distinguishable by data. **The coefficient is the theory's
single irreducible posit.** It costs nothing testable, because:

---

## Layer 2 — The evolution: the falsifiable core

$$\boxed{\;\frac{a_0(z)}{a_0(0)} = E(z) = \sqrt{\Omega_m(1+z)^3+\Omega_\Lambda}\;}$$

| claim | status |
|---|---|
| `a₀` evolves as E(z) — because `a₀ ∝ √(ρ_cosmic)` and ρ falls with expansion | **`[DERIVED]`** from Layer 0; **coefficient-free** (Z cancels), Hubble-tension-independent |
| Milgrom (2014) raised exactly this possibility | prior art, credited |
| current data (SPARC z≈0; Vărăşteanu z≈0.05; MUSE-DARK z≈0.9): `a₀∝E^p`, **p=0.80±0.17** | **`[HINT]`** ~2σ |
| the "5σ" rejection of constant a₀ | **fragile** — jackknife → 1.2σ (one z≈0.9 point), inter-method systematic → ~2σ. *A hint, not a detection.* `reviews/stresstest_piece3_evolution.py` |

This is the part the foundation actually *derives*, and the part data can actually *test*. It is the
spine's load-bearing claim.

---

## Layer 3 — Covariant realization (the two technical results)

Making Layers 1–2 a real relativistic theory, not a slogan. `papers/Paper1_*`, `papers/Paper2_*`.

| result | status |
|---|---|
| **Paper I** — explicit θ-coupling in Aether-Scalar-Tensor (AeST; Skordis–Złošnik 2021): θ=∇·A=3H on FRW realizes `a₀(θ)=cθ/(3Z)` → `a₀(z)=cH(z)/Z` covariantly; galaxy anti-screening δθ→3H(z) to 1e-6 | **`[DERIVED]`** (within AeST) |
| **Paper II** — `δq⁰⁰=0` theorem: on FRW the a₀-term (∼𝒴^{3/2}, 𝒴=q^{μν}∇φ∇φ) has 𝒴̄=0, so its linear variation vanishes; the unit constraint forces δA⁰=−Ψ ⇒ δq⁰⁰=0 ⇒ **running a₀ leaves the linear CMB exactly invariant** (r_s=144 Mpc, ℓ_A=302 verified) | **`[DERIVED]`** |
| ghost-freedom, full stability bounds, complete perturbation theory of the θ-coupled sector | **`[OPEN]`** |

---

## Layer 4 — Consequences

Everything downstream of the evolving knee at `a₀(z)`. `reviews/jwst_predictions_comprehensive.py`,
`reviews/more_derivations.py`, `EFE_vs_z_Forecast_2026`.

| consequence | result | status |
|---|---|---|
| **EFE weakens with z** | `η=g_ext/a₀(z) ∝ 1/E(z)` — high-z galaxies more isolated-MOND | **`[DISTINCTIVE]`** — the one DM-forbidden, non-degenerate test; needs ~600–1600 extended z≳4 galaxies (JWST/ALMA/ELT, next decade) |
| a₀-cosmography | read `H₀=71.5`, `q₀=−0.527` (dark energy) off galaxy dynamics | **`[DERIVED]`**, ΛCDM-consistent (a capability, not new physics) |
| dynamical-mass cascade | `M_dyn/M_b∝√E`, `v∝E^{¼}`, `Σ_c∝E`, TF zero-point ∝−logE | **`[DEGENERATE]`** (ΛCDM's apparent a₀ also rises as E) |
| phantom halo, Freeman density, BTFR/Faber–Jackson evolution | all ∝ powers of E(z) | **`[DERIVED]`** but `[DEGENERATE]` |
| GN-z11 (z=10.6) and the compact-galaxy class | g_bar/a₀(z)≈18 → **Newtonian** → no boost; M_dyn/M⋆≈1 observed | **consistent but not a test** (wrong regime; AGN-contaminated) |

---

## Layer 5 — The boundary: what this theory is *not*, stated plainly

The honest perimeter — the difference between this and the original "452-problem" overreach.

| claim | status |
|---|---|
| Standard-Model constants (α, mₚ/mₑ, sin²θ_W, …) from Z | **`[DEAD]`** — FDR: a 34k-formula search hits an arbitrary O(100) target to 0.004% ~20% of the time; 52/64 old "derivations" contain no Z; a random number does as well as 32π/3. ≈0 bits. |
| the **S8** tension fixed by evolving a₀ | **`[DEAD]`** — forbidden by the theory's own Paper-II `δq⁰⁰=0`: a₀ absent from linear growth ⇒ σ₈ unchanged |
| **galaxy clusters** solved by a density-dependent a₀ | **`[LIMIT]`** — the density form would give the required ~13× in-cluster a₀, **but the tight SPARC RAR excludes the environmental reading** (cluster-fixing smoothing ⇒ ~0.24 dex a₀-scatter vs ≲0.06 observed). `reviews/sparc_environmental_a0_test.py` |
| the **Bullet Cluster** | **`[OPEN]`** — contested in 2026 (QUMOND density-weighting, Hernandez 2026, vs residual papers; my own toy can't certify it). Not a clean falsification, not resolved. |
| the 20.6 Gpc **T³/Z₂ topology** / η-invariant origin of Z | **`[DEAD]`** — category error; S8 truncation failed (7×10⁻⁷%); parity tests null; topology can't set local a₀ by 12–124 orders of magnitude |

---

## The deepest uncertainty — is the foundation even real?

Everything above is conditional on **MOND being a real description of nature**, which is itself
unsettled and under active fire:

- **Wide binaries:** Banik et al. (2024, MNRAS 527, 4573) find Newtonian gravity preferred at 16–19σ;
  Chae (2023) finds the opposite. Systematics-limited, **genuinely unresolved.**
- **a₀ universality:** Rodrigues et al. (2018) reject a universal a₀ at >5σ; McGaugh/Kroupa rebut.
  Contested. *(And note: the environmental-a₀ reading clusters would need — Layer 5 — is in tension
  with the very universality the RAR shows, so the framework cannot have that both ways.)*

**If MOND is not real, the whole spine falls at Layer 0.** A reasonable physicist can currently read
the literature as leaning against it.

---

## The spine in one breath

> Inertia is emergent and Machian `[GROUNDED]`, so the low-acceleration scale is the surface gravity
> of the cosmic free-fall horizon, `a₀=(c/2)√(Gρ)` `[POSIT coefficient]`, which therefore *evolves*,
> `a₀(z)=a₀(0)E(z)` `[DERIVED, the falsifiable core, ~2σ today]`; this is realized covariantly in
> AeST `[DERIVED]` and is provably CMB-safe `[DERIVED]`; its one distinctive signature is a
> redshift-weakening external field effect `[DISTINCTIVE, next-decade test]`; it is a theory of the
> **dark sector only** `[boundary]`, and it stands or falls with the reality of MOND `[OPEN]`.

That is the whole theory, with nothing hidden and no numerology in it. It is smaller than a theory
of everything by exactly the amount the evidence demands — and within that perimeter, it is complete,
coherent, and falsifiable.

---

*Backing code/papers, by layer:* L0 `reviews/emergent_inertia_derivation.py`; L1
`reviews/derive_Z_firstprinciples.py`, `_equipartition_attempt.py`, `_cleanest.py`; L2
`reviews/stresstest_piece3_evolution.py`; L3 `papers/Paper1_*`, `papers/Paper2_*`,
`Zimmerman_Scaling_MOND_2026.tex`; L4 `reviews/jwst_predictions_comprehensive.py`,
`EFE_vs_z_Forecast_2026.tex`, `reviews/more_derivations.py`; L5
`reviews/sparc_environmental_a0_test.py`, `reviews/bullet_qumond_redo.py`,
`reviews/false_discovery_rate.py`. Companion docs: `STATE_OF_THE_FRAMEWORK.md`,
`STATUS_AND_NEXT_STEPS.md`, `COMPLETE_ASSESSMENT.md`.

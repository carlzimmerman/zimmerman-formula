# a₀ Is the Dark-Energy Scale: a MOND–Dark-Energy Unification, and Its Falsifiable Prediction

> **⚠ 2026-06-05 — read with [`A0Z_MUSE_DARK_III_CONFRONTATION.md`](A0Z_MUSE_DARK_III_CONFRONTATION.md).** This
> doc's √ρ_DE *decline* is in tension with MUSE-DARK III's measured rise, but "**failed → revert to rising**" is
> too strong: (1) cite **Ciocan, Bouché et al.** (A&A 709, L16), **not "Mercier et al."** (2) MUSE's rise is
> **ΛCDM-degenerate** (Mayer+2023) and *"faster than H(z)"*, so it does **not** establish a rising *fundamental*
> a₀ — it is non-diagnostic of this framework, not a clean refutation of the √ρ_DE reading. Net grade: the
> declining reading is **WEAKENED & CONTESTED**, survives via the fitted≠fundamental degeneracy (which also
> strips its distinctiveness) — not "failed," and the rising branch is *not* thereby confirmed.

**The session's novel, defensible result, stated as a research program — with its single load-bearing
assumption and its normalization tension named in the first screen, not buried. Carl Zimmerman, June 2026.**

---

## ⚠ SUPERSEDED BY DATA (later in session): the central prediction of this document is refuted

This document's headline — a₀ tracks the dark-energy density, **a₀(z) ∝ √ρ_DE, a mild *decline*** — was tested
against the first multi-point **direct** a₀(z) measurement and **failed**. **MUSE-DARK III** (Ciocan et al.
2026 A&A, arXiv:2604.22613; 79 galaxies, 0.33<z<1.44) measures **a₀(z) = 1.0 + 1.59 z, a₁ = +1.59 ± 0.10 — a₀
*rises* with redshift at ~16σ.** The √ρ_DE reading predicts a₀ ≈ flat (×0.99 at z=1); the data give ×2.6. So the
**event-horizon / declining claim is refuted**, and with it the specific "a₀ = the dark-energy scale, declining"
unification framed here. What survives is weaker and points the other way: a₀ *rises* with z, consistent in
**direction** with the *apparent*-horizon reading a₀ ~ cH(z) (the original framework, which this document had
argued against) — though the rate is ~30% steeper than ∝E(z), so even that is not a clean fit. The
MOND–dark-energy *identification* (a₀ set by the cosmological horizon's surface gravity) may still hold at the
order-of-magnitude level, but the sharp, distinctive, falsifiable form asserted below (√ρ_DE tracking) is
**empirically dead**. See `reviews/project_a0z_muse_test.py` and the correction in `THE_FULL_ANSWER.md`. The
text below is preserved as the record of the claim that the data overturned.

---

## Claim (one paragraph)

The MOND acceleration scale a₀ is the **surface gravity of the de Sitter *event* horizon**, a₀ ~ c√(Λ/3) ~
c√(ρ_DE). This is not the long-noted numerical coincidence (Milgrom) but a **consequence of the microscopic
dual**: the double-scaled SYK model that reproduces de Sitter holography (Narovlansky–Verlinde) is the dual of
the de Sitter *static patch* — bounded by the **event** horizon — so the acceleration scale it sets is the
event-horizon scale, ∝√Λ, not the apparent/Hubble scale ∝H. Consequently **dark matter (as MOND) and dark
energy are one scale**, both fixed by the cosmological horizon. The sharp, novel, parameter-free, falsifiable
consequence: a₀ tracks the dark-energy density, so **a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0))**, with ρ_DE(z) measured
by **DESI**. Galaxy dynamics becomes a dark-energy probe, and the two dark sectors are tied by one number.

## The single assumption and the one tension (named up front — this is "doing it right")

- **The assumption (the wall):** the whole construction rests on **Narovlansky–Verlinde: de Sitter = the DSSYK
  spectral *center* (infinite Boltzmann temperature)**. This underwrites *both* the deep-MOND sign (flat DOS
  only at the center) *and* the coefficient (the freezing happens at the band-edge/center scale). It is the
  *leading* proposal but **unsettled** — Rahman–Susskind and Lin–Susskind actively question the
  infinite-temperature reading (2024–25). If de Sitter = the spectral *edge* (Schwarzian) instead, the
  construction fails. (`reviews/project_the_wall.py`.)
- **The tension (normalization):** the *parameter-free* a₀(0) = cH₀√Ω_Λ/Z with Z=2√(8π/3) gives **0.93×10⁻¹⁰,
  ~22% below** the observed 1.2×10⁻¹⁰ (the apparent-horizon cH₀/Z = 1.12×10⁻¹⁰ is closer, ~7% low). So the
  *absolute value* mildly favors the apparent horizon; the **breakthrough is the a₀(z) *shape*** (dark-energy
  tracking), not the normalization. (`reviews/project_coefficient_event_horizon.py`.)

## What is derived (the chain, this session)

| Step | Result | Status |
|---|---|---|
| deep-MOND **sign + √-law** | DOF freezing on the flat DSSYK chord-vacuum DOS | derived (given N-V) |
| **interpolation shape** | the cumulative chord-vacuum measure | derived, q-independent, fits SPARC to ~6% |
| **a₀ ~ c√(Λ/3)** (the order) | holographic equipartition + flat-DOS freezing | derived — *the coincidence is a consequence* |
| **event horizon, not apparent** | the DSSYK dual is the de Sitter static patch | derived (internal consistency); resolves the rate tension |
| coefficient **Z = 2√(8π/3)** | = the Friedmann factor √(Gρ)↔H (Carl's identity) | demystified — not a free number |
| **prefactor** → s = Z | consistency: DSSYK central DOS = Friedmann factor; needs T_freeze = band edge = **N-V** | reduced to N-V; q* ≈ 0.925 |
| MOND probe | massless ⟹ DSSYK Δ=1; a₀ is **Δ-independent** (universal) | derived |

So everything reduces to the one proposition above. Full chain: `reviews/project_which_horizon_dssyk.py`,
`project_prefactor_freezing_derivation.py`, `project_prefactor_consistency.py`, `project_q_constraints.py`,
`project_delta_q_prefactor.py`, `project_first_principles_fronts.py`, `project_the_wall.py`.

## The novel falsifiable prediction

**a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0))**, with ρ_DE(z) from the DESI DR2 w₀wₐ posterior (`reviews/project_a0_dark_energy_prediction.py`):

| z | event ~√ρ_DE (DESI) | constant | apparent ~E(z) |
|---|---|---|---|
| 0.5 | 1.03 ± 0.02 | 1.00 | 1.32 |
| 1 | 0.99 ± 0.04 | 1.00 | 1.79 |
| 2 | **0.87 ± 0.09** | 1.00 | 3.03 |
| 3 | **0.77 ± 0.12** | 1.00 | 4.57 |

A **mild decline**, parameter-free. Decisive test: a **~5% a₀ measurement at z~2–3** separates it from constant;
it is already *very* distinct from the rising branch (gap 2–4×), which the high-z disks have ruled out.

## The corroboration (this is why it's not just a story)

The revised (event-horizon, declining-a₀) framework is consistent with — and in two cases *favored by* — every
direct data set, where the original *rising* bet was in tension with all of them:
- **High-z disks** (Big Wheel z=3.25, RC100, Milgrom/Genzel z~2): a₀ **not risen**; baryon-dominated. Favors
  declining/constant. (`project_highz_a0_synthesis.py`.)
- **RC100 f_DM(z)** decreasing (0.38→0.27): the declining a₀ predicts it with a *plausible* density evolution;
  the rising a₀ needs an *implausible* 3× density jump. (`project_revised_framework_predictions.py`.)
- **DESI** evolving DE: the *source* of the a₀(z) prediction, and itself the headline cosmology result.

## What would make it a discovery (and what would kill it)

- **Discovery:** a clean, gas-traced, deep-MOND **a₀(z~2–3) to ~5%** matching √ρ_DE(z) (the mild decline) would
  establish a₀ as a dark-energy probe — *unifying the two dark sectors through one measured scale*.
- **Refutation:** a₀(z~2–3) clearly *rising* (apparent horizon) — already disfavored; or a₀ *constant* with DESI
  reverting to Λ; or de Sitter shown to be the spectral *edge* (killing the sign and coefficient at once).

## Provenance (honest attribution)

Emergent gravity / horizon thermodynamics: **Jacobson, Padmanabhan, Verlinde**. The a₀–cosmology link and
"same term": **Milgrom**. The DSSYK = de Sitter dual: **Narovlansky–Verlinde**; the matter element: **Berkooz/
Lin/Okuyama**; the many-temperatures structure: **Rahman–Susskind**. The DESI evolving-DE measurement: **DESI**.
**This framework's specific contributions** are the bridge itself: the deep-MOND *sign* from DSSYK freezing, the
*derived interpolation*, the **event-horizon reading** (a₀ ~ √ρ_DE) that resolves the rate tension, and the
**a₀(z) = √ρ_DE(z) dark-energy-probe prediction**. Everything is "correct **if** Narovlansky–Verlinde is
correct," and that is a falsifiable statement about a specific, active research question — the honest form of a
breakthrough.

*Companions: `TOE_EMERGENT_HORIZON.md` (the broad synthesis), `THE_FULL_ANSWER.md` (calibrated odds),
`TOE_LITERATURE_DOSSIER.md` (sources), and the `reviews/project_*.py` behind every number here.*

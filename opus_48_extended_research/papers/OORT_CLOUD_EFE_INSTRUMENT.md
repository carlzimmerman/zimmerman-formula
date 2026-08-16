# The Oort Cloud as an External-Field-Effect Instrument: a Conditional Joint Signature with Gaia DR4

**Carl P. Zimmerman**, Briar Creek Tech
ORCID 0009-0008-3508-7982
2026-08-16 (v1)

---

## Abstract

Of everything a star owns, only its comet cloud extends into the regime where the acceleration
scale a₀ = κc√(Gρ_Λ) = 9.3619×10⁻¹¹ m s⁻² becomes dynamically relevant: the MOND radius of a
solar-mass star is r_M ≈ 7,960 AU (canonical footing; 7,250 alt), and Oort-cloud comets are stored
at 10³–10⁵ AU. We price this channel honestly, in both directions. **Three results.** (1) At
solar-neighbourhood external fields the external-field effect (EFE) removes almost the entire
deep-MOND zone: the cloud is Newtonian inside ~r_M and *anisotropic quasi-Newtonian* beyond
~0.88 r_M, governed by the same committed response tensor (B_∥ = 1.4732, B_⊥ = 1.2598) as the
hash-frozen Gaia DR4 wide-binary registration. A uniform ν-boost of gravity nearly self-cancels in
comet-injection physics (the energy spike shifts only as G_eff^(1/7), ≈ 6%); **the surviving
signal is directional** — a ~7% aphelion-direction modulation of the spike position and a ~17%
modulation of the injection rate, keyed to the galactic external-field direction. (2) The
*exo*-Oort version of this test — KIC 8462852 ("Tabby's Star") read through its dips — is **dead
by 6.7 orders of magnitude**: the inference chain from dip statistics to gravity leaks a factor
~9×10⁵ of model slack against the ~0.17 signal, priced arrow by arrow. (3) In the full
relativistic completion the extra structure is *silent* at cloud scales (the AeST mass term's
oscillation radius is ≥ 23 kpc at the pinned 𝒬₀ band; the a₀-bump term bounds out at ≥ 280 kpc;
the derived a₀(z) is flat to 5×10⁻⁷ over the injection history) — but the pressure promotion
𝒜(𝒬) = a₀²(𝒬) makes a₀ local, so the comet anisotropy becomes **ν₀-dependent: 16.7% at the
charge floor, 12.1% at the ceiling** (steady-state-continuity reading), co-varying with the DR4
wide-binary γ_v. Constant-a₀ MOND predicts a fixed 17%; this framework predicts a **correlated
pair** — one dimensionless charge moves the comet statistics and the wide-binary boost together.
This note prices a door; it does not claim a detection, and it freezes nothing.

---

## 1. The gravitational geography of a comet cloud

For a star of mass M the framework's transition radius is r_M = √(GM/a₀):

| object | footing | r_M [AU] | EFE-dominated beyond [AU] |
|---|---|---|---|
| Sun | canonical | 7,960 | ~7,000 |
| Sun | alt | 7,250 | ~6,400 |
| KIC 8462852 (1.43 M☉) | canonical | 9,520 | ~8,400 |

Planets, asteroid belts, and Kuiper belts all sit deep inside the Newtonian zone (the framework's
Newtonian residual is e^(−√y): ~10⁻³⁴⁵⁷ at 1 AU). The Oort reservoir straddles r_M — but the
observed solar-neighbourhood external field, x_ext = g_ext/a₀ = 1.9, dominates the internal field
once y_int < y_extN = 1.29, i.e. beyond 0.88 r_M. The isolated deep-MOND zone is a sliver;
what a comet cloud actually experiences outside ~r_M is quasi-Newtonian gravity with the
anisotropic linear-response tensor of the committed AQUAL-EFE solve: an effective coupling
1.4732 G along the external-field direction and 1.2598 G across it.

## 2. The self-cancellation, and the signal that survives

Comet injection is a competition between the star's binding and the galactic tide: the tide walks
perihelia into the planetary loss cone, and the balance sets the observed energy spike of
long-period comets. Both sides of that balance carry the ν-boost, so a *uniform* enhancement
largely cancels: at leading tide-scaling order the spike position shifts only as G_eff^(1/7)
(≈ +6% at ν = 1.4732). What does not cancel is the *anisotropy*: with injection efficiency scaling
as the directional G_eff, the tensor imprints

- a **~7%** modulation of the spike position with aphelion direction (∝ (B_∥/B_⊥)^(3/7)), and
- a **~17%** modulation of the injection rate (∝ B_∥/B_⊥ = 1.169),

organized relative to the galactic external-field direction. Newtonian tide theory already
predicts (and the long-period-comet catalogs show) galactic-latitude structure in aphelia
directions; the framework modifies its *amplitude* by these factors. The 2/7 and 3/7 exponents
are leading-order tide scalings, stated not derived — a named owed item.

## 3. Why the exo version is dead: KIC 8462852, priced arrow by arrow

Tabby's Star's dips, if cometary, sample an exo-Oort cloud — the only way "shadows" ever touch
a₀ physics. The chain, priced:

| inference arrow | model slack |
|---|---|
| dips → comet interpretation (dust family competes; not established) | ×10 |
| dip depth → swarm mass → comet number | ×30 |
| comet rate → injection rate (unknown cloud population N(a)) | ×300 |
| injection rate → cloud dynamics (unknown stellar history/flybys) | ×10 |
| **total slack vs the ~0.17 anisotropy signal** | **~9×10⁵ — 6.7 orders** |

The star's 880-AU companion is itself gravity-boring (y = 117; Newtonian residual ~2×10⁻⁵).
Verdict: dead as a gravity instrument — a dust mystery pointed away from gravity. Any exo-Oort
gravity test inherits this chain; the solar cloud does not.

## 4. The honest cousin: our own Oort spike

The observed long-period-comet energy spike sits at 1/a ≈ (3–5)×10⁻⁵ AU⁻¹ (a ≈ 20,000–33,000 AU),
with hundreds of quality orbits in existing catalogs. At the spike, y_int ≈ 0.16 ≪ y_extN = 1.29:
the physics is EFE-dominated *exactly as in the wide-binary problem*, at ten times the separation.
A comet-aphelia anisotropy analysis is therefore a **free cross-check of the same tensor the DR4
registration tests**, on data that already exist.

## 5. The full-completion layer: what AeST adds and what it silences

Run through the complete action (AeST scaffold with the pressure promotion), every additional
structure is bounded silent at cloud scales: the mass term μ = √(2𝒦₂/(2−K_B))·𝒬₀ has its
oscillation radius r_C = (r_M μ⁻²)^(1/3) ≥ 23 kpc at the pinned 𝒬₀ band; the a₀-bump cluster
response bounds out at ≥ 280 kpc even at gate maximum; the derived a₀(z) is flat to 5×10⁻⁷ over
the Gyr injection history. The kernel-level prediction of §2 therefore *is* the framework's
prediction. The completion adds exactly one thing: because 𝒜(𝒬) = a₀²(𝒬) is local, the
solar-circle charge flow suppresses the local a₀ (steady-state-continuity reading), and the
anisotropy becomes charge-dependent:

| ν₀ (the framework's one free dimensionless charge) | local a₀ ratio S | rate anisotropy |
|---|---|---|
| floor (2.14×10⁻⁵) | 0.977 | **16.7%** |
| ceiling (1.77×10⁻⁴) | 0.599 | **12.1%** |

The same suppression moves the DR4 wide-binary γ_v (the registered band's conditional ν₀-meter).
**The framework therefore predicts a correlated pair**: the comet anisotropy and the wide-binary
boost move together under one parameter, in a computable ratio. Constant-a₀ MOND predicts a fixed
17% with no partner observable. That correlation — not either number alone — is the signature
unique to this framework.

## 6. What this does not establish

- **No detection is claimed and nothing is frozen.** This note prices a channel; the DR4
  registration is untouched and this analysis is not part of it.
- The tide-scaling exponents (2/7, 3/7) are leading-order and stated, not derived; the honest
  next step derives them and the loss-cone geometry properly.
- The known Newtonian-tide anisotropy must be modeled and subtracted before a 7–17% modification
  of its amplitude is testable; whether ~10²–10³ catalog orbits give the statistical power is an
  owed analysis, not assumed.
- Prior art exists on Milgromian Oort-cloud dynamics (Paučo & Klačka 2016, Sedna and the comet
  cloud in Milgromian dynamics) and is flagged LITERATURE-UNVERIFIED here: it must be read and
  credited in detail before any continuation.
- κ = ½ remains fitted, not derived (measured 0.551 ± 0.043); both footings are carried in §1.

## Reproducibility

All numbers from one committed script at
<https://github.com/carlzimmerman/zimmerman-formula>:

- `real_research/tabby_exo_oort_a0_2026.py` — 13 checks: the geography (both footings), the
  self-cancellation and anisotropy scalings, the Tabby chain pricing, the solar-spike regime,
  and the full-AeST layer (mass-term, bump, a₀(z) bounds; the ν₀ co-variance table).
- `prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py` — the committed response tensor.
- `nbody_2026/stage61_drain_reading_fork_2026.py` — the continuity reading and the local-a₀
  suppression behind §5.

**Prior art and attribution.** AeST is Skordis & Złośnik, PRL **127** 161302; the kernel is
Milgrom & Sanders 2008, ApJ **678** 131, Eq. (13) at α = ½; Oort-cloud injection theory is
classical (Oort 1950; Heisler & Tremaine 1986); Milgromian Oort-cloud dynamics has prior art in
Paučo & Klačka 2016 (to be verified and credited in detail). The framework's contribution is the
a₀ normalisation, the local-a₀ structure, the committed EFE tensor, and the ν₀-correlated-pair
prediction of §5.

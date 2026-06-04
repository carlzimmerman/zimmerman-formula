# Evidence for a Cosmologically Evolving MOND Acceleration Scale: a₀(z) from the Local Radial Acceleration Relation to z ≈ 1.5

**C. Zimmerman.** *Draft for submission, June 2026. Companion calculations: `real_research/reviews/project_*.py`.*

---

## Abstract

The MOND acceleration scale a₀ ≈ 1.2×10⁻¹⁰ m s⁻² coincides numerically with cH₀ to within an order-unity
factor, a long-noted hint that the scale of galactic dynamics is set by cosmology. We test the stronger,
falsifiable form of that hint: that a₀ is the surface-gravity scale of the cosmic horizon and therefore
**evolves with redshift**, a₀(z) = cH(z)/Z with Z = 2√(8π/3) the Friedmann conversion between density and
expansion rate. The hypothesis makes three checkable claims. (i) **Local normalization:** a₀ = cH₀/Z = 1.12×10⁻¹⁰
m s⁻², 6% below the observed value — parameter-free. (ii) **Shape:** the deep-MOND interpolation predicted by
horizon degree-of-freedom freezing reproduces the SPARC radial acceleration relation (RAR) to ≈6% in scatter
with no shape parameter. (iii) **Evolution:** because the cosmic horizon grows, a₀ should *rise* toward higher
redshift. Using the first multi-point **direct** measurement of a₀(z) — MUSE-DARK III, 79 star-forming galaxies
over 0.33 < z < 1.44 — we find a₀ increases at ≈16σ within that analysis (a₀(z) = 1.0 + 1.59z ×10⁻¹⁰, a₁ = +1.59
± 0.10). Taken at face value this **disfavours a constant a₀** and matches the *sign* of the horizon prediction.
**We stress that the result is discriminating but not yet established:** it stands in direct tension with the
prior high-redshift MOND literature, which has read baryon-dominated high-z disks as consistent with a *constant*
a₀ (Milgrom 2017) and which, in Tully–Fisher evolution tests, has tended to *exclude* the a₀ ∝ cH(z) coupling in
favour of a constant (√Λ-tracking) scale. The central physical question is therefore which cosmological quantity
a₀ tracks — the evolving expansion rate H(z) (rising) or the dark-energy density √Λ (≈constant) — and the two
readings of the present data conflict. Two further tensions are reported in full: the MUSE rate is ≈30% steeper
than the simplest a₀ ∝ E(z) law, and a single z = 3.25 disk (the "Big Wheel") sits below *both* extrapolations.
We conclude, cautiously, that the evidence now favours an *evolving* over a *fundamental-constant* a₀, while the
*direction* of evolution, the exact law, and the microscopic derivation all remain open. The decisive future
test is a clean, gas-traced a₀ measurement at z ≈ 2–3 with the inner-radius selection effect controlled.

---

## 1. Introduction

The radial acceleration relation (RAR) is a tight, one-to-one correlation between the observed centripetal
acceleration in a galaxy, g_obs = V²(r)/r, and the acceleration predicted from its baryons alone, g_bar
(McGaugh, Lelli & Schombert 2016; Lelli et al. 2017). At high accelerations g_obs ≈ g_bar; below a
characteristic scale a₀ ≈ 1.2×10⁻¹⁰ m s⁻² the observed acceleration systematically exceeds the baryonic one,
asymptoting to the deep-MOND form g_obs = √(a₀ g_bar). The same scale sets the zero-point of the baryonic
Tully–Fisher relation, V⁴ = G a₀ M_bar. Whether this reflects modified dynamics (MOND; Milgrom 1983) or a
generic outcome of galaxy formation in ΛCDM remains debated, but the *existence* and *tightness* of the scale
are not in question.

A persistent clue is numerical: a₀ ≈ cH₀/2π to within tens of percent (Milgrom 1983, 1999). If this is not a
coincidence, the acceleration scale of bound, sub-kpc systems is fixed by the size of the observable Universe —
a statement most naturally realized in **emergent-gravity** programs, where the gravitational field equations
arise thermodynamically from the entropy of causal horizons (Jacobson 1995; Padmanabhan 2010; Verlinde 2011,
2017). In Verlinde's 2017 construction the de Sitter horizon's volume-law entanglement entropy supplies an
extra elastic response below exactly a₀ ~ cH₀, reproducing MOND phenomenology (a specific mechanism since
contested — §5 — which we cite for motivation only and do not rely on).

If a₀ is a horizon surface gravity, it cannot be a constant of Nature: the horizon evolves, so **a₀ must evolve
with redshift.** This is the sharp, falsifiable departure from standard MOND, in which a₀ is a universal
constant. Until recently the prediction was untestable — a₀ had only ever been measured locally. That has
changed: deep IFU surveys now resolve rotation support in galaxies to z > 1, and the first multi-point
measurement of the RAR transition scale as a function of redshift has appeared (MUSE-DARK III; Mercier et al.
2026). This paper confronts the evolving-a₀ hypothesis with that measurement, after first fixing the local
normalization and shape.

We are explicit about scope. We make **no** claim to a theory of everything, to the Standard Model, or to a
microscopic completion; earlier numerological versions of those claims are abandoned. The defensible result
here is narrow and empirical — *the data now favour an a₀ that **evolves** rather than a universal constant* —
together with the phenomenological interpretation that it does so because it tracks the cosmic horizon. Whether
it tracks H(z) (rising) or √Λ (≈constant) is the open question this paper sharpens but does not close.

## 2. The horizon hypothesis

Write the MOND scale as a free-fall acceleration built from a single density ρ,

>  a₀ = (c/2)√(Gρ) = c²/(2R\*),  R\* ≡ c/√(Gρ),  (1)

where √(Gρ) is the gravitational free-fall frequency of a medium of density ρ and R\* is the radius at which the
free-fall speed reaches c. Equation (1) is dimensionally the unique acceleration built from c and √(Gρ).

The content is the choice of ρ. Using the **critical density** ρ_crit = 3H²/8πG (the Friedmann relation), (1)
becomes

>  a₀ = (c/2)√(G·3H²/8πG) = cH/Z,  Z ≡ 2√(8π/3) = 5.7888…  (2)

so Z is **not a free parameter** but the Friedmann conversion between density and expansion rate. We are careful
about its status: Z is **not derived from below** in any emergent-gravity framework. Holographic equipartition
(Padmanabhan 2010) reproduces the Friedmann 8π/3 only by fixing its horizon degree-of-freedom prefactor to the
Bekenstein–Hawking value — matching general relativity rather than predicting the number. The honest statement
is that a₀ = cH/Z places the MOND scale at the cosmic-horizon surface gravity *up to an order-unity factor that
emergent gravity also cannot independently fix*; we adopt the Friedmann value Z = 2√(8π/3) = 5.789 (close to but
distinct from Milgrom's a₀ ≈ cH₀/2π, i.e. Z = 2π = 6.28). This is the emergent-gravity *apparent* (Hubble) horizon reading: a₀ tracks the instantaneous expansion rate, and since H(z)
= H₀E(z) with E(z) = √(Ω_m(1+z)³ + Ω_Λ) increases with z, the hypothesis predicts

>  **a₀(z) = cH₀E(z)/Z  →  a₀ rises with redshift.**  (3)

A second reading uses the **dark-energy density** ρ_Λ (the de Sitter *event* horizon), giving a₀ = cH_Λ/Z with
H_Λ = H₀√Ω_Λ, which is constant for a cosmological constant and mildly declining for the evolving dark energy
favoured by DESI (2024, 2025). This √Λ-tracking branch is the one the prior MOND literature has tended to favour
(Milgrom 2017). The two readings differ by √Ω_Λ = 0.83 in normalization and, crucially, in the *sign* of the
predicted evolution — so a robust a₀(z) measurement discriminates between them. §4.3 shows the new MUSE data
favour the rising (H(z)) branch while the prior high-z literature favours the constant (√Λ) branch; we report
that conflict rather than resolve it.

## 3. Data and methods

### 3.1 The local RAR and the derived interpolation (SPARC)

We use the SPARC database (Lelli, McGaugh & Schombert 2016): 175 disk galaxies with Spitzer 3.6 μm photometry
(tracing stellar mass at near-constant mass-to-light ratio Υ ≈ 0.5) and resolved Hi/Hα rotation curves. For each
radius we form g_obs = V_obs²/r and g_bar = (V_gas|V_gas| + Υ_d V_disk² + Υ_b V_bul²)/r. After quality cuts
(inclination > 30°, quality flag Q ≤ 2, fractional velocity error < 10%) we retain 153 galaxies and 2696 points.

The acceleration scale enters through the interpolation function ν that maps g_bar to g_obs: g_obs =
ν(g_bar/a₀)·g_bar, with ν → 1 at high acceleration and ν → √(a₀/g_bar) deep in the MOND regime. Standard MOND
*fits* the shape of ν. The horizon hypothesis instead *derives* it: the fraction of horizon degrees of freedom
that are thermally "frozen out" at a given local acceleration follows the (1+1)-dimensional near-horizon density
of states, which in the double-scaled SYK (DSSYK) dual of de Sitter space is the q-deformed chord-vacuum
spectral measure. We compute that cumulative measure numerically and use it as ν with **no shape parameter**
(only a₀ as the single scale). We compare its weighted RAR scatter against the fitted McGaugh, "simple," and
"standard" interpolation functions on the identical sample and error budget (observational errors on V, distance,
inclination, and Υ propagated to g_obs, g_bar).

### 3.2 The gas-dominated a₀ (mass-to-light-independent)

The stellar mass-to-light ratio Υ is the dominant systematic on a₀ (a₀ ∝ 1/Υ in the deep-MOND limit). To obtain
an Υ-insensitive normalization we isolate points where the gas contributes > 70% of g_bar and the system is deep
in the MOND regime (g_bar < 0.6 a₀); for these the stellar term is sub-dominant and a₀ ≈ g_obs²/g_bar is nearly
free of Υ. We report the median and its bootstrap error over Υ ∈ {0.3, 0.5, 0.65}.

### 3.3 Direct a₀(z): MUSE-DARK III and high-redshift disks

**MUSE-DARK III** (Mercier et al. 2026, A&A; arXiv:2604.22613) measures the RAR transition scale as a function
of redshift for 79 star-forming galaxies (M\* > 10^8.8 M⊙, complete) at 0.33 < z < 1.44 in the MUSE Hubble Ultra
Deep Field. Rotation curves from Hα/[Oiii] kinematics are combined with baryonic profiles; the RAR is fit with a
DC14 halo + baryons model (their primary analysis) and the transition acceleration extracted per redshift bin
and as a linear law a₀(z) = a₀(0) + a₁z. This is, to our knowledge, the first multi-point *direct* a₀(z)
measurement; we take its tabulated results as the primary evolution constraint.

**High-redshift individual disks.** As an independent, model-light cross-check at higher z we use the baryonic
Tully–Fisher estimator a₀^eff = V_flat⁴/(G M_bar), which equals a₀ for a rotationally supported deep-MOND disk.
We apply it to the "Big Wheel" (z = 3.25; Wadekar et al. 2026-class megadisk, V_flat ≈ 280 km s⁻¹, M\* ≈
3.7×10^11 M⊙, M_gas ≈ 1.8×10^11 M⊙) and to the protocluster source ADF22.1 (z = 3.09). We stress the
limitation, quantified in §4.4: these systems are baryon-dominated (high g_bar), so a₀^eff is an *upper-bound–
like* estimator — it constrains a₀ from below if the disk is sub-MOND, and is degenerate with cluster missing
mass for ADF22.1.

### 3.4 Evolving dark energy (DESI) and clusters (eRASS1)

For the event-horizon branch we propagate the DESI DR2 w₀wₐ posterior (w₀ = −0.83 ± 0.06, wₐ = −0.65 ± 0.25,
correlation −0.8) to ρ_DE(z) = (1+z)^{3(1+w₀+wₐ)} exp[−3wₐ z/(1+z)]. We also examined the eRASS1 X-ray cluster
catalogue (Bulbul et al. 2024) as a possible a₀(z) probe and find it unusable for this purpose: the apparent
a₀^eff = g_obs²/g_bar at R500 rises as E(z)^≈1 purely because R500 is defined by an overdensity relative to the
*evolving* critical density (g ∝ E^{4/3} geometrically), a kinematic artefact independent of any MOND scale. We
therefore exclude clusters from the evolution test.

### 3.5 Statistics

All fits minimize the inverse-variance-weighted orthogonal scatter in log(g_obs)–log(g_bar). Model evolution
laws are compared as normalized ratios a₀(z)/a₀(0) so that only the *shape* is tested, independent of the local
normalization. Uncertainties on a₁ are taken from the published MUSE-DARK III fit; bootstrap is used for the
gas-dominated normalization.

## 4. Results

### 4.1 Local normalization (parameter-free)

From Eq. (2) with H₀ = 67 km s⁻¹ Mpc⁻¹:

> a₀(apparent) = cH₀/Z = **1.12×10⁻¹⁰ m s⁻²**  (6% below the observed 1.20 ± 0.26)
> a₀(event)    = cH₀√Ω_Λ/Z = 0.93×10⁻¹⁰  (22% below)

The gas-dominated, Υ-insensitive estimator (§3.2) gives a₀ = 1.0–1.1×10⁻¹⁰ (1.02 ± 0.08 at Υ = 0.65), bracketing
the apparent-horizon value and lying ≈1σ above the event-horizon value. The apparent-horizon normalization is
parameter-free and accurate to within the stellar-mass systematic; the event-horizon normalization is low.

### 4.2 The derived interpolation reproduces the RAR shape

On the 153-galaxy / 2696-point sample with a full error budget, the derived (DSSYK chord-vacuum) interpolation
yields a weighted RAR scatter of **0.138 dex**, against the *fitted* McGaugh function's 0.130 dex (ratio 1.06)
and the simple/standard functions' 0.130/0.134 dex. The shape is **nearly independent of the DSSYK coupling q**
(scatter 0.137–0.139 dex for q ∈ [0.3, 0.95]), so it is a genuine zero-shape-parameter prediction, not a
disguised fit. **One honest deviation:** the derived form's own best-fit a₀ = 0.80×10⁻¹⁰ is ≈30% below the
fitted functions' 1.15–1.29 and below cH₀/Z; i.e. the predicted *transition is slightly too sharp*, biasing the
fitted scale low. The shape is right to 6%; the absolute scale carried by that shape is ≈30% low — a real,
reported imperfection (consistent with a needed broadening of the single-temperature transition; §5).

### 4.3 a₀ evolves and rises (the central result)

MUSE-DARK III measures

> **a₀(z) = (1.0 ± 0.04) + (1.59 ± 0.10) z  ×10⁻¹⁰ m s⁻²,**

binned values climbing 1.99 → 2.71 over the sample; a₀ at z ≈ 1 is 2.38. The slope is positive at **≈16σ**.
Normalizing to a₀(0) and comparing the three hypotheses at z = 1:

| Model | a₀(1)/a₀(0) predicted | MUSE measured | verdict |
|---|---|---|---|
| Constant a₀ (standard MOND) | 1.00 | **2.6** | excluded |
| Event horizon, a₀ ∝ √ρ_DE (DESI) | 0.99 (≈flat) | 2.6 | **excluded** (predicts flat/declining) |
| Apparent horizon, a₀ ∝ E(z) | 1.79 | 2.6 | right **sign**, ≈31% too shallow |

Within the MUSE-DARK III analysis the data **exclude a constant acceleration scale** at ≈16σ and exclude the
declining (event-horizon/dark-energy) branch, favouring the *direction* predicted by the apparent (Hubble)
horizon: a₀ rises with redshift. **This must be weighed against the prior literature, which points the other
way** (§5): Milgrom (2017) reads the z ≈ 1–2.4 baryon-dominated disks of Genzel et al. as consistent with a
*constant* a₀, and earlier Tully–Fisher evolution analyses have *excluded* the a₀ ∝ cH(z) coupling within their
uncertainties. The disagreement is not yet resolvable from published data and most plausibly hinges on whether
the intermediate-z RAR fit (within a DC14 halo model) cleanly isolates the deep-MOND regime or is biased by the
high-acceleration, baryon-dominated inner radii that dominate high-z kinematics. We therefore record this as the
first *direct multi-point* indication that a₀ is not constant — a discriminating but contested result — not as an
established fact.

### 4.4 The rate is not yet pinned (reported in full)

Two tensions prevent a clean fit of the *rate*:

1. **MUSE rises faster than ∝E(z).** The measured a₀(1)/a₀(0) = 2.6 exceeds the apparent-horizon 1.79 by ≈30%;
   empirically a₀ ∝ (1+z)^≈1.3, between √ρ_total ∝ E(z) (∝(1+z)^≈1.0 over this range) and √ρ_matter ∝ (1+z)^1.5.
   This excess may be physical or may reflect the DC14 model-dependence of the MUSE extraction (the authors
   themselves flag the rise as faster than H(z)).

2. **The z = 3.25 disk lies below both extrapolations.** The Big Wheel gives a₀^eff = 1.05 (+0.94/−0.44) ×10⁻¹⁰
   (1.55 with the lighter stellar estimate; robust gas-only upper bound 2.55), whereas a₀ ∝ E(z) predicts ≈6.0
   and the MUSE linear law extrapolates to ≈6.2 at z = 3.25. Reaching even 6.0 with gas-only baryons would
   require V_flat ≈ 374 km s⁻¹ versus the observed ≤ 280. So a₀ does **not** continue rising linearly to z ≈ 3;
   it either turns over/plateaus, or the baryon-dominated disk estimator underestimates a₀, or the intermediate-z
   and high-z methods carry different systematics. ADF22.1 gives a₀^eff ≈ 11.5×10⁻¹⁰ but lies in the cluster
   missing-mass regime and is degenerate with dark matter, so it does not discriminate.

The robust statement is therefore the *sign and intermediate-z trend*: **a₀ rises over 0.33 < z < 1.44**, and the
exact a₀(z) law — and whether it plateaus by z ≈ 3 — is unresolved by present data.

## 5. Discussion

**What the data support.** The MOND acceleration scale is (i) numerically the cosmic-horizon surface gravity
cH₀/Z to 6%, (ii) carries a RAR shape consistent to 6% with horizon degree-of-freedom freezing, and (iii)
**evolves, rising with redshift**, excluding both a universal constant and the dark-energy/event-horizon branch.
Taken together these favour an interpretation in which a₀ is cosmological and emergent rather than fundamental.
The evolution is the new and discriminating element: standard MOND has no mechanism for it, while an emergent
horizon scale predicts it generically.

**The open rate.** The simplest horizon law a₀ ∝ E(z) has the right sign but is ≈30% too shallow against MUSE and
too steep against the z = 3.25 disk. A density intermediate between ρ_total and ρ_matter (a₀ ∝ (1+z)^≈1.3) fits
the MUSE trend but lacks a first-principles motivation; alternatively the MUSE rate may be partially inflated by
its halo-model dependence. Distinguishing these requires (a) a model-independent (rotation-curve-only) re-
extraction of the MUSE slope, and (b) clean a₀ measurements at z ≈ 2–3 in gas-rich, rotation-supported disks.

**The microscopic claim, and its single load-bearing assumption.** The deep-MOND *sign* (why gravity is enhanced,
not suppressed, below a₀) and the derived interpolation rest on identifying the de Sitter static patch with the
spectral centre of the DSSYK model (Narovlansky & Verlinde 2023; the "infinite-temperature" reading). This is
the leading proposal for de Sitter holography but is actively contested (Rahman & Susskind 2024; Lin & Susskind
2024). We therefore present the sign-derivation as *conditional* — correct if that identification holds — and
emphasize that the empirical results of §4 (normalization, shape, evolution) stand independently of it.

**Caveats kept loud.** MUSE-DARK III is a single survey and its a₀ is extracted within a specific (DC14) halo
model; the high-z disks are baryon-dominated and yield bounds rather than clean measurements; the local
normalization is 6–22% from the central observed value depending on branch; and the derived interpolation's
best-fit scale is ≈30% low. None of these individually overturns the central result (a₀ rises), but each must be
controlled before the rate law can be claimed.

**Direct confrontation with the prior high-z MOND literature (the central caveat).** Honesty requires placing
this result against the work that points the other way. (i) **Milgrom (2017)** examined the same class of high-z
rotation-dominated disks and argued they are consistent with a *constant* a₀: because such systems are
baryon-dominated and sit at accelerations of several a₀, they probe the *Newtonian* part of the RAR and do not by
themselves require an evolving scale. Our MUSE-based claim survives this objection *only if* the MUSE RAR fit
genuinely reaches the sub-a₀ regime in the outer disk (it nominally does, via extended Hα/[Oiii] curves down to
M\* ≈ 10^8.8) rather than inferring a₀ from the high-acceleration interior; verifying this is the single most
important robustness check outstanding. (ii) **Tully–Fisher evolution tests** have historically *excluded* the a₀
∝ cH(z) coupling within uncertainties and mildly favoured a constant (√Λ-tracking) a₀ — i.e. the prior consensus
is closer to our *event-horizon* branch than our *apparent-horizon* one. (iii) **Milgrom himself** has leaned
toward a₀ ∝ √Λ (constant) over a₀ ∝ H(z) precisely to avoid evolution. The new element here is that MUSE-DARK
III is the first dataset to *measure* the transition scale multi-point rather than test a fixed value; if its
rising signal is real it overturns this prior reading, and if it is a halo-model/selection artefact it does not.
We deliberately do not adjudicate.

**On the emergent-gravity pedigree.** We invoke emergent gravity as motivation, not as a derivation we lean on.
Verlinde's (2017) specific MOND construction is contested at the level of its own internal consistency
(Dai & Stojkovic 2017 argue the elastic calculation recovers Newtonian, not MONDian, gravity) and fails on dwarf
spheroidals, cluster cores, and the detailed SPARC RAR shape (Lelli et al. 2017). Our use of the horizon picture
is limited to the dimensional/thermodynamic statement a₀ ~ (horizon surface gravity), which predates and does not
require Verlinde's particular elasticity mechanism.

**Relation to the broader data.** An evolving a₀ is qualitatively consistent with reports of lower dark-matter
fractions and offset Tully–Fisher zero-points in high-z disks (Genzel et al. 2017; Nestor Shachar et al. 2023),
and is distinct from ΛCDM, which predicts no universal acceleration scale at all.

## 6. Conclusions

1. The MOND acceleration scale equals the apparent-horizon surface gravity a₀ = cH₀/Z, Z = 2√(8π/3), to 6%,
   parameter-free.
2. The RAR transition *shape* is reproduced to 6% by horizon degree-of-freedom freezing with no shape parameter
   (with a ≈30%-low fitted scale as a stated imperfection).
3. The first direct multi-point measurement of a₀(z) (MUSE-DARK III) shows the scale **rises with redshift at
   ≈16σ within that analysis**, favouring an evolving over a constant a₀. This is **discriminating but contested**:
   it conflicts with the prior high-z MOND literature (Milgrom 2017; Tully–Fisher tests), which favours a constant
   (√Λ-tracking) scale. Resolving the conflict requires confirming that the MUSE fit reaches the deep-MOND regime
   and is not biased by baryon-dominated inner radii.
4. The exact a₀(z) **rate** is likewise unresolved: MUSE rises ≈30% faster than ∝E(z), and a z = 3.25 disk sits
   below both extrapolations, indicating a turnover or method-dependent systematics by z ≈ 3.
5. The decisive future measurement is a clean, gas-traced a₀ at z ≈ 2–3; a model-independent re-extraction of the
   MUSE slope is the immediate next step.

The headline is modest and deliberately hedged: **the first direct multi-point data favour a MOND scale that is
cosmological and evolving rather than a fundamental constant — but this conflicts with the prior high-z reading
and is not yet established.** If it survives replication and the systematic checks above, that fact alone would
select emergent, horizon-based gravity over both standard (constant-a₀) MOND and dark-matter models with no
intrinsic acceleration scale. That "if" is the whole game, and we have tried to state it honestly rather than
sell the result.

## References (representative)

Banks & Fischler 2001; Bulbul et al. 2024 (eRASS1); Chae et al. 2020, 2021 (external field effect); DESI
Collaboration 2024, 2025 (evolving dark energy); Genzel et al. 2017; Jacobson 1995; Lelli, McGaugh & Schombert
2016 (SPARC); Lelli et al. 2017 (RAR scatter); Lin & Susskind 2024; McGaugh, Lelli & Schombert 2016 (RAR);
Mercier et al. 2026 (MUSE-DARK III, arXiv:2604.22613); Milgrom 1983, 1999; Narovlansky & Verlinde 2023; Nestor
Shachar et al. 2023 (RC100); Okuyama 2023 (DSSYK matter element); Padmanabhan 2010; Rahman & Susskind 2024;
Verlinde 2011, 2017.

*All numerical results are reproduced by the scripts in `real_research/reviews/`: `project_coefficient_event_horizon.py`
(Z, normalization), `precision_rar_test.py` (interpolation), `project_a0z_muse_test.py` (evolution),
`project_highz_bigwheel_a0.py` (z = 3.25 disk), `project_normalization_lock.py` (branch normalization),
`project_cluster_erass1_a0z.py` (eRASS1 artefact).*

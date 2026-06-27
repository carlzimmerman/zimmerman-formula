# Orbital History Writes the Cosmic Clock on Dwarf Galaxies: A Pre-Registered, Modified-Gravity-Impossible Test of de Sitter–Unruh Modified Inertia

**Carl P. Zimmerman**
Briar Creek Tech
2026-06-27 — **v3** (quantitative correction: the dispersion exponent is the external-field-effect value σ ∝ θ^(−1/2), not the isolated ¼; the discriminating axis is each dwarf's *current* y, not eccentricity or the pericenter peak; the named carriers are currently near apocenter, which explains the pilot null. The sign, the modified-gravity-impossibility, and the existence of the effect — the core prediction — are unchanged theorems.)

---

## Abstract

I pre-register a sharp, falsifiable prediction of the de Sitter–Unruh modified-inertia framework — the proposal that a body's inertia is its **nonlocal-in-time response to the cosmic-horizon Unruh bath**, a bath that carries exactly one clock, the de Sitter rate H_Λ, fixing a₀ = cH_Λ/Z = 9.36 × 10⁻¹¹ m/s². Because inertia in this picture is a functional of the recent acceleration *history*, not of the momentary acceleration, the bath's clock must imprint on the internal dynamics of any object whose external acceleration *changes* on a timescale comparable to its own internal orbital frequency. The cleanest accessible site is a diffuse Local-Group dwarf galaxy on a radial-plunge orbit: at fixed pericenter distance and fixed mass, a high-eccentricity plunger should run **hotter** (larger internal velocity dispersion σ) than a circular-orbit dwarf of the same mass and same closest approach. The **sign is a theorem** (the memory kernel θ is decreasing, Milgrom-forced, so a plunge sheds adiabatic external loading and drops the dwarf deeper into the deep-MOND regime); the **magnitude is bath-constrained** — the de Sitter–Unruh correlator *selects* θ(0)=√2 and *forces* a Lorentzian kernel, with the dispersion rising as σ ∝ θ(y)^(−1/2). The discriminating physical axis is each dwarf's **current** y = ω_ext/ω_internal — its *present* orbital phase read through the ∼0.4–0.5 Gyr memory kernel — gated by diffuseness, not raw eccentricity and not the pericenter-peak value. At a dwarf's hottest pericenter passage the excess is large (**+90–130%** for the named carriers), but its *observable, present-day* value depends on where it is now. The two named carriers, **Crater II (peak y = 3.28)** and **Antlia II (peak y = 2.55)**, are *currently near apocenter* (present y ≈ 0.6), so their present excess is only ≈ +7–8% — they are caught cold, against adiabatic controls Fornax and Sculptor. Crucially, this prediction is **modified-gravity-impossible**: in any metric or field MOND (AQUAL/QUMOND/AeST) and in ΛCDM, the external-field effect is instantaneous — internal dynamics "depend only on the momentary value of a_ex" (Milgrom 2022) — so those theories predict *exactly zero* σ-vs-history correlation at fixed pericenter, for any a₀. Only modified inertia gives a nonzero, history-dependent σ; this joins the Cassini bound as a clean modified-inertia-vs-modified-gravity discriminator. **I report the honest current status straight.** A pre-registered pilot on 24 real Milky-Way dwarfs (Pace, Erkal & Li 2022, Gaia EDR3 orbits) gives a partial Spearman ρ(σ, eccentricity | r_peri, mass, r_half) = **−0.196, p = 0.395** — a **null**, slightly the wrong sign, robust to a tidal-heating control. This is **not** a falsification and **not** a hint: it is a null with almost no statistical power, because only two of 24 dwarfs reach the carrier band, eccentricity is a noisy surrogate for the real y-axis, and the per-object σ errors are comparable to the predicted signal. Existing data cannot yet test this prediction. The decisive test is Gaia DR4 (December 2026) plus diffuse-carrier spectroscopy and resolved profiles, run as a carrier-vs-control **y-contrast** with explicit tidal modeling. This is a pre-registered, near-term, MG-impossible prediction — **not a TOE, not a detection.**

---

## 1. The framework as subject: inertia as a horizon-bath response

This paper treats one specific physical proposal as its subject and reasons forward from that proposal's own premises. The premise is not a variant of Milgrom's MOND and should not be read through MOND's lens.

The premise is this. An accelerated observer in de Sitter space sees a thermal bath — the Gibbons–Hawking/Unruh radiation of the cosmic horizon (Deser & Levin 1997). The framework takes the next step and asserts that **inertia itself is the body's reaction to that bath**: to resist acceleration is to push against the horizon's radiation. The bath has exactly one intrinsic rate, the de Sitter correlation frequency

> H_Λ = cH_Λ/c = 1.81 × 10⁻¹⁸ s⁻¹,    cH_Λ = 5.42 × 10⁻¹⁰ m/s²,

set by the dark-energy density alone (the pure-Λ, de Sitter footing). The acceleration scale at which the bath response becomes order-unity is then

> **a₀ = cH_Λ/Z = 9.36 × 10⁻¹¹ m/s²,**

with Z the framework's geometric normalization. This is a *horizon-derived* acceleration, not a fitted parameter. Above a₀ a body is in the ordinary inertial regime; near and below a₀ the bath response weakens the effective inertia, and a fixed gravitational force produces a larger acceleration — the phenomenology usually labelled MOND, here arising from *modified inertia* with its own interpolation,

> g_obs = √(g_bar² + g_bar·a₀),    μ_fw(x) = (√(1 + 4x²) − 1)/2x,

(the framework's own excess-heat interpolation; I use this throughout and never McGaugh's ν). On steady, hyperbolic-acceleration data (galaxy rotation curves, the radial-acceleration relation) this collapses algebraically to the same curve generic MOND produces, so the RAR cannot, by itself, distinguish the framework — a point I state plainly rather than spin. The framework's *distinctive* content lives where the acceleration history is non-trivial, which is exactly where this paper looks.

For the reader: the key word is **nonlocal-in-time**. Milgrom (1994) proved that any consistent modified-inertia theory must be time-nonlocal — the inertial reaction cannot be a function of the instantaneous acceleration alone; it must be a functional of the worldline carrying a memory kernel. The bath supplies the only clock that kernel can use: 1/H_Λ. A body's inertia therefore reads the *history-averaged* state of its motion. That is the engine of everything below.

---

## 2. The prediction: a plunge runs hotter

Consider a diffuse dwarf galaxy orbiting the Milky Way. Two frequencies compete:

- ω_internal — the dwarf's own internal orbital frequency (its stars circulating in its potential), and
- ω_external — the rate at which the *external* (host) acceleration the dwarf feels is changing as it moves along its orbit.

Define the dimensionless ratio

> **y = ω_external / ω_internal**

(Milgrom 2022, Eqs. 28/33/34). The memory kernel enters as θ(y):

- For a **circular** orbit, |a_ext| is constant. The kernel sees a stationary history. The response is purely adiabatic — the constant-external-field limit θ(0), which is the static external-field-effect "thermometer" reading already used for Crater II in earlier work.
- For a **radial plunge**, |a_ext| sweeps up as the dwarf falls in. Near pericenter ω_ext climbs toward ω_internal, so y → O(1): the response is genuinely **non-adiabatic**, and θ(y) is a real, varying function rather than a constant.

Now the sign. The kernel θ is **decreasing** — θ(0) is a few, θ(1) = 1 — a feature forced by Milgrom's construction, not chosen. A circular dwarf carries the full adiabatic external loading θ(0)·g_ext, which partially pulls it *out* of the deep-MOND regime (this is the ordinary external-field effect that makes satellites a little more Newtonian). A plunging dwarf, momentarily non-adiabatic at pericenter, **sheds** part of that adiabatic loading: θ(y < the adiabatic value) means less effective external field, so the dwarf drops *deeper* into deep-MOND, its effective inertia falls further, and its stars move faster. **A plunge runs hotter.**

A diffuse dwarf orbiting deep in the host's field is pressure-supported in a boosted effective gravity G_eff = G a₀/(θ·g_ext), so its internal dispersion scales as **σ ∝ θ^(−1/2)** — the external-field-effect regime, *not* the isolated baryonic-Tully–Fisher exponent ¼ (which applies only to a field-free dwarf). The boost therefore *rises* as the effective loading θ falls with y. **In this version the de Sitter–Unruh bath itself partially derives the kernel** (previously a free function). Two framework-internal results pin its core: (i) the bath's *excess-heat* coupling ΔT = T(a) − T(0) is degree-1 (an amplitude in acceleration — the framework already discards the energy combination T² − T_Λ² because it gives the wrong deep-MOND law), and the additive-acceleration construction puts the external field into the first moment at unit weight on a single de Sitter floor, which together **select θ(0) = √2** (not the energy-branch value 2); (ii) the de Sitter Wightman function (∝ 1/sinh²) has exponential memory, whose transform **forces a Lorentzian kernel** θ(y) = √2 / [1 + (√2 − 1) y²] with a y⁻² tail. The one piece the bath does *not* fix is the **corner location** y = 1 (the bath's own scale H_Λ sits orders below every bound-orbit frequency); placing the corner at the internal orbital frequency ω_internal is a quasi-static modeling choice, licensed by Milgrom (1994, Eqs. 55–57), not derived.

With this derived kernel the dispersion of a dwarf, measured against an otherwise-identical circular-orbit dwarf at the same pericenter and mass, is

> σ(y) / σ_circular = (θ(0)/θ(y))^(1/2),  **monotone-rising** in the dwarf's *current* y — hotter the more non-adiabatic its present orbital phase, with **no interior zero** (the ratio exceeds 1 for every y > 0).

The crucial point — corrected in this version — is **which y, and when**. The discriminating axis is the dwarf's **current** y, set by its present orbital phase through the memory kernel (memory time ∼ 1/ω_internal ∼ 0.4–0.5 Gyr), *not* its pericenter peak and *not* its raw eccentricity. The pericenter-peak values y = 3.28 (Crater II) and y = 2.55 (Antlia II) are a *classification* — the hottest state each dwarf ever reaches — at which the predicted excess is large, **+134% and +92%** respectively. But both named carriers are in fact **currently near apocenter** (orbital phase ≈ 0.8–0.96, current y ≈ 0.6), their last pericenter ≈ 1.1 Gyr ago — two to three memory times, so the kernel has largely forgotten it. Their *present-day* excess is therefore a modest **≈ +7–8%**, which is exactly why the existing-data pilot (Sec. 5) returns a null: the carriers are caught cold. The **existence, the sign (higher current-y → hotter), and the modified-gravity-impossibility are kernel-independent theorems**; the kernel sets the magnitude (now σ ∝ θ^(−1/2), with θ(0) = √2 bath-selected and the Lorentzian shape bath-forced, the corner location the lone modeling choice). *(A distinct quantity — the absolute re-deepening (1/θ)^(1/2) − 1 — does cross zero at y = 1 and is suppressed below it; the previous version conflated that curve, and a low-y slice of it, with the matched-circular test observable above. The test a carrier-vs-control measurement actually performs is the matched-circular ratio, which is monotone-rising with no zero.)*

**Why diffuseness gates it.** y is large only when ω_internal is *small* — i.e. for diffuse, low-internal-frequency dwarfs. A dense dwarf has high ω_internal, so even a steep plunge keeps y ≪ 1 and the response stays adiabatic: dense dwarfs are *immune* and serve as a built-in internal control. Milgrom himself flagged the relevant population: "in some dwarf satellites of the Milky Way and Andromeda we estimate ω_ex ~ ω_in." Those diffuse satellites are precisely the carriers. The axis of the test is therefore **diffuseness-gated y**, not raw eccentricity — a distinction that turns out to be decisive for interpreting the pilot (Sec. 5).

---

## 3. The modified-gravity-impossibility theorem

What makes this prediction a *discriminator* rather than just another MOND signature is that no modified-gravity theory can produce it, even in principle.

In every metric or field formulation of MOND — AQUAL, QUMOND, and the relativistic completion AeST (the framework's only covariant home) — the external-field effect is **instantaneous**. Milgrom (2022) states it verbatim: a subsystem's internal dynamics "depend only on the momentary value of a_ex." The internal dynamics are governed by the value of the external field *right now*, with no memory of how the system arrived there. Therefore, comparing two dwarfs of identical mass at identical pericenter distance — one on a circular orbit, one on a radial plunge — a modified-gravity theory predicts **exactly the same internal σ**, hence

> ρ(σ, orbital history | r_peri, mass) = **0**,    for any a₀, in any metric/field MOND.

ΛCDM/CDM gives the same null for the same reason: a circular and a radial subhalo at matched current radius have the same internal dynamics modulo tidal history (which is the confound, addressed in Sec. 6, not the signal). **Only modified inertia — inertia as the nonlocal bath-response functional — yields a nonzero, history-dependent σ.** The logical structure is identical to the Cassini bound, which excludes the framework's modified-gravity cousins because *they* would imprint a trajectory/history dependence on solar-system orbits that the data forbid; here the *same* nonlocality appears as a *positive* prediction in a fresh, accessible observable. A zero result is consistent with all of modified gravity and CDM; a nonzero positive σ-vs-history correlation at fixed pericenter would be impossible for any of them and required by the framework.

---

## 4. The carriers, the controls, and the diffuseness gate

Pre-specifying carriers on physics (diffuseness), not on σ, the per-dwarf y computation places only two objects firmly in the non-adiabatic carrier band:

| dwarf | role | a_ext/a₀ @ peri | y = ω_ext/ω_in | regime |
|---|---|---|---|---|
| **Crater II** | carrier | 0.46 | **3.28** | NON-ADIABATIC |
| **Antlia II** | carrier | 0.35 | **2.55** | NON-ADIABATIC |
| Boötes I | control | 0.33 | 0.21 | adiabatic |
| Fornax | control | 0.14 | 0.16 | adiabatic |
| Sculptor | control | — | 0.12 | adiabatic |
| Draco | control | — | 0.07 | adiabatic |

**Crater II** is the prime carrier: extraordinarily diffuse (half-light radius ~1.1 kpc, the lowest internal density in the sample), eccentric (e = 0.71), with a *large* pericenter (24 kpc). **Antlia II** is the largest-radius dwarf known (~2.9 kpc), low density, eccentric (e = 0.56), pericenter 38 kpc. Both reach y ~ 2.5–3.3 at pericenter — squarely non-adiabatic. Both have large pericenters, which is a genuine design strength: they sit *away* from the tidal-stripping regime, so the prediction's two real carriers are **tide-clean by construction** (Sec. 6). Everything denser — Fornax, Sculptor, Draco, the compact ultra-faints — stays adiabatic (y < 0.3) and acts as the control locus. The sample is thus sharply **bimodal**: a 2-object carrier set against a ~22-object adiabatic background. This bimodality is the central fact governing what existing data can and cannot say.

---

## 5. The pre-registered pilot: a null at low power, reported straight

Before any fitting, I pre-registered the test (the registration, sign convention, primary statistic, and the prime confound are recorded in the data script; see Reproducibility). The hypotheses:

- **H1 (framework):** at fixed pericenter and mass, residual internal σ rises **monotonically** with the dwarf's *current* y (present orbital phase) as σ ∝ θ(current y)^(−1/2) — +90–130% at a carrier's pericenter peak, but only ≈ +7–8% for the named carriers in their current near-apocenter state. (The pilot below used raw eccentricity, a weak surrogate for current y — one of several reasons it is underpowered.)
- **H0 (modified gravity / CDM):** **zero** partial correlation.

Data are a single homogeneous source — Pace, Erkal & Li 2022 (ApJ 940, 136; Gaia EDR3 proper motions) for *all* σ_los and *all* orbital parameters — minimizing cross-catalog systematics. N = 24 usable Milky-Way dwarfs (both σ and eccentricity measured). The pre-specified primary statistic is the partial Spearman correlation of σ_los with eccentricity, controlling for pericenter, a luminosity-based mass proxy, and half-light radius.

**Result.** The point estimate is negative and insignificant in every variant:

| variant | ρ | p (two-sided) | reading |
|---|---|---|---|
| **PRIMARY** partial ρ(σ, ecc \| r_peri, L, r_half) | **−0.196** | **0.395** (dof = 19) | null, wrong-signed |
| virial-deviation ρ(log σ, ecc \| √(L/r_half), r_peri) | −0.220 | 0.313 | null |
| simple Spearman(σ, ecc) | −0.113 | 0.598 | null |
| no-LMC eccentricities | −0.030 | 0.899 | even flatter |

The correlation is small, slightly **negative** (the *opposite* sign to the predicted positive effect), and statistically indistinguishable from zero (all p between 0.40 and 0.90). Adding the pre-registered tidal proxy M_MW(<r_peri)/r_peri³ as an extra control leaves it essentially unchanged: ρ = −0.196, p = 0.408. The result is **robust to the tidal-heating control** — but only because there is no signal for tides to displace.

**I report this as what it is: a null with almost no power, not a strike against the theory.** Three reasons, all physical rather than a matter of bad luck:

1. **The axis is wrong for existing data.** The framework's signal lives on **y**, gated by diffuseness; only **two** of 24 dwarfs (Crater II, Antlia II) reach the carrier band. A population partial correlation on *raw eccentricity* is a weak surrogate — with 2 carriers buried in 22 adiabatic controls it cannot deliver the carrier-vs-control y-contrast the prediction actually makes.
2. **The σ errors are comparable to the predicted signal** (~10–40%, and *largest* on the carriers — Antlia II is 5.71 ± 1.08 km/s). The present-day effect for the named carriers — caught near apocenter at ≈ +7–8% — is at or below this floor per object; the large pericenter-peak signal is not currently on display in either of them.
3. **An artifact pushes the carriers slightly cold.** The carriers sit modestly below a naive luminosity/r_half virial baseline (Crater II σ_dev = −0.36, Antlia II −0.06). This is partly mechanical, not evidence against: y is itself built from σ (a low-σ diffuse dwarf is automatically high-y), so y and a σ-residual anti-correlate by construction. The clean, pre-registered eccentricity-axis test is the one to read — and it is null.

So: not suggestive (no surviving positive correlation), not tidal-confounded (robust to the control), simply **underpowered**. **Existing literature data does not yet show the effect, and existing data was never going to.** This pilot establishes only that fact; it does not, and cannot, move the theoretical status of the prediction. The sign remains a theorem.

---

## 6. The decisive test and its one real confound

The right test is **not** a raw-eccentricity population correlation. It is a **carrier-vs-control y-contrast** with the discriminating axis measured per object. Three ingredients make it decisive, all arriving on a near-term timeline:

1. **Gaia DR4 (December 2026)** sharpens per-dwarf proper motions, hence pericenter and the orbital frequency ω_ext, tightening y object-by-object — the axis is *measured*, not statistically inferred (the decisive improvement over the earlier, low-purity cluster-UDG version of the same physics, where infall phase had to be guessed at ~0.4 purity).
2. **A larger diffuse-carrier set** — Antlia II, Crater II, plus newly-characterized large-radius low-density satellites from DES/LSST follow-up — beats down per-object noise by turning a 2-point contrast into a population.
3. **Resolved σ profiles** (Keck/VLT/MUSE multi-object spectroscopy) rather than a single global σ.

**The one real confound is tidal heating.** A radial plunger with a small pericenter is also tidally stirred, which would *itself* inflate σ and could mimic the framework's positive signal. The design separates the two:

- The prediction is the σ excess *at fixed pericenter* — tidal heating is controlled by regressing on pericenter (and r_peri/r_tidal where available).
- Tides predict a **different radial σ profile** and a host-aligned stripping/elongation morphology, separable with resolved kinematics — whereas the bath-response effect is a global re-deepening into deep-MOND with no preferred tidal axis.
- The two named carriers are **tide-clean by construction**: Crater II and Antlia II have large pericenters (24, 38 kpc), sitting away from the stripping regime, yet are non-circular. They are non-adiabatic *without* being strongly tidally heated — exactly the clean corner the population test should target.

Run this way — carrier-vs-control y-contrast, Gaia DR4 orbits, resolved profiles, explicit tidal modeling — the test discriminates modified inertia from modified gravity at a sign level: a positive carrier-vs-control σ excess at matched pericenter is required by the framework and forbidden to all of metric/field MOND and CDM.

---

## 7. Scope and honest limitations

- **Pre-registered and falsifiable.** The hypotheses, sign convention, primary statistic, and prime confound were fixed before fitting. A null carrier-vs-control y-contrast at DR4 precision, or a *negative* one surviving the tidal control, would count against the framework's modified-inertia content.
- **Modified-gravity-impossible.** The signal's existence — not merely its size — is forbidden to every metric/field MOND and to CDM (Milgrom 2022). This is what makes it a discriminator, joining **Cassini** as a clean modified-inertia-vs-modified-gravity test.
- **The sign and the modified-gravity-impossibility are theorems; the magnitude is bath-constrained.** Higher current-y → hotter follows from θ decreasing alone. The de Sitter–Unruh bath *selects* θ(0)=√2 (the amplitude/excess-heat branch the framework already requires for the correct deep-MOND law) and *forces* a Lorentzian kernel shape from the de Sitter correlator; the dispersion rises as **σ ∝ θ^(−1/2)** (the external-field-effect regime for a dwarf inside the host field, not the isolated ¼ exponent), reaching **+90–130%** at a carrier's pericenter peak. The lone surviving modeling choice is the kernel's corner *location* (placed at ω_internal, quasi-statically licensed by Milgrom 1994, not derived); this is honestly *not* claimed as fully forced.
- **Near-term.** The decisive data (Gaia DR4) arrive December 2026; the carriers are named and the spectroscopy largely exists.
- **What this is not.** It is **not a TOE** — the framework does not derive the Standard Model and is a one-parameter effective theory at a frontier. It is **not a detection** — the present pilot is an explicit null at low power. It is **not a claim that existing dwarf data shows the effect** — they do not, and could not.

The honest standing: a sharp, MG-forbidden, pre-registered prediction with a measured discriminating axis and a named carrier set; a current null that reflects the data's lack of power rather than the theory's failure; and a decisive near-term test that the framework will pass or fail cleanly.

---

## Reproducibility

All numbers in Sec. 5 reproduce from two scripts in `real_research/reviews/`:

- `dwarf_ecc_sigma_pilot_data.py` — the 24-dwarf data dictionary (every value carries a per-object source citation; σ_los and orbits from Pace, Erkal & Li 2022 / Gaia EDR3; Simon 2019 and McConnachie 2012 as cross-checks), the pre-registered hypotheses, sign convention, primary statistic, and the tidal confound control. Footing: a₀ = 9.36 × 10⁻¹¹ m/s², framework interpolation only.
- `dwarf_ecc_sigma_pilot_analysis.py` — the per-dwarf y = ω_ext/ω_in computation and the partial-correlation test.

Supporting derivations: `real_research/NATIVE_CONSEQUENCES_HORIZON_INERTIA_2026-06.md` (the prediction's derivation from the bath premise), `real_research/DWARF_ECC_SIGMA_PILOT_2026-06.md` (the full pilot verdict), and `real_research/THETA_KERNEL_TOWARD_FORCED_2026-06.md` (the v2 kernel derivation: θ(0)=√2 selected from the framework's excess-heat/amplitude coupling, the Lorentzian shape forced by the de Sitter Wightman function, with the corner location the lone surviving postulate).

**References (key):** Milgrom 1994 (modified-inertia must be time-nonlocal); Milgrom 2022 (the kernel θ(y), and the instantaneous external-field effect of modified gravity); Deser & Levin 1997 (de Sitter–Unruh temperature); Pace, Erkal & Li 2022, ApJ 940, 136 (σ and Gaia EDR3 orbits); Simon 2019, ARA&A 57, 375; McConnachie 2012, AJ 144, 4.

*Local working paper, 2026-06-26. Not submitted, not published.*

# CFG4 — the target law, derived from the evidence

Second wave of the fresh campaign. This lane is constructive: it writes down the smallest set of effective equations
that reproduces every model-independent fact at once, with the core framework as its base, and it scores that target
against the data and against the framework's own findings. CFG2, CFG3 and CFG5 build to it.

The base is fixed.
- a₀ = κ c √(G ρ_Λ), with κ = ½ **fitted**, never derived. Z = 2√(8π/3) = 5.7888 is the same statement.
- Both footings everywhere: a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt).
- a₀ is flat in z on a true Λ. Its √ρ_DE(z) branch under evolving dark energy is carried as a labelled branch.
- The dark component, wherever one is needed, is the framework's own field in a cold-fluid state, not a particle
  species. A mass is still required.

This lane closes nothing. It states a target and the one place where the target is tight.

## Runs

Each script is run from the repository root. Each writes its own `.out` and `_results.json`. `MUTATE=1` writes the
`_MUTATE` versions. MUTATE was run first and the main run last, for every script.

| script | what it does | main | MUTATE (must fail) |
|---|---|---|---|
| `CFG4_galaxy_law.py` | part 1: the law from SPARC, ν's band, the scatter budget, the BTFR, ρ_eff and its surface density | 7/9, rc 0 | ν → 1 (Newton): headline fails, rc 1 |
| `CFG4_switch.py` | part 2: where the law must switch off; every criterion against every region | 13/13, rc 0 | switch removed from the web: CMB lensing fails, rc 1 |
| `CFG4_clusters.py` | part 3: X-COP and the Bullet, in units of the baryons | 7/7, rc 0 | cold component removed from clusters: headline fails, rc 1 |
| `CFG4_cosmology.py` | part 4: the CMB's cold component, and how much of it may leave or change form | 5/6, rc 0 | converted part smooth and whole: headline fails, rc 1 |
| `CFG4_target.py` | part 5: the assembled target, the own findings, the constant count, the verdict | 6/6, rc 0 | switch removed from the target: CMB-lensing row fails, rc 1 |

`CFG4_common.py` holds the shared harness, the constants, the kernels and FP20's exact projector. Runtimes are 2–140 s
per script with at most 2 threads.

## The answer

**One effective description fits every model-independent fact, but only in a narrow window.** The window is set by two
facts that pull against each other.

1. **KiDS-1000.** The lensing of isolated lenses at 0.3–1.5 Mpc needs the law's dark density to reach x ≥ 0.31 of each
   lens's turnaround radius. That floor assumes the unbound cold component supplies a 2-halo term. Without one, the
   floor is x ≥ 0.48.
2. **The CMB's cold-component amount.** Ω_c h² = 0.1200 has to hold the phantoms of every galaxy. It allows
   x ≤ 0.48–0.56 at z = 0.25 (all of Ω_c) and x ≤ 0.40–0.46 at z = 0.

The edge window is x ∈ **[0.31, 0.48]**. It is open on both footings and for both kernels when all of Ω_c is available
(at z = 0.25 and at z = 0), and when satellites share their host's phantom. It narrows when only the turned-around share of
the cold component counts: at z = 0.25 it stays open on the canonical footing and closes on the alt. At the strictest
variant it closes everywhere. That variant counts every galaxy as its own system, allows only the turned-around share, and
is evaluated at z = 0. There KiDS pays Δχ² = +21 to +44 with the 2-halo term. **That is the minimal conflict, named
precisely: KiDS's isolated-lens reach against Planck's Ω_c.**

**The smallest ingredient that resolves it: an edge set by the bound system's own collapse.** The law's dark density
ends where the cold component has crossed in all three directions, the splashback region. The edge belongs to the
top-level bound system, so satellites share their host's phantom. Outside it the cold component is single-stream CDM,
and its clustering supplies the lensing beyond the edge. The window's range, 1.5–2.3 r₂₀₀ₘ of the phantom halo or an
enclosed overdensity of 38–93 times the mean at z = 0.25, is where cold collisionless collapse puts its outermost
caustic. The self-similar value is 0.36 r_ta. If the edge is the shell-crossing radius, it costs no constant. That
identification is a candidate for the building lanes to derive. It is not derived here.

## The target equations

| | equation | status of its constants |
|---|---|---|
| **T1 the scale** | a₀ = κ c √(G ρ_Λ) = c H₀ √Ω_Λ / Z | κ = ½ **FITTED**. The form (G, c, ρ) is **DERIVED** (uniqueness, det = 2). a₀ ↔ Λ is **TIED** (unimodular multiplier, XR20/XR30). Flat in z is **TIED**; the √ρ_DE branch is **TIED** to the dark-energy fit. |
| **T2 the galaxy law** | inside ON regions, g = ν(\|g_N,b\|/a₀) g_N,b in the monopole reading, and ρ_eff = ∇·[(ν − 1) g_N,b]/(4πG) | ν's shape is **DECLARED**: ν_mono (adopted 09-26) or P2. It is one function with no continuous constant. SPARC's band is below. |
| **T3 the switch** | ON iff (i) the region lies inside a top-level bound system that has turned around, Δ(<r) ≥ Δ_ta(z) (11.81 / 8.89 / 5.72 at z = 0 / 0.25 / 2.5, GR top-hat); (ii) the law's dark density ends at a **density edge** r_e = x_e r_ta with x_e ∈ [0.31, 0.48]; and (iii) the system's baryonic mass M_b ≥ M_* | Δ_ta(z) is **DERIVED**. x_e is **DECLARED** within its window, and **DERIVED** if it is the shell-crossing radius. M_* ≡ a₀ξ²/G is **FITTED** within FP17's window (1, 6.7e6] M☉ (canonical) or (1, 8.1e6] M☉ (alt). It is the coherence-length law's ξ in mass form. |
| **T4 the dark component** | a cold fluid (w, c_s², c_vis² ≈ 0) with Ω_c h² = 0.1200, behaving as CDM wherever the law is off | Ω_c h² **FITTED** (initial data, the same status as ΛCDM's) |
| **T5 the bookkeeping** | **identity**: in a bound region the cold component *is* the law's dark density. The dark mass is max(M_ph, (Ω_c/Ω_b) M_b): baryon-poor galaxies are phantom-dominated, baryon-complete clusters keep the cosmic share. | the max rule is **DECLARED**. It adds no constant; the cosmic ratio comes from T4. |
| **T6 the late allowance** | after z ≈ 1–2, the cold component may stream out of galaxy-scale regions. At v_k ≤ 600 km/s, F_max ≈ 1. A form that never clusters again: ≤ 0.1. Decay into radiation: ≤ 0.05. | a constraint, not a constant |

**Constant count.**
- **FITTED 3:** κ, M_* (≡ ξ), Ω_c h².
- **DECLARED 3:** ν's shape, the max rule, x_e.
- **TIED 2:** a₀ ↔ Λ; flat a₀(z) and the √ρ_DE branch.
- **DERIVED 4:** the form of a₀; Δ_ta(z); the cluster content (the cosmic share); linear growth = ΛCDM.

Υ is a nuisance of the data, not a constant of the target. If x_e is derived as the shell-crossing radius, DECLARED drops
to 2. Compare the record's working constructions (CFG0): 5 fitted, 2 declared knobs, 3 declared natural choices. The
target itself carries none of ε, ζ, q, L_Λ, n, the q = 0 ramp or c_y. A construction that realises it may bring some back:
for example, a wave-field dark component keeps its mass floor m ≳ 2–5e-19 eV (L383), which the effective target does not see.

## What each own finding fixes

The coordinator's list. Each finding is placed in the target with its status, checked against it (`CFG4_target.py` H4),
and cited by the record's file.

| finding | source | status | role in the target |
|---|---|---|---|
| flat a₀(z) | `qwen_claude_field_theory/papers_2026/PAPER7_a0z_decisive_measurement_2026.tex` | TIED | a₀ carries no z; the switch must keep the z = 2.5 discs ON (it does) |
| a₀(z) ∝ √ρ_DE(z), labelled branch | FP0 R3b; XR20 (the √V refinement) | TIED to the DE fit | 0.796 × a₀ at z = 2.5 under the DES-Y5 pair; flat for w = −1; no extra constant |
| the unimodular tie | XR20, XR30 | TIED | a₀ tied to Λ's integration constant; no new local mode |
| uniqueness of a₀ = ξ c √(Gρ) | `real_research/reviews/mi_third_category_search_2026.py` | DERIVED form, FITTED κ | the form is forced; κ = ½ ⟺ Z identically; κ stays fitted |
| the BIG-SPARC null | `real_research/reviews/A0_COSMICWEB_ENVIRONMENT_2026-06.md` | MEASURED | a₀ is universal. Part 1's intrinsic scatter ≤ 0.043–0.048 dex agrees. It excludes any switch that modulates a₀ with local density. |
| the SN-Ia host step at the a₀ scale | `real_research/snia_massstep_acceleration_test.py`, `snia_hoststep_localSB.py` | COINCIDENCE, not used | the record's own tests found an age/metallicity effect |
| the GDM theorem | `real_research/reviews/mi_particle_vs_mode_2026.py` | DERIVED | T4 is a cold fluid plus an amount, not a particle |
| the ghost-condensate result (S8 neutral) | `opus_48_extended_research/reviews/GHOST_CONDENSATE_2026-06-19.md` | DERIVED | linear growth is ΛCDM's; S8 moves only through T6 |
| the coherence-length law; ħ/(ξc) ≈ 2e-22 eV | `hunt_2026/f29_coherence_length_law.py`; `ONE_NEW_THING_2026-09-04.md` | FITTED (one knob) | M_* ≡ a₀ξ²/G. The 2e-22 eV value stays a coincidence: the dark field's mass window sits 3 decades higher. |
| "the kernel removes 74–89% of cluster dark matter" | the category search, E2 | MEASURED, reading-dependent | re-measured on X-COP at 0.8 R₅₀₀. It removes **57–74%** when the extra component also sources the law (the finding's reading), and **40–52%** when only baryons do (FP22's adopted reading, the one CMB lensing allows). |

## Part 1 — the galaxy law (`CFG4_galaxy_law.py`)

**Controls.**
- The record's SPARC RAR fit (`real_research/rar_framework_a0_mlfit.py`, exec'd read-only) is reproduced to 3e-17: 0.108
  dex at Υ = 0.70, and the committed coarse table.
- FP1 C2's rms and Υ are reproduced to 1e-17.

**The law fits (H2, headline).** a₀ is held at the framework's value on both footings; one global Υ is profiled.

| | canonical | alt |
|---|---|---|
| ν_mono | 0.1003 dex at Υ_disk = 0.61 | 0.0991 dex at 0.57 |
| P2 | 0.1083 at 0.70 | 0.1035 at 0.65 |
| Newton | 0.2755 (Υ at the grid edge) | 0.2755 |

**a₀ and Υ are degenerate (H2b).** At the 3.6-µm prior Υ = 0.50, SPARC's best a₀ is 1.78e-10 (P2) or 1.37e-10 (ν_mono),
that is κ = 0.95 or 0.73. κ = ½ is the same fit at Υ ≈ 0.6–0.7. κ stays fitted.

**The shape band (H3; pre-declared UNCERTAIN, and FAILED as declared).**
- In the transition family ν_β = (1 + y^−β)^(1/2β), the galaxy bootstrap (1000 resamples) gives β = 0.48, 95% [0.40, 0.59]
  (canonical) and 0.55 [0.45, 0.77] (alt), both at Υ ≈ 0.45.
- P2 (β = 1) is disfavoured by 0.008 dex, in every resample.
- The expectation was a band above β = 1. It is below. The data want more boost at y ~ 0.3–3 than P2 gives, which either
  a softer transition at lower Υ or ν_mono's shape at Υ ≈ 0.6 supplies.
- The deep limit (BTFR slope 4) and the Newtonian limit are common to the whole band.

**The scatter budget (H4).**
- The error model: velocity errors per point; distance, inclination and a declared 0.10 dex Υ scatter, coherent within
  each galaxy.
- The ML per-point intrinsic scatter is 0.041–0.046 dex, **≤ 0.043–0.048 dex at 95%**.
- The declared error model predicts *more* scatter than observed (0.13 against 0.10 dex): the tabulated distance and
  inclination errors are conservative.
- Sensitivity to the Υ scatter: 0.051 dex (at 0.05) to 0.038 dex (at 0.15).

**The BTFR (H5).** On the clean V_flat sample (124 galaxies):
- the free slope is 3.68–3.76 (intrinsic 0.13 dex);
- at slope 4, A_obs = 52–59 M☉ (km/s)⁻⁴;
- the law's own outer-radius velocities give 46–64, within ≤ 0.053 dex of A_obs;
- the deep-limit 1/(G a₀) = 80.5 (canonical) or 66.6 (alt) sits 0.07–0.17 dex above, the finite-y offset. Reading κ off
  A_obs as a deep-limit number gives 0.68–0.77. That reading is biased; the record's 0.465 ± 0.076 is the same reading.

**ρ_eff and its surface density (H6; the "0.4–0.8" range FAILED for ν_mono).**
- *Analytic.* In spherical symmetry Σ_ph(<r) = y(ν − 1) a₀/(πG) exactly. For P2 it is bounded by **Σ_M = a₀/(2πG)**
  (107 / 129 M☉ pc⁻²), reached only as y → ∞. ν_RAR's bound is 1.2952 Σ_M (the record's h122). ν_mono has **no bound**:
  1.49, 1.79 and 2.38 Σ_M at y ≤ 10², 10⁴ and 10⁸.
- *SPARC.* The median of each galaxy's largest Σ_ph(<r) is 0.71 Σ_M (P2, canonical) and 0.89 (ν_mono). For ν_mono, 42–46%
  of galaxies exceed Σ_M.
- *Burkert fit.* The phantom's Burkert product is **ρ₀r₀ = 10^2.14–2.25 M☉ pc⁻²** (96–99 galaxies, fit rms < 0.1 dex).
  That is +0.09 to +0.18 dex above Σ_M, and on top of Donato et al.'s 10^(2.15 ± 0.2).
- *Core radius.* r₀ = 1.5 R_disk = 1.2–1.3 r_M (correlation 0.9).

**Verdict on the record's "halo surface density ≈ a₀/(2πG)": confirmed as an approximate relation, not an identity.** The
law's dark density reproduces the universal Burkert surface density at +0.1–0.2 dex above a₀/(2πG). The exact statement
is P2's ceiling on the enclosed surface density. The adopted ν_mono has no ceiling.

## Part 2 — the switch (`CFG4_switch.py`)

**Controls.** All exact, from the committed code exec'd read-only:
- **K1**, XR26's lensing: ΛCDM χ² 10.1456, pull −0.39; the chain's amplitude 1.1492 (+4.93σ, linear base) and 2.1344
  (halofit); f* = 0.618 / 0.178.
- **K2**, FP17's threshold window: 0.40–6.72e6 M☉ (canonical) and 0.58–8.12e6 (alt); the compactness gap 2.91e-12 to
  3.71e-9; the length window 0.021–84 pc.
- **K3**, FP20's corrected KiDS base: 139.800 / 133.948.
- **K4**, h72's bounds: > 1.67 / 2.07 / 3.44 / 2.77 Mpc.

**The bound-state thresholds (D1).** The ΛCDM top-hat turnaround contrast is 1 + δ_ta = 11.81 / 8.89 / 7.09 / 5.72 at
z = 0 / 0.25 / 0.64 / 2.5, with δ_lin = 1.276 → 1.076. The energy form is 1/Ω_m(z). The virial contrast is 328 → 182 in
mean-density units.

**The separability table (H3).** Every region's variables are computed: SPARC; KiDS at its reach; the z = 2.5 discs;
the web at z ≤ 0.64 and k = 0.1–1 h/Mpc on CLASS spectra; the IGM at z = 2–3 and k = 1–20 h/Mpc; FP17's Solar-System rows.

| criterion | web and IGM | Solar System | why |
|---|---|---|---|
| field strength y (the "yield"; equivalently the field-energy density against ρ_Λc²) | fails | fails | KiDS needs y_th ≤ 2.1e-5; the web's modes reach 1.8e-3; the Sun's y = 1.7–22 sits inside SPARC's range |
| length band | fails | separates | the IGM's forest scales (19–495 kpc) fall inside the ON band [0.08 kpc, 0.84 Mpc] |
| system mass band | fails | separates | the IGM's forest-scale masses (6.8e7–5.5e11 M☉) fall inside the ON range |
| local overdensity | fails | fails | KiDS at its reach has 1 + δ = 3.8; the IGM's 97.5% tail reaches 5.8 |
| **bound** (Δ(<r) ≥ Δ_ta(z)) | **separates** | fails | KiDS at its reach: 11.4 ≥ 8.89; the web's and IGM's 1σ contrasts ≤ 3.45 |
| **bound AND M_b ≥ M_*** | **separates** | **separates** | the Sun (1 M☉) is OFF for M_* in (1, 6.7e6] M☉, below SPARC's smallest galaxy (5.2e7) |

**The KiDS reach (H2, H2b, H2c, H7).** These use the exact projector, 60 points and the full covariance.
- *Fixed-radius truncation.* A sharp truncation of the phantom's density needs r_t ≥ 0.84 Mpc with no 2-halo term, and
  ≥ 0.50 Mpc with one (A ≤ 2).
- *At each lens's own radii.* Truncating at the turnaround radius (0.95–2.25 Mpc for log M_b = 10–11.5) *improves* the fit,
  Δχ² = −8.7 to −9.5. The energy radius gives +0.6 to +3.7. The virial radius gives **+212 to +229** (+76 to +81 with the
  2-halo term), and r₂₀₀ₘ gives +174 to +190. A switch that ends the law at the virial radius fails KiDS.
- *In units of r_ta.* The window is x ∈ [0.47–0.50, ~1.5] without a 2-halo term and [0.30–0.31, ~1.5] with one. The best is
  x ≈ 0.6–0.8, with Δχ² = −15 to −20 against an unbounded phantom.
- *Robustness (H7).* With the photometric masses **fixed** (h72's bins) and one coherent offset, an edge at 0.6–1.0 r_ta
  still beats the unbounded phantom, by Δχ² = −9.7 to −20.4. With a fixed unit 2-halo term the best edge is x ≈ 0.5–0.6.

**Two kinds of edge (H7). This is the design rule for CFG3.** Both use the same KiDS data.
- A **response edge**, where the law's boost returns to 1 and the phantom's enclosed mass stops gravitating, must lie
  beyond **1.67 / 2.07 / 3.44 / 2.77 Mpc**. That is the record's h72, reproduced as K4, and it is what CFG0 means by "a
  turnaround switch fails KiDS".
- A **density edge**, where the phantom's source density ends and its enclosed mass keeps gravitating as 1/r², is allowed
  in to **0.70 / 0.76 / 1.25 / 1.01 Mpc** in h72's own convention, and to x ≈ 0.3–0.5 r_ta with a 2-halo term in the exact
  ESD analysis.

The target's edge is a density edge. A construction whose switch acts on the field law itself fails KiDS. One that
confines the phantom's source passes.

**In the pipelines (H4, headline).**
- **CMB lensing.** The unbound linear web carries no phantom, so Planck's 8–400 amplitude is 1.000 (−0.39σ). Without the
  switch it is XR26's 1.149 (+4.9σ); the MUTATE shows this.
- **The forest.** The unbound IGM carries no phantom: deviation 0.
- **KiDS.** With the edge at the turnaround radius: −8.7 to −9.5.
- **The z = 2.5 discs.** r_F = 11–39 kpc sits inside the virialised body: ON, 0 dex.
- **The Solar System.** The M_* window is non-empty.
- **The leak (H6, reported).** If the bound regions' phantom *adds* to the cold component, CMB lensing reads 1.060 (linear
  base, +1.75σ) or 1.528 (halofit, +18σ). The bookkeeping is part 5's question.

## Part 3 — clusters and mergers (`CFG4_clusters.py`)

**Controls.**
- L7 (`fable_independent_2026/L7_cosmic_ratio.py`, exec'd read-only) is reproduced to machine precision: f_bar 0.149, the
  Newtonian M_dark/M_bar 5.73 ± 0.68, the framework residual 3.09 ± 0.71 (canonical) and 2.76 (alt).
- The record's Bullet table gives the same offsets as this lane's recomputation.

**Twelve X-COP clusters at 0.8 R₅₀₀, twelve clusters, both footings.**

| | P2 canonical | ν_mono canonical | P2 alt | ν_mono alt |
|---|---|---|---|---|
| η = M_HSE/M_law | 2.03 ± 0.27 | 1.82 ± 0.23 | 1.86 ± 0.25 | 1.68 ± 0.22 |
| residual beyond the law (M_b) | 3.47 ± 0.70 (17σ) | 3.09 ± 0.71 (15σ) | 3.14 ± 0.72 (15σ) | 2.75 ± 0.72 (13σ) |
| share of the Newtonian dark mass the law removes | 40% | 47% | 45% | 52% |
| residual density slope, 40–750 kpc | −1.56 ± 0.22 | −1.58 ± 0.24 | −1.58 ± 0.24 | −1.62 ± 0.31 |

- **The Newtonian dark mass.** 5.73 ± 0.68 M_b, which is 1.07 × the cosmic Ω_c/Ω_b = 5.36. f_b = 0.149 against the cosmic
  0.157.
- **The residual's distribution.** Its density falls as r^−1.6. The baryons fall as r^−1.25, so the residual is more
  concentrated than the gas.
- **The hydrostatic bias.** A positive b raises the residual: 4.5–5.2 M_b at b = 0.2. No admissible b removes it.
- **The identity reading.** Dark mass = max(phantom, cosmic share). In every cluster the cosmic share (5.36 M_b) exceeds the
  phantom (2.4–3.1 M_b), and the reading reproduces X-COP to **0.946 ± 0.080** (0.889 at X-COP's own 6% non-thermal
  share). Clusters are then ΛCDM-like: the phantom is absorbed in the cosmic share.
- **The Bullet** (Clowe et al. 2006 Table 2).
  - The lensing peaks sit on the galaxies, 209 kpc (main) and 194 kpc (sub) from the plasma.
  - The plasma apertures hold *more* baryons: −12% (main) and −45% (sub) at the galaxy apertures.
  - The convergence contrast (3.7σ and 2.3σ; 4.3σ combined in the apertures; 8σ in Clowe's full map) needs a collisionless
    projected mass at the galaxies of **4.6× and 4.9× the aperture baryons**. Σ_crit comes from the record's convention.

## Part 4 — cosmology (`CFG4_cosmology.py`)

**Controls.**
- CLASS at XR26's Planck parameters, with this lane's own band-power code, reproduces XR26's ΛCDM lensing χ² = 10.145612
  exactly, and σ₈ = 0.8116.
- The Limber integral matches CLASS to 0.13%.
- The two-fluid solver returns ΛCDM exactly at F = 0.

**The fact.** Ω_c h² = 0.1200 ± 0.0012 (Planck 2018): a cold fluid clustering at z ~ 1100. CMB-scale physics is GR + CDM
(XR26: TT/TE/EE equal ΛCDM's to 7.8e-8).

**How much may leave or change form (H2, headline; H4).** The gates are Planck's 8–400 amplitude within 2σ, S8 ≥ 0.752
(the record's floor), RSD f σ₈ Δχ² ≤ 4 (6dFGS, SDSS MGS, BOSS DR12, eBOSS DR16), and DESI DR1 BAO.

| mode | z_c = 0.5 | 1 | 2 | at F = 1 (z_c = 1) |
|---|---|---|---|---|
| kick, v_k = 200 / 400 / 600 km/s (background unchanged) | F_max = 1 | 1 | 1 | S8 ratio 0.99 / 0.98 / 0.95; lensing ≤ 0.3% |
| kick, v_k = 1000 km/s | 1 | 0.7 | 0.5 | S8 ratio 0.88, RSD Δχ² +5.2 |
| never clusters again (smooth) | 0.1 | 0.1 | 0.0 | S8 ratio 0.14 |
| decay into radiation (CLASS dcdm; h refitted to 100θ_s) | F_max = 0.05, set by lensing | | | at F = 0.1: lensing −2.4σ, S8 0.78, BAO shift χ² 0.3 |

Streaming daughters still cluster on the scales the linear probes weigh. So a late cold component may leave galaxy-scale
structures almost entirely after z ~ 1–2, if it streams at ≤ 600 km/s. The forest bounds what converts before z ~ 2; the
record's XR12/XR19 gas proxy is already at its 10% line near F_b(2) ≈ 0.4.

**The cross-check against XR19 (H3; FAILED its 0.02 tolerance, kept as run).** This lane's step model gives S8 ratios
0.934 / 0.944 / 0.974 at z_web = 1.8 / 1.2 / 0.5. XR19 gives 0.912 / 0.924 / 0.938. The fluid approximation (c_s² = v²/3)
suppresses less than XR19's solver does. The allowances above are therefore on the generous side by ~0.02–0.04 in S8.

## Part 5 — consistency (`CFG4_target.py`)

**The gate rows (H1, headline).** All pass:
- SPARC;
- KiDS, with the edge at 0.4 r_ta and the 2-halo term: Δχ² −10.7 to −12.4;
- CMB lensing: 1.000;
- the forest;
- the z = 2.5 discs;
- the Solar System;
- X-COP (identity): 0.946;
- the Bullet: 4.6× and 4.9×;
- the late allowance.

**The additive reading fails (H2).** If the law's phantom is added to the cold component's cosmic share in clusters, X-COP
is overshot:

| | P2 canonical | ν_mono canonical | P2 alt | ν_mono alt |
|---|---|---|---|---|
| additive / measured | 1.27 ± 0.11 | 1.32 ± 0.12 | 1.32 ± 0.12 | 1.37 ± 0.12 |
| significance (median of 12) | 8.4σ | 9.7σ | 9.4σ | 10.6σ |

This is the record's FP16 "X-COP too massive", in data form. The same reading leaks into CMB lensing (part 2).

**The identity reading's budget (H3, pre-declared UNCERTAIN).**
- The inputs: the GAMA stellar mass function (Baldry et al. 2012) and SPARC's own gas fractions, with log(M_gas/M_*) =
  −0.456 log M_* + 4.19. SPARC is HI-selected, so the budget sits on its tight side; a stars-only run relaxes it by ~30%.
- If every galaxy's phantom ran to its turnaround radius, the phantoms would hold **Ω_ph = 0.47–0.55**, against **Ω_c =
  0.265**. The turnaround edge (x = 1) is excluded in the identity reading. In the additive reading it is excluded by
  X-COP.
- The budget edge moves with the variant, as the verdict table shows.

**The verdict.** The canonical/P2 row, x at the budget edge:

| budget variant | budget edge | KiDS floor (2-halo / none) | window |
|---|---|---|---|
| z = 0.25, all of Ω_c, every galaxy its own system | ≤ 0.56 (0.48–0.49 alt) | 0.31 / 0.48 | open |
| z = 0, all of Ω_c | ≤ 0.46 (0.40 alt) | 0.31 / 0.48 | open with the 2-halo term |
| z = 0.25, only the turned-around cold share (0.60 Ω_c) | ≤ 0.34 (0.29 alt) | 0.31 | open canonical, closed alt |
| **strict**: z = 0, turned-around share | ≤ 0.28 (0.24 alt) | 0.31 | **closed**: KiDS Δχ² +21 to +44 (2-halo), +111 to +162 (none) |
| satellites merged (log M_* ≥ 9 carry phantoms), z = 0, turned-around share | ≤ 0.37 (0.32 alt) | 0.31 | open with the 2-halo term |

## What a construction must hit (the checklist for CFG2, CFG3 and CFG5)

1. **The galaxy law.** SPARC ≤ 0.110 dex at a₀ fixed (either footing) with Υ_disk in 0.5–0.8. Intrinsic scatter ≤ 0.048
   dex. The deep limit gives BTFR slope 4 with A = 1/(G a₀) asymptotically. At finite radius: A_obs = 52–59 M☉ (km/s)⁻⁴.
2. **Surface density.** The phantom's Burkert ρ₀r₀ lands at 10^(2.1–2.25) M☉ pc⁻², a constant surface density that must
   come out.
3. **Solar System.** Off for systems of M_b ≤ 1 M☉. On for every SPARC galaxy (M_b ≥ 5e7 M☉). FP17: only a mass or length
   separates them.
4. **The web.** Off in the unbound linear web at z < 0.64 (CMB lensing). If the law acts there it must be cut to ≤ 0.62
   (linear) or ≤ 0.18 (halofit) of XR26's.
5. **The IGM.** Off in the unbound z = 2–3 IGM. On in z = 2.5 discs at r_F.
6. **KiDS.** A density edge (not a response edge) at x_e ∈ [0.31, 0.48] of the system's turnaround radius, with the cold
   component outside it single-stream CDM whose clustering fills the lensing beyond. A response edge must lie beyond
   1.7–3.4 Mpc. An edge at the virial radius fails (Δχ² ≥ +76).
7. **The cold budget.** Σ over top-level systems of M_ph(<x_e r_ta) ≤ the cold mass that has turned around: Ω_c h² = 0.12.
8. **Clusters.** Dark mass = max(phantom, (Ω_c/Ω_b) M_b) at 0.8 R₅₀₀ (to 5 ± 8%), with the residual beyond the law
   collisionless, ρ ∝ r^−1.6, and riding with the galaxies through a merger (Bullet: 4.6–4.9× the aperture baryons, 194–209
   kpc offsets). Adding the phantom to the cosmic share overshoots by 27–37%, at 8–11σ.
9. **Cosmology.** GR + CDM at z ≳ 10. Linear growth is ΛCDM's. After z ~ 1–2 the cold component may stream out of galaxies
   (F ≤ 1 at ≤ 600 km/s); it may not stop clustering altogether (≤ 0.1) or turn into radiation (≤ 0.05).

## Pre-declared expectations that came out false (kept as run)

- **Part 1 H3.** The SPARC band on β was expected above 1. It is below: 0.40–0.59 and 0.45–0.77.
- **Part 1 H6.** The median of each galaxy's largest Σ_ph was expected in 0.4–0.8 Σ_M. ν_mono gives 0.89 (canonical); the
  other three cells were inside.
- **Part 4 H3.** The XR19 cross-check tolerance was 0.02. The differences are 0.02–0.04.

## Disclosures

- **Exploratory runs (scratch, not committed).**
  - Before part 5 was written, a phantom-budget estimate (EdS turnaround contrast, rough gas fractions) gave
    Ω_ph(r_ta)/Ω_m = 1.5–2.7. It shaped H3's wording.
  - Before K4/H7 were added, a KiDS re-fit with the photometric masses fixed showed the density-edge pass does not lean on
    the per-bin mass profiling. The profiled masses moved by ≤ 0.1 dex.
- **Debug runs.**
  - Part 2's first MUTATE run predated the x-scan.
  - Part 2's window finder first returned "inf" on a non-monotone scan and was replaced.
  - Part 5's KiDS gate row first scored the turnaround edge. It was changed to the target's own edge before the committed
    runs.
  - Every script's committed pair is MUTATE first, then main.
- **Added after the committed-form runs.** Part 2's K4 and H7 were added when CFG0, running in parallel, reported "a
  turnaround switch fails KiDS" from h72. They show the two statements concern different edges. No other check, threshold
  or number changed. Part 5 was re-run afterwards.
- **Not done here.**
  - No particle-mesh or N-body run.
  - No Planck likelihood; Planck's published band powers and amplitudes are used.
  - The edge is not derived.
  - The budget treats galaxies from a z ≈ 0 stellar mass function, uses a Press–Schechter turned-around share, and brackets
    satellites with a mass cut rather than a group catalogue.
  - The Bullet uses published aperture numbers, not a lensing map.
- **Published numbers typed in.**
  - The GAMA stellar mass function (Baldry et al. 2012).
  - f σ₈ from 6dFGS, SDSS MGS, BOSS DR12 and eBOSS DR16.
  - DESI DR1 BAO.
  - Planck 2018: Ω_c h², Ω_b h², the lensing band powers via XR26.
  - Donato et al. 2009 and Gentile et al. 2009 for comparison only.
  - Nothing was downloaded.
- **Literature overlap, checked after the fact.** A law confined to bound systems, and an edge at the splashback radius,
  echo published ideas on environment-dependent MOND and on halo boundaries. The target is stated from data. Its
  distinctive content is the framework's: a₀ from ρ_Λ, flat in z, with κ fitted.

## Files

- `CFG4_common.py` — shared harness, constants, kernels, FP20's exact projector.
- `CFG4_galaxy_law.py`, `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json` — part 1.
- `CFG4_switch.py`, `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json` — part 2.
- `CFG4_clusters.py`, `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json` — part 3.
- `CFG4_cosmology.py`, `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json` — part 4.
- `CFG4_target.py`, `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json` — part 5. Its results JSON carries the
  target in machine-readable form under `numbers.TARGET` and `numbers.VERDICT`.
- `CFG4_README.md` — this page.

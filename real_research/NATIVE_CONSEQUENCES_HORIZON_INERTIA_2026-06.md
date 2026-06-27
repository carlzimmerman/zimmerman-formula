# Native consequences of inertia-from-the-horizon-bath — the sharpest NEW one

**Date:** 2026-06-26  **Footing (sealed):** a₀ = cH_Λ/Z = 9.36e-11 m/s²; cH_Λ = 5.42e-10;
H_Λ = cH_Λ/c = 1.81e-18 s⁻¹ (de Sitter / cosmic-horizon Gibbons-Hawking rate);
the framework's OWN excess-heat interpolation g_obs = √(g_bar² + g_bar·a₀), ν(y)=√(1+1/y),
μ_fw(x)=(√(1+4x²)−1)/2x. No McGaugh ν used; no data fit triggered (forward consequence).
LOCAL file — do not git-push.

The premise throughout: **inertia is a body's nonlocal-in-time RESPONSE to the de Sitter
cosmic-horizon Unruh bath.** Modified inertia, not modified gravity, not a fitted-a₀ MOND.
The bath is the subject; I reason from it to new consequences.

---

## The single sharpest NEW native consequence

**Diffuse Milky-Way / Local-Group dwarf-spheroidal internal velocity dispersion correlates
with the dwarf's own ORBITAL ECCENTRICITY at fixed pericenter radius — radial-plunge dwarfs
run HOTTER than circular-orbit dwarfs of the same mass and same closest-approach distance.**

This is the bath's clock made observable. The mechanism:

1. The horizon bath has exactly ONE rate, H_Λ (the horizon's correlation/Gibbons-Hawking
   frequency). Milgrom (1994) proved modified inertia MUST be time-nonlocal — a memory kernel.
   So the inertial response is a functional of the whole recent worldline, weighted by a kernel
   θ(y), y = ω_ext/ω_internal (Milgrom 2022, Eq. 28/33/34), with the only intrinsic clock the
   bath supplies being 1/H_Λ.
2. A dwarf's inertia therefore reads the **history-averaged magnitude** of its acceleration, not
   the momentary value. For a CIRCULAR orbit |a_ext| is constant → the kernel sees a stationary
   history → pure adiabatic θ(0) (the EFE-thermometer reading already banked for Crater II). For a
   RADIAL/eccentric PLUNGE, |a_ext| sweeps as the dwarf falls in → near pericenter
   ω_ext → ω_internal (y→O(1)) → genuinely non-adiabatic, θ(y) a real function, not a constant.
3. Because θ is decreasing (θ(0) ~ a few, θ(1)=1, Milgrom-forced), a plunging dwarf sheds the
   adiabatic external loading → drops DEEPER into the MOND regime → HOTTER σ than a circular dwarf
   at the same pericenter radius.

**Numerical check (clean-room, a₀=9.36e-11, framework μ_fw), /tmp/mi_dwarf.py:**

| dwarf | a_ext/a₀ @peri | y = ω_ext/ω_in | regime |
|---|---|---|---|
| Crater II | 0.46 | **2.6** | NON-ADIABATIC |
| Antlia II | 0.35 | **2.5** | NON-ADIABATIC |
| Bootes I | 0.40 | 0.57 | borderline |
| Fornax (dense control) | 0.23 | **0.20** | adiabatic (stays cold-circular-like) |

Amplitude on σ: σ ∝ (θ_eff)^¼ → radial-vs-circular ratio **1.19–1.28 (≈19–28% hotter)** for
θ(0) = 2…e. The diffuse low-internal-frequency dwarfs Milgrom himself flagged ("in some dwarf
satellites of the Milky Way and Andromeda we estimate ω_ex ~ ω_in") are exactly the carriers; dense
dwarfs (Fornax) stay adiabatic and show no effect — a built-in internal control.

### (i) Genuinely NEW vs the corpus? — YES, as an observable, with a shared mechanism

- The θ(ω_ext/ω_in) non-adiabatic-inertia mechanism IS banked, but ONLY for **cluster UDGs**
  (`reviews/member_MI_nonadiabatic_plunge.py`, `GENUINE_MI_CLUSTER_DISTINCTIVE`,
  `SIGMA_SPREAD_MI_TEST`), where the discriminating axis is cluster-orbital **infall phase
  inferred STATISTICALLY** (purity ~0.4, kr proxy, unidentified Coma/Hydra members).
- In the corpus, MW dwarfs (Crater II, Antlia II) appear ONLY as **static EFE thermometers** —
  σ vs host-field MAGNITUDE, the adiabatic θ(0) reading (`STATE_OF_THE_FRAMEWORK.md` L162,
  `TESTABLE_PREDICTIONS.md`, `PROGRAM_20_FINDINGS.md` row 15, paper row 6). **No file uses
  σ-vs-orbital-eccentricity-at-fixed-pericenter as the discriminator**, and no file transplants the
  non-adiabatic θ(y) effect to Local-Group satellites.
- What is new: the carrier population (resolved MW/LG dwarfs) AND a CLEAN per-object x-axis —
  **Gaia-measured orbital eccentricity per dwarf** (Pace+2022, Battaglia+2022 proper motions →
  pericenter and eccentricity known object-by-object) replaces the statistically-inferred,
  poor-purity cluster infall phase. Same physics class, decisively better-controlled test.
- Distinct from all four banked native predictions: s^TX SME dipole, the relational cluster
  σ-spread (cluster a_ex, statistical infall), the CMB-apex anisotropy, a₀(z).

### (ii) Modified-gravity-IMPOSSIBLE? — YES, by theorem (not a kernel choice)

In ANY modified-gravity host (AQUAL/QUMOND/AeST quasi-static — the framework's only covariant
home), the external-field effect is INSTANTANEOUS: internal dynamics depend ONLY on the momentary
a_ext (Milgrom 2022, verbatim, "depends only on the momentary value of a_ex"). So at fixed
pericenter radius MG predicts **EXACTLY ZERO** σ-vs-eccentricity correlation, for ANY a₀. ΛCDM/CDM
likewise → ~0 (a circular and a radial subhalo at the same radius have the same internal dynamics
modulo tidal history). Only modified INERTIA — inertia as the nonlocal bath-response functional —
gives a nonzero, eccentricity-dependent σ. The EXISTENCE and SIGN are kernel-independent
(guaranteed by θ(0) > θ(1), Milgrom-forced: radial plunge → hotter). Same logical class as Cassini
(history/trajectory dependence a local field theory cannot produce), in a new accessible observable.

### (iii) TESTABLE? — YES, ABOVE FLOOR IN PRINCIPLE, kernel-hostage on the exact coefficient

- **Instrument/data:** internal σ from Keck/VLT/MUSE multi-object spectroscopy (in hand for the
  classical + many ultra-faint dwarfs); orbital eccentricity/pericenter per object from **Gaia DR3
  → DR4 (Dec 2026)** proper motions. The discriminating axis is directly MEASURED per dwarf, not
  inferred — this is the decisive improvement over the banked cluster version.
- **Signal vs floor:** predicted 19–28% σ excess for radial vs circular diffuse dwarfs at matched
  pericenter. Dwarf σ measurement errors are ~10–20% and tidal/sample-size scatter is comparable,
  so the effect is **near-to-above floor**, NOT clearly buried — and it is a CORRELATION across the
  diffuse-dwarf population (Antlia II, Crater II, Bootes I, Hercules, Tucana II … vs Fornax-like
  dense controls), which beats down the per-object noise. This is genuinely better-positioned than
  the cluster σ-spread (purity ~0.4) it descends from.
- **Honest ceiling (both ways):** the EXACT amplitude needs the real memory kernel θ(y), which the
  framework has NOT derived — the SAME open θ(y) that bounds every banked relational prediction. So
  the SIGN and EXISTENCE are sharp theorems; the magnitude carries a factor-~2 kernel uncertainty.
  Tidal heating is a real confound (radial plungers also get tidally stirred) and must be modeled —
  but tides predict a DIFFERENT radial profile and a host-stripping signature, separable with
  resolved kinematics. Rate this **PARTIAL → strong**: distinctive, MG-impossible, above-floor in
  principle, with a clean Gaia-measured axis and a named carrier set, not yet a single
  pre-registered numeric kill.

---

## Runner-up (also new, weaker): the Local-Group timing-orbit frequency-memory boost

The same bath clock gives a second, lower-purity consequence: on the MW–M31 timing orbit
ω_LG/H_Λ ~ 7.6 (period ~10s of Gyr, radius ~Mpc, g_bar ~ 0.01 a₀, deep-MOND), the convex excess-T
average (Jensen) over the eccentric plunge raises ⟨T(a)⟩ above T(⟨a⟩), giving an O(1) (~18% in a
toy at ω/H_L~5, a_pk=5a₀, /tmp/mi_check.py) EXTRA boost over the instantaneous interpolation. This
is also NEW (corpus has only the STATIC 58× timing boost, "inherited from Milgrom",
`STATE_OF_THE_FRAMEWORK.md` L163) and also MG-impossible (frequency/memory dependence). But it is
WEAKER as a test: a single system, with ~50% observational timing-mass scatter already, so the
~10–30% memory enhancement is near-degenerate with the mass uncertainty. Improvable with Gaia/JWST
proper motions on more galaxy-pair first-infall orbits, but the dwarf-eccentricity correlation
above is the cleaner, higher-N, per-object-controlled version of the SAME bath-clock physics — so
that is the one to credit loud.

## What stays honest / null (no oversell)

- Static RAR / SPARC: the hyperbolic-motion bath response collapses ALGEBRAICALLY to
  g_obs=√(g_bar²+g_bar·a₀) (sympy-level), so steady-acceleration data CANNOT separate the framework
  from generic MOND. Said plainly — not a manufactured win.
- Galaxies (ω~200 H_Λ), wide binaries (ω~100 H_Λ), solar system (g≫a₀, bath at floor): all in the
  instantaneous limit → NO memory effect. Stated, not buried.
- The temp-route deep-MOND a₀_eff = 2cH_Λ is ~11.6× the density-route a₀=9.36e-11 — the known
  temp-vs-density split; the density footing is the sealed one and is what I used.

---

## WHAT TO TELL CARL

Your horizon bath has a CLOCK — the cosmic-horizon correlation rate H_Λ — and because inertia is the
body's nonlocal RESPONSE to that bath, the clock has to show up in the dynamics. It does, in a place
nothing in your corpus has pointed at yet: **a diffuse Milky-Way dwarf that falls in on a radial
plunge should run hotter than the same dwarf on a circular orbit at the same closest approach — by
about 20%.** Crater II and Antlia II actually reach the non-adiabatic band (ω_ext ~ 2.5 ω_internal
at pericenter); dense Fornax stays cold and circular-like as a built-in control. This is your
bath-response inertia reading the dwarf's history, not its momentary position — which is why it is
strictly impossible for any field/metric MOND: those theories see only the momentary external field,
so they predict EXACTLY zero σ-vs-eccentricity correlation. The new and decisive part vs your banked
cluster-UDG version: here the discriminating axis is the dwarf's orbital eccentricity, which Gaia
MEASURES per object — no statistical infall-phase guessing. The honest catch is the same one that
bounds your other relational predictions: the exact 20% needs the memory kernel θ(y) you haven't
derived, so the SIGN (plunge → hotter) is a clean theorem and the magnitude is good to a factor ~2,
with tidal heating the confound to model. This is a NEW MI-vs-MG door — the bath's clock written on
Local Group dwarfs — joining Cassini and the relational σ-spread.

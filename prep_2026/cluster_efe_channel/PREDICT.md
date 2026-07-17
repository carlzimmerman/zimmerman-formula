# PREDICT — the cluster-member infall-phase EFE σ-spread (MI-class vs MG)

**Lane:** PREDICTION. **Script:** `predict.py` (exit 0, numpy+sympy, both footings) · log `predict.out`.
**Date:** 2026-07-17. **Framework:** de Sitter–Unruh MODIFIED INERTIA (Zimmerman).
g_obs = ν(y)·g_bar, ν = √(1+1/y), y = g_bar/a₀, a₀ = cH_Λ/Z, Z = √(32π/3) = 5.789.
Milgrom 1983/1999 (PLA 253:273) wellhead credit for the ν-kernel; distinctive content = the
**cH_Λ/Z coefficient** + the time-nonlocal MI completion K(□_u). **a₀'s value and s = −1 remain
postulates. MG = 0 is the sole theorem-grade claim.**

---

## The observable (the mechanism, precisely)

A galaxy falling into a cluster feels the cluster's external field g_ext. Both MI and MG have an
External Field Effect that loads the member's internal MOND boost. They differ in **time-dependence**:

- **MG (QUMOND/AeST/TeVeS/f(R)):** the EFE is **instantaneous** — internal dynamics are set by the
  **current** g_ext = g_ext(cluster-centric position) only. Two members at the same current
  position have **identical** internal boost ⇒ the infall-phase spread is **exactly zero**.
- **MI (this framework + ANY history-dependent inertia):** inertia is a functional of the member's
  **acceleration history** via K(□_u), so the internal boost depends on the **infall phase** through
  the Milgrom-2022 (PRD 106 064060) subsystem boost θ(y), y = ω_ex/ω_in. A first-infall galaxy near
  pericentre has a different history than a backsplash galaxy at the **same current radius**. So at
  **fixed current g_ext**, MI predicts a **spread** in (internal σ)/(baryon-predicted σ) correlated
  with infall phase.

This is the **nearer-powerable** sibling of the star-orbit σ-spread. The just-completed star-orbit
swing (`prep_2026/sigma_spread/MI_SPREAD.md`) established that the **6–13% band belongs to THIS
channel** (the subsystem-boost EFE), not the star-orbit-within-one-system channel (which τ_mem ≫
τ_orbit freezes to sub-percent). This lane sharpens THIS channel.

---

## The sharpened prediction (all reproduced by `predict.py`, both footings)

### (1) Magnitude — banked 6–13% CONFIRMED as the fiducial-kernel band
Fiducial diffuse deep-MOND member (a_in ≈ 0.3 a₀ internal, a_ex ≈ a₀ external, at the transition
shell), relational spread across the infall-phase window y ∈ [0, 1.5]:

| kernel θ(y) | y≤1.5 spread | y≤1 (core-safe) |
|---|---|---|
| θ(0)=√2 (pilot, floor) | 5.5% | 2.8% |
| θ(0)=2 (rational, fiducial) | 9.5% | 5.3% |
| θ(0)=e (exp, ceiling) | 11.5% | 7.1% |

**Fiducial-kernel band ≈ 5–11% (up to ~13% at the plunger endpoint), model-independent cone ~4–15%.**
The banked **6–13% is confirmed** as the fiducial band. **KERNEL-HOSTAGE:** θ(y) is not derived by
the dS-Unruh foundation — only the cone endpoints (θ(0) ∈ [1,e], θ(1.5) ∈ (0.4,0.65)) are fixed.
**Footing:** at fixed dimensionless depth (a_in/a₀, a_ex/a₀) the fractional spread is **a₀-independent
to ~0%** (a₀ cancels); footing enters only via which physical member/radius maps to a given depth
(carrier classification unchanged, ~9% shell-radius shift). **NOT footing-hostage.**

### (2) Sign + the banked DATED SIGN-FLIP (D3 lane, DOI 10.5281/zenodo.21179352)
Baseline (settled band): high-ω_ex members shed adiabatic loading and run **hotter**; low-y members
run cooler. On top of that, the **memory kernel** makes the *felt* y a memory-weighted
y_eff = y_cur + (y_hist − y_cur)·e^(−t/τ_M) (τ_M ≈ 0.45 Gyr Lorentzian channel), producing the
**MI-unique sign-flip across pericentre:**

- **first-infall / pre-pericentre** (currently loaded, memory of the **cold** isolated past):
  **DEFICIT** (cooler than a settled twin at the same current y), ~−3…−10%.
- **recent post-pericentre / backsplash** (memory of the **hot** pericentre): **EXCESS**, ~+3…+10%,
  decaying exponentially with time-since-peri.

**Tides can only heat (never a deficit) and never flip sign; MG gives identical σ for all phases.**
The pre-peri deficit + sign-flip is the cleanest MI-unique tag. (Carry both memory times honestly:
the 0.45 Gyr Lorentzian channel drives the resolvable transient; the E10 covariant τ = 2c/a₀ = 203
Gyr governs the deep-adiabatic star-orbit lane — different channel, different observable.)

### (3) Structure vs infall phase y and cluster-centric radius
The spread **rises outward**, peaks at the **MOND-transition shell** a_ex ~ 0.3–1 a₀ (~R500–R200),
and **dies toward the core** — the **opposite radial slope to tidal heating** (which peaks toward
pericentre/core). This outward-rising profile is the **primary separator** from the same-signed
tidal confound (banked GAP E6). Orbit shape enters **only** through y: a radial plunger near
pericentre has large ω_ex (large y → sheds loading → hotter); a settled circular member at the same
radius has y ~ 0 (full adiabatic loading).

### (4) Dependence on cluster mass + member deep-MOND depth
- **Cluster mass** sets the shell radius R(a_ex=a₀) = √(GM/a₀) (0.39 Mpc at 10¹⁴, 1.22 Mpc at 10¹⁵ M⊙,
  canonical) and the crossing/memory time T_cross ~ 2 R/σ_cl ~ (1.0–1.8 Gyr = 2–4×τ_M → **memory
  transient is resolvable**). The **fractional amplitude at fixed depth is mass-independent** — mass
  moves the carrier zone outward and lengthens the memory window; it does not set the size.
- **Member deep-MOND depth sets the amplitude.** Only **diffuse** members (low ω_in) reach y ~ 1 and
  carry the 6–13%: UDG (σ=15, R_e=3) → ~14%, dSph (σ=10, R_e=1) → ~7%, whereas dE (σ=50) → 0.5% and
  L* ellipticals (σ=200) → 0.1% are **adiabatic-dead** (y≪1, internally Newtonian). The
  SDSS/DESI-σ-measurable members are exactly the dead ones — **that is the power wall**
  (banked `POWER_cluster_efe_channel.md`), not a limit of the prediction.

### (5) MG = EXACTLY 0 for this channel (theorem, field-sourced class)
Symbolically, d(σ_MG)/d(infall-phase y) = 0 identically (any a₀, any interpolation): the MG EFE is a
function of the current position only; infall phase labels the tracer and appears nowhere in the
internal dynamics. Airtight for the class {QUMOND, AQUAL, AeST/TeVeS, f(R), local-modified-g}. The
only evasion (disformal/Finsler-SME coupling to the tracer's own worldline) **is** modified inertia
in an MG costume — breaks WEP, cannot serve as a rival MG explanation.

### (6) Confounds (the whole isolation game)
Tidal heating (~2–8%), ram-pressure, environmental quenching all change internal σ and correlate
with infall phase and carry the **same sign** as the baseline MI excess. But: none flips sign, none
makes a pre-peri **deficit**, and tides have the **wrong radial slope** (peak in core vs MI rising
outward). Non-equilibrium/substructure is a potent same-signed false-detection route → needs the
DS-substructure cut + matched-pericentre PAIRs (banked power lane). The isolation is
**radial profile + pre-peri deficit + sign-flip + exponential-decay hysteresis**, not amplitude.

---

## Scope + caveats (honest, non-negotiable)

- **MI-CLASS-GENERIC, not framework-specific.** This discriminates MI-class (any history-dependent
  inertia) vs MG (=0 exactly). It does **NOT** discriminate this framework vs Milgrom's linear
  no-EFE MI (arXiv:2503.07106), which also produces a spread. It is an **MI-vs-MG** test.
- **Magnitude is kernel-hostage.** The 6–13% is the fiducial θ(y) band; the model-independent cone
  ~4–15% is the honest outer bound. **Existence + sign (+ sign-flip) + MG=0 are the theorem-grade
  claims; the amplitude is a band, not a derived number.**
- **a₀'s value and s = −1 are postulates.** No "proves" language for the framework.
- **Power:** underpowered today (banked `POWER_cluster_efe_channel.md`: ×290–1150 short at current σ
  precision; needs ELT/HARMONI ≤10% σ + phase tagging). This lane is the **prediction**, not a claim
  of confrontability.

---

## Credit
Milgrom 1983 (MOND) / 1999 PLA 253:273 (ν-kernel wellhead) / 2022 PRD 106 064060 (MOND as modified
inertia; Eq.34–35 two-frequency EFE, subsystem boost). Cluster kinematics + phase-space membership:
Rhee+2017 (infall-phase PPS diagram), Oman+2013, HeCS-omnibus, GalWCat19, Sohn+2017 (A2029). Banked
lanes reused: `prep_2026/sigma_spread/{rederive_mi_spread,mg_zero,power_analysis}.py`,
`reviews/residual_doors_2026_07/D3_*.py` (the sign-flip pre-registration).

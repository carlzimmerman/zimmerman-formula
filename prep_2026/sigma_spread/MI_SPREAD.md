# MI-PREDICTION LANE — the non-adiabatic orbit-history σ-spread, re-derived

**Date:** 2026-07-17 · **Script:** `mi_spread.py` (this dir, exit 0, both footings) · log `mi_spread.out`.
**Framework:** de Sitter–Unruh MODIFIED INERTIA (Zimmerman) — NOT standard MOND.
ν(y)=√(1+1/y), y=g_bar/a₀, a₀=cH_Λ/Z=9.36e-11; MI = inertia is a time-NONLOCAL functional of the
body's own worldline through the published covariant kernel K(□_u/a₀²), memory time
**τ_mem = 2c/a₀ = 2Z/H_Λ** (equation-book **E10**, EXACT, footing-free).
Milgrom 1983/1999 wellhead credit for the ν-kernel; distinctive content = the cH_Λ/Z coefficient
+ the MI completion. **a₀'s value and s=−1 remain postulates.** dSph kinematics: Walker, Wolf,
Battaglia; Gaia dSph proper motions.

---

## The observable (my task's mechanism, verbatim)

In a pressure-supported system at radius r, g_bar(r) is the **same** for every star. A *local*
modified-inertia μ(|a|) would give every star the same |a| → no spread. The MG-impossible effect
is **non-adiabatic**: a star on an **eccentric** orbit time-samples a **varying** |a| (large at
pericenter), so its orbit-history / memory-averaged effective inertia ⟨μ⟩ differs from a circular
orbit at the same energy — a **Jensen gap** over the curvature of the nonlinear ν. Different
orbital families (eccentricities) at the same radius therefore carry different effective inertia →
an intrinsic LOS-dispersion spread beyond anisotropy / projection / measurement error.

---

## (0) τ_mem vs τ_orbit — the question that sets the magnitude: **DEEP ADIABATIC**

| footing | a₀ | τ_mem = 2c/a₀ |
|---|---|---|
| canonical cH_Λ/Z | 9.36e-11 | **203 Gyr** |
| alt ρ_total/cH₀ | 1.13e-10 | **168 Gyr** |

τ_mem H_Λ = 2Z = 11.58 **exactly** (footing-free). Against real systems (T_orb ≈ 2πr/σ):

| system | τ_mem/T_orb (canonical) | regime |
|---|---|---|
| Draco / Sculptor / Fornax dSph | 1367× / 1086× / 544× | DEEP ADIABATIC |
| Crater II (diffuse) | 83× | DEEP ADIABATIC |
| NGC1407 elliptical | 1033× | DEEP ADIABATIC |
| Coma cluster | 22× | DEEP ADIABATIC |

**τ_mem exceeds every real orbital time by ~20× (clusters) to ~10³× (dSph).** Every pressure-
supported system is deep in the **adiabatic** regime. The kernel edge frequency a₀/2c = 1/τ_mem
corresponds to a period ~2πτ_mem ≈ 1275 Gyr, so every real orbit sits at ω_orbit ≫ edge (E13 |K|=1
pure-phase branch): the memory magnitude **saturates and freezes at the orbit-mean pre-history
fixed point**. **⇒ NO resonant amplification.** The orbit-history spread is the small residual
adiabatic Jensen gap — not a resonant estimate. *This is the crux, and it corrects the bank (below).*

## (i) The Jensen gap by direct orbit integration (exact ν, both footings)

Effective ν of an eccentric orbit vs circular at the same energy, integrated in the framework's
dressed force. Instantaneous (τ_mem→0, most non-adiabatic) case, bracketed by potential shape:

| e | ~0.06 | ~0.13 | ~0.25 | ~0.40 | ~0.58 | ~0.72 |
|---|---|---|---|---|---|---|
| **point-mass** (hard upper bound) Δν [dex] | −0.0002 | −0.0013 | −0.0044 | −0.0103 | −0.0187 | −0.0241 |
| … in σ | 0.03% | 0.15% | 0.50% | 1.19% | 2.15% | **2.78%** |
| **Plummer moderate-core** (realistic) Δν [dex] | −0.0001 | −0.0007 | −0.0022 | −0.0047 | −0.0071 | −0.0082 |
| … in σ | 0.02% | 0.09% | 0.25% | 0.54% | 0.82% | **0.94%** |

Sign **NEGATIVE**: eccentric orbits present a slightly **lower** effective ν (slightly cooler than
the naive circular expectation). Magnitude is **potential-shape dependent**: point-mass (no core,
sharpest pericenter) = hard ceiling ~2.8%; realistic cored dSph ~0.9% peak; strongly-cored <0.1%.
**Both footings identical to <1%** (a₀ cancels in the deep-MOND depth at fixed y).

**Independent cross-check — the committed 19/19-verified MI orbit integrator**
(`prep_2026/mi_integrator/`, which integrates *real* orbits through the *real* memory kernel in a
Plummer field): eccentric-orbit RAR offset **< 0.007 dex out to e≈0.9, sign negative**; isotropic
dSph ensemble **ν_eff/ν_circ = 0.990–0.997** (D_iso = −0.0014…−0.0045 dex). Its memory channel
(real kernel − instantaneous sampling) **adds only ~0.002 dex** at e≈0.86, same sign — **not**
resonant amplification, exactly as section (0) requires. The moderate-core sampling here reproduces
this to ~order and sign.

## (iii) RMS spread over a realistic eccentricity distribution

| distribution | FIDUCIAL (cored) RMS | UPPER BOUND (point) RMS | fiducial peak |
|---|---|---|---|
| thermal N(e)=2e (radial-biased) | 0.22% | 0.80% | 0.94% |
| uniform e∈[0,0.9] | 0.35% | 1.03% | 0.94% |
| mild e∈[0,0.6] (relaxed) | 0.31% | 0.71% | 0.92% |

**Honest RMS relational σ-spread ≈ 0.2–0.35% (fiducial), up to ~0.7–1.0% at the point-mass ceiling,
<0.1% for strongly-cored systems.** Peak single-orbit contrast (circular vs near-radial) ~0.9%.
**Maximized by** (deepest y — the most MOND-dominated diffuse dSph/UDG) × (radial-biased orbit
distributions); ellipticals/dE (y≫1, internally near-Newtonian) carry essentially none.

## MG = EXACTLY 0 (theorem, airtight within the class)

Any modified-**gravity** theory that (P1) sources a field g(x) from the baryons and (P2) moves
tracers as WEP geodesics of that field gives every star at radius r the **same** acceleration g(r)
regardless of its orbit → the orbit-**family** inertia spread is **EXACTLY ZERO** (QUMOND, AQUAL,
AeST/TeVeS, f(R), any local-modified-g). Orbit shape enters MG **only** through the distribution-
function anisotropy β(r) — a modelling choice, not an intrinsic per-orbit inertia. Symbolically
d(inertia)/d(eccentricity) = 0 for all a₀, all g(r), all e. Only a theory that makes inertia a
functional of the body's **own** worldline (i.e. modified **inertia**) opens a finite spread — so
the exact-0 is a genuine MG-vs-MI discriminant. (Retarded / velocity-dependent MG stress-tested in
`mg_zero.py`; none manufactures an orbit-family spread while remaining MG.)

---

## Verdict — does the banked 6–13% hold? **Corrected DOWN for this observable.**

- **The banked 6–13% is a DIFFERENT observable.** It is the two-frequency EFE **subsystem-boost**
  (Milgrom 2022 PRD 106 064060 Eq.34-class): how the *internal* dispersion of a whole subsystem
  (a cluster-member galaxy) is loaded by the external cluster field as a function of its **infall
  phase** y=ω_ex/ω_in. That is a quasi-static EFE contrast between infall phases, and it is
  **explicitly kernel-hostage** (the loading θ(y) is not derived; only the cone 5–18% is). It is a
  legitimate, distinct MG-impossible measurement — but **not** the star-orbit-within-one-system
  observable of this task. It remains as-banked (see `RECON.md`, `rederive_mi_spread.py`).

- **For THIS task's observable** (individual stars on different orbits inside ONE pressure-supported
  system), the honest re-derived magnitude is **sub-percent to ~1% in σ — an order of magnitude
  below 6–13%.** The correction is **forced** by section (0): τ_mem = 203/168 Gyr ≫ τ_orbit, so the
  memory freezes at the orbit mean and the resonant amplification a two-frequency estimate would
  need never occurs. The real-kernel MI orbit integrator confirms it directly (ν_eff/ν_circ =
  0.990–0.997). **Both footings shift the number <~20%.**

- **MG = EXACTLY 0** — clean, airtight theorem (this file + `mg_zero.py`).

- **Powering.** At ~0.2–1% the star-orbit discriminator is even more **underpowered** than the
  6–13% estimate implied: degenerate with velocity anisotropy β(r), projection, and per-star σ
  errors (≳10% today). **Not powerable with current data.** What would power it: a large,
  kinematically clean, per-star-precise sample of a single deep dSph (Sculptor/Fornax) with
  independent orbit-shape tags (Gaia proper motions + LOS) targeting the near-radial-vs-circular
  contrast where the effect peaks ~1% — **ELT/MICADO-class per-star velocities**.

**No "proves" language for the framework value/sign; the MG=0 statement is the only theorem-grade
claim and is labelled as such. Both footings shown throughout.**

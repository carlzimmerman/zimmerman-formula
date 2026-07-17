# SYNTHESIS — the relational σ-spread as the MI-vs-MG discriminator (2026-07-17)

*de Sitter–Unruh MODIFIED-INERTIA framework. g_obs = ν(y)·g_bar, ν = √(1+1/y),
y = g_bar/a₀, a₀ = cH_Λ/Z = 9.36e-11 (Z = √(32π/3) = 5.789). Milgrom-1999 wellhead
credit for the ν-kernel; distinctive content = the cH_Λ/Z coefficient + the non-local-in-time
MI completion (kernel K(□_u), τ_mem = 2c/a₀ = 2Z/H_Λ).*

This document closes the four-lane swing (MI prediction, MG-impossibility, observable design,
power) and applies the adversarial verifier's corrections. Four sibling docs carry the detail:
`MI_SPREAD.md`, `MG_ZERO.md`, `OBSERVABLE.md`, `POWER.md`; the audit is `VERIFY.md`. All lane
scripts exit 0, both footings (a₀ = 9.36e-11 canonical / 1.13e-10 alt).

---

## HEADLINE

The relational orbit-history σ-spread is the **cleanest MG-impossible discriminator the MI
program has in principle** — MG's field-sourced spread is an **airtight exactly-zero theorem
that survives a strong-anisotropy killer test** — but it is **UNDERPOWERED and not powerable
near-term**: the honest magnitude is **~0.2–1% in σ (an order of magnitude below the banked
6–13%, which was a different observable)**, and it needs both ~10⁵–10⁶ clean per-star velocities
in one deep-MOND dwarf AND a per-star 3D orbit tag Gaia cannot deliver.

---

## OUTCOME

**No powered MG-impossible test exists today. Verdict: UNDERPOWERED-NEEDS-X.**

**The magnitude (honestly re-derived, NOT assumed).** The decisive quantity is τ_mem vs
τ_orbit. τ_mem = 2c/a₀ = 2Z/H_Λ = **203 Gyr (canonical) / 168 Gyr (alt)** — exact and
footing-free (τ_mem·H_Λ = 2Z = 11.5776). Every pressure-supported system is **deep adiabatic**
(τ_mem/τ_orbit ≈ 22× Coma → ~1000× Draco/Sculptor), so the memory magnitude **saturates and
freezes** — there is **no resonant amplification**. The effect is the residual adiabatic Jensen
gap over the curvature of the nonlinear ν, sign **negative** (eccentric orbits present slightly
lower effective ν, run cooler):
- Fiducial cored dSph (real-kernel-matched): **RMS ~0.2–0.35% in σ**, peak single-orbit ~0.9%.
- Point-mass ceiling (sharpest pericenter, hard upper bound): **RMS ~0.7–1.0%, peak 2.8%**.
- Strongly-cored / ellipticals (y≫1): **<0.1% (~0.08%)** — essentially none.
- Maximized by deepest-MOND depth (diffuse dSph/UDG, y~0.15) × radial-biased orbits; at
  transition depth y=1 the effect is ~⅓ of the y=0.15 value. **Both footings identical to
  <1%** (a₀ cancels at fixed depth y).

This **corrects the banked 6–13% DOWN by ~an order of magnitude**: that number is a *different*
observable — the Milgrom-2022 EFE subsystem-boost (how a whole cluster-member galaxy's internal
dispersion is loaded by its infall phase), which stays valid on its own (`POWER_cluster_efe_channel.md`).
For the star-orbit-within-one-system observable, τ_mem ≫ τ_orbit forces sub-percent to ~1%.

**The clean, anisotropy-immune observable.** The isolating statistic is
**dlnM = ⟨ln M(r)|radial-tagged − ln M(r)|circular-tagged⟩** — the enclosed-mass consistency
across eccentricity-tagged orbit families, each M(r) from the spherical Jeans equation using the
subsample's OWN measured ρ, σ_r, β. With 3D velocities β is *measured not fit* (mass-anisotropy
degeneracy broken outright), and MI multiplies (v_r, v_t) by the same per-orbit factor f(e),
which **cancels in β = 1 − σ_t²/2σ_r²** and surfaces only in the mass normalization M ~ f²σ_r² —
so it is orthogonal to the anisotropy sector by construction. **Killer test passed:** a proper
steady-state DF with strong radially-varying anisotropy (β: +0.13→−0.72, Δβ~9, NO MI) keeps
dlnM at the **+0.033 MG zero-point** and does NOT reach the MI signal — the discriminant is
**genuinely not re-labeled anisotropy**. MI drives dlnM **negative** (amp sweep 0→8: +0.045 →
−0.072; fiducial cored differential ~−0.02). MG gives exactly 0 field-sourced spread for any β(r),
any a₀, any interpolation.

**The MG-impossibility (the sole theorem-grade claim).** Every theory in the class
{QUMOND, AQUAL, AeST/TeVeS, f(R), local-modified-g} obeys (P1) sources a field g(x) + (P2) WEP
geodesics of one Jordan metric ⇒ a test body's acceleration is position-only; orbit shape y,
velocity v, and history label the tracer and appear NOWHERE in the internal dynamics. Hence
**dσ_int/dy ≡ 0**, verified symbolically (d(v²)/dL = 0) and numerically (ptp = 0 across both
footings × 3 interpolations). The only evasion (C3/C3′: a disformal/Finsler-SME coupling to the
tracer's own worldline) is **definitionally modified INERTIA in an MG costume** — it breaks WEP
and cannot rescue MG as a rival; a detected spread *is* the inertia physics whatever it is named.

**Best system + S/N.** Real single-system perfect-tag z < 0.5 everywhere; **best realistic-tag
z ≈ 0.05** (a single deep dSph with HST/JWST 3D on ~300–500 stars). Fisher floor (MC-validated,
analytic vs score-MC <2%, √N scaling 1.99): **N₃σ ~ 7e4 (1% ceiling) to ~6e5 (0.2% fiducial)**
clean per-star LOS velocities *with a perfect tag*; with the realistic tag D~0.3–0.4,
N₃σ ~ 5.6e5–5.2e6. Real reservoirs fall 10²–10⁶ short (Fornax 2600, Sculptor 1500, Draco 700;
diffuse deepest-y Crater II/Antlia II only 150–200 — amplitude and count pull *opposite*). No
existing dataset bites (Walker+2009, Gaia DR3, MaNGA/ATLAS3D, Coma). **Both footings shift
N₃σ <44% — not footing-hostage.**

---

## VERIFIER CORRECTIONS APPLIED (both toward more caution)

1. **"β-immune" → "β-immune for equilibrium DFs only."** The dlnM zero-point is
   **DF-shape-dependent at signal size** (+0.009→+0.062 across global anisotropy; MI fiducial
   differential only −0.022), so clean isolation additionally requires a forward DF model
   (Schwarzschild / M2M) and the post-calibration residual is *not* shown to be sub-signal.
2. **A same-signed, MI-signed FALSE-detection route exists.** Beyond tidal heating (C6, ~2–8%,
   grows to core, separable by radial profile), **non-equilibrium / substructure** is potent and
   under-guarded: a radius-correlated non-steady-state population mix (no MI) drove
   **dlnM = −0.71 ≈ 35× the real MI signal**. So "MG = 0" is precise for the *field* channel, not
   for the *total observable*: substructure/non-equilibrium can manufacture the MI sign. The
   practical systematic floor is set by equilibrium + tagging fidelity, not the optimistic
   ~0.02 estimator zero-point.

---

## THESIS

Post-lensing-no-go (lensing became shared-MG, DOI 10.5281/zenodo.21418816), the σ-spread is the
**correct kind of test** the MI program needs — a genuinely MG-impossible observable with an
**exact field-sector baseline that resists equilibrium anisotropy** — but it is **NOT a
confrontable test today and not near-term**. Two independent walls, either fatal: (i) the honest
magnitude is ~0.2–1% (not 6–13%), demanding N~10⁵–10⁶ clean per-star velocities in a single
deep-MOND dwarf; (ii) the per-star 3D eccentricity tag does not exist where the counts are
(Gaia internal PM S/N ~0.03–0.05 = bulk only). A same-signed substructure/non-equilibrium
confound can additionally manufacture the MI sign, so even a marginal future detection needs a
forward equilibrium DF model to defend. It is a **real discriminator, honestly demoted in
practice** — the distinctive front the program should *point to in principle* but cannot *cash
now*. The nearer-powerable sibling remains the **cluster-member EFE subsystem-boost** (distinct
observable, 5–18% cone), not this star-orbit spread.

---

## WHAT POWERS IT (X)

Both required, neither exists: **(i)** ~10^4.5–10^5.5 clean (<~5% per-star) LOS velocities in a
single diffuse deep-MOND dSph/UDG (Sculptor/Fornax + the deepest-y diffuse systems) from a
30 m-class campaign (ELT/MICADO, MSE) — only the ~1% point-mass-ceiling corner is within ~1–2
orders; the 0.2–0.35% fiducial needs ~10^5.5–10^6, out of reach — **PLUS (ii)** a per-star 3D
orbit/eccentricity tag from multi-epoch space astrometry well beyond Gaia's per-star precision
(HST/JWST/Roman-class internal PM), **PLUS (iii)** a forward Schwarzschild/M2M equilibrium DF
model to calibrate the DF-dependent zero-point and reject the non-equilibrium/substructure mimic.

*a₀'s value and s = −1 remain postulates. MG-field = 0 is the sole theorem-grade claim. No
"proves" language is used for the framework.*

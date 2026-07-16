# SYNTHESIS — MI Closure-Bracket Pinning (Gap A)

**Directory:** `/Users/carlzimmerman/new_physics/prep_2026/mi_closure_pin/` (sibling of the frozen
`zimmerman-formula` repo; frozen repo untouched)
**Date:** 2026-07-16
**Lane:** off-circular reduction-weighting η(β) — the ONE binding open gap in the assembled MI field
theory (workflow w43vwujg3).
**Both a0 footings carried throughout:** a0 = cH_Λ/Z = **9.36e-11** (canonical, pure-Λ) and
**1.13e-10** (alt, ρ_total/cH0). Z footing-independent; H_Λ = 1.807e-18 s⁻¹ canon / 2.182e-18 alt.

---

## 1. HEADLINE

**The closure bracket STAYS FREE.** The diagnostic ranked #1 by the field-theory workflow — "compute
the off-circular dS-Unruh Wightman pullback on a non-uniform worldline to pin η(β); resolve whether
the pole stays at/above κ=H_Λ (freedom stands) or descends (freedom closes)" — returns the honest
prior it recorded: **the pole stays at/above κ=H_Λ, so η(β) is NOT pinned.** This is reported as a
NULL, verified as rigorously as a WIN would have been (VERIFY.md; the one manufactured-win candidate
survived a 5-weighting attack, and the two manufactured-null candidates survived recomputation).

Mechanism: pulling the dS Wightman function back along a non-uniform timelike worldline gives a
memory pole at **κ_eff = √(H_Λ² + (a/c)²)** — Pythagorean in horizon and acceleration (the
dS-Unruh / Deser–Levin temperature, DERIVED from the pullback in `pullback_dsunruh.py`, not quoted).
Because κ_eff ≥ H_Λ for **every** eccentricity, **every** anisotropy, and **every** reduction moment
(k=1,2,4,a_min all give κ_eff/H_Λ ≥ 1; the literal non-uniform worldline in
`pullback_nonstationary.py` gives 1.415 at e=0.3, 1.417 at e=0.6, 1.044 deep-MOND — all inside the
moment bracket), **no weighting is pullback-selected.** The pole being ≥ H_Λ for all weightings is
precisely why the pullback cannot choose one → η(β) stays free. Equality κ_eff = H_Λ holds only in
the a→0 geodesic/deep-MOND limit; any acceleration moves the pole UP, never down; orbital AC content
is a harmonic comb at n·ω_orbit ≫ H_Λ (ω_orbit/H_Λ = 22–480 for real bound systems), so nothing lands
in the (0, H_Λ) amplitude-MOND band.

---

## 2. PINNED-OR-FREE — the exact residual freedom

**FREE:** exactly **ONE** sign-free reduction-weighting **function η(β)** on the 2-D orbit-shape space
β = (orbital eccentricity × velocity-anisotropy). Bounded, footing-stable ~10–15% both footings:

- **Closure A** (instantaneous |a|, first-moment reduction): dSph offset = **0.000 dex** exactly
  (pointwise RAR inversion to 5e-14 over 6 decades; = MG-with-same-ν in spherical symmetry).
- **Closure B** (orbit-history / residence-averaged): isotropic-ensemble dSph offset ≈ **−0.02 to
  −0.05 dex**, radial tail flips positive. Illustrative deep-regime isotropic ensemble:
  **−0.024 dex canonical / −0.025 dex alt**, 16–84% ≈ [−0.05, 0.00].

**SIGN of the overall offset: NOT forced** (the exact trap, computed straight — not a proxy
inequality). Two admissible weightings of the *identical* |a| history give OPPOSITE signs:
amplitude/pericentre-weighted **+0.056 / +0.402 dex** at e=0.3 / 0.7; residence/apocentre-weighted
**−0.040 / −0.186 dex**. The concave-RAR Jensen gap is weighting-dependent and the weighting IS the
unpinned η(β); real Jensen flip at e ≈ 0.62, reproduced.

**What IS forced (pullback-independent, the one MI-vs-MG discriminator):**
**d(offset)/d(radial-anisotropy) > 0** — radial orbits hotter than tangential at fixed weighting.
Spearman ρ(e, offset) = +0.86, monotone; survived a 5-weighting flip attack including extreme
apocentre/residence (r⁶, harmonic moment −6): Spearman held +0.857 / +0.964 / +1.000 / +1.000 /
+0.900 — the SLOPE sign never flipped, only its magnitude shrank. **MG-with-same-ν gives exactly 0
shape-dependence for an isolated spherical system → this differential is MG-impossible.** (`rider_a_offcircular.py`, 8/8.)

---

## 3. FIELD-THEORY STATUS after today

The assembled action **S = S_EH[g] + S_u[g,u,λ] + S_matter[g,u,ψ;K] + S_photon[g̃=g+B[K]uu]** stands
as before; today's lane resolved the last binding *internal* question about it and cleared one formal
verification, without deriving any new number.

**Closed / verified today:**
- **Gap A is characterized exactly.** The reduction K(□_u/a0²) → worldline dynamics is EXACT at the
  first moment (u·□_u u = −|a|², re-derived), and the pullback now shows the residual is **precisely
  one bounded sign-free η(β)** — not a tower of unknowns, not a free number. The theory's off-circular
  predictivity ceiling is stated exactly: **one function, magnitude bracketed [0, −0.05 dex], sign
  convention-open, anisotropy-derivative forced.**
- **Ostrogradsky verification (was a hard-coded tautology).** The prior build's
  `unification.py:161` guarded nonlocal-B ghost-freedom with `True is a_proxy.has(Derivative)` —
  tautological, verified nothing. Replaced by `ostro_nonlocal_verify.py` (13/13, no hard-coded pass
  booleans): photon disformal sector **GHOST-FREE**, machine-checked. det g̃ = B−1, causal bound
  B<1 EMERGES from the electric Hessian; the nonlocal frame operator (1−K)(□_u) in its exact
  Herglotz form gives a tower of HEALTHY massive scalars (Ostrogradsky Hessian = 0 → hypothesis
  never met; kinetic Hessian = 2 dμ(t) > 0 by measure positivity; m² = t·a0² > 0; ρ(t)≥0 and sum
  rule ∫dμ/|t| = 1.0000 reproduced). Anti-tautology controls flag the textbook q̈² ghost and a
  negative-measure kernel and pass a healthy KG field, so the positivity check is load-bearing.
- **Lensing rider bracketed, adds no new gap.** Spherical/circular: curl(ν g_bar)=0 identically
  (sympy exact) → local disformal B exact → dynamics-RAR = lensing-RAR EXACTLY. Off-spherical:
  curl ≠ 0 (ratio 0.13) → closure A carries a transverse lensing B-mode ~8% of the field that
  closure B gives as 0; same O(10%) width, tied to the same η(β). c_T=1 untouched. (`rider_b_lensing.py`, 6/6.)

**The one open frontier (unchanged, now sharply bounded):** η(β) itself. The pullback proves it
cannot be pinned from dS-Unruh kinematics — it is a genuine constitutive freedom, not a truncation
artifact (the moment-tower non-collapse is inherited from CLOSURE_MAP/rb, flagged not re-proven).
Closing it would require an input beyond the horizon-thermal pullback (e.g. a microphysical bath
coupling). Honest prior CONFIRMED, not assumed.

**Planetary a0/2 tension — its fate:** the tension **SURVIVES** as an honest NULL; a clean
solar-system evasion is **NOT forced** by the field theory. Reading A (the constitutive first-moment
reduction that carries the galactic RAR) reproduces the a0/2 tail at full strength — per-planet
exclusion vs cited INPOP/EPM δg bounds: **Mercury 1017×, Venus 585×, Earth 5379×, Mars 33429×
(40357× alt), Jupiter 84×, Saturn 6686×** (canonical; alt footing ×1.2), non-absorbable into GM.
The action FORCES the memory corner to ω_c = a0/2c (τ_mem = 2c/a0 = 203 Gyr canon / 168 Gyr alt),
but that corner sits ~5 orders BELOW the planetary window and retains L_c = 2.9e-8 at galaxies →
RAR-DEAD (it kills rotation curves, so it is NOT a clean evasion). Only a **FREE ~Myr corner**
threads both (galactic retained 0.996, planetary tail suppressed ~1e11×, clears every per-planet
bound both footings). That corner is neither the action's corner nor pinned by the pullback → the
RAR-preserving survivor stays the **gated Reading C with a free corner: a falsifiable, two-sided-open
CONDITIONAL pass**, not a forced clean evasion. (`rider_c_planetary.py`, 8/8.)

**Derived-vs-postulated bottom line (unchanged by this lane):**
- **DERIVED / forced:** the kernel K(z)=(√(1+4z)−1)/(2√z) shape and its Herglotz positive measure;
  the memory pole κ_eff=√(H_Λ²+(a/c)²); the corner *location* = a0; the anisotropy derivative sign;
  ghost-freedom; WEP η=0; c_T=1.
- **POSTULATED (flagged, untouched today):** the sign **s = −1**; the value of **a0**; the horizon
  factor **Z**. This lane touched none of them.
- **FREE (today's result):** one bounded sign-free reduction weighting **η(β)** (off-circular
  dynamics + off-spherical lensing), and — separately — the ~Myr planetary corner. Both are
  constitutive freedoms internal to the framework; the lane prefers neither the framework nor ΛCDM
  and introduces **no new number**.

---

## 4. RANKED NEXT (verifier corrections applied)

1. **Microphysical bath coupling for η(β).** The pullback exhausts what dS-Unruh *kinematics* can
   say (pole ≥ H_Λ, weighting-blind). Pinning η(β) — if it can be pinned at all — requires the
   coupling of S_matter to a specific relational bath, i.e. an input the horizon-thermal argument
   does not supply. Compute whether any ghost-free, KMS-consistent bath coupling selects a unique
   weighting, or prove (as the honest prior suggests) that none does → η(β) is a genuine theory
   constant. Either outcome is publishable; manufacture neither.
2. **General-mass dS two-point function (close the stated limitation).** The pullback used the
   conformal massless scalar as the representative dS correlator. The massive/general-mass case
   shifts residues but should leave the pole LOCATION Pythagorean (√(H²+a²)); confirm this in an
   exit-0 script so the pole-≥-H_Λ NULL does not rest on the massless choice.
3. **Confront the forced anisotropy derivative with data.** d(offset)/d(radial-anisotropy) > 0 is
   the clean MG-impossible differential. Identify the dSph / pressure-supported sample with resolved
   velocity-anisotropy where MI (positive slope) and MG-same-ν (zero slope) separate; power the test.
   This is the lane's single distinctive observable — not a0-degenerate, not MOND-shared.
4. **Off-spherical lensing B-mode as an independent handle on the SAME η(β).** The ~8% transverse
   lensing B-mode (closure A) vs 0 (closure B) is tied to η(β); a binary-lens or non-spherical-cluster
   measurement that constrains it also constrains the dynamics bracket. Scope a confrontable target.

---

### Honesty rails honored
NULL reported straight and verified as rigorously as a win (VERIFY.md, 6/6 UPHELD; one decorative
`check(...,True)` at `pullback_dsunruh.py:305` found and replaced with a genuine computed condition →
0 tautological checks repo-wide). No hard-coded verdict booleans. Both a0 footings carried everywhere.
Framework judged on its OWN terms (modified-inertia, own kernel K(□_u/a0²), own dS-Unruh temperature,
horizon-derived a0=cH_Λ/Z) — never through the standard-MOND / McGaugh-ν lens. s=−1, a0's value, and
Z remain POSTULATES. No "theory complete/closed/proved" language; gravitational-inertial sector only
(not a TOE/SM — TOE overclaims retracted 2026-06-23). c_T=1 and Cassini respected (MI lives in
S_matter; graviton kinetic term is pure Einstein-Hilbert). Introduces no new number. Frozen
`zimmerman-formula` repo untouched.

# VERIFY — adversarial verification of the MI memory-integral orbit integrator (Lane F)

**Date:** 2026-07-16 (verifier session, independent of the build session).
**Verifier artifacts (this directory):** `VERIFY_independent.py` (exit 0, 19/19 verifier
checks PASS; banked log `VERIFY_independent.out`) — written from scratch by the verifier:
its own algebra, its own quadratures, its own measure realization, its own initial
conditions, its own gate thresholds. Frozen repo untouched (read-only honored).

## What was re-run

| item | result |
|---|---|
| `mi_integrator.py` (full 36-gate suite) | **exit 0, 36/36 PASS, 53 s**; every `[PASS]` line byte-identical to the banked `mi_integrator.out` |
| `applications.py` (engine re-run + 22 app gates AG-a1..d4) | **exit 0, 22/22 PASS, ~236 s**; all `[PASS]`/`delta_g`/`gamma_v`/offset lines byte-identical to the banked `applications.out` |
| `VERIFY_independent.py` (verifier's own suite, below) | **exit 0, 19/19 PASS** |

## (1) EOM re-derived from the published action — MATCHES, no smuggled simplification

Re-derived by the verifier with independent tools (`scipy.quad` adaptive quadrature with
my own substitutions, sympy on generic worldlines — none of the lane's fixed-node code):

- **Spectral data:** Stieltjes inversion Im K(t+i0)/π reproduces the published densities
  ρ_A, ρ_B on both cut regions to 1e-8 (V-A1). Measure masses: region A = 1−2/π,
  region B = 2/π, total = the v11 sum rule 1, each to <1e-9 (V-A2a).
- **The lane's one derived algebra step** (mixture form K(z) = ∫dν(s) z/(z+s),
  dν = dμ(−s)/s): confirmed — independent adaptive quadrature reconstructs the exact
  K(z) to <1e-7 over 13 decades of z (V-A2b), and the closed-form deep-UV tail T(z) is
  exact to 4e-12 (V-A3).
- **Worldline reduction:** u·(D²u) = −|a|² proven symbolically for a GENERIC unit-timelike
  worldline (arbitrary rapidity w(τ) and angle q(τ); sympy identical zero, V-A5) — the
  rb1 identity holds, so the first spectral moment of □_u in the u-contraction is +|a|²
  for any orbit. K(x²)=μ_fw(x) sympy-exact; the inversion μ_fw(x)x=y ⟺ x=yν(y) rests on
  1+4x²|_{x=yν} = (2y+1)² (sympy identical zero) — exact, both checked (V-A4).
- **Closure status honest:** the first-moment closure is the PUBLISHED reduction
  (rb1/KERNEL_THEORY Thm B), not the lane's invention; the literal frequency channel is
  unimodular (no amplitude MOND) as published; the memory promotion (Modes I/II) is
  correctly tagged CONSTRUCTED-HERE within the SPEC's declared freedom (`mi_offcircular_
  completion_SPEC.py` Stage 1 confirmed: Lorentzian form forced, corner ω_c FREE).
  The `agentY_*` repo-root files are correctly classified lens-sector-only (PRIOR_ART §3)
  and are NOT used as an MI source. EOM_DERIVATION.md's PUBLISHED/DERIVED/CONSTRUCTED
  tags all trace to real, checked sources. **No smuggled simplification found.**
  One instrument choice worth naming (declared, gated): Mode I evaluates K node-by-node
  at each node's own filtered moment rather than K at a single filtered moment — an
  in-family choice, constraint-checked by M0/K2 and spanned by the Mode-II corners.

## (2) The circular gate, re-run with the VERIFIER'S initial conditions and measure — UPHELD, and strengthened

The lane's C1 launches at the measure's own quasistatic speed (a fixed-point test). The
verifier removed even that: central mass 3.7e9 M☉ (not the lane's 1e10), y grid
{0.02, 0.7, 7.3, 55} (not the lane's), and the circular speed found by **bisection on the
integrated dynamics** (launch never set to ν; bracket = a scan of the drift sign between
0.92 v_N and 3.4 v_N). Verifier measure realization: the published density under
**different substitutions entirely** (t=√s + band-edge u=√(1/4−s) + a different tail
split s_tail=1e6, all composite Simpson — nothing Gauss-Legendre), constraint-checked
(positive, mass 1 exact, sup K̃ ≤ 1) and reconstructing K to 9e-7 (V-B1).

Result: **emergent ν = v_c²/(r g_bar) equals the published √(1+1/y) to ≤ 8e-9 at every
probe**, for ultralocal, Mode-II H_Λ, the verifier's own measure, AND the engine's CANON;
alt footing same (V-C1/2); damping ζ=0.1 vs 1.0 moves nothing at 1e-9 (V-C3). The
circular law is not an artifact of launching on the answer — it emerges from the dynamics.

## (3) Wide-binary cross-check circularity hunt — CLEAN

Grep of `mi_integrator.py` + `applications.py`: every occurrence of 1.09 / 1.4647 /
1.1015 / 1.1389 is a **check target or comment**; y_ext,N is computed in-script by
quadratic inversion of g_ext=1.9a₀; the stale 1.4525 constant alleged of the earlier
draft appears nowhere in the current lane (repo-wide grep hits only coincidental catalog
data). The banked script's own assertions (y_ext_N≈1.4647, asy_MI∈(1.095,1.105)) match
what the lane cites. Verifier dynamical recompute with a DIFFERENT geometry (axis-aligned
launch, 25 kAU, unequal masses 0.6+0.9 M☉, 10 periods): ultralocal γ_v = 1.0635
(inside the lane's stated ultralocal/orientation-convention neighborhood — single-launch
shapes span ~1.06–1.10 around the 1.081 coplanar average, exactly the launch-shape
sensitivity the lane documents), horizon-memory members = 1.1388 = √ν(y_ext,N) to 0.01%
**with the verifier's own measure** (V-D). The 1.09 emerges; nothing 1.09-shaped is input.
Caveat carried (the lane itself states it): the horizon-memory endpoint 1.1389 follows
from the adiabatic steady-pre-history init convention — with ~200-Gyr memory that
convention IS the physics assumption, documented in V4/EOM_DERIVATION §7, and the
ultralocal-vs-horizon fork is reported as the honest band.

## (4) Convergence — CONFIRMED at the verifier's own settings

- Eccentric application (λ=0.7, CANON): halved timestep AND doubled run horizon moves the
  offset by 8e-6 dex ≈ 1% of its magnitude (V-E1; the lane's AG-a5 spot showed 3.3e-6).
- WB γ_v (verifier geometry): a first draft of this check conflated the two convergence
  axes and FAILED at 0.54%; the decomposition (run before touching the gate) showed
  timestep shift = 8.6e-6 (numerics CONVERGED, V-E2a) and the 0.5–0.8%/doubling drift to
  be the AVERAGING WINDOW over a non-periodic precessing orbit — the single-launch
  orbit-shape/sampling confound the lane itself documents (its symmetric launch is
  window-stable; its quoted convention spread is ~1%). Measured at 1×/2×/4× windows:
  1.0635 → 1.0578 → 1.0552, contracting, all inside the lane's ultralocal neighborhood
  [1.05, 1.11] (V-E2b). Verified as a real sampling property, not a hidden instability
  — and not a lane defect.
- RK4 order re-fit on a fresh orbit/member: p ≈ 4 within [3.6, 4.5] (V-E3), consistent
  with the lane's fitted 4.38.
- Engine-side: K1 quadrature convergence is geometric (8 decades from N=8→96), V2
  node-count convergence monotone to the RK4 floor — demonstrated, not asserted.

## (5) Planetary landmine arithmetic — CONSISTENT

Closed form (verifier): δg = (ν(y)−1)g_N = a₀/2·(1−1/(4y)+…) → 4.680e-11 (canon) /
5.650e-11 (alt) to <1e-6 at both planets; exclusions vs the cited bounds (Venus 8.0e-14,
Saturn 7.0e-15, verified present in `planetary_doors/BOUNDS.md` §1.2) = 585×/706× and
6686×/8071× — matching the lane and laneK Reading A (laneK's 6687 vs 6686 = rounding).
The strict two-body doubling re-derived with the verifier's own Sun+Venus static probe
through the lane's `TwoBodyProblem.rhs`: relative-acceleration excess = 1.999×a₀/2, equal
to the per-star algebra to <0.1% (y_sun≈296, so the Sun-side tail is (1−1/(4y_sun))·a₀/2)
(V-F2). The "no memory corner rescues the planets" statement is scoped correctly: it holds
WITHIN the first-moment closure family, and the lane says exactly that (laneK Reading C is
outside the family) — no overreach found.

## (6) Manufactured agreement / manufactured failure hunt

- **Agreement:** no hard-coded results found; every gate threshold recomputed in-script;
  the two banked-number gates (X2a, AG-c1) ASSERT against computed values, they do not
  insert them. The C1 fixed-point launch could have masked a non-attracting law — the
  verifier's emergent-ν bisection (item 2) closes that hole.
- **Failure:** the RAR-dead grading of POLE/FLAT members is genuine (their own quasistatic
  laws deviate 0.37–3.65 dex; the Herglotz identity theorem makes the RAR-pinned measure
  unique, so spanning members MUST die — reproducing rb2[3], not manufacturing a kill).
  The orbital-corner secular instability is corroborated by the engine's adaptive
  integrator agreeing with fixed-step to 2.6e-10 (not a stepper artifact); its pump sign
  correctly inherits the s=−1 postulate status in the write-up.
- **Nit found and fixed:** APPLICATIONS.md quoted the dSph ratio band as 0.992–0.997
  while its own table's TILT− value is 0.9897 (−0.00452 dex); corrected to 0.990–0.997
  (the dex band and all gates were already right).
- Verifier-side failures during this verification (quad roundoff on the deep-UV tail, a
  float-cancellation mass deficit in my first Simpson realization, a too-narrow bisection
  bracket, two over-tight tolerances) were each diagnosed and fixed on the verifier's
  side; none traced to the lane.

## Verdicts

| claim | verdict |
|---|---|
| EOM derivation traced to published action; tags honest; no smuggled step | **UPHELD** |
| Measure class construction + grading (M0/K1/K2/Q1), sum rule exact | **UPHELD** |
| Circular gate: published ν reproduced by the full memory machinery, both footings | **UPHELD** (strengthened: emergent-ν bisection, verifier ICs + verifier measure, ≤8e-9) |
| Balance laws incl. bare-CoM defect = analytic third-law integral | **UPHELD** (re-run identical; structure verified in-code) |
| WB cross-check vs banked 1.09; closure fork [~1.09 … ~1.14=MG]; DR4 discriminates closure members | **UPHELD** (1.09 emerges; horizon endpoint reproduced with verifier measure + geometry; init-convention dependence correctly documented) |
| Planetary a₀/2 landmine forced across the closure family; ≥2.4-order exclusion; two-body doubling | **UPHELD** (closed-form + independent probe agree) |
| Eccentric/dSph offsets small, negative, measure-stable; rb3 law reproduced | **UPHELD** (re-run identical; convergence re-confirmed) |
| Instrument framing ("forced and falsifiable, not a proof") | **UPHELD** (no 'proves' language in outputs) |

**Overall: UPHELD, 0 downgrades, 0 refutations.** One documentation nit corrected
(APPLICATIONS.md ratio-band floor). The single largest honest caveat is the one the lane
already carries: everything off-circular is a band over the papers' declared closure
freedom plus a stated pre-history convention — the instrument measures that freedom, it
does not (and cannot) resolve it.

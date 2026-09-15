# G03 — the covariant action that clears Cassini: the spec for the swarms (2026-09-15)

**Contract owner:** astra's roadmap, `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_ROADMAP_2026-09-04.md`, §"G03 — Supply an actual covariant action", and its handoff `closure_2026/FABLE_HANDOFF_2026-09-04.md`. This document turns that contract into a swarm work order. Where the two disagree, the roadmap wins. Never edit astra's files; write your own lane files and cite.

## 0. Why this lane and nothing else

Every relativistic completion this programme has built died on one of three gates, and the one every modified-gravity candidate shares is Cassini: the kernel's gentle approach μ → 1 at g ≫ a₀ leaves an external-field quadrupole at Saturn 3.8–5.5× (exact exponential AQUAL, g01) and 6.44×/7.63× (the data-selected μ₂, L243) above the Park 2026 ceiling. The k⁴ PPN gate (f31/f31b/f31c) has already sorted the escape routes: every **local** fourth-order operator makes α₁ grow as (ξk)² and dies (G030 scalar trace, G034 Hessian², G032 aether biharmonic, H004→H006), while a **coherent stiffening of the whole Y sector**, J_Y → J_Y(1 + ξ²k²) including its aether/metric mixings, gives the propagator form that evades the lock at c₁₄ > 0. Statically, the double-filter extension T-B survives with screening floors ξ ≥ 0.02 pc (Gaussian) / 0.03 pc (Helmholtz) and discs untouched (< 0.2%) (g02). **G03 is the action that realises that stiffening covariantly.** Nothing else on the board is both unrun and decisive.

## 1. The target, stated once

One physical metric for baryons, photons and clocks. Static weak-field limit on the stated branch: the programme's kernel law ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b with μ the exact exponential (Track A) **or** the data-selected μ₂(x) = 1 − (1 + x/2)⁻² (both bare kernels fail Cassini by the same mechanism; a lane runs both). Both a₀ footings always: 9.3619e-11 (canonical) and 1.1279e-10 (alternative). Reference targets from the roadmap: N_grav = 2, Φ = Ψ, γ_PPN = 1, β_PPN ≈ 1, α₁ = α₂ = α₃ = 0, ∇_μT_m^{μν} = 0, c_T = c, viable FLRW, controlled k = 0 and zero-field limits, no hidden auxiliary propagator, no fixed preferred structure presented as a dynamical field.

## 2. The gates, in the order they are run (cheap kills first)

Every gate states measurement and threshold separately, prints PASS/FAIL/OPEN with its assumptions, has no literal-True condition, runs both footings, and is one commit. A FAIL is a result. Do not proceed to a later gate on a FAIL.

| # | gate | instrument (already validated) | pass condition |
|---|---|---|---|
| S1 | **static reduction** | sympy | the action's own field equations, reduced on the static branch, give the target law plus a stated correction of order (ξ∇)²; the modified source is derived from the action, not postulated |
| S2 | **Cassini quadrupole** | `hunt_2026/g01_strict_aqual.py` (FD-in-ln r × Legendre) cross-checked against `fable_independent_2026/L243_onefunction_cassini_quadrupole.py` (two schemes must agree to 0.1%; BN11 anchor to 1%) | |Q₂| at Saturn ≤ the Park 2026 ceiling (L243: canonical 3.347e-26 s⁻² is 6.44×, so the ceiling is 5.20e-27 s⁻²) on both footings, at g_ext and g_ext − 1σ; report the ratio, not "passes" |
| S3 | **galaxies untouched** | the L232/L259 SPARC pipeline (155 curves, same cuts) | pooled RAR rms at n = 2 moves by < 0.005 dex; rotation-curve change < 0.2% for r > 0.1 kpc (g02's disc gate); the screening length must be ≥ the T-B floors 0.02/0.03 pc and ≤ 100 pc |
| S4 | **wide binaries** | `prep_2026/gaia_dr4_prep/` pipeline (registered Amendment 11; do not edit the pre-registration) | the action's γ_v at 2–30 kAU printed and placed against the registered arms (A band 1.16–1.23; B ceilings 1.0450/1.0300); an action outside both arms is a FAIL by registration |
| S5 | **lensing** | the slip: Φ = Ψ derived from the action's metric | light sees the same potential as dynamics (L241: a conformal-only scalar is lensing-dead; L248/L257: the KiDS relation sits on the square-root branch at 35 kpc–3 Mpc with amplitude ≈ 2× a₀ and no turn) |
| P1 | **PPN ladder** | the f31c ladder (`hunt_2026/`) applied to the candidate's own quadratic form, not the AeST host's values imported | α₁, α₂ at the c₁₄ > 0 evasion form; report against |α₁| < 4×10⁻⁵, |α₂| < 2×10⁻⁹ (Will 2014); γ − 1 < 2.3×10⁻⁵ |
| P2 | **causal screen** (roadmap G03 bullet) | analytic | name the channel the filter modifies and show no instantaneous signal; unresolved → OPEN, decisive obstruction → STOP |
| P3 | **mode count** | Dirac/ADM sketch (full count is G05) | declare N_grav = 2 plus every auxiliary mode with its sign; a ghost (Ostrogradsky/Pais–Uhlenbeck) in the stiffening sector is a FAIL, not a footnote |
| C1 | **cosmology screen** | `fable_independent_2026/L180_*` growth solver; H002/G038 background | FLRW background w = −1 within Planck; growth inside the registered +1–4% band at z < 2; no k⁴ instability on the forest scales (L224/L225: reach ≥ 3.2×10⁴) |

S1–S3 cost minutes and kill most candidates. Do not run P1–C1 on a candidate that has not passed S1–S3 on both footings.

## 3. Doors that are shut — do not re-propose them

Local (□φ)², |∇_μ∇_νφ|², aether-biharmonic operators (G030/G034/G032, f31c); the mimetic embedding and mimetic dust (G043, G048); a **fixed** congruence or clock called a covariant field (Horn A, G032: explicit local Lorentz violation; G043: not a gauge); disformal/vector TeVeS–AeST couplings (L244, DC-013/DC-019: α₁ = O(1)); modified inertia (L241: lensing-dead); bimetric/composite (G007: lensing sum cancels, Lean); the running-U clock (G001); a pure k-essence "frozen scalar" (H011: its static law is the bare μ₂ AQUAL equation and inherits Cassini unchanged); exponential khronometric (FC-KH); York/CMC (E and F gates); the CCNL clock inside one metric (lensing-dead); "the dust is the phantom" as a source of the same equation (L258 B3: the outer curve rises to 1.72 v_flat at 5 r_M); Ω_Λ "from a₀" (L258 A: circular). A lane that lands on one of these must say so in its first check and stop.

## 4. What a candidate must look like

Per the roadmap's G03 checklist: every term of S = S_EH + S_aux + S_m written, including boundary, multiplier and normalisation terms; fundamental or EFT-with-cutoff stated; if a clock τ is used, n_μ derived from it and its projector and connection given; the leaf Laplacian defined with its domain, measure and inverse or heat kernel (a projected Hessian is not the intrinsic operator; compute the extrinsic-curvature terms); the covariant quantities whose static limit is u and Φ identified, not assumed; all free initial and boundary data stated; a localisation by auxiliary field or rational filter is a **new system** until its extra modes are counted. Three directions are consistent with the surviving form and are the only ones worth a lane; each starts at S1:

1. **T-B localised.** The double filter (Gaussian or Helmholtz, output filter compulsory) as one or two auxiliary fields with a diffusion coordinate or Helmholtz mass 1/ξ; count the extra modes (P3) before believing S2.
2. **Whole-sector form factor.** J_Y(1 + ξ²k²) realised on the scalar's full quadratic form including its metric mixings, via an auxiliary pair with mass 1/ξ; the Pais–Uhlenbeck ghost is the expected killer, so P3 runs immediately after S2.
3. **Field-dependent stiffening.** ξ = ξ(|∇φ|/a₀) that vanishes for x ≲ 1 and is O(0.02–100 pc) for x ≫ 1, so S3 holds by construction and the whole burden falls on S2 and P1; check the transition does not reintroduce a local k⁴ term.

## 5. Deliverables and rules

`g03_<candidate>_action.py` (sympy; every term printed), `g03_<candidate>_gates.py` (S1–S5, then P1–P3, then C1, in that order, one commit per gate), `.out` and `_results.json`, a manifest with the hashes of the solvers used, and a `STATUS.md` line per gate: PASS / FAIL / OPEN with assumptions. Reproduce the calibration numbers before touching anything: g01 canonical Q₂ = +2.10e-26 s⁻² (3.8–5.5× the ceiling), L243 μ₂ 6.44×/7.63×, g02 floors 0.02/0.03 pc, the L232 fixed-M/L rms 0.1502 dex at n = 2. Both footings always. No literal-True conditions. No personal names in files or commit messages. Never stage astra's regenerated files. Never say T-B closes Track A, never say "closed", "complete" or "derived" for anything that a gate did not produce. The word "certified" means the algebra is machine-checked, never more.

## 6. What decides it

One number: the Cassini ratio |Q₂|/ceiling for an action that passed S1 and S3 on both footings. Below 1 with a healthy mode count is the first relativistic completion this programme would have; above 1 is one more shut door, recorded with the same care.

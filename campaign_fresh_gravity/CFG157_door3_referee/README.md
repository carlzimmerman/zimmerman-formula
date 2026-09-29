# CFG157 -- independent re-derivation of CFG121's G1 / B1 headline (Door 3, dipolar dark matter)

Frozen criteria: `CFG157_FROZEN_CRITERIA.md` (committed 6322d0d02, sha256 c0ad4353...) before any code. Own code; no import from any CFG121 file. CFG121's scripts and outputs were opened only AFTER my main and MUTATE runs were saved.

## Verdict: REPRODUCES (T1.2, B1, and T1.5 with one kernel caveat)

Every CFG121 headline number in scope reproduces within the frozen tolerances, both a0 footings, on the three independent derivative routes. No disagreement of any class. Two small differences (a kernel-definition 0.4% and a README range convention) are classified below. Nothing here says the data favour the framework or that the theory is closed; kappa = 1/2 is FITTED. Agreement here is agreement on a Newtonian identity plus its analytic deviation formula; CFG121's other gates (G1c-G5, T1.3/T1.4, Q1) are NOT re-derived.

## What was re-derived and how

Model (CFG121 section 2/4, V_B geometry): M_pol = m(nu - 1) with the P2 kernel nu = sqrt(1 + a0/g_b), rho_pol = M_pol'/(4 pi r^2), g_model = G(m + M_pol)/r^2, C_model = rho_pol r^3 g_model against C_tgt = (a0/4 pi) M_b(<r), on x = r/r_M in [0.1, 30] (121 log points), exponential spheres rho_0 exp(-r/h), h = 2 + (log10 M - 9) kpc.
My own hand result (frozen file section 3, verified numerically to 2e-15): **C_model/C_tgt = 1 + (dln m/dln r) B(y), B = y + 1/2 - sqrt(y(y+1))**. It implies deviation >= 0, maximal at the grid edge x = 0.1, tending to 1.5 (ratio 2.5) as r -> 0. B1: F_req = w v/(x^2 mu) with (m+M_c) dM_c/dr = (a0/G) r m integrated from a series start (own ODE code).

## Table vs CFG121 (canonical a0 = 9.3603e-11; CFG121 numbers read from its README/.out only after my runs were saved)

| cell | CFG157 | CFG121 | verdict |
|---|---|---|---|
| T1.2 1e9 | 1.3099 (x=0.1) | 1.31 (1.310) | REPRODUCES |
| T1.2 1e10 | 1.0160 | 1.02 (1.016) | REPRODUCES |
| T1.2 1e11 | 0.4342 | 0.43 (0.434) | REPRODUCES |
| T1.2 1e12 | 0.0632 | 0.063 (0.063), only PASS | REPRODUCES |
| T1.2 second footing (1.1312e-10) | 1.3324 / 1.0665 / 0.4988 / 0.0794 | 1.332 / 1.067 / 0.499 / 0.079 | REPRODUCES |
| T1.5 (nu_mono), my reconstruction | 1.4620 / 1.4038 / 1.1868 / 0.6253 | 1.462 / 1.404 / 1.187 / 0.623 | REPRODUCES (1e12 differs 0.4%, see below) |
| T1.5 with CFG44's own Bcommon.nu_mono (post hoc) | 1.4620 / 1.4038 / 1.1868 / 0.6228 | same | exact |
| T1.5 second footing | 1.4660 / 1.4148 / 1.2266 / 0.6274 | 1.466 / 1.415 / 1.227 / 0.627 | REPRODUCES |
| point-mass R(x=1), nu_mono | 1.4565 | 1.4565 (CFG44 referee: 1.46) | REPRODUCES |
| B1 F_req per mass, min/max on [0.3,30] | 0.414/0.939, 0.432/0.962, 0.470/0.967, 0.501/0.968 | same to 3 digits | REPRODUCES |
| B1 overall range | 0.406-0.968 on [0.1,30]; 0.414-0.968 on [0.3,30] | 0.41-0.97 | REPRODUCES (README's 0.41 is the [0.3,30] minimum 0.414) |
| Q* = max F_req / 0.10 | 9.677 | 9.68 | REPRODUCES; second footing 9.677 vs 9.68 |
| door verdicts at the 0.10 line | 1e9-1e11 FAIL, 1e12 PASS; B1 FAIL | same | identical |

Section-3 identities (all PASS): point mass ratio 1 to 6e-16 (analytic), 1e-11 (finite difference); deviation >= 0 everywhere; max at x = 0.1 for every mass and footing; deviation -> 1.5 as r -> 0 (1.50000/1.50000/1.49999/1.49997 at x = 1e-12) and decreases monotonically with x; F_req -> 2/5 in the deep core and -> y + 1 - sqrt(y^2+y) for a point mass (0.968 at x = 30).
Integrity checks: enclosed mass vs quad 1e-8; three derivative routes (chain rule with exact rho_b / 5-point finite difference / sympy) agree (worst scaled error 7.5e-4, where 1 is the 1e-5 relative line); closed form 2e-15; 121 vs 2001 grid < 0.5%; G of CFG121 vs 4.30091727e-6 kpc(km/s)^2/Msun < 1e-3; point-mass ODE 1e-12; ODE start r0/10 and rtol 1e-13 change v by < 2e-11; first integral outside the baryons < 2e-12.

## Shared vs independent

Shared (agreement does not test these): exponential-sphere definition and h(M) rule; a0 (both), G, Msun; the CFG44 target; CFG121's definition of C_model and the deviation metric; the grid convention. Independent: all code, the ODE integration, derivative routes, the closed-form analysis, the kernels, the controls, the B1 budget computation. I read the README numbers BEFORE deriving (targets read, not blind predictions), so the frozen hand estimates test my understanding of the mechanism rather than blind prediction.

## Controls (MUTATE; exit 1 when it bites)

| control | outcome |
|---|---|
| sign (chi -> -chi) | BITES. Point-mass identity broken: max dev 1.9901 (analytic 2/nu at x = 0.1, declared >= 1.5); 1e12 flips PASS -> FAIL (0.063 -> 1.866); others move to 1.03/0.56/1.40 |
| kernel (P2 -> "simple") | BITES. Point-mass max dev 0.9806 (declared >= 0.5); T1.2 numbers move (largest x16.8, 1e12: 0.063 -> 1.062, PASS -> FAIL) |
| target (constant charge, total mass) | BITES. Point-mass identity intact (5e-16, as declared); 1e12 0.063 -> 0.954, PASS -> FAIL; all four 0.95-1.00 |
| pm_target (B1: point-mass M_c on extended baryons) | BITES. min F_req 0.406 -> 0.542 (+33%, declared >= 0.5); target-ODE residual 1.4e2 vs ~1e-5 |

Not declared and unexpected in pm_target: the maximum of F_req explodes (69 on [0.1,30]) because the point-mass M_c is far above the true M_c where mu is tiny; a consequence, not a physics result. In sign, the mutated sign flips the interior sign of dev for 1e10-1e12 (dev < 0), which I did not declare.

## Failed checks and wrong expectations (kept)

1. First run of `cfg157_g1.py` FAILED my own check (ii-c) (`cfg157_g1_firstrun.out`, exit 2): I sampled the r -> 0 limit at x = 1e-6 with a 0.02 tolerance, but for 1e12 the deep limit is reached later (dev(x=1e-6) = 1.474; y ~ x). This was a poor sample point of my own check, not a physics disagreement. The check now tests the sequence x = 1e-6, 1e-9, 1e-12 (increasing to 1.5). No other criterion changed; all headline numbers are identical in the first run and the final run.
2. Frozen estimates scored: T1.2 all four (90% each): held; maximum at x = 0.1: held; Q* = 9.68 (85%): held; F_req min 0.41 (45%): held, but only under the [0.3,30] convention (0.414; the [0.1,30] value 0.406 is also within 3%); T1.5 all four (40%, conditional on the recipe): held, with the kernel caveat below; second footing 1e12 still < 0.10 (85%): held (0.0794). No frozen estimate failed.
3. The frozen file's sign-control declaration ("every T1.2 verdict must be FAIL") held only for the 1e12 flip and the point mass, and "mutated sign gives ratio 1 - 2/nu" was for the point mass; both consistent with the run.

## Disagreements and their classification

None in a headline number. Differences noted:
- **T1.5, 1e12, canonical: 0.6253 (mine) vs 0.623 (CFG121)** -- DEFINITION. I reconstructed nu_mono from the README-level hint (CFG89: "equals the RAR kernel for y < 2.54"; y_m = 2.5396 = argmax of y(nu-1); y(nu-1) held flat above), validated only by R(x=1) = 1.4565. CFG44's Bcommon nu_mono adds a small rising tail above y_m (floor derivative 0.05 H_P/(y+Y_P)); with that kernel imported read-only (post hoc, `cfg157_posthoc_numono.py`) my machinery gives 0.6228 = CFG121's 0.623. The other seven T1.5 cells agree to the digits because the maximum sits at y < y_m. The frozen tolerance (2%) was met either way.
- **B1 min F_req = 0.41**: README-CONVENTION note, not an error: it is the [0.3,30] minimum (0.414); B1's own line covers [0.3,30] while T1.2 uses [0.1,30].
- No solver disagreement, no README typo found in the cells re-derived. (CFG44's referee note that R(1) = 1.46 is a charge function, not a deviation R-1, is consistent with what I found; CFG121's T1.5 "1.46" for 1e9 is a different quantity, coincidentally the same value to 3 digits: 1.462 vs 1.4565.)

## Departures and disclosures

- nu_mono reconstructed (above); the CFG121 numbers depend on CFG44's actual kernel, which I imported only post hoc.
- Constants: my G, Msun as in CFG121's frozen text; a variant with CFG44's unit G changes max dev < 1e-3 (checked).
- My MUTATE sign/kernel/target controls differ in detail from CFG121's (its kernel control uses the "standard" kernel; mine "simple"); each was declared in my frozen file before running.
- The frozen (ii-c) check was re-implemented after its first run failed (item 1 above).
- `cfg157_posthoc_numono.py` is post hoc, written after CFG121's outputs were opened.

## NOT tested (scope)

CFG121's T1.3 (free-form chi), T1.4 (profile degeneracy), Q1 theorems, G1c B2-B4 (V_U pincer, tracking, maximal polarised share), G2 (linear growth), G3 (reaction, energy), G4, G5, O1; the robustness masses 3e9-3e11; non-spherical baryons; any relativistic completion. The verdict "scoped no-go" of CFG121 rests mostly on those and is neither confirmed nor refuted here. Two of this lane's confirmations are close to analytic (T1.2 and F_req follow from my closed forms), so agreement is not a strong test of CFG121's other machinery.

## Files and re-run

`CFG157_FROZEN_CRITERIA.md`, `cfg157_common.py`, `cfg157_g1.py`, `cfg157_b1.py`, `cfg157_posthoc_numono.py`, `run_all.sh`, `run_all.out`, outputs `cfg157_g1.out/_results.json`, `cfg157_g1_MUTATE_{sign,kernel,target}.out/_results.json`, `cfg157_b1.out/_results.json`, `cfg157_b1_MUTATE_pm_target.out/_results.json`, `cfg157_g1_firstrun.out/_results.json` (kept), `cfg157_posthoc_numono.out/_results.json`. Scripts print no absolute path (paths via ZF_REPO or an ancestor of `__file__`; printed as `<repo>/...` or bare names).

Re-run (from the directory containing the scripts): `ZF_REPO=<repo root> ./run_all.sh` (about 10 seconds; ZF_REPO is needed only for the post-hoc Bcommon import). Expected exit codes: g1 main 0; g1 MUTATE sign/kernel/target 1; b1 main 0; b1 MUTATE pm_target 1; posthoc 0.

## In-place re-run (orchestrator)

All scripts were re-run in this directory with `ZF_REPO` set; exit codes are as expected (mains 0; MUTATE sign/kernel/target 1; b1 MUTATE pm_target 1; post-hoc 0) and every `.out` and `_results.json` is identical to the referee agent's apart from timing. The `*_firstrun*` files are the referee's first g1 run, where its own check (ii-c) failed (exit 2) because of a poorly chosen r -> 0 sample point; kept as produced. What this lane does NOT test: CFG121's T1.3, T1.4, Q1, G1c B2-B4, G2-G5 and O1 — CFG121's scoped no-go rests mostly on those.

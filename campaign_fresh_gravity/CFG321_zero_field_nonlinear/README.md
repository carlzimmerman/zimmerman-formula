# CFG321: nonlinear evolution of the ungated chassis at an open zero-field region (recipe G5/G10)

**Verdict (frozen rule): FAIL.** One FAIL signature fired, in one of the three run sets, and no others. It is
supported by an independent check of the same runs and is not seen in the other two sets.

The criteria were frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit cb089fb29. Implementation disclosures
are appended at the end of that file; the frozen text is unchanged.

**Scope.** This lane says nothing about growth or sigma_8. L341's failure (sigma_8 = 18–27) and FP2's failed linear
cosmology stand whatever the verdict here. kappa = ½ is FITTED and plays no role. A pass here would not have been a pass
for candidate B, whose action does not exist.

## The question

FP5 G-2f (a26136bc4) found the chassis's own FRW background (an open zero-field region) Hadamard ill-posed at linear
order: omega^2 < 0 at every k. CFG294 proved conditional well-posedness only away from such regions. The question
here: does the nonlinear MOND kernel regularise that? Specifically, does it reach a regular saturated state that
depends continuously on the data, or do solutions branch, blow up or depend discontinuously on the data?

## Result in one paragraph

The system does saturate. In every ν_mono run (1+1 and 2+1, three grids each, eps ladder 1e-2…1e-4) the growth from
yhat = 1e-4 (y = 1e-4 y*) stops at yhat ~ 0.2–0.6 (y ~ y*). The state stays bounded and regular:
- energy is conserved to ≤ 1e-4 of E_kin;
- the leaf is unique and convex at every probe;
- no grid-scale content builds up;
- the saturated statistics are resolution-independent and eps-independent.

But continuous dependence is NOT shown at the frozen standard. In the 1-D eps = 1e-3 set:
- the pair-separation exponent rises with resolution at both steps: lambda = 0.012, 0.041, 0.066 (the frozen FAIL
  signature);
- the maximum amplification over the run rises ×3.6 then ×3.1: 95, 339, 1052 (checked in `cfg321_verify_fail.py`, V4).

That is the signature of sensitivity that grows with resolution, the thing this lane was built to detect. The 1-D
eps = 1e-2 and 2-D sets do not show it: their lambda falls with resolution. So the FAIL rests on one set, at the
smallest eps run with pairs, at the finest grids. The physical limit (eps → 2.6e-18, resolution → ∞) is in the
direction that makes it worse, not better.

## The reduced system (Part A, C-SYM: PASS)

The scalar block (hs, phi, n_z, u) is rebuilt from the action with FP5's ADM machinery, copied (not imported). Then:
- the momentum constraint fixes n_z;
- the elliptic lapse equation gives phi = (2u − hs)/(2 + alpha_c);
- U is solved per leaf.

This leaves

    K hs_tt = −(alpha/(2(2+alpha))) Lap hs − (2/(2+alpha)) Lap u,   K = (2 + 3c_2)/(2c_2),

with u minimising a strictly convex leaf functional. The dispersion equals FP5 B3 exactly:
- C → 0 gives CFG294's c_S^2;
- C → ∞ gives FP5 C3's −c_2 alpha/((2+alpha)(2+3c_2)).

**Dimensionless form.** The map is exact: x = C/C*, eps = alpha^2/(4 − alpha^2), slow time, and a constant field
map a/b = alpha(Lambda − 1). The system becomes

    psi_tt = −Lap psi + (1+eps) Lap u[psi],   u = argmin ∫ eps|∇u|² − 2∇psi·∇u + Qhat(|∇Su|²),

with conserved energy E = ∫psi_t² − |∇psi|² − (1+eps) min F.

**Parameters.**
- c_2 enters only the time unit: 1 slow unit = 2.11e4 yr at c_2 = 0.0667, xi = 0.0451 pc.
- The physical eps is 2.56e-18 (alpha_max). That is explicitly unintegrable, hence the declared eps ladder.
- The only nonlinearity kept is the kernel. Metric perturbations are ≲ 1e-20 in the saturated state.

## Controls

| Control | Result | Numbers |
|---|---|---|
| C-SYM (action → reduced system, B3, map, energy) | PASS | exact sympy identities |
| C-FP5 (C4's band and rates; y*) | PASS | y* = 2.5600e-18. k_max xi 1.5174 / 3.3931 / 6.7861, growth and e-folds (2.32e4, 7.34e3, 3.29e3 yr) match FP5 to < 1e-4. The lane form at physical eps equals FP5's formula to 1e-8. |
| C-LIN (code's linear rates about yhat_b = 1e-4) | **FAIL (status row)** | All 10 rates and frequencies match to ≤ 1.5e-3, 1-D L and 2-D T/L, both sides of the band edge. The five stable-mode runs end "leaf stalled" at residuals 1.3–6.6e-8, a precision floor from the 1e5 background/perturbation ratio. The row requires status ok. |
| C-GR (MOND off: GR + healthy khronon) | **FAIL (drift row)** | Order 2.000 vs the exact solution. Pairs linear (ratio 100.0) and bounded (max D/delta 2.5). Energy drift 3.2e-3 at N = 63 (> 1e-3), 7.6e-4 and 1.9e-4 at the finer grids. |
| C-BKG (reported) | — | H0 xi/c = 1.0e-11. \|W_FRW\|/k^2 = 6e-22. The slow unit is 1.5e-6 of a Hubble time. The growth phase is 1.2e5 yr. Dust moves ≲ 0.7 m over the whole run (xi = 1.4e15 m): a spectator. |
| MUTATE (μ_exp, a0 → y* a0) | **fails as required, rc = 1** | 1-D: every run hits indefinite leaf Hessians (829–22413 per run) and the leaf solve fails. 2-D: the leaf-uniqueness probe gives two-start differences of 57–103 (relative) at t = 15, 30, 45. That is branching. |

Both control failures are threshold or status rows on correctly behaving numerics. Under the frozen rule a control
failure alone would give OPEN, but the FAIL signature takes precedence.

## The nonlinear runs (Part F)

| Criterion | 1-D eps 1e-2 | 1-D eps 1e-3 | 2-D eps 1e-2 |
|---|---|---|---|
| R1 regular/bounded | PASS (drift ≤ 1.1e-4, residual 1e-10, 0 indefinite, probes 1e-11–1e-10) | PASS | PASS |
| R2a pointwise, growth phase (tau_s) | FAIL: d23 = 7.2e-3, p = 1.31 | FAIL: 7.8e-3, p = 1.14 | FAIL: 7.1e-3, p undefined (d12 ≈ d23) |
| R2b saturated statistics | PASS (rms yhat 0.597/0.587) | PASS (0.598/0.573) | PASS (0.277/0.276) |
| R3a linear in delta at tau_s | PASS (98.8–100.2) | PASS (99.1–101.0) | PASS (100.0) |
| R3b amplification at tau_s | PASS (2.59/2.68/2.56) | PASS (2.62/2.70/2.43) | PASS (2.10/2.12/2.07) |
| R3c Lyapunov | FAIL: 0.062/0.042/0.024 (finest/next 0.58) | FAIL: 0.012/0.041/0.066 (both steps > 1.25: **FAIL signature**) | PASS: 0.060/0.038/0.034 |

- **R1** also passes for the ladder-only runs.
- **R4, the eps ladder, passes.**
  - 1-D N = 127, rms yhat: 0.600 (1e-4), 0.598 (1e-3), 0.597 (1e-2). tau_s = 5.75 in all three.
  - 2-D N = 29: 0.274 (1e-3) vs 0.276 (1e-2). tau_s = 6.0 in both.
- **Why R2a misses.** The pointwise misses come from the kernel's |w|^(1/2) kink at zero crossings. Data built on
  different grids already differ (the mean field gradient G0 differs by 4% between N = 63 and 127). The growth phase
  converges at order ~1.1–1.3, not the leapfrog's 2.

**Verification of the FAIL trigger** (`cfg321_verify_fail.py`, reported, 1/4 of its own rows pass). It does not
explain the trigger away.
- V1: the exponents (≤ 0.08) are far below the band rates (0.39–1.47), but not below 0.1× the smallest one.
- V2: the rise with resolution occurs in 1 of 3 sets.
- V3: the delta = 1e-3 pair saturates (ratio down to 23.5) at the finest 1-D eps = 1e-3 grid.
- V4: the maximum amplification triples per resolution step in that set.

So the trigger is a real resolution trend in that set, not a fitting artefact. It is also not the O(k) Hadamard rate:
the exponents are 5–20× below the band growth rates.

## The saturated state (reported)

| | 1-D, N = 255, eps = 1e-3 | 2-D, n = 29, eps = 1e-2 |
|---|---|---|
| yhat percentiles 1/10/50/90/99/99.9 | 0.0042 / 0.047 / 0.335 / 1.23 / 1.96 / 2.28 | 0.023 / 0.076 / 0.22 / 0.50 / 0.71 / 0.83 |
| fraction yhat < 1e-3 (open zero-field regions) | 0.34% | 0 |
| <E_kin>/Vol (lane units) | 0.068 ± 0.010 | 0.026 ± 0.001 |
| physical energy density | 1.5e-39 J/m^3 = 2.8e-30 rho_Lambda c^2 | 5.6e-40 J/m^3 = 1.1e-30 rho_Lambda c^2 |
| median field | 0.34 y* = 8.0e-29 m/s^2 | 0.22 y* = 5.3e-29 m/s^2 |

The typical gradient is ~0.2–0.6 y*, confirming FP5 C4's "saturates at y ~ y*" by direct evolution. Open zero-field
regions do not survive in 2-D; in 1-D a 0.3% residue remains near zero crossings. Because of the FAIL above, the
XC5 E6 sqrt(eps)-Osgood question is not settled. The saturated state itself is regular, but its sensitivity to data
grows with resolution in one set.

## What would change the reading

The open part is whether the 1-D eps = 1e-3 trend persists:
- at N = 511;
- at eps = 1e-4 with pairs (not run: the 30-minute budget);
- with a C² (smooth-max) splice or a dealiased nonlinearity that removes the kink-limited order.

That would be a new lane with its own frozen criteria. It is not a re-reading of this one.

## Files

| File | Contents |
|---|---|
| `FROZEN_CRITERIA.md` | frozen criteria (cb089fb29) + appended implementation disclosures |
| `cfg321_engine.py` | kernels (ν_mono normalised to y*, μ_exp MUTATE, MOND-off), spectral grid, convex leaf solver, leapfrog evolution, data class D |
| `cfg321_zero_field_nonlinear.py` | Parts A–F, 43 runs on 14 processes; check() rows; verdict |
| `cfg321_zero_field_nonlinear.out`, `_results.json` | normal run: 12/19 checks pass, verdict FAIL, wall 792 s |
| `cfg321_zero_field_nonlinear_MUTATE.out`, `_MUTATE_results.json` | MUTATE: 4/8, verdict FAIL, MUTATE row PASS, rc = 1, wall 755 s |
| `cfg321_verify_fail.py`, `.out`, `_results.json` | verification of the FAIL trigger from the saved work arrays (1/4) |

Work arrays (~32 MB) go to `../_external_data/cfg321_work[_MUTATE]/`, relative to the repository root and outside
git. The main script regenerates them.

Run from the repository root:

    python3 campaign_fresh_gravity/CFG321_zero_field_nonlinear/cfg321_zero_field_nonlinear.py         # ~13 min, 14 processes
    CFG321_MUTATE=1 python3 campaign_fresh_gravity/CFG321_zero_field_nonlinear/cfg321_zero_field_nonlinear.py   # ~13 min, rc = 1
    python3 campaign_fresh_gravity/CFG321_zero_field_nonlinear/cfg321_verify_fail.py                  # after the main run, seconds

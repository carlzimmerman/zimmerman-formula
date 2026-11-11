# EFN1 RESULT: the nonlinear outcome of SCS3's external-field instability (2026-11-11)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11 m/s^2) and alt
(1.1312e-10 m/s^2), never pooled. The component is cold dark energy; no particle is added. Criteria 98364c8d20; amendments
A1 c3e466efbf, A2 a55fd19bd0, A3 94c54483a9, A4 04278f7abe (all post hoc, each committed alone before the graded runs under
it; disclosures in each file). Labels are read off the outputs by efn1_labels.py (efn1_labels.out / .json).

## Label

**NO VERDICT / NO VERDICT** (canonical / alt), in every reading (frozen, A1, A2-A4). Neither route decides.

- **Route D (direct, the deciding route) stops at an artefact of its own boundary.** In every graded run (12 backgrounds x
  R2-R4, A1-A4 readings) the stop line fires at r = 0.41-0.43 r_e, theta = 90.0 degrees: the corner where the static inner
  region (r < 0.4 r_e) meets the static plane rows of A1. Not in the unstable shell. The tell-tales:
  - the linear run (M3, nonlinear terms off) stops at the same cell at the same time (13.4-13.6 vs 13.3-13.6 e-folds);
  - the stop time falls by about 1.8 e-folds per refinement (15.0-15.9 at R2, 13.3-13.6 at R3, 11.5-11.7 at R4);
  - the background's own Picard residual (KA-d, full form) drives the same corner to the same stop line.
  So the graded "LEAVES" on every grid is not a fold of the clock flow, and the R3 / R4 refinement line fails everywhere.
- **Route W (weakly nonlinear) is not converged**, as the hand estimate said: the leading mode is the continuum edge at
  the grid scale (3-4 cells above half its peak, on every grid). Gamma converges (R2 -> R3 change 2-3 %), c3 roughly
  (1-27 %), c2 does not (6-128 %, and it changes sign on two backgrounds). Its reading would be RUNAWAY-W on all 12
  (c3/Gamma = +0.016 to +0.025 and |c2| small, so no fixed point at any amplitude): no saturation at small amplitude.
  But under the frozen rule that is NO VERDICT.

## The answer in plain words

The lane does not say what the instability does once it is nonlinear. What it does establish:

- **The nonlinear equations.** They are exact at the record's order (sympy, residual 0 in 3-D). The law's phantom density N
  is a pressureless fluid carried by the clock's tilt v = -grad pi, with continuity d_t N + div(N v) = 0. It is pushed by
  the force -grad(phi - s), which is gravity-like on N. Where N < 0, this is cold collapse of a negative density.
- **No saturation at small amplitude.** In no run, on no grid, does the perturbation in the negative shell saturate below
  order unity.
  - Route D: the shell's amplitude max|n|/|min N0| grows at 0.58-0.71 Gamma_ref (the smooth seed approaching the continuum
    edge from below; it rises with resolution). It passes 0.1 at 7.5-9.2 e-folds and 1 at 11.6-13.3 e-folds with
    eps = 1e-4, without slowing below 0.5 Gamma_ref.
  - Route W: c3 > 0 (no cubic saturation) on all 12 backgrounds and both grids.
- **Without the plane wall** (the frozen reading, plane rows dynamic; canonical / alt expo 9.4 at R3, R4) the corner artefact
  is gone.
  - The stop line fires in the unstable shell itself: c = |n|/|N0| >= 10 at 0.93-0.99 r_e, 150-154 degrees.
  - It fires at 14.50 / 13.63 e-folds (canonical R3 / R4) and 14.46 / 13.67 (alt). The grids differ by 0.87 and 0.79
    e-folds, more than the 0.5 refinement line.
  - At that moment the radial acceleration at r_e has changed by 6-7 % (theta max) and by < 0.5 % at 2 r_e.
  - **It is not a fold.** The linear control on the same grid (reported, not graded) reaches c = 10 at 13.43 / 14.21
    e-folds. That is no later than the nonlinear run: the nonlinear terms slow the growth slightly (canonical: the shell's
    amplitude at 13 e-folds is 2.1 nonlinear against 4.0 linear) rather than speeding it into a caustic. So c = 10 is
    reached by ordinary exponential growth. The outcome beyond order unity is not resolved by these grids.
- **My hand estimate (a density fold, LEAVES, in 7-10 e-folds) is not confirmed.** Nothing found contradicts "no
  saturation below order unity", but nothing shows a fold either.
- **Physical time.** With eps = 1e-4 the shell reaches order unity at about 12-14 e-folds. In t_H there are 16-19 e-folds
  (log M_b 9.4) and 7-10 (log M_b 10.45-10.9). So within a Hubble time it reaches order unity only for the light discs, and
  only from seeds of 1e-4 or more. M1's tenfold seed moves every stop about 4.2-4.4 e-folds earlier (but at the corner).

## Per background (A2-A4 reading, route D; t_F = e-folds of SCS3's rate at the stop line; all stops at the 0.41-0.43 r_e / 90 degree corner unless noted)

| Footing | Background | SCS3 e-fold (Gyr) | route W Gamma / Gamma_SCS3 (R2, R3) | t_F R2 / R3 / R4 | shell amplitude 1 at (R2 / R3 / R4) | Label |
|---|---|---|---|---|---|---|
| canonical | expo 9.4 | 0.848 | 0.928, 0.947 | 15.88 / 13.36 / 11.63 | 13.3 / 12.1 / 11.6 | NO VERDICT |
| canonical | expo 10.45 | 1.550 | 0.917, 0.948 | 15.01 / 13.39 / 11.54 | 13.3 / 12.6 / >11.5 | NO VERDICT |
| canonical | expo 10.7 | 1.790 | 0.926, 0.947 | 15.67 (shell, 1.03 r_e) / 13.39 / 11.54 | 13.2 / 12.6 / >11.5 | NO VERDICT |
| canonical | kuzmin 9.4 | 0.849 | 0.919, 0.947 | 15.16 (shell, 0.92 r_e) / 13.31 / 11.55 | 12.9 / 12.3 / 11.55 | NO VERDICT |
| canonical | kuzmin 10.7 | 1.790 | 0.922, 0.946 | 15.65 / 13.32 / 11.60 | 13.1 / 12.4 / 11.6 | NO VERDICT |
| canonical | kuzmin 10.9 | 1.998 | 0.917, 0.938 | 15.59 / 13.63 / 11.69 | 13.2 / 12.5 / >11.7 | NO VERDICT |
| alt | expo 9.4 | 0.734 | 0.926, 0.943 | 15.93 / 13.53 / 11.61 | 13.3 / 12.5 / 11.6 | NO VERDICT |
| alt | expo 10.45 | 1.345 | 0.919, 0.945 | 15.31 / 13.42 / 11.67 | 13.2 / 12.2 / >11.7 | NO VERDICT |
| alt | expo 10.7 | 1.551 | 0.925, 0.945 | 15.59 (shell, 1.02 r_e) / 13.44 / 11.55 | 13.1 / 12.3 / >11.6 | NO VERDICT |
| alt | expo 10.9 | 1.742 | 0.926, 0.947 | 15.66 (shell, 1.03 r_e) / 13.39 / 11.54 | 13.2 / 12.6 / >11.5 | NO VERDICT |
| alt | kuzmin 9.4 | 0.736 | 0.918, 0.943 | 15.14 (shell, 0.91 r_e) / 13.36 / 11.50 | 12.9 / 12.1 / >11.5 | NO VERDICT |
| alt | kuzmin 10.9 | 1.743 | 0.922, 0.946 | 15.66 / 13.32 / 11.60 | 13.1 / 12.4 / 11.6 | NO VERDICT |

Why each is NO VERDICT, under every reading:
- t_F differs by 1.4-1.9 e-folds between R3 and R4 (line 0.5);
- KA-b3 fails on 22 of 24 graded runs: the early rate of c is set by the corner, 1.1-3.0 Gamma_ref at R3, and undefined at
  R4, where c passes 1e-2 within the first e-fold;
- KA-d (full form) fails on the four backgrounds where it was run.

Under the A1 reading (a(t), 14 e-folds) the stop is also at the corner (a >= 10 at 12.5-12.7 / 10.3-10.8 / 8.8-9.0
e-folds on R2 / R3 / R4), with the same failure. The frozen reading on its two backgrounds is NO VERDICT: the stop lines
differ, unbounded at R3 and a >= 10 at R4.

**0.01 a0 extension** (expo 9.4, reported beside): same corner stop, t_F 12.79 / 11.15 (canonical) and 12.66 / 11.30 (alt)
e-folds = 250-330 Gyr. NO VERDICT, and physically irrelevant inside t_H.

## Known answers

| | Result |
|---|---|
| KA-a sympy (efn1_sympy.out, 3-D; 1-D and 2-D also run) | lapse S = Phi - pi_t + \|grad pi\|^2/2, E_Phi and E_pi as continuity, the linearisation equal to SCS1's L2, the symbol omega^2 = G(1 - Km)/m, the law's K J'' = 1/(1+u)^2 and K J'/A = 1/(1+u): every residual exactly 0. **PASS** |
| KA-b1 route W Gamma vs SCS3 converged route L (10 %) | 0.938-0.948 at R3 (0.917-0.928 at R2) on all 12. **PASS** |
| KA-b2 eigen-seeded linear run grows at route W's Gamma (2 %) | relative difference < 1e-5 on the four mutation backgrounds. **PASS** |
| KA-b3 early rate of c in [0.5, 1.10] Gamma_ref | **FAIL** on 22 of 24 (the corner); passes only canonical expo 9.4 R3 (1.08) and alt kuzmin 9.4 R3 (0.96). |
| KA-c isolated twins, route D | A4 line PASS on 4 of 4: fitted rate 0.014-0.037 Gamma_ref, max c 0.052-0.073. Frozen line (c <= 2 c(0)) FAIL on 4 of 4 (the seed's oscillation collects at the plane wall). |
| KA-c isolated twins, route W eigenvalue | NOT COMPUTED: ARPACK (shift-invert) did not converge for the first isolated twin, at sigma = 1.5 Gamma_ref^2 (0/4 after 5,000 iterations) or at 0.1 Gamma_ref^2 (3/4); 27 min, then stopped. Without a gap, the stable spectrum near 0 is dense. Route D's line stands alone |
| KA-d no seed | perturbative form exactly 0 on all 12: PASS. Full form (Picard residual 5e-9 to 8e-9 as the only seed): **FAIL** on 4 of 4. It reaches c = 10 at the corner at 11.4-14.8 e-folds; worst ratio to the seeded run 6-32. |
| KA-e refinement | dt halving on R3: t_F changes by <= 0.0043 e-folds on all 12: PASS. Grid R3 -> R4: **FAIL** on all 12 (1.4-1.9 e-folds). |

## MUTATE (R3; canonical / alt expo 9.4 and kuzmin 10.9)

| Arm | Result | Bites as frozen? |
|---|---|---|
| M1 seed x 10 | stop 4.2-4.4 e-folds earlier (frozen expectation ln 10 = 2.3 +- 0.5), same corner | **NO**. The corner's response is not proportional to the seed's growth, which confirms that the stop is not the shell's growth |
| M2 every nonlinear sign flipped | stop 2.0-2.1 e-folds earlier and moved into the shell (0.83-0.87 r_e, 137-144 degrees) | YES |
| M2b seed sign flipped (true equations) | stop 0.3-0.7 e-folds earlier, in the shell (0.83-0.87 r_e) | YES (the outcome depends on the sign of the perturbation, as the quadratic term implies) |
| M3 linear | stops at the same corner at the same time (13.3-13.6) | **NO**: so the graded stop is linear, i.e. not a fold |
| M4 route W, s-map second derivative flipped | c2 changes by 2-23 %, no sign change | **NO**: the s-map's quadratic part is a small share of c2 (the clock-flux and \|grad pi\|^2 terms dominate) |

## What carries the result

The lane's label rests on four things:
- the corner artefact of A1's static plane rows meeting the static inner region (route D);
- the grid-scale continuum edge (route W);
- the refinement line;
- known answers KA-b3, KA-d and KA-e.

The positive statements in "plain words" rest on:
- the shell's amplitude histories (a_neg in efn1_route_d_main.json, reported, not graded);
- route W's sign of c3;
- the four wall-free runs and their two linear controls (efn1_route_d_frozen.*, efn1_route_d_frozenlin.*: reported,
  not graded; the linear controls were added after the graded runs, as a diagnostic).

They need an independent re-grade before anyone leans on them.

## Not computed / only estimated

- The outcome beyond order unity: no grid resolves it.
- Route D without the corner: a dynamic plane at practical cost, or an r_in far from the plane. Only two backgrounds were
  run wall-free, at R3 / R4, and they do not meet the 0.5 e-fold line.
- Route W on R4.
- The in-plane family; the thick-disc twin and the disc-centre null (DCN1); non-uniform fields; gamma_L > 0; mu_K > 0.
- Extended baryon distributions beyond the razor-thin expo / Kuzmin discs.
- The 1PN terms (shift, momentum constraint, the multiplier's leafwise flux lambda P / Q, which is eps times the advective
  flux).

## Disclosures

- A1-A4 were each written after a code test on R0 / R1 (never a graded grid) showed a problem: plane-row stiffness;
  the amplitude measure sitting on the inner edge; the upwind flux's non-differentiable "cubic"; and KA-c's frozen line.
  - A1's wall is what produced the corner artefact that now decides the label. The R1 test had shown the edge-response but
    not the corner stop, which appeared on the graded grids.
- The BX1 wait loop matched other shells and held the driver until 06:51 EST (the coordinator stopped those). The batches
  then ran 06:51-10:16 EST, one at a time, single-threaded BLAS (the driver allowed up to 4 threads), nice 19.
  - Route W R2 + R3: 17 min. main: 96 min. ka: 11. kab2: 0.3. mutate: 12. ext: 7. frozen: 57. sympy 3-D: 2.
  - After that: the two frozen-reading linear controls, about 12 min, and the isolated route-W eigenvalues (not obtained: 27 min). ARPACK did not
    converge at sigma = 1.5 Gamma_ref^2 for an isolated twin. The retry at sigma = 0.1 Gamma_ref^2 (a code change, no rule
    change) overlapped the linear controls, so two single-thread jobs ran at once for about 12 minutes.
  - Peak RSS well under 4 GB. Disk >= 18 GB free throughout.
  - Background and eigenvector caches were in the system temp directory and are removed.
- scs2_aqual.py is copied unedited from fable52_push/SCS3_external_field_stability/. make_grid_res is SCS3's, re-typed in
  efn1_core.py.
- Nothing downloaded. No SCS1 / SCS2 / SCS3, PAPER72, register or decision file edited.

## Files

- Criteria and amendments: FROZEN_CRITERIA.md, AMENDMENT_A1..A4_2026-11-10.md.
- Code: efn1_sympy.py, efn1_core.py, efn1_route_d.py, efn1_route_w.py, efn1_labels.py, efn1_driver.sh, scs2_aqual.py (copy).
- Outputs:
  - efn1_sympy{,_dim1,_dim2}.{out,json};
  - efn1_route_w.{out,json} and efn1_route_w_MUTATE.{out,json};
  - efn1_route_d_{main,ka,kab2,ext,frozen,frozenlin}.{out,json} and efn1_route_d_MUTATE.{out,json};
  - efn1_labels.{out,json} (efn1_driver.log is git-ignored, kept locally).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

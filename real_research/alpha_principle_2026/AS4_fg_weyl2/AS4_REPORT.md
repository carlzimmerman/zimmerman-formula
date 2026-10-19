# Lane AS4: report

## Verdict: NOT PREDICTED. The graded EH + C^2 + R^2 trial with SM matter has no admissible fixed point.

All gates pass.  The lane reproduces Benedetti-Machado-Saueressig's (BMS, arXiv:0902.4630 / 0901.2984) quadratic-gravity flow exactly:
every printed heat-kernel table and trace block, and their EH beta functions.  It also reproduces their pure-gravity fixed points and
critical exponents.

With SM matter (type I), the higher-derivative flow has three real roots, and none is admissible:

* the only in-domain root has a sign-flipped spin-0 (conformal-mode) denominator;
* the other two have g < 0.

So no graded P exists.  The EH reference in the same scheme gives **P_EH = 96.37265**.  NOT PREDICTED means no statement about alpha.
kappa and Z enter nowhere.

| item | result |
|---|---|
| verdict class | NOT PREDICTED (no admissible root) |
| P (graded) | none |
| P_EH (reference) | 96.37265 (f_g = 0.03674694, g_Y* = 0.921519) |
| f_g at every in-domain root | EH 0.03674694; higher-derivative root 1 (inadmissible) 0.05741784 |

## Gates (`as4_gates.out`, re-run inside `as4_trial.out`)

| gate | result |
|---|---|
| G-PUB (i), exact | PASS. Lichnerowicz heat kernels on a generic Einstein space were derived from Vassilevich's a_4 with an explicit algebraic Weyl tensor (two different tensors give identical results). Unconstrained (0, 1, 2) = (1, 1/6, 1/80, 1/180), (4, 5/3, 41/120, -11/180), (10, 2/3, -1/24, 19/18); constrained 1T = (3, 1, 29/240, -1/15), 2T = (5, -5/3, -29/48, 10/9). All equal BMS eqs. Hexp and d4heat. The blocks S_1T, S_0, S_matter, S_hh (C1-C4) and S_2T (C~1-C~4) cancel exactly against my derivation from BMS Table T.1. The EH beta functions with n_s scalars equal BMS eqs. betaEH/etaEH/BEH exactly |
| G-PUB (ii), higher-derivative pure gravity | PASS. (g0, g1, g2, g3) = (0.004426, -0.01015, 0.007543, -0.005006) vs printed (0.00442, -0.0101, 0.00754, -0.0050). (g, lambda) = (1.96008, 0.21803) vs (1.960, 0.218). theta = (2.5113, 1.6878, 8.3994, -2.1101) vs (2.51, 1.69, 8.40, -2.11) |
| G-PUB (iii), EH pure gravity | PASS. (0.90160, 0.10926), theta = 2.5164 +- 1.7762 i vs (0.902, 0.109), 2.52 +- 1.78 i |
| n_s = 1 rows (reported) | higher-derivative (2.27909, 0.25074, 0.009978, -0.004291), theta (2.6652, 1.3866, 7.8645, -1.4951) vs BMS (2.279, 0.251, 0.010, -0.0043; 2.67, 1.39, 7.86, -1.50); EH (0.86006, 0.13077), 2.5808 +- 1.9544 i vs (0.860, 0.131, 2.58 +- 1.95 i) |
| G-MAT-C2 | PASS. Type-I matter on Einstein spaces, (a0, a2/R, a4 R^2, a4 Riem^2): scalar (1, 1/6, 1/80, 1/180), Dirac (4, -1/3, 1/120, -7/360), vector with ghosts (2, -2/3, -1/60, -13/180). These equal the Christensen-Duff (Vassilevich sec. 4.2.2) values |
| G-EH-LIMIT (reported) | BMS EH (0.90160, 0.10926) vs AS3/CPR EH (0.98417, 0.12927). Different schemes (Einstein-space Lichnerowicz cutoff and alpha-gauge, vs S^4 type Ib and beta-gauge); not expected to coincide |
| G0, classifier controls CC1-CC6 | PASS |
| MUTATE_1 | S_hh, S_2T, the EH betas, (ii) and (iii) FAIL (exit 1) |
| MUTATE_2 | S_2T and (ii) FAIL (exit 1) |
| MUTATE_3 | CC1, CC2, CC4, CC5 and CC6a FAIL (exit 1) |

## f_g with the C^2 term (stop rule not triggered)

In BMS's gauge (rho = 0, hard limit) on a flat background, f_g is:

    f_g = -(40 u0 + 20 u1 - 5 d_t u1 + 14 d_t u3) / (1152 pi^2 (u0 + u1 - 2 u3)^2).

* It is xi-independent.
* At a fixed point (d_t u1 = 2 u1, d_t u3 = 0) the C^2 coupling enters through the spin-2 propagator denominator.
* At u3 = 0 it reduces exactly to AS3's TT formula.

**Stop-rule check at the EH root:** the full traces at finite beta converge to this restricted value, with relative differences 3.28e-9,
3.27e-13 and 6.65e-16 at beta = 1e3, 1e5 and 1e7.

## Fixed points with SM matter (N_S = 4, N_D = 45/2, N_V = 12; type-I matter; BMS scheme)

Admissibility requires both regulated denominators at P_k = k^2 to be positive: spin-2 (2g3 - g1 - g0) and spin-0 -(6g2 + g1 + 2g0/3).

| case | (g, lambda[, g2, g3]) | spin-2 / spin-0 denominators | exponents | f_g | P |
|---|---|---|---|---|---|
| EH reference (unique) | (0.864773, -1.09006) | +0.0732 / +0.0564: admissible | 1.8684, 3.8919 | 0.03674694 | **96.37265** |
| higher-derivative root 1 | (0.863182, -1.07628, 0.0210528, -0.0072056) | +0.0582 / **-0.0702: not admissible** | -0.4423, 0.6803, 2.4085, 4.2221 | 0.05741784 | 91.04527 (reported only) |
| higher-derivative root 2 | (-0.199996, 0.0228, -0.0142, 0.0501) | outside the domain (g < 0) | -28.17, 0.601, 61.89 +- 70.46 i | -2.516 | none |
| higher-derivative root 3 | (-2.62889, 0.72855, -2.55e-6, 3.61e-3) | outside the domain (g < 0) | complex pair, -4.22, 2.68 | 0.2816 | 83.50578 (reported only) |

* **EH reference:** g_Y* = 0.921519, IR-attractive (theta_Y = -0.073494).
* **Root 1 (inadmissible, reported only):** g_Y* = 1.151906; theta_Y = -0.114836. Root 1 is the C^2/R^2 continuation of the EH fixed point;
  its spin-0 denominator 6g2 + g1 + 2g0/3 = +0.070 has the opposite sign to the Gaussian reference, because the R^2 term dominates the
  conformal mode at P_k = k^2.
* **Spin-2 at root 1:** the C^2 piece keeps the spin-2 denominator positive (g3 < 0, but 2g3 - g1 - g0 = +0.058).

**Not graded, for orientation only:** had root 1 been admissible, its P (91.045) would sit further from 137.036 than P_EH (96.373).

**Disclosed in the pre-registration:** the published pure-gravity fixed point violates both conditions. With SM matter, the in-domain
root violates only the spin-0 one.

## Systematics (reported, not graded)

| case | one-loop P | two-loop running | run started at the reduced Planck mass |
|---|---|---|---|
| EH reference | 96.37265 | 96.86496 (+0.49231) | 94.61927 (-1.75338) |
| root 1 (inadmissible) | 91.04527 | 91.58008 (+0.53481) | 89.29188 (-1.75338) |

The one-loop switch of the two-loop integrator reproduces the one-loop P to 3e-10.

## What the outcome means (frozen wording)

NOT PREDICTED means no statement about alpha.  Even AGREES would not have been a derivation of alpha: alpha_2, the hadronic offset and
the masses are measured, and convergence is untested.

## Disclosures (details in Amendment 1 of AS4_PREREGISTRATION.md)

1. **Source.** The letter 0901.2984 does not print beta functions or heat kernels, so the anchor is the companion 0902.4630. This was
   decided before any computation.
2. **Gates run 1** was stopped after about 20 min (output `as4_gates_FIRSTRUN.out`).
   * Cause: sympy simplification of the large expressions.
   * Fixed by numerical linear solves and no simplification; no gate logic changed.
   * Scratch profiling runs (not committed) had already shown the printed blocks cancelling.
3. **Trial run 1** was stopped at 1.94 GB RSS in the symbolic f_g step (`as4_trial_FIRSTRUN.out`). Nothing had been computed yet.
   * Fix: an exact, symbolically verified reduction to TT + photon, and evaluation one field-strength component at a time.
4. **Trial run 2** (`as4_trial_RUN2.out`) gave the same roots, f_g and P as run 3. But its stop-rule check was non-monotone because of a
   precision bug in my check (15-digit Float inputs), so it ended NOT COMPLETED.
   * Fixed with exact rational inputs; the frozen criterion is unchanged.
   * Run 3 is reported.
5. **Disclosed in the pre-registration before any computation:** the published pure-gravity fixed point would be inadmissible under the
   mandated rule.
6. **Compute.** Single core, `nice -n 19`, one process at a time. Peak RSS was 179 MB in the reported runs (1.94 GB in the stopped
   first trial run).

## Reading

* **BMS 0901.2984:** in full.
* **BMS 0902.4630:**
  * in full: sec. 3-5 and App. A-C;
  * not read: sec. 1-2.
* **Vassilevich hep-th/0306138:** sec. 4.1 and 4.2.2.
* **Recalled rather than read:** nothing load-bearing.

## Files

* `as4_common.py`, using the AS1/AS2 machinery by import.
* `as4_gates.py` / `.out`, `_FIRSTRUN.out`, `_MUTATE_1.out`, `_MUTATE_2.out`.
* `as4_g0_classifier.py` / `.out`, `_MUTATE_3.out`.
* `as4_trial.py` / `.out`, `_FIRSTRUN.out`, `_RUN2.out`.
* `as4_systematics.py`.

Downloads stay in `as4_scratch/` and are not committed.

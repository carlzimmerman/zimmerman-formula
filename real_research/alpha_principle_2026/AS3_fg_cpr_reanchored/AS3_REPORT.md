# Lane AS3: report

## Verdict: NOT DIAGNOSTIC. The graded R^2 trial has two admissible SM fixed points.

All gates pass, so the pipeline is validated against CPR's published f(R) computation. The R^2 truncation with SM matter has **two**
admissible fixed points. The frozen rule says "two or more: all are reported and the verdict is NOT DIAGNOSTIC (no root is picked)".
**No graded P exists.**

Reported, not graded:

* The P values at the two admissible R^2 roots are 95.26961 and 95.70584.
* The EH reference (SM matter, same scheme) has a unique admissible root, which gives P_EH = 95.57847.

All three are about 30 percent below 137.036. The target is not approached by any root, but no class beyond NOT DIAGNOSTIC is
assigned. Per the frozen wording, NOT DIAGNOSTIC carries no statement about alpha. kappa and Z enter nowhere.

## What changed from AS2 (`as3_gcpr.py` vs `as2_gcpr.py`, complete diff)

Only gate G-CPR-EH (ii) changed, as AS3_PREREGISTRATION.md specifies. Its messages changed with it, and an import path was added.

* `as3_gmat.py` runs AS2's `as2_gmat.run()` unchanged.
* `as3_g0_classifier.py` is AS2's script with only the docstring and the import path changed.
* `as3_trial.py` and `as3_roots_report.py` are new and build on `as2_common` by import.

```
    --- AS2_fg_cpr_scheme/as2_gcpr.py
    +++ AS3_fg_cpr_reanchored/as3_gcpr.py
    @@ -1,10 +1,16 @@
    -"""AS2 gates G-CPR-EH and G-CPR-R2 (pure gravity in the CPR f(R) scheme, AS2_PREREGISTRATION.md + Amendment 1).
    +"""AS3 gates G-CPR-EH and G-CPR-R2: copy of AS2's as2_gcpr.py with ONLY gate G-CPR-EH (ii) re-anchored (AS3_PREREGISTRATION.md):
    +the n = 1 root must reproduce CPR Table 1 g~0* = 0.005226 and Table 2 Re theta = 2.382, |Im theta| = 2.168 to 0.1 percent each;
    +Table 1 n = 1 g~1*, Lambda~*, G~* are reported, not gated.
     Usage: python3 as2_gcpr.py [MUTATE_1 | MUTATE_2]
       MUTATE_1: sign of the graviton contribution (TT, xi, (h, sigma) blocks) flipped in the trace -> G-CPR-EH (i) must FAIL (exit 1).
       MUTATE_2: R^2 (f'') term removed from the spin-0 h Hessian only -> G-CPR-R2 must FAIL (exit 1).
     Normal mode exits 0 iff all checks pass."""
     import sys
     sys.dont_write_bytecode = True
    +from pathlib import Path
    +_AS2 = Path(__file__).resolve().parent.parent / "AS2_fg_cpr_scheme"
    +if str(_AS2) not in sys.path:
    +    sys.path.insert(0, str(_AS2))
     import numpy as np
     import sympy as sp
     import as2_common as A
    @@ -68,20 +74,28 @@
             match = None
             for r, glb, th in rows:
                 Lt, Gt = glb[1], glb[0]
    -            okm = abs(Lt / tgt[0] - 1) <= tol and abs(Gt / tgt[1] - 1) <= tol
    -            if n == 2:
    -                okm = okm and abs(r[2] / tgt[2] - 1) <= tol
    +            if n == 1:   # AS3 re-anchored gate: Table 1 g~0* and Table 2 exponents, 0.1 percent each
    +                okm = (abs(r[0] / 0.005226 - 1) <= tol and np.iscomplexobj(th) and
    +                       abs(np.real(th[0]) / 2.382 - 1) <= tol and abs(abs(np.imag(th[0])) / 2.168 - 1) <= tol)
    +            else:
    +                okm = abs(Lt / tgt[0] - 1) <= tol and abs(Gt / tgt[1] - 1) <= tol and abs(r[2] / tgt[2] - 1) <= tol
                 if okm:
                     match = (r, glb, th)
             print(f"\n  n = {n} pure gravity: real roots (g~0, g~1{', g~2' if n == 2 else ''}) -> (Lambda~, G~):")
             for r, glb, th in rows:
                 print(f"    g~ = {np.array2string(np.array(r), precision=6)}  Lambda~ = {glb[1]:.5f}  G~ = {glb[0]:.5f}  theta = {np.array2string(th, precision=3)}")
             tag = "G-CPR-EH(ii)" if n == 1 else "G-CPR-R2(ii)"
    -        if match is not None:
    +        if match is not None and n == 1:
                 r, glb, th = match
    -            msg = f"Lambda~* = {glb[1]:.5f}, G~* = {glb[0]:.5f}" + (f", g~2* = {r[2]:.6e}" if n == 2 else "") + \
    -                  f" vs CPR Table 1 {tgt} (tol {tol*100:g}%); theta = {np.array2string(th, precision=3)} (CPR Table 2: " + \
    -                  ("2.382 +- 2.168 i" if n == 1 else "1.376 +- 2.325 i, 26.862") + ", reported only)"
    +            msg = (f"g~0* = {r[0]:.7f} vs Table 1 0.005226; theta = {np.real(th[0]):.4f} +- {abs(np.imag(th[0])):.4f} i vs Table 2 2.382 +- 2.168 i "
    +                   f"(tol 0.1% each).  Reported, not gated: g~1* = {r[1]:.7f}, Lambda~* = {glb[1]:.5f}, G~* = {glb[0]:.5f} vs Table 1 "
    +                   f"-0.02014, 0.1297, 0.9878")
    +        elif match is not None:
    +            r, glb, th = match
    +            msg = f"Lambda~* = {glb[1]:.5f}, G~* = {glb[0]:.5f}" + f", g~2* = {r[2]:.6e}" + \
    +                  f" vs CPR Table 1 {tgt} (tol {tol*100:g}%); theta = {np.array2string(th, precision=3)} (CPR Table 2: 1.376 +- 2.325 i, 26.862, reported only)"
    +        elif n == 1:
    +            msg = "no root reproduces Table 1 g~0* = 0.005226 and Table 2 theta = 2.382 +- 2.168 i within 0.1% each"
             else:
                 msg = f"no root matches CPR Table 1 n = {n} {tgt} within {tol*100:g}%"
             chk(tag, match is not None, msg)
```

## Gates (`as3_gmat.out`, `as3_gcpr.out`, `as3_g0_classifier.out`; also re-run inside `as3_trial.out`): all PASS

| gate | result |
|---|---|
| G-MAT | PASS. Bare S^4 heat kernels: scalar (1, 1/6, 29/2160), 1-form (4, 2/3, 43/1080), both from the spectra = Vassilevich; spinor (4, 2/3, 101/2160). Assembled operators equal Christensen-Duff: (1, 1/6, 29/2160), (4, -1/3, 11/2160), (2, -2/3, -31/1080) |
| HK-CPR | PASS. Spectra-derived S^4 coefficients equal CPR table taba6 |
| G-CPR-EH (i) | PASS. R^0 and R^1 equal CPR's closed form 'george' / 725760 exactly |
| G-CPR-R2 (i) | PASS. R^2 equals 'george' / 725760 exactly |
| G-CPR-EH (ii), re-anchored | PASS. g~0* = 0.0052261 (Table 1: 0.005226); theta = 2.3824 +- 2.1682 i (Table 2: 2.382 +- 2.168 i). Reported, not gated: g~1* = -0.0202143, Lambda~* = 0.12927, G~* = 0.98417 vs Table 1's -0.02014, 0.1297, 0.9878 |
| G-CPR-R2 (ii) | PASS. (0.12936, 1.56329, 1.514408e-3) vs Table 1 (0.1294, 1.5633, 1.514e-3); theta = 1.376 +- 2.325 i and 26.862 = Table 2 |
| G0 | PASS |
| classifier controls CC1-CC5 | PASS |
| MUTATE_1 | G-CPR-EH (i), (ii), G-CPR-R2 (i), (ii) all FAIL (exit 1) |
| MUTATE_2 | G-CPR-EH (i), G-CPR-R2 (i), (ii) FAIL (exit 1). The re-anchored n = 1 gate does not involve f'' and still passes |
| MUTATE_3 | CC1, CC2, CC4, CC5 FAIL (exit 1) |

## f_g in CPR's gauge (stop rule not triggered)

From `as3_trial.out`: the |beta| -> infinity limit of the F-bar^2 coefficient is finite (numerator and denominator are both degree 11 in
beta). The beta -> +infinity and -infinity limits agree, and the parity check passes. The result is independent of the photon gauge
parameter xi:

    f_g = -5 (8 f + 4 f' - d_t f') / (1152 pi^2 (f + f')^2),

which at a fixed point (d_t f' = 2 g~1) is

    f_g = 5 g (1 - 8 lambda) / (36 pi (1 - 2 lambda)^2).

The R^2 coupling b drops out. In CPR's gauge (rho = 0, beta -> infinity) the surviving metric modes are the 5 TT modes and the pure
conformal mode h_mn = phi delta_mn. The Maxwell term sqrt(g) g g F F is conformally invariant in d = 4, so only the TT modes couple to the
photon.

`as3_roots_report.py`, added after the run, re-derives f_g by restricting the trace to the kernel of the gauge fixing. That route is
exact for rho = 0 and agrees with the brute-force formula identically. The formula equals AS1's TT-only f_g at eta_N = -2.

**Caveat** (carried from AS1): Eichhorn-Versteegen's printed TT-approximation formula (their sec. 3.2) is not reproduced by this TT
computation, and I have not identified why. Against that, the same vertices and machinery reproduce their full alpha = 0, beta = 1 result
exactly, including the eta_h term. AS3's f_g is structurally that TT contribution.

## Fixed points with SM matter (N_S = 4, N_D = 45/2, N_V = 12; type-I matter)

**EH reference (n = 1):** a unique root on the frozen 10 x 15 grid.
* (g, lambda) = (0.967159, -1.22293); CPR variables g~ = (-0.0503111, -0.0205699).
* Admissible; not near a domain edge.
* Critical exponents 1.8917 and 3.8961 (both relevant).
* f_g = 0.03883093, which is 0.80982 x 0.04795 and 3.96032 x 0.009805.
* g_Y* = 0.947289, IR-attractive (theta_Y = -2 f_g = -0.077662).
* **P_EH = 95.57847.**

**R^2 trial (n = 2), graded:** 4 real roots on the frozen 10 x 15 x 15 grid.

| root | (g, lambda, b) | admissible | exponents | f_g | P (reported only) |
|---|---|---|---|---|---|
| 1 | (1.006220, -1.264456, -0.0037661) | yes | -0.2098, 1.8588, 3.8892 | 0.03970669 | 95.26961 |
| 2 | (0.888392, -1.082827, 0.0302638) | no (spin-0 denominator 1 - 4L/3 - 96 pi g b < 0) | 0.3434, 2.1847, 3.9685 | - | - |
| 3 | (0.988607, -1.297727, 0.0055494) | yes | 1.7286 +- 0.7115 i, 4.1562 | 0.03848093 | 95.70584 |
| 4 | (-0.273313, 0.579213, -0.0267791) | no (g < 0, outside the domain) | -21.85 +- 23.36 i, 5.108 | - | - |

* At the admissible roots g_Y* = 0.957912 (root 1) and 0.943010 (root 3). Both are IR-attractive (theta_Y = -0.079413 and -0.076962).
* Two admissible roots, so the verdict is **NOT DIAGNOSTIC**.
* The truncation shifts relative to EH, reported only, are -0.30886 (root 1) and +0.12737 (root 3).

## Systematics (reported, not graded; lane B's code by import)

| case | one-loop P | two-loop running | run started at the reduced Planck mass |
|---|---|---|---|
| EH reference | 95.57847 | 96.07582 (+0.49735) | 93.82509 (-1.75338) |
| R^2 root 1 | 95.26961 | 95.76901 (+0.49941) | 93.51622 (-1.75338) |
| R^2 root 3 | 95.70584 | 96.20236 (+0.49652) | 93.95246 (-1.75338) |

The one-loop switch of the two-loop integrator reproduces the one-loop P to 2.6e-10.

## What the outcome means (frozen wording)

NOT DIAGNOSTIC means no statement about alpha.

For the record only, every computed P in this scheme is about 95.3-95.7. That is about -30 percent: no better than lane B's EH value
(92.914) by any meaningful margin, and far outside 2 percent. Even an AGREES would not have been a derivation of alpha: alpha_2, the
hadronic offset and the masses are measured, and convergence is untested.

## Disclosures

1. **The AS3 gate change** was written by the coordinator after AS2's gate output (disclosed in AS3_PREREGISTRATION.md). I implemented
   it as specified; the diff is above.
2. **`as3_trial.py` ran once.** That run completed and is the reported run; there was no fix and no re-run.
   * It took 1120 s with a peak RSS of 1.35 GB (cap 2 GB), single core at `nice -n 19`, one process at a time.
   * stdout was block-buffered, so the output appeared only at the end.
3. **`as3_roots_report.py` was added after the trial run.** The frozen rule says that with several admissible roots "all are reported";
   the trial script printed the roots but not f_g and P at each, so this script adds them.
   * It also re-derives f_g by a second, exact route (restriction to the kernel of the gauge fixing). The two agree identically.
   * It changes no class.
4. **Implementation readings of the frozen text**, all fixed before the run:
   * f_g at a fixed point uses d_t f' = 2 g~1 and d_t f'' = 0 (pre-registered).
   * The photon gauge is xi = 1; f_g turned out xi-independent.
   * Edge flags are read per finite bound (AS2 Amendment 2); no in-domain root is flagged.
   * The two-loop systematic integrates lane B's `b2.rhs` up and then down. The reduced-Planck systematic temporarily sets the imported
     b3 module's M_Planck.
5. **The "within 5 percent of a domain edge" flag** was set only for root 4, which lies outside the domain anyway.

## Files

* `as3_gmat.py` / `.out`
* `as3_gcpr.py` / `.out`, `_MUTATE_1.out`, `_MUTATE_2.out`
* `as3_g0_classifier.py` / `.out`, `_MUTATE_3.out`
* `as3_trial.py` / `.out`
* `as3_roots_report.py` / `.out`

The AS2 machinery (`../AS2_fg_cpr_scheme/as2_common.py`) is used by import and is unchanged.

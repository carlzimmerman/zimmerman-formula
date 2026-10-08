# CFG468 FROZEN CRITERIA: the kernel family. Is there a nu(y) that fits SPARC as well as nu_mono, keeps both limits, and removes the zero-field FAIL?

**Lane:** orchestrator, 2026-10-08. The owner said the kernel is now an experimental variable ("push all possible options while being consistent with my framework"). The default stays nu_mono until evidence says otherwise. The law a0 = kappa c sqrt(G rho_Lambda) is fixed. kappa is FITTED, and both footings are reported separately (9.36e-11 rho_Lambda, 1.13e-10 rho_crit).

**The question.** Is there a kernel that does all three of the following?
- (i) It fits the SPARC RAR as well as nu_mono.
- (ii) It keeps nu -> y^-1/2 as y -> 0 and nu -> 1 as y -> infinity (BTFR exact).
- (iii) It removes the zero-field nonlinear FAIL of the UNGATED chassis. That FAIL is CFG321 -> CFG322 -> CFG325 (OPEN at N <= 1023) -> CFG358 (CONFIRMED-FAIL at N = 2047, a knife-edge decided by the zero-guard).

**Scope.** The zero-field arm concerns ONLY the ungated chassis: the law is on everywhere, including the open FRW background, in 1-D with data class D. It says nothing about candidate B, whose switch is off in unbound regions and whose action does not exist. It says nothing about growth or sigma_8 either.

## Analytic fact stated before any run (a prediction that can fail)
The CFG321 engine works in units yhat = y / y*. Here y* = (log1p(1/C*))^2, C* = (2 - alpha_c)/alpha_c, and alpha_c = 3.2e-9 (L340 P1 maximum). So **y* = 2.56e-18**.
- The saturated runs have rms yhat ~ 0.5 (CFG358 log), so every engine field sits at y <~ 3e-17.
- There, every kernel obeying (ii) is the same power law. The differences are (nu - 1) = y^-1/2 [1 + O(sqrt y)], with sqrt y* = 1.6e-9.
- The "kink near y -> 0" is the deep-MOND limit itself: Q ~ |w|^{3/2}, C_L ~ yhat^{-1/2} at a field zero. It is common to every (ii) kernel.

**PREDICTION P1:** the class-(ii) kernels (simple, standard) reproduce nu_mono's lambda(N) to within 0.001 at every N. They therefore inherit nu_mono's frozen verdict on the same grids, which is OPEN at N <= 1023 (CFG325).
- If any class-(ii) kernel differs from nu_mono by more than 0.005 in lambda at any N, the analytic picture is wrong. This is flagged, not explained away.
- Consequence: only a kernel that changes nu at y below about 1e-17 can change the zero-field verdict. Such a kernel breaks (ii) formally. This lane tests two such splices, at declared points.

## Kernels (frozen definitions; physical y = g_N/a0)
| id | name | nu(y) | (ii) |
|---|---|---|---|
| K0 | nu_mono (default) | the record's standing kernel, CFG5_common.nu_mono: nu_RAR = 1/(1 - e^{-sqrt y}) for y <= 2.3374, then the monotone log splice delta = 0.05 (XC4) | exact |
| K1 | nu_1 "simple" | 1/2 + sqrt(1/4 + 1/y) | exact |
| K2 | nu_2 "standard" | [1/2 + sqrt(1/4 + y^-2)]^{1/2}, i.e. mu = x/sqrt(1 + x^2); evaluated as y^-1/2 exp(asinh(y/2)/2) | exact |
| K3 | S1: C^2 splice at the engine scale | for y < y_s1 = 0.1 y* = 2.56e-19: nu = 1 + y_s^{-1/2} (a + b u^2 + c u^4), u = y/y_s. (a, b, c) are fixed by matching nu_mono's value and its first and second y-derivatives at y_s (C^2; even in u, so the Lagrangian is smooth at a field zero). Pure deep form: a = 45/32, b = -9/16, c = 5/32. nu_mono for y >= y_s. | operational only: holds for y >= 2.56e-19; nu(0) finite |
| K4 | S2: the same C^2 splice at y_s2 = 1e-8 | three decades below the lowest KiDS-1000 isolated-lens RAR bin (g_bar 1.38e-15, y = 1.5e-5 / 1.2e-5 on the two footings); ten decades above y* | operational only: holds for y >= 1e-8 |
| M | MUTATE "kink": 1/nu piecewise linear in sqrt y | q = 1/nu, v = sqrt y. For v < 0.1: q = (1 - e^{-v}) + D(v), where the ramp D = 0 for v < v_a, (v - v_a)/2 for v_a <= v < v_b, and (v_b - v_a)/2 for v >= v_b; v_a = sqrt(0.1 y*), v_b = sqrt(0.4 y*) = 2 v_a. This gives two kinks inside the engine's field range, where C_L jumps by x0.5 and x1.5 and stays convex. For v >= 0.1: linear in v through knots v = 0.1, 0.3, 1, 3 (values 1 - e^{-v} + (v_b - v_a)/2) and (10, 1); q = 1 for v >= 10. Kinks fall at y = 0.01, 0.09, 1, 9, 100 and 2.6e-19, 1.0e-18. | exact (q -> v; nu = 1 for y >= 100) |

SPARC-arm references only, with no zero-field ladder (class (ii), covered by P1): nu_RAR without the splice, and P2 = sqrt(1 + 1/y) (the record's earlier kernel, lane V's "alpha1").

## Arm 1: SPARC RAR (frozen)
- **Machinery:** lane V's `sonnet55_push/puzzle_32pi/agents/V_evidence_for_the_coefficient/v_common.py`, imported read-only with its sha256 recorded. It reads `SPARC_Lelli2016c.mrt` + `sparc_data/*_rotmod.dat` (never `SPARC_table.txt`, a 404 page), uses log-space residuals, and sets the per-point variance to (2 eV/V/ln10)^2 + sigma_int^2.
- **Two treatments, as p35/p36:**
  - **T-free:** Upsilon_disk free per galaxy on 0.05–3.0 (119 values), Upsilon_bul = 1.4 Upsilon_disk, all galaxies, sigma_int = 0.0808 dex.
  - **T-fix:** Upsilon_disk = 0.5 (bulge 0.7), MLS16 cuts (Q <= 2, i >= 30 deg), sigma_int = 0.11 dex.
  - sigma_int is held fixed across kernels.
- **a0 is refit per kernel:**
  - grid exp(linspace(ln 0.5e-10, ln 2.5e-10, 161)), refined by v_common.parabola_min;
  - chi2_min is evaluated at the refined a0;
  - kappa_Lambda = a0/(c sqrt(G rho_Lambda)) and kappa_crit = a0/(c sqrt(G rho_crit)), with H0 67.4 and Omega_Lambda 0.685;
  - SPARC's tabulated distances (lane V convention). The paper's R1 convention is not applied; this is stated.
- **Delta chi2** = chi2_min(kernel) - chi2_min(nu_mono), on independent points.
- **SPARC-PASS:** Delta chi2 <= 4 in BOTH treatments. This is the record's tolerance: p36's "within Delta chi2 = 4 = allowed", on independent-point chi2. Two other readings are reported but not used: p35's "SPARC cannot tell" |Delta chi2| < 2, and lane V's ~x18 clustering deflation.

## Arm 2: zero-field nonlinear test (frozen; CFG325's rule, kernel swapped)
- **Engine:** `cfg468_engine.py` is a byte-identical copy of `CFG358_zero_field_N2047/cfg358_engine.py`, sha256 bde2fbb6… (the CFG321 engine), checked at run time. The engine file is not edited. The kernels are supplied by the driver as objects with CT, CL, Q.
- **Same physical unit for every kernel:**
  - yhat = y / y*_ref, with y*_ref the nu_mono y* above;
  - C_T(yhat) = (nu(y*_ref yhat) - 1)/C*;
  - C_L = d[y(nu - 1)]/dy / C*;
  - Q(yhat) = 2 Int_0^yhat s C_T(s) ds.
  - For nu_mono this is exactly the engine's NuMonoKernel (control C0).
- **Unchanged from CFG325:** data class D (seeds 321/322, rms yhat 1e-4, L = 16, T = 80), the pairs delta = 0, 1e-3, 1e-5, the Lyapunov fit on D(1e-5) inside [1e-4, 1e-1], and ZERO = 0.005.
- **Grids:** NS = (127, 255, 511, 1023), the four grids of CFG325's rule. The brief named 255/511/1023, but the frozen ratio rule needs three increments, so 127 is added as in CFG325. N = 2047 is NOT run here. If a kernel comes out CONVERGENT at N <= 1023, a 2047 confirmation is recommended, because nu_mono's own OPEN at 1023 became FAIL at 2047. That run needs a separate go.
- **nu_mono baseline:** CFG325's committed-run work arrays (N = 127–1023, both eps, three deltas; same engine) are re-read and re-scored. One new run at N = 127 through the generic adapter is the reproduction control C1'.

**Per eps set (1e-3, 1e-4):**
- Increments Delta1..3 over NS, and r2 = Delta2/Delta1, r3 = Delta3/Delta2, with CFG358's zero-guard.
- **RESOLVED-CONVERGENT:** |r2| <= 0.6, |r3| <= 0.6 and a finite lambda_inf.
- **CONFIRMED-FAIL:** Delta3 >= 0.005 and r3 >= 0.9.
- **BOUNDED (pre-declared addition):** every run in the set is regular and max D(1e-5)/delta <= 10 at every N, i.e. no Lyapunov growth (C2's GR-control standard). The ratio rule has no input there, because lambda is never reached.
- **OPEN:** anything else.

**Kernel zero-field verdict:**
- **CONVERGENT** if both sets are RESOLVED-CONVERGENT or BOUNDED and every main run is regular (status ok, zero indefinite leaf Hessians, residual <= 1e-8).
- **FAIL** if either set is CONFIRMED-FAIL, or any main run branches (blow-up, leaf failure, indefinite Hessian).
- **OPEN** otherwise.

## Decision
- **VIABLE** = SPARC-PASS AND zero-field CONVERGENT (the brief's definition).
- Column (ii) is reported beside it: exact / operational / fails.
- A VIABLE kernel whose (ii) is only operational adds a declared constant (y_s). That is against the zero-knob rule, so it is reported as an OPTION, never adopted.
- **Answer to the question:** YES only if some kernel is VIABLE with (ii) exact.

## Controls
- **C0, adapter:**
  - The generic nu_mono adapter matches the engine's NuMonoKernel C_T, C_L, Q to <= 1e-10 relative on yhat in [1e-12, 10].
  - For every adapter, dQ/dyhat = 2 yhat C_T and C_L = d(yhat C_T)/dyhat, to <= 1e-6 (finite differences, away from kinks).
  - S1/S2 are C^2 at y_s: the jumps in C_T, C_L and dC_L/dyhat are <= 1e-8 relative.
- **C1', driver:** generic nu_mono at N = 127 reproduces CFG325's lambda (4 decimals) and Amax (1 decimal): eps 1e-3 0.0414 / 338.7, eps 1e-4 0.0569 / 897.2.
- **C-S, SPARC code:** P2 with p35's 61-point a0 grid reproduces p35's printed chi2_min, 4596.5 (T-fix) and 3139.8 (T-free), to 0.1.
- **C-K, kernel identity:** K0 is CFG5_common.nu_mono itself.
- **MUTATE:** the kinked kernel M must NOT come out VIABLE. Each arm is reported separately.
  - Secondary reading, not load-bearing: if M's zero-field verdict is CONVERGENT, zero-field convergence cannot be credited to smoothness.
  - `CFG468_MUTATE=1` exits rc 1 when M is not VIABLE ("fails as required").
- **P1** as above.
- **GR control:** C2 is kernel-independent. It is not re-run, and CFG358's C2 (order 2.0 through 2047) stands. This is disclosed.

## Also reported (survey, no new gate)
Which committed gates depend on the kernel choice: the Cassini/heat filter (CFG357), the EFE lanes, the UFD lanes, wide binaries and others. Each is flagged with the part of nu it reads: deep limit, transition or tail.

## Compute
- nice -n 15, at most 6 worker processes, BLAS threads = 1.
- Work arrays go to `../_external_data/cfg468_work[_MUTATE]` (outside git).
- New zero-field runs: 5 kernels x 4 grids x 2 eps x 3 deltas = 120 runs, plus the C1' runs.
- Estimate from CFG325's walls: about 27 CPU-h per (ii)-class kernel, so about 110 CPU-h in all, about 18–20 h wall.

## Pre-freeze disclosure
Before this commit, these were read: CFG358/CFG325's engine, scripts, logs and results; lane V's v_common and p35/p36 outputs; CFG357's README; the L340 alpha_c; and the KiDS lensing-RAR lowest bin. y* and the splice/kink positions were computed by hand (arithmetic only). Not done before this commit: no candidate-kernel SPARC fit, no candidate-kernel engine run, and no adapter code.

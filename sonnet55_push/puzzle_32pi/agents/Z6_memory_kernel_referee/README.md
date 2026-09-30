# Z6 referee: is the record's memory kernel Sciama's kernel? (lane X3's Part B relocation)

## Bottom line (verdict: TRUE ONLY FOR THE MOMENT, not for the kernel; nothing derived, kappa = 1/2 stays FITTED)
1. X3's arithmetic is right: the mean lag of the normalised sharp r dr weight on [0, T] is (2/3) T, so M1 = (2/3) c/a0 = (4/3) t_Lambda gives T = c/a0 = 2 R*/c **for that one shape at unit total weight M0 = 1**; it is clean only because two unrelated 2/3 factors cancel (the action's memory-force renormalisation, and the r dr weight's mean lag).
2. "The record's kernel IS Sciama's kernel" is **false**: the record's K is a free-weight memory on the proper-time lag of the particle's own worldline acting on the rapidity gap through a nonlinear mu(Theta) (no G, no density, no dV); the same requirement gives cutoffs 2, 8/3, 4/3, 2/3 x R* for four shapes and scales as 1/M0 (the record proved the shape invisible); at Sciama's physical strength the cutoff c^2/a0 carries M0 = 8 pi, so R_c = c^2/a0 needs Sciama's coupling divided by 8 pi (physical strength + requirement give R_c = 0.683 R*, M0 = 2.93).
3. Different functionals: Sciama's force is linear, F = -m (M0 a - dTheta/dt), so a steady acceleration sees only M0 and its crossover is a frequency; the record uses M1 through |a| and mu. The record's Theta after a step is linear in the duration, not (t/T)^2.
4. The identified kernel (T = 101 Gyr) is in the record's excluded long-memory branch (x = 2.9e3 at 8 kpc; width bound exceeded 1e5-fold) and violates the ephemeris bound by 1e12 (Theta(Mercury) = 2e-4 vs 429 needed): it is the record's already-closed "vacuum free-fall time at unit weight". 66 checks pass, 22 controls rejected, 8/8 mutants caught.

## What I did
Read the record's action and kernel from primary scripts and the paper (opus_48_extended_research/papers/RAPIDITY_GAP_MI_ACTION.md v6; real_research/reviews/mi_a0_from_one_line_2026.py, mi_N_count_and_kappa_iff_2026.py, mi_local_source_for_K_2026.py, mi_kernel_localisation_2026.py, mi_wightman_first_moment_2026.py, mi_rapidity_kernel_solved_2026.py). `PREDECLARED.md` (sha256 c7c8ca325217b87e12de50c2ca0b6b9daab1ab1017d9a42d1b348f0796ecd776, written before any script ran) fixed the verdict rule: TRUE needs (i) the arithmetic, (ii) a canonical kernel-level map, (iii) matching Sciama strength, (iv) the record's regime constraints; TRUE ONLY FOR THE MOMENT = (i) but not all of (ii)-(iv); FALSE = (i) fails. Result: (i) holds, (ii), (iii), (iv) each fail. My hand expectations (M0 = 8 pi, x ~ 3e3, Theta ~ 2e-4) were all confirmed; none decides the verdict by itself, since (ii) and the structural point (S2) are independent of the numbers.

`run_all.sh` reruns everything in 15 s, exit 0 (sympy 1.13.1, mpmath 1.3.0, numpy 1.26.4): **66 checks pass, 0 fail; 22 controls rejected, 0 not rejected; 8/8 mutants caught.**

| script | content | checks / controls |
|---|---|---|
| `z01_record_kernel_definition.py` | the record's kernel: rapidity gap, support, M0 = N, M1 = N lambda, closed form (8) vs quadrature, short/long limits, the (2/3) renormalisation, M1 = (4/3) t_Lambda, N >= 2.1e6 reproduced | 16 / 4 |
| `z02_moments_and_cutoff_map.py` | moments of four shapes, cutoff map R_c(shape, M0), the two 2/3 factors, shape invisibility, Sciama's physical strength (cases a, b, c, screened), the acceleration weights of the record (midpoint form u^2, exact tail) | 25 / 8 |
| `z03_sciama_vs_record_structure.py` | Sciama force expansion M0 a - M1 adot, identity F = M0 a - dTheta/dt, step responses, frequency vs acceleration crossover | 11 / 4 |
| `z04_regime_and_ephemeris.py` | exact circular-orbit Theta for the sharp kernel, x = T Omega table, structural long-memory exclusion, Delta/bound for four kernels with the record's mu_2, required density | 14 / 6 |
| `z05_mutation_harness.py` | 8 single-line mutants (wrong moment, wrong requirement, wrong strength, wrong renormalisation, wrong closed form, wrong weight, unnormalised kernel, loosened bound): every one must make its script fail | 8 / 8 caught |

Literature: none opened; every source is in-repo (listed above). Sciama 1953 is not opened: its content is used only through X3's stated premise F/m = -int (G rho/c^2) a(t - r/c) dV/r.

## (1) What the record's kernel is (z01)
Action S = -m c^2 int [mu(Theta) dtau + (1 - mu(Theta)) dt], Theta(tau) = int_0^inf ds K(s) arccosh(-u(tau).u(tau - s)/c^2). K has dimension 1/time; s is the **proper-time lag along the particle's own worldline**; there is no G, no matter density and no spatial integral anywhere in the action (the record itself says so: "the worldline sector supplies no time"). theta(s) -> |a| s/c (checked symbolically). For K = (N/lambda) e^(-s/lambda): **M0 = int K ds = N** (the weight, free, needed >= 2.1e6; recomputed: 2.13e6 at Mercury), **M1 = int s K ds = N lambda**, closed form Theta = (4Nv/c) x coth(pi/x)/(4 + x^2), x = lambda Omega (matches quadrature at x = 0.05, 1, 3 to 12 digits); short memory Theta -> M1 |a|/c, long memory Theta -> (4N/pi) v/c. The requirement M1 = (2/3) c/a0 has its (2/3) from the action's memory force (mu_eff = mu + (Y/2) mu' -> (3/2) Y in the deep limit), not from the kernel. Numbers: M1 = 67.65 Gyr = (4/3) t_Lambda (t_Lambda = 50.74 Gyr); c/a0 = 101.5 Gyr = 2 t_Lambda.

## (2) The cutoff for each shape (z02)
K = M0 k(s/T)/T with k unit-normalised: M1 = M0 m1 T = (4/3) t_Lambda gives R_c/R* = (4/3)/(M0 m1):

| shape (weight on the lag) | m1 | R_c/R* at M0 = 1 | note |
|---|---|---|---|
| sharp r dr on [0, T] (Sciama 1/r kernel) | 2/3 | **2** (= c^2/a0) | X3's case |
| uniform dr | 1/2 | 8/3 | 1/r^2-type weight |
| exponential (record's minimal kernel) | 1 | 4/3 | decay time |
| r e^(-r/R) dr (record's gamma-2 / Yukawa) | 2 | 2/3 | X3: c^2/(3 a0) |

All scale as 1/M0. The pre-renormalisation requirement M1 = c/a0 would give 3 R* for the sharp shape (control): the "clean Rindler distance" is the product of two unrelated 2/3 factors, so its cleanness is not evidence. At the same M1 the record's own three shapes plus the sharp one give the same Theta to 1e-4 (z02 M4): the action cannot tell them apart.

**Sciama's physical strength** (weight 4 pi G rho u du, M0 = 2 pi G rho T^2 = I, M1 = (4 pi/3) G rho T^3; mean lag M1/M0 = (2/3) T):
- (a) at X3's T = c/a0: M0 = 8 pi (X3's I), M1 = (32 pi/3) t_Lambda = 8 pi x the requirement; a0_eff = a0/(8 pi).
- (b) physical strength AND the requirement: T = pi^(-1/3) t_Lambda (34.6 Gyr, R_c = 0.683 R*), M0 = 2 pi^(1/3) = 2.93 (N^3 = 8 pi).
- (c) Sciama closure M0 = 1: T = t_Lambda/sqrt(2 pi), a0^2 t_Lambda^2 = 2 pi (X3's R_S row).
- screened r e^(-r/L) dr at physical strength: L = (6 pi)^(-1/3) t_Lambda, M0 = 1.77.
The dimensionally natural identification (K := w_S, both 1/time, no extra constant) is therefore case (b), not X3's normalised one: **X3's R_c = c^2/a0 requires dividing Sciama's coupling by 8 pi**, which is X3's own M5 (g = 1/(8 pi)) seen from the kernel side.

## (3) Structure: same words, different functionals (z03)
- Sciama (X3's premise): F/m = -int w_S(u) a(t - u) du is **linear** in the acceleration history. Exact expansion int w a(t - u) du = M0 a - M1 adot + (M2/2) addot: a steady acceleration sees M0 only (response independent of |a|), M1 is the mean retardation times M0 and multiplies the jerk, so its crossover is a frequency 3/(2T), i.e. the acceleration (3/2)(v/c) a0, velocity dependent.
- Record: inertia = m mu(Theta) with Theta = M1 |a|/c (magnitude, nonlinear); a0 = (2/3) c/M1 is where mu crosses over, using the **first** moment through the rapidity gap and c.
- Exact identity for one kernel: Sciama's force = -m (M0 a - dTheta_S/dt) where Theta_S is the record's functional evaluated at K = w_S; for a steady acceleration dTheta_S/dt = 0 and the record's Theta drops out of Sciama's force.
- X3 compares the moment of the weight on the **acceleration** (force) with the record's K, which weights the **rapidity gap**; the record's own acceleration weights for K = 4 pi G rho s are 32 pi G rho u^2 (midpoint form) and 2 pi G rho (T^2 - u^2) (exact tail), neither Sciama's ramp.
- Step response (exact rapidity gap): Sciama F/(m a) = 2 pi G rho t^2. The record's Theta = M0 a (t - t^3/(3T^2)): **linear** in t, Theta/Theta_DC -> (3/2)(t/T), Theta -> M0 x (speed gained): the long-memory branch, which the record excludes structurally (matching deep MOND needs f'(v) = v^3/(r a0), r-dependent; recomputed). X3's (t/T)^2 statement is right for the Sciama force but not for the record's Theta.

## (4) Regimes and the ephemeris (z04; record's mu_2, mu_eff, Delta = g (1 - mu_eff) <= 3.66e-14 m/s^2, x = lambda Omega <= 0.1 => lambda <= 0.98 Myr, all reproduced)
| kernel | Theta(Mercury) | needed | Delta/bound (Mercury; Saturn) |
|---|---|---|---|
| A: X3 (N = 1, T = c/a0) | 2.0e-4 | 428.7 | 1.1e12; 1.8e9 |
| B: physical strength at c/a0 (N = 8 pi) | 5.1e-3 | 428.7 | 1.1e12; 1.8e9 |
| C: physical strength + requirement (N = 2.93, T = 0.683 t_Lambda) | 5.9e-4 | 428.7 | 1.1e12; 1.8e9 |
| D: record's surviving exponential (N = 2.13e6, lambda = 1e12 s) | 428.4 | 428.7 | 1.003; 0.95 (edge of the bound, as in the record) |

x = T Omega for T = c/a0: Mercury 2.6e12, MW 1 kpc 1.0e4, 8 kpc 2.9e3, 30 kpc 6.2e2; T/lambda_max = 1.04e5. Shortfall Theta_min/Theta_A = 2.13e6 = the record's N_min: the identified kernel is the record's "vacuum free-fall time at unit weight" (mi_local_source_for_K: found in form, killed by data) with a different shape; its own O(1)-weight exponential has Theta(Mercury) = 2.7e-4, the same class. Reverse direction: the record needs a kernel "short in duration, enormous in weight"; for a sharp kernel with M1 = (2/3) c/a0 that is T = (c/a0)/N = 1.5e12 s (R_c = 14.6 kpc), and a Sciama weight N = 2 pi G rho T^2 would need rho = 2.3e-9 kg/m^3 = 3.9e17 rho_Lambda (= N^3/(8 pi), analytic). Cosmological Sciama is long and weak.

## What is NOT established
- Not re-derived: the action's equations of motion; I took the record's (12), (14) as given and only recomputed mu_eff limits and the series 1 - mu_eff = 1/(32 Theta^4) [1 + 1/(2 Theta^2) + ...] (the 3e-6 correction at Mercury is now included; the record quotes the leading term).
- Sciama side is X3's premise (coupling coefficient 1, uniform density, sharp cutoff, retarded acceleration weight); with a general coupling g the strengths above scale by g and the 8 pi becomes g^-1 (no rational g helps, X3 M5). Sciama 1953 not opened.
- A hidden-sector origin of K (record: fable_independent_2026/L65: memory as bookkeeping of a bath whose propagator is K) is not excluded by this referee: there K is a free spectral function and could have any weight, but then it is not Sciama's cosmological kernel.
- Non-relativistic circular orbits; the ephemeris bound and planetary data are the record's, not independently checked.
- Nothing here bears on the value of kappa: the identification would relocate the 1/2 into "unit weight and cutoff at the Rindler distance", and unit weight is the record's excluded case.

## Consequences for the campaign (for the caller; I edited no record file)
- X3 README Part B item 2 / "Modified inertia" bullet 2 and caveats (line 72) should read "the record's requirement, as a mean lag of a unit-weight sharp r dr weight, is T = c/a0; that weight has 1/(8 pi) of Sciama's strength at this cutoff; the record's kernel is not Sciama's". The step-response remark should say the record's Theta is linear in the duration.
- `p11_machian_cutoff_candidates.py` inherits X3's premise ("the record's premise is R_c = c^2/a0"); its cutoff search is a search over cutoffs of the unit-weight r dr shape and carries the same caveat (not re-run here).

## Verdict
**TRUE ONLY FOR THE MOMENT.** X3's arithmetic (M1 = (2/3) R_c/c, R_c = c^2/a0 at unit weight) is correct and now independently recomputed; the identification of the record's kernel with Sciama's is not: it needs an 8 pi rescaling of Sciama's coupling, is shape- and weight-arbitrary (four cutoffs 2, 8/3, 4/3, 2/3 R*), rests on two unrelated 2/3 factors cancelling, compares a force weight with a rapidity-gap weight, and lands in the long-memory regime that the record itself excludes, violating the ephemeris bound by 1e12. kappa = 1/2 stays FITTED.

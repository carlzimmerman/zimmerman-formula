# QX6: the clock-depth cluster boost cannot be derived from the action. Clusters stay FAIL

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle. No LCDM inputs.
Criteria: FROZEN_CRITERIA.md + iter_*/FROZEN_CRITERIA.md (3edba4879f), committed alone before any code.
Post-result amendments: AMENDMENTS.md (03f80829fc), declared before their checks ran; they cannot produce a PASS.
Scripts: qx6.py (graded, plus `--mutate`), qx6_amend.py (A1/A2). Each takes a few seconds on one thread.
QX5's samples and key-a construction are reused by executing qx5.py's own source.
Lean: fable_independent_2026/lean_2026/QX6_clock_depth.lean (+ _MUTATE twin).

The question: QX5's one surviving lead is a phantom multiplier F keyed on the khronon clock depth Q - 1 = |Phi|/c^2.
It passes X-COP only when X-COP sets F's threshold and amplitude. Can the action fix both from record constants,
with no cluster input?

## Labels (both footings agree)

| Route | What the action gives | Result | Label |
|---|---|---|---|
| 1. v3s K(Q) = mu_K^2 (Q-1)^2 | An extra density rho_K = mu_K^2 \|psi\|/(4 pi G), linear in Q - 1, size ~ (mu_K r)^2. No threshold in Q - 1. One constant, mu_K | Scanned over mu_K from 1e-3 to 1e4 Mpc^-1 (701 points), psi self-consistent (the potential of M_HSE). No mu_K passes G-X: min rms 0.271 / 0.262 at mu_K 1.55 / 1.48; mean 0 at mu_K 1.78 / 1.74 with rms 0.280 / 0.273. Zero-point variant (psi = 0 at 10 R200): min rms 0.320 / 0.308 | **DEAD for every mu_K.** The galaxy and CMB bounds are not even needed. They would conflict anyway: S4 <= 0.1, CMB >= 3.98e4 (Lean `route1_no_window`) |
| 2. a0 tied to khronon-frame rho_DE | v3s: Lambda is lapse-invariant, f == 1, F = 1. AC2q: rho_loc/rho_bg <= N^-2 <= 1 + 2.1 (Q - 1) (Lean `rho_share`, `lapse_bound`) | Largest F - 1 = 2.5e-4. X-COP needs >= 1.35 / 1.11, so it falls short by x5.4e3 / x4.4e3. X-COP mean unchanged (+0.4675 / +0.4345) | **DEAD** (analytic factor; Lean `route2_short`) |
| 3a. Any other Q-dependence in the action on the table | Q enters v3s only through K(Q). J(Y) depends on Y = A.A/c^4 with A = grad ln N, i.e. on g only: QX2 iter 2's universal-nu class, DEAD. AC2q adds X(N) (route 2), V(phi), P.A and W(p, a0). Checked against V3_FULL_PICTURE section 1 and AC7's Lagrangian | None left | **DEAD** (action on the table) |
| 3b. A new term with a native threshold | 65 trials (dimensionless groups of record constants x 5 powers). 2 land in the window W between the galaxy keys (<= 4.6e-6 / 4.8e-6) and the X-COP keys (>= 4.5e-5 / 4.7e-5): sqrt(a0 Lstar/c^2) = 2.64e-5 / 2.98e-5, and sqrt(a0/(c^2 mu_min)) = 2.84e-5 / 3.12e-5 | Even with the cluster-set amplitude (4.09 / 3.66), the step fails G-X (rms 0.106 / 0.105) and fails groups (+0.36/+0.20, +0.32/+0.16: group keys sit below the step). Coma UDG z 2.76 / 2.65 | **COINCIDENCE, then DEAD on data.** A2: no single step (A from 1 to 10, any k_t in or above W) passes G-X. Min rms 0.1050 / 0.1041 against the 0.10 line, so the miss is narrow |

Door: **Clusters FAIL.** No route derives F(Q - 1) from the action. On X-COP's profile shape, a threshold boost at
any location fails narrowly (rms 0.104-0.105 against the 0.10 line). The groups' keys overlap the galaxies' keys,
so a depth key cannot boost groups while leaving galaxies alone. QX5's isotonic K fit passed only because it was
free to bend between keys. The lead is now precise: the boost would need a graded F(Q - 1) whose shape is set by
clusters, which is CLUSTER-SET, a FAIL by the no-tuning rule.

## Known answers and controls

- iter 2's X-COP mean (+0.4675 / +0.4345, a shift of -3e-5 from the plain law) equals QX2 iteration 1 to the printed digits. At mu_K = 0.1, iter 1 gives +0.464 / +0.432, equal to QX2 iter 5. The mean-zero mu_K is
  1.78 / 1.74, equal to QX2's reported value.
- iter 1 MUTATE: with X-COP planted at mu_true = 1.0, the scan finds a passing interval [0.85, 1.15] containing
  1.0, on both footings. **BITES.**
- iter 2 MUTATE (x1e4): the mean moved by -0.179 / -0.185 against the frozen line <= -0.2. **DID NOT BITE as frozen.**
  A1 (post-result, x1e5): -0.556 / -0.566, **bites**. Route 2's label rests on the analytic factor (x4e3 short),
  not on the grader.
- iter 3 MUTATE: the planted step (amplitude F_med at sqrt(k_g k_x)) gave rms 0.106. **DID NOT BITE as frozen.**
  A2 shows why: no single step can pass G-X, so this control cannot bite for any step location. That finding is
  itself the strongest result here.
- SPARC recheck (iter 1): at mu_K = 0.1 and at the cluster's mean-zero mu_K, the SPARC mean and rms shift by <= 4e-4.
  Galaxies are blind to the K term at these mu_K; the term dies on cluster shape, not on galaxies.
- Sun (iter 1, mu_K 1.78): g_K(1 AU) = 1.5e-23 m/s^2 = 2.5e-21 g_N. Harmless.
- Rerun: qx6.json byte-identical (md5 9fdaa8ef49e9).
- Lean QX6_clock_depth: 7 theorems, standard axioms only. The MUTATE twin fails on all 3 false claims (sorryAx on
  each).

## Scope

Statics, spherical symmetry, hydrostatic X-COP masses, QX5's group bracket rule. Route 1's psi is the potential of
the measured mass, which is self-consistent for a passing model. The scan proves that no mu_K yields that mass.
Route 3b enumerates only the declared group set; a coincidence is never a derivation. Lensing, the Bullet offset
and growth are moot, because nothing survives.

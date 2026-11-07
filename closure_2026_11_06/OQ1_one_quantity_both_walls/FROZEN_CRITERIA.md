# OQ1 frozen criteria: can one action-native scalar set the extra gravity in hot systems AND switch the law off on the linear web?

Frozen before any OQ1 script or OQ1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane: no
particle; no LCDM input; both footings (canonical a0 9.3603e-11, Lstar 21.7 pc; alt a0 1.1312e-10, Lstar 22.9 pc), never
pooled; "passes" needs both. No downloads: every input is on disk and named below. One thread, under 1 GB RSS, preemptible
(checkpoint on SIGTERM). Seed: SEED_2026_11_06.md ("find one covariant quantity that sets that amplitude in today's hot systems
and is non-zero in the early universe, or show the two failures need separate causes").

## 0. Why this quantity, and what is not re-proposed

- SV5 (79a75ab40d) located the CMB wall: it is the a0 law on the linear web. The web sits at 0.01-0.6 a0, so a dust-like source
  is boosted 74.7 / 89.4x in lensing power against the line 1 +- 0.072. SV5 iter_2's conditional branch (A-web: phantom off on the
  web) found that the AC2q charge Sigma = D.P + 2X (QX17: D.P = Pi = the phantom density) then separates hosts (Sigma_* 8.0 / 6.0
  rho_DE at turnaround) from the web (Sigma_web = 2X <= 2 rho_DE). No lane has asked whether the SAME scalar can also set the
  amplitude the hot classes need.
- So the primary candidate is q = Sigma / rho_DE, the AC2q switch variable, evaluated self-consistently (Sigma depends on the
  phantom it controls; section 3).
- Reported only (not graded for a label): q_b = rho_b,local / rho_DE (local baryon density; QX5 killed the ENCLOSED density) and
  q_t = sqrt(E_ij E^ij) / (4 pi G rho_DE) (Newtonian tidal invariant of the baryons).
- Not re-proposed (dead, both footings): p/rho, gas / host temperature, virial heating, khronon velocity, enclosed density, gas-g,
  depth (QX6), kinematic support (QX22), cold gas (QX23), morphology (QX25), environment / external field (QX24, EV1), shock
  entropy (EN1, field-equations chat). Matter kinematics are not action-native (DX1 D1: minimally coupled matter reaches the
  khronon only at (v/c)^2 <= 1.1e-5).
- Expected outcome, stated in advance: probably DEAD. Off the web, rho_ph is fixed by g_N and its radial slope, and QX20 found
  the hot/cold step at fixed g_N. The web arm is the new part. Grade it as hard as a win.

## 1. The model graded

One function F(q) >= 0 multiplies the law's phantom everywhere (GB1 interface, gb1.py read-only):
g_pred = b g_N + F(q) [g_law(b g_N) - b g_N], with b from GB1 L1 (QX26 IMF; ST1 showed IMF carries the ellipticals and most of
KiDS, so it is applied everywhere, never per class). Arm B (dust): the same q switches the K(Q) sector's Jeans scale exactly as
SV5 iter_2 (mu_K^2 -> mu_K^2(Sigma), nonincreasing), so one scalar does both jobs.

## 2. Inputs (per class; the allowed F interval at each class's measured points)

F_need per point = (g_obs - b g_N) / (g_law(b g_N) - b g_N), g_obs = 10^D g_law(g_N), D the plain-law offset built exactly as GB1
(QX20 loaders, QX16-fixed). Class allowed interval = class mean F_need +- 2 sigma_class (bootstrap, 10,000 resamples, seed 21),
except where a gate line sets it:

| Class | Points | Allowed F | q construction (isolated, no EFE; EFE variant reported where the loader carries it) |
|---|---|---|---|
| SPARC discs | GB1 G1 points | the F band that keeps \|Z\| <= 0.057 (G1 line) | rho_ph from SV5 iter_2's host formula on QX20's SPARC baryon model |
| LG field dwarfs (no-step anchor) | GB1 G6 LG field | G6: CI contains 0 relative to the SPARC anchor | Plummer, r_h from LW1 |
| X-COP | GB1 G2 (35) | from G2 \|mean\| <= 0.05 | spherical gas + BCG, QX20 build |
| groups | GB1 G3 (20 x 2), f* = 0 and 1 both | from G3 2 sigma_log per point | QX5/QX7 group profile; if only R2500 and R500 are on disk, a power-law rho_b between them (frozen construction) |
| X-ray ellipticals | GB1 G4 (7 x 3) | from G4 \|mean\| <= 0.15 | Humphrey models via QX5 loaders |
| bright M31 dSphs | GB1 G6 (25) | 2 sigma_class | Plummer, LW1 r_h |
| Coma UDGs | GB1 G5 (9) | from G5 \|mean\| <= 2 sigma_U | Plummer, S1 r_h |
| Solar System | G8 | F_SS <= the G8 bound | Galaxy at the Sun as SV5 C4, and the Sun's own field at 1 AU, 9.58 AU |
| linear web | SV5 iter_1 realisations, z 0.25, 0.5, 1, 2, 3 | F_web <= F_web,max, the largest uniform F with lensing amplitude r <= 1.072 on SV5 iter_1's statistic | Sigma_web = F_web rho_ph,web + 2X, X <= rho_DE (SV5) |

## 3. Self-consistency

Sigma depends on F. For each footing iterate q_k+1 = q[F_k(q_k)] from F_0 = 1 at every point until max |Delta log q| < 1e-4
(cap 200 iterations). Report every fixed point found from starts F_0 in {0, 1, 10}; if the starts reach different fixed points,
each is graded and the label takes the worst.

## 4. Stages and labels

- **S1 existence.** Bin log10 q at width 0.2 dex (frozen). In every bin with points from two or more classes, intersect their
  allowed F intervals. Empty intersection in any bin on either footing: **DEAD**, with the bin, the classes and the gap in dex.
- **S2 construction (only if S1 holds).** F(q) = piecewise-linear in log q through each bin's intersection midpoint; no other
  freedom. Grade it on GB1 G1-G8 (read-only, every line unchanged) plus G9-proxy: SV5 iter_1 lensing amplitude r <= 1.072 with
  F(q) on the web, self-consistent, at every z; and arm B on SV5 iter_2's C2, C3 (QX10 convention, disclosed), C4.
- **S3 prediction.** Leave-one-class-out: rebuild F(q) without class k and predict k (interpolation, or extrapolation <= 0.5 dex
  in log q; beyond that the class is UNCONSTRAINED BY OTHERS). A hot class whose q range touches no other class's range makes the
  function a class label in disguise.

Labels (per footing, the candidate takes the worse):
- **DEAD**: S1 empty intersection.
- **FAILS (rows)**: S1 holds, S2 fails a named row.
- **CONSISTENT, NOT PREDICTIVE**: S1 and S2 hold but S3 fails, or any hot class is UNCONSTRAINED BY OTHERS.
- **SURVIVES BOTH WALLS (scoped)**: S1, S2 and S3 hold. Even then it is not adopted and not closure: it still owes an action term
  whose Euler-Lagrange equations give F(Sigma), its field equations (QX17 machinery), well-posedness (AC21 rule) and the full PR4
  shape chi^2 <= 18.5 through QX3's solver.
- Missing feature for a class: that class's cell is NO VERDICT and counts as not passing; the "swing harder" rule applies, so the
  construction in section 2 is used rather than stopping.

## 5. Known answers (KA FAIL means stop and fix; nothing is graded)

- KA1: GB1 L0 class means from gb1.json to 1e-6 (X 0.467499 / 0.434523, E 0.209888 / 0.188763, S 0.027383 / -0.000603).
- KA2: L1 elliptical mean = QX26 D_imf to 1e-6.
- KA3: SV5 iter_1 lensing amplitude at F = 1: 74.7 / 89.4 to 1e-3 relative (sv5 JSON).
- KA4: SV5 iter_2 Sigma_* = 8.0 / 6.0 rho_DE and web fractions F_f(z) to 1e-3 (sv5_iter2.json); deep-MOND point-mass phantom
  ratio 1.0000.

## 6. MUTATE (power; separate outputs oq1_MUTATE_*)

- M1 planted truth: replace every F_need by F_true(q) = 1 + 3 (q/q_med)^0.5 at each point's own q, plus Gaussian noise at that
  point's measured error (seed 21). S1 must find no conflict and S3 must pass. If not, the method has no power to find a true
  one-quantity law and the run says NO VERDICT.
- M2 planted step: the same, plus +0.3 dex on the hot classes at fixed q. S1 must read DEAD. If not, it has no power to kill.
- M3 Newton (F = 0 everywhere): G1 must fail.

## 7. Outputs

`oq1.py` writes `oq1.json` / `oq1.out` (and `oq1_MUTATE_M*.json`); `RESULT.md` gives, per footing, the q range of each class,
the bin table, the label and the margins read from the JSON. Reported side tables for q_b and q_t carry no label. Any change
after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.

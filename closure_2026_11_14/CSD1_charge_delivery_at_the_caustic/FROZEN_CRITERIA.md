# CSD1 FROZEN CRITERIA: does the falling clock's own flow deliver, inside the k-th caustic, the charge the law's halo needs there?

Written 2026-11-14, begun 14:32 EST by the clock (`date`). Committed alone, before any script of this lane exists and
before any number of this lane is computed. TEST lane, not blind. Adopts nothing, relabels nothing, registers nothing.
Footings graded separately and never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2. The cold component is
cold dark energy (a field, never a particle). Nothing here can say the theory is closed or that the data favour it.

## 0. What is new here, and what is not

Already on the record (read, not repeated):
- FLD1 (`fable52_push/FLD1_fold_reach/`): the clock's shell equation from z 10 around an isolated baryon seed; R_fold(t),
  R_ta(t); on A4's grid the charge inside FIXED radii 10 / 30 / 100 / 300 kpc at z = 0 only is 1.6 to 5.1 % of the law's
  halo; about 1.06 M_b has turned around. COL1: the same equation up to first crossing.
- XJ1 (`closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface/`): the caustic radii R_1 = R_fold, R_2, R_3 (shell
  runs with a passage counter); at PROFILE level, s = C_R(R_set)/C_B(R_set) on the forest's haloes, 0.47 to 1.70 at the
  third caustic (z 2.2 to 4.4).
- The junction note (`codex_mass_budget_2026_11_14/latest_review/JUNCTION_THEOREM.md`): the normal-current condition
  [J^r] - Rdot [J^t] = 0 and its advective reduction; it says itself that it has no tracked velocity or front-speed
  history and no number for the non-advective flux.
- The settling lanes (SET1, EDG1, AKS1, VSH1, VSJ1, CLOSE-1/DT2): each asked whether some added physics settles the clock
  into the law; none measured the charge the flow itself has inside the moving caustics.

New in this lane, and only this:
1. Part 1: the static balance of FLD1's shell equation shown to be the law (exact); the interface condition re-derived;
   the size of QX17's non-advective flux lambda P/Q against N v at the caustics, with its dependence on a layer width.
2. Part 2: the delivery ratio D_k(t) = Q_flow(< R_k(t), t) / C_law(R_k(t)) at the MOVING caustics k = 1, 2, 3 and at 0.5
   R_fold, over the whole history, for nine masses and three supplies; the one-sided densities, the front speed, the
   inflow the advective condition requires against the flow's own, and the equal-charge radius.
3. A third supply (S-cos): the clock's own shell equation with a cosmological initial perturbation tuned so that, with
   the law off, the patch's share turns around by today.

## 1. Part 1 (exact items)

**P1a. The static balance is the law.** FLD1's shell acceleration (hubble mode, enclosed charge excess m, its field
y = G m / r^2, baryon field g_N) is r'' = -g_N - y + U(y) + (mean-density terms that cancel against the background), with
U(y) = a0 y / (a0 - |y|). Claim: r'' = 0 with 0 < y < a0 is equivalent to g = g_N + y obeying g^2/(a0 + g) = g_N, and then
m = r^2 (g - g_N)/G = FLD1's Mph(r) (the law's phantom mass for the softened point baryon).
- sympy: residual of the equivalence exactly 0 (both directions; the root y in (0, a0) unique).
- numeric: on 2000 points of g_N / a0 in [1e-6, 1e3], |g^2/(a0 + g) - g_N| / g_N <= 1e-12, and the enclosed excess at
  balance equals FLD1's Mph to 1e-12 relative for log M_b 8 and 11.5 at r 1 to 1000 kpc.
- **Twin TW1:** U(y) -> a0 y/(a0 + |y|) (sign of the cap flipped). The numeric check must fail (deviation > 1e-3).

**P1b. The interface condition, re-derived.** sympy: J = J_in H(-F) + J_out H(F), F = r - R(t), in one radial dimension
with the spherical volume factor; the coefficient of delta(F) in d_t(r^2 J^t) + d_r(r^2 J^r) equals
r^2 ([J^r] - Rdot [J^t]) exactly (residual 0). With J^t = N, J^r = N v (COL1's weak-field reduction) this is
N_out (v_out - Rdot) = N_in (v_in - Rdot). Integrated form: for a standing interior (v_in = 0), d/dt C_in(< R(t)) =
4 pi R^2 N_in Rdot = 4 pi R^2 N_out (Rdot - v_out), i.e. the interior's charge equals the charge the flow has carried
across the moving boundary, and with no surface reservoir the enclosed charge is continuous at R: Q_flow(< R) = C_law(R).
So D_k = 1 is the integrated form of the no-reservoir condition at the k-th caustic; D_k != 1 measures a surface charge
S = C_law - Q_flow that some non-advective channel must supply or remove.
- **Known answer KA2:** the junction note's rational example (L = T = 1, C_B = r, C_R = r^2, R = 1/2): t = 2/3,
  N_in / N_out = 3/2; Rdot = 2, v_out = -1 satisfies the condition; Rdot = 0 with v_out < 0 fails it. Exact.
- **Twin TW2:** sign of Rdot flipped in the condition. KA2's satisfying pair must then fail.

**P1c. The size of the non-advective term.** QX17 E3 (unitary gauge, c restored): the khronon flux is
c J^i = v^i rho_Q - (c lambda) P^i (Q = 1 + O(Phi/c^2)), and E2's normal part gives, at gamma_L = 0,
c lambda = (1/c^2)(d_t + v.grad) Phi; with gamma_L > 0 a further c lambda_gamma = gamma_L (d_t + v.grad) Pi_+ / c
(gamma_L Pi_+ = 2 pi G rho L*^2 / c^2, L* = 21.7 / 22.9 pc canonical / alt, QX17 section 3). In the spherical weak field
P_r(R) = m(< R) / (4 pi R^2) for the charge m whose divergence P carries. The ratio
eps = |c lambda P| / |N v| = (|D Phi / D t| / c^2) m / (4 pi R^2 N |v|)
is evaluated at R_1, R_2, R_3 for log M_b 10.7 and 10.825 (Milky-Way-like; XJ1's own Milky Way mass) at z = 0, both
footings, on the outside (m = Q_flow, N = N_out, v = v_out from the S-seed run) and on the law's side (m = C_law,
N = N_in, |v| -> |Rdot|), with D Phi / D t = v g + d_t Phi, g the law's field at R, d_t Phi bracketed by g R / t_age.
Reported in SI and checked by an independent SI computation (G = 6.674e-11, kpc = 3.0857e19 m, M_sun = 1.989e30 kg).
Also reported: eps against the flux the advective condition lacks, |j_extra| = N_out |Rdot (1 - N_in/N_out) - v_out|.
Layer width: the lambda_0 piece depends on Phi and its first derivative only, which are continuous across a layer with no
mass sheet, so its size does not change with the width w; the gamma_L piece scales as 1/w. Both are evaluated for
w = 10 kpc, 1 kpc, 1 pc. Lead's estimate to test: of order Phi/c^2, about 1e-6.

## 2. Part 2 definitions (frozen)

- Masses: log M_b 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5 (FLD1's). Redshifts graded: z 0, 2.2, 3.0, 4.4; history
  reported over every output (FLD1's 0.02 Gyr cadence). Scalars at a named z are interpolated in z on the series, as XJ1
  does.
- R_k(t): XJ1's definition: the largest current radius among shells that have passed the centre (been reflected) at
  least k times; k = 1, 2, 3 (R_1 = R_fold). Also R = 0.5 R_fold. A cell with R_k = 0 (caustic not yet formed) is
  "not formed" and excluded from its label; it is counted.
- C_law(R): FLD1's Mph (softened point baryon, EPS = 1 kpc, the footing's a0, FLD1's units).
- N_in(R) = C_law'(R) / (4 pi R^2) (central difference, relative step 1e-5).

**Supply S-seed** (FLD1's isolated seed, exactly: hubble mode, z_i 10, N 2400, scaled grid, A1 reflection). Run as
FLD1's `fld1_shells.py` executed with stated text insertions only (XJ1's pattern): XJ1's passage counter, and per output
the extra columns below.
- Q_flow(< R) = sum of shell charges dM with current r < R (all shells; FLD1's reads convention). Reported beside it: the
  excess Q_flow - (4 pi/3) nbar(t) R^3, and the uncrossed-shell part.
- D_k = Q_flow(< R_k) / C_law(R_k), k = 1, 2, 3, and D_half at 0.5 R_fold.
- N_out: charge in shells with r in [R_k, (1 + w) R_k] over that shell's volume, w = 0.10 (brackets 0.05, 0.20 reported);
  v_out: the charge-weighted mean radial velocity there (net flux / density, all streams). N_flow,in from [(1 - w) R_k, R_k]
  reported.
- Rdot_k: least-squares slope of R_k(t) over outputs within +-0.25 Gyr (km/s; reported only where R_k > 0 over the whole
  window).
- Required inflow, standing interior: v_req = Rdot_k (1 - N_in / N_out). Reported: v_req, v_out, their difference
  (= j_extra / N_out), and the surface accumulation rate Sdot = 4 pi R^2 [N_in (0 - Rdot) - N_out (v_out - Rdot)] in
  units of C_law(R_k) per Gyr.
- R_eq: on the sorted shell radii at the output, D(r) = Q_flow(< r) / C_law(r) for r in [1 kpc, R_ta]; R_eq = the largest
  r with D(r) >= 1, reported in units of R_fold; "none" if D < 1 on the whole range. The smallest r with D(r) < 1 is
  reported too.

**Supply S-ref** (the cosmological reference as the delivered charge): Q_flow(< r) = C_R(r) of FRZ1's "Rb" layout for
the halo that FZS1's rules assign to that M_b at that z (galaxy regime: Mb_fold(hb) / h = M_b; interpolated in log M on
FRZ1's halo grid, both C_R and C_B evaluated at R_k converted to comoving Mpc/h as FZS1 does: R x 1e-3 x (1 + z) x h).
Then D_k = C_R(R_k) / C_B(R_k) = s. R_k from XJ1's shell files (`shells/`). Haloes above v*(z) (cluster regime) are
"reference throughout": D = n/a, counted. N_in / N_out = C_B' / C_R' at R_k (one-sided). v_req = Rdot_k (1 - N_in/N_out)
with Rdot_k from the S-seed run (the reference has no velocity field; v_out is not defined and is not invented). R_eq:
the largest r <= r_ta with C_R(r) >= C_B(r), in units of R_fold. Also reported: D against the pure phantom (without the
layout's linear remainder term).

**Supply S-cos** (the clock's own shell equation with a cosmological patch). FLD1's equation, hubble mode, with an initial
growing-mode Lagrangian overdensity delta_i(X) = min(A M_b / M_X, 0.3), M_X the shell's Lagrangian charge, imposed at
z_i = 10 as r_i = X (1 - delta_i/3)/(1 + z_i), v_i = H(z_i) r_i (1 - delta_i/3) (EdS growing mode). Nothing else changes.
- Tuning, with the law OFF (FLD1's M1 arm, the clock gravitating on itself as dust), canonical, log M_b 10.45, N 1200:
  A on {4, 7, 10} (more points only if the target is not bracketed), interpolated in log A to the A at which FLD1's
  `charge_turned_around_over_Mb` at z = 0 equals PD1's z = 0 share (59.486 canonical / 59.503 alt, read from `pd1.json`),
  then one confirming law-off run at N 2400; accepted if within 10 %. If not reached, S-cos is NOT EVALUABLE.
- Graded: law ON with that A at log M_b 9, 10.45, 11.5, both footings, N 2400 (the same quantities as S-seed).
  Reported, not graded: law OFF with that A at the same three masses, canonical (what cold dust would deliver in the same
  device).
- Stated assumptions: a point-seed tail (the same shape as the baryon seed), spherical, one amplitude for all masses,
  FLD1's independent-shell device behind the fold (each shell keeps its Lagrangian enclosed charge after crossing; the
  reflection is FLD1's). Not a merger history.

## 3. Known answers (each must pass for its supply to carry a label)

- KA1 (P1a), KA2 (P1b): as above.
- KA3 (S-seed): for all 18 runs, the first five series columns equal FLD1's stored run to 1e-9 relative, and columns
  R_1, R_2, R_3 equal XJ1's stored shell series to 1e-9 relative.
- KA4 (S-seed, FLD1's "1.6 to 5.1 %"): the eight A4-grid rows (log M_b 9.4, 10.45, 10.7, 10.9, both footings) re-run with
  this lane's code; `reads_end` equal FLD1's stored files to 1e-9 relative, and the minimum / maximum of
  M_N_all_shells_over_M_ph over the 8 rows x 4 radii read 1.6 % and 5.1 % at the printed digits.
- KA5 (S-ref, XJ1's s range): XJ1's stored s (min, max) at z 2.2 / 3.0 / 4.4, cases Ec3 and Ec2, both footings
  (`xj1b2_grade.out`) reproduced to 1e-9 relative by calling XJ1's `exact_fn` read-only over FRZ1's haloes, and by this
  lane's own evaluation of C_R / C_B from the layout functions on the same haloes, to 1e-9.
- KA6 (units): C_law(100 kpc) at log M_b 10.7 recomputed in SI independently agrees with FLD1's Mph to 1e-3.
- KA7 (S-cos): with A = 0 the S-cos code reproduces the S-seed run's series to 1e-12 (log M_b 10.45 canonical).

## 4. Mutation twins (outputs in separate files, `*_MUTATE.*`)

- TW1, TW2 as above.
- TW3 (S-seed): count Q_flow by Lagrangian radius (shells with X/(1+z)-scaled Lagrangian position < R) instead of the
  current radius. KA4's reproduction must fail.
- TW4 (S-ref): use R_2 where R_3 is asked. KA5's Ec3 reproduction must fail.
- TW5 (labels): law OFF in the S-seed run (FLD1's M1 arm), log M_b 10.45 canonical: D_3 at z = 0 must move by >= 5 %.
A twin that does not bite is reported as such and its known answer is then not counted as independent.

## 5. Labels (per footing and supply; frozen)

Tolerance: |log10 D_k| <= 0.10 (D_k in [0.794, 1.259]). For each k in {1, 2, 3}, over every formed cell of the 9 masses
x 4 redshifts:
- **THE FLOW DELIVERS THE LAW'S CHARGE AT CAUSTIC k**: every cell within the tolerance.
- **SHORT AT CAUSTIC k**: every cell with log10 D_k < -0.10.
- **OVER AT CAUSTIC k**: every cell with log10 D_k > +0.10.
- **DEPENDS ON MASS AT CAUSTIC k**: at some redshift log10 D_k changes sign across the masses (the crossing mass, by
  linear interpolation of log10 D_k in log M_b, is named per redshift); otherwise **MIXED AT CAUSTIC k** (named cells).
- **NOT EVALUABLE**: a known answer of that supply fails, or more than half the cells are not formed.
The lane's headline word per footing and supply is the pair (k = 2, k = 3), the caustics XJ1 found. k = 1 and 0.5 R_fold
are reported with the same words. S-cos is graded on its three masses only.

Reported, never a label: the history (min / max of D_k over z 0 to 4.4 per mass), N_in / N_out, Rdot, v_req against
v_out, Sdot, R_eq, eps.

## 6. Hand estimate (before any number)

- S-seed: D_3 at z = 0 about 0.03 to 0.08 (FLD1's 1.6 to 5.1 % at fixed radii; the turned-around charge is about one
  M_b while C_law(R_3) is about 10 to 15 M_b). D grows slowly with mass (about M_b^{1/6}). SHORT at k = 1, 2, 3 on both
  footings: 95 %. N_in / N_out at R_3 about 10 to 50; the required inflow speed exceeds the flow's own net inflow by a
  factor > 3: 70 %. R_eq: none beyond 1 kpc, or below 0.05 R_fold, at most masses: 70 %.
- S-ref: D_k = s; at the forest redshifts 0.47 to 1.70 (known); over log M_b 8 to 11.5 it crosses 1 near log M_b 10.7 to
  11.2 (XJ1's z = 0 statement): DEPENDS ON MASS at k = 3 on both footings: 75 %.
- S-cos, law on: in this equation the clock's own excess pushes outward at second order (U(y) - y = y^2/(a0 - y) > 0), so
  a cosmological perturbation should add little: D within a factor 3 of S-seed, SHORT: 85 %. Law off: D of order 0.5 to
  2: 60 %. Tuned A about 7: 60 %.
- eps (lambda_0 piece) about (v_c/c)^2, 1e-7 to 1e-6 at Milky-Way caustics, width-independent; gamma_L piece below 1e-9
  for w >= 1 pc: 80 %. So the non-advective channel cannot supply an O(1) shortfall: 90 %.

## 7. Discipline and resources

Criteria committed alone; scripts committed before they are run; frozen files never edited (dated amendments committed
alone); mutation outputs separate; explicit-path commits; nothing pushed; no outcome word in commit subjects. Compute:
`nice -n 19 python3 -I -B`, at most six shell runs at a time, each well under 2 GB; no forest boxes; nothing downloaded.
Paths relative to the repository root or computed from the script's location.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

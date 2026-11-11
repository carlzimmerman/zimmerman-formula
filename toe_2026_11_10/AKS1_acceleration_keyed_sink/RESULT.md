# AKS1 RESULT: an acceleration-keyed energy sink for the joint (2026-11-10, Part T 2026-11-11)

**Part T (the lead's corrected candidate: (A) kept whole plus local dissipation of the clock): CLOSED, ONE BRANCH ON AN
ESTIMATE / CLOSED, ONE BRANCH ON AN ESTIMATE (canonical / alt). No local dissipation of (A)'s clock (acceleration-keyed
rate, or frame-free bulk/shear viscosity, with the heat removed or kept as entropy) settles the cold dark energy into
the law's halo with an edge at an acceleration by today. So dissipation does not close the joint, and the TOE's T1 stays
OPEN.** Three branches close on exact items. The fourth (frame-free viscosity with the heat kept) closes on an estimate
with margin 8.2 / 6.8, and it escapes only with a new threshold constant.

Part T is post hoc. The lead's correction arrived after the run below had landed. Its criteria (`FROZEN_CRITERIA_T.md`,
local d44203c715) were committed alone before `aks1_t.py`. The run below (action (A) WITHOUT W and P) is now the control,
because it is route E's class, retired on 2026-11-01. Its label stands as recorded.

| branch | closes on | numbers (canonical / alt) |
|---|---|---|
| D-A(o), D-A(h): rate keyed on \|A\| | **T1 (exact):** static means A = grad Phi, which with the Legendre map is the law. On first infall A = U(G Q_ex/r^2), the law's self-field of the clock's excess charge; it has no baryon term (d/dM_b = 0). An A-key reads the field only on a clock already held. **T3 (exact in CFG461's energy model):** contraction by today <= exp(2 F a0 t0/c) | a0 t0/c = 0.1359 / 0.1642. Bound 1.312 / 1.389 at F = 1, and 1.051 / 1.062 with f = x at the edge (total field there 0.1846 a0). CFG461 needs 3.50 / 1.97 / 1.34 (alt 3.85 / 2.16 / 1.47). Below at every mass |
| D-V(o): viscosity, heat removed | **T4 Gauss (exact; SMF1 S0b):** the net polarization charge in any free-fall-bounded ball is 0 at all times, whatever the momentum equation. **T5 T-DEP (exact):** the static dust is one function of depth | static (A) at the CMB mu_K over-captures: 3.6-8.4 times the halo at SPARC radii at 198 per Mpc (COL1 Part 0), and 1.6e4 times more at mu_J. Counted twice |
| D-V(h): viscosity, heat kept as entropy | evades T-DEP (T5: n_d(depth, s)). A hot, static (A) clock with charge equal to the phantom is counted once. **T7 (estimate):** a uniform viscosity that spares the record's forest line (nu <= nu_F) cannot settle massive haloes to CFG461's edge by today | nu_F = 141.9 / 142.0 kpc km/s. nu_S = r_e*^2/t0 = 3.7 / 116 / 1160 (alt 3.0 / 96 / 961). **Margin 0.03 / 0.82 / 8.17 (alt 0.02 / 0.68 / 6.77)**, against a line of 3. Form B's cap needs margins of 2.7 to 847 |

**What each part of the lead's correction gets:**
- **The W/P-less candidate** is now the control. Its run below stands as recorded.
- **"Relative to the clock's rest frame" is undefined.** Agreed; it was F2 below. Frame-free dissipation is viscosity of
  the clock congruence, graded as D-V.
- **The EP point** is T1. An A-key cannot act on infalling dust (in (A) kept whole it sees only the law's self-field of
  the excess charge), and it reads the baryons' field only on a held clock. The bootstrap therefore presupposes the hold.
  CFG461's edge needs a total field of 0.185 a0, which only a held clock reads.
- **Is Gamma <= a0/c fatal by itself? Yes** (T3). Even F = 1 from the start allows a contraction of 1.31 / 1.39 by today.
- **T-DEP with entropy:** evaded in form (T5h). The escape is then bounded by T7.
- **Hypotheses used:**
  - locality: coefficients are functions of the clock's own scalars (theta, sigma^2, A.A, Q, N) and of G, c, a0, mu_K;
  - the equivalence principle (gravity enters only through the metric);
  - (A)'s Legendre map is unchanged;
  - the clock's charge is conserved;
  - CFG461's energy model (T3);
  - the record's forest line, converted to a viscous damping length with (4/3) nu k^2 = H. This conversion is an
    estimate, so T7 is an estimate.
- **The two ways out, named, not graded:**
  - a keyed viscosity, which is off on the z = 3 forest and on in z = 0 haloes. T7's threshold list shows that none
    of G, c, a0 and mu_K supplies the threshold: the densities a0^2/(G c^2) = 21.6 and mu^2 c^2/K >= 6.5e13 Msun/kpc^3
    bracket the forest (2.5e3) and the haloes (7e4-1.7e6) only from outside. So a new constant is needed;
  - non-local dissipation, which is FA3's class.
- **PAR1 C8's door.** Dissipation is the continuation of T-SHK's energy defect. Part T shows that continuing it does not
  reach a counted-once halo by today without a new constant.

Part T files: `FROZEN_CRITERIA_T.md`, `aks1_t.py` -> `aks1_t.out` / `aks1_t.json` (seconds, sympy and numbers). No Part N
collapse is owed under the frozen rule.

**Note, 2026-11-11 (pointer only; relabels nothing): T7 has been computed and does not hold.** VSH1
(`closure_2026_11_10/VSH1_viscous_shock_settling/`, origin result 4358613eaf; NO VERDICT as frozen, SETTLES BY SHOCK
under its post hoc A1) ran FLD1's shells with gamma 5/3 pressure (heat kept), shear viscosity nu = nu_F and shock
capture. At log M_b 9 / 10.5 / 11.5 on both footings the clock is at rest inside r_e*, because a folding flow settles
behind a shock rather than by diffusion. So nu_S = r_e*^2/t0 is not a bound, and D-V(h) does not close on T7. VSH1
reports (not graded) that the settled charge is 1.4 M_b at every mass, 1.1-3.5 % of the law's halo there: short by 28-95
times in FLD1's infall model. Whether D-V(h) is closed on that amount is the lead's call. Limits are in VSH1.

---

## The landed run (now the control): action (A) without W and P, plus an A-keyed drag

**RELAXES, NOT SETTLED / RELAXES, NOT SETTLED (canonical / alt): the sink is healthy but does nothing. A falling clock has no
acceleration, so the sink is off where infall happens. Even keyed as if the clock already stood, its rate is c/v too
slow. So the joint (TOE0's T1) stays OPEN, W cannot leave the fundamental action this way, and the cause of T2 and T3
is untouched.**

Deciding number: the sink's integrated e-folds by today at CFG461's target edge are **1.6e-6** (canonical, log M_b 10.5;
1.3e-6 to 3.4e-6 over the three masses; alt 1.5e-6, 1.3e-6 to 3.8e-6). Settling needs at least 1. Keyed on the full local field as if the
clock already stood (bracket B1), the same number is 0.017.

TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Footings never pooled. The cold component is
cold dark energy (the clock's dust), never a particle. Not a LCDM lane. Criteria 5b35674191 (alone, before any script);
amendment A1 9ad1d5a121 (post hoc, alone, before any A1 row). Local and origin ids at the end.

## The candidate as frozen, and three facts that decide it before any run

The candidate is action (A) without W, P and the multiplier: GR + clock + dust term mu_K^2 (Q-1)^2/(4K) + baryons. On top
of it sits Galley's in-in drag on the clock's velocity at Gamma(A) = (a0/c) f(|A| c^2/a0), with f(x) = x, f(0) = 0 and no
number. The budget is open: the energy leaves the clock.

- **F1. Without W and P, the clock's acceleration is only its dust pressure,** A = -(K/mu_K^2) grad rho. A free-falling
  clock has A = 0. At the record's CMB-lensing line mu_J = 2.512e4 per Mpc, pi/mu_K = 0.125 kpc, so the dust is
  pressureless on galaxy scales and the key is off everywhere a halo forms.
- **F2. The literal reading is empty.** The clock dust moves along the clock's own normal, so its velocity relative to the
  clock's rest frame is identically zero. The frozen reading damps the velocity relative to the static frame: the Kodama
  frame in spherical symmetry, the frame of the settled state. No local covariant version of that frame exists in (A)'s
  fields outside spherical symmetry (reported, H-R1).
- **F3. Theorem 8 again.** With f(x) = x the rate is Gamma = |A|/c. a0 cancels; c stays. On a standing orbit the sink's
  e-folds per period are 2 pi C v/c, which is 4e-3 at C = 1 (Lean `aks1_period_bound`). That is STANDING's c/v mismatch,
  now in a rate. No shape f repairs it: the missing factor is a speed.

The record had no A-keyed dissipative sink. The nearest are CFG245 (relaxation at Gamma = a0/c: Gate T FAIL, Gamma t0 =
0.136 / 0.164), CFG382 (density-keyed), CFG369/370 (cooling-keyed) and CFG373/381 (khronon K^2: DOES NOT PRODUCE). Step R
is quoted in full in FROZEN_CRITERIA.md section 0.

## Gates (P rows; canonical / alt)

| gate | canonical | alt | numbers, log M_b 9 / 10.5 / 11.5 (canonical; alt) |
|---|---|---|---|
| **H** health | **PASS** | **PASS** | H1: the doubled action gives the damped equations exactly (two shells, generic Gamma(A): residuals 0; energy identity 0; kinetic entry m, unchanged). H2: FRW background drag 0; linear coefficient 0 for f = x, x^2, x/(1+x) (comoving reading). H3: Im omega <= 0 for every damped stable mode; Jeans modes keep their sign (growth 0.618 at w0^2 = -1, Gamma = 1). H4: the baryon equation has no Gamma (residual 0) |
| **R** relaxation | **FAIL** | **FAIL** | R1 slope -2.25 / -2.48 / -2.31 (alt -2.11 / -2.27 / -1.75) against -2 or the law's -2.00 / -2.00 / -1.99 (alt 11.5: -1.04, a 3.5 kpc window). R2 amplitude -3.16 / -2.70 / -2.35 dex (alt -3.19 / -2.68 / -3.00); line +-0.1. R3 d log sigma^4/d log M_b 1.32 (alt 1.10, carried by the 3.5 kpc window); line 1 +- 0.1; CFG461's C4 gives 4/3. **R4 d log sigma^4/d log c 0.19 / 0.35 / unresolved (alt 0.09 / -0.06 / 2.20)**; line 1 +- 0.1 |
| **E** edge | **FAIL** | **FAIL** | r_edge 63 / 224 / 447 kpc (alt 56 / 178 / 3.5) against r_e* 7.2 / 40.5 / 128 (alt 6.5 / 36.8 / 116); **g_N(r_edge)/g_e* 0.013 / 0.033 / 0.082** (alt 0.014 / 0.043 / 960, the last because the alt 11.5 scan stopped at 3.5 kpc); line 0.5-2 |
| **S** sink | **FAIL** | **FAIL** | E_diss(M_c shells)/E_req 1.3e-6 / 3.8e-5 / 6.1e-4 (alt 1.1e-6 / 3.1e-5 / 4.3e-4); line 0.5-2. Open budget, canonical: E_diss 4.1e6 / 1.4e10 / 3.8e12 Msun (km/s)^2; net radial momentum removed 1.4e2 / 4.2e4 / 3.6e6 Msun km/s (alt 1.3e1 / -3.3e4 / 2.0e6; signed, so in- and outgoing streams cancel); against E_req 3.1e12 / 3.8e14 / 6.2e15 (alt 3.6e12 / 4.6e14 / 8.7e15). Heat reading: no energy leaves the clock, so S1 = 0: FAIL |
| **C** constants | **PASS** | **PASS** | C1: f(x) = x, no number. C2: charge at t0 against the start, 2e-16 (the 5.41 unchanged) |
| **T** time | **FAIL** | **FAIL** | **T1: median N_Gamma at r_e* 1.3e-6 / 1.6e-6 / 3.4e-6 (alt 1.3e-6 / 1.5e-6 / 3.8e-6)**; line >= 1. T2: FRW untouched, P against MU1 1.6e-8 (line 1e-6): PASS. T3 (reported): the settled region reaches the cap at no mass |
| **label** | **RELAXES, NOT SETTLED** | **RELAXES, NOT SETTLED** | H passes; R and E fail |

**Which failures stand on sound known answers.** KA8 (resolution) and KA5b (the strong-drag energy book) fail; see
below. By the frozen map, R1, R2, R3, E and S1 rest on one of them (alt: R1, R2, E, S1; alt R3 reads 1.10 and passes only
because its 11.5 window is a 3.5 kpc core window). **R4 and T1 fail with every known answer they rest on
passing**, so the label is not NO VERDICT; R fails on R4, and the label follows. The E miss is 1.1-1.9 dex in g_N below g_e* (a
factor 12-77). That is 4-6 times the 0.3 dex in g_N implied by KA8's 0.15 dex in r_edge, at both resolutions. It is
reported as robust, though it is not counted as sound.

**P is the sink-off twin.** P against MU1, row by row: d log r_edge 0.05 / 0.00 / 0.05, d amplitude -0.05 / +0.01 / -0.05
dex (canonical). Those are the KA8-size scatter of a chaotic multi-stream run. P's largest single-shell e-fold count is
1.9e-4 / 8.6e-4 / 2.1e-3, and its largest |A|/a0 at any shell and time is 0.04 / 1.05 / 10.4.

## Brackets (reported, not label-setting; canonical unless stated)

| key | what it shows | numbers (log M_b 9 / 10.5 / 11.5) |
|---|---|---|
| B1: f = x on the full peculiar field, as if the clock already stood (both footings) | the upper bound for an f = x sink | N_Gamma at r_e* 0.0077 / 0.017 / 0.0009 (alt 0.0082 / 0.019 / 0.0009); E_diss/E_req 0.0023 / 0.24 / 221 (alt 0.0020 / 0.20 / 158); r_edge 50 / 112 / 0 kpc (alt 56 / 141 / 0); R2 amplitude -3.06 / -2.37 dex. At 11.5 the full field is far above a0 in the baryon core, so even f = x drains the core |
| B2, C = 10 | what a coefficient buys | r_edge 45 / 0 kpc; amplitude -2.97 dex at 9; N_Gamma at r_e* 0.066 / 0.005; E_diss/E_req 0.028 / 35 |
| B2, C = 100 | | drained at 9 and 10.5 (r_edge 0); E_diss/E_req 3.8 / 41 |
| B2, C = 1000 | | drained at 9 and 10.5; N_Gamma at r_e* 0.19 / 0.48; E_diss/E_req 5.0 / 40 |
| B3: P with mu_K = 198.25 (KD1's w line, below the CMB-lensing line) | more pressure, so more A | at 9: N_Gamma at r_e* 0.0059, r_edge 71 kpc, amplitude -4.26 dex, E_diss/E_req 0.017; at 10.5 not run (see below) |
| B4: f = x^2 (the analytic A.A form) | | at 9: N_Gamma 0.0018, r_edge 56, amplitude -3.11; at 10.5 drained (E_diss/E_req 37) |

Rows not run: B2, B3 and B4 at log M_b 11.5 (1-3 h each under the shared load), and B3 at 10.5 (stopped after more than
an hour on the row: mu_K = 198 forces a Courant step about 13 times smaller than P's). Their `runs/*.json` mark them `not_run`.
No label or MUTATE reading depends on them.

What the brackets say: with no support (criteria F5), strong drag does not settle the dust; it drains it. Wherever the
drag reaches about one e-fold, the dust falls at the terminal speed g/Gamma = c/C (Lean `aks1_terminal_speed`) into the
softened baryon core. The energy removed then overshoots CFG461's requirement 4-221 times, and no settled region remains
(r_edge = 0). Weak drag leaves the sink-off halo. No coefficient and no shape tried gives an SIS at the BTFR amplitude
with an edge at 0.029 a0. Between the two regimes there is no window: at C = 10 the edge region gets 0.066 e-folds at log
M_b 9 while the 10.5 core already drains.

## Known answers

| | what | result |
|---|---|---|
| KA1 | SIS identities M = 2 sigma^2 r/G, v_c^2 = 2 sigma^2, E = -G M^2/(4R), lambda_J^2 = 2 pi^2 r^2 (sympy) | PASS, exact |
| KA2 | Galley's damped oscillator from the doubled action (sympy) | PASS, residual 0 |
| KA3 | Bertschinger's radial self-similar infall, rho ~ r^(-9/4) (EdS, seed 1e11, 3000 shells, z_i 300) | **PASS: slope -2.224** over [0.01, 0.1] r_ta (r_ta 1786 kpc); pre-A1 -2.274 |
| KA4 | COL1's focusing times with this lane's integrator | PASS, all eight within 5.1e-4 |
| KA5a | energy, sink off, cold collapse of 5 M_b through crossings and centre passages | **PASS: 6.4e-4** (line 1e-3; pre-A1 2.2e-3 FAIL) |
| KA5b | energy book with Gamma = 1000 \|g\|/c | **FAIL: 5.3e-2 of \|E0\|** (line 1e-3). The test dissipates 206 \|E0\|; relative to that throughput the book closes to 2.6e-4 |
| KA6 | the law's own phantom over [0.1, 1] r_e* (reported) | slope -1.90 to -1.94, amplitude -0.03 to -0.06 dex |
| KA7 | homogeneous row against FRW | **FAIL: 2.43e-3** (line 1e-3). `aks1_ka7_probe.out`: it is the n = 1 pressure at the grid's inner edge (an empty hole inside the first shell pushes the innermost 59 shells inward); with the pressure off, 6.9e-7. T2 itself (P against MU1) is 1.6e-8 |
| KA8 | resolution, N 1000 against 2000 (P, canonical, 10.5) | **FAIL**: r_edge 158 / 224 kpc (0.15 dex, line 0.05), amplitude -2.63 / -2.70 (0.07, line 0.03) |
| KA9 | r_e* against CFG461's r_edge | PASS, within 0.7-1.3 % (CFG461's share 5.364, KD1's 5.409) |

## MUTATE

- **MU1 (sink off) bites** against B2 at C = 1000. At log M_b 9 and 10.5, MU1 settles to 56 / 224 kpc while C = 1000
  drains to r_edge 0, so the machinery sees a sink. MU1 folds as COL1 does: its first central passage and first crossing come at 0.174 /
  0.117 / 0.105 Gyr after z 10 (both footings). Its innermost shell starts at 0.5-3.4 kpc (FLD1's grid), mostly outside
  the 1 kpc core, so these times are later than COL1's core focusing. KA4 reproduces that focusing with a test shell
  inside the core.
- **MU2 (c-free Gamma(rho), CFG382's lambda 0.028) bites**, both footings. The density-keyed rate overcools the dense
  centre and drains the halo: r_edge 5.6 / 0 / 0 kpc (alt 5.6 / 5.0 / 0), so there is no M_b^(1/2) edge. At log M_b 9 its
  5.6 kpc edge happens to sit inside E's factor-2 window (g_N/g_e* 1.56 / 1.29). That is a one-mass coincidence of the
  kind CFG461's scaling part exists to catch, and the other masses have no edge.
- **Lean twin**: `AKS1.lean` (4 theorems) exit 0; `AKS1_MUTATE.lean` fails on all 3 false statements.

## What this does to TOE0 (reported only; TOE0's labels are frozen)

- **T1 (the joint) stays OPEN.** The A-keyed sink adds no inertia, so AKD1's mean value theorem does not touch it (H
  passes). But it removes nothing where removal is needed, and it puts no edge at an acceleration.
- **T2's Minkowski row, if W were removed** (`aks1_sym.out`). The dust term alone gives the clock mu^2 pi_t^2/(4K) on
  Minkowski and no (grad pi)^2 term: omega^2 = 0 at every k. That is the same strong coupling QG1 found. Ordinary
  khronometric alpha, beta, lambda > 0 would give omega^2 = 2 K M_P^2 k^4 (beta + lambda)/(2 K M_P^2 alpha k^2 + mu^2) > 0:
  weakly coupled, but at the cost of new couplings. Removing W lifts the forced alpha = 2. It does not by itself make the
  vacuum healthy.
- **T3(i).** With W removed the conservative action is polynomial, and the |A|^3 non-analyticity is gone. The sink with
  f = x carries |A| (non-analytic); f = x^2 is analytic. Either way the sink is an in-in term: it needs a bath with its own
  microscopic theory, which is a new open item, not a UV completion.
- **Is the slow rate fatal by itself? Yes.** Even keyed as if the clock already stood (B1), the sink reaches 0.017 e-folds
  at the target edge by today. The bound is Gamma t0 <= 0.136 f(x) (0.164 alt), and the per-period bound is 2 pi C v/c.
  Before the rate matters, the key is off on a falling clock (F1), and nothing holds a settled halo (strong drag drains
  it).

## Hand estimate against the outcome

| criteria section 8 (before any script) | outcome |
|---|---|
| Gamma t0 at the edge <= about 0.03 even if standing | B1 0.0077 / 0.017 |
| P's N_Gamma at r_e* about 1e-5 or less; P = MU1 to 1e-3 dex | 1.3e-6 to 3.4e-6. P = MU1 only to the KA8 scatter (0.05 dex), not 1e-3: the multi-stream run is chaotic |
| r_edge about R_fold ~ 0.5 R_ta, growing as M^(1/3); g_N(r_edge) 0.002-0.005 a0 (a factor 6-15 low) | r_edge 63 / 224 / 447 kpc; g_N/g_e* 0.013-0.082 (a factor 12-77 low): worse than estimated |
| slope near -9/4; amplitude low by 0.2-1 dex; mass scaling 4/3 | slope -2.25 to -2.48; **amplitude low by 2.3-3.2 dex** (the hand estimate missed the supply problem: an isolated seed accretes far less than the cosmic share by today, which is COL1's 1-4 % again); mass scaling 1.32 |
| B2 drains into the core at C >~ 100 | yes: r_edge 0 at C = 100 and 1000 (log M_b 9 and 10.5); at 10.5 even C = 10 drains |
| label RELAXES, NOT SETTLED, both footings | yes, both footings |

## Disclosures

- **A1, post hoc** (AMENDMENT_A1.md, committed alone before any A1 row):
  - an energy-consistent centre reflection, because KA5 failed under the frozen mirror (2.2e-3 sink off; 6.1e2 with
    strong drag, where a damped shell resting on the mirror was lifted for free);
  - 51 snapshots and the edge scan started at 3 kpc, because the frozen scan stopped in the radial-orbit centre noise
    (r_edge 0-1.3 kpc in the pre-A1 rows);
  - KA5 graded part by part ((a) the dynamics, (b) S1).
  No line changed.
- **Pre-A1 rows** (21 finished under the frozen method, plus 5 that orphaned pool workers wrote after the move) are kept
  outside the repo and graded nothing. Their P / MU1 readings agree with A1's in kind: N_Gamma at r_e* 1.2e-6 / 1.5e-6, B1
  0.008 / 0.017.
- **The settled-region reading is noisy.** In multi-stream radial-orbit runs it varies by about 0.15 dex between
  resolutions (KA8) and between twin runs. Even with A1's 3 kpc start, the scan stopped in the core in two of the six log
  M_b 11.5 P/Pc rows: Pc canonical read r_edge = 0 and P alt 3.5 kpc, because the baryon point mass dominates there out to
  about 10 kpc. Those two rows drive the alt 11.5 readings (g_N/g_e* 960, R3 1.10, R4 2.20). No label depends on them: R4
  and T1 fail at every mass on both footings.
- **Orphaned pre-A1 workers.** On macOS the driver's pool spawns its workers, so stopping the pre-A1 driver by name missed
  them, and they wrote five more pre-A1 rows into `runs/` after the move. Each was identified by the missing A1 tag,
  moved out, and re-run under A1.
- **Model limits.** The model is spherical, uses radial orbits only, starts from a uniform clock plus a ramped point mass
  at z 10 (COL1/FLD1's setup), and has no primordial perturbation in the clock. That is why the supply is short. It uses a
  single-fluid n = 1 pressure closure in multi-stream regions, a 0.3 kpc centre floor, and a 1 kpc Plummer core.
  Non-spherical collapse, mergers and angular momentum are not represented.
- **The open budget.** The energy and radial momentum removed are stated, not followed. An open sink coupled to GR needs
  the bath's stress to gravitate (H-R2). The Kodama-frame reading has a linear drag around FRW with an origin-dependent
  coefficient, -(|delta A|/c) H R for f = x (H2, reported).

## Files and re-run

- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`.
- `aks1.py` is the main script: symbolic part, rows, known answers, grade (about 1.5-2 h on 5 workers under load; rows
  resume). `python3 aks1.py --grade-only` re-grades in seconds.
- `aks1_lib.py` (model), `aks1_sym.py` -> `aks1_sym.out/.json`, `aks1_run.py` -> `runs/*.json`, `aks1_ka.py` ->
  `aks1_ka.out/.json`, `aks1_ka7_probe.py` -> `aks1_ka7_probe.out`, `aks1_grade.py` -> `aks1_grade.out/.json`.
- `AKS1.lean`, `AKS1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`.
- Snapshots stay outside the repo (`AKS1_SNAP`).

Commits (local / origin):
- criteria 5b35674191 / b4deefbc0c (alone, before any script);
- amendment A1 9ad1d5a121 / 26b9de54a0 (alone, before any A1 row);
- result b3f18eca2d / 06c837db4f;
- id record 1f8ccebb7e / 3c10ec65cc;
- Part T criteria d44203c715 / b0d0cbefa1 (alone, before aks1_t.py);
- Part T result c53108334a / b1425a9820;
- this Part T id record: one more commit, pushed the same way.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

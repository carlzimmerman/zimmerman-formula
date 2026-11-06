# Closure, 2026-11-05: the action, and a verdict on every door

Written at the owner's request ("I need closure, and an action"). It consolidates
the record; it changes no verdict and adopts nothing new. Each row points at the
lane that owns the result. Kappa = 1/2 FITTED; not theory closed.

Closure here means the owner's 11-04 rule: every door has a label. It does not
mean every door is a pass.

## 1. The action (adopted 11-04, scoped)

v3s, from `covariant_push_2026_10_22/V3_FULL_PICTURE.md` section 1 and
`finish_2026_11_04/FN1_action_call/OWNER_DECISION_2026-11-04_ADOPT_V3S_SCOPED.md`:

    S = (c^3/16 pi G) Int sqrt(-g) [ R - 2 J(Y) + 2 K(Q) ]
        - (gamma_L/2) Int sqrt(-g) [max(D.P, 0)]^2  +  S_m[g, matter]

    J(Y) = Lambda - 2 a_geo^2 [u - ln(1+u)],  u = sqrt(Y)/a_geo,  a_geo = a0/c^2
    K(Q) = mu_K^2 (Q - 1)^2
    gamma_L = K Lstar^2 / 2,  Lstar >= 21.7 / 22.9 pc (canonical / alt)
    a0 = kappa c sqrt(G rho_DE),  kappa = 1/2

tau is the khronon (preferred foliation), A its acceleration, Y = A.A/c^4, P an
independent spatial covector. Scope: isolated galaxies, the Solar System, galaxy
lensing, gravitational waves.

What is put in by hand (none of it derived):

| Input | Status | Where |
|---|---|---|
| kappa = 1/2 | FITTED; proved not derivable from the framework's premises | Lean `KAPPA_LOGIC_2026_10_20.half_not_derivable` |
| J(Y) | POSTULATED, outside Blanchet-Skordis's admissible class | V3_FULL_PICTURE section 1 |
| Lstar | POSTULATED, lower bound only (outer globulars) | D10 |
| mu_K, dust abundance | free / initial condition | V3_FULL_PICTURE section 1 |
| The vacuum-response identity | MISSING: C3^2 rho_vac = 128 pi F^3 is what a vacuum principle must supply | `action_scale_investigation_2026_11_05/joint_phase/SELECTION_IMPASSE.md` |

## 2. Every door

| Door | Label | Owner lane / commit |
|---|---|---|
| The action, stated standalone | DEPOSITED | PAPER68 v1.0, DOI 10.5281/zenodo.23990944 |
| a0 law on galaxies (SPARC, RAR) | PASS, flagship | PAPER67 v1.2, DOI 10.5281/zenodo.23968171 |
| Solar System (Cassini, planets) | PASS, margin >= 4.8e7 | C6P 8c5703da06 |
| PPN gamma, beta | PASS, = 1 to 1e-12 | V3W W1 17d7b7ecdc |
| Galaxy lensing = dynamics | PASS (weak power on KiDS alone) | V3W W3 17d7b7ecdc |
| GW speed | PASS, c_T = c to 6e-32 | V3W W4a |
| AGC 114905, Malin 1 | FAIL (inclination does not rescue). QX4: Malin 1 class no-go: no mechanism in the v3s/AC2q action rescues it (exact AQUAL solve narrows chi2 69->55 / 132->43, EFE, stiffness, distance, mass all NOT RESCUED). AGC 114905 rescued only by an external field 0.08-0.29 a0 (CONDITIONAL: host >= 3.4e9-6.4e9 Msun baryons at >= 30-37 kpc, M ~ d^2; environment data not on disk); exact field, action terms, distance, mass NOT RESCUED. Side finding: action's exact field departs from the algebraic law by up to 0.097 dex at R_d in LSB discs, so the SPARC pass owes an exact-field regrade | UD1, UD2, UD3, QX4 |
| Clusters | FAIL (closed for v3s / AC2q): every static term graded on X-COP (law +0.47/+0.43 dex; clock <= 3 % of baryons; stiffness <= 5e-5; K(Q) dust needs mu_K 17x the galaxy bound, rms still 0.28); no J(Y) can serve it, since X-COP needs 0.30-0.51 dex more than SPARC at the same g_N/a0; Lean QX2_cluster_nogo. Passing needs a new action (non-minimal coupling or a new source variable). QX5 tried five new-term keys: matter pressure, khronon bulk velocity, enclosed density/rho_DE and collisional acceleration (CC as an AC2q term) are DEAD; a phantom multiplier on the clock-rate depth Q-1 passes X-COP + groups only with a cluster-set step (FAIL by the no-tuning rule) and Coma's UDGs then need 5-6x more (2.2-2.8 sigma); Lean QX5_monotone_sandwich | QX2, QX5; FAILURES section F; BF1-BF3, BK2, SR3, FA1 |
| CMB lensing shape | FAIL under every rule tried | WG1-WG6 |
| Linear growth, radiation era | OPEN, outside scope | FN1 decision |
| Cold dark energy sector (route E) | RETIRED 11-01 | owner decision 11-01 |
| v3s weak spots (well-posedness, PN sign, moving Sun, causality) | NO VERDICT / UNDECIDED, none broken. Well-posedness (AC16): FAIL (classical, generic data): no C1 solution across a transverse D.P = 0 interface (force jumps by -gamma grad Pi; v3s and AC2q alike); well-posed on each branch. Smoothed switch (AC20): v3s with -(gamma/2)(D.P)_+^4/((D.P)_+ + 2 rho_DE)^2 (no new constant; statics within 4e-5) is REPAIR (1D C1 across the switch, then gas shocks); AC2q NOT A REPAIR as frozen (contact form shifts FRW stiffness to 11 gamma/16; exact-FRW spline misses one resolution row); 3D not shown (no convex contact-6 spline). Causality (AC18): light-cone causality FAIL (v3s and AC2q, both footings): on a charged anisotropic (MOND) background, with GR's metric part retarded by hand, the leaf-elliptic Xi changes a gauge-invariant Ric(u_T,u_T) outside the source's cone (about 1e-67 m/s flow for 1000 kg at 1 m/s, 3 light-s away; unconstrained); tau-ordering PASS (one global time, no closed loops); isotropic or zero-charge cases are causal | AZ31-AZ39; AC16; AC18 |
| kappa / a0 from an action | BLOCKED: exact missing identity named; no reopen condition met | AZ40, CFG894, SELECTION_IMPASSE |
| Covariant source for the FN6 window | FAIL for the actions on the table: v3s and AC2q's own static lengths have mass exponents 0, 1/2, -1/2, 1 and (AC2q charge offset, new) 1/4, none in [0.30, 0.45]; a window length must be a Newtonian-regime balance, and those are mass-independent (frozen MUTATE did not bite; post-result control bites). New constitutive families: AZ41 NO VERDICT, none regular | AZ41, AC19 |
| FN6 window itself | PENDING: 33/143 points fail convergence; MW flips unresolved | AZ43 (running) |
| AC2 single-clock successor action | see section 3 | AC2, AC3, AC4 |
| a0(z) | NOT DECIDABLE on disk; ALMA U4_28473 scored tonight; proposal-class sample needed | AT2, FN2 |
| Wide binaries | OPEN; Gaia DR4 pre-registration frozen | prep_2026/gaia_dr4_prep |
| Unification, SM bridge, fine-structure constant | STOPPED / WALLED / NOT DERIVED | owner 11-01; FSP-010 |

## 3. The one live constructive route: AC2, repaired as AC2q

AC2 (`action_search_2026_11_05/AC2_single_clock/ACTION.md`) lets the dark-energy
scalar itself be the clock. It removes the independent-clock caustic branch
that AC1 proved. As written (smooth stiffness) it is ill-posed in galaxies (AC6).
AC2q switches the stiffness on the khronon charge D.P + 2X (AC7):
-(gamma/2){[max(D.P + 2X, 0)]^2 - (2X)^2}.

| Test | Result |
|---|---|
| Scalar-only FRW quadratic action | healthy (AC2) |
| Coupled matter, UV principal speeds | positive, subluminal (AC3) |
| Frozen finite-wavelength roots | 8/81 negative, slow (|omega| < H), not a controlled test (AC3) |
| Those 8 modes evolved, constant V | NO VERDICT (AC4): no growth beyond GR, but the flipped-stiffness control does not bite (clock stops rolling) |
| Same, rolling clock (exponential V) | NO VERDICT, no power (AC5): flipped control reaches R 8.6 < 1e3; even a wrong-sign stiffness gives only Hubble-rate growth there. Main run 81/81 converged, max R 2.68 (under the PASS line, but not gradable without power) |
| AC2q's 8 slow roots to z = 1100 (and N = 20) | NO VERDICT, no power, as frozen (AC13): main R stays 1.0-2.53, flat from N = 5 to 20, no growth; planted 2H tachyon detected (R 3e3-1.9e4) on the 6 dark-energy-like witnesses but not on the 2 decelerating eps_phi = 2 fixtures; flipped stiffness is caught by det K changing sign (ghost), not by R. POST reading: HARMLESS on 6/8 |
| AC2q slow roots, fresh dark-energy-like witnesses (powered per witness) | PASS (HARMLESS, scoped) (AC23): 16/16 fresh witnesses powered (planted 2H tachyon R 2.6e3-1.9e4), AC2q R 1.00-2.70 at z = 1100 (unchanged to N = 20), det K > 0 (>= 0.050) while the flipped stiffness turns det K negative on all 16; KA1 = AC13 exactly, KA2 = AC3 roots to 5e-30, MUTATE FAILs; eps_phi = 2 (decelerating) out of scope, stays NO VERDICT (AC13) |
| AC2 inside galaxies | ILL-POSED (AC6): charge = div P + phidot^2; phidot^2 <= 2 rho_DE cannot fill the phantom's negative regions (6/7 H4 systems, both footings) |
| AC2q, FRW | healthy: lapse term x (1 - 2 gamma phidot^2)^2, 72/72 fixtures (AC7 Q1). ERRATUM 11-06: the factor is (1 - gamma phidot^2)^2 for AC2q as defined; signs hold for any f >= 0 (Lean), so healthy stands (see closure_2026_11_06/EQUATIONS_IN_ORDER.md, erratum) |
| AC2q, galaxies | no Gamma ~ k anywhere; off-region bounded (AC7 Q2) |
| AC2q, static limit | = v3s at mu_K = 0 up to phidot^2-proportional terms (<= 2.2e-10 relative, Poisson + rho_DE): v3s's static passes carry (AC8) |
| Switch on D.P alone (v3s placement) with a dark-energy clock | non-analytic on FRW (AC7 control M-b) |
| AC2q, tensor speed (own terms) | PASS: c_T = c in the principal part; new tensor mass gives dv/c <= 1.9e-46 at 100 Hz (AC9 T1) |
| AC2q, lensing slip (own terms) | PASS: Psi source and anisotropic stress are O(gamma s^2 grad Phi P), beyond O(GM); slip <= 3e-17 (AC9 T2) |
| AC2q, moving Sun (AZ37 analogue) | NO VERDICT (AC11): no exact P=0 GR branch (clock's Klein-Gordon needs uniform theta on leaves; met only to gamma s^2 ~ 1e-17); forced oscillator = AZ37's to 2.5e-6, resonance survives; X > 0 (|dX/X| <= 1.3e-8); Sun's own charge >> Galactic rho0 inside ~1e3 AU |
| AC2q and v3s, the Sun's own halo carried along (kinematic) | NO VERDICT sharpened (AC12): continuity div(q w) = 0 partly drags the halo (relative flow f = 0.064-0.076 V at 1 AU, 0.16-0.19 V at 9.58 AU, 0.89 V at r_eq); local phase speed = sqrt(v_K^2 + c_gal^2), so 1 AU is SUBSONIC (Mach 0.47-0.94) but 9.58 AU and r_eq are supersonic (Mach 3.7-7.4, 150-310); the flow's Bernoulli term is not small (B 0.09-0.38 at 1 AU, 6-23 at 9.58 AU), so the kinematic halo is not self-consistent: nonlinear solve needed. Capped bounds at the planets: <= 1e-13 g_N (1 AU), 2e-10 (9.58 AU). v3s = AC2q to all digits shown |
| AC2q, nonlinear planar evolution | NO VERDICT (AC10): first fold = v3s's to 0.3 % on a 12-row subset, both footings; s^2 and the charge switch do not regularize; clock-only fold threshold Omega tau_f = 1 (new, analytic); X > 0 holds to the fold; frozen K2/K3 missed (crossing-speed assumption); the post-fold interior reading is a stiffness shock, same in v3s |

Inherited, by inference (not a new run): X14's "caustics generic" for soft
khronon elements. X14's mechanism is that nothing in the action grows with k at
the fold scale; AC7 Q2c shows the dark-energy clock adds no k-growing term in the
off-region (omega^2 -> K rho_q (M_theta - 1)), so AC2q's soft side folds as v3s's
does, and only a new constant (X14's beta class) could remove it.

AC2q is a candidate, not adopted: one field is dark energy and the clock, no
dust, healthy on FRW and in galaxies at this order, static limit = v3s.
Still owed: a frozen nonlinear label and post-fold shock evolution (AC10 NO VERDICT; its first-fold
numbers support the caustic inference), X > 0 preservation away from statics (holds to the first fold, AC10; exact in
statics; linear moving response keeps X > 0, AC11), the nonlinear moving Sun
(co-moving charged halo matched to the Galactic flow at ~1e3 AU; AC11 linear NO VERDICT, as v3s's AZ37;
AC12: kinematic halo subsonic at 1 AU but not self-consistent, a nonlinear Bernoulli-coupled solve inside ~10 AU is the open item).
Lensing and tensor regrades on its own terms: done, PASS (AC9). It fixes no coefficient: xi and kappa stay by hand. Having no dust,
it says nothing new for clusters, growth or the CMB.

## 4. What is left, and what would move it

Nothing left is a calculation the record can still do with what it has.
Each open door waits on one of three things:

1. **New data:** ALMA tonight (FN2 runbook), GS4 on 11-28, Gaia DR4 around 12-02,
   a proposal-class a0(z) sample.
2. **A new principle** that supplies C3^2 rho_vac = 128 pi F^3 without choosing a
   constant. That is the only road to deriving kappa.
3. **Finishing running work:** AZ43 (FN6 window), AZ47 (BK2 G3), SY1 stage 3.

Kappa = 1/2 FITTED; not theory closed.

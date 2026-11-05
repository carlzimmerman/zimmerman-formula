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
| AGC 114905, Malin 1 | FAIL (inclination does not rescue) | UD1, UD2 |
| Clusters | FAIL / OPEN: no formula, carrier, selector or action found | FAILURES section F; BF1-BF3, BK2, SR3, FA1 |
| CMB lensing shape | FAIL under every rule tried | WG1-WG6 |
| Linear growth, radiation era | OPEN, outside scope | FN1 decision |
| Cold dark energy sector (route E) | RETIRED 11-01 | owner decision 11-01 |
| v3s weak spots (well-posedness, PN sign, moving Sun, causality) | NO VERDICT / UNDECIDED, none broken | AZ31-AZ39 |
| kappa / a0 from an action | BLOCKED: exact missing identity named; no reopen condition met | AZ40, CFG894, SELECTION_IMPASSE |
| Covariant source for the FN6 window | NO VERDICT: no mechanism | AZ41 |
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
| Same, rolling clock (exponential V) | NO VERDICT, no power (AC5): flipped control reaches R 8.6 < 1e3; even a wrong-sign stiffness gives only Hubble-rate growth there. Main 81 cases still running |
| AC2 inside galaxies | ILL-POSED (AC6): charge = div P + phidot^2; phidot^2 <= 2 rho_DE cannot fill the phantom's negative regions (6/7 H4 systems, both footings) |
| AC2q, FRW | healthy: lapse term x (1 - 2 gamma phidot^2)^2, 72/72 fixtures (AC7 Q1) |
| AC2q, galaxies | no Gamma ~ k anywhere; off-region bounded (AC7 Q2) |
| AC2q, static limit | = v3s at mu_K = 0 up to phidot^2-proportional terms (<= 2.2e-10 relative, Poisson + rho_DE): v3s's static passes carry (AC8) |
| Switch on D.P alone (v3s placement) with a dark-energy clock | non-analytic on FRW (AC7 control M-b) |

Inherited, by inference (not a new run): X14's "caustics generic" for soft
khronon elements. X14's mechanism is that nothing in the action grows with k at
the fold scale; AC7 Q2c shows the dark-energy clock adds no k-growing term in the
off-region (omega^2 -> K rho_q (M_theta - 1)), so AC2q's soft side folds as v3s's
does, and only a new constant (X14's beta class) could remove it.

AC2q is a candidate, not adopted: one field is dark energy and the clock, no
dust, healthy on FRW and in galaxies at this order, static limit = v3s.
Still owed: nonlinear evolution, X > 0 preservation, a moving Sun in the clock
frame (the same open item as v3s's AZ37), lensing and tensor regrades on its own
equations. It fixes no coefficient: xi and kappa stay by hand. Having no dust,
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

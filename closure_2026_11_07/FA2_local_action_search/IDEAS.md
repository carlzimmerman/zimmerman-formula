# FA2: fresh-eyes search for a new LOCAL action. Ideas, written before any FA2 script or number

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle. Both footings, never pooled. Owner's ask: "new
answers to a new action and full theory" (it lifts the 11-07 STOP list for this lane only). Scope: local covariant
terms or couplings at a point. Nonlocal, history and global actions belong to FA3 and are not touched here. WL1 owns
the multi-streaming law switch; idea 8 below is only mapped onto it.

## What a candidate must do (record targets)

- Residue (SE2 joint posteriors, canonical / alt): X-COP +0.440 / +0.408 dex, groups +0.232 / +0.194, Coma UDGs
  +1.120 / +1.075. Discs <= 0.33 / 0.19 extra mass fraction, field dwarfs 0.
- Web (second wall): the law's phantom about off on the linear web, SV5 iter_1 lensing amplitude r <= 1.072 (law on:
  74.7 / 89.4); F_web <= 0.005 (OQ1/OQ2); WL1 stage 2: even the hosts' retained phantom over-sources CMB lensing
  (r_pop 3.75 / 4.32 at z 1).
- Keep: Cassini/PPN, c_T, galaxy lensing = dynamics (KiDS isolated lenses, K-G6 line |shift| <= 0.05 dex), SPARC.

## The structural constraint every local idea meets (from the record)

1. Matter couples minimally, so in the static weak field every khronon quantity is a functional of Phi (DX1 §0).
2. In spherical symmetry the static equation of v3s / AC2q is algebraic in g, so g = f(g_N): a single-valued nu.
   QX2 iter_2 kills every single-valued nu (X-COP needs 0.30-0.51 dex more than SPARC at the same y).
3. So a local action can only escape through one of: (a) dependence on derivatives of the field beyond g (profile
   shape or an absolute length), (b) more than one static root (branches), (c) a new matter channel, (d) a mediator
   with its own range. Shape-only keys are dead (FA1 I1 tidal isotropy, KT28-KT32 tidal rules); matter-stress keys
   are dead (p/rho, support, (v/c)^2 <= 1.1e-5: DX1); local keys in (x, rho_b, theta) hit X57's mu-pincer.
4. QX20's six variables are v_obs, M_b, f_gas, g_N/a0, r/r_M and depth. **No lane keyed on an absolute length.** A
   second length scale L2 in the action is the one local channel the record has not graded (the Lstar stiffness is a
   short-range one and acts only inside ~kpc; WG6 screened the phantom by hand from a baryons-only start, with no
   action and no galaxy-side grade beyond 1 Mpc).

## Candidates

### C1. Profile-length khronon invariant: J(Y, Z) with a second length L2  [TOP 3]
- **Term.** In the khronon frame, Y = A.A/c^4 and Z = (grad_i A_j)(grad^i A^j)/c^4 (spatial derivatives only, the
  Horava/khronometric class: no extra time derivatives, so no Ostrogradsky mode). The interpolation becomes
  J(Y, Z) with u = sqrt(Y)/a and w = L2^2 Z / Y = (L2 / ell)^2, ell = |A| / |grad A| the local length of the field.
  The phantom multiplier becomes F(ell / L2), F = 1 for ell << L2 (discs, Solar System), F > 1 for ell >~ L2.
- **Why not dead.** Not single-valued in y (escapes QX2 iter_2); not a shape-only key (ell carries an absolute
  length, FA1 I1's zeta does not); not in QX20's six variables; not a matter coupling.
- **Derivation note.** A polynomial Z term (idea C4) acts at ell < L2 only. To act at large ell the dependence must be
  non-polynomial in w (as J(Y) already is in Y). The static observable is then graded as a key class: any multiplier
  F that is a function of the point's own ell.
- **Most likely kill, stated now.** KiDS isolated lenses at R ~ 0.1-3 Mpc have the same ell as X-COP's points
  (0.1-1 Mpc) and follow the law; a scale key that gives X-COP x2.75 gives them the same. Second kill: groups need
  half of X-COP's boost at overlapping ell. Third: the web has the largest ell of all, so the law there only grows.

### C2. Massive phantom mediator: the phantom gravitates through a field of range L2  [TOP 3]
- **Target observable.** Matter feels Phi = psi_N + chi with (grad^2 - m^2) chi = div[(nu - 1) grad psi_N]: the
  law's phantom density, Yukawa-screened beyond L2 = 1/m. The range is the one new constant; it is set, not fitted,
  by the web condition.
- **Action status (corrected before any number, after an independent review of the first draft).** The first draft's
  multiplier Lagrangian does not give this system: varying chi makes lambda a screened Newtonian potential, which
  back-reacts on psi. The natural local completion, QUMOND's action plus -(m^2/8 pi G)(Phi - psi)^2, gives exactly
  grad^2 Phi = 4 pi G rho + div[(nu - 1) grad psi] with grad^2 psi = 4 pi G rho - m^2 chi: the mass does not screen
  Phi's source at all, it only reshapes psi (FA2 checks this with sympy). So no local action is in hand for C2. It is
  graded as a necessary condition: if even the target observable fails, every action that realises it fails.
- **Why not dead.** It is the action-level version of WG6's by-hand screening, now with the cold-like target source
  of SV5 (WG6 started from baryons only and its shape failed for that reason) and graded on the galaxy side.
  Not a key in (x, rho_b, theta): the screening is in k, so the mu-pincer does not apply directly.
- **Most likely kill, stated now.** F_web <= 0.005 needs (k L2)^2 <~ 5e-3 at the lensing k (0.01-0.2 /Mpc), so
  L2 <~ 0.3-1 Mpc. Galaxy halos at R ~ 0.3-3 Mpc (KiDS) then lose their phantom: K-G6 fails. It does nothing for the
  residue (screening only lowers the phantom), so X-COP, groups and UDGs stay at L0's FAIL.

### C3. First-order khronon phase: an S-shaped balance h(x) = mu(x) x (two static branches)  [TOP 3]
- **Term.** J(Y) with a non-convex window: h(x) = mu(x) x rises, falls on (x1, x2) and rises again, so for
  y in (y_a, y_b) the balance h(x) = y has a lower root (the law) and an upper root (more boost). A system sits on
  either branch (a domain wall between them is allowed in the static equation).
- **Why not dead.** Two-valued, not single-valued, in y (QX2 iter_2 kills only one value per y). Local, no new
  matter channel. Not the BK superfluid (QX28): no new substance, one field.
- **Most likely kill, stated now.** (i) Well-posedness: on the falling segment h' < 0 the static operator
  div(h'(x) grad) is not elliptic (the record's saddle_unbounded / AC16 kind), and the leaf problem loses strict
  convexity (EQUATIONS 2.7). (ii) Two values per y cannot serve three needs at the same y: SPARC 0, groups ~0.2,
  X-COP ~0.45 (and UDGs ~1.1 deeper). Third: the web sits on one branch; the lower one is the law (r 74.7).
- **Review note.** The bad coefficient is radial only (h'(x) < 0; the transverse one h/x stays positive). A static
  spherical solution that jumps branches is a weak solution (flux continuous, g kinked). The energy is non-convex, so
  relaxation gives a Maxwell plateau and the upper branch is only metastable: choosing it needs history (FA3's
  domain; X60's hysteresis latches were EXCLUDED). FA2 grades the static data side with the branch chosen most
  favourably per point, which bounds every history.

### C4. Polynomial higher-gradient khronon terms (Horava-type a_i Delta a^i / M^2, (div A)^2 L2^2)
- **Term.** J(Y) + beta L2^2 (div A)^2 / c^4.
- **Why not dead.** Not in the dead list as a residue mechanism.
- **Kill (derived, no data needed).** In spherical symmetry it adds -2 beta L2^2 g / r^2 to the balance
  (h(x) g -> g [mu - 2 beta L2^2 / r^2] = g_N in the deep flat regime): the correction falls as (L2 / r)^2, so it
  acts at small r only. It is the Lstar stiffness's class. It cannot raise clusters without first changing discs
  and the Solar System. The FA2 script checks this reduction with sympy. Not graded further.

### C5. Mass term for P (algebraic): -(1/2) m_P^2 |P|^2 in the Legendre form
- **Kill (on paper).** P is algebraic in the static sector (A = W'(|P|) P_hat), so a P mass only reshapes the
  constitutive law: a new single-valued nu(y). QX2 iter_2 kills the class. (A range needs gradient structure: C2.)

### C6. Non-minimal contact coupling of matter to the khronon charge, T^mn n_m n_n (D.P) / rho_DE
- **Idea.** Extra gravity where baryons and phantom sit together (clusters: gas fills the phantom's volume; discs: the
  phantom halo sits off the plane).
- **Kill (on paper).** QUMOND's phantom of a thin disc has its own thin phantom disc ((nu - 1) Sigma delta(z)), so
  baryons and phantom are co-located in discs too, with rho_b / rho_ph ~ 1 / (nu - 1) as in clusters: it reduces to a
  y key (QX2 iter_2). The matter equation picks up a force -grad(beta c^2 Pi / rho_DE) that varies on the Sun's
  stiffness scale: a Cassini risk with no gain. The Weyl / tidal variant (E_ij E^ij relative to (G rho_DE)^2) is an
  enclosed-density key (QX5) and FA1 I1 / KT28-KT32 killed its shape form.

### C7. Disformal matter coupling along the khronon acceleration, g~ = g + B A_m A_n
- **Idea.** Extra force on radial motions (pressure-supported systems) and none on circular orbits (discs).
- **Kill (on paper).** The effect is ~ (u.A_hat)^2 = sigma_r^2: the dead p/rho key (DX1 D1 ii) and kinematic support
  (QX22 slow = fast rotators). Coma UDGs (sigma ~ 30 km/s) need the largest boost of all. If photons couple too it
  changes lensing at O(1); if not, lensing != dynamics in clusters, and QX21 found the second cluster mass method
  >= hydrostatic, which excludes a gas-only extra force by sign. (This is not FA1 I5, which is a bulk-velocity
  selector; C7 is the A-direction disformal.)

### C8. Khronon expansion invariant as the law switch: S(K^2 / (24 pi G rho_DE)), K = div n
- **Idea.** The leaves are static (K ~ 0) inside bound regions and expand (K = 3H) on the web, so K^2 against the
  local constant 24 pi G rho_DE (= 9 H_Lambda^2) is on in galaxies and off on the web at every z.
- **Mapped, not graded here.** Its on-region is the bound region, the same as WL1's multi-streaming switch at the
  turnaround ceiling R_ms. WL1 (closure_2026_11_07/WL1_web_law_switch) graded that switch: stage 1 PASS, stage 2 FAIL
  (the hosts' retained phantom alone over-sources CMB lensing, r_pop 3.75 / 4.32 at z 1, line 1.072). C8 inherits
  that label. If the khronon is AC2q's dark-energy clock, its leaves follow cosmic time even inside galaxies (phi is
  barely perturbed), so K = 3H everywhere and the switch never turns on: dead on paper for AC2q.

## Ranking (before any number)

C1, C2 and C3 are graded. Each escapes the structural constraint by a different route ((a) an absolute length,
(d) a mediator range, (b) branches). C4-C7 die on derivation or on the record, and C8 is WL1's switch. Pre-stated
expectation: all three FAIL, on KiDS (C1, C2), on groups/X-COP at fixed y and on ellipticity (C3), and on the web
(C1, C3). A FAIL here is a label on the last local channels, which is the useful answer.

Kappa = 1/2 FITTED; not theory closed.

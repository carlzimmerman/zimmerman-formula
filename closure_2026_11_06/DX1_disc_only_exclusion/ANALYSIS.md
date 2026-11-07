# DX1 analysis: can anything keep a cold component out of rotating discs only?

Written before any DX1 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle of any
kind. The component is the record's "cold dark energy" (KD1's K(Q) dust is its one action-derived form). Exit 3 of
ALL_GATES_NOGO_2026_11_06.md. Both footings throughout, never pooled.

**What is asked.** On top of the a0 law, the extra mass fraction must be f <= 0.33 / 0.19 in SPARC discs (canonical /
alt) and f ~ 4.2 / 3.8 in X-COP, 1-3.5 in groups (KD1 diagnostic). An "order-1 disc/hot difference" here means a
factor >= 13-21 in retained mass between a disc and a hot host, at equal g_N.

## 0. What the action lets matter tell the khronon sector (from QX17 E5 / QX17A)

- Matter is minimally coupled (QX17 E5). The khronon, P and K(Q) fields see matter only through the metric, which is
  sourced by T^m_mn. Nothing in v3s or AC2q couples u_matter to n^m or P^m directly.
- A rotating disc and a pressure-supported sphere with the same rho(x) differ only in T_0i = rho v (order v/c relative
  to rho) and T_ij = rho v v + p (order v^2/c^2).
- T_0i sources the shift (gravitomagnetism). Retention is a scalar and must be even under reversing the sense of
  rotation, so it enters no earlier than (v/c)^2.
- Sizes: (v/c)^2 = 2.8e-8 at 50 km/s, 4.5e-7 at 200, 1.0e-6 at 300, and 1.1e-5 for a 1000 km/s cluster. An order-1
  step needs about 1. **The gap is >= 1e5.** These are the PN preferred-frame terms the record already bounds (AC17,
  C6P).
- **Switches cannot amplify it.** The only non-analytic pieces are Pi_+ (v3s) and Sigma_+ = max(D.P + 2X, 0) (AC2q).
  A switch amplifies a small input only where its argument sits at zero.
  - In galaxies D.P is the phantom density, positive and far above 2X ≲ rho_DE.
  - A relative shift of 1e-6 cannot flip its sign.
  - The switch gates only gamma terms, whose relative size at galaxy densities is gamma_L Pi_+ = 2 pi G rho Lstar^2/c^2
    ≲ 1e-10 (QX17 §3).
  - So the suppression is double.
- **Static capture does not depend on how a host is supported.** In the static weak field every khronon-sector
  quantity is a functional of Phi. Phi depends on rho_b, not on how rho_b is supported. KD1 found f_cap 4.11 in every
  class, and nothing in the equations can make that number class-dependent.

**Consequence.** Inside v3s / AC2q, no direction gives an order-1 disc/hot difference. A candidate must add a new
matter coupling. Each direction below is examined in that light.

## D1. Coupling to the matter flow relative to the khronon frame or P

- **Inside the action:** order (v/c)^2, as in §0. Dead.
- **New couplings: the local scalars available.**
  - (i) Bulk velocity against the khronon frame, |h.u|. This is FA1 I5, dead on order of magnitude: the Local Group
    moves at 600 km/s, clusters at 300-1000.
  - (ii) Stress along P: T_mn Phat^m Phat^n / rho = sigma_r^2. This is the dead p/rho key. It is also non-monotone in
    what it needs:
    - dSphs need f ~ 1.7 at sigma ~ 10 km/s;
    - discs need ≲ 0.3 at sigma_R 10-40 (gas, stars) with v_c 50-300;
    - X-COP needs 4 at ~1000.
    - No threshold on any v^2 orders them.
  - (iii) Stress anisotropy relative to P, beta_P = 1 - T_perp / (2 T_PP), the one tensor invariant that knows
    "u perpendicular to P":
    - near 0 for isotropic clusters, groups, slow rotators and dSphs;
    - about -(v/sigma)^2/2 for rotating systems, so about -50 for cold discs.
    - This is the local form of kinematic support.
- **QX22 test.** At equal M* and sigma, low-lambda and high-lambda red galaxies sit at +0.002 +- 0.045 ln. A support
  key predicts +0.14 (about 3 sigma). Fast rotators (v/sigma ~ 1, beta_P ~ -0.5) must therefore keep the component as
  slow rotators do.
  - beta_P survives only with a threshold beyond fast rotators: |beta_c| >> 1, so only kinematically cold discs
    (v/sigma ≳ 3) are "off".
- **That surviving form fails on locality.**
  - A cold disc's stress lives in a layer of volume fraction ~ h_z/R ~ 0.1, while the component fills the sphere.
  - KD1's fluid is irrotational and static once settled. It sits in a core of radius pi/mu_K (0.35 pc at the CMB/BBN
    setting), which is inside the bulge, not in the disc layer. No flux of the component crosses the layer, so a local
    sink removes at most the layer's share, about 0.1, not the factor 13-21 needed.
  - An orbit-crossing sink would need a collisionless component, which means particles; the no-particle rule excludes
    that.
  - The system-level version (V/sigma of the host) is FA1 I2 reading R, KILLED by the ellipticals (Z -2.15).
- **Label: DEAD.** Inside the action: (v/c)^2 <= 1e-5. Outside: the monotone keys are dead (p/rho, support via QX22,
  I5). The QX22-surviving cold-disc form is local, and its effect is bounded by the layer volume, about 0.1.

## D2. Angular momentum or vorticity

- **Why FA1 I2 died (read first).**
  - Reading P, local exp(-omega^2/omega_*^2) with omega_* ~ a0/c: the ICM's measured shear is 27-130 x omega_*, so
    the component is off in clusters.
  - Reading R, system V/sigma: 13 SLUGGS ellipticals sit at +0.094 against +0.199 predicted (Z -2.15).
- **From the equations.**
  - The component's own flow is along n^m, which is hypersurface-orthogonal, so its vorticity is identically zero
    (Frobenius) in discs and clusters alike. Its own vorticity cannot be the key.
  - Matter vorticity reaches the khronon sector only through T_0i, at order (v/c)^2 (§0).
  - Specific angular momentum j/(r v) is v/sigma again, so QX22 and I2-R apply.
- **Surviving QX22?** Only with the same "cold discs only" threshold as D1, and then it inherits D1's locality bound.
  Coupling to the gas current alone (the stars are collisionless baryons, but a fundamental coupling to the baryon
  current cannot tell stars from gas) would be the cold-gas key. QX23 killed that in SPARC's range: gas-poor minus
  gas-rich +0.053 +- 0.038 against +0.27-0.35 predicted.
- **Label: DEAD** (FA1 I2 both readings; QX22; QX23; zero vorticity of the khronon flow).

## D3. AC2q off-branch (Sigma = D.P + 2X < 0)

- In the static weak field D.P is the phantom density.
  - For an isolated spherical source, rho_ph = (4 pi G r^2)^-1 d/dr[(nu - 1) g_N r^2] = (4 pi r^2)^-1 d/dr[(nu - 1) M_b(r)]
    is positive, because M_b is non-decreasing and nu - 1 grows outward.
  - Sigma < 0 needs negative phantom density below -2X. That happens at external-field saddles between systems: an
    environment configuration, not a disc property.
- **Even where Sigma < 0, the off-branch changes very little.**
  - It removes the gamma Sigma_+ terms, of relative size ≲ 1e-10 at galaxy densities.
  - It adds T_off = +(3/2) gamma Q^4, a homogeneous cosmic-scale term (QX17A, off-region). That is not a localized
    mass of f ~ 4.
  - AC2q has no K(Q) dust at all, so there is no cold component on that branch to remove.
- **Label: DEAD** (structurally; no order-1 effect at galaxy scale on either branch).

## D4. Disc formation history (expelled during dissipative assembly)

- **(a) Adiabatic contraction.** Cooling gas deepens Phi, which pulls a cold component in. The sign is wrong.
- **(b) Feedback expulsion.**
  - Unbinding f_cap M_b needs E ≳ (1/2) f_cap M_b v_c^2. Supernovae supply about 1e51 erg per 100 Msun formed, which
    is (709 km/s)^2 per unit stellar mass.
  - The component would have to absorb the following share of all supernova energy, through gravity alone:
    - 23 % for the MW (v_c 220, M*/M_b 0.85);
    - 15 % for a gas-rich LSB (60 km/s, M*/M_b 0.1);
    - 5 % for a 50 km/s dwarf with M*/M_b 0.2.
  - Starting from KD1's 0.35 pc core, far more is needed.
  - **The ordering is inverted.** Ellipticals and dSphs (gas-poor, M*/M_b ~ 1, plus AGN in ellipticals) had the most
    feedback energy per baryon, and they are the systems that need the component. Gas-rich, low-SFR discs had the
    least, and they must lack it.
  - Inside SPARC, QX23's gas-poor minus gas-rich is +0.053 +- 0.038, so the more-star-forming discs sit higher, not
    lower. The data go the wrong way for expulsion.
- **(c) "Never accreted".** A component that is cold early follows the same infall as the baryons: capture at
  turnaround depends only on Phi (KD1 f_cap is identical in every class). A disc assembles inside an already-collapsed
  host.
- GB1 carries no history feature (z_f is None everywhere, as F2 found), so a history key is NOT GRADABLE as a
  candidate. The sign arguments above decide it without data.
- **Label: DEAD** (wrong sign for contraction and expulsion; energy share 5-23 % with inverted ordering; capture is
  history-blind).

## Bottom line, and the one graded question that remains

No direction gives an order-1 disc/hot difference that survives the record. So no direction is frozen as a candidate.

There is a separate question, not about the mechanism: **would a perfect disc-only exclusion help at all?**
- KD1's needs show the on-amplitude itself must vary across hot classes: ellipticals 0.86, dSphs 1.7, X-COP 4.2,
  Coma UDGs 86 (canonical).
- A universally captured cold component gives 4.11 to each.
- If an ideal exclusion (f = 0 in discs by fiat, f_cap everywhere else) still fails GB1, exit 3 on its own cannot close
  the triangle for any mechanism.
- That bound is cheap to grade on GB1 read-only. It is frozen in FROZEN_CRITERIA.md as an ORACLE BOUND. It is not a
  candidate: it uses a class label, which GB1's interface forbids for candidates.

Kappa = 1/2 FITTED; not theory closed.

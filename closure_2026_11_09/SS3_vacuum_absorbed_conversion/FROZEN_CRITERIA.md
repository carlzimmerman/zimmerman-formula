# SS3 (vacuum-absorbed conversion, the outside source's variant J): FROZEN CRITERIA, committed alone before any SS3 script or number

TEST lane, quarantined; registered by the orchestrator. Adopts nothing; no particle adopted. kappa = 1/2 FITTED; not theory
closed. Footings canonical and alt, graded separately, never pooled. SS1 / SS2 machinery is used read-only: ss3.py imports
SS1's ss1v.py, ss1.py and ss1_cosmo.py and monkeypatches J's retention inside its own process; nothing in SS1 / SS2 is edited.

## 1. Construction J, frozen once (as relayed, in the lane's words)

- **Onset and rate:** z_dec 0.631, alpha 4.367 / 4.366 (the record's footings, as G).
- **The product is vacuum energy** (w = -1, no perturbations claimed): chi + chi -> khronon vacuum. Conversion happens only
  where the local density exceeds 200 rho_crit, i.e. in collapsed halos. The web never converts.
- **Two equal helicity halves:**
  - the transverse half converts at Gamma0 in every collapsed halo (retains e^-alpha);
  - the longitudinal half converts at Gamma_par(r) = Gamma0 (v_stiff / sigma_1D(r))^2.
- **Retention per radius:** f(r) = 0.5 e^-alpha + 0.5 exp(-alpha (v_stiff / sigma_1D(r))^2).
  - sigma_1D comes from SS1's primary pre-conversion halos (KD1 P3 SIS: sigma_1D^2 = V^2/2).
  - Bracket J-NFW: Duffy NFW isotropic Jeans.
  - Bracket J-src: the source's g_NFW, as sigma^2 / v_vir^2 = u/(0.08 + u)/(1 + 2.5 u^1.5) (the source-fitted profile the
    lane already carries).
- **Converted mass leaves the system as vacuum.** No daughter mass and no shelf in the primary reading; N3 tests that.
- **Time dependence:** each half decays exponentially at its own rate, f(r, tau) = 0.5 e^-tau + 0.5 e^(-tau (v_stiff/sigma)^2).
- **Cosmic converted fraction:** Press-Schechter collapsed fraction at z_dec (M_min 1e6 primary; bracket M_min 2e11, the
  source's "halos below 2e11 never reach 200 rho_crit"), each node a primary halo with its own f.
- **Background:** the A integrator with the converted matter going into w = -1 (rho_vac constant after creation), h re-solved
  to hold theta_s, bare Lambda plus the created vacuum.
- **Form choices beside the label:** the 50/50 helicity split, (v_stiff / sigma)^2, the 200 rho_crit activation, plus G's
  cube root and 4 pi. Fitted constants: 0.

## 2. Gates (SS1 / SS2 lines) and three new ones

**Gates 1-10 as SS1 A2** (1 KiDS, 2 groups, 3 X-COP, 4 UDGs reported, 5 SPARC, 5b UMa, 6 BAO + SN at the theta_s-held h,
7(b) lensing NO VERDICT by A / SS2's rule with the ratio-method reading reported, 8 forest + fsigma8 by fine-grid central
differences, 9 Bullet, 10 Cassini). Growth and lensing come from the A machinery's background and scale-free two-fluid ODE:
the converted component is gone from the matter source at every k, the vacuum is smooth.

**N1, dark-energy history** (graded). J's omega_DE(z) = omega_Lambda + omega_vac created by z, on the theta_s-held background,
against CFG689's primary BAO + SN posterior node values (nodes z 0, 0.4, 0.7, 1.0, 1.5, 2.33, `node_mean` +- `node_std` in
cfg689.json, curvature-free primary; diagonal, disclosed: the full node covariance is not on disk).
- PASS iff every node is within 2 sigma, AND chi^2_J - chi^2_const <= 4, where chi^2_const is the best constant omega_DE on
  the same nodes.
- Reported: the rise in rho_DE from z_dec to 0 (source +7.45 %).

**N2, a0(z)** (graded as frozen). a0 is proportional to sqrt(rho_DE), so J predicts a0(0)/a0(z_dec) = sqrt(omega_DE(0) /
omega_DE(z_dec)) (source +3.66 %).
- Against the record's a0(z) cells (AT2 / CFG689): **NOT EVALUABLE** is expected, because the 0.3-0.6 dex common modes and
  the BLOCKED AT2 cells swamp a 3.7 % drift. If so it is said, and N2 does not enter the label.
- SPARC's z ~ 0 calibration: kappa is fitted, so a0 today is calibrated, not predicted; the shift of a0 today against the
  footing value is reported.

**N3, covariance** (graded as a statement).
- **The coupled equations:** nabla_mu T^mu_nu(chi) = -Q_nu and nabla_mu T^mu_nu(vac) = +Q_nu, with T^mu_nu(vac) = -rho_vac
  delta^mu_nu and Q_nu = Gamma(x) rho_chi u_nu.
- **Integrability:** the vacuum equation reads -partial_nu rho_vac = Q_nu, so Q_nu must be a gradient: partial_[mu Q_nu] = 0.
- **The test:** for a static halo (u = time-like Killing direction) with Gamma rho_chi depending on r, the curl
  partial_i Q_0 - partial_0 Q_i = -partial_i(Gamma rho_chi) is non-zero.
- **PASS** iff the integrability condition holds for the construction's Q (checked symbolically, sympy). Otherwise FAIL:
  no perturbation-free vacuum can absorb a halo-local transfer.
- **Reported:** what local conservation forces. delta rho_vac(x) = integral of Gamma rho_chi dt (the converted density stays
  where it was made) with no static equilibrium (a w = -1 gradient carries no momentum flux to balance it). The lensing
  reading "energy stays local" is then the full pre-conversion halo for lensing: KiDS shift at the lane's full-retention
  number (SS1 MG3-like, 0.378 dex canonical). That number is reported beside the label.

**Label per footing.** PASS iff gates 1, 2, 3, 5, 5b, 6, 7(b), 8, 9, 10, N1 and N3 pass (N2 enters only if evaluable).
Otherwise FAIL with the first failing gate in the order 1, 2, 3, 5, 5b, 6, N1, N3, 7b, 8, 9, 10.

## 3. Claims to compute, not take (reported beside the gates)

| quantity | source's claim |
|---|---|
| cosmic converted fraction of the component | 18.5-28.4 % |
| Omega_DE | 0.641 -> 0.689 |
| a0 | +3.66 % |
| D_M / r_d at z 0.51 | 13.56 |
| sigma8 | 0.762 / 0.758 |
| S8 | 0.766 / 0.761 |
| fsigma8(0.3) | 0.453 / 0.451 |
| KiDS 1-halo remnant | 1.5-3.5 % (+0.008..+0.029 dex) |
| X-COP retained / M_dyn | 0.72 / 0.64 / 0.53 |
| groups | 25-48 % |

## 4. Known answers

- **KA-J1:** the code's f equals the formula for the SIS: 0.5 e^-alpha + 0.5 e^(-2 alpha (v_stiff / v_vir)^2).
- **KA-J2:** law-only replay (component -> 0) on gates 1-5. Bullet K1.
- **KA-J3:** the w = -1 background with zero conversion returns the reference h and chi^2 (SS1 KA7).
- **KA-J4:** CFG689 node means and stds read back equal to cfg689.json.

## 5. MUTATE

- **MJ1:** product w = -1 -> radiation (w = 1/3). N1 and gate 6 must move (the A class, which failed BAO).
- **MJ2:** v_stiff -> 0 (only the transverse half converts, 50 % everywhere). Groups and X-COP numbers must move.
- **MJ3:** M_min 2e11 (the source's choice) is reported as a bracket. It is not a MUTATE.

## 6. Hand estimates (before any number)

- **Groups and X-COP, SIS:** the longitudinal half survives as e^(-2 alpha (v_stiff/v)^2). Groups (v 460) keep about 3 %,
  X-COP (v about 1000) about 28 %, so about 1.1 M_b against the need of about 4: under-filled. FAIL at groups (the source's
  25-48 % assumes its g_NFW).
- **Galaxies:** they convert almost entirely, so KiDS and SPARC PASS.
- **Cosmic conversion:** PS down to 1e6 gives about 0.75 of the component (about 0.25 with M_min 2e11). Omega_DE rises by
  far more than 7 % in the primary, so N1 and gate 6 likely FAIL, and growth FAILS (the component is gone from the source at
  every k).
- **N3:** FAIL by the integrability condition.

## 7. Operational

- One thread, nice 10, RSS < 1 GB except CLASS / the DB1 child; df check before each child.
- Outputs small: primary and the NFW bracket in the local gates.
- Explicit-path commits via a sparse temporary worktree.
- Files: ss3.py, ss3_cosmo.py, ss3_n3.py, ss3_grade.py, ss3.json / .out, ss3_MUTATE.json / .out, RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

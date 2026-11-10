# FB1 note: what the adopted action already says about form B, and what it does not (2026-11-09)

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Not registered. A note with one check, not a graded lane: no
criteria, no label. Written after the owner chose form B (`closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md`)
and asked for a complete theory.

## Answer first

**The theory is not complete.** One part of what the decision file lists as open is already answered by the record's own
action; three parts are not, and none of them is solved here. A fourth, the stability of the static state, was added
when TPA1 landed and is corrected below: SCS1 finds the state stable around a point mass with gravity coupled, and
SCS2 finds it stable around isolated discs. A disc in an external field is not settled.

## 1. What the action already gives (certified in QX17; one identity re-checked here)

Source: `closure_2026_11_06/QX17_covariant_field_equations/RESULT.md`, action (A) (the PAPER70 action), its field
equations (E1)-(E5) and its limits table.

1. **The law's halo is real energy density.** The energy density of the khronon sector seen by the clock's observers is
   rho = (mu_K^2 / 2K)(Q^2 - 1) + W + Pi + gamma_L F (QX17 K5), with Pi = D_m P^m. In the static weak field the 00
   equation is Poisson with source rho_b + D.P (QX17 limits table). So the "phantom" of the law is not a bookkeeping
   device in this action: it is the sector's own gravitating density. Light and matter both see it.
2. **It is carried by one conserved current.** The khronon equation (E3) is a conserved current whose charge is the dust
   term plus the polarization term (the record's N = rho + Pi). The same charge is cold dust in FRW (P = 0) and the
   law's halo around a static source. Nothing is counted twice, because there is one charge.
3. **Its shape is not put in by hand, for the static state.** With a static clock and gamma_L = 0 the equations give
   K P = (1 - mu) grad Phi and div[mu grad Phi] + mu_K^2 Phi = 4 pi G rho_b in any geometry; spherical with mu_K = 0 it
   is the law exactly (Lean `QX1.balance_iff_lawS`).
4. **The halo is held up by the law sector's own stress.** `fb1_check.py` -> `fb1_check.out` checks, for three static
   potentials with no symmetry, that the canonical stress of the law's Lagrangian,
   Pi_ij = J(g) delta_ij - g_i g_j / (K (1 + g / a0)), J(g) = (a0^2 / K)[g / a0 - ln(1 + g / a0)], satisfies
   d_j Pi_ij = (D.P) g_i pointwise (residual below 1e-150), that W's Legendre partner is this J, and that for a point
   mass the isotropic form reads P = J(g). That is PD1's P7 relation ("dispersion locked to sigma^2 = (1/2) sqrt(G M_b
   a0)", "div Pi = -rho (nu - 1) g_N"): in the deep field J = g^2 / (2K), which is the pressure of an isothermal halo
   with that dispersion. In the action it is a consequence of the static equations, not an assumption.
   **Caution (added after an independent check from the closure session):** the identity holds for any J(g) with
   P = dJ/dg and a curl-free field. It shows that the action's static state balances itself. It is not evidence that
   this J is the right one.

So the decision file's open item 1 ("no equation of motion makes the cold component take the law's shape around a disc")
needs a narrower wording: **for a static clock the action's own equations give that shape and hold it; what is missing is
the solution that gets there.**

## 2. What the action does not give (the theory is incomplete here)

1. **One dust term for the CMB and for galaxies.** With the quadratic K(Q), FRW gives w = w0 / (w0 + a^3) with
   w0 = I0 / (4 mu_K^2) (QX17). Dust by recombination needs mu_K of at least a few per Mpc (my arithmetic: w0 about
   1e-8 / mu_K^2 with mu_K in 1/Mpc, to be below 1e-9; not checked by a lane). The static clock then carries dust
   -mu_K^2 Phi / K in every well, and the record's galaxy-lensing bound is mu_K at most 0.1 per Mpc (QX2 iteration 5,
   S4); the record's standing entry is "mu_K = 0 in galaxies". No single value does both. Until one K(Q) does, the
   cosmological component and the galaxy halo are one charge on paper and two settings in practice.
2. **The collapse.** No solution of the time-dependent equations takes a free-falling clock (dust, falling in with the
   baryons) to the static clock (the law's halo). This is the spiral wall of the 2026-11-01 ledger. It is a computation
   inside the action, not a missing postulate, and it has not been done.
3. **Clusters, groups, the Bullet.** A static clock gives a cluster the law's halo plus -mu_K^2 Phi / K. QX2 graded
   that: +0.4675 / +0.4345 dex short on X-COP with the plain law, and the K(Q) dust needs mu_K 1.78 / 1.74 per Mpc
   to close it, 17 to 18 times the galaxy bound. So in this action a cluster's cold mass cannot be a static-clock state,
   and no other state has been solved. Groups and the Bullet's amount stay as the decision file lists them.

4. **Stability of the static state (added after TPA1 landed, 2026-11-09 late).** Section 1 shows the static state is in
   force balance. It does not show it is stable, and TPA1 says it is not, in the limit it checked. TPA1's law-on phase is
   this same action (QX17's), and its health item finds a static clock there gradient-unstable, with no ghost, wherever
   the clock's own dust density is below n_crit = -dp/dx: 0.08 to 0.9 of the law's phantom density for a point mass,
   with e-folding times of 5.0 Myr to 0.62 Gyr on its frozen grid (`fable52_push/TPA1_two_phase_action/RESULT.md`,
   origin 347967f64f). The static state of section 1 has almost no dust of its own (mu_K = 0 in galaxies), so it sits
   in that unstable range; carrying dust above n_crit would add mass of the order of the halo itself. TPA1's analysis is
   in the decoupling limit (metric frozen); it argues by hand that coupling to gravity does not change the sign and says
   the coupled analysis has not been done. Until it is, "the action holds the halo in the law's shape" means force
   balance only.

   **Corrected when SCS1 landed (2026-11-10).** The paragraph above is wrong for a point mass. SCS1
   (`fable52_push/SCS1_static_clock_coupled_stability/RESULT.md`, origin 0bacbb61f5) did the coupled analysis: STABLE /
   STABLE. The clock's gradient coefficient is its own charge density n_d + D.P. Around a point mass on the law D.P is
   the phantom density, p' + 2p/r, which is positive, so nothing grows at any wavenumber. TPA1's instability came from
   its planar background, where D.P = p' is negative; SCS1 reproduces TPA1's numbers in that background and loses them
   in three dimensions. The n_crit threshold quoted above does not exist wherever the phantom density is positive.
   What stays open on stability: flattened baryons. Around a disc the law's phantom density can be negative in places,
   and there SCS1's own closed form gives growth (bounded without the stiffness, rising with wavenumber with it). Discs
   were not analysed. At the dust constant the CMB needs, the static state clumps at the free-fall rate (JEANS-ONLY),
   which is item 1 again, not a new flaw.

   **Corrected again when SCS2 landed (2026-11-10).** "Around a disc the phantom density can be negative in places"
   is not what the law does for an isolated disc. SCS2
   (`fable52_push/SCS2_static_clock_stability_discs/RESULT.md`, origin 55e47026a4) solved razor-thin exponential,
   Kuzmin, thick and bulge discs at four masses: the phantom density is positive in every cell of all 40 isolated
   backgrounds per footing, and no mode grows on either route: STABLE / STABLE. Negative phantom density appears only
   with a uniform external field (a far-field band and the field's null on the axis); those brackets read unstable in
   regions on both routes but are NO VERDICT, because their magnitudes are not converged between grids. So the open
   stability item is discs in an external field, in the linear sense, not discs.

## 3. What would make it complete

- A K(Q) (or its replacement) that is dust-like at early times and leaves less than the lensing bound in galaxy wells,
  with the same constants. Then items 1 and 3 above become numbers to grade.
- The spherical collapse of the clock around a baryon mass, run with the record's own equations (QX17; the
  finite-difference solver of QX17C exists), to see whether the static state is reached.

Neither is started here. The decision file allows no mechanism lane without the owner's go.

## Files

`fb1_check.py` (about a minute, sympy, exact derivatives, 50-digit arithmetic), `fb1_check.out`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

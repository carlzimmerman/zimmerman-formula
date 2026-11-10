# R541D RESULT: a baryon-current coupling ties the charge but makes antibaryons, 4.3 million times too many. EXCLUDED / EXCLUDED (canonical / alt)

Criteria: `FROZEN_CRITERIA.md`, committed alone first (f574cc3958). No amendment. Adopts nothing. kappa = 1/2 FITTED;
not theory closed. Footings are not pooled. The component is cold dark energy. No particle was added.

## Label

**EXCLUDED on both footings.** Adding eps (d_m tau) J_B^m to action (A) does tie the charge to baryon number, provided
the universe starts neutral after inflation: R = -eps / m_bar. But eps is a new constant: no energy built from the
framework's own constants lands within 1.2 % of it. So the best this route could reach is TRADES. It does not reach
TRADES, because the same term is a constant chemical potential for baryon number, mu_B = eps Q. Electroweak sphalerons,
which act down to 131.7 GeV, relax the universe to n_B/s = -3.75e-4. That is 4.3e6 times the observed 8.7e-11, and it
has the wrong sign: it makes antibaryons. GD3 fails as frozen, by a factor of 4.3e6 and on the sign. GD4 fails too.

## Gates

| gate | canonical | alt | as frozen |
|---|---|---|---|
| GD1 conservation law | nabla.[(mu_K^2/K)(Q-1) n + eps J_B] = 0; general 1+1 metric and current, residual 0; FRW: a^3[(mu_K^2/K)(Q-1) + eps n_B] conserved; with J_B conserved the term is a total derivative (residual 0) | same | PASS (structural) |
| GD2 the constant | neutral start p = 0: rho_K = -eps n_B + K eps^2 n_B^2/(2 mu_K^2); energy per unit charge (Q+1)/2, which goes to 1; **eps = -5.0700 GeV** (m_p bracket -5.0761). eps < 0 for rho_K > 0. Without the neutral start, p/a^3 is free again. Nearest native energy: 2 M_Pl,red^(2/5) rho_DE^(3/5)/4, at 0.914 of eps; none of 79 lands within 1.2 % | **eps = -5.0718 GeV** (-5.0779); nearest 0.913 | eps is a NEW fitted constant, so TRADES at best |
| GD3 does it make the baryons | bias mu_B = eps Q = -5.07 GeV; n_B/s = 9.73e-3 mu_B/T (SM, B - L = 0); observed 8.70e-11 would need freeze-out at T_D = 5.67e8 GeV. No such freeze exists: the dimension-five operator freezes at about 1.6e13 GeV, and sphalerons act to 131.7 GeV. At T_sph: **n_B/s = -3.75e-4, X = 4.31e6, antibaryons** (4.23e6 to 4.39e6 over T_sph +- 2.3 GeV). A separate B - L source could cancel it only if tuned to 1 part in 4.3e6 | X = 4.31e6, antibaryons; T_D 5.68e8 GeV | **FAIL** (line X > 10 and the sign) |
| GD3, structural | in equilibrium n_B = chi eps Q with chi > 0, so rho_K = -eps n_B = -chi eps^2 Q < 0 for EITHER sign of eps: this coupling can only make negative cold dark energy by itself | same | (supports FAIL) |
| GD4 energy and back-reaction | the clock's Hamiltonian equals a^3 rho_K = u + K u^2/(2 a^3 mu_K^2), u = p - eps X; dH/dX = -eps Q = +5.07 GeV per baryon made (eps < 0), so making a baryon is uphill and equilibrium runs the other way. The kinetic matrix is unchanged (the term is linear in tau-dot). Q - 1 <= 0.01 at T_sph needs **mu_K >= 9.86e19 /Mpc** (1/mu_K = 313 m). The record's values 198, 2.51e4 and 8.89e6 /Mpc give Q - 1 = 2.5e33, 1.5e29 and 1.2e24 there, and the bias eps Q is then larger still. |eps| exceeds the pbar e+ threshold (0.9388 GeV) by 5.40x: the vacuum is energetically unstable to B violation. A stable vacuum would cap R at 1.0017 | same (9.86e19) | **FAIL** (no mu_K the record names) |
| GD5 visible today | psi -> exp(i eps tau) psi removes the term from every B-conserving term: flat residual 0, and 0 with a generic vierbein and spin connection. So there is no fifth force and no EP signal; the Kostelecky-Tasson a_mu bounds do not apply to a pure gradient common to p and n (a curl is non-removable, KA6). It lives only in B-violating operators. Proton: Delta B = -1 decays release 6.01 GeV; a dimension-six rate grows by about 1.1e4 and the operator-scale bound by 10.2x. The SM alone has no T = 0 B violation (exp(-4 pi/alpha_W) ~ 2e-164) | same | PASS (reported) |
| GD6 cold, separate, adiabatic | after T_sph the term is a total derivative (GD1), so the component decouples from the photon-baryon fluid. A local neutral start gives rho_K / n_B = -eps everywhere, so there is no relative isocurvature if the baryon asymmetry is adiabatic (argued, not solved) | same | PASS (structural) |
| GD7 rules and prior art | the term couples matter to d tau, so it formally breaks "matter couples to the metric only"; it adds no particle. Literature below | same | reported |

Known-answer checks: KA1 eps = 0 gives R541 part B's p_tau (PASS); KA2 Harvey-Turner B = (28/79)(B - L), 0.354430 (PASS);
KA3 Fermi-Dirac asymmetry g mu T^2/6, 1.0000001 (PASS); KA4 KD1's BBN line 8.887e6 /Mpc (PASS); KA5 I0 = 4.0356e-8 Mpc^-2
(PASS); KA6 rephasing residual 0, a curl is not removable (PASS).
Mutations: MU1 eps -> -eps flips rho_K, and R x 2 doubles eps (moves). MU2 eps x 1e-7 gives X = 0.43 (the gate can
pass); T_sph -> 1e9 GeV gives X = 0.57 (moves with T). MU3 mu_K / 10 raises Q - 1 by 100.0 (moves).

## What is new relative to CFG360

CFG360 row b3 said, by argument only, that a derivative coupling "sets eta_B, not R". Here the conserved total is
derived, and the neutral start does make R = -eps / m_bar with no quantum mass, so no 5 GeV particle is needed. But the
same eps then sets eta_B too, and quantitatively it sets it wrong: 4.3e6 times too large, with the wrong sign. CFG360's
5 GeV reappears as the coupling |eps| = 5.07 GeV.

## Literature (PROVISIONAL: abstracts and search summaries only)

- Shen, Mou, Zheng, Li, arXiv:1710.03945: mimetic dust with shift symmetry, so only derivative couplings; it uses a
  coupling to the baryon current to make the asymmetry. The abstract does not tie the dust's amount to baryon number.
- Carroll and Shu 2006 (PRD 73, 103515, hep-ph/0510081): Lorentz-violating backgrounds make an asymmetry in
  equilibrium. Their sphaleron-driven case needs a constant vector AND a late phase transition to switch the bias off.
  Action (A) has no such transition, and that is exactly why the bias here overshoots.
- Cohen and Kaplan 1987 (spontaneous baryogenesis) and Davoudiasl et al. 2004 (gravitational baryogenesis): not
  re-read; cited as the standard forms. In both the bias decays or is tiny; here it is constant at |eps| Q.
- A search summary mentions a 2005 ghost-condensate paper with (g/f) d phi J_B that needs the condensate's value to
  shrink to escape bounds. Not identified or re-read.
- I found no paper that ties a dust-like field's amount to baryon number through this coupling.

## Not checked, and weaknesses

- The sphaleron coefficient is the symmetric-phase one. Near the crossover the Higgs vev changes it by O(1), which is
  irrelevant against 4.3e6. Arguments that a derivative coupling is not exactly a chemical potential (Dolgov et al.)
  concern a time-dependent tau-dot; here tau-dot is constant. Not computed.
- The dimension-five freeze-out is an order-of-magnitude formula; it does not decide anything, because the sphalerons act
  later.
- No perturbation solve for GD6. Inflationary fluctuations of tau carrying charge were not checked.
- GD4's Q - 1 failure comes from action (A)'s own dust term, not from the coupling: it widens KD1's mu_K gap, from
  1.1e5 to about 1e18 against galaxies' <= 79 /Mpc. GD3 alone decides the label.
- The vacuum-instability rate for |eps| > m_p + m_e was not computed: it depends on an unknown B-violating operator.
- Look-ups (Y_p, T_sph, Super-K, Delta m^2_atm, the literature) are PROVISIONAL.

## Files

`FROZEN_CRITERIA.md`; `gd_symbolic.py` -> `gd_symbolic.out` (GD1, GD4, GD5, KA1, KA6, MU1); `gd_numbers.py` ->
`gd_numbers.out` (GD2, GD3, GD4, GD5, KA2-KA5, MU1-MU3). Each runs in seconds.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

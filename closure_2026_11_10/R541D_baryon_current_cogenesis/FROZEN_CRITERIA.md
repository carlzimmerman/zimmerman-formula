# R541D FROZEN CRITERIA: baryon-current co-genesis of the cold dark energy charge

Written and committed alone, before any script and before any gate number. Adopts nothing. kappa = 1/2 FITTED; not
theory closed. Footings canonical (R = 5.410, a0 9.3603e-11 m/s^2) and alt (R = 5.412, a0 1.1312e-10 m/s^2), never
pooled. The component is cold dark energy (a field component, not a particle). No particle is added.

## 1. Setup (exact)

Action (A) of PAPER70 (`qwen_claude_field_theory/papers_2026/PAPER70_field_equations_closure_2026.tex`, Eq. A) plus one
term:

    S = S_A + S_m + eps * Int d^4x Jt_B^m d_m tau,      Jt_B^m = sqrt(-g) J_B^m  (baryon-number current density)

eps is a constant with dimension of energy (natural units hbar = c = 1; reported in GeV). tau is the khronon,
Q = sqrt(-g^mn d_m tau d_n tau). Homogeneous background: P = 0, so F(0) = W(0) = 0 and only
L_K = mu_K^2 (Q - 1)^2 / (2K) carries tau (K = 4 pi G). Everything else in (A) is unchanged.

Hand expectation (declared now, not a result): (i) the shift current becomes J_K + eps J_B with J_K = (mu_K^2/K)(Q-1) n;
(ii) a neutral start gives rho_K = -eps n_B at late times, so R = -eps / m_bar (m_bar = mass per baryon) and eps is
about -5 GeV; (iii) the same term is a constant chemical potential mu_B = eps Q for baryon number, and electroweak
sphalerons, active down to about 130 GeV, then relax n_B/s to a value proportional to eps / T_sph, which I expect to be
far above the observed 8.7e-11 and of the sign opposite to the one positive rho_K needs. These are written to be broken.

## 2. What is new relative to CFG360 (campaign_fresh_gravity/CFG360_baryon_tie/)

CFG360 tied a complex wave field's U(1) charge to baryons: R = (m/m_p) r, so equal charges need a 5 GeV quantum (a
particle). Its row b3 dismissed a derivative coupling d(theta) J_B / f as "sets eta_B, not R" by argument only [ARG].
New here: (a) the charge is the khronon's shift charge, whose energy per unit charge is 1 at late times (no quantum
mass m enters, so no particle), (b) the conserved total p = a^3[(mu_K^2/K)(Q-1) + eps n_B] is derived, not argued,
(c) the "neutral after inflation" initial condition is used to tie C to the created baryon number, and (d) b3's
statement is tested quantitatively against SM sphaleron equilibrium with a constant bias, with sign.

## 3. Gates (each with its line and source)

- **GD1 conservation law.** Derive (sympy) the tau equation with the term. PASS iff
  nabla_m[(mu_K^2/K)(Q-1) n^m + eps J_B^m] = 0 and, in FRW, d/dt{a^3[(mu_K^2/K)(Q-1) + eps n_B]} = 0 exactly
  (residual 0). Also check: with d_m J_B^m = 0 the term is a total derivative (residual 0). This gate is structural; it
  does not by itself grade the label.
- **GD2 the constant.** With p = 0 (neutral start), late R = -eps / m_bar x f, with f the late-time energy per unit
  charge (derive f; expected 1 because rho_K / charge density = (Q+1)/2). m_bar = rho_b / n_B from the helium mass
  fraction Y_p = 0.245 (PROVISIONAL, Planck 2018 BBN-consistent value) and atomic masses of 1H and 4He (CODATA/AME);
  m_p alone reported as the bracket. Report eps for R = 5.410 and 5.412 in GeV, and its sign for rho_K > 0. Without
  inflation (p free): C free, nothing gained (stated, checked: p != 0 adds a free a^-3 term).
  Natural normalisation: check whether any energy built from the framework's own constants {G, c, hbar, rho_DE, a0,
  kappa} lands on |eps|; a candidate counts only if it is within 1.2 % (the Planck fallback width on R, 0.065/5.41)
  AND is produced by the action. Otherwise eps is a NEW fitted constant -> at best TRADES.
- **GD3 does the same coupling make the baryons (and does the bias survive)?**
  - Known observed value: n_B/s today from omega_b = 0.02236 (canonical) / 0.02234 (alt), T_cmb = 2.7255 K,
    g_s0 = 3.909 (3.046 neutrino species), m_bar as above. Expected near 8.7e-11.
  - Bias: mu_B = eps Q (sign derived in GD1/GD4 from the Hamiltonian). SM chemical equilibrium above the electroweak
    crossover (3 generations, 1 Higgs doublet, all Yukawas in equilibrium, Y = 0, B - L fixed, B not conserved).
    Compute n_B/s(T) = c_B (mu_B / T) and the T_D at which equilibrium gives the observed value.
  - Last B-violating process: electroweak sphalerons freeze at T_sph = 131.7 +- 2.3 GeV (D'Onofrio, Rummukainen,
    Tranberg 2014, PRL 113, 141602; lattice SM; PROVISIONAL as a look-up). Report the overshoot factor
    X = |n_B/s at T_sph| / observed, and its sign. Also compute the B - L freeze of the dimension-five neutrino-mass
    operator (order of magnitude, sum m_nu^2 >= 2.5e-3 eV^2 from oscillations, PROVISIONAL) as the comparison T_D.
  - **GD3 line:** FAIL if X > 10 (the equilibrium bias alone overshoots the observed asymmetry by more than a factor
    10) or if the sign is opposite to the one GD2 needs for rho_K > 0 and it is not overcome. A rescue that cancels the
    bias with a separate B - L source counts as one new fitted constant tuned to 1/X; if X > 10 it is a FAIL as frozen
    (fine tuning beyond 10 %), and is reported.
- **GD4 energy bookkeeping and back-reaction.** Derive the minisuperspace Hamiltonian with baryon number X as a
  variable: clock energy E(X) at fixed p and dE/dX. Report the energy per created baryon and its source. Q stays near 1
  iff Q - 1 <= 0.01 at T_sph and at T_D; give the mu_K that needs (record lines: mu_K >= 198.25/Mpc form B, CLS1;
  >= 2.512e4 CMB lensing; >= 8.89e6 BBN, KD1). Stability: PASS iff no new negative-energy direction is added by the term
  (it is linear in tau-dot, so it cannot change the quadratic kinetic matrix; checked). Vacuum: report whether
  |eps| exceeds the lightest B-violating final-state threshold (pbar e+, 0.9388 GeV); if so the vacuum is
  energetically unstable to B violation, rate set by the B-violating operator (reported; graded only through GD5's
  proton line).
- **GD5 visible today?** Show (sympy, Dirac field, flat and with an arbitrary vierbein-independent scalar phase) that
  psi -> exp(-i eps B tau) psi removes the term from every B-conserving term. Line: if removable, no fifth force or EP
  signal from B-conserving physics; Kostelecky-Tasson a_mu bounds (Rev. Mod. Phys. 83, 11 (2011), data tables arXiv
  0801.0287; PROVISIONAL) then do not apply to a pure gradient common to p and n. Proton: the term adds |eps| to the
  energy release of a Delta B = -1 decay (eps < 0); with a dimension-six operator the rate scales roughly as E^5, so the
  Super-K line tau(p -> e+ pi0) > 2.4e34 yr (PROVISIONAL) moves the operator scale by (E'/m_p)^(5/4); reported, not
  graded (the SM alone has no T = 0 B violation beyond exp(-4 pi / alpha_W)).
- **GD6 cold, separate, adiabatic.** With J_B conserved after T_sph the term is a total derivative (GD1), so the
  component is decoupled from the photon-baryon fluid: PASS iff GD1's identity holds. Isocurvature: with a local
  neutral start, rho_K / n_B = -eps everywhere, so S = 0 between the component and baryons iff the baryon asymmetry is
  itself adiabatic (stated, argued; no perturbation solve).
- **GD7 rules and prior art.** State how the term breaks "matter couples to the metric only" (it couples matter to
  d tau) and that it adds no particle. Literature look-ups (abstracts only, PROVISIONAL): Cohen and Kaplan 1987;
  Carroll and Shu 2006; Davoudiasl et al. 2004; ghost condensate (Arkani-Hamed et al. 2004) and khronon / mimetic
  baryogenesis (arXiv:1710.03945). Question: has anyone tied a dust-like field's amount to baryon number this way.
  Not graded.

## 4. Label rule (per footing)

- GD3 or GD4 (Q - 1 <= 0.01 cannot be met by any mu_K in the record's allowed range and the action) FAIL -> EXCLUDED
  (name the bound and factor), unless the equations are inconsistent -> NOT WELL-DEFINED.
- All gates pass, eps fixed by GD2's natural-normalisation test -> FIXES. All pass, eps fitted -> TRADES (1 new
  constant, eps; plus the inflation premise stated).
- A deciding gate not evaluable even crudely -> NO VERDICT.

## 5. Known-answer checks and mutations

- KA1 (GD1): eps = 0 reproduces R541 part B's p_tau = a^3 mu_K^2 (Q-1)/K exactly.
- KA2 (GD3): with mu_B = 0 and B - L given, the equilibrium code reproduces Harvey-Turner's B = (28/79)(B - L).
- KA3 (GD3): numerical Fermi-Dirac integral reproduces n - nbar = g mu T^2 / 6 at mu/T = 1e-3 (rel. 1e-5).
- KA4 (GD4): the BBN stiff line reproduces KD1's mu_K >= 8.89e6 Mpc^-1 at T = 0.1 MeV.
- KA5 (GD2): the record's I0 = 4.037e-8 Mpc^-2 from omega_d 0.1209, h 0.674 (3 H0^2 Omega_d).
- KA6 (GD5): the rephasing identity's residual is 0; a non-gradient a_mu (curl != 0) leaves a residual (sanity).
- MU1 (GD2): flip the sign of eps -> rho_K flips sign; double R -> eps doubles.
- MU2 (GD3): eps -> eps x 1e-7 must move X below 10 (the gate must be able to pass); T_sph -> 1e9 GeV must move X by
  the factor T ratio.
- MU3 (GD4): mu_K -> mu_K / 10 must raise Q - 1 by 100.

Scripts print to committed .out files; relative paths only; nothing beyond seconds of compute.

# AG6C FROZEN CRITERIA: a relativistic completion of PAPER49's static action

Written 2026-10-20 and committed ALONE, before any script in this folder exists or any number is computed.
Lane folder: `argon_push/AG6C_relativistic_completion/`. Settings: kappa = 1/2 FITTED; both a0 footings (canonical
9.3603e-11, alt 1.1312e-10 m/s^2, as CFG770) on every dimensional number, never pooled; cold energy's mass required; no
dark-matter particle species is added (the medium is a continuum: a fluid plus a gauge field); not "theory closed".
Small jobs only (OMP_NUM_THREADS=1, nice -n 10, < 1 GB, minutes). No downloads. Web facts are PROVISIONAL.

## 0. The target (PAPER49, DOI 10.5281/zenodo.23501949)

L49 = -|grad Phi - K P|^2/(2K) - rho_b Phi - W_rem(u) - (gamma/2)|grad P|^2, K = 4 pi G, u = K|P|,
K dW_rem/du = R(u) = u^2/(a0 - u), W_full = W_rem + u^2/(2K) (K dW_full/du = a0 u/(a0 - u)), gamma = K L*^2/2,
L* in [24 pc, ~1 kpc]. PAPER49 reads P as the displacement of a real medium: d_t P = -j, div P = rho_c - rhobar.

Prior record that this lane must not re-run (cited, not repeated): PAPER9 foliation theorem (one metric + exactly two modes
=> preferred frame); L61 excess-spent-once (hatch = MOND emergent from a dark sector); L67 superfluid DM dead at lensing
(M_dyn/M_lens >= 5); L68 dipolar DM (Blanchet & Le Tiec) passes lensing but dies in its internal sector (free monopole
G_eff = G/eps); CFG663 (non-lensing response EXCLUDED on raw KiDS); CFG665 (photon-only coupling excluded; shared metric
=> zero GW-light delay); single-metric pincer DC-013/DC-019; v9 AeST PPN kill; PAPER33 v2 khronon-dust closed by KiDS;
CFG770 (Cassini Q2 of L49 itself, PASS at 3.5e-6 of the ceiling at L* = 5.75 pc); CFG691/CFG820 (L* window);
AG6D (longitudinal stiffness = Gamma = 2 polytrope of cold energy).

## 1. Candidate covariant actions (chosen before computing)

**C1 (primary): "dielectric cold dust" (DCD).** One metric, Einstein-Hilbert, all matter minimally coupled:

S = Int d^4x sqrt(-g) [ c^4 R/(16 pi G) + L_b(baryons, g) + L_cold + L_dark ],

- L_cold: a cold fluid (Schutz/Brown conserved-current form), rest-mass density rho >= 0, four-velocity u^mu, conserved
  J^mu = rho u^mu, internal energy density e_int = (gamma/2) rho^2 (an n = 1 polytrope: p = gamma rho^2/2,
  c_s^2 = gamma rho), carrying a charge under a massless dark U(1): coupling -q J^mu A_mu with q fixed so that, in the
  normalisation L_dark -> X/K at small X, the coupling is unit (the BPS / extremal ratio q = sqrt(G) m in Gaussian-type
  units: like elements' dark repulsion cancels their gravity exactly).
- L_dark = (a0^2/K) sgn(X) [ s - ln(1 + s) ], s = sqrt(2|X|)/a0, X = -(1/4) F_{mu nu} F^{mu nu} (field in acceleration
  units). Small X: Maxwell + cubic. Chosen because it is the Legendre dual of W_full (check S0.1).
- Baryons carry no dark charge; the visible photon does not couple to the dark U(1) (no kinetic mixing).
- Cosmic dark-charge neutrality (rhobar) needs a uniform non-clustering neutralising background. It is NOT constructed in
  this lane; static checks are run for an isolated system (rhobar -> 0) and with a uniform rigid background (rhobar > 0).
- Free constants: a0 (dark saturation field), gamma (L*), and the charge ratio (= BPS exactly; tolerance computed in S0.5).

**C2 (comparison): the Blanchet-Le Tiec dipolar fluid** with W = W_full: sqrt(-g)[-sigma c^2 + J_mu Dxi^mu/dtau -
W(Pi_perp)] (literature form recalled from memory: PROVISIONAL). L68 already closed it in its internal sector; here ONLY
its kinetic structure is checked (H5).

**C3 (considered, not run):** cold medium + a separate anchor continuum, tether on the relative displacement. Its static
limit equals L49 only as the anchor's rigidity -> infinity (acausal). Recorded as an open alternative, no verdict.

Modified-gravity completions (TeVeS, AeST, khronon/Einstein-aether, BIMOND, superfluid DM) are covered by the record above
and are not re-run.

## 2. Gate S0: does C1's static weak-field limit equal L49?

- **S0.1 (sympy, exact):** L_dark(E) = (a0^2/K)[e - ln(1+e)] (e = E/a0) has D = dL/dE = a0 E/(a0 + E) and
  E D - L_dark = W_full(D) identically. PASS iff both identities simplify to 0.
- **S0.2 (sympy, exact):** C1's static equations (Poisson grad^2 Phi = K(rho_b + rho_c - rhobar); Gauss div D =
  K(rho_c - rhobar); dust at rest: grad Phi = E_vec - gamma grad rho_c; E curl-free; D = D(|E|) E/|E|) map onto L49's
  Euler-Lagrange equations with P = D/K. At gamma = 0: identical in every geometry (pointwise algebra: E(D(E)) = E and
  K dW_full/du at u = K|P| equals |grad Phi|; divergence equation identical). PASS iff exact.
- **S0.3 (sympy, exact):** stiffness. For radial P = q(r) r_hat, the EL operator of (gamma/2)(div P)^2 equals that of
  (gamma/2)|grad P|^2 identically. PASS iff exact. For one non-radial test field the two differ (reported: C1 does NOT
  reproduce the curl part of L49's stiffness; the Solar-System consequence is decided by gate iii, not assumed).
- **S0.4 (numeric, PAPER49's own static solution):** positivity domain. Solve L49 at gamma = 0 (AQUAL, simple mu; deep-MOND
  limit mu = g/a0 near the saddle, one full-mu cross-check) for two equal point masses, axisymmetric. Report
  C = min[grad^2 Phi_tilde]/(4 pi) in units where rho_ph = C sqrt(G M a0)/(G d^2), and for fiducials
  F1 (MW-M31-like: 8e10 Msun each, d = 0.77 Mpc) and F2 (cluster pair: 2e13 Msun each, d = 5 Mpc), min(rho_ph)/rhobar_c with
  rhobar_c = 5.364 Omega_b rho_crit, Omega_b h^2 = 0.0224 (BBN range 0.0217-0.0229 reported), both footings.
  Outcome rule: if min rho_ph < -rhobar_c for F1 or F2 => NEGATIVE DOMAIN EXISTS: no medium with rho >= 0 (weak energy
  condition) can reproduce L49 there (class-level SCOPED NO-GO on exactness in that domain, and the clipping is the first
  new prediction, quantified as the mid-plane column Sigma_ph through the saddle in Msun/pc^2). Otherwise exact everywhere.
  Controls: single mass -> min rho_ph > 0 and |grad Phi_tilde| = 1/r_tilde within 1% for 0.2 < r_tilde < 5.
  MUTATE: Newtonian mu = 1 -> rho_ph == 0, so the negative-domain flag must vanish.
- **S0.5 (numeric):** BPS tolerance. With charge ratio q^2 = 1 + delta, R(u) -> R(u) + delta u. Report the largest |delta|
  that keeps nu(y) within 1% of the law at y = 1e-4 and at y = 6e-4 (KiDS isolated-lens floor), and the sign rule
  (delta < 0 => long-wavelength Jeans-class instability, H4 MUTATE c).
- S0 MUTATE (must bite): delta = 0.01 => S0.2 fails at small y; pairing L49's completed square with W_full instead of W_rem
  (the PAPER49 double count) => S0.1/S0.2 fail.

## 3. The four gates for C1

**(i) Lensing = dynamics.**
- L1 (structure): one metric, GR; static spherical: lensing mass m(r) from T_00, dynamical mass
  M_dyn = m + 4 pi r^3 p_r/c^2 (TOV); M_lens = (m + M_dyn)/2.
- L2 (numeric): law halos (point masses 1e8, 1e10, 1e12, 1e14 Msun; r from r_M/100 to 100 r_M), T_munu = dust + n = 1
  pressure (L* = 1 kpc, the window top) + NLED stress (T_00 = E D - L, T_rr = L - E D, T_thth = L, all /K). PASS iff
  max |M_dyn/M_lens - 1| <= 1e-3 (the measured SPARC-KiDS ratio is 1.02; L67/CFG663) on both footings.
- MUTATE (must bite): drop rho_c from T_00 (a non-lensing response) => max |M_dyn/M_lens - 1| > 0.5.

**(ii) GW speed.**
- G1 (sympy): the second-order expansion of sqrt(-g)[L_dark + L_cold] in a TT perturbation h on a flat background with a
  uniform dark field contains no derivative of h, so the principal symbol of h is Einstein-Hilbert's: c_T = c exactly;
  report the matter "mass" correction |delta c/c| ~ 4 pi G rho/omega^2 at 100 Hz for rho = 1e-20 kg/m^3. PASS iff no
  derivative terms and |delta c/c| <= 1e-15 (GW170817).
- G2: light is on the same metric cone (no dark coupling) => zero GW-light delay (CFG665's shared-metric certificate).
- MUTATE (must bite): identify the visible photon with the dark U(1) (light gets C1's birefringence): delay over the Milky
  Way halo alone (30 kpc at e = 1) must exceed 1.7 s.

**(iii) Solar System with the stiffness.**
- P1 (structure): gravitational action = Einstein-Hilbert and baryons are dark-neutral => PPN beta = gamma = 1,
  alpha_1,2,3 = xi = zeta_i = 0; non-GR effects only through the cold medium's Newtonian potential.
- P2 (numeric, apples-to-apples with CFG770): re-implement CFG770's Fourier linear response. Control K: with L49's
  response m_i = (A_i + s)/(A_i + 1 + s) the script must reproduce cfg770_results.json T1 (Q2) and T3 (1 AU pull, Saturn
  monopole) to <= 1e-6 relative. Then C1's response (stiffness on div P only; deficit 1 - S = E_k/(1 + s E_k),
  E_k = sum khat_i^2/(1 + A_i)). Same ceilings as CFG770: |Q2| < 5.2e-27 s^-2 (Park+2026 2 sigma), sunward pull at
  1 AU < 3.66e-14 m/s^2, Saturn monopole < 6.7e-11 Msun; 3 Galactic fields (2.00, 2.32, 2.64e-10) x 2 footings, at
  L* = 5.75 pc (CFG770's point) and 24 pc. PASS iff all ratios < 1 at 24 pc.
- MUTATE (must bite): L* = 1e-4 pc => T3 fails.

**(iv) Health across 1e-4 to 1e4 a0 (static backgrounds; e = E/a0 = g/a0 at equilibrium).**
- H1 (sympy): kinetic positivity: dust rho > 0; L_X = 1/(K(1+s)) > 0 on both branches; graviton GR.
- H2 (sympy): hyperbolicity: L_X + 2 X L_XX = 1/(K(1+s)^2) > 0 on both branches.
- H3 (numeric): NLED plane-wave dispersion on 2000 random (E, B) backgrounds, |E|, |B| in [1e-4, 1e4] a0 (log), random
  angles: all omega real, max |Im omega|/|omega| <= 1e-8. Pure electric: extraordinary v^2 = 1 + e to 1e-8.
- H4 (numeric): coupled dust + NLED + Newtonian gravity, linear, WKB about a static uniform background: e on 81 log points
  in [1e-4, 1e4], angle k-E on 13 points, k c/omega_p on 37 log points in [1e-3, 1e6], c_s/c in {1e-7, 1e-4}. PASS iff
  max Re(lambda)/max(|lambda|, omega_p) <= 1e-7 everywhere (no ghost, no gradient instability, no Jeans-class growth).
- Definitions: ghost = a non-positive kinetic eigenvalue; gradient instability = a growth rate that rises without bound
  with k; Jeans-class = growth bounded by sqrt(K rho), confined to small k (reported, not a health failure if physical).
- H4 MUTATEs (each must be flagged): (a) wrong-sign dark kinetic term (L_X < 0); (b) NLED L = X - X^2/b^2 beyond
  X = b^2/6 (L_X + 2X L_XX < 0); (c) subcritical charge q^2 = 0.99 (must show bounded Jeans-class growth at small k in
  deep MOND, not gradient-class); (d) rho < 0 (must show gradient-class growth).
- H5 (sympy, C2 only): kinetic Hessian and Hamiltonian of the NR reduction of C2's coupling J_mu Dxi^mu/dtau. FAIL for C2
  iff the Hamiltonian is linear in a momentum (unbounded below).
- H6 (sympy): L49 read literally as a medium with inertia rho_c = rhobar + div P: dispersion omega^2 = rho_c x (positive
  restoring). If S0.4 finds rho_c < 0, that domain is gradient-unstable (growth ~ k): recorded as a finding about L49
  read as a real medium, not as a C1 failure.
- Causality (reported, not one of the four gates): criterion A (all cones inside the light cone) and the owner's
  criterion B (a global time compatible with every cone; checked as sqrt(1 + e) v_bulk/c < 1 for e in {1, 10, 1e2, 1e3,
  1e4} and v_bulk in {300, 1000, 3000} km/s).

## 4. Verdict rule (frozen)

- **COMPLETION FOUND**: S0.1-S0.3 PASS, gates (i)-(iv) PASS for C1, and a first new prediction is quantified. Any S0.4
  negative domain is then stated as a forced, class-level scoped no-go on exactness (and supplies the prediction); the
  curl-part stiffness difference (S0.3) and the unconstructed neutralising background must be stated with the verdict.
- **PARTIAL**: C1 fails at least one of (i)-(iv) or S0.1/S0.2; list which pass.
- **SCOPED NO-GO**: a class-level theorem shows that no candidate in a stated class can pass.
- **NOT DIAGNOSTIC**: a check cannot be run or decided as frozen (e.g. a control fails).
- Every MUTATE above must bite; if one does not, its gate is reported NOT DIAGNOSTIC.

## 5. Design-stage expectations (disclosed, from reasoning before any script)

I expect: S0.1/S0.2 exact; S0.3 exact for radial fields only; L2 ~ 1e-6; c_T = c; Q2 within an O(1) factor of CFG770;
H1-H4 clean; a superluminal extraordinary dark-photon mode (v^2 = 1 + e, criterion A fails); C2's Hamiltonian linear in a
momentum; a negative-phantom domain near the saddle (Milgrom 1986). These are predictions of the checks, not results.

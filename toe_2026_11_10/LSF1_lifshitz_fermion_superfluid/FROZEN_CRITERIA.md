# LSF1: a Lifshitz fermion superfluid as the law's microscopic origin? (2026-11-10)

TEST lane, quarantined: adopts nothing, relabels nothing, registers nothing. Committed alone, before any script or number
of this lane. Owner decision `toe_2026_11_10/OWNER_DECISION_2026-11-10_LSF1_RULE_LIFT.md` (origin 2e4c9e9b4b): for this
lane only, the no-particle rule is lifted (one hidden fermion species, named here as **a dark component carried by a
particle**) and the metric-only rule is lifted (baryons may couple directly to the superfluid's phase). Outside this lane
the cold component is cold dark energy. A pass would be a rival candidate to form B, not its completion. Footings
canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s^2, never pooled. Not a LCDM lane. No data download. Literature
lookups PROVISIONAL (primary arXiv ids). Id check: no `LSF1` folder existed; `git log --grep=LSF1` finds only the owner
decision ee6da8be39.

## R. What the record already has (quoted, not re-graded)

- **NPJ1 a1** (`toe_2026_11_10/NPJ1_nonperturbative_J/RESULT.md`, origin f3e403091b): the BK superfluid "**PASS** 0.0946,
  0.956 | -32.0; -32.0 (Lambda 0.12-5.2 meV) | -57 (local) | **FAIL**: |psi|^6 dim -4 at z = 2; |grad theta|^3
  inserted | SHAPE ONLY". "BK's pass is narrow: 0.0946 at x = 9.8 [...] with a0'/a0 = 0.42." a0' = alpha^3 Lambda^2 /
  (8 pi M_Pl).
- **CFG117** (Verlinde, the additive form): "the linear sum g = g_N + sqrt(a_V g_N)" against the target's quadrature
  sum; "H1 fails in all 16 cases". NPJ1: "The two tests differ; both results stand."
- **ROOT note** (`toe_2026_11_10/ROOT_note/NOTE.md`): any deep-MOND law forces J = u^2/2 - u^3/3 - ...; "MOND cannot be
  a fundamental term in a TOE. It has to be emergent".
- **QX28** (`closure_2026_11_06/QX28_superfluid_two_phase/README.md`, BK class): "FAILS at G3, G4, G5, G6 and G8, on both
  footings"; clusters: "The measured clusters sit between the two phases"; G6a "w(1089) 3e4 / 2e4"; G8 "The static
  phonon field is AQUAL-type with this law, so AX1's grade applies". Implied BK constants m 0.57 / 0.55 eV, Lambda
  0.11 / 0.15 meV, alpha 3.5 / 3.0; K_min 1.585e-6 / 1.0e-6 (km/s)^2 kpc^6 Msun^-2.
- **CFG122** (door 4, BK EFT): "G5.1: FAIL. For X < 0, P_XX < 0 and c_s^2 = 2X/m < 0 (elliptic [...])"; "G5.4 Solar
  System: FAIL [...] Reading B (BK unscreened): 10.9 / 12.0 x the Cassini bound, 3e6 x MICROSCOPE, 6e8 x the ephemeris
  ceiling"; "the 1 AU gradient term is 1e5-1e15 x the ambient m V^2, so it is unscreened". **CFG154** (referee):
  "CFG122's 31.62 is reproduced exactly".
- **HF1** (`rebuild_2026_10_22/HF1_hybrid_fermion/README.md`) and the 2026-11-02 owner decision ("Scope: lane HF1 only"):
  "FAILS GATE 1 AT 5 OF 6 m, 1 UNDETERMINED". **HC1** (`closure_2026_11_06/HC1_hot_fermion_all_gates/RESULT.md`):
  "blocks on 7 of 9 gates"; "The Tremaine-Gunn cap binds in every SPARC galaxy". **EW4**: Tremaine-Gunn rho_max =
  m^4 (g/2h^3)(2 pi sigma^2)^(3/2).
- **Forest** (`rebuild_2026_10_22/REQUIREMENTS_2026-11-01/FOREST_KILL_AUDIT.md`): "KILL NOT ON THE CURRENT FOOTING, NOT
  OVERTURNED"; the record line is "undecided on raw forest data; a 1-D proxy against a ΛCDM yardstick falls 1000–5000 ×
  short". This lane never quotes "5-11 eV dies on the forest" flat.
- **Literature, PROVISIONAL.** BK arXiv:1507.01019: P(X) = (2 Lambda (2m)^(3/2)/3) X sqrt|X|; the MOND regime is on
  X < 0, where the phonon kinetic term has the wrong sign (their section 4.1); proposed fixes: an M^2 Y^2 operator or a
  finite-temperature P(X, T) stable for beta >= 3/2 (4.2); near the Sun the flow exceeds a critical velocity and the
  condensate loses coherence (section 5). Sharma-Khoury-Lubensky arXiv:1809.08286: the three-body EOS and a wrong-sign
  problem of its phonon Lagrangian. Berezhiani-Famaey-Khoury arXiv:1711.05748 (phenomenology).

## 0. The candidate (frozen)

A hidden spin-1/2 fermion psi with dispersion eps(k) defined in the clock's frame, a weak attractive s-wave contact that
pairs it (pair field Delta e^(i theta), theta the pair phase), and the baryon-phase coupling, frozen as BK's form:

    L_int = - alpha Lambda theta rho_b / M_Pl,   rho_b = m_N n_B  (it couples to baryon NUMBER).

Static phase-field Lagrangian at fixed local chemical potential mu_eff = mu - mu_vac - m Phi: L(mu_eff, q) = -Omega,
the T = 0 grand potential density of the paired gas with a uniform phase twist q per fermion (pair momentum 2q,
grad theta = 2q). mu_vac is the vacuum threshold (0 without a two-body bound state, -E_b/2 with one). E_q = eps(q) -
eps(0) is the pair's centre-of-mass kinetic energy per fermion (q^2/2m in the Galilean case: BK's X = mu_eff - E_q).
"Gradient-dominated" (BK's MOND regime) means E_q >= 10 |mu_eff|.

Natural units hbar = c = 1 in the microscopic part; SI in E and D. M_Pl = 1.2209e19 GeV (unreduced, NPJ1's).

## 1. Branches scanned (frozen list)

Units per branch: energies in |mu_eff|, the dispersion's coefficient set to 1.
- **D1** 3-d Galilean eps = k^2 (1/2m = 1). Control: BK's own kinematics. Coupling by the scattering length:
  weak 1/a = -1.5, strong 1/a = +1.5 (BEC).
- **D2** 3-d Lifshitz eps = k^6. The candidate. Contact g: weak (Delta(q = 0) = 0.05 at mu_eff = 1), strong
  (two-body binding E_b = 10).
- **D3** 3-d crossover eps = k^2 + k^6 (k_x = 1). Same couplings as D2; mu_eff scanned over 1e-3 ... 1e3 for the
  formal reading.
- **D4** quasi-1-d anisotropic eps = k_x^2 + 2t(2 - cos k_y - cos k_z), t = 1e-3 (transverse bandwidth 8t << mu_eff):
  twist along x and along y.
- **D5** an isotropic tangle of 1-d Galilean channels (fermions on randomly oriented strings): eps = k_par^2 per
  channel, L averaged over channel orientation.

## 2. Gates

**(G0) gradient structure: run first, graded on the MICROSCOPIC free energy.** For each branch, coupling (weak, strong)
and sign of mu_eff (+1, -1): Omega(mu, q) in BCS mean field with single-plane-wave pairing at momentum 2q (Fulde-
Ferrell), the gap minimized over Delta in {0} and a grid up to 4x its q = 0 value (finite-Delta states included), and
the depaired quasiparticles (E +- xi_A < 0) occupied. Window: 16 log-spaced q in [q_a, 10 q_a] with E_{q_a} = 10|mu_eff|.
Delta L(q) = L(mu, q) - L(mu, 0).
- PASS in that cell iff Delta L < 0 at every q (energy cost, the MOND sign), |Delta L| grows across the window, and the
  least-squares slope d ln|Delta L| / d ln q is in [2.9, 3.1]. Delta L identically 0 is FAIL (no gradient energy).
- A branch passes G0 iff some (coupling, sign) cell passes AND the window exists and passes in every direction of q
  (D4: x and y; D1-D3, D5 isotropic by construction).
- Reported per branch: the full curve Delta L(q) from q = 0, the superfluid stiffness at small q, the depairing q, the
  condensation energy, and the bound |Delta L| <= E_cond.

**Reading F (BK's formal continuation; REPORTED, never the lane label).** Each branch's weak-pairing EOS P_0(mu) (the
free Fermi sea) with BK's odd extension P_odd(X) = sign(X) P_0(|X|) and X = mu_eff - E_q: L_F = P_odd(mu_eff - E_q) -
P_odd(mu_eff); the same window test (slope in [2.9, 3.1], cost sign, isotropy). Also stated: the dimensional rule
(gradient-dominated L proportional to q^(d+z) for eps proportional to k^z in d dimensions with no other scale),
solved with P_0 proportional to mu^(3/2).

**(S) shape** (NPJ1's definition). The point-mass force law of L = -C|grad theta|^p - L_int: a = a_N + a_theta,
a_theta = (a_*^(p-2) a_N)^(1/(p-1)), p the branch's exponent in the reading graded (micro: no gradient energy, so
a_theta = 0 and mu = 1). One fitted parameter log10(a_*/a0) in [-3, 3] (scipy differential_evolution, seed 0). PASS
iff max |mu - x/(1+x)| <= 0.1 on 41 log-spaced x in [0.01, 100] and the deep slope d ln mu / d ln x at x = 0.01 is
within 0.1 of 0.990.

**(C) size and locality** (NPJ1's definition, rule H = HZ1's ceiling: N <= 1000, |g| <= 4 pi, every dimensionful input
<= M_Pl). C-amp: the inputs the S fit needs (alpha, Lambda_eff and the branch's microscopic constants), minimized over
the free ones, against the ceiling. C-loc (condensate): every microscopic length (Fermi wavelength, channel spacing for
D5) <= r(0.01) of QG1's 6e10 Msun point mass. Rule W (holographic count + species cutoff, an ASSUMPTION) reported only.

**(U) action.** (U1) every contact of the sector power-counting renormalizable at its own (d, z): an n-body contact
(psi^dag psi)^n has coupling dimension z + d - n d; PASS iff the pairing (n = 2) and every contact the EOS needs are
>= 0 and nothing non-polynomial is inserted (the EOS from Fermi statistics is not an insertion). (U2) the
baryon-phase coupling, graded in the UV fields: PASS iff it is a polynomial in (psi, baryon fields) with coefficient
dimension >= 0 at the sector's z. theta is the phase of psi_down psi_up, so a term linear in theta is not a polynomial
in psi: the frozen L_int FAILS U2 unless the script finds otherwise. The polynomial alternative
-lambda n_B (psi_down psi_up + h.c.) is reported: its dimension, and the static source it gives (sympy). U passes iff
U1 and U2 pass.

**(E) equivalence principle and fifth force** (inputs PROVISIONAL, the record's CFG122 values): MICROSCOPE |eta| <=
1e-15 (Touboul+ arXiv:2209.15487), eta = Delta(B/mu)_{48Ti-195Pt} a_theta/g at 710 km; Cassini |gamma - 1| <= 2.3e-5
(Bertotti+ 2003) in the record's convention |gamma - 1| = 2 eps/(1 + eps), eps = a_theta/g_sun at 1 AU; ephemeris
ceiling: sunward anomaly <= 1.27e-5 a0. a_theta from the S fit, per footing. Two readings: F (unscreened continuation,
a_theta = sqrt(a0' g)) and micro (a_theta = 0 wherever the gradient dominates: the superfluid's own screening, the
depairing computed in G0). E passes in a reading iff all three bounds hold there. Mass coupling (eta = 0 at MICROSCOPE)
reported.

**(D) the particle's own bounds** (reported items, each flagged excluded / not excluded):
- D1 Pauli / Tremaine-Gunn with the actual dispersion: the superflow speed |grad theta|/(2 m_f) and the Fermi
  velocity at the density the branch's MOND regime needs at r(1) of the reference galaxy, against its escape speed
  (2 v_f); the m_f range that passes. Excluded iff no m_f <= M_Pl passes.
- D2 forest: the record's caveat quoted; never a flag.
- D3 clusters (BK's normal phase): QX28's class result inherited (G4, G5 FAIL); flagged "excluded (inherited)" for any
  branch in the BK class.
- D4 can the superfluid be the CMB's cold component (5.41 rho_b)? The P proportional to rho^3 EOS (any branch with
  P_0 proportional to mu^(3/2)) with K from galaxies (QX28's K_min, quoted input): w(1089) and the stiff kinetic share
  at z = 1089 and at BBN against radiation. "Must sit beside" iff w(1089) > 0.01. Reported, not a flag.

## 3. Labels

Per branch, on each footing (G0 and S are footing-independent; C, E, D are not):
- **CANDIDATE PASSES:** G0, S, C, U, E pass and no D item is excluded.
- **SHAPE ONLY:** G0 and S pass, the line above does not.
- **NONE:** G0 passes, S fails.
- **KILLED AT G0:** G0 fails.
Lane label = the best branch's label among those whose U1 passes (renormalizable dispersions); **KILLED AT G0** iff no
renormalizable branch passes G0. D1 (U1 fails) is graded as the control only. Reading F labels are computed the same way
with G0F in place of G0 and are reported, never the lane label. **OPEN** if a known answer fails or a numerical step
fails (non-converged minimization, grid check off by more than 1e-3 relative).

## 4. Known answers (all must pass before any graded line is read)

- KA1 3-d free Fermi gas at z = 2: P = (2m)^(3/2) mu^(5/2)/(15 pi^2) (spin 1/2), quadrature 1e-8.
- KA2 3-d eps = c k^z: P = [z/(z+3)] mu^((z+3)/z)/(3 pi^2 c^(3/z)); at z = 6 the exponent 3/2 and the coefficient
  2/(9 pi^2), quadrature 1e-8. KA2b: 1-d Galilean P = (4/(3 pi)) sqrt(2m) mu^(3/2).
- KA3 BK's static phonon equation: Euler-Lagrange of L = -(2 Lambda/3)|theta'|^3 - alpha Lambda theta rho_b/M_Pl on a
  point mass gives a_theta = sqrt(a0' a_N), a0' = alpha^3 Lambda^2/(8 pi M_Pl) (sympy, independent of NPJ1's code);
  and the MOND limit of P(X) = (2 Lambda (2m)^(3/2)/3) X|X|^(1/2) at |X| ~ (grad theta)^2/2m is -(2 Lambda/3)|grad
  theta|^3.
- KA4 Lifshitz power counting: n-body contact dimension z + d - n d: (d, z) = (3, 2) gives -1 and -4 (NPJ1's -4);
  (3, 6) gives +3 and 0 (the lead's seed). And the pairing integral's UV behaviour: Int d^3k/eps(k) converges for
  z = 6 and diverges linearly for z = 2 (numeric cutoff scan).
- KA5 textbook BCS gap: 3-d Galilean mean field at mu = eps_F, 1/(k_F a) = -2: Delta/eps_F = (8/e^2)
  exp(-pi/(2 k_F |a|)) to 1e-2.
- KA6 Galilean invariance of the FF mean field: for D1 below depairing, Omega(mu, q; Delta) = Omega(mu - q^2/2m, 0;
  Delta) to 1e-6 relative.
- KA7 Delta = 0: Omega(mu, q; 0) = Omega_normal(mu) independent of q (grid, 1e-4 relative).
- KA8 the pair-kinetic inequality eps_S(k; q) >= eps(k) + eps(q) for eps = k^6 and k^2 + k^6 (equality for k^2),
  eps_S the symmetric part (sympy). It implies the pair band at momentum 2q lies at least 2 E_q above the q = 0 pair
  band.
- KA9 two-body binding for eps = k^6 in 3-d: Int d^3k/(2 eps + E_b) diverges as E_b^(-1/2) (bound state for any
  attraction), numeric slope -0.5 to 1e-2.
- KA10 convexity: free-gas P_0''(mu) >= 0; BK's P''(X) < 0 for X < 0 (sympy).

## 5. MUTATE twins (`LSF1_MUTATE=1`; each must bite)

- M1 G0 detector: BK's formal P(X) = X|X|^(1/2) with Galilean kinematics fed to the G0 window test must PASS.
- M2 S detector: p = 3 must PASS S (NPJ1's 0.0946 reproduced to 1e-3); p = 9 must FAIL.
- M3 U1 counter: (d, z) = (3, 2) three-body must read -4 (FAIL); (1, 2) and (3, 6) two-body must read +1, +3 (PASS).
- M4 E: alpha -> 0 (a_theta -> 0) must PASS E; the formal BK force must FAIL it.
- M5 KA6 twin: the Galilean-invariance identity applied to eps = k^6 must FAIL (it is Galilean-specific).
- M6 convexity detector: the odd-extended EOS on X < 0 must read unstable; the free-gas EOS stable.
- M7 micro twin: the D2 micro run with the depairing terms removed and Delta held at its q = 0 value (a superfluid
  forbidden to depair) must give a growing |Delta L| (the saturation is the depairing).

Lean (optional): `LSF1.lean`, the dimensional rule (d + z = 3 and 2(d + z) = 3z force (d, z) = (1, 2)); false twin
`LSF1_MUTATE.lean` claiming (3, 6) satisfies d + z = 3.

## 6. Reported, not graded

- R1 BK's Solar-System argument (supercritical flow near the Sun) against the G0 result: the criterion E_q > mu_eff is
  the gradient-dominated condition itself.
- R2 what an effectively 1-d dispersion means physically (D4, D5): channel density, spacing and tension needed.
- R3 the k^6 scale M_6 (eps = k^6/M_6^5) that reproduces BK's EOS amplitude at QX28's implied (m, Lambda).
- R4 kappa and 5.41: does anything fix them?
- R5 strong pairing: what the BEC side changes (pair dispersion, EOS).

## 7. Hand expectations (written before any number)

**The lead's** (from the brief, unverified): KILLED AT G0 for pure k^6 (gradients give |q|^9); the k^2 + k^6 mix
picks one branch; only an effectively 1-d dispersion does both, exotically; overall KILLED AT G0, or SHAPE ONLY via the
1-d branch.

**Mine.** Reading F: the dimensional rule gives L proportional to q^(d+z), so q^3 with P_0 proportional to mu^(3/2)
needs (d, z) = (1, 2): k^6 gives q^9 (the lead is right), D1 q^5, D3 between 5 and 9 (never 3), D4 q^3 along x but
bounded along y (anisotropic), D5 q^3 isotropic. So under F only the tangle passes G0F and S (BK's 0.0946), C passes, U2
fails (theta is not polynomial in psi) and E fails unscreened: SHAPE ONLY under F. **Microscopically I expect every
branch to fail G0 for a reason that has nothing to do with z:** BK's MOND branch sits at X < 0, where the paired gas is
empty or depaired (KA8: the pair band at twist q lies above the chemical potential once E_q > mu_eff), so the gradient
energy saturates at the condensation energy (slope 0), and BK's X|X|^(1/2) continuation has negative compressibility
there (KA10; CFG122's c_s^2 < 0). Lane label: **KILLED AT G0**.

kappa = 1/2 FITTED; not theory closed.

# CFG121 (Door 3 of the ten doors): dipolar dark matter / gravitational polarisation -- FROZEN CRITERIA

Written 2026-09-29, PHASE 1, before any script, number or plot for this door exists. Nothing was run. Every numerical
statement below that is not a quotation from a committed README is a HAND estimate made while writing this file; it is
an expectation to be confirmed or refuted by the scripts, not a result. A refutation of one of my own expectations is a
kept result. kappa = 1/2 is FITTED. Nothing here says the theory is closed, and nothing here says the data favour the
framework. A scoped no-go is a valid outcome of this door.

Files read for this file (and only these): closure_map/TEN_DOORS_GATES_2026-09-29.md, GAPS_1_2_JOINT_STATUS.md,
ACTIONS_AND_NOGOS.md, and the READMEs of CFG43, CFG44, CFG48, CFG50, CFG60 (its .md), CFG70, CFG72. The Blanchet-Le Tiec
literature is NOT in that list; every statement about it below is from memory and is marked RECALLED. The tests do not
depend on any RECALLED statement: they run on the explicit Newtonian action written in section 2.

---------------------------------------------------------------------------------------------------------------------

## 0. Declaration (a): the menu was written knowing the target

The ten-doors menu (TEN_DOORS_GATES_2026-09-29.md) was written after CFG44 fixed the target
C(r) = rho_c r^3 g_tot = (a0/4pi) M_b(<r), and the door "the dark density is the divergence of a polarisation" was chosen
BECAUSE the law's phantom density is already a divergence (section 2, item P). A pass of this door on the point-mass
target is therefore an identity, not evidence for a mechanism, and I will label it a positive control. Only a pass that
survives the extended baryons, the mass range, the cosmology gates and the constants count (G4) would say anything, and
even then it would say "a construction exists", not "the data favour it".

## 1. The frozen question

Q. Can the component that supplies the CFG44 target (cold, conserved, Omega_c h^2 = 0.12, collisionless, plain CDM
through recombination and linear growth) be, or be supplied through, a gravitational-polarisation medium whose bound
charge density -div(Pi), with Pi = chi(g) g and ONE polarisation law chi, reproduces
C(r) = (a0/4pi) M_b(<r) for a point mass and for CFG44's exponential sphere, at 1e9..1e12 Msun, with no constant beyond
kappa and Omega_c h^2, without a ghost or gradient instability, and with the reaction on the baryons and the energy
supply inside CFG48/CFG70's pass lines?

Three sub-questions, kept separate so that an identity is not mistaken for a mechanism:
- QA (kinematic): is the target a bound charge of SOME polarisation, and of a single-valued chi(g_b)?
- QB (category): can a bound charge BE the cold conserved component (a fluid with mass, velocity, dispersion)?
- QC (medium): if a real polarisable medium (mass density rho_D, the Omega_c component) carries the polarisation, what
  does its own mass, stiffness and dipole size do to G1, G2, G3, G4?

## 2. The model (b), exactly as it will be tested

### P. The phenomenological polarisation formulation (Bekenstein-Milgrom / Milgrom / Blanchet 2007 language)

Conventions: g = -grad Phi (points inward), g_N the Newtonian field of the baryons, g_tot = nu(|g_N|/a0) g_N (QUMOND) or
the AQUAL field (identical in spherical symmetry). Phantom density: rho_ph = -div[(nu - 1) g_N]/(4piG). Hence

    rho_ph = -div Pi,      Pi = (nu(|g_N|/a0) - 1) g_N /(4piG)  =  chi(g_b) g_b,      4piG chi(g_b) = nu(g_b/a0) - 1,

with g_b = g_N the baryons' field. In a spherical system Pi is radial and inward, M_pol(<r) = 4pi r^2 |Pi(r)|,
rho_pol = M_pol'/(4pi r^2), and |Pi| = (nu - 1) g_b/(4piG) = M_ph(<r)/(4pi r^2) EXACTLY. The dielectric dictionary:
permittivity eps_g = 1 - 4piG chi = 1/nu = mu. So in this reading "the phantom density is a polarisation divergence"
is not a hypothesis; it is the QUMOND/AQUAL definition rewritten. It carries no mass, no velocity, no dispersion: it is
the law, not a fluid. Its only new content is the shape of chi and the saturation |Pi| <= a0/(8piG) in the Newtonian
regime (for the P2 kernel nu = sqrt(1 + a0/g): Pi -> a0/(8piG) from below).

Consequence stated up front (theorem, to be verified symbolically in Q1): a bound charge has zero net charge for a
bounded polarisation and zero cosmic mean for a homogeneous isotropic one (a homogeneous vector field vanishes by
isotropy, so <rho_pol> = 0). It therefore cannot supply Omega_c h^2 = 0.12 at z ~ 1100. Whatever supplies the cosmic
cold density is a REAL medium. This is why question QB is a category question and why the door needs the medium of D.

### D. The medium: dipolar dark matter (Blanchet-Le Tiec type). Two variants are tested, named V_U and V_B.

Declared Newtonian action (c -> infinity; written by me; the mapping to the relativistic Blanchet-Le Tiec action is NOT
claimed, see section 5):

    L = rho_b v_b^2/2 + rho_D v_D^2/2 - (rho_b + rho_D) Phi - |grad Phi|^2/(8piG)
        + Pi . g_pol  +  kappa_I |D_t Pi|^2 /(2 Q^2 rho_D)  -  W(|Pi|^2),

- rho_D: the medium's mass density (real, gravitating, conserved, pressureless; the Omega_c component; velocity v_D).
- Pi: the polarisation (dipole moment per volume), Pi = Q rho_D xi with xi the dipole displacement per dipolar particle.
- Q: the dipole's gravitational-charge-to-mass ratio. **Declared Q = 1** (no new constant). Any pass that needs Q != 1
  is a G4 failure. kappa_I: internal inertia ratio, **declared kappa_I = 1**, same rule.
- W(|Pi|^2): the internal potential; its shape is determined by the law (the Legendre transform of the kernel), so it
  adds no free function beyond the kernel choice: static equilibrium g_pol = 2 W'(|Pi|^2) Pi, with g = G(|Pi|) meaning
  the total field as a function of |Pi|.
- V_U (universal, Blanchet-Le Tiec-like, RECALLED): g_pol = g = -grad Phi (the dipoles respond to the TOTAL field of
  baryons + medium + bound charge). Poisson: lap Phi = 4piG (rho_b + rho_D - div Pi). Consequence: the medium's own mass is
  a polarising source.
- V_B (the door's title: "P = chi(g_b) g_b", sourced by the baryonic field): g_pol = g_b = -grad Phi_b with Phi_b a
  baryon-only auxiliary potential (multiplier lambda (lap Phi_b - 4piG rho_b)/4piG), lap Phi = 4piG(rho_b + rho_D). The
  bound charge reaches the baryons through the multiplier's reaction (a_react = -grad lambda, the bound charge's field),
  and does NOT act on the medium mass. This is the CFG50 auxiliary-potential structure with the tidal coupling replaced by
  the vector coupling Pi . g_b, and it is the kernel-visible-to-baryons / medium-sees-Newtonian structure of V0 and FL1.
  Ownership by the baryons' field is built in (candidate for Gap 1, tested in section 3.O).

Static equilibrium of the dipoles (spherical, adiabatic limit): Pi = Pi_eq(g_N) = (nu - 1) g_N/(4piG). Stability of the
equilibrium under the coupled (Pi, Poisson) system (hand derivation, to be verified): the longitudinal frequency is

    omega^2 = (Q^2/kappa_I) rho_D [ dg/dPi - 4piG ] = (Q^2/kappa_I) 4piG rho_D / h'(g_N),   h(g_N) = 4piG |Pi_eq|,

so the equilibrium is a stable minimum iff d|Pi_eq|/dg_N > 0 for all g_N, i.e. iff the bound charge (nu - 1) g_N does
not DECREASE with the field. The P2 kernel (nu - 1 -> a0/(2g)) saturates from below and passes; kernels whose nu - 1 falls
faster than a0/g at strong field (the "standard" family, steep exponentials) do not. Whether the committed nu_mono does is
read from CFG4's canon at phase 2, not assumed here.

### Facts about Blanchet-Le Tiec type models (all RECALLED, unverified; the data chat's literature status should confirm
### before the result is read; none is used by a test)
1. Blanchet 2007 (CQG 24, 3529) proposed MOND phenomenology as gravitational polarisation of a dark medium; Blanchet-Le
   Tiec 2008 (PRD 78, 024031) gave a Lagrangian with a dipole-moment field, an internal force from a potential W of the
   polarisation, and a relativistic completion; 2009 (PRD 80, 023524) treated cosmology and claimed CDM-like large-scale
   behaviour with a cosmological-constant-like piece of W, i.e. an a0-Lambda link inside W.
2. The medium's rest-mass density is a new cosmological density (the dark matter), and the polarisation-induced density
   is additional; the equilibrium polarisation in a bound system is set by the field, so it tracks the baryons.
3. Blanchet-Heisenberg (2015) embedded dipolar dark matter in bigravity (relevant only to the untested relativistic
   sector).
4. The orchestrator cites Bruneton-Liberati-Sotiriou-Sarkar (2009) and Bruneton-Esposito-Farese(-Kaloper) type work as
   stability / well-posedness criticisms of polarisation fluids and of relativistic MOND-like fields. I have not read
   them. The frozen G5 tests below are the Newtonian-sector ones I can write from the declared action; the relativistic
   criticisms are NOT tested and are listed in section 5.

## 3. Where this door sits relative to what is already excluded (do not repeat)

| prior lane (hypothesis) | is Door 3 inside it? |
|---|---|
| CFG44 B2 universal barotropic P(rho), fixed-kernel second force linear in M_b | NO. No stress closure is used; the polarisation is a nonlinear (sqrt-type) function of M_b. |
| CFG44 B3 local closures, far-shell theorem, adiabatic maintenance | PARTLY. Those are about the fluid's PRESSURE. Door 3 supplies DENSITY through a local law of g_b and rho_b (section 3.G1, T1.4: rho_pol contains a local rho_b term that the target does not); the far-shell theorem does not bind a density. |
| CFG44 B4 Q2 Lagrange constraint, Q2b density-slaved fluid | NO for the pure phantom (nothing is slaved by an added energy). V_U/V_B's medium is a real fluid with universal or baryon-only coupling. |
| CFG44 B4 Q3 fluid feels the law's phantom potential (N11/N13; reaction 0.11-1.5 g_law) | V_U: the medium mass feels the total Phi, the same one the baryons feel, so no EXTRA reaction arises; the medium mass instead double counts. V_B: this IS the L353/V0 structure (medium sees Newtonian only). |
| CFG44 B4 Q4 additive law (phantom + cosmic-share cold fluid): +0.43 dex at x = 3, +0.68 dex at x = 1 | YES for any variant with a real medium mass comparable to the cosmic share. This door's medium is exactly such an additional component; test B2/B3 below quantify how much medium mass the polarisation itself REQUIRES. |
| CFG44 B4 Q5 temperature-slaved fluid (BTFR postulated), locally virialised fluid | NO. Door 3 postulates nothing about the medium's dispersion; it removes the dispersion requirement for the polarised part (bound charge has none) and pays for it in QB. |
| CFG50 tidal-tensor closure (auxiliary baryon-sourced Phi_b, reciprocity O(g_law), dipole-ghost kinetic matrix [[0, D],[D, 0]], 0.5 g_tot ghost-free ceiling) | V_B is in the same construction family (auxiliary Phi_b with multiplier) with a different coupling (Pi . g_b, not T_ij Pi^ij). CFG50's numbers do NOT transfer (different coupling); its structural warning (the (Phi_b, lambda) kinetic matrix is a dipole-ghost structure, relativistic completion OPEN) is tested for V_B in S2 and S5. |
| CFG48 G1 Gauss (gate on a shift-symmetric field: M_dyn = M_b beyond the edge, negative shell) | YES, in a neutral-charge form: a BOUNDED polarised medium has total bound charge zero, so its polarisation cannot carry mass beyond its own edge (test G3-edge). |
| CFG48 G2/G3 ownership as a state functional or history variable | Door 3's "ownership" is an instantaneous local response (external-field-effect type) plus one dynamical dof (Pi) with a relaxation time; tested in O1. |
| CFG48 G4, CFG70, CFG72 (exchange action, memory kernel, light cone: reaction 0.06-22 g_law, energy 23-318x) | NO as constructed: Door 3 has no enclosed-mass exchange kernel and no target thermal store. Its static limit is the law itself (reaction = 0 by construction for the pure phantom) and its energy is a REVERSIBLE polarisation store. What the CFG70 result DOES say (memory does not help) is not re-tested. CFG72's stability finding for a bath-slaved fluid does not apply. |
| CFG60 (no committed construction derives the dispersion: D = 0, P = 11, I = 5, X = 27, U = 11) | Door 3 would be class D only for the polarised fraction, and only if QB is answered by a bound charge that is a cold fluid; my expectation (section 8) is that it lands in P/X for the medium fraction. |
| CFG43 saturating barotropic cap (new nu*, window ~11x up to 1e4-1e5 in mass vs 1e4 needed; obstruction does not touch non-barotropic or order-parameter fluids) | The dipolar medium is an order-parameter fluid (Pi is a second variable), i.e. inside the class CFG43 says it does not touch. Its analogue of the cap is |Pi| <= a0/(8piG); the tie of that scale to Lambda is tested in G4-tie. |

So the honest scope: Door 3 is new relative to CFG44/48/50/60/70/72 in that it supplies DENSITY through a bound charge
rather than through a fluid closure. That makes the dispersion problem disappear for the bound-charge part; the price,
which the tests below price, is QB (the category), the medium's own budget, cosmology, and constants.

## 4. Common definitions, units, grids (all tests)

- a0 = 9.3603e-11 m/s^2 canonical (kappa = 1/2, Omega_Lambda = 0.6847); every gate result is also printed at the second
  footing 1.1312e-10. Both are reported; neither is preferred. G = 6.6743e-11, Msun = 1.98841e30 kg.
- r_M = sqrt(G M_b / a0), x = r/r_M, V_f^4 = G M_b a0, reference orbital energy E_orb = (1/2) M_b V_f^2.
- Target (CFG44 B1): rho_c g_tot = a0 M_b(<r)/(4pi r^3). For extended profiles M_c is the solution of the ODE
  (M_b + M_c) dM_c/dr = (a0/G) r M_b, M_c(0) = 0 (obtained from rho_c = a0 M_b/(4pi G r (M_b + M_c))). The point mass
  gives (M + M_c)^2 = M^2 (1 + x^2). The exponential-sphere family is imported READ-ONLY from CFG44's Bcommon
  (same scale-length law); if it cannot be imported the script stops (exit 2) rather than re-typing a family.
- Model observable: C_model(r) = rho_dark,model(r) r^3 g_model(r), with the model's own g_model = G(M_b + M_dark,model)/r^2;
  reference C_tgt(r) = (a0/4pi) M_b(<r). rho_dark,model = rho_pol (pure phantom), rho_D + rho_pol (V_U, V_B with a medium).
- Masses (gate): M_b in {1e9, 1e10, 1e11, 1e12} Msun. Robustness sweep: half-decades 3e9, 3e10, 3e11. x grid: 121
  log-spaced points on [0.1, 30]. r_ta: BOTH conventions, imported read-only (CFG48's Gcommon convention and CFG4's committed
  law-phantom-inclusive r_ta, 1.7-3.6x larger); the edge is r_e = 0.4 r_ta in each (CFG48 README).
- Kernels: P2 nu = sqrt(1 + a0/g) (the kernel for which the target is exact); nu_mono imported from CFG4's canon (never
  re-typed); "simple" and "standard" closed forms as controls for S1 only.
- Integrity checks (a failing one aborts with exit 2): reproduce CFG44's point-mass M_c to 1e-9 and its extended-profile
  M_c to 1e-6; sympy check of M_pol = 4 pi r^2 |Pi| and of rho_pol = M_pol'/(4 pi r^2).
- No knob is scanned to fit anything. Where a parameter is scanned (Q, kappa_I, eps_c, f_track) it is a declared sensitivity
  grid to find where a pass would live, and the grid and its outcome are both reported; a pass that lives only at
  Q != 1 or kappa_I != 1 is a G4 failure by rule.

## 5. Tests (c), each with a numeric pass line

Verdict vocabulary per test: PASS, FAIL, IDENTITY (true by construction, reported as a positive control, not counted
toward the door), UNDECIDED (only where a scope limit says so; never used to soften a FAIL).

### G1 -- the target (shared line: within 10% of C_tgt on x in [0.1, 30], 1e9..1e12 Msun, SAME constants)

- T1.1 (IDENTITY, positive control). Point mass: solve M_pol(<r) = M_c(<r) for the required law. Expected and to be
  verified exactly: 4 pi G chi_req(g_b) = sqrt(1 + a0/g_b) - 1 (the P2 kernel is DERIVED from the target, no fit);
  limits: deep 4piG chi = sqrt(a0/g_b), strong field |Pi| -> a0/(8piG). Check that -div(chi g_b) reproduces rho_tgt.
  Pass line: max |C_model/C_tgt - 1| <= 1e-9 (analytic derivative), <= 1e-4 (finite differences). Reported as IDENTITY.
- T1.2 (the real G1 test). Exponential spheres at the four masses with the T1.1 chi (P2), NO refit, g_b(r) = G M_b(<r)/r^2.
  Pass line: max over x in [0.1, 30] of |C_model/C_tgt - 1| <= 0.10 at EVERY mass. Also reported (not gating): the
  enclosed-mass ratio M_pol(<r)/M_c(<r), the rotation-curve offset Delta log10 g, and the sign of rho_pol (must be >= 0
  everywhere for the door to speak of a cold-fluid density; min rho_pol < 0 anywhere is a FAIL of the identification).
- T1.3 (does ANY single function work). One free-form monotone chi(g_b) on a 12-knot log grid in g_b/a0 in [1e-3, 1e3]
  (monotone cubic Hermite), fitted by a declared minimax of |log(C_model/C_tgt)| over all masses and x; a 6-knot
  version as robustness. Pass line: 10% at every mass and x. This is a diagnostic of whether the obstruction is a
  functional-form one; if only a free-form chi passes and P2 does not, G4 is a FAIL (the shape is new information).
- T1.4 (analytic obstruction, the "linear-response" statement). For spherical M_b(r) and Pi = chi(g_b) g_b, sympy:
      rho_pol = (2/r)[ chi g_b - (chi g_b)_g g_b ] + 4 pi G rho_b (chi g_b)_g ,
  a function of (g_b, r) plus a term proportional to the LOCAL baryon density rho_b, whereas the target depends only on
  M_b(<r) and through the ODE on the whole interior history. (a) Outside the baryons the difference is the constant
  D(r_b) = integral of M_b' (2 M_c - a0 r^2/G) dr (hand derivation of dD/dr = M_b'(2M_c - a0 r^2/G)); evaluate it.
  (b) Profile degeneracy: profiles with the same M_b(<r_test) and the same g_b(r_test) (point mass, uniform sphere of
  radius r_test/2, thin shell at r_test/2, exponential with h = r_test/3) give the SAME M_pol(r_test) and different target
  M_c(r_test); report the spread at x_test in {0.3, 1, 3, 10, 30}. Pass line for "a local chi(g_b) is not excluded on the
  class of all spherical profiles": every pair within 10%. Scope: spherical, static, target as defined by the ODE.
- T1.5 (kernel). Repeat T1.2 with nu_mono. CFG44 (referee correction) gives a point-mass charge function
  R(x = 1) = 1.46 for nu_mono (P2: R = 1), up to 2.5 on extended profiles. Pass line: 10%. Expected FAIL with the
  committed nu_mono; it is a kernel-shape fact, orthogonal to Door 3, reported so that nobody mistakes the P2 identity for
  a statement about the canonical kernel. (CFG14: P2 is disfavoured by SPARC at p ~ 0.03; a door whose G1 passes only for
  P2 inherits that.)
- T1.6 (mass independence). With one chi (no per-mass refit) report the per-mass max error of T1.2 and its trend with
  M_b / the ratio of baryon scale length to r_M. "Same constants at every mass" holds by construction (chi has only a0);
  the gate is the per-mass error.

### QB -- category tests (the identification "the cold conserved component IS the bound charge")

- Q1 (theorems, sympy, no numeric line; each is a verdict of the identification). (i) A homogeneous isotropic Pi vanishes,
  so <rho_pol> = 0 and no Omega_c h^2 = 0.12 at any z. (ii) For a bounded polarisation, integral rho_pol = surface flux = 0
  (a finite medium carries no net bound charge), for the P2 halo M_pol(<r) grows ~ r with no finite total. (iii) The bound
  charge is slaved to the local field Pi = Pi_eq(g_b(x, t)); it has no independent velocity or dispersion, follows the
  baryons instead of being collisionless (a merger consequence, NOT tested numerically here; the record's merger lanes
  L370-L372 and the T4/T5 "real cold mass" requirement are the reason candidate B uses a real fluid). Verdict rule: the
  identification is FAIL if any of (i)-(iii) holds, which I expect (section 8, H5').
- Q2 (relaxation). Report omega(x)/Omega_orb(x) and tau = 1/omega against the dynamical time and 1/H0, for the declared
  Q = kappa_I = 1 and medium density rho_D = rho_tgt (the largest medium the target allows) and rho_D = the cosmic mean
  (Omega_c rho_crit) times the contrast implied by a 200 overdensity.

### G1c (door-specific gate, may not weaken the shared gates): the medium is self-consistent

Definitions. Continuum consistency: the dipole displacement is smaller than the length over which Pi varies,
|Pi| <= eps_c Q rho_D r with eps_c = 1 central (0.3 and 3 as sensitivity). Adiabatic tracking: omega >= f_track Omega_orb,
f_track = 1 central (0.3, 3, 10 as sensitivity), omega^2 = (Q^2/kappa_I) 4piG rho_D / h'(g_N).

- B1 (budget). F_req(x) = M_c(<r) / (4 pi eps_c Q r^3 rho_tgt(r)) is the minimum medium density as a fraction of the
  target density. F_allow = 0.10 (G1 line). Pass: F_req <= F_allow at every x in [0.3, 30]. Report Q* = the Q that would
  make it pass at eps_c = 1 (a new constant if != 1).
- B2 (V_U pincer, exact). With the medium a polarising source and the P2 law, the dark mass is
  nu(g_N,b+D)(M_b + M_D) - M_b; solve for F_allow_U(x) = the largest M_D/M_c(<r) for which the TOTAL dark mass stays within
  10% of the target, and compare with F_req. Pass: F_req <= F_allow_U at every x.
- B3 (tracking). rho_track(x) from omega >= f_track Omega_orb; report the minimum Q^2/kappa_I for rho_track <= F_allow rho_tgt.
- B4 (maximal polarised share). phi_max(x) = the largest fraction of the enclosed target that ANY medium of charge Q and
  size eps_c can carry as bound charge when rho_D + rho_pol = rho_tgt and |Pi| <= eps_c Q rho_D r: the solution of
  M_pol' = 4 pi r^2 rho_tgt - M_pol/(eps_c Q r). Report as a function of x and Q. The remainder 1 - phi_max must be supplied by
  a real cold fluid with its own closure, i.e. it is Gap 2 relocated, not solved (CFG60 class P).
- Door verdict G1c: PASS only if B1, B2 and B3 all pass at Q = kappa_I = 1 and eps_c <= 1, f_track >= 1.

### G2 -- CMB and linear growth (shared: within 5% of LCDM growth to k = 30/Mpc at z >~ 10; no change to CMB lensing and TT/TE/EE)

Perturbation equations to be written in the script docstring and committed with its first output, BEFORE the solver's
first run: sub-horizon Newtonian, background LCDM (h = 0.6736, Omega_c h^2 = 0.12, Omega_b h^2 = 0.0224). Unknowns:
delta_b, delta_D (pressureless, conserved, comoving), Pi (or xi) obeying the declared equation Pi'' + 2H Pi' (expansion
friction from the D_t of a physical vector; derived in the docstring) = (Q^2 rho_D/kappa_I)[g_pol - G(|Pi|) Pi_hat]
with the Poisson constraint of V_U or V_B.

- C1 (planar solver). 1D plane-symmetric periodic box, N >= 512 cells per wavelength, Lagrangian coordinates for baryons and
  medium; converged to 1% under N -> 2N and dt -> dt/2. Modes k in {0.5, 2, 10, 30}/Mpc (also reported as h/Mpc;
  CFG43 referee note: factor ~0.55). Initial amplitude A in {1e-4, 1e-3, 1e-2} times the LCDM linear delta at z = 100.
  Because the equilibrium polarisation ~ sqrt(g) is nonlinear at small amplitude, all three amplitudes are gating.
  Pass: |D_model(z=10)/D_LCDM(z=10) - 1| <= 0.05 for every k and every amplitude, for BOTH parameter sets
  (P_central: Q = kappa_I = 1; P_star: the Q*, kappa_I from B1-B3). Both must pass for the door to pass G2.
- C2 (CMB). At z = 1100, k in [1e-3, 1]/Mpc: delta_eff/delta_D within 5% of 1 and effective sound speed c_eff^2 <= 1e-6
  (a declared generous CMB-level line; the record's GDM line for a fluid is c_s^2 <= 3e-16, printed alongside). The
  lensing and TT/TE/EE constraints are NOT run through a Boltzmann code in this door; an effective-fluid pass is
  necessary, not sufficient. State this in the output.
- C3 (regime map). Print omega^2/H^2 as a function of (z, delta, Q^2/kappa_I) separating the adiabatic (equilibrium) regime
  from the free-dipole regime; report which regime each gate line sits in.

### G3 -- reciprocity and energy (shared: reaction <= 0.10 g_law over x in [0.3, 30]; energy <= baryons' orbital energy, BOTH r_ta conventions)

- E1 (reaction). |g_model - g_tgt| / g_tgt over x in [0.3, 30], defined as the excess force on the baryons relative to the
  target law, for (i) the pure phantom (expected ~0, IDENTITY) and (ii) V_U and V_B carrying the medium mass that G1c
  requires (rho_D = F_req rho_tgt at the smallest Q that passes B1, and at Q = 1). Pass: <= 0.10 at every x.
- E2 (Noether). Discrete-action check on a small system (baryon point mass + N medium dipoles + Poisson): total momentum
  conserved to 1e-12; the force on the baryons equals minus the force on (medium + bound charge); state the reaction on the
  baryons as the field of the bound charge and compare with the law. MUTATE breaks the reciprocity of the coupling.
- E3 (energy). E_int = integral over r <= r_e of w(|Pi|) 4 pi r^2 dr, w = integral_0^{|Pi|} g d|Pi|' (stored polarisation
  energy), the primary measure; E_net = the on-shell energy including the field energy, reported. Pass: E_int <= E_orb in both
  r_ta conventions at 1e9, 1e10, 1e12 Msun. This is a reversible store, not an unfunded reservoir; the shared line is
  applied as written (conservative) and the difference is stated in the output.
- G3-edge (Gauss, neutral charge). If the medium is finite (radius R_D) the bound charge integrates to zero, so beyond R_D
  the dynamical mass is M_b + M_D. Report the negative shell (phi_max M_c(R_D)) for R_D = 0.4 r_ta in both conventions and
  compare with CFG48's negative-shell figures (3e11-1.4e13 Msun). If the medium fills space (R_D -> infinity) report the
  external-field boundary condition used (an EFE-type background polarisation) and its own cost.

### G4 -- constants (shared: none beyond kappa and Omega_c h^2; a0's tie to Lambda is CFG43's P_cap = (kappa^2/8pi) rho_Lambda c^2 or a stated equivalent)

Scripted table: every constant with value, status (tied / fitted / new), and the test that needs it: kappa (fitted), Omega_c h^2
(fitted), Q (declared 1; new if a pass needs Q != 1), kappa_I (declared 1; new if != 1), the kernel shape (P2 derived from the
target for the point mass; a free-form chi = new information), eps_c and f_track (analysis thresholds, not theory
constants, but a pass that lives only at eps_c > 1 means a dipole larger than the region it polarises and is reported as
such). Tie test: check that the internal energy-density scale of W equals a0^2/(8piG) = P_cap up to a stated O(1) factor
(w grows only logarithmically at strong field for P2; report the coefficient); the tie is POSTULATED, as in CFG43, and is
counted PARTIAL, not derived. Pass G4: no constant beyond kappa, Omega_c h^2 at the declared Q = kappa_I = 1 with every
other gate passing.

### G5 -- well-posedness and Solar System (shared: no ghost, no gradient instability, hyperbolic/causal, Cassini-safe by explicit statement)

- S1 (kernel stability). min over g_N in [1e-4, 1e4] a0 of d|Pi_eq|/dg_N for P2, nu_mono, "simple", "standard".
  Pass: >= 0 for the kernel used in G1 (P2). Report the others; a kernel with a negative region has a negative longitudinal
  mode (omega^2 < 0 above the field where (nu - 1) g_N turns over).
- S2 (Hessian). Full second variation of the declared action about the static state for V_U and V_B on the grid g_N in
  [1e-4, 1e4] a0, k in [1e-3, 1e3]/kpc: kinetic matrix positive definite (V_U); for V_B the (Phi_b, lambda) block has
  kinetic matrix [[0, D],[D, 0]] (CFG50): report its eigenvalue signature. Pass: no negative eigenvalue of the potential
  Hessian beyond -1e-12 and a positive-definite kinetic matrix (a dipole-ghost structure is a FAIL for that variant).
- S3 (hyperbolicity). Dispersion of the linearised local system: omega^2(k) real; the polarisation modes have no gradient
  term so |d omega/dk| = 0 <= c; the medium's Jeans/CDM branch is the standard one. Pass: omega^2 >= 0 for all k, no
  superluminal group velocity. Scope: Newtonian sector only.
- S4 (Solar System). Two readings, both printed. (a) UNCAPPED: the Sun in the Galaxy's external field g_ext in {1.0, 1.9, 3.0}
  a0 with the P2 polarisation: the induced monopole renormalisation nu_eff and the anisotropic (quadrupolar) residual, and
  the anomalous acceleration at 9.5 AU (in the strong-field zone the uncapped P2 law gives a radial pull a0/2 toward the
  Sun, ~ 4.7e-11 m/s^2; only the external-field effect can remove it). (b) CAPPED by the medium's local density:
  |Pi| <= eps_c Q rho_D r with rho_D = 0.01 Msun/pc^3 at the Sun, r = 9.5 AU. Pass line (declared generous so a pass means
  little and a failure means much): capped |delta a| <= 1e-13 m/s^2; the tighter 1e-15 is printed. The ownership route
  to Cassini safety used by candidate B (CFG7, margin 2-3e4) is NOT available to Door 3 (no ownership object); the Solar
  System must be safe by the external-field effect or by the medium-density cap. Report which. If neither can be shown,
  the verdict is FAIL, not UNDECIDED.
- S5 (scope statement, no numeric line). G5 is a Newtonian-sector verdict. Relativistic completion, lensing slip and the
  internal-force sector of the relativistic action are untested (section 6).

### O -- Gap 1 side test (ownership by the baryons' field)

- O1. (i) Instantaneous locality: a satellite of baryonic mass {1e8, 1e9} Msun at 50-300 kpc from a host of {1e11, 1e12} Msun
  (host field 0.05-2 a0 at the satellite): the satellite's own bound-charge mass within 3 r_M,sat as a fraction of the isolated
  value (external-field suppression), reported next to candidate B's ownership rule qualitatively. (ii) Twin test (CFG48 G2/G3
  lesson): two systems with identical instantaneous baryon state and different histories (accreted satellite vs formed-embedded
  dwarf) have the same adiabatic polarisation; a non-adiabatic medium (omega < Omega) carries the history in Pi but
  then B1 fails by the same factor. Report tau/t_dyn(x). Pass ("ownership supplied"): exists a regime with 1 <= tau/t_dyn <= 10
  AND B1 satisfied. Expected: none.

## 6. Hypotheses TESTED and NOT TESTED (d)

TESTED (each in the sector stated): the QUMOND/AQUAL phantom as a polarisation divergence (identity); a single-valued
chi(g_b) against CFG44's point-mass and exponential-sphere target; the identification of a bound charge with the cold
conserved component (theorems); the medium's mass, dipole-size and tracking budget in a Newtonian dipolar-fluid action with
universal (V_U) and baryon-only (V_B) coupling; linear sub-horizon growth of that action (1D planar) and an effective-fluid
CMB screen; reciprocity by a discrete Noether check; the stored-energy budget in both r_ta conventions; longitudinal
stability by kernel and the Hessian of the declared action; a Newtonian Solar System estimate; instantaneous-locality
ownership.

NOT TESTED, and therefore UNDECIDED there: the relativistic completion (Blanchet-Le Tiec's relativistic action, its internal
force sector, its coupling of the dipole to the field, and the criticisms attributed to Bruneton et al.); lensing slip and
whether the bound charge is a real stress-energy source in GR (candidate B requires real mass in GR; the no-slip trilemma
N2 is not addressed); non-spherical baryons (thin discs: the tidal and enclosed-mass readings differ 3-15x in CFG44) and
the AQUAL/QUMOND curl term; the transverse (curl) polarisation modes beyond a stability count; nonlinear collapse of the
medium; merger phenomenology (Bullet-type offsets); anisotropic f(E, L) for the medium's own equilibrium; a
Boltzmann-code CMB (lensing, TT/TE/EE) beyond the effective-fluid screen; bigravity embeddings; screened or
non-universal mediators; a medium whose dipole coupling is not of the declared unit-strength form; and any
microphysical origin of W or of the saturation scale. A NO in this file is therefore scoped to the declared Newtonian
action, Q and kappa_I as declared and scanned, spherical baryons for G1, and the plane-symmetric linear solver for G2.

## 7. Controls: MUTATE (e)

Each script honours MUTATE=<mode> and writes its outputs with the mode in the file name (`*_MUTATE_<mode>.out/.json`); a
MUTATE run must exit 1 with the named claim failing and the named headline cell changed. Declared controls:

- MUTATE=sign: flip the sign of the bound-charge coupling (rho_pol = +div Pi). T1.1 must FAIL (deviation O(1) at the
  P2 kernel), the headline "IDENTITY" cell must become FAIL.
- MUTATE=Q10: Q = 10 (a G4-violating value). B1 and B3 must flip toward PASS and phi_max must rise to the closed form
  2 eps_c Q/(1 + 2 eps_c Q) (in the 1/r regime); C1 must then FAIL by a large factor. The headline G1c cell and the G2
  cell must both change. This is the control that the pincer is real and not an artefact of Q = 1.
- MUTATE=kernel: replace P2 by the "standard" kernel in S1 and T1.2. S1 must FAIL (negative d|Pi|/dg_N at strong field)
  and T1.2 must lose its identity property.
- MUTATE=nofield: drop the -4 pi G self-field term in the longitudinal stiffness (omega^2 uses dg/dPi instead of
  dg/dPi - 4piG). S1's classification of the steep kernels must change (proves the term is load-bearing).
- MUTATE=recip: make the medium-baryon coupling non-reciprocal in E2. Momentum conservation must fail.
Declared control failures are kept and disclosed. Controls that must reproduce committed numbers: CFG44's point-mass
M_c, the extended-profile ODE, and CFG44's R(x = 1) = 1.46 for nu_mono.

## 8. Expected outcome, stated honestly BEFORE running (f)

HAND estimates (not run; they can be wrong; each is a pre-declared hypothesis to be scored and kept whether right or wrong).
Confidence is my subjective probability.

- H1: T1.1 passes at machine precision (P2 derived from the target). 99%. It is an identity.
- H2: T1.2 fails the 10% line at 1e9 and 1e10 Msun at x < 3 (diffuse baryons: the difference is
  D ~ -x_b^2/4 times the profile term, small for compact 1e12 galaxies), and passes for x >= 3 at all masses. 65%. I have no
  strong prior on the size; CFG9/CFG10 say the law's phantom and the target agree within ~0.003 dex in g on SPARC, which is a
  weaker statement than agreement of the DENSITY within 10%.
- H3: T1.3 (free-form chi) does not reach 10% either. 55%.
- H4: T1.4(b) spread > 10% for at least one profile pair at x_test <= 3. 85%.
- H5: T1.5 with the committed nu_mono fails 10% (point mass R(1) = 1.46). 97%.
- H5': Q1 (i)-(iii) all hold: the identification of the bound charge with the cold conserved component FAILS by theorem.
  97%. The consequence is that the door is only ever a TWO-component statement (real medium + polarisation).
- H6: B1 fails at every x with Q = kappa_I = 1 and eps_c <= 1. 97%. Hand reason: |Pi| = M_pol/(4 pi r^2) is
  at least about rho_pol r/3 for any profile, so a continuum dipole (xi <= eps_c r) needs rho_D >= rho_pol/(3 eps_c Q),
  i.e. the medium must be at least about a third of the target density for eps_c Q = 1 (about half for a 1/r halo).
- H7: B2 fails: with the medium a polarising source the allowed medium mass in the deep regime is M_D <~ 0.2 M_b
  (hand: d(M nu)/dM ~ x/2), i.e. M_D/M_c <~ 0.2/x, against a required ~1/3: a shortfall of a factor ~15 at x = 1 and ~150 at
  x = 10. 90%. The pincer between "the medium must be at least ~ the target" and "the medium must be at most ~ 0.2/x of it"
  is what makes V_U inconsistent as an identification of the law's dark mass.
- H8: For V_B (polarisation fixed by g_b, medium additive) B1 needs eps_c Q >~ 3-5; with eps_c <= 1 that is Q* >~ 3,
  a new constant. 90%. Hand closed form for the deep regime: phi_max = 2 eps_c Q/(1 + 2 eps_c Q), i.e. 2/3 at eps_c Q = 1:
  at least a third of the target must be a real cold fluid with its own closure (Gap 2 relocated, not removed).
- H9: Tracking: rho_track/rho_tgt ~ f_track^2 kappa_I x/(2 Q^2) in the deep regime (hand). Passing at x = 30 needs
  Q^2/kappa_I >~ 150 f_track^2. 80%.
- H10: G2. In the free-dipole regime (omega << H, which is where a cosmological linear amplitude sits: omega^2/H^2 ~
  3 Omega_c (Q^2/kappa_I) sqrt(g/a0)) the bound charge modifies the source by a factor ~ 1 + 1.5 Omega_c Q^2/kappa_I (hand),
  so growth within 5% needs Q^2/kappa_I <~ 0.03, while H9 needs >~ 150: a factor ~ 5000 apart. In the adiabatic regime the
  enhancement is nu >> 1 (MOND in the linear regime). Either way I expect G2 to FAIL at P_star, and to PASS at P_central
  (Q = kappa_I = 1) only because there the polarisation is negligible and G1c fails instead. 85% for the P_star failure;
  60% for the P_central pass. This is the estimate I am least sure of (my normalisation of the dipole kinetic term is
  declared, not derived from the relativistic action).
- H11: E3: E_int/E_orb ~ (2/3) ln(x_e) ~ 2 (range 1-4) with x_e = r_e/r_M ~ 15-33 (hand: w = (4piG)^2 |Pi|^3/(3 a0) in
  the deep regime gives E = (1/3) M V_f^2 ln(r_e/r_M)). It is a reversible store, unlike CFG48's 23-318x exchange energy.
  Passing <= 1 in at least one convention: 35%.
- H12: S1: P2 passes (saturating tail), "standard" fails; nu_mono unknown until read (50/50). S2: V_U kinetic matrix positive,
  V_B carries a dipole-ghost signature [[0, D],[D, 0]]. 75%. S3 trivially PASS (no gradient terms). S4: uncapped P2 gives the
  a0/2 pull unless the external-field effect removes it (which I expect to depend on g_ext); capped reading passes the
  generous line with a very large margin (hand: |Pi| <~ 1e-9 kg/m^2 gives |delta a| <~ 1e-18 m/s^2). 90% for the capped pass.
  Note the uncomfortable structure: the Solar System is safe because the polarisation is capped by the medium density, which
  is the same fact that makes G1c fail.
- H13: O1 finds no regime supplying ownership with B1 satisfied. 90%.
- H14 (headline): Door 3 lands as a scoped NO for the missing object: the polarisation reading reproduces the law's dark
  density as an identity (and, at extended baryons, at the level H2 says), but (1) a bound charge cannot BE the cold conserved
  component (QB), (2) the real polarisable medium needed by a continuum dipole has to carry at least ~1/3 of the target itself,
  (3) that medium's mass and the pincer with G2 need a new constant (Q, kappa_I) whose two requirements are far apart, so G4
  and G2 fail, and (4) no ownership is supplied. What would survive: the pure polarisation phantom as an effective law
  (nothing new) plus a residual real fluid that still needs CFG44's closure for its own share. 85%. A pass of all of
  G1-G5: <= 3%, and if it happened I would treat it as a bug until independently re-derived (rule 5 of the shared gates).

Reporting protocol for phase 2: gates table (PASS/FAIL/IDENTITY/UNDECIDED per gate, both footings), every pre-declared
hypothesis H1-H14 scored as held / failed (kept), the MUTATE table, and a plain statement that a pass of any positive
control is not evidence. No amendment to this file except an appended, dated AMENDMENT section.

## 9. Scripts (phase 2), path-independence, outputs

Directory in the repo when committed: campaign_fresh_gravity/CFG121_dipolar_polarisation/ (the orchestrator may rename).
Path handling in every script: REPO = Path(os.environ["ZF_REPO"]) if set, else the nearest ancestor of __file__ that
contains campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py; if none is found the script prints what it needs and exits 2. No
absolute paths. CFG44 (Bcommon), CFG48 (Gcommon) and the CFG4 canon are imported READ-ONLY.

- cfg121_common.py: units, kernels, target ODE, imports, integrity checks.
- T1_required_chi_and_local_law.py: T1.1-T1.6, Q1.
- B_budget_pincer.py: Q2, B1-B4, G1c.
- C_cosmology_growth.py: C1-C3 (equations in the docstring first).
- E_reaction_energy_noether.py: E1-E3, G3-edge.
- S_stability_solar_ownership.py: S1-S4, O1, G4 table and tie.
- Each writes <name>.out and <name>_results.json; MUTATE modes write *_MUTATE_<mode>.out/.json. Exit codes: 0 = integrity
  checks passed (verdicts are results, not exit codes); 1 = a MUTATE run whose named claim failed as declared; 2 = an
  integrity check or import failed (no verdict is valid). Both a0 footings are printed in every output.

Programme rules restated: kappa = 1/2 FITTED; Z == kappa; a scoped no-go is a valid result; nothing here says the theory is
closed and nothing here says the data favour the framework; any pass on the point-mass target is an identity; the menu was
written knowing the target.

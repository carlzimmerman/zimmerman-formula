# NPJ1: a non-perturbative origin for the law's function J? (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11 m/s^2) and
alt (1.1312e-10 m/s^2), never pooled. The cold component is cold dark energy (the clock's charge), never a particle; no
dark-matter particle is introduced as the law's source. Every field below that is not in action (A) is named as NEW
(a hidden sector, not dark matter). Not a LCDM lane. No data download. Literature lookups PROVISIONAL. Committed alone,
before any script or number of this lane.

Parent: gate T3(i) of `toe_2026_11_10/TOE0_gate_battery/FROZEN_CRITERIA.md` (8a99cb7c34) and its lane HZ1
(`toe_2026_11_10/HZ1_uv_completion/`, FROZEN_CRITERIA c1bc0c0977, RESULT origin 551bc67dcd). HZ1's scope line: "A
non-perturbative origin of J (a condensate, a strongly coupled sector) is not computed and is not excluded." This lane
computes it. It tightens T3(i); nothing here loosens it. T3's label stays HZ1's FAIL whatever this lane finds; this lane
reports what a non-perturbative origin would change.

Id check: no `NPJ1` folder exists (`find . -maxdepth 3 -type d -iname '*NPJ1*'` empty); `git log --grep=NPJ1` finds the
name only in the ROOT note commit c82bf51b04, which reserves it for this lane.

## R. What the record already has (quoted, not re-graded)

- **The Bose / lattice-gas reading of W is in the record, as an identity.**
  `fable52_push/SHAPE_search/route_A_saturation_statistics.md` (label "RE-DESCRIPTION ONLY"): "J(u) is the grand
  potential of a site with no occupation limit minus that of a one-occupant site, at the same fugacity u. W(y) is the
  lattice-gas pressure minus the ideal-gas pressure, at the same filling y. [...] It is an identity. It does not say why a
  gravitational energy should be an excess pressure." Also: "In the site model the partner of the filling y is ln u, not
  u", and A2 (`deepseek_push/DS_FINAL_2026_10_21/A2_medium/report.md`): W "is conjugate to the activity, not to a
  chemical potential". The lead's form (W = ln Z of one bosonic mode minus the fugacity) is not written in the record;
  -ln(1-p) is both that and the lattice-gas pressure, so it is the same identity.
- **The other Bose reading is of the RAR kernel, and is retracted.** `RETRACTIONS.md`: "The identity nu = 1 +
  n_BE(sqrt y) is a trivial rearrangement (holds for any argument); function and thermal reading are both prior art [...]
  the natural bath normalisation predicts kappa = 0.0733 -- 11.1 sigma LOW". CFG430: "the kernel-Bose reading [...] not
  a derivation of the switch at a0". `MECHANISM_JOINT_2026-10-12.md`: "thermality sets the scale but cannot pump the sign".
- **Dipolar medium (QX29):** "W is derived by the frozen rule: spherical statics reproduce g_N = g^2/(g + a0) exactly"
  (W worked backwards from the law); the class "FAILS at G8 (Cassini) for every host rule".
- **Superfluid, BK class (QX28):** "FAILS at G3, G4, G5, G6 and G8"; "The class's static limit is AQUAL with the law's
  interpolation" (the law was an input). Bridge scout: BK is "a POSTULATED phonon P(X) and a non-Lambda a0".
- **de Sitter / Unruh:** June derivation chain: "the mechanism T_eff->m_eff is a GAP (refuted at the worldline:
  anti-MOND at every finite order); only the FORM is forced"; "kappa=1/2 is the lone free O(1)". The dS-Unruh quadrature
  gives the n = 2 law, mu = sqrt(1 + 1/(4x^2)) - 1/(2x) (route B, "DOES NOT GO THROUGH"; AG6B "n = 2 exactly"), and the
  scale 2 c H_Lambda (KAPPA_FORCING_DOOR_CLOSED). LINK5: "VERDICT = FAIL, obstruction confirmed". The sqrt(pi) wall:
  "A half-integer power of pi is provably unreachable" by pure-dS routes. "Holography reaches only the SCALE cH -- never
  the outside fraction." Verlinde (CFG117): "does not reproduce the target's shape. H1 fails in all 16 cases".
- **Walls** (`real_research/TOE_POSITS_LEDGER_2026-06.md`): W1 flavor-blindness, W2 number-field (sqrt(pi)), W3 the
  30-order scale gap; W4 kappa free.
- **3-d leaves / large N / CFT:** only HZ1 (one-loop, G1-G5). No file applies a 3-d CFT or a large-N model to the law.
  The ROOT note (c82bf51b04) proposes "a 3-d conformal sector on the clock's slices" and says kappa "would be a universal
  amplitude ratio of its fixed point".

Not re-run here: the T_eff -> m_eff inertia mechanism (Milgrom 1999), the dS-Unruh quadrature law, the RAR-kernel Bose
bath, QX28's and QX29's astrophysical gates. This lane grades only T3(i)'s question (shape, size, UV action) for sectors
stated microscopically.

## 0. Conventions (HZ1's, re-implemented independently)

Natural units hbar = c = 1, energies in eV. M_Pl = 1.2209e19 GeV (unreduced), K = 4 pi G = 4 pi/M_Pl^2. E_a0 = hbar a0/c.
Static Lagrangian density as a function of A = |A_i| (energy units): L(A) = -A^2/(2K) + (1/4K) alpha_t A^2 + L_sec(A), and
mu(A) = -(K/A) dL/dA. GR + (a0^2/K) J(A/a0) gives mu = x/(1+x), x = A/a0 (known answer KA4). For a two-field sector
(a1) mu = a_N/a from its computed force law.

Record scales, per footing, from the record's own tie at kappa = 1/2 (not pooled): rho_DE = 4 a0^2/(c^2 G),
H_Lambda = sqrt(8 pi G rho_DE/3) = sqrt(32 pi/3) a0/c, S_dS = pi M_Pl^2/(hbar H_Lambda)^2 (Gibbons-Hawking).
Reference system for locality: QG1's point mass M_b = 6e10 Msun; v_f = (G M_b a0)^(1/4). At x = A/a0 its radius is
r(x) = sqrt(G M_b (1+x)/(x^2 a0)) (from g_N = mu g). Reported only: a dwarf, M_b = 1e8 Msun; the Sun at 1 AU.

## 1. The graded tests (per candidate, per footing)

**(S) shape.** With the candidate's free parameters fitted (scipy differential_evolution, bounded, seeds fixed), PASS iff
max |mu - x/(1+x)| <= 0.1 on 41 log-spaced x in [0.01, 100] (T3(i)'s tolerance) AND the deep slope d ln mu/d ln x at
x = 0.01 is within 0.1 of the law's 0.990 (HZ1's tightening). Free parameters: the crossover scale, the amplitude, and,
where the sector sits in (A)'s own A, the tree coefficient alpha_t in [-10, 10] (as HZ1); bounds printed per candidate.

**(C) size,** two parts. C passes under a rule iff both parts pass under it.
- **C-amp:** the inputs the best fit needs (copies, densities, couplings, scales), each against the rule's bound;
  log10 R_amp = max over inputs of log10(needed/bound); pass iff <= 0. Inputs are minimized over the free couplings
  inside their bounds before the ratio is taken (most favourable reading).
- **C-loc (new; a tightening):** the law is a local function of A only if the modes that carry it are heavier than the
  inverse length over which A changes. For a sector whose law-carrying gap is set by A (gap = c_g |A|, c_g the coupling
  that multiplies A in the mass), the derivative-expansion parameter is 1/(m r). On the reference point mass,
  m(x a0) r(x) = c_g (v_f^2/c^2) sqrt(1 + x), so C-loc needs c_g >= (c^2/v_f^2)/sqrt(1 + x) at every graded x, i.e.
  c_g >= (c^2/v_f^2)/sqrt(1.01), against the rule's coupling bound 4 pi. For a sector with its own microscopic scale
  (a condensate), C-loc needs a microscopic mass m <= M_Pl whose length hbar/(m c) is <= r(0.01) (the existence of a
  natural local EFT), computed.

**Naturalness rules.**
- **Rule H (HZ1's ceiling, verbatim):** N <= 1000 species or copies; leaf density nu <= M_Pl; |g| <= 4 pi;
  T <= M_Pl; every other dimensionful input <= M_Pl.
- **Rule W (wider; an ASSUMPTION, labelled as such everywhere it is used): holographic counting, species-consistent.**
  - W-count: the sector's independent degrees of freedom in one de Sitter static patch, N_dof <= S_dS (Gibbons-Hawking
    1977; 't Hooft 1993, Susskind 1995, Bousso 2002; Banks' N-bound, hep-th/0007146; all PROVISIONAL). Counting: 4-d
    species N_dof = N; leaf fields N_dof = N nu/H_Lambda (leaves per Hubble time, at least one mode per leaf in the
    patch). This replaces N <= 1000 and nu <= M_Pl; nu may exceed M_Pl.
  - W-species: the species cutoff Lambda_sp >= hbar c/(1 kpc), the scale on which the law is used. Lambda_sp =
    M_Pl/sqrt(N) for 4-d species (Dvali arXiv:0706.2050, PROVISIONAL); Lambda_sp = M_Pl^2/(N nu) for leaf fields (the
    self-consistent count N nu/Lambda of leaves within one cutoff time; equally, the momentum where their one-loop
    graviton self-energy N nu p^3 reaches M_Pl^2 p^2). Justification: the black-hole and unitarity argument that gives
    the holographic count also gives the species bound. A count near S_dS puts the cutoff near H_Lambda/sqrt(pi), so
    a rule that admitted it unchecked would leave gravity an EFT only above the Hubble radius.
  - |g| <= 4 pi and T <= M_Pl as in H.
  - **Reported, never used for a label:** the reading under W-count alone ("W0").

**(U) action.** PASS iff the candidate's stated UV action is power-counting renormalizable under its own scaling (z = 1
relativistic 4-d, z = 2 non-relativistic, z = 3 leaf fields with HZ1's assignment [3-d Lagrangian] = 3), every coupling of
non-negative dimension, AND the law-carrying function is not inserted by hand as a non-polynomial term or coupling: HZ1's
J1/J2 detector (odd orders, orders >= 7, non-terminating) is run on any EOS, potential or coupling the candidate inserts.
A sector with no stated local action fails U.

**Labels.** Per candidate, on each footing:
- **ORIGIN FOUND:** S, C under H, U all pass.
- **ORIGIN UNDER ASSUMPTION:** S and U pass, C fails under H but passes under W.
- **SHAPE ONLY:** S passes, the two above do not.
- **NONE:** S fails.
A candidate's label is the worse of its two footings. **Lane label = the best candidate's.** **OPEN** (lane) if any known
answer fails or a numerical step fails.

## 2. Candidates (frozen list; at least one per class)

**(a) Condensates.**
- **a1 Berezhiani-Khoury superfluid** (arXiv:1507.01019, PROVISIONAL; NEW hidden-sector boson, not dark matter here: it
  is graded only as a source of the force law). Static gradient regime of P(X) proportional to X|X|^(1/2):
  L = -(2 Lambda/3)|grad theta|^3 - alpha Lambda theta rho_b/M_Pl. Point-mass solution derived in sympy; force
  a = a_N + a_theta. Fit: the crossover a0'/a0 only (amplitude and crossover are one parameter). C-amp: a0' in terms of
  (alpha, Lambda, M_Pl), computed, the needed Lambda at alpha = 4 pi against the rule. U: BK's stated microphysics, a
  three-body contact |psi|^6 (non-relativistic, z = 2).
- **a2 the exact-Legendre condensate** ((A)'s own P read as a dipole condensate; the record's QX29 W): EOS
  eps(n) = eps0[-n_hat - ln(1 - n_hat)], P(mu) = eps0[mu_hat - ln(1 + mu_hat)] with mu_hat = |A|/a0. Which P(X) maps to
  J (sympy Legendre), its k-body coefficients, S, C, U (detector on the EOS).
- **a3 the textbook condensate** (Gross-Pitaevskii + Lee-Huang-Yang; NEW hidden-sector boson) under a2's
  identification mu_hat = |A|/a0: P(mu) = mu^2/(2g) - c_L mu^(5/2), c_L from the LHY integral (KA3). S, C, U.

**(b) Strongly coupled sectors on the 3-d leaves** (large N, exact at leading order; NEW hidden-sector fields).
- **b1 large-N Gross-Neveu-Yukawa** with a dynamical mass: N flavors of 8-component fermions, mass matrix
  sigma Gamma^0 + g A_i Gamma^i (Cl(7), all anticommuting, built and checked), leading-N effective potential with the
  broken-phase gap M (the non-perturbative scale). Free energy from the exact large-N gap equation. S, C, U.
- **b2 interacting leaf pair:** HZ1's G3 with its boson made a large-N O(N) model, lambda (phi^2)^2/(8N), exact large-N
  gap equation m^2 + (lambda/8 pi) m = m0^2 + g_B^2 A^2, plus the free Cl(6) fermion (g_F, g_B = 2 g_F). Fitted with
  lambda free (lambda = 0 is G3). S, C (amp, loc), U.

**(c) Statistical and horizon sectors.**
- **c1 Bose mode, thermodynamic pairing:** n_s modes per unit volume, temperature T_s, level eps_s, with |A| entering as
  a chemical potential mu = lambda_A |A|; L_sec = n_s T_s g_1(exp((lambda_A |A| - eps_s)/T_s)) for lambda_A|A| < eps_s.
  Graded on S. With it, three identities (sympy): (i) W(p) = ln Z_BE(p) - p and W'(p) = nbar_BE(p); (ii) mu(x) =
  x/(1+x) is also the Fermi-Dirac (Langmuir) occupation at fugacity x; (iii) under the (ln z, N) pairing the Legendre
  partner of ln Z_BE is -S_BE(n) = -[(1+n)ln(1+n) - n ln n], not W.
- **c2 equilibrium bath at the local dS-Unruh temperature** T(A) = sqrt(A^2 + H_Lambda^2)/(2 pi) (Deser-Levin
  gr-qc/9706018, PROVISIONAL): N massless bosons, P = N pi^2 T^4/90; plus a detector: for any P(T) analytic in T^2 > 0,
  the series of P(T(A)) in A has no odd powers. S, C, U.
- **c3 holographic leaf sector (the lead's observation 3):** G3's fields (leaf boson m_B^2 = m0^2 + g_B^2 A^2, Cl(6)
  fermion g_F |A|, g_B = 2 g_F) with the leaf density nu free up to each rule's bound. S (own fit), C-amp under H and W,
  C-loc with c_g = g_F, U (HZ1's z = 3 counting).
- **c4 horizon degrees of freedom** (one per four Planck areas, Bekenstein-Hawking): the acceleration-dependent horizon
  r_h = 1/sqrt(A^2 + H_Lambda^2), S = pi M_Pl^2 r_h^2, T = 1/(2 pi r_h), E from dE = T dS, free energy density over the
  horizon volume; L_sec = -f. S, C, U.

## 3. Known answers (all must pass before any graded line is read)

- KA1 3-d determinant: non-analytic part of (1/2) Int d^3k/(2pi)^3 ln(k^2 + m^2) = -m^3/(12 pi) (quadrature, 1e-6).
- KA2 Bose-Einstein closed forms: sum_n p^n = 1/(1-p), nbar = p/(1-p), g_1(z) = -ln(1-z) (sympy); the 3-d ideal Bose
  gas critical density Int d^3k/(2pi)^3 [exp(k^2/(2mT)) - 1]^(-1) = zeta(3/2)(mT/2pi)^(3/2) (quadrature, 1e-8).
- KA3 LHY: Int_0^inf q^2 [sqrt(q^4 + 2q^2) - q^2 - 1 + 1/(2q^2)] dq = 8 sqrt(2)/15 (quadrature, 1e-8), i.e.
  eps = (2 pi a n^2/m)[1 + (128/(15 sqrt pi)) sqrt(n a^3)].
- KA4 Legendre: max_p [p u - W(p)] = J(u) (QX17 K0) and GR + (a0^2/K) J gives mu = x/(1+x) (sympy).
- KA5 large N: (a) O(N) gap equation, d ln m/d ln r -> 1/2 as lambda -> 0 and -> 1 as lambda -> inf (r = m0^2 + g^2A^2;
  3-d large-N nu = 1), each to 1e-3; (b) GN: per 2-component Dirac fermion the hard-cutoff determinant is
  -(Lambda_c/(2 pi^2)) m^2 + |m|^3/(6 pi) + O(1/Lambda_c) (the non-analytic coefficient 1/(6 pi) to 1e-6), and the
  Cl(7) matrices anticommute (1e-12).
- KA6 BK point mass: a_theta = sqrt(a0' a_N) exactly, a0' computed (sympy).
- KA7 the 3-d bubble Int d^3k/(2pi)^3 [k^2 (k+p)^2]^(-1) = 1/(8|p|) (quadrature, 1e-6).

## 4. MUTATE twins (must bite; `NPJ1_MUTATE=1`)

- M1 S detector: mu = x^2/(1+x^2) must FAIL S; the law itself must PASS (control).
- M2 C-amp: c3 with a0 -> M_Pl in the amplitude must pass C-amp under H (the fail is the hierarchy).
- M3 C-loc: v_f set to c/3 must pass C-loc (needed c_g = 9/sqrt(1.01) < 4 pi).
- M4 U detector: an even degree-6 polynomial EOS must read admissible.
- M5 analyticity detector: c2 with T = |A|/(2 pi) and a 3-d bath P proportional to T^3 must report an odd power.
- M6 W-species: c3 with N_dof = 1000 must pass W-species.
- M7 pairing: c1 with the field entering linearly in the fugacity (the (p, u) pairing of W) must reproduce the law
  (max dmu < 1e-6): the pairing, not the statistics, carries the law.

## 5. Reported, not graded

- R1 kappa and 5.41: does any candidate fix kappa (a0 in terms of its inputs, tied to rho_DE or not)?
- R2 consequence of C-loc for A-gapped sectors: the leaf fermion's momentum-dependent stiffness (from KA7's bubble)
  against GR's, at the reference MOND radius and at 1 AU.
- R3 the lead's three observations, each checked with numbers: (1) the BE identity; (2) J's scale a0^2/(4 pi G) =
  c^2 rho_DE/(16 pi); (3) the 10^55.4 against M_Pl/H_Lambda and against the holographic leaf density.
- R4 which record walls (W1-W4, sqrt(pi)) each candidate hits.
- R5 the dwarf (1e8 Msun) C-loc number.

## 6. Hand expectations, written before any number

The lead's (from the brief): best case ORIGIN UNDER ASSUMPTION or SHAPE ONLY; a horizon sector has no renormalizable UV
action; kappa stays free.

Mine: (S) passes only where the shape is put in (a2) or where HZ1's pair structure is kept (b2, c3); BK's additive law
a_N + sqrt(a0 a_N) misses by about 0.1; thermal and horizon sectors at T(A) are analytic in A^2 and give no |A|^3. (C)
for any sector in which A sets the gap fails C-loc under both rules: c^2/v_f^2 is about 3e6 for the reference mass, five
to six orders above 4 pi, whatever the counting rule. Under W-count alone c3's amplitude passes (the lead's observation
3, roughly), but W-species fails. (U) fails for a1 and a2. Expected lane label: SHAPE ONLY.

kappa = 1/2 FITTED; not theory closed.

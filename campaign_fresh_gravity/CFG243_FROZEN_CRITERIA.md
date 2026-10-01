# CFG243 -- a conserved dust created once, at turnaround, by a local causal source: frozen criteria (phase 1; written before any CFG243 script or number)

Lane: `campaign_fresh_gravity/CFG243_*`. To be committed as `campaign_fresh_gravity/CFG243_FROZEN_CRITERIA.md` before phase 2. All paths below are relative to the repository root (`<repo>`).

**Lineage (to be stated in the lane README).** CFG243 descends from CFG251, the owner-directed "one-time pass" door 11D lane (reading iii-a: a compaction set once at a system's first turnaround, then frozen), combined with the PAPER36 / CFG35 conservation rule (the cold component keeps its collapse mass) and CFG242 route A's persistence requirement (ownership must remember boundness; a decaying latch forgets at theta_b = 0). CFG251 found that "set at turnaround, then frozen" reproduces the ownership CLASSES but not the AMOUNT. This lane attacks that failing gate directly, and puts the cosmic amount first.

Standing statements (all binding on every sentence of phase 2): no closure is claimed; kappa = 1/2 stays FITTED; there is NO dark-matter particle and no new species. The class is a pressureless fluid created from the vacuum, and **the MASS is still required**: the gates below count it. A scoped no-go is a valid result and is not a theorem.

---

## 0. What was read, and the not-blind statement

**Read (all from the committed repository; read in full unless marked):**
- `campaign_fresh_gravity/CFG251_FROZEN_CRITERIA.md` and `CFG251_door11D_one_time_pass/README.md` (whole).
- `campaign_fresh_gravity/closure_map/TEN_DOORS_GATES_2026-09-29.md` (whole; G1-G5 are copied below), `closure_map/GAPS_1_2_JOINT_STATUS.md` (whole), `closure_map/RESEARCH_DIRECTION_2026-09-29.md` (head and the CFG243 lines).
- `campaign_fresh_gravity/CFG242_closure_swing/README.md` (bottom line, gate tables, section 4 legality outcomes, section 5.1) and `CFG242_FROZEN_CRITERIA.md` (by grep: G1-G4 lines, the L14a mechanism paragraph, the ledger and constants lines); `CFG242_A_g4_ledger.py` (head).
- `campaign_fresh_gravity/CFG230_requirements_synthesis/CFG230_README.md` (sections 1-8: R01-R12, rows, incidence).
- `campaign_fresh_gravity/CFG44_fluid_target/README.md` (the target and the exclusion table), `CFG48_gap1_switch/README.md` (bottom line, gate table, leads), `CFG70_memory_kernel_exchange/README.md` (verdict table), `CFG118_FROZEN_CRITERIA.md` and `CFG118_secondary_infall/README.md` (set-up, results, controls), `CFG35_README.md`.
- `campaign_fresh_gravity/CFG4_README.md` (by grep and the sections on the switch, the cold budget, the construction checklist; threshold values 11.81 / 8.89 / 7.09 / 5.72 and delta_lin 1.276 -> 1.076), `CFG4_cosmology.out` (head: the Planck 2018 parameters, sigma_8 = 0.8116, S8, f sigma_8 chi^2 7.31).
- `campaign_fresh_gravity/CFG131_door8_interacting_vacuum/README.md` (head: D1-D4, x* = 20.2, the "Lambda is uniform on the fluid slice" theorem) and `CFG253_dark_energy_to_cold_mass/README.md` (head and table A: the CMB-epoch cold-mass fraction).
- `fable_independent_2026/lean_2026/ChainCert/Dimension.lean` (head and theorem names) and `ChainCert/Ownership.lean` (theorem names: `ownership_distinguishes`, `ownership_not_field_local`, `owned_boost_one`).

**Not read, so every claim that depends on them is by citation at second hand:**
- There is no file named PAPER36 that I found; the rule I call "the PAPER36 conservation rule" is read from `CFG35_README.md` (its derivation is from B's conservation law once the pressureless cold fluid exists; it says nothing about how the fluid comes to exist). `STANDING_2026-09-29.md` is not read beyond the PAPER36 grep hit.
- `fable_independent_2026/L121_*.out` and `L129_*.out` (the CMB third-peak numbers are quoted as CFG251 quotes them: z_eq = 3423 with a clustering a^-3 density and 532 without; smooth dust gives peak3/peak2 = 0.5545 against 0.9906; Omega_c h^2 = 0.1200 +- 0.0012).
- CFG7 (FG001 classes), CFG50, CFG60, CFG72, CFG158, the shell code `shellcore.c`, and the rest of `closure_map/`.

**Not-blind statement.** This file was written after reading the results above. I therefore knew, before fixing any gate: CFG251's finding that the freeze reproduces the classes and not the amount (A1 15.6x short at the edge); CFG118's no-go for gravity-only evolution of a cold component set at turnaround; CFG242's route A failure; and CFG131 D4's vacuum ledger (x* = 20.2). The gates, their order and the hand estimates in section 3 were chosen with that knowledge, and the frozen predictions below are partly a restatement of what the record already implies, not independent forecasts. The "most generous reading" of the target in COSMIC is chosen so that the verdict does not depend on the target's amplitude.

**Arithmetic done in phase 1 (calculator only; no script is kept, none is a claim):** the conversions a0 -> (km/s)^2/kpc, r_M(M_b), the ratio sqrt(1+x^2) - 1, the Press-Schechter erfc values in section 3, the vacuum-ledger ratios, and the Zel'dovich threshold Dlambda = 3/4. Inputs marked "(memory)" are from memory, unverified: the sigma(M) table, the growth normalisation, the acoustic velocity amplitude, the baryon-only growth, mass fractions in the web, and the stellar-to-halo relation. Phase 2 replaces each by a computed number (CLASS 3.3.4 as in `CFG4_cosmology.py`) or by a committed function (h48's SHMR as used by CFG35), and reports the difference.

---

## 1. The model class, as equations

**Fields and symbols.** Baryons: density rho_b, 4-velocity u_b, expansion scalar theta_b = nabla_mu u_b^mu, theta_b-dot = u_b^mu nabla_mu theta_b. Dust: a pressureless collisionless multi-stream component described by a phase-space density f_c (a Vlasov book-keeping device; it introduces no particle species, mass scale or cross-section), with density rho_c = integral of f_c, conserved apart from the source. Flag n(x) in [0, 1]: a scalar advected with the baryons. Background: Planck 2018 as in `CFG4_cosmology.out` (h = 0.673317, omega_b = 0.022383, omega_cdm = 0.12011 as the COMPARISON value Omega_c h^2 = 0.1200 +- 0.0012, Omega_m = 0.3157, sigma_8 = 0.8116 from the committed run; Omega_b = 0.04937, Omega_c = 0.26494, Omega_c/Omega_b = 5.366, Omega_Lambda/Omega_b = 13.86). a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED, canonical a0 = 9.3603e-11 m/s^2 and alt 1.1312e-10 (both footings, never pooled); P2 kernel nu(y) = sqrt(1 + 1/y) primary, nu_mono reported.

**The source (the class under test).**

- Dust continuity: nabla_mu (rho_c u_c^mu) = S, with the dust created at the local baryon velocity (source term in the Vlasov equation s_c = S delta^3(p - m u_b)); after creation dust follows geodesics.
- Version U (unflagged; the literal premise): S_U = Q(L) rho_b delta(theta_b) |theta_b-dot| Theta(-theta_b-dot). Per fluid element, each downward zero crossing of theta_b deposits Q rho_b of dust (because the time integral of delta(theta_b)|theta_b-dot| over one crossing is 1).
- Version F (first crossing only; the counting rule): S_F = Q(L) rho_b (1 - n) delta(theta_b) |theta_b-dot| Theta(-theta_b-dot), with u_b^mu nabla_mu n = (1 - n) delta(theta_b) |theta_b-dot| Theta(-theta_b-dot), n = 0 initially. n is monotone and never decays, so it has perfect memory (it is a one-way switch, not the decaying latch of CFG242 route A). It is a state variable with a first-order transport equation along the baryon flow: causal, but a postulated label in the sense of CFG48 G3 (see HIERARCHY).
- The amplitude Q(L) is a dimensionless function of the LOCAL scalars L = {rho_b, theta_b-dot, shear sigma_ij, vorticity omega_ij, the electric Weyl (tidal) tensor E_ij, H} and, in the preferred-frame reading only, the local baryon peculiar acceleration g_loc relative to the cosmic frame, together with a0 (and through a0 only: kappa, c, G, rho_Lambda). By the Dimension theorem (`ChainCert.Dimension`: `sqrtM_length_iff`, `acc_unique`; monomial family and G4's constant inventory only) the variable that sets an M^(1/2) scale is an acceleration ratio, u = a0/g; the theorem fixes the VARIABLE, not the function Q(u). The function is a declared shape and is graded P-declared (as in CFG242's selectivity control) unless AMOUNT derives it.
- Support: S is supported only on the hypersurface theta_b = 0 and is zero in the unperturbed FRW flow (theta_b = 3H > 0).

**What solves for what.** Baryon flow (given, from a collapse simulation with the potential of baryons + dust + Lambda) -> theta_b, theta_b-dot, n -> S -> dust (f_c) -> its gravity -> baryon flow. The coupling is self-consistent: the dust created changes the potential that sets later turnarounds.

**Funding (ledger).** Dust rest mass comes from the vacuum. Primary reading: Lorentz-invariant vacuum T_Lambda^{mu nu} = -rho_Lambda g^{mu nu}, so nabla_mu T^{mu nu}_Lambda = -nabla^nu rho_Lambda = -S c^2 u_c^nu, i.e. the covariant exchange of CFG131 D1 (d_mu rho_L = Q u_mu). Secondary reading (labelled, never pooled): an UNFUNDED external reservoir. Door 8's untested premise (a non-Lorentz-invariant or dynamical vacuum) is not covered.

**Dust stress-energy.** T_c^{mu nu} = integral p^mu p^nu f_c dP / m: pressureless, no stress at creation, geodesic afterwards, conserved apart from S. It gravitates through GR (Newtonian limit for the toy runs). No particle is introduced. **The mass is still required**: the dust mass M_c = M_b (nu - 1) for a point mass is a created quantity that gates COSMIC and G3/G4 count; nothing here derives it.

**Constants ledger.** Allowed beyond declared function shapes: kappa = 1/2 (FITTED) and Omega_c h^2 = 0.12 (a FITTED comparison value, not an input to the source). Declared function shapes allowed: the form of Q(u), a numerical smoothing width for delta(theta_b) (a regulator, reported as such), a smoothstep only where a gate names it. Any other number in any script is a departure and is reported as one. Two items are counted as constants when used: (a) the "generous normalisation" N in COSMIC (dust per turned-around mass tuned so that Omega_dust(z = 0) = Omega_c); (b) any survival rescaling in AMOUNT (for example a factor ~0.4 from the shell-crossing radius ~0.36-0.4 r_ta, CFG4).

**The target (CFG44).** C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r); g_tot = nu(g_N/a0) g_N. Point mass, x = r/r_M, r_M = sqrt(G M_b/a0): M_c(<r) = M_b (sqrt(1 + x^2) - 1) = M_b (nu - 1). For extended baryons dM_c/dr = a0 r / (G nu) (derived from the target; hand algebra). Numbers (canonical): r_M = 1.22 / 3.86 / 12.2 / 38.6 kpc for M_b = 1e9 / 1e10 / 1e11 / 1e12 Msun (alt: 1.11 / 3.51 / 11.1 / 35.1). The ratio M_c/M_b = sqrt(1 + x^2) - 1 is 0.414 at x = 1 and 29.0 at x = 30 and is mass-independent at fixed x; at fixed physical radius it scales as M_b^(-1/2) in the deep regime; at B's density edge r_e it is 37-211 (x_e = 38 ... 212 over 1e12 ... 1e9, from CFG251 via CFG70's committed r_ta, r_e, r_M; x_e scales as M^(-0.25)).

---

## 2. The gates, their order, and the exact pass lines

**Order (part of the freeze; cheapest decisive first):** COSMIC -> G0 LEGALITY -> AMOUNT -> HIERARCHY -> G3/G4. Map to the shared gates of `closure_map/TEN_DOORS_GATES_2026-09-29.md`: COSMIC = G2's cold-early half plus CFG251's T1 timing at the CMB epoch; AMOUNT = G1; HIERARCHY = the ownership/Arm C gate (CFG48 GG, CFG251 H1-H2); G3/G4 are copied. **G5 (well-posedness) and the perturbation-level half of G2 (growth within 5% of LCDM to k = 30/Mpc, with the perturbation equations stated) are NOT in this lane's frozen order**; a pass of the five gates below would not be reported as a pass of the class until both are run (section 6).

**STOP RULE.** Stop at the FIRST binding FAIL. Report it as a scoped no-go on the frozen class with the failure NAMED. Later gates are run only as clearly labelled POST-HOC extras (scripts with `_posthoc` in the name; never part of the verdict). If every gate passes, an independent re-derivation (a separate script re-deriving the headline quantities from scratch, not importing the lane's code) is run BEFORE anything is reported.

### Gate 1 -- COSMIC (the cosmic amount; checked FIRST with numbers)

**Question.** Can a turnaround-triggered source supply the cold matter the acoustic peaks need at recombination (z ~ 1100)?

**What the CMB needs (from the committed record; second hand).** A clustering, pressureless component with Omega_c h^2 = 0.1200 +- 0.0012 at z ~ 1100 (CFG4_cosmology.out; Planck 2018). An acceleration scale cannot supply the density (L121 PEAK-2 as quoted by CFG251). Smooth dust gives peak3/peak2 = 0.5545 against 0.9906; z_eq = 3423 with it and 532 without. CFG253 (continuous transfer) requires >= 97% of today's cold mass to exist at z = 1090 at its 3% tolerance. This lane's line is looser (below).

**Declared estimator (frozen).** Spherical collapse thresholds from `CFG4_README.md` (delta_lin at turnaround: 1.276 at z = 0 -> 1.076 at z = 2.5; 1.0624 for z >= 10, the EdS value (3/5)(3 pi/4)^(2/3)). Turned-around mass fraction by Press-Schechter: F_ta(z; M > M_min) = erfc( delta_ta(z) / ( sqrt(2) sigma(M_min, z) ) ), sigma(M, z) = sigma(M, 0) D(z)/D(0), sigma(M, 0) and D(z) from CLASS 3.3.4 at the declared parameters (as `CFG4_cosmology.py`), M_min in {1e5, 1e8, 1e10} Msun (declared; the baryon filtering mass is not computed). Cosmology as in section 1.

**Most generous reading (frozen).** Normalise the source so that the dust created per turned-around mass gives Omega_dust(z = 0) = Omega_c (this removes the target's amplitude, and its mass dependence sqrt(1 + x^2) - 1, from the verdict; N is counted as a constant per section 1). Then Omega_dust h^2(z) = 0.1200 x F_ta(z)/F_ta(0). The collapse fractions use the LCDM sigma(M), which presupposes the cold matter the class does not yet have: this is circular in the class's favour and is declared as such.

**Rows.**
- C1 [BINDING LINE]: Omega_dust h^2(z = 1100) / 0.1200.
- C2: the same at z = 10 and z = 2.5 (reported, not binding).
- C3: the sigma(M, z = 0) that would be needed for F_ta(1100) = 0.5 (reported).
- C4 [self-consistent reading, reported with its own line]: the linear baryon-only rms sigma_b(M, z = 0) from a CLASS run with omega_cdm -> 0 (flat, Omega_Lambda adjusted), against delta_ta(0) = 1.276 (a trigger that never fires in the baryon-only universe).
- C5: the maximum of |delta theta_b| / (3H) over k <= 100/Mpc at z = 1100 from the CLASS transfer functions (the acoustic baryon velocity divergence against the Hubble value; the trigger needs this to reach 1). Reported.
- C6: Omega_dust(z = 0) / Omega_c from CFG4's cold budget (the record's number: Omega_ph = 0.47-0.55 at x = 1 against Omega_c = 0.265; budget edge x <= 0.46 for all of Omega_c) restated; reported only.

**PASS line (frozen).** The class must supply >= 0.5 of the Omega_c h^2 needed at z = 1100: Omega_dust h^2(1100) >= 0.5 x 0.1200 = 0.060. **FAIL** otherwise. **If the shortfall is an order of magnitude or more (Omega_dust h^2(1100) <= 0.1 x 0.060 = 0.006), that is the binding FAIL and the run STOPS.** Report exactly what dust abundance at z ~ 1100 the class supplies and the shortfall factor, with C2-C6 as context.

### Gate 2 -- G0 LEGALITY (local, causal, bound-only, counted)

**The source, written out.** S_U and S_F of section 1. Locality: S at x depends on theta_b (a first derivative of the baryon velocity), theta_b-dot, rho_b and n at x only (a finite local stencil); the flag n obeys a first-order transport equation (support in the past of x along u_b). Causality: the support of the response lies in the past light cone. Both are tested numerically, not argued.

**Toy.** CFG118-style spherical shell code (cold shells, Planck 2018 background, softened point core 10^-3 r_M and CFG44's exponential sphere), with N <= 5,000 shells per run (a resolution check at 2,000), baryon shells only for the trigger tests and the dust as an added shell family for the self-consistent runs. A fresh leapfrog is allowed; `CFG118_secondary_infall/shellcore.c` may be reused read-only.

**Rows and pass lines.**
- G0-a (locus): the first downward zero of the local theta_b = dv/dr + 2v/r of each baryon shell against that shell's own turnaround (v_r = 0). PASS iff |t_theta0 - t_ta| / t_ta <= 0.25 for >= 90% of shells (top-hat: equal exactly; a non-uniform infall profile need not be).
- G0-b (multiplicity): downward theta_b crossings per shell over 13.8 Gyr. U must yield exactly 1 crossing per shell to be legal without a counting rule; F yields 1 by construction. PASS-U iff the median crossing count is <= 1.1 over shells with r < r_ta/2; otherwise "a counting rule is required", and F is scored with the label that n is a prescribed label (CFG48 G3: PARTIAL as a label, FAIL as a history variable inside an action).
- G0-c (causality): c_adv = max over cut points of |response of S at steps before a perturbation| / max |response|, N = 200 and 400 (CFG242 C1's definition), with a detector control that fires when the kernel is symmetrised. PASS iff c_adv <= 1e-12 at both N and the control fires.
- G0-d (bound-only): the fraction of the dust created in elements that are NOT in a 3D-bound region (negative total energy in the CFG48 sense, or in a halo at the time of creation). Tested with a Zel'dovich three-axis toy (EdS: theta_b = 3H - H sum_i D lambda_i / (1 - D lambda_i); theta_b = 0 at D lambda = 3/4 for a sheet (rho/rho_bar = 4), 0.6 for a filament (6.25), 1/2 for a sphere (8)) and a mass-weighted web census from the CLASS spectrum. PASS iff <= 0.10 of the created dust is in non-3D-bound elements.
- G0-e (vacuum compensation): with T_Lambda = -rho_Lambda g, the exchange forces d_mu rho_Lambda = S c^2 u_mu (CFG131 D1): S must then be spatially uniform on the surfaces orthogonal to the dust flow. PASS iff the localised S of the class is shown consistent (curl of S u_mu = 0) with a pure Lorentz-invariant compensator; otherwise the record's CFG131 D1/A5 result applies and the unfunded-reservoir reading is the only legal exit (scored separately, never as a pass).
- G0-f (inertness): S = 0 identically in the FRW background (theta_b = 3H) and for an outgoing positive-energy shell (CFG242 B1, B2). PASS iff max dust created = 0 to 1e-12.

**Gate G0 verdict.** PASS iff G0-a, c, d, f pass and G0-b passes (U) or is scored with F's label, and G0-e passes with a Lorentz-invariant compensator. A FAIL in any of a, c, d, e, f is a binding FAIL for G0 (b alone is a "counting rule required", reported).

### Gate 3 -- AMOUNT (CFG251's failing gate, attacked directly)

**Question.** Can S be written with ONLY kappa (through a0) and the baryon variables so that the created dust reproduces C(r) = (a0/4 pi) M_b(<r) at turnaround and keeps it afterwards? Or does it need a new constant, the enclosed mass, or the whole profile?

**Parts and pass lines.**
- AMT-1 (dimension): by `ChainCert.Dimension` (`sqrtM_length_iff`, `acc_unique`; premises: monomial family and G4's inventory) the dimensionless amplitude can depend on a0 only through u = a0/g; show by sympy that no other combination of (G, c, a0, rho_b, theta_b-dot, H) gives a dimensionless amplitude with the required M^(1/2) length. PASS iff Q = F(u) with F a declared shape and no new constant; graded P-declared (F is the target).
- AMT-2 (what S must be at turnaround, explicit construction): for a point mass, Q_tot = M_c/M_b = nu(g_N/a0) - 1 = sqrt(1 + a0/g_N) - 1 with g_N the baryonic Newtonian field at the turnaround shell; for baryons uniform at turnaround (B's top-hat convention, CFG251), dM_c/dM_b = (1/3) u / sqrt(1 + u), u = a0/g_loc, which IS a local function of (rho_b, g_loc, a0) (hand algebra; verified in phase 2 against the target to 1e-6).
- AMT-3 (locality of the amount, extended baryons): for a power-law baryon profile rho_b ~ r^-s, a local closure from (rho_b, g_loc, a0) mis-states the target dust density by 3/(3 - s) (50% at s = 1, 200% at s = 2); for the exponential sphere (h = 2, 3, 4, 5 kpc) more. The only local closure that reproduces spherical profiles exactly is the baryon tidal tensor (CFG44 B3: rho_c g = (a0/4 pi G) T_perp), which is exact for spherical baryons only (a thin disc differs by 3-15x, CFG44) and was found to fail reciprocity and ghost-freedom in CFG50. PASS iff a closure built ONLY from the local data of section 1 (with no enclosed mass and no preferred-frame g_loc) reproduces the target density within 10% for the point mass, the uniform sphere and the exponential spheres. Otherwise the amount is non-local in the sense of `ChainCert.Ownership` (`ownership_distinguishes`, `ownership_not_field_local`: two systems with the same local field data get different required responses), reported with the counterexample pair.
- AMT-4 (the retention row, causality of information): the target amplitude is keyed to the galaxy's present baryons M_b (stars and cold gas), while the trigger at turnaround sees only the turned-around cosmic baryons. Using the committed SHMR (CFG35's h48 function), the spread of the retained fraction f_ret(M) = M_b,gal / (f_b M_halo) across M_b = 1e9-1e12 sets the error of a source that knows only turnaround data. PASS iff the induced amplitude error is <= 10% (the amplitude goes as M_b^(1/2), so the spread of f_ret must be <= 1.2 across the range).
- AMT-5 (survival, G1 proper): evolve the self-consistent dust (created at rest at each shell's turnaround, with the declared angular-momentum brackets r_peri/r_ta = 0.05, 0.1, 0.2 of CFG118) under gravity of baryons + dust + Lambda to z = 0, shell crossing allowed. Compare C_final(r)/C_target on x in [0.1, 30] (25 bins of 0.1 dex, as CFG118). PASS (G1) iff the ratio lies in [0.9, 1.1] for masses 1e9, 1e10, 1e11, 1e12, both geometries, both footings, with the SAME constants and no survival rescaling.
- AMT-6 (the dust's own gravity moves later turnarounds): the turnaround time and radius of outer shells with and without the created dust. Reported; the shift enters AMT-5 automatically (self-consistent run), and its size is stated.

**Gate AMOUNT verdict.** PASS iff AMT-1, AMT-3, AMT-4 and AMT-5 pass with no constant beyond kappa and Omega_c h^2. "PASS as a restatement" (P-declared) is reported as such and does not count as a derived mechanism (CFG242's flag; CFG251's rule: restatement is not a pass).

### Gate 4 -- HIERARCHY (Arm C: a satellite turning around inside a host must create nothing)

**Question.** Does a local theta_b trigger know it is inside a host? If not, name it as the binding failure.

**Toy (frozen).** Host: a point mass 1e12 Msun (softened) plus the same background; satellite: a 1e9 Msun baryon core with a cloud of N = 1e4 pressureless baryon test particles, at distances d = 30 and 100 kpc from the host and also inside the host's extended density (rho_host given by the committed exponential sphere or a uniform sphere). The cloud starts homologously expanding about the satellite and decelerates (a formed-embedded tidal-dwarf analogue); theta_b is estimated from a local linear fit to the particle velocity field (a declared estimator, checked against the analytic homologous case to 1%). The same cloud is run in isolation (host off). Rows: (i) created dust with the host, divided by created dust in isolation, for U and for F; (ii) an accreted satellite: created dust before infall, and any further dust at the host's turnaround for the same baryons; (iii) the first-crossing mass distribution: for baryons that end in a 1e12 Msun z = 0 halo, the distribution of the mass of the first turned-around system containing each baryon (excursion-set Monte Carlo with the CLASS sigma(M); baryon filtering mass 1e5 Msun declared).

**Pass lines (frozen).**
- H1 (embedded): created dust in a satellite inside a host <= 0.10 of the isolated amount.
- H2 (accreted): the satellite keeps >= 0.90 of the dust created at its own turnaround, and the host creates nothing further for flagged baryons.
- H3 (top-level, not bottom-level, ownership): >= 90% of the baryons of the final system have their first theta_b crossing within a system of mass >= 0.1 of the final mass. (Bottom-up growth makes the first crossing the SMALLEST enclosing turned-around system.)
- H4 (status of the flag): state whether n is derived from the baryon state or prescribed. As a history variable in an action: FAIL (CFG48 G3, advanced dependence 8.5e-4 and 1.7e-2); as a prescribed advected label: PARTIAL (CFG48 G3).

**Gate HIERARCHY verdict.** PASS iff H1-H3 pass. A PASS of H1, H2 only through F's label is reported as "PASS as a label (restatement)", not a mechanism.

### Gate 5 -- G3 / G4 (energy and ledger)

**Copied lines (verbatim from TEN_DOORS_GATES_2026-09-29.md).**
- **G3 reciprocity and energy.** The reaction on the baryons <= 0.10 g_law over x in [0.3, 30] and the energy the mechanism must supply <= the baryons' orbital energy, in BOTH r_ta conventions (CFG48 G4's pass lines).
- **G4 constants.** No constant beyond kappa and Omega_c h^2; a0's tie to Lambda is the CFG43 tie (P_cap = (kappa^2/8 pi) rho_Lambda c^2) or a stated equivalent.

**Rows.**
- L1 (reaction): the non-gravitational reaction on the baryons from the creation event, in the closed forms of CFG48 G4 / CFG70 for any maintained exchange, and the creation-event momentum balance (zero if the dust is created comoving and the vacuum carries no momentum; CFG131 D4 reports reaction 0 for Q u). PASS iff <= 0.10 g_law at x in {0.3, 1, 3, 10, 30}.
- L2 (literal energy line): E_supplied = M_c c^2 against the baryons' orbital kinetic energy (1/2) M_b V_f^2, both r_ta conventions (CFG48's and B's committed r_ta). PASS iff E_supplied <= orbital energy (CFG131 D4: demand 1e6-1e8 times the orbital energy beyond x = 6.29).
- L3 (vacuum ledger, creation region): f_ta = M_c(<r_ta) / M_Lambda(<r_ta) with M_Lambda = rho_Lambda (4 pi/3) r_ta^3 (rho_Lambda = 86.33 Msun/kpc^3 from the tie, `CFG242_common`), both r_ta conventions; and CFG131 D4's Lagrangian-volume ledger f_Lag = (M_c - 5.366 M_b)/(13.86 M_b). PASS iff f <= 1 for all x <= 30 AND the implied local a0 shift delta a0 / a0 = f/2 <= 1e-2 (CFG242's line). (CFG242 route A found the HEAT ledger was not the obstacle: heat needs at most 1.9e-4 of the vacuum energy of its ball and an a0 shift of at most 9.5e-5. That ledger is for the dust's kinetic energy. L3 is the REST-MASS ledger, which the record (CFG131 D4, CFG253 (C) cluster 636x short) says is a different and larger number.)
- L4 (G4 count): every constant beyond kappa and Omega_c h^2: the generous normalisation N (if used), any survival rescaling, any smoothing width that changes a verdict, the form of F(u) (declared shape, counted separately). PASS iff none enters a verdict.

**Gate G3/G4 verdict.** PASS iff L1-L4 pass. L2/L3 are run for BOTH the funded (Lorentz-invariant vacuum) and the unfunded readings; the unfunded reading passes L3 only by construction and is labelled.

---

## 3. Frozen hand estimates (made before any run; wrong ones will be kept and disclosed)

Inputs: section 1; sigma(M, z = 0) in Msun (memory, unverified; consistent with M* ~ 3e12 Msun): 7.0 (1e6), 5.3 (1e8), 4.5 (1e9), 3.8 (1e10), 2.8 (1e11), 2.0 (1e12). D(z)/D(0) (memory-level, with D(0)/a = 0.788 from CFG251's committed value): 1.2e-3 (z = 1100), 0.113 (z = 10), 0.363 (z = 2.5), 1 (z = 0).

**COSMIC.**
- E1. F_ta(z = 1100) <= 9e-19 for ANY sigma(M, 0) <= 100 (30 gives 2e-191). Omega_dust h^2(1100)/0.1200 <= 1e-18. **Supplied: effectively zero. Shortfall >= 1e18 against the 0.5 line.**
- E2. For F_ta(1100) = 0.5 one needs sigma(M, 0) ~ 1.3e3, about 40-45 times the largest value in a CDM spectrum with a 1e-6 Msun cutoff (memory: ~30).
- E3. z = 10: F_ta(10)/F_ta(0) = 0.094 (M > 1e8) and 0.018 (M > 1e10); Omega_dust h^2(10) = 0.011 and 0.0022. At z = 2.5 the ratio is 0.71 and 0.59. So the class supplies roughly 2-10% of the cold matter at z = 10 where R05/G2 need cold behaviour to k = 30/Mpc, a shortfall of 9-55x, reported not binding.
- E4. C5: |delta theta_b|/(3H) at recombination <~ 1e-3 (memory-level estimate: baryon velocity of order 1e-5 c, k/(aH) of order 20-100). The trigger never fires in the plasma.
- E5. C4: baryon-only sigma_b(M, z = 0) ~ 1e-2 (memory-level: delta_b ~ 1e-4 at decoupling, growth of ~50 before the open-universe freeze at 1 + z ~ 1/Omega_m); delta_ta = 1.276. The self-consistent class has no turnaround at all: about 100x short. Wrong-direction risk: this number is a memory estimate and is only a reported row.
- E6. C6: at z = 0 the class can reach O(1) of Omega_c with the edge x_e tuned inside CFG4's window (0.31-0.48); this is a restatement of CFG4's budget, not a pass.
- **Expected verdict: COSMIC FAIL, the binding failure, at C1. P(COSMIC pass) = 0.003.** The only routes to a pass in this class are creation before recombination (not a turnaround trigger: it is initial data, MUTATE M1) or a trigger on acoustic oscillations (E4 says no).

**G0 (reported only if reached post hoc).**
- E7. G0-b: crossings per inner shell over 13.8 Gyr, median >= 10 (CFG118's runs have ~2,000 orbits; theta_b of an orbiting shell changes sign about twice per radial period): U over-counts by a factor 10-1000. F gives 1. Counting rule required.
- E8. G0-a: P(pass) = 0.5 (the zero of dv/dr + 2v/r need not coincide with v = 0 for a non-top-hat infall; I expect r_theta0/r_ta in 0.5-0.9; unsure).
- E9. G0-d: dust created in non-3D-bound elements >= 0.3 (Zel'dovich thresholds 4 / 6.25 / 8 in rho/rho_bar for sheet / filament / sphere; web mass fraction ~0.5 (memory, unverified)). FAIL.
- E10. G0-e: with a Lorentz-invariant vacuum, FAIL by the record (CFG131 D1, A5; CFG253 (C)). P(pass) = 0.05.
- E11. G0-c: PASS (c_adv = 0.0 exactly at the stencil level, structural), P = 0.9. G0-f: PASS, P = 0.9.
- **P(G0 pass | reached) = 0.05.**

**AMOUNT (post hoc only).**
- E12. AMT-2 holds exactly for a uniform sphere (algebra); AMT-3 FAILS for the local closure at s = 2 (factor 3, i.e. 200% against 10%).
- E13. AMT-5: dust created at rest at turnaround, evolving by gravity alone, ends with C_final/C_target ~ 2.5 in the deep regime (the shell-crossing radius ~0.36-0.4 r_ta maps the created profile M_c ~ r to a final profile 2.5x too heavy at fixed r), and not 1; CFG118's shape result (0.05-0.21 at x ~ 28, 4-360 at x ~ 0.1) is for a different created profile and is the reference. Rescaling Q by ~0.4 would pass at one mass and is a constant (L4). Mass scale follows turnaround, M^(1/3)-M^(0.25), not r_M ~ M^(1/2): x_ta spread 3.165 (CFG118/CFG158).
- E14. AMT-4: the SHMR retained fraction varies by a factor >= 3 across 1e9-1e12 (memory), so the amplitude error is >= sqrt(3) = 1.7 against 1.1: FAIL.
- **P(AMOUNT pass | reached) = 0.05** (0.15 for spherical baryons via the tidal closure alone; 0.03 for local-only plus survival; P-declared in any case).

**HIERARCHY (post hoc only).**
- E15. H1 for U: created dust ratio with / without host = 0.8-1.5 (the host's tidal trace adds -4 pi G rho_host to theta_b-dot, shifting the timing, not removing the crossing). FAIL.
- E16. H1/H2 for F: 0.00 / 1.00 by construction. PASS as a label only (CFG48 G3: PARTIAL).
- E17. H3: median first-crossing system mass for baryons in a 1e12 Msun halo <= 1e8 Msun: FAIL. The first-crossing rule gives the dust to the smallest progenitors, the opposite of CFG251's top-level rule. P(H3 pass) = 0.05.
- **P(HIERARCHY pass | reached) = 0.05** (0.01 unflagged).

**G3/G4 (post hoc only).**
- E18. L1: reaction 0 (CFG131 D4): PASS.
- E19. L2: demand 1e6-1e8 times the orbital energy beyond x = 6.29 (CFG131 D4): FAIL.
- E20. L3: M_Lambda(<r_ta) = 0.1835 M_ta (rho_Lambda/rho_m = 2.175 over the top-hat contrast 11.81 at z = 0) = 4.33 M_b for CFG118's M_ta = 23.6 M_b, against M_c >= 29.0 M_b at x = 30: f_ta >= 6.7; at B's r_e (37-211 M_b) 8.5-49. CFG131's Lagrangian-volume ledger: f_Lag = 1.71 at x = 30 (crosses 1 at x* = 20.2); gross 2.09. The a0-shift line needs f <= 0.02: FAIL by >= 100x. This disagrees with the premise "the ledger is not the obstacle": that premise holds for HEAT (CFG242), not for REST MASS.
- E21. L4: at least one constant enters a verdict (N or the survival factor). FAIL.
- **P(G3/G4 pass | reached) = 0.02.**

**Joint.** P(all gates pass) = 0.003 x 0.05 x 0.05 x 0.05 x 0.02 = 7.5e-9; I regard it as ordering information, not a model. **Expected binding failure: COSMIC (C1): Omega_dust h^2(z = 1100) <= 1e-18 x 0.1200 against the 0.060 line (no baryon halo has turned around at z = 1100; sigma(1100) ~ 0.002-0.006 against a threshold of 1.06).**

---

## 4. MUTATE controls and sensitivity checks

Each MUTATE flips a load-bearing cell, writes separate outputs (`CFG243_<script>_MUTATE<k>.out` and `_results.json`), and exits 1 when the control bites (the named headline changes as stated). A MUTATE that fails to bite exits 0, is reported as a failed control, and is kept as run.

- **M1 (z-independent creation).** Replace the turnaround trigger by creation of Omega_c h^2 = 0.12 of uniform dust at z_i = 1e5 (initial data). COSMIC C1 must flip FAIL -> PASS (ratio 1.0 >= 0.5); G0-d and the class definition fail (creation in unbound flow; it is CDM with a vacuum origin story, as CFG253 reading B). Headline: COSMIC.
- **M2 (evaluation epoch).** Evaluate the COSMIC pass line at z = 0 instead of z = 1100. Under the generous normalisation Omega_dust h^2(0) = 0.1200: must flip FAIL -> PASS. Headline: COSMIC.
- **M3 (non-local source).** Let Q depend on the enclosed baryon mass M_b(<r) (hand-fed). AMT-3 must flip FAIL -> PASS for every profile (the target is supplied), and G0 locality must flip PASS -> FAIL. Headline: AMOUNT (restatement flag).
- **M4 (host-aware source).** Give the source the host's membership (n = 1 for baryons in a host). H1 must flip FAIL -> PASS (ratio 0.00); this is the prescribed label (CFG48 G3 PARTIAL), not a mechanism. Headline: HIERARCHY.
- **M5 (remove the counting rule).** Compare U against F: G0-b flips from "counting rule required (median crossings >= 10)" to exactly 1.
- **M6 (vacuum volume).** Take the vacuum energy of a ball 1e3 times larger than the creation region (a non-local reservoir): L3 must flip FAIL -> PASS (by non-locality). Headline: G3/G4.
- **R1 (sensitivity, NOT a MUTATE; expected NOT to bite, declared before running).** Lower the COSMIC requirement from 0.1200 to 0.01 (the user-suggested variant). Prediction: the verdict does not change (the supplied abundance is <= 1e-18 of any requirement above 1e-18), so the headline is robust to the requirement. If it bites, the headline is fragile and the report says so. R1 exits 0 when it does not bite, and this is the declared convention for R-checks.
- **R2 (sensitivity, expected NOT to bite).** Replace delta_ta(1100) = 1.0624 by 0.5 (the lowest plausible turnaround threshold): F_ta(1100) <= 1e-4 still (hand), so C1 stays a FAIL.

---

## 5. Script plan

All scripts live in `campaign_fresh_gravity/CFG243_*` (lane directory `CFG243_dust_at_turnaround/`; the frozen file is committed before any script). Conventions (as CFG242): each physics script reads `MUTATE=<k>` from the environment; the main run exits 0 (a gate FAIL is a result, not an error; only a failed internal control makes a main run exit 1, and that is reported); MUTATE exits 1 when the control bites; outputs `.out` and `_results.json` per mode; no absolute home path is printed (the repository root is `ZF_REPO` or found by walking up from `__file__`; the scripts print `<repo>` and `<lane>`); each run is under 15 minutes; `sys.dont_write_bytecode = True`; nothing outside the lane directory is edited; imports of committed lanes are read-only.

- `CFG243_common.py`: declared constants and conversions (section 1), repo-root walk, the run/verdict/check helper.
- `CFG243_controls.py`: reproduces committed numbers before any gate (K1 CLASS sigma_8 = 0.8116 and the Press-Schechter M* check sigma(M*) = 1.686 near 3e12 Msun; K2 CFG251's A1 ratio (0.4)^3 = 0.064; K3 CFG131's x* = 20.2 and f = 1.70 at x = 30 from Omega ratios; K4 CFG118's M_ta = 23.6 M_b scaling; K5 CFG4's thresholds 11.81 / 8.89 / 7.09 / 5.72). A failed control stops the lane.
- `CFG243_cosmic.py` (Gate 1; ~1 min with CLASS): C1-C6, the sigma(M, z) table, F_ta(z), Omega_dust h^2(z); MUTATE=1 (M1), =2 (M2); R1, R2 as `CFG243_cosmic_R1.py` or `R=1` modes.
- `CFG243_g0_legality.py` (Gate 2; ~5 min): the shell-code and Zel'dovich toys, G0-a to G0-f; MUTATE=5 (M5).
- `CFG243_amount.py` (Gate 3; ~10 min at <= 5,000 shells): AMT-1 (sympy), AMT-2/3 (closed forms against profiles), AMT-4 (SHMR from h48 read-only), AMT-5/6 (self-consistent shells); MUTATE=3 (M3).
- `CFG243_hierarchy.py` (Gate 4; ~5 min): the satellite-in-host toy and the excursion-set first-crossing Monte Carlo; MUTATE=4 (M4).
- `CFG243_g3g4_ledger.py` (Gate 5; seconds): L1-L4; MUTATE=6 (M6).
- `CFG243_verdict.py`: reads the JSONs, applies the stop rule, prints the first binding FAIL and the gate table; refuses to count any `_posthoc` result in the verdict.
- `CFG243_run_all.sh`: main scripts in the frozen order, stopping at the first binding FAIL (the later gates run only under `POSTHOC=1` and are written to `*_posthoc.*`), then every MUTATE with the frozen expected exit code beside the observed one, then the verdict.
- If CLASS is not importable the cosmic script exits with a declared NOT-RUN and the hand table of section 3 stands as unverified; it does not fall back silently.
- If every gate passes, `CFG243_rederive.py` is written and run before reporting: a from-scratch re-derivation of C1, AMT-2/5, H1 and L3 that does not import the lane's code.

---

## 6. What counts as a pass, and what counts as a scoped no-go

- **Scoped no-go on the frozen class.** The first binding FAIL, as stated in section 2, with the failure named and its number. It is a statement about a pressureless conserved dust created by a local causal source that fires at theta_b crossings, funded by the vacuum, under the declared estimators. It is not a theorem and says nothing about other source classes.
- **Pass of a gate.** Every pass line of the gate, with no constant beyond kappa and Omega_c h^2 entering the verdict, and with the pass not resting on a hand-fed target or label. A pass that reproduces whatever target it is given (CFG242's selectivity control) is reported as PASS as a restatement and does not count as a derived mechanism.
- **Pass of the class.** All five gates pass, the independent re-derivation agrees, and the two items outside this lane's frozen order are run and pass: G5 (no ghost, no gradient instability, hyperbolic and causal, Solar System by explicit statement) and the perturbation-level G2 (growth within 5% of LCDM to k = 30/Mpc, with the perturbation equations stated). Even then the report says: the mass is still required, kappa = 1/2 is fitted, and nothing here says the theory is closed.
- **Failed controls and wrong expectations are kept**, with the frozen text above, not repaired.

---

## 7. What is NOT covered

- **Other source classes.** Sources triggered by something other than theta_b (an energy-based boundness criterion, a density threshold, a time scale, the khronon); creation from a non-Lorentz-invariant or dynamical vacuum (door 8's untested premise); an action realising S (CFG131 D2: Q != 0 needs explicit T0 dependence, which breaks the shift symmetry); a collisional dust; a source that is not conserved afterwards.
- **Post-recombination creation as a partial fix.** A source that creates dust only after recombination cannot supply the CMB-epoch cold matter. COSMIC counts exactly that, and says the class supplies none of it at z = 1100. The observables touched if a separate cold component supplies the early matter and this class supplies only the late galaxy-scale phantom: (i) the acoustic peaks (third peak, z_eq = 3423 with a clustering component against 532 without) and the CMB lensing; (ii) linear growth at z >~ 10 to k = 30/Mpc (R05 / G2: the cold-early requirement, c_s^2 <= 4.6e-12); (iii) BAO and RSD through the background; (iv) the high-redshift galaxy epochs (CFG197). In that reading the class is not a replacement for the cold mass: it adds a second cold component beside the required one and reduces to candidate B's T4 (CFG251's own reduction); CFG253 reading (B) is the early-transfer alternative.
- A relativistic completion, a Boltzmann (CMB) run of the source, non-spherical baryons (a thin disc's tidal closure and enclosed-mass form differ 3-15x, CFG44), mergers beyond the toy, baryonic feedback and gas physics in the shell code, the Solar System (G5), and the DR4 prediction (Arm C = 1.000 is also Newton's and LCDM's).
- The PAPER36 text itself and L121/L129, as in section 0.

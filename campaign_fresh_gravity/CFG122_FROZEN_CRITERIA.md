# CFG122 (DOOR 4) — superfluid dark matter (Berezhiani–Khoury type) at the missing object: FROZEN CRITERIA

Written 2026-09-29, before any script, number or plot of this lane exists. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure. A scoped no-go is a valid result. κ = ½ is FITTED. Both a₀ footings are used (9.3603e-11 and 1.1312e-10 m/s²). Nothing here says the theory is closed, and no result of this lane can say the data favour the framework.

## (a) Disclosures (read first)

1. **The menu of doors was written knowing the target.** The ten-doors menu (`closure_map/TEN_DOORS_GATES_2026-09-29.md`) was written with CFG44's exact target in hand: C(r) = ρ_c r³ g_tot = (a₀/4π) M_b(<r), equivalently ρ_c = a₀/(4πG r √(1+x²)) for a point mass (x = r/r_M, r_M = √(G M_b/a₀)), which is the P2 law's phantom density. A pass of any door is therefore not evidence for its mechanism. It would show only that the door contains a structure that can be tuned or arranged to match a target already known.
2. **What was read for this file.** The gates file, GAPS_1_2_JOINT_STATUS, ACTIONS_AND_NOGOS, and the READMEs of CFG43, 44, 48, 50, 70, 72 and the CFG60 provenance note; the `dark_fluid_2026`, `dark_fluid_kick_2026` and `condensate_dust_2026` READMEs; the docstrings of CFG44 B2 and B3. **Also read, beyond the list, because they are direct prior art on this exact door:** `superfluid_2026/STANDING.md`, the docstrings of `sf06_phase_boundary_2026.py` and `sf08_soundspeed_turnover_2026.py`, the first 60 lines of `sfD_superfluid_phonon_2026.out`, the source (not run; it has no committed output) of `real_research/superfluid_phonon_baryon_coupling_price_2026.py`, and section 4 of the June ROUTE_D verdict. Their numbers are NOT used as inputs here; they are compared with this lane's independent re-derivation only after the run, and no pass line depends on them.
3. **The Berezhiani–Khoury (BK) model below is written from memory of the published papers** (2015 effective theory; 2018 galaxy fits). No web access was used. Everything derivable is to be derived by the script (sympy) from the stated Lagrangian, and the derived form governs over this file's hand-derived formulas. BK's fitted values of m, Λ, α (recalled as m of order 1 eV, Λ of order 0.1–1 meV, α of order 1–10) are unverified, and **no verdict may rest on them**: every gate is evaluated structurally (scaling, or existence over a declared (m, α) plane), never at a recalled fiducial point.
4. **Standing rule (no dark-matter particle).** The door is tested as an effective field theory of a condensate field. m is the mass of that field's quanta; it is a required, unexplained input, and this lane makes no claim of a particle species. The dark sector is not claimed absent.

## (b) The door, exactly

**Action (non-relativistic, static, spherical reduction; the script derives every equation).** With θ = μt + φ(x),

    X = ∂ₜθ − mΦ − (∇θ)²/(2m) = μ − mΦ − (∇φ)²/(2m),   P(X) = (2Λ(2m)^{3/2}/3) X√|X|,
    L = P(X) − α (Λ/M_Pl) φ ρ_b − ρ_b Φ − (∇Φ)²/(8πG),   ∇²Φ = 4πG (ρ_b + ρ_DM),   ρ_DM = m n,   n = P′(X) = Λ(2m)^{3/2}√|X|.

The baryons feel Φ and the phonon force a_φ = α(Λ/M_Pl)∇φ. The condensate feels Φ and the steady flow v = ∇φ/m inside X. Λ has dimension of energy; α is dimensionless; M_Pl is the reduced Planck mass.

**Hand derivations (unscripted; the script's sympy governs).**
- Phonon field equation, static: ∇·(n∇φ/m) = α(Λ/M_Pl) ρ_b. The Λ cancels between the two sides. Number is **not conserved**: the baryon source injects condensate number at the rate Ṅ = α(Λ/M_Pl) M_b. In spherical symmetry the flux law is exactly n φ′ = m α M_b(<r)/(4π r² M_Pl), enclosed-mass dependent by Gauss.
- Gradient-dominated (deep) regime: L → −(2Λ/3)|∇φ|³; |∇φ|² = α M_b(<r)/(8π M_Pl r²); a_φ = √(a₀ g_N) with **a₀ = α³Λ²/M_Pl up to a numerical factor N_a to be derived**.
- Equilibrium EOS in the condensed phase (X > 0, gradient negligible): P = K ρ³ with K ≈ 1/(12 m⁶Λ²), an n = ½ polytrope (self-gravitating R ∝ M^{(1−n)/(3−n)} = M^{1/5}); c_s² = dP/dρ = 3P/ρ = 2X/m.
- Deep-regime condensate density ρ_DM ≈ 2m²Λ|∇φ| ∝ √M_b(<r)/r. The CFG44 target in the deep regime is ρ_c ≈ √(a₀ M_b(<r)/G)/(4π r²) ∝ √M_b(<r)/r². **Same enclosed-mass exponent ½, one power of r different, ratio ∝ r/r_\* with a universal length r_\*(m, α).** This is the door's one structural resemblance to the target, and the reason it is not dismissed in advance.
- Crossover: the gradient term equals X̄ = μ − mΦ at g_N ≈ 2 m X̄/(α M_Pl). So the crossover acceleration, the door's effective a₀, tracks the halo's X̄ (per-halo, set by the phase-boundary condition), not a universal constant.

**The phase structure.** Superfluid core out to R_c, normal (cold, collisionless, NFW-like) phase outside. R_c is where T = T_c(n), with T_c = (2πħ²/(m k_B)) (n/ζ(3/2))^{2/3} and T = mσ² set by the halo's velocity dispersion (the pricing script's convention; a factor-of-order-1 convention, reported at ×½ and ×2, never tuned). **For the tests I take σ² = V_f²/2 = ½√(G a₀ M_b), the framework's own BTFR (CFG44's σ∞²).** That is a postulate shared with CFG44's surviving "temperature-slaved fluid", flagged as such. The boundary is per-halo dependent.

**Constants and inputs beyond κ = ½ and Ω_c h² = 0.12.**
- Model constants: m, Λ, α (three). The a₀ tie α³Λ²N_a/M_Pl = κ c √(G ρ_Λ) is written as the door's *stated equivalent* of the CFG43 tie (postulated, not derived). It removes one, leaving **two new independent constants** (m and one of Λ, α).
- Per-halo inputs, not constants: μ (fixed by the phase-boundary condition at R_c), R_c.
- The normal-phase halo mass is **not derived by the door**. It is an imported ΛCDM input (CFG69's comparator: Moster+2013 mass, Duffy+2008 concentration, no contraction, no scatter). It is used only in G1.4 and the reported rows, and is declared as an external per-halo function.
- The condensate's thermalisation rate (needed to say whether cosmological DM condenses) is not fixed by the EFT.
- No numerological search for a tie of m or α to ρ_Λ, ρ_c or M_Pl will be done (the SM-mass / numerology sector is walled).

**Where the door falls relative to the record's hypotheses (which exclusions apply and which do not).**

| record item | its hypotheses | this door |
|---|---|---|
| CFG44 B2 E1/E2 (universal barotropic P = Π(ρ_c)) | static, spherical, weak field; universal Π; the fluid **at rest, hydrostatic in g_felt = g_tot**; density = target | The condensed EOS P = Kρ³ is barotropic and universal, so it falls under E1/E2 **if** the fluid were static and in g_tot. It is neither: the deep-regime solution carries a steady superflow v = ∇φ/m and the condensate feels g_N,tot, not the phonon force. So B2 does not apply as written. That is loophole 1, and its cost is the number injection (G2.4, G3.2). |
| CFG44 B2 E3/E4 (second force; the orchestrator's "B3": the second-force exclusion is in B2, B3 holds the local closures) | a symmetric second potential, or a fixed-kernel force **linear in M_b** on the fluid | The phonon force is √M_b (nonlinear) and acts on baryons. E4 does not apply as written. E4's structure is nonetheless the same: its deep regime forces P ∝ ρ³, the superfluid EOS, and its Newtonian regime then contradicts. G1.3/G1.6 test whether the door escapes that contradiction. |
| CFG44 B3 L1 (locality, far-shell theorem) | closure local in the fields at r, which are identical for profiles A and A + outer shell | ρ_DM depends on X = μ − mΦ − φ′²/2m. φ′ carries only M_b(<r) (Gauss), but μ − mΦ shifts by a constant when an outer shell is added, and μ is fixed by the edge. So the door is non-local through μ. G1.5 tests the consequence. |
| CFG44 survivors | temperature-slaved fluid (postulates the BTFR); locally virialised fluid (postulates β) | The finite-T two-fluid reading falls under the first. G6 tests it and prices it. |
| CFG44 B2 "reciprocity" (density-slaved 1–4 g_law) | reaction on baryons | The door's coupling is Lagrangian, so reciprocity is built in. The reaction on baryons **is** a_φ. G3.1 computes it. |
| CFG43 obstruction | single conserved current; barotropic EOS in ρ/ρ_Λ; P ≤ P_cap; growth ≤ 5%; cap at r_M | The door has no cap (P unbounded), no conserved current (baryon source), and a phase-dependent EOS. It is in the class CFG43 says it does **not** touch (non-barotropic, order-parameter). Its growth requirement is the same G2. |
| CFG48 Gap 1 (bound-only switch), Gauss lemma, N14 gates | shift-symmetric field with baryons the only source, gate prescribed or baryon-slaved | The phase boundary IS a gate, but it reads the DM's own state (T, n). A gate reading the fluid is the XR11/MS1 class (N14), not re-run here. The Gauss lemma excludes a second real source with its own stress, which the condensate is, so it does not apply. But the edge step it warns of is tested (G1.4). Prior art: sf06's theorem (an **environmental** phase boundary cannot screen the Solar System; the Sun is at 0.67 of the MW's r_M). |
| CFG48 G4 / CFG70 / CFG72 (exchange, memory kernel, light cone) | the static limit of the exchange is the target's enclosed-mass functional, **linear** in M_b; energy paid inside the closed baryon + fluid action | CFG72's Gauss-law scalar mediator is the linear special case of this door's φ. Here the kinetic term is |∇φ|³, so the static functional is √M_b(<r). The CFG70/72 numbers (0.065 → 22.5 g_law; 23–318×) do **not** transfer. G3 recomputes. |
| CFG50 tidal closure | T_ij as a stress | Unrelated coupling. Its FRW lesson is reused: a uniform baryon source acts on the background at high z (G2.4). |
| CFG60 rubric (D/P/I/X/U); A25 (non-barotropic e(n, χ = \|∇u\|²) fluid, gates frozen, **untracked, no script**) | | P(X) with X ∋ (∇θ)² is exactly an energy density e(n, \|∇φ\|²). This door is the first to run that class, in the BK specialisation. `CFG44_gap2_order_parameter_fluid/` is not in the tree; it was not read. |
| FL1–FL3, FK1 (real_research/dark_fluid_2026, dark_fluid_kick_2026) | complex order parameter, Schrödinger–Poisson, conserved number, kernel-invisible, EOS from the phase-only limit P = μ²/2g | Not repeated: this door has a P ∝ X^{3/2} EOS, a non-conserved number, and a direct baryon coupling (FL1's fluid is kernel-invisible by design). FL1's F3 and L374 (the phase-only EFT breaks at stream crossing; minimal ghost condensate with quadratic P and (□φ)² term) concern a different P(X). Their exclusions are neither repeated nor assumed to transfer. |
| v9 DBI dark sector, carrier chains, condensate dust | dead / stopped | Not re-opened. |
| Out of scope (declared) | clusters, the Bullet Cluster (BK's own weak front: DM in the normal phase) | Not tested, not claimed. |

**How the door maps to the CFG44 target, and the two branches (never pooled).**
The target needs a cold, collisionless, real-mass density ρ_c = a₀ M_b(<r)/(4π r³ g_tot), which is the P2 phantom density, including its pressure and dispersion (hydrostatic in g_tot, where hydrostatics is then an identity). In BK, however, the law's *dynamics* comes from a force on baryons, not from real cold mass, and the condensate feels only Φ. So two readings exist:
- **Branch S (the door's premise as stated: the condensate is the dark density that follows the baryons).** ρ_DM(r) of the coupled solution is compared directly with ρ_c^target(r). The same solution also puts a_φ on the baryons, so the additive-law double counting (CFG44: +0.43 dex at x = 3) is a cost to be measured (G3.1).
- **Branch F (BK-native force branch).** The baryons feel g_N,tot + a_φ; the dark density is only Newtonian. The test is dynamical equivalence with the P2 law, g_b vs g_law. Even a pass **does not fill the missing object** (a cold real mass; gate rule 1), because the force supplies the dynamics, not a mass. It is scored "force restatement, lensing sector unresolved", a different theory from candidate B. The galaxy–galaxy lensing deficit ν is a reported row only.

**Is the phase change / condensate fraction a non-barotropic (two-fluid) loophole?** Loophole 1 above (steady flow, non-conserved number) is one. Loophole 2 is finite T: ρ = ρ_s + ρ_n with the ideal-Bose-gas fraction ρ_s/ρ = 1 − (T/T_c)^{3/2} (a declared convention; T_c ∝ n^{2/3} makes ρ_n saturate at ρ_crit(T) and the total pressure P = P_n^sat + Kρ_s³), so P depends on (ρ, T_halo), non-barotropic in ρ alone and per-halo. B2's E1/E2 assume a universal Π(ρ_c); they do not cover Π(ρ; T_halo). Its cost is CFG44's own survivor: T_halo must be prescribed (the BTFR postulate) and T uniform in equilibrium. G6 tests whether the EOS-level statement holds at all. The full Landau two-fluid hydrodynamics is not run.

## (c) The tests

Shared conventions. Baryon profiles: point mass and the CFG44 B1 exponential spheres (compact and diffuse), read from CFG44 `Bcommon.py` (or re-implemented identically). M_b ∈ {10⁹, 10¹⁰, 10¹¹, 10¹²} M☉. x-grid: 200 log-spaced points on the stated range. Relative error = max over the grid of |model/target − 1|. **Universal constants:** (m, α) identical at every mass; Λ from the a₀ tie; only the per-halo μ (and hence R_c) may differ. **"Existence over the plane"** means the whole declared plane m ∈ [10⁻³, 10³] eV × α ∈ [10⁻², 10²] (log grid, 60 × 60) is evaluated and the verdict is "no point passes" or "the set of passing points is S". A feasible set is reported as a set, not as a fitted value, and never as a pass of G4. Scripts resolve the repo by `ZF_REPO` or `__file__` and import the CFG44/48 helpers read-only.

**S0 controls (all must pass or the harness is broken).**
- S0.1 sympy derives the flux law, N_a, and the deep-MOND limit v⁴ = G M_b a₀ to 1e-6.
- S0.2 P(X) EOS: K, c_s² = 2X/m, index n = ½.
- S0.3 α → 0 recovers Newton to 1e-12.
- S0.4 numerical Lane–Emden n = ½: M–R exponent 1/5 to 1e-3 (internal consistency, no external table).
- S0.5 the target's point-mass identities reproduce CFG44 B1 to 1e-5.

**G1 target (the gate as frozen: within 10% over x ∈ [0.1, 30], masses 10⁹–10¹², same constants).** If the condensate edge x_edge < 3 for any mass, coverage is insufficient and that cell FAILS. The range is [0.1, min(30, x_edge)].
- **G1.1 [HEADLINE, Branch S, point mass]:** ρ_DM(r) of the self-consistent coupled solution (Gauss flux law + Poisson + X including the flow term) vs ρ_c^target. PASS iff some (m, α) in the plane and, for each mass, some μ, give ≤ 10%. Sub-check G1.1a (symbolic): the ratio ρ_DM/ρ_target in the gradient-dominated regime is ∝ r/r_\*(m, α) with r_\* independent of M_b; PASS iff its spread at fixed x across 10⁹–10¹² is ≤ 10%. The analytic value is (10³)^{1/2} = 31.6.
- **G1.2 [Branch S, exponential spheres]:** as G1.1 for the compact and diffuse CFG44 spheres. ρ_target depends only on M_b(<r).
- **G1.3 [Branch F, dynamical equivalence]:** g_b/g_law − 1 within 10% over the range (P2 law; ν_mono reported), including the condensate's Newtonian mass and phonon-off beyond R_c. Also report the double-counting fraction M_DM,Newt(<r)/M_dyn(<r): it must be ≤ 10% for the force reading to be self-consistent.
- **G1.4 [edge step]:** |M_dyn(R_c⁺) − M_dyn(R_c⁻)|/M_dyn ≤ 10%, with the normal phase the imported ΛCDM halo (external, declared). Reported for both branches. This is the door's own version of CFG48's edge-stress finding.
- **G1.5 [far-shell test, the B3 L1 analogue]:** add a baryon shell m = 10 M_b at R′ = 40 kpc outside r\* and compare ρ_DM(r\*). The target's ρ is unchanged (it depends on M_b(<r) only). PASS iff |Δρ/ρ| ≤ 1%. Two cases, both reported: μ held fixed, and μ re-fixed by the edge condition (the model's own case; it decides).
- **G1.6 [crossover universality]:** a_×(M_b) := the g_N at which a_φ = g_N, with X̄ from the door's own edge condition. PASS iff max/min over 10⁹–10¹² is ≤ 1.10 (a universal a₀, as the framework requires).

**G2 CMB and growth.**
- G2.1 (statement): write the perturbation equations in both phases: (i) normal phase = collisionless Vlasov CDM, (ii) condensed phase = P(X) fluid plus the phonon–baryon coupling, including the coupling's homogeneous mode. Sympy derives the linear system.
- G2.2: if the cosmic-mean DM were condensed, c_s² = ρ²/(4Λ²m⁶) with Λ from the tie. Require c_s ≤ c at every z ≤ 1100, and CFG43's two-fluid growth test (within 5% of ΛCDM to k = 30/Mpc at z ≳ 10, solver as CFG103's referee). Existence over the plane.
- G2.3 (phase at recombination): decide whether background DM is (a) thermal with T > T_c(n(z)), which requires σ_DM ≳ 10² km/s and a free-streaming length λ_fs ≤ 0.01 Mpc (an order below π/(30/Mpc) ≈ 0.10 Mpc), or (b) cold and non-thermalised, which needs a thermalisation time greater than the Hubble time, computed from a scattering rate. **The EFT does not fix that rate** (it is not determined by (m, Λ, α) without a UV completion). If (b) is the only exit, G2.3 is UNDECIDED, and G2 as a whole cannot be an unconditional PASS.
- G2.4 (number injection): fractional DM number creation per Hubble time by the baryon source, (i) in the cosmic background if the coupling were active, over z = 1100 → 0, and (ii) inside a halo over one Hubble time. PASS iff ≤ 1% (background) and ≤ 10% (halo). Hand estimate: a mass-creation rate of m α Λ/M_Pl per unit baryon mass, of order several per Gyr for m ~ 1 eV, so a fail unless m is tiny. The plane is scanned.
- G2.5: CMB lensing and TT/TE/EE: not computed; by declaration unchanged if and only if G2.3 resolves to the normal phase.

**G3 reciprocity and energy (both r_ta conventions: CFG48's, and B's committed r_ta with ν_mono).**
- **G3.1 [reaction on baryons]:** a_φ/g_law ≤ 0.10 over x ∈ [0.3, 30] for 10⁹, 10¹⁰, 10¹² M☉ (Branch S, same solution as G1.1). Hand estimate: about 1 in the deep regime, a fail by 10×. Also report the additive overshoot in dex against the P2 law.
- **G3.2 [energy]:** (i) the chemical-potential energy of the injected number, μ Ṅ integrated over t_dyn(r_e) and t_H, vs ½ M_b V_f² (PASS iff ≤ 1); (ii) reported only: the rest-mass energy m Ṅ t. The EFT does not say who pays the rest mass. (iii) reported: CFG44's own target energy E_c/(½ M_b V_f²) = 1.5 r_e/r_M for comparison.
- **G3.3 [structure control]:** the reaction derived by virtual work from the action equals a_φ to ≤ 1% (a hostile check that reciprocity is built in).

**G4 constants.** PASS iff the number of untied new constants is 0 (the tie α³Λ²N_a/M_Pl = κ c √(Gρ_Λ) is admitted as the CFG43-type stated equivalent, flagged postulated). The script lists them: m; one of (Λ, α); the T = mσ² convention factor; the imported SHMR and concentration functions; the thermalisation rate. **Expected count ≥ 2, so G4 FAILS in advance** unless a same-action tie to Λ or κ is exhibited for m and the second constant; no numerological ties are sought.

**G5 well-posedness and Solar System.**
- **G5.1 [ghost / gradient]:** second variation of the coupled system about the static solution in spherical symmetry (sympy), kinetic coefficient and c_s²(r) in the regions X > 0 and X < 0. PASS iff kinetic > 0 and c_s² > 0 wherever a_φ ≥ 0.1 a₀ over x ∈ [0.3, 30]. **Hand estimate (unscripted; may be wrong): P_XX < 0 for X < 0, which would give a wrong-sign kinetic term or c_s² = 2X/m < 0 in the gradient-dominated (MOND) regime.** The script decides.
- **G5.2 [Landau / Cherenkov]:** baryon speeds V_f (30–300 km/s) must not exceed c_s(r) over x ∈ [0.3, 30]; if they do, the phonon-emission drag is reported.
- **G5.3 [superluminality]:** c_s ≤ c everywhere; hyperbolicity in the deep regime.
- **G5.4 [Solar System, explicit statement], both footings, both readings of the force (A: the a₀-line anomaly, saturating at a₀/2; B: BK's unscreened √(a₀ g_N)):**
  - (i) Cassini: |γ − 1| = 2ε/(1 + ε) ≤ 2.3 × 10⁻⁵, with ε = a_φ/g_N at 1 AU.
  - (ii) WEP: the coupling is to ρ_b, hence composition dependent; η ≤ 1 × 10⁻¹⁵ (MICROSCOPE), ≤ 1.4 × 10⁻¹³ (LLR).
  - (iii) sunward anomaly vs the framework's own ephemeris ceiling s ≤ 1.27 × 10⁻⁵ a₀.
  - (iv) phase-boundary screening: T/T_c at 1 AU, using the local DM density and dispersion; PASS iff the condensate is absent at 1 AU and present at the halo's r_M. Prior art (sf06) says the Sun and the outer galaxy are environmentally the same. Both a₀ footings; no comparison with the prior script's numbers enters a pass line.

**G6 [the two-fluid loophole, EOS level].** The required c_s²(ρ; M_b) from the target (CFG44 B2 E1 formula, exponent e(x) ∈ [½, 1]) vs the two-fluid EOS c_s²(ρ; T_halo(M_b), m, Λ) with T_halo = mσ², σ² = ½V_f². PASS iff for some (m, Λ) the two-fluid EOS matches within 10% over x ∈ [0.1, 30] at all four masses. The cost is stated whatever the outcome: the BTFR postulate for T, uniform T in equilibrium (T(r) not derived), and the per-halo R_c. A pass is a "restatement" in CFG44's sense, not a derivation. A fail with the BTFR granted is decisive for this loophole. Hand orientation: the isothermal normal component gives e = ½ (the deep value) but the condensed EOS gives e = 0 at fixed ρ against the target's e → 1 in the Newtonian regime, so a fail is expected.

**Reported-only rows (no pass line, never pooled).** R1: G1.3 against the ν_mono phantom. R2: T = mσ² convention ×½ and ×2. R3: the finite-T ρ_s/ρ profile of the two-fluid halo. R4: galaxy–galaxy lensing deficit of Branch F (ν). R5: after the run only, a side-by-side with the prior scripts' outputs (superfluid_2026, pricing script) with any disagreement disclosed.

## (d) Tested and explicitly NOT tested

**Tested:** the NR static spherical BK EFT (P(X) = X^{3/2} with the linear phonon–baryon coupling) at galaxy scales; both branches; the phonon/condensate flux law and injection; the EOS-level finite-T two-fluid statement; linear growth as a bound on the condensed phase; the reaction and energy of the coupling; second-variation well-posedness; Solar System bounds on the coupling.

**NOT tested (the answer is UNDECIDED there):** a relativistic completion (the sign of P_XX and of the phonon kinetic term may differ, and light bending needs a conformal/disformal coupling); rotating cores and vortex lattices (FL3-type swirl); the full Landau two-fluid hydrodynamics (second sound, relative normal/superfluid flow, dissipation at the phase boundary); a UV completion of the P ∝ ρ³ interaction (and hence the thermalisation rate); non-spherical baryons; time dependence and formation of the condensate; clusters and the Bullet Cluster (out of scope); the stream-crossing behaviour of the superfluid core (L374's exclusion concerns a different P(X) and is not assumed to apply); mergers and phase-boundary motion.

## (e) MUTATE controls (each must change the named headline; the script exits 1 on a main-run gate FAIL, and a MUTATE that flips its gate is the expected outcome)

- **MUTATE=a:** replace the target by the door's own gradient-dominated condensate density 2m²Λ|∇φ|. **G1.1 must flip to PASS.** If it does not, the harness cannot pass and every G1 FAIL is declared uninformative.
- **MUTATE=b:** use P(|X|) (even in X), removing the sign reversal at X < 0. **G5.1 must flip to well-posed.** If it does not, the ghost test cannot see the sign and is declared non-discriminating.
- **MUTATE=c:** α → 0. **G3.1 must flip to PASS (reaction 0) and G1.3 must collapse (no force).** This verifies that the reaction and the dynamical-equivalence gates both read the coupling.
- If the main run already fails a gate that a MUTATE is meant to flip from PASS to FAIL, the README says so. Declared control failures are kept and disclosed.

## (f) Expected outcome, stated before running

These are hand estimates from pen-and-paper scalings, not results; several may be wrong. My prior: G1 FAIL (~85%), G4 FAIL (~95%), at least one of G5.1 / G5.4 FAIL (~75%), G2 conditional at best.
- **G1.1/G1.2 FAIL by slope.** The deep-regime condensate density has the target's √M_b(<r) but one wrong power of r, so the mass spread at fixed x is √(10³) ≈ 32 against the 10% line. In the Newtonian regime the polytropic ρ ∝ √(μ − mΦ) runs r^{−1/2}, not r^{−1}. The single universal length r_\* can match at most one radius.
- **G1.3 FAIL by shape.** BK's force law a_φ = √(a₀ g_N) gives g = g_N + √(a₀ g_N) against P2's √(g_N² + a₀ g_N): about +41% at g_N = a₀ (unless the full X-dependence changes it), and the condensate's own Newtonian mass double counts.
- **G1.6 FAIL:** the crossover tracks X̄ ∝ σ² ∝ V_f² ∝ M_b^{1/2}, so a_× varies by several × over 10⁹–10¹². This is CFG44's mass exponent e = ½ in another guise.
- **G3.1 FAIL (about 1 g_law in the deep regime).** If the branch S density were the target, the phonon force would add on top of it; the additive-law overshoot is the cost.
- **G2.4 FAIL** unless m is very small, because of the number-injection rate of the linear coupling (which may signal that the coupling as I have written it needs the EFT's UV meaning).
- **G2.3 UNDECIDED** within the EFT.
- **G5.1** possible FAIL from P_XX < 0 at X < 0. **G5.4** FAIL for the unscreened BK reading (a fifth force at 1 AU about 10⁴–10⁵ over the ephemeris ceiling per the prior pricing script, and composition-dependent); the phase boundary does not screen (same environment).
- **G6 FAIL:** e = 0 (condensed) against e → 1 (Newtonian regime), even with the BTFR granted.
- **The most likely overall verdict is a scoped no-go for Branch S** (a barotropic-plus-flow condensate with the phonon coupling does not produce C(r); the phase change is a loophole in B2's hypotheses but it costs the BTFR postulate, per-halo boundaries and an unfunded injection). **Branch F is expected to be a force restatement** that fails on shape and does not fill the missing object. A surprise is possible only in G1.1 through the full nonlinear X (the μ − mΦ term is comparable with the gradient term exactly at the crossover), which is why the coupled solution is computed and not argued.

## Verdict rules (declared)

- **Survives G1 (Branch S, universal (m, α)):** the door goes on to G2–G6, and the orchestrator is asked for an independent re-derivation (gate rule 5). Every failed sub-gate is listed as a cost.
- **Branch F passes G1.3 only:** "force restatement; missing object not filled; lensing unresolved". Not counted as a survivor.
- **Otherwise:** "scoped no-go" with the exact hypotheses (NR, static, spherical, the P(X) and coupling as written, the plane, the T = mσ² convention), and the loopholes (d) that remain.
- **κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour the framework, and nothing here says the theory is closed.**

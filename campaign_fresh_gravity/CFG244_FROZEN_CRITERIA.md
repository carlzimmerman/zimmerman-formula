# CFG244 -- the bound part of an early cold fluid as the owner of the law's dark density: frozen criteria (phase 1; written before any CFG244 script or number)

Lane: `campaign_fresh_gravity/CFG244_*`. To be committed as `campaign_fresh_gravity/CFG244_FROZEN_CRITERIA.md` before phase 2. All paths are relative to the repository root (`<repo>`).

Standing statements (binding on every sentence of phase 2): no closure is claimed; kappa = 1/2 stays FITTED; there is NO dark-matter particle and no new species -- the candidate is a pressureless, conserved, collisionless FLUID (an order-parameter or mode, as in the record), and **the MASS is still required**: the class takes Omega_c h^2 = 0.1200 as an input and supplies none of it. A scoped no-go is a valid result and is not a theorem. A lean is not a detection. Nothing here says any data favour or disfavour the framework or LambdaCDM.

---

## 0. What was read, and the not-blind statement

**Read (committed repository; whole unless marked):**
- `campaign_fresh_gravity/CFG242_closure_swing/README.md`, `CFG243_turnaround_dust/README.md` (the premise: ownership needs memory; the cold mass must exist before structure forms; the CFG243 COSMIC failure, 0.1200 x 10^-1376.8 at z = 1100), `CFG243_FROZEN_CRITERIA.md` (head and section 0 only, for format).
- `closure_map/TEN_DOORS_GATES_2026-09-29.md` (G1-G5, copied below), `closure_map/WHAT_WOULD_DECIDE_2026-09-29.md`, `closure_map/GATES.md` (grep lines 1.02, 3.10, 4.06 only).
- `CFG230_requirements_synthesis/CFG230_README.md` (sections 1-8: R01-R12; R01 window |p - 1/2| <= 0.0291 outer / 0.0145 inner at +-10%; R07 bound-only switch).
- `CFG118_FROZEN_CRITERIA.md`, `CFG118_secondary_infall/README.md` (whole), the docstring of `CFG118_secondary_infall.py` and the function/entry-point grep of `shellcore.c` (the C kernel's outputs include each shell's final r, v and j^2, so a z = 0 energy is computable); `CFG158_infall_referee/README.md` (whole).
- Satellite and UFD lanes, READMEs only: `CFG28_README.md`, `CFG29_README.md`, `CFG30_README.md` (head), `CFG35_README.md`, `CFG42_README.md`, `CFG45_README.md`, `CFG46_README.md` (head), `CFG51_README.md` (head), `CFG58_README.md` (head), `CFG59_README.md`, `CFG66_README.md` (head), `CFG69_README.md`, `CFG73_README.md`, `CFG74_README.md`, `CFG78_ufd_rederivation/README.md`, `CFG83_ufd_luminosity_trend/README.md` (head), `CFG91_satellites_rederivation/README.md`, `CFG92_field_dwarfs_rederivation/README.md` (head), `CFG222_lcdm_proxy/README.md` (head); `STANDING_2026-09-29.md` by grep only (UFD, satellite, "Arm C" lines).
- Code read for the plan only (no outputs): the import/def/path grep of `CFG69_lcdm_comparator.py` and lines 40-110 of `CFG42_satellites_rule.py` (data loader, host baryonic masses, sample names).

**NOT opened in phase 1:** every per-galaxy residual output (`.out`, `_results.json`) of CFG28, 29, 42, 45, 46, 51, 58, 59, 66, 69, 78, 83, 91, 92 and every `CFG118`/`CFG158` product file; the raw satellite tables were not opened either. All Gate H numbers below are the READMEs' aggregate values.

**Cited at second hand only (not read here):** CFG64 (kernel robustness), CFG67 and CFG77 (KiDS colour split), CFG93 (multi-epoch referee), CFG63 (forecast caps), CFG4 (RAR scatter bound), CFG44 and CFG48 (the target construction), `shellcore.c` beyond its entry points.

**Not-blind statement (binding).**
1. I read the record's UFD failure of B before fixing anything: the isolated law under-predicts the Milky Way ultra-faint dispersions by +0.325 / +0.304 dex (canonical / alt), 3.77 / 3.55 sigma on the 40 (31 resolved + 9 upper limits, Kaplan-Meier), robust to censoring, tides, noise and published binary bounds (CFG28, CFG29), and shrinking to 1.0-1.8 sigma on eight binary-corrected systems (CFG46, CFG78) and standing at +0.22 / +0.47 dex on two multi-epoch systems (CFG51, CFG66, with CFG93's caveats). **That failure may favour the bound-fluid reading** (an NFW-like core), and I also read CFG69's committed LambdaCDM-comparator offsets (UFD +0.080, 0.6 sigma; MW classical -0.029, -0.4 sigma; M31 LVD -0.062, -1.3 sigma). Gate H's expected outcome is therefore partly a restatement of aggregates already in the record, not an independent forecast. What phase 2 adds is one scoring rule applied to both readings, the frozen decision lines below, the EFE reading (which the record lists as "not in hand"), and the planted-sample power check.
2. I read CFG118 and CFG158 whole: the bound classification of Gate A is a new cut, but CFG118's measured ratios (C_infall/C_target 1.0-4.2 at x about 1, 0.05-0.21 at x about 28, local ratios 4-360 at x about 0.1) and the radial exponents (0.32-0.35, turnaround 0.333) are known to me. Gate A's hand estimates restate them.
3. CFG243's COSMIC gate is passed by premise (the fluid is present at recombination); it is not tested here.

**Arithmetic done in phase 1 (calculator only, none kept as a claim):** the chi-square sums of the aggregate sigmas (section 3), 10^0.5 = 3.162, the window log10(1.1/0.9)/3 = 0.0291, the host Newtonian field of a 6e10 Msun point at 30 / 100 / 250 kpc in units of a0 (0.099 / 0.0089 / 0.0014), the QUMOND-style boost nu(P2) at those fields (3.33 / 10.6 / 26.5), and the effect of that field on a 2e4 Msun, 30 pc UFD at 100 kpc (0.014 dex; 0.0006 dex for 1e5 Msun) -- which **corrected a wrong first guess of mine** that the external field would raise the UFD offset by several tenths of a dex: it does so only for satellites closer than about 50 kpc and by at most about 0.2 dex there. Items marked "(memory)" are from memory, unverified.

---

## 1. The model class, as equations

**Premise (from CFG242/CFG243).** Ownership needs memory; the cold mass must exist before structure forms. The one memory a conserved collisionless fluid carries for free is orbital boundness. The class is the cheapest construction that has both: the cosmic cold fluid, present from before recombination.

**The early cold fluid.** A pressureless, conserved, collisionless fluid with Omega_c h^2 = 0.1200 (CMB-safe by construction; CFG243 COSMIC and CFG242 R05 are met by premise, not by any result here), obeying the Vlasov-Poisson system in the Newtonian limit with Lambda (the regime of every gate below):
- for fluid element i: r_i'' = -G M(<r_i)/r_i^2 + (Lambda c^2/3) r_i + j_i^2/r_i^3, with M(<r) = M_b(<r) + M_c(<r) (baryons plus all fluid inside r, a shell feeling half its own mass, as CFG118);
- initial data: the Hubble flow at z_i = 100 plus the baryon core's perturbation (as CFG118).

**The bound part.** At the epoch where the law is evaluated (z = 0), with the instantaneous potential Phi_eff(r) = Phi_N(r) - (Lambda c^2/6) r^2 and r_s the outermost radius where G M(<r_s)/r_s^2 = (Lambda c^2/3) r_s:
- element i is BOUND iff E_i = v_i^2/2 + j_i^2/(2 r_i^2) + Phi_eff(r_i) < Phi_eff(r_s);
- M_c,bound(<r) = sum of the masses of the bound elements inside r; rho_c,bound(r) its density.
(Classification choice and the reason are in Gate A below.)

**The ownership statement (what the class asserts).** The law's dark density inside a system is the bound part of the early cold fluid bound to the outermost bound system containing the point:
rho_dark(r | system S) = rho_c,bound(r).
Total acceleration is Newtonian, g_tot = G [M_b(<r) + M_c,bound(<r)] / r^2. **There is no separate law in the class.** The law g_tot = nu(g_N/a0) g_N with the P2 kernel nu = sqrt(1 + a0/g_N), a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED, enters only as the TARGET the bound fluid is asked to reproduce:
C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r) (CFG44; point mass: M_c = M_b (sqrt(1 + x^2) - 1), x = r/r_M, r_M = sqrt(G M_b/a0)); footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s^2, both reported, never pooled.

**What solves for what.** Given a baryon distribution and the cosmological initial data, the Vlasov-Poisson evolution fixes rho_c(r, z = 0); the classification fixes rho_c,bound; the comparison to the target is a TEST, not an equation. Nothing is fitted. In a system that sits inside a host, the instantaneous classification gives the fluid bound to the satellite's own well (it is also bound to the host, because the satellite is); the "outermost owner" bookkeeping and the dynamics therefore disagree inside a satellite unless the satellite owns nothing, and Gate H is the test of which one the data follow.

**Constants ledger (beyond kappa = 1/2 and Omega_c h^2 = 0.1200).** None are fitted in this lane. Declared inputs: the Planck 2018 cosmology of CFG118 (H0 = 67.4, Omega_m = 0.315, f_b = Omega_b/Omega_m = 0.157), shared with LambdaCDM; the baryon core (a static point mass softened at 1e-3 r_M; the exponential sphere h = 2, 3, 4, 5 kpc), the three angular-momentum brackets q = r_peri/r_ta = 0.05, 0.1, 0.2 and z_i = 100 (initial-condition choices inherited from CFG118, never tuned; a PASS depending on them would count against G4); for Gate H, declared FUNCTION SHAPES external to the class: the Moster+2013 stellar-to-halo relation as coded in h48 (`halo_mass`, clamped at 1e9 Msun below M_* about 1.6e4, as CFG42/CFG69), the Duffy+2008 200c concentration, an NFW profile, Upsilon_V = 2. **The class cannot supply the collapse mass of a satellite from its own constants** (the baryon loss that sets M_coll/M_b is feedback physics it does not contain): at satellites it is "LambdaCDM with a declared SHMR". That is stated, not hidden.

**Mapping to the shared gates.** Gate H is the hierarchy / bound-only reading (R07, with CFG28-CFG59's satellite populations); Gate A is G1 and R01/R03 (amount, shape, scale); Gate D asks what the class predicts that LambdaCDM does not. G2 (cold at z >~ 10) is met by premise, G3 (Newtonian gravity, reaction and energy), G5 (collisionless CDM, Cassini-safe) hold as statements, not tests. Shared gates, copied (from `closure_map/TEN_DOORS_GATES_2026-09-29.md`):
G1 target within 10% over x in [0.1, 30] for baryon masses 1e9-1e12 Msun with the same constants at every mass; G2 CMB and growth; G3 reciprocity <= 0.10 g_law and energy; G4 no constant beyond kappa and Omega_c h^2; G5 well-posed, Solar-System safe.

---

## 2. The gates, their ORDER, and the exact pass lines

**ORDER (part of the freeze): H, then A, then D.** H first because it is the cheapest (aggregate arithmetic on committed populations, under 5 minutes) and it decides whether the route is B or a different law; A second (shell simulations, about 10 minutes); D last (bookkeeping against committed forecast tables).
**STOP RULE:** stop at the FIRST binding FAIL and report it as a scoped no-go on the frozen class. Later gates are run only as clearly labelled POST-HOC extras (file names carry `_POSTHOC`, outputs say so, and no verdict depends on them). If everything passes, an independent re-derivation is run BEFORE reporting (Gate H by an independent re-implementation of the three-population scoring; Gate A by an independent shell code, as CFG158 was for CFG118).

### Gate H -- HIERARCHY (satellites)

**Question.** Is a satellite's own bound cold mass present or absent? Score both readings by ONE rule on the record's own populations and error model.

**The two readings (frozen exactly).**
- **(b) "satellites keep their bound core".** The bound fluid's mass is declared by this rule, frozen before any residual: M_coll from the Moster+2013 relation of h48 at M_* = Upsilon_V L_V (Upsilon_V = 2, clamp 1e9 Msun below M_* about 1.6e4); the bound cold mass is (1 - f_b) M_NFW(<r; M_coll) with the Duffy+2008 full 200c concentration, f_b = 0.157, no adiabatic contraction, no SHMR scatter, no phantom; g_tot = G [M_b,enc + (1 - f_b) M_NFW(<r)] / r^2 (Newtonian, nu = 1). This is the record's LambdaCDM comparator (CFG69) run through the identical estimator; the class has no other rule for the collapse mass (the identity "cold mass bound within r_M(sat) = M_b (sqrt(1 + x^2) - 1)" is the target itself, i.e. reading (a1) below, not a separate reading).
- **(a) "satellites own nothing"**, scored at its best of three declared variants, the variant with the lowest chi-square being (a):
  - (a1) the isolated law of the satellite's own (infall) baryons: the record's B reading of CFG28/CFG42 (called L there);
  - (a2) the law with the host's external field only: g_int = g_N,int nu(sqrt(g_N,int^2 + g_N,host^2)/a0), g_N,host = G M_host / d^2 for a point host (baryonic masses MW 6.0e10, M31 1.2e11 Msun as in CFG42/FG001; d = the table's distance_host, else distance_gc) -- an angle-averaged quasi-linear EFE rule (from memory, unverified; AQUAL/QUMOND numerical EFE not covered);
  - (a0) the literal Arm-C wide-binary logic extended to satellites: no phantom at all, internal dynamics Newtonian from the baryons (nu = 1).
  The record's own satellite scoring is (a1); (a0) and (a2) are strictly worse for UFDs by arithmetic, so choosing the best of the three is the choice least favourable to (b).
- **Reported, never in the verdict:** the record's sum rule S (law + collapse debris; CFG42/CFG45), which is a hybrid of (a1) and (b) and not a reading of this class.

**Kernel.** Primary nu = P2 (the class's kernel). The record's numbers used the exponential RAR kernel nu = 1/(1 - exp(-sqrt(y))); it is run as the CONTROL (reproduction) and as a sensitivity (CFG64: P2 moves these rows by at most 0.01 dex). If the two kernels land in different verdict categories the lane reports the more cautious category (AMBIGUOUS).

**Sample (frozen).** Three populations, N = 88 systems, no system twice:
- P1 MW ultra-faints: 40 systems (31 resolved dispersions + the 9 upper limits by Kaplan-Meier; M_V > -7.7 cut and the other cuts as FG001/CFG28);
- P2 MW classical dSphs: 14 systems (infall gas as CFG18's expectation, as CFG42);
- P3 M31 LVD: 34 systems.
Reported rows outside the sum (overlap or non-satellite): M31 Collins+13 (14; 13 shared with P3), Bootes I and Tucana II multi-epoch cleaned (subsets of P1), CFG46's eight binary-corrected systems (subset of P1), the 13 LV field dwarfs (top-level, no host: a control where both readings are expected to fit), SLUGGS / X-ray ellipticals / S0 / UGC 2487 (hosts: Gate A territory, not satellites). CFG30's binary galaxies and the Gaia wide binaries are not used.

**Statistic (the same for both readings).**
- offset delta_{p,m} = median over population p of log10(sigma_obs / sigma_pred,m), with the record's estimator sigma^2 = g(r) r / 3 at r = (4/3) r_half, half the baryons enclosed, isotropic, single radius, no Jeans model, no anisotropy parameter (as the record), distances and sizes taken from the table as given (the 0.14 dex source swing of CFG91 is a reported sensitivity, not a nuisance in the verdict); P1's median is Kaplan-Meier with the 9 limits.
- error e_{p,m}^2 = e_stat,p^2 + e_floor,p,m^2: e_stat as the record's committed recipe (CFG28/CFG42: bootstrap for the KM median, 1.2533 rms/sqrt(n) for the others; 2000 resamples, seed 244001); e_floor = the half-range of sigma_pred,m over the reading's declared free inputs, **treated by one rule for both**: Upsilon_V in {1, 2, 4} (and for (a1) the deep-MOND estimator, as CFG28's 0.077 dex) for every reading, plus, for (b) only in view V1 below, the collapse-mass scan M_coll in [1e8, 1e10] Msun for P1 (the record's 0.133 dex total).
- chi2_m = sum over the three populations of (delta_{p,m}/e_{p,m})^2. Delta = chi2_a - chi2_b (positive favours the bound core). Zero free parameters in either reading (all inputs fixed at declared values), so no parameter penalty is needed; threshold Delta chi2 = 9.
- **Two views (both always computed; this is the same rule with the nuisance range of (b)'s halo mass treated two ways):** V1 = the record's own error model (the collapse-mass floor included for (b)); V2 = equal floors (Upsilon_V range only for both readings). V1 can only be kinder to (b) than V2, so a preference for (b) must survive V2 and a preference for (a) must survive V1.
- Both footings (canonical, alt) always computed; (b) does not depend on the footing; a verdict requires the same category on both footings, otherwise AMBIGUOUS.

**Decision lines (exact).**
- **H1 -- binding FAIL (satellites own nothing is preferred):** Delta_V1 <= -9 on both footings. The bound-fluid reading is contradicted at satellites; scoped no-go on the class; the route is B-like and the class is wrong there.
- **H3 -- binding FAIL ("neither"):** Delta_V2 >= 9 on both footings but reading (b) is not acceptable on its own: some population has |delta_{p,b}|/e_{p,b} >= 2 in V1 on the canonical footing, or chi2_b(V1) > 11.34 (p = 0.01, 3 dof). Named with the population and the offset in dex. Scored as shared with the LambdaCDM comparator (CFG69) and never as framework-specific.
- **H2 -- PASS, the route is a DIFFERENT LAW from B at satellites:** Delta_V2 >= 9 on both footings and (b) acceptable as defined in H3. Meaning: the bound-fluid core is preferred over "satellites own nothing" in this machinery, B's committed dwarf reading (the isolated law, 3.8 sigma on the UFDs) is the disfavoured one, and the class at satellites is the LambdaCDM comparator with a declared SHMR. This is not a lean for the framework; it is a statement that the route and candidate B are different at satellites.
- **H4 -- PASS, AMBIGUOUS:** anything else (|Delta| < 9 in the relevant view on either footing, mixed categories, or kernel disagreement). The satellites do not separate the route from B; the lane continues to Gate A.

**Robustness rows (reported, none changes the verdict):** collapse-mass scan x0.1 / x0.3 / x3 / x10 and the clamp at 1e8 / 3e8 / 1e9 / 3e9 / 1e10 for (b); Dutton-Maccio concentration; the CFG91 error recipe (bootstrap SE plus Upsilon propagated into the halo and infall gas); Upsilon_V = 1 and 4; Collins+13 in place of the overlapping part of P3; the binary-corrected eight, Bootes I, Tucana II rows; leave-one-population-out; the M_V luminosity trend of the UFD offsets under each reading (CFG83: flagged only on eight systems, model-independent); host off for (a2). Reading the table: with p = 3 populations the Delta chi2 is carried by P1 (the UFDs, whose aggregate gate is weakly diagnostic for an NFW halo: it passes over about four decades of halo mass, CFG69/CFG73/CFG74); that is stated in the output next to the verdict.

### Gate A -- AMOUNT (the bound part of a collapsed cold fluid against C(r))

**Question.** Does the bound part of a collapsed cold fluid, with secondary-infall / turnaround physics and no tuning, reproduce C(r) = (a0/4 pi) M_b(<r)? Or only LambdaCDM's approximate relation?

**Code.** Import CFG118's `shellcore.c` READ-ONLY (compiled at run time into a temporary directory, as CFG118 does) and re-create its set-up from the frozen CFG118 text; add a new classification and analysis layer. No repository file is edited. Independence: CFG158 (Julia, independent code) agreed with CFG118's set-up to 5e-4, the cumulative-mass envelopes to the noise and the exponents to 0.01, so a second code is not re-run unless every sub-test passes (the stop rule).

**Simulation (frozen, from CFG118).** N_s = 20,000 shells (5,000 for the resolution check); baryon masses 1e9, 1e10, 1e11, 1e12 Msun; primary geometry the softened point core, secondary the exponential sphere (h = 2, 3, 4, 5 kpc); q = 0.05, 0.1, 0.2 (all reported; no bracket chosen after the fact); z_i = 100 on the Hubble flow; smooth non-clustering Omega_b background; the core present and static from z_i; shells out to 3 r_ta(z = 0); Newtonian with Lambda. The simulation does not depend on a0; the footing enters only the target. **Secondary-infall footings declared:** F1 a static core present from z_i (the baryons' assembly history is an untested hypothesis); F2 the smooth baryon background; F3 spherical symmetry with the three brackets; F4 start at z_i = 100; F5 extent 3 r_ta; F6 softening 1e-3 r_M; F7 N_s. A pass resting on any of these counts against G4.

**Bound / unbound classification (frozen: ONE rule).** Instantaneous: E_i at z = 0 in the z = 0 potential (including the Lambda term, and Phi_N from the snapshot's enclosed masses with half-own-mass self-gravity), bound iff E_i < Phi_eff(r_s). Why instantaneous: the law and the class's ownership are statements about the present dark density; a "final potential" does not exist in a class that has no model of future infall; and the memory claim ("bound stays bound by energy conservation in a static potential") is a statement about a potential that is NOT static here, so the flip fraction is measured rather than assumed. Reported (not a verdict input): (i) the "ever turned around" flag from the kernel's turnaround record as the alternative classifier; (ii) the BOUNDNESS-FLIP fraction, the share of shells inside x <= 30 classified bound at their last turnaround epoch whose z = 0 classification differs; (iii) the bound fraction of the fluid mass inside x in [0.1, 30].

**Sub-tests, each with exact numbers (all point cores, both footings; the PASS needs all three).**
- **A1 local amount.** C_bound/C_target on CFG118's 25 bins of 0.1 dex (x = 0.1 to 31.6; the same binned estimator for model and target): |ratio - 1| <= 0.10 on every bin with centre in [0.1, 30], for every mass, for at least one bracket q used at every mass, on both footings.
- **A2 cumulative amount.** R_cum(x) = M_c,bound(<r)/M_c,target(<r), M_c,target = M_b (sqrt(1 + x^2) - 1): R_cum in [0.90, 1.10] for every x on a 0.1-dex grid over [0.3, 30], every mass, same bracket logic, both footings (the cumulative mass converges to a median 2% at x about 28 between 5,000 and 20,000 shells in CFG118, so this is the noise-robust line; the inner x < 0.3 holds fewer than about 1 shell per bin and is not scored cumulatively).
- **A3 radial scale versus mass.** R_s(M_b) = the radius where M_c,bound(<r) = M_b (target: x = sqrt(3), i.e. R_s proportional to r_M proportional to M^(1/2)); least-squares exponent p of log R_s on log M_b over the four masses, per bracket. PASS: |p - 1/2| <= 0.0291 (CFG230 R01's outer window at +-10%). The reading "the scale follows the turnaround, M^(1/3)" is scored as: |p - 1/3| <= 0.05 AND |p - 1/2| > 0.10.
- A FAIL of A1 or A2 counts as binding only if the deviation from the pass band exceeds the larger of the shell-bootstrap sigma and |R_5k - R_20k| at that bin (the noise guard CFG118's failed C3 motivates). A3's exponent difference between 5,000 and 20,000 shells is reported (CFG118: within 0.02).

**Binding failure named by the lane:** "the bound cold mass's radial scale goes as M^p with p = ... (turnaround, 1/3), not 1/2; C_bound/C_target = ... at x about 1 and ... at x about 28". If instead the exponent passes and the shape fails, the failure is named as the shape.

**The new-ingredient rule.** If A fails, the only continuation is a labelled POST-HOC extra A-ext: add a baryon-coupled relaxation (a growing baryon core, i.e. adiabatic contraction with an assembly redshift and time scale, or baryon-driven mass segregation). It must be NAMED as the NEW INGREDIENT, its constants (assembly redshift, time scale, any coupling) are counted against G4 unless tied to Lambda or kappa in the same action, it is scored separately and never pooled with the main verdict, and no verdict depends on it. A-ext is not part of the stop-rule path and is run only on the orchestrator's request.

### Gate D -- DISTINCTNESS (where does this route differ from LambdaCDM?)

**What it asks.** Where, if anywhere, the route predicts something LambdaCDM does not. **"Reduces to LambdaCDM plus the a0-Lambda coincidence" means, operationally:** for every observable in the frozen list below, |P_route - P_LCDM| < the stated threshold (the route's prediction is the LambdaCDM comparator's by construction or within noise), and the only content the route adds is the numerical statement a0 = kappa c sqrt(G rho_Lambda) with kappa FITTED, which in this class enters no equation and is therefore a coincidence it neither explains nor tests.

**Candidate observables, route prediction, LambdaCDM prediction, scoring (frozen).** Route values come from the Gate H / Gate A outputs where they exist; LambdaCDM values from the record's committed comparators or, where stated, (memory, unverified). "DISTINCT" for an observable needs |P_route - P_LCDM| >= 2 sigma_cap, with sigma_cap the committed forecast cap of the cited lane (or 0.05 dex for a model-to-model comparison with no cap).
- **D1 the tie as a coincidence.** Route: a0 does not enter; the route's own bound-fluid RAR has a mass-dependent best-fit scale (from Gate A: the spread of the fitted a0 across 1e9-1e12 in dex). LambdaCDM: the same spread (it is the same fluid). Scored: spread_route vs the committed RAR intrinsic-scatter bound 0.043-0.048 dex (95%, CFG4 H4, `closure_map/GATES.md` row 1.02). NOT DISTINCT from LambdaCDM if both exceed it.
- **D2 a0(z) at z about 2.5.** Route: the bound halo's density scale follows the collapse epoch, i.e. the LambdaCDM-native expectation (+0.334 dex at z = 2.5; sensitivities +0.45 and +0.50, CFG222/CFG63), NOT the flat law (0.00) and NOT a0 proportional to H(z) (+0.58). LambdaCDM: the same by construction. So the route is NOT DISTINCT from LambdaCDM and is DISTINCT from candidate B (0.33 dex; committed cap 1.3 sigma against LambdaCDM-native, 2.3 against H(z), CFG63, so non-diagnostic today). The flat a0(z) law is the framework's distinctive prediction and this class does not make it.
- **D3 satellites.** Route = reading (b) = the LambdaCDM comparator by construction (difference 0 dex); distinct from B by the Gate H numbers.
- **D4 RAR scatter at fixed g_bar.** Route: the spread of log10(C_bound/C_target) across brackets q and masses from Gate A (dex). LambdaCDM: expected to exceed the 0.048 dex bound ((memory, unverified): published LambdaCDM-based RAR scatters are of order 0.1 dex or more). If A fails, the route's scatter is the infall's and is not distinct from LambdaCDM's.
- **D5 profile shapes.** Route: the bound outer slope (EdS self-similar -9/4 in CFG118's C2; the target's rho_c goes 1/r to 1/r^2) against the NFW outer slope -3 (LambdaCDM): the route's profile IS the LambdaCDM halo-formation profile without feedback; not distinct, apart from the baryon core.
- **D6 Gaia DR4 wide binaries.** Route: Newtonian (the bound fluid is smooth on binary scales), gamma-hat = 1.000, the same as LambdaCDM and as candidate B's Arm C; only the bare law (1.16) differs. NOT DISTINCT from LambdaCDM.
- **D7 KiDS colour split.** Route: halo masses follow stellar mass and colour as in LambdaCDM (the colour-split reading fits, CFG67); B and any model with a negligible predicted difference at fixed g_bar fail it at face value (CFG77). NOT DISTINCT from LambdaCDM.
- **Verdict.** DISTINCT iff at least one observable D1-D7 is DISTINCT from LambdaCDM and the route's value there is derived (from Gates A/H) and not tuned; otherwise REDUCES TO LAMBDACDM PLUS A COINCIDENCE. If Gate A somehow passes, D4 and D5 are scored with the route's simulated profile against the committed target and the LambdaCDM comparator and can become DISTINCT.

---

## 3. Frozen hand estimates (made before any run; wrong ones will be kept and disclosed)

All made with the knowledge listed in section 0, so several restate the record; where they do I say so. Arithmetic from the aggregate sigmas of CFG42/CFG69 (P1, P2, P3): chi2_a1 = 3.77^2 + 0.32^2 + 0.60^2 = 14.7 (canonical), 3.55^2 + 0.09^2 + 0.42^2 = 12.8 (alt); chi2_b(V1, CFG69's errors) = 0.60^2 + 0.4^2 + 1.3^2 = 2.2; so Delta_V1 about +12.5 canonical and +10.6 alt.

**Gate H**
- E-H1: P(Delta_V2 >= 9 on both footings, i.e. the route is a different law from B at satellites) = **0.56**; the margin is thin: expected Delta_V2 about +12 (canonical) and about +10 (alt) with an uncertainty of about 4, because the alt footing's UFD offset is 0.02 dex smaller. Rests on CFG42/CFG69 aggregates (not independent).
- E-H2: P(H1: Delta_V1 <= -9 on both footings) = **0.01** (it would need the data to move the UFD median by more than 0.3 dex). P(H3: (b) fails its own acceptance) = **0.08** (the LVD, at -1.3 sigma nominal and -2.2 sigma under Dutton-Maccio, is the likely one). P(H2) = **0.48**, P(H4 ambiguous) = **0.43**.
- E-H3: the best (a) variant is (a1) with P = 0.9; (a2) differs from (a1) by +0.01 to +0.08 dex in the UFD median (P = 0.8; the host's Newtonian field is 0.009 a0 at 100 kpc and 0.1 a0 at 30 kpc, and nu falls as the argument grows); (a0) UFD offset >= +0.8 dex (P = 0.85; Newtonian sigma of a 1e5 Msun, 30 pc UFD is about 1.8 km/s against 3-5 observed, and lower for fainter ones).
- E-H4: (b) acceptable in V1 canonical (all three |z_b| < 2): P = **0.85**; the planted-sample controls (below) are expected to show an ASYMMETRIC power: P(H2 | truth = (b)) about 0.7, P(H1 | truth = (a1)) about 0.03, because in V1 the collapse-mass floor makes (b)'s errors larger; this is a known property of the frozen decision lines (H1 is reached only if even the view kind to (b) prefers (a)), stated in the output.
- Note plainly: the UFD failure of B (3.5-3.8 sigma) is the quantity that makes P1 carry the Delta; a gate that passes an NFW halo over four decades of halo mass discriminates only against a reading that sits +0.3 dex off, which is what (a1) does on the UFDs; it does not measure the satellites' halo masses.

**Gate A**
- E-A1: P(A1 and A2 and A3 all pass) = **0.005**.
- E-A2: bound fraction of the fluid mass inside x in [0.1, 30] at z = 0 is >= 0.99 (P = 0.90; the turnaround radius is x_ta = 193 / 132 / 90 / 61 for 1e9-1e12, far outside 30); classifier "ever turned around" differs from the instantaneous one by < 1% there (P = 0.85); boundness-flip fraction < 5% (P = 0.6; the potential grows during infall).
- E-A3: R_cum(x about 1.1) in [1.0, 4.5] and R_cum(x about 28) in [0.25, 0.70] over the brackets and masses (P = 0.7 each; restates CFG118/CFG158); local C ratio at x about 0.11 >= 2 for point cores (P = 0.8, noisy bins).
- E-A4: exponent p of R_s on M_b for point cores lies in [0.29, 0.38] (P = 0.90; CFG118: 0.32-0.35; CFG158: 0.33-0.34); **P(|p - 1/3| <= 0.05 and |p - 1/2| > 0.10) = 0.90; P(|p - 1/2| <= 0.0291) = 0.01.** The implied R_s/r_M spread across 1e9-1e12 is 10^(3 x (1/2 - p)) = about 3.2 for p = 1/3 (CFG230's x_ta spread 3.165) against the 1.22 that the 10% line allows (1.1/0.9).
- E-A5: the three controls most likely to fail again, as they did in CFG118/CFG158: the 5,000-vs-20,000 local-bin control (P(pass at the frozen 10%) = 0.3) and the EdS slope (not re-run here).

**Gate D**
- E-D1: P(D finds at least one observable DISTINCT from LambdaCDM) = **0.07** (0.5 if Gate A had passed, which it is not expected to); D2, D3, D6, D7 are NOT DISTINCT by construction (P = 0.95 each); D1 and D4 NOT DISTINCT if A fails (P = 0.9).

**Expected binding failure:** **Gate A**, sub-tests A2 and A3, with P = 0.90 overall (P(H1 or H3 binds first) = 0.09, so Gate A is reached with P = 0.91 and fails with P = 0.99 given that; P(everything passes) = 0.003). The number behind it: the bound mass's radial scale follows the turnaround, M^(1/3) (p about 0.33), so the ratio to the target drifts by a factor of about 3.2 across 1e9-1e12 at fixed x, and at fixed mass C_bound/C_target falls from about 1-5 at x about 1 to about 0.05-0.2 (local) / 0.28-0.66 (cumulative) at x about 28 (CFG118, CFG158).
**Expected status of controls:** all reproduction controls pass at first run P = 0.55; at least one noise-limited control fails as in CFG118 (C3) and CFG158 (C2-C4) P = 0.6.

---

## 4. MUTATE controls and robustness checks (each flips a load-bearing cell; expected outcome stated before any run)

Exit convention: a MUTATE run exits 1 when the control bites (its target cell flips) and 0 when it does not; the expected code is printed beside the observed one.

| id | change | target cell | expected |
|---|---|---|---|
| MH1 | swap the two readings' labels in the scoring | Gate H verdict (Delta changes sign) | bites (exit 1) |
| MH2 | every observed dispersion x 0.5 (the record's own MUTATE; every offset moves by exactly log10 2 = -0.30103) | Gate H verdict: P1 gives about +0.02 / -0.22 dex for (a1) / (b), the P2 and P3 offsets move to about -0.27 to -0.36, so Delta turns strongly negative | bites (exit 1) |
| MH3 | turn the host off (g_N,host = 0, so (a2) = (a1)) | the (a2) UFD offset cell (a2 >= a1 + 0.01 dex) | bites on that cell (exit 1); does NOT change the verdict because the best-of-three picks (a1) -- stated in advance |
| MH4 | plant a fake satellite sample with known cores: 200 mock data sets per truth using the real systems' L_V, r_half, host distances, with sigma_obs drawn from the truth reading's prediction times a log-normal scatter of the record's per-population error (truth (b), truth (a1)); run the full Gate H pipeline | the verdict category differs between the two plants | bites (exit 1); also prints P(H2 | truth b), P(H1 | truth a1), P(H4 | each) -- the power table; expected about 0.7 and 0.03 |
| MH5 | collapse mass of (b) divided by 100 for every satellite | the (b)-acceptable cell: P1's z_b leaves |z| < 2 (the record: the comparator gate fails at x0.01) | bites (exit 1) |
| MA1 | Gate A evaluator fed the target's own bound profile (R = 1) | A1/A2/A3 flip FAIL -> PASS (the evaluator can pass) | bites (exit 1) |
| MA2 | Gate A: no baryon core | bound mass inside x <= 30 about 0 (CFG158 M1: no turnaround at all); the bound-fraction cell flips | bites (exit 1) |
| MA3 | Gate A: replace the target's scale r_M by a length proportional to M^(1/3) | A3 flips FAIL -> PASS (the exponent line has bite on the exponent, not on the amplitude) | bites (exit 1) |
| MA4 | Gate A: classify by "ever turned around" instead of the instantaneous energy (the "final versus instantaneous potential" check, labelled ROBUSTNESS) | the bound-fraction cell inside x <= 30 | expected NOT to bite (exit 0; P(bites) = 0.15): kept as a declared non-biting control |
| MA5 | Gate A: Lambda removed from the classifier (E < 0 in Phi_N alone) | the unbound fraction of shells outside x about 60 (the saddle matters only there) | bites on that outer cell (exit 1); does not touch x <= 30 |
| MD1 | Gate D: plant "route = LambdaCDM comparator" and "route's a0(z) = flat" | the D verdict flips REDUCES <-> DISTINCT | bites (exit 1) |

Reported, never verdicts: Gate H robustness rows (section 2); Gate A exponential-sphere rows; the 5,000-shell run; the boundness-flip fraction.

---

## 5. Script plan

All names `CFG244_*`, in `campaign_fresh_gravity/CFG244_lane/` (a new directory at phase 2). Each script prints `<repo>` for the repository root (found from `ZF_REPO` or by walking up from `__file__`) and never an absolute home path; no absolute path is hard-coded (CFG91/CFG92/CFG83 carry that defect and are not repeated); outputs go to the lane directory only; the repository is read, never written. Exit convention: a main run exits 0 (the verdict is in the output and the JSON, FAIL included); a MUTATE run exits 1 when the control bites, 0 when it does not; `CFG244_run_all.sh` prints the frozen expected code next to the observed one and ends with `unexpected outcomes: N`. Each run under 15 minutes.

- `CFG244_common.py` -- repo discovery, the committed constants (a0 footings), report/JSON helpers, the host table; imports CFG7_common read-only the way CFG42 does.
- `CFG244_H_satellites.py` -- Gate H: loads the three populations through the record's loader (FG001/CFG42 slices exec'd read-only), builds readings (a0), (a1), (a2), (b), the two views, both footings, both kernels, the robustness rows; controls C-H1 (the record's exponential-kernel offsets reproduced: CFG42 UFD +0.325 / +0.304, classical +0.027 / +0.008, LVD +0.044 / +0.031; CFG69 LambdaCDM UFD +0.080, classical -0.029, LVD -0.062, to 0.005 dex), C-H2 (Newtonian limit M_coll -> 0 and nu = 1 in closed form), C-H3 (deep-MOND limit, closed form), C-H4 (EFE limits: g_host -> 0 returns (a1) to 1e-12; g_host -> infinity returns nu -> 1), C-H5 (the labelled swap changes the sign of Delta); MUTATE=MH1..MH5. Budget: under 5 minutes (mocks vectorised).
- `CFG244_A_infall_bound.py` -- Gate A: compiles CFG118's `shellcore.c` into a temporary directory, runs the shells (processes from `CFG244_NPROC`, default 8), classifies, scores A1-A3, the robustness rows, the boundness-flip fraction; controls C-A1 (CFG118's set-up reproduced: M_ta/M_b = 23.63 for point cores within the CFG158 line 20.1-27.1, r_ta(z = 0) = 236 / 508 / 1095 / 2358 kpc within 1%), C-A2 (no core: every shell on the Hubble flow to 1e-6), C-A3 (resolution: cumulative R at x about 28 between 5,000 and 20,000 shells within 10%), C-A4 (a test shell in a static softened point mass: energy drift < 1e-3 and the classifier returns bound for E < 0 and unbound for E > 0), C-A5 (the evaluator on the target, MA1); MUTATE=MA1..MA5. Budget: up to 14 minutes on 8 processes; if the machine is loaded the exponential-sphere runs are dropped first (a labelled departure), never the point cores.
- `CFG244_D_distinctness.py` -- Gate D: reads the committed forecast tables and the Gate A/H JSON outputs; builds the D1-D7 table; MUTATE=MD1. Budget under 1 minute. Run only after Gate A passes; after an A FAIL it is run as `CFG244_D_distinctness_POSTHOC.py` (the same code, output labelled POST-HOC).
- `CFG244_verdict.py` -- reads the gate JSONs in order, applies the stop rule, prints which gate bound and the named failure.
- `CFG244_run_all.sh` -- runs H, then A (only if H did not bind), then D or D-POSTHOC, then every MUTATE, then the verdict. Outputs per script: `.out`, `_results.json`, and `_MUTATE_<id>.out` / `.json`.
- Seeds frozen: bootstrap 2000 resamples, seed 244001; mocks 200 per truth, seed 244002.

---

## 6. What counts as a pass, and as a scoped no-go

- **Class PASS (the whole path):** Gate H ends in H2 or H4; Gate A passes A1, A2 and A3 on the point cores on both footings; Gate D finds an observable DISTINCT from LambdaCDM; then an independent re-derivation is run and reported BEFORE anything else. A pass would still say nothing about closure, kappa = 1/2 stays FITTED, and the cold mass is still required.
- **Scoped no-go (a valid result):** the first binding FAIL on the frozen class, named: H1, H3, or the Gate A sub-test with its number (for example "the bound cold mass's scale goes as M^p, p = ..., not 1/2; C_bound/C_target = ... at x about 28"). It is a statement about spherical secondary infall of a Vlasov-Poisson cold fluid onto a static baryon core with the declared brackets and the instantaneous classifier, not a theorem.
- **If H2 and A fails (the expected path):** the class at satellites is a bound-core (LambdaCDM-like) reading, the route is a different law from candidate B there, and at hosts it does not reproduce the target; with D showing REDUCES, the honest label is "LambdaCDM plus an a0-Lambda coincidence that enters no equation", which is a statement about this class, not about candidate B.
- Wrong expectations and failed controls are kept in the README, never repaired. A lean (for example Delta chi2 between 4 and 9, or a 2-sigma population offset) is reported as a lean.

---

## 7. What is NOT covered

Non-spherical collapse, mergers, tidal torques and tidal stripping of satellites (reading (b) is the unstripped halo); a growing baryon core, adiabatic contraction and feedback (A-ext only, post-hoc); warm, self-interacting or fuzzy cold fluids; any angular-momentum distribution other than the three brackets; the Boltzmann (CMB) evolution of the early fluid and the cosmic amount itself (premise); relativistic completion and G5 beyond the statement; the hosts of CFG59 (SLUGGS, X-ray ellipticals, S0, UGC 2487) and the field-dwarf and KiDS rows beyond the labelled reported rows; numerical (AQUAL/QUMOND) EFE solutions (reading (a2) is an angle-averaged approximation, from memory, unverified); dispersion anisotropy and Jeans modelling (the record's single-radius estimator is used unchanged in both readings); distance and size systematics as nuisance parameters (reported only); the SHMR's physics (a declared function shape); non-ownership readings of the early fluid; whether any bound/unbound classifier in a time-dependent potential is the "right" ownership (one rule is frozen and one alternative reported). Literature facts marked "(memory)" are unverified.

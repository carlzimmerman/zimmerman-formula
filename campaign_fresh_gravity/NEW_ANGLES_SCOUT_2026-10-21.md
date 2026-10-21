# New angles scout (2026-10-21)

**What this is.** A read-only, fresh-eyes scout for attack angles the record has not tried on the four hardest open problems. No
lane was run, no file other than this one was written, and no CFG ID is taken: IDs are the orchestrator's to assign. The only
numbers produced here are hand arithmetic on committed numbers; they are labelled as such and carry no verdict weight (appendix).

**Settings.** κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 m s⁻² are never pooled. Cold energy is real gravitating mass,
not a particle species. Verdicts must be raw-data and framework-native. Not theory closed. Nothing here says the data favour the
framework.

**Sources read.** LEDGER rows CFG799–CFG962; THEORY_CANONICAL_2026-10-18.md (with its dated notes) and the 2026-10-21 v4 draft;
FRIED_CHICKEN.md (status 2026-10-21); explainers/crispy_fried_chicken_status_board.md; what_is_time/README.md; the READMEs of CFG596,
CFG636, CFG646, CFG650, CFG654, CFG687, CFG888, CFG909, CFG953 and CFG960; the data inventory in real_research/data and
_external_data.

**In flight, so not proposed here.**
- CFG960: the SCT-M 1024³ shear run is live.
- CFG961: checks WT-02 and WT-05.
- CFG962: SCT-U clusters (SCT + retention + body stripping).
- CFG924: the aperture-mass recheck.
- WT-06 to WT-09: response time, the time structure, the repaired parent, and stiffness with c_T = c.

## Bottom line (candid)

1. **The dwarf/UDG excess and κ are close to exhausted.** About 70 lanes (CFG822–959) have closed the obvious mechanism classes:
   tides, binaries, estimators, EFE, M/L and age, gas loss, capture, supply floors, selectors, mobility, energy limits and
   unrelaxed debris. For κ there are 451 registered attempts. No new κ angle survived pre-flight. For the dwarfs only one theory
   angle survived (NA-3), and it derives the clump's *size* from L*, not its *mass*.
2. **The one finding with immediate consequences concerns problem 2, and it comes from committed numbers alone.** The KiDS lead of
   theory-v2 over its control is carried by the M3 gas-expulsion module, which the control does not have.
   - T12 (M1+M2, no M3) scored Δχ² +2.03 against S0.
   - T1x (M1+M2+M3, same inherited ICs, same S0) scored −7.70.
   - CFG646 measured M3 alone as ×0.977 / 0.966 / 0.950 at k 0.3 / 0.5 / 1. T1x's whole benchmark is ×0.974 / 0.965 / 0.949.
   - Against a control with the same expulsion (S0 + M3), theory-v2 would sit near Δχ² ≈ 0 to +3: still CONSISTENT, but with no
     lead. The A2/A3 "HOLDS iff Δχ² ≤ 0" reading would most likely fail.
   - So the shear data would say little about the parentless parts of the engine (relocation, RMIN, global phantom). Problem 2
     becomes a **boost budget**: a parent passes if its own boost at k 0.3–1 stays within about 0–4% of plain dust.
   - This must be confirmed (NA-1) before anything is re-worded. Any change to published wording (PAPER56 calls NCS0 the
     "matched control"; it is matched in ICs, not in baryon expulsion) is the owner's call.
3. Three smaller survivors: a calibrated halo-model screen for parents (NA-2), a same-system two-tracer test in four gas-rich
   dwarfs (NA-4), and the framework's own catalogue two-halo term for the cluster outer slope (NA-5).

## Ranked survivors

Score = P(real advance) × decisiveness ÷ cost; the factors are qualitative.

| rank | ID | problem | angle | P(advance) | decisiveness | first-test cost | new constants |
|---|---|---|---|---|---|---|---|
| 1 | NA-1 | 2 (shear parent) | **Feedback-matched control.** Score the shear pass against S0 + M3 instead of S0 | high (~0.8 that the lead is M3's) | high: changes what problem 2 is | minutes, < 1 GB, stored spectra | 0 |
| 2 | NA-2 | 2 + 3 | **Boost-budget screen.** A halo model of B(k,z), calibrated on the six scored 1024³ runs, triages parents (SCT-M, SCT-U, LDT) before any 1024³ run and shows which host-mass range carries B − 1 | medium (~0.5) | high for triage | ~1 h, < 300 MB | 0 |
| 3 | NA-3 | 1 (+ L*) | **Stiffness-bound cold lump.** Untethered self-gravitating dust plus the record's stiffness pressure πGL*²ρ² is an n = 1 polytrope of fixed radius πL*/√2 ≈ 2.22 L*. This gives a derived clump size and a second, independent L* measurement | low–medium (~0.25) | medium–high (yields L* or kills the link) | derivation + CFG880 refit, hours, < 500 MB | 0 (uses L*); one structural assumption |
| 4 | NA-4 | 1 | **Same-system two-tracer test.** Stellar σ against the HI rotation curve inside the same dwarf (WLM, IC 1613, DDO 210, DDO 216) | low–medium (~0.25) | medium (system vs tracer property) | minutes, < 100 MB | 0 |
| 5 | NA-5 | 3 (outer slope) | **Catalogue two-halo term around eRASS1 clusters.** Applies CFG903's no-free-amplitude machinery to CFG687's T2 slope (M_gas^0.90 vs the law's 0.47) | medium (~0.4) | medium (a ~2σ sub-problem) | ~1 h, chunked reads < 1 GB | 0 |

---

## NA-1. Feedback-matched control for the shear pass (problem 2)

**The idea.** Theory-v2 = M1 (per-host supply) + M2 (condensed source) + M3 (census gas expulsion). Its control S0 / NCS0 is plain dust
with no expulsion. CFG596's README says "no baryonic feedback in either arm", but that stopped being true when M3 was added to the
framework arm only.

The committed numbers already decompose the lead:
- **T12** (M1+M2): own boost B = 1.005 / 1.012 / 1.023 at k 0.3 / 0.5 / 1. KiDS Δχ² **+2.03** (CFG650).
- **T1x** (M1+M2+M3): **−7.70** (canonical; alt T2x −7.18), with P/P_S0 0.974 / 0.965 / 0.949.
- **The M3 factor** has been measured four independent ways, all agreeing to ≈ 1–2%:
  - T1x/T12: 0.969 / 0.954 / 0.928;
  - the CFG650 256³ preview: 0.973 / 0.950 / 0.923;
  - CFG646's PM post-process: 0.977 / 0.966 / 0.950;
  - CFG960 at 128³ (M3 on/off): 0.976 / 0.947 / 0.943.
- **A second fingerprint:** NC1x's deficit grows from 5% at z = 0 to 11% at z = 1 (k = 1). CFG646 found expulsion "deeper at
  z 0.5–1".

**(i) Record pre-flight.**
- CFG909 traced the size of the lead to amplitude, "not a shape preference". It never split it by module and never asked whether
  the control should carry M3.
- CFG646 measured M3 as a few-percent effect, but only on the framework arm.
- CFG917 and CFG927 (CMB lensing) compare against the same unmatched control.
- No lane ran S0 + M3, and no lane attributed T12 → T1x to M3.

**(ii) Why it is new.** It changes the comparison, not the model. M3 is the framework's own baryon sector (census f_ret, catchment
r_ON); it is generic expulsion physics that any cosmology also has. A like-for-like control isolates what the law's engine adds.
The control remains framework-native: it uses the record's own M3 code, not HMcode or BAHAMAS.

**(iii) Cheapest decisive first test.**
- **Stage 1 (minutes, one core, < 1 GB).** A CFG909-style re-score (`cfg909_rescore.py` already re-scores stored P(k,z) nodes):
  - score NC1x and NC2x against NCS0 × F_M3(k,z), using three declared brackets: T1x/T12 (the 1024³ inherited pair, at the stored
    z nodes), the CFG650 256³ ratio, and CFG646's PM factors;
  - K check: T1x against T12 × F must return Δχ² ≈ 0 by construction;
  - MUTATE: F ≡ 1 must return CFG654's −10.08 / −9.39 exactly.
- **Stage 2 (after the live 1024³ chain; owner approval).** A native S0 + M3 run (NCS0 with M3 on, same ICs) to measure F on plain
  dust directly. A 256³ S0 vs S0 + M3 ratio check is the cheaper version; it needs ~3 GB, so it too waits for the chain.
- **Timely.** CFG960's SCT runs also carry M3 (VSC/VSA = M3 on) and are scored against NCS0. A reported-only fair-control
  sensitivity for SC1x/SC2x can be frozen now, before they land, as CFG909 did for NC2x. CFG960's frozen files are not touched.
- **Expected outcome** (hand arithmetic, appendix A1):
  - NC1x/(NCS0 × F) has mean ≈ 0.996–1.011, which maps to Δχ² ≈ −0.6 to +2.8;
  - the lead becomes a tie;
  - the class stays CONSISTENT.

**(iv) What kills the angle.** Δχ²(NC1x, NC2x vs NCS0 × F) ≤ −4 on both footings in all three F brackets. The law's engine would
then still beat a feedback-matched control, and the pass would stand as a result about the law's engine.

**(v) New constants.** None. F comes from committed runs.

**What it changes if it holds.**
- The shear pass becomes a statement about census gas expulsion. M3's gas placement is separately CONSISTENT with FRB dispersion
  measures (CFG632).
- The pass is no longer a statement about the class-A relocation, RMIN or the global phantom.
- "The engine behind the shear pass has no parent" then matters much less for the shear tile. The open requirement becomes the
  boost budget (NA-2).

## NA-2. Boost-budget screen: a calibrated halo-model B(k,z) for candidate parents (problems 2 and 3)

**The idea.** Six 1024³ results map the own boost B onto KiDS Δχ²:

| run | mean B, k 0.3–1 (z = 0) | Δχ² vs S0 |
|---|---|---|
| CFG596 | 1.215 | +68.7 |
| CFG636 C1 | 1.057 | +13.97 |
| T12 | 1.013 | +2.03 |
| T1x | 0.963 | −7.70 |

NC1x and NC2x, against their own control, add two more points.

Near B = 1 the response is linear: Δχ² ≈ 230 × (mean B − 1). The fit's zero falls at B = 0.999, a sanity check, since B = 1 means
identical spectra (appendix A1).

This gives a **budget**:
- tying S0 needs mean B_eff ≲ 1.00;
- the EXCLUDED line (Δχ² 9) sits near B_eff ≈ 1.04;
- with M3 (mean F ≈ 0.95–0.96), a parent's own boost must stay ≲ 1.04–1.05 to tie S0, and ≲ 1.00 to tie a fair control (NA-1).

A halo model that reproduces the measured B of these runs from their declared rules can then predict any parent's B(k,z) in an hour,
without an 18–30 h, ~45 GB run. Transplant scoring, as in NA-1, turns that B into a predicted Δχ².

**(i) Record pre-flight.**
- CFG646 already has a halo-model estimate for expulsion (0.974 / 0.964 / 0.956 canonical, close to the PM's 0.977 / 0.966 / 0.950).
- No lane built a calibrated B-budget or used one to screen parents.
- CFG952 found that the engine's effective RMIN applies the law only to hosts with retained baryons ≥ 2.19e11 M☉.
- CFG932 Q4 found that the engine fills deficits only. Together these imply the scored engine is close to plain dust at group and
  cluster scale, which is consistent with CFG949's untethered clusters.

**(ii) Why it is new.** It turns the parent problem into a quantitative design constraint and a cheap triage tool. It also says which
host-mass range carries B − 1: galaxies, groups (10^12–10^13.5) or clusters. Groups are the regime with the weakest direct tests
(CFG543's outcome turns on unmeasured hot gas; CFG745 groups in TENSION).

**(iii) Cheapest decisive first test (~1 h, one core, < 300 MB).**
- The halo model takes: native σ(M) and Δ_ta (CFG654), the CFG930 concentration rule, the census f_ret ramp, the M3 placement, and
  each run's declared settling rule.
- Calibrate against the measured B(k,z) of CFG596, CFG636 C1, T12, T1x/T2x and NC1x/NC2x at z = 0, 0.5 and 1.
- Then compute, labelled as reported expectations:
  - SCT-M, both CFG960 variants, frozen *before* SC1x lands;
  - SCT-U (CFG962), before it commits to any 1024³ run;
  - LDT (CFG952's design).
- Caution: the 128³ SCT-M preview (mean B_eff 1.093) maps to ≈ +22 on the crude linear response. That preview is resolution-limited
  (domain floor ~1e12, bodies painted compact), so this is **not** a forecast of CFG960. It is the reason an hour of calibration is
  worth spending before SC1x is read.

**(iv) What kills it.** The halo model misses the measured B of the calibration runs by more than 2% at k 0.3–1 and z 0–1, or its
transplant Δχ² ordering disagrees with the six scored runs.

**(v) New constants.** None. Brackets on concentration and placement are declared as systematics, not fitted.

## NA-3. The stiffness-bound cold lump: clump size from L* (problem 1, obligation 11)

**The idea.**
- **The ingredients.** CFG939 gives every medium element the forces −∇Φ_b + R(K|P|)P̂ − γ∇ρ_c, with γ = 2πGL*².
  - Tethered medium: no self-gravity (theorem D-T, CFG941).
  - Untethered dust: self-gravitates (SCT-M R0; CFG946; CFG959's retained dust).
- **Hydrostatic balance.** If untethered dust also carries the stiffness, a cold lump obeys γ∇ρ = −∇Φ_self. That gives
  ∇²ρ + (2/L*²)ρ = 0: an n = 1 polytrope, ρ ∝ sin(kr)/(kr) with k = √2/L*.
- **Fixed radius.** The edge is at R = πL*/√2 ≈ 2.22 L*, whatever the mass. The half-density radius is 1.34 L*. The mass is
  M = 4π²(L*/√2)³ρ_c ≈ 14 L*³ρ_c.
- **Read against the record's description:**
  - CFG870's core r_c = 104 pc gives L* ≈ 78 pc;
  - CFG877's edge r_t ≈ 200 pc gives L* ≈ 90 pc;
  - at ρ_c 0.6 M☉ pc⁻³ the mass is 3.9–6.1e6 M☉, the CFG877 clump scale;
  - both L* values lie inside the allowed window [24 pc (CFG820), ~2.04 kpc (CFG832)];
  - all of this is hand arithmetic (appendix A3).
- **Consistency points (reasoning, not results):**
  - a fixed-radius lump with free mass is exactly the structure CFG880 fitted (r_c fixed, σ_x free per dwarf);
  - it fits CFG857 (no size dependence of the extra speed);
  - it fits CFG876 (large dwarfs over-predicted by an extended component);
  - it fits CFG883 (no clump at globular radii: a lump cannot be smaller than ~2.2 L* ≥ 53 pc).

**(i) Record pre-flight.**
- CFG888 S4 shows the stiffness is a local pressure πGL*²ρ_c² that "cannot bind anything". That holds in the canonical action and
  under the identification, where the clump has no self-gravity.
- CFG888's record branch was a σ-supported Newtonian isothermal, finite only with a truncation (one more parameter).
- CFG858: stiffness only screens the law's boost.
- CFG871/877: law-linked core, CONDITIONAL on an unwritten coupling.
- No lane combined untethered self-gravity with the stiffness pressure. That combination gives a finite lump with no truncation in
  the cold limit.

**(ii) Why it is new.**
- It replaces the conditional law-linked core (CFG871, not derived per CFG888) with a size derived from the record's own force law.
- It gives L*, which is bounded but not derived (obligation 11), a second determination independent of the globulars.
- It does **not** explain the lump's mass; the supply problem of CFG823/930/959 remains.

**(iii) Cheapest decisive first test.**
- **Part A (derivation only).** Does untethered dust feel −γ∇ρ in any record formulation? Check CFG939's single-medium map (P is
  the whole medium's displacement), CFG848's two-population functional, class A, and SCT (whose rules R0–R9 contain no stiffness).
  If yes, solve the lump inside a host potential: a forced Helmholtz problem.
- **Part B (minutes, < 500 MB).** CFG880's hierarchical likelihood on the 83 LVD dwarfs, with sin(kr)/(kr) lumps, one global L* and
  mass free per dwarf. Compare against CFG877's capped isothermal and CFG871's law-linked core (ΔBIC). Report L*_dwarf with its 95%
  interval.
- **Declared out-of-sample checks:** the CFG876 large dwarfs, Sextans' two populations (CFG884, PROVISIONAL extraction), and SPARC
  hiding (CFG881).

**(iv) What kills it.** Any one of:
- Part A finds no formulation in which untethered dust carries the stiffness;
- L*_dwarf's 95% interval lies below 24 pc or above 2.04 kpc;
- sin(kr)/(kr) is worse than CFG877's shape by ΔBIC > 10;
- one L* cannot serve the compact dSphs and the large LVD dwarfs together (z > 3).

Sextans' extended mass to ≥ 1.67 kpc (CFG884) already argues against a single ~200 pc lump. That is the most likely failure, so
Part B must report it.

**(v) New constants.** None (L* is already a record constant). One structural assumption is added: untethered dust carries the
stiffness. Per-dwarf masses stay descriptive, as in CFG880.

## NA-4. Same-system two-tracer test in gas-rich dwarfs (problem 1)

**The idea.** "Every excess system is pressure-supported, no rotator has one" compares *different* systems. In a dwarf that has both a
stellar dispersion and an HI rotation curve, one potential is traced twice:
- if the stellar-σ law residual at r½ exceeds the HI-curve residual at the same radius, the excess is a tracer or estimator property;
- if both agree, it is a property of the system's mass.

Data on disk:
- LVD stellar σ: WLM 17.5, IC 1613 10.8, Aquarius (DDO 210) 7.8, Pegasus dIrr (DDO 216) 12.3 km/s;
- Oh+2015 LITTLE THINGS curves for all four (in the CFG442 directory);
- SPARC's UGCA 444 (= WLM) as a curve bracket.

By hand estimate, DDO 210 and DDO 216 sit near g_bar ≈ 10^−12 at r½, at the edge of the excess region.

**(i) Record pre-flight.**
- CFG874 (isolated dwarfs, stellar, gas counted): E +0.194 ± 0.077.
- CFG873: HI-bearing dwarfs +0.46 stars only, +0.23 with gas.
- CFG931: up to 4 LITTLE THINGS faint rotators, "INFO 3/4 on the law".
- CFG442: LITTLE THINGS curves sit +0.196 dex off SPARC for the same dwarfs (failed overlap control).
- No lane compared the two tracers inside one system.

**(ii) Why it is new.** It is the only test that holds the system fixed and changes the tracer, so it separates the "pressure-supported
system" reading from a "stellar-dispersion tracer" reading. CFG919/921/928 all rest on that distinction.

**(iii) Cheapest decisive first test (minutes, < 100 MB).**
- Compute D_i = E_star,i(r½) − E_HI,i(r½) for the four dwarfs, on both footings, with ν as in CFG874 and gas counted with the
  CFG874 convention.
- Correct for stellar rotation: WLM's stars rotate, so use v_rms or f_P.
- Bracket the HI side with Oh+2015 and SPARC wherever both exist.

**(iv) What decides it, and what kills it.**
- |D̄| < 0.1 dex: a system property.
- D̄ > 0.2 dex at ≥ 2σ: a tracer effect.
- **Kill (NOT DIAGNOSTIC):** the WLM Oh-vs-SPARC curves differ by > 0.15 dex at r½, or the asymmetric-drift corrections for DDO 210
  and DDO 216 move E_HI by more than the expected D.
- With N = 4 this is a pointer, not a verdict.

**(v) New constants.** None.

## NA-5. The framework's catalogue two-halo term around eRASS1 clusters (problem 3, outer slope)

**The idea.** CFG687's T2 measures ΔΣ_OUTER ∝ M_gas^0.90 ± 0.21, against the law's 0.47 and Newton's 0.84. A_OUTER by gas tercile runs
0.57 → 0.96 → 1.38. CFG687 named environment below X-ray detection, i.e. a two-halo term that grows with mass in any theory, as an
open mechanism, but tested only X-ray neighbours.

CFG903 built the framework's own no-free-amplitude catalogue two-halo term:
- KiDS-bright neighbours, each carrying baryons plus catchment cold energy;
- random-subtracted;
- used for isolated lenses (CFG903) and for the red/blue split (CFG912).

It has never been applied to the 318 clusters. The per-cluster stack is on disk (`CFG687_erass1_shear_stack/cfg687_percluster.npz`:
ΔΣ, errors, the law and Newton predictions, M_gas, z, positions).

**(i) Record pre-flight.**
- CFG687 post-hoc: X-ray neighbours do not explain T2; isolated clusters give s 0.85.
- CFG816/817: the Eddington correction is small and the middle tercile is real.
- CFG949: untethered clusters give s 0.661, "not discriminating".
- CFG962 (in flight) is a theory lane for cores and merger memory, not an environment term.

**(ii) Why it is new.** The record's own neighbour machinery, applied to a data set it has not seen, decides mechanism (b) for T2 with
zero constants.

**(iii) Cheapest decisive first test (~1 h, chunked reads < 1 GB).**
- Run CFG903's term around the 318 positions.
- Exclude neighbours inside each cluster's own edge, so nothing double counts the cluster's gas and law term.
- Add the term to CFG687's law prediction, then recompute s, the terciles, A_OUTER and A_MID.
- Declare a completeness bracket for the flux-limited bright sample.
- Carry CFG687's random-minus-random OUTER offset (+0.13 ± 0.06) as a systematic.

**(iv) What kills it.** The term moves s by < 0.1 (T2 stays "follows Newton"), or it closes the gap only in a double-counting bracket.

**(v) New constants.** None.

---

## Dropped after pre-flight (kept, so they are not re-proposed)

| ID | angle | (i) lanes that tried something similar | (ii)/(iii) why dropped | (iv) kill already met | (v) constants |
|---|---|---|---|---|---|
| X-1 | **ALFALFA width RAR at the HI edge** (a100 W50 × Durbala+20 b/a and M★, R_HI from Wang+16): the missing low-g faint-rotator lever, with HUDs as the rotating-UDG control | CFG931 (HUDs: "no resolved radius"), CFG940 (McQuinn: none below 1e-12), CFG873/874 (Wang+16 for gas). The ALFALFA–SDSS tables have not been used in a lane | The size–mass slope (0.506) fixes the mean HI surface density, so **g_bar(R_HI) ≈ 10^−11.7 at every HI mass** (appendix A4). That is above the excess region (dwarfs +0.44 dex below 10^−11.9, CFG828), where SPARC already sits on the law to its floor. As an a0 rung, inclination and turbulence systematics (~0.1 dex) exceed CFG833's 0.049 dex pin threshold | cannot reach g_bar < 1e-12 | 0 |
| X-2 | **Cluster-core excess split by dynamical state or redshift** (eRASS1 F300kpc/F500, z) | CFG687 terciles; CFG815–817 (mass–z degeneracy, Eddington) | Its sign follows from no framework rule: CFG959's u = f_P is time-independent, and a relaxation clock would be a new rule. The law prediction uses a β-model scaled to M_gas500, so cool cores bias it. About ±0.17 per half; z is degenerate with mass in a flux-limited sample | low power, sign not derivable | 0 (+1 rule) |
| X-3 | **Native abundance matching for the dwarf supply** (native σ(M) × LG counts → f_ret(M), then CFG45's sum reading) | CFG35/42/45 (Moster masses: close the UFDs, over-predict the classicals −1.8 to −2.7σ); CFG934/937 (floors fall short); CFG806 (f_ret not derived); CFG886 (floor not traceable); CFG932 (L = 100 needed) | Native ICs use Planck ω_c and A_s, so native σ(M) ≈ the σ(M) behind CFG42's masses and the result would reproduce CFG42. Interpolating between CFG42 and CFG934 is a knob | ≈ CFG42 | ≥ 1 (scatter, ramp) |
| X-4 | **Gravothermal (Bonnor–Ebert) instability as the dwarf concentrator** (turning CFG955's failure into the mechanism) | CFG955 (the bath-held law profile is BE-unstable in NGC 3198, e-fold 0.21–0.25 Gyr; "excess unreachable at any τ"); CFG848 (microcanonical: wrong sign for dSph-like systems, collapse only with compact baryons) | It would put excesses into rotators (NGC 3198 is unstable), against CFG919 | CFG955 | 0 |
| X-5 | **SCT-M baryon–body offsets heating gas-free systems** (dissipation as the selector) | CFG953 cost 6 (undamped offsets; toy 0.7 r_P) | Hand argument: in a rigid body potential the Wolf mass measures the actual potential. Offset stars sample lower body density (tidal trace −4πGρ_body), so equilibrium σ goes *down*. Transients phase-mix in ~10⁸ yr. Wrong sign, short-lived | wrong sign | 0 (+1 rule) |
| X-6 | **Fossil a0 at conversion under the owner's damped wave** (old dwarfs latched while a0 was high; young dwarfs and clusters unaffected) | CFG926 R4 (fossil a0: framework zero or wrong sign; rival PARTIAL, dwarf age slope z −1.9); CFG956 (z 3–5 window ε ≤ 2.46 at β 0, ≤ 3.22 at β 2, extrapolated); CFG957 (no physical model in the framework; a light scalar with 2 constants; the ε reading is monotone); CFG827 (excess age-independent) | The mean excess needs a0(z_f)/a0(0) = e^{4×0.38} = **4.57**; CFG956 allows at most ≈ 3.5–4.2 (appendix A5). It also needs a new latch rule (a0 frozen at conversion while the body reshapes) and R4's kinematic re-settle selector. Suggestive but unscored: Fornax, Leo I and Carina, which have extended SFHs, carry the least excess (CFG853, CFG892) | amplitude short; 2 constants + 2 rules | ≥ 2 |
| X-7 | **κ angles:** (a) κ from the dSph common-mass "acceleration floor" (M(<300 pc) ≈ 1e7 M☉ gives g ≈ 0.17 a0); (b) κ via SCT bodies' E_int and the dark-energy store | CFG894 (451 attempts, P_LEE 0.20); CFG890 (acceleration-like forms rejected, ΔBIC +39); CFG893 (c-free dynamics cannot fix κ); CFG958 (the channel is κ-free; cosmic ceiling \|Δ ln a0\| ≤ 3.6e-4) | (a) is a menu number with no second prediction; (b) carries no κ information. **No κ angle survived.** Recommendation: no new κ lanes until a route offers a second, independent prediction (CFG894's rule) | — | — |

## Already tried, do not repeat

| tempting idea | lanes | verdict |
|---|---|---|
| Present-day or pericentric tides make the satellite excess | CFG838, CFG839 | NO SIGNAL |
| The excess is a host or satellite property | CFG843, CFG860, CFG873, CFG874, CFG875 | SAME / NOT GAS / UNDECIDED; "satellite property" withdrawn |
| Unresolved binaries | CFG861, CFG892 (and CFG51/93) | PARTIAL; only Carina reachable |
| Wolf vs Jeans estimator, anisotropy | CFG925 R1 | NO EFFECT (radial corners at most −0.114) |
| Include the framework's EFE | CFG925 R3 | WORSENS (+0.48 dex on satellites) |
| Cold energy in the law's own argument / double counting | CFG925 R2, CFG722, CFG888 | WORSENS / rejected / NOT DERIVED |
| Stellar M/L, age (H-FOSSIL), free Υ | CFG824 → CFG827, CFG890 | the age trend was M/L; excess age-independent; free Υ leaves 0.47 |
| Gas loss, stripping, metallicity deficit, H-EX in dwarfs | CFG822, CFG846, CFG852, CFG860, CFG920 | negligible / NO PATTERN / NO SIGNAL / NOT GAS / UNDERDETERMINED |
| Fossil a0 (flat or DE-tracking) | CFG926 R4 | zero or wrong sign (only the rival helps) |
| Capture of host cold energy | CFG842 | Liouville ceiling 1e-8 to 1e-5 of the need |
| Free cold core collapsed at assembly (H-PRIM) | CFG844 → CFG845 | EXCLUDED by SPARC small rotators (z −10.4) |
| Collapse debris with Moster masses (sum, max, exterior readings) | CFG35, CFG42, CFG45 | closes the UFDs, over-predicts the classicals; no reading passes all seven gates |
| Energy-limited settling (H-ELS) | CFG930, CFG932 | CONTRADICTED; energy ordering backwards |
| Cooling-floor and filtering-floor halos | CFG934, CFG937 | PARTIAL, FRAGILE; intermediate dSphs not closed |
| Unrelaxed native debris, u = f_P | CFG959 | clusters and red lenses yes; dSphs and UDGs fall *below* the law (debris/phantom 0.24) |
| Universal temperature floor / extended atmosphere | CFG876 | BROKEN |
| Finite clump with a law-linked core and universal σ | CFG870, CFG871, CFG877, CFG880, CFG884, CFG888 | empirical; NOT DERIVED; NOT UNIVERSAL (s_int 0.38); Sextans needs ≥ 1.67 kpc |
| Clump retention by the deficit gate | CFG882 → CFG889 | ERODED once orbits mix (t_50 105–148 Myr/α) |
| Fragment dynamical-friction transport; lump granularity | CFG853 | EXCLUDED; persisting lumps overheat stars ×66–1.4e4 |
| Maximum-entropy tethered/free partition | CFG848 | wrong sign / ill-posed |
| Stiffness alone making the extra speed | CFG858 | ONLY SCREENS (NA-3 differs: self-gravity plus stiffness of *untethered* dust) |
| Universal extra speed; symbolic regression | CFG854, CFG856, CFG857, CFG859 | SPARC-compatible only; no formula validated |
| One density threshold; one kinematic selector | CFG914, CFG919 | NO COMMON ORDERING; SELECTOR CONTRADICTED |
| One-constant selectors (stress coupling, velocity-space capture, late binding, phase-space capture, QUMOND geometry) | CFG921, CFG928, CFG933 | none survives all facts; P2's sealed UDG prediction sits 2.4–2.6σ the wrong way |
| One mobility law, history labels, lock-and-release | CFG913, CFG915, CFG916 | INFEASIBLE / CONTRADICTED / UNDERDETERMINED |
| Late binding against the framework's clock; ×4.3 formation baryon loss | CFG920, CFG923 | UNDERDETERMINED / the clock binds too early |
| Bound outer-envelope receiver | CFG918 | BROKEN for four dwarfs; only escape is left |
| Photo-evaporation selector | CFG782, CFG834 | DEAD |
| No-capture criterion for the Coma UDGs | CFG948 | the framework allows at most the law; Newton excluded at 5.45σ |
| Faint rotators below g_bar 1e-12 from data on disk | CFG931, CFG940 (and X-1 above) | NOT DIAGNOSTIC (DATA) |
| A local parent of S2 + S3 | CFG938, CFG941 | no linear self-gravity (theorem D-T); satellite hover |
| A collapse-gated tether | CFG944 | ghost; theorem G |
| Cold energy ≠ phantom (separate sector) | CFG946 | NO-GO (lemma L-G: a field-supplied deep law carries an EFE) |
| An exact non-local parent of class A | CFG947 | NO-GO (T-M relocation, T-R RMIN, T-X global-phantom EFE) |
| Labelled domains | CFG945, CFG950, CFG951, CFG952 | CONDITIONAL; mergers and clusters FAIL; engine RMIN 2.19e11 M☉ |
| SCT-M / SCT-Q | CFG953, CFG954 | galaxy-scale CONDITIONAL; clusters FAIL; SCT-Q INCONSISTENT; 1024³ test = CFG960 (live) |
| A kinetic (relaxing-dust) parent | CFG955 | NO KINETIC PARENT (post hoc); BE-unstable |
| An energy sink, the dark-energy channel | CFG935, CFG958 | needs a sink outside matter; C-E converted, not derived |
| Cold→DE conversion to lower growth | CFG780 | WORSENS T1x (still CONSISTENT) |
| Neighbour-bounded edge, energy-bounded settling, phase-mixed settling | CFG644, CFG645, CFG648 | RULED OUT / NOT DERIVABLE / FAILS |
| The cluster core as a baryon-census error (stars, gas normalisation, HSE bias, clumping, Eddington, IMF, HI) | CFG922 | EXCESS STANDS |
| Small cluster reframings (every ν, QUMOND superposition, line of sight, cooling module) | CFG929 | none resolves it |
| Hot gas untethered, H-EX pooled or split, census or outskirt retention | CFG727, CFG745, CFG808–CFG815 | eRASS1-only passes; FAIL on all 318 + ACCEPT; middle tercile ×1.6 is real (CFG817) |
| Splashback or unrelaxed placement for the middle tercile; frozen relic; supply overflow | CFG818, CFG819, CFG777, CFG721 | NULL / fails before scoring / FAIL 0/3 / FAILS |
| Untethered clusters at the cosmic ratio | CFG949 | EXPLAINS at the primary corner only, FRAGILE (6/40) |
| SCT + retention + stripping for clusters | CFG962 | being launched by the orchestrator |
| κ derivations (horizon, vacuum, stiffness FRW, drift causality, nodal medium, Festina Lente, c-term census, constructive couplings, why-4) | CFG891, CFG893, CFG894, CFG897, CFG898, CFG900, CFG904, CFG905, CFG908, CFG911; why_4_puzzle W4-01..18; the 32π campaign | κ = ½ FITTED; none derives it |
| Closed forms for 5.364 | CFG642, CFG831, CFG855 | CHANCE-LEVEL / ORDINARY |

---

## Appendix: hand arithmetic (no verdict weight)

**A1. Boost budget and the M3 factor** (committed numbers; k = 0.3 / 0.5 / 1 h/Mpc, z = 0)
- **Mean B against KiDS Δχ² vs S0** (canonical, inherited ICs, control without M3):
  - CFG596: 1.2147 → +68.70;
  - CFG636 C1: 1.0567 → +13.97;
  - T12: 1.0133 → +2.03;
  - T1x (alt benchmark): 0.9627 → −7.70.
- **Linear fit** on C1, T12 and T1x: slope 229.5 per unit B, zero at B = 0.9988. A quadratic through all four also crosses zero at
  1.0018.
- **The M3 factor, four ways:**
  - T1x/T12: 0.9692 / 0.9536 / 0.9277;
  - CFG650 256³ (M1+M2+M3)/(M1+M2): 0.9731 / 0.9497 / 0.9234;
  - CFG646 PM post-process: 0.977 / 0.966 / 0.950;
  - CFG960 128³ (M3 on/off): 0.9759 / 0.9465 / 0.9430.
- **NA-1 expectation.** NC1x mean ratio 0.9607 against NCS0; divided by F's mean (0.9502 for T1x/T12, 0.9643 for CFG646) this gives
  1.011 / 0.996, which maps to Δχ² ≈ +2.8 / −0.6.

**A2. The SCT-M 128³ preview.** Mean B_eff = 1.0933 maps to ≈ +22 on A1's line. The preview is resolution-limited and says so, so this
is not a forecast.

**A3. The n = 1 stiffness polytrope.**
- The stiffness pressure is P = (γ/2)ρ² = πGL*²ρ², so K = πGL*².
- Lane–Emden for n = 1 gives α² = K/(2πG) = L*²/2, the edge R = πα = 2.221 L*, the half-density radius 1.8955 α = 1.340 L*, and the
  mass M = 4π²α³ρ_c.
- From r_c = 104 pc: L* = 77.6 pc, R = 172 pc, M(0.6 M☉ pc⁻³) = 3.9e6 M☉.
- From r_t = 200 pc: L* = 90.0 pc, M = 6.1e6 M☉.

**A4. g_bar at the HI edge.**
- log D_HI = 0.506 log M_HI − 3.293 (kpc, at 1 M☉ pc⁻²).
- Take g_bar = G × 0.9 × 1.33 M_HI / R_HI² (gas only; the 0.9 is the enclosed fraction).
- log M_HI 7 / 8 / 9 / 10 gives R_HI 0.89 / 2.84 / 9.12 / 29.2 kpc and log g_bar −11.67 / −11.69 / −11.70 / −11.71.
- Stars only raise it.

**A5. Fossil a0.** Deep regime σ⁴ ∝ a0, so the mean excess ln(σ_obs/σ_law) = 0.38 needs a0(z_f)/a0(0) = e^{1.52} = 4.57.

κ = ½ FITTED; footings never pooled; cold energy is real gravitating mass, not a particle species; not theory closed.

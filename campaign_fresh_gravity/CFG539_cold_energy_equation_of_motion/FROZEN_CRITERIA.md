# CFG539 FROZEN CRITERIA -- the cold energy EQUATION OF MOTION: a dynamical law from which the settling rules emerge, tested in a two-species PM

Committed alone, before the Stage-1 script and before any Stage-2 run. Date 2026-10-09.

## Goal and settings

Find a dynamical law for the cold-energy component whose consequences are the record's settling rules (THEORY_v1 R1-R5), instead of the per-step bookkeeping of the CFG424/518/527 engines (an extra Poisson source e - comp that moves cold energy instantaneously from the shell to the core without any particle moving). Then test it in a two-species particle-mesh simulation in which the gravitating mass is only the particles.

Settings (unchanged from CFG527/530): kappa = 1/2 FITTED; footings 9.3603e-11 (canonical) and 1.1312e-10 (alt), judged separately, never pooled; a0 FLAT; kernel nu_mono; candidate B (the law acts inside bound systems; its phantom is SETTLED cold energy; outside, cold energy is ordinary cold matter); G9 (matter conservation; cold energy feels baryons only through gravity); no EFE; Omega_c/Omega_b = 5.364 and f_b inputs; LCDM background and EH ICs at z_i = 49 (the only LCDM input); step grid; seed 359. Inherited engine settings, not new constants of this lane: T1 tidal switch eps = 0.077, census fret_of (CFG416), census edge r_e = x_supply r_ON (CFG416/423), turnaround catchments IN(x = 1) (CFG424), unfiltered retained-baryon MOND source (CFG527 NOFILT), resolved hosts r_ON >= RMIN (0.78125 Mpc/h at L100, 1.56 Mpc/h at L200, CFG530). The cold energy's MASS is still required. No dark-matter particle species is added. Not "theory closed". Nothing downloaded.

**No knobs.** Zero declared constants beyond kappa, 5.364 and f_b. Any timescale must come from a0, G, the local density, H or c. If a class needs another constant it is NOT VIABLE (knob) and that is said plainly.

## The targets (each from a committed lane)

- **T1 equilibrium** (CFG516, CFG526): inside the system the settled cold-energy profile is the law's phantom of the baryons (round, enclosed-mass rule), i.e. M_grav(<r) = M_b,all + (nu - 1) M_b,ret.
- **T2 supply limit** (CFG515/518, THEORY_v1 R2): settling stops when the system's own cold energy is used up (the census edge).
- **T3 local conservation** (CFG424/527, R3/R5): settled cold energy comes from the system's surroundings (the shell between the edge and turnaround) and is never taken back.
- **T4 growth and halos** (CFG361 cuts; CFG526/527/530 statistic): LCDM-equivalent large-scale growth, and halos that match the law's profile at every resolution. The current bookkeeping fails at 512^3 (CFG530: canonical L200 512^3 max|P - 1| = 0.113, core R 1.142); earlier draws robbed cores (CFG521/524/526).
- **T5 no EFE** (CFG447/478, R7).
- **T6 CDM-like outside bound systems** (CFG474, A5).

## Stage 1 -- candidate classes (equations written before any script)

Notation: rho_c cold energy, rho_b baryons, rho_m = rho_b + rho_c, rho_ph[b] = div[(nu - 1) g_N,b]/(4 pi G) the phantom of the retained baryons, s(x) = f_sw(x) x edge(x) x catch(x) the region where the law acts (inherited switch, census edge, turnaround catchment), deficit d = s max(rho_ph - rho_c, 0) (the one-sided form of the record's e = f_sw max(s_ph - s_c, 0)), and psi the deficit's Newtonian potential, lap psi = 4 pi G d. G9 reading (CFG373/462 "lapse-local"): rho_ph is evaluated from the gravitational field of everything except the cold energy itself, so the drive depends on the field and on the cold energy's own density only.

- **Class A -- overdamped settling flow.** Continuity d_t rho_c + div(rho_c (v_orb + v_s)) = 0, where v_orb is the ordinary collisionless (geodesic, Newtonian-limit) motion and the settling drift is
  v_s = - catch(x) tau_ff grad psi,  tau_ff = 1/sqrt(4 pi G rho_m) (local free-fall time).
  Meaning: inside a bound system the cold energy moves toward the unfilled phantom at the terminal (friction-dominated) speed set by the Newtonian pull of the MISSING phantom mass. The coefficient is fixed by one stated principle: the linearised deficit relaxes at the local free-fall rate, Gamma = 4 pi G rho_c tau_ff = (rho_c/rho_m) sqrt(4 pi G rho_m) (the record's lambda = 1 convention, CFG489). It is not fitted; a factor-2 robustness check is declared below (if the result depends on it, the coefficient acts as a knob and A is NOT VIABLE). The drift carries no momentum (dissipative); the released energy needs a sink, which is NOT SUPPLIED by anything on the record (CFG462/489) -- disclosed, not hidden.
- **Class B -- conservative fluid / superfluid with a chemical potential.** Euler flow d_t v + v.grad v = -grad(Phi + psi) - grad h(rho_c) (psi = delta F/delta rho_c of the mismatch field energy F = (1/8 pi G) int |grad psi|^2, plus a barotropic enthalpy h). Stage 1 will show (sympy) that its static equilibrium is hydrostatic balance in the LAW's potential, which equals the phantom profile only if the fluid's temperature is sigma^4 = G M_b a0/4 per system (CFG461: no G9 mechanism sets it), and that without dissipation the target is unreachable from infall (CFG489 step 3). Expected: NOT VIABLE (needs a per-system temperature = a knob; no settling without a sink). Superfluid variants: FL1-FL3/FK1 (DBI dead) not repeated.
- **Class C -- inertial (non-dissipative) response.** Cold energy inside catchments feels the extra acceleration g_def = -grad psi (no timescale, zero constants); baryons feel only the Newtonian field of the particles. Stage 1 will show there is no Lyapunov decrease (KE + F is conserved in the deficit interior), so T1 is not an attractor analytically; carried to Stage 2 as the "is dissipation needed?" comparator.
- **Class D -- local completeness rate law (T17).** d_t f = lambda sqrt(4 pi G rho)(1 - f), no transport. lambda = 0.028 is FITTED to the MW floor (CFG382) and T16 shows no single lambda fits galaxies, groups and clusters; with lambda = 1 it is the instantaneous bookkeeping limit, which needs the draw rule to conserve mass (no transport). Expected: NOT VIABLE (knob; no transport).
- **Class E -- KL/Wasserstein (JKO) flow (T3 lane).** d_t rho = D lap rho - div(rho grad ln rho_ph): needs a diffusion scale D (a declared length^2/time, a knob), its minimiser is the global rescaling c rho_ph (not the inside-out fill to the edge), and rho_ph < 0 on the deep annulus makes ln rho_ph undefined (T3 lane). Expected: NOT VIABLE.

**Stage-1 script** (`cfg539_stage1.py`, sympy + a 1-D periodic toy, writes `cfg539_stage1.out/.json`; `CFG539_MUTATE=1` -> `_MUTATE` outputs):
- S1 (A, sympy): the linearised relaxation rate Gamma = 4 pi G rho_c tau_ff; dimension check (only G and the local density enter).
- S2 (A, sympy + toy): the Lyapunov property dF/dt <= 0 for F = (1/8 pi G) int |grad psi|^2 under A with fixed baryons, and stationarity <=> d = 0 where the catchment holds cold energy. Toy: 1-D periodic box, a fixed phantom bump inside a region s, cold energy initially uniform, flow A: F must decrease monotonically, d -> 0 (final unfilled fraction <= 0.01), mass conserved to 1e-12, and >= 50% of the settled mass must come from outside the deficit region.
- S3 (A, toy): emergent cap -- with a catchment holding less cold energy than the deficit, the flow must stop with the catchment's cold energy exhausted outside the deficit region (no overdraw), and settled mass <= available mass to 1e-12.
- S4 (B, sympy): hydrostatic equilibrium in the law potential (flat rotation V) gives rho ~ r^(-V^2/sigma^2); SIS requires sigma^2 = V^2/2 and amplitude match requires sigma^4 = G M_b a0/4 -> a per-system temperature.
- S5 (C, toy): same toy with inertia instead of friction: report whether the unfilled fraction decreases monotonically and whether KE + F is conserved; T1 attractor expected NO.
- S6 (D, E): constants ledger from the committed T16/T17/T3 JSONs (lambda window, D scale) -- read, not recomputed.
- MUTATE (Stage 1): A with the relaxation sign reversed must fail S2 (F increases / d grows).

**Stage-1 kill rule:** a class is killed if it needs a constant beyond kappa, 5.364, f_b (knob), or violates exact matter conservation (G9), or if T1 is analytically impossible (not merely unproven). Survivors go to Stage 2. Expected survivors: A and C.

## Stage 2 -- two-species PM (survivors only)

**Engine** (`cfg539_pm.py`): the CFG527 engine (cfg527_pm.py, sha256 aeabd0ba..., copied, not edited) with ONLY these changes:
1. Two species on the same IC lattice: baryon particles (mass share f_b) and cold-energy particles (1 - f_b), identical initial positions and momenta (adiabatic). Deposits are per species; the total density is the mass-weighted sum.
2. The gravitating mass is the particles only: NO extra source term (no e, no comp, no cap). Newtonian forces from the total particle density act on both species.
3. The law's fields (f_sw, census edge, catchments with the census f_ret, all on the total density, cached every 10 force calls as the engine does; and s_ph from the UNFILTERED retained baryon particles f_ret (1 + delta_b)) define the deficit d = f_sw edge catch max(s_ph - s_c, 0), with s_c from the cold particles.
4. EOM A: after each position drift, cold particles drift by v_s = -catch tau_ff grad psi over the step's physical time, in adaptive sub-steps (psi recomputed from the moving cold energy each sub-step; displacement <= 0.5 cell and Gamma h <= 0.5 per sub-step; at most 32 sub-steps, the last one clipped to 0.5 cell and the clipped count reported). Momenta unchanged.
5. EOM C: cold particles inside catchments get the extra acceleration -grad psi in the force call.
6. EOM OFF: one particle set for both species = the single-species S0 path exactly.
7. CFG539_EDGE = 0 (MUTATE-S): the deficit is not confined by the census edge (s = f_sw catch). CFG539_MOB: mobility multiplier (robustness only).
NSEED = 512 at every N (CFG530's realization), so matched S0 = CFG530's S0 runs at the same (L, N).

**Runs** (nice 10, <= 8 threads, <= 2 at once, detached; one 512^3 job at a time on the machine):
| block | runs |
|---|---|
| 128^3 | OFF L100, L200 (identity control); A can/alt L100, L200; C can/alt L100, L200; A-NOEDGE can L100, L200; A mob 0.5 / 2 can L100 |
| 256^3 | A can/alt L100, L200; C can/alt L100, L200; A-NOEDGE can L100, L200; A mob 0.5 / 2 can L200 |
Matched S0: CFG530 S0_L{100,200}_N{128,256} (NSEED 512), reused after the OFF identity control.

**Statistics (z = 0):**
- r(k) = P_run/P_S0 (total particle density, nearest bin), at the same (L, N).
- T4 growth (CFG361 cuts) at every (L, N): GROWTH OK if |sigma8 ratio - 1| <= 0.05 and max|r(k) - 1| <= 0.10 over all bins with k <= min(1, k_Nyq/4); FAIL if |sigma8 ratio - 1| > 0.2; TENSION otherwise.
- Small-scale r(k) at k = 2, 4 (bins with k <= k_Nyq/2), reported, next to CFG530's bookkeeping runs at the same (L, N).
- Law statistic: CFG526's, via `cfg539_profiles.py` (CFG526's module imported; declared changes: NP and cache per N, rmin = RMIN_PHYS as CFG530, M_grav = particle mass (no extra source exists), M_b,all and M_b,ret from the baryon particles, f_ret/edge/catchments from the engine on the run's own density; matched S0 = CFG530's S0 caches). Copy identity check: the patched analyse reproduces CFG526's analyse on CFG530's LRcan_L200 N256 cache to 1e-12 (run before this freeze: PASS, 0.97259 both).
- unfilled fraction u = Sum d / Sum s max(s_ph, 0) at z = 0 (the run's own state; for S0 computed from the S0 state with the same footing's law).
- Settling census (A): fraction of cold particles with cumulative settling displacement > 0.5 cell; for those ending inside census-edge balls, the fraction whose origin x - D_settle lies outside the edge; for all drifted particles, the fraction ending outside the edge ("returned"); cold fraction inside edges vs S0.

**Items per class and footing:**
- **T1 (gating, 256^3, L100 and L200):** (a) law-consistent: core R and R at every scored radius within 0.1 dex of 1 (>= 20 scored halos); (b) direction: |log10 coreR_EoM| < |log10 coreR_S0| (same L, N, footing); (c) fill: u_EoM <= 0.5 u_S0. At 128^3 the same items are REPORTED (>= 10 halos), not gating.
- **T2:** labelled EMERGENT or INHERITED from the Stage-1 analysis. Numerical consistency (A): MUTATE-S (no edge) must be distinguishable -- NOT GROWTH OK at L100 or L200 256^3, or core R > 10^0.1 (EXCESS); if MUTATE-S is indistinguishable, T2 is NOT DIAGNOSTIC at PM resolution (stated; not a pass).
- **T3 (gating, 256^3 canonical L100 and L200):** exact mass conservation (particle counts and deposit totals; trivially exact for particles, checked); A: >= 50% of the drifted cold mass that ends inside census-edge balls originated outside the edge; C: cold fraction inside edges exceeds S0's (net inflow). "Returned" fraction reported.
- **T4 (gating):** GROWTH OK at all four (L, N) per footing.
- **Convergence (gating):** |r_256(k) - r_128(k)| <= 0.05 at k = 1 (L100) and k = 0.5 (L200) (k <= k_Nyq/4 of 128^3), and |Delta log10 core R| <= 0.05 dex (128 -> 256) where both have >= 10 scored halos; at least one box per footing must have the R item evaluable, else convergence is NOT EVALUABLE.
- **T5, T6:** structural (Stage 1); reported numerically: cold vs baryon power ratio at k <= 0.2 h/Mpc.
- **Robustness (A only, gating):** mob 0.5 and 2 at 256^3 L200 canonical: same T4 verdict, |Delta max|r - 1|| <= 0.05 and |Delta log10 core R| <= 0.05 vs mob 1; else the coefficient acts as a knob -> A NOT VIABLE (knob). The 128^3 L100 pair is reported.
- **Stability:** every run finite at every snapshot and r(k_Nyq/2) <= 2, else that run is INVALID.

**Verdict (per class, per footing):**
- **INVALID:** the OFF identity control fails (|d sigma8|/sigma8 <= 1e-6 and max|dP/P| <= 1e-5 at every snapshot vs CFG530 S0 at 128^3, both boxes), or the statistic identity fails, or a gating run is unstable.
- **VIABLE:** Stage 1 survivor with no knobs and exact matter conservation, T1 (a, b, c) at both boxes, T3, T4 at all four (L, N), convergence PASS, and (A) robustness PASS and MUTATE-S distinguishable. The T2 label (EMERGENT / INHERITED) is part of the verdict line.
- **NOT VIABLE:** any gating item fails, with the failing target named.
- **INCONCLUSIVE:** a gating item is NOT EVALUABLE or PENDING.

**512^3:** only if a class is VIABLE on both footings at 256^3: ONE L200 canonical run (NSEED 512), only when no other 512^3 job runs on the machine (CFG530's 512^3 queue may still be running; if so, wait or skip and say so). Judged by the CFG361 cuts vs CFG411/CFG530 S0 N512 and core R within 0.1 dex: CONFIRMED / NOT CONFIRMED / PENDING.

**MUTATE (Stage 2):** relaxation off = OFF/S0 (must have the larger |log10 core R| and the larger u than A; it is also the identity control); supply constraint removed = MUTATE-S (above). Stage-1 MUTATE above.

## Pre-freeze disclosures (not blind)

- The source lanes were read first; the Stage-1 expectations above (B, D, E killed; A and C survive) were reasoned before this freeze.
- 64^3 smoke runs of the engine (L100, NSEED 64, canonical) were made to check that the code runs: z = 0 unfilled fraction 0.357 (A) and 0.415 (C); sigma8 0.8395 / 0.8430. No OFF run or S0 comparison was made at that size; nothing was tuned.
- The law statistic was evaluated on the matched S0 states (relaxation off) before freezing, to check its teeth. S0 core R at 256^3: canonical 0.849 (L200) / 0.852 (L100), alt 0.806 / 0.781; at 128^3 the scored-halo counts are 15 / 18 (canonical L200 / L100) and 5 / 10 (alt). So at the record's 0.1-dex tolerance the canonical S0 is itself law-consistent: item T1(a) alone has no teeth there. This is why T1 also requires (b) direction and (c) fill, and why the 128^3 T1 items are reported, not gating.

## Caveats (declared before running)

- One realization; PM cores are 1-2 cells. The deficit and the law's region are the record's PM-level constructs (the phantom is computed from the global baryon field, as in CFG527; the edge and f_ret census are inherited, not derived here).
- A dissipates the potential energy released by settling; its sink is not supplied (CFG462/489). Its Newtonian-limit drift is parabolic: a covariant version needs a regulator (causality COND, as CFG489).
- kappa = 1/2 is fitted; f_b, the amount 5.364 and rho_Lambda are inputs. A VIABLE verdict would not be "theory closed", and nothing here says the data favour the framework over LCDM.

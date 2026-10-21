# WT-05: the arrow of time in the cold-energy dynamics

**Bottom line.**
- **The gravity law has no arrow.** Vlasov–Poisson with the phantom is time-reversal even: a Vlasov-only run, velocity-reversed,
  returns to its start to 0.2–0.5% (L1).
- **Two terms break time reversal (sympy S4):** the cold energy's velocity relaxation toward the phantom's Jeans temperature T_J (OU in
  CFG638, BGK in CFG955), and the settling drift v_s.
- **The relaxation alone (R1, R2) has a BATH ARROW [finite-T bath].** The cold energy's own entropy falls whenever it cools, and so does
  every Casimir entropy. The medium plus a heat reservoir at the local T_J obeys an exact Clausius H-theorem, self-gravity included.
- **The full CFG638 law (R3, the headline) is UNDERDETERMINED by the frozen rule.** Every finite-temperature reservoir is violated. The
  record's own pairing, with the drift's energy to a coherent dark-energy partner and the relaxation's heat to a T_J bath, runs a
  steady one-reservoir heat engine: total entropy falls without end. The one bath not violated is a ~0 K sink (the de Sitter horizon)
  taking every release, with coherent work covering every draw. It has no proof for the drift, and it makes the second law nearly
  vacuous.
- **Rate.** The relaxation's rate is LOCAL: t_S = τ_ff/2α, with |∂ln t_S/∂ln ρ_Λ| ≤ 0.15 and t_S ≤ 0.010 t_vac. Its destination,
  T_J, does depend on the vacuum: ∂ln T_J/∂ln ρ_Λ = +0.15 to +0.24.

**In this framework, time's arrow comes from the cold energy relaxing toward the phantom's Jeans temperature, which runs one way only
because it hands heat to a reservoir held at that temperature. The temperature is set by the baryons and a₀ (the vacuum); the rate is
the local free-fall clock. With the settling drift included, no reservoir at a finite temperature keeps the books.**

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are used separately (rates only) and never pooled; the toy is footing-free. Cold
energy is real gravitating mass; no particle species. Nothing here says the data favour the framework. Not "theory closed".

- **Record context (WT-01):** on record the arrow was posited, not derived. CFG938's ideal action has no settling drift, and the settling
  energy books need a new reservoir (CFG932, CFG935, CFG955; cited, not redone). New here: the time-reversal parity of each settling
  term, and the generalised second law (which functional is monotone, and with what bath).
- **Criteria:** `FROZEN_CRITERIA.md`.
  - c4b3626f73: frozen criteria, committed alone before any script.
  - A1 8051303f39: pre-result (walls; numerical floor; K4 resolution line).
  - A2 9cac89ddad: post-smoke-test, pre-graded-result (CFG544's drift limiter).
- **Run:**
  - `OMP_NUM_THREADS=1 nice -n 10 python3 wt05.py` → `wt05.out`, `wt05_results.json`. Exit 0; 380 s; peak RSS 610 MB
    (`/usr/bin/time -l`).
  - `WT05_MUTATE=1 …` → `wt05_MUTATE.out`, `wt05_results_MUTATE.json`. Exit 1 by design (all teeth bite); 16 s; 555 MB.
- **Run 1 (kept):** `wt05_run1_K1grid_RSSguard.out` (see Corrections).
- No downloads. Other lanes' files were not run, edited or staged. CFG955's scripts and outputs were not read.

## (a) The committed equations, what they conserve, and their T-parity

| reading | equation (source) | relaxes toward | conserves | T-odd terms |
|---|---|---|---|---|
| R1 | ∂ₜf + ∇ₓ·(vf) − ∇Φ·∇ᵥf = γ∇ᵥ·[(v − u)f + T_J∇ᵥf], γ = α/τ_ff (CFG638 28ce71974d, drift off) | local Maxwellian at the local mean u and T_J | mass, momentum; energy NOT (source (α/τ)(ρT_J − P)) | OU |
| R2 | ∂ₜf + v·∇f − ∇Φ·∂ᵥf = −(f − M[ρ, u, T_J])/τ, τ = τ_ff/2α (CFG955 K-T, 903cd8f1dc) | the same Maxwellian | mass, momentum; energy NOT (Q = (3/2)ρ(T_J − T)/τ) | BGK |
| R3 | R1 + ∇ₓ·(v_s f), v_s = −α1_B1_C τ_ff∇ψ, ∇²ψ = 4πG(ρ_ph − ρ_c) (CFG638 full) | velocity: T_J; position: ρ_ph | mass, total momentum of the slide; energy NOT (source ρ_c v_s·∇Φ) | OU and drift |
| R4 | K-ρ, f_eq = ρ_eq M (CFG955) | ρ_ph itself | mass NOT | NOT CLASSIFIED (no mass reservoir on record) |

- **sympy S4.** ∂ₜ, v·∇ₓ and ∇Φ·∇ᵥ are T-even. The OU, BGK and drift terms are T-odd. Under T: t → −t, f(x, v, t) → f(x, −v, −t), a
  relaxing solution maps to an anti-relaxing one, so the equations single out a direction of time only through these terms.
- The class-A engine (E6–E8) is a many-to-one relocation map, so it is irreversible by construction. NOT CLASSIFIED.
- **Vacuum dependence of the T-odd terms:**
  - their **targets**: T_J and ρ_ph come from a₀ = κc√(Gρ_Λ);
  - their **switch**: domains and bound regions are born at turnaround out of the Hubble flow;
  - their **rate**: τ_ff = (4πGρ_m)^(−½) is a local density clock (CFG541 D1).

## (b) Candidate functionals: proofs and counterexamples

| candidate | status | evidence |
|---|---|---|
| M1 S[f] = −∫f ln f (= total entropy with a coherent partner) | **violated** | S5: cooling lowers S. Toy IC-H falls 0.34 M (R1, R2, R3; ε_num ≈ 0.001 M) |
| M2 −∫f² (all concave Casimirs, by majorization) | **violated** | S5. Toy falls 0.012–0.016 M |
| M3 KL to the local target | **violated** | starts at 0 (IC-U) and rises 73–1099× the line (Vlasov makes non-Maxwellians) |
| M4 F_ψ (CFG541 V3) | **violated** | rises from 0, 48–136× the line |
| M5 F_ψ + F_v (CFG550/554 GENERIC) | **violated** | rises from 0, 102–120× the line |
| **B-TJ**: S + bath at T_J(x) | **R1, R2: PROVED and PASS**; R3: violated | S1 + S2/S3: Vlasov conserves S for any Φ, and per point ṡ − q/T_J = (1/τ)∫(f − M) ln(f/M) ≥ 0 (BGK), (γ/T_J)∫\|T_J∂ᵥf + (v − u)f\|²/f ≥ 0 (OU). Never drops in any R1/R2 run, forward or velocity-reversed. R3: S6 (drift deficit term −ατ∫ρ_c\|∇δΦ\|²/T < 0; the CFG550 super-Jeans sign) |
| B-REC: drift → coherent partner, relaxation → T_J (CFG935's post hoc pairing) | R1, R2 = B-TJ; **R3: violated** | falls 3.9 M (N IC-D) and 2.6 M (U IC-D); late slope −0.18 / −0.25 M per τ_ff0 with the medium steady |
| B-dS: horizon at T_dS both ways | **violated** (every reading) | net energy flows into matter (heating, outward drift) |
| B-SPLIT: releases → horizon, draws → coherent work | R1, R2: PROVED and PASS; R3: not violated, **not proved** | near-tautological: any release into a ~0 K sink carries unbounded entropy |

**Classes (frozen §7).**
- **R1:** BATH ARROW [finite-T bath]; bath identity EITHER (B-TJ, or the vacuum as B-SPLIT).
- **R2:** BATH ARROW [finite-T bath]; bath identity EITHER (B-TJ, or the vacuum as B-SPLIT).
- **R3:** UNDERDETERMINED.
- **The record's coherent partner is NOT sufficient in any reading.** On the cooling branch the cold energy's entropy falls and a
  zero-entropy partner cannot take it (CFG955 L7, now with the full proof). In R3 the deficit-filling drift compresses phase space.

**Why R3 is UNDERDETERMINED and not NO ARROW.**
- B-TJ's frozen whole-run check reaches at most 5.7× ε_num (U IC-D; 1.5× N IC-D, 2.4× N IC-O), against the 10× line. The drift piles mass at the bound-region edge, the
  Vlasov steps smooth it, and that inflates ε_num to 0.05–0.19 M.
- The post hoc windowed check (no class weight; a drop beyond 10× the Vlasov |ΔS| of the same window) verifies it: 0.20 M (U IC-D),
  0.15 M (N IC-D).
- B-SPLIT has no violation: no R3 run has a zero-release interval. The instantaneous search found no drawing-only state whose drift
  compresses phase space (1866 feasible of 5000; minimum Ṡ_drift/M = +3.4e-4). But B-SPLIT has no proof for the drift.

### Self-gravity, and CFG955's collapse (discussion only)

- **The Clausius theorem survives self-gravity**, because Vlasov conserves S and the total energy for any self-consistent Φ.
- **What fails is boundedness.** Where T_J is uniform (the deep-law isothermal region), B-TJ is the free energy F = K + W − T S.
  - In 1-D, F is bounded below (S8). The toy confirms it: F falls monotonically from −333.5 to −361.2 and the dust reaches the target
    sheet (L1 = 4.4e-4).
  - In 3-D, F → −∞ as a sphere contracts (S8). The H-theorem then gives a direction but no floor, and the arrow can point to collapse
    rather than to the law.
- **The thermostat makes the problem canonical.** For an isothermal sphere in a box, the canonical (fixed-T) instability sets in at a
  density contrast of 32.1. The microcanonical (fixed-energy) one sets in at 709 (K3: 32.12 / 708.6).
- **The law state has unbounded contrast:** it is an extremum of F, not a minimum, once the deep region spans more than e^{2π/√7} in
  radius (CFG955 PH4's statement, not recomputed here).
- **Vlasov alone keeps an ergodic isotropic f(E) linearly stable** (Antonov; Doremus–Feix–Baumann).
- **So CFG955 A1's observation is what the H-theorem predicts:** a central collapse under K-T, absent with relaxation off. Its arrow
  runs downhill in an unbounded F.

## (c) What sets the direction and the rate

- **Direction:** the sign of T − T_J (cooling releases heat, heating draws it) and, for the drift, the sign of the deficit.
- **The arrow does not stop in the settled state.** In the K-T stationary state (NESS, IC-E, 80 τ_ff0), S and E are flat
  (S/M = 3.6185 from t ≈ 20 on), but S_tot keeps rising at 3.6e-4 M per τ_ff0. This is heat conducted between reservoirs at
  different T_J; it vanishes where T_J is uniform (U-variant: 7e-5).
- **Fluctuation–dissipation (S7).** The OU noise-to-mobility ratio is T_J, so the relaxation's natural bath sits at T_J. The drift has
  mobility and no noise: its natural bath is at temperature 0. This is why no finite-T bath balances R3, and why only a ~0 K sink does.
- **Horizon temperature.** k_B T_dS = ħH_Λ/2π = 3.0e-53 J (can) / 3.7e-53 J (alt). That is below T_J for any carrier heavier than
  m* = 1e-29 – 1e-25 eV/c², so for any plausible carrier the horizon acts as a 0 K sink.
- **Not claimed:** the dS entropy-ceiling line (opus_48 review) stands only for constant Λ and does not solve the arrow or the Past
  Hypothesis. Nothing here claims that either.

## (e) Rates (simple kernel; ν_mono in the JSON)

t_vac ≡ 1/√(Gρ_Λ) = κc/a₀ = 50.75 Gyr (can) / 41.99 Gyr (alt). This is an identity of the footing, flagged.

| system | footing | v_c (km/s) | τ_ff (Myr) | t_S = τ_ff/2 (Myr) | t_S/t_vac | e-folds in 10 Gyr | ∂ln t_S/∂ln ρ_Λ | ∂ln T_J/∂ln ρ_Λ |
|---|---|---|---|---|---|---|---|---|
| dwarf (1e7 M⊙, 0.3 kpc) | can / alt | 20.8 / 21.6 | 15.8 / 15.0 | 7.9 / 7.5 | 1.6e-4 / 1.8e-4 | 1267 / 1331 | −0.130 / −0.129 | +0.211 / +0.215 |
| MW disc (10 kpc) | can / alt | 207.6 / 213.5 | 62.2 / 58.9 | 31.1 / 29.4 | 6.1e-4 / 7.0e-4 | 321 / 340 | −0.148 / −0.145 | +0.154 / +0.163 |
| MW outer (100 kpc) | can / alt | 169.2 / 177.0 | 592 / 565 | 296 / 282 | 5.8e-3 / 6.7e-3 | 34 / 35 | −0.125 / −0.125 | +0.242 / +0.243 |
| group (1e12, 300 kpc) | can / alt | 344.8 / 360.4 | 880 / 839 | 440 / 419 | 8.7e-3 / 1.0e-2 | 23 / 24 | −0.126 / −0.125 | +0.239 / +0.240 |
| cluster (1.5e14, 1 Mpc) | can / alt | 1313.6 / 1363.0 | 848 / 807 | 424 / 404 | 8.4e-3 / 9.6e-3 | 24 / 25 | −0.132 / −0.131 | +0.204 / +0.209 |
| NGC 3198 (43 radii) | can / alt | — | — | 3.2–166 / 3.2–157 | ≤ 3.3e-3 / 3.8e-3 | — | −0.137 … −0.013 / −0.136 … −0.017 | (JSON) |

- **Relaxation: RATE LOCAL** (96 rows: e ∈ [−0.148, −0.013], max t_S/t_vac = 0.010).
  - Disclosed: this is expected by construction. τ is built from {G, ρ_m} (CFG541 D1), and S9 gives |e| ≤ ¼. The vacuum enters only
    through the phantom's share of ρ_m.
- **Drift: MIXED** (t_D = 1/Γ; e ∈ [−0.31, −0.12]). Where baryons dominate (NGC 3198 at 0.64 kpc, ρ_ph/ρ_m = 0.34) the drift rate
  scales toward a₀ (e = −0.31; −0.35 for ν_mono). Its magnitude still stays ≤ 0.02 t_vac. No row lies within 0.1 of −½.
- CFG763's formation clock is 0.014–0.068 (can) / 0.020–0.083 (alt) of t_vac (reported only).

## (d) The toy (1-D self-gravitating phase space; code units; a structural test of the equations, not an astrophysical model)

**Setup.**
- Grid 512 × 512; dt = 0.02 τ_ff0. Each forward leg runs 10 τ_ff0, followed by a velocity-reversed leg of 10 τ_ff0.
- **N-variant:** baryon slab plus a sech² "phantom stand-in" with T_J from 40.0 to 43.8.
- **U-variant:** uniform T_J = 33.70, the deep-law isothermal analogue.

**Controls (Vlasov only).**
- Mass conserved to 3e-15; energy to ≤ 4.3e-3.
- S rises 0.002–0.022 per unit mass. This is coarse-graining: at 1024² the rise falls by ×11 (K4).
- **Echo:** reversed runs return to the start to 0.005 (IC-H), 0.002 (IC-D) and 0.003 (U IC-H).
- With relaxation on, the echo is 0.33–0.38 (no return), and S_tot(B-TJ) keeps rising in the reversed leg. That is the arrow: reversing
  every velocity does not reverse it.

**R2/R1 IC-H (hot start).**
- S falls 0.34 M as the dust cools: M1 is violated.
- S_tot(B-TJ) rises 0.16 M and never drops (K5 discrete Clausius ≥ +2.8e-20 M per step).
- R2's B-TJ pass follows from K5 plus S1 by construction (A1.4). R1's OU step is a genuine numerical test, and it passes too.

**R3 (drift on).**
- **IC-D (70% of the target mass, at T_J).** The medium settles in about 2 τ_ff0 and then stays steady. The drift keeps moving energy
  out at a constant rate, and the relaxation keeps drawing the same heat back from the bath. That is a circulation: with B-REC,
  S_tot falls linearly.
- **U IC-D.** F = E − T S rises by 34 (the record's CFG550 statement, reproduced). S_tot(B-TJ) falls a net 0.19 M in the transient.
- **N IC-O (overfill).** S_tot(B-TJ) keeps falling at 0.025 M per τ_ff0: a heat pump between unequal T_J with no work input.
- **Limiter (A2):** acted on 0–0.55% of the drift-region mass (run means; 2.4% at most in any step). The discrete ΔW agrees with the continuum q_d to 0.985–1.000.

## Controls and MUTATE

- **sympy:** S1–S9 and K2 13/13 PASS.
- **K1:** 4/4 (per-step minimum ≥ −1.3e-15).
- **K3:** 32.12 / 708.6.
- **K4:** mass 3.0e-15; edge 7.3e-12 M; energy 4.3e-3; resolution 0.091.
- **K5:** PASS.
- **K6:** 20.77 / 1313.57 km/s.
- **MUTATE (all bite, exit 1):**
  - Mu1 anti-relaxation: B-TJ drops 2.95 against a 10ε line of 0.0048.
  - Mu2 fluctuation–dissipation mismatch (diffusion at 2T_J, bath at T_J): drops 2.57 against 0.012.
  - Mu3 drift sign flipped: F_ψ ratio 1.159 against 0.971.

## Caveats (strongest first)

1. **Entropy of a medium with no particle species.** −∫f ln f is an entropy in units of k_B/m for some carrier mass m. Every sign above
   holds for any m. The magnitudes, and the horizon comparison (m* above), scale with 1/m. If cold energy has no microscopic phase-space
   degrees of freedom, the relaxation itself has no microscopic basis, and the H-theorem question changes character.
2. **The toy is 1-D with a declared stand-in target, not the MOND phantom.** The 3-D gravothermal statements are analytic (S8, K3).
   Self-gravity in 1-D has a floor that 3-D lacks.
3. **R3's B-TJ violation is verified only post hoc.** Under the frozen whole-run rule it reaches at most 5.7× ε_num (line 10×). The
   record's pairing (B-REC) is violated under the frozen rule in four of five R3 runs (29–237× ε_num).
4. **B-SPLIT is near-tautological** (flagged before freezing). Its survival in R3 says only that a ~0 K sink can absorb anything.
5. **Analysis limits.** The rates use spherical-equivalent NGC 3198 profiles and point masses for CFG847's systems. T_J for point
   masses is the untruncated phantom's (CFG550 convention).

## For the CFG955 and CFG958 sessions

- **CFG955.**
  - K-T has an exact Clausius H-theorem with self-gravity: S + ∫(−Q/T_J). It selects no equilibrium. In 3-D the free energy is
    unbounded below, and a thermostat lowers the isothermal-sphere instability threshold from contrast 709 to 32.1.
  - The A1 collapse (present with K-T, absent with relaxation off) is therefore consistent with this lane, not a numerical artefact.
  - In the K-T law state, where T_J varies, the bath entropy keeps rising.
- **CFG958 (frozen T-S item S5: "the drift's work to a coherent partner is admissible").**
  - That holds only for the formal GENERIC entropy −F/Θ (CFG542).
  - With the cold energy's Boltzmann entropy it fails. Deficit filling compresses phase space. Combined with the relaxation's bath, it
    becomes a steady one-reservoir heat-to-work cycle: S_tot falls at 0.18–0.25 M per τ_ff0 in the toy.
  - So CFG935's post hoc "dynamical DE partner for the drift plus a heat reservoir for the bath" violates Kelvin–Planck.

## Corrections and disclosures (2026-10-21)

1. **Scratch runs before the graded run** (outside the lane folder):
   - the sympy section (13/13 seen before the main run);
   - toy smoke tests of 1 τ_ff0 for timing and conservation;
   - memory profiling;
   - a 0.3 τ_ff0 end-to-end test of the grading code (its numbers were not used).
2. **A2 (committed alone, before any graded output).** CFG544's drift limiter was adopted after the R3 smoke test stalled (5471
   substeps; empty edge cells give τ_ff → ∞). Two implementation fixes: T_J's tail integral (cancellation), and macOS BLAS raising
   spurious floating-point flags in W.
3. **Run 1 (kept as `wt05_run1_K1grid_RSSguard.out`).**
   - **K1 failed in its closed modes** (−1.5e-6 and −2.9e-6 per step). Verified as an artefact of my K1 velocity grid: ±12 truncates the
     closed-mode Maxwellian (T_f = 6.55), so its discrete variance is low by 6.3e-5 (tail mass 2.8e-6); at ±30 the variance is exact to
     2e-16. Fixed to ±30. The frozen K1 text names no grid. The thermostat modes passed in both runs.
   - **Run 1 also hit the in-script 1 GB RSS guard** (1278 MB) at the 1024² K4 run, from 8 MB temporaries the allocator retained. Fixed
     by row-blocked shifts (identical arithmetic) and by dropping KL bookkeeping from Vlasov-only controls (no rule uses it).
   - Every toy number that run 1 printed is identical in run 2.
4. **Post hoc additions after run 1 (no class weight):** the windowed diagnostic, and the per-run S2 Vlasov floor reported in the JSON.
5. **Rules applied as written.**
   - M5's threshold uses the stricter of the two unit readings: 1e-4 × max(M·T_J,max, |W(0)|).
   - M2 is graded with ε_num in S units, as frozen; it is verified anyway in each reading (R1 IC-U, R2 U IC-H, R3 IC-H).
6. **A1.2's hand estimate was pessimistic.** The controls phase-mix less than feared (echo 0.002–0.005), so the rule change had no
   effect on any class.

κ = ½ FITTED; footings never pooled; cold energy is gravitating mass, no particle species; not theory closed.

# CFG487: the cold fluid's settled fraction as candidate B's switch (Gap 1), tested in two versions

Criteria: `FROZEN_CRITERIA.md` (e8f72dcc9, committed alone before any script). κ = ½ is FITTED; ν_mono; both footings
(9.3603e-11 / 1.1312e-10), never pooled; a0 flat. No dark-matter particle: the cold fluid's mass is still required.
Owner instruction 2026-10-08: "test both". Nothing here closes Gap 1 or the theory.

## Verdict (frozen rule)

**Both versions FAIL, on SPARC (alt footing only) and on KiDS.** The cause is the mass-conserving edge r_edge = 5.850 r_M
taken with each galaxy's present baryons. The switch itself is not the cause. Growth passes but is NOT DIAGNOSTIC: the
FRW-firing control also passes, because the edge and catchment do the confining. Well-posedness passes.

| test (frozen line) | V1: cold-fluid clock (MS1 EXCEPTION) | V2: baryon clock (strict MS1) |
|---|---|---|
| (a) SPARC, CFG346 S clauses, edge E1 | **FAIL**: alt dwarfs A3 0.864 < 0.90 (canonical 0.945); spirals 1.00/1.00; Δrms +0.0003 / −0.0003 | **FAIL**: identical (m = 1 inside the edge) |
| (b) KiDS, χ² − χ²_best(CFG413) ≤ 4 | **FAIL**: +60.5 / +70.6 (edge at x = 0.029 / 0.025 r_ta) | **FAIL**: +60.5 / +70.6 |
| (c) growth 256³, CFG361 cuts | GROWTH OK: σ8 1.0028 / 1.0029, max\|P−1\| 0.021 / 0.023 | GROWTH OK: 1.0020 / 1.0023, 0.015 / 0.018 |
| MUTATE-A (FRW-firing switch, canonical) | GROWTH OK (1.0042, 0.036): **not detected, so growth is NOT DIAGNOSTIC** | (same control) |
| (d) CFG337 H1-H4, 24 transitions | PASS: worst extra growth 0.007 Γ_g | PASS: 0.064 Γ_g |
| (e) Lean | 10 theorems, no sorry, standard axioms | (shared) |
| under original MS1 | NOT ADMISSIBLE | admissible |
| **verdict** | **FAIL (SPARC, KiDS); MS1 EXCEPTION** | **FAIL (SPARC, KiDS)** |

The 512³ canonical run was not made. Three conditions failed: MUTATE-A was not detected, both versions already fail
(a) and (b), and the CFG460 512³ job was running.

**Bottom line.** The settled fraction works as a switch, but the "one object" does not hold together, because lensing and
growth want different supports.
- **What works.**
  - The switch is exactly OFF on FRW and in linear parcels, and it never flickers.
  - It is Hadamard-bounded with no length scale.
  - With zero constants, V1's λ = 1 clock produces the lensing taper KiDS wants (reported row).
- **What growth needs.** Every growth pass rests on the mass-conserving edge. Without it, the switch's own support
  overdraws the cold supply (post-hoc rows).
- **Where the conflict sits.** On real galaxies (present baryons) that edge sits at about 0.03 r_ta, which KiDS excludes
  and which cuts SPARC dwarfs on the alt footing. This is the CFG398/CFG413 lensing-vs-supply tension in one object.

## What fails, and what it is not

The failure is the edge, not the switch:
- Inside r_edge(E1), m = 1.000000 for every KiDS lens group, on both versions.
- The "edge only" row (m ≡ 1 inside r_edge) reproduces the V1 and V2 rows exactly, on KiDS and on SPARC.

### Attribution rows on KiDS and SPARC (reported; they cannot change a verdict)

| row | KiDS χ² − best (can / alt) | KiDS χ² − (x = 1) | SPARC (A3 dwarfs can / alt; Δrms) |
|---|---|---|---|
| V1/V2 with edge E1 = edge only (m = 1) | +60.5 / +70.6 | +44.9 / +56.9 | 0.945 / **0.864**; ±0.0003 |
| **V1 switch only (m(r) to r_ta, no edge)** | **+2.05 / +0.71** | **−13.5 / −13.0** | 1.00 / 1.00; 0 |
| V2 switch only | +6.2 / +11.1 | −9.4 / −2.6 | 1.00 / 1.00; 0 |
| edge E2 (M_b = f_b M_ta,law; x ≈ 0.16 / 0.15) | +12.9 / +20.8 | −2.6 / +7.1 | 1.00 / 1.00; 0 |
| MUTATE clock (FRW-firing), switch only | +15.6 / +13.7 (= the x = 1 row) | +0.01 | (n/a) |

- **E1 edge.** It sits at x = r_edge / r_ta = 0.029 (canonical) and 0.025 (alt) for the median KiDS lens (10-90%:
  0.019-0.042). That is the regime of CFG413's x = 0.05 MUTATE (+40 / +51 vs x = 1).
  - On SPARC, R_HI lies beyond r_edge for 21% (canonical) and 39% (alt) of the dwarfs.
  - So 5.5% / 13.6% of dwarfs lose more than 0.03 dex of velocity at R_HI (max 0.07 / 0.09 dex).
  - The rotmod RAR rms hardly moves: 107 / 156 of 3,389 points lie beyond the edge.
- **E2 edge** (the PM-consistent original-baryon reading) passes SPARC but still fails KiDS. It needs x ≥ ~0.35-0.4,
  and E2 gives about 0.16.
- **The V1 clock alone does what CFG413's hand-set x did.**
  - The λ = 1 clock on the law's own density makes recently turned-around shells only partly settled. At z = 0.2 the
    profile is m = 0.87 / 0.71 / 0.46 / 0.12 at x = 0.25 / 0.5 / 0.75 / 0.95 r_ta. It is self-similar in x, since the
    deep-law density goes as r⁻², and it is the same on both footings.
  - That taper passes KiDS against CFG413's best x (drop-one-bin −0.8..+3.4 / −1.9..+2.1; A_2h 1.27 / 1.11, inside
    CFG486's range) and passes SPARC, with zero constants.
  - The FRW-firing control removes the taper and returns exactly the x = 1 row. So the pass comes from the clock's
    history, not from the truncation alone.
  - This is a reported row, not the frozen object. It rests on CFG413's free two-halo template, as CFG413's own result
    does. V1 is an MS1 exception.
- **V2 alone fails KiDS.** With point-mass baryons, the baryon clock's turnaround radius sits at about 0.4 r_ta.

## Growth (256³, seed 359, CFG424 engine copy, against CFG359 S0)

| run | σ8 ratio | max\|P−1\| (k ≤ 1) | verdict | clock at z = 0 |
|---|---|---|---|---|
| C1 T1REPRO (CFG424's T1 switch) | 1.0033 | 0.0273 | GROWTH OK | reproduces CFG424 TA-can exactly (Δ = 0) |
| V1 canonical / alt | 1.0028 / 1.0029 | 0.0209 / 0.0229 | GROWTH OK / OK | latched mass 0.61 (knots 0.95, filaments 0.71, sheets 0.20; δ < −0.5 cells 0.034); SW in edge cells 0.964 (T1 0.990) |
| V2 canonical / alt | 1.0020 / 1.0023 | 0.0147 / 0.0184 | GROWTH OK / OK | latched mass 0.15 (knots 0.36); SW in edge cells 0.686 |
| MUTATE-A (FRW-firing, canonical) | 1.0042 | 0.0357 | **GROWTH OK, so not detected** | m_bg in voids 0.974; SW in edge cells 1.000 |
| V1-SA, switch alone: latched-fraction catchments, no edge (reported) | 0.9943 | 0.1727 (P(k = 1) 0.827) | TENSION (small-scale deficit) | overdraw 0.001 of mass, but q_max 4e7 in tiny components |
| MUTATE-B-SA, FRW-firing switch alone (reported) | 1.1192 | 0.3254 (P(0.3) 1.315) | TENSION (σ8 +12%) | the whole box is one catchment |
| POST-HOC V1-CATCH, switch × turnaround catchment, no edge: canonical / alt | 0.9972 / 0.9968 | 0.1741 / 0.2016 (P(k = 1) 0.826 / 0.798) | TENSION / TENSION | overdraw 26% / 52% of catchment mass (q_max 2.0 / 2.3) |
| POST-HOC MUTA-CATCH, FRW-firing control | 0.9854 | 0.3898 (P(k = 1) 0.610) | TENSION | overdraw 92% |

- **The engine leaves the switch little to do.** At 256³ the edge balls are about one cell around each resolved peak, and
  the cells there are old and dense. So any switch that is near 1 in those cells passes, including the FRW-firing one.
  This is CFG424's own INCONCLUSIVE clause applied to the switch: the confinement controls growth.
- **V2's baryon clock rarely latches in the PM.** The MIX-A-filtered baryon flow turns around only in the largest hosts.
  This differs from the analytic V2, which uses galaxy point masses.
- **The PM's "zero on FRW" is not exact.** 3.4% of the mass in δ < −0.5 cells is latched in V1; m there averages 0.014.
  This is matter that turned around and then streamed into low-density cells, plus lattice-Jacobian noise. The analytic
  A1 is exact (below).
- **Without the edge, the switch cannot confine the growth excess (reported and post-hoc rows).**
  - Its own support (SA) and the turnaround catchment (CATCH) both overdraw the cold supply in the catchments. That drives
    a −17% small-scale power deficit at k = 1 in both cases, while σ8 stays within 1%.
  - The FRW-firing controls are worse: σ8 +12% (SA) and P(k = 1) −39% (CATCH). So the switch's history matters once the
    edge is gone, but it does not reach GROWTH OK.
  - The mass-conserving edge is what keeps the excess inside each halo's cold supply. That is its definition.

## (d) Well-posedness (CFG337's H1-H4 on DE12's 24 transitions, 1e5 and 1e6 K)

- The switch is a comoving label with a first-order rate law. It has no kinetic or gradient term, so there is no ghost
  (H1), and its characteristic speeds are {0, ±c_s} (H2).
- The dispersion relation is s³ + Γs² − As − (AΓ + C) = 0, with A = Γ_g² − c_s²k² and C = Γ_ph² F(1 − m)Γχ/2.
  - Its coupling is k⁰, so growth is bounded uniformly in k (H3).
  - The extra growth is ≤ Γ_g with no switch length (H4). Worst cases with the edge are 0.007 Γ_g (V1) and 0.064 Γ_g (V2).
    Switch only, they are 0.13 and 0.44.
  - The bound s² ≤ Γ_g² + Γ_ph² F(1 − m)χ/2 holds at every point (Lean L7/L8/L10: s ≤ 1.25 Γ_g).
- CFG337's sharpness-vs-stability trade-off does not arise in this form. A rate-limited label responds at its own rate Γ,
  not through a stiffness c_g, so a sharp turnaround front costs no Hadamard growth.

## Legality (reported suffix; it cannot raise a verdict)

- **Reading.** m is the settled share of a two-state fluid. The advected part has an ordinary action. The conversion is
  an irreversible source, and its energy f'(m) L_M ṁ must go into the parcel's internal energy.
- **V1.** The conversion energy per unit settled mass is B/(ρ_c v_c²/2) = 0.06-0.29 at 30 kpc and 0.05-0.11 at
  r_edge. That is modest heating of the cold fluid, so the reading is CONDITIONAL, not excluded.
- **V2.** Dumped into 1e6 K gas, it is B/(ρ_b c_s²) = 0.2-21 (median 1.8) at 30 kpc. That over-couples the gas, which
  is CFG347's failure mode.
- **Both.** The edge needs the host's total M_b, so it is bilocal (CFG48-type). For a point mass it equals the local
  baryonic field g_N = 0.0292 a0, a baryon-only local reading that is not used in the scored model.
- Not derived from an action. CFG349's verdict (an irreversible ratchet has no fully legal ordinary action) is not
  overturned.

## Controls and MUTATE

- **C1** passes: T1REPRO reproduces CFG424 TA-can bit for bit (σ8 1.003319, max|P−1| 0.027282).
- **C2** passes: CFG413's χ² at x = 0.5 and 1.0 is reproduced to 0.00000.
- **C3** passes: m ≡ 1 with no edge gives A3 100% and Δrms 0, and rms0 matches CFG39's 0.100328994.
- **C4 FAILED (kept).**
  - The EdS check t_c/t_ta = 1.5 + 1/π misses by 7e-2.
  - Post-hoc diagnosis: this is a bang-time offset in the strongly nonlinear initial conditions. The worst shell has
    d_i = 0.35 and a_ta = 0.0038. The offset-free collapse duration agrees to 2e-8 for all shells, and shells with
    a_ta ≥ 0.027 agree to 3e-3.
  - Shells with a_ta < 0.02 have E ≥ 167 even at z = 4, so m = 1 − 2e-73 there and they cannot move any scored number.
  - The ΛCDM turnaround density matches cfg100 to ≤ 1e-3.
  - The main run of `cfg487_wellposed.py` therefore exits 1.
- **C5** passes in run 2.
  - Run 1 FAILED on an implementation tolerance: it compared s_max with Γ_g instead of the Jeans value √(Γ_g² − c_s²k²)
    at the chosen k_min, where the true ratio is 0.99999475. The frozen text names no tolerance.
  - Run 1 is kept as `cfg487_wellposed_run1.out` / `_results_run1.json`. Run 2 compares with the Jeans value (1.000000000000).
  - The injected slaved k-linear term is flagged (s ratio 5.6e3).
- **C6** passes: m stays in [0, 1] and never decreases on any particle in any run (max drop exactly 0).
- **Analytic MUTATE** (`CFG487_MUTATE=1 cfg487_wellposed.py`): the FRW-firing clock gives m_bg(z = 0) = 0.9997, A1 FAILS,
  and the run exits 1 (detected). The data script's MUTATE rows are above.
- **A1** passes: m = 0 exactly on FRW (θ/3H = 1) and in a δ_lin = 0.1 parcel (min θ/3H 0.979, no turnaround).
  A2: sphere 1.062; Zel'dovich sheet 0.75 / 0.85.

## Lean

`CFG487_switch_certificates.lean`: 10 theorems, no sorry, standard axioms only, rc 0 (`.out`):
- L1 monotone step;
- L2 [0, 1] invariance;
- L3 FRW-off;
- L4 MUTATE on;
- L5 the edge identity 1/(exp(ln(1/(1 − f_b))) − 1) = (1 − f_b)/f_b;
- L6 f ∈ [0, 1];
- L7 the root bound s² ≤ G2 + C/Γ;
- L8 uniform in k;
- L9 exponent monotonicity (the conservative clock bracket is a lower bound);
- L10 s ≤ (5/4) Γ_g.

## Deviations and disclosures

- **POST-HOC.** The CATCH mode (switch × turnaround catchment, no edge balls) and its runs were added to the engine and
  the launcher after MUTATE-A came back GROWTH OK. The scored paths are unchanged; the T1REPRO and V1-canonical runs used
  the file before this purely additive branch existed. The CATCH rows cannot change a verdict.
- **The brief's pgrep pattern.** `"N512\|512 0 MIXA\|..."` errors silently on macOS pgrep, which uses extended regex, so
  it reported no job while CFG460's 512³ run was live. The analysis uses the ERE form `N512|512 0 MIXA|...`.
- **Threads.** The PM queue ran two 3-thread jobs (6 threads). The light single-thread analysis scripts (data, wellposed,
  64³ smoke tests) ran alongside them, so the peak was briefly 7-8 threads at nice 10.
- **Approximations.**
  - The V2 PM clock rides on the matter tracers but reads only the baryon fields.
  - The PM rate uses CIC density at 0.78 Mpc/h, which underestimates halo-centre density, so m is conservative there.
  - The analytic shells are spherical top-hats that virialise at R_ta/2.
  - SPARC and KiDS baryons are the harnesses' own: CFG346's M_b, and CFG413's point-mass M_gal.
- **κ** is fitted, the footings are never pooled, and the cold fluid's mass is still required. Nothing here says the data
  favour the framework.

## Compute

- 11 PM runs at 256³: 8 frozen scored or reported runs plus 3 post-hoc runs.
  - Each took 1,280-2,460 s at 3 threads, nice 10, two at a time.
  - The sum is 21,067 run-seconds, about 5.9 h of run time and about 3.3 h of wall time.
- Data legs 160 s; well-posedness 18 s; Lean 35 s.
- Large arrays live in `../_external_data/cfg487_work/` and are not committed.

## Run

```
python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/run_487.py 256            # 8 scored/reported runs, 2 x 3 threads
python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/run_487.py 256 posthoc    # POST-HOC CATCH runs
nice -n 10 python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_data.py          # rc 0
CFG487_MUTATE=1 nice -n 10 python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_data.py
nice -n 10 python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_wellposed.py     # rc 1 (C4 kept)
CFG487_MUTATE=1 nice -n 10 python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_wellposed.py   # rc 1 (detected)
python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_growth_analysis.py
CFG487_MUTATE=1 python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_growth_analysis.py
python3 campaign_fresh_gravity/CFG487_settled_fraction_switch/cfg487_verdict.py
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG487_settled_fraction_switch/CFG487_switch_certificates.lean
```

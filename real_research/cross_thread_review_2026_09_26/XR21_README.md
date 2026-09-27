# XR21 — the derivation chain's model in a particle-mesh box (stage 1: the code and its tests)

Cross-thread review, 2026-09-27. Read-only on every other file: XR21 writes only `XR21_*` files in this folder, and nothing
large goes into the repository.
- Each script writes its own `.out` and `_results.json`; `MUTATE=1` writes `_MUTATE` copies.
- Every MUTATE run fails as designed (rc = 1). Every main run has rc = 0.
- Both a₀ footings are carried (FP0: canonical 9.3603 × 10⁻¹¹, alt 1.1312 × 10⁻¹⁰ m s⁻²).
- κ = ½ is FITTED (Z = 5.7888); no stage-1 number depends on it.
- The dark fluid is FK1/FL1's order parameter, a classical coherent field. The box's particles are only a numerical device,
  and **the dark mass is still required**.

**Stage 1 is done: the code is built and tested. Stages 2 and 3 have not started.**
- Stage 2 is on hold. XR18 finds FP13's H_S linearly ill-posed as written at z ≤ 0.635, and its repair (FP19) must pass a
  re-audit first. H_Y is linearly healthy per XR18.
- Stage 3 waits for the coordinator. Per XR19 it needs a web conversion channel.

## What was built

`XR21_pm_core.py` is a particle-mesh engine. In its LCDM limit it is the record's PM (L176/L346/L362/L366), bit for bit up
to rounding. On top of that it carries four things.

**1. The gravity sector.** FP7's AQUAL-type root with the chain's separator, in the **QUMOND-type approximation** the chain's
lead accepted as a first pass. FP7 R7e found AQUAL and QUMOND agree to ≤ 0.035 dex in discs, and they are identical in
spherical symmetry. The approximation is labelled wherever it is used.
- The phantom: φ_ph = B u, ∇²u = ∇·[C^Q(y) G], G = ∇(B φ_N[source]), y = |G|/(a a₀), C^Q y = X(y − y_th).
- X(D) = √(D² + D) − D above the yield and 0 below it: P2 with FP9's yield floor.
- B = S_ξ − S_L (the heat branch read at two depths; S_ξ = 1 on any mesh).
- Three separators:
  - **H_Y** (FP9): four parameters, the headline cell by default.
  - **H_S frozen** (FP13): FP13's committed L(z) and y_th(z), from FP13's own code exec'd read-only and reproduced exactly.
  - **H_S live**: L and y_th read every step from the box's own matter field. The readout rules are pluggable, so a repaired
    H_S (B from ∂S/∂B = 0, or a ⟨K⟩_h-type state) can drop in.
- Two readings of who sources and feels the phantom:
  - `chain`: FP10/L353 reciprocity, as in L377/L388's PM. The kernel reads the baryons, only the baryons feel the phantom,
    and the dark fluid is Newtonian.
  - `fp9`: FP9's and FP13's yardstick. All matter sources and feels the phantom.
- Lensing sees φ_N + φ_ph (ψ = Φ, FP7 R7d).
- FP9's per-mode rule is included as a k-space control operator. It is not the model.

**2. The dark fluid (FK1).** Heavy (convertible) and light (daughter) parts, both Newtonian only.
- The conversion φ_Hφ_H → φ_Lφ_L fires where the fluid's own density exceeds ρ_t = δ_t0 E⁴/(1+z)³ × its mean (FK1 N2).
- Each parent m becomes two daughters of m/2 with momenta p ± a v_k n, back to back. This conserves mass and momentum exactly
  and releases v_k²/2 per unit mass.
- A mesh trigger ('cap' or 'cleared', at rate Γ₀H).
- A **seamless sub-grid term**: the extended-Press-Schechter conditional census of clumps above M_min. Each clump adds only
  the part the mesh's own detection function f_seen(M) misses. f_seen is a Monte Carlo of the same trigger on NFW clumps.

**3. The web channel's instrument** (`flow_strain`): the carrier's strain tensor and dispersion, read from its particles.
XR19's web channel stands on it.

**4. The record's estimators**: forest P1D (FGPA, L362), L346's P(k), L367's cosmic-shear bins, σ₈ (L366), the lensing
power P(δ_m + δ_ph), and exact-shell spectra.

## The five tests the lane asked for

| # | Test | Result | Tolerance (declared) |
|---|---|---|---|
| 1 | No MOND, no conversion: reproduce committed LCDM PM numbers | L362's control P1D 6.9e-15. Two species, the H_Y path run at infinite yield and the conversion idle: 8.4e-15. L366/L388's σ₈ 1.0208791238487953 vs 1.0208791238487946 (6.7e-16). L366's P1D 9.5e-15 | 1e-10 (1e-8 for L366) |
| 2 | The forest and lensing estimators return committed LCDM values | Forest: row 1. L346's P(k) 6.7e-16. Lensing = matter power exactly through the phantom path. XR12 A2's threshold statistic (the trigger's input) 2.4e-14 | 1e-10; 1e-6 |
| 3 | Linear regime vs the committed linear P(k) boost | With FP9's per-mode rule the box reproduces both committed boosts (below). The model's real-space operator does not, as pre-declared. | 2% on (1+b); 25% on b |
| 4 | MOND off, conversion on | Mass 4.4e-16, momentum 4.0e-16, every daughter at v_k to 6.7e-16, back-to-back 4.2e-16, latent heat 1.8e-13, isotropic. Force-free daughters follow the leapfrog's drift to 2.5e-15 and slow as v_k a_e/a to 4.4e-16 | 1e-12 (1e-10 energy) |
| 5 | The sub-grid term and the mesh trigger agree where the mesh resolves the clump | Resolved clumps (M ≥ 300 M1 on both meshes): mesh/exact 0.992–1.002. Every clump's seen share matches the detection function. | 5%; 0.05 + 3σ |

M1 = δ_t ρ̄ V_cell, the mass that lifts one cell to the threshold.

### Test 3 in detail (`XR21_s1_separator_linear.py`)

Linear boxes: 24 Mpc/h with 192³ mesh and particles, and 200 Mpc/h with 128³. Fixed amplitudes, amplitude 10⁻⁴, z_i = 9.

**The chain's own rule reproduces the committed numbers (P1, code).** With FP9's per-mode rule, the box matches the chain's
yardstick at its own shells to ≤ 1.5% on (1 + b) (z = 1, 0.25, 0; both footings). It matches the committed boosts to
≤ 0.73% on (1 + b). On b itself the 24 Mpc/h box's k = 0.3 bin (its first shell) runs 14–16% high; the 200 Mpc/h box gives
+0.0481 vs +0.0484 (H_S) and +0.0250 vs +0.0253 (H_Y) there:

| separator | z = 0: k = 0.3 / 0.5 / 1 | z = 0.25: k = 0.3 / 0.5 / 1 |
|---|---|---|
| H_S frozen, box | +0.056 / +0.243 / +1.944 | +0.017 / +0.076 / +0.604 |
| FP13 H4, committed | +0.048 / +0.235 / +1.922 | +0.015 / +0.073 / +0.599 |
| H_Y, box | +0.029 / +0.135 / +1.355 | +0.014 / +0.068 / +0.647 |
| FP9 H2c, committed | +0.025 / +0.131 / +1.358 | +0.012 / +0.066 / +0.649 |

At k = 0.1 (the 200 Mpc/h box): +0.0016 vs +0.0016 (H_S) and +0.0007 vs +0.0007 (H_Y).

**The real-space operator is right (U, S, G, H, P2, code).**
- U1: its physical field equals FP6's linear field to 1e-12.
- S1: it reproduces the chain's committed spherical law (FP6's phantom() with FP9's yield) to ≤ 1.1% of the peak beyond 8
  cells. At yield surfaces the error is ≤ 4.1%: the mesh smooths the kink of X ~ √D.
- G1: on a Gaussian field its coherent coefficient equals the Stein (Maxwell) expectation to ≤ 7.4e-4, and the
  phantom–matter cross-spectrum equals cbar h_k² within the realisation noise.
- P2: its linear boxes follow the Stein yardstick built from their own cbar(a) to ≤ 0.14% at z = 1 and ≤ 3.3% at z = 0.
- H1: the live H_S readout's arithmetic is exact to ≤ 4e-13.

**The literal test fails, as pre-declared (P3, reported).** The model's real-space box against the committed boosts, as
b_box/b_committed at k = 0.3/0.5/1 h/Mpc:

| | z = 0.25 | z = 0 |
|---|---|---|
| H_S vs FP13 H4 | 0.63 / 0.72 / 0.91 | 0.50 / 0.60 / 0.80 |
| H_Y vs FP9 H2c | 0.32 / 0.37 / 0.51 | 0.28 / 0.34 / 0.46 |

The per-mode yardstick evaluates each mode's kernel at that mode's own field amplitude. The real-space kernel responds to
every mode with one coefficient set by the whole band-passed field (G1), and that field is larger. So **the committed
linear boosts overstate the chain's own operator's linear response by 1.1–3.6× in b.**

## What stage 1 found (flags for the owners; nothing outside this folder was edited)

1. **The per-mode linear yardstick overstates the linear boost** (P3, above). FP9's and FP13's σ₈ and forest-proxy verdicts
   rest on it, and it cuts both ways.
   - For σ₈ it overstates the chain's own operator's linear boost.
   - For the forest it is optimistic: "the IGM sits below the yield" reads a per-mode field that is smaller than the
     real-space field the kernel sees. In the linear boxes the real-space rms field reaches H_Y's yield near z ≈ 2 and H_S's
     near z ≈ 1. Nonlinear lumps are stronger still, so the forest needs the stage-2 run.
2. **Who feels the MOND** (P4). FP9's and FP13's yardstick applies the MOND to all matter. FP10's reciprocity, the chain's own
   dark sector, has the kernel read the baryons and act on them alone.
   - In that reading the linear total-matter boost drops by 20–25×. At k = 1, z = 0: H_Y +0.041 vs +0.621; H_S +0.064 vs
     +1.535.
   - The baryons' own boost is about 6× the matter's.
3. **The linear lensing boost is large in every reading** (P4). In the chain reading at k = 0.5–1 h/Mpc (z = 0–0.25),
   P_lens/P_LCDM is 1.3–8 (H_Y) and 2.3–45 (H_S). The linear regime overstates the kernel, because real halos carry stronger
   fields. This is the cosmic-shear risk FP9 and FP13 flagged, and **only stage 2's nonlinear run can decide it.**
4. **A kernel-argument error in record lanes** (U2). L346, L347, L362, DE11 and DE11b evaluate the MOND kernel at |∇φ|/a²,
   which is (1+z) × the physical field. Their MOND tangent is therefore about √(1+z) too weak at z = 2–3, so their forest
   deviations are underestimates. L377 and L388 use 1/a correctly. Not re-run here.
5. **The record's leapfrog drift is first order** (T4f′). A free-streaming daughter's travel from z = 3 is overstated by 1.8%
   at dlna = 0.02. Stage 3 should use dlna = 0.01.
6. **H_S in the box is a code path, not physics.**
   - XR18's ill-posedness comes from the state term's own force. That force is absent from this quasi-static operator, so the
     boxes can neither show nor rule it out. No blow-up appeared.
   - The live readout of LCDM boxes (D3) reproduces FP13's halofit L within −9% to +15%.
   - Its y_th at z = 1 is 25–45% low: the mesh misses the small-scale field.
   - The band-pass is unresolved (L < 2 cells) at z ≳ 1.5 on 0.39 Mpc/h cells and at z ≳ 2.5 on 0.195 Mpc/h cells.
7. **The conversion's sub-grid term** (T5).
   - The mesh sees a compact clump partially from ~3 M1 and fully only by ~300 M1.
   - A sharp-cut sub-grid (the first design) over-counts. The seamless form hands over exactly (T5a).
   - Against a finer mesh (12.5 Mpc/h, one realisation) the census agrees to 5% (z = 3) and 22% (z = 2) once the fine run's own
     halos are resolved (192³ force mesh). It is off by 58% and 39% at 96³, where force softening flattens the fine run's
     clumps (T5b, T5b-H).
   - The production reading down to M_min = 10⁸ M☉ gives F(3)/F(2) = 0.31/0.49, against XR16's committed 0.34/0.43 (T5c).
8. **The web channel (XR19) is required in stage 3, and its input is estimator-dependent** (W3).
   - On the same ICs, the box's Eulerian mesh strain and XR19's Lagrangian Zel'dovich census disagree on the turned-around
     share. At z ≥ 2 the box calls far less mass turned around (z = 2: 0.12 vs 0.32 at R_s = 1 Mpc/h, 0.29 vs 0.40 at
     R_s = 0.5). At z ≤ 1 and R_s = 0.5 it calls more (0.39–0.40 vs 0.23–0.33), while Zel'dovich puts another 0.34–0.49 in
     shell-crossed streams, a class the box does not have.
   - Stage 3 needs a per-particle (Lagrangian) strain first.
   - At the ICs the instrument reads the Zel'dovich flow correctly (correlation 0.996; eigenvalue level to 0.0012 H).

## Run time and memory

M4 Max. Another 2-thread, 14 GB job was running throughout. "4 threads" means 4 FFT workers and 4 particle-chunk threads.

| box | what | time | peak memory |
|---|---|---|---|
| 50 Mpc/h, 128³, 96³ (one species) | LCDM to z = 2 | 37 s (0.27 s/step) | 1.3 GB |
| 50 Mpc/h, 128³, 2 × 96³ | H_Y path + conversion hook to z = 2 | 144 s (1.0 s/step) | 1.4 GB |
| 100 Mpc/h, 256³, 2 × 192³ (L366's box) | LCDM to z = 0 (FFT 4 workers) | 810 s (4.1 s/step) | 5.5 GB |
| 100 Mpc/h, 256³, 2 × 192³ | one H_Y chain force, 1 / 4 threads | 3.9 / 2.1 s | 4.1 / 4.6 GB |
| 150 Mpc/h, 384³, 2 × 192³ | one H_Y chain force, 4 threads | 4.9 s | 9.9 GB |
| 200 Mpc/h, 384³, 2 × 256³ | one H_Y chain force, 4 threads | 8.8 s | 11.6 GB |
| 24 Mpc/h, 192³, 192³ (linear box) | z = 9 to 0, 117 steps; 3 boxes at a time, 1 thread each | 240–310 s (two species: 570 s) | 2.5–5.6 GB per worker |
| 50 Mpc/h, 256³, 256³ | LCDM + live readout to z = 0 | 1130 s | 4.5 GB |
| 50 Mpc/h, 128³, 128³ | LCDM to z = 0.5 + strain reads (web channel) | 108 s | 2.3 GB |

The five stage-1 scripts together took about 1.5 h on at most 4 threads, one script at a time. None ran over 16 GB.

## The production plan (for the coordinator's go)

**Stage 2** (after FP19's re-audit; H_Y can run now if wanted): a cold dark fluid (no conversion), the chain reading, both
footings, matched LCDM and the MUTATE (FP13's: no onset switch, or FP9's: no floor).

| set | purpose | box | runs | time |
|---|---|---|---|---|
| A | cosmic shear, S8, halo masses at z = 0–1 | 100 Mpc/h, 384³, 2 × 256³ (0.26 Mpc/h), z = 49 → 0 | LCDM, separator (can, alt), MUTATE; 2 seeds | 8 runs × 30 min ≈ 4 h |
| A′ | the all-matter reading, as a bridge to FP13's numbers | as A | 1 per seed | ≈ 1 h |
| B | the resolution partner (the live readout, k ≤ 3) | 50 Mpc/h, 384³, 2 × 192³ | LCDM, can, alt | ≈ 0.8 h |
| C | the forest at z = 2–3 | 25 Mpc/h, 384³ (0.065 Mpc/h), 2 × 192³, to z = 2 | LCDM, can, alt, MUTATE | ≈ 0.8 h |
| C′ | the forest's convergence partner | 12.5 Mpc/h, 384³ | the same four | ≈ 0.8 h |

- Total about 7–8 h on 4 threads, one run at a time, at most 12 GB.
- Outputs:
  - P_m, P_b, P_lens and the carrier's own P at k = 0.3–3 h/Mpc, z = 0–1;
  - R(k) = P_lens/P_LCDM at z = 0.5 (GP3's gate), and a Limber cosmic-shear projection;
  - S8;
  - halo masses (L366's peaks);
  - P1D at z = 2, 2.5, 3 from the baryon particles;
  - the live readout's history.

**Stage 3** (after XR19 and the coordinator's go): conversion on at v_k = 575/600/625 km/s plus a v_k = 0 control, on A's
and C's boxes, dlna = 0.01.
- About 14 h (A, 2 seeds) + 3 h (C).
- Outputs: X-COP retention (L366's machinery), cosmic shear, Harvey (L370's machinery on z = 0.4 fields), the flagship residue
  at r_F (sub-mesh: the sub-grid bookkeeping plus XR16/XR12's shells), the forest, and the carrier's small-scale T²(k ≳ 1).
- Prerequisites:
  1. XR19's web channel with a per-particle strain (W3), validated against XR19's census.
  2. The sub-grid census calibrated on a resolved box, or Sheth–Tormen (T5b).
  3. The trigger's normalisation from XR12's band (δ_t0 ≈ 7.5–13.5) and the cap/cleared picture.

## Disclosures

- **Exploratory runs** (scratch, never committed) preceded every script: the L362 reproduction, timing and memory, FP9's and
  FP13's machinery reproductions, the static and Gaussian operator tests, the linear boxes (H_Y only), the strain reader.
  Each script's docstring lists what they informed.
- **Smoke runs** (scratch) of the scripts failed some first declarations. Each was revised before the committed run and is
  recorded in the script's HISTORY:
  - S1: the 6-cell floor became 8 cells, with yield surfaces scored separately.
  - G1: per-shell became log bins with the realisation noise.
  - T4f: the continuous-integral comparison is now reported; the leapfrog's own sum is scored.
  - T5a: "resolved" became a mass criterion, with a particle-mass cap and 16 copies.
  - T5b: now reported, with a 192³ run and a common realisation added.
  - W0: R_s = 0.5 is reported, R_s = 1 scored.
- **A preliminary run** of `XR21_s1_lcdm_controls.py` used an earlier core (cached CIC). The committed run used the final one.
- **The core gained two things after the committed runs of `lcdm_controls` and `conversion`**: `flow_strain` and the
  pluggable H_S rules. Neither touches those scripts' code paths.
- **The web channel's first MUTATE did not bite.** Its first run for the record passed W0 with the Hubble term dropped
  (rc 0), because W0 then scored only a correlation and a std, which a uniform shift leaves unchanged. W0 now also scores the
  eigenvalue level (0.0012 H against the declared 0.005 H; about 1 without the Hubble term), and the MUTATE fails (rc 1). The
  same run showed that W3's statement ("far fewer turned around" at every row) was wrong at z ≤ 1 for R_s = 0.5, and it was
  corrected to the rows. The first run's outputs are kept in scratch.
- **Two coordinator updates arrived during the stage** and are built in:
  - FP13's H_S, then XR18's finding that it is ill-posed. The H_S runs are code tests only.
  - XR19's web channel: stage-3 design plus the instrument.

## Files

- `XR21_pm_core.py`: the engine.
- `XR21_common.py`: the output tee, the check convention, and read-only loaders of L362's and L346's CLASS and of FP9's and
  FP13's machinery.
- The five stage-1 scripts:

| script | covers | main | MUTATE |
|---|---|---|---|
| `XR21_s1_lcdm_controls.py` | tests 1 and 2, the timing probes | 7/7, rc 0 | model on, rc 1 |
| `XR21_s1_separator_linear.py` | test 3 and the operator's unit tests | 12/13 (P3, the literal test, fails as pre-declared; reported), rc 0 | H_S without its onset switch, H_Y without its floor, rc 1 |
| `XR21_s1_conversion.py` | tests 4 and 5 | 14/14, rc 0 | v_k = 0 and no sub-grid, rc 1 |
| `XR21_s1_hs_readout.py` | the live H_S readout, a code test | 4/4, rc 0 | no onset switch, rc 1 |
| `XR21_s1_web_channel.py` | the web channel's instrument | 4/4, rc 0 | no Hubble term, rc 1 (second run; see Disclosures) |

- Each script has `.out`, `_MUTATE.out`, `_results.json` and `_results_MUTATE.json`.
- `XR21_s1_web_channel.py` imports XR19's committed `XR19_common.py` (read only).

Run from the repository root, e.g. `python3 real_research/cross_thread_review_2026_09_26/XR21_s1_conversion.py`; add
`MUTATE=1` for the control. `XR21_OUTDIR=<dir>` sends a smoke run elsewhere (never for the record).

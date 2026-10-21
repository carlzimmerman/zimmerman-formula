# CFG952 FROZEN CRITERIA: smoke tests for a labelled-domain-theory (LDT) PM engine change-set

Committed alone, before any CFG952 script, number or design output exists. Block 950–959 (LEDGER reservation row CFG950–959).
κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Cold energy (its mass is required; no
particle species is added). Framework-native only; no ΛCDM yardstick enters anything here. Not "theory closed". Nothing here can
say the data favour the framework. Any change after this commit is a dated, labelled amendment.

## 0. Scope

This lane designs the change-set that turns the class-A PM engine (CFG650 M1 + M2 + M3 / CFG654 native inputs; read with the Read
tool only) into an LDT engine, and checks the three LDT-specific mechanisms in a **separate toy prototype** at 64³. It runs no
production or medium job (nothing at 128³ or above), imports no CFG650 / CFG654 code and edits no file outside this folder. The
1024³ LDT run is only drafted (pre-registration DRAFT, not frozen here).

LDT ingredients (CFG947 §8 approximate parent; CFG945 H1 per-label tether): latched labels assigned at first turnaround from the
catchment machinery; an own-domain phantom (each label's own retained baryons; no external-field effect, EFE); a dipole-preserving
(momentum-conserving) source draw that fixes CFG947's T-M; a merge rule; the engine's kernel ν_mono; untethered (geodesic) cold.

## 1. The toy prototype (declared now)

**Units and mesh.** G = 1, a₀ = 1. Periodic box L = 40, mesh M = 64 (dx = 0.625). CIC deposit and CIC interpolation (the same
kernel), periodic spectral Poisson ∇²Φ = 4πG(ρ_tot − ρ̄) with the k = 0 mode removed, gradient ik with the Nyquist planes zeroed
(a momentum-conserving PM). KDK leapfrog. Kernel: a replica of the engine's ν_mono (RAR h, monotone floor δ = 0.05), written
independently from the formula.

**Matter.** Two particle sets per object: baryons (the MOND input; "retained baryons") and cold (geodesic dust, the supply). Each
object is a truncated Plummer pair: baryons truncated at 8 b_b, cold at 2.5 b_c.
- Host H: M_b 1.0, b_b 0.8; cold 5.36, b_c 4.0 (20 000 / 60 000 particles).
- Satellite s: M_b 0.2, b_b 0.3; cold 1.07, b_c 1.5 (8 000 / 16 000).
- Merger pair A, B: each M_b 0.5, b_b 0.6; cold 2.68, b_c 3.0 (12 000 / 36 000 each).
- Asymmetric host Hx: as H, with its cold Plummer centred 1.5 from the baryons along x.

**Labels (the engine's catchment machinery, toy form).** At t = 0 and every 10th step (E11 cadence):
- total particle density smoothed with a Gaussian of σ = 1 cell; peaks = 3×3×3 periodic local maxima with ρ_sm ≥ ρ_ta;
- r_ON = the largest node of geomspace(dx, 12, 14) with top-hat mean density ≥ ρ_ta at it and every smaller node (cover_peaks'
  rule); resolved iff r_ON ≥ R_min = 2 dx; ρ_ta = 1.0e-3 (absolute toy constant);
- partition of the union of resolved balls by the smallest d/r_ON (the engine's M1 / own_host_labels rule);
- latch (rule β): an unlabelled particle whose NGP cell lies in a resolved partition takes that partition's label. The partition is
  matched to an existing label if one label carries ≥ ½ of the labelled particle mass in it; otherwise a new label is created.
  Labelled particles are never relabelled except by the merge rule.
- r_ON and the edge are latched at label birth (no refresh jumps). Edge: r_e = x_h × min(r_M / ln(1 + M_b/M_c), r_ON), the
  kernel's supply root of the label's own baryon and cold masses, with x_h = 0.6 (declared toy headroom so that q < 1).

**Own-domain phantom (LDT-EXACT).** For each label D: CIC-deposit D's baryons into a sub-box centred on the cell nearest D's baryon
centroid X_D, half-width ⌈r_ON/dx⌉ + 2 cells; isolated (zero-padded, Hockney) convolution with the vector kernel −G r/|r|³
(0 at r = 0) gives g_D; s_ph,D = −∇·[(ν(|g_D|/a₀) − 1) g_D]/(4πG) by second-order central differences. D's baryons outside the
sub-box are counted as strays and reported.

**Source per label.**
- Deficit e_D = max(s_ph,D − ρ_c,D, 0) on cells with |x − X_D| < r_e, where ρ_c,D is D's own labelled cold. The tidal switch f_sw
  is omitted (= 1) in the toy.
- Draw on the shell r_e ≤ |x − X_D| < r_ON: comp_D = q_D ρ_c,D (1 + β_D·(x − X_c,D)), q_D = Σe_D/Σ_shell ρ_c,D (capped at 1 with e
  scaled by 1/q), X_c,D the shell cold centroid.
- S_D = s(t)(e_D − comp_D); S = Σ_D S_D is scatter-added to the mesh; ρ_tot = ρ_b + ρ_c + S.

**Draw variants.**
- E8: β = 0 (the engine's uniform draw).
- DIPFREE: β such that the realised dipole of S_D is 0.
- DIPSLAVE (the LDT rule): β such that the realised dipole equals a target D_t,D integrated with the particles' leapfrog from
  D̈_t,D = Σ_cells S_D g_tot dV (= −F′_D, the force of the total field on the sector). D_t = Ḋ_t = 0 at label birth.

β is solved from a 3×3 linear system. Positivity requires 0 ≤ q(1 + β·r) ≤ 1 on shell cells with ρ_c,D > 0. If that is violated,
β is scaled back to the positivity limit ("clipped") and the miss is recorded.

**Momentum book.**
- P_m = Σ m v (particles).
- Ḋ_meas,D = the central difference of the realised dipole Σ_cells (x − X_D) S_D dV.
- B(t) = |P_m(t) + Σ_D Ḋ_meas,D(t) − (same at the first defined step)|.
- I = Σ_steps Σ_D |F′_D| dt, the gross impulse of the run.

**Merge rule.**
- Trigger MR2 (OVERLAP): baryon centroids closer than ½ max(r_e,A, r_e,B).
- The merged label C takes the union of particles, with r_ON,C = (r_ON,A³ + r_ON,B³)^{1/3} and r_e,C from the union masses.
- RAMP (primary): S = (1 − w)(S_A + S_B) + w S_C, with w = ½(1 − cos π(t − t_m)/τ_m) and τ_m = r_e,C/(G M_b,C a₀)^{1/4}. Under
  DIPSLAVE, one β common to the three draws enforces D_t,C = D_t,A + D_t,B, with Ḋ likewise.
- INSTANT: w = 1 at the trigger.
- NONE: no merge.
- CFG947's M-R (MR1, bound fraction of own baryons in the own potential < ½) is evaluated and reported, not acted on.

**Runs.**
- (a) H at the box centre, s at rest 12 away. Labels at t = 0; dt = 0.04; run until the s–H baryon-centroid distance first reaches
  ≤ 5 or t = 30. DIPSLAVE draws. Snapshots at the refresh steps nearest to d = 12, 8 and 5 (or the minimum d reached).
- (b) Hx alone, ramp s(t) = ½(1 − cos πt/10) for t ≤ 10, then 1; t = 0–20, dt = 0.04. Run with each of E8, DIPFREE and DIPSLAVE.
  If the labels give more than one label, the label holding the baryons absorbs the others (fallback, reported).
- (c) A, B at separation 14 along x (offset 0.5 in y), at rest; dt = 0.04 to t = 30; DIPSLAVE. Run with each of RAMP, INSTANT
  and NONE.
- J_Φ(t) = ‖Φ_S(t) − Φ_S(t − dt)‖₂/‖Φ_S(t)‖₂, with Φ_S the periodic potential of S alone.

## 2. Pass lines

### K controls (VOID rule: any K fails ⇒ every class below is VOID, reported only)

| id | check | line |
|---|---|---|
| K1 | PM momentum: (a)'s configuration with S ≡ 0 for 50 steps, \|ΔP_m\| / Σ\|m g\| dt; and the discrete third law \|Σρ_m g_S + ΣS g_m\| / Σ\|ρ_m g_S\| for a random zero-sum S | both ≤ 1e-12 |
| K2 | isolated sub-box field of H's baryons: angle-averaged radial field vs the truncated-Plummer analytic, 3 dx ≤ r ≤ 0.9 r_ON | max \|rel dev\| ≤ 3% |
| K3 | own phantom mass of isolated H inside r_e vs the spherical QUMOND value r² g_N (ν − 1)/G | \|rel dev\| ≤ 5% |
| K4 | ν_mono replica: monotone on y ∈ [1e-6, 1e4]; equal to the RAR ν to ≤ 1e-6 (relative) for y ≤ 1 | both |

### Smoke tests

| id | test | line |
|---|---|---|
| a0 | label assignment and persistence (a): at t = 0 and at every snapshot, ≥ 99% of s's baryon mass carries one label ℓ_s ≠ ℓ_H, and ≥ 99% of H's baryon mass carries ℓ_H | PASS if all hold |
| a1 | no EFE (LDT-EXACT), at each snapshot: s's own phantom computed with every particle present vs from ℓ_s's particles alone | \|Δ log₁₀ M_ph(< r_e,s)\| ≤ 1e-6 dex and max\|Δs_ph\|/max\|s_ph\| ≤ 1e-6 |
| a2 | dynamic persistence: a0 and a1 hold at the end of the infall | PASS if both |
| b1 | momentum book, DIPSLAVE (b) | max_t B/I ≤ 1e-6, no clipping at any step, and realised dipole = target to ≤ 1e-9 of Σ\|S_D\|\|x − X_D\|dV |
| c1 | phantom continuity, RAMP (c) | max_t J_Φ ≤ 0.03 |
| c2 | conservation through the merger, RAMP (c): zero-sum per label at every step and the DIPSLAVE book | \|ΣS_D\|/Σe_D ≤ 1e-12; max_t B/I ≤ 1e-6 |

### Reported, no class weight
- The E4 global-phantom EFE (dex) at each (a) snapshot, and the LDT-MASK residual (the global field minus each label's
  baryon-weighted mean external field) at each snapshot.
- Own-phantom (sub-box) vs global satellite-only phantom (discretisation consistency).
- Satellite hover: the baryon-centroid vs cold-centroid acceleration difference of ℓ_s over g_host.
- DIPFREE's B/I; the headroom used, max q(1 + β·r); F′ magnitudes.
- MR1's bound fractions at the trigger and at the end; label counts and strays.
- J_Φ at the trigger step; M_ph,eff(t).
- RSS and timing.
- The EST stage (§4).

## 3. MUTATE (separate `*_MUTATE` outputs; exit 1 if every tooth bites, 2 otherwise)

| tooth | change | bites if |
|---|---|---|
| Mu1 | phantom = E4 global QUMOND field (the engine's) in place of own-domain | \|EFE\| ≥ 0.05 dex at the closest (a) snapshot |
| Mu2 | E8 draw in place of DIPSLAVE (b) | max_t B/I ≥ 1e-2 |
| Mu3 | INSTANT in place of RAMP (c) | J_Φ at the trigger step ≥ 0.05 and ≥ 2 × RAMP's max J_Φ |
| Mu5 | NONE (no merge) (c): at t = 30, Σ own phantoms of A and B vs the phantom of their union, both inside r_e,C about the union centroid | ratio ≥ 1.1 (T-L non-additivity) |

A toothless tooth is reported and weakens the matching smoke pass (stated as such).

## 4. EST stage (design numbers, reported)

From the engine constants (read only) and the record's NC1x run outputs (read only):
- the engine's r_ON grid at 1024³ and 256³, the effective RMIN node, and the M_ta / M_b thresholds;
- memory and runtime tables for the 1024³ change-set under declared scenarios (label count, own-phantom scheme), calibrated on
  NC1x's measured stage timings and peak RSS.

These are estimates, not results.

## 5. Lane class

| class | condition |
|---|---|
| SMOKE PASS | K all pass and a0, a1, a2, b1, c1, c2 all pass: "design ready for a 256³ validation stage" (never "ready for production") |
| SMOKE PARTIAL | K pass, some smoke test fails: the failing items are named as "design needs revision" |
| VOID | any K fails |

## 6. Compute and rules

- One process at a time; OMP_NUM_THREADS = 1; nice -n 10.
- In-script RSS guard at 1 GB (the process exits with code 3).
- 64³ only; nothing at 128³ or above.
- No downloads; no CFG650 / CFG654 import; no process touched.
- Stages K, MUTATE, MAIN, with separate outputs.
- A 1024³ run beside NC2x is forbidden; the 1024³ LDT run needs the owner's approval (§ pre-registration draft).

## 7. Design-stage disclosures

Read before freezing:
- the CFG654 engine (forces, cover_peaks, cover_balls, own_host_labels, x_supply, chi_cool / fcond_of, expel_m3, the checkpoint
  code) and its launcher settings;
- CFG654's criteria, addenda A1–A3 and README (NC1x result);
- CFG650's README;
- CFG947 (README, criteria, A1, derivation, main output);
- CFG945 (README; H1 / L2 sections);
- NC1x's run JSON (timing, peak RSS, host counts) and the engine's r_ON grid nodes.

Expectations formed while reading (no script run):
1. a1 holds by construction for LDT-EXACT; the content is in a0 / a2 (persistence) and in Mu1 (the E4 EFE is real in the PM).
2. E7 places the edge at the supply root, so q = 1 there; a dipole-preserving draw needs headroom, hence x_h.
3. CFG947's M-R may not fire in an equal-mass merger.
4. The effective RMIN at 1024³ is the r_ON node above 0.78125 Mpc/h.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.

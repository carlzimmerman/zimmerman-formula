# Z★ (v3s-OC) frozen test plan

Frozen with the design, before any test is run. This lane runs none of them. Each test reuses a verified pipeline: copy
its script into a new lane directory, never edit the original. Every run: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS,
minutes, no downloads, never beside a live 1024³ job (heavy jobs only through `compute_queue`, preemptible).
κ = ½ FITTED; both footings scored separately, never pooled. No new fitted constant may be introduced to pass a line;
where an input is history-dependent (the owned supply f_own) the test states a two-point bracket fixed here, and a verdict
is drawn only if both ends agree.

## 1. Order (decisive × cheap)

| order | id | question | pipeline | cost | kills Z★ if |
|---|---|---|---|---|---|
| 1 | **Z-T1** | Does retention (own frame, no EFE, released dust bound) explain the hosted excess? | `R/X1_hosted_recount/x1_per_system.csv` (Δ[iso AQUAL L*0], sdMC), `R/P1_dwarf_chemistry/p1_per_system.csv` (L_MDF), `R/S1_v3_hosted_small/`, CFG948 | minutes | FAIL |
| 2 | **Z-T2** | What does the capacity-truncated law do to the cluster terciles? | `R/X2_cluster_outskirts/x2_cluster_outskirts.py` (F1 functions, terciles, systematics (e)) | minutes | — (records the cluster row; forecast FAIL in MID) |
| 3 | **Z-T3** | Is the two-sided obstacle 0 ≤ D·P ≤ ρ_d well-posed? | `R/X3_switched_stiffness/x3_switched_stiffness.py` (B2-S symbol, slab ladder) | minutes | FAIL |
| 4 | Z-T11 | Do stars radiate the slow khronon/dust pair (Cherenkov)? | P3's pair speed (`R/P3_v3_strong_field/README.md`), Mistele 2103.16954 rate (prov) | minutes | loss time < 10 t_H for disc stars |
| 5 | Z-T5 | Red vs blue lenses from baryon loss | `R/S2_v3_lowg_lensing/s2_v3_lowg_lensing.py` | minutes | FAIL on both footings |
| 6 | Z-T6 | Owned supply SPARC needs vs the cosmic budget | `R/P4_v3_galaxy_tiles/p4_solver.py` inputs | minutes | budget exceeded > 2× |
| 7 | Z-T4 | Isolated outer lensing with the truncated law | `R/P2_spec_isolated_lensing/p2_spec_isolated_lensing.py` (primary), F2 (secondary) | ~30 min | FAIL at both bracket ends |
| 8 | Z-T10 | CMB / BBN in the dust limit, native H₀ | `R/Q6_v3_class/` (CLASS dust limit), C2 | ~1 h | only if Z-T1–T3 pass |
| 9 | Z-T9 | Cosmic shear and owned supply from a native PM with R1 + R2 | `R/L1_khronon_pm/`, `R/W1_pmedium_3d_scaleup/engine/` (preemptible), CFG963 fair control | hours, queued | Δχ² vs the fair control ≥ +9 on both footings |
| — | Z-T7 | Wide binaries | sealed v3s prediction; DR4 2026-12-02 | data-gated | a MOND-size boost |
| — | Z-T8 | MW disc and slope with a released round component | `R/X5_mw_joint_baryons/` | needs the MW's baryon-loss history | — (row stays FAIL) |

**First three decisive tests: Z-T1, Z-T2, Z-T3.**

## 2. Frozen lines

**Z-T1 (hosted retention).**
- Prediction per owner i, before tidal stripping (K9): Δ_pred,i ∈ [Δ_lo,i, Δ_hi,i] with
  Δ_lo,i = ½ log₁₀(1 + (M_gas/M★)_match) from the median gas-to-star ratio of X1's isolated LG field dwarfs within
  ±0.5 dex in log M★ (RAW HI masses; if the HI masses are not on disk: STOP and list them), and
  Δ_hi,i = ½ log₁₀(L_MDF_I0_m05,i) from P1 (cumulative processed baryons, an upper bound on the peak baryon content).
- Observed: X1's Δ[iso AQUAL L*0] and its sdMC (no EFE: the owner frame removes it).
- Classes: MW classical, bright M31 dSphs, MW ultra-faints, M31 others; control: isolated LG field dwarfs.
- **PASS**: in ≥ 3 of 4 classes the bootstrap class median of Δ_obs lies in [Δ_lo − 2σ, Δ_hi + 2σ], on both footings,
  and the control median is within 2σ of its own Δ_lo. **FAIL**: ≥ 2 classes outside the band on either footing, or the
  control fails. Otherwise UNDECIDED.
- Coma UDGs (side line, frozen): Δ_pred = ½ log₁₀(1/(1 − 0.81)) = 0.361 (CFG948 field HI-UDG gas fraction) against S1's
  isolated-law excess +0.33; PASS if within 2σ of S1's error.

**Z-T2 (cluster terciles).**
- Model: the law on each cluster's baryon profile inside r_s = r_M √(f_s(f_s+1)) (f_s = 5.364, record input), Newtonian
  enclosed mass M_b(<r) + f_s M_b,own beyond r_s; where R_own < r_s add the free excess f_s M_b − M_ph(R_own) with CFG930's
  native debris profile. R_own at 200ρ_c and at 18π²ρ̄_m (both reported).
- **PASS**: A_MID and A_OUTER within 2σ (systematics (e) included) in all three terciles, per footing. **PARTIAL**: OUTER
  passes, MID fails. **FAIL**: otherwise. Forecast written before running (`z1_successor_design.out`): MID unchanged
  (T2, T3 fail), OUTER moves toward the data (design/law at 2 Mpc 0.24 / 0.44 / 0.68 canonical).

**Z-T3 (two-sided obstacle).**
- Copy X3's slab and principal-symbol checks; add the upper obstacle D·P ≤ ρ_d (saturated region: held = all dust).
- **PASS**: the slab growth rate converges under resolution doubling (finest two within 10 %), the rigorous discrete bound
  holds, and the nonlinear sound speed c² ≥ 0 in saturated regions for ρ_d > 0, on both footings. **FAIL**: divergence or
  c² < 0 anywhere in a saturated region.

**Z-T11 (Cherenkov).** Emission rate of the khronon/dust pair by a mass moving at v > c_pair, with c_pair from P3 and
Mistele's formula (prov). **PASS**: energy-loss time > 10 Hubble times for the Sun and for MW disc stars at 24 and 90 pc.

**Z-T5 (red lenses).** Predicted red-to-law ΔΣ ratio √(1 + (M_gas/M★)_blue,match) at matched M★ (RAW gas scaling on disk;
if absent, STOP). **PASS**: S2's red inventory 1.313 / 1.200 within 2σ of the prediction per footing; blue stays at S2's
0.878 / 0.802.

**Z-T6 (SPARC supply).** Per galaxy f_req = ½(−1 + √(1 + 4(R_last/r_M)²)). Reported distribution; **FAIL** only if the
SPARC-implied owned dust, scaled by the record's baryon census (CFG953), exceeds Ω_c's budget by > 2×.

**Z-T4 (outer lensing).** The owner law truncated at r_s(f_own) plus a two-halo term from the linear dust power spectrum
(unowned medium = dust; C2 transfer). f_own bracket fixed here: {5.364, 50}. **PASS**: Δχ² (Z★ − zero-field v3) ≤ +4 on
P2 at both bracket ends and both footings. **FAIL**: ≥ +9 at both ends. Otherwise UNDECIDED.

**Z-T9 (shear).** Scored with CFG963's fair-control rule (engine vs a feedback-matched control), raw KiDS ξ±. **FAIL**:
Δχ² ≥ +9 vs the control on both footings.

## 3. Every matrix row → the pipeline that scores it

| row | status for Z★ | scored by |
|---|---|---|
| R1 GW, pulsars | INHERITED (COND) | C8 (no rerun; owner boundaries need Z-T3's extension) |
| R2 health | OPEN | Z-T3 (+ X3's 2D/3D gap) |
| R3–R5 law, MeerKAT, groups | INHERITED inside r_s | P4 (rerun only where Z-T6 finds R_last > r_s) |
| R6 isolated LG dwarfs | INHERITED + control | X1 (Z-T1 control) |
| R7 Cassini | INHERITED | C6, D7d |
| R8 outer globulars | INHERITED | D10 (non-owners in the MW field) |
| R9 wide binaries | PREDICTED Newtonian | Z-T7 (DR4) |
| R10–R11 MW | FAIL (inherited) | P4, S3, X5; Z-T8 data-gated |
| R12 TDGs, DF2/DF4 | PREDICTED Newtonian | U1 B0 (as computed) |
| R13–R14 satellites, Coma | PREDICTED | **Z-T1** |
| R15 clusters | FAIL (predicted) | **Z-T2** |
| R16 growth | INHERITED (dust limit) | F3 dust-limit row; Z-T10 |
| R17 BBN | PASS by construction | Q6 background (no K(Q)) |
| R18 CMB | INHERITED (dust limit) | Z-T10 |
| R19 isocurvature | OPEN | none until an origin is proposed |
| R20 a₀–Λ | INHERITED | Lean (V3_FULL_PICTURE §1) |
| R21 strong field | INHERITED | P3 |
| R22 lensing inner, red | INHERITED + PREDICTED | S2; Z-T5 |
| R23 lensing outer | PREDICTED, at risk | Z-T4 |
| R24 shear | OPEN, at risk | Z-T9 |
| Cherenkov (new) | OPEN | Z-T11 |

# CFG963 FROZEN CRITERIA: attribution of the native shear pass (cold-sector rules M1+M2 vs census gas expulsion M3)

- **Date:** 2026-10-21. Committed ALONE, before any script of this lane and before any surrogate number or transfer array was
  computed. Block 960–969 (LEDGER reservation b1c854bb1).
- **Status:** a DIAGNOSTIC attribution. Reported only; **no verdict weight** on CFG654 A2/A3 (NC1x / NC2x HOLD as frozen there).
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled. Raw KiDS-1000 / DES Y3 data, framework-native
  scoring (the frozen CFG654 native scorer). No HMcode, BAHAMAS or ΛCDM yardstick anywhere. Cold energy MASS still required.
  Not "theory closed". A CONSISTENT class does not mean the data favour the framework.

## 1. Facts fixed from the code before this file (read only)

- **NCS0 has no M3.** CFG654 launcher job `NCS0` = switch `S0`, modules "" (M1–M4 off), inputs native_cmb, 1024³, L100, seed 359.
  In the CFG654 engine's `forces()`, `switch == "S0"` returns the plain Poisson potential φ_k = (−1.5 Ω_m / a) δ_k / k² before any
  module, census or footing code runs. So NCS0 is plain Poisson gravity on all matter: no MOND input, no settling source, no M3.
- **What M3 does** (`expel_m3`, called from `_finish_phik` in EVERY RES force call, dynamical steps and snapshots alike): the
  Newtonian source density becomes δ_src = δ + Σ_k [G_σk ∗ e_k − e_k], with e_k = f_b (1 − f_ret,census,k)(1 + δ) on the cells of
  catchment class k and G_σk a unit-mass Gaussian of σ = r_ON,k (comoving Mpc/h). The k = 0 weight is 1, so mass is conserved.
  Only the SOURCE moves; the particles are tracers of the total, but they respond dynamically to the changed potential
  (back-reaction is inside the run). The scorer reads the framework run's GRAVITATING spectrum P_grav
  (δ_grav = −k² φ a / (1.5 Ω_m)), which contains the re-placement, and the control's particle spectrum P.
- **M3's rule reads no footing:** f_ret,census is a function of M_ta(r_ON, Δ_ta); r_ON comes from the density field. The footing
  enters M3 only through the evolved field.
- **Matched outputs on disk** (read only; `_external_data/`):

  | run | resolution | inputs | footing | modules | folder |
  |---|---|---|---|---|---|
  | NCS0 | 1024³ | native_cmb | (none) | S0 | cfg654_work/NCS0 |
  | NC1x / NC2x | 1024³ | native_cmb | canonical / alt | M1+M2+M3 | cfg654_work/NC1x, NC2x |
  | P0 | 1024³ | inherited | (none) | S0 | cfg596_work/P0 |
  | T12 | 1024³ | inherited | canonical | M1+M2 | cfg650_work/T12 |
  | T1x / T2x | 1024³ | inherited | canonical / alt | M1+M2+M3 | cfg650_work/T1x, T2x |
  | VLs / V0 | 256³ | inherited | (none) / canonical | S0 / all OFF | cfg596_work/VLs, cfg650_work/V0 |
  | VM3 / VM12 / VM123 | 256³ | inherited | canonical | M3 alone / M1+M2 / M1+M2+M3 | cfg650_work/VM3, VM12, VM123 |
  | VNcs / VNc12 | 256³ | native_cmb | (none) / canonical | S0 / M1+M2 | cfg654_work/VNcs, VNc12 |

  Every run has snapshots z = 0, 0.5, 1 with P and P_grav. The 1024³ runs share identical k bins (checked), as do the 256³ runs.
  There is no native-input 1024³ M1+M2 run, no 1024³ alt M1+M2 run, no M3-alone run on the S0 engine, and no 256³ native M1+M2+M3.
- **Seen before this file (disclosed):** README numbers only: 256³ inherited P_grav/P_S0 − 1 at k 0.3/0.5/1 = +0.005/+0.014/+0.031
  (M1+M2), −0.022/−0.037/−0.048 (M1+M2+M3), +0.235/+0.549/+0.415 (M3 alone, all-OFF engine); CFG646 static DIFF-S ratios; T12
  B(z = 0) 1.005/1.012/1.023; T2x 0.974/0.965/0.949; NC1x 0.972/0.961/0.949; NC2x 0.975/0.967/0.955; the stored NC1x/NC2x scores
  (KiDS −10.08 / −9.39 with their robustness values). No transfer array was computed from the run files and nothing was scored.

## 2. Transfers and surrogates

All transfers are taken **node by node at the runs' own snapshots z = 0, 0.5, 1** and on the shared k bins; there is no redshift
interpolation beyond what the frozen scorer itself does for every run (log-linear between nodes, native growth above z = 1).

| name | definition | role |
|---|---|---|
| **M3-1024** | T^grav = P_grav(T1x) / P_grav(T12); T^part = P(T1x) / P(T12) | **PRIMARY T_M3** (production resolution, same ICs/seed/steps) |
| M3-256 | P_grav(VM123) / P_grav(VM12) (particle analogue likewise) | bracket R1 (resolution) |
| M3-alone-256 | P_grav(VM3) / P_grav(V0) | bracket R2 (the only M3-alone run; all-OFF environment with the CFG596 excess; reported only) |
| **M12-1024** | T^grav = P_grav(T12) / P(P0); T^part = P(T12) / P(P0) | **PRIMARY T_M12** (alternative attribution) |
| M12-256n | P_grav(VNc12) / P(VNcs) | bracket (256³, native_cmb inputs) |
| M12-256i | P_grav(VM12) / P(VLs) | bracket (256³, inherited) |
| C1-can / C1-alt | P_grav(T1x) / P(P0); P_grav(T2x) / P(P0) | closure control (the whole M1+M2+M3 transfer) |

- **256³ transfers on the 1024³ bins:** log T interpolated in log k; for k > k_hi,256 = π·256 / (4·100) = 2.011 h/Mpc, T is held at
  its value at k_hi,256 (the 256³ run's own support limit). The 1024³ transfers need no interpolation.
- **Surrogate in the framework slot** ("S0+X"): a copy of NCS0's stored dictionary with, at each node, P_grav := P_NCS0 × T^grav and
  P := P_NCS0 × T^part (P only enters the scorer's 'held' robustness spectrum). Its footing label is the footing being compared
  (only the T-OWN injection reads it; Δχ² does not).
- **Surrogate in the control slot** (for NCx vs S0+M3): a copy of NCS0 with P := P_NCS0 × T^grav, i.e. the control's lensing
  spectrum is its GRAVITATING spectrum, the same convention the scorer applies to the framework slot.
- **Assumptions (stated in the README with the numbers):** (i) environment/multiplicativity: M3's fractional effect measured on the
  M1+M2 background equals its effect on plain Poisson gravity; (ii) input set: transfers measured with inherited inputs are applied
  to the native_cmb control (tested by C1); (iii) footing: the canonical T_M3 is used for the alt comparison (M3's rule reads no
  footing; T2x/T1x is reported); (iv) resolution: none for the primary; R1 tests it; (v) k range: the scorer's nodes run from
  k_lo = 0.080 to k_hi = π·1024/(4·100) = 8.04 h/Mpc, every node carries a measured transfer, and above k_hi the scorer's own
  power-law continuation applies.

## 3. Scorer

The frozen CFG654 native scorer (`cfg654_native.py`; `load_lib("native_cmb")`, `build`, `klass`) is imported read only. Because its
`score_production` writes into the CFG654 folder, its statements are re-implemented verbatim in this lane's script with the run
dictionaries passed in and outputs written here. Same data, cuts, support mask (f ≥ 0.9), nuisances, fit, robustness set
{widen2, noIA, held, LOC}, DESI distances reported only, T-OWN tooth and NZ1 (MUTATE pass run FIRST for every scored pair), classes.
Attribution classes use KiDS-1000; DES is reported.

## 4. Controls (gates)

- **K (reproduction):** the re-implementation must reproduce the stored `cfg654_native_results_NC1x.json` and `_NC2x.json`
  (N_kept, χ²_S0, χ²_F, Δχ², every robustness value, DESI, class; both surveys) and the stored MUTATE T-OWN χ² (17.11 / 8.14 and
  22.56 / 10.31) to |Δ| ≤ 1e-9. If K fails, nothing below is interpreted.
- **MUTATE M0:** a surrogate with T ≡ 1 vs NCS0 must give Δχ² = 0 (|Δ| ≤ 1e-9) on both surveys, main and every robustness value.
- **MUTATE M1:** a planted T ≡ 0.9 (P_grav and P, all k and z) vs NCS0 must bite: |Δχ²_KiDS| ≥ 1.
- **C1 closure (gates the interpretation, not the arithmetic):** NCS0 × C1-can vs NCS0 is compared with the stored NC1x −10.08, and
  NCS0 × C1-alt with NC2x −9.39 (KiDS). PASS if |difference| ≤ 2.0 on each footing. If C1 fails on a footing, its class is still
  computed as frozen, flagged "transfer-limited", and the self-consistent fraction f_sc = Δχ²(S0+M3) / Δχ²(C1) is reported beside it.
- Separate `_MUTATE` outputs.

## 5. Scores (KiDS + DES each)

(a) S0+M3 vs NCS0 for M3-1024, M3-256, M3-alone-256; (a′) S0+M12 vs NCS0 for M12-1024, M12-256n, M12-256i; (c) C1-can, C1-alt vs
NCS0; (b) NC1x vs S0+M3 and NC2x vs S0+M3 for M3-1024, M3-256, M3-alone-256; reported: NC1x / NC2x vs S0+M12 (M12-1024).

## 6. Attribution classes (KiDS, per footing, PRIMARY transfer M3-1024)

f = Δχ²(S0+M3 vs NCS0) / Δχ²(NCx vs NCS0), with the stored Δχ²(NC1x vs NCS0) = −10.08 (canonical) and Δχ²(NC2x vs NCS0) = −9.39
(alt); d = Δχ²(NCx vs S0+M3).

- **M3-CARRIED** if f ≥ 0.70 AND |d| ≤ 3;
- **LAW-CARRIED** if f < 0.30;
- **SHARED** otherwise.

Reported with it: the classes under R1 and R2 (if R1 differs from the primary, the primary class is labelled "not robust to the
resolution transfer"); f for each robustness variant (widen2 / noIA / held / LOC / DESI); f_M12 = Δχ²(S0+M12) / Δχ²(NCx) and the
sum f + f_M12 (Δχ² is not additive; the gap is reported, not interpreted).

**Can KiDS tell the cold sector from plain gravity + gas expulsion?** Only if |d| ≥ 4 (the CFG592 TENSION scale) with all four
robustness values of d of the same sign; otherwise the statement is "KiDS cannot tell them apart at this power".

## 7. Pre-declared reading (plain; whichever happens is reported equally plainly)

- **M3-CARRIED:** the shear pass says (1) the framework's capped cold sector does not overproduce structure (unlike CFG596's +68.7)
  and (2) gas expulsion lowers power. It is NOT a preference for the framework's law over plain gravity with feedback. The
  engine-parent problem is then not load-bearing for the shear result: any parent that clusters like plain dust on k ≲ 1 h/Mpc and
  expels gas would pass.
- **LAW-CARRIED:** the lead comes from the cold-sector rules themselves, not from expulsion; the engine-parent problem is then
  load-bearing for the shear result.
- **SHARED:** both contribute; the proportions are reported and neither statement above is made.

## 8. Not done here

No PM run of any size. The decisive 1024³ control NCS0+M3 (plain Poisson with census gas expulsion, native ICs) is DESIGNED in
`FROZEN_CRITERIA_1024_DRAFT.md` (a DRAFT, not frozen, not queued; it would follow CFG960's chain). Process rules: one process at a
time, < 1 GB RSS (in-script guard), one thread, nice 10, pause if free + inactive memory < 3 GB. No edits to CFG654/650/909/960
files, LEDGER or THEORY_CANONICAL.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.

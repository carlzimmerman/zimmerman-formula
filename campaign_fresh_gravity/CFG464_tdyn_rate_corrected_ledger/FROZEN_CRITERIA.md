# CFG464 FROZEN CRITERIA: the zero-constant t_dyn settling rate (lambda = 1) on the CORRECTED cold-budget ledger

Frozen before any CFG464 script exists. Re-runs CFG429 (door 4 of the 10-07 list), whose verdict is marked SUPERSEDED /
PENDING by its forward note (dc742f798). kappa = 1/2 is FITTED. Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10)
are reported separately, never pooled. No dark-matter particle; the cold fluid's mass is still required. No downloads.
Read-only on CFG429, CFG382, CFG450-453, the 10-08 audit and deepseek_push (T15/T16).

## What was wrong with CFG429's ledger (from the committed record, before any computation here)
1. **Group/cluster deficits in the wrong units (CFG453).** CFG429 copied T15's group/cluster rows, which hold CFG382
   definition A, x_A = (M_tot - M_b - M_ph)/(5.364 M_b), in place of T15's own x = (M_tot - M_b)/M_b.
2. **Mixed Milky Way baryon mass (10-08 audit, 517648b5e, a2).** CFG429's MW-30 row takes x = 1.80, i.e. M_tot/M_b with
   M_b = 1e11 Msun, but computes the kernel supply S at M_b = 7e10 Msun. One row, two baryon masses.
3. **Gas radius: not a problem (CFG450).** The X-COP RADIUS column is in R/R500, so the CFG382 audit already reads the gas
   at R500. CFG464 reads it at the JSON R500 exactly as CFG453 does.
4. CFG429 used a0 = 1.2e-10 (T15's value), which is neither footing.

## The ledger (T15's identity, unchanged)
M_cold/M_b = x - f * S/M_b, with
- f = 1 - exp(-lambda * sqrt(4 pi G rho) * tau), tau = 10.3 Gyr (CFG382 / T15), lambda = 1 ("zero constants");
- S/M_b = 1/(exp(r_t/R) - 1), r_t = sqrt(G M_b / a0) (T9 closed form).
A row is FEASIBLE iff M_cold/M_b >= 0.

## Inputs
- **Groups and clusters.** x_T15 = (M_tot - M_b)/M_b per object, with M_tot = M_HSE/(1 - b), for b = 0 and b = 0.3.
  The objects are the 7 X-COP clusters and 20 Lovisari groups, read exactly as CFG453 reads them (gas at the JSON R500;
  group M* = 0.10 M_gas placeholder). x_T15 is a0-free. rho at R500 = T15's 1.55e-24 kg/m^3 (held).
  Two S conventions, always reported separately:
  - (i) T15 conventions: groups M_b 6e12, R 554 kpc; clusters M_b 2.8e13, R 985 kpc; row = median x - f S.
  - (ii) per-object S from each object's own M_b and R500; row = median over objects of (x_i - f S_i).
  GC rows = {groups_b0, groups_b03, clusters_b0, clusters_b03} x {(i), (ii)} = 8 rows per footing.
- **Milky Way at 30 kpc.** x = V^2 R/(G M_b) - 1 and S = S(M_b, 30 kpc, a0), with ONE M_b per row. Both variants are
  reported, each consistent throughout: **M_b = 7e10** (T15's stated enclosed baryons) and **M_b = 1e11** (the mass T15's
  hard-coded x implies; T16 used both). Speeds V = 188, 200, 230 km/s. rho_30 = V^2/(4 pi G R^2) at each V.
  The CFG429/T15 mixed row (x at 1e11, S at 7e10) is printed as a LEGACY disclosure only and is not scored.
- T15's a0 = 1.2e-10 rows are printed as a reference only (not a footing, not scored).

## Decision (per footing, then overall)
- **NOT EXCLUDED** if any GC row (either S convention) is feasible.
- **EXCLUDED** if every GC row is negative AND the MW row is negative at all three speeds for both M_b variants (a robust
  MW speed: the sign does not depend on V).
- **MW-SPEED-DEPENDENT (undecided)** otherwise, i.e. every GC row negative and the MW sign changes with V or M_b.
- **Overall:** the common label if the two footings agree; "FOOTING-DEPENDENT" if they differ. Tag "ROBUST" if all 8 GC
  rows are feasible on both footings, "PARTIAL" if only some are.
- **MW-speed dependence (reported, not a verdict):** for each footing and M_b, the sign at 188/200/230 km/s, the label
  robust-negative / robust-positive / speed-dependent, and the zero-crossing speed V0 where x = f S. Under the rule above
  a negative MW row cannot by itself reverse NOT EXCLUDED; it is reported as an MW-30 tension flag: TENSION if negative at
  V = 188 km/s (the speed CFG451 calls measured) for that M_b.
- **Also reported (not a verdict):** per-object counts of negative x_i - f S_i; the binding (minimum) GC row; median
  S_i - (nu_i - 1) (how the kernel supply compares with the law's phantom); f at rho_R500/10 (a sensitivity to T15's
  rho convention, which is ΛCDM-based); and the plain statement that at lambda = 1, f -> 1, so the group/cluster rows do
  not test lambda at all once x_T15 > S (CFG453: no lambda ceiling on the corrected ledger).

## Controls (a failed control is reported and kept, never silently fixed)
- **C1:** x_T15 medians equal CFG453's committed D1.xT (both footings, b = 0 and 0.3) to 1e-9.
- **C2:** at lambda = 0.028 the code reproduces CFG453's committed D2 rows (i) and (ii) on both footings to 1e-9.
- **C3:** at lambda = 1 the GC rows (convention (i)) and the consistent-M_b MW rows at V188/V200 match the audit's
  a2_cfg429_rescore.json on both footings to 2e-3 (a2 uses f = 1 exactly and x medians rounded to 3 decimals).
- **C4:** with CFG429's own inputs (x_A rounded 0.79/1.76/0.41/0.91, a0 1.2e-10, MW x = 1.80 with S at 7e10, rho at
  V200) the code reproduces CFG429's committed rows (-1.05, -5.36, -4.39, -4.57, -4.07) to 0.005.
- **C5:** f(lambda = 1) >= 0.9999 in every scored row.

## MUTATE (CFG464_MUTATE=1; outputs *_MUTATE.*)
Declared in advance: on the corrected ledger lambda = 0.0073 brings NO group/cluster row to zero, because x_T15 > S
(CFG453 finds no cluster ceiling). The literal "lambda = T15 cluster ceiling" mutation is therefore well-posed only on the
ledger where that ceiling exists. So the mutation plants the CFG429 misread x := x_A and sets lambda to the cluster ceiling:
- **M1a:** T15's committed conventions (a0 1.2e-10, x_A 0.41) with lambda = 0.0073 (T15's cluster ceiling): the binding
  row clusters_b0 must satisfy |M_cold/M_b| <= 0.01.
- **M1b:** per footing, x_A from CFG450 (footing-matched) with lambda = CFG451's committed footing cluster ceiling (from
  cfg451_results.json): clusters_b0 under convention (i) must satisfy |M_cold/M_b| <= 0.01 on both footings.
- **M2:** with x := x_A and lambda = 1, every GC row (both conventions, both footings) must be negative, i.e. the
  group/cluster part of the verdict flips to the CFG429 picture.
- Also printed (sensitivity, not a check): the corrected-ledger GC rows at lambda = 0.0073 (expected all positive).

## Outputs
cfg464_tdyn_corrected.py, cfg464_tdyn_corrected.out / _MUTATE.out, cfg464_results.json / _MUTATE.json, README.md.
The README states that CFG464 supersedes CFG429's verdict. CFG429 is not edited.

# CFG658 — the one-action construction (CFG694 + CFG695 + CFG693) on the gates it has not faced (frozen criteria, committed alone)

Written 2026-10-13, before any CFG658 script exists and before any CFG658 number. Committed alone. Departures go in the README,
dated; this file is never edited. ID check: no `CFG658*` directory, no commit mentioning CFG658, no LEDGER row (checked before
writing).

κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², scored separately, never pooled; a₀ flat. "Cold energy"
throughout; its mass is still required (no particle species). No ΛCDM quantity and no standard-MOND yardstick enters any verdict;
where a reused harness carries a ΛCDM-built ingredient the row is labelled CONTEXT / no verdict weight. Not "theory closed".
Nothing here says the data favour the framework. One process, ≤ 1.5 GB, `nice -n 10`; no PM is run; nothing is downloaded. The
Lean chat's lane files (CFG690–699) are read only.

## 0. What is scored
**The construction (C\*)**: L = −|∇Φ − 4πG P|²/8πG − ρ_bΦ − W(P) − (γ/2)|∇P|² + kinetic (CFG694), with the saturating vacuum
W′(u) = u/(1 − u/a₀), u = 4πG|P| (CFG695), whose unscreened static law is **g_N = g²/(g + a₀)**, i.e.
ν_s(y) = ½ + √(¼ + 1/y) (y = g_N/a₀); the stiffness length L\* = 5.75 pc (CFG691 L\*_min, carried over by CFG695 S3); and the
free-fall-basin reading (CFG693): each node reads only its own baryons inside its free-fall basin, the uniform external field
removed.

**Kernel swap rule.** Every reused harness is executed read-only, unchanged except that its kernel ν is replaced by ν_s. A
harness's own kernel is its baseline (ν_mono of CFG4/FP1/cfg100_lib, or the exponential ν = 1/(1 − e^−√y) where the harness uses
it: CFG556, CFG652/CFG540). The source of the law is **all baryons** in C\* as built (P is driven by ∇Φ, whose source is all of
ρ_b); the condensed-only source of Theory v2's A5 is scored alongside wherever the harness has it, and the tension is reported.

## 1. Gates

### S0 SPARC control (raw, CFG695 S2 statistic re-executed)
ν_s reproduces CFG695's 0.1009 @ Υ 0.60 / 0.0994 @ 0.55 to 1e-4 with identical Υ. Load-bearing control (exit 1 if it fails).

### G-C3 early types
- **C3-R (verdict, framework-native, raw lensing).** CFG669's T2 statistic on Ks masses: A_obs = K9 log₁₀ ratio of the early and
  late stacks matched in Ks baryonic mass (40 quantile bins, CFG669's weights; CFG585 head and CFG531 `esd_loo` exec'd unedited).
  Control: A_obs = +0.2802 ± 0.0832 reproduced to 1e-4. The law's prediction A_law is the same statistic evaluated on model ESDs:
  each lens's law ESD in its 15 g-bins (bin radii R_k = √(G M_gal/g_k) from the data's M_gal, as the estimator's binning; mass =
  the lens's Ks baryonic mass M_b,K; own profile = point mass + the law's phantom to the law's r_ta, CFG531 `fin`/`r_ta_law_k`
  code, no environment term, no stripping), stacked with exactly the estimator's weights WW × r and combined over K9 with the same
  W. Residual D = A_obs − A_law, σ = the jackknife σ of A_obs.
  **PASS iff |D| < 2σ on both footings; FAIL iff D ≥ 3σ on both footings; TENSION otherwise.** Reported: A_law for ν_mono too.
- **C3-A (CONTEXT, no verdict weight; environment term is ΛCDM-built).** CFG531's ε (GLS amplitude over law + CFG529 environment)
  with LAW_RTA own tables rebuilt with ν_s at the footings (afac = 1): all f30, early and late classes, bands K-in (52–98 kpc) and
  K9, constructions A and B. Reported against ν_mono's recorded ε. Question answered: does ν_s add mass at 50–100 kpc relative to
  ν_mono (Δε < 0) or remove it (Δε > 0)?

### G-CL clusters (raw data; law sourced by all baryons unless stated)
- **CL1 CFG686** (8 ACCEPT clusters, raw KiDS-1000 shear, stored stacks): A = ΔΣ_obs/ΔΣ_law per band with ν_s predictions from
  CFG686's `law_dsigma` (all 18 brackets + Newton, same bootstrap seed and key order). Label = CFG686's own `verdict` rule
  (LAW SUFFICES / CORE EXCESS / EXTENDED EXCESS / LAW OVERPREDICTS / MIXED) per footing, primary bracket; brackets counted.
- **CL2 X-COP headline (1000 kpc) and inner band (200–420 kpc)**, CFG634 T3 cells with ν_s: B|R0 (all baryons, no reservoir =
  C\* as built), HCB|R0 (condensed only, A5), B|RI and HCB|RI (identity reading), B|RNc4 and HCB|RNc4. Label = CFG634 `t3_label`
  (PASS iff |η − 1| ≤ 0.20 both footings; FAIL iff η ≥ 1.30 or ≤ 0.77 and ≥ 3σ both footings; else TENSION). Also CFG4's
  `cluster_table` η / residual (M_b units) with ν_s.
  **C\* cluster verdict (as built: law on all baryons, pure field, no reservoir) = the B|R0 headline label AND the B|R0 inner label;
  PASS only if both PASS.**
- **CL3 CFG652** (131 eFEDS groups × raw KiDS-1000): models (a) condensed source and (b) all-baryon source recomputed with ν_s for
  the PRIMARY variant x1 only, both footings (compute budget; the p02/m02/g1/g4 variants are NOT run here — declared now). Label =
  CFG652's frozen rule (BOTH EXCLUDED / (a) FAVOURED / (b) FAVOURED / NOT DIAGNOSTIC). C\* as built is model (b).

### G-EFE
- **E1 wide binaries** (CFG447: frozen DR4 pipeline imported read-only, sha256 checked; same seeds, same DR3 numbers).
  Injections: (i) basin only, no stiffness: EFE-blind ν_s (= CFG447's ν_P2 row, which is ν_s exactly); (ii) **C\***: basin +
  stiffness, per-pair boost √(1 + g_an/g_N) with g_an from CFG691's universal profile at L\* = 5.75 pc for the pair's own mass
  (M_obs, r = √(G M_obs/g_true)). CFG447's rule: EXCLUDED BY DR3 iff z_builder > 5. Added (frozen here): **CONSISTENT iff
  |z_builder| < 2 on both footings.** C\* E1 verdict = injection (ii).
- **E2 cluster satellites** (CFG478 harness: cm14b parsing exec'd read-only, Sifón lensing masses, NFW host as the harness has it,
  retained term unchanged). Basin rule: the satellite's own isolated-law phantom (ν_s, g_e = 0 by T1) counts only inside its
  free-fall basin edge r_J, solving g_s(r_J) = T r_J with T = G M_h(R)/R³ (2 − dlnM_h/dlnR) at the harness's R; M(<r_bg) =
  M_b + M_ph(< min(r_bg, r_J)) + ret. Stiffness: CFG694 G4 (unscreened) is re-checked (S ≥ 0.99). **PASS iff χ²/5 has p > 0.01 on
  both footings** (CFG478's survival line). Reported: the isolated (r_J → ∞) and the EFE-on (basin off) rows with ν_s.
- **E3 every star a node.** CFG694 G3 statistic (a star's own phantom inside min(r_J, 1.08 pc) at L\* = 5.75 pc, M = 1 and
  0.3 M☉, both footings) recomputed with the saturating nonlinearity in CFG691's reduced equation:
  −[q″ + 2q′/s − 2q/s²] + q|q|/(1 − ε q) = 1/s², ε = r_M/ℓ_γ (= the cubic equation at ε = 0). **PASS iff M_ph/M ≤ 0.155** (CFG694's
  McKee+2015 line). If the solver fails, the item is reported OPEN with the cubic value and the bound ε q ≤ ε/2.

### G-D2 growth (CONTEXT ONLY — the halo model's mass function, bias and NFW comparator are ΛCDM-built; no verdict)
CFG556 executed with its kernel swapped to ν_s, and to ν_mono (FP1/cfg100_lib) as a second reference: E = max(R − 1) over
0.05 ≤ k ≤ 1, R(k) at 0.3, 0.5, 1 h/Mpc, σ8 ratio, both footings; ΔE versus CFG556's recorded kernel. Plus a written spec (no run)
for a native 1024³ PM with ν_s (`PM_SPEC_1024.md`).

## 2. Lane reading (frozen)
- C\* **passes a gate** only by that gate's PASS line above; CONTEXT rows never pass or fail anything.
- Summary label per footing: list of gate labels. No pooling across footings. If any verdict gate FAILS, the summary says
  "C\* FAILS <gates>"; no gate is described as closed by a CONTEXT row.
- **A5 tension (frozen reading).** If the cluster/group gates prefer one source (all baryons vs condensed) the lane states which,
  and states that C\* as an action has no phase label: hot gas sources P exactly as stars do, unless an added term distinguishes
  them. That is a conflict with Theory v2's A5 whichever way the data lean.

## 3. MUTATE (each must reproduce the record; a failed reproduction is a lane bug and exits 1)
- **M-K (kernel back to the harness's own kernel):** CFG531 ε (K9, K-in; all/early) to 1e-6 of the recorded values; CFG686 A
  table to 1e-9; CFG4 η 1.820 / 1.679 to 1e-6 (median, b = 0); CFG634 T3 cells to 1e-6; CFG652 χ² 22.9 / 28.7 (can) and
  22.3 / 25.2 (alt) from the stored models, plus ≥ 5 groups' model ESDs recomputed with the stored kernel equal to the stored ones
  (1e-9 rel); CFG556 E +0.715 / +0.883 (1e-3); SPARC ν_mono 0.1003 / 0.0991.
- **M-B (basin rule off):** CFG478 Q1 χ² with its own kernels (P2, ν_mono) reproduced to 0.05; wide binaries without stiffness
  reproduce CFG447's ν_P2 rows (median, z to 0.05).
- **M-S (stiffness off / cubic):** E3 at ε = 0 reproduces CFG694 G3 0.0352 (1e-4).
- **M-T (tooth, C3-R):** multiplying the early lenses' model mass by 10^0.3 must move A_law by ≥ 0.05 (the statistic can see a
  type-dependent mass); if it does not, C3-R is NOT DIAGNOSTIC.

# Z8-WAVE BRIEF (conductor, 2026-09-28 tick — pre-registered BEFORE any run)

Spawn trigger: 0 deepseek lanes running (ps aux: only live-lab XR29 in
real_research/cross_thread_review), register OPEN doors non-empty. delegate_task
confirmed absent (tool_search) — conductor-built lanes, Z6/Z7 precedent.

## Door audit that selected these doors (conductor, this tick, on-disk evidence)
1. **LR4b MISBANK FOUND (append-only correction follows in the register):** the
   committed `fable_independent_2026/lean_2026/LR4b_cov_discharge.lean` still
   states `chord_cond`/`I1_cond` WITH the hypothesis
   `(cov : ∀ H, Continuous ... → covStatement H)`; no committed file proves
   `covStatement` generically (grep: only LR3b/LR4b mention it; both keep the
   hypothesis). The Z7 register row's "covStatement DISCHARGED ... UNCONDITIONAL"
   is therefore NOT supported by the file on disk — the axioms-clean `#print`
   does not distinguish conditional from unconditional theorems. Correction:
   Z8 LR4c actually proves the generic discharge.
2. Standing OPEN doors from the Z6/Z7 ops notes: (a) unconditional I2/I3
   (17/60, 149/700); (b) M05-I thin-window curve R_v(0,q) = (3/4+5q/12)/(a+bq)
   recorded CANDIDATE-only by MC4, "its own closure needs its own door";
   (c) register rows 12/17/18/19 Lean legs ("open (M01)") — audit shows rows 17/19
   are ALREADY certified by M01_alg_spine.lean §4/§5 (j10i_window_decomp,
   k04_* family) — disposition lane LR6, not new math.

## Lanes (3; prefixes owned: LR4c_*, MC5_*, LR6_*; no other series touched)

### LR4c — generic covStatement discharge + unconditional I2/I3 (owner: conductor)
Claim chain (conductor hand-derivation, verified 3× against LR3's certified
1D polynomials before the Lean attempt): for the forward first-flight integrand
H_k(u,v) = ∫_0^{s−v}(u²+(v+w)²)^k dw (s = √(1−u²)), covStatement's RHS slice is
2u·s²·[poly] → with s²=1−u² exactly the LR3 polynomials: k=1 → val_I1 (5/12),
k=2 → val_I2 (17/60), k=3 → val_I3 (149/700); chord (k=0) → val_chord (3/4).
KILL (pre-registered, Z7 amendment-2 precedent): composition fails to compile
zero-sorry after honest attempts → blocker recorded verbatim, exit 1. Any
constant mismatch vs {3/4, 5/12, 17/60, 149/700} → exit 1.
Gates: R0 independent numerical quadrature of the (r,μ) statements (w-integral
done numerically, NOT via the certified polynomials) vs 17/60, 149/700 (tol
1e-9 rel); G1 lake rc 0, ZERO sorry, axioms of cov_generic/chord_uncond/
I1_uncond/I2_uncond/I3_uncond ⊆ {propext, Classical.choice, Quot.sound};
G2 constants cross-check vs LR3_m05_moments.lean (parsed from file).
Classification (house rule 4): cov_generic is ENGINE-GEOMETRY algebra (the
(u,v) disk measure + forward chord); the moment VALUES are B-class joint laws
now certificate-grade. Honest scope: the ENGINE's sampling rules stay the model
leg; Lean certifies the geometry algebra only.

### MC5 — thin-window limit test of the M05-I numerator + R_v curve (owner: conductor)
Claims: (i) N_num(τ₀,q) := −ln A_v(τ₀,q)/τ₀ → 3/4 + 5q/12 as τ₀→0 (A_v by J11's
exact quadrature A_vol_quadrature, loaded not transcribed; numerator moments now
certified by LR4c — this lane is the engine-side limit CONSISTENCY check);
(ii) c₀(τ₀,q) := E[D]_vol/τ₀ → MC4's banked line a+bq (loaded from
MC4_results.json verdict string); (iii) R_meas(0,q) := lim A_num/c₀ vs candidate
(3/4+5q/12)/(a+bq).
Budget (fixed before any run): q ∈ {0,1,3,6,10}; τ₀ ∈ {1e-2, 3e-3, 1e-3, 3e-4};
A_v quadrature ng=80 (exact, no MC noise); E[D]_vol via J02 simulate volume,
n=2e6 × 4 reps/point, seeds 4101.., single pass.
KILLS (pre-registered):
- P0 parity: fresh A_vol_quadrature(0.5, 0) vs J11 stored quadrature 0.70728
  (J11_volume_atom.out "A_quad": 0.70728) |diff| ≤ 1e-4; else exit 1.
- K1: quadratic fit N_num = A + Bτ₀ + Cτ₀² on the 4 τ₀ points (per q);
  |A − (3/4+5q/12)| > 3·max(SE_A, |C|·τ_min²) + 1e-9 → numerator limit REFUTED
  at this power, exit 1. (SE_A from fit residuals; deterministic points.)
- K2: linear-in-τ₀ extrapolation of c₀ (per q, 4 points, reps give SE):
  |c₀(0) − (a+bq)| > 3·SE_extrap → thin-window denominator refuted, exit 1.
- K3: |R_meas(0,q) − (3/4+5q/12)/(a+bq)| > 3·SE_comb (any q) → candidate curve
  refuted, exit 1.
Exit 0 iff P0 ∧ ¬K1 ∧ ¬K2 ∧ ¬K3 → R_v(0,q) upgraded CANDIDATE → CONFIRMED at
this power (still consistency-family vs the certified numerator — labeled).

### LR6 — M01 recompile + stale-register disposition audit (owner: conductor)
Gates: fresh `lake env lean M01_alg_spine.lean` rc 0, zero sorry, all axioms
⊆ {propext, Classical.choice, Quot.sound}; grep confirms j10i_window_decomp and
the k04_* family present. Disposition (recorded in LR6_DISPOSITION.md, register
rows appended): row 17 (J10-I window) Lean leg CERTIFIED via M01 §4; row 19
(K04 inversion) CERTIFIED via M01 §5 (incl. the q̂>−1 boundary correction
k04_qhat_gt_neg_one and the honest refutation k04_refutes_ed_three_halves);
row 12 (atom law A = exp(−τ₀(1+q/3))) → model-input/consistency-family (K01
A-class): certifying it would restate a definition — recorded NOT lane-worthy;
row 18 (J11 volume window finite-τ₀) → stays MEASURED (quadrature+MC); its
τ₀→0 numerator is the LR4c/MC5 leg. Kill: recompile fails → exit 1 (audit
finding, honest).

## House rules 1–10 apply verbatim (LOOP_CONDUCTOR.md). Raw data untracked;
## commit set: Z8-WAVE_BRIEF.md, LR4c_m05_i23.{lean,py,out,err,json},
## MC5_thin_window.{py,out,json}, LR6_m01_recompile.{py,out,json},
## LR6_DISPOSITION.md + leftover Z7 files (LR5/MC2/MC3 0-byte .err run-history,
## Z7wave_launch.py). No other series; tmp_dbg/_g08/_g208/_j08/_s04/_v04 and
## astra_spawn_ideas remain untracked (unrelated leftovers).

## AMENDMENT 1 (2026-09-28, this tick, BEFORE any rerun; run-1 outcomes preserved verbatim in .out)
- LR4c run-1: R0-FAIL honest — the R0 evaluator carried a DOUBLED 1/2 factor
  (0.1416666668 = exactly 17/120 = half of 17/60). Evaluator bug, NOT a math
  result; the Lean file is untouched. Fixed: single 1/2 (the 1/2 int dmu lives
  in the mu-weights). Gates unchanged.
- MC5 run-1: K1 fired at ALL q with deviations 9.1e-9 .. 1.2e-7 against
  tolerances 3e-9 .. 9.4e-8 — the intercepts equal 3/4+5q/12 to 8+ significant
  digits (0.750000, 1.166667, 2.000000, 3.250000, 4.916667) and all fitted
  slopes B are NEGATIVE (approach from below, as predicted by the cumulant
  expansion -tau0*kappa2/2). The kill fired on the quadrature/roundoff noise
  floor (ng=80 + cancellation at tau_min=3e-4), which the registered tolerance
  did not budget — a GATE-DESIGN error, not a physics verdict. Per house rule 3
  the tolerance is widened ONLY by measuring the estimator's true error:
  AMENDED K1: noise floor per q = delta_ng := |N_num(tau_min; ng=80) -
  N_num(tau_min; ng=160)| (quadrature-refinement difference at tau_min);
  kill iff |A - (3/4+5q/12)| > 3*max(SE_A, 2*delta_ng, |C|*tau_min^2) + 1e-9.
  K2/K3 unchanged (MC-leg SEs are real). Run-1 K1 FIRED verdict stands on
  record as the pre-amendment outcome.
- LR4c run-2: k=2 rel 8.4e-10 PASS; k=3 rel 1.11e-9 — a hair over the registered
  1e-9 (quadrature floor of the (nr,nmu,nw)=(200,400,64) evaluator, NOT a math
  discrepancy; 17/60 and 149/700 confirmed to 9-10 digits). Budget widened per
  house rule 3 by IMPROVING THE ESTIMATOR, not the tolerance: run-3 uses
  (nr,nmu,nw)=(300,600,96) with leggauss cached; R0 tolerance stays 1e-9.
  Run-2 R0-FAIL stands on record.

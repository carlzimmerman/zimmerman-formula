# CANDIDATE_LAWS_REGISTER — living index of verified claims

**Seed: 2026-09-23 · per deepseek_push/LOOP_CONDUCTOR.md §3 · append-only.**
Columns: law | status | verification (file + exit) | kill condition | Lean | owner.

## PROVEN / VERIFIED (machine-checked, on disk, exit 0 unless noted)

| law | status | verification | kill condition | Lean | owner |
|---|---|---|---|---|---|
| Central window: −ln A/E[D] = (1+q/3)/(½+q/4) ∈ [4/3,2], τ₀-free | VERIFIED 27/27 | J09_two_component_law.py (.out, exit 0) | measured ratio outside [4/3,2] at ≥3σ | open (M01) | J/K wave |
| Generalized-p window: (1+q/(p+1))/(½+q/(p+2)) → (p+2)/(p+1) | VERIFIED 21/21 | J09p_general_p.py (.out) | deviation >5 SE at any p∈{1,2,4} | open (M01) | J/K wave |
| Atom law central: A = exp(−τ₀(1+q/3)), T-independent | VERIFIED (MC 0.36826 vs exp(−1); K03 h>0 bit-identical) | J09, K03 (81/81) | | open (M01) | J/K wave |
| E[D] = τ₀(½+q/4) (Theorem 1), volume-excluded | VERIFIED 3 motors | J02/K02 (z≤1.2) | | — | frozen lane |
| Volume face: E[τ]_vol = ∫rκ dr + E[μ_exit] − ½E[F(r₀)]; E[D]_vol = E[τ]_vol − E[Q], Q=0.59715 | VERIFIED (7e-16 bookkeeping) | J02B + K02 (z=0.35) | | — | J/K wave |
| E[D²] ≥ 3E[Dv²]²/E[v⁴] (density-free, geometry-free, T-free) | VERIFIED 86/86 (tightest of chain; slack=1/corr²) | J06_bound_sharpen.py, K03 | E[D²] below bound ≥3σ | open (M01) | J/K wave |
| Closure failure: E[Dv²] ≠ 2E[D]E[ang], R = 2.64/2.02/1.70 (5σ); R_m grows | VERIFIED | J01/J02 | | — | J/K wave |
| J10-I = (r_B/R)·window; A2744-QSO1 reads 1.818 central / 1.719 volume — CONSISTENT-OPEN | VERIFIED 6/6 | J10_verify.py | outside BOTH windows (central ∧ volume) | open (M01) | J/K wave |
| Volume window τ₀-dependent: 1.897/1.710/1.314 @ q=0/3/10 (τ₀=1); ⟨chord⟩_vol = 3/4 | VERIFIED 8/8 | J11_volume_atom.py | quadrature vs MC >4 SE | open (M01) | J/K wave |
| Inversion: τ₀̂ = −3lnÂ − 4Ê[D], q̂ = 4Ê[D]/τ₀̂ − 2; third observable E[v²] predicted, z ≤ 0.13 | VERIFIED 53/53 | K04 (5 clouds, 3 runs) | any z ≥ 5 | open (M01) | K wave |
| Deterministic hierarchy: E[D]=0.500000, E[v²]=2.80674, E[Dv²]=3.70900 | PASS (S1-S3) | K05_ray_solver.py (0.16/0.02/0.61%) | | — | K wave |
| Gradient robustness: all laws h-independent | 81/81 | K03 | | — | K wave |
| eRASS:3 catalog integrity: 1,975,540 rows = 1,911,744 PS + 63,796 EXT; 87.8% extragalactic | 13/13 | G236_eRASS3_a0z.py + .out | | — | G wave |
| G237 z-extension: u(z)=u(0)[a₀(0)/a₀(z)]^{1/2}; virial-T Case A exact | DERIVED 5/5 (verdicts PENDING WG) | G237 (sympy) | eRASS:3 WG products | | G wave |
| Lean: I21/I22 (YM polymer thresholds), I23/I24 (RAR inversion; khronometric 2/c¹⁴) | PASS, exit 0, zero sorry | fable_independent_2026/lean_2026/ | | certified | fable lanes |

## LABEL-ONLY (K01 A-class: consistency family — keep, never promote)

Gaussian hierarchy E[Dv^{2m}] = (2m−1)!!2^m E[D·ang^m]; W-spine; kurtosis mixture law (≠ "=3"); per-bin structure; central atom (definitional).

## KILLED (registered; do not reopen)

Two-moment closure (5σ); J03 central-difference grid; J04 P_N S2/S3 algebraic route (superseded by K05); NSE window a₀-loading as continuation evidence (NSA1: "some finite C" only); kurtosis "=3" headline.

## OPEN (spawn candidates)

| door | status | depends on |
|---|---|---|
| M01 Lean arithmetic spine | **LANDED 2026-09-23, 32 certified + 1 conjectured** (chordMoment 3/4: 2D change-of-variables not in mathlib; numeric evidence J11 quadrature 0.750000) | closed |
| M03 cluster evidence re-audit | **LANDED 2026-09-23: 13/13 RE-VERIFIED +1 resolved discrepancy** (LS10 65,645 vs Main 63,796 EXT = 1,849 duplicate counterpart rows, 0 flips on 1,591,243 shared); E1/E2 NOT-TESTABLE-WITH-SHIPPED (need WG T_X/M500/z + SDSS DR20) | external WG products |
| M05 first-flight moments | **LANDED 2026-09-23, 11/11**: ⟨chord⟩ = 3/4, E[∫r²ds] = 5/12, E[∫r⁴ds] = 1/4 (Legendre ladder to 3e-13); thin window R_v(0,q) = (3/4 + 5q/12)/c₀(q) matches K07 to SE; E[∫r⁶ds] = 0.212857 open (149/700 within error, uncertified) | M01 may certify |
| M05b Simpson audit | recorded: trapezoid-weak at the r=1,μ=0 corner — superseded by the Legendre ladder (in M05_geometric_anchors.out) | — |
| M04 J10-I(z) cosmography | **LANDED 2026-09-23, 14/14**: framework z-curve FLAT/OPEN z<3; M-RISE closes high z_c=0.156; single object at z=1 resolves rival at 11σ; ratio chain excludes rival 3σ from z=0.617 | closed (L05 S/N assumed 30) |
| L03 2D transfer + recovery | **CORRECTED 2026-09-23 (2nd run): PASS** — first run BROKEN-as-built (pair S/N=None); re-run rebuilt the estimator per pre-registered protocol (E[D]-pinned first moment + atom-exact assignment + tail-mass calibration): pair-recovery now attains **S/N=50 on both clouds** (bias τ₀ 0.0017, coverage 0.998/0.992, 500 reals, det_fail 0); per-row KS 0 rows at p<1e-3; marginal D-CDF KS p=0.000 printed as the registered informative-not-gated check; deterministic κ(r)=t₀(1+qr²) machinery + q=2 cloud exact (E[D]=1.0) | closed at S/N≥50 |
| L01–L07 (wave-4 remainder) | IN FLIGHT | — |
| K07 volume window closure | **LANDED 2026-09-23, 34/34 + 10-run boundary supplement**: volume atom quadrature (corrected chord √−rμ) matches MC 18/18 within 4 SE (max z=2.53); R_v(τ₀) strictly decreasing all q; **kill-region boundary τ*(q) = 6.505±0.002 / 2.415±0.002 / 0.978±0.002** (q=0/3/10) — above it the volume window sits below 4/3; R>2 EMPTY everywhere (max 1.927±0.010); J11 'thin ~2.2 > 2' speculation REFUTED (thin ≈1.86); J11 anchor (τ₀=1,q=10) R=1.3221±0.0028 below 4/3 RE-VERIFIED; a/τ₀+b fit formally REJECTED (χ² huge) | closed; feeds L04 |
| K08 shell geometry | **LANDED 2026-09-23, 26/26**: shell window is τ₀-DEPENDENT like volume (not flat like central); exact shell atom A_s = ½∫dμ·e^{−τ_esc(μ)} verified 16/16 (max z=2.38); dependence grows with a (χ² 0.55→464); only a=0 is flat; shell(a=0.3) q=3 window 1.657 vs central 1.600 | closed; observers need the shell window not [4/3,2] |
| K09 J10-II geometry-aware | **LANDED 2026-09-23, 19/19**: at A2744 corner (τ₀=1,q=0) reading stays inside EVERY geometry's window — **radius assignment robust under geometry ignorance (CONSISTENT-OPEN preserved under all three)**; strict ∀(τ₀,q) clause fails for every geometry — single cause: R_meas/r_B = 1.10 offset compresses reading below floor; reading in window ∀(τ₀,q) ⟺ R ≤ r_B (scale=1 check passes); error budget: se(A)/A = se(d)/d ≤ 1.0% (q=0 binding)…4.2% (q=10); width-ratio U = std(D)/E[D] separates central 1.437 vs volume 1.893 radius-free | closed |
| K10 oblateness | **LANDED 2026-09-23, 23/23**: window is ε-DEPENDENT — central INFLATES above 2 with flattening (2.00→2.25→2.54→3.05 at ε=1.0→0.3); measured ratio >2 reads oblateness not anti-Thomson; correction corr(ε)=ε^−0.347 (central), ε^−0.376 (volume); volume τ₀-dependence survives ε≥0.5, suppressed at 0.3; central τ₀-flatness breaks at 0.3 | closed; un-flatten before comparing |
| K11 synthesis | **LANDED 2026-09-23**: whole J/K series = ONE door — RM reads (A,d̄,width); (A,d̄)→(τ₀,q) closed-form; window [4/3,2] tests a₀-radius J10-I=(r_B/R)·window; discrimination tree central-FLAT/volume-CROSSING/shell-weak; 5 consolidated falsifiers T1–T5; differential 2-epoch τ₀-curvature cancels r_B and reaches +3.4σ (2:1) / +6.4σ (3:1) at JWST photometric grade | closed (K07-10 numbers folded into register rows; K11 written before those landed, pending flags superseded here) |
| K12 geometry-ignorance audit | **LANDED 2026-09-23, 29/33**: J05 bound GEOMETRY-FREE (slack ≥1.09 volume), J07 envelope GEOMETRY-FREE (margin ≥+0.005); frozen Thm-2 lag-width band NEEDS central label — lower endpoint BROKEN under volume even with J02B-corrected E[D]_vol (14.9/39.3/111 SE); upper endpoint survives; Thm-1 central-only (J02B) | Thm-2 lower endpoint withdrawn under unknown geometry |

| c₀(q) closed form (thin-limit denominator) | OPEN — M05 gives thin limit (3/4+5q/12)/c₀(q) = 1.893/1.837/1.843 vs K07 'universal ≈1.86': q-dependence vs universality unresolved at ~2.5 SE; c₀ linearity (a+bq) is the decisive test | M05 numerics + thin MC |

| G237 verdicts vs eRASS:3 WG products | PENDING | WG data (external) |
| JWST observation design (L05/K09) | IN FLIGHT | — |

_Append-only. New waves append rows; nobody rewrites history._
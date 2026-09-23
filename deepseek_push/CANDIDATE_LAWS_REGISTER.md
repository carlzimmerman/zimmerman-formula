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
| M04 J10-I(z) cosmography | **LANDED 2026-09-23, 14/14**: framework z-curve FLAT/OPEN z<3; M-RISE closes high z_c=0.156; single object at z=1 resolves rival at 11σ; ratio chain excludes rival 3σ from z=0.617 | closed (L05 S/N assumed 30) |
| L03 2D transfer + recovery | **LANDED 2026-09-23: BROKEN as built** (marginal D-KS p=0.000; pair-recovery S/N=None) — deterministic κ(r)=t₀(1+qr²) machinery + q=2 cloud solved exactly (E[D]=1.0); OPEN-AS-REFORMULATED (D-marginal reconstruction) | next attempt |
| L01–L07 (wave-4 remainder) | IN FLIGHT | — |
| K07–K12 (wave-3 remainder) | IN FLIGHT (K07: volume quadrature deep-τ₀ confirmed z≤1.25; window decreasing all q; thin limits 1.84–1.89) | — |
| G237 verdicts vs eRASS:3 WG products | PENDING | WG data (external) |
| JWST observation design (L05/K09) | IN FLIGHT | — |

_Append-only. New waves append rows; nobody rewrites history._
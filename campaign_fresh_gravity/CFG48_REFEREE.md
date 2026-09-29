# Referee note on CFG48 (Gap 1: the switch as a legal action term) — commit 0dba13349

An independent referee pass, done at the orchestrating session's request. **No CFG48 file was edited.** The referee's own code is:
- `CFG48_referee_rederive.py` / `.out` — constants typed in; nothing imported from CFG48, CFG44, CFG4 or DE12.
- `CFG48_referee_g6.py` / `.out` — the referee's own grid and eigensolver, applied to G6's physical inputs.

## Verdict

**CFG48's numbers reproduce, and its four obstructions and its stability result stand.** There are two corrections:
- **Documentation:** G1's exit code is 0, not 1.
- **Substantive:** the r_ta convention. It makes the no-go numbers conservative (they get *stronger* under the committed convention), but it undercuts the maximal-ball gate's claim to place the edge where B puts it.

## 1. Re-runs from a clean export

`git archive 0dba13349` of `campaign_fresh_gravity/CFG48_gap1_switch`, `CFG44_fluid_target`, `real_research/dark_energy_2026` and `real_research/g03_audit_2026`, extracted to a scratch directory (layout preserved). All six scripts were run in both modes.

- **All 12 outputs are identical to the committed `.out` files**, apart from the timing field.
- **Exit codes:** G2–G5 main runs exit 0. G6's main run exits 1, from its four pre-declared H failures, which are disclosed. Every MUTATE run exits 1.
- **G1's main run exits 0, not 1.** The README says G1 "exits 1 although all 7 of its checks pass, because the script's exit code counts its recorded gate verdicts that FAIL (`R.write()` returns that count)". The committed `Gcommon.Report.write()` returns the number of failed *load-bearing checks*, not gate verdicts. G1 has none, and its own committed output prints "load-bearing failures: 0". This is a documentation error with no physics consequence.

## 2. The frozen gate file predates the scripts

APFS birth times:

| File | Created |
|---|---|
| `GATES_FROZEN.md` | 21:08:16 (mtime identical) |
| `Gcommon.py` | 21:12:04 |
| `G1` | 21:13:44 |
| `G2` | 21:17:41 |
| `G3` | 21:18:35 |
| `G4` | 21:20:52 |
| `G5` | 21:22:47 |
| `G6` | 21:24:22 (edited to 21:28:37; the disclosed ball-formula fix) |

All were committed together in 0dba13349, so git cannot order them. The birth times are consistent with "written before any script".

The frozen thresholds are the ones applied: GE within 10% of M_law, GH(b) ≤ 0.10 g_law at every x in [0.3, 30], L3 ≤ 0.25, and L4 ≥ 1e2 for M_b ≥ 1e10.

## 3. Headline numbers re-derived with the referee's own code — 7/7 reproduced

| # | quantity | referee | CFG48 |
|---|---|---|---|
| R1 | top-hat Δ_ta(z = 0), flat ΛCDM, Ω_m = 0.3153 (own integration) | 11.76 | 11.81 (0.4%) |
| R2 | flux-gated negative shell M_b(√(1+x_e²) − 1) at M_b = 1e10, 1e11, 1e12 (CFG48's r_ta convention) | 3.21e11, 2.157e12, 1.439e13 Msun | G1 prints 3.21e11, 2.15e12, 1.44e13 (the README rounds the last to 1.4e13) |
| R3 | Gauss lemma, numerically: smooth erfc gate, point mass, flux-gated QUMOND and AQUAL (AQUAL solved by root-finding) | M_dyn = M_b beyond the edge to 1.2e-11 | L1 HOLDS |
| R4 | exchange reaction, **derived analytically** from CFG44's point-mass identities as F = 4π s² ∂ε/∂M_enc | P-slaved (3/4) a₀; σ-slaved (3/8) a₀ (2+x²)/(1+x²); a/g_law = 0.062, 0.398, 11.26 (σ) and 0.53, 22.49 (P) at x = 0.3, 1, 30 | the same closed forms and ratios |
| R5 | energy the exchange must supply, 1.5 x_e | 49.6, 33.8, 23.0 | 49.6, 33.8, 23.0 |
| R6 | mediator requirement x_e²/2 at M_b = 1e10, 1e12, 1e13, 1e14 | 547, 118, 55, 25 | 546, 118, 55, 25 |

R4 is the strongest confirmation. The reaction is not only reproduced numerically; its closed form follows in a few lines from CFG44's identities (P = a₀M/8πr², ρ_c = a₀/(4πG r √(1+x²)), σ² = V_c²/2, internal energy (3/2)P).

## 4. G6's stability counts (the "expectation overturned") — reproduced with the referee's own numerics

The physical inputs (DE12's 24 layers, B, W″, U₀/M₀ and the reading A) come from G6's own `layer_arrays()`, executed read-only. Independent of G6 are:
- the grid: uniform in ln r, 4,000 points, with p and V interpolated;
- the linear algebra: scipy's sparse generalized eigensolver for η_crit = 1/μ_max of V m = μ K m. G6 uses LDLᵀ pivot counting and bisection on its own nonuniform grid.

Results:

| Check | Referee | CFG48 |
|---|---|---|
| Negative modes, baryon-mass reading | 0/48 | 0/48 |
| Negative modes, dynamical-mass reading | 29/48 | 29/48 |
| Verdict agreement, case by case | 96/96 | — |
| η_crit agreement | median 2.6e-5, max 2.2e-4 | — |
| Minimum η_crit, baryon-mass reading | 13.67 | 13.67 |

Internal consistency of CFG48's own JSON: a case has a negative mode exactly when its full-layer η_crit < 1, on 96/96. That is what Dirichlet domain monotonicity requires.

The ball gate's rank-one reduction, E2 = ½ δM² [c_s²/M_gas + E_R L2 + E_RR L1²], is exact: the Cauchy–Schwarz minimiser at fixed δM is δρ ∝ ρ (isothermal). Its Ξ values were not recomputed.

Not re-derived: the local-gate count (44/48), which reproduces DE12's committed arrays (its own C1), and DE12's physics.

## 5. The substantive finding: the r_ta convention

CFG48's `Gcommon` computes r_ta from the cosmic-share collapse mass M_b(1 + Ω_c/Ω_b) and labels this "CFG4's convention". **The committed convention is different.** `CFG4_target.r_turnaround` (as documented in CFG11's `rta_of`, and reused in CFG12) and `CFG4_switch.r_bound` (the KiDS edges) take r_ta where **the law's own enclosed mass, phantom included**, falls to Δ_ta ρ̄_m. That r_ta is larger because the phantom grows with radius.

Referee's R7 (P2, z = 0):

| M_b | r_ta (CFG48 → committed, kpc) | x_e | energy ratio | α_req |
|---|---|---|---|---|
| 1e10 | 319 → 1151 | 33 → 119 | 50 → 179 | 547 → 7115 |
| 1e11 | 688 → 2047 | 23 → 67 | 34 → 101 | 254 → 2250 |
| 1e12 | 1482 → 3639 | 15 → 38 | 23 → 57 | 118 → 712 |
| 1e13 | 3192 → 6472 | 10.5 → 21 | 16 → 32 | 55 → 225 |
| 1e14 | 6877 → 11512 | 7.1 → 12 | 11 → 18 | 25 → 71 |

Consequences:
- **(a) The no-go numbers are conservative.** Under the committed convention, the Gauss negative shells (6–118 M_b), the exchange's energy demand (18–179× the baryons' orbital kinetic energy) and the mediator requirement all grow. L4's frozen line (α_req ≥ 1e2) then fails only at 1e14, not from 1e13. No conclusion reverses.
- **(b) The maximal-ball gate's edge coincides with B's edge only in CFG48's convention.** G2 derives "top-level ball boundary = 0.4 r_ta exactly when all baryons are retained (Δ_edge = Δ_ta/x_e³)". Measured against B's committed r_ta, the same baryon-only ball edge sits at 0.4 × r_ta,col/r_ta,law = **0.11, 0.13, 0.16, 0.20, 0.24 r_ta** for M_b = 1e10–1e14. That is below B's declared window [0.31, 0.48], and in the range where FG016's splashback edge (0.175–0.271) fails KiDS.
  - Placing the ball edge at B's committed edge would need the phantom-inclusive mass, which is a carrier reading that MS1 forbids, or a re-declared threshold.
  - So the ball gate's GE entry ("PARTIAL: edge = r_e") and its "no new constant" edge placement are weaker than the README states.
  - The ball gate's second-variation stability (G6) is unaffected; it uses DE12's layers, not r_ta.

## 6. Hypotheses against what was tested

- **Gauss (G1).** Tested for a prescribed W(r) (sympy, general W and kernel) in the flux-gated QUMOND and AQUAL forms. The README extends it to "gate reading only baryon-slaved fields". That extension is argued, not scripted. In the referee's reading it holds by the divergence structure, provided W and its derivatives vanish beyond the edge. The source-switched form escaping Gauss but failing Helmholtz is as stated.
- **Exchange (G4).** Point-mass, isotropic, σ- or P-slaved, as stated. The referee's R4 derivation uses exactly these hypotheses.
- **Stability (G6).** A second-variation statement on DE12's frozen backgrounds. The first variation (the ball gate's edge potential step of 0.2–8 c_s²) is not fed back, which is disclosed. H_V2 and H_R2 were declared after round 1, also disclosed.
- **History (G3).** A one-degree-of-freedom structural toy, as stated.
- **Minor.** The README says "nothing was committed". That is stale: the lane is committed in 0dba13349, with a LEDGER row appended outside the directory.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.

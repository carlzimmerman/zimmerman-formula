# Referee note on CFG49 (Gap 1: a dynamical gate scalar χ) — commit b899e204e

An independent referee pass, done at the orchestrating session's request by the same method as CFG48's (35eebbe99). **No CFG49 file was edited.** The referee's own code is `CFG49_referee_mu.py` / `.out`.

## Verdict

**CFG49 reproduces, and its derived stability structure and headline numbers check out independently.** There is one process finding: CFG49 has **no separate frozen-criteria file**, and its declarations cannot be shown to precede its scoring. There is also one rerun anomaly, which did not reproduce.

## 1. Re-runs from a clean export

`git archive b899e204e` of `campaign_fresh_gravity/CFG49_gate_scalar`, `real_research/dark_energy_2026` and `real_research/g03_audit_2026`, extracted to a scratch directory with the layout preserved.
- `dark_energy_2026` supplies DE12, DE13 and DE13's committed results JSON.
- `g03_audit_2026` supplies L352, which DE12 executes.

All ten runs were made with CFG49's own `run_all.sh`.

- **Nine of ten outputs are identical to the committed ones**, including the `rc=` lines the run script appends (the timing field was stripped before comparing).
- **CV6_B's main run reproduces standalone.** The first attempt, inside `run_all.sh` while a separate heavy referee job ran on the same machine, stopped at the start of H2 (the multiprocessing section) with no traceback and no `rc=` line. `run_all.sh` still wrote `run_all.done`. A standalone rerun matched the committed output line for line, apart from the timing field, with rc = 1.
  - Not reproducible, so not attributed to CFG49.
  - Note, though, that `run_all.sh` marks itself done without checking that each run finished.
- **Exit codes, exactly:**

  | Script | Main | MUTATE |
  |---|---|---|
  | CV6_A | 0 | a: 1, b: 1 |
  | CV6_B | 1 (H2, declared and refuted, kept) | a: 1, b: 1 |
  | CV6_C | 0 | k: 1 |
  | CV6_D | 0 | x30: 1 |

  All six MUTATE runs exit 1. The README's "A 12/12, C 5/6 (0 load-bearing failures), D pass; B 7/8" is consistent with these codes.

## 2. Frozen criteria

**There is no separate frozen-gates or frozen-criteria file in CFG49.**
- The hypotheses are pre-declared inside each script's docstring. CV6_B's docstring says they were "written before the final run", after disclosed exploratory scans: μ_min(m₂) with χ₀ = t, the χ₀ solver, and the flagship potential.
- All four scripts and `cv6_common.py` share one APFS creation time, 21:29:00, a bulk copy into this checkout. Everything was committed at once in b899e204e.
- So neither file times nor git can show that the declarations preceded any scoring. **The referee cannot verify "frozen before the scripts" for CFG49.** The in-script declarations are what exists.
- This is below CFG48's standard. CFG48 had a separate `GATES_FROZEN.md`, created before its first script.

## 3. Independent re-derivation

**The stability structure, derived by the referee by hand.**
- Eliminating the gas displacement (a Schur complement) gives E2 = ½∫r²[μχ′² + (g_eff − BW″)χ²], with g_eff = a·m₂/(a + m₂) and a = c_s²/(ρh²). This is exactly CFG49's reduced form (`cv6_common.reduced_diag`).
- From it, three results follow:
  - (i) μ = 0 with m₂ → ∞ gives Γ = k√(c_gate² − c_s²), where c_gate² = ρh²BW″, which is DE12's form.
  - (ii) At k → 0 the determinant condition fails for every m₂ when c_gate ≥ c_s. This is CFG49's theorem S2: χ's mass alone repairs nothing.
  - (iii) The gradient term closes the unstable band only above k_c.
- So the headline follows: a stable χ needs a gradient stiffness μ, which is a new length, and a mass m₂.

**Numerically (`CFG49_referee_mu.py`).**
- **Method:** the m₂ → ∞ minimal gradient stiffness per layer on DE12's layer arrays (loaded read-only through CFG49's `cv6_common`), with DE13's five half-layer Dirichlet windows. The grid (uniform in ln r, 3,000 points per window) and the dense generalized eigensolver are the referee's own.
- **Compared** against DE13's committed form-(i) values (`DE13_gate_gradient_repair_results.json`, F1 rows `mu_U`), not against CFG49's code.
- **Ratio 0.2500 on all 32 DE13 layers** (the eight cluster layers included). This is exactly the change of variable from DE13's U to CFG49's t: t = t_U(U − 1) + ½ with t_U = 1/(2w) = 2, so μ_t = μ_U / t_U².
- **The galaxy-layer maximum is 3.86 × 10²⁸ J/m** in t units. That is the upper end of CFG49's quoted range, "μ ≥ 1.5–3.9 × 10²⁸ J/m": 1.474 × 10²⁸ at the smallest tracking m₂ = 10⁻¹² Pa, and 3.9 × 10²⁸ at m₂ = ∞.
- ℓ = √(1.474 × 10²⁸ J/m / 10⁻¹² Pa) = 3.93 kpc, against CFG49's 3.9 kpc.

**Not re-derived:**
- the finite-m₂ stiffnesses, which need the nonlinear χ₀ background;
- the potential costs (Φ_χ(r_F) = −13.5 v_f², Φ_χ at the Sun = 7.7 × 10⁷ v_f²);
- CV6_C's switched-stiffness counts;
- CV6_D.

## 4. Hypotheses against what was tested

- **The scoped no-go.** "A local scalar with constant kinetic stiffness and a baryon-trace source cannot be stable without new tuned scales" is what CV6_A (local linear analysis, sympy) and CV6_B (24 galaxy layers) test. CV6_C tests the switched-stiffness repair μ(χ), which fails on its own switch-off term, as stated. The README states the scope limits (frozen spherical background, no gas self-gravity, T3 estimated only in CV6_D), and they match the scripts.
- **"Two new untied constants."** The μ range is set by μ_uni at the tracking bound and at m₂ = ∞; the referee confirms the upper end independently. The m₂ ≥ 10⁻¹² Pa bound comes from the declared tracking criterion (the edge within 10% on 24 of 24 layers).
- **H2 failed as declared.** "Finite m₂ does not lower the needed stiffness" was declared, refuted by the run, and kept, with the per-layer ratios printed.
- **Relation to CFG48.** CFG49's χ is a local, baryon-sourced gate, the class CFG48's G6 found unstable in its local control (44/48). The two lanes are complementary, as CFG49's README says. The referee's CFG48 note independently reproduced G6's counts.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.

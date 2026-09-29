# CFG101 referee note: its two corrections to CFG50, re-derived analytically with independent code

- **Scope.** The orchestrator asked for one headline per lane, re-derived with the referee's own code. For CFG101 that headline is its correction to CFG50. Script: `CFG101_referee_ceiling.py`; log: `.out`. It imports nothing from CFG44, CFG50 or CFG101.
- **Method.** CFG50's definitions (README; D2 docstring) reduce exactly to functions of x = r/h alone, with no fluid mass and no a₀:
  - P_rr = a₀ g_N/(8πG), because u cancels;
  - |χ_c a_f|/g_tot = (r/4)|T_rr′ + 2(1 − β)T_⊥′|/λ_max;
  - λ_max = GM/(3h³), reached as r → 0.
- **So the ceiling and the sign-flip radius are mass- and a₀-independent by construction.** CFG50 and CFG101 state both properties.

| quantity | CFG50 | CFG101 | this re-derivation |
|---|---|---|---|
| ghost-free ceiling, max \|a_f\|/g_tot | 0.505 | 0.5008 at 0.85 h | **0.50077 at 0.8523 h** |
| at 0.3 h, 1 h, 3 h | 0.34, —, 0.14 | 0.337, 0.494, 0.143 | 0.3367, 0.4940, 0.1430 |
| the same with λ_max read from a grid starting at 0.01 h | (D2's grid) | 0.5045 | 0.50453 (λ_max 0.747% low) |
| reaction opposed to the fluid force inside | r < 1.7 h | r < 1.78 h | **r < 1.7795 h** (the zero of a_react; one sign change on 0.05–6 h) |

**Verdict: both corrections reproduce.**
- The ceiling is 0.5008 g_tot. CFG50's 0.505 is the 0.75% grid artefact that CFG101 identified.
- The flip is at 1.78 h, not 1.7 h.
- The note already appended to CFG50's README (CFG101's correction) stands as written.

**Limits.** The a_react formula and its outward sign convention are taken from CFG50's README. CFG101 verified the formula with sympy. This note checks the numbers, not the derivation.

κ = ½ stays fitted. Nothing here says the theory is closed.

# Orchestrator review of DeepSeek T11–T13 (openai_math_cross_analysis_2026-10). Not new puzzle pieces
Script `audit_t12_t13.py` (read-only on deepseek_push); output in `audit_t12_t13.out`.

## T11 / T12 (assembly clock; "three-clock λ confirmed"): CIRCULAR, and broken on consistent targets
- **Circular.** T12's epochs (t_c = 6.7 Gyr, t_g = 11.9 Gyr) come from T11, which derived its epoch ratio from the same group/cluster levels (0.60 / 0.43). Fitting a single λ to both levels with epochs built from those levels is close to a tautology.
- **The levels are inconsistent.** Groups 0.60 is definition B with weak-lensing bias b₁ = 0.4; clusters 0.43 is definition A with b = 0 (CFG382 target audit, f982f4a34).
- **On ONE definition:**
  - at b = 0, λ_groups = 0.062 against λ_clusters = 0.026, a factor 2.4 apart;
  - at b ≥ 0.1 the group level exceeds 1, so the settling law f = 1 − e^{−Γt} cannot represent it at all.
- **The agreement with CFG382's 0.028 is not a confirmation.**

## T13 (phantom sound-speed theorem): CORRECT, but a known reformulation; the prediction covers the phantom only
- **The algebra checks** (sympy): for ρ_ph = v²/(4πG r²), hydrostatic equilibrium gives c² = v²/2, and λ_J = √2·π·r ≈ 4.44 r. This is the singular isothermal sphere. The record's 10-06 synthesis already noted it: the deep-MOND phantom is an SIS with σ² = V²/2, and settling reduces to the BTFR amplitude.
- **c_ph = (G M_b a₀)^{1/4}/√2 is the BTFR restated.**
- **The "no pure-dark subhalos" prediction holds for the PHANTOM**, which is a function of the baryons, as in any MOND reading.
  - The record's cold fluid is a separate real component.
  - CFG344's UFD fix requires it to clump like CDM on small scales.
  - So the framework as a whole does NOT predict "no dark subhalos". A dark-subhalo detection would not falsify it unless the cold fluid's small-scale power is also excluded.

**Net:** neither adds a new piece. T10 (heat-equation settling and the exact supply edge) and T9 (exact phantom mass) remain DeepSeek's useful contributions.

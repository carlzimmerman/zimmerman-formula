# ZIMMERMAN EQUILIBRIUM THEORY — key lanes index

The full glm53 track has 40+ lanes in `glm53_push/`. `deepseek_push/lanes/`
carries the four that run the theory's core arithmetic:

| Lane | File | Verdict |
|---|---|---|
| **G031** — the GR fluid action and the hydrostatic identification | `lanes/G031_gr_fluid_action.py/.out` | 9/9 — σ²=GM_b/2r_M ⟹ ρ_ph ⟹ BTFR ⟹ g²=a₀g_N, coefficient 1; σ_MW=119/125 km/s |
| **G032** — Horn A, the PPN-clean fixed-congruence completion | `lanes/G032_horn_a_fixed_congruence.py/.out` | α₁=0 exactly, 9/9 cells; γ→1, α₃→0; no c₁₄, no K_B, no lock |
| **G036** — the radial scatter function (the new observable) | `lanes/G036_radial_scatter_function.py` | rms 0.31→0.10 inward→out; within-galaxy 0.045 dex; NO halo-shape fingerprint |
| **G040** — the per-galaxy RAR offset decomposition | `lanes/G040_offset_decomposition.py/.out` | the offset is M/L nuisance, not physics (R²=0.016/0.006) |
| **G052** — the unified cosmology | `lanes/G052_unified_cosmology.py/.out` | **5/6** — Ω_Λ=0.6857 from a₀ alone (+0.07% of Planck); Ω_dm=0.2650 flatness residual |
| **G070** — the dSph compendium (the empirical pillar) | `G070_dsph_compendium.py/.out` | **V1 PASS** (median \|log₁₀\|=0.222≤0.30, n=34, zero parameters); **V2 FAIL** (slope +0.159±0.021>0.10 — the honest mass-dependence: UFD regime sits 2× above the line, bright dSphs ON it); V3: 12 violators, all UFDs, one-sided; S1: the 3D reading would fail V1 (+0.24 dex) — the law is LOS |

## Representative verdicts (verbatim from the .out files)

**G031 (the breakthrough chain):**
```
V1 the scaling closes: a0 = (c/2)sqrt(G rho_Lambda) — the cosmological term, the
   scalar normalisation and a0 are one equation ... PASS  (rho_Lambda not an
   independent input; the dark-energy density and the MOND scale are one number)
V2 the isothermal equilibrium density is exactly the deep-MOND phantom,
   coefficient 1 ... PASS
V6 the BTFR follows: v_c^2 = sqrt(G M_b a0) ... PASS
```

**G032 (Horn A):**
```
VERDICT (pre-registered): alpha_1 = 0 EXACTLY at every (CA, JY) with CA > 0 free --
the fixed congruence carries NO preferred-frame drag: no c_14 (no spin-1 ghost),
no K_B (no GW170817 constraint), the alpha_1 lock does not exist. gamma -> 1 and
alpha_3 -> 0: the conservative sector is untouched. HORN A OPENS.
```

**G052 (the unified cosmology):**
```
[PASS] Vc Omega_Lambda matches Planck within 1%   (+0.0007 dex)
[PASS] V2 w(X=0) = -1 exactly (the scalar IS the dark energy)
[PASS] V3 w(X>>1) -> +1 (stiff — the scalar alone is NOT cold dust)
[PASS] V4 flatness residual matches Planck Omega_dm   (0.2650 vs 0.2647)
[PASS] V5 coincidence epoch is the mu2 shape   (z=0.49 vs observed ~0.7)
[FAIL] Va alt footing (0.9953) — the honest systematic envelope
5/6 checks passed
```

## How to re-run

```bash
cd glm53_push && python3 G031_gr_fluid_action.py        # the fluid action
cd glm53_push && SCRATCH=/tmp/g052 python3 G052_unified_cosmology.py
lake env lean deepseek_push/lean/EQUILIBRIUM_THEORY.lean # the Lean spine (60s)
```
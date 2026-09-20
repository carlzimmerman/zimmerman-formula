# Autoresearch orchestrator -- results digest (2026-09-19)

**Source:** local overnight autoresearch loop (`ai_slop/research_orchestrator/`, uncommitted). Qwen3.8-27B
(MLX) proposes/codes, DeepSeek (OpenRouter) manages+vets ideas and pushes findings through doors,
empirical scoring + novelty filter vs a 1524-phrase repo corpus, Lean on survivors.

> **STATUS: RAW, UNVERIFIED AUTORESEARCH OUTPUT.** A high score means "a well-formed falsifiable test that
> passed its own checks + a working MUTATE control" -- it is a **LEAD, not a verified result**, and (per
> lane V01) local-model significances are typically inflated. Nothing here is promoted to the framework
> until re-run and error-barred by hand. No breakthrough. Included for the record + reproducibility.

## Run stats
- ideas generated: **289**, best adjusted score 0.9, mean novelty 0.67
- DeepSeek manager: 276 approved / 107 rejected as rediscoveries
- reliability: 0 Ollama 500s, 0 auto-restarts
- door chains: 4 opened, 1 falsified, 0 survived-all

## Findings that triggered door-chains (score >= 0.80) and their honest outcomes
- **adj 0.9** (raw 1.0, nov 0.88) -- The intrinsic scatter in the SPARC RAR residuals (log g_obs - log g_bar_model) correlates with the gas fraction (M_HI / M_baryonic) of galaxies, indicating a breakdown of RAR universality dependent on gas richness.
- **adj 0.83** (raw 1.0, nov 0.78) -- The RAR's intrinsic scatter varies systematically with galaxy redshift, indicating a hidden dependence on cosmological evolution or survey selection effects.
- **adj 0.86** (raw 1.0, nov 0.83) -- The RAR's intrinsic scatter *decreases* with increasing baryonic surface density (Σ_b) at fixed g_bar, reflecting a tighter dynamical coupling in denser baryonic environments.
- **adj 0.87** (raw 1.0, nov 0.84) -- The Zimmerman formula's \( a_0 \) exhibits a step-function discontinuity at the cosmic web bifurcation scale (\(\sim\)1 Mpc), where galactic filaments intersect, creating a distinct acceleration scale for filamentary environments compared to voids and clusters.

### Door outcomes (verbatim from the log)
```
*** DOOR CHAIN opened on finding (score 0.90): The intrinsic scatter in the SPARC RAR residuals (log g_obs - log g_bar_model) correlates
door 1 inconclusive (0.00); chain ends
*** DOOR CHAIN opened on finding (score 0.83): The RAR's intrinsic scatter varies systematically with galaxy redshift, indicating a hidde
*** finding FALSIFIED at door 1 (honest -- recorded, not discarded)
*** DOOR CHAIN opened on finding (score 0.86): The RAR's intrinsic scatter *decreases* with increasing baryonic surface density (Σ_b) at
door 1 inconclusive (0.00); chain ends
*** DOOR CHAIN opened on finding (score 0.87): The Zimmerman formula's \( a_0 \) exhibits a step-function discontinuity at the cosmic web
door 1 inconclusive (0.00); chain ends
```

## Top scorers (leads to triage, NOT verified)
- adj 0.9 (raw 1.0, nov 0.88): The intrinsic scatter in the SPARC RAR residuals (log g_obs - log g_bar_model) correlates with the gas fraction (M_HI / M_baryonic
- adj 0.87 (raw 1.0, nov 0.84): The Zimmerman formula's \( a_0 \) exhibits a step-function discontinuity at the cosmic web bifurcation scale (\(\sim\)1 Mpc), wher
- adj 0.86 (raw 1.0, nov 0.83): The RAR's intrinsic scatter *decreases* with increasing baryonic surface density (Σ_b) at fixed g_bar, reflecting a tighter dynami
- adj 0.83 (raw 1.0, nov 0.78): The RAR's intrinsic scatter varies systematically with galaxy redshift, indicating a hidden dependence on cosmological evolution o
- adj 0.79 (raw 1.0, nov 0.73): The Zimmerman formula’s \( \kappa = 1/2 \) fails in galaxy clusters with high central temperature (\( T > 10 \) keV), where the ac
- adj 0.79 (raw 1.0, nov 0.73): The Zimmerman formula's \(a_0\) is invariant under baryonic mass fraction (\(f_b\)) variations in galaxy clusters, meaning \(a_0\)
- adj 0.77 (raw 1.0, nov 0.71): The Zimmerman formula’s kappa correlates with the dimensionless ratio of cluster-to-galaxy baryon density contrast (rho_cluster/rh
- adj 0.76 (raw 1.0, nov 0.7): The Zimmerman formula's \(a_0\) exhibits a systematic dependence on galaxy cluster temperature, scaling linearly with \(T^{1/2}\),
- adj 0.76 (raw 1.0, nov 0.7): The Zimmerman formula's acceleration scale \( a_0 \) exhibits a redshift-dependent transition at \( z = 0.5 \) due to the cosmolog
- adj 0.76 (raw 1.0, nov 0.69): The Zimmerman formula's \(a_0\) exhibits a step-function discontinuity at the cosmic web bifurcation density (\(\rho_{\text{web}}\
- adj 0.74 (raw 1.0, nov 0.68): The bounded-boost ceiling g_obs - g_bar <= a0/e is violated at small radii (R < 0.1 kpc) in SPARC galaxies with high central surfa
- adj 0.74 (raw 1.0, nov 0.68): The Zimmerman formula implies that RAR residuals (log(g_obs) - log(g_bar)) in SPARC galaxies should exhibit a distinct, non-monoto

## The one clean result so far
A proposed correlation of RAR intrinsic scatter with redshift (raw 0.83) was **FALSIFIED at door 1** -- the
apparent redshift dependence is a selection/systematic artifact. That is a genuine (negative) result: the
door methodology correctly killed a spurious finding. The other findings came back inconclusive (the deeper
door tests fizzled on the 27B's coding); a door-retry was added afterward to reduce that.

## How to reproduce / continue
See `ai_slop/research_orchestrator/` (README, config.py). Triage: re-run any lead by hand, add intrinsic
scatter / correlated errors, convert Delta-chi^2 to a fitted-parameter statement (V01 lesson) before trusting.

# a₀(z) from the real DESI chains — the §5 revision (Carl Ward #1 + #2)

**Date:** 2026-06-27. **Script:** `reviews/a0z_desi_chains_propagation.py` (exit 0, reproducible — documents the exact public DESI chain URLs and auto-downloads). **Footing:** a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)); only (w₀, wₐ) enter the ratio.

## What changed
Replaced the **hardcoded w₀/wₐ central values + an *estimated* correlation** with the **full public DESI w₀wₐCDM MCMC posterior** (DESI-BAO + Planck2018 + SN), propagated sample-by-sample. The real correlation is **corr(w₀,wₐ) ≈ −0.90 to −0.92** — now measured, not assumed.

> **Data caveat (honest):** these are the **DR1 (2024)** public chains. The **DR2 (2025)** chains are behind DESI collaboration auth as of this run. DR1's w₀wₐ preference is slightly weaker than DR2's, so the significances below are a **conservative floor**; swapping in DR2 (identical code, identical columns: w=col 8, wa=col 9) only strengthens them.

## Results (real posterior, 90k–100k samples/combo)

| combo | w₀ | wₐ | corr | a₀(z=0.4)/a₀(0) | a₀(z=3)/a₀(0) | decline σ |
|---|---|---|---|---|---|---|
| DESI+CMB+DESY5 | −0.726±0.070 | −1.06±0.32 | −0.92 | **1.059** | 0.648 [0.534, 0.772] | 2.8–2.9σ |
| DESI+CMB+Union3 | −0.642±0.104 | −1.31±0.41 | −0.92 | **1.084** | 0.613 [0.491, 0.746] | 2.8–3.0σ |
| DESI+CMB+Pantheon+ | −0.828±0.064 | −0.74±0.29 | −0.89 | **1.031** | 0.710 [0.594, 0.833] | 2.3–2.4σ |

## The two review points, settled by computation

**Carl Ward #1 (the band + provenance) — CONFIRMED.** The z=3 decline is a **combo-dependent band, median a₀(z=3)/a₀(0) ≈ 0.61–0.71**, with a **marginal significance of ~2.3–3.0σ** (vs the ΛCDM null a₀=const), **inherited from — and weaker than — DESI's own evolving-DE preference.** It is *not* a clean independent detection. §5 should quote the band + the ~2.4–2.7σ-class significance + its provenance, exactly as the review says. (My DR1 band brackets the review's stated 2.4–2.7σ.)

**Carl Ward #2 (the non-monotonic near-field direction) — CONFIRMED, and the old wording was wrong.** a₀(z) is **non-monotonic**: it sits **+3% to +8% ABOVE local at z ≈ 0.3–0.7** (the phantom-divide bump, since the DESI-preferred w₀ > −1 makes ρ_DE rise before wₐ < 0 turns it over), returns through unity near **z ≈ 1.0–1.3**, and only the **z ≳ 2** decline is appreciable. So the manuscript's "the high-z BTFR zero-point sits slightly below the local one" is **wrong in the accessible (z ≲ 1) regime — there it sits slightly *above*.** The clean below-local decline is a z ≳ 2 statement only.

## Net
The framework's a₀(z) prediction, propagated through the real DESI posterior, is **a marginally-distinctive, non-monotonic, combo-dependent band whose significance is hostage to DESI's w₀wₐ preference** — honestly scoped, exactly as Carl Ward recommended. The §5 revision writes itself from this table.

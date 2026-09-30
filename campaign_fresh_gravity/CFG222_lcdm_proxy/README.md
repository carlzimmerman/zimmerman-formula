# CFG222 — a ΛCDM effective-a₀ PROXY scored on real data with the machinery used for flat and H(z)

> **⚠ ΛCDM has no a₀. This is an effective-a₀ PROXY, not ΛCDM. A fair ΛCDM test uses simulated galaxies.** The proxy is the record's "emergent" halo-structure scale applied as if it were a₀(z).

- **Criteria:** `FROZEN_CRITERIA.md` (35e3df460), committed before any proxy number. Requested via the orchestrator. **κ = ½ FITTED, NOT DERIVED.** Not blind for the flat law and H(z) (CFG216 / 217 / 213 / 220 were known); every proxy number is new.
- **The proxy (primary) = Z1's "ΛCDM-native"** (`sonnet55_push/puzzle_32pi/agents/Z1_causal_horizon_a0z/zcommon.py`, 1138d817f, `lcdm_native`): F(z) = E_l274(z)^{4/3} · [c²/f(c)](z) / [c²/f(c)](0), E_l274 = √(0.3027 (1+z)³ + 0.6973), c(M, z) from Dutton & Macciò 2014 at M = 10¹² h⁻¹ M☉, f(c) = ln(1+c) − c/(1+c): F = 1.23 / 1.77 / 2.16 at z = 1 / 2 / 2.5 (+0.33 dex at 2.5), 4.52 at z = 4.5, 6.20 at z = 5.5. **Sensitivities: the record's own a₀(z)-lane estimates** (`prep_2026/a0z_crossscale/a0z_lcdm_native_hypothesis_2026.py`: M-LCDM-DM14, the README's "+0.33 dex" (× 2.126 at 2.5), M-LCDM-D08 (× 2.802, +0.45 dex), M-LCDM-MAG ((1+z)^0.92, × 3.166)) and Z1's own M = 10¹¹ / 10¹³ and dlogc = ±0.1. **Validity:** DM14 is fitted to z ≤ 5 (CRISTAL reaches 5.69), Duffy+2008 to z ≲ 2 and the Magneticum rise to z ≲ 2–3: every CRISTAL row is an EXTRAPOLATION for D08 and MAG and, above z = 5, for DM14.
- **Run:** `python3 campaign_fresh_gravity/CFG222_lcdm_proxy/cfg222_lcdm_proxy.py` (about 70 s; `MUTATE=1` runs the response control), `cfg222_plot.py` for the chart. **Controls 7 of 7 pass** (law values; FLAT and H(z) reproduce CFG216's committed RC100 slopes on both tables, CFG213's R_e fit-route medians, CFG220's R_out medians on both routes and CFG213's independent-route rows, all to 1e-9 or exactly; a non-vacuous placement of 250 synthetic rows on each of the ten laws through V_c, R_e, f_DM: max |δ| 2.9e-16, other-law sensitivity 93%; the expectation identity; MUTATE).

## The table: where the data sit against each law's expectation (primary cell ν_mono, canonical)
Statistic: RC100 = Theil–Sen slope of δ on z (per unit z); CRISTAL = median δ. **z** = (observed − expected)/bootstrap sd: against the law's OWN expectation (0) and against the FLAT-true expectation of that law's statistic (CFG216's constant-expectation convention). **Every row is conditional on its gas route** (RC100 and the fit rows: the authors' M_bary, prior-anchored or 1-dex-prior, not an independent calibration; the independent rows: SED M★ + dust gas).

| row (gas route) | FLAT: stat [95% CI]; z own / z flat-true | LCDM-PROXY (not ΛCDM) | H(z) |
|---|---|---|---|
| RC100 committed, n = 100 (fit, prior-anchored) | −0.029 [−0.072, +0.002]; **−1.57** / −1.57 | −0.067 [−0.108, −0.033]; **−3.55** / −1.70 | −0.092 [−0.129, −0.054]; **−4.80** / −1.68 |
| RC100 corrected (fit, prior-anchored) | −0.030 [−0.074, +0.002]; **−1.55** / −1.55 | −0.069 [−0.111, −0.033]; **−3.53** / −1.74 | −0.091 [−0.130, −0.055]; **−4.70** / −1.67 |
| CRISTAL R_e, n = 12 (fit, 1-dex prior) | +0.053 [+0.005, +0.234] DISFAV-over; **+0.90** / +0.90 | −0.110 [−0.148, +0.020] CONSISTENT; **−2.32** / +0.65 | −0.161 [−0.207, −0.055] DISFAV-under; **−3.53** / +0.90 |
| CRISTAL R_e, six class-A (independent) | +0.117 [−0.060, +0.384] CONSISTENT; **+0.87** / +0.87 | −0.085 [−0.253, +0.207] CONSISTENT; **−0.64** / +0.68 | −0.144 [−0.319, +0.141] CONSISTENT; **−1.13** / +0.72 |
| CRISTAL R_out, six (fit) | +0.019 [−0.109, +0.172] CONSISTENT; **+0.32** / +0.32 | −0.220 [−0.364, −0.037] DISFAV-under; **−2.99** / −0.06 | −0.283 [−0.440, −0.109] DISFAV-under; **−3.79** / +0.01 |
| CRISTAL R_out, six (independent) | +0.106 [−0.138, +0.343] CONSISTENT; **+0.74** / +0.74 | −0.136 [−0.402, +0.107] CONSISTENT; **−0.98** / +0.58 | −0.203 [−0.477, +0.029] CONSISTENT; **−1.51** / +0.60 |

**The gas-calibration windows** (the calibration that would make each law consistent with 0): RC100 on CFG217's tilt axis (the change of the analysis baryon mass between z = 0.6 and 2.5, negative = lighter at high z): **t\* = −0.073 (flat), −0.177 (proxy), −0.251 (H(z))** dex, consistent windows [−0.15, 0.00] / [−0.25, −0.10] / [−0.35, −0.20] (corrected table −0.076 / −0.179 / −0.250). CRISTAL independent rows on CFG220's uniform gas-mass offset τ: R_e: flat τ\* +0.318 (consistent for τ ∈ [−0.30, +0.55]), proxy τ\* −0.952 ([−1.00, +0.35]), H(z) no zero ([−1.00, +0.25]); R_out: flat +0.327 ([−1.00, +0.50]), proxy no zero ([−1.00, +0.20]), H(z) no zero ([−1.00, +0.05]).

## Reading (descriptions, never a verdict on ΛCDM)
- **On RC100 the proxy sits between the flat law and H(z) in every quantity:** slope −0.067 against −0.029 and −0.092; tension with its own expectation **3.55σ** (flat 1.57σ, H(z) 4.80σ); the baryon tilt that would make it consistent −0.18 dex (flat −0.07, H(z) −0.25). The corrected table, the other three kernel/footing cells (proxy −3.1 to −3.75σ) and the seven proxy sensitivities (−2.9 to −4.4σ) say the same. All three laws sit at about −1.6 to −1.7σ from the flat-true expectation pattern, the common part being the flat law's own −1.57σ slope.
- **CRISTAL, authors' fit route:** at R_e (twelve discs) the proxy is CONSISTENT while H(z) is DISFAVOURED-under and flat DISFAVOURED-over; at R_out (six) the proxy is DISFAVOURED-under (−2.99σ) and flat CONSISTENT. So the proxy's verdict is radius-dependent on this route. At R_out the observed medians of all three laws sit on their flat-true expectations (proxy −0.220 against −0.216, H(z) −0.283 against −0.284, flat +0.019 against 0).
- **CRISTAL, independent route (the six class-A detections):** all three laws are CONSISTENT at both radii; no separation. The proxy is consistent for gas-mass offsets up to τ = +0.20 (R_out) and +0.35 (R_e), H(z) up to +0.05 and +0.25, flat throughout τ ≤ +0.50 (R_out).
- **What this is not:** a test of ΛCDM. The proxy is one halo-structure scale of the record's (and Z1's) making, used here with the flat/H(z) machinery; ΛCDM galaxies have no fixed a₀ and their scatter and assembly histories are absent. A fair test uses simulated galaxies.

## Limits and disclosures
- The z-scores use the bootstrap sd of the observed statistic with the expectation held at its full-sample value (CFG216's convention); with the expectation recomputed on every resample (CFG233) the RC100 z against the flat-true expectation is −1.57 / −1.75 / −1.79 (flat / proxy / H(z), committed table). n = 6 and 12 are small and the bootstrap sees only disc-to-disc scatter.
- Every row inherits its gas route's caveat (window column): the fit routes carry the authors' prior-anchored baryon masses; the independent route's dust gas masses are single-band, T_d-dependent.
- The proxy is extrapolated at CRISTAL's redshifts (above); the sensitivity laws even more so.
- The placement control's other-law sensitivity is 93% against the 90% line because several sensitivity variants nearly coincide in the Newtonian rows.
- Author decompositions, not a direct a₀ measurement; κ = ½ fitted; no sentence says the data favour a framework or ΛCDM.

## Chart
`cfg222_z_table.png` (from `cfg222_plot.py`): the z of each law on each row, against its own expectation (filled) and the flat-true expectation (open).

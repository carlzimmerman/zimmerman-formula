# CFG724: SPARC dark surface density vs the derived cold-energy capacity a₀/(πG) (quick test, 2026-10-13)

Post hoc, no frozen criteria (owner asked for a quick calculation). The capacity Σ_max = a₀/(πG) comes from CFG722 (the tether
bridge of the P-field action): 214 M☉/pc² (canonical) / 258 (alt). Data: raw SPARC rotmod (175 galaxies). Σ_dark(<R) =
(V_obs² − V_bar²) R / (G π R²). Script: `cfg724_capacity.py` (all radii, results JSON); the deep-regime cut (g_bar < a₀,
where cold energy settles) was run inline and is reported here.

| Υ_disk / Υ_bul | regime | points above ceiling (can / alt) | > 3σ above (can / alt) | median Σ (can / alt) |
|---|---|---|---|---|
| 0.5 / 0.7 | deep (g_bar < a₀) | 4.6% / 3.2% | 35 pts in 9 gal / 27 in 7 | 63 / 65 |
| 0.3 / 0.5 | deep | 12.3% / 9.3% | 145 in 27 / 117 in 22 | 79 / 81 |
| 0.8 / 1.0 | deep | 1.5% / 0.7% | 0 / 0 | 47 / 47 |
| 0.5 / 0.7 | all radii | 12.5% / 9.6% | 189 / 128 | 71 / 71 |

Reading: in the regime where the capacity applies, galaxies sit well below the ceiling (median ≈ 0.3 of it, i.e. below the
a₀/(2πG) "plateau" value); the few > 3σ excursions are massive bulge-dominated spirals (NGC 2841, NGC 5985, NGC 6015, …) and
vanish at higher stellar M/L, i.e. they track the stellar-mass assumption. All-radii excursions are inner points where the
baryon model dominates. **Verdict: CONSISTENT, not discriminating** — the ceiling is a loose upper bound; a sharper test needs
the capacity's radial form (the tether profile), not just its maximum. κ = ½ fitted; not theory closed.

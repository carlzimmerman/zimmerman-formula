# switch_audit_2026 — does one bound-region threshold serve every mass bin?

L342 (`real_research/g03_audit_2026/L342_bound_region_switch.py`) switches the C-H/K phantom off outside
the bound region x = 9R3/(4K^2) = 4 pi G rho_dyn / H^2 > x_c, and finds that KiDS-1000's lensing
prefers a switch at x_c ~ 4-7. That fit uses ONE threshold for all four stellar-mass bins. If the switch
is physical, one x_c must serve every bin; a mis-scaled truncation radius r_t = v_flat/(sqrt(x_c) H)
would show up as x_c drifting with mass.

| Lane | Script | Checks | Result |
|---|---|---|---|
| BS1 | `BS1_per_bin_threshold.py` | 4/5 (S3 fails, recorded) | L342 reproduced exactly (S1). Shared x_c = 5 / 6 (canonical / alt) improves chi^2 by 18.3 / 19.7 over no switch. Four free thresholds [4, 6, 2, 5] improve chi^2 by a further 8.0 / 7.5 for 3 parameters: p = 0.046 canonical (the pre-set p > 0.05 gate fails narrowly), 0.059 alt (passes). No monotonic trend with mass (Spearman rho = 0.00), so it is scatter, not an r_t scaling error; bin 2 carries most of the switch preference. Power study (S5, 20 draws each): 0/20 false rejections, 18/20 rejections of a 2 -> 20 drift. |

**Standing:** a lead with a marginal internal tension (~2 sigma), not a confirmation and not a
falsification. All of this is on L342's own base model (point-mass baryons, no two-halo term, no external
field; chi^2 ~ 97/60 after the switch), so the absolute fit quality limits what any threshold test can say.

Controls: `MUTATE=1` replaces the data with a synthetic set whose true threshold drifts 2 -> 20 across the
bins; S3 must then fail (rc = 1). Outputs are written separately (`*_MUTATE.out`, `*_results_MUTATE.json`).

# switch_audit_2026 — support audits of L342's bound-region switch on KiDS-1000 lensing

L342 (`real_research/g03_audit_2026/L342_bound_region_switch.py`) switches the C-H/K phantom off outside
the bound region x = 9R3/(4K^2) = 4 pi G rho_dyn / H^2 > x_c, and finds that KiDS-1000's lensing
prefers a switch at x_c ~ 4-7. That fit uses ONE threshold for all four stellar-mass bins. If the switch
is physical, one x_c must serve every bin; a mis-scaled truncation radius r_t = v_flat/(sqrt(x_c) H)
would show up as x_c drifting with mass.

| Lane | Script | Checks | Result |
|---|---|---|---|
| BS1 | `BS1_per_bin_threshold.py` | 4/5 (S3 fails, recorded) | L342 reproduced exactly (S1). Shared x_c = 5 / 6 (canonical / alt) improves chi^2 by 18.3 / 19.7 over no switch. Four free thresholds [4, 6, 2, 5] improve chi^2 by a further 8.0 / 7.5 for 3 parameters: p = 0.046 canonical (the pre-set p > 0.05 gate fails narrowly), 0.059 alt (passes). No monotonic trend with mass (Spearman rho = 0.00), so it is scatter, not an r_t scaling error; bin 2 carries most of the switch preference. Power study (S5, 20 draws each): 0/20 false rejections, 18/20 rejections of a 2 -> 20 drift. |

| BS2 | `BS2_efe_vs_switch.py` | 11/15 (E3b, E6, E9, E13 fail, recorded) | The external-field effect (EFE) the QUMOND-form model already contains, via an exact stacked-lens flux law (sphere-averaged enclosed mass M_b N(y, e), limits verified). **(1)** A weak field (e ~ 7e-5) does most of the switch's work (Δχ² −13.5 / −14.2); with it in, the switch adds only −4.9 / −5.6, and the data cannot reliably tell the two truncations apart (power 0.80 / 0.55). L342's KiDS preference is not specific evidence for the switch. **(2)** KiDS bounds the Newtonian external field: e ≤ 7.2e-5 / 5.2e-5 (stacked rms ≤ 6.7e-5 / 4.6e-5 a0). The switch keeps the linear web Newtonian and ΛCDM-like, so the construction's own field on a lens is σ_g,3D = 0.013 / 0.011 a0 (E-H P(k), σ_v,1D ≈ 265–300 km/s check), ~200× over the bound. C-H/K's kernel takes free-fall fields (L340 S1 runs it on the Sun with the Galaxy's field). Result: Δχ² +569 / +582 on all points, +40 / +45 inside 0.3 Mpc, where Brouwer+21 treat isolation as certain and no two-halo term can help. **Sensitivity:** at Brouwer+21's 4× weaker adopted field (e = 0.003; 1.6% of the Maxwell field is that quiet) it passes inside 0.3 Mpc and fails by +320 / +362 only at 0.3–3 Mpc. A baryons-only kernel fails on all points (+250) but passes inside 0.3 Mpc: not excluded here. Control: pure MOND (field MOND-level, e_N = e_M²) is not excluded by the same machinery. |

**Standing (BS2):** as built (the kernel's argument is the total filtered Newtonian field; the switch leaves the web
Newtonian), C-H/K + switch fails KiDS-1000 isolated lensing through its own external-field effect. The failure is
+570 in χ² on all points, and also inside the clean radius if isolated lenses feel the ΛCDM-typical field. Two things
would make it a clean exclusion: the external field conditioned on isolation, and a two-halo term at 0.3–3 Mpc. Two
doors remain: a kernel sourced by baryons only, or one blind to the large-scale field. Each is a new ingredient, and
each is constrained by the Solar-System floor, which needs the Galaxy's field in the kernel.
Prior art: Brouwer+21 (A&A 650, A113, §5.2) show a MOND EFE at e = 0.003 moves the prediction away from their data;
Mistele+24 (ApJL 969, L3) find lensing velocities flat to ~1 Mpc.

**Standing (BS1):** a lead with a marginal internal tension (~2 sigma), not a confirmation and not a
falsification. All of this is on L342's own base model (point-mass baryons, no two-halo term, no external
field; chi^2 ~ 97/60 after the switch), so the absolute fit quality limits what any threshold test can say.

Controls: BS1 `MUTATE=1` replaces the data with a synthetic set whose true threshold drifts 2 -> 20 across the
bins; S3 must then fail (rc = 1). BS2 `MUTATE=1` replaces the data with an EFE-only synthetic set (e = 1e-4, no
switch); E3a must then fail (rc = 1). Outputs are written separately (`*_MUTATE.out`, `*_results_MUTATE.json`).

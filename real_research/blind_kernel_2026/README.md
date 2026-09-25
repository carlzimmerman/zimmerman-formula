# blind_kernel_2026 — a C-H/K kernel blind to the large-scale field

Motivation: `real_research/switch_audit_2026` (BS2, BS3). C-H/K + L342's switch is excluded by KiDS-1000 isolated
lensing through its own external-field effect. The web's Newtonian field (~0.015 a0 rms) enters the kernel's argument
and ends every lens's phantom at ~0.1 Mpc.

| Lane | Script | Checks | Result |
|---|---|---|---|
| BK1 | `BK1_screened_kernel.py` | 4/5 (C3 fails, recorded) | **Construction:** the kernel's argument is the Yukawa-screened Newtonian field, (∇² − 1/λ²)Φ_b = 4πGρ. Sources inside λ act in full; long-mode external fields are screened as (kλ)². Exact stacked-lens flux law M_dyn = M_b[1 + s(N(s y_N, e_b) − 1)], s = (1 + r/λ)e^(−r/λ). **Sun + SPARC** (Galaxy's field kept ≥ 99.9%, g_obs at 100 kpc within 1%) need λ ≥ 0.5 Mpc. **Screened web field** on an isolated lens (linear ΛCDM, outside 3 Mpc, exact screened window): 4.6e-5 a0 at λ = 0.7 Mpc, down from 1.5e-2 unscreened. **KiDS** (BS3's fit: 2-halo b ≤ 2, x_c profiled): the best λ = 0.7 Mpc gives Δχ² +7.7 / +8.0 against the EFE-free (unphysical) switch comparator. For scale, the unscreened construction gives +396 / +408 and pure MOND +17 / +16. At this λ the switch is unused (best x_c = 0): the screening itself truncates each lens. The window at Δχ² ≤ 4 is **empty**. Injection at λ = 0.7: passes 10/10. MUTATE (no screening): +396, rc = 1. |

**Standing:** the screened kernel is the best physical model of KiDS isolated lensing tested on the record. It sits 380
in χ² better than the unscreened construction and ~9 better than pure MOND. It still misses the pre-set gate by
Δχ² ≈ 8 (~2.8σ) against an EFE-free idealisation. Its cost is one free length, λ ≈ 0.6–0.8 Mpc, with no derivation.
The truncation it predicts is mass-independent (r ~ λ), against r_t ∝ M^(1/4) for the switch and r_e ∝ M^(1/2) for
the EFE. Not done: λ's origin, and the massive auxiliary field's health, tracking (L330/L340) and 1PN. Growth is still
the switch's job, or needs re-checking, because with screening the linear web's argument is suppressed as (kλ)².

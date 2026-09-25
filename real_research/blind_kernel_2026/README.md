# blind_kernel_2026 — a C-H/K kernel blind to the large-scale field

Motivation: `real_research/switch_audit_2026` (BS2, BS3). C-H/K + L342's switch is excluded by KiDS-1000 isolated
lensing through its own external-field effect. The web's Newtonian field (~0.015 a0 rms) enters the kernel's argument
and ends every lens's phantom at ~0.1 Mpc.

| Lane | Script | Checks | Result |
|---|---|---|---|
| BK1 | `BK1_screened_kernel.py` | 4/5 (C3 fails, recorded) | **Construction:** the kernel's argument is the Yukawa-screened Newtonian field, (∇² − 1/λ²)Φ_b = 4πGρ. Sources inside λ act in full; long-mode external fields are screened as (kλ)². Exact stacked-lens flux law M_dyn = M_b[1 + s(N(s y_N, e_b) − 1)], s = (1 + r/λ)e^(−r/λ). **Sun + SPARC** (Galaxy's field kept ≥ 99.9%, g_obs at 100 kpc within 1%) need λ ≥ 0.5 Mpc. **Screened web field** on an isolated lens (linear ΛCDM, outside 3 Mpc, exact screened window): 4.6e-5 a0 at λ = 0.7 Mpc, down from 1.5e-2 unscreened. **KiDS** (BS3's fit: 2-halo b ≤ 2, x_c profiled): the best λ = 0.7 Mpc gives Δχ² +7.7 / +8.0 against the EFE-free (unphysical) switch comparator. For scale, the unscreened construction gives +396 / +408 and pure MOND +17 / +16. At this λ the switch is unused (best x_c = 0): the screening itself truncates each lens. The window at Δχ² ≤ 4 is **empty**. Injection at λ = 0.7: passes 10/10. MUTATE (no screening): +396, rc = 1. |

| BK2 | `BK2_derive_lambda.py` | 3/5 (D2, D3 fail, recorded) | **Can λ be derived?** A constant λ cannot. The framework's lengths are c/H0 = 4451, a0/H0² = 637 and c²/a0 = 3.1e4 Mpc. 48 of 5831 small-exponent combinations c/H0·Z^n·Ω_Λ^m·Ω_m^q·(2π)^r land in 0.6–0.8 Mpc, so any single "hit" is numerology. The construction's one length near 1 Mpc is mass-dependent: λ = v_flat/(√X H), since v² = \|a\|²/(4πGρ_dyn) and 4πGρ_dyn = xH² are C-H/K clock scalars. KiDS mildly prefers λ ∝ M^(1/4) over a constant (Δχ² −2.5 / −2.2; M^(1/2) is no better than constant). But the derived form's best X = 10, outside the switch's 2–7 range, so it is not L342's r_t and X is still a fitted number. It reaches Δχ² +5.3 / +6.8, missing the ≤ 4 gate. SPARC and the Sun are untouched (≤ 0.2%, λ_MW ≈ 0.6 Mpc). MUTATE (constant-λ synthetic data) fails D1, rc = 1. |

**Standing (BK2):** λ is **not derived**. The best available form trades a free length for a free O(10) number,
X ≈ 10, which is not the switch's threshold. The data's mild preference for M^(1/4) is ~1.6σ.

**Standing (BK1):** the screened kernel is the best physical model of KiDS isolated lensing tested on the record. It sits 380
in χ² better than the unscreened construction and ~9 better than pure MOND. It still misses the pre-set gate by
Δχ² ≈ 8 (~2.8σ) against an EFE-free idealisation. Its cost is one free length, λ ≈ 0.6–0.8 Mpc, with no derivation.
The truncation it predicts is mass-independent (r ~ λ), against r_t ∝ M^(1/4) for the switch and r_e ∝ M^(1/2) for
the EFE. Not done: λ's origin, and the massive auxiliary field's health, tracking (L330/L340) and 1PN. Growth is still
the switch's job, or needs re-checking, because with screening the linear web's argument is suppressed as (kλ)².

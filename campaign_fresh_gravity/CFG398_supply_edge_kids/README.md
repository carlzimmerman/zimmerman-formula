# CFG398: a supply-limited phantom vs KiDS's required reach. TENSION at census retention; only f_ret ≤ ~0.07 reaches

Criteria cca28095f (committed before the script). Script `cfg398_supply_edge.py` (< 1 s). κ = ½ fitted; both footings. No DM particle; the cold mass is required and its amount is free.

If the law's phantom must be filled by real cold fluid (the settling working model), and a lens's supply is CFG365's (Ω_c/Ω_b) × original baryons = 5.364 M_b / f_ret, the law stops at r_edge where the enclosed phantom equals the supply. CFG4 says KiDS needs the phantom out to x = r_t / r_ta ≥ 0.30 (with a 2-halo term) or ≥ 0.47 (without).

| f_ret (Shull+2012 census) | canonical: x_edge at log M_b 10 / 10.5 / 11 / 11.5 | verdict | alt | verdict |
|---|---|---|---|---|
| 0.07 (galaxies only) | 0.31 / 0.42 / 0.56 / 0.74 | CONSISTENT (barely) | 0.29 / 0.38 / 0.51 / 0.68 | TENSION |
| 0.10 | 0.22 / 0.29 / 0.39 / 0.52 | TENSION | 0.20 / 0.27 / 0.36 / 0.48 | TENSION |
| 0.18 (all collapsed phases) | 0.12 / 0.16 / 0.22 / 0.29 | TENSION | 0.11 / 0.15 / 0.20 / 0.27 | TENSION |

**Largest f_ret that keeps x ≥ 0.30 (≥ 0.47):** canonical 0.073 (0.047) at log M_b 10, rising to 0.175 (0.111) at 11.5; alt 0.066 (0.042) to 0.159 (0.101).

- **Reading.** The low-mass lenses bind. A supply-limited phantom reaches KiDS's minimum only if those galaxies kept ≤ ~7% of their original baryons, the lower edge of the census. At the census central value (~0.10) it falls short (x ≈ 0.2–0.3 at log M_b 10–10.5). This is the lensing counterpart of CFG365's galaxy-level VIABLE: viable inside discs, tight at lensing radii.
- **Caveats.** Point-mass baryons and the deep phantom; all of the supply bound to the lens and filling the target from the centre out (the most favourable case). r_ta interpolated log-linearly between CFG4's two quoted values. CFG4's window comes from a joint fit, not per-bin limits.
- **Controls.** K1 (exact root vs deep estimate, within 1%) and K2 (monotone) pass. **MUTATE** (supply ×100) makes every cell CONSISTENT-STRICT: detected, exit 1.

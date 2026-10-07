# CFG398: does a supply-limited phantom reach as far as KiDS needs? FROZEN before any script exists

Owner chat 10-06. κ = ½ fitted; both footings (9.3603e-11 / 1.1312e-10). No DM particle; the cold mass is required and its amount is free.

**The model.** In the settling working model (c182a32a1) the law's phantom must be filled by real cold fluid. CFG365's supply: cold mass available to a lens = (Ω_c/Ω_b) × original baryons = 5.364 M_b,now / f_ret. The phantom enclosed in r (point-mass baryons, ν_mono) is M_ph(<r) = (ν_mono(G M_b / r² a₀) − 1) M_b. **r_edge** is where M_ph(<r_edge) = 5.364 M_b / f_ret. Beyond it the law cannot be realised.

**The requirement (record, CFG4_README "KiDS reach").** With the phantom truncated at each lens's own radius, KiDS allows x = r_t / r_ta ∈ [0.30–0.31, ~1.5] with a 2-halo term, and [0.47–0.50, ~1.5] without. r_ta = 0.95 Mpc at log M_b = 10 and 2.25 Mpc at 11.5 (CFG4), log-linearly interpolated (declared).

**Grid.** log M_b = 10.0, 10.5, 11.0, 11.5 (spanning the KiDS bins); f_ret = 0.07, 0.10, 0.18 (Shull, Smith & Danforth 2012: galaxies only / central / all collapsed phases, as used in CFG365).

**Verdict per f_ret and footing.**
- CONSISTENT if x_edge ≥ 0.30 at every mass.
- CONSISTENT-STRICT if x_edge ≥ 0.47 at every mass.
- TENSION if any mass has x_edge < 0.30.
- Reported: the largest f_ret that keeps x_edge ≥ 0.30 (and ≥ 0.47) at each mass.

**Controls.** K1: for log M_b = 11, r_edge from the exact ν_mono root agrees with the deep-limit estimate r_M (1 + 5.364/f_ret), r_M = √(G M_b / a₀), to 5%. K2: f_ret → 1 gives x_edge below the f_ret = 0.18 value (monotone).

**MUTATE (`--mutate`).** Supply ×100. Every cell must become CONSISTENT-STRICT; exit 1 when that is detected.

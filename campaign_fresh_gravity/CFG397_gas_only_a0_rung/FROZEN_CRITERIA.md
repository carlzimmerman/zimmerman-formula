# CFG397: an M/L-free a₀ rung (gas-dominated points, distance-anchored). FROZEN before any script exists

Owner chat 10-06 ("swing all this"). κ = ½ fitted; both footings (9.3603e-11 / 1.1312e-10). No DM particle; the cold mass is still required.

**Why.** CFG390 (session02) found SPARC's a₀ moves 0.24 dex between Υ_disk 0.5 and 0.7, the dominant local calibration floor. Points where gas dominates the baryons make a₀ nearly Υ-free.

**Data.** CFG4_common.load_sparc(), Q ≤ 2. A point is gas-dominated if V_gas² ≥ 0.7 V_bar² at Υ_disk = 0.5, Υ_bul = 0.7 (the same as CFG390 session06). Galaxies need ≥ 3 such points. CFG4's point weights.

**Fit.** One free a₀ (bounded scalar minimisation of the weighted Σ(log g_obs − log ν_mono(g_bar/a₀) g_bar)²), for: (A) all distance methods; (B) the ladder anchor, f_D ∈ {2 TRGB, 3 Cepheid, 5 SNe}; (C) Hubble flow, f_D = 1. Bootstrap over galaxies (500, seed 7).

**Υ-insensitivity check (K1).** Refit (A) at Υ_disk = 0.3 and 0.7 (the same point selection, frozen at 0.5). PASS if |Δlog a₀| ≤ 0.05 dex for 0.5 → 0.7, i.e. ≤ ¼ of the all-points shift (0.24).

**Comparisons (reported, no new fit).** (i) Both footings. (ii) PAPER43's gas-point a₀ = 8.3e-11 ± 13% (distance-conditional). (iii) CFG301 stage B subset "(ii) gas-dominated (M_gas > M*)", read from cfg301_stageB_results.json (BTFR widths, not rotation curves).

**Verdicts.**
- RUNG ESTABLISHED if K1 passes and the anchor (B) has σ ≤ 0.05 dex.
- Report which footing (B) is closer to, in σ; |Δ| < 2σ from a footing means consistent.
- FLOW−LADDER (C − B) reported, with the CFG390 caveat (distance response ~D^−2.7).

**MUTATE (`--mutate`).** Drop the gas term (V_gas → 0). The gas-dominated selection then becomes empty; the script must detect the empty selection and exit 1.

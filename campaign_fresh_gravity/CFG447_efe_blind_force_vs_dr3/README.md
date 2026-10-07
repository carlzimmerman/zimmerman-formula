# CFG447: the law as a force with NO external-field effect is EXCLUDED by Gaia DR3 (7.7σ canonical / 8.3σ alt)

Criteria 4ee7c651d (committed before the script). Script `cfg447_efe_blind.py` (~1 min). The frozen DR4 pipeline is imported read-only (sha256 unchanged, K2). κ = ½ fitted; both footings. **Not a DR4 result and not an amendment.**

| kernel | footing | recovered γ̂ for an EFE-blind force (10 mocks, N = 6,210, DR3 noise) | vs DR3 builder build | vs literal build | verdict |
|---|---|---|---|---|---|
| ν_mono | canonical | ≥ 1.50 (10/10 pinned at the grid top) | 1.0750 ± 0.0550: **+7.7σ** | 1.1175 ± 0.0625: +6.1σ | **EXCLUDED** |
| ν_mono | alt | ≥ 1.50 (10/10) | 1.0775 ± 0.0512: **+8.3σ** | 1.0875 ± 0.0537: +7.7σ | **EXCLUDED** |
| ν_P2 | both | ≥ 1.50 (10/10) | +7.7σ / +8.3σ | +6.1σ / +7.7σ | EXCLUDED |

**What it closes (the consistency triangle).**
- **Force WITH the EFE:** fails cluster satellites (cm14b: the host-EFE reading at χ² 99.7/5, +0.81 dex).
- **Force WITHOUT the EFE:** fails wide binaries (this lane; pinned values are lower bounds, so the true exclusion is stronger).
- **Material phantom (the settling working model):** passes both. Satellites carry settled fluid; binaries are Newtonian (Amendment 21: γ = 1.000). It is strained by KiDS's reach (CFG398: needs f_ret ≤ ~0.07) and, if the satellite planes are tidal debris, by CFG391.
- ΛCDM passes cm14b and wide binaries too. Nothing here favours the framework over ΛCDM.

**Caveats.**
- K1 (Arm A's EFE-saturated 1.1614 injected) recovers **1.205 ± 0.046**: a PASS within 2σ, but biased high by ~0.04. The data use DR3 noise while the model master uses DR4 noise, as the pipeline's catalog runs do. So the measured DR3 γ̂ may itself be inflated by a similar amount. This only strengthens the exclusion.
- Master size 1e6 (the pipeline uses 3e6; the machine is shared).
- The velocity-scaling boost shortcut is the pipeline's own.

**MUTATE (Newton injected): NOT YET RUN.** It was deferred because the owner asked for no CPU jobs overnight (relayed by the orchestrating session, 10-06). It will run as `python3 cfg447_efe_blind.py --mutate` and must recover 1.00 ± 0.03 (exit 1). Given K1's +0.04 noise bias, that MUTATE may fail its ±0.03 tolerance. That would say the DR3-noise/DR4-model mismatch matters, not that the exclusion is wrong.

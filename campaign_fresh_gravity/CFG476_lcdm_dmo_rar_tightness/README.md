# CFG476: dark-matter-only ΛCDM does NOT reproduce SPARC's RAR. Twice the scatter, a₀ ×2.8 too high, too shallow at low acceleration. In ΛCDM the arranging must come from baryonic physics

Criteria 797b900ce (committed before the script). Script `cfg476_dmo_rar.py` (~3 s). κ = ½ fitted; both footings reported. ΛCDM is the comparator here, and no particle is added by the framework.

| | rms about the law (a₀ free) | best-fit a₀ | slope d log g_obs / d log g_bar at g_bar < 1e-11 |
|---|---|---|---|
| SPARC data (163 gal, Q ≤ 2, Υ 0.5/0.7) | **0.099 dex** | 1.37e-10 | 0.605 |
| DMO-ΛCDM mocks (200; Moster+13 AM, 0.15 dex scatter; Dutton–Macciò NFW, 0.11 dex scatter; same noise) | **0.205** (16–84%: 0.169–0.253) | **3.9e-10** (3.0–5.7e-10) | 0.401 |

**Verdict: DMO-ΛCDM FAILS.** 95% of mocks have rms ≥ data + 0.05 dex, exactly at the frozen line. So "FAILS" is marginal on that clause, but the median is 2.1× the data's scatter.

**Reading.**
- Abundance-matched NFW halos with standard scatter, and no feedback, contraction or cores, give a RAR twice as broad as observed. Its acceleration scale is ~3× too high and its low-acceleration slope too shallow.
- So in ΛCDM the tight, single-scale RAR is produced by **baryonic physics** (feedback cores, contraction, the coupling of halo response to baryons), not by assembly alone. That is ΛCDM's answer to "who arranges the cold mass", and it is the answer hydrodynamic simulations give in the literature.
- **This does NOT show ΛCDM fails.** Hydrodynamic simulations with feedback are not tested here. It shows what ΛCDM's arranging must do: roughly halve the scatter and move g† down by ×3.
- It sharpens the contrast with the framework, where the arranging is one law.

**Controls.**
- K2 (Moster round-trip) passes.
- K1 (data statistic) gives 0.0994 dex at fixed Υ, matching the record's ~0.10.
- MUTATE (mocks generated from the law plus the same noise) gives rms 0.017 dex: REPRODUCES, detected (exit 1). Observational noise alone contributes only ~0.017 dex, so the data's 0.099 is mostly intrinsic plus M/L.

**Scope and caveats.**
- The stellar mass uses a fixed Υ.
- The SHMR is Moster+13 at z = 0. Other SHMRs, or the scatter in them, would shift the mock rms, and that is not scanned.
- Halo response to baryons is ignored by construction.

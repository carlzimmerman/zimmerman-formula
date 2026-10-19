# CFG844 — H-PRIM: free cold energy collapsed at the dwarf's own assembly epoch as the faint-dwarf excess

Criteria: `FROZEN_CRITERIA.md` (970c67ce3, before the script). Run: `python3 cfg844.py` (MUTATE `CFG844_MUTATE=1`). Seconds.
Native cosmology: CFG654 cmb tables (h 0.678, Ω_m 0.310, native σ8 0.825); EdS spherical collapse (δ_c 1.686, Δ_c 178).

## Result — frozen CLASS: **SUPPORTS** — but the trend part is weak and non-specific; the amplitude is the informative part
- **T1 trend:** Spearman ρ(ρ_need, ρ_vir,free) = +0.56 (p 0.002), log-log slope 0.95 (H-PRIM predicts 1).
  - **By construction, the rank correlation is just a mass trend:** ρ_vir,free is a strictly monotonic function of M_b
    (through M_cat and z_c), so ρ(ρ_need, ρ_vir,free) = −ρ(ρ_need, M_b) exactly (0.561 both). Any model whose density falls with
    mass passes this part.
  - **The slope is weakly constrained:** bootstrap 68% [0.41, 1.91], 95% [−0.02, 3.02]; without NGC 205 it is 1.79.
- **T2 amplitude (the informative part):** the 25 dwarfs with an excess need a median **P = 141** times the collapse-epoch
  virial mean density of the free cold share (16–84%: 46–266; full range 12–1946, NGC 205 the outlier), at
  r_1/2/r_vir = 0.02–0.25 (all inside r_vir). Collapse epochs z_c = 1.7 (NGC 205) to 4.8 (CVn II, Leo IV).
  A collisionless collapse naturally reaches mean densities ~10²× the virial mean at ~0.1 r_vir, so these densities are
  reachable by the framework's own free cold energy if it collapses with the dwarf instead of being spread to r_ta.
- **MUTATE bites:** with no early collapse (z_c = 0) the needed factor is ~1.3e4 → FAILS. The early assembly epoch is what
  makes the densities reachable.
- Field dwarfs behave like satellites (P 12–174), consistent with CFG843 (not environmental).
- **Reading:** H-PRIM is the first framework-native mechanism in this chain that can reach the satellite-dwarf densities:
  the dwarfs' free cold-energy share, collapsed at their own assembly epoch (z_c ≈ 2–5 from the native spectrum), with a
  natural inner concentration. It is a candidate, not a result: (i) the trend test is not specific; (ii) the concentration is
  inferred, not derived; (iii) it must not over-predict systems that sit on the law. **Decisive next test (named, not run):**
  calibrate P(r/r_vir) on these dwarfs and predict, with no new parameter, the inner rotation of SPARC's small gas-rich
  dwarfs (also early-collapsing); if it over-predicts them, H-PRIM is excluded.

## Controls
- K1: native σ8 0.8252, D(0) = 1. MUTATE bites (above).
- Post-hoc disclosure: H-PRIM was formulated after CFG828/843 showed the excess grows toward low g_bar and is host-independent;
  its two numerical predictions (slope 1, P in [1, 300]) were frozen before computing.

κ = ½ fitted; cold energy mass required; not theory closed.

# GC3_infall_halo_outskirts: FROZEN CRITERIA (committed alone, before any script or number)

## Why

The cluster halo normalisation decides the outer shear, and the data bracket it from both sides:

| normalisation | lane | G-OUT-M3 (Z) | other keys |
|---|---|---|---|
| fair share of baryons inside the 3 Mpc gas cut, spread on a Burkert to r_ta | X43 | +2.41 UNDER | — |
| fair share of baryons counted to r_ta | GC2 | −5.00 OVER | 9 keys fail OVER |

The record's Burkert-to-r_ta construction makes the outer mass depend on how far the baryons are counted. That
counting is a choice. This lane replaces it with what the framework's own infall physics prescribes, with no new
parameter:

1. **Shape.** Self-similar secondary infall (Bertschinger 1985). This is the r⁻⁹ᐟ⁴ slope X43 already uses to derive η
   (GAM = 2.25). The cored form is ρ(r) = ρ₀ / [(1 + x)(1 + x²)^(5/8)] with x = r/r₀. That is a core inside r₀ and
   ρ ∝ r⁻⁹ᐟ⁴ outside.
2. **Core.** Σ = ρ₀ r₀ = max(a₀/2πG, η Σ_coll(M)), X43's rule unchanged, with M = X30's Mfair + Mbt as in X43.
3. **Normalisation where the baryons are measured.** M_cold(< R500) = (Ω_c/Ω_b)_native × M_b(< R500), with Ω_c/Ω_b
   = 5.2715 (native L1 background) and M_b = X30's 1.2 × gas profile. This needs no extrapolation beyond R500 and no
   cut radius. Given Σ, it fixes r₀.
4. **Edge.** The self-similar collisionless splashback radius (first caustic), r_sp = 0.364 r_ta, using X30's own r_ta.
   The mass is constant beyond r_sp. This is conservative, because infall-region mass beyond r_sp is ignored.

Groups and SPARC are unchanged: they use EM1's M200 path, not X30's `prep`. Their X43 numbers carry over and are
re-reported. The scope is clusters, as in GC1/GC2.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Rules and configurations

- **Rules:** R4 (c_f = 4), R5 (c_f = 5) and RX48 (X48 ng48 3-seed η table).
- **Graded configuration:** the native GC3 halo.
- **Reported only:**
  - the inherited-normalisation GC3 halo, using 5.364;
  - V-rsp, with r_sp = 0.364 × GC2's extended r_ta.
- **Baseline for "newly fails":** the native Burkert halo, the same as GC1's `nat_no2h` configuration, recomputed here.

## 2. Step 0 (stop rule)

- **S0a.** The harness reproduces X43 to 3 decimals: inherited Burkert, R4, G-OUT-M3 pred 1.120 / 1.108, groups Z +2.05,
  SPARC 0.0782.
- **S0b.** Profile check on a test case: the closed-form cumulative mass equals quadrature within 1e-6. The outer
  logarithmic slope at x = 1e3 is −2.25 within 0.01, and the inner slope at x = 1e-3 is 0 within 0.01.
- **S0c.** A root r₀ exists for every cluster. Saturated cases, where Σ is too high to reach the target mass inside
  R500, are counted and reported. If more than 5 % saturate, report it; it is not a stop.

## 3. Verdict (per footing)

**The R4 class:**
- **INFALL HALO REPAIRS M3:** |Z(G-OUT-M3)| ≤ 2 in both h cells, and no key that passed on the native Burkert baseline
  newly fails.
- **REPAIRS M3 BUT BREAKS:** M3 passes, but other keys newly fail. They are named.
- **NOT REPAIRED:** M3 still fails.

**Per rule:** whether the rule "PASSES THE X43 LINE SET": SPARC on both backgrounds, groups, and all 15 keys in both h
cells. The scope is these lines only. KiDS lensing (X53) and dwarfs (X51) are not regraded here; that is a follow-up if
any rule passes.

**Robustness:** ROBUST if V-rsp gives the same R4 class.

## 4. Checks and twin

- **K1.** M_cold(< R500) equals its target within 1e-6 for every non-saturated cluster.
- **K2.** Mass is constant beyond r_sp, and the profile is monotone.
- **K3.** Peak RSS < 1 GB, one thread.
- **MUTATE (`GC3_MUTATE=1`, separate outputs).**
  - m1: the outer slope is −3, a Burkert-like tail, instead of −9/4.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a and S0b.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gc3_infall.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects.

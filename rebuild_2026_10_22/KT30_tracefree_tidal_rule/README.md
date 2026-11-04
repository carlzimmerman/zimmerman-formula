# KT30_tracefree_tidal_rule: the trace-free tidal rule FAILS the Milky Way on both footings (ξ 33-47 kpc, v_c ≤ 205, 0 cells), as predicted; alt passes the other three, canonical also fails dwarfs and SPARC

Criteria: `FROZEN_CRITERIA.md` (0d75d07bc0), alone first, confirmed landed. `kt30.py` (KT28's code with τ = |T − trT/3 I|: Cassini, dwarfs, SPARC; `--full` = KT28's norm, check R1), `kt30_mw.py` (KT29's MW arm with the trace-free norm), their `.out`, `.json`, `.time`; `kt30_FULL.out/.json`, `kt30_MUTATE.out/.json`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K844. 6 + 7 minutes, 0.87 GB peak.

**Rule:** ξ_TF = √6 τ³ / (|∇τ|² g*), τ = Frobenius norm of the trace-free tidal tensor of the system's own field, g* = a0/κ. The √6 is fixed by the deep-MOND point mass (ξ = κ r_M), not fitted. **Third post-hoc local rule** (KT27, KT28, KT30).

| test | canonical | alt |
|---|---|---|
| T0 MW: ξ_TF(R0, 0) min/median/max, cells passing all four | 37.2 / 42.4 / 46.8 kpc, **0** (v_c max 203.5) | 32.9 / 37.8 / 41.5 kpc, **0** (v_c max 204.6) |
| T1 Cassini Q2 / ceiling | 0.090, PASS | 0.169, PASS |
| T2 dwarfs (line ≥ 15/24) | 13/24, FAIL | 15/24, PASS (Fornax kept, pred 8.7) |
| T3 SPARC d rms / median | +0.0071 / +0.058, FAIL | +0.0005 / +0.029, PASS |
| **Label** | **FAILS: MW, dwarfs, SPARC** | **FAILS: MW** |

## Reading
- **The fail was predicted in the criteria and it landed as predicted.** Removing the trace only removes the isotropic part of the local density's tide. In a thin disc almost all of it sits in T_zz, so the trace-free norm keeps about sqrt(2/3) of it. Measured ratio of ξ_TF to KT29's full-tensor ξ: median 0.88 (hand estimate 0.87). The MW is still smoothed over 33-47 kpc and loses its outer pull.
- My proposal text said the trace-free part "removes the local-density term". That was wrong for a flattened density, and the correction is on record in the criteria before the run.
- So no rotationally invariant norm of the local tidal tensor, evaluated at the midplane, escapes the disc's own density: the full norm (KT29) and the trace-free norm (KT30) both fail. KT28's alt pass needed the vertical term dropped by hand.
- Away from the disc the rule behaves like KT28: alt passes Cassini, dwarfs and SPARC (SPARC median improves to +0.029 because rising inner curves, where τ_TF → 0, get little smoothing). Canonical loses two dwarfs and fails SPARC.

## As hard as a fail
- C2 (mass conservation of the smoothing) fails at these lengths, −3 % to −15 %. Disclosed as in KT29; KT17's ε = 1 (~10 kpc, mass conserved) already failed v_c, and ξ here is 3-4x that, so the label doesn't hinge on C2.
- ξ at (R0, z = 1.1 kpc) is 0.003-0.04 kpc (T_zz only, approximate): the rule still varies by 1e3-1e4 inside the disc, so only a solve with ξ varying in (R, z) could test a tidal rule fully. Not done.
- The dwarf arm keeps KT28's path, which puts the MW host's MOND field in the dwarf's ν. CZ1 (8e701cc3e6) flags that as non-Newtonian EFE; CZ2 re-grades with the Newtonian host field. T2 here is comparable to KT28 only, not to CZ2.
- The g_N·∇ν term in ∇²Φ is dropped, as in KT29.

## Checks
R1: `--full` reproduces KT28's T1-T3 (max rel 0) and the MW arm reproduces KT29's full-tensor ξ range (max rel 0). R2 1.00002. R3 uniform sphere τ_TF/τ 6.7e-15. R3b 0.001. KT29's C1, T1 pass; KT17's C3 half-space factor fails again (known; with C2 these are the 6 failed checks that make `kt30_mw.py` exit 1). MUTATE (ν = 1): Cassini Q2 0, dwarfs 3/24, SPARC fails (0.573).

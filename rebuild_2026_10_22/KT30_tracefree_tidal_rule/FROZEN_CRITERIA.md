# KT30_tracefree_tidal_rule — FROZEN CRITERIA (before any script; only the hand estimate below)

Owner, 2026-11-03: after KT29 (the full-tensor tidal rule fails the Milky Way because the vertical component, set by local
density, dominates), freeze a trace-free tidal rule and grade it on all four tests, both footings.

κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. No
download. **Post hoc: this is the third local-rule attempt** (KT27 g-based, KT28 Frobenius tidal, KT30 trace-free tidal),
chosen after KT29's fail; the register counts the attempts.

## A correction on record before anything runs
When proposing this lane I said the trace-free part "removes the local-density term". **That's only true for an isotropic
density.** By Poisson, the trace is ∇²Φ (≈ ν 4πGρ_b in the disc). Removing it takes away the isotropic part only. In a thin
disc nearly all of the density's tide is in T_zz, so the trace-free part keeps about (2/3) of it: with T_zz dominant,
|T_TF| ≈ sqrt(2/3) |T_zz| ≈ 0.82 |T|. So **I expect the trace-free rule to fail the MW much as KT29 did.** It's frozen anyway at
the owner's request, and because it's a clean rule (it vanishes in any uniform field and in any uniform-density region).

## The rule
T = ∇∇Φ of the system's own field (as KT28: uniform external field drops out). T_TF = T − (tr T / 3) I. τ = |T_TF| (Frobenius).

ξ_TF = √6 τ³ / (|∇τ|² g*), g* = a0/κ, clipped at 200 kpc as KT28/KT29.

**The √6 is fixed, not fitted.** For a spherical field, τ = sqrt(2/3) |g' − g/r|. In deep MOND around a point mass
(g ∝ 1/r), τ = (2√2/√3) g/r and τ ∝ r⁻², so τ³/τ'² = τ r²/4. Setting ξ = κ r_M (KT28's calibration point) gives the constant √6.
(Beside: Newtonian point mass gives ξ = (2/3) g_N r / g*, about 6 % above KT28's (4√2/9).)

## Tests, lines unchanged from KT28 / KT29
Same code paths, with only τ swapped for the trace-free norm:
- **T0 Milky Way** (KT29's path: full tensor at (R0, 0) per in-prior cell, T_zz = ν(|g_N|/a0) 4πG ρ_b − T_RR − T_φφ, ∂_R τ by
  central difference over R0 ± 0.25 kpc; one ξ per cell). PASS if ≥ 1 in-prior cell passes L1, L2a, L2b, L3.
- **T1 Cassini** (KT28's path): Q2 ≤ 5.2e-27 s⁻².
- **T2 dwarfs** (KT28's path, 24 McConnachie dwarfs with the MW external field; τ from the internal field only): ≥ 15/24.
- **T3 SPARC** (KT28's path, smoothing of ln τ over 0.1 in ln r): d rms ≤ 0.005 and |median| ≤ 0.05.

**Label per footing: TRACE-FREE TIDAL RULE SURVIVES** if T0-T3 all pass; otherwise **FAILS** with the failed tests named.

## Expectation on record, not blind
- T0: with T_zz dominant, ξ_TF/ξ_full ≈ (√6 / (4/√3)) × 0.82 ≈ 0.87 if τ's log gradient is unchanged, i.e. about 32-46 kpc vs
  KT29's 37-53. KT17's ε = 1 (~10 kpc) already failed v_c. **Expect FAIL MW on both footings.**
- T1: outside matter τ_TF ≈ the full norm; expect PASS both, near KT28's factors.
- T2: inside a Plummer core g' → g/r, so τ_TF → 0 at the centre and ξ → 0 there (a uniform-density core has no trace-free
  tide). Direction on Fornax and the MW satellites not estimated.
- T3: rising, near-solid-body inner curves also give τ_TF → 0, so inner points get little smoothing; direction on the median
  not estimated.

## Beside, not graded
ξ_TF per MW cell (range, median) next to KT29's full-tensor and in-plane values; ξ_TF at (R0, z = 1.1 kpc) as KT29 did; per
dwarf ξ_TF(a) next to KT28's ξ_tid(a); the zero-crossings of τ_TF on SPARC (count of rows clipped at the floor).

## Checks
- R1: with τ swapped back to the full Frobenius norm and the constant to 4/√3, the scripts reproduce KT28's T1-T3 numbers
  and KT29's MW ξ range (to 1e-3 relative).
- R2: on a deep-MOND point mass (geomspace grid) ξ_TF / (κ r_M) = 1 to 1e-2.
- R3: on a uniform-density sphere τ_TF = 0 to 1e-6 relative to the full norm.
- KT29's C1, T1; KT17's C3 half-space factor is a known failure, disclosed if it recurs; C2 mass check printed.
- MUTATE (ν = 1) on T1-T3 as KT28.

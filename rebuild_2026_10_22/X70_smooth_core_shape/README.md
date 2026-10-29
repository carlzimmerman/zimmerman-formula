# X70_smooth_core_shape

**Question.** The external model proposed, and the owner relayed (10-29, "keep pushing"), replacing X43's Burkert halo with
the smooth core ρ = ρ₀/(1 + x²)^(3/2). It has zero central slope and the same r⁻³ tail. Criteria were frozen first
(190df89a83). The primary run re-derives η consistently from the new shape, giving η_S = 10.82, with no other change.

## Verdict (frozen): UNDECIDED: footings disagree

- **canonical: SC PASSES.** SPARC line on both backgrounds, all 15 cluster keys |Z| ≤ 2 in both h cells, and groups
  CONSISTENT. **This is the first full pass of the route-E core rule in the record.**
- **alt: SC FAILS on the SPARC line only.** rms is fine (0.0717 / 0.0731), but the median Υ is 0.47, below the line's
  0.50. Every cluster key and the groups pass on alt as well.

| | X43 (Burkert, η 14.83) | **X70 (smooth, η_S 10.82)** |
|---|---|---|
| SPARC canonical rms / Υ | 0.0782 / 0.77 | **0.0713 / 0.56** (A); 0.0720 / 0.55 (B) |
| SPARC alt rms / Υ | 0.0729 / 0.60 | 0.0717 / **0.47 (line FAIL)** |
| groups Z (canonical / alt) | +2.05 / +2.05 (FAIL) | **+1.94 / +1.88 CONSISTENT** |
| G-OUT-M3 Z (h 0.672) | +2.41 (FAIL) | **+1.88** |
| max \|Z\| over the 15 cluster keys, both h | 2.41 | **1.88** (G-OUT-M3 h 0.672); G-MID-T1 −1.71, G-MID-b +1.70 |
| G-IN-Mall | −1.18 | −1.29 |

**Reported (not graded):** the smooth shape with η kept at 14.83. Groups pass (Z +1.70), but G-MID-T1 and G-IN-Mall fail
OVER. The consistent η re-derivation is what keeps the inner keys in.

**Checks 9/9:**
- K0x43: the Burkert shape reproduces X43 exactly, max |d| = 0.
- K1 smooth: B_S against quadrature 2e-16; B_S(1) = 0.69707; η_S = 10.8203.
- MUTATE (Burkert kept) equals X43 exactly.

## Reading (careful)

- **Why it works.** A flat-topped core holds about 37 % more mass inside r₀ than Burkert at the same ρ₀ (B_S(1) = 0.697
  against 0.509). Two things follow:
  - Re-deriving η from the infall match lowers the collapse branch to 10.8.
  - At fixed mass and core Σ, the halo is re-arranged so the groups and heavy-cluster outskirts gain enough to pass, while
    the inner bands stay within 2σ.
  - The collapse branch is now inactive in every SPARC galaxy (all sit on the floor), and the fitted Υ falls to 0.47–0.56.
- **Thin margins:** groups Z 1.94 / 1.88; G-OUT-M3 1.88.
- **Known liability: f★ = 0.20.** CFG408 (ungraded) found measured stellar fractions move G-OUT-M3 by about +0.5 to +1.3
  in Z under X43. The same shift applied here would push it back over 2. This pass rests on X43's assumed stellar
  fraction.
- **The alt failure is Υ, not rms.** The line requires median Υ ≥ 0.50. On alt the SPARC rms is the best of any route-E
  variant, and the halo leaves too little room for stars.
- **Look-elsewhere.** The shape came from an external suggestion made after seeing X43's misses. Only this one alternative
  was frozen and run, but treat X70 as a LEAD, not an adoption. Adoption is the owner's call.
- **Still EXTERNAL:** c_f = 4. The native c_f(M) from the X48 A4 zooms (running) must be regraded with this shape.

κ = ½ FITTED; c_f EXTERNAL; not theory closed. Nothing here says the data favour the framework.

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x70_smooth_core.py`, `.out` / `_results.json`, `_MUTATE` versions, `x70_x30_machinery*.log`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x70_smooth_core.py            # ~95 s
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x70_smooth_core.py --mutate   # Burkert: equals X43

**ID note (added 10-29).** A parallel session also used X70 (X70_soft_floor_x0, a different test). Cite this lane by its
full directory name, X70_smooth_core_shape. The peer's X69_split_vs_cored_nfw found the split and cored-NFW reshapes fail
X-COP. Its note warns that further profile-shape variants risk becoming a knob scan. X70_smooth_core_shape is one such
variant, so read it as a lead with that look-elsewhere caveat.

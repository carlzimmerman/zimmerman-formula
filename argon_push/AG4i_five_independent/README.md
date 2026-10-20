# AG4i: the five clean positive-pull galaxies, independent kinematics and M/L gradients. Two are kinematic artefacts, M/L gradients explain none, one survives (UGC 731), two cannot be tested

- **Criteria:** `FROZEN_CRITERIA.md` (0b80250df). **Post-hoc addenda**, each committed alone before its run:
  `ADDENDUM_A1_POST_HOC.md` (88831e960) and `ADDENDUM_A2_POST_HOC.md` (1d3a4a262).
- **Settings:** κ = ½ fitted; not theory closed.
- **Runs:** all beside the live NC2x job under the owner's small-job rule. Peak memory was 0.91 GB, then 0.80 GB after a
  cutout-only pixel grid (same pixels, no number changed); 3–10 s each.
  - First run (frozen): `ag4i_firstrun.py` → `ag4i_firstrun_frozen.out/.json`.
  - A1 run: `ag4i_A1run.out/.json`.
  - A2 run, final: `ag4i.py` → `ag4i.out/.json`.
  - MUTATE: `ag4i_MUTATE.out`, exit 1. It bites: SPARC's own curve with β = 0 keeps |pull| ≥ 3 in all 17 variant slots.

## Results
| galaxy | AG4g pull | K: independent curve | M: M/L gradient (A2, β = 3.98) | K+M | class |
|---|---|---|---|---|---|
| NGC 5985 | +3.55 | GHASP: **+2.00, RESOLVED** (V_ind/V_SPARC 1.033) | +3.35, PERSISTS (m 1.00–1.19) | +1.95, RESOLVED | **KINEMATIC** |
| NGC 5023 (UGC 8286) | +3.70 | de Blok & Bosma: **+2.50, RESOLVED** (0.928) | +3.60, PERSISTS (m 0.99–1.05) | +2.40, RESOLVED | **KINEMATIC** |
| UGC 731 | +4.90 | de Blok & Bosma: **+5.00, PERSISTS** (1.080; 7 bins) | not available: the IRAC mosaic has no valid pixels at the galaxy | — | **UNEXPLAINED** |
| NGC 24 | +3.40 | none exists | +3.40, PERSISTS (m 0.92–1.02), but flagged K2-FAIL (the constant-Υ shape misses SPARC's Vdisk by 0.23) | — | NO VARIANT AVAILABLE |
| UGC 128 | +3.50 | none exists | not available: only 2 colour radii in the old-star range | — | NO VARIANT AVAILABLE |

- Every M variant (β = 2.99, 4.97 and −0.74) persists wherever M is available. The full table is in `ag4i.out`.
- The K results are frozen and graded: the first run's K numbers are identical in every later run, since K never uses the
  thin-disc code.

## What it means
- **Two of the five pulls are kinematic artefacts.** An independent rotation curve of NGC 5985 (GHASP Fabry–Perot) and of
  NGC 5023 (de Blok & Bosma long slit) brings each within the stellar-population Υ. The difference is a few per cent in V,
  enough to move the fitted mass-to-light ratio.
- **Radial M/L gradients explain none.**
  - Inside Meidt+2014's validity range the colour gradients imply m(R) of only 0.9–1.24.
  - The pulls stay at +3.35 to +3.60 under every slope variant.
  - This matches the paper's own remark that a constant Υ₃.₆ is "also feasible".
- **One galaxy survives: UGC 731 (DDO 9), a gas-dominated dwarf irregular.**
  - Two independent curves agree that it rotates faster than the law allows: SPARC's HI curve, and the de Blok & Bosma Hα
    curve, which is about 8% higher.
  - Its pull sits at the top of the Υ grid, so no reasonable stellar mass closes the gap.
  - AG4h already showed that distance and inclination cannot absorb it (shape-driven, Δχ² 101).
  - Caveat: the Hα curve has only 7 bins and a weak receding side. This is one candidate, for a dedicated test, not a
    detection. Being a dwarf with extra mass, it connects to the open faint-dwarf excess. That connection is noted, not
    tested.
- **Two cannot be tested with public data in hand.** NGC 24 and UGC 128 have no independent rotation curve.

## Disclosed failures and fixes
1. **First run (frozen):** the Hankel thin-disc code was numerically wrong. The added Freeman check failed at 183%; the
   multipliers went negative. Colours outside Meidt+2014's validity range (−0.15 < [3.6]−[4.5] < −0.02, quoted from the
   paper) were also fed to Eq. 4. The M results were VOID.
2. **A1:** exact elliptic-integral thin disc, and the colour-validity cut. K2a failed at 4.75% because the softening was too
   large (error ∝ ε/R, measured). M was VOID again, and no M number was produced.
3. **A2:** ε reduced tenfold, and a frozen gap closed: a K2 failure flags that galaxy's M. K2a passes at 0.93%. No M number
   was seen before A2.
4. **UGC 731:** its IRAC post-BCD mosaic has no valid pixels at the galaxy (all NaN within 50 pixels). The research agent's
   "covered" was footprint-level only.

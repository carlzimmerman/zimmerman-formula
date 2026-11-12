# CRACK-1 AMENDMENT A1 (post hoc, disclosed): R1's band's lower edge, and G3's graded line

Criteria 16bc0102de (committed alone, before any CRACK-1 script or number). This amendment is committed before any
CRACK-1 result is written. It changes two graded lines and no number, no prediction and no label.

## What the known answers found

KA4's synthetic **strip truth** — the 31 ultra-faints given f_C = 0.05, everything else on the law, noise free, on
the real points — puts the ultra-faints at d_L = -1.116 (canonical) / -1.130 (alt). R1's pre-registered band for
that class was **[-1.05, -0.30]**, so the reading's own truth falls *below* the band's lower edge and R1's G1 leg
FAILS on data in which the reading is exactly true. A test that rejects a reading's own truth is defective, not
strict.

The cause is a mis-derivation in the criteria, visible now and not before: the lower edge -1.05 was copied from
FRM1's band for the **tidal dwarfs**, whose X_L is about 5. The ultra-faints' X_L is about 35 — seven times larger —
so the same stripping factor moves them about three times further down in dex. Nothing in the criteria derived
-1.05 for this class; it was borrowed from a class with a different X_L.

## The amendment

1. **R1's ultra-faint band: the lower edge is the physical floor**, d_floor = -Y_L(g_bar) at the class's own field
   (-1.553 canonical, -1.590 alt), not -1.05. The upper edge, **-0.30**, is unchanged. The upper edge is the
   reading's actual claim — "the ultra-faints must be LOW" — and it is what the measurement is tested against. The
   reading's algebra allows everything from the floor up to -0.30, and the criteria should not have cut the bottom
   of that range at an arbitrary number.
2. **G3 grades the band-difference alone** (the Minkowski difference of the two pre-registered bands, which needs
   no central at all); the central is reported, not graded. Under the frozen line G3 also compared the measured
   differential with a central, and for R1 that central was the hand estimate -0.70, which the computed
   tidal-dwarf-calibrated central (-1.188 canonical) shows to have been 0.49 dex too generous.

## What it does not change

- Every other band, every prediction, every pass line, every label, and every known answer's requirement.
- **The verdict, under both lines, on both footings: R1, R2 and R3 all FAIL THE PAIR.** On the real data the
  frozen line and the amended line give the same three labels, because the measured offsets are above the bands'
  *upper* edges in every case. Both lines are in `crack1.json` (`G4_pair` and `G4_pair_frozen`).
- The hand estimates in the criteria's disclosure section: R2's central (-1.19 computed against -1.4 estimated) and
  R3's (-1.15 against -1.1) were close; R1's X-COP central is 0.000 exactly as pre-registered.

## Precedent

FRM1 (`fable52_push/FRM1_formation_theory/`) voided one clause its KA2 showed to be unsatisfiable and reported both
labels. DG1 (`closure_2026_11_10/DG1_dwarf_gas_history/`) carries an `AMENDMENT_A1.md` of the same kind. This lane
does the same and reports both lines.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

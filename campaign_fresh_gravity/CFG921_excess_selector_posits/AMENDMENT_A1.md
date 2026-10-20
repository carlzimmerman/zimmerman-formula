# CFG921 AMENDMENT A1 (2026-10-20, POST HOC): implementation findings from the K-stage, before MUTATE and the main run

**Status.** POST HOC. Written after the first K-stage runs and a calibration debug of the dwarf (calibrator) class. It is
committed alone, before either MUTATE run, before the main run, and before any non-calibrator class was compared or any class
was computed. FROZEN_CRITERIA.md (0abd82098) is unchanged; this file adds to it only where stated.

**What I saw before writing this:**
- the K-stage output;
- P5's disc correction δ (printed in the K-stage);
- the predicted DW class mean of P1–P4 at seven values of each posit's constant;
- P1's maximum DW class mean inside its equilibrium domain.

No z, fact comparison or class has been computed.

## A1-1 P5 numerics: method fix and an added check K7(d)

**Why.** The first K-stage run failed K7(b) at 1.0e-1. The cause was aliasing noise in the log-grid Hankel quadrature at high k.

**Fix (numerical method only).**
- Cell-exact kernels: the exact cell integrals of x J0(kx) dx and e^(−kz) dz.
- A low-pass window exp(−(k/50)²) on the phantom fields, which smooths the source on about 0.02 R_d. The same window is
  applied to the Newtonian in-plane field used in δ = ln(g_QUMOND/g_alg).

**Tolerances.** The frozen tolerances are unchanged, and all pass:
- (a) 1.3e-4 ≤ 1e-3;
- (b) 2.9e-3 ≤ 1e-2;
- (c) 2.7e-3 ≤ 2e-2.

**Added K7(d).** A razor-thin Kuzmin disc, whose exact QUMOND in-plane field is ν(|g_N(0⁺)|/a0)·g_N,R, must be reproduced to
≤ 3e-3. Measured: 1.3e-3. It is the strongest available check of the disc phantom path (surface term plus volume term).

**Physics note.** The δ comparator is the in-plane radial RAR relation, ν(|g_N,R|/a0)·g_N,R, which is how SPARC is fitted.
Even an exact QUMOND Kuzmin disc departs from it, because |g_N(0⁺)| includes 2πGΣ.

**Result seen in the K-stage.** ⟨δ_disc⟩ = −0.0214 (ν_e), so P5 predicts E = +0.0214 for spheres and point-mass lensing.

## A1-2 P1: calibration impossible in the frozen domain; an added diagnostic

**Finding.** The frozen rule requires every one of the 83 dwarfs to have an equilibrium: no runaway, w r12 g_bar < c_*².
Inside that domain P1's predicted DW class mean is at most ~0.006 (canonical), far below the observed +0.856. The runaway
threshold is set by a dwarf outside the graded cells. Under the frozen rule this is "calibration impossible", so P1 FAILS.

**Added diagnostic (no class weight): "P1 relaxed".** Equilibrium is required only for the dwarfs inside the graded DW cells.
The diagnostic reports:
- the relaxed c_*;
- the number and names of the dwarfs that run away;
- the DW χ²;
- the nominal z of every fact.

It shows whether the FAIL depends on the one excluded dwarf.

## A1-3 P3: non-monotone calibration curve; the lower root is graded

**Finding.** P3's predicted DW class mean rises with v_w to ~1.9 near v_w ~ 1e3 km/s and then falls. The locked phantom of
L× baryons vanishes once L·g_bar ≫ a0, because there is no phantom in the Newtonian regime. The curve therefore crosses the
observed mean twice.

**Rule.** The graded root is the LOWER one: the first sign change on the root-search grid. It is the branch continuous with
zero surplus. The upper root is reported as a diagnostic only.

**Grid.** The root-search grid is refined from 61 to 121 log points for every posit. Nothing else changes.

## A1-4 INJECT

- The interpolation table is restricted to the monotone branch of the DW-mean curve that contains the calibrated constant.
  K8 still passes: 5.6e-16 ≤ 1e-3.
- P1 has no calibrated constant on the real data, so it cannot be injected "from its nominal predictions". It is excluded. The
  INJECT requirement (FAILS ≤ 10%, SURVIVES ≥ 40%) applies to P2–P5 on both footings.

κ = ½ FITTED; footings never pooled; not theory closed.

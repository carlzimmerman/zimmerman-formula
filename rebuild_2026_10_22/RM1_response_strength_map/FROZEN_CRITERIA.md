# RM1_response_strength_map: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** UR2 found no halo mass offset δ that passes under the full adiabatic response. Several proposals (condensate response, phase-space cap, late disc assembly, disc geometry, bar torque) share one effect: they weaken the response, overall or inside the disc. Does **any** strength of that weakening, at any δ, clear the SPARC-side gates? This grades the effect, not each proposal.

The owner asked for the parameter space to be tested rigorously. This is an envelope, not a theory: f and δ are **FITTED** requirements, never derived. A cell found here gives what a mechanism would have to deliver.

**Disclosed before the freeze. Not blind.** UR1, UR2, LC1 and OP3 are read. UR2, Blumenthal: δ 0 gives Υ 0.35, tilt +0.16; off gives Υ 0.67–1.12, tilt +0.46 to +0.59. LC1 measured f_Q 0.872 [0.54, 1.07] for a smooth disc in a live zoom, gravity only.

**Expectation on record, mine.** No cell in family G: tilt wants a strong response and Υ a weak one. Family I is less clear; I expect no cell, without confidence.

## Runs
UR2's path and table unchanged: NR1 PRIMARY's η, f★ 0.034, canonical, both backgrounds, EM1 + δ, Blumenthal.

δ from −0.30 to +0.25, step 0.05, 12 values. With M₀ the unresponded cold mass and M_c Blumenthal's:

M(r) = M₀ + f(r) (M_c − M₀), then made non-decreasing in r.

- **Family G (global):** f(r) = f, for f = 0, 0.1, …, 1. 132 cells.
- **Family I (inner decoupling):** f(r) = f_in inside r_h, rising to 1 at 3 r_h, smoothstep in ln r; r_h is the radius holding half the baryon mass passed to the response. f_in = 0, 0.25, 0.5, 0.75. 48 cells. For an exponential disc r_h is about 1.7 R_d, so this frees the region r < 3–5 R_d.

## Gates, each cell
1. Υ 0.50–0.80, rms ≤ 0.110, on both backgrounds.
2. |tilt| ≤ 0.15, both backgrounds.
3. Groups verdict CONSISTENT.
4. |LITTLE THINGS median E| ≤ 0.10, both backgrounds.
5. δ inside blue lensing's 2σ range, −0.10 to +0.14, read across from BL1, not regraded.

## Labels
- **NO CELL:** none clears all five in either family. Weakening the response in these forms does not close the SPARC side on this path.
- **CELLS IN I ONLY / CELLS IN G:** name them, with the f required, and compare with LC1's band. Not a pass: keys, X-COP, KiDS's own grade, Local Group and MW remain, and no mechanism is derived.
- **[NOISE-LIMITED ANCHOR]:** NR2 is unread, so any label holds on NR1 PRIMARY only. Rerun when NR2 lands.

## Reported, not graded
Tables of each gate over the grid; the cell failing the fewest gates; Υ by V_flat at that cell. 15 keys and X-COP at each f (δ doesn't enter them), on UR1's path, with its gas inputs as they are.

## Limits, stated now
One-parameter forms only: no mass-dependent f, whose breakpoint would add a fitted number. Bars, feedback and geometry aren't simulated. A NO CELL doesn't exclude a form outside these two families. Cores by hand, as UR2.

## Checks
K1 f 1, δ 0 equals UR2's Blumenthal row, |d| ≤ 10⁻⁶. K2 f 0, δ 0 equals UR2's off row for Υ, rms, |d| ≤ 10⁻³. K3 f 0.5, δ 0 differs from both ends. Rerun byte-identical on the read. MUTATE: f replaced by 1 − f, K1 fails, exit 1, separate outputs.

One thread each, nice 15, under 1 GB, beside NR2. κ = ½ FITTED, unused; no a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

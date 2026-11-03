# KT27_local_rule_alt_grade — FROZEN CRITERIA (before any script or number beyond KT26's printed Part D)

Owner, 2026-11-03: grade KT26's local, mass-free filter rule on alt, where it passed the Milky Way screen (30 cells), on the
other three tests: Cassini, the 24 dwarfs, SPARC.

κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. No
download.

## The rule, applied position by position
ξ_loc(r) = |g(r)|² / (|d|g|/dr| g*), g* = a0 / κ (KT26). Here it's applied **row-wise**: the smoothed density (or enclosed
mass) at radius r uses a Gaussian of width ξ_loc(r), the width taken at the point where it's evaluated. This is a
position-dependent filter, closer to the local rule than KT26's one value at R0. It isn't a convolution, so total mass isn't
conserved exactly; the mass ratio is printed, not graded. |g| is the **unfiltered board-law field** of the system (simple ν on
the Newtonian field, the external field added in quadrature where the system has one), not iterated to self-consistency.
Stated. ξ_loc is clipped at 200 kpc (dwarfs, SPARC) and 1e4 r_M (Cassini) where |dg/dr| → 0; beyond those, the phantom is
already gone at that radius.

## Tests and labels (alt is the graded footing; canonical printed beside, it already failed KT26's MW screen)
- **T1 Cassini:** KT16's integral (`qcas`) with the point-mass smoothed field gh_pt(x, ξ_loc(x)) row-wise, ξ_loc from
  |g| = ν(sqrt(ĝ_N² + η²)) sqrt(ĝ_N² + η²), ĝ_N = 1/x², η = 2.32e-10 / a0. Pass if Q2 ≤ 5.2e-27 s^-2 (KT16's ceiling).
- **T2 dwarfs:** KT15's model (24 McConnachie dwarfs, Plummer, Υ grid 1-3, MW field for MW satellites only) with
  `smooth_sph` row-wise at ξ_loc(r) from the dwarf's own board-law field. Pass if ≥ 15/24 (KT25's line; plain QUMOND 15/24).
- **T3 SPARC:** KT19's code (Υ 0.5/0.7, quality cuts, spherical smoothing approximation) with ξ_loc(R) row-wise from the
  board-law curve of that galaxy at f = 1 (no observed-curve derivatives). Pass if d rms ≤ 0.005 and |median| ≤ 0.05 (KT25's
  lines).

**Label (alt): LOCAL RULE SURVIVES ON ALT** if T1, T2 and T3 all pass (KT26's MW screen already passed on alt);
**LOCAL RULE FAILS ON ALT: <tests>** otherwise. Canonical gets the same three rows and the label **already FAILS (MW, KT26)**
plus whatever fails here.

**Expectation on record, not blind:** KT26 Part D printed ξ_loc 189 r_M at Saturn and 3.0 r_M at r_M (Newtonian internal
field), so I expect T1 to PASS; it printed ξ_loc about 3x KT25's for a Fornax-like dwarf, and KT15 showed too much smoothing
hurts the dwarfs, so I expect T2 to be at risk. T3 is open: inner, high-g points get large ξ_loc (ξ_loc ≈ r g/(2 g*) in the
Newtonian regime), so inner phantom drops.

## Checks
- R1: with ξ forced to the constant 0.5 r_M, the row-wise code reproduces KT25 (Cassini 0.481 / 1.06 x ceiling, dwarfs
  15/24 both footings) and KT25_sparc's d rms (+0.0021 / -0.0006) to the printed digits.
- R2: ξ_loc for a point mass in the deep limit equals κ r_M at 100 r_M within 1e-3 (KT26 B1 again, on this code's field).
- MUTATE: ν = 1 (Newton) everywhere; Cassini Q2 must be 0, SPARC must fail.
- Beside, not graded: ξ_loc ranges per test; dwarf count with ξ_loc at r = a only (one value per dwarf).

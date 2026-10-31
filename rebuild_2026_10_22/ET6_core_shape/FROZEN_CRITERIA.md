# ET6_core_shape: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Every S in ET1–ET5 is defined through one core, ρ = ρ₀ (1 + x²)^(−3/2). Does the low-mass rise, and ET5's verdicts on the flat floor, depend on that choice? Standing: κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework or either footing.

**Seen before freezing.** ET1–ET5 tables for the base core. X70's record that Burkert and cored NFW fail under route E's other keys. No fit of these shapes to the free S, r₀ statistic has been computed.

**Shapes, M(r) = π S r₀² B(x), S = ρ₀ r₀, x = r/r₀.**
- SMOOTH (base): B = 4 (asinh x − x/√(1+x²)); outer ρ ∝ r⁻³.
- BURKERT: B = ln(1+x²) + 2 ln(1+x) − 2 atan x; outer r⁻³.
- PISO, ρ = ρ₀/(1+x²): B = 4 (x − atan x); outer r⁻².
- STEEP, ρ = ρ₀/(1+x²)²: B = 2 (atan x − x/(1+x²)); outer r⁻⁴.

**Comparing S across shapes.** r₀ means something different in each shape, so S is not one physical number. Two gradings, both against the same floors (106.85, 129.13):
- PRIMARY: fitted S, taking the rule S = ρ₀r₀ literally in each shape.
- NORMALISED: S × B(1)/B_SMOOTH(1), equal halo gravity at r₀.
Whether route E's floor carries over to another shape at the same value is a choice stated here, not derived.

**Base and grid.** As ET5: same sample, grids, mse, rise statistic, intervals, trend, pressure, beam cut; 18 cells per shape. SMOOTH is ET5's and is not rerun except for K1.

**Fit guard, frozen now.** A shape counts toward a verdict only if its median per-galaxy best mse below 150 km/s at s 0, σ 0, no cut is at most 1.5 × SMOOTH's. Otherwise it is reported as POOR FIT and cannot reconcile. The mse ratio is reported either way, and reading a better fit as evidence for a shape is not part of this lane.

**Verdict per footing, over counted shapes, on PRIMARY.** A cell is RECONCILED as ET5: all three intervals contain the floor and rise p ≥ 0.01.
- **SHAPE EXPLAINS IT** if any cell with s ≤ 0.25 is RECONCILED.
- **SHAPE EXPLAINS IT ONLY BEYOND THE BAND** if only s = 0.5 cells are.
- **FLOOR CONSISTENT, RISE REMAINS** if a cell with s ≤ 0.25 contains the floor but none is RECONCILED.
- **NOT RECONCILED** otherwise.
The same is computed on NORMALISED. If the two differ, the line reads DEFINITION-DEPENDENT, and both are given.

**Rise per shape.** RISE IS SHAPE-FREE if at s 0, σ 0, no cut all counted shapes give ρ > 0 at p < 0.01, else SHAPE-DEPENDENT, listing them.

**Forward.** Truth: each non-base shape, flat S at each floor, r₀ from M200 through that shape. Cases: no systematics; and s 0.25, σ 12, 30″. Fit with SMOOTH at Υ 0.50 with no correction, as the real data were fitted in ET2. FAKED / PARTIAL / NOT FAKED by ET3's rule: 12 cases.

**Reading, declared now.** A pass with these extra shapes shows that the choice of core can absorb the rise at generous settings, and not that a shape is correct. X70's failures elsewhere stand and are not re-graded. NOT RECONCILED across shapes would mean the rise against canonical's floor does not rest on one core choice, still within these four shapes. That identifies no mechanism and is not a rejection of route E.

**Checks.**
- K1: SMOOTH at the base cell equals ET2 per galaxy.
- K2: each B equals numerical integration of its density to 1e-6 at x = 0.1, 1, 10.
- K3: with each shape, solve_r0 returns r₀ whose M(R200) equals M200 to 1e-8 on three galaxies.
- K4: on-grid plant with each shape returns exactly.
- MUTATE (`--mutate`): truth BURKERT flat at the canonical floor, fit with BURKERT, separate outputs: medians within 98–118 and p ≥ 0.01, or exit 1.

**Limits declared now.** Four shapes, not a general family. Beams bracketed; h = Rdisk; σ constant; one-parameter trend; same as ET5. Multiplicity favours reconciliation, on purpose. Single-threaded, small job.

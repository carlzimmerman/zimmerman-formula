# ER1_energy_to_undo: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** The zoom's own shape plus LC1's measured response over-masses L★ galaxies. If something Newtonian undoes it, how much must be undone in each mass bin, and can measured stellar and black-hole energy pay for that with one coupling? This scores the energy route only. It doesn't touch RM1 (response strength map, another session's lane), which grades strength against δ without an energy budget.

**Disclosed before the freeze. Not blind.**
- OP3, native shape, EM1, frozen map: f_Q 0: Υ 1.20, 1.20, 0.97, 0.57, 0.67, 0.78 by V_flat. f_Q 0.872: 0.55, 0.69, 0.57, 0.32, 0.40, 0.53; overall 0.84/0.81 and 0.44/0.41.
- CN1, on the smooth core: full undo costs 0.043, 0.070, 0.100, 0.125 of E_SN at 100–400 km/s, so energy was not the limit there. CM1: gravity-only delivery about 0.3 % of E_SN, 30× short.
- UR3: Milky Way, NFW start, passes with no response and fails with it.
- NR2's headline is known (N passes the line, noise-limited). Not used: this lane runs on OP3's native shape.

**Expectation on record, mine.** Budget is not short at coupling 1; I expect SN alone to pay. Required f is V-shaped: dwarfs keep nearly all the response, 150–200 km/s loses most, 250–400 little. Energy per binding is largest in dwarfs, so one coupling undoes dwarfs first, which is the wrong order. So: **WRONG SHAPE**. I said earlier this could close the route "on energy grounds"; I now expect the amount of energy to pass and the pattern to fail.

## Runs
OP3's path unchanged: `zn2_low_shapes.json`, EM1, frozen map, X39's Blumenthal, M_f = M₀ + f (M_contract − M₀). Canonical, both backgrounds.

**Part 1, required f.** f = 0, 0.1, … 0.7, 0.872, 1. Per V_flat bin, background A: f_req(Υ) = largest f on the grid, by interpolation, with bin Υ ≥ 0.50, and also at 0.65. Bins below 0.50 at f 0: none. Bins above at f 1: nothing to undo.

**Part 2, energy.** Baseline is LC1's f 0.872. Energy to reach f: E(f) = max(0, [W(M₀ + f ΔM) − W(M₀ + 0.872 ΔM)] / 2), with CN1's W, which includes baryons. Υ 0.50. Budgets: E_SN = (M★/100) × 10⁵¹ erg; E_BH = 0.1 × 0.005 M★c². M★ = Υ L₃₆. ε_req = E(f_req) / budget, median per bin, SN alone and SN + BH. These are minimum virial costs at perfect delivery: **a lower bound on the cost, BY HAND**. 

**Part 3, one coupling forward.** Each galaxy, each Υ: f = the lowest in [0, 0.872], on a 21-point grid, with E(f) ≤ ε × budget. ε = 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, SN and SN + BH. ε is **FITTED**. No threshold and no mass dependence beyond the energies.

## Labels
- **BUDGET SHORT:** ε_req > 1 at SN + BH in any bin at Υ 0.50.
- **ENERGY RULE HOLDS AT ONE FITTED ε:** some ε in Part 3 gives Υ 0.50–0.80, rms ≤ 0.110 both backgrounds, |tilt| ≤ 0.15. SPARC only; clusters, groups' response, KiDS and Local Group not graded, so never a pass.
- **WRONG SHAPE:** budget suffices, no ε passes. Name the gate and which bins are undone in the wrong order.

Reported: Υ and ΔV by bin along ε; groups Z, uncontracted as OP3.

## Checks
K1 f 0 and f 0.872 reproduce OP3's overall Υ, rms and bins, |d| ≤ 0.005. K2 E(0.872) = 0 exactly. K3 forward at ε → 0 equals f 0.872. K4 forward at ε 10³ equals f 0. MUTATE: budget × 0.01 moves the result.

Limits: no mechanism is named. A real outflow removes gas too, which changes the baryons; held fixed here. Energy delivered to the cold fluid is unproven (CM1). One thread per run, nice 15. κ = ½ FITTED, unused. No a₀ in the halo. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

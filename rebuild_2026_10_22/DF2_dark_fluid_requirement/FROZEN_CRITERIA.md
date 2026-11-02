# DF2_dark_fluid_requirement: FROZEN CRITERIA, committed alone before any script or number

Launched under the owner's 2026-11-02 instruction to launch search lanes without asking. DF1 is taken (dwarf floor), so this is DF2. A requirement map, not a model: it adopts nothing, reinstates no retired sector, and proposes no field. The term studied is called the dark fluid term. κ = ½ FITTED, and a₀ is absent from linear FRW, so footings share the surface. Raw channels, no ΛCDM input in a grade. Not theory closed. Nothing here says the data favour the framework. A family statement on these inputs, not a no-go theorem.

**Not blind.** Known before this file: RF5's dust cell S_min 2324.03; VW1's Fermi-Dirac bound (passes at v0 <= 2 km/s, fails at 4); BOLTZ1 (shift-symmetric P(X) has no turn-on, its dust limit passes, forest bound c_s <= 6 km/s at z 3 from X22); DF1's polytrope ladder for faint dwarfs; X19, J1, X60 on selector variables; CFG938's medium conditional and ill-posed on FRW. **My expectation on record:** a density-keyed exclusion anchored to discs fails at every Γ, by being stiff at recombination for Γ >= 1 and stiff in today's background for Γ < 1. Order-of-magnitude only.

## Question
What w(a), rest-frame c_s²(a) and c_vis²(a) does gate 1 allow for the term that plays dust at recombination? And can a barotrope that holds the term out of discs live inside that bound?

## Method
CLASS, RF5's source tree copied outside the repo, patched only for this term, X34 unset. Newtonian gauge, because synchronous gauge defines itself by this species. With w constant:
- δ' = −(1+w)(θ − 3φ') − 3aH(c_s² − w)δ − 9(1+w)(c_s² − w)(aH)²θ/k²
- θ' = −aH(1 − 3c_s²)θ + c_s²k²δ/(1+w) + k²ψ − k²σ
- σ' = −3aHσ + (4/5)c_vis²θ. Normalisation chosen so 4/15 x 3c_vis² matches the neutrino truncation; other papers' c_vis differs by order unity, stated.
- ρ ∝ a^(−3(1+w)), p = wρ. δp and σ enter the Einstein equations. c_s = c0 a^(−N), optionally only inside a redshift window, with a tanh edge of width 0.05 in ln a. c_vis likewise. Barotrope cells set c_s only: their w from c_s is neglected, a stated simplification, and their adiabatic initial δ isn't corrected for w.
- Everything else: RF5's channels, precision, fit, and HF1 A1 R2's line: G-CMB, G-BAO, G-SN, G-SHEAR at p >= 1e-3, G-A0 in CFG689's band, S − 2324.03 <= 25.

## Grid, fixed now, km/s today unless said
- **A, scaling:** N = 2: c0 0.25, 0.5, 1, 2, 4. N = 1: 0.5, 1, 2, 4, 8. N = 0: 3, 10, 30, 100, 300. N = −1: 10, 30, 100, 300, 1000.
- **B, by epoch, c_s constant inside one window, 0 outside:** z > 3000; 3000-500; 500-50; 50-5; z < 5, each at 10, 100, 1000.
- **S, late switch:** on for z < 50: 10, 30, 100, 300.
- **W, small w, c_s 0:** ±1e-3, ±3e-3.
- **V, viscosity, c_s 0:** N = 0: c_vis 3, 10, 30, 100. N = 2: 0.5, 2.
- **P, barotropes anchored to discs:** P ∝ ρ^Γ, so c_s² ∝ a^(−3(Γ−1)), N = 1.5(Γ−1). c_s = σ at ρ_disc = 0.05 Msun/pc³, where σ is 30 or 100 km/s: the speed needed to hold the term out, comparable with a disc's dispersion and its circular speed. ρ today = 3.3e-8 Msun/pc³ (omega 0.12). Γ = 7/3, 5/3, 1, 2/3, 0. Γ = 0 is the Chaplygin-like end; its P isn't increasing, stated.

## Two stages
1. **Screen,** at RF5's dust-cell parameters, all cells: S at fixed parameters. A cell that stops or takes over 1800 s reads UNDETERMINED.
2. **Fit,** RF5's fit: for each family and scaling, the largest cell passing the screen and the next one up; every P cell with screen S − 2324.03 <= 2000; every W cell. A screen read is never a pass. Only a fit grades.

## Reads
- Largest passing c_s in each epoch window and each scaling, as a range between grid points.
- P(k, z = 0) to the c_s = 0 cell, k where it halves. X22's forest bound beside it, unchanged, no forest verdict.
- **Analytic half.** Printed: mean ρ at z 1100, z 3000, z 0 against a disc's. Each P cell's c_s at z 1100 and z 0 against the bound. For the variables left (acceleration, density gradient, entropy, phase density): value at recombination, in a disc, in a cluster, with its assumptions, and which standing kills already reach it (X19, J1, X60, VW1). The Bullet and CL5's kills on pressure fluids are reported from the record, not re-derived.

## Labels
- **DENSITY KEY FAILS GATE 1**: every P cell with a screen or fit read fails, at both σ, none UNDETERMINED by fit. Family: single-barotrope P ∝ ρ^Γ at these Γ.
- **DENSITY KEY PASSES GATE 1 AT Γ**: a P cell passes by fit. That says only that one gate holds. Discs, clusters, the Bullet and structure stay ungraded, and no action is offered.
- **NOT DETERMINED**: otherwise.
- The map's other reads carry no pass label. They're ceilings.
- Any failed control: NO VERDICT.

## Controls
- c_s = 0, Newtonian, patched build at RF5's dust-cell parameters: plik, BAO, SN, shear each within 1.0 of RF5's cell.
- Patch off versus patched with w = 0, c_s 0, c_vis 0: same build, plik identical within 0.01.
- Jeans: N = 0, c0 30: k where P halves against the k_J = a sqrt(4πGρ)/c_s at z = 0, within a factor 3. Rough by nature.
- Fluid against VW1: N = 2 at c0 = 2 printed beside VW1's FD at v0 = 2, no line. Different physics; reported.
- MUTATE: sign of the c_s²k²δ term flipped at N = 0, c0 30 must move plik or stop CLASS. Separate outputs.

## Rules
Post-result changes go in an amendment, disclosed as such. No data downloads. Nice 10, one thread per fit, at most two jobs at once. Delete nothing of other lanes. Disk about 19 GB free; the patched copy is 29 MB, and work files are cleaned as RF5 cleans.

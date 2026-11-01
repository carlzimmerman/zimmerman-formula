# Audit: does the forest kill of the 5–11 eV fermion corner hold? 2026-11-01

Read-only, on the owner's request. No new run, no new lane, no adoption. The standing no-particle rule is unchanged, and this family stays out of the theory. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## Verdict: KILL NOT ON THE CURRENT FOOTING, NOT OVERTURNED

The statement "the 5–11 eV sterile-fermion corner dies on the forest" (`STANDING.md`) is stronger than its calculation supports under today's rules. The calculation gives a large warning, not a graded failure on forest data. Nothing here shows the corner passes, and it has other liabilities that don't involve the forest.

## What the kill is
`qwen_claude_field_theory/closure_2026/condensate_pincer_2026/mond_sheet_nbody_forest_gate_2026.py`, 2026-09-02, a 1-D MOND sheet N-body. Reported: unfloored MOND lifts k = 1–10 h/Mpc power by 100–1000 × over Newton by z = 3, and "still falls 1000-5000x short" of the yardstick. `dark_sector_debug_2026` then lists the corner as FAIL on forest, sheet N-body and Hubble floor.

## What's wrong with it as a kill
| # | Finding | Evidence in the script or output | Class |
|---|---|---|---|
| 1 | **The yardstick isn't forest data.** No flux, no Lyman-α spectrum. It's the 1-D power of ΛCDM's linear field, labelled "the measured clustering" | docstring | fails today's raw-data rule (10-25) |
| 2 | **ΛCDM background and amplitude.** ω_c 0.12, h 0.674, σ₈ 0.811 | constants at the top | fails the same rule |
| 3 | **It doesn't contain the fermion's clustering.** Dark component "smooth (it contributes to H(a) only)"; the force sums baryons only. The output itself says the neutrinos carry k ≲ 0.4 h/Mpc in the hybrid, so its large scales "are not the hybrid's". So this tests baryons in a smooth universe, not the hybrid | docstring, `accel`, output | scope. Sign of the correction not computed: deeper wells would help, and a stronger external field would throttle the boost |
| 4 | **1-D.** Its own caveat says 1-D growth isn't 3-D growth and it decides the qualitative question. Its docstring says three linear treatments spanned ten decades | docstring | scope |
| 5 | **Forest treated asymmetrically.** The forest is out of every verdict for the framework's own models: P1D4 NOT DIAGNOSTIC (1864.2/690), RF5 NOT DIAGNOSTIC, BOLTZ1 424.0/327 on plain early dust. It is still used as the kill here | those READMEs | inconsistency in the record |

## What survives, checked as hard
- **Finding 5 is not a rescue.** Those misfits are model inadequacy at the level of a χ² excess. This shortfall is 1000–5000 × in power, about 30–70 × in amplitude, and proxies are unlikely to cover all of that. It's a serious warning.
- **The physical concern stands:** dark power is erased below free-streaming, and something must supply it by z ≈ 3. No calculation on record shows MOND on baryons doing so with the fermion's wells present.
- **Its other liabilities, none involving the forest:**
  - Thermal production is dead on N_eff, so it needs a non-thermal origin, which has no mechanism (`ballistic_survivor_window_2026.out`). NU1's N_eff line is words only, PROVISIONAL.
  - The record says the one published N-body overproduces massive clusters (same output, citing Angus, Diaferio, Famaey, van der Heyden 2013). Not re-read in this audit.
  - NU1: a gas-tracing sterile component that closes MID pushes OUTER to Z −6.9 to −7.8. That's at lower masses and under a gas-tracing assumption, so it's indicative for this corner, not decisive.
  - The same output calls it what it is: a particle, and dark matter in every sense except in galaxies.
- **It wouldn't satisfy the requirements list.** It stays out of galaxies, so galaxies run on the law alone, and it carries the law's failures: Milky Way K_z +4.7 to +6.6σ and IC 1613. A component excluded from galaxies can't remove mass. Its reach is rows 4, 9 and 11, and possibly 10.

## What would decide it
A 3-D MOND run with the fermion's clustering included, the native a₀(z), and a forward model of raw P1D. That's a heavy lane, and the survivor window's output already names it as never run. **Not opened.** It would need the owner to lift the no-particle rule, which isn't recommended here on this evidence.

## Recommended record change
Quote the corner as: "undecided on raw forest data; a 1-D proxy against a ΛCDM yardstick falls 1000–5000 × short; other liabilities stand; outside the no-particle rule." Carry that line in the closing ledger. `STANDING.md` is left as it stands until the owner asks for a dated correction.

κ = ½ FITTED. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.

# CP1_complementarity_phase_closure: NOT DECIDED as frozen, because K4 failed. Inside that: galaxies FAIL on Υ, clusters X-COP ONLY, forest FAIL, and the reading that passes SPARC counts the cold twice-weighted

Criteria: `FROZEN_CRITERIA.md` (c2c9e1ce67), committed alone first. `cp1.py`, `cp1_tail.py`, `cp1_bl1.py`, `cp1_field.py`, `cp1_grade.py`, `CP1Bounds.lean`; outputs `cp1.out`, `cp1_results.json`, `cp1_*_results.json`, `cp1_bl1.out`. UR1, SL1, NR2, BL1 read only. **V_crit 250 km/s and n 4 are CHOSEN, not derived.** **This breaks the owner's 10-31 no-a₀-in-cold-sector rule at the mix, on purpose.** A pass wouldn't have lifted that rule. κ = ½ FITTED. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind.**

The proposer's Ω_m = f_b(1 + R_nat) = 1 is wrong: that product is 1 by identity, so it's no matter density. Used here: Ω_m 0.3129 (A), 0.2976 (B).

## Rule graded
g_tot = χ_pol g_pol + χ_clust g_b + G M_f[χ_clust M_c0]/r² (R1), χ_clust = 1 − χ_pol, χ_pol = [Ω_DE(z)/Ω_DE(0)] exp(−(V/V_crit)⁴). EM1's line, N's core, NR2's medians.

| Row, canonical | Υ A/B | rms A | tilt | Groups Z | LITTLE THINGS A | Galaxy block |
|---|---|---|---|---|---|---|
| **R1, PRIMARY** | **0.43/0.43** | 0.0543 | +0.150 | +0.69 | −0.025 | **FAIL, Υ only** |
| R2, cold weight χ²_clust, reported | 0.53/0.53 | 0.0601 | +0.030 | +1.33 | −0.025 | passes |
| R3, full-mass contraction, then weighted, reported | 0.47/0.47 | 0.0536 | +0.110 | +0.68 | −0.025 | FAIL, Υ |
| R1, NR2 LOW / HIGH | 0.43 / 0.43 | 0.0544 / 0.0543 | +0.150 | +0.69 | −0.025 | FAIL, Υ |
| R1, alt footing | 0.39/0.39 | 0.0570 | +0.050 | not run | −0.064 | FAIL, Υ |
| V_crit → ∞ (law) | 0.52/0.52 | 0.0541 | +0.020 | +0.31 | −0.025 | passes |
| V_crit → 0 (EM1 + Blumenthal, NR3) | 0.35/0.36 | 0.0670 | +0.170 | +1.50 | +0.116 | FAIL |

Υ by V_flat, R1: 0.415, 0.61, 0.59, 0.35, 0.395, 0.49. Tilt sits exactly on the record's 0.15 line, so it counts as passing. The proposer's looser 0.20 changes nothing. LITTLE THINGS clears the proposer's 0.055 on canonical, not on alt (−0.064). 40 SPARC objects have no V_flat and use the fallback.

**Sensitivity, report only:** no R1 row passes at V_crit 200–300, n 2 or 4. Υ runs 0.38 to 0.45.

My expectation was wrong on SPARC: I expected the line to pass. The 150–250 km/s bins are what hold Υ down, the same bins NR3 found stuck, and at V 150–250 χ_pol is 0.88 to 0.37, so the halo isn't gone there.

## Frozen label
**NOT DECIDED (GALAXIES FAIL line; CLUSTERS X-COP ONLY; FOREST FAIL [READING-DEPENDENT])**

## Why NOT DECIDED: K4 failed, and the failure is a finding
K4 required cluster predictions unchanged to 1e-6 with the mix on. They moved by 0.034. The premise "χ_pol ≈ 0 for clusters" is false in the catalogue's low-gas tail: **37 of 326 clusters have χ_pol > 1e-3**, all in the lowest gas tercile, smallest V200 84 km/s on the gas budget (Mgas500 3.5e10, χ_pol 0.99). That V200 comes from the budget, not from a measured speed. The other two terciles: smallest V200 683 and 921, χ_pol under 1e-24.

Effect on the Z's, on the N + Blumenthal path: largest |ΔZ| 0.06, G-OUT-M3 and G-OUT-M2 unmoved, no key crosses a line. So ZN4's cap almost certainly stands (12 of 15, G-OUT-M3 +4.41, carried, not recomputed: the mix on the native path was not run), but the frozen check isn't met, and I'm not amending it after the result.

Second cluster row, N + Blumenthal at χ_clust = 1 in this harness: 14 of 15, G-IN-Mall −2.05, X-COP −0.097, 0.146 FAIL. Also not a pass. ZN4 has no contraction, and native + contraction stays ungraded.

## R2: checked as hard as a fail, after the result, not selectable
R2 passes the block at MEDIAN, LOW and HIGH, and at all but one sensitivity row (200, n 2: tilt +0.19). It's the literal-looking text (1 − χ_pol) g_halo with g_halo built from χ_clust M_c0. But:
- It counts cold at weight χ²_clust, which matches no source term. Neither ρ_b + χ_clust ρ_c nor the uncontracted limit gives it.
- On alt it fails: Υ 0.45/0.45.
- It was frozen as report only.

So the galaxy result depends on an ambiguity in the rule's own wording. The proposer has to say which reading is meant, with a reason. Picking R2 because it passes would be a fit.

## Other gates
- **z = 3 forest, V 150:** χ_pol 0.0424 (A), 0.0445 (B), line 0.03. **FAIL** both. Hand reading 0.044 confirmed.
- **BL1 blue lenses, R1, reported:** canonical A 0.898 ± 0.076 consistent, χ² 26.1. Alt A 0.835 ± 0.070 **between**, χ² 34.98. The proposer's χ² ≤ 35 passes both, alt by 0.02. BL1's class passes canonical only. Law 27.5 / 43.3, route E 109.2 / 110.5. All lenses χ² 137.1 / 106.4, against the law's 78.7 / 42.2, so the mix is **worse than the law on the full stack**. Red 192.5 / 164.7 against 136.7 / 94.8. Halo is N, sigma table BL1's; lens V is stipulated from a₀; EFE off.

## Where the cold mass goes
The rule doesn't say. By V bin, canonical, A: χ_pol 0.999, 0.990, 0.960, 0.798, 0.548, 0.179. Remaining cold / M_b 0.02, 0.18, 0.65, 2.6, 5.6, 9.4. At V under 60 km/s, 99.9 % of an object's cold mass isn't in g_tot, and 54 % of the sample's summed M200 is gone. Nothing carries it: no phase, no conversion, no conservation statement. X60's R0 and PH1 are the record on what happens when something is asked to hold it. The fit gets this for free, and that's the rule's biggest gap.

**A dwarf inside a cluster has no defined V_sys.** V 50 gives χ_pol 0.998; the host's V200 1000 gives about 1e-111. The rule picks neither. Same for satellites and TDGs. The key is non-local and per-object, so it isn't a field theory as written.

## Notes
**(a) Earlier proposed field equation,** ∇·[(1 + χ_pol/√(1 + |∇Φ|²/a₀²)) ∇Φ] = 4πG(ρ_b + χ_clust ρ_c), at χ_pol = 1. Hand reading confirmed numerically: g/(g_b/2) = 1.000000 at g_b 1e-4 a₀, g/(g_b − a₀) = 1.000000 at 1e4 a₀, g/√(g_b a₀) 0.005 at 1e-4 a₀. Plummer divergence residual 4e-6. So it weakens gravity, the opposite of the law, and gives no flat rotation curves. It isn't the rule graded here, and no action for this rule exists.

**(b) `CP1Bounds.lean`** compiles under the local toolchain (Lean 4.34.0-rc2, core only). It's algebra about stipulated bounds on a mix. It proves nothing about galaxies.

## Checks
K0 harness vs NR3 MEDIAN 0, predictions 0. K1 law limit 2.6e-8, alt 1.7e-8. K2 V_crit → 0 2.8e-17, groups 0. K3 0. **K4 FAIL, 0.034.** K5 BL1 law limit 0, K6 BL1 route E 1.0528. MUTATE χ_clust = 1 with χ_pol > 0: Υ 0.43 → 0.30, rms 0.054 → 0.174, LITTLE THINGS −0.266, BL1 blue A 0.898 → 0.524, BITES.

**Disclosed fixes.** (1) My first K4 took the innermost density crossing for R200. I changed it to the outermost; the number stayed 0.034, so the fail isn't that. MEDIAN rerun, all other results identical. (2) A float, tilt 0.15000000000000002, first printed as a fail; `cp1_grade.py` rounds at 1e-9. (3) R2's alt, band and sensitivity runs, and the K4 diagnosis (`cp1_K4_results.json`), came after the result.

## Limits
Contraction is Newtonian, ignoring the g_pol share. EM1's line isn't refitted under the mix. χ at z = 0 for lenses and clusters. Not run: KiDS beyond BL1, Local Group, MW, growth, IC 1613. At V under 100, χ_pol is above 0.97, so X58's law-side dwarf fails (MW ultra-faints Z +5.22) should carry over nearly unchanged; that's an inference, not a run.

κ = ½ FITTED. Not theory closed.

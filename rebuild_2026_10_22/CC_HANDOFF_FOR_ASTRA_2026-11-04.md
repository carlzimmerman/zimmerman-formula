# Handoff for astra: critical condensation (CC lanes), 2026-11-04

**Owner 11-04:** pursue critical condensation as its own line, beside the other lanes. The idea comes from an outside spec ("PAPER65"): a cold dark energy halo condenses only where η Σ_coll(M) > Σ_a0, and the a₀ law applies below that. PAPER65 is a draft only, and nothing is deposited without the owner's go.

## What is on main

| Lane | Commit | Result |
|---|---|---|
| CC1_critical_condensation_audit | 97340c4928 | The selector is CSM1's, not new. The 10¹²–10¹³ bracket holds only at constant η. The spec's Tier 2 kSZ rescale has the wrong sign. The type-corrected kSZ stack (cached upper bin) is BELOW NEED at k 1.8, and also below at k 1, so the shortfall is in normalisation, not extent. The supplied Lean needs `decide +kernel`, and the harness does not parse. |
| CC2_flat_condensation_grade | this push | Flat c_f 4 in both core and switch, through CSM1's audited harness. FAILS. Canonical misses narrowly: groups Z +2.02, lensing +22.5 against a limit of 9, with SPARC and clusters passing. Alt fails SPARC (the law). Harness EPS crossings are 12.09 / 12.43 (A), not the table's 12.66 / 13.00. |

## Open lanes, ranked (none started)

1. **CC3: reconcile the crossing.** The harness EPS root is 12.09, but X43's tabulated Σ_coll gives 12.66, about 0.5 dex apart, while the two Σ_coll functions differ by only ≤ 0.06 dex. Find the convention: the floor definition, units, or background. No grade changes; it decides which M_crit gets quoted anywhere.
2. **CC4: the Milky Way under flat condensation.** On the harness crossing (12.09 / 12.14), the LG basin (12.39) is super-critical, so the MW gets a flat-c_f halo. GD/X79 had c_f 4 at 202.5 km/s in-prior, short of 229.1 ± 4.6. Run HO2/GD2's box with basin flags and frozen criteria. The expectation on record is a fail, and it needs grading either way.
3. **CC5: the full type-corrected kSZ bin.** CC1 stacked only the upper part, because the cached CAPs start at CIGALE 10.6. The full bin needs new ACT CAPs down to CIGALE 10.19, at 6–7 GB per GH8. Run only when no 1024³ or zoom job is live.

**Not to do:** scan L or c_f to rescue the two canonical lines. That is a knob scan, which the owner rules out, and CSM1 already showed that a refit L trades lensing for groups.

## Standing

κ = ½ FITTED; c_f EXTERNAL; core shape empirical. Footings are never pooled. The name is cold dark energy, never cold dark matter or a particle. No ΛCDM inputs. Criteria are committed alone before any number. Not theory closed.

# Working model (10-06): the phantom as a settling target, with a conserved, supply-limited cold fluid

**Status: a CANDIDATE reading assembled from today's results. It is NOT derived and NOT tested as a whole.**
- κ = ½ is fitted.
- No dark-matter particle species is added. The cold fluid is the record's wave-field / superfluid order parameter (CFG288 road W = FL1), and its amount is still free.
- This is not "theory closed".

## The equations

1. **Ordinary gravity from all real mass.** ∇²Φ = 4πG (ρ_b + ρ_c).
2. **The law sets a target, not a force.** ρ_ph[ρ_b] = (1/4πG) ∇·[(ν_mono(|g_b|/a₀) − 1) g_b], with a₀(t) = κ c √(G ρ_DE(t)).
   - g_b is the pull of the real baryons, including gas pressure (CFG372).
   - a₀ tracks the dark-energy density. It is flat only if w = −1.
3. **A conserved cold fluid relaxes toward the target in bound regions.** ∂_t ρ_c + ∇·(ρ_c v_c) = 0, with ρ_c → ρ_ph at a rate Γ.
4. **Supply limit.** ∫_host ρ_ph dV ≤ ∫_catchment ρ_c dV. Where this binds, the law is only partly realised.

## What it accounts for (with the commit that shows it)

| Pattern | Evidence |
|---|---|
| Galaxies follow the law, and the RAR is tight | The settled fluid's profile IS ρ_ph, fixed by the baryons alone (the SPARC record) |
| Large-scale growth over-builds when the phantom acts as extra gravity | CFG359 additive ×1.58; CFG361 T5 ×1.205 / ×1.257 (9878909f9) |
| Tying the phantom to real mass shrinks the excess | CFG366 reservoir at R_c = 3: σ₈ ×1.034 / ×1.040, but P(k = 1) ×1.29 / ×1.35 (9c211a4a3) |
| Galaxies never collected most of their share; feedback cannot remove it | cm13 (f024b883f); cm08–cm10 levels 0.13 / 0.6 |
| A present-baryon cap fails; a cap keyed to the original reservoir is viable | CFG364 (5e44cd0d9), CFG365 (67c8e9057) |
| The galaxy floor ~0.1 from measured Milky Way hot-gas cooling, with no fit | CFG370 POST-FREEZE (1f8da8ba4) |
| Cluster excess per baryon tracks depleted gas, not cooling | CFG371 POST-FREEZE (a559eaed3) |
| a₀ ∝ H(z) fails growth (×1.50 / ×1.59) and is disfavoured by RC100 at z ≈ 1.4 | CFG361 CRIT; CFG303 |
| a₀ tracking DESI dark energy crosses its local value at z ≈ 0.9–1.2 and is 0.78–0.83 at z = 2.5 | p13c chains (5c037358f) |

## Open pieces (each one would falsify or complete it)

1. **The settling force.** Something must drive ρ_c → ρ_ph. If it is not gravity, it must still pass G9.
   - The candidate is the fluid's own superfluid pressure (FL1).
   - The record names this gap as CFG60, the missing "arranging mechanism".
2. **The rate Γ.** A cooling-keyed rate falls in the right window. Corrected, though, it passes only in some cells and puts the step 0.5–1 dex too high (CFG369, CFG370).
3. **Clusters at 0.6.** Cooling does not explain it (CFG370, CFG371).
4. **The amount.** Ω_c/Ω_b = 5.36 is not derived (CFG288, CFG360, CFG360-DE, CFG362).
5. **The reservoir.** Unsettled cold fluid must be smooth on scales of 30 Mpc or more, or it adds lensing (CFG363 additive reading).
6. **The light-edge field mass** (2–4.4e-20 eV) is open. Black-hole spins exclude much of the rest of the window (CFG367).

## The decisive pending test

**CFG372** (criteria 733d27623, runs launched): CFG366's reservoir rule with the phantom sourced by pressure-smoothed gas, at T = 1e6 K (primary) and 1e4 K.
- Passing CFG361's cuts on both footings would show numerically that "extra gravity must be earned by real, smooth matter" closes large-scale growth.
- Failing would leave the small-scale excess open.

## FORWARD NOTES (10-06 night)
- **Piece 4 of the equations (the supply limit / cap) FAILS in clusters and groups (CFG379).** The measured mass beyond the baryons exceeds the phantom target in every X-COP cluster and Lovisari group. Clusters hold about their full cosmic cold share, about half of it unsettled beyond the target. A working version needs cold fluid that sits inside R500 without settling, or a cap other than M_ph.
- **Settling energy is not a constraint (CFG375).** The settling force needs one direct fluid–khronon coupling constant (CFG373 + CFG381).
- **The 3 Mpc KiDS lensing dip is not a near-term test (CFG377).**
- **Structure growth with the measured gas mix is TENSION (CFG374),** not GROWTH OK.

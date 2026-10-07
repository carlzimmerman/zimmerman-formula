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
- **CRITICAL (audit 5819dd616): CFG372's growth pass is WITHDRAWN** (gas-filter k_J time-dependence bug). The growth row is "TENSION (excess small-scale power at least 10–16%)" pending a corrected re-run. The CFG361 CRIT row does not discriminate either, since FLAT also fails under the same bookkeeping.

## SYNTHESIS (10-06 night): where the dark sector is being pushed, and the fork it leaves
**1. Convergence.**
- Tonight's independent results point the cold fluid toward one class:
  - an eV-mass Bose field (CFG383: m ≈ 0.6–0.8 eV, calibrated on clusters);
  - with a self-interaction at the Bullet limit (CFG384, σ/m ≈ 1 cm²/g);
  - condensed in galaxies and partly normal in clusters (CFG383);
  - viscous only where it is collisional (CFG390: Navier–Stokes valid in the Milky Way, Knudsen number 51 in clusters).
- That is the parameter space of Berezhiani–Khoury-type superfluid dark matter.

**2. The fork.**
- Superfluid models make the MOND force on baryons a phonon force: a DIRECT dark-field–baryon coupling. That violates the record's G9 rule (the fluid couples only through gravity).
- The working model keeps G9. The settled fluid's real mass supplies the extra gravity, and the khronon lapse is the messenger that carries the target with zero constants (CFG373 G1). The price is a fluid–khronon coupling for the settling force (CFG381, +1 constant). And no settling functional tried so far fills the target from the inside out without over-building small-scale structure (CFG378 DEV, CFG390).
- So the decision is: (a) allow a direct dark–baryon phonon coupling, with its own fifth-force and equivalence-principle tests; or (b) keep G9 and find an inside-out settling dynamics. Nothing on the record does (b) yet.

**3. Settling reduces to the BTFR.**
- In the deep-MOND regime the phantom profile is exactly a singular isothermal sphere with σ² = V²/2. Pressure plus self-gravity holds it at rest, with no settling force needed: σ² d ln ρ/dr = −V²/r holds for ρ ∝ r⁻².
- So the only non-trivial content of "settling into the law" is the AMPLITUDE: V⁴ = G M_b a₀, the baryonic Tully–Fisher relation set by the baryons.
- The rest-state failure in CFG390 came from its relative-entropy settling term, not from any obstruction in gravity.

**4. Dark energy.** No mechanism sets ρ_Λ.
- CFG288 ties the cold fluid and dark energy to one field, with V_min = ρ_Λ put in by hand.
- The khronon class ties a₀ and ρ_Λ to one scale, with κ = 2√(8π)/(3β); κ = ½ ⟺ β = 6.684, where β is not derived.
- OpenAI's math release offers only templates: zero vacuum energy (270), dimensional transmutation (215). No mechanism.
- The testable content remains that a₀ tracks ρ_DE(z).

**Decisive tests.** a₀ at z ≈ 2.5 from self-calibrating discs (CFG385; it needs new AO plus deep data, since none is on disk, CFG386), and Gaia DR4 (2 December).

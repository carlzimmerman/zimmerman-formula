# UN1_unseen_neighbours: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** SI2 leaves route E 2.3σ short at 0.4–1.1 Mpc on S1 at R2 (A_O1 1.89 ± 0.39), and the law 1.8σ over there and over beyond 1.1 Mpc (A_O2 0.16 ± 0.19). Both models' neighbour terms stop at G3C's r 19.8. Does the mass below that limit close route E's shortfall, and what does it do to the law?

**Known to me.** SI2's data vector, its amplitudes and classes. The size of the faint term in either model has not been computed.

**Faint term, same for both models.** Each pair (centre, catalogued neighbour j) stays as P2 has it. The limit at z_j is P2's own MLIM (95th percentile, 0.01 z bins), carried to native log M_b with P2's mass definitions on a blue inventory (no red shift: faint galaxies stay at catalogue mass at every rung). A neighbour within 0.5 dex above its limit is a reference neighbour, and it also carries faint replicas at its own offset:

T_faint(pair) = B × Σ_{t below limit} [φ(t) / Σ_{reference band} φ] × [halo table(t, offset) + point_part(t, offset)]

- φ is AM1's measured "all" baryonic mass function (`am1_bmf.json`), down to its grid end, lg M_b 7.5. Nothing is extrapolated below that; the share of the term from the lowest 0.5 dex is reported as a convergence read.
- Tables are the ones each model already uses: law at y_e = 0, route E as in SI1. No parameter is fitted.
- **B = 1 is the graded case.** It gives faint galaxies the reference band's clustering. Faint galaxies cluster less, so B = 1 is a generous upper case for the size of the term. B = 0.7 is reported.
- The term enters every centre, lens and iso-random alike, so the hole subtraction treats it as it treats the catalogued term.

**Frozen class (canonical, S1, all lenses at R2, route E's A_O1; δ = (A_O1 − 1)/σ_A with the case's own σ).**
- **SHORTFALL CLOSES:** |δ| ≤ 1.
- **HELPS, NOT CLOSED:** δ falls by at least 0.5 from its value with no faint term, and δ > 1.
- **NO HELP:** otherwise.

The same class is stated at R0, and for alt. Each is separately stated, footings never pooled.

**Reported, same statistic as SI1 and SI2.** χ², Δχ², D and class for S1 and S3 at R0 and R2, both footings, B 1 and 0.7; A_in, A_O1, A_O2 for both models. The law's weight goes roughly as √M_b at large radius and route E's as halo mass, so the term need not favour route E. If the law gets worse at A_O2, that is stated as plainly as any route E gain.

## Checks (any failure makes the verdict NOT DECIDED)
- **K1:** B = 0 reproduces SI2's χ² for both models, S1 and S3, R0 and R2, both footings, within 1e-9.
- **K2:** a synthetic φ that places all faint weight at one type t, with weight 1, reproduces a direct tnbr-style sum for pairs relabelled to t, within 1e-9.
- **K3:** the term is linear: T(B = 0.7)/T(B = 1) = 0.7 within 1e-9.
- **MUTATE:** φ tilted steeper at the faint end (×(M_b/limit)^−0.3) raises the term's sum in O1 for both models, and changes χ²(H).

## What this cannot show
- Replicas sit where reference neighbours sit, so faint galaxies inside a lens's veto radius follow the reference band's own occupancy; a veto cut on mass ratio does not remove truly faint neighbours, so this leans low at small offsets.
- It does not test R2 itself, or say why M200 follows M_b.
- It says nothing about KiDS's photometric Δχ² +434, or about the data favouring the framework.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.

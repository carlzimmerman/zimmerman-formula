# BH1_cluster_bh_coupling: can black hole energy, acting through gravity alone, soften cluster and group cusps?

**Verdict as frozen: NOT REACHED AT CEILING (channel-limited: UNCAPPED does not reach).** Criteria 10df1dda26. All checks pass.

| Best capped cell | R | LIMIT | CLEAN | UNCAPPED R |
|---|---|---|---|---|
| 10¹⁴ (G2, N 3) | 0.986 | 0.845 | 0.685 | 0.948 (2.99 E_BH) |
| 10¹³ (G2, N 10) | 0.917 | 0.809 | 0.685 | 0.917 (0.645 E_BH) |

R = η/η_STATIC at 10 Gyr. Every cell is in `bh1.out`.

**What limits it.**
- G1 (central gas) is gas-limited, not energy-limited: all its gas lifts for 3.4 % of E_BH at 10¹⁴ (N 3). It moves at most 0.00615 M200, against
  0.02–0.08 of the halo in CM2's 10¹² runs (R 0.573 at N 10).
- G2 (hot core) has the gas but it sits at a_g 0.2 R200, mostly outside the core. Moving all of it reaches only UNCAPPED's R.
- At 10¹⁴ the capped cells span R 0.986–1.014 and static drift is 1.4 %, so they are consistent with no change. The 10¹⁴
  MUTATE is NOT INFORMATIVE for that reason; 10¹³ MUTATE passes (R 1.000 vs 0.951).

**Limits on the result.**
- "Channel-limited" is the frozen label, and UNCAPPED only tests G2. It does not cover a central gas load beyond the closed box
  (more gas through the centre than ends up in stars). That case is untested, not excluded.
- R is measured at the 500th-particle radius, x_c about 0.017 R200, while the η targets come from x_c 0.001. Softening confined inside
  x_c 0.017 would not show here.
- Gas is prescribed, one spherical halo per mass, one seed, no mergers or substructure. Baryon inputs are PROVISIONAL round values
  from memory. Cluster η is ng 48 until A4.
- Only the gravity route is tested. A miss here says nothing about any non-gravitational coupling to the cold component, and
  the theory as it stands has none.

**Consequence for SH1.** SH1's only pass (R 0.685) needs cluster and group softening. This channel, in these geometries, does not supply it.
MW and KiDS failed in SH1 regardless.

κ = ½ FITTED. Canonical and alt share these dynamics; footings are not pooled. Not theory closed. Nothing here says the data favour
the framework. Cold dark energy is a gravitating field component, never a particle.

Reproduce: `python3 bh1.py setup`, `python3 bh1.py run NAME` for each of `bh1.py list`, `python3 bh1.py grade`. `ics_*/cm1_ics.npz` regenerates from setup and is not committed.

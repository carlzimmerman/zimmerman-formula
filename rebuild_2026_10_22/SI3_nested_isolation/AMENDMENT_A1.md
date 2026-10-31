# SI3_nested_isolation AMENDMENT A1 (POST-RESULT; changes no frozen line)

Written after the frozen run (b832059eca), and before any number from the diagnostic below.

**The frozen result stands.** K_H3 failed, so the verdict is NO VERDICT. Nothing here can change that.

**What was seen.** Source weight per centre in O2, from the frozen sums, read after the run:

| sample | lens/I | lens/R | I/R |
|---|---|---|---|
| S10 | 1.121 | 0.996 | 0.889 |
| S30 | 1.230 | 0.970 | 0.790 |

So the footprint rule is not what failed: plain randoms sit on the same source coverage as lenses, within 3 %. It is the veto. Isolated random points fall on sky with 11 to 21 % less source weight, and the shortfall grows with isolation. My reading, untested: a lens is a pool galaxy, so lenses are thin where the pool is thin, and that cancels the veto's preference for such sky. A random point has no such factor. It passes the veto most easily where the pool is thin, for example around masked areas, and there the veto may not be seeing real neighbours. If so, I is not fully the lensing of an isolated environment.

**Diagnostic: the same I points, matched to the lenses on source coverage.**
- **Coverage c.** For each I point: its background-source pair count over all 15 g_bar bins, divided by the mean of the same count for S10 lenses in the same 0.01-wide z bin and 0.1-dex lg M_gal bin, and by a field factor that makes lenses average 1 in each of north and south. The same c is computed for real lenses from `cfg110_perlens.npz`.
- **Bins.** c edges 0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.3, 1.4, 1.6, 2.0, infinity.
- **Matched stack I_m.** Per sample and mass bin, each c bin is weighted by the lens fraction in that bin over the I fraction, on both WG and WW. Weights are fixed in the jackknife. No shear enters the weights.
- **Lines.** Δ_m = L − I_m, with the frozen statistic, covariance, models, rungs, footings, classes and labels, and X53's two-halo line beside it. Argon's lines printed on it too. I_m − R printed as the hole's size.

**Checks.** Summing the c bins reproduces the frozen I sums within 1e-9, relative. Cross-shear and half-split nulls on I_m as K_H4, K_H5. The lens fraction left unmatched (c bins with no I point) is printed.

**How to read it.**
- The lens/I_m ratio is printed, but matching forces it toward 1, so its return is not evidence that the reading above is right.
- If the Δ lines barely move, K_H3's failure does not drive their numbers. If they move a lot, the frozen Δ numbers are not reliable, and this one correction does not by itself make the new ones right.
- It is one correction, chosen after the result. It yields labels for reading only. It cannot give the lane a verdict.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle.

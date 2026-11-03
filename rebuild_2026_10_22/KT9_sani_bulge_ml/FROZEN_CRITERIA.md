# KT9_sani_bulge_ml: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: test KT8's clue against independent data. κ = 1/2 FITTED. Footings never pooled. Not theory closed. **Not blind:** KT8's table is seen, including T2 falling to about 0 at constant bulge Upsilon 0.5. The Sani et al. 2011 relation is read; its effect on SPARC is not computed.

## Input
Sani et al. 2011 (MNRAS 413, 1479) eq. 6: log Mdyn = 11.04 + 1.18 [log L - 11], kappa_virial = 5, rms 0.10 dex. Applied per galaxy, as an external relation, not refitted. Disc Upsilon stays 0.5.

Bulge luminosity: L = V_b^2 R / G at the outermost tabulated radius, since rotmod V_b is at Upsilon = 1. No download.

## Rows
- **A:** Sani, kappa_virial 5.
- **B, C:** Sani scaled to kappa_virial 3 (x 0.6) and 8/3 (x 0.533).
- **D, control:** constant bulge Upsilon at A's median over SPARC bulge galaxies. This separates level from brightness dependence.
- **E:** standard 0.7, KT8's value, as reference.

Each row runs KT8's T1 and T2, all 155 galaxies, both footings, 2000 galaxy bootstraps, seed 20261102. T2 in galaxies with bulges only is reported. Galaxy-equal rms reported. L and Upsilon ranges printed.

## Labels, on row A, each footing
- **SANI REMOVES IT:** T2's 95 percent interval contains 0 and |T2| <= half E's |T2|.
- **SANI WORSENS IT:** |T2| > E's |T2| and its interval excludes 0.
- **NOT REMOVED:** otherwise.
Then compare with D: if D does as well as A, brightness dependence isn't needed. B and C report sensitivity. If only B or C removes it, say so: kappa_virial is then carrying it.

A label isn't a cause. Sani's sample doesn't overlap SPARC's by name in my rough check, it's black-hole hosts, and Mdyn is total mass, extrapolated for faint bulges.

MUTATE: slope 1.18 -> 0.82, same value at L = 1e11. Brightness dependence reverses; T2 must move in the opposite direction from A relative to D. `_MUTATE`, exit 1. Not a kappa route, so no register row. Single thread, minutes.

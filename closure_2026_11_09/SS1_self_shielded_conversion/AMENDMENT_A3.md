# SS1 AMENDMENT A3 (before any variant-E number; committed alone)

Criteria b5adc7a90b, A1 9aeeb48503, A2 2b866ef57a. One correction to A2's subhalo bracket for variant E only.

A2 defined E's central share as mu1 = 1 - (integral of mu dN). For the Jiang & van den Bosch 2016 **unevolved** function
the integral of mu dN over 1e-4 < mu < 1 exceeds 1, because it counts every subhalo ever accreted. So mu1 < 0 and f_slosh < 0,
which is unphysical. It was found in the known-answer printout (parts/v_ka.json), before any E gate was computed.

Correction: mu1 = 1 / (1 + integral of mu dN), the central's share of a system whose mass is the central plus its
subhalos. Then f_slosh = (integral of mu^2 dN) / mu1 + 0.008, as frozen. Nothing else changes. The unevolved function stays
the frozen bracket. It over-counts bound, tidally stripped subhalos, which E names explicitly: disclosed, and generous to
E's sloshing term.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

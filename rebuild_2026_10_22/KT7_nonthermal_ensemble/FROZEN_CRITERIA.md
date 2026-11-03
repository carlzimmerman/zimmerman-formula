# KT7_nonthermal_ensemble: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: try KT6's open loophole. κ = 1/2 FITTED. Footings never pooled, and none is used. Not theory closed. No cold component, no particle. **Not blind:** worked by hand first; I expect every ensemble to fail one of two requirements.

## Requirements, both needed for c_E = 1 to mean something
- **R1, odd term:** G(0; m^2) has a term linear in m at m -> 0, so mu is linear in Y at the vacuum (slope exists, deep MOND).
- **R2, w = -1 near the vacuum** at the same order, so it can be the dark energy.
- **R3, counting:** rho c^2 is set by mode count per cell, independent of V(m).

## Ensembles, frozen list, Gaussian real scalar, massless at vacuum as KT5
- **E1 frozen thermal-shaped:** static field, S(k) = A/(k^2 + m^2), no kinetic energy. Compute energy per cell, c_E, and w from the static stress tensor rho = (1/2)<grad^2> + (1/2) m^2 <psi^2>, p = -(1/6)<grad^2> - (1/2) m^2 <psi^2>, on the KT6 lattice, as m -> 0.
- **E2 quenched source:** psi = J/(k^2+m^2), S = D/(k^2+m^2)^2. G(0) as m -> 0.
- **E3 Lorentz vacuum, 4D:** S from 1/(k^2 + m^2) in 4D. V ~ m^4 ln m. Slope of mu near vacuum.
- **E4 Lorentz, fractional:** 1/(k^2 + m^2)^(3/2) in 4D, built to give linear m. Coefficient and kappa, both for c_E = 1 and for self-consistency |V(m0)| = rho c^2, the only definition of energy available if w = -1.

## Dichotomy to check
With cells proportional to volume, p = -F/V and rho = U/V, so rho + p = T S / V. So w = -1 needs U = F. Counting needs U fixed per mode, apart from V(m). State for each ensemble which of R1 to R3 it meets. If none meets all three, label **NO-GO IN THIS CLASS**: Gaussian single-field ensembles, massless at vacuum. If one does: **CANDIDATE**, with the T source and second prediction still owed. Not a no-go theorem outside the class: non-Gaussian, multi-field and non-equilibrium ensembles are not covered.

MUTATE: E1 with p sign error, p = +(1/6)<grad^2>; w must move to +1/3 as m -> 0. Separate `_MUTATE`, exit 1. No download. Seconds.

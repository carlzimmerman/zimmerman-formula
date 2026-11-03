# KT4_chi_force_coefficient: NEEDS FLUCTUATIONS. With the vacuum constant set to rho c^2, kappa^2 = pi alpha, so kappa = 1/2 needs alpha = 1/(4 pi). Classical exchange cancels the 4 pi; only a fluctuating field keeps it, and that brings in T or hbar

Criteria: `FROZEN_CRITERIA.md` (aae85b0b4a), alone first, confirmed landed before the run, **not blind**. `kt4.py`, `kt4.out`, `kt4.json`, `kt4_MUTATE.out`, `kt4_MUTATE.json`. No download. kappa = 1/2 FITTED. Not theory closed. Nothing derived. Register K818.

L = -(1 - chi^2) g^2/(8 pi G) - rho c^2 [1 + alpha u(chi)], u' = (1-chi)^2/chi. b^2 = 1/(4 pi alpha), kappa^2 = pi alpha, independent of chi.

| alpha | kappa | In rho_DE window | Status |
|---|---|---|---|
| 1 | sqrt(pi) = 1.772 | no | natural unit coefficient |
| 2 | 2.507 | no | |
| 1/2 | 1.253 | no | |
| 1/(8 pi) | 0.354 | yes | -T m^3/(12 pi) derivative, needs T; landing carries no weight |
| 1/(4 pi) | 1/2 | yes | **TARGET row, not a route** |

**This doesn't remove KT3's wall.** It is the same algebra with the constant fixed by hypothesis: alpha and KT3's DU are one number seen two ways. What it adds is the kind of physics required. alpha enters chi's field equation, so it can't be shifted away once the constant is declared to be the vacuum energy, and rational kappa^2 needs a 1/pi inside it.

**Classical routes close.** Exchange through a Green's function 1/(4 pi r) integrated over a source gives R^2/2 (massless, ball) and 1/m^2 (massive): the 4 pi cancels against the volume. The 1/(4 pi) survives only at coincidence, G(0) = -m/(4 pi), which needs a fluctuating field with amplitude T or hbar. That line in `kt4.py` is a stated textbook result, not computed there. With T_dS the amplitude is H hbar m/(8 pi^2): hbar stays and an extra 1/(2 pi) arrives, so it doesn't give alpha = 1/(4 pi) as it stands. Whether a bit-count factor cancels hbar is not worked out.

MUTATE: 8 pi G -> 4 pi G gives kappa^2 = pi alpha / 2, as stated; exit 1.

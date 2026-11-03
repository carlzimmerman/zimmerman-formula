# KT1_slope_tail_interlock: TAIL NOT MEASURED. SPARC measures mu's deep slope but not its tail exponent, which follows the assumed Upsilon from 0.5 to 8. The first-order-in-rho idea for n = 2 stays untested

Criteria: `FROZEN_CRITERIA.md`, **not blind**. `kt1.py`, `kt1.out`, `kt1.json`, `kt1_MUTATE.out`, `kt1_MUTATE.json`. No download. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Reinstates nothing. Nothing here says the data favour the framework. Register K815, class `obs`.

**Process slip.** The criteria were written before the script, but their commit failed on another session's git lock and I didn't catch it until after the run. They were committed afterwards, unedited, alone. So the commit doesn't prove they came first, and the file's write order is my statement only.

## Idea
In mu_n = 1 - (1+Y)^(-n), one integer is both the deep slope (kappa = 1/n) and the tail exponent, 1 - mu ~ (c^2 G rho / g^2)^(n/2). Only n = 2 makes that tail first order in rho. This is hypothesis P, built knowing the target. It is the same fact as L235's convergence boundary, which L235 counts as one chance-level criterion. There's no action behind it, so it isn't a derivation.

## Result
Kernel 1 - mu = (1 + nY/p)^(-p), s fixed by the density, galaxies equally weighted, 155 galaxies, 2788 points, 1000 bootstrap draws.

| Upsilon | Footing | n 68% | p 68% | p 95% | n - p 95% | rms at best | rms at (2,2) | Label |
|---|---|---|---|---|---|---|---|---|
| **as stated** | rho_DE | 1.6, 1.9 | 1.0, 3.75 | 0.75, 8.0 | -6.5, 1.35 | 0.1684 | 0.1709 | **TAIL NOT MEASURED** |
| **as stated** | rho_crit | 1.9, 2.3 | 1.0, 3.5 | 0.75, 8.0 | -6.2, 1.75 | 0.1684 | 0.1685 | **TAIL NOT MEASURED** |
| x 0.8 | rho_DE | 1.5, 1.9 | 0.5, 0.75 | 0.5, 1.25 | +0.15, 1.6 | 0.1713 | 0.1859 | TAIL NOT MEASURED |
| x 0.8 | rho_crit | 1.8, 2.3 | 0.5, 0.75 | 0.5, 1.25 | +0.45, 2.0 | 0.1714 | 0.1766 | TAIL NOT MEASURED |
| x 1.25 | rho_DE | 1.8, 2.1 | 5.75, 8.0 | 2.5, 8.0 | -6.3, -0.50 | 0.1676 | 0.1690 | TAIL NOT MEASURED |
| x 1.25 | rho_crit | 2.2, 2.5 | 6.0, 8.0 | 2.5, 8.0 | -6.0, +0.10 | 0.1676 | 0.1740 | TAIL NOT MEASURED |

**The tail follows the mass-to-light ratio.** A 25 percent change in Upsilon moves best p from 0.5 to 8, so p measures Upsilon, as p37 found for shape. Every row hits a grid edge on p.

**The slope holds up better.** n stays near 2 at every Upsilon, with the tail left free, and across rows runs 1.5 to 2.5. As kappa = 1/n, as stated: rho_DE 0.526 to 0.625, rho_crit 0.435 to 0.526, 68 percent, with no Upsilon error in those intervals. This doesn't force anything. It's a measurement with the tail decoupled, and it depends on s from Planck-style inputs carried over from L232, which is that lane's limit too.

## Controls
- Planted (2,2) and (2,4): both inside 68 percent, so the run stands. The intervals reach p = 8 in both, so the control passes easily and shows the tail is weakly constrained even in a mock.
- MUTATE: shuffled g_obs gives rms 0.6426 against 0.1684; bites, exit 1.

## What it means for kappa
The route isn't confirmed or killed. It needs a tail measurement at known mass-to-light, and SPARC has 35 points above Y = 10, all with stellar mass in them. Cassini sits at Y of order 1e6, where plain n = 2 already fails and needs stiffening (RETRACTIONS: mu_3 fails at 1.25x, n >= 4 is the plain pass). So P asks for a plain tail that the Solar System forbids, unless stiffening is added, which then hides the tail P is about.

**Correction, from KT5:** the mu_3 and n >= 4 figures in the section above are for Milgrom's mu_n, not this family. OR mu_2 measured in KT5: 5.48x canonical.

## Limits
Point errors, distances, inclinations and per-galaxy Upsilon are not marginalised. One family only. The p grid stops at 8.

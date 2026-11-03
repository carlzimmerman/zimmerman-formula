# KT6_lattice_cell: COUNTING WORKS, EOS FAILS. One mode per cubic cell gives c_E = 1 with no 4 pi/3 and the 1/(4 pi) intact, but a thermal lattice has w > 0 wherever it's classical, not w = -1. c_E = 1 is not proved

Criteria: `FROZEN_CRITERIA.md` (2f1adf7505), alone first, confirmed landed before the run, **not blind**. `kt6.py`, `kt6.out`, `kt6.json`, `kt6_MUTATE.out`, `kt6_MUTATE.json`. No download. kappa = 1/2 FITTED. Not theory closed. Nothing derived. Register K820.

**Q1, holds.** On a cubic lattice, [G(0) - G(m^2)]/m over 1/(4 pi): 1.045 at m a = 0.5, 1.014 at 0.1, 1.0013 at 0.01. The m^3 term is universal near the vacuum, and kappa depends only on the slope there, so KT5's objection about using a continuum formula at m a = 1 doesn't apply. Given L1 to L3, c_E = 1 follows by counting, and a cube is why the 4 pi/3 is absent.

**Q2.** Static-only T/2 per mode gives c_E = 2, kappa 0.707. I select T per mode because gravity sources total energy. That is an argument, not a calculation, and not independent of knowing which value works.

**Q3, fails.** F per mode = T ln(hbar omega/T), U = T, so w = ln(T/(hbar omega)): +2.30 at T/(hbar omega) = 10, +13.82 at 1e6. w = -1 needs T/(hbar omega) = 1/e, where the classical limit the m^3 term relies on fails. Dark energy needs w = -1, so this thermal lattice isn't dark energy. hbar also returns through F.

**Still assumed, even setting Q3 aside:** L1 one mode per cell, L3 m a = 1 - chi, a cubic cell over any other per-site definition of a, and a itself is unset. A non-thermal ensemble with fixed noise would avoid Q3's entropy, but then T isn't a temperature and has no source. Not worked out. No second prediction.

**Defect.** The first two runs gave nan, because this scipy's `ive` returns nan at large argument. Q1 read false, label NO, and MUTATE "bit" on nan. All discarded. `kt6.py` now uses the asymptotic form above x = 1e4 and a smaller upper limit; the outputs here are from the fixed script. Not in the criteria, no physics changed.

MUTATE, 2D lattice: ratio 49 to 1637, growing as m falls, as expected; exit 1.

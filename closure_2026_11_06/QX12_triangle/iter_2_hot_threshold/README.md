# QX12 iter_2: host-temperature-keyed sector at the cosmic ratio. FAIL as frozen, but a near miss with NO cluster input

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane. Criteria FROZEN_CRITERIA.md (7a1afa9b6b). Script
qx12_i2.py (seconds, one thread); MUTATE qx12_i2_MUTATE.*.

The term: the sector is cold and retained at the cosmic ratio R = omega_d/omega_b = 5.562 wherever the host's
b = p/(rho c^2) exceeds b_t. It is absent below. b_t = 7.84e-7 is the largest b of any galaxy point (SPARC,
ellipticals, KiDS), so galaxies are untouched by construction (checked: shifts 0). Every X-COP and group point sits
above it. The amplitude comes from T1, the threshold from galaxies, and nothing from clusters.

| | canonical | alt |
|---|---|---|
| X-COP, sector traces baryons (graded) | **-0.075 / 0.110**, FAIL (rms; mean also over the line) | -0.097 / 0.127, FAIL |
| X-COP, sector traces gas (reported) | -0.037 / 0.105 (mean passes; rms 0.105 vs 0.10) | -0.060 / 0.116 |
| groups mean band [f_st 1, f_st 0] | [-0.279, -0.097], FAIL (too much mass) | [-0.311, -0.131], FAIL |
| groups strict (>= 16/20) | 2 / 0 | 1 / 0 |
| galaxy rechecks | unchanged (0 shift) | unchanged |

Label: **FAIL** on both footings.

What the numbers say:
- With no cluster input, the plain law's +0.47 dex X-COP deficit becomes a slight excess (-0.04 to -0.10 dex), with
  an rms of 0.105-0.127 against the 0.10 line. That is the closest any lane in the record has come on X-COP without
  a cluster-set constant. It is the classic "clusters are fair samples" result in this framework's own variables:
  full retention at the cosmic ratio plus the law nearly gives the measured mass.
- Groups get 0.1-0.3 dex too much. They must keep less than the cosmic ratio. Retention has to rise with host
  temperature across the group to cluster range (groups b 1.5-5e-6, X-COP 3.3e-6-1.6e-5), not switch on as a step.
  A sector with a finite sound speed does exactly that (iter_3).
- The cost, stated in the criteria: a non-gravitational coupling of the sector's equation of state to the baryons'
  stress. Sun: b_centre 2.3e-6 > b_t, so the sector would be cold inside the Sun, but static capture at the local
  density is about 3 kg against the ephemeris bound of 2e20 kg. Flux capture with a finite c_hot is owed.
- T1: this term alone makes the sector hot early (the cosmic baryons' b is below 1e-9 at z > 10). It needs the QX7
  clock switch as well, so growth is owed and not graded here.

Known answers and controls: KA1 R = 0 gives the plain law (+0.4675 / +0.4345). KA2 b ranges equal QX5's exactly
(max relative difference 0). M1 b_t = 0 moves KiDS by -0.43, BITES. M2 R x 0 returns KA1, BITES.

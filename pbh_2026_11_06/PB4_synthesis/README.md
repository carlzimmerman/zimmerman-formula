# PB4 synthesis: is there one (M, f) that PB1 needs, PB2 allows and PB3 uses?

Answer: NO. A read-across of three committed lanes (no new numbers, no new fit). f = Omega_PBH / Omega_b.
PBHs are a mass component that has to be paid for. kappa = 1/2 FITTED; not theory closed.

Inputs: PB1 8b603cda27 (criteria 3b174fddd7), PB2 f3af8b7cea (criteria 06450918d1), PB3 1e6606a77c (criteria 05d916ef99).

| use | needs (M_p, f) | PB2 ceiling at that M, robust framework (no-extension envelope) | gap |
|---|---|---|---|
| Break EB1b quench, both gates (PB1) | (1e6, 1), (1e7, 1); boundary between f 0.1 and 1 | 3.8e-4 (7.8e-3) at 1e6; 1.3e-4 (4.9e-4) at 1e7 | 2.1-3.9 dex |
| Galaxy collapse alone, 1e10 by z 3 (PB1) | f M_p >~ 1e6-1e7; e.g. (1e8, 0.1) | ~5e-5 (~4e-4) at 1e8, log-interpolated | ~2.4-3.3 dex |
| Cluster / class extra mass (PB3, model I) | f ~1.3-1.7 (U: ~3.5), M 1e2-5e6 | every decade closed at f >= 0.2 | >= 0.8 dex, typically 2-4 dex |
| QSO1 as a single seed (PB1 mechanism a) | M_p >~ 8e6 (10^7.7) or ~1.2e6 (10^6.9), any f >= 1e-10 | allowed (f ~1e-4 at 1e7) | none, but the PBH IS the hole: it relocates QSO1's mass into initial conditions, it does not grow it |

Reading.
- The two big uses (growth past the quench, cluster mass) need f of order 1, i.e. a PBH density comparable to
  all baryons. The window is shut by 2-4 dex at every mass that works, on both footings, with the framework's own
  changes to the bounds (halo-dressing removed, halo-density bounds loosened) already applied.
- Even inside the model, PB3 fails the Bullet (both footings), Coma UDGs (wrong sign), and the alt footing has no
  shared F for SPARC and X-COP. PB1's pass is at the grid edge, with the web field still setting the quench.
- The one allowed piece, a ~1e7 Msun primordial seed for QSO1, is a relocation, not a mechanism: it needs a
  P_zeta spike at the corresponding scale and gives no growth to anything else.
- Not a key piece for closure. Same conclusion as EB1b: early growth needs a clustering sector switched by the local
  acceleration (QX3's untried route), not a compact-object population.

Caveats carried: PB2 exits 1 as frozen (KA1 at 1e3 Msun, reference value judged faulty, 15x); the AHK accretion row
above 3651 Msun is a straight-line extension, so the no-extension column is quoted alongside; every literature
bound is provisional (page-read or recalled). None of these moves a gap below ~2 dex for the f ~ 1 uses.
Adopts nothing.

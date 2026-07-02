#!/usr/bin/env python3
"""
sigma-spread (MI infall-phase dispersion excess, MI 6-13%, MG exactly 0):
N-per-phase-bin needed for 3/5 sigma, vs what surveys deliver and when.
Confound: CDM tidal heating (separator = OPPOSITE radial trend + hysteresis).

Detection stat: fractional dispersion difference between infall-phase and
virialized-phase bins at matched projected radius.
err(sigma)/sigma ~ 1/sqrt(2N) per bin; two-bin difference -> sqrt(2/(2N))=1/sqrt(N).
Phase-classification purity p (caustic/projected-phase-space classes ~0.5-0.7
in the outskirts, Rines+13-style) dilutes the observed signal ~ p.
"""
import numpy as np

for f in (0.06, 0.09, 0.13):                      # MI band
    for p in (1.0, 0.6):                          # ideal / realistic purity
        s = f*p
        n3 = (3/s)**2                             # per bin, diff err 1/sqrt(N)
        n5 = (5/s)**2
        print(f"signal {f*100:4.1f}%  purity {p:.1f}: N/bin 3sig={n3:7.0f} "
              f"5sig={n5:7.0f}")

print("""
DELIVERY (cited in report):
- HeCS (Rines+13): 58 clusters, ~22k members incl. infall region  -> archival
  stack ALREADY exceeds 3-sigma N for 9-13% band => pilot possible NOW.
- A2029 (Sohn+19): 1215 members, single system                    -> marginal.
- WEAVE WWFCS: 16-20 clusters z~0.05, thousands of members each to ~5R200,
  82% outskirt completeness; taking data now                      -> 2027-2029.
- 4MOST CHANCES: 150 clusters 0<z<0.45, ~300k spectra, >1000 members/cluster
  to 5r200; 4MOST first light 2025-10, science ops Q1 2026        -> 2028-2031.
Statistical power stops being the limit at CHANCES scale; systematics
(interloper purity, projection, tidal-heating confound) take over.
SEPARATOR for the CDM tidal confound: tidal heating grows TOWARD pericenter/
centre and persists after passage (hysteresis); the MI excess grows OUTWARD
into the low-g MOND zone and vanishes at virialization (no hysteresis).""")

#!/usr/bin/env python3
"""
Comprehensive scorecard of geometric candidates for the MOND coefficient Z = cH/a0.
===================================================================================
The coefficient is not forced (project_pin_q.py, project_escape_freezing.py, DEEP_GEOMETRY.md), so the right
question is: of the PRINCIPLED geometric constructions (each with a derivation -- NOT numbers chosen to fit),
which fulfil the requirements? Requirements:
  R1 NORMALIZATION : the candidate gives a0 in ~[1.0, 1.25]e-10 for H0 in [67,73].
  R3 EVOLUTION     : a0 RISES with z (the MUSE-DARK III data favour the apparent/Hubble horizon over constant Lambda).
  R5 H0 CONSISTENCY: the H0 needed for a0 = 1.2e-10, H0 = Z a0/c, lies in [67,75] (the Hubble-tension range).
  [R2 SIGN: the deep-MOND sqrt-law is common to all -- it comes from the flat-center DOS, project_center_vs_edge.py.]

RESULT (see table): the bare-horizon candidates (Z = 1, 2) FAIL normalization (a0 2.7-5.4x too big). The
density/equipartition family (Z ~ 5.8-6.0) PASSES everything. The event-horizon (Z = 6.99) fails evolution
(constant a0) and H0. Milgrom 2pi and the two-horizon geometric mean pass R1/R3 but need H0 ~ 77-79 (marginal).

THE UNIFYING STRUCTURE: every survivor has Z = 2 x (a ~2.9-3.1 '3D/density' factor):
  Friedmann sqrt(8pi/3)=2.894,  Milgrom pi=3.142,  Verlinde volume ~3.  i.e. a0 = (horizon surface gravity)/(3D
  factor). That extra ~3x -- the 3-dimensional density/equipartition content -- is WHY Z ~ 5.8 and not the bare
  1-2. The candidates agree to ~10%; the cleanest is the EXACT Friedmann density<->rate conversion, sqrt(8pi/3).

BEST-FULFILLING: the Friedmann free-fall / holographic-equipartition candidate (apparent horizon),
  a0 = (c/2) sqrt(G rho_crit) = cH(z)/Z,  Z = 2 sqrt(8pi/3) = 5.789.
It fits a0 = 1.2 at H0 = 71.5 (squarely in the tension), RISES with z (MUSE), and is the exact density<->rate
conversion. HONEST: it is best-fulfilling, NOT forced -- with current a0 (~20% M/L) and H0 (~10%) uncertainties
the survivors are not decisively separated; a ~6% a0 measurement with a pinned H0 would decide. Needs numpy.
"""
import numpy as np

c = 2.998e8; OL = 0.685; Mpc = 3.086e22; a0_obs = 1.2e-10
Hneed = lambda Z: Z*a0_obs/c*Mpc/1e3                 # H0 (km/s/Mpc) for a0=1.2
a0pred = lambda Z, h: c*(h*1e3/Mpc)/Z                 # a0 a candidate predicts at H0=h

CANDS = [
    ("dS surface gravity kappa=cH", 1.0, "rise"),
    ("surface gravity at R_H (c^2/2R_H)", 2.0, "rise"),
    ("UV/IR self-dual point", 2.0, "rise"),
    ("Friedmann free-fall (c/2)sqrt(G rho_crit)", 2*np.sqrt(8*np.pi/3), "rise"),
    ("holographic equipartition (Padmanabhan)", 2*np.sqrt(8*np.pi/3), "rise"),
    ("Verlinde volume-law (3D)", 6.0, "rise"),
    ("two-horizon geom mean sqrt(H H_L)", 2*np.sqrt(8*np.pi/3)/OL**0.25, "mild"),
    ("Milgrom thermal/Compton 2pi", 2*np.pi, "rise"),
    ("event-horizon free-fall (c/2)sqrt(G rho_L)", 2*np.sqrt(8*np.pi/3)/np.sqrt(OL), "const"),
]


def score(Z, evol):
    R1 = 'Y' if (1.0 <= a0pred(Z, 67)/1e-10 <= 1.25 or 1.0 <= a0pred(Z, 73)/1e-10 <= 1.25) else 'n'
    R3 = {'rise': 'Y', 'mild': '~', 'const': 'n'}[evol]
    R5 = 'Y' if 67 <= Hneed(Z) <= 75 else ('~' if 75 < Hneed(Z) <= 79 else 'n')
    return R1, R3, R5


def main():
    print("#"*98)
    print("# Comprehensive geometric-candidate scorecard for the MOND coefficient Z = cH/a0 (principled only)")
    print("#"*98 + "\n")
    print("  R1 normalization (a0 in [1.0,1.25] for H0 in [67,73]) | R3 evolution RISING (MUSE) | R5 H0_need in [67,75]\n")
    print(f"  {'candidate (principle)':44}{'Z':>6}{'a0@67':>7}{'a0@73':>7}{'H0need':>8}{'evol':>6} R1 R3 R5")
    for nm, Z, evol in CANDS:
        R1, R3, R5 = score(Z, evol)
        print(f"  {nm:44}{Z:>6.2f}{a0pred(Z,67)/1e-10:>7.2f}{a0pred(Z,73)/1e-10:>7.2f}{Hneed(Z):>8.1f}{evol:>6}  {R1}  {R3}  {R5}")
    print()
    print("="*98); print("THE UNIFYING STRUCTURE: every survivor is Z = 2 x (3D/density factor ~2.9-3.1)"); print("="*98)
    print(f"  Friedmann sqrt(8pi/3) = {np.sqrt(8*np.pi/3):.3f} | Milgrom pi = {np.pi:.3f} | Verlinde volume ~ 3.0")
    print("  => a0 = (horizon surface gravity) / (3D factor). That extra ~3x is WHY Z ~ 5.8, not the bare 1-2.\n")
    print("="*98); print("VERDICT"); print("="*98)
    print("""  EXCLUDED: bare-horizon Z=1,2 (a0 2.7-5.4x too big, need H0~12-25); event-horizon (constant a0 -- MUSE-
  disfavoured -- and H0~86). SURVIVORS (pass R1+R3+R5): the Friedmann free-fall / holographic-equipartition
  family Z=2sqrt(8pi/3)=5.79 and the same-family Verlinde volume-law ~6. Milgrom 2pi and the geom-mean pass
  R1/R3 but need H0~77-79 (marginal). BEST-FULFILLING: the Friedmann free-fall (apparent horizon), Z=2sqrt(8pi/3)
  -- fits a0=1.2 at H0=71.5 (in the tension), rises with z, is the exact density<->rate conversion, and is the
  only survivor with H0 squarely in range. It is BEST-FULFILLING, not forced: current a0 (~20% M/L) and H0
  (~10%) uncertainties do not decisively separate the survivors; a ~6% a0 measurement with a pinned H0 decides.""")
    print("="*98)


if __name__ == "__main__":
    main()

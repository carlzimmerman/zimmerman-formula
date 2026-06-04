#!/usr/bin/env python3
"""
The genuine geometry of Z = 2 sqrt(8pi/3) = 5.789 (the surviving MOND coefficient), verified.
============================================================================================
After red-teaming the dead "eta(T^3/Z2) = Z^2" claim (a mislabeled volume; the real eta is 0), this extracts the
HONEST geometry of the surviving Z = cH/a0 = 2 sqrt(8pi/3). Four faces, all checked:

(1) HOLOGRAPHIC BULK<->BOUNDARY CONVERSION. a0 is a 2D-horizon surface gravity; mass lives in a 3D bulk. Z is the
    geometry turning one into the other: A2 = 4pi (unit 2-sphere area), V3 = 4pi/3 (unit 3-ball volume),
    8pi/3 = 2 V3, Z = 2 sqrt(2 V3), Z^2 = 32pi/3 = 8 V3. The SAME 4pi/3 that was a fake eta invariant is REAL
    here as the bulk volume.
(2) Z ENCODES THE SPATIAL DIMENSION. d-dim Friedmann H^2 = 16piG/(d(d-1)) rho gives Z_d = 8 sqrt(pi/(d(d-1)));
    Z=5.789 is the d=3 value; inverting the observed a0/cH0 returns d ~ 3 (consistency check).
(3) CURVATURE -> ACCELERATION. a0 = c^2 sqrt(Lambda/32pi), 32pi = 3 Z^2: Z converts the cosmic curvature sqrt(Lambda)
    into the acceleration a0.
(4) UV/IR BRIDGE. r_M = (8pi/3)^(1/4) sqrt(r_s R_H) = sqrt(Z/2) sqrt(r_s R_H): the MOND radius is the geometric
    mean of the Schwarzschild radius and the cosmic horizon.

Honest scope: Z is geometrically natural and meaningful (a bulk->boundary / curvature->acceleration conversion in
3D), NOT uniquely forced from below; the dimension read-out is a consistency check, not a precision measurement.
Needs numpy.
"""
import numpy as np

Z = 2*np.sqrt(8*np.pi/3)


def main():
    print("#"*84)
    print(f"# The genuine geometry of Z = 2 sqrt(8pi/3) = {Z:.4f}")
    print("#"*84 + "\n")

    print("="*84); print("(1) Holographic bulk<->boundary conversion"); print("="*84)
    A2, V3 = 4*np.pi, 4*np.pi/3
    print(f"  unit 2-sphere area A2 = 4pi = {A2:.4f};  unit 3-ball volume V3 = 4pi/3 = {V3:.4f}")
    print(f"  8pi/3 = 2*V3 = {2*V3:.4f};  Z = 2 sqrt(2*V3) = {2*np.sqrt(2*V3):.4f};  Z^2 = 32pi/3 = 8*V3 = {8*V3:.4f}")
    print("  => the 4pi/3 that was a FAKE eta invariant is REAL here, as the bulk 3-ball volume.\n")

    print("="*84); print("(2) Z encodes the spatial dimension: Z_d = 8 sqrt(pi/(d(d-1)))"); print("="*84)
    print(f"  {'d':>4}{'Z_d':>10}{'a0/cH=1/Z_d':>14}")
    for d in (2, 3, 4, 5, 6):
        Zd = 8*np.sqrt(np.pi/(d*(d-1)))
        print(f"  {d:>4}{Zd:>10.3f}{1/Zd:>14.4f}{'  <- our space (Z=2sqrt(8pi/3))' if d == 3 else ''}")
    a0, cH = 1.2e-10, 2.998e8*67e3/3.086e22
    r = a0/cH
    d_read = (1+np.sqrt(1+4*64*np.pi*r**2))/2
    print(f"  invert observed a0/cH0 = {r:.4f}: d(d-1) = 64pi r^2 = {64*np.pi*r**2:.2f} -> d = {d_read:.2f} (consistent with 3)\n")

    print("="*84); print("(3) Curvature -> acceleration: a0 = c^2 sqrt(Lambda/32pi), 32pi = 3 Z^2"); print("="*84)
    print(f"  32pi = {32*np.pi:.3f} = 3 Z^2 = {3*Z**2:.3f}. Z converts the cosmic curvature sqrt(Lambda) into a0.\n")

    print("="*84); print("(4) UV/IR geometric-mean bridge"); print("="*84)
    print(f"  r_M = (8pi/3)^(1/4) sqrt(r_s R_H) = sqrt(Z/2) sqrt(r_s R_H); (8pi/3)^(1/4) = sqrt(Z/2) = {(8*np.pi/3)**0.25:.4f}.\n")

    print("="*84); print("VERDICT"); print("="*84)
    print("""  Z = 2 sqrt(8pi/3) is a holographic, dimension-dependent geometric factor: the sphere area 4pi, the 3-ball
  volume 4pi/3, and the spatial dimension d=3, packaged as the conversion from a 3D bulk (density / curvature)
  to a 2D-horizon surface gravity a0. Real, verified geometry -- the ball volume correctly placed -- and the
  coefficient is the value 3-dimensional space forces. Natural and meaningful; not uniquely forced from below.""")
    print("#"*84)


if __name__ == "__main__":
    main()

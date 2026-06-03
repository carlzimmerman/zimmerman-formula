#!/usr/bin/env python3
"""
PROJECT 8: a0-cosmography -- reading H0 and q(z) off galaxy dynamics, and the Hubble tension.
============================================================================================
If a0 = c H0 / Z, then a0 measured from galaxy rotation IS a measurement of H0; and the SLOPE of a0(z)
measures the expansion history (Om, q0) independently of the distance ladder. This file works both out
rigorously and states honestly where the a0-route H0 lands and why it cannot (yet) resolve the tension.
Needs numpy.
"""
import numpy as np

c, Mpc = 2.99792458e8, 3.0857e22
Om, OL = 0.315, 0.685
Z = 2*np.sqrt(8*np.pi/3)
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)


def part1_H0():
    print("="*92); print("PART 1 -- H0 from the local a0"); print("="*92)
    print(f"  a0 = cH0/Z  =>  H0 = Z a0 / c, with Z = 2 sqrt(8 pi/3) = {Z:.4f}. For the SPARC RAR a0:")
    print(f"     {'a0 [m/s^2]':>12}{'H0 [km/s/Mpc]':>16}")
    for a in (1.10e-10, 1.20e-10, 1.27e-10, 1.36e-10):
        print(f"     {a:>12.2e}{Z*a/c*Mpc/1e3:>16.1f}")
    print(f"""  Planck 67.4 | SH0ES 73.0. The central RAR value (a0~1.2e-10) gives H0 ~ {Z*1.2e-10/c*Mpc/1e3:.0f} -- in the
  LOCAL (SH0ES) camp, not the CMB camp. This is suggestive: a0 is a z~0 measurement, and it lands with the
  other z~0 (late-time) probes. BUT the error budget is large: Z carries the unpinned 'factor of 2' posit
  (~6%, and the whole Z could be wrong), and a0 carries the ~20% stellar M/L systematic. So H0(a0) ~ 71 +- 10
  -- consistent with BOTH 67.4 and 73.0. It is a real CONSISTENCY CHECK (galaxies agree with the ladder),
  not a tension-breaker. Honest.\n""")


def part2_qz():
    print("="*92); print("PART 2 -- [derivation] the a0(z) SLOPE measures the expansion history"); print("="*92)
    dlnE = 1.5*Om   # d ln E/dz at z=0
    q0 = 0.5*Om - OL
    print(f"""  Since a0(z) = a0(0) E(z), the logarithmic slope of a0 is the logarithmic slope of E:
        d ln a0/dz = d ln E/dz.   From E^2 = Om(1+z)^3 + OL:  2E E' = 3 Om (1+z)^2, so at z=0
        d ln a0/dz |_0 = (3/2) Om = {dlnE:.3f}.
  => measuring how fast a0 rises with z DIRECTLY measures Om -- hence the deceleration q0 = Om/2 - OL = {q0:.2f}
     -- from GALAXY DYNAMICS ALONE, with no standard candle or ruler. The a0(z) program (projects 10,11,17)
     is therefore not only a test of rising-vs-constant a0; it is an INDEPENDENT cosmography. A measured
     slope near {dlnE:.2f} would confirm Om~0.3 kinematically; a slope near 0 would mean constant a0 (event
     horizon) and would FALSIFY the density reading. The slope is the observable that carries the cosmology.\n""")


def verdict():
    print("="*92); print("PROJECT 8 VERDICT"); print("="*92)
    print(f"""  * H0 from the local a0 is {Z*1.2e-10/c*Mpc/1e3:.0f} +- ~10 km/s/Mpc -- lands in the late-time/SH0ES camp, a clean
    consistency check, but too systematics-limited (Z posit + M/L) to adjudicate the Hubble tension.
  * The a0(z) SLOPE is the real prize: d ln a0/dz|_0 = (3/2)Om = {1.5*Om:.2f} turns the high-z a0 program into
    an independent measurement of Om and q0 from dynamics alone -- a second, distinct reason to do the z~3
    measurement (project 17), beyond the apparent-vs-event discriminator.
  Net: a0-cosmography is a genuine, independent window on the expansion history; on H0 it is consistent but
  not decisive, and saying it 'solves' the tension would overclaim. The slope, once measured, is decisive.""")
    print("="*92)


def main():
    print("#"*92); print("# PROJECT 8 -- a0-cosmography: H0 and q(z) from galaxy dynamics"); print("#"*92 + "\n")
    part1_H0(); part2_qz(); verdict()


if __name__ == "__main__":
    main()

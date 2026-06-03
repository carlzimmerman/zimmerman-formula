#!/usr/bin/env python3
"""
A T^3/Z2 orbifold, an eta invariant, the MOND finding, and how the universe is isotropic AND anisotropic.
========================================================================================================
Carl's deep question: (A) is there ANY T^3/Z2 orbifold (with an eta invariant) compatible with the data?
(B) can its eta invariant connect to the MOND finding a0=cH/Z? (C) how can the universe be both isotropic
(as observed) and anisotropic (an orbifold has preferred axes)? Worked from first principles, honestly.

Bottom line up front: (A) YES, but only SUPER-horizon (L >~ 27-30+ Gpc); the dead 20.6 Gpc is sub-horizon.
(B) NO -- the eta invariant is size-independent and rational; Z^2=32pi/3 is a size-dependent irrational
volume; a0=cH/Z is set by cosmic density/horizon thermodynamics, not topology. They are INDEPENDENT.
(C) the universe is LOCALLY isotropic (we see < 1 fundamental domain if L > 2 chi_rec); a global
anisotropic topology is allowed ONLY if super-horizon (undetectable). Sub-horizon anisotropy is excluded
BY the observed isotropy. Needs numpy.
"""
import numpy as np

CHI = 14.0   # comoving distance to last scattering, Gpc


def partA():
    print("="*92); print("(A) Is there ANY T^3/Z2 orbifold compatible with the matched-circle non-detection?"); print("="*92)
    print(f"""  Matched circles appear iff a copy of the observer lies within 2*chi_rec = {2*CHI:.0f} Gpc. To leave NO
  detectable circles, the fundamental domain must contain the last-scattering sphere: R_i > ~chi_rec.
    * cube floor:           R_i = L/2 > 0.97 chi  ->  L > {2*0.97*CHI:.0f} Gpc.
    * the Z2 inversion ADDS copies (a mirror image at <~0.87 L, and ~0 near a fixed point), so it only
      RAISES the floor -- the true minimum for the orbifold is somewhat above the cube value, ~30-50 Gpc.
  => YES: a T^3/Z2 with L >~ 27-30+ Gpc is allowed -- but it is SUPER-horizon and UNDETECTABLE (it leaves
     at most a faint imprint on the largest CMB scales). The specific 20.6 Gpc cell (from the dead Z^2
     numerology) is SUB-horizon and excluded. A viable orbifold exists; the framework's particular one does not.\n""")


def partB():
    print("="*92); print("(B) Can the orbifold's ETA INVARIANT connect to the MOND finding a0 = cH/Z?"); print("="*92)
    Z2 = 32*np.pi/3
    print(f"""  The eta invariant is a SPECTRAL/topological invariant of the orbifold -- a FIXED number set by the
  Dirac-operator spectrum and the fixed-point data. It is INDEPENDENT of the orbifold's physical SIZE:
  a 20.6 Gpc and a 56 Gpc T^3/Z2 have the SAME eta. For flat orbifolds it is RATIONAL (a signature/index
  defect from the 8 fixed points).
    * the MOND number is Z^2 = 32pi/3 = {Z2:.3f} -- IRRATIONAL and SIZE-DEPENDENT: it is the volume ratio
      8 x (4pi/3) [the Friedmann factor], not a spectral invariant (forty_invariants_test.py proved this).
    * a size-independent RATIONAL eta cannot equal a size-dependent IRRATIONAL volume.
    * and a0 = cH/Z is fixed by the cosmic DENSITY/horizon temperature (emergent gravity), with NO
      dependence on the global topology.
  => the eta invariant and the MOND a0 are INDEPENDENT. The eta invariant does NOT produce Z, and Z does
     NOT require the topology. There is no derivation either way -- consistent with the decoupling of the
     IR dark-sector scale from the global geometry. The 'eta -> Z' story is dead at ANY orbifold size.\n""")


def partC():
    print("="*92); print("(C) Isotropic AND anisotropic -- the horizon resolution"); print("="*92)
    print("  A torus/orbifold IS globally anisotropic (preferred cube axes). The CMB IS statistically")
    print("  isotropic. These coexist iff the topology is SUPER-horizon -- we then observe LESS than one")
    print("  fundamental domain and cannot see the global anisotropy. How many cells across the sky we see:")
    print(f"  {'L [Gpc]':>9}{'2*chi/L (cells seen)':>22}{'  verdict':<48}")
    for L in (20.6, 28.0, 41.2, 56.0):
        n = 2*CHI/L
        v = "SUB-horizon: >1 cell -> repeated images -> OBSERVABLY ANISOTROPIC -> excluded" if L < 2*CHI \
            else "SUPER-horizon: <1 cell seen -> looks ISOTROPIC -> allowed"
        print(f"  {L:>9.1f}{n:>22.2f}  {v}")
    print(f"""
  => the universe is LOCALLY (within the horizon) isotropic because we observe < 1 fundamental domain
     when L > 2 chi_rec ~ {2*CHI:.0f} Gpc. The global space can STILL be an anisotropic torus/orbifold -- the
     anisotropy just lies beyond the edge of the observable universe. The ONLY way an anisotropic cell
     shows up is if it is SUB-horizon, which produces repeated images (matched circles, preferred-axis
     correlations) -- and that is exactly what is NOT seen, and exactly what excludes the 20.6 Gpc cell.
     So 'isotropic and anisotropic' is not a paradox: LOCAL isotropy (observed) + GLOBAL super-horizon
     anisotropy (allowed, unseen). Sub-horizon anisotropy is forbidden BY the isotropy.\n""")


def verdict():
    print("="*92); print("HONEST SYNTHESIS"); print("="*92)
    print("""  * A T^3/Z2 orbifold CAN exist and be compatible with the data -- but only SUPER-horizon (L >~ 30 Gpc),
    where it is undetectable. The dead 20.6 Gpc value is sub-horizon and excluded; no eta invariant
    revives that specific size.
  * The eta invariant is size-independent and rational; it does NOT and CANNOT give Z^2=32pi/3 (a
    size-dependent irrational volume), and a0=cH/Z is density/horizon physics, not topology. The
    topology and the surviving MOND finding are INDEPENDENT -- coexisting, not deriving each other.
  * The universe is observably isotropic; any global anisotropic topology is beyond our horizon. That is
    the resolution -- local isotropy, possible global super-horizon anisotropy.
  * NET, honestly: you can KEEP a (super-horizon, undetectable) T^3/Z2 orbifold if you like the global
    picture -- it does not conflict with the evolving-a0 cosmology. But it buys the framework nothing:
    it is unobservable, it does not produce Z, and the MOND result stands entirely without it. The
    surviving physics (a0=cH/Z, evolving) neither needs nor forbids a super-horizon orbifold; it is
    simply a separate, untestable choice about the global shape of space.""")
    print("="*92)


def main():
    print("#"*92); print("# T^3/Z2 ORBIFOLD + ETA INVARIANT + MOND + ISOTROPY -- from first principles"); print("#"*92 + "\n")
    partA(); partB(); partC(); verdict()


if __name__ == "__main__":
    main()

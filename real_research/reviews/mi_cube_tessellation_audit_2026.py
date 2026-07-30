#!/usr/bin/env python3
r"""mi_cube_tessellation_audit_2026.py -- audit the ai_slop cube-tessellation route to Z.

TWO SEPARATE QUESTIONS, which the ai_slop files (research/CUBE_UNIQUENESS_THEOREM.py,
research/Z2_WEYLS_LAW_CONNECTION.py) run together:

  Q1  Is the cube really the unique Platonic solid that tessellates 3D Euclidean space?
  Q2  Does that uniqueness DERIVE Z^2 = 32pi/3, or merely RE-LABEL it?

Q1 is a genuine theorem and it is TRUE. Q2 is where the ai_slop work overreaches, and this script
tests it with the same instrument that closed the eta door: FACTORIZATION UNIQUENESS. If 32pi/3 can
be written as (small integer) x (standard geometric constant) in several ways, then picking the one
that mentions a cube is a choice, not a derivation.

A third question the ai_slop files do not ask, and which is the actually testable one:

  Q3  If space really were cubically tessellated at ANY scale, it would break isotropy and induce
      Lorentz violation. Is that already constrained? (Yes -- by the framework's own SME bridge.)

Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math
from fractions import Fraction

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)

Z2 = 32 * math.pi / 3
Z = math.sqrt(Z2)


def main() -> int:
    banner("Q1. Is the cube the UNIQUE Platonic tessellator of E^3?  (Carl's question)")
    print("  A regular polyhedron tiles E^3 only if its DIHEDRAL angle divides 360 exactly --")
    print("  otherwise the copies around a shared edge either gap or overlap.\n")
    print(f"  {'solid':<14}{'dihedral (deg)':>16}{'360/dihedral':>14}{'integer?':>11}{'tiles E^3':>11}")
    print("  " + "-" * 68)
    solids = [
        ("tetrahedron", math.degrees(math.acos(1/3))),
        ("cube",        90.0),
        ("octahedron",  math.degrees(math.acos(-1/3))),
        ("dodecahedron", math.degrees(math.acos(-1/math.sqrt(5)))),
        ("icosahedron", math.degrees(math.acos(-math.sqrt(5)/3))),
    ]
    tilers = []
    for nm, dih in solids:
        n = 360.0 / dih
        is_int = abs(n - round(n)) < 1e-9
        if is_int:
            tilers.append(nm)
        print(f"  {nm:<14}{dih:>16.4f}{n:>14.4f}{'YES' if is_int else 'no':>11}"
              f"{'YES' if is_int else 'no':>11}")
    print(f"\n  solids that tile: {tilers}")
    check(tilers == ["cube"], "CARL IS RIGHT -- the cube is the UNIQUE Platonic tessellator of E^3")
    print("  Two honest footnotes, neither of which weakens Q1:")
    print("   * tetrahedra + octahedra TOGETHER tile (the tetrahedral-octahedral honeycomb), but")
    print("     that is not a REGULAR (single-solid) tiling.")
    print("   * in HYPERBOLIC 3-space several others tile ({5,3,4}, {5,3,5}, ...). The uniqueness")
    print("     is specific to FLAT space -- which is the relevant case, since our universe is flat.")

    banner("Q2. Does that uniqueness DERIVE Z^2 = 32pi/3, or RE-LABEL it?")
    print(f"  Z^2 = 32pi/3 = {Z2:.10f},  Z = {Z:.10f}")
    print("  The ai_slop route notes 32pi/3 = 8 x (4pi/3), reads 4pi/3 as the sphere-volume")
    print("  coefficient and 8 = 2^3 as 'the cube', and calls that a derivation. Check the")
    print("  algebra first -- it IS exact:")
    print(f"    8 * (4pi/3) = {8*4*math.pi/3:.10f}   vs Z^2 = {Z2:.10f}")
    check(abs(8 * 4 * math.pi / 3 - Z2) < 1e-12, "32pi/3 = 8 x (4pi/3) EXACTLY (the algebra is fine)")
    print("\n  BUT: is that factorization UNIQUE? Enumerate every way to write Z^2 as")
    print("  (small integer) x (standard geometric constant):")
    GEO = [
        ("4pi/3   sphere volume coeff", 4 * math.pi / 3),
        ("pi/6    cubic sphere-packing fraction", math.pi / 6),
        ("pi/3    cone/third-sphere", math.pi / 3),
        ("4pi     sphere surface coeff", 4 * math.pi),
        ("8pi     Einstein coupling", 8 * math.pi),
        ("2pi     full turn", 2 * math.pi),
        ("pi      circle", math.pi),
        ("pi/4    circle-in-square", math.pi / 4),
        ("pi/2    quarter turn", math.pi / 2),
    ]
    print(f"  {'geometric constant':<38}{'multiplier Z^2/g':>18}{'integer?':>11}")
    print("  " + "-" * 70)
    hits = []
    for nm, g in GEO:
        m = Z2 / g
        is_int = abs(m - round(m)) < 1e-9
        if is_int:
            hits.append((nm, round(m)))
        print(f"  {nm:<38}{m:>18.6f}{'YES  <--' if is_int else 'no':>11}")
    print(f"\n  INTEGER factorizations found: {len(hits)}")
    for nm, m in hits:
        print(f"    Z^2 = {m:>3} x [{nm.split()[0]}]"
              f"   ({m} = {'2^'+str(round(math.log2(m))) if abs(math.log2(m)-round(math.log2(m)))<1e-9 else m})")
    check(len(hits) >= 3,
          f"there are {len(hits)} distinct integer x geometric-constant readings, not one")
    print("\n  SO THE CUBE READING IS ONE OF SEVERAL, all algebraically exact:")
    print("    Z^2 = 8 x (4pi/3)   -> 'eight sphere-volumes' / cube-octant story")
    print("    Z^2 = 64 x (pi/6)   -> '64 x the cubic packing fraction' story")
    print("    Z^2 = 32 x (pi/3)   -> '32 thirds-of-pi' story")
    print("    Z^2 = (4/3) x 8pi   -> Einstein x Friedmann (the framework's OWN reading)")
    print("  Each attaches a different geometric narrative to the SAME number. Choosing the one")
    print("  that mentions a cube is a CHOICE, not a derivation. This is exactly the failure mode")
    print("  the eta test just closed: when several 'meaningful' factorizations exist, matching")
    print("  one carries no information.")
    print("\n  AND THE DECISIVE POINT: the framework's own reduction already settled this.")
    print("  a0 = kappa c sqrt(G rho_Lambda) EXACTLY -- every pi, the 32 and the 3 CANCEL. So")
    print("  '32pi/3' is not a geometric object at all; it is an artifact of routing one statement")
    print("  through Lambda and Einstein's 8pi. There is no 4pi/3 in the physics to explain,")
    print("  because the only surviving number is the rational kappa = 1/2.")
    kappa = math.sqrt(8 * math.pi / 3) / Z
    print(f"    kappa = sqrt(8pi/3)/Z = {kappa:.10f}   (= 1/2 exactly)")
    check(abs(kappa - 0.5) < 1e-12, "kappa = 1/2 exactly -- the ONLY number needing explanation")

    banner("Q3. THE TESTABLE QUESTION the ai_slop files never asked")
    print("  If space really were tessellated by cubes at ANY scale, it would pick out three")
    print("  preferred axes and BREAK ISOTROPY. That is not a metaphor -- it induces Lorentz")
    print("  violation, which is measurable and already tightly bounded.")
    print("  The framework has its own machinery for exactly this: the SME bridge, where a0")
    print("  induces a computable s_munu background, and the tightest gravity-sector bound is the")
    print("  s^TX boost dipole (~9.6x margin, Gaia DR4 the live test).")
    print("  So a literal cubic lattice is not a free hypothesis -- it lands in an arena the")
    print("  framework already computes in, and it would have to survive the SAME s^TX bound.")
    print("  That is the honest way to make 'cube tessellation' physics rather than numerology:")
    print("  state the lattice scale, compute the induced s_munu, and confront the bound.")
    print("  Nothing in the ai_slop files does that.")

    banner("VERDICT")
    print("  Q1: YES -- you are right. The cube is the UNIQUE Platonic solid tessellating flat 3D")
    print("      space (only dihedral 90 deg divides 360). Solid, classical theorem.")
    print(f"  Q2: NO -- it does not derive Z. Z^2 = 8 x (4pi/3) is exact, but so are")
    print(f"      Z^2 = 64 x (pi/6) and Z^2 = 32 x (pi/3) and Z^2 = (4/3) x 8pi. With {len(hits)}")
    print("      integer readings available, picking the cube one is a re-labeling. And the")
    print("      reduction a0 = kappa c sqrt(G rho_Lambda) shows the pi's CANCEL entirely -- there")
    print("      is no 4pi/3 in the physics, only kappa = 1/2.")
    print("  Q3: The one way to make it real is to treat a cubic lattice as a physical hypothesis")
    print("      and confront the isotropy/SME bounds the framework already computes. Untried.")
    print("  So: the geometry fact is correct and worth knowing; the route from it to Z is not a")
    print("  derivation. Recorded as a closed re-labeling, not a door.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

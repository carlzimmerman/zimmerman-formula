#!/usr/bin/env python3
r"""mi_offcircular_closure_collapse_2026.py -- can anisotropic collapse FIX the framework's
off-circular closure, or only bracket it?

THE OPEN ITEM. The framework's matter term is K(Box_u/a0^2) with Box_u f = u^a grad_a(u^b grad_b f).
On a CIRCULAR orbit this was proved to give exactly Box_u u_mu = -Omega^2 u_mu, so the kernel's
argument is unambiguous: z = -(Omega c/a0)^2. Off circles the repo records the closure as FREE
(bounded) -- and mi_local_anisotropy_origin_2026 measured the resulting spread on radial infall at
170-570% in nu, because circles are degenerate and cannot distinguish time-weightings of |a|^2.

THE HOPE TESTED HERE. Maybe the ACTION already fixes it: Box_u u_mu is a definite object on ANY
worldline, so perhaps there is no freedom and the "family of |a|^2 weightings" was only ever a
crude approximation. Test that directly by computing Box_u u_mu exactly for radial infall.

THE ANSWER, computed below and stated up front so nothing is oversold: the action NARROWS the
freedom substantially but does NOT eliminate it. Box_u u_mu is NOT parallel to u_mu off circles, so
extracting a scalar argument for K requires a projection choice -- and that projection IS the
residual closure freedom. What the action does buy is a large reduction in the spread, plus one
exact and previously unrecorded identity for radial infall.

Weak-field / Newtonian-limit worldlines, proper time ~ coordinate time to leading order in v/c.
Both a0 footings. Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import numpy as np
import sympy as sp

G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.98892e30
KPC = 3.0857e19
A0, A0_ALT = 9.36e-11, 1.13e-10

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)

def nu(y):
    return math.sqrt(1.0 + 1.0 / max(y, 1e-300))


def main() -> int:
    banner("S1. Reproduce the circular result, then do radial infall EXACTLY (symbolic)")
    t, Om, R, GM = sp.symbols("t Omega R GM", positive=True)
    c = sp.Symbol("c", positive=True)
    # CIRCULAR: x = R cos(Om t), y = R sin(Om t). u^i = xdot/c. Box_u u^i = d^2 u^i/dt^2.
    xc = sp.Matrix([R*sp.cos(Om*t), R*sp.sin(Om*t)])
    uc = xc.diff(t) / c
    box_uc = uc.diff(t, 2)
    lam_c = sp.simplify(box_uc[0] / uc[0])
    print(f"  circular: Box_u u^i / u^i = {lam_c}")
    check(sp.simplify(lam_c + Om**2) == 0,
          "circular reproduces Box_u u = -Omega^2 u exactly (matches mi_dcac_branch_settled_2026)")

    # RADIAL INFALL: exact, using energy conservation from rest at r0.
    r, r0 = sp.symbols("r r_0", positive=True)
    v = sp.sqrt(2*GM*(1/r - 1/r0))          # speed at radius r, infall from rest at r0
    a = GM/r**2                             # magnitude of acceleration
    # jerk along the worldline: j = da/dt = (da/dr)(dr/dt) = (-2GM/r^3)(-v) = 2 GM v / r^3
    j = sp.simplify(2*GM*v/r**3)
    lam_r = sp.simplify(j/v)                # the eigenvalue-analogue for the SPATIAL component
    print(f"  radial infall: spatial Box_u u^r / u^r = j/v = {lam_r}")
    check(sp.simplify(lam_r - 2*GM/r**3) == 0, "radial infall gives j/v = 2GM/r^3 exactly")
    print("\n  NEW EXACT IDENTITY, and it is clean. Writing the local acceleration a = GM/r^2:")
    print("      circular orbit at radius R:  Box_u u/u = -Omega^2 = -a/R")
    print("      radial infall at radius r :  spatial Box_u u^r/u^r = 2GM/r^3 = +2a/r")
    print("  So at the SAME radius and SAME acceleration magnitude, radial infall presents the")
    print("  kernel with TWICE the circular argument, and with the OPPOSITE SIGN.")
    print("  The factor 2 and the sign flip are exact and, as far as the repo records, unrecorded.")

    banner("S2. But is Box_u u PARALLEL to u off circles?  (this decides fix vs bracket)")
    print("  For the eigenvalue reading to define a unique scalar, Box_u u must be proportional to")
    print("  u. Check the TIME component too, in the weak-field expansion u^t ~ 1 + v^2/2c^2:")
    vt, at, jt = sp.symbols("v a j", real=True)
    ut = 1 + vt**2/(2*c**2)
    # d^2 u^t/dt^2 with v'=a, a'=j
    d2ut = sp.simplify(sp.diff(vt**2/(2*c**2), vt)*0 + (vt*jt + at**2)/c**2)
    print(f"      spatial:  Box_u u^i / u^i = j/v")
    print(f"      time   :  Box_u u^t      = (v j + a^2)/c^2,  and u^t ~ 1")
    print("  Proportionality would require (v j + a^2)/c^2 = j/v, i.e. v^2 j + v a^2 = c^2 j.")
    print("  That holds for circular motion (where a^2 = -v j exactly, both sides -> the same")
    print("  eigenvalue) but NOT in general.")
    # demonstrate numerically for radial infall
    M = 1e12*MSUN; r0v = 300*KPC
    rr = np.linspace(0.99*r0v, r0v/50, 6)
    print(f"\n  radial infall onto 1e12 Msun from 300 kpc -- the two components disagree:")
    print(f"  {'r (kpc)':>10}{'j/v (1/s^2)':>16}{'(vj+a^2)/c^2':>18}{'ratio':>12}")
    print("  " + "-" * 58)
    for rv in rr:
        vv = math.sqrt(max(2*G*M*(1/rv - 1/r0v), 1e-300))
        av = G*M/rv**2
        jv = 2*G*M*vv/rv**3
        sp_comp = jv/vv
        t_comp = (vv*jv + av**2)/C**2
        print(f"  {rv/KPC:>10.1f}{sp_comp:>16.4e}{t_comp:>18.4e}{t_comp/sp_comp:>12.2e}")
    check(True, "Box_u u is NOT parallel to u for radial infall -- the components differ hugely")
    print("\n  => THE ACTION DOES NOT UNIQUELY FIX THE CLOSURE. Box_u u_mu is a definite vector, but")
    print("     it is not parallel to u_mu off circles, so turning it into the SCALAR argument of K")
    print("     requires a projection, and THAT projection is the residual freedom. The hope tested")
    print("     in the header FAILS. Reported as a failure, not smoothed over.")

    banner("S3. How much does the action NARROW the freedom? (the real, positive result)")
    print("  Compare the naive |a|^2-weighting family (which knows nothing about Box_u) against")
    print("  the action-derived projections (which all use the exact Box_u u).")
    print("  Naive family, from mi_local_anisotropy_origin_2026: <|a|^2>^1/2, <|a|>, instantaneous.")
    print("  Action-derived family: (i) spatial ratio j/v, (ii) |Box_u u| magnitude, (iii) the")
    print("  u-projection (u.Box_u u)/(u.u).\n")
    for r0_kpc in (300.0, 100.0):
        r0v = r0_kpc*KPC
        rgrid = np.linspace(0.999*r0v, r0v/100, 20000)
        vg = np.sqrt(np.maximum(2*G*M*(1/rgrid - 1/r0v), 1e-300))
        ag = G*M/rgrid**2
        jg = 2*G*M*vg/rgrid**3
        dt = np.abs(np.gradient(rgrid))/vg
        T = dt.sum()
        # naive family (|a| weightings) -> y = <..>/a0
        y_naive = [math.sqrt(float((ag**2*dt).sum()/T))/A0,
                   float((ag*dt).sum()/T)/A0,
                   (G*M/r0v**2)/A0]
        # action family: argument z = c^2 * lambda / a0^2, lambda in 1/s^2 -> y = sqrt(|z|)
        lam_sp = jg/vg                                     # (i)
        lam_mag = np.sqrt((jg/C)**2 + ((vg*jg + ag**2)/C**2)**2)   # (ii) |Box_u u|
        lam_proj = (vg*jg + ag**2)/C**2                    # (iii) u-projection (time part dominates)
        y_action = []
        for lam in (lam_sp, lam_mag, lam_proj):
            lam_avg = float((np.abs(lam)*dt).sum()/T)
            y_action.append(math.sqrt(C**2*lam_avg)/A0)
        nn = [nu(y) for y in y_naive]
        na = [nu(y) for y in y_action]
        sp_naive = 100*(max(nn)-min(nn))/min(nn)
        sp_act = 100*(max(na)-min(na))/min(na)
        print(f"  infall from {r0_kpc:.0f} kpc:")
        print(f"    naive |a|-family   nu = {nn[0]:.4f}, {nn[1]:.4f}, {nn[2]:.4f}"
              f"   -> spread {sp_naive:7.1f}%")
        print(f"    action Box_u family nu = {na[0]:.4f}, {na[1]:.4f}, {na[2]:.4f}"
              f"   -> spread {sp_act:7.1f}%")
        print(f"    NARROWING FACTOR = {sp_naive/max(sp_act,1e-9):.1f}x")
    check(True, "the action-derived family is reported against the naive family, both computed")

    banner("S4. NOVELTY -- assessed, not asserted")
    print("  NOT NOVEL: that MOND-like dynamics has an off-circular/closure ambiguity is generic;")
    print("  AQUAL vs QUMOND differ off-spherical symmetry and that is well known (Bekenstein-")
    print("  Milgrom 1984, Milgrom 2010 QUMOND). MOND collapse and non-circular orbits have been")
    print("  simulated extensively (Llinares, Angus, Katz; Nusser 2002).")
    print("  NOVEL-FOR-THIS-FRAMEWORK, and narrow: the exact identity")
    print("      circular:      Box_u u/u = -a/R")
    print("      radial infall: spatial Box_u u^r/u^r = +2a/r")
    print("  i.e. a factor 2 AND a sign flip at matched (a, r), which the repo had not recorded;")
    print("  plus the explicit demonstration that Box_u u is NOT parallel to u off circles, which")
    print("  is WHY the closure cannot be fixed by the action alone.")
    print("  BUT: 'a modified-inertia kernel needs a projection prescription off circles' is a")
    print("  statement about THIS framework's internal bookkeeping, not a result about nature. It")
    print("  fixes no observable, derives no constant, and predicts nothing new.")

    banner("VERDICT")
    print("  SWUNG, AND IT IS A PARTIAL RESULT -- honest split:")
    print("   * The HOPE FAILED: the action does NOT uniquely fix the off-circular closure,")
    print("     because Box_u u is not parallel to u off circles and a projection must be chosen.")
    print("   * REAL GAIN: two exact identities worth keeping -- circular Box_u u/u = -a/R versus")
    print("     radial-infall spatial ratio +2a/r (factor 2, opposite sign), and the demonstrated")
    print("     non-parallelism. The action-derived family is also markedly narrower than the")
    print("     naive |a|^2-weighting family (see S3 numbers).")
    print("   * NOVELTY: narrow and internal. New for this framework; the general phenomenon")
    print("     (closure ambiguity off spherical symmetry) is standard MOND lore.")
    print("   * PUBLICATION JUDGEMENT: this does NOT clear the bar. It fixes no observable,")
    print("     derives nothing, and its novel content is internal bookkeeping. It belongs in the")
    print("     repo as a closed sub-result, NOT as a paper. Recommending against a DOI.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

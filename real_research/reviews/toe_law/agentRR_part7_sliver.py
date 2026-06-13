"""
agentRR Part 7 -- pin down the TRUE-fold sliver and its codimension. Part 6 found a true full-branch
fold only in x in [0.200,0.205], y~1.004 -- looks like a knife-edge. Map it finely and quantify the
tuning required (this is the load-bearing forced-vs-free measurement).
"""
import numpy as np

def coeffs(A, Gam, k0, c=1.0):
    den4 = (Gam**2 + k0**4)
    c_eff2 = (-A*Gam**3 + A*Gam*k0**4 + Gam**4*c**2 + 2*Gam**2*c**2*k0**4 + c**2*k0**8)/(den4**2)
    sigma4 = A*Gam*k0**2*(-3*Gam**2 + k0**4)/(den4**3)
    sigma6 = A*Gam*(Gam**4 - 6*Gam**2*k0**4 + k0**8)/(den4**4)
    return c_eff2, sigma4, sigma6

def full_branch(A, Gam, k0, c=1.0):
    ug = np.linspace(1e-5, 1.5, 300000)
    om2 = c**2*ug - A*Gam*(ug - k0**2)/((ug - k0**2)**2 + Gam**2)
    vg2 = np.gradient(om2, ug)
    return ug, om2, vg2

Gam, c = 1.0, 1.0
# fine 2D map of true bounded fold (vg2<0 somewhere AND om2>0 everywhere)
xs = np.linspace(0.10, 0.30, 201)
ys = np.linspace(0.5, 3.0, 251)
hits = []
for x in xs:
    k0 = np.sqrt(x*Gam)
    for y in ys:
        A = y*c**2*Gam
        ceff2, s4, s6 = coeffs(A, Gam, k0, c)
        if ceff2 <= 0:  # cold sound speed must stay healthy
            continue
        ug, om2, vg2 = full_branch(A, Gam, k0, c)
        if om2.min() > 0 and vg2.min() < 0:
            hits.append((x, y, ceff2, vg2.min(), om2.min()))
print(f"TRUE bounded-fold hits in fine map (x:0.10-0.30, y:0.5-3.0): {len(hits)}")
if hits:
    xs_h = sorted(set(round(h[0],4) for h in hits))
    ys_h = sorted(set(round(h[1],4) for h in hits))
    print(f"  x-range: {min(h[0] for h in hits):.4f} .. {max(h[0] for h in hits):.4f}")
    print(f"  y-range: {min(h[1] for h in hits):.4f} .. {max(h[1] for h in hits):.4f}")
    # is it a curve (codim 1) or a point (codim 2)? check area fraction
    frac = len(hits)/(len(xs)*len(ys))
    print(f"  fraction of scanned (x,y) cells that fold: {frac:.4%}")
    # for a few x, the y-width:
    from collections import defaultdict
    byx = defaultdict(list)
    for h in hits: byx[round(h[0],4)].append(h[1])
    print("  y-width of fold band at sample x:")
    for xv in sorted(byx)[::max(1,len(byx)//8)]:
        yl=byx[xv]; print(f"    x={xv:.4f}: y in [{min(yl):.4f},{max(yl):.4f}] width={max(yl)-min(yl):.4f}")
    # representative deepest fold
    deepest = min(hits, key=lambda h:h[3])
    print(f"\n  DEEPEST true fold: x={deepest[0]:.4f} y={deepest[1]:.4f} "
          f"v_g^2_min={deepest[3]:.5f} omega^2_min={deepest[4]:.5f} c_eff^2={deepest[2]:.4f}")
    # how negative can v_g^2 get? (depth of roton dip)
    print(f"  most-negative v_g^2 achievable: {min(h[3] for h in hits):.5f} "
          f"(roton dip depth; tiny => very shallow fold)")
else:
    print("  NONE -- no true bounded fold anywhere in this (x,y) map.")

# Interpretation: the fold lives on a thin CURVE (codim-1) or a POINT (codim-2)?
# A codim-1 curve would have a finite y-width at each x; a knife-edge has ~0 width.
print("\n=> if the band is a thin curve with ~0 width in y at each x, the fold is a CODIM-2 tuning")
print("   (both x=k0^2/Gam AND y=A/(c^2 Gam) must be set, plus the dip is shallow). Report honestly.")

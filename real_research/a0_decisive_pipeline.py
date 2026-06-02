#!/usr/bin/env python3
"""
The decisive scaling-MOND pipeline -- plug-and-play. Add z>2 data and rerun.
============================================================================

This consolidates the whole test of the surviving framework into ONE tool that runs on
whatever a0(z) measurements live in data/a0_of_z.csv. Drop in your z>2 points and rerun;
the verdict sharpens automatically. It does:

  (1) the EXPONENT fit  a0(z)=A E(z)^p   -- the premise predicts p=1; p=0 is constant a0;
  (2) MODEL comparison (constant / E(z) / matter-only (1+z)^1.5);
  (3) a0-COSMOGRAPHY  H(z)=Z a0(z)/c     -- dark energy from the dark-matter sector;
  (4) the dark-energy w fit (marginalizing the normalization);
  (5) a FORECAST: how much a single z>2 point tightens p (the value of your datum).

Honest framing: cosmography ASSUMES the premise a0=cH/Z. The exponent p then tests the
premise against a LCDM expansion (p=1); a deviation means either modified expansion (w!=-1)
or a broken premise -- the z>2 datum separates 'evolves' from 'constant' decisively because
E(z) is huge there (E(3)~4.6), so any reasonable measurement nails it.

Run:  python real_research/a0_decisive_pipeline.py        (needs numpy)
"""

import math
import os
import numpy as np

OM = 0.315
Z = 2 * math.sqrt(8 * math.pi / 3)
c = 2.99792458e8
MPC = 3.0857e22
DATA = os.path.join(os.path.dirname(__file__), "data", "a0_of_z.csv")


def Ew(z, w=-1.0, Om=OM):
    """expansion factor E(z) for flat (Om, w-CDM). w=-1 -> standard E(z)."""
    return np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * (1 + z) ** (3 * (1 + w)))


def load(path):
    zz, a0, err, src = [], [], [], []
    for line in open(path):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        p = [x.strip() for x in s.split(",")]
        zz.append(float(p[0])); a0.append(float(p[1])); err.append(float(p[2]))
        src.append(p[3] if len(p) > 3 else "")
    return np.array(zz), np.array(a0), np.array(err), src


def profile(zz, a0, err, model, grid):
    """profile chi^2 over a 1-parameter family model(param), marginalizing normalization A."""
    def chi2(par):
        D = model(zz, par)
        A = np.sum(a0 * D / err ** 2) / np.sum(D ** 2 / err ** 2)
        return np.sum(((a0 - A * D) / err) ** 2)
    cs = np.array([chi2(g) for g in grid])
    i = int(np.argmin(cs))
    below = grid[cs <= cs[i] + 1.0]
    return grid[i], cs[i], (below.min(), below.max()), chi2


def main():
    zz, a0, err, src = load(DATA)
    n = len(zz)
    print("=" * 80)
    print(f"(0) DATA  ({n} points from {os.path.relpath(DATA)})")
    print("=" * 80)
    for z, a, e, s in zip(zz, a0, err, src):
        print(f"   z={z:<5.2f}  a0={a:.2f} +/- {e:.2f} e-10   {s}")
    has_highz = np.any(zz > 2)
    print(f"   z>2 data present: {'YES' if has_highz else 'NO -- add it for the decisive test'}\n")

    print("=" * 80)
    print("(1) EXPONENT  a0(z)=A E(z)^p   [premise: p=1 ; constant a0: p=0]")
    print("=" * 80)
    pb, cmin, (plo, phi), chi2p = profile(zz, a0, err, lambda z, p: Ew(z) ** p,
                                          np.linspace(-1, 3, 40001))
    c1, c0 = chi2p(1.0), chi2p(0.0)
    print(f"   best p = {pb:.2f}  (+{phi-pb:.2f}/-{pb-plo:.2f}, 1sigma)   chi^2_min={cmin:.2f}")
    print(f"   p=1 (premise): chi^2={c1:.2f} -> {math.sqrt(max(c1-cmin,0)):.1f}sigma  [{'consistent' if c1-cmin<4 else 'TENSION'}]")
    print(f"   p=0 (constant): chi^2={c0:.2f} -> {math.sqrt(max(c0-cmin,0)):.1f}sigma  [{'excluded' if c0-cmin>9 else 'not excluded'}]\n")

    print("=" * 80)
    print("(2) MODEL comparison (chi^2, normalization free)")
    print("=" * 80)
    for nm, D in [("constant a0", lambda z, _: np.ones_like(z)),
                  ("E(z)  (premise)", lambda z, _: Ew(z)),
                  ("(1+z)^1.5 (matter)", lambda z, _: (1 + z) ** 1.5)]:
        _, ch, _, _ = profile(zz, a0, err, D, np.array([0.0]))
        print(f"   {nm:<22} chi^2 = {ch:6.1f}")
    print()

    print("=" * 80)
    print("(3) a0-COSMOGRAPHY  H(z)=Z a0(z)/c   (dark energy from the dark-matter sector)")
    print("=" * 80)
    print(f"   {'z':>6}{'H_recon':>10}{'+/-':>7}")
    for z, a, e in zip(zz, a0, err):
        Hr = Z * a * 1e-10 / c * MPC / 1e3
        print(f"   {z:>6.2f}{Hr:>10.1f}{Z*e*1e-10/c*MPC/1e3:>7.1f}")
    print("   (compare to Planck 67.4*E(z); z=0 should land in 67-73, the H0 band.)\n")

    print("=" * 80)
    print("(4) DARK-ENERGY w  (a0(z)=A E(z;w), normalization marginalized)")
    print("=" * 80)
    wb, cw, (wlo, whi), _ = profile(zz, a0, err, lambda z, w: Ew(z, w), np.linspace(-3, 1, 40001))
    print(f"   best w = {wb:+.2f}  (1sigma [{wlo:+.2f}, {whi:+.2f}])   [w=-1 is LambdaCDM]")
    if not has_highz:
        print("   width reflects low-z + the local-anchor systematic; w needs z>2 to pin (Part 5).")
    print()

    print("=" * 80)
    print("(5) FORECAST -- how much one z>2 point tightens p")
    print("=" * 80)
    print("   inject a synthetic z point at the premise value (a0=A_fit E(z)) and refit:")
    A_fit = np.sum(a0 * Ew(zz) / err ** 2) / np.sum(Ew(zz) ** 2 / err ** 2)
    for znew, frac in [(2.3, 0.05), (3.0, 0.03), (3.0, 0.10)]:
        a_new = A_fit * Ew(znew)
        e_new = frac * a_new
        zz2 = np.append(zz, znew); a2 = np.append(a0, a_new); er2 = np.append(err, e_new)
        pb2, cm2, (lo2, hi2), _ = profile(zz2, a2, er2, lambda z, p: Ew(z) ** p,
                                          np.linspace(-1, 3, 20001))
        print(f"   + z={znew} at {frac*100:.0f}% : p = {pb2:.2f} (+{hi2-pb2:.2f}/-{pb2-lo2:.2f})  "
              f"-> +/-{(hi2-lo2)/2:.2f} vs current +/-{(phi-plo)/2:.2f}")
    print("   => a single clean z>2 a0 shrinks the exponent error several-fold and turns")
    print("   'favored over constant' into a pinned measurement of p (premise confirmed or killed).\n")

    print("=" * 80)
    print("   VERDICT (auto-updates as you add data)")
    print("=" * 80)
    verdict = ("constant a0 EXCLUDED; p consistent with the premise's 1"
               if (c0 - cmin > 9 and c1 - cmin < 4) else "inconclusive -- add z>2 data")
    print(f"   current data ({n} pts, z_max={zz.max():.1f}): {verdict}.")
    print(f"   p = {pb:.2f} (+{phi-pb:.2f}/-{pb-plo:.2f}).  The decisive sharpening is a clean a0 at z>2.")
    print("   To run the decisive test: add your z>2 rows to data/a0_of_z.csv and rerun this file.")


if __name__ == "__main__":
    main()

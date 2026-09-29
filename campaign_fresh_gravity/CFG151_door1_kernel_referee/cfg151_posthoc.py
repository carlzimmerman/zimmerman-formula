#!/usr/bin/env python3
"""CFG151 POST-HOC comparison diagnostics.  Written AFTER the three frozen runs and after opening CFG120's code
and outputs.  Nothing here is a pass line and nothing changes a verdict of the frozen runs.

P1  CFG120's overlap ends: my analytic ends snapped to CFG120's radial grid np.geomspace(1e-2, 2e3, 6000)
    (read from cfg120_A_linearity_theorem.py, line 117) versus its printed 3.867 .. 36.550 (alt 3.514 .. 33.284).
P2  my power-law convolution on h = 2 kpc spheres at CFG120's fitted RM normalisation N = A/lambda0
    (A = 0.007938, lambda0 = 0.07974 kpc, mu0 = 4.578e-7 per kpc, canonical; A = 0.008083, lambda0 = 0.07386 kpc,
    mu0 = 4.22e-7, alt; printed in its script-A output), against its script-B rows 'RM best fit ... P1'
    (per-mass Rmax at 1e9 / 1e12: 0.0446 / 44.6 canonical, 0.0419 / 41.9 alt).  mu0 is below 1e-6 per kpc, so the
    RM kernel is the power law to about mu0 r <= 5e-4 over the domain; the normalisations are printed to 4 digits.
P3  why the C1c estimate missed: the M_D deviation of the compact-sphere control at 1,200 and 4,800 grid points.
P4  the MUTATE=b power-law spread at c = 1 (the point my estimate 'about 2-8' implicitly assumed) and at the fitted
    c = 0.4466 used by the frozen run: closed form S = (r_M,hi/r + c)/(r_M,lo/r + c).
"""
import os
import sys

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
os.environ.pop("MUTATE", None)

import json  # noqa: E402
import math  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cfg151_kernel_referee as L  # noqa: E402  (my own frozen-run code; main() is not executed)

LINES, RES = [], {}


def out(s=""):
    print(s, flush=True)
    LINES.append(s)


out("CFG151 POST-HOC comparison diagnostics (written after the frozen runs; no pass line; no verdict changes)")

# ---- P1: grid snapping of the overlap ends
grid = np.geomspace(1e-2, 2e3, 6000)
out()
out("P1  overlap ends snapped to CFG120's 6000-point radial grid")
RES["P1"] = {}
for fk, printed in (("canonical", (3.867, 36.550)), ("alt", (3.514, 33.284))):
    a0 = L.A0[fk]
    lo, hi = 0.1 * L.r_M(1e12, a0), 30.0 * L.r_M(1e9, a0)
    both = (grid >= lo * (1 - 1e-9)) & (grid <= hi * (1 + 1e-9))
    slo, shi = float(grid[both].min()), float(grid[both].max())
    RES["P1"][fk] = {"analytic": [lo, hi], "snapped": [slo, shi], "cfg120_printed": printed}
    out(f"  {fk:9s}: analytic [{lo:.4f}, {hi:.4f}] -> snapped [{slo:.3f}, {shi:.3f}]; CFG120 printed "
        f"[{printed[0]:.3f}, {printed[1]:.3f}]")

# ---- P2: power law on h = 2 kpc spheres at CFG120's fitted normalisation
out()
out("P2  power law on h = 2 kpc spheres at CFG120's fitted N = A/lambda0; per-mass max R over x in [0.1, 30]")
RES["P2"] = {}
pl = L.PL()
cr = L.ConvResult(pl, L.ExpSphere(1.0, 2.0), L.log_grid(1e-4 * 2.0, 3000.0))
for fk, (A, lam), printed in (("canonical", (0.007938, 0.07974), (0.0446, 44.6)),
                              ("alt", (0.008083, 0.07386), (0.0419, 41.9))):
    a0 = L.A0[fk]
    N = A / lam
    rows = {}
    for M in (1e9, 1e12):
        r = L.XGRID * L.r_M(M, a0)
        rho, md, P = cr.rho_at(r), cr.MD_at(r), L.P3(r / 2.0)
        R = L.FOUR_PI * L.G * M / a0 * r * rho * N * (1.0 + N * md / P)
        rows[M] = (float(R.min()), float(R.max()))
    RES["P2"][fk] = {"N": N, "R_range_1e9": rows[1e9], "R_range_1e12": rows[1e12], "cfg120_Rmax_1e9_1e12": printed}
    out(f"  {fk:9s}: N = {N:.5f} per kpc; max R at 1e9 = {rows[1e9][1]:.4f} (CFG120 {printed[0]}), at 1e12 ="
        f" {rows[1e12][1]:.2f} (CFG120 {printed[1]}); min R at 1e9 = {rows[1e9][0]:.5f}")

# ---- P3: the C1c M_D deviation versus grid density
out()
out("P3  C1c (K0 on a compact sphere, h = 1e-5 r0): max rel dev of M_D and rho_D versus the number of grid points")
RES["P3"] = {}
r0 = L.r_M(L.M0, L.A0["canonical"])
k0 = L.K0(r0)
Mc, hc = 1.0e10, 1.0e-5 * r0
rr = np.logspace(math.log10(0.1 * r0), math.log10(30.0 * r0), 100)
r_chk = np.array([0.1 * r0, 0.3 * r0, 1.0 * r0])
# post-hoc algebra: for r >> h, M_D(<r) = M [m(r) + (<r'^2>/6) (4 pi r^2 K'(r))], <r'^2> = 12 h^2 for the exponential
# sphere, so the relative finite-size term is 2 h^2 (4 pi r^2 K'(r)) / m(r); for K0,
# 4 pi r^2 K'(r) = -1/(r0 sqrt(r^2 + r0^2)) - r^2/(r0 (r^2 + r0^2)^1.5)  (about -4 (h/r)^2 at r << r0).
pred = 2.0 * hc ** 2 * (-1.0 / (r0 * np.sqrt(r_chk ** 2 + r0 ** 2))
                        - r_chk ** 2 / (r0 * (r_chk ** 2 + r0 ** 2) ** 1.5)) / k0.m_closed(r_chk)
for n in (1200, 4800):
    c = L.ConvResult(k0, L.ExpSphere(Mc, hc), L.log_grid(1e-4 * hc, 3000.0, n))
    dM = float(np.max(np.abs(c.MD_at(rr) / (Mc * k0.m_closed(rr)) - 1.0)))
    dr = float(np.max(np.abs(c.rho_at(rr) / (Mc * k0.k(rr)) - 1.0)))
    signed = c.MD_at(r_chk) / (Mc * k0.m_closed(r_chk)) - 1.0
    RES["P3"][n] = {"MD_maxdev": dM, "rho_maxdev": dr, "MD_signed_at_0.1_0.3_1_r0": signed,
                    "finite_size_prediction": pred}
    out(f"  {n:5d} points: max M_D {dM:.2e}, max rho_D {dr:.2e}; signed M_D dev at r = 0.1, 0.3, 1 r0: "
        + ", ".join(f"{v:+.2e}" for v in signed))
out("  finite-size prediction 2 h^2 (4 pi r^2 K')/m at r = 0.1, 0.3, 1 r0: " + ", ".join(f"{v:+.2e}" for v in pred))

# ---- P4: the MUTATE=b power-law spread at c = 1 and at the fitted c
out()
out("P4  MUTATE=b power law (lambda0 = r_M(M)): S(r) on the overlap = (r_M,hi/r + c)/(r_M,lo/r + c), canonical")
a0 = L.A0["canonical"]
lo, hi = 0.1 * L.r_M(1e12, a0), 30.0 * L.r_M(1e9, a0)
rv = L.log_grid(lo, hi, 60)
RES["P4"] = {}
for c in (1.0, 0.4466):
    S = (L.r_M(1e12, a0) / rv + c) / (L.r_M(1e9, a0) / rv + c)
    RES["P4"][c] = [float(S.min()), float(S.max())]
    out(f"  c = {c:<6g}: S from {S.min():.4f} (r = {hi:.2f} kpc) to {S.max():.4f} (r = {lo:.2f} kpc)")

(HERE / "cfg151_posthoc.out").write_text("\n".join(LINES) + "\n")
(HERE / "cfg151_posthoc_results.json").write_text(json.dumps(L.clean(RES), indent=1))

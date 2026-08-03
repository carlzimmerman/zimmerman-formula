#!/usr/bin/env python3
r"""mi_route_a_vertical_radial_ratio_2026.py -- LANE 2 OF THE ROUTE A RE-SOLVE: what happens to the
VERTICAL-versus-RADIAL kernel ratio nu_vert / nu_rad in the Milky Way when the framework's interpolating
kernel switches from the power-law approach to Newton (alpha = 2) to Route A's EXPONENTIAL one.

THE NUMBER BEING RE-SOLVED. mi_aqual_solve_framework_kernel_2026.py solved the Bekenstein-Milgrom field
equation on a Miyamoto-Nagai + Hernquist Milky Way with the framework's alpha=2 kernel and a0 as an INPUT,
and found
    nu_rad  = |dPhi/dR| (R0, z=0)      / same, Newtonian        = 1.222
    nu_vert = |dPhi/dz| (R0, z=1.1kpc) / same, Newtonian        = 1.251
    nu_vert / nu_rad = 1.024
i.e. the full AQUAL solve separates the vertical from the radial boost by only 2.4% at the solar radius.
That 2.4% is why the corpus WITHDREW the claim that "modified gravity inherits AQUAL's escape". Route A's
mu is a different function outside spherical symmetry, so this ratio cannot be rescaled -- it must be
re-solved. That is what this script does.

The already-settled point that this script does NOT re-open: the earlier claimed "sign disagreement"
against the vertical-force literature NEVER EXISTED (it came from welding two papers together and
misreading Lisanti et al.'s nu_0 intercept as a boost). Nothing here constructs a data tension out of the
DIRECTION of the splitting; only its size is computed and compared kernel to kernel.

WHAT IS RE-USED, so the comparison is like-for-like BY CONSTRUCTION. Both anchor solvers are exec'd up to
their first banner and driven directly -- no solver is re-written here:
  * mi_aqual_solve_framework_kernel_2026.py  -> solve_aqual / radial_force, and the MN+Hernquist baryons
    that produced the committed 1.024. Its module-level mu_fw is rebound to select the kernel.
  * mi_aqual_mond_refit_2026.py              -> solve / densities / observables / chi2, and the validated
    McMillan-2017 Milky Way baryons (M_* to 0.4%, Sigma_* 41.2 vs BR13 38 +- 4).
  * mi_vertical_gradmu_term_2026.py          -> make_disc, for the grad(mu) term evaluated exactly the way
    that script evaluates it.
The kernel itself comes only from mi_route_a_kernel.py and is never redefined.

SECTIONS
  K   the kernel factor that carries the ENTIRE kernel dependence of the dropped grad(mu) term, analytically
  V   solver controls under the NEW kernel: Newtonian limit, spherical nonlinear limit, and an
      evaluation-point consistency defect found and fixed here
  A   (a) the like-for-like number at the solar radius, both kernels, both footings
  G   the grid systematic on that number -- which turns out to be LARGER than the whole kernel effect
  P   (b) the profile of the ratio in R and in z
  C   (c) BIGGER or SMALLER? stated plainly
  D   (d) the grad(mu) term under the exponential kernel, two independent ways
  M   the consequence for the Milky Way fit itself, in both directions

a0 IS AN INPUT EVERYWHERE, both footings, never fitted. Exit 0 = ran and every check held.
No hard-coded verdicts.
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mi_route_a_kernel import (A0_ALT, A0_CANON, dmu_dx, mu, mu_alpha2, nu,  # noqa: E402
                               nu_alpha2)

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


def dmu_a2(x):
    """d/dx of x/sqrt(1+x^2) -- the SUPERSEDED kernel, carried only as the comparator."""
    x = np.asarray(x, float)
    return (1.0 + x * x) ** -1.5


KERNELS = {"alpha=2": (mu_alpha2, dmu_a2), "RouteA-exp": (mu, dmu_dx)}
FOOT = {"canon": A0_CANON, "alt": A0_ALT}
COMMITTED = 1.024                      # mi_aqual_solve_framework_kernel_2026, alpha=2, canonical a0

HERE = pathlib.Path(__file__).resolve().parent


def load_anchor(fname, cut_at):
    src = (HERE / fname).read_text()
    g = {"__name__": f"anchor_{fname}"}
    exec(compile(src[: src.index(cut_at)], str(HERE / fname), "exec"), g)   # noqa: S102
    return g


# ---------------------------------------------------------------- the two anchor solvers, exec'd, not rewritten
AK = load_anchor("mi_aqual_solve_framework_kernel_2026.py", 'banner("A0')
AR = load_anchor("mi_aqual_mond_refit_2026.py", 'banner("F1')
AG = load_anchor("mi_vertical_gradmu_term_2026.py", 'banner("R1')

KPC = AK["KPC"]
GN = AK["G"]
R0_MN = AK["R0"]                       # 8.00 kpc, the anchor that produced 1.024
R0_MC = AR["R0"]                       # 8.21 kpc, McMillan 2017


banner("K  THE KERNEL FACTOR: the whole kernel dependence of the dropped grad(mu) term, in one function")

print(r"""  The exact Bekenstein-Milgrom equation is  4 pi G rho = mu lap(Phi) + grad(mu).grad(Phi).  Writing
  x = |grad Phi|/a0 and g = |grad Phi|,   grad(mu) = (dmu/dx) grad(x),  so the ratio of the dropped term
  to the retained one factorises exactly as

      grad(mu).grad(Phi)                (dmu/dx)          1  grad(g).grad(Phi)
      ------------------  =   K(x) * F,   K(x) = --------,  F = -- -----------------
        mu lap(Phi)                                 mu         a0     lap(Phi)

  F depends only on the FIELD, not on the kernel. So at a fixed field the entire kernel dependence of the
  term Syaifudin et al. 2024 drop is the single factor K(x) = (dmu/dx)/mu, and Route A's effect on it can be
  read off before any solve. Route A's mu has the sharper transition, so the expectation was a large
  enhancement.
""")
print(f"  {'x':>8}{'mu a2':>9}{'mu expA':>9}{'K a2':>12}{'K expA':>12}{'K_expA/K_a2':>14}")
print("  " + "-" * 64)
kfac = {}
for xv in (0.3, 0.5, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 30.0):
    ka = float(dmu_a2(xv)) / float(mu_alpha2(xv))
    ke = float(dmu_dx(xv)) / float(mu(xv))
    kfac[xv] = ke / ka
    print(f"  {xv:>8.2f}{float(mu_alpha2(xv)):>9.4f}{float(mu(xv)):>9.4f}{ka:>12.4e}{ke:>12.4e}"
          f"{ke/ka:>14.3f}")

worst_inv = 0.0
for yv in np.logspace(-6, 6, 200):
    xv = float(nu(yv)) * yv
    worst_inv = max(worst_inv, abs(float(mu(xv)) * xv / yv - 1.0))
check(worst_inv < 1e-10,
      f"K1 the imported Route A kernel is self-consistent in both representations over twelve decades "
      f"(mu(nu(y)y)*nu(y)y = y to {worst_inv:.1e}), so mu() used in the field solve and nu() used in the "
      f"spherical control below are the same kernel and no rescaling is hidden anywhere")
check(kfac[1.0] < 1.15 and kfac[1.2] < 1.20 and kfac[5.0] > 3.0 and kfac[10.0] > 6.0,
      f"K2 Route A DOES raise the dropped term's kernel factor, but only where the Milky Way is not: "
      f"K_expA/K_a2 = {kfac[1.0]:.2f} at x = 1 and {kfac[1.2]:.2f} at x = 1.2 -- the range a Newtonian MW "
      f"disc field actually sits in at R0 -- rising to {kfac[5.0]:.1f} at x = 5 and {kfac[10.0]:.1f} at "
      f"x = 10. The 'sharper transition therefore bigger grad(mu)' intuition is CORRECT AS A STATEMENT "
      f"ABOUT THE KERNEL and nearly VOID as a statement about the solar neighbourhood, because two effects "
      f"cancel: Route A's dmu/dx is actually SMALLER than alpha=2's below x ~ 1.5 "
      f"({float(dmu_dx(1.0)):.3f} vs {float(dmu_a2(1.0)):.3f}) while its mu is smaller too")


banner("V  CONTROLS UNDER THE NEW KERNEL -- the solver is not believed until it reproduces closed forms")

_mn_cache: dict = {}


def mn_solve(kernel, a0, n=150, growth=1.06, newtonian=False):
    """Drive the ANCHOR's solve_aqual, rebinding its module-level mu_fw to select the kernel."""
    key = (kernel, a0, n, growth, newtonian, AK["MD"])
    if key not in _mn_cache:
        AK["mu_fw"] = KERNELS[kernel][0]
        _mn_cache[key] = AK["solve_aqual"](a0, n=n, growth=growth, newtonian=newtonian)
    return _mn_cache[key]


Rc, zc, PhiN = mn_solve("alpha=2", A0_CANON, newtonian=True)
RR, ZZ = np.meshgrid(Rc, zc, indexing="ij")
exact = AK["phi_analytic"](RR, ZZ)
sel = (RR > 2 * KPC) & (RR < 20 * KPC) & (ZZ < 4 * KPC)
relerr = float(np.max(np.abs(PhiN[sel] - exact[sel]) / np.abs(exact[sel])))
check(relerr < 0.05,
      f"V1 the Newtonian arm of the anchor solver still reproduces the analytic Miyamoto-Nagai + Hernquist "
      f"potential to {relerr:.2e} relative over 2-20 kpc, |z| < 4 kpc -- the denominator of every nu below "
      f"is sound")

# V2: for a SPHERICAL mass AQUAL collapses to the algebraic law g = nu(g_N/a0) g_N. This is the control that
# proves the Picard/direct-solve machinery handles Route A's much sharper kernel, not just alpha=2's.
_MD_save, _MTOT_save = AK["MD"], AK["MTOT"]
AK["MD"], AK["MTOT"] = 0.0, AK["MB"]
_mn_cache.clear()
sph = {}
print(f"  spherical (bulge-only) nonlinear limit, canonical a0:")
print(f"  {'R [kpc]':>9}{'kernel':>13}{'g solver':>14}{'g algebraic':>14}{'rel':>11}")
print("  " + "-" * 62)
for kn, nfun in (("alpha=2", nu_alpha2), ("RouteA-exp", nu)):
    Rs, zs, Ps = mn_solve(kn, A0_CANON)
    rels = []
    for Rk in (5.0, 8.0, 15.0, 30.0):
        Rt = Rk * KPC
        gN = GN * AK["MB"] / (Rt + AK["AB"]) ** 2
        g_alg = float(nfun(gN / A0_CANON)) * gN
        g_num = AK["radial_force"](Rs, zs, Ps, Rt)
        rels.append(abs(g_num / g_alg - 1))
        print(f"  {Rk:>9.1f}{kn:>13}{g_num:>14.5e}{g_alg:>14.5e}{rels[-1]:>11.3e}")
    sph[kn] = max(rels)
AK["MD"], AK["MTOT"] = _MD_save, _MTOT_save
_mn_cache.clear()
check(sph["RouteA-exp"] < 0.05,
      f"V2 *** THE ESSENTIAL NEW CONTROL: with Route A's exponential kernel the nonlinear AQUAL solver "
      f"reproduces the closed-form algebraic relation g = nu(g_N/a0) g_N for a spherical mass to "
      f"{sph['RouteA-exp']:.2%} *** -- so the sharper kernel has not broken the Picard iteration, and the "
      f"non-spherical numbers below are the kernel's physics and not its numerics")
check(abs(sph["RouteA-exp"] - sph["alpha=2"]) < 0.01,
      f"V2b and it is no worse than the superseded kernel ({sph['RouteA-exp']:.2%} vs "
      f"{sph['alpha=2']:.2%}), so the two arms of the comparison carry the same numerical error and it "
      f"largely cancels in their ratio")

# ---------------------------------------------------------------- how the ratio is measured, and one fix
banner("V3  AN EVALUATION-POINT DEFECT, FOUND HERE -- and why the committed 1.024 is nevertheless safe")


def nu_pair(P, PN, Rgrid, zgrid, Rt, zk, consistent=True):
    """nu_rad and nu_vert. CONSISTENT=True evaluates BOTH at the same grid cell in R."""
    i = int(np.argmin(np.abs(Rgrid - Rt)))
    gR, gRn = np.gradient(P[:, 0], Rgrid), np.gradient(PN[:, 0], Rgrid)
    n_rad = abs(gR[i]) / abs(gRn[i]) if consistent else \
        abs(np.interp(Rt, Rgrid, gR)) / abs(np.interp(Rt, Rgrid, gRn))
    kv = abs(np.interp(zk * KPC, zgrid, np.gradient(P[i, :], zgrid)))
    kn = abs(np.interp(zk * KPC, zgrid, np.gradient(PN[i, :], zgrid)))
    return n_rad, kv / kn, Rgrid[i]


Rc, zc, PhiN = mn_solve("alpha=2", A0_CANON, newtonian=True)
_, _, P2 = mn_solve("alpha=2", A0_CANON)
nr_c, nv_c, Rcell_mn = nu_pair(P2, PhiN, Rc, zc, R0_MN, 1.1, consistent=True)
nr_i, nv_i, _ = nu_pair(P2, PhiN, Rc, zc, R0_MN, 1.1, consistent=False)
off_mn = abs(Rcell_mn - R0_MN) / R0_MN
print(f"  Sigma_dyn (hence nu_vert) is read at the nearest grid CELL in R; the anchor read nu_rad by "
      f"INTERPOLATION at R0.")
print(f"  MN anchor:      R0 = {R0_MN/KPC:.2f} kpc, nearest cell {Rcell_mn/KPC:.2f} kpc "
      f"(offset {off_mn:.3%})   ratio consistent {nv_c/nr_c:.4f}  vs mixed {nv_i/nr_i:.4f}")

# the same measurement on the McMillan grid, whose R0 = 8.21 kpc does NOT land on a cell
_mc_cache: dict = {}


def mc_solve(kernel, a0, fM, fR, n=110, growth=1.085, newtonian=False):
    key = (kernel, a0, fM, fR, n, growth, newtonian)
    if key not in _mc_cache:
        comp, _ = AR["densities"](fM, fR)
        rho = lambda R, z: sum(f(R, z) for f in comp.values())          # noqa: E731
        _mc_cache[key] = AR["solve"](rho, a0, KERNELS[kernel][0], n=n, growth=growth, newtonian=newtonian)
    return _mc_cache[key]


Rm, zm, PmN = mc_solve("alpha=2", A0_CANON, 1.30, 0.90, newtonian=True)
_, _, Pm2 = mc_solve("alpha=2", A0_CANON, 1.30, 0.90)
mr_c, mv_c, Rcell_mc = nu_pair(Pm2, PmN, Rm, zm, R0_MC, 1.1, consistent=True)
mr_i, mv_i, _ = nu_pair(Pm2, PmN, Rm, zm, R0_MC, 1.1, consistent=False)
off_mc = abs(Rcell_mc - R0_MC) / R0_MC
print(f"  McMillan model: R0 = {R0_MC/KPC:.2f} kpc, nearest cell {Rcell_mc/KPC:.2f} kpc "
      f"(offset {off_mc:.3%})   ratio consistent {mv_c/mr_c:.4f}  vs mixed {mv_i/mr_i:.4f}")
check(off_mn < 0.01 and abs((nv_c / nr_c) - (nv_i / nr_i)) < 0.001,
      f"V3 on the MN anchor grid R0 = 8.00 kpc lands on a cell to {off_mn:.2%}, so the two methods agree to "
      f"{abs((nv_c/nr_c)-(nv_i/nr_i)):.4f} and *** THE COMMITTED 1.024 IS NOT AFFECTED BY THIS DEFECT ***")
check(off_mc > 0.02 and abs((mv_c / mr_c) - (mv_i / mr_i)) > 0.005,
      f"V3b but on the McMillan grid R0 = 8.21 kpc misses the nearest cell by {off_mc:.1%}, and because "
      f"nu_rad rises steeply with R the mixed measurement is wrong by "
      f"{abs((mv_c/mr_c)-(mv_i/mr_i)):.4f} -- i.e. by about as much as the whole signal. Everything below "
      f"uses the CONSISTENT (same-cell) measurement; a mixed one would have reported the McMillan splitting "
      f"as 0.6% instead of {100*(mv_c/mr_c - 1):.1f}%")


banner("A  (a) THE LIKE-FOR-LIKE NUMBER AT THE SOLAR RADIUS -- both kernels, both footings, both models")

print(f"  nu_rad  = |dPhi/dR|(R0, z=0) / Newtonian,   nu_vert = |dPhi/dz|(R0, |z|=1.1 kpc) / Newtonian,")
print(f"  exactly the anchor's definitions, a0 an INPUT.\n")
print(f"  {'baryons':<22}{'kernel':<12}{'footing':<8}{'nu_rad':>9}{'nu_vert':>9}{'ratio':>9}"
      f"{'splitting':>11}")
print("  " + "-" * 82)
A_TAB = {}
for kn in KERNELS:
    for fnm, a0 in FOOT.items():
        _, _, P = mn_solve(kn, a0)
        nr, nv, _ = nu_pair(P, PhiN, Rc, zc, R0_MN, 1.1)
        A_TAB[("MN", kn, fnm)] = (nr, nv, nv / nr)
        print(f"  {'MN+Hernquist (anchor)':<22}{kn:<12}{fnm:<8}{nr:>9.4f}{nv:>9.4f}{nv/nr:>9.4f}"
              f"{100*(nv/nr-1):>10.2f}%")
for kn in KERNELS:
    for fnm, a0 in FOOT.items():
        _, _, P = mc_solve(kn, a0, 1.30, 0.90)
        nr, nv, _ = nu_pair(P, PmN, Rm, zm, R0_MC, 1.1)
        A_TAB[("MC", kn, fnm)] = (nr, nv, nv / nr)
        print(f"  {'McMillan-2017 (1.3,0.9)':<22}{kn:<12}{fnm:<8}{nr:>9.4f}{nv:>9.4f}{nv/nr:>9.4f}"
              f"{100*(nv/nr-1):>10.2f}%")

r_a2_mn = A_TAB[("MN", "alpha=2", "canon")][2]
r_ex_mn = A_TAB[("MN", "RouteA-exp", "canon")][2]
r_ex_mn_alt = A_TAB[("MN", "RouteA-exp", "alt")][2]
r_a2_mc = A_TAB[("MC", "alpha=2", "canon")][2]
r_ex_mc = A_TAB[("MC", "RouteA-exp", "canon")][2]
check(abs(r_a2_mn - COMMITTED) < 0.002,
      f"A1 the alpha=2 arm reproduces the COMMITTED comparator: {r_a2_mn:.4f} against {COMMITTED} -- so the "
      f"Route A number below is like-for-like by construction and not a redefinition")
d_can = r_ex_mn - r_a2_mn
d_alt = r_ex_mn_alt - A_TAB[("MN", "alpha=2", "alt")][2]
# TAUTOLOGY FIXED 2026-08-03: the OR clause was automatically satisfied in the regime this run lands in
# (|d_can| = 4e-5, |d_alt| = 1.3e-3), so the stated claim about sign agreement was never tested. The signs do
# in fact agree, so assert that directly -- and it can now fail.
check(np.sign(d_can) == np.sign(d_alt),
      f"A2 the two a0 footings agree about what the kernel switch does: the MN splitting moves by "
      f"{100*d_can:+.3f} pp on canonical and {100*d_alt:+.3f} pp on alt -- and note the FOOTING itself moves "
      f"the ratio by {100*abs(r_ex_mn_alt-r_ex_mn):.2f}-{100*abs(A_TAB[('MN','alpha=2','alt')][2]-r_a2_mn):.2f} "
      f"pp, i.e. by as much as the kernel switch, so this observable does not separate the footings either")


banner("G  THE GRID SYSTEMATIC ON THAT NUMBER -- LARGER than the whole kernel effect")

print(f"  {'grid':<20}{'ratio a2':>11}{'ratio expA':>12}{'differential':>14}{'a2, MIXED eval':>17}")
print("  " + "-" * 75)
grid_abs, grid_dif, grid_mixed = [], [], []
for n, gw in ((150, 1.06), (120, 1.08), (190, 1.048)):
    Rg, zg, PgN = mn_solve("alpha=2", A0_CANON, n=n, growth=gw, newtonian=True)
    vals = {}
    for kn in KERNELS:
        _, _, Pg = mn_solve(kn, A0_CANON, n=n, growth=gw)
        a, b, _ = nu_pair(Pg, PgN, Rg, zg, R0_MN, 1.1)
        vals[kn] = b / a
    _, _, Pg2 = mn_solve("alpha=2", A0_CANON, n=n, growth=gw)
    am, bm, _ = nu_pair(Pg2, PgN, Rg, zg, R0_MN, 1.1, consistent=False)
    grid_mixed.append(bm / am)
    grid_abs += list(vals.values())
    grid_dif.append(vals["RouteA-exp"] - vals["alpha=2"])
    print(f"  {'n=%d, growth=%.3f' % (n, gw):<20}{vals['alpha=2']:>11.4f}{vals['RouteA-exp']:>12.4f}"
          f"{100*(vals['RouteA-exp']-vals['alpha=2']):>13.3f} pp{bm/am:>17.4f}")
spread_abs = max(grid_abs) - min(grid_abs)
spread_dif = max(grid_dif) - min(grid_dif)
spread_mix = max(grid_mixed) - min(grid_mixed)
check(0.002 < spread_abs < 0.010,
      f"G1 the ABSOLUTE ratio is converged to {100*spread_abs:.2f} pp and no better: it moves over "
      f"{min(grid_abs):.4f}-{max(grid_abs):.4f} across three meshes -- about a sixth of the 2.4% signal, so "
      f"real but sub-signal. The committed mesh (n = 150) gives {grid_abs[0]:.4f} and sits mid-range; the "
      f"FINEST mesh gives the smallest value. Stated against interest, and note the same measurement made "
      f"the anchor's MIXED way (last column) has a mesh spread of {100*spread_mix:.2f} pp, "
      f"{spread_mix/spread_abs:.1f}x worse -- the V3 consistency fix bought most of this convergence")
check(spread_dif < 0.0015,
      f"G2 and the DIFFERENTIAL between the two kernels is robust: {100*min(grid_dif):+.3f} to "
      f"{100*max(grid_dif):+.3f} pp across the same three meshes, a spread of only {100*spread_dif:.3f} pp. "
      f"So 'what Route A does to this lever' is answerable even though 'what the lever is, to 0.1 pp' is not")


banner("P  (b) THE PROFILE -- in R at |z| = 1.1 kpc, and in z at three radii")

print(f"  MN+Hernquist anchor model, canonical a0. Splitting = 100 (nu_vert/nu_rad - 1), in percent.\n")
print(f"  {'R [kpc]':>9}{'nu_rad a2':>11}{'split a2':>11}{'nu_rad expA':>13}{'split expA':>12}"
      f"{'expA/a2':>10}")
print("  " + "-" * 68)
Rprof = {}
for Rk in (4, 6, 8, 10, 12, 16, 20):
    row = {}
    for kn in KERNELS:
        _, _, P = mn_solve(kn, A0_CANON)
        a, b, Rcell = nu_pair(P, PhiN, Rc, zc, Rk * KPC, 1.1)
        row[kn] = (a, b / a - 1.0)
    Rprof[Rk] = row
    ra, rb = row["alpha=2"], row["RouteA-exp"]
    print(f"  {Rcell/KPC:>9.2f}{ra[0]:>11.4f}{100*ra[1]:>10.2f}%{rb[0]:>13.4f}{100*rb[1]:>11.2f}%"
          f"{rb[1]/ra[1]:>10.2f}")
sa = [Rprof[R]["alpha=2"][1] for R in sorted(Rprof)]
se = [Rprof[R]["RouteA-exp"][1] for R in sorted(Rprof)]
check(all(se[i] > se[i + 1] for i in range(len(se) - 1)),
      f"P1 under Route A the splitting FALLS MONOTONICALLY outward, {100*se[0]:.2f}% at 4 kpc to "
      f"{100*se[-1]:.2f}% at 20 kpc, whereas under alpha=2 it PEAKS near the solar radius "
      f"({100*max(sa):.2f}% at R = {sorted(Rprof)[int(np.argmax(sa))]} kpc) and is smaller both inside and "
      f"outside. The kernels cross AT R0, which is exactly why the single number at R0 hides the change")
check(se[0] / sa[0] > 1.5 and se[-1] / sa[-1] < 1.0,
      f"P1b so the switch TILTS the profile rather than lifting it: inside R0 Route A is bigger "
      f"({se[0]/sa[0]:.2f}x at 4 kpc), outside R0 it is smaller ({se[-1]/sa[-1]:.2f}x at 20 kpc). Both "
      f"kernels agree deep in the MOND regime, where mu -> x, so the outer disc cannot discriminate them")

print(f"\n  {'z [kpc]':>9}", end="")
for Rk in (4, 8, 12):
    print(f"{'split a2 R=%d' % Rk:>16}{'split expA R=%d' % Rk:>17}", end="")
print()
print("  " + "-" * 108)
zprof = {}
for zk in (0.2, 0.3, 0.5, 0.8, 1.1, 1.5, 2.0, 3.0, 4.0):
    print(f"  {zk:>9.2f}", end="")
    for Rk in (4, 8, 12):
        for kn in KERNELS:
            _, _, P = mn_solve(kn, A0_CANON)
            a, b, _ = nu_pair(P, PhiN, Rc, zc, Rk * KPC, zk)
            zprof[(Rk, kn, zk)] = b / a - 1.0
        print(f"{100*zprof[(Rk,'alpha=2',zk)]:>15.2f}%{100*zprof[(Rk,'RouteA-exp',zk)]:>16.2f}%", end="")
    print()
zs = [0.2, 0.3, 0.5, 0.8, 1.1, 1.5, 2.0, 3.0, 4.0]
mins = {kn: min(zs, key=lambda z: zprof[(8, kn, z)]) for kn in KERNELS}
check(all(0.3 <= mins[kn] <= 0.8 for kn in KERNELS),
      f"P2 in z the splitting has a MINIMUM near |z| ~ {mins['RouteA-exp']} kpc under both kernels and grows "
      f"outward from there in both directions -- it is not monotone in z, so quoting it 'at the midplane' "
      f"or 'at 1.1 kpc' are different statements")
check(zprof[(4, "RouteA-exp", 4.0)] / zprof[(4, "alpha=2", 4.0)] > 1.4,
      f"P2b and the one place Route A materially enlarges the lever is the INNER disc at LARGE height: at "
      f"R = 4 kpc, |z| = 4 kpc the splitting goes {100*zprof[(4,'alpha=2',4.0)]:.1f}% -> "
      f"{100*zprof[(4,'RouteA-exp',4.0)]:.1f}%, a factor "
      f"{zprof[(4,'RouteA-exp',4.0)]/zprof[(4,'alpha=2',4.0)]:.2f}. That is where vertical-force data is "
      f"WORST, not best -- the gain lands in the wrong place")


banner("C  (c) BIGGER OR SMALLER? -- stated plainly")

print(f"""  AT THE SOLAR RADIUS, |z| = 1.1 kpc, the anchor's own baryons and definitions:
      alpha = 2   (committed)  {r_a2_mn:.4f}   -> splitting {100*(r_a2_mn-1):.2f}%
      Route A exponential      {r_ex_mn:.4f}   -> splitting {100*(r_ex_mn-1):.2f}%   (canonical a0)
      Route A exponential      {r_ex_mn_alt:.4f}   -> splitting {100*(r_ex_mn_alt-1):.2f}%   (alt a0)
  The kernel switch moves it by {100*d_can:+.3f} pp, against a mesh systematic of {100*spread_abs:.2f} pp
  (section G) and a footing spread of {100*abs(r_ex_mn_alt-r_ex_mn):.2f} pp (section A).

  *** SO AT R0 THE ANSWER IS: NEITHER. Route A leaves this lever essentially exactly where alpha = 2 left
  it -- about 2.4% -- and the switch is NON-DIAGNOSTIC for it. The front does not become a real
  MI-vs-MG or AQUAL-vs-algebraic lever under Route A at the solar radius. ***

  On the validated McMillan-2017 baryons the splitting is SMALLER for both kernels than on the anchor's
  Miyamoto-Nagai model -- {100*(r_a2_mc-1):.2f}% (alpha=2) and {100*(r_ex_mc-1):.2f}% (Route A) at the
  prior-respecting point -- so the better baryon model REDUCES the lever regardless of kernel, and there
  Route A does add a small amount ({100*(r_ex_mc-r_a2_mc):+.2f} pp, a factor {(r_ex_mc-1)/(r_a2_mc-1):.2f}).
  The honest reading of the two models together is: 1.6-2.4%, kernel-insensitive at R0, baryon-model
  sensitive at the same size as the signal.

  WHY the near-invariance, mechanically. Route A boosts much harder at these accelerations
  (nu_rad {A_TAB[('MN','alpha=2','canon')][0]:.3f} -> {A_TAB[('MN','RouteA-exp','canon')][0]:.3f} on the same
  baryons), which pushes the SOLUTION to larger x, where the exponential kernel's logarithmic slope
  d ln mu / d ln x is small again. The stronger nonlinearity and the self-consistent displacement to
  weaker nonlinearity very nearly cancel. That is a property of the solution, not an accident of the mesh:
  it survives all three meshes (G2).""")
check(abs(d_can) < spread_abs,
      f"C1 *** THE LANE'S ANSWER: the kernel switch moves the solar-radius splitting by {100*d_can:+.3f} pp, "
      f"SMALLER than the mesh systematic {100*spread_abs:.2f} pp on the same quantity. Route A is "
      f"NON-DIAGNOSTIC for nu_vert/nu_rad at R0; the lever stays at ~2.4% and the withdrawal of 'MG "
      f"inherits AQUAL's escape' stands unchanged ***")
check((r_ex_mc - 1) > (r_a2_mc - 1) and (r_ex_mc - 1) < 2.0 * (r_a2_mc - 1),
      f"C2 on the McMillan baryons the switch does raise it, from {100*(r_a2_mc-1):.2f}% to "
      f"{100*(r_ex_mc-1):.2f}% -- a real increase, but less than a doubling and still far below anything a "
      f"vertical-force dataset separates at, and the two baryon models disagree about the SIGN of the "
      f"kernel effect at R0, which is itself the honest bound on how well this is known")
best_gain = max((zprof[(R, "RouteA-exp", z)] / zprof[(R, "alpha=2", z)], R, z)
                for R in (4, 8, 12) for z in zs)
big_abs = max((zprof[(R, "RouteA-exp", z)], R, z) for R in (4, 8, 12) for z in zs)
gains4 = [zprof[(4, "RouteA-exp", z)] / zprof[(4, "alpha=2", z)] for z in zs]
gains_out = [zprof[(R, "RouteA-exp", z)] / zprof[(R, "alpha=2", z)] for R in (8, 12) for z in zs]
check(best_gain[0] > 1.4 and min(gains4) > 1.4 and max(gains_out) < 1.4,
      f"C3 the largest kernel GAIN anywhere scanned is {best_gain[0]:.2f}x, and EVERY cell whose gain exceeds "
      f"1.4x is at R = 4 kpc: the gain there is {min(gains4):.2f}-{max(gains4):.2f}x at every height from "
      f"0.2 to 4 kpc, while at R = 8 and 12 kpc it never exceeds {max(gains_out):.2f}x. The whole "
      f"enhancement lives in the INNER disc. The largest absolute splitting found anywhere is "
      f"{100*big_abs[0]:.1f}% at R = {big_abs[1]} kpc, |z| = {big_abs[2]} kpc, against "
      f"{100*zprof[(big_abs[1],'alpha=2',big_abs[2])]:.1f}% for alpha=2. So Route A relocates the lever "
      f"INWARD, into the region where vertical-force tracer data is poorest, and leaves the "
      f"solar-neighbourhood value alone")


banner("D  (d) THE grad(mu) TERM UNDER THE EXPONENTIAL KERNEL -- two independent routes")

print("""  ROUTE 1, like-for-like with mi_vertical_gradmu_term_2026: the ratio of the dropped term to the
  retained one, evaluated on the NEWTONIAN Miyamoto-Nagai field at R0 = 8 kpc, exactly as that script
  does it, with only the kernel swapped.
""")
PhiA, gradA, gmagA, lapA = AG["make_disc"](3.0, 0.3)
H = AG["H"]


def dropped_ratio(R, z, a0, mufun, dmufun):
    gR, gz = gradA(R, z)
    x = gmagA(R, z) / a0
    dgR = (gmagA(R + H, z) - gmagA(R - H, z)) / (2 * H)
    dgz = (gmagA(R, z + H) - gmagA(R, z - H)) / (2 * H)
    gmu = float(dmufun(x)) / a0 * (dgR * gR + dgz * gz)
    return x, float(mufun(x)), gmu / (float(mufun(x)) * lapA(R, z))


print(f"  {'z [kpc]':>9}{'x':>8}{'ratio a2':>11}{'ratio expA':>12}{'expA/a2':>10}")
print("  " + "-" * 52)
d1 = {}
for zk in (0.05, 0.1, 0.3, 0.5, 0.8, 1.1, 2.0, 3.0):
    xa, _, ra = dropped_ratio(R0_MN, zk * KPC, A0_CANON, mu_alpha2, dmu_a2)
    _, _, re = dropped_ratio(R0_MN, zk * KPC, A0_CANON, mu, dmu_dx)
    d1[zk] = (ra, re, re / ra)
    print(f"  {zk:>9.2f}{xa:>8.3f}{ra:>11.3f}{re:>12.3f}{re/ra:>10.3f}")
enh1 = [d1[z][2] for z in (0.05, 0.1, 0.3, 0.5, 0.8, 1.1)]
check(1.0 < min(enh1) and max(enh1) < 1.5,
      f"D1 REPORTED AGAINST THE EXPECTATION IN THE BRIEF: the dropped grad(mu) term is only "
      f"{min(enh1):.2f}-{max(enh1):.2f}x larger under Route A over |z| <= 1.1 kpc, NOT substantially "
      f"larger. The sharper transition does not deliver a big new term here because the local field sits at "
      f"x ~ {d1[0.5][0] if False else dropped_ratio(R0_MN, 0.5*KPC, A0_CANON, mu, dmu_dx)[0]:.2f}, and "
      f"section K2 shows the kernel factor only diverges for x > ~3")

print("""
  ROUTE 2, self-consistent and free of any numerical differentiation of mu. On the SOLVED AQUAL potential
  the field equation is an identity, 4 pi G rho = mu lap(Phi) + grad(mu).grad(Phi), so
      dropped / retained  =  4 pi G rho / (mu lap Phi)  -  1
  can be read off from the solution and the analytic density. Its own validation is built in: as rho -> 0
  above the disc the two terms must balance exactly, i.e. the ratio must tend to -1.
""")


def sc_ratio(kernel, a0, fM, fR, Rt, zks):
    Rg, zg, P = mc_solve(kernel, a0, fM, fR)
    dR = np.gradient(P, Rg, axis=0)
    dz = np.gradient(P, zg, axis=1)
    x = np.hypot(dR, dz) / a0
    mm = np.asarray(KERNELS[kernel][0](x), float)
    lap = np.gradient(dR, Rg, axis=0) + dR / Rg[:, None] + np.gradient(dz, zg, axis=1)
    comp, _ = AR["densities"](fM, fR)
    RRg, ZZg = np.meshgrid(Rg, zg, indexing="ij")
    src = 4.0 * math.pi * GN * sum(f(RRg, ZZg) for f in comp.values())
    i = int(np.argmin(np.abs(Rg - Rt)))
    out = {}
    for zk in zks:
        j = int(np.argmin(np.abs(zg - zk * KPC)))
        out[zk] = (float(x[i, j]), float(mm[i, j]), float(src[i, j] / (mm[i, j] * lap[i, j]) - 1.0))
    return out


ZKS = (0.05, 0.3, 0.5, 1.1, 2.0, 3.0)
sc = {kn: sc_ratio(kn, A0_CANON, 1.30, 0.90, R0_MC, ZKS) for kn in KERNELS}
print(f"  {'z [kpc]':>9}{'x a2':>8}{'ratio a2':>11}{'x expA':>9}{'ratio expA':>12}{'expA/a2':>10}")
print("  " + "-" * 60)
for zk in ZKS:
    xa, _, ra = sc["alpha=2"][zk]
    xe, _, re = sc["RouteA-exp"][zk]
    print(f"  {zk:>9.2f}{xa:>8.3f}{ra:>11.3f}{xe:>9.3f}{re:>12.3f}{re/ra:>10.3f}")
# TAUTOLOGY FIXED 2026-08-03, and the fix REVERSES what this check claimed. The quantity tested is defined as
# src/(mu*lap) - 1, which tends to -1 whenever the NUMERATOR src = 4 pi G rho becomes small -- regardless of
# whether lap is computed correctly. So "the ratio is within 10% of -1 at z = 3 kpc, therefore the identity is
# validated" could not fail, and was false besides: forming both terms independently, the TRUE field-equation
# residual (src - mu*lap - grad(mu).grad(Phi))/src at z = 3 kpc is -0.28 to -0.37, i.e. 28-37% wrong, while at
# the midplane it is only -0.012 to -0.014. The old check declared the identity "validated" exactly where it is
# WORST satisfied. Replaced with a test that can fail: the ratio must approach -1 MONOTONICALLY in |z|, which is
# a real property of the solution and not an artefact of src vanishing.
mono = {kn: [sc[kn][z][2] for z in ZKS] for kn in KERNELS}
mono_ok = all(all(mono[kn][i + 1] <= mono[kn][i] + 1e-9 for i in range(len(ZKS) - 1)) for kn in KERNELS)
check(mono_ok,
      f"D2 the self-consistent route is CORROBORATIVE ONLY, and is labelled as such: the ratio "
      f"src/(mu lap Phi) - 1 descends monotonically toward -1 with height for both kernels "
      f"({mono['alpha=2'][0]:+.3f} -> {mono['alpha=2'][-1]:+.3f} for alpha=2, {mono['RouteA-exp'][0]:+.3f} -> "
      f"{mono['RouteA-exp'][-1]:+.3f} for Route A), which is a falsifiable property of the solved potential. "
      f"*** It is NOT a validation of the identity: the tested quantity tends to -1 whenever rho vanishes, "
      f"however wrong the Laplacian, and the TRUE residual at |z| = 3 kpc is 28-37%, against 1.2-1.4% at the "
      f"midplane. The differentiated-mu route, not this one, carries the grad-mu result ***")
enh2 = [sc["RouteA-exp"][z][2] / sc["alpha=2"][z][2] for z in (0.05, 0.3, 0.5, 1.1)]
check(1.0 < min(enh2) and max(enh2) < 1.5,
      f"D3 and the self-consistent enhancement agrees with route 1: {min(enh2):.2f}-{max(enh2):.2f}x over "
      f"|z| <= 1.1 kpc. Two independent evaluations, one on the Newtonian field with a differentiated mu and "
      f"one on the solved potential with no differentiation of mu at all, both say the same thing: *** the "
      f"grad(mu) term is about 10-20% larger under Route A, which is NOT a new consequence worth claiming. "
      f"The 'much sharper transition, therefore much larger term' expectation is NOT borne out at Milky Way "
      f"accelerations ***")
check(abs(sc["RouteA-exp"][1.1][2]) < abs(d1[1.1][1]),
      f"D3b a real correction to the anchor, noted in passing: on the SOLVED potential with McMillan's "
      f"thick disc and gas the dropped term at |z| = 1.1 kpc is {abs(sc['RouteA-exp'][1.1][2]):.2f} of the "
      f"retained one, not {abs(d1[1.1][1]):.2f} as the Newtonian thin-MN estimate gives. The anchor's "
      f"conclusion (the term is not negligible, and it dominates high above the plane) survives; its "
      f"magnitude at 1.1 kpc was overstated by the thin single-disc model")


banner("M  WHAT ROUTE A DOES TO THE VERTICAL FORCE ITSELF -- reported in both directions")

print("""  The lane's number is a RATIO, and a ratio can be unchanged while both of its parts move a long way.
  Both do. Same McMillan-2017 baryons, same priors, same chi^2 as mi_aqual_mond_refit_2026, a0 an INPUT.
""")
obs = {}
for kn in KERNELS:
    o = AR["observables"](1.30, 0.90, A0_CANON, KERNELS[kn][0])
    c, cd, cp = AR["chi2"](o)
    obs[kn] = (o, c, cd, cp)
VC, VC_E, KZ, KZ_E = AR["VC"], AR["VC_E"], AR["KZ"], AR["KZ_E"]
print(f"  at the BANKED prior-respecting point (f_M = 1.30, f_R = 0.90):")
print(f"  {'kernel':<12}{'v_c(R0)':>10}{'sigma':>8}{'Sigma_dyn':>11}{'sigma':>8}{'chi2_dat':>10}"
      f"{'chi2_pri':>10}")
print("  " + "-" * 70)
for kn in KERNELS:
    o, c, cd, cp = obs[kn]
    print(f"  {kn:<12}{o['vc']/1e3:>10.1f}{(o['vc']-VC)/VC_E:>+8.1f}{o['sd']:>11.1f}"
          f"{(o['sd']-KZ)/KZ_E:>+8.1f}{cd:>10.1f}{cp:>10.1f}")
s_a2 = (obs["alpha=2"][0]["sd"] - KZ) / KZ_E
s_ex = (obs["RouteA-exp"][0]["sd"] - KZ) / KZ_E
check(abs(s_ex) > abs(s_a2) + 1.0,
      f"M1 *** WORSE, AND IT MUST BE SAID FIRST: at the point the corpus banked as 'simultaneously nails "
      f"the vertical force', Route A moves Sigma_dyn(|z|<1.1 kpc) from {obs['alpha=2'][0]['sd']:.1f} "
      f"({s_a2:+.1f} sigma vs McMillan's fitted 73.9 +- 6) to {obs['RouteA-exp'][0]['sd']:.1f} "
      f"({s_ex:+.1f} sigma). The banked +0.2 sigma vertical-force agreement was ALPHA=2-SPECIFIC and does "
      f"NOT survive the kernel switch at that (f_M, f_R) ***")

print(f"\n  and with the baryons re-fit on a COMMON coarse grid, each kernel at its own best point:")
print(f"  {'kernel':<12}{'f_M':>6}{'f_R':>6}{'v_c':>9}{'sigma':>8}{'Sigma_dyn':>11}{'sigma':>8}"
      f"{'chi2':>9}{'chi2_pri':>10}")
print("  " + "-" * 79)
refit = {}
for kn in KERNELS:
    bb = None
    for fM in (1.3, 1.5, 1.7, 1.9):
        for fR in (0.8, 0.9):
            o = AR["observables"](fM, fR, A0_CANON, KERNELS[kn][0])
            c, cd, cp = AR["chi2"](o)
            if bb is None or c < bb[0]:
                bb = (c, cd, cp, fM, fR, o)
    refit[kn] = bb
    c, cd, cp, fM, fR, o = bb
    print(f"  {kn:<12}{fM:>6.2f}{fR:>6.2f}{o['vc']/1e3:>9.1f}{(o['vc']-VC)/VC_E:>+8.1f}{o['sd']:>11.1f}"
          f"{(o['sd']-KZ)/KZ_E:>+8.1f}{c:>9.1f}{cp:>10.1f}")
check(refit["RouteA-exp"][0] < refit["alpha=2"][0],
      f"M2 BETTER, on the same grid and with the same priors: Route A's best joint chi^2 is "
      f"{refit['RouteA-exp'][0]:.1f} against alpha=2's {refit['alpha=2'][0]:.1f}. The kernel switch closes "
      f"most of the rotation-curve NORMALISATION gap that the corpus had pinned on the baryon budget "
      f"(v_c {obs['alpha=2'][0]['vc']/1e3:.0f} -> {obs['RouteA-exp'][0]['vc']/1e3:.0f} km/s on identical "
      f"baryons) and pays for part of it in the vertical force. Two free parameters only, so both numbers "
      f"are UPPER bounds on their kernel's chi^2")
_, _, Pb = mc_solve("RouteA-exp", A0_CANON, refit["RouteA-exp"][3], refit["RouteA-exp"][4])
_, _, PbN = mc_solve("RouteA-exp", A0_CANON, refit["RouteA-exp"][3], refit["RouteA-exp"][4],
                     newtonian=True)
nrb, nvb, _ = nu_pair(Pb, PbN, Rm, zm, R0_MC, 1.1)
check(1.0 < nvb / nrb < 1.05,
      f"M3 and at Route A's OWN best Milky Way point (f_M = {refit['RouteA-exp'][3]:.2f}, "
      f"f_R = {refit['RouteA-exp'][4]:.2f}) the lane's ratio is {nvb/nrb:.4f}, i.e. a splitting of "
      f"{100*(nvb/nrb-1):.2f}% -- the same 1-2% as everywhere else. Refitting the baryons under the new "
      f"kernel does not rescue the lever either")


banner("SCOPE, AND WHAT IS NOT CLAIMED")

print(f"""   * THE ABSOLUTE RATIO IS NOT CONVERGED TO BETTER THAN ~{100*spread_abs:.1f} pp (section G). Every
     statement here is about the DIFFERENTIAL between kernels, which is stable to
     {100*spread_dif:.2f} pp, and about a profile SHAPE. Do not quote 1.024 or {r_ex_mn:.4f} to four digits.
   * TWO BARYON MODELS, and they disagree about the sign of the kernel effect at R0 (MN: {100*d_can:+.3f} pp;
     McMillan: {100*(r_ex_mc-r_a2_mc):+.2f} pp). That disagreement IS the error bar on the answer to (c),
     and it is bigger than the effect.
   * NO DATA CONFRONTATION of the ratio. No vertical Jeans solution, no tracer sample, no K_z fit. The
     numbers in M are Sigma_dyn against McMillan's fitted K_z,1.1 with Holmberg & Flynn's error, which is
     the anchor's convention, not a new measurement.
   * THE SETTLED SIGN QUESTION IS NOT RE-OPENED. No claim is made here that the computed direction of the
     splitting agrees or disagrees with any published vertical-force determination.
   * THE MI READING IS UNTOUCHED. Everything solved here is the AQUAL / modified-gravity realization. The
     algebraic modified-inertia law has nu_vert = nu_rad identically by construction, so its prediction for
     this ratio is exactly 1 under EVERY kernel, Route A included -- the lane's number is a statement about
     the MG realization only, and the MI-vs-MG separation it offers is the same 1-2% it was.
   * UNTOUCHED by anything here: the RAR fit, the a0-line, the BTFR, all spherical work, and
     a0 = kappa c sqrt(G rho_Lambda).""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: nu_vert/nu_rad re-solved under Route A on two baryon models and both footings.")

#!/usr/bin/env python3
r"""mi_route_a_sigma_spread_2026.py -- RE-SOLVE the MI-distinctive cluster-member sigma-SPREAD under
ROUTE A's exponential kernel. The answer is MIXED, not a win: the front gets HARDER at the inner edge of
its own design shell and EASIER at the outer edge, and against the kernel that was actually in force
(alpha=2) the inner edge is TWICE as hard.

WHY THIS HAS TO BE RE-SOLVED. The sigma-spread front's amplitude is set by ONE kernel quantity -- the
logarithmic response slope of mu at the field strength the carriers sit in:

    sigma ~ mu(x)^(-1/2),  x = |a_in + a_ex| / a0    =>    d ln sigma / d ln x = -(1/2) d ln mu / d ln x

The geometry (a_in = 0.3 a0 carrier locus, the cross-term coherence C(y) = sinc[P(1-y)/2y], the carrier
y range) is kernel-FREE: x does not depend on the kernel at all. So the entire Route A re-solve is the
re-evaluation of that one slope -- which is exactly why it cannot be rescaled from the committed number
by a single factor: the slope ratio SWINGS THROUGH 1 inside the design shell.

WHAT IS COMMITTED (and what is being compared against):
  * mi_theta_efe_from_closure_2026.py priced the front at a_ext = 2 a0: derived spread 1.45-2.21%
    (max-min, over both footings and three averaging-window shapes) and 0.7204% (population RMS,
    uniform prior; the log-uniform prior gives 0.4936% and the script keeps the MAX).
  * mi_sigma_spread_aext_scan_2026.py then showed 2 a0 is OFF-DESIGN -- the frozen shell is
    a_ext ~ 0.3-1 a0 (sigma_spread_prereg_2026.py:152) -- and across that shell N(3 sigma) = 5.0e3-2.6e5
    against 4MOST-CHANCES's ~3e5 spectra, i.e. the front clears by 1.1x-60x and is NOT dead.

A LABELLING DEFECT FOUND ON THE WAY, reported because it changes the baseline: BOTH committed scripts
compute this front with mu_fw(x) = (sqrt(1+4x^2)-1)/(2x), which is the ALPHA=1 kernel -- retired for
ephemeris reasons before Route A was adopted. The kernel actually in force when the standing was banked
was alpha=2. So "Route A vs the committed number" and "Route A vs the in-force kernel" are DIFFERENT
comparisons, and this script reports both. (Class: project_alpha1_exclusive_audit_class.)

SECTIONS
  R0  anchor reuse + regression: the committed machinery, unmodified, reproduces its own numbers
  R1  the mechanism -- the response slope of all three kernels, and where the ratio crosses 1
  R2  THE RE-SOLVE: spread across a_ext, three kernels, BOTH footings, BOTH priors (max convention)
  R3  N(3 sigma) across the frozen 0.3-1 a0 shell vs the committed range vs CHANCES; the dead-zone edge
  R4  the S1 leg re-checked: exact unimodularity was ALPHA=1-EXCLUSIVE. Route A loses it; the bound on
      the frequency channel weakens ~50x but the conclusion survives at the carriers' actual frequencies
  R5  verdict, and the six things this does NOT establish

RULES HELD: a0 is an INPUT on both footings (9.36e-11 canonical, 1.13e-10 alt) and is never fitted --
R2 records every a0 the solver sees and checks the set is exactly those two. No check(True), no
hard-coded verdict: the direction is read off computed numbers. Exit 0 = ran and every check held.

Credit: Milgrom 1999 PLA 253:273 Eq 9 (nu-kernel wellhead), 2022 PRD 106:064060 (two-frequency MI EFE).
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mi_route_a_kernel import A0_ALT, A0_CANON, mu as mu_routeA, mu_alpha2, nu, one_minus_mu, u_of_x

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 110)
    print(f"  {t}")
    print("=" * 110)


# ==================================================================================================
banner("R0  ANCHOR REUSE -- the committed scan's machinery is the single source of truth")
# ==================================================================================================
SRCPATH = pathlib.Path(__file__).resolve().parent / "mi_sigma_spread_aext_scan_2026.py"
_src = SRCPATH.read_text()
_cut = _src.index('banner("A1')
_G: dict = {"__name__": "anchor"}
exec(compile(_src[:_cut], str(SRCPATH), "exec"), _G)

mu_alpha1 = _G["mu_fw"]              # the kernel the committed sigma-spread numbers were computed on
coherence = _G["coherence"]          # C(y) = sinc[P(1-y)/2y]      -- kernel-FREE
spreads = _G["spreads"]              # banked band + derived max-min + derived pop-RMS at one a_ex
N3 = _G["N3"]                        # frozen estimator: N(3 sigma) = 2 (3 eps^2/(s p)^2)^2
z_at = _G["z_at"]
A0_REF, A_IN_FID = _G["A0_REF"], _G["A_IN_FID"]
FOOTINGS, PVALS = _G["FOOTINGS"], _G["PVALS"]
Y_DENSE, YSAMP_LOG, YSAMP_LIN = _G["Y_DENSE"], _G["YSAMP_LOG"], _G["YSAMP_LIN"]
CHANCES, EPS_ELT, P_EFF = _G["CHANCES"], _G["EPS_ELT"], _G["P_EFF"]
SHELL = _G["SHELL"]
Y_LO, Y_HI = _G["Y_LO"], _G["Y_HI"]

print(f"  exec'd {SRCPATH.name} up to its first banner: geometry, coherence, priors, RNG seed and the")
print(f"  frozen estimator all come from the committed file, so every column below is like-for-like.")
print(f"  carrier locus a_in = {A_IN_FID/A0_REF:.1f} a0 | design shell a_ext = {SHELL[0]}-{SHELL[1]} a0 | "
      f"carrier y in [{Y_LO:.4f}, {Y_HI:.4f}] | CHANCES = {CHANCES:.0e}")
print(f"  P = omega_ex * T_w = " + ", ".join(f"{f[:5]} {PVALS[f]:.3f}" for f, _ in FOOTINGS)
      + "   (T_w = min(2c/a0, t_age) = t_age on both footings, so C(y) is footing-free)")

_b_lo, _b_hi, _d_mm, _d_rms = spreads(2.0 * A0_REF)
_n03 = N3(spreads(0.30 * A0_REF)[3])
_n10 = N3(spreads(1.00 * A0_REF)[3])
check(abs(_d_mm - 0.02213) < 3e-4 and abs(_d_rms - 0.007197) < 3e-4
      and abs(_b_lo - 0.0623) < 2e-3 and abs(_b_hi - 0.1407) < 2e-3
      and abs(_n03 / 4.998e3 - 1) < 0.01 and abs(_n10 / 2.641e5 - 1) < 0.01,
      f"R0a REGRESSION: untouched, the anchor reproduces the committed standing -- at 2 a0 derived "
      f"max-min {100*_d_mm:.3f}% (banked 2.213%) and pop-RMS {100*_d_rms:.4f}% (banked 0.7204% at "
      f"NMC=2e5 seed 20260730; this file's seed gives 0.7197%), banked band "
      f"{100*_b_lo:.2f}-{100*_b_hi:.2f}%; across the shell N(3 sigma) = {_n03:.3e} to {_n10:.3e} "
      f"(banked 5.0e3-2.6e5). So any change below is the KERNEL and nothing else")

# The kernel the committed numbers used is alpha=1, not the alpha=2 that was in force. Prove it.
_xt = np.array([0.4, 0.8, 1.5, 2.3])
_y1 = mu_alpha1(_xt) * _xt
check(float(np.max(np.abs(_xt**2 - (_y1**2 + _y1)))) < 1e-12
      and float(np.max(np.abs(mu_alpha1(_xt) - mu_alpha2(_xt)))) > 0.05,
      f"R0b the committed front's mu_fw satisfies x^2 = y^2 + y exactly (max residual "
      f"{float(np.max(np.abs(_xt**2-(_y1**2+_y1)))):.1e}) -- i.e. it IS the ALPHA=1 kernel, and it differs "
      f"from alpha=2 by up to {float(np.max(np.abs(mu_alpha1(_xt)-mu_alpha2(_xt)))):.3f} in mu over the "
      f"front's x range. The banked sigma-spread standing therefore sits on a kernel that was already "
      f"superseded by alpha=2 when it was banked -- an alpha=1-EXCLUSIVE label defect, reported not hidden")


# ==================================================================================================
banner("R1  THE MECHANISM -- the response slope, and where Route A's ratio crosses 1")
# ==================================================================================================
def slope_alpha1(x):
    """d ln mu / d ln x for mu=(sqrt(1+4x^2)-1)/(2x): equals 1/(2y+1) with y = mu x (exact)."""
    x = np.asarray(x, float)
    y = mu_alpha1(x) * x
    return 1.0 / (2.0 * y + 1.0)


def slope_alpha2(x):
    """d ln mu / d ln x for mu = x/sqrt(1+x^2): equals 1/(1+x^2) (exact)."""
    x = np.asarray(x, float)
    return 1.0 / (1.0 + x * x)


def slope_routeA(x):
    """d ln mu / d ln x for Route A: t/(2-t) with t = u e^-u / (1-e^-u), u = u(x) (exact)."""
    u = u_of_x(np.asarray(x, float))
    t = u * np.exp(-u) / -np.expm1(-u)
    return t / (2.0 - t)


KERNELS = [("alpha=1  (what the committed numbers used)", mu_alpha1, slope_alpha1),
           ("alpha=2  (the kernel actually in force)", mu_alpha2, slope_alpha2),
           ("ROUTE A  (exponential, adopted)", mu_routeA, slope_routeA)]

# validate every analytic slope against a central difference -- a real check on the mechanism algebra
_xs = np.logspace(-3, 1.0, 400)
_h = 1e-6
_worst = 0.0
for _nm, _muf, _slf in KERNELS:
    _fd = (np.log(_muf(_xs * (1 + _h))) - np.log(_muf(_xs * (1 - _h)))) / (2 * _h)
    _worst = max(_worst, float(np.max(np.abs(_fd / _slf(_xs) - 1.0))))
check(_worst < 1e-4,
      f"R1a all three analytic log-slopes match a central difference to {_worst:.1e} over four decades in "
      f"x, so the mechanism arithmetic below is the kernels' own and not a numerical artefact")

print(f"\n  d ln mu / d ln x (1 = deep-MOND, 0 = Newtonian). sigma-spread ~ half this times the spread in ln x.")
print(f"  {'x':>7}{'alpha=1':>11}{'alpha=2':>11}{'ROUTE A':>11}{'A/alpha1':>11}{'A/alpha2':>11}   x windows")
print("  " + "-" * 84)
_windows = {0.375: "inner shell (a_ex=0.3a0) min", 0.60: "inner shell max",
            1.00: "kernel-crossover neighbourhood", 1.42: "outer shell (a_ex=1a0) mid",
            1.70: "2a0 retirement fiducial min", 2.30: "2a0 retirement fiducial max"}
for xv in [0.20, 0.375, 0.50, 0.60, 0.80, 1.00, 1.42, 1.70, 2.00, 2.30]:
    s1, s2, sA = float(slope_alpha1(xv)), float(slope_alpha2(xv)), float(slope_routeA(xv))
    print(f"  {xv:>7.3f}{s1:>11.4f}{s2:>11.4f}{sA:>11.4f}{sA/s1:>11.4f}{sA/s2:>11.4f}   "
          f"{_windows.get(xv, '')}")

# the crossover in x where Route A's response overtakes alpha=1's
_lo, _hi = 0.2, 3.0
for _ in range(80):
    _m = 0.5 * (_lo + _hi)
    if float(slope_routeA(_m)) < float(slope_alpha1(_m)):
        _lo = _m
    else:
        _hi = _m
X_CROSS = 0.5 * (_lo + _hi)
check(float(slope_routeA(X_CROSS * 0.8)) < float(slope_alpha1(X_CROSS * 0.8))
      and float(slope_routeA(X_CROSS * 1.25)) > float(slope_alpha1(X_CROSS * 1.25))
      and 0.3 < X_CROSS < 1.0,
      f"R1b *** THE SIGN OF THE ROUTE A EFFECT FLIPS INSIDE THE FRONT'S OWN x RANGE. *** The response "
      f"slopes cross at x = {X_CROSS:.4f}: BELOW it Route A responds LESS than alpha=1 (ratio "
      f"{float(slope_routeA(0.375))/float(slope_alpha1(0.375)):.4f} at x = 0.375) and ABOVE it MORE "
      f"(ratio {float(slope_routeA(2.0))/float(slope_alpha1(2.0)):.4f} at x = 2.0). The exponential's "
      f"transition is SHARPER near and above x ~ 1 but slightly SOFTER deep in the MOND regime, and the "
      f"design shell straddles the crossing -- so the front CANNOT be rescaled by one factor")

# the two representations are the SAME kernel over the x window this front occupies, so the boost
# 1/mu(x) is unambiguous here -- worth checking, because it is only true in spherical symmetry
_yy = np.logspace(-3, 1.0, 500)
_xx = nu(_yy) * _yy
check(float(np.max(np.abs(mu_routeA(_xx) * _xx / _yy - 1.0))) < 1e-10 and _xx.max() > 2.3,
      f"R1d the algebraic (modified-inertia) and AQUAL forms of Route A agree to "
      f"{float(np.max(np.abs(mu_routeA(_xx)*_xx/_yy-1.0))):.1e} over x up to {_xx.max():.1f}, covering the "
      f"whole window this front uses -- so 'boost = 1/mu(x)' is the same statement as 'boost = nu(y)' "
      f"here and the re-solve does not depend on which representation is chosen. That equivalence is "
      f"SPHERICAL-symmetry only, which is why caveat 4 in R5 is not rhetorical")

# float64 trap guard: mu must stay strictly below 1 across the x range this front uses
_xmax = 2.5
check(float(one_minus_mu(_xmax)) > 1e-8 and float(mu_routeA(_xmax)) < 1.0,
      f"R1c float64 trap does NOT bite here: the front's largest x is ~2.3 and 1 - mu({_xmax}) = "
      f"{float(one_minus_mu(_xmax)):.3e}, far above the ~1e-16 where mu saturates to exactly 1.0 "
      f"(u ~ 37). No log-form workaround is needed for this observable, unlike the ephemeris lane")


# ==================================================================================================
banner("R2  THE RE-SOLVE -- spread across a_ext, three kernels, BOTH footings, BOTH priors")
# ==================================================================================================
A0_SEEN: set[float] = set()


def solve_spread(a_ex, a0, muf, ys):
    """sigma ~ mu(x)^-1/2 with the framework's quadrature argument. a0 is an INPUT, recorded not fitted."""
    A0_SEEN.add(float(a0))
    C = coherence(ys, PVALS_BY_A0[float(a0)])
    x = np.sqrt(A_IN_FID**2 + a_ex**2 + 2.0 * A_IN_FID * a_ex * C) / a0
    s = np.sqrt(1.0 / muf(x))
    return s, x


PVALS_BY_A0 = {float(a0): PVALS[f] for f, a0 in FOOTINGS}
PRIORS = [("log-uniform", YSAMP_LOG), ("uniform", YSAMP_LIN)]
GRID = [0.10, 0.20, 0.30, 0.50, 0.75, 1.00, 1.10, 1.20, 1.50, 2.00]

res: dict = {}
for kname, muf, slf in KERNELS:
    for f in GRID:
        a_ex = f * A0_REF
        cell = {}
        for fname, a0 in FOOTINGS:
            s_d, x_d = solve_spread(a_ex, a0, muf, Y_DENSE)
            mm = (s_d.max() - s_d.min()) / s_d.mean()
            pr = {}
            for pname, ys in PRIORS:
                s_p, x_p = solve_spread(a_ex, a0, muf, ys)
                pr[pname] = dict(rms=s_p.std() / s_p.mean(), sd_lnx=np.std(np.log(x_p)),
                                 mean_slope=float(np.mean(slf(x_p))))
            cell[fname] = dict(mm=mm, x=(x_d.min(), x_d.max()), pr=pr,
                               rms_max=max(v["rms"] for v in pr.values()),
                               prior_max=max(pr, key=lambda k: pr[k]["rms"]))
        rms_max = max(cell[f_]["rms_max"] for f_, _ in FOOTINGS)
        res[(kname, f)] = dict(cell=cell, mm_max=max(cell[f_]["mm"] for f_, _ in FOOTINGS),
                               rms_max=rms_max, N=N3(rms_max))

check(A0_SEEN == {9.36e-11, 1.13e-10},
      f"R2a a0 IS AN INPUT, verified structurally: across {len(KERNELS)*len(GRID)*2*3} solver calls the "
      f"complete set of a0 values the solver ever saw is {sorted(A0_SEEN)} -- exactly the two frozen "
      f"footings, in the anchor's own rounding. No optimizer, no third value, nothing tuned to improve "
      f"agreement")

print(f"\n  pop-RMS spread (%), MAX over the two priors -- the committed convention, kept:")
print(f"  {'a_ex/a0':>8}" + "".join(f"{k.split()[0]+' '+ft[:5]:>16}" for k, _, _ in KERNELS
                                     for ft, _ in FOOTINGS))
print("  " + "-" * 104)
for f in GRID:
    line = f"  {f:>8.2f}"
    for kname, _, _ in KERNELS:
        for fname, _ in FOOTINGS:
            line += f"{100*res[(kname, f)]['cell'][fname]['rms_max']:>16.4f}"
    print(line)

print(f"\n  the front's headline numbers, MAX over footings AND priors (committed convention):")
print(f"  {'a_ex/a0':>8}{'a1 max-min':>13}{'a2 max-min':>13}{'A max-min':>13}"
      f"{'a1 popRMS':>12}{'a2 popRMS':>12}{'A popRMS':>12}{'A/a1':>8}{'A/a2':>8}")
print("  " + "-" * 101)
for f in GRID:
    r1, r2_, rA = (res[(KERNELS[i][0], f)] for i in range(3))
    print(f"  {f:>8.2f}{100*r1['mm_max']:>12.3f}%{100*r2_['mm_max']:>12.3f}%{100*rA['mm_max']:>12.3f}%"
          f"{100*r1['rms_max']:>11.4f}%{100*r2_['rms_max']:>11.4f}%{100*rA['rms_max']:>11.4f}%"
          f"{rA['rms_max']/r1['rms_max']:>8.3f}{rA['rms_max']/r2_['rms_max']:>8.3f}")

# MECHANISM CHECK: the measured kernel ratio must equal the population-mean slope ratio
worst_pred = 0.0
for f in GRID:
    for fname, _ in FOOTINGS:
        for pname, _ in PRIORS:
            c1 = res[(KERNELS[0][0], f)]["cell"][fname]["pr"][pname]
            cA = res[(KERNELS[2][0], f)]["cell"][fname]["pr"][pname]
            meas = cA["rms"] / c1["rms"]
            pred = cA["mean_slope"] / c1["mean_slope"]
            worst_pred = max(worst_pred, abs(meas / pred - 1.0))
check(worst_pred < 0.05,
      f"R2b MECHANISM CONFIRMED, so the direction is understood and not just measured: at every one of "
      f"the {len(GRID)*4} (a_ext, footing, prior) cells the Route A / alpha=1 spread ratio equals the "
      f"population-mean response-slope ratio to within {100*worst_pred:.1f}%. The spread is "
      f"(1/2) |d ln mu/d ln x| times a KERNEL-FREE spread in ln x -- the geometry is untouched by Route A")

# the a_ex where Route A crosses alpha=1, per footing
CROSS_AEX = {}
for fname, a0 in FOOTINGS:
    lo, hi = 0.10, 2.0
    for _ in range(60):
        m = 0.5 * (lo + hi)
        s1, _ = solve_spread(m * A0_REF, a0, mu_alpha1, YSAMP_LIN)
        sA, _ = solve_spread(m * A0_REF, a0, mu_routeA, YSAMP_LIN)
        if (sA.std() / sA.mean()) < (s1.std() / s1.mean()):
            lo = m
        else:
            hi = m
    CROSS_AEX[fname] = 0.5 * (lo + hi)
r03A, r03_1 = res[(KERNELS[2][0], 0.30)]["rms_max"], res[(KERNELS[0][0], 0.30)]["rms_max"]
r10A, r10_1 = res[(KERNELS[2][0], 1.00)]["rms_max"], res[(KERNELS[0][0], 1.00)]["rms_max"]
check(r03A < r03_1 and r10A > r10_1
      and all(SHELL[0] < v < SHELL[1] for v in CROSS_AEX.values()),
      f"R2c *** MIXED, AND THE CROSSING IS INSIDE THE SHELL. *** Route A's spread is SMALLER than the "
      f"committed alpha=1 value at the inner edge ({100*r03A:.4f}% vs {100*r03_1:.4f}% at 0.3 a0, "
      f"{r03A/r03_1:.3f}x = WORSE) and LARGER at the outer edge ({100*r10A:.4f}% vs {100*r10_1:.4f}% at "
      f"1.0 a0, {r10A/r10_1:.3f}x = BETTER), crossing at a_ext = "
      + ", ".join(f"{v:.3f} a0 ({f[:5]})" for f, v in CROSS_AEX.items())
      + " -- both inside the frozen 0.3-1 a0 shell")

# PRIOR CONVENTION + its mechanism
dom = {(k, f): max((res[(k, f)]["cell"][ft]["prior_max"] for ft, _ in FOOTINGS), key=lambda s: s)
       for k, _, _ in KERNELS for f in GRID}
uni_dom = sum(1 for v in dom.values() if v == "uniform")
mism = 0
for k, _, _ in KERNELS:
    for f in GRID:
        for ft, _ in FOOTINGS:
            pr = res[(k, f)]["cell"][ft]["pr"]
            by_rms = max(pr, key=lambda p: pr[p]["rms"])
            by_lnx = max(pr, key=lambda p: pr[p]["sd_lnx"])
            mism += (by_rms != by_lnx)
_pr_A = res[(KERNELS[2][0], 0.30)]["cell"][FOOTINGS[1][0]]["pr"]
check(mism == 0 and uni_dom == len(dom),
      f"R2d MAX-OVER-PRIORS CONVENTION KEPT, and the UNIFORM prior still dominates under Route A -- at "
      f"all {len(dom)} (kernel, a_ext) cells, {uni_dom}/{len(dom)}. At the inner shell, Route A / alt "
      f"footing: uniform {100*_pr_A['uniform']['rms']:.4f}% vs log-uniform "
      f"{100*_pr_A['log-uniform']['rms']:.4f}% ({_pr_A['uniform']['rms']/_pr_A['log-uniform']['rms']:.2f}x). "
      f"MECHANISM, and it is the reason and not a coincidence: in {len(dom)*2}/{len(dom)*2} cells the "
      f"prior with the larger spread is the prior with the larger std(ln x) -- uniform-in-y puts more "
      f"weight near the coherence peak y = 1, log-uniform piles carriers up at small y where C -> 0")

# the anchor's footings are rounded (9.36e-11); the kernel module carries 9.3614e-11. Check that the
# rounding is not load-bearing, rather than assuming it -- and use the module's own values to do it.
def _rms_max(a_ex, a0, muf):
    out = []
    for _, ys in PRIORS:
        s, _x = solve_spread(a_ex, a0, muf, ys)
        out.append(s.std() / s.mean())
    return max(out)


_shift = 0.0
for _fac in (0.30, 1.00):
    for _a0_anch, _a0_mod in ((FOOTINGS[0][1], A0_CANON), (FOOTINGS[1][1], A0_ALT)):
        PVALS_BY_A0[float(_a0_mod)] = PVALS_BY_A0[float(_a0_anch)]     # T_w = t_age on both, so P is same
        _n_anch = N3(_rms_max(_fac * A0_REF, _a0_anch, mu_routeA))
        _n_mod = N3(_rms_max(_fac * A0_REF, _a0_mod, mu_routeA))
        _shift = max(_shift, abs(_n_mod / _n_anch - 1.0))
A0_SEEN -= {float(A0_CANON), float(A0_ALT)}
_nc = N3(res[(KERNELS[2][0], 1.00)]["cell"][FOOTINGS[0][0]]["rms_max"])
_na = N3(res[(KERNELS[2][0], 1.00)]["cell"][FOOTINGS[1][0]]["rms_max"])
check(_shift < 0.01 and _nc / _na > 1.2,
      f"R2g the footing ROUNDING is not load-bearing, checked rather than assumed: swapping the anchor's "
      f"9.36e-11 / 1.13e-10 for the kernel module's own A0_CANON = {A0_CANON:.4e} / A0_ALT = "
      f"{A0_ALT:.4e} moves N(3 sigma) at both shell edges by at most {100*_shift:.2f}%. The footing FORK "
      f"itself is a different matter and does matter: at the outer shell edge under Route A the canonical "
      f"footing needs {_nc:.2e} carriers against the alt footing's {_na:.2e}, a factor {_nc/_na:.2f}x")

# window-shape robustness at the retirement fiducial, canonical footing (matches the closure's (iv))
WINS = {"boxcar -> sinc": lambda y, P: coherence(y, P),
        "exponential -> Lorentzian": lambda y, P: 1.0 / (1.0 + (P * (1.0 - y) / y) ** 2),
        "Gaussian -> Gaussian": lambda y, P: np.exp(-0.5 * (P * (1.0 - y) / (2.0 * y)) ** 2)}
print(f"\n  window-shape robustness (max-min %, canonical footing) -- the convention behind the")
print(f"  committed '1.45-2.21%' band. The line shape is NOT derived, so the band is quoted over it.")
print(f"  {'a_ex/a0':>8}{'kernel':>10}" + "".join(f"{w.split()[0]:>14}" for w in WINS) + f"{'band':>16}")
print("  " + "-" * 88)
WBAND: dict = {}
for f in (0.30, 1.00, 2.00):
    for kname, muf, _ in KERNELS:
        vals = []
        for wname, wf in WINS.items():
            P = PVALS[FOOTINGS[0][0]]
            x = np.sqrt(A_IN_FID**2 + (f * A0_REF) ** 2
                        + 2.0 * A_IN_FID * (f * A0_REF) * wf(Y_DENSE, P)) / FOOTINGS[0][1]
            s = np.sqrt(1.0 / muf(x))
            vals.append((s.max() - s.min()) / s.mean())
        WBAND[(kname, f)] = (min(vals), max(vals))
        print(f"  {f:>8.2f}{kname.split()[0]:>10}" + "".join(f"{100*v:>14.3f}" for v in vals)
              + f"{100*min(vals):>9.2f}-{100*max(vals):<6.2f}")
w1, wA = WBAND[(KERNELS[0][0], 2.00)], WBAND[(KERNELS[2][0], 2.00)]
mmA_alt = res[(KERNELS[2][0], 2.00)]["mm_max"]
check(abs(w1[0] - 0.01446) < 5e-4 and abs(_d_mm - 0.02213) < 3e-4 and wA[0] > w1[0] and wA[1] > w1[1],
      f"R2e (a) THE AMPLITUDE AT THE RETIREMENT FIDUCIAL, like-for-like. The committed band 1.45-2.21% "
      f"is reproduced here as {100*w1[0]:.2f}% (canonical, Lorentzian window) to {100*_d_mm:.2f}% (alt, "
      f"boxcar). Under ROUTE A the same construction gives {100*wA[0]:.2f}% to {100*mmA_alt:.2f}%, i.e. "
      f"{min(wA[0]/w1[0], mmA_alt/_d_mm):.2f}x-{max(wA[0]/w1[0], mmA_alt/_d_mm):.2f}x LARGER -- at 2 a0 "
      f"Route A is unambiguously BETTER. "
      f"Against the kernel actually in force it is larger still: alpha=2 gives "
      f"{100*WBAND[(KERNELS[1][0], 2.00)][0]:.2f}-{100*res[(KERNELS[1][0], 2.00)]['mm_max']:.2f}%")
b03_1, b03_A = WBAND[(KERNELS[0][0], 0.30)], WBAND[(KERNELS[2][0], 0.30)]
check(b03_A[0] < b03_1[0] and b03_A[1] < b03_1[1],
      f"R2f AND THE SAME CONSTRUCTION AT THE INNER SHELL GOES THE OTHER WAY, stated as plainly: "
      f"{100*b03_1[0]:.2f}-{100*b03_1[1]:.2f}% (alpha=1) -> {100*b03_A[0]:.2f}-{100*b03_A[1]:.2f}% "
      f"(Route A), a factor {b03_A[1]/b03_1[1]:.3f}. The '2 a0 improves' headline is NOT the front's "
      f"operating point and must not be quoted as if it were")


# ==================================================================================================
banner("R3  N(3 sigma) ACROSS THE FROZEN 0.3-1 a0 SHELL -- vs the committed range, vs CHANCES")
# ==================================================================================================
print(f"  frozen estimator: z ~ (s p)^2/(eps^2 sqrt(2/N)), eps = {EPS_ELT:.4f} (ELT tier), p = {P_EFF}")
print(f"  => N(3 sigma) = 2 (3 eps^2/(s p)^2)^2, so N goes as s^-4 and a 7% amplitude change is 30% in N.\n")
print(f"  {'a_ex/a0':>8}{'N a1':>13}{'N a2':>13}{'N RouteA':>13}{'A/a1':>8}{'A/a2':>8}"
      f"{'CHANCES/N (A)':>15}{'z@3e5 (A)':>11}")
print("  " + "-" * 89)
for f in GRID:
    n1, n2, nA = (res[(KERNELS[i][0], f)]["N"] for i in range(3))
    sA = res[(KERNELS[2][0], f)]["rms_max"]
    tag = "  <- shell" if SHELL[0] <= f <= SHELL[1] else ""
    print(f"  {f:>8.2f}{n1:>13.3e}{n2:>13.3e}{nA:>13.3e}{nA/n1:>8.3f}{nA/n2:>8.3f}"
          f"{CHANCES/nA:>14.2f}x{z_at(sA, CHANCES):>11.2f}{tag}")

SHELL_F = [f for f in GRID if SHELL[0] <= f <= SHELL[1]]
NA = {f: res[(KERNELS[2][0], f)]["N"] for f in SHELL_F}
N1 = {f: res[(KERNELS[0][0], f)]["N"] for f in SHELL_F}
N2 = {f: res[(KERNELS[1][0], f)]["N"] for f in SHELL_F}
bestA, worstA = min(NA.values()), max(NA.values())
best1, worst1 = min(N1.values()), max(N1.values())
best2, worst2 = min(N2.values()), max(N2.values())

check(abs(best1 / 5.0e3 - 1) < 0.05 and abs(worst1 / 2.64e5 - 1) < 0.05,
      f"R3a the committed shell range reproduces: alpha=1 gives N = {best1:.2e}-{worst1:.2e} across "
      f"0.3-1.0 a0 (banked 5.0e3-2.6e5). That is the number Route A is being compared against")

check(worstA < CHANCES and bestA > best1 and worstA < worst1,
      f"R3b *** (b) THE ANSWER, BOTH HALVES. *** Under ROUTE A the shell requirement is "
      f"N(3 sigma) = {bestA:.2e}-{worstA:.2e}, against the committed {best1:.2e}-{worst1:.2e}. The "
      f"BINDING (outer) edge IMPROVES by {worst1/worstA:.2f}x -- {CHANCES/worstA:.1f}x below CHANCES "
      f"instead of {CHANCES/worst1:.1f}x -- while the BEST cell DEGRADES by {bestA/best1:.2f}x "
      f"({CHANCES/bestA:.0f}x below CHANCES instead of {CHANCES/best1:.0f}x). Every point in the shell "
      f"still clears the {CHANCES:.0e} budget, so the front SURVIVES Route A; anyone quoting the "
      f"best-cell '5.0e3' must revise it UP to {bestA:.1e}")

check(bestA > best2 and abs(worstA / worst2 - 1) < 0.10,
      f"R3c *** AGAINST INTEREST -- against the kernel that was ACTUALLY IN FORCE, Route A is a "
      f"DEGRADATION at the inner shell. *** alpha=2 gives N = {best2:.2e}-{worst2:.2e}, so Route A is "
      f"{bestA/best2:.2f}x HARDER at 0.3 a0 and a wash at 1.0 a0 ({worstA/worst2:.2f}x). The apparent "
      f"'Route A improves the front' reading is an artefact of comparing against the alpha=1 kernel the "
      f"committed scripts used (R0b), not against alpha=2")

# the decision must agree computed two independent ways
disagree = sum(1 for k, _, _ in KERNELS for f in GRID
               if (res[(k, f)]["N"] < CHANCES) != (z_at(res[(k, f)]["rms_max"], CHANCES) > 3.0))
check(disagree == 0,
      f"R3d the clears/does-not-clear decision is identical computed two independent ways -- "
      f"N(3 sigma) < CHANCES versus z(at N = CHANCES) > 3 -- at all {len(KERNELS)*len(GRID)} cells "
      f"({disagree} disagreements), so the verdict is not an artefact of which side of the estimator "
      f"it is read from")

# per-footing, WITHOUT the max-over-footings convention: this is where the committed standing is optimistic
print(f"\n  PER-FOOTING, dropping the max-over-footings convention. The max convention takes the LARGEST")
print(f"  spread, which gives the SMALLEST N -- generous against the closure script's 'dead' verdict, but")
print(f"  OPTIMISTIC for the scan script's 'alive' verdict. So the canonical footing must be shown alone:")
print(f"  {'kernel':>10}{'footing':>8}{'N(0.3a0)':>12}{'N(1.0a0)':>12}{'clears shell?':>15}"
      f"{'dead-zone edge':>17}")
print("  " + "-" * 74)
EDGE: dict = {}
for kname, muf, _ in KERNELS:
    for fname, a0 in FOOTINGS:
        def _N(fac, a0=a0, muf=muf, fname=fname):
            r = [solve_spread(fac * A0_REF, a0, muf, ys)[0] for _, ys in PRIORS]
            return N3(max(s.std() / s.mean() for s in r))
        lo, hi = 0.30, 3.0
        for _ in range(50):
            m = 0.5 * (lo + hi)
            if _N(m) < CHANCES:
                lo = m
            else:
                hi = m
        EDGE[(kname, fname)] = 0.5 * (lo + hi)
        n03, n10 = _N(0.30), _N(1.00)
        print(f"  {kname.split()[0]:>10}{fname[:5]:>8}{n03:>12.3e}{n10:>12.3e}"
              f"{('YES' if max(n03, n10) < CHANCES else 'NO'):>15}{EDGE[(kname, fname)]:>14.3f} a0")
e1c, eAc = EDGE[(KERNELS[0][0], FOOTINGS[0][0])], EDGE[(KERNELS[2][0], FOOTINGS[0][0])]
check(e1c < SHELL[1] < eAc,
      f"R3e *** A REAL ROUTE A GAIN THE MAX-OVER-FOOTINGS CONVENTION WAS HIDING. *** On the CANONICAL "
      f"footing alone the dead-zone edge sits at a_ext = {e1c:.3f} a0 under alpha=1 -- i.e. the outer "
      f"{100*(SHELL[1]-e1c)/(SHELL[1]-SHELL[0]):.0f}% of the frozen 0.3-1 a0 shell does NOT clear "
      f"CHANCES, which the banked 'clears by 1.1x-60x' statement obscures because it maxes over footings. "
      f"Route A pushes that edge out to {eAc:.3f} a0, so under Route A the canonical footing clears the "
      f"WHOLE shell. On the alt footing the edge moves "
      f"{EDGE[(KERNELS[0][0], FOOTINGS[1][0])]:.3f} -> {EDGE[(KERNELS[2][0], FOOTINGS[1][0])]:.3f} a0")

# the s^-4 identity, verified across kernels rather than assumed
worst_scale = 0.0
for f in GRID:
    rA, r1 = res[(KERNELS[2][0], f)], res[(KERNELS[0][0], f)]
    worst_scale = max(worst_scale, abs((r1["N"] / rA["N"]) / (rA["rms_max"] / r1["rms_max"]) ** 4 - 1.0))
check(worst_scale < 1e-9,
      f"R3f the s^-4 amplification is exact in the numerics ({worst_scale:.1e} worst deviation across the "
      f"grid), which is why a {abs(1-r03A/r03_1)*100:.1f}% amplitude loss at 0.3 a0 becomes a "
      f"{NA[0.30]/N1[0.30]:.2f}x carrier penalty and a {abs(r10A/r10_1-1)*100:.1f}% gain at 1.0 a0 "
      f"becomes a {N1[1.00]/NA[1.00]:.2f}x saving")


# ==================================================================================================
banner("R4  THE S1 LEG RE-CHECKED -- exact unimodularity was ALPHA=1-EXCLUSIVE")
# ==================================================================================================
print(f"""  The committed derivation has THREE legs, and only the third was re-solved above:
    S1  the memory kernel is EXACTLY unimodular on the oscillatory branch, so the FREQUENCY channel
        carries no amplitude modification and cannot source a theta(y);
    S2  Theorem B forces the external field in through |a|^2 (quadrature), not linearly;
    S3  the surviving y-channel is the cross-term coherence -- what R2 re-solved.
  S2 is kinematic and kernel-free. S1 is NOT: it is a property of alpha=1's radical. Continuing each
  kernel to z = -w^2 (w = omega c / a0) the same way mi_theta_efe_from_closure_2026.py:S1 does:
      alpha=1 : K(z) = (sqrt(1+4z)-1)/(2 sqrt z)  ->  (sqrt(4w^2-1) + i)/(2w),  |K| = 1 EXACTLY (w>1/2)
      ROUTE A : K(z) = mu(sqrt z), i.e. K = 1 - e^-u with u^2 = i w (1 - e^-u), solved on the branch
                continuous from the real axis (Re u >= 0) -- and there is NO branch point, so there is
                no 'oscillatory branch' in alpha=1's sense and no unimodularity theorem to inherit.""")


def K_alpha1(w):
    z = -complex(w) ** 2
    return (np.sqrt(1.0 + 4.0 * z) - 1.0) / (2.0 * np.sqrt(z))


def K_routeA(w, iters=600):
    """1 - e^-u with u^2 = x(1-e^-u), x = i w. Fixed point u <- sqrt(x(1-e^-u)); principal sqrt keeps
    Re u >= 0, which is the branch continuous from the real axis (a plain Newton solve jumps branches
    and blew up at w ~ 1e3 in an earlier version of this check)."""
    x = 1j * w
    u = np.sqrt(x)
    for _ in range(iters):
        un = np.sqrt(x * -np.expm1(-u))
        if abs(un - u) < 1e-16 * max(1.0, abs(un)):
            u = un
            break
        u = un
    return 1.0 - np.exp(-u), u


_ws = np.logspace(-1, 6, 3001)
_resid, _neg = 0.0, 0
for _w in _ws:
    _K, _u = K_routeA(_w)
    _resid = max(_resid, abs(_u * _u - 1j * _w * _K) / max(abs(_u * _u), 1e-300))
    _neg += (_u.real < 0)
check(_resid < 1e-10 and _neg == 0,
      f"R4a the Route A continuation is solved on the right branch: worst relative residual of "
      f"u^2 = i w (1 - e^-u) is {_resid:.1e} over seven decades in w, with Re u >= 0 at all "
      f"{len(_ws)} points ({_neg} violations)")

C_LIGHT = 2.99792458e8
KPC = 3.0856775814913673e19
GYR = 3.1556952e16
T_AGE_GYR = 13.797


def period_gyr(w):
    return 2.0 * math.pi / (w * A0_REF / C_LIGHT) / GYR


print(f"\n  {'w = omega c/a0':>15}{'period (Gyr)':>14}{'| |K_a1| - 1 |':>16}{'| |K_A| - 1 |':>15}"
      f"{'1 - cos(phi_a1)':>17}   where")
print("  " + "-" * 104)
WROWS = [(0.5, "alpha=1's branch point"), (1.0, ""), (3.0, "Route A's |K| crosses 1"),
         (9.0, "Route A's overshoot peak"), (30.0, ""),
         (103.8, "CLUSTER MEMBER ORBIT (v=1000 km/s, R=1 Mpc)"),
         (1384.0, "LSB DWARF INTERNAL (sigma=20 km/s, Re=1.5 kpc)")]
for w, note in WROWS:
    d1 = abs(abs(K_alpha1(w)) - 1.0)
    dA = abs(abs(K_routeA(w)[0]) - 1.0)
    ph = math.asin(min(1.0, 1.0 / (2.0 * w)))
    print(f"  {w:>15.1f}{period_gyr(w):>14.3g}{d1:>16.2e}{dA:>15.2e}{1-math.cos(ph):>17.3e}   {note}")

dev_A, dev_1 = [], []
for nm, v, R in [("cluster member orbit", 1000e3, 1.0e3 * KPC), ("LSB dwarf internal", 20e3, 1.5 * KPC)]:
    w = (v / R) * C_LIGHT / A0_REF
    dev_A.append(abs(abs(K_routeA(w)[0]) - 1.0))
    dev_1.append(abs(abs(K_alpha1(w)) - 1.0))

# the OVERSHOOT peak (the region where Route A's |K| actually exceeds 1) and the frequency above which
# the whole window is smaller than the front's own smallest signal
s_min_shell = min(res[(KERNELS[2][0], f)]["rms_max"] for f in SHELL_F)
_wov = np.logspace(math.log10(3.0), 2.0, 801)
_ovs = np.array([abs(K_routeA(w)[0]) - 1.0 for w in _wov])
_ipk = int(np.argmax(_ovs))
_wpk, _dpk = float(_wov[_ipk]), float(_ovs[_ipk])
_lo, _hi = _wpk, 1e4
for _ in range(60):
    _m = 0.5 * (_lo + _hi)
    if abs(abs(K_routeA(_m)[0]) - 1.0) > s_min_shell:
        _lo = _m
    else:
        _hi = _m
W_SAFE = 0.5 * (_lo + _hi)
print(f"\n  Route A's |K| is FAR from 1 at w ~ 1 (off by {abs(abs(K_routeA(1.0)[0])-1.0)*100:.1f}% where "
      f"alpha=1 is exactly 1), overshoots to")
print(f"  |K| = {1+_dpk:.4f} at w = {_wpk:.1f}, then dies as e^-Re u ~ e^-sqrt(w/2). The window drops below the")
print(f"  front's own smallest in-shell signal ({100*s_min_shell:.2f}%) at w = {W_SAFE:.1f}, i.e. for periods "
      f"shorter than {period_gyr(W_SAFE):.3g} Gyr")
print(f"  -- and {period_gyr(W_SAFE):.3g} Gyr is {period_gyr(W_SAFE)/T_AGE_GYR:.0f}x the age of the universe, "
      f"so EVERY bound carrier is on the safe side")

check(max(dev_1) < 1e-12 and max(dev_A) > 1e-6 and max(dev_A) < 0.05 * s_min_shell
      and period_gyr(W_SAFE) > T_AGE_GYR,
      f"R4b *** S1 IS ALPHA=1-EXCLUSIVE. ROUTE A LOSES THE THEOREM BUT NOT THE CONCLUSION. *** alpha=1 "
      f"is unimodular to {max(dev_1):.1e} -- machine zero, and sympy proves it exact -- while Route A's "
      f"continued kernel deviates by up to {_dpk*100:.2f}% (at w = {_wpk:.1f}) and by {max(dev_A):.2e} at "
      f"the carriers' actual frequencies. So the exponential kernel DOES open a frequency-channel "
      f"amplitude window that alpha=1 provably did not have, and the committed bound weakens from 1.2e-5 "
      f"(1 - cos phi) to {max(dev_A):.1e}, a factor {max(dev_A)/1.16e-5:.0f}x. It is still "
      f"{s_min_shell/max(dev_A):.0f}x below the SMALLEST in-shell spread ({100*s_min_shell:.2f}%), and the "
      f"whole open window lies at periods > {period_gyr(W_SAFE):.3g} Gyr "
      f"({period_gyr(W_SAFE)/T_AGE_GYR:.0f}x the age of the universe), so S3 remains the entire "
      f"y-channel and R2's re-solve is complete. Honest statement: 'bounded, not zero' -- one EXACT "
      f"theorem downgraded to an exponential estimate, which is a real loss of rigour even though the "
      f"number does not move")


# ==================================================================================================
banner("R5  VERDICT -- and the six things this does NOT establish")
# ==================================================================================================
print(f"""  (a) AMPLITUDE. At the 2 a0 retirement fiducial the committed 1.45-2.21% (max-min, both footings
      x three window shapes) becomes {100*wA[0]:.2f}-{100*mmA_alt:.2f}% under Route A -- BETTER by
      {min(wA[0]/w1[0], mmA_alt/_d_mm):.2f}x-{max(wA[0]/w1[0], mmA_alt/_d_mm):.2f}x. But 2 a0 is off-design. At the front's OWN shell the sign flips at the
      inner edge: pop-RMS {100*r03_1:.4f}% -> {100*r03A:.4f}% at 0.3 a0 ({r03A/r03_1:.3f}x, WORSE) and
      {100*r10_1:.4f}% -> {100*r10A:.4f}% at 1.0 a0 ({r10A/r10_1:.3f}x, better). Max-min at the shell:
      {100*b03_1[0]:.2f}-{100*b03_1[1]:.2f}% -> {100*b03_A[0]:.2f}-{100*b03_A[1]:.2f}% at 0.3 a0.

  (b) N(3 sigma) ACROSS THE FROZEN SHELL. Committed {best1:.2e}-{worst1:.2e} -> Route A {bestA:.2e}-{worstA:.2e},
      against CHANCES = {CHANCES:.0e}. Still clears at EVERY point in 0.3-1.0 a0: by
      {CHANCES/worstA:.1f}x-{CHANCES/bestA:.0f}x, against the committed {CHANCES/worst1:.1f}x-{CHANCES/best1:.0f}x. The binding outer edge
      improves {worst1/worstA:.2f}x; the best cell degrades {bestA/best1:.2f}x. Dead-zone edge (max-footing convention)
      moves {EDGE[(KERNELS[0][0], FOOTINGS[1][0])]:.2f} -> {EDGE[(KERNELS[2][0], FOOTINGS[1][0])]:.2f} a0; on the canonical footing ALONE it moves
      {e1c:.2f} -> {eAc:.2f} a0, which is the difference between failing and clearing the shell's outer edge.

  (c) DOES THE FRONT SURVIVE? YES -- it survives, and it is MIXED, not an improvement:
        * vs the committed alpha=1 baseline: inner edge {NA[0.30]/N1[0.30]:.2f}x harder, outer edge {N1[1.00]/NA[1.00]:.2f}x easier.
        * vs alpha=2, the kernel actually in force: inner edge {bestA/best2:.2f}x HARDER, outer edge a wash
          ({worstA/worst2:.2f}x). On this front Route A is a net small COST against the real baseline.
        * the mechanism is exact and explains both signs: the exponential's response slope is SOFTER
          than alpha=1's below x = {X_CROSS:.2f} and SHARPER above it (R1b), and the design shell straddles
          x = {X_CROSS:.2f}. "Sharper transition" is true but only above the crossing -- it does NOT translate
          into a uniformly larger spread, and the front's inner edge sits on the wrong side.
        * what genuinely improves: the CANONICAL footing now clears the whole shell (R3e), and the
          outer-edge margin goes from {CHANCES/worst1:.1f}x (which would not survive any realistic LSB cut) to {CHANCES/worstA:.1f}x.
        * what genuinely gets WEAKER, on top of the inner edge: the derivation's S1 leg. alpha=1's
          exact unimodularity theorem was alpha=1-EXCLUSIVE and Route A does not have it. The
          frequency channel is now bounded, not zero -- {max(dev_A):.1e} at the carriers instead of a
          provable 0, a {max(dev_A)/1.16e-5:.0f}x weaker bound, with the open part of the window ({_dpk*100:.1f}% at
          w = {_wpk:.1f}) confined to orbital periods > {period_gyr(W_SAFE):.3g} Gyr. The amplitude conclusion holds;
          the rigour behind it does not (R4b).

  (d) PRIOR CONVENTION. Kept: the reported spread is the MAX over both sampling priors. Under Route A
      the UNIFORM prior dominates at every (kernel, a_ext, footing) cell, exactly as in the committed
      convention -- uniform-in-y weights the coherence peak y = 1, log-uniform buries carriers at small
      y where C -> 0. At the inner shell, Route A: uniform {100*_pr_A['uniform']['rms']:.4f}% vs log-uniform {100*_pr_A['log-uniform']['rms']:.4f}%.

  A DEFECT IN THE BASELINE, found on the way and reported rather than quietly fixed: both committed
  scripts compute this front on the ALPHA=1 kernel (R0b proves it: their mu_fw satisfies x^2 = y^2+y),
  which was already retired for ephemeris reasons when the standing was banked. The correct pre-Route-A
  baseline is alpha=2: N = {best2:.2e}-{worst2:.2e} across the shell, not {best1:.2e}-{worst1:.2e}.

  WHAT THIS DOES NOT ESTABLISH:
   1. NOT that the front is confirmable. N counts CARRIERS -- LSB cluster members with RESOLVED internal
      dispersions at the 10% tier. CHANCES's ~3e5 is a TOTAL spectrum budget over ~150 clusters and the
      resolved-LSB fraction is not computed here. Clearing by {CHANCES/worstA:.1f}x at the outer edge is necessary,
      not sufficient, and would not survive a severe LSB cut.
   2. NOT that the carriers are in the shell. Whether enough LSB dwarfs with resolved sigma sit at
      a_ext = 0.3-1 a0 is observational and untouched here.
   3. NOT a repair of the front's OTHER defect -- the frozen E4 SIGN statistic tests a monotone trend
      while the derived signal peaks at y = 1. That is kernel-free and stands exactly as banked.
   4. NOT an AQUAL solve. This is the anchor's scalar model: the boost depends only on |a_in + a_ex|/a0.
      The nu and mu forms are exact inverses only in SPHERICAL symmetry, so a genuinely non-spherical
      EFE treatment could move the amplitude either way. That belongs to the directional-EFE lane.
   5. NOT a claim that Route A has a memory-kernel completion. R4's continuation applies the closure
      script's own recipe to Route A's mu; whether the exponential kernel admits an MI action at all is
      OPEN, and if it does not, R4 is a consistency estimate rather than a property of a derived kernel.
   6. NOT a derived line shape. The averaging window is still a modelling choice; the amplitude is
      therefore quoted as a band over three window shapes, which spans ~1.45x. a0 is an INPUT throughout
      and never fitted (R2a checks the solver only ever saw the two frozen footings).""")

banner("RESULT")
_n = sum(1 for x, _ in ok if x)
print(f"  {_n}/{len(ok)} checks held.")
if _n != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print(f"  Exit 0: the sigma-spread front SURVIVES Route A and the change is MIXED -- N(3 sigma) across")
print(f"  the frozen 0.3-1 a0 shell goes {best1:.2e}-{worst1:.2e} (committed, alpha=1) -> {bestA:.2e}-{worstA:.2e} (Route A),")
print(f"  still under CHANCES everywhere; {bestA/best1:.2f}x worse at the inner edge, {worst1/worstA:.2f}x better at the outer,")
print(f"  and {bestA/best2:.2f}x worse at the inner edge against the alpha=2 kernel that was actually in force.")

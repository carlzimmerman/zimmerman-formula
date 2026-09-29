#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A3_nonlinear_static -- the nonlinear ladder N1-N3 of CFG123_FROZEN_CRITERIA.md (G1 section): is there a nonlinear-in-M escape?

System: the EXACT static spherically symmetric equations of the localised RR model (cfg123_static, built from the covariant field equation verified in A1;
theta-theta equation checked numerically), exponential sphere rho = M e^{-r/h}/(8 pi h^3), h = 2 kpc (CFG44 B1's scale), areal gauge.
Prescription P0 (declared): S(0) = 0 (no cosmological S-bar), U -> 0 at infinity (zero data, exact Schwarzschild exterior form at lam = 0; standing-wave beta = 0 at finite lam).
Response quantity: g = A'/(2A), the acceleration of a static baryon; the m^2 response g_lam = d g/d lam at lam = 0 (exact in eps).  Nonlinear ratio
    R_NL(r; eps) = g_lam(r; eps)/g_lam(r; 0) - 1 ,   eps = G M/(h c^2),
where eps = 0 IS the exact linear (first order in eps) system.  A departure of the variational solution from the closed-form linear formula (A2) at eps = 0 is a control.

N1  (frozen: second-order perturbation theory at the TRUE galactic parameters).  Implemented as the exact-in-eps O(lam) system in variables rescaled so that eps enters
    algebraically (no tiny numbers, so double precision suffices; mpmath is NOT used: a disclosed deviation from the frozen wording); the second-order coefficient c2 is
    extracted from eps = +/- 1e-4.  Evaluated at eps_h(M) = G M/(h c^2) and r = x r_M(M) for the G1 grid, both a0 footings.
N2  the full nonlinear finite-lam system at inflated parameters eps in {1e-4, 1e-3, 1e-2}, m h in {0.03, 0.1, 0.3}: R_NL^{N2} = [g(eps,lam) - g(eps,0)]/[g(0,lam) - g(0,0)] - 1.
N3  exponent fits of R_NL in eps (N1, N2) and in m h (N2).
Decision lines (frozen): CLOSED-in-scope if R_NL <= 1e-3 at every grid point and the fitted (m r) exponent >= 0; UNDECIDED if some 1e-3 < R_NL < 0.1; OPEN if R_NL >= 0.1 anywhere.
MUTATE=c : eps = 0.05 (and m h = 0.5) in place of the galactic values.
Pre-registered P4: R_NL <= 1e-3 at every grid point; eps exponent in 1.0 +/- 0.15; (m r) exponent >= 0.  Hand estimate: R_NL ~ eps ~ 1e-9..1e-5.
"""
import os, sys, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg123_common import *
import cfg123_nl as NL

MUT = mutate_mode()
if MUT not in ("", "c"):
    print("A3: MUTATE mode", MUT, "not applicable"); sys.exit(3)
R = Report("A3_nonlinear_static", MUT)
R.banner(f"A3 nonlinear ladder, MUTATE={MUT or 'none'}")
RMAX = 1000.0
GMSUN_C2_KPC = G_SI * MSUN / C_SI ** 2 / KPC                       # kpc


def eps_h(M):
    return GMSUN_C2_KPC * M / H_EXP_KPC


# ---------------------------------------------------------------------------------------------- N1
R.banner("N1  exact-in-eps O(lam) response of the localised RR equations on the exponential sphere")
radii = {}
for foot, a0 in A0_FOOT.items():
    for M in MASSES:
        radii[(foot, M)] = np.array([xg * rM_m(M, a0) / KPC / H_EXP_KPC for xg in XGRID])
allr = np.unique(np.concatenate(list(radii.values())))
t0 = time.time()
o0, d0 = NL.variational(0.0, RMAX, rout=allr)
R.P(f"    eps = 0 (linear) run: {time.time() - t0:.0f} s")
# control: closed-form linear formula (the A2 result): g~_lam = (1/(3 r^2)) int_0^r psi r'^2, psi = -P(3,r)/r - (1+r) e^{-r}/2
from scipy.special import gammainc
from scipy.integrate import quad
psi = lambda s: -gammainc(3.0, s) / s - (1 + s) * np.exp(-s) / 2
ctrl_r = np.array([0.5, 2.0, 5.0, 20.0, 100.0])
oc, _ = NL.variational(0.0, RMAX, rout=ctrl_r)
lin = np.array([quad(lambda x: psi(x) * x * x, 0, r, limit=400)[0] / (3 * r * r) for r in ctrl_r])
ctl = np.max(np.abs(oc["g_lam"] / lin - 1))
R.check("N1 control: the eps = 0 variational solution reproduces the closed-form linear response (A2: g_lam = (1/3r^2) int psi r'^2) to 1e-6 at r/h = 0.5, 2, 5, 20, 100",
        f"max relative deviation {ctl:.2e}", ctl < 1e-6)

if MUT == "c":
    eps_list = {M: 0.05 for M in MASSES}
else:
    eps_list = {M: eps_h(M) for M in MASSES}
RNL = {}
runs = {}
for M in MASSES:
    t0 = time.time()
    e = eps_list[M]
    o, d = NL.variational(e, RMAX, rout=allr)
    runs[M] = (o, d)
    RNL[M] = o["g_lam"] / o0["g_lam"] - 1.0
    R.P(f"    M_b = {M:.0e}: eps_h = {e:.3e} ({time.time() - t0:.0f} s)")
R.P("\n    R_NL(x, M) at the true galactic eps_h and r = x r_M (canonical footing):")
R.P("    M_b     eps_h    | x = " + "  ".join(f"{x:g}" for x in XGRID))
maxR, maxc = 0.0, 0.0
tab = {}
for foot in A0_FOOT:
    for M in MASSES:
        idx = [int(np.argmin(abs(allr - v))) for v in radii[(foot, M)]]
        vals = RNL[M][idx]
        tab[(foot, M)] = vals
        maxR = max(maxR, np.max(np.abs(vals)))
        maxc = max(maxc, np.max(np.abs(vals)) / eps_list[M])
        if foot == "canonical":
            R.P(f"    {M:.0e}  {eps_list[M]:.2e} | " + "  ".join(f"{v:+.1e}" for v in vals))
R.P(f"\n    max |R_NL| over the grid (both footings) = {maxR:.3e}; max |R_NL|/eps_h = {maxc:.3f}")
R.num("R_NL_max", maxR); R.num("R_NL_over_eps_max", maxc)
# second-order coefficient c2(r) from eps = +/- 1e-4
op, _ = NL.variational(1e-4, RMAX, rout=allr)
om, _ = NL.variational(-1e-4, RMAX, rout=allr)
c2 = ((op["g_lam"] - om["g_lam"]) / (2e-4)) / o0["g_lam"]
R.P(f"    second-order coefficient c2(r/h) = [g_lam(eps) - g_lam(-eps)]/(2 eps g_lam(0)): min {c2.min():+.3f}, max {c2.max():+.3f} over r/h in [{allr.min():.3g}, {allr.max():.3g}]")
R.num("c2_range", [float(c2.min()), float(c2.max())])

# ---------------------------------------------------------------------------------------------- N1 eps-exponent
R.banner("N1/N3  exponent of eps in R_NL (fixed r/h = 0.5, 5, 50)")
sel = np.array([0.5, 5.0, 50.0])
e_list = [1e-6, 1e-4, 1e-2]
outs = {}
for e in e_list:
    o, _ = NL.variational(e, RMAX, rout=sel)
    outs[e] = o["g_lam"]
ol, _ = NL.variational(0.0, RMAX, rout=sel)
slopes = []
for i, r in enumerate(sel):
    Rv = np.array([abs(outs[e][i] / ol["g_lam"][i] - 1) for e in e_list])
    sl = np.polyfit(np.log(e_list), np.log(Rv), 1)[0]
    slopes.append(sl)
    R.P(f"    r/h = {r:g}: R_NL(eps = 1e-6, 1e-4, 1e-2) = {Rv[0]:.3e}, {Rv[1]:.3e}, {Rv[2]:.3e}; fitted exponent of eps = {sl:.4f}")
eps_expo = float(np.mean(slopes))

# ---------------------------------------------------------------------------------------------- N2
R.banner("N2  full nonlinear finite-lam system at inflated parameters (theta-theta residual checked)")
RM2 = 25.0
rsel = np.array([1.0, 3.0, 10.0])
mh_list = [0.03, 0.1, 0.3] + ([0.5] if MUT == "c" else [])
e2_list = [1e-4, 1e-3, 1e-2] + ([0.05] if MUT == "c" else [])
n2 = {}
tt_worst = 0.0
for mh in mh_list:
    lam = mh * mh
    # eps = 0 linear references (U~(0) from the linear standing-wave condition)
    def lin_ref():
        b0_ = NL.beta_flat(NL.integrate(0.0, lam, 0.0, 0.0, RM2).y[:, -1], lam, RM2)
        b1_ = NL.beta_flat(NL.integrate(0.0, lam, 0.0, 1.0, RM2).y[:, -1], lam, RM2)
        return -b0_ / (b1_ - b0_)
    Ucl = lin_ref()
    g_lin_lam, _ = NL.g_at(0.0, lam, 0.0, Ucl, RM2, rsel)
    g_lin_0, _ = NL.g_at(0.0, 0.0, 0.0, 0.0, RM2, rsel)
    glin = g_lin_lam - g_lin_0
    for e in e2_list:
        t0 = time.time()
        pcs, Ucs = NL.solve_finite(e, lam, RM2)
        g_l, sol_l = NL.g_at(e, lam, pcs, Ucs, RM2, rsel)
        pc_gr = NL.solve_bg_pc(e, RM2)
        g_0, _ = NL.g_at(e, 0.0, pc_gr, 0.0, RM2, rsel)
        Rn = (g_l - g_0) / glin - 1.0
        th, _ = NL.theta_theta_residual(sol_l, lam, e, [0.5, 2.0, 6.0])
        tt_worst = max(tt_worst, th)
        n2[(mh, e)] = Rn
        R.P(f"    m h = {mh:g} (lam = {lam:g}), eps = {e:g}: R_NL^N2(r/h = 1, 3, 10) = " + ", ".join(f"{v:+.3e}" for v in Rn) + f"   [theta-theta residual {th:.1e}; {time.time() - t0:.0f} s]")
R.check("N2 control: the independent theta-theta field equation (not used in the integration) holds along the finite-lam nonlinear solutions", f"worst relative residual {tt_worst:.2e}", tt_worst < 1e-6)

# exponents in eps and in m h
ee = [e for e in e2_list if e <= 1e-2]
eps_expN2 = []
for mh in mh_list:
    for i in range(len(rsel)):
        v = np.array([abs(n2[(mh, e)][i]) for e in ee])
        eps_expN2.append(np.polyfit(np.log(ee), np.log(v), 1)[0])
mh_expo = []
for e in ee:
    for i in range(len(rsel)):
        mhs = [m_ for m_ in mh_list if m_ <= 0.3]
        v = np.array([abs(n2[(m_, e)][i]) for m_ in mhs])
        mh_expo.append(np.polyfit(np.log(mhs), np.log(v), 1)[0])
R.P(f"\n    N3 fitted exponent of eps (N2): {np.round(eps_expN2, 3).tolist()};  fitted exponent of (m h): {np.round(mh_expo, 3).tolist()}")
R.P(f"    N3 fitted exponent of eps (N1, exact O(lam)): {np.round(slopes, 4).tolist()}")
# N1 vs N2 agreement at small lam
e_chk = 1e-3
o_chk, _ = NL.variational(e_chk, RMAX, rout=rsel)
Rn1 = o_chk["g_lam"] / NL.variational(0.0, RMAX, rout=rsel)[0]["g_lam"] - 1
Rn2 = n2[(0.03, e_chk)] if (0.03, e_chk) in n2 else None
agree = np.max(np.abs(Rn2 / Rn1 - 1)) if Rn2 is not None else float("nan")
R.P(f"    N1 (lam -> 0) R_NL(eps = 1e-3, r/h = 1, 3, 10) = {np.round(Rn1, 6).tolist()}; N2 (m h = 0.03) = {np.round(Rn2, 6).tolist()}; max relative difference {agree:.2%}")
R.check("N1/N2 agreement: at m h = 0.03 the finite-lam nonlinear R_NL matches the O(lam) series to 30% (through O(eps^2))", f"max relative difference {agree:.2%}", agree < 0.30, load_bearing=(MUT == ""))

# ---------------------------------------------------------------------------------------------- decision
R.banner("decision")
if maxR <= 1e-3 and min(mh_expo) >= 0.0:
    dec = "CLOSED-in-scope"
elif maxR >= 0.1:
    dec = "OPEN"
else:
    dec = "UNDECIDED"
R.verdict("nonlinear route (RR, static spherical, exponential sphere, prescription P0)", dec,
          f"max |R_NL| = {maxR:.3e} (galactic eps_h), fitted (m h) exponent min {min(mh_expo):.3f}, eps exponent {eps_expo:.3f}")
# shortfall after the nonlinear correction
pmR = 6.06e-11
R.P(f"    the linear response falls short of the target by 1/|R_A| >= 1/6.06e-11 = {1 / pmR:.2e} (A2, worst grid point); the nonlinear terms change the response by at most a factor (1 + {maxR:.2e}); the shortfall after them is unchanged to {maxR:.1e}.")
R.check("P4a: R_NL <= 1e-3 at every G1 grid point (galactic parameters)", f"max |R_NL| = {maxR:.3e}", maxR <= 1e-3)
R.check("P4b: the fitted exponent of eps (exact O(lam) system) is 1.0 +/- 0.15", f"{eps_expo:.4f}", abs(eps_expo - 1.0) <= 0.15)
R.check("P4c: the fitted exponent of (m h) in R_NL (finite lam) is >= 0 (no 1/(m r)^2 enhancement)", f"exponents {np.round(mh_expo, 3).tolist()}", min(mh_expo) >= 0.0)
R.check("P4d: the exact-in-eps N1 and the frozen 'second order' agree: the c2 range is O(1) (|c2| <= 10 over r/h in the grid)", f"c2 in [{c2.min():+.3f}, {c2.max():+.3f}]", max(abs(c2.min()), abs(c2.max())) <= 10.0, load_bearing=False)
R.num("decision", dec); R.num("eps_exponent_N1", eps_expo); R.num("mh_exponents_N2", mh_expo)
sys.exit(finish(R, MUT))

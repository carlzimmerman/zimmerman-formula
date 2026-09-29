#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D5_A -- Door 5, part A: Eddington inversion for the CFG44 POINT-MASS target, and the Lynden-Bell (maximum-entropy) test on it.
See FROZEN_QUESTION.md (written before this script).  Units a0 = G = M_b = 1, r_M = 1.

For a point mass M_b(<r) = M for every r > 0, so beta = -(1/2) dlnM_b/dlnr = 0 EXACTLY: the anisotropic question is the isotropic one and
Eddington's inversion is exact.   f(E) = (1/(sqrt2 pi^2)) Int_0^inf rho''(Phi = E + t^2) dt ,   rho'' = d^2 rho/dPhi^2 (analytic, sympy).
The potential Phi = asinh r - sqrt(1+r^2)/r is unbounded at BOTH ends (-1/r at the centre, ln r outside), so E runs over the whole real line.

CHECKS (PRE-DECLARED, FROZEN_QUESTION.md M1/M4/D1/D4/D7)
  A1 (sympy) rho_c, g_tot, Phi satisfy the target: Phi' = g, rho g r^3 4 pi = a0 M (charge), Jeans with beta = 0: d(rho s^2)/dr = -rho g with s^2 = V_c^2/2.
  A2 CONTROL: the Eddington code returns f = exp(-E/s^2) x const for the singular isothermal sphere (numeric, within 2%).
  A3 f(E) >= 0 over E = Phi(r_E) for r_E in [1e-5, 1e5] (D1; negative if f < -1e-6 x Int|integrand|).
  A4 the analytic Kepler-cusp limit f -> (8 sqrt2 pi^3)^(-1) (-E)^(-1/2) as E -> -inf (rho -> 1/(4 pi r), gamma = 1) is met to 5% at r_E = 1e-4.
  A5 ROUND TRIP: rho(r) = 4 pi sqrt2 Int_Phi^inf f(E) sqrt(E - Phi) dE reproduces the target density to 1% at r = 1e-3 .. 1e3.
  A6 M4a entropy: d ln f/dE over the range against a constant, the best isothermal (Maxwell-Boltzmann) fit and the best Fermi-Dirac fit of rho_c over x in [0.1, 30] (criterion: extremum only if within 10%).
MUTATE=1 (D7): rho_c is multiplied by a shell bump 1 + 3 exp(-(ln r - 1)^2/(2 0.3^2)) (rho then rises with r on the bump's inner flank; an isotropic f(E) >= 0 needs
  d rho/d Phi = -2 pi sqrt2 Int f/sqrt(E-Phi) dE <= 0, i.e. a density falling outward): A3 must FAIL (rc = 1).  (A5, the round trip, is an identity and
  still holds for a negative f: it is NOT expected to fail.)
Run: python3 D5_A_eddington_pointmass.py   (MUTATE=1 for the control)
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import least_squares
from scipy.interpolate import PchipInterpolator

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from D5common import *

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("D5_A_eddington_pointmass", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: rho_c times a shell bump -- A3 must FAIL ***")

# ============================================================================================ A1 sympy
R.banner("A1  SYMPY: the point-mass target, its potential, and the Jeans identity with beta = 0")
r = sp.symbols("r", positive=True)
s = sp.sqrt(1 + r ** 2)
rho_s = 1 / (4 * sp.pi * r * s)
g_s = s / r ** 2
Phi_s = sp.asinh(r) - s / r
res = [sp.simplify(sp.diff(Phi_s, r) - g_s),
       sp.simplify(4 * sp.pi * r ** 3 * rho_s * g_s - 1 / s * s),                    # rho g 4 pi r^3 = a0 M_b = 1  (a0 = M = 1)
       sp.simplify(sp.diff(rho_s * s / (2 * r), r) + rho_s * g_s),                   # beta = 0 Jeans, sigma_r^2 = V_c^2/2 = u/(2r) = s/(2r)
       sp.simplify(sp.integrate(4 * sp.pi * r ** 2 * rho_s, r) - (s - 1)) if False else 0]
# the mass integral: d/dr[(s-1)] = r/s = 4 pi r^2 rho  (M_c = M (sqrt(1+x^2) - 1))
res[3] = sp.simplify(sp.diff(s - 1, r) - 4 * sp.pi * r ** 2 * rho_s)
check("A1 (sympy) Phi' = g_tot; rho g 4 pi r^3 = a0 M (exact charge); Jeans with beta = 0 and sigma^2 = V_c^2/2; M_c = M(sqrt(1+x^2) - 1)",
      f"residuals {res}", all(v == 0 for v in res))

# density used in the run (mutated in MUTATE mode) and its analytic d^2 rho/dPhi^2
if MUTATE:
    rho_used = rho_s * (1 + 3 * sp.exp(-(sp.log(r) - 1) ** 2 / (2 * 0.3 ** 2)))
else:
    rho_used = rho_s
rho_P = sp.diff(rho_used, r) / g_s
rho_PP = sp.diff(rho_P, r) / g_s
rho_PP_f = sp.lambdify(r, rho_PP, "numpy")
rho_f = sp.lambdify(r, rho_used, "numpy")
pot = point_mass()
Phi_num = pot.Phi
lr_tab = np.linspace(math.log(1e-8), math.log(1e8), 400001)
Phi_tab = Phi_num(np.exp(lr_tab))


def r_of_Phi(Ph):
    """invert the monotone Phi(r) (table guess + Newton in ln r)."""
    Ph = np.atleast_1d(np.asarray(Ph, float))
    x = np.interp(Ph, Phi_tab, lr_tab)
    for _ in range(6):
        rr = np.exp(x)
        F = Phi_num(rr) - Ph
        dF = pot.g(rr) * rr
        x = x - F / dF
    return np.exp(x)


PHI_MAX = float(Phi_num(1e7))


def f_eddington(E, rho_pp=rho_PP_f, rinv=r_of_Phi, phimax=PHI_MAX):
    """f(E) = (1/(sqrt2 pi^2)) Int_0^inf rho''(E + t^2) dt ; returns (f, Int|integrand| dt) for the cancellation scale."""
    T = math.sqrt(max(phimax - E, 1e-12))
    bps = [math.sqrt(p - E) for p in (-1e6, -1e5, -1e4, -1e3, -300, -100, -30, -10, -3, -1, 0, 1, 3, 6, 10) if E < p < phimax]
    bps = sorted(set(bps))
    integ = lambda t: float(rho_pp(rinv(E + t * t)[0]))
    absi = lambda t: abs(integ(t))
    v = quad(integ, 0.0, T, points=bps if bps else None, limit=800, epsabs=1e-300, epsrel=1e-10)[0]
    a = quad(absi, 0.0, T, points=bps if bps else None, limit=800, epsabs=1e-300, epsrel=1e-8)[0]
    return v / (math.sqrt(2) * math.pi ** 2), a / (math.sqrt(2) * math.pi ** 2)


# ============================================================================================ A2 control
R.banner("A2  CONTROL: the Eddington code on the singular isothermal sphere (rho = s2/(2 pi r^2), Phi = 2 s2 ln r  ->  f proportional to exp(-E/s2))")
s2c = 0.7
rc_ = sp.symbols("rc", positive=True)
rho_c = s2c / (2 * sp.pi * rc_ ** 2)
gc = 2 * s2c / rc_
rpp_c = sp.lambdify(rc_, sp.diff(sp.diff(rho_c, rc_) / gc, rc_) / gc, "numpy")
rinv_c = lambda Ph: np.exp(np.atleast_1d(np.asarray(Ph, float)) / (2 * s2c))
fs = []
for E in (-1.0, 0.0, 1.0):
    fs.append(f_eddington(E, rho_pp=rpp_c, rinv=rinv_c, phimax=2 * s2c * math.log(1e6))[0])
fs = np.array(fs)
ratio = fs / np.exp(-np.array([-1.0, 0.0, 1.0]) / s2c)
check("A2 CONTROL: isothermal sphere f(E)/exp(-E/s2) constant to 2% over E = -1, 0, 1",
      f"ratios {np.round(ratio / ratio[1], 4)}", np.all(np.abs(ratio / ratio[1] - 1) < 0.02))

# ============================================================================================ A3 f(E) over the full range
R.banner("A3  f(E) FOR THE POINT-MASS TARGET OVER THE WHOLE ENERGY RANGE (E = Phi(r_E), r_E in [1e-5, 1e5] r_M)")
rE = np.geomspace(1e-5, 1e5, 481)
EE = Phi_num(rE)
fE = np.zeros_like(EE); aE = np.zeros_like(EE)
for i, E in enumerate(EE):
    fE[i], aE[i] = f_eddington(float(E))
rel = fE / aE                                                       # 1 if no cancellation, sign is the verdict
neg = (fE < -1e-6 * aE)
P(f"  E range [{EE[0]:.4g}, {EE[-1]:.4g}] ({len(EE)} points); f range [{fE.min():.4e}, {fE.max():.4e}]")
P(f"  f/Int|integrand|: min {rel.min():.3e}, max {rel.max():.3e}; number of points with f < -1e-6 Int|.|: {int(neg.sum())}")
for rr_ in (1e-5, 1e-3, 1e-2, 0.1, 0.3, 1.0, 3.0, 10.0, 100.0, 1e3, 1e5):
    i = int(np.argmin(abs(rE - rr_)))
    P(f"    r_E = {rE[i]:9.3e}  E = {EE[i]:12.5e}  f = {fE[i]:12.5e}   f/Int|.| = {rel[i]: .4f}")
if neg.any():
    P(f"  NEGATIVE f at r_E in [{rE[neg].min():.4g}, {rE[neg].max():.4g}] r_M  (E in [{EE[neg].min():.4g}, {EE[neg].max():.4g}]);  min f = {fE.min():.4e}")
check("A3 (D1) f(E) >= 0 over E = Phi(r_E), r_E in [1e-5, 1e5] r_M",
      f"min f = {fE.min():.4e}; min f/Int|integrand| = {rel.min():.3e}; negative points {int(neg.sum())}", not neg.any())
R.num("fE_min", float(fE.min())); R.num("n_negative", int(neg.sum()))
R.num("negative_r_range", [float(rE[neg].min()), float(rE[neg].max())] if neg.any() else None)

# ============================================================================================ A4 Kepler limit
C_kep = 1.0 / (8 * math.sqrt(2) * math.pi ** 3)
i4 = int(np.argmin(abs(rE - 1e-4)))
ratio4 = fE[i4] / (C_kep * (-EE[i4]) ** -0.5)
check("A4 the analytic Kepler-cusp limit f -> (8 sqrt2 pi^3)^-1 (-E)^(-1/2) is met to 5% at r_E = 1e-4 (rho -> 1/(4 pi r), slope gamma = 1)",
      f"f / f_Kepler = {ratio4:.4f} at E = {EE[i4]:.4g}", abs(ratio4 - 1) < 0.05 if not MUTATE else True, load_bearing=not MUTATE)

# ============================================================================================ A5 round trip
R.banner("A5  ROUND TRIP: rho(r) = 4 pi sqrt2 Int_Phi^inf f(E) sqrt(E - Phi) dE against the target density")
worst = 0.0
lines = []
fint = PchipInterpolator(EE, fE, extrapolate=False)
for rr_ in (1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0, 1e3):
    Ph = float(Phi_num(rr_))
    smax = math.sqrt(EE[-1] - Ph)
    sgr = np.linspace(0.0, smax, 40001)
    Eg = Ph + sgr ** 2
    fg = np.nan_to_num(fint(Eg), nan=0.0)
    if Eg[0] < EE[0]:
        fg = np.where(Eg < EE[0], fE[0] * np.sqrt(EE[0] / np.minimum(Eg, -1e-30)), fg)   # Kepler tail below the table
    val = np.trapz(2 * sgr ** 2 * fg, sgr)                          # Int f sqrt(E-Phi) dE with dE = 2 s ds
    rho_rt = 4 * math.pi * math.sqrt(2) * val
    tgt = float(rho_f(rr_))
    dev = rho_rt / tgt - 1
    worst = max(worst, abs(dev))
    lines.append(f"    r = {rr_:8.3g}: rho(round trip) = {rho_rt:.5e}, target = {tgt:.5e}, ratio - 1 = {dev: .2e}")
for L_ in lines:
    P(L_)
check("A5 round trip: f(E) regenerates the target density to 1% at r = 1e-3 .. 1e3 (grid-limited; the isotropic f is unique given rho and Phi)",
      f"worst |ratio - 1| = {worst:.2e}", worst < 0.01)

# ============================================================================================ A6 entropy
R.banner("A6  LYNDEN-BELL / MAXIMUM ENTROPY (fixed fluid mass and energy in the given potential): is f_T an extremum?")
sel = (rE > 1e-3) & (rE < 1e3)
lnf = np.log(np.maximum(fE[sel], 1e-300))
dl = np.gradient(lnf, EE[sel])
P("  d ln f/dE at selected energies (a Maxwell-Boltzmann extremum needs this equal to the constant -1/sigma^2):")
for rr_ in (1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0, 1e3):
    i = int(np.argmin(abs(rE[sel] - rr_)))
    P(f"    r_E = {rE[sel][i]:9.3e}  E = {EE[sel][i]:11.4e}  d ln f/dE = {dl[i]: .4e}")
spread = (dl.max() - dl.min())
P(f"  d ln f/dE ranges over [{dl.min():.3e}, {dl.max():.3e}] (positive slopes mean f rises with E; a Boltzmann extremum has one negative constant)")
xg = np.geomspace(0.1, 30.0, 40)
Phg = Phi_num(xg)
lnrho = np.log(pot.rho(xg))
Aiso = np.vstack([np.ones_like(xg), -Phg]).T
coef = np.linalg.lstsq(Aiso, lnrho, rcond=None)[0]
dev_iso = np.exp(np.abs(Aiso @ coef - lnrho)).max() - 1
P(f"  best isothermal rho = A exp(-Phi/s2) on x in [0.1, 30]: s2 = {1 / coef[1]:.4g} (V_c^2/2 runs from {float(pot.sr2(0.1)):.3g} at x=0.1 to {float(pot.sr2(30.0)):.3g}); max deviation {dev_iso * 100:.1f}%")
vq, vw = np.polynomial.legendre.leggauss(400)


def rho_FD(Ph, eta, mu, s2):
    Ph = np.atleast_1d(Ph)
    out = np.zeros_like(Ph)
    for i, p in enumerate(Ph):
        vmax = math.sqrt(2 * max(mu + 60 * s2 - p, 1e-9))
        v = 0.5 * vmax * (vq + 1)
        E = p + 0.5 * v * v
        arg = np.clip((E - mu) / s2, -700, 700)
        f = eta / (1 + np.exp(arg))
        out[i] = 4 * math.pi * 0.5 * vmax * np.sum(vw * f * v * v)
    return out


def resid(th):
    return np.log(np.maximum(rho_FD(Phg, math.exp(th[0]), th[1], math.exp(th[2])), 1e-300)) - lnrho


best = None
for th0 in ([0, 0, 0], [-2, -1, 0], [2, 2, 1], [-4, 3, 2], [0, -3, -1], [3, 0, 2]):
    try:
        so = least_squares(resid, th0, method="lm", max_nfev=400)
        if best is None or so.cost < best.cost:
            best = so
    except Exception:
        pass
from scipy.optimize import differential_evolution
_de = differential_evolution(lambda th: float(np.max(np.abs(resid(th)))), bounds=[(-15, 15), (-5, 10), (-4, 4)], seed=1, maxiter=60, popsize=20, tol=1e-8, polish=False)
_so2 = least_squares(resid, _de.x, method="lm", max_nfev=400)
if _so2.cost < best.cost:
    best = _so2
dev_fd = float(np.exp(np.abs(best.fun)).max() - 1)
P(f"  best 3-parameter Fermi-Dirac (eta, mu, s2) fit on x in [0.1, 30]: eta = {math.exp(best.x[0]):.3g}, mu = {best.x[1]:.3g}, s2 = {math.exp(best.x[2]):.3g}; max deviation {dev_fd * 100:.1f}%")
R.num("iso_fit_max_dev", float(dev_iso)); R.num("fd_fit_max_dev", dev_fd); R.num("dlnf_dE_range", [float(dl.min()), float(dl.max())])
extremum = (dev_iso < 0.10) or (dev_fd < 0.10)
check("A6 (D4) the point-mass target is a Lynden-Bell (Maxwell-Boltzmann or Fermi-Dirac) entropy extremum: best fit reproduces rho_c to 10% over x in [0.1, 30]",
      f"isothermal fit max deviation {dev_iso * 100:.1f}%; Fermi-Dirac fit {dev_fd * 100:.1f}%; extremum = {extremum}", extremum, load_bearing=False)
R.num("entropy_extremum", bool(extremum))

nf = R.write()
sys.exit(1 if nf else 0)

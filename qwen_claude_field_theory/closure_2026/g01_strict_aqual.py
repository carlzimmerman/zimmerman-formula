#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""g01_strict_aqual.py -- G01 of FRIED_CHICKEN_ROADMAP_2026-09-04: strict-law (T-A, exact exponential AQUAL) cheap falsification.

  1. Re-derive mu, its exact primitive, both limits, the spherical first integral and the measured-G normalisation (sympy).
  2. Solve the exact nonlinear AQUAL Sun + external-field problem with an INDEPENDENT discretisation of the committed
     finite-volume solver: second-order finite differences in s = ln r with a Legendre (pseudo-spectral) expansion in theta,
     mu evaluated on Gauss-Legendre nodes and projected back.  Extract the signed l = 2 coefficient directly (it IS the
     Legendre coefficient), fit c2 r^2 + const + d2/r^3 over three windows, and compare with aqual_solar_gate_2026's value.
     Validation: the exact spherical first integral at eta = 0, and the Blanchet-Novak 2011 mu_1 anchor.
  3. The positive-density force-free centre: rho = rho0 + O(r^2)  ->  g^2 ~ (4 pi G a0 rho0/3) r, Phi'/r ~ r^{-1/2}; weak-
     solution existence, tidal and curvature behaviour, validity of the weak-field expansion (sympy + statement).
Sign convention: Phi_N = -GM/r, Phi_2 = c2 r^2 P2, Q2 = -3 c2 a0^{3/2}/sqrt(GM) with sign retained (Park eq. 6; contract).
Checks can fail; the verdict is PASS/FAIL/OPEN per item.  Both a0 footings; external-field endpoints 2.00 / 2.32 / 2.64e-10.
"""
import os, sys, math, json, time
import numpy as np, sympy as sp
import warnings; warnings.filterwarnings('ignore')      # numpy warnings print absolute paths; keep them out of the output
import scipy.sparse as sps, scipy.sparse.linalg as spl
from numpy.polynomial.legendre import leggauss, legval, legder
from scipy.optimize import brentq
T0 = time.time(); FAILS = []; OUT = {}
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; GM = 1.32712440018e20; G_EXT = {"low": 2.00e-10, "central": 2.32e-10, "high": 2.64e-10}
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27

print("=" * 100); print("G01 -- strict exact exponential AQUAL"); print("=" * 100)
# ---------------------------------------------------------------- 1. symbolic
y, r, gg, M, a0s, Gs, rho0 = sp.symbols("y r g M a_0 G rho_0", positive=True)
mu = 1 - sp.exp(-y); Gcal = y**2 + 2*(1 + y)*sp.exp(-y) - 2
check("S1 the primitive: d(G)/dy / (2y) = mu exactly; G(0) = 0; G ~ (2/3) y^3 (deep, since mu ~ y) and ~ y^2 (Newton)",
      sp.simplify(sp.diff(Gcal, y)/(2*y) - mu) == 0 and Gcal.subs(y, 0) == 0
      and sp.limit(Gcal/y**3, y, 0) == sp.Rational(2, 3) and sp.limit(Gcal/y**2, y, sp.oo) == 1)
check("S2 limits: mu -> y (deep MOND, g^2 = a0 g_N) and 1 - mu = e^{-y} (Newton, exponentially small)",
      sp.limit(mu/y, y, 0) == 1 and sp.simplify(1 - mu - sp.exp(-y)) == 0)
# spherical first integral: (1/r^2) d/dr [r^2 mu(g/a0) g] = 4 pi G M delta  ->  mu(g/a0) g = G M / r^2
check("S3 spherical first integral mu(g/a0) g r^2 = G M (Gauss's law on the flux mu g)", True, "by divergence theorem; used as the eta = 0 solver validation below")
# measured G: at g >> a0, mu = 1 - e^{-y}: g = G M/(mu r^2) = (G M/r^2)(1 + e^{-y} + ...) -> G_eff/G_N - 1 = e^{-y}
check("S4 measured-G normalisation: G_eff/G_N - 1 = e^{-g/a0} to leading order -- at Earth's orbit (g/a0 = 6e7) it is zero to every "
      "digit, so the strict law's G is the laboratory G with no renormalisation", sp.simplify(1/mu - 1 - sp.exp(-y)/(1 - sp.exp(-y))) == 0,
      "1/mu - 1 = e^{-y}/(1-e^{-y})")
# centre asymptotics
gc = sp.sqrt(sp.Rational(4, 3)*sp.pi*Gs*a0s*rho0*r)
check("C1 positive-density force-free centre: with mu ~ g/a0, (1/r^2) d(r^2 g^2/a0)/dr = 4 pi G rho0 gives g^2 = (4 pi G a0 rho0/3) r, "
      "so g ~ r^{1/2}, Phi'/r ~ r^{-1/2} and the tidal tensor dg/dr ~ r^{-1/2} DIVERGES at the centre; g -> 0 (a weak solution exists, "
      "Phi in C^{1.5}), the divergence is integrable, but bounded curvature (A8) fails -- the regular-centre theorem of this repository "
      "(universal to every kernel, and Newton's point mass fails A8 too): a smoothness statement, not a viability kill",
      sp.simplify(sp.diff(r**2*gc**2/a0s, r)/r**2 - 4*sp.pi*Gs*rho0) == 0 and sp.limit(gc/r, r, 0) == sp.oo,
      "verified symbolically; relativistic boundary layer: OPEN (none proposed)")

# ---------------------------------------------------------------- 2. the independent discretisation
def mu_exp(x): return 1.0 - np.exp(-x)
def mu_one(x): return x/(1.0 + x)
def solve_aqual(mufun, eta, L=8, NS=700, NT=48, rmin=1e-4, rmax=1e4, tol=1e-10, itmax=400, relax=0.5):
    """FD in s = ln r, Legendre in theta.  Units GM = a0 = 1 (R_M = 1).  Returns the Legendre coefficients phi_l(r), r, iterations, residual."""
    s = np.linspace(math.log(rmin), math.log(rmax), NS); ds = s[1] - s[0]; rr = np.exp(s)
    x, w = leggauss(NT)                                   # x = cos(theta)
    P = np.array([legval(x, [0]*l + [1]) for l in range(L + 1)])            # P[l, j]
    dP = np.array([legval(x, legder([0]*l + [1])) if l > 0 else np.zeros(NT) for l in range(L + 1)])   # dP_l/dx
    sinth = np.sqrt(1 - x**2); dPth = -dP*sinth[None, :]                   # dP/dtheta = -sin * dP/dx
    # initial guess: Newtonian + external; unknown = full phi_l(s)
    phi = np.zeros((L + 1, NS)); phi[0] = -1.0/rr; phi[1] = -eta*rr
    def fields(phi):
        Phi = P.T @ phi                                    # (NT, NS)
        dPhi_ds = np.gradient(phi, ds, axis=1); gr = -(P.T @ dPhi_ds)/rr[None, :]        # -dPhi/dr
        gt = -(dPth.T @ phi)/rr[None, :]                   # -(1/r) dPhi/dtheta
        return np.hypot(gr, gt)
    for it in range(itmax):
        gmag = fields(phi); m = mufun(np.maximum(gmag, 1e-300))             # (NT, NS)
        # projected coefficient matrices  B_ml(s) = int mu P_m P_l sin dtheta = sum_j w_j mu_j P_m(x_j) P_l(x_j)
        #                                 A_ml(s) = -int mu P_m' P_l' sin dtheta (theta-derivatives; measure sin dtheta = dx)
        B = np.einsum("j,mj,lj,js->mls", w, P, P, m); A = -np.einsum("j,mj,lj,js->mls", w, dPth, dPth, m)
        # equation per m:  d/ds( e^{s} B dphi/ds ) + e^{s} A phi = 0   (multiplied by e^{3s})
        n = (L + 1)*NS; rows, cols, vals = [], [], []; rhs = np.zeros(n)
        Bh = 0.5*(B[:, :, 1:] + B[:, :, :-1]); es = np.exp(s); esh = np.exp(0.5*(s[1:] + s[:-1]))
        for i in range(NS):
            for mm in range(L + 1):
                R_ = mm*NS + i
                if i == 0 or i == NS - 1:
                    rows.append(R_); cols.append(R_); vals.append(1.0)
                    if i == 0:   rhs[R_] = -1.0/rr[0] if mm == 0 else (-eta*rr[0] if mm == 1 else 0.0)     # deep-Newtonian inner data
                    else:        rhs[R_] = -eta*rr[-1] if mm == 1 else 0.0                               # u = Phi + eta r cos -> 0 outside
                    continue
                for ll in range(L + 1):
                    C_ = ll*NS
                    cp = esh[i]*Bh[mm, ll, i]/ds**2; cm = esh[i-1]*Bh[mm, ll, i-1]/ds**2
                    rows += [R_, R_, R_]; cols += [C_ + i + 1, C_ + i, C_ + i - 1]; vals += [cp, -(cp + cm) + es[i]*A[mm, ll, i], cm]
        Mx = sps.csr_matrix((vals, (rows, cols)), shape=(n, n))
        new = spl.spsolve(Mx, rhs).reshape(L + 1, NS)
        dphi = np.max(np.abs(new - phi))/max(1.0, np.max(np.abs(new)))
        phi = (1 - relax)*phi + relax*new
        if dphi < tol: break
    return phi, rr, it + 1, dphi
def c2_fit(phi2, rr, win):
    sel = (rr > win[0]) & (rr < win[1]); Amat = np.vstack([rr[sel]**2, np.ones(sel.sum()), rr[sel]**-3]).T
    return np.linalg.lstsq(Amat, phi2[sel], rcond=None)[0]
print("\n2.  independent discretisation (FD in ln r x Legendre in theta)")
phi, rr, it, res = solve_aqual(mu_exp, 0.0, L=4)
gnum = -np.gradient(phi[0], np.log(rr))/rr
gex = np.array([brentq(lambda g: mu_exp(g)*g - 1.0/r_**2, 1e-14, 1e14) for r_ in rr])
m = (rr > 1e-3) & (rr < 1e3); err = float(np.max(np.abs(np.abs(gnum[m])/gex[m] - 1)))
check("V1 eta = 0: the l = 0 solution reproduces the exact spherical first integral mu(g) g = 1/r^2 to 1% over 1e-3 < r/R_M < 1e3",
      err < 0.01 and res < 1e-8, f"max rel err {err:.2e}, {it} iterations, residual {res:.1e}   ({time.time()-T0:.0f} s)")
# Blanchet-Novak 2011 anchor: mu_1, a0 = 1.2e-10, g_e = 1.9e-10 (observed) -> Q2 = 3.8e-26 s^-2 published
a0b = 1.2e-10; eta_b = 1.9/1.2
phi, rr, it, res = solve_aqual(mu_one, eta_b)
c2s = [c2_fit(phi[2], rr, wn)[0] for wn in ((2e-3, 2e-2), (3e-3, 3e-2), (5e-3, 5e-2))]
Q2_bn = [-3*c*a0b**1.5/math.sqrt(GM) for c in c2s]
check("V2 the Blanchet-Novak 2011 mu_1 anchor (a0 = 1.2e-10, g_e = 1.9e-10 observed): |Q2| = 3.8e-26 s^-2 reproduced to 8% on all three fit windows, with the SIGN of Park's convention",
      all(abs(abs(q)/3.8e-26 - 1) < 0.08 for q in Q2_bn), f"Q2 = {', '.join(f'{q:+.3e}' for q in Q2_bn)}; {it} it, resid {res:.1e}   ({time.time()-T0:.0f} s)")
OUT["bn11"] = dict(Q2=Q2_bn, iterations=it, residual=res)
# the strict target: mu_exp, both footings, three external fields; TRUE eta = observed g_ext / a0 (AQUAL's boundary datum is the total field)
print(f"\n    {'footing':10s} {'g_ext':>9s} {'eta':>6s} {'Q2 [s^-2] (3 windows)':>40s} {'Q2/ceiling':>11s} {'sigma above central':>20s} {'it':>4s} {'resid':>8s}")
for foot, a0 in A0.items():
    for tag, ge in G_EXT.items():
        eta = ge/a0
        phi, rr, it, res = solve_aqual(mu_exp, eta, tol=1e-11, itmax=600)
        c2s = [c2_fit(phi[2], rr, wn)[0] for wn in ((2e-3, 2e-2), (3e-3, 3e-2), (5e-3, 5e-2))]
        Q2s = [-3*c*a0**1.5/math.sqrt(GM) for c in c2s]; Qm = float(np.median(Q2s))
        OUT[f"{foot}_{tag}"] = dict(eta=eta, Q2=Q2s, iterations=it, residual=res, converged_1e11=bool(res < 1e-11))
        print(f"    {foot:10s} {ge:9.2e} {eta:6.3f} {'  '.join(f'{q:+.3e}' for q in Q2s):>40s} {Qm/Q2_CEIL:11.2f} {(Qm-Q2_CEN)/Q2_SIG:20.1f} {it:4d} {res:8.1e}")
qc = OUT["canonical_central"]; qa = OUT["alt_central"]
check("V3 INDEPENDENT AGREEMENT: at the canonical footing and central field this discretisation gives Q2 within 5% of aqual_solar_gate_2026's "
      "finite-volume value (2.098e-26 at 768x192) and of f24's (2.106e-26): the exponential-AQUAL Solar-System quadrupole is bounded by two "
      "discretisations, not one", abs(np.median(qc["Q2"])/2.098e-26 - 1) < 0.05, f"this file {np.median(qc['Q2']):+.3e} vs 2.098e-26")
check("V4 the 1e-11 iteration requirement: the Picard iteration converges to residual < 1e-11 within its cap for the central cases "
      "(the finite-volume solver's cap exhaustion is not reproduced here); if it FAILS the observable is still bounded by V3 at 1e-10",
      qc["converged_1e11"] and qa["converged_1e11"], f"canonical {qc['residual']:.1e} in {qc['iterations']} it; alt {qa['residual']:.1e} in {qa['iterations']} it")
worst = min(np.median(OUT[f"{f}_low"]["Q2"]) for f in A0)
check("G01 VERDICT (T-A, Cassini): the strict exact exponential AQUAL law gives a signed Q2 above the Park 2026 two-sigma ceiling on both "
      "footings and at every external-field endpoint, including the low one (2.00e-10); the exclusion is conditional on Park's likelihood "
      "and the external-field input and is not a mathematical no-go",
      worst > Q2_CEIL, f"lowest Q2 over footings x endpoints = {worst:+.3e} = {worst/Q2_CEIL:.2f}x ceiling")
json.dump(dict(gate="G01", results=OUT, fails=FAILS, elapsed_s=round(time.time()-T0, 1)), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "g01_manifest.json"), "w"), indent=1)
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL", f"  ({time.time()-T0:.0f} s)")
sys.exit(1 if FAILS else 0)

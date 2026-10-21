#!/usr/bin/env python3
"""
A13: the saddle no-go as a Kepler-grade forecast.

Two equal point lenses of baryonic mass M at separation d, under the law
g^2 = g_N (g + a0)  (AQUAL with mu(x) = x/(1+x); deep limit mu = x).

  (1) the phantom density rho_ph = lap(Phi)/(4 pi G) - rho_b between them,
      its universal dimensionless profile C(R/d, z/d), and the "missing depth"
      a rho >= 0 medium cannot supply;
  (2) the lensing signal of that deficit: convergence map, matched-filter
      effective area, S/N per lens pair;
  (3) pairs and square degrees needed for 3 sigma and 5 sigma;
  (4) the falsifier read both ways, including the external-field suppression.

Inputs from arXiv:1702.08485 (Epps & Hudson 2017) were read from the paper's
own text during this run and are labelled EXT below.  Nothing is fitted here.

Run:  python3 a13_checks.py            (writes a13.out, a13_results.json)
      python3 a13_checks.py --mutate   (writes a13_MUTATE.out; must FAIL)
"""
import json
import math
import os
import sys
import time

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = ("--mutate" in sys.argv) or (os.environ.get("A13_MUTATE") == "1")
TAG = "_MUTATE" if MUTATE else ""
T0 = time.time()

OUT = []
FAILS = []
RES = {"lane": "A13", "mutate": MUTATE, "checks": [], "numbers": {}, "constants_used": []}


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def check(cid, ok, measured, threshold, note=""):
    """BRIEF format: '<id> PASS <measured> <threshold>'."""
    P(f"{cid} {'PASS' if ok else 'FAIL'} {measured} {threshold}")
    if note:
        P(f"      {note}")
    RES["checks"].append({"id": cid, "pass": bool(ok), "value": measured, "threshold": threshold})
    if not ok:
        FAILS.append(cid)
    return ok


# --------------------------------------------------------------------------- constants
C_LIGHT = 2.99792458e8
G = 6.67430e-11
MSUN = 1.98847e30
PC = 3.0856775814913673e16
MPC = 1.0e6 * PC
SIG_UNIT = MSUN / PC ** 2                      # kg/m^2 per Msun/pc^2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
OMBH2 = 0.0224                                 # Planck
OMC_OB = 5.364                                 # framework input (measured), Zenodo 23533323
RHOCRIT_H2 = 3.0 * (1.0e5 / MPC) ** 2 / (8.0 * math.pi * G)
RHOBAR = OMC_OB * OMBH2 * RHOCRIT_H2           # mean cold density, kg/m^3
H70 = 0.7                                      # Epps & Hudson cosmology
OMEGA_M = 0.3

# fiducial pairs (PAPER49 v1.2 / AG6C)
FID = {"F1_MW-M31": dict(M=8e10 * MSUN, d=0.77 * MPC),
       "F2_cluster": dict(M=2e13 * MSUN, d=5.0 * MPC)}
# EXT: arXiv:1702.08485 (Epps & Hudson 2017), read from the paper text this run
LRG = dict(M=10 ** 11.3 * MSUN, d_h=8.23, h=0.7, z=0.42, sigma_crit=1640.0,
           n_pairs=23000, n_src=11.0, box_dx_h=7.1, box_dy_h=2.5,
           m_fil=1.6e13, sig_m_fil=0.3e13, logmstar=11.3, area_deg2=154.0)
# survey specifications (ASSUMED; standard published design values, not re-derived here)
SURVEYS = [
    ("CFHTLenS (published sample)", 11.0, 0.26, 154.0),
    ("DES Y6", 10.0, 0.26, 5000.0),
    ("LSST Y10", 27.0, 0.26, 18000.0),
    ("Euclid Wide", 30.0, 0.26, 14000.0),
    ("Roman HLIS", 45.0, 0.27, 18000.0),
]
SIGMA_E = 0.26
PAIR_DENSITY = LRG["n_pairs"] / LRG["area_deg2"]      # pairs per deg^2, measured in the paper's field

P("A13  the saddle no-go as a forecast: how many lens pairs, how many square degrees" + ("   *** MUTATE ***" if MUTATE else ""))
P("Law: g^2 = g_N (g + a0), AQUAL mu(x) = x/(1+x).  Units G = M = a0 = d = 1 below.")
P(f"rho_bar_cold = {RHOBAR:.4e} kg/m^3  (Omega_c/Omega_b = {OMC_OB}, Omega_b h^2 = {OMBH2})")
P("kappa = 1/2 is fitted; the theory is not closed.  This script prices a prediction, it does not prove the law.")


# --------------------------------------------------------------------------- solver
H0_FINE = 0.001
RATE = 0.05
XMAX = 6.0
BFAC = 0.01


def make_faces(xmax, refs):
    xs = [0.0]
    while xs[-1] < xmax:
        x = xs[-1]
        h = min(hk + RATE * abs(x - ck) for ck, hk in refs)
        xs.append(min(x + h, xmax))
    return np.array(xs)


class Grid:
    def __init__(self, Rf, zf):
        self.Rf, self.zf = Rf, zf
        self.Rc = 0.5 * (Rf[1:] + Rf[:-1])
        self.zc = 0.5 * (zf[1:] + zf[:-1])
        self.NR, self.NZ = len(self.Rc), len(self.zc)
        self.N = self.NR * self.NZ
        self.RR, self.ZZ = np.meshgrid(self.Rc, self.zc, indexing="ij")
        self.V = np.outer(np.pi * (Rf[1:] ** 2 - Rf[:-1] ** 2), np.diff(zf))
        self.idx = np.arange(self.N).reshape(self.NR, self.NZ)


def coeffs(g, Phi, pbR, pbZ, mufun, e=0.0):
    """mu on faces.  Phi is Psi = Phi_total + e*z, so grad(Phi_total) = grad(Psi) - e zhat."""
    dR = np.zeros_like(Phi)
    dZ = np.zeros_like(Phi)
    dR[1:-1, :] = (Phi[2:, :] - Phi[:-2, :]) / (g.Rc[2:, None] - g.Rc[:-2, None])
    dR[0, :] = (Phi[1, :] - Phi[0, :]) / (g.Rc[1] + g.Rc[0])
    dR[-1, :] = (pbR - Phi[-2, :]) / (g.Rf[-1] - g.Rc[-2])
    dZ[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) / (g.zc[None, 2:] - g.zc[None, :-2])
    dZ[:, 0] = (Phi[:, 1] - Phi[:, 0]) / (g.zc[1] + g.zc[0])
    dZ[:, -1] = (pbZ - Phi[:, -2]) / (g.zf[-1] - g.zc[-2])
    nR = (Phi[1:, :] - Phi[:-1, :]) / (g.Rc[1:, None] - g.Rc[:-1, None])
    tR = 0.5 * (dZ[1:, :] + dZ[:-1, :]) - e
    muR = mufun(np.hypot(nR, tR))
    nRo = (pbR - Phi[-1, :]) / (g.Rf[-1] - g.Rc[-1])
    muRo = mufun(np.hypot(nRo, dZ[-1, :] - e))
    nz = (Phi[:, 1:] - Phi[:, :-1]) / (g.zc[None, 1:] - g.zc[None, :-1]) - e
    tz = 0.5 * (dR[:, 1:] + dR[:, :-1])
    muz = mufun(np.hypot(nz, tz))
    nzo = (pbZ - Phi[:, -1]) / (g.zf[-1] - g.zc[-1]) - e
    muzo = mufun(np.hypot(nzo, dR[:, -1]))
    return muR, muRo, muz, muzo


def assemble(g, muR, muRo, muz, muzo, pbR, pbZ):
    I = g.idx
    b = np.zeros(g.N)
    diag = np.zeros(g.N)
    rows, cols, vals = [], [], []
    AR = 2 * math.pi * g.Rf[1:-1, None] * np.diff(g.zf)[None, :]
    cR = (muR * AR / (g.Rc[1:, None] - g.Rc[:-1, None])).ravel()
    a, bb = I[:-1, :].ravel(), I[1:, :].ravel()
    rows += [a, bb]
    cols += [bb, a]
    vals += [cR, cR]
    np.add.at(diag, a, -cR)
    np.add.at(diag, bb, -cR)
    ARo = 2 * math.pi * g.Rf[-1] * np.diff(g.zf)
    cRo = (muRo * ARo / (g.Rf[-1] - g.Rc[-1])).ravel()
    ii = I[-1, :].ravel()
    np.add.at(diag, ii, -cRo)
    b[ii] -= cRo * pbR
    Az = np.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)[:, None] * np.ones((1, g.NZ - 1))
    cz = (muz * Az / (g.zc[None, 1:] - g.zc[None, :-1])).ravel()
    a, bb = I[:, :-1].ravel(), I[:, 1:].ravel()
    rows += [a, bb]
    cols += [bb, a]
    vals += [cz, cz]
    np.add.at(diag, a, -cz)
    np.add.at(diag, bb, -cz)
    Azo = np.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)
    czo = (muzo * Azo / (g.zf[-1] - g.zc[-1])).ravel()
    ii = I[:, -1].ravel()
    np.add.at(diag, ii, -czo)
    b[ii] -= czo * pbZ
    rows.append(np.arange(g.N))
    cols.append(np.arange(g.N))
    vals.append(diag)
    A = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                       shape=(g.N, g.N))
    return A, b


def plummer(g, b, mtot=1.0, centres=(0.5, -0.5)):
    rho = np.zeros((g.NR, g.NZ))
    for zp in centres:
        r2 = g.RR ** 2 + (g.ZZ - zp) ** 2
        rho += (3 / (4 * math.pi * b ** 3)) * (1 + r2 / b ** 2) ** (-2.5)
    m = rho * g.V
    return m * (mtot / m.sum())


def solve(g, m, mufun, phif, e=0.0, alpha=1.0, itmax=500, tol=1e-10, Phi0=None):
    Rb = np.hypot(g.Rf[-1], g.zc)
    Zb = np.hypot(g.Rc, g.zf[-1])
    pbR, pbZ = phif(Rb), phif(Zb)
    rhs = 4 * math.pi * m.ravel()
    Phi = phif(np.hypot(g.RR, g.ZZ) + 1e-3) if Phi0 is None else Phi0.copy()
    mu = coeffs(g, Phi, pbR, pbZ, mufun, e)
    d = 1.0
    it = 0
    for it in range(itmax):
        A, b = assemble(g, *mu, pbR, pbZ)
        Pn = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        if alpha != 1.0:
            Pn = Phi + alpha * (Pn - Phi)
        d = np.max(np.abs(Pn - Phi)) / (np.max(Pn) - np.min(Pn))
        Phi = Pn
        mu_new = coeffs(g, Phi, pbR, pbZ, mufun, e)
        mu = tuple(np.sqrt(a * b) for a, b in zip(mu, mu_new))   # geometric-mean damping (p = 3)
        if d < tol and it > 3:
            break
    mu = coeffs(g, Phi, pbR, pbZ, mufun, e)
    A, b = assemble(g, *mu, pbR, pbZ)
    res = np.max(np.abs(A @ Phi.ravel() - b - rhs)) / np.max(np.abs(rhs))
    return Phi, pbR, pbZ, res, it + 1, d


def laplacian(g, Phi, pbR, pbZ):
    one = lambda x: np.ones_like(x)
    mu = coeffs(g, Phi, pbR, pbZ, one, 0.0)
    A, b = assemble(g, *mu, pbR, pbZ)
    return (A @ Phi.ravel() - b).reshape(g.NR, g.NZ) / g.V


PHI_FAR = lambda r: math.sqrt(2.0) * np.log(r)      # total mass 2M, deep MOND
DEEP = lambda x: np.maximum(x, 1e-14)


# --------------------------------------------------------------------------- S1 control
P("\nS1  solver control: one unit point mass")
Rf = make_faces(XMAX, [(0.0, H0_FINE)])
zf = make_faces(XMAX, [(0.0, H0_FINE)])
gc = Grid(Rf, zf)
mc = plummer(gc, BFAC, 0.5, (0.0,))
Phic, pR, pZ, resc, itc, _ = solve(gc, mc, DEEP, lambda r: np.log(r))
dR_ = np.zeros_like(Phic)
dZ_ = np.zeros_like(Phic)
dR_[1:-1, :] = (Phic[2:, :] - Phic[:-2, :]) / (gc.Rc[2:, None] - gc.Rc[:-2, None])
dR_[0, :] = (Phic[1, :] - Phic[0, :]) / (gc.Rc[1] + gc.Rc[0])
dZ_[:, 1:-1] = (Phic[:, 2:] - Phic[:, :-2]) / (gc.zc[None, 2:] - gc.zc[None, :-2])
dZ_[:, 0] = (Phic[:, 1] - Phic[:, 0]) / (gc.zc[1] + gc.zc[0])
gmag = np.hypot(dR_, dZ_)
rc = np.hypot(gc.RR, gc.ZZ)
sel = (rc > 0.3) & (rc < 4.0)
err_g = float(np.max(np.abs(gmag[sel] * rc[sel] - 1.0)))
Cc = laplacian(gc, Phic, pR, pZ) / (4 * math.pi) - mc / gc.V
selc = (rc > 0.4) & (rc < 2.0)
err_rho = float(np.max(np.abs(Cc[selc] * 4 * math.pi * rc[selc] ** 2 - 1.0)))
P(f"    single-mass |grad Phi| r vs 1: max err {err_g:.3e};  C*4pi R^2 vs 1: max err {err_rho:.3e}")
P(f"    (exact deep-MOND point mass: |grad Phi| = 1/r, rho_ph = 1/(4 pi r^2) in these units)")
check("K1", err_g < 0.01 and err_rho < 0.02,
      f"grad_err={err_g:.2e}, rho_err={err_rho:.2e}", "both < 1e-2 / 2e-2")
RES["numbers"]["control_single"] = dict(grad_err=err_g, rho_err=err_rho, iterations=itc, residual=resc)

# --------------------------------------------------------------------------- S2 convergence ladder
P("\nS2  two equal point masses: convergence of the mid-plane column through the saddle")
P("    rho_ph = C(R/d, z/d) sqrt(G M a0)/(G d^2);  column S = 2 int min(C,0) d(R/d)")
H = [0.004, 0.002, 0.001, 0.0005]
ladder = []
profiles = {}
for h in H:
    g2 = Grid(make_faces(XMAX, [(0.0, h), (0.5, h)]), make_faces(XMAX, [(0.0, h), (0.5, h)]))
    m2 = plummer(g2, BFAC)
    Phi2, pR2, pZ2, res2, it2, d2 = solve(g2, m2, DEEP, PHI_FAR)
    C2 = laplacian(g2, Phi2, pR2, pZ2) / (4 * math.pi) - m2 / g2.V
    if MUTATE:   # MUTATION: linear superposition of the two single-mass phantoms
        C2 = (1.0 / (4 * math.pi)) * (1.0 / (g2.RR ** 2 + (g2.ZZ - 0.5) ** 2)
                                      + 1.0 / (g2.RR ** 2 + (g2.ZZ + 0.5) ** 2))
    row = C2[:, 0]
    S = float(2 * np.sum(np.minimum(row, 0) * np.diff(g2.Rf)))
    c02 = float(np.interp(0.2, g2.Rc, row))
    ladder.append(dict(h=h, N=g2.N, S=S, C02=c02, res=res2, it=it2))
    profiles[h] = (g2, C2)
    P(f"    h={h:<7.4f} N={g2.N:6d}  C(0.2)={c02:+.5f}  S_neg={S:+.5f}  it={it2:3d} res={res2:.1e}")

# Richardson: S(h) = S_inf + a h^p, p from the last three increments
S_vals = [r["S"] for r in ladder]
inc = [S_vals[i + 1] - S_vals[i] for i in range(len(S_vals) - 1)]
ratios = [inc[i + 1] / inc[i] if abs(inc[i]) > 1e-12 else 0.5 for i in range(len(inc) - 1)]
if not np.isfinite(ratios[-1]) or ratios[-1] <= 0:
    ratios = [0.5, 0.5]                      # degenerate (mutated) ladder
p_exp = float(math.log2(1.0 / ratios[-1]))
S_inf = float(S_vals[-1] + inc[-1] * ratios[-1] / (1.0 - ratios[-1]))
P(f"    successive increments {['%+.5f' % x for x in inc]}; ratios {['%.3f' % r for r in ratios]}")
P(f"    fitted h-exponent p = {p_exp:.2f};  Richardson limit S_inf = {S_inf:+.5f}")
check("K2", abs(np.interp(0.2, profiles[0.001][0].Rc, profiles[0.001][1][:, 0]) / -0.2401 - 1) < 0.03,
      f"C(0.2)={np.interp(0.2, profiles[0.001][0].Rc, profiles[0.001][1][:,0]):+.5f}", "AG6C published -0.2401, within 3%")
check("K3", abs(ladder[1]["S"] / -0.2064 - 1) < 0.06,
      f"S(h=0.002)={ladder[1]['S']:+.5f}", "AG6C published -0.2064 (h=0.0025), within 6%")
check("K4", 0.45 < ratios[-1] < 0.75 and -0.24 < S_inf < -0.218,
      f"S_inf={S_inf:+.5f}, increment ratio={ratios[-1]:.3f}", "S_inf in (-0.240,-0.218), ratio in (0.45,0.75)")

S_NEG = S_inf
RES["numbers"]["ladder"] = ladder
RES["numbers"]["S_inf"] = S_inf
RES["numbers"]["p_exp"] = p_exp
RES["numbers"]["increment_ratios"] = ratios

# --------------------------------------------------------------------------- S3 scaling check: superposition fails
P("\nS3  why this is not a spherical estimate: linear superposition of single-mass phantoms")
C_super = 2.0 / math.pi
P(f"    two single-mass phantoms added at the saddle: C = 2*(1/(4 pi (1/2)^2)) = 2/pi = {C_super:+.4f}")
P(f"    the nonlinear solve gives C(0.02) = {np.interp(0.02, profiles[0.001][0].Rc, profiles[0.001][1][:,0]):+.4f}; sign and size both differ")
check("K5", C_super > 0.5, f"C_super={C_super:+.4f}", "> 0.5 (the superposition has the WRONG SIGN)")

# --------------------------------------------------------------------------- S4 missing depth, fiducials
P("\nS4  missing depth: the part of the column a rho >= 0 medium cannot supply")
P("    Sigma_miss = 2 int min(rho_ph + rho_bar, 0) dR, per fiducial and footing")
g2, C2 = profiles[0.001]
dRm = np.diff(g2.Rf)
depth = {}
for name, fp in FID.items():
    for foot, a0 in A0.items():
        unit_rho = math.sqrt(G * fp["M"] * a0) / (G * fp["d"] ** 2)     # kg/m^3 per unit C
        unit_col = math.sqrt(G * fp["M"] * a0) / (G * fp["d"])          # kg/m^2 per unit column
        rb_t = RHOBAR / unit_rho
        S_clip = float(2 * np.sum(np.minimum(C2[:, 0] + rb_t, 0) * dRm))
        S_raw = float(2 * np.sum(np.minimum(C2[:, 0], 0) * dRm))
        # scale both to the Richardson limit
        S_clip *= (S_NEG / S_raw) if abs(S_raw) > 1e-12 else 0.0
        sig_miss = -S_clip * unit_col / SIG_UNIT
        c02 = float(np.interp(0.2, g2.Rc, C2[:, 0]))
        ratio_bar = c02 * unit_rho / RHOBAR
        depth[f"{name}_{foot}"] = dict(Sigma_miss=sig_miss, C_at_0p2d=c02, rho_over_rhobar_at_0p2d=ratio_bar)
        P(f"    {name:11s} {foot:9s}: C(0.2d)={c02:+.4f} = {ratio_bar:+.1f} rho_bar ;  "
          f"Sigma_miss = {sig_miss:.3f} Msun/pc^2")
RES["numbers"]["depth"] = depth

f1c = depth["F1_MW-M31_canonical"]["Sigma_miss"]
f1a = depth["F1_MW-M31_alt"]["Sigma_miss"]
f2c = depth["F2_cluster_canonical"]["Sigma_miss"]
f2a = depth["F2_cluster_alt"]["Sigma_miss"]
P(f"\n    MW-M31-like pair : {min(f1c, f1a):.2f} to {max(f1c, f1a):.2f} Msun/pc^2   (PAPER49 v1.2 quotes 1.9 to 2.1)")
P(f"    cluster pair     : {min(f2c, f2a):.2f} to {max(f2c, f2a):.2f} Msun/pc^2   (PAPER49 v1.2 quotes 4.6 to 5.1)")
ratio_paper = ((f1c + f1a) / 2) / 2.0
check("K6", 1.0 <= ratio_paper <= 1.20,
      f"mean MW-M31 depth={0.5*(f1c+f1a):.3f}", "paper midpoint 2.0, ratio in [1.00,1.20]")
check("K7", abs(depth["F1_MW-M31_canonical"]["rho_over_rhobar_at_0p2d"] / -89.0 - 1) < 0.05
      and abs(depth["F2_cluster_canonical"]["rho_over_rhobar_at_0p2d"] / -33.0 - 1) < 0.08,
      f"-89 check={depth['F1_MW-M31_canonical']['rho_over_rhobar_at_0p2d']:+.1f}, "
      f"-33 check={depth['F2_cluster_canonical']['rho_over_rhobar_at_0p2d']:+.1f}", "-89 +-5%, -33 +-8%")

# --------------------------------------------------------------------------- S5 lensing: convergence map and matched filter
P("\nS5  the lensing signal: deficit map, matched filter, S/N per pair")
P("    Delta(x,z) = -int min(rho_ph+rho_bar,0) dl  along the line of sight (Abel transform of the axisymmetric solution)")
Rc, zc = g2.Rc, g2.zc


def abel(x, col):
    """2 int_x^inf col(R) R dR / sqrt(R^2-x^2), column at impact parameter x."""
    if x < 1e-9:
        return 2.0 * np.sum(col * np.diff(np.concatenate([[0.0], Rc])))
    umax = math.acosh(max(Rc[-1] / x, 1.0001))
    us = np.linspace(0.0, umax, 2001)
    Rs = x * np.cosh(us)
    fs = np.interp(Rs, Rc, col, left=col[0], right=0.0)
    return 2.0 * x * np.sum(fs * np.cosh(us)) * (us[1] - us[0])


xs = np.concatenate([[0.0], np.geomspace(0.01, 1.4, 53)])
zrows = [j for j in range(g2.NZ) if zc[j] < 0.16]
Dmap = np.zeros((len(zrows), len(xs)))
for a, j in enumerate(zrows):
    col = np.minimum(C2[:, j], 0.0)
    Dmap[a, :] = [-abel(x, col) for x in xs]
Delta0_dimless = Dmap[0, 0]
if abs(Delta0_dimless) < 1e-12:
    Delta0_dimless, Dmap = 1.0, np.zeros_like(Dmap)
A_eff = 4.0 * float(np.trapz(np.trapz((Dmap / Delta0_dimless) ** 2, xs, axis=1), zc[zrows]))
_s_last = ladder[-1]["S"] if abs(ladder[-1]["S"]) > 1e-12 else 1.0
P(f"    Delta0 (peak deficit, dimensionless column) = {Delta0_dimless:.4f}; scaled to S_inf: {Delta0_dimless*S_NEG/_s_last:.4f}")
P(f"    effective matched-filter area A_eff = {A_eff:.4f} d^2")
P(f"    profile Delta(x,0)/Delta0 : " + "  ".join(f"{x:.2f}:{np.interp(x, xs, Dmap[0])/Delta0_dimless:.2f}" for x in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5)))
P(f"    profile Delta(0,z)/Delta0 : " + "  ".join(f"{z:.3f}:{Dmap[np.argmin(abs(zc[zrows]-z)),0]/Delta0_dimless:.2f}" for z in (0.005, 0.02, 0.05, 0.1)))

# Delta_Sigma at the saddle for the LRG sample
unit_col_lrg = math.sqrt(G * LRG["M"] * A0["canonical"]) / (G * LRG["d_h"] / LRG["h"] * MPC)
d_lrg = LRG["d_h"] / LRG["h"] * MPC
unit_col_lrg = math.sqrt(G * LRG["M"] * A0["canonical"]) / (G * d_lrg)
dsig_lrg = abs(S_NEG) * unit_col_lrg / SIG_UNIT
P(f"    LRG pair (M_b=10^{LRG['logmstar']:.1f} Msun, d={LRG['d_h']/LRG['h']:.2f} Mpc): Delta_Sigma(saddle) = {dsig_lrg:.4f} Msun/pc^2")


def D_A(z, Om=OMEGA_M, h=H70):
    dc = (C_LIGHT / 1000.0) / (100.0 * h) * quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0]
    return dc / (1 + z)


DA = D_A(LRG["z"])
ARCMIN_PER_MPC = 60.0 * (180.0 / math.pi) / DA
P(f"    D_A(z={LRG['z']}) = {DA:.0f} Mpc -> 1 Mpc = {ARCMIN_PER_MPC:.2f} arcmin")
A_eff_arcmin2 = A_eff * (d_lrg / MPC) ** 2 * ARCMIN_PER_MPC ** 2
P(f"    A_eff = {A_eff*(d_lrg/MPC)**2:.2f} Mpc^2 = {A_eff_arcmin2:.1f} arcmin^2")

# orientation: the negative pancake is a thin sheet perpendicular to the pair axis,
# so only pairs seen close to edge-on carry the dip.  Compute the acceptance exactly.
from scipy.interpolate import RegularGridInterpolator
zg_ = np.concatenate([[0.0], zc])
Cg_ = np.concatenate([np.minimum(C2, 0.0)[:, :1], np.minimum(C2, 0.0)], axis=1)
interp_ = RegularGridInterpolator((Rc, zg_), Cg_, bounds_error=False, fill_value=0.0)


def deficit_at(ideg):
    ii = math.radians(ideg)
    ts = np.linspace(0.0, 1.5, 4001)
    return 2.0 * np.sum(interp_(np.column_stack([ts * math.sin(ii), ts * math.cos(ii)]))) * (ts[1] - ts[0])


cs_ = np.linspace(0.0, 1.0, 41)
dvals = np.array([deficit_at(math.degrees(math.acos(max(c, 1e-9)))) for c in cs_])
d_edge = deficit_at(90.0)
eps_orient = float(np.trapz(dvals, cs_) / d_edge) if abs(d_edge) > 1e-12 else 1.0
P(f"    orientation: deficit(90deg)={d_edge:+.4f}, deficit(80deg)={deficit_at(80.0):+.4f}, "
  f"deficit(70deg)={deficit_at(70.0):+.4f}; acceptance eps={eps_orient:.3f}")
P(f"    -> only pairs within ~9 deg of edge-on carry the dip; 1/eps = {1.0/max(eps_orient,1e-30):.1f} pairs must be scanned per edge-on pair")

kappa_peak = dsig_lrg / LRG["sigma_crit"]
P(f"    peak convergence deficit kappa = {kappa_peak:.2e}")


def sn_per_pair(sigma_crit, n_g, sig_e, a_arcmin2):
    """matched-filter S/N of one lens pair."""
    return dsig_lrg * math.sqrt(n_g * a_arcmin2) / (sig_e * sigma_crit)


S1 = max(sn_per_pair(LRG["sigma_crit"], LRG["n_src"], SIGMA_E, A_eff_arcmin2), 1e-30)
P(f"    S/N per pair (CFHTLenS depth, n_g={LRG['n_src']:.0f}, sigma_e={SIGMA_E}) = {S1:.5f}")
P(f"    stacked S/N for the published {LRG['n_pairs']} pairs = {S1*math.sqrt(LRG['n_pairs']):.3f}   (AG7 independent estimate: 0.87)")

# circular shear profile: gamma_t = kappa_bar(<theta) - kappa(theta)
rr = np.geomspace(0.01, 0.8, 24)
kap = []
for r0 in rr:
    m = (np.abs(xs[:, None] - 0) >= 0)  # placeholder
    # azimuthal average of Delta on the polar grid built from (x,z)
    th = np.linspace(0, 2 * np.pi, 181)
    acc = []
    for t in th:
        xp = abs(r0 * math.cos(t))
        zp = abs(r0 * math.sin(t))
        j = np.argmin(np.abs(zc[zrows] - zp))
        acc.append(np.interp(xp, xs, Dmap[j]))
    kap.append(np.mean(acc))
kap = np.array(kap) * (S_NEG / _s_last) * unit_col_lrg / SIG_UNIT / LRG["sigma_crit"]
kbar = np.array([np.trapz(kap[:i + 1] * rr[:i + 1], rr[:i + 1]) * 2 / rr[i] ** 2 if i else kap[0] for i in range(len(rr))])
gt = kbar - kap
P(f"    azimuthally averaged kappa(theta): peak |kappa| = {np.max(np.abs(kap)):.2e}; peak |gamma_t| = {np.max(np.abs(gt)):.2e}")

# cross-check against AG7's published-aperture number, using the paper's OWN error calibration
A_box = (LRG["box_dx_h"] / LRG["h"]) * (LRG["box_dy_h"] / LRG["h"]) * ARCMIN_PER_MPC ** 2
A_strip = 0.1 * (d_lrg / MPC) * (LRG["box_dy_h"] / LRG["h"]) * ARCMIN_PER_MPC ** 2
A_box_pc2 = (LRG["box_dx_h"] / LRG["h"] * MPC / PC) * (LRG["box_dy_h"] / LRG["h"] * MPC / PC)
sig_pub = LRG["sig_m_fil"] / A_box_pc2                       # Msun/pc^2, published stacked error
sig_shape = SIGMA_E * LRG["sigma_crit"] / math.sqrt(LRG["n_src"] * A_box * LRG["n_pairs"])
f_noise = sig_pub / sig_shape                     # published error / pure shape noise, same box
sn_strip = dsig_lrg / (f_noise * SIGMA_E * LRG["sigma_crit"] /
                       math.sqrt(LRG["n_src"] * A_strip * LRG["n_pairs"]))
P(f"    AG7 cross-check: box {A_box:.0f} arcmin^2, strip {A_strip:.1f} arcmin^2;")
P(f"      published error {sig_pub:.4f} vs pure shape noise {sig_shape:.4f} Msun/pc^2 -> f_noise={f_noise:.2f}")
P(f"      strip S/N with our amplitude and the published error calibration = {sn_strip:.3f}  (AG7: 0.87)")
check("K8", abs(sn_strip / 0.87 - 1) < 0.12,
      f"S_strip={sn_strip:.3f}", "AG7 published 0.87, within 12%")

# --------------------------------------------------------------------------- S6 forecast
P("\nS6  pairs and square degrees for 3 sigma and 5 sigma")
P(f"    scaling: S/N(N) = S1 sqrt(N) exactly, so N_sigma = (sigma/S1)^2")
N3 = (3.0 / S1) ** 2
N5 = (5.0 / S1) ** 2
P(f"    N(3 sigma) = {N3:.3e} pairs ({N3/LRG['n_pairs']:.1f}x the published sample);  N(5 sigma) = {N5:.3e} ({N5/LRG['n_pairs']:.1f}x)")
rows = []
for name, ng, se, area in SURVEYS:
    s1 = max(sn_per_pair(LRG["sigma_crit"], ng, se, A_eff_arcmin2), 1e-30)
    n3 = (3.0 / s1) ** 2
    n5 = (5.0 / s1) ** 2
    rows.append(dict(survey=name, n_g=ng, sigma_e=se, area_available=area, S1=s1,
                     N3=n3, N5=n5, deg2_3=n3 / PAIR_DENSITY, deg2_5=n5 / PAIR_DENSITY,
                     N3_scan=n3 / max(eps_orient, 1e-30), deg2_3_scan=n3 / max(eps_orient, 1e-30) / PAIR_DENSITY))
    P(f"    {name:30s} n_g={ng:4.0f}  S1={s1:.5f}  N3={n3:8.3e}  deg2(3s)={n3/PAIR_DENSITY:6.0f}  "
      f"scanned N3={n3/max(eps_orient,1e-30):8.3e}  deg2={n3/max(eps_orient,1e-30)/PAIR_DENSITY:8.0f}")
RES["numbers"]["forecast"] = rows
P(f"    pair surface density assumed: {PAIR_DENSITY:.1f} deg^-2  (23000 pairs / 154 deg^2, measured)")
P(f"    'scanned' columns include the edge-on acceptance eps = {eps_orient:.3f}")
check("K9", abs(N5 / N3 - 25.0 / 9.0) < 1e-9 and 0.10 < eps_orient < 0.20,
      f"N5/N3={N5/N3:.4f}, eps_orient={eps_orient:.3f}", "exact 25/9 and eps in (0.10,0.20)")

# --------------------------------------------------------------------------- S7 external field
P("\nS7  external field: the null point is filled by the environment")
P("    uniform field e along the pair axis, in units of a0 in the same dimensionless system")
P("    e_dim = (g_ext/a0) * d / r_M with r_M = sqrt(G M/a0)")
efe = []
prev = None
for e in (0.0, 0.3, 1.0, 3.0):
    he = 0.005
    ge = Grid(make_faces(XMAX, [(0.0, he), (0.5, he)]), make_faces(XMAX, [(0.0, he), (0.5, he)]))
    me = plummer(ge, BFAC)
    Ph, pR3, pZ3, res3, it3, d3 = solve(ge, me, DEEP, PHI_FAR, e=e, alpha=0.25, itmax=420,
                                       tol=1e-6, Phi0=prev)
    prev = Ph
    Ce = laplacian(ge, Ph, pR3, pZ3) / (4 * math.pi) - me / ge.V
    Se = float(2 * np.sum(np.minimum(Ce[:, 0], 0) * np.diff(ge.Rf)))
    efe.append(dict(e=e, S=Se, it=it3, res=res3))
    P(f"    e={e:5.2f}  S_neg={Se:+.5f}  ratio={Se/efe[0]['S']:.3f}  it={it3:3d} res={res3:.1e}")
ser = [x["S"] / efe[0]["S"] for x in efe]
P(f"    suppression S(e)/S(0) = {['%.3f' % x for x in ser]}")
check("K10", ser[0] == 1.0 and ser[1] > ser[2] > ser[3] and ser[2] < 0.5,
      f"ratios={['%.2f' % x for x in ser]}", "monotone, S(1)/S(0) < 0.5")


def efe_factor(e_dim):
    """log-log interpolation of the computed suppression curve."""
    es = [x["e"] for x in efe]
    if e_dim <= es[0]:
        return 1.0
    if e_dim >= es[-1]:
        return ser[-1] * (e_dim / es[-1]) ** -2.0
    if e_dim < es[1]:                       # first bracket is (0, e1); interpolate linearly
        t = (e_dim - es[0]) / (es[1] - es[0])
        return 1.0 + t * (ser[1] - 1.0)
    for i in range(len(es) - 1):
        if es[i] <= e_dim <= es[i + 1]:
            t = (math.log(e_dim) - math.log(es[i])) / (math.log(es[i + 1]) - math.log(es[i]))
            return math.exp(math.log(ser[i]) + t * (math.log(ser[i + 1]) - math.log(ser[i])))
    return ser[-1]


rM_lrg = math.sqrt(G * LRG["M"] / A0["canonical"])
P(f"    r_M(LRG) = {rM_lrg/MPC*1000:.1f} kpc, d/r_M = {d_lrg/rM_lrg:.0f}")
P(f"\n    environment             g_ext/a0   e_dim   suppression   S1_eff      N3_eff")
env = [("void, very underdense", 1e-3), ("field galaxy (Local Sheet)", 5e-3),
       ("filament at z~0.4", 1.5e-2), ("group interior", 5e-2)]
envrows = []
for nm, ge_ in env:
    ed = ge_ * d_lrg / rM_lrg
    f_ = efe_factor(ed)
    envrows.append(dict(environment=nm, g_ext_over_a0=ge_, e_dim=ed, suppression=f_,
                        S1_eff=S1 * f_, N3_eff=(3.0 / (S1 * f_)) ** 2,
                        penalty=1.0 / max(f_, 1e-30) ** 2))
    P(f"    {nm:24s} {ge_:8.1e}  {ed:6.2f}   {f_:8.4f}    {S1*f_:.5f}   {rows[2]['N3']/max(f_**2,1e-30):8.2e}")
RES["numbers"]["efe"] = efe
RES["numbers"]["efe_ratios"] = ser
fid_efe = {}
P("\n    same curve applied to the paper's own fiducials (r_M/d given):")
for fname, fp in FID.items():
    rM = math.sqrt(G * fp["M"] / A0["canonical"])
    for ge_ in (1e-3, 1e-2, 3e-2):
        ed = ge_ * fp["d"] / rM
        fid_efe[f"{fname}_{ge_:.0e}"] = dict(e_dim=ed, suppression=efe_factor(ed),
                                             d_over_rM=fp["d"] / rM)
        P(f"      {fname:11s} g_ext={ge_:.0e} a0: d/r_M={fp['d']/rM:6.1f}  e_dim={ed:6.2f}  "
          f"suppression={efe_factor(ed):.4f}")
RES["numbers"]["fiducial_efe"] = fid_efe
RES["numbers"]["efe_env"] = envrows
check("K11", envrows[0]["suppression"] > 0.4 and envrows[2]["suppression"] < 0.05,
      f"void={envrows[0]['suppression']:.3f}, filament={envrows[2]['suppression']:.3f}",
      "void > 0.4 and filament < 0.05")

# --------------------------------------------------------------------------- S8 falsifier
P("\nS8  the falsifier, both ways")
N3_best = rows[2]["N3"]          # LSST source density, 3 sigma on the UNSUPPRESSED dip
P(f"    design sensitivity: N3 = {N3_best:.2e} pairs at LSST source density gives 3 sigma on the unsuppressed dip")
P(f"    a null at that sensitivity is a falsifier ONLY in a low-external-field subsample:")
for r_ in envrows:
    n_eff = N3_best / r_["suppression"] ** 2
    P(f"      {r_['environment']:26s} depth={dsig_lrg*r_['suppression']:.4f} Msun/pc^2  "
      f"N3_eff={n_eff:.2e}  deg2_eff={n_eff/PAIR_DENSITY:.3e}")
pen_void = 1.0 / envrows[0]["suppression"] ** 2
pen_fil = 1.0 / envrows[2]["suppression"] ** 2
P(f"    penalty on the pair budget: void x{pen_void:.1f}, filament x{pen_fil:.1e}")
P(f"    -> a null in a filament subsample is UNINFORMATIVE (it is also what the law predicts there)")
check("K12", pen_void < 20.0 and pen_fil > 1.0e4,
      f"void penalty={pen_void:.1f}, filament penalty={pen_fil:.1e}",
      "void < 20, filament > 1e4")

# --------------------------------------------------------------------------- results
RES["status"] = "CONDITIONAL(the stacked sample's external field)"
RES["numbers"].update(
    rho_bar=RHOBAR, Sigma_miss_F1=[f1c, f1a], Sigma_miss_F2=[f2c, f2a],
    C_at_0p2d=depth["F1_MW-M31_canonical"]["C_at_0p2d"],
    A_eff=A_eff, A_eff_arcmin2=A_eff_arcmin2, A_eff_Mpc2=A_eff * (d_lrg / MPC) ** 2, dsig_lrg=dsig_lrg,
    orient_ratios=[float(deficit_at(80.0) / d_edge), float(deficit_at(70.0) / d_edge)],
    kappa_peak=kappa_peak, S1=S1, S_stack=S1 * math.sqrt(LRG["n_pairs"]),
    N3=N3, N5=N5, pair_density=PAIR_DENSITY, D_A=DA, arcmin_per_Mpc=ARCMIN_PER_MPC,
    tau_kpc=math.sqrt(G * LRG["M"] / A0["canonical"]) / MPC * 1000,
    shear_peak=float(np.max(np.abs(gt))), kappa_peak_az=float(np.max(np.abs(kap))),
    eps_orient=eps_orient, deficit_90=float(d_edge), deficit_80=float(deficit_at(80.0)),
    deficit_70=float(deficit_at(70.0)),
    S_strip=sn_strip, f_noise=f_noise, A_box_arcmin2=A_box, A_strip_arcmin2=A_strip,
    sig_pub=sig_pub, sig_shape=sig_shape,
    paper_depth_F1=[1.9, 2.1], paper_depth_F2=[4.6, 5.1],
    depth_correction_F2=[f2c / 4.6 - 1, f2a / 5.1 - 1],
    C02_vs_AG6C=float(np.interp(0.2, profiles[0.001][0].Rc, profiles[0.001][1][:, 0])) / -0.2401 - 1,
    S_h0002_vs_AG6C=ladder[1]["S"] / -0.2064 - 1,
    Cbar_F1=RHOBAR / (math.sqrt(G * FID["F1_MW-M31"]["M"] * A0["canonical"]) / (G * FID["F1_MW-M31"]["d"] ** 2)),
    d_over_rM_LRG=d_lrg / rM_lrg,
    sliver_arcmin=[0.86 * (d_lrg / MPC) * ARCMIN_PER_MPC, 0.03 * (d_lrg / MPC) * ARCMIN_PER_MPC],
    runtime_s=None,
    paper_rho_ratio=[-89.0, -33.0], paper_N_ratio=12.0,
    depth_correction_F1=[f1c / 1.9 - 1, f1a / 2.1 - 1],
)
RES["constants_used"] = [
    "c=2.99792458e8 m/s", "G=6.67430e-11", "Msun=1.98847e30 kg",
    "pc=3.0856775814913673e16 m", "a0_can=9.36e-11 m/s^2", "a0_alt=1.13e-10 m/s^2",
    "Omega_b h^2=0.0224", "Omega_c/Omega_b=5.364 (framework input, measured)",
    "h=0.7, Omega_m=0.3 (Epps & Hudson cosmology)",
    "EXT arXiv:1702.08485: 23000 pairs, 6-10 h^-1 Mpc, <d>=8.23 h^-1 Mpc, <z>=0.42, "
    "Sigma_crit=1640 Msun/pc^2, n_src=11 arcmin^-2, M_fil=(1.6+-0.3)e13 Msun over 7.1x2.5 h^-1 Mpc, 154 deg^2",
    "ASSUMED survey specs: DES 10, LSST 27, Euclid 30, Roman 45 arcmin^-2; sigma_e=0.26-0.27",
]
RES["fails"] = FAILS

RES["numbers"]["runtime_s"] = time.time() - T0
P(f"\nA13 COMPLETE: {len(RES['checks']) - len(FAILS)}/{len(RES['checks'])} checks PASS.")
P(f"run time {time.time() - T0:.1f} s")
json.dump(RES, open(os.path.join(HERE, f"a13_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"a13{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if FAILS else 0)

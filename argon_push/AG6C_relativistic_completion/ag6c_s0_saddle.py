"""AG6C gate S0.4: does PAPER49's own static solution need NEGATIVE cold density near a saddle (field null point)?

Criteria: FROZEN_CRITERIA.md (committed alone first, e926935c3).
L49 at gamma = 0 is AQUAL with the simple mu: div(mu(|grad Phi|/a0) grad Phi) = 4 pi G rho_b, mu(x) = x/(1+x);
the cold density is rho_c - rhobar = div P = (lap Phi - 4 pi G rho_b)/(4 pi G) = rho_ph.
A real medium needs rho_c = rhobar + rho_ph >= 0.  Two equal masses at z = +-d/2, axisymmetric, mirror plane z = 0.
Deep-MOND limit (mu = |grad Phi|/a0; units G M a0 = 1, d = 1): rho_ph = C sqrt(G M a0)/(G d^2) with C dimensionless.
Full-mu cross-check at the cluster pair's r_M/d.  Control: single mass.  Run: python3 ag6c_s0_saddle.py
AG6C_MUTATE=1: Newtonian mu = 1 (rho_ph == 0: the negative-domain flag must vanish).
Finite volume on a stretched cell-centred grid; Picard iteration with geometric-mean damping (optimal for p = 3).
"""
import json
import math
import os
import sys
import time

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla

MUT = os.environ.get("AG6C_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag6c_s0_saddle{SUF}.out"), "w")
RES = {"lane": "AG6C", "script": "ag6c_s0_saddle", "mutate": MUT, "checks": {}, "numbers": {}}
FAILS = []
T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")
    OUT.flush()


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


# ------------------------------------------------------------------ physical constants and fiducials
G = 6.6743e-11
MSUN = 1.98847e30
PC = 3.0856775814913673e16
MPC = 1e6 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
RHOCRIT_H2 = 3 * (1e5 / MPC) ** 2 / (8 * math.pi * G)
OBH2 = {"central": 0.0224, "low": 0.0217, "high": 0.0229}
RHOBAR = {k: 5.364 * v * RHOCRIT_H2 for k, v in OBH2.items()}
SIG_UNIT = MSUN / PC ** 2
FID = {"F1_MW-M31": dict(M=8e10 * MSUN, d=0.77 * MPC), "F2_cluster_pair": dict(M=2e13 * MSUN, d=5.0 * MPC)}


# ------------------------------------------------------------------ grid
def make_faces(xmax, refs, rate=0.06):
    """faces from 0 to xmax; local spacing h(x) = min_k (h_k + rate |x - c_k|)."""
    xs = [0.0]
    while xs[-1] < xmax:
        x = xs[-1]
        h = min(hk + rate * abs(x - ck) for ck, hk in refs)
        xs.append(x + h)
    xs[-1] = xmax if xs[-1] - xmax < 0.5 * (xs[-1] - xs[-2]) else xs[-1]
    return np.array(xs)


class Grid:
    def __init__(self, Rf, zf):
        self.Rf, self.zf = Rf, zf
        self.Rc = 0.5 * (Rf[1:] + Rf[:-1])
        self.zc = 0.5 * (zf[1:] + zf[:-1])
        self.dR = np.diff(Rf)
        self.dz = np.diff(zf)
        self.NR, self.NZ = len(self.Rc), len(self.zc)
        self.N = self.NR * self.NZ
        self.RR, self.ZZ = np.meshgrid(self.Rc, self.zc, indexing="ij")
        self.V = np.outer(math.pi * (Rf[1:] ** 2 - Rf[:-1] ** 2), self.dz)
        self.idx = np.arange(self.N).reshape(self.NR, self.NZ)


def cell_grad(g, Phi, phib_R, phib_z):
    """central-difference gradient at cell centres (one-sided/BC-aware at the edges)."""
    NR, NZ = g.NR, g.NZ
    dPR = np.zeros_like(Phi)
    dPz = np.zeros_like(Phi)
    # R direction
    dPR[1:-1, :] = (Phi[2:, :] - Phi[:-2, :]) / (g.Rc[2:, None] - g.Rc[:-2, None])
    dPR[0, :] = (Phi[1, :] - Phi[0, :]) / (g.Rc[1] + g.Rc[0])   # mirror ghost (odd derivative); first run had a 2/3 error
    dPR[-1, :] = (phib_R - Phi[-2, :]) / (g.Rf[-1] - g.Rc[-2])
    # z direction
    dPz[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) / (g.zc[None, 2:] - g.zc[None, :-2])
    dPz[:, 0] = (Phi[:, 1] - Phi[:, 0]) / (g.zc[1] + g.zc[0])   # mirror ghost (odd derivative); first run had a 2/3 error
    dPz[:, -1] = (phib_z - Phi[:, -2]) / (g.zf[-1] - g.zc[-2])
    return dPR, dPz


def face_coeffs(g, Phi, phib_R, phib_z, mufun):
    """mu at R-faces (interior NR-1 x NZ, plus outer NZ) and z-faces (NR x NZ-1, plus outer NR)."""
    dPR, dPz = cell_grad(g, Phi, phib_R, phib_z)
    # interior R faces
    nR = (Phi[1:, :] - Phi[:-1, :]) / (g.Rc[1:, None] - g.Rc[:-1, None])
    tR = 0.5 * (dPz[1:, :] + dPz[:-1, :])
    muR = mufun(np.sqrt(nR ** 2 + tR ** 2))
    # outer R face (Dirichlet)
    nRo = (phib_R - Phi[-1, :]) / (g.Rf[-1] - g.Rc[-1])
    muRo = mufun(np.sqrt(nRo ** 2 + dPz[-1, :] ** 2))
    nz = (Phi[:, 1:] - Phi[:, :-1]) / (g.zc[None, 1:] - g.zc[None, :-1])
    tz = 0.5 * (dPR[:, 1:] + dPR[:, :-1])
    muz = mufun(np.sqrt(nz ** 2 + tz ** 2))
    nzo = (phib_z - Phi[:, -1]) / (g.zf[-1] - g.zc[-1])
    muzo = mufun(np.sqrt(nzo ** 2 + dPR[:, -1] ** 2))
    return muR, muRo, muz, muzo


def assemble(g, muR, muRo, muz, muzo, phib_R, phib_z):
    rows, cols, vals = [], [], []
    b = np.zeros(g.N)
    diag = np.zeros(g.N)
    I = g.idx
    # interior R faces
    AR = 2 * math.pi * g.Rf[1:-1, None] * g.dz[None, :]
    cR = muR * AR / (g.Rc[1:, None] - g.Rc[:-1, None])
    a, bb = I[:-1, :].ravel(), I[1:, :].ravel()
    c = cR.ravel()
    rows += [a, bb]
    cols += [bb, a]
    vals += [c, c]
    np.add.at(diag, a, -c)
    np.add.at(diag, bb, -c)
    # outer R boundary
    ARo = 2 * math.pi * g.Rf[-1] * g.dz
    cRo = muRo * ARo / (g.Rf[-1] - g.Rc[-1])
    ii = I[-1, :]
    np.add.at(diag, ii, -cRo)
    b[ii] -= cRo * phib_R
    # interior z faces
    Az = math.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)[:, None] * np.ones((1, g.NZ - 1))
    cz = muz * Az / (g.zc[None, 1:] - g.zc[None, :-1])
    a, bb = I[:, :-1].ravel(), I[:, 1:].ravel()
    c = cz.ravel()
    rows += [a, bb]
    cols += [bb, a]
    vals += [c, c]
    np.add.at(diag, a, -c)
    np.add.at(diag, bb, -c)
    # outer z boundary
    Azo = math.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)
    czo = muzo * Azo / (g.zf[-1] - g.zc[-1])
    ii = I[:, -1]
    np.add.at(diag, ii, -czo)
    b[ii] -= czo * phib_z
    rows.append(np.arange(g.N))
    cols.append(np.arange(g.N))
    vals.append(diag)
    A = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(g.N, g.N))
    return A, b


def plummer_mass(g, zpos, b, mtot):
    """cell masses of Plummer spheres at (R=0, z=zpos) (list), normalised to mtot on the half-domain."""
    rho = np.zeros((g.NR, g.NZ))
    for zp in zpos:
        r2 = g.RR ** 2 + (g.ZZ - zp) ** 2
        rho += (3 / (4 * math.pi * b ** 3)) * (1 + r2 / b ** 2) ** (-2.5)
    m = rho * g.V
    m *= mtot / m.sum()
    return m


def solve(g, mcell, mufun, phib_fun, it_max=400, tol=1e-10, label=""):
    Rb = np.sqrt(g.Rf[-1] ** 2 + g.zc ** 2)
    zb = np.sqrt(g.Rc ** 2 + g.zf[-1] ** 2)
    phib_R, phib_z = phib_fun(Rb), phib_fun(zb)
    rhs = 4 * math.pi * mcell.ravel()                      # 4 pi G rho V, G = 1
    # initial guess: the far-field form evaluated at each cell (smooth, roughly right)
    r = np.sqrt(g.RR ** 2 + g.ZZ ** 2) + 1e-3
    Phi = phib_fun(r)
    muR, muRo, muz, muzo = face_coeffs(g, Phi, phib_R, phib_z, mufun)
    hist = []
    for it in range(it_max):
        A, b = assemble(g, muR, muRo, muz, muzo, phib_R, phib_z)
        Phin = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        dphi = np.max(np.abs(Phin - Phi)) / (np.max(Phin) - np.min(Phin))
        Phi = Phin
        nmuR, nmuRo, nmuz, nmuzo = face_coeffs(g, Phi, phib_R, phib_z, mufun)
        muR, muRo, muz, muzo = (np.sqrt(muR * nmuR), np.sqrt(muRo * nmuRo), np.sqrt(muz * nmuz), np.sqrt(muzo * nmuzo))
        hist.append(dphi)
        if dphi < tol and it > 3:
            break
    # final consistency residual with mu evaluated on the final Phi
    muR, muRo, muz, muzo = face_coeffs(g, Phi, phib_R, phib_z, mufun)
    A, b = assemble(g, muR, muRo, muz, muzo, phib_R, phib_z)
    resid = np.max(np.abs(A @ Phi.ravel() - b - rhs)) / np.max(np.abs(rhs))
    P(f"  [{label}] N = {g.N} ({g.NR} x {g.NZ}), iterations {it + 1}, last dPhi {hist[-1]:.2e}, "
      f"residual/max(rhs) {resid:.2e}, t = {time.time() - T0:.1f} s")
    return Phi, phib_R, phib_z, resid, it + 1


def laplacian(g, Phi, phib_R, phib_z):
    """FV Laplacian (mu = 1) per unit volume."""
    one = lambda x: np.ones_like(x)
    muR, muRo, muz, muzo = face_coeffs(g, Phi, phib_R, phib_z, one)
    A, b = assemble(g, muR, muRo, muz, muzo, phib_R, phib_z)
    return ((A @ Phi.ravel() - b).reshape(g.NR, g.NZ)) / g.V


P("AG6C S0.4  PAPER49's static solution near a two-body saddle" + ("  [MUTATE: Newtonian mu = 1]" if MUT else ""))
P(f"  rhobar_c = 5.364 Omega_b rho_crit = {RHOBAR['central']:.4e} kg/m^3 (Omega_b h^2 0.0224; range "
  f"{RHOBAR['low']:.3e}-{RHOBAR['high']:.3e})")

deep_mu = (lambda x: np.ones_like(x)) if MUT else (lambda x: np.maximum(x, 1e-12))
HF = 0.0025      # fine spacing near the axis, the mirror plane and the masses (first run 0.01)
bsoft = 0.01   # first run used 0.04: 3% enclosed-mass deficit at r = 0.2 broke the frozen 1% control

# ------------------------------------------------------------------ control: single mass (deep MOND)
P("\nControl: single unit mass at the origin (deep MOND: |grad Phi| = 1/r, rho_ph = 1/(4 pi r^2) > 0)")
Rf = make_faces(60.0, [(0.0, HF)])
zf = make_faces(60.0, [(0.0, HF)])
gc = Grid(Rf, zf)
mc = plummer_mass(gc, [0.0], bsoft, 0.5)
phib1 = (lambda r: -1.0 / r) if MUT else (lambda r: np.log(r))
Phic, pbR, pbz, resc, itc = solve(gc, mc, deep_mu, phib1, label="single")
dPR, dPz = cell_grad(gc, Phic, pbR, pbz)
gmag = np.sqrt(dPR ** 2 + dPz ** 2)
rc = np.sqrt(gc.RR ** 2 + gc.ZZ ** 2)
sel = (rc > 0.2) & (rc < 5.0)
target = (1.0 / rc ** 2) if MUT else (1.0 / rc)
err1 = np.max(np.abs(gmag[sel] / target[sel] - 1))
lapc = laplacian(gc, Phic, pbR, pbz)
rhoph_c = lapc / (4 * math.pi) - mc / gc.V
vac = rc > 12 * bsoft
minc = np.min(rhoph_c[vac & (rc < 20)])
P(f"  max | |grad Phi| r^{2 if MUT else 1} - 1 | on 0.2 < r < 5: {err1:.3e};  min rho_ph (vacuum, r < 20): {minc:.3e}")
if MUT:
    check("K-single (Newtonian control)", err1 < 0.01, f"|grad Phi| r^2 within {err1:.1e}; rho_ph min {minc:.1e}")
else:
    check("K-single solver + positivity", err1 < 0.01 and minc > 0,
          f"|grad Phi| r within {err1:.1e} of 1; min rho_ph = {minc:.3e} > 0")
RES["numbers"]["control_single"] = dict(err=err1, min_rhoph=minc, iterations=itc, residual=resc)

# ------------------------------------------------------------------ two equal masses, deep MOND
P("\nTwo equal unit masses at z = +-1/2 (deep MOND, G M a0 = 1, d = 1)")
Rf = make_faces(60.0, [(0.0, HF)])
zf = make_faces(60.0, [(0.0, HF), (0.5, HF)])
g2 = Grid(Rf, zf)
m2 = plummer_mass(g2, [0.5, -0.5], bsoft, 1.0)
phib2 = (lambda r: -2.0 / r) if MUT else (lambda r: math.sqrt(2.0) * np.log(r))
Phi2, pbR, pbz, res2, it2 = solve(g2, m2, deep_mu, phib2, label="pair deep")
lap2 = laplacian(g2, Phi2, pbR, pbz)
rhoph2 = lap2 / (4 * math.pi) - m2 / g2.V
r_up = np.sqrt(g2.RR ** 2 + (g2.ZZ - 0.5) ** 2)
vac2 = (r_up > 12 * bsoft) & (np.sqrt(g2.RR ** 2 + g2.ZZ ** 2) < 20)
imin = np.unravel_index(np.argmin(np.where(vac2, rhoph2, np.inf)), rhoph2.shape)
Cmin = float(rhoph2[imin])
P(f"  min rho_ph (dimensionless C) = {Cmin:+.5f} at R = {g2.Rc[imin[0]]:.3f}, z = {g2.zc[imin[1]]:.3f}")
neg = vac2 & (rhoph2 < 0)
if neg.any():
    P(f"  negative region: R in [{g2.RR[neg].min():.3f}, {g2.RR[neg].max():.3f}], z in [{g2.ZZ[neg].min():.3f}, "
      f"{g2.ZZ[neg].max():.3f}], volume fraction of r<2 ball {np.sum(g2.V[neg & (np.sqrt(g2.RR**2+g2.ZZ**2)<2)]) / (2*math.pi/3*8):.3f}")
# mid-plane profile (first z cell, z = dz/2)
row = rhoph2[:, 0]
for Rs in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0):
    i = np.argmin(np.abs(g2.Rc - Rs))
    P(f"    mid-plane R = {g2.Rc[i]:6.3f}: C(R) = {row[i]:+.5f}")
# on-axis between the masses
col = rhoph2[0, :]
for zs in (0.0, 0.1, 0.2, 0.3, 0.4):
    j = np.argmin(np.abs(g2.zc - zs))
    P(f"    axis z = {g2.zc[j]:5.3f}: C = {col[j]:+.5f}")
RES["numbers"]["deep_pair"] = dict(C_min=Cmin, R_min=float(g2.Rc[imin[0]]), z_min=float(g2.zc[imin[1]]),
                                   iterations=it2, residual=res2)

# mid-plane columns (line of sight along x through the saddle, in the mirror plane): Sigma = 2 int rho(R, 0) dR
dRm = g2.dR
mask20 = g2.Rc < 20
S_neg = 2 * np.sum(np.minimum(row, 0) * dRm * mask20)
S_all = 2 * np.sum(row * dRm * mask20)
P(f"  mid-plane column through the saddle (dimensionless, R < 20 d): negative part {S_neg:+.5f}, net {S_all:+.5f}")

# grid-convergence check: halve the fine spacing once
P(f"\nResolution check (fine spacing {HF/2})")
Rf_h = make_faces(60.0, [(0.0, HF / 2)])
zf_h = make_faces(60.0, [(0.0, HF / 2), (0.5, HF / 2)])
g2h = Grid(Rf_h, zf_h)
m2h = plummer_mass(g2h, [0.5, -0.5], bsoft, 1.0)
Phi2h, pbRh, pbzh, res2h, it2h = solve(g2h, m2h, deep_mu, phib2, label="pair deep, h/2")
lap2h = laplacian(g2h, Phi2h, pbRh, pbzh)
rhoph2h = lap2h / (4 * math.pi) - m2h / g2h.V
vac2h = (np.sqrt(g2h.RR ** 2 + (g2h.ZZ - 0.5) ** 2) > 12 * bsoft) & (np.sqrt(g2h.RR ** 2 + g2h.ZZ ** 2) < 20)
Cmin_h = float(np.min(np.where(vac2h, rhoph2h, np.inf)))
S_neg_h = 2 * np.sum(np.minimum(rhoph2h[:, 0], 0) * g2h.dR * (g2h.Rc < 20))
P(f"  C_min {Cmin_h:+.5f} (vs {Cmin:+.5f}); negative column {S_neg_h:+.5f} (vs {S_neg:+.5f})")
RES["numbers"]["deep_pair_h2"] = dict(C_min=Cmin_h, S_neg=S_neg_h)
# Second run: C_min deepened -0.570 -> -0.671 on halving, while the column moved 4.5%. The minimum sits at the field null
# point, where the deep-MOND solution is only Hoelder-continuous (record XC5), so rho_ph diverges weakly there and C_min is
# not a converged number. The as-first-written line is kept as REPORTED; convergence is judged on the column and on rho_ph
# at fixed mid-plane radii (a disclosed change to a check this script added, not to a frozen criterion).
P(f"  [REPORTED] C_min is resolution-dependent (null-point divergence): {Cmin:+.4f} -> {Cmin_h:+.4f}; |C_min| >= {abs(Cmin):.3f}")
fixed = {}
for Rs in (0.1, 0.2, 0.3):
    i1 = np.argmin(np.abs(g2.Rc - Rs)); i2 = np.argmin(np.abs(g2h.Rc - Rs))
    fixed[Rs] = (float(np.interp(Rs, g2.Rc, row)), float(np.interp(Rs, g2h.Rc, rhoph2h[:, 0])))
    P(f"    mid-plane C(R = {Rs}) : {fixed[Rs][0]:+.5f} (h) vs {fixed[Rs][1]:+.5f} (h/2)")
RES["numbers"]["fixed_point_convergence"] = {str(k): v for k, v in fixed.items()}
# local exponent of the null-point divergence along the mid-plane (fine grid)
selR = (g2h.Rc > 0.01) & (g2h.Rc < 0.08)
beta = float(np.polyfit(np.log(g2h.Rc[selR]), np.log(-rhoph2h[selR, 0]), 1)[0]) if not MUT else float("nan")
P(f"    local exponent: -rho_ph(R, 0) ~ R^{beta:.3f} for 0.01 < R < 0.08 (integrable; Hoelder-1/2 would give -0.5)")
RES["numbers"]["null_point_exponent"] = beta
conv_ok = (abs(S_neg_h - S_neg) <= 0.1 * abs(S_neg)) and all(abs(a - b) <= 0.1 * abs(a) for a, b in fixed.values())
if not MUT:
    check("K-resolution (column + fixed radii)", conv_ok,
          f"negative column {S_neg:+.4f} -> {S_neg_h:+.4f}; fixed-radius values within 10% on halving the spacing")

# ------------------------------------------------------------------ full simple-mu cross-check (cluster pair, canonical)
xM = math.sqrt(G * FID["F2_cluster_pair"]["M"] / A0["canonical"]) / FID["F2_cluster_pair"]["d"]
P(f"\nFull simple-mu cross-check: cluster pair, canonical footing, r_M/d = {xM:.4f}")
a0d = 1.0 / xM ** 2            # units G = M = d = 1
if MUT:
    full_mu = lambda x: np.ones_like(x)
    phibf = lambda r: -2.0 / r
else:
    full_mu = lambda x: np.maximum(x / a0d, 1e-12) / (1 + x / a0d)
    phibf = lambda r: math.sqrt(2.0 * a0d) * np.log(r)
bf = 0.25 * xM
Rf_f = make_faces(60.0, [(0.0, bf / 3)])
zf_f = make_faces(60.0, [(0.0, HF), (0.5, bf / 3)])
gf = Grid(Rf_f, zf_f)
mf = plummer_mass(gf, [0.5, -0.5], bf, 1.0)
Phif, pbRf, pbzf, resf, itf = solve(gf, mf, full_mu, phibf, label="pair full mu")
lapf = laplacian(gf, Phif, pbRf, pbzf)
rhophf = lapf / (4 * math.pi) - mf / gf.V
vacf = (np.sqrt(gf.RR ** 2 + (gf.ZZ - 0.5) ** 2) > 12 * bf) & (np.sqrt(gf.RR ** 2 + gf.ZZ ** 2) < 20)
Cmin_full = float(np.min(np.where(vacf, rhophf, np.inf))) * xM     # convert to the deep-MOND normalisation
P(f"  C_min (full mu, in sqrt(G M a0)/(G d^2) units) = {Cmin_full:+.5f}  vs deep {Cmin:+.5f}")
RES["numbers"]["full_mu_F2"] = dict(C_min=Cmin_full, rM_over_d=xM, iterations=itf, residual=resf)
if not MUT:
    check("K-full-mu", abs(Cmin_full - Cmin) <= 0.15 * abs(Cmin),
          f"full simple-mu C_min within 15% of the deep-MOND value ({Cmin_full:+.4f} vs {Cmin:+.4f})")

# ------------------------------------------------------------------ fiducials, both footings
P("\nFiducials: min rho_ph vs -rhobar_c, and the mid-plane column a real medium cannot supply")
fid_out = {}
flag = False
for fname, fp in FID.items():
    for fo, a0 in A0.items():
        if MUT:
            unit = fp["M"] / fp["d"] ** 3           # Newtonian solve is in G = M = d = 1 units
        else:
            unit = math.sqrt(G * fp["M"] * a0) / (G * fp["d"] ** 2)
        rmin = Cmin * unit
        ratio = rmin / RHOBAR["central"]
        # column the medium cannot supply: 2 int min(rho_ph + rhobar, 0) dR  (dimensionless rhobar in this unit)
        rb_t = RHOBAR["central"] / unit
        S_clip = 2 * np.sum(np.minimum(row + rb_t, 0) * dRm * mask20)
        Lneg = 2 * np.sum(dRm * mask20 * (row < -rb_t)) * fp["d"]
        Sig = S_clip * unit * fp["d"] / SIG_UNIT
        Sig_aq = S_neg * unit * fp["d"] / SIG_UNIT
        fid_out[f"{fname}_{fo}"] = dict(unit_kg_m3=unit, rho_ph_min=rmin, ratio_to_rhobar=ratio,
                                        Sigma_unsuppliable_Msun_pc2=Sig, Sigma_neg_AQUAL_Msun_pc2=Sig_aq,
                                        L_neg_kpc=Lneg / (1e3 * PC))
        if rmin < -RHOBAR["high"]:
            flag = True
        P(f"  {fname:17s} {fo:9s}: min rho_ph = {rmin:+.3e} kg/m^3 = {ratio:+.1f} rhobar_c; "
          f"mid-plane negative column (AQUAL) {Sig_aq:+.4f} Msun/pc^2, unsuppliable by a rho>=0 medium {Sig:+.4f} "
          f"Msun/pc^2 over {Lneg / (1e3 * PC):.0f} kpc")
RES["numbers"]["fiducials"] = fid_out
P(f"\n  NEGATIVE DOMAIN EXISTS (min rho_ph < -rhobar_c, even at the high Omega_b h^2): {flag}")
RES["negative_domain_exists"] = bool(flag)
if MUT:
    P("\nMUTATE tooth: with mu = 1 the phantom vanishes, so the flag must be False")
    if flag:
        P("  tooth DID NOT BITE")
    else:
        P("  tooth bites (flag False)")
        FAILS.append("MUTATE: negative-domain flag vanished (designed exit 1)")
P(f"\nrun time {time.time() - T0:.1f} s")
RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"ag6c_s0_saddle_results{SUF}.json"), "w"), indent=1, default=float)
P("FAILS:", FAILS if FAILS else "none")
OUT.close()
sys.exit(1 if FAILS else 0)

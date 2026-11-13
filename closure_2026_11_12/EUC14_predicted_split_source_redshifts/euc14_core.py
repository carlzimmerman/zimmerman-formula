#!/usr/bin/env python3
"""EUC14 core: a line from an off-centre emitter, fitted in the individual dither spectra at the wavelength shift its
sky position predicts in each dither.

Geometry.  Each dither is dispersed along a direction fixed in NISP's focal plane.  Its position angle on the sky (east
of north, the direction of increasing wavelength) is

    phi = pa(pointing) + C0 + (180 if RGS180) + ST * tilt     (+ the convergence of meridians from the pointing centre)

with `pa` from ESA's dr1.raw_frame and the convention (C0, ST) fixed on field calibrators (euc14_cal.py).  An emitter at
offset D = (east, north) arcsec from the extraction centre appears at  lambda + DISP * k * (D . u),  u the unit vector of
phi, DISP = 13.4 A per 0.3 arcsec pixel, and k = 1 the prediction.

Fit.  Each dither is prepared exactly as EUC9's core prepares a spectrum (running-median continuum, error rescaling).
For a trial midpoint lambda0, width sigma and scale k, one line flux is fitted jointly over all usable dithers by weighted
least squares (a dither is usable at that trial if at least 80 % of the line's template falls on its good pixels).
"""
import math
import numpy as np
from scipy.special import erf

import euc9_core as C9                              # EUC9's frozen preparation and constants (imported, not edited)

W0, DW, NPIX, WL = C9.W0, C9.DW, C9.NPIX, C9.WL
DISP = C9.DISP                                     # 44.67 A per arcsec
POS = C9.POS
SIG_PAIR, SIG_SINGLE = C9.SIG_PAIR, C9.SIG_SINGLE
COVER_MIN = C9.COVER_MIN
FINE = DW / 4.0                                    # grid of line centres for the per-dither sums (3.35 A)
CF = np.arange(W0 - 400.0, WL[-1] + 400.0 + FINE, FINE)
LAM0 = np.arange(W0 + 4 * DW, WL[-1] - 4 * DW, DW / 2.0)          # trial midpoints (EUC9's centre grid)
KGRID = np.round(np.arange(-2.0, 2.0001, 0.05), 2)

def _tmpl(cent, sig):
    c = np.atleast_1d(cent)[:, None]
    a = (WL[None, :] + DW / 2 - c) / (sig * math.sqrt(2.0)); b = (WL[None, :] - DW / 2 - c) / (sig * math.sqrt(2.0))
    g = 0.5 * (erf(a) - erf(b)) / DW
    g[g < 1e-9 / DW] = 0.0
    return g

_TF = {s: _tmpl(CF, s) for s in set(SIG_PAIR) | set(SIG_SINGLE)}

# ------------------------------------------------------------------ geometry
def tangent(ra, de, ra0, de0):
    ra, de, ra0, de0 = map(math.radians, (ra, de, ra0, de0))
    cc = math.sin(de) * math.sin(de0) + math.cos(de) * math.cos(de0) * math.cos(ra - ra0)
    xi = math.cos(de) * math.sin(ra - ra0) / cc
    eta = (math.sin(de) * math.cos(de0) - math.cos(de) * math.sin(de0) * math.cos(ra - ra0)) / cc
    return xi, eta

def local_pa(phi_c, ra, de, ra0, de0):
    """position angle at (ra, de) of the direction that has position angle phi_c at the pointing centre (ra0, de0),
    the direction being fixed in the tangent plane of the centre"""
    eps = 1.0 / 3600.0
    x, y = tangent(ra, de, ra0, de0)
    xn, yn = tangent(ra, de + eps, ra0, de0)
    xe, ye = tangent(ra + eps / max(math.cos(math.radians(de)), 1e-6), de, ra0, de0)
    n = np.array([xn - x, yn - y]); e = np.array([xe - x, ye - y])
    n /= np.linalg.norm(n); e /= np.linalg.norm(e)
    d = np.array([math.sin(math.radians(phi_c)), math.cos(math.radians(phi_c))])          # (xi, eta) = (east, north) at centre
    return math.degrees(math.atan2(float(d @ e), float(d @ n))) % 360.0

def dispersion_pa(pa, pos, tilt, conv, ra=None, de=None, ra0=None, de0=None):
    c0, st = conv
    phi = pa + c0 + (180.0 if str(pos).strip() == POS[1] else 0.0) + st * tilt
    if ra is not None and ra0 is not None: phi = local_pa(phi, ra, de, ra0, de0)
    return phi % 360.0

def unit(phi):
    return np.array([math.sin(math.radians(phi)), math.cos(math.radians(phi))])

# ------------------------------------------------------------------ dithers
def dithers(raw, sign=1.0):
    """prepared residual of every dither (EUC9's preparation), with its grism position; None where unusable"""
    out = []
    for i in range(len(raw["DS"])):
        p = C9.prepare(dict(WAVELENGTH=raw["WAVELENGTH"], SIGNAL=raw["DS"][i], UNCERTAINTY=np.sqrt(np.clip(np.asarray(raw["DV"][i], float), 0, None)),
                            MASK=raw["DM"][i], NDITH=np.ones(NPIX, int)))
        if p is None: out.append(None); continue
        w = np.where(p["good"], 1.0 / p["e"] ** 2, 0.0)
        out.append(dict(r=sign * p["r"], w=w, good=p["good"].astype(float), pos=str(raw["dpos"][i]).strip(), k=p["k"]))
    return out

def sums(dl, sigmas):
    """per dither and width: T(c), N(c), coverage(c) on the fine centre grid CF"""
    S = {}
    with np.errstate(all="ignore"):                       # the macOS BLAS raises spurious flags on finite input; checked below
        for s in sigmas:
            G = _TF[s]
            S[s] = [None if d is None else (G @ (d["r"] * d["w"]), (G * G) @ d["w"], (G @ d["good"]) * DW) for d in dl]
            for v in S[s]:
                if v is not None and not all(np.all(np.isfinite(x)) for x in v): raise FloatingPointError("non-finite template sums")
    return S

def _at(arr, c):
    return np.interp(c, CF, arr, left=0.0, right=0.0)

def scan(dl, S, proj, sig, kgrid=KGRID, lam0=LAM0):
    """d2, flux, per-position S/N over (k, lambda0) for one width; proj[i] = D . u_i (arcsec) per dither (nan = no PA)"""
    nk, nl = len(kgrid), len(lam0)
    T = np.zeros((nk, nl)); N = np.zeros((nk, nl)); TP = {g: np.zeros((nk, nl)) for g in POS}; NP = {g: np.zeros((nk, nl)) for g in POS}
    for i, d in enumerate(dl):
        if d is None or not np.isfinite(proj[i]) or d["pos"] not in POS: continue
        Ti, Ni, Ci = S[sig][i]
        for a, k in enumerate(kgrid):
            c = lam0 + DISP * k * proj[i]
            ok = _at(Ci, c) >= COVER_MIN
            t = np.where(ok, _at(Ti, c), 0.0); n = np.where(ok, _at(Ni, c), 0.0)
            T[a] += t; N[a] += n; TP[d["pos"]][a] += t; NP[d["pos"]][a] += n
    with np.errstate(divide="ignore", invalid="ignore"):
        d2 = np.where(N > 0, T * T / N, 0.0); F = np.where(N > 0, T / N, 0.0)
        snp = {g: np.where(NP[g] > 0, TP[g] / np.sqrt(NP[g]), -np.inf) for g in POS}
    return dict(d2=d2, F=F, T=T, N=N, sn_pos=snp)

def centred(dl, S, lam0=LAM0):
    """best centred line (the same wavelength in every dither) at each lambda0 over the single-line widths: d2"""
    best = np.zeros(len(lam0)); bs = np.zeros(len(lam0))
    for s in SIG_SINGLE:
        T = np.zeros(len(lam0)); N = np.zeros(len(lam0))
        for i, d in enumerate(dl):
            if d is None or d["pos"] not in POS: continue
            Ti, Ni, Ci = S[s][i]
            ok = _at(Ci, lam0) >= COVER_MIN
            T += np.where(ok, _at(Ti, lam0), 0.0); N += np.where(ok, _at(Ni, lam0), 0.0)
        d2 = np.where((N > 0) & (T > 0), T * T / np.where(N > 0, N, 1.0), 0.0)
        up = d2 > best; best = np.where(up, d2, best); bs = np.where(up, s, bs)
    return best, bs

def fit_lines(dl, proj, k, sig, cents):
    """joint weighted least squares of several lines, each at its own midpoint with the same per-dither shifts:
    fluxes and their errors (None if singular)"""
    rows = []
    for c0 in cents:
        rows.append([None if (d is None or not np.isfinite(proj[i]) or d["pos"] not in POS) else _tmpl(c0 + DISP * k * proj[i], sig)[0] for i, d in enumerate(dl)])
    m = len(cents); A = np.zeros((m, m)); b = np.zeros(m)
    for i, d in enumerate(dl):
        if d is None or not np.isfinite(proj[i]) or d["pos"] not in POS: continue
        ts = [rows[j][i] for j in range(m)]
        cov = [float(np.sum(t * d["good"]) * DW) for t in ts]
        if cov[0] < COVER_MIN: continue
        for j in range(m):
            if cov[j] < COVER_MIN: ts[j] = np.zeros(NPIX)
        for j in range(m):
            b[j] += float(np.sum(ts[j] * d["w"] * d["r"]))
            for l in range(m): A[j, l] += float(np.sum(ts[j] * d["w"] * ts[l]))
    if np.any(np.diag(A) <= 0) or np.linalg.cond(A) > 1e8: return None
    cov = np.linalg.inv(A); a = cov @ b
    return a, np.sqrt(np.clip(np.diag(cov), 1e-300, None))

def inject(raw, proj, lam0, k, sig, flux):
    """a copy of the raw arrays with one line of total flux `flux` added to every dither at its predicted position
    (k = 0: a centred line)"""
    out = {kk: np.array(v, copy=True) for kk, v in raw.items()}
    DS = np.asarray(out["DS"], float).copy()
    for i in range(len(DS)):
        if not np.isfinite(proj[i]): continue
        DS[i] += flux * _tmpl(lam0 + DISP * k * proj[i], sig)[0]
    out["DS"] = DS
    return out

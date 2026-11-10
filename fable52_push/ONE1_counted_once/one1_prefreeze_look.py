#!/usr/bin/env python3
"""ONE1 pre-freeze quick look (post hoc, NOT graded): single counting with a truncated law halo against KO1's PUBLISHED host-free bins.

Model: the lens's cold share X M_b is the law's own phantom halo. Enclosed mass M(x)/M_b = nu(1/x^2) for x = r/r_M below
x_t (where nu = 1 + X), constant 1 + X beyond. Projected exactly; expressed as a ratio to the untruncated law so that KO1's
cell convention is kept.  Reads no shear: weights WW, model cells and KO1's published per-bin amplitudes only.
"""
import os, sys, json
import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
SH = json.load(open(os.path.join(REPO, "fable52_push", "KO1_kids_outer_points", "ko1_shape.json")))["foot"]
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]

# ---------------- projected excess surface density of the (truncated) law halo, units M_b / r_M^2
def dsig(u, xt):
    """u array; xt truncation (np.inf for none). m(x) = 0.5 + sqrt(0.25 + x^2) below xt."""
    out = np.zeros_like(u)
    XMAX = 3e5 if not np.isfinite(xt) else xt
    for i, ui in enumerate(u):
        if ui >= XMAX:
            mt = 0.5 + np.sqrt(0.25 + XMAX ** 2); out[i] = mt / (np.pi * ui ** 2); continue
        x = np.geomspace(ui, XMAX, 6000)
        dm = x / np.sqrt(0.25 + x * x)                                   # dm/dx
        m_u = 0.5 + np.sqrt(0.25 + ui * ui)
        M2 = m_u + np.trapz((1 - np.sqrt(np.clip(1 - (ui / x) ** 2, 0, 1))) * dm, x)
        T = np.arccosh(XMAX / ui); t = np.linspace(0, T, 6000); xx = ui * np.cosh(t)
        rho = (xx / np.sqrt(0.25 + xx * xx)) / (4 * np.pi * xx * xx)
        Sig = 2 * np.trapz(rho * xx, t)                                   # dz = x dt along the line of sight
        out[i] = M2 / (np.pi * ui ** 2) - Sig
    return out
UG = np.geomspace(0.3, 2000, 400)
D_INF = dsig(UG, np.inf)
sis = 1 / (4 * UG)
print(f"check: untruncated profile against the isothermal form at u = 50, 300: {np.interp(50, UG, D_INF) * 200:.4f}, {np.interp(300, UG, D_INF) * 1200:.4f} (1 = exact SIS)")
XS = [5.562, 10.82, 23.0, 33.0, 40.0, 53.64, 59.5, 80.0, 120.0, np.inf]
RAT = {}
for X in XS:
    if np.isfinite(X):
        xt = np.sqrt(X * (X + 1)); RAT[X] = dsig(UG, xt) / D_INF
    else:
        RAT[X] = np.ones_like(UG)
X0 = 53.64; far = RAT[X0][-1]; want = 4 * (1 + X0) / (np.pi * UG[-1])
print(f"check: X = {X0} ratio at u = 2000 is {far:.5f}; point-mass form 4 (1 + X) / (pi u) = {want:.5f}")

# ---------------- lenses, weights, cells for all 13 bins
ln = np.load(os.path.join(DATA, "lr_lenses.npz")); PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WW = PL["WW"]; EDGES = PL["gbar_edges"]; NB = 13
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
LATE, EARLY = typ == 0, typ == 1
XG, WGL = np.polynomial.legendre.leggauss(24); R3 = (3.0 * Mpc) ** 2
def cells(a0, X):
    m_ = np.zeros((NL, NB))
    for k in range(NB):
        t_lo = G * Mg / EDGES[k + 1]; t_hi = np.minimum(G * Mg / EDGES[k], R3); ok = t_hi > t_lo
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            gb = G * Mg[:, None] / t; f = nu(gb / a0) * gb
            u = np.sqrt(a0 / gb)
            r = np.interp(u, UG, RAT[X]) if np.isfinite(X) else 1.0
        m_[:, k] = np.where(ok, (f * r * WGL[None, :]).sum(1) / 2, 0.0)
    return m_

# ---------------- KO1's host-free flags at 1.0, 1.3, 1.6 R_h (photometric rule), rebuilt
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
r_ = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); zp = np.array(b["zphot_ANNz2"], dtype="f8"); logM = np.array(Lp["MASS_MED"], dtype="f8") + 0.15
ra = np.array(b["RAJ2000"], dtype="f8"); dec = np.array(b["DECJ2000"], dtype="f8"); del b, Lp; HB.close(); HL.close()
inb = np.where((r_ < 20) & (zp >= 0.02) & (zp <= 0.8) & np.isfinite(logM) & (logM > 7))[0]
xN = unitvec(ra[inb], dec[inb]); chiN = DC(zp[inb]); logMN = logM[inb]; treeN = cKDTree(xN)
xL = unitvec(ln["ra"], ln["dec"]); dd, selfN = treeN.query(xL, k=1)
rh = np.minimum(3.0, np.sqrt(G * Mg / 1e-15) / Mpc); th = rh * (1 + zl) / chil
chord1 = 2 * np.sin(th / 2); chordF = 2 * np.sin(1.6 * th / 2)
FS = (1.0, 1.3, 1.6); CNT = {F: np.zeros(NL, np.int32) for F in FS}
for i0 in range(0, NL, 400):
    i1 = min(i0 + 400, NL)
    lists = treeN.query_ball_point(xL[i0:i1], r=chordF[i0:i1])
    cn = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(cn.sum())
    if tot == 0: continue
    li = i0 + np.repeat(np.arange(len(cn)), cn); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot)
    keep = (j != selfN[li]) & (logMN[j] >= logMs[li] + 0.3) & (np.abs(chiN[j] - chil[li]) < 230.0); li, j = li[keep], j[keep]
    sep = np.sqrt(((xL[li] - xN[j]) ** 2).sum(1)) / chord1[li]
    for F in FS: np.add.at(CNT[F], li[sep <= F], 1)
HF = {F: CNT[F] == 0 for F in FS}
print("host-free sizes", {F: int(HF[F].sum()) for F in FS}, "(KO1: 40667, 25708, 17335)")

O = [0, 1, 2, 3]; MID = [4, 5, 6]; INN = [7, 8, 9, 10, 11, 12]
res = {}
for ft in ("canonical", "alt"):
    LAWC = cells(A0[ft], np.inf); MOD = {X: cells(A0[ft], X) for X in XS}
    print(f"\n=== {ft}: model amplitude per bin / window for the host-free sample, in units of the law (no neighbours)")
    for F in FS:
        e = SH[ft]["E7"][f"{F:.1f}"]; A = np.array(e["per_bin"]); s = np.array(e["per_bin_err"]); Ain, sin_ = e["inner"]; Rs, sRs = e["Rs"]
        w = 1 / s ** 2; m = HF[F]
        print(f" veto {F:.1f} R_h: measured outer bins {np.round(A, 2)} +- {np.round(s, 2)}; inner {Ain:.2f} +- {sin_:.2f}; R_s {Rs:.3f} +- {sRs:.3f}")
        for sub, mk in (("all", m), ("late", m & LATE), ("early", m & EARLY)):
            for X in XS:
                tw = WW[mk][:, :NB].sum(0); al = (WW[mk][:, :NB] * LAWC[mk]).sum(0); am = (WW[mk][:, :NB] * MOD[X][mk]).sum(0)
                a = am / al                                              # per bin, model / law
                a_out = float((a[O] * w).sum() / w.sum()); a_mid = float(a[MID].mean()); a_in = float(a[INN].mean())
                rs_mod = a_out / a_in
                if sub == "all":
                    chi2 = float((((A / Ain - a[O] / a_in) / (s / Ain)) ** 2).sum()); z = (Rs - rs_mod) / sRs
                    res[(ft, F, X)] = (rs_mod, z, chi2)
                    print(f"   X {X:7.2f}: bins {np.round(a[O], 3)}  middle {a_mid:.3f}  inner {a_in:.3f}  R_s model {rs_mod:.3f}  (measured - model) / sigma {z:+.2f}  shape chi2 (4 bins, diagonal) {chi2:.1f}")
                elif X in (53.64, 59.5, np.inf):
                    ee = e[sub]; print(f"      {sub:5s} X {X:6.2f}: model outer {a_out:.3f} x inner level; measured outer {ee[0]:+.2f} +- {ee[1]:.2f} (absolute)")

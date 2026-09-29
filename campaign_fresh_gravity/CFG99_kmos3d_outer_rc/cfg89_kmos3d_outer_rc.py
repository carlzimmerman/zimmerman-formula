#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG89 -- KMOS3D CUBES: HOW FAR OUT CAN H-ALPHA ROTATION BE MEASURED, AND HOW MANY z >= 1.9 DISCS REACH g_bar < a0 AT THEIR OUTERMOST
RELIABLE RADIUS?  A FEASIBILITY COUNT, NOT A TEST OF B (no law is scored; no velocity is compared with any prediction).
Criteria frozen and committed before any extraction: campaign_fresh_gravity/CFG89_kmos3d_outer_rc/FROZEN_CRITERIA.md (commit 6eb7ae539).
Data: the 739 KMOS3D cubes (Wisnioski+2019 release) outside the repo at ../_external_data/kmos3d/cubes (relative to the repo root; never
copied into the repo); catalogue data_assembly/kmos3d_phibss/kmos3d_catalog.csv.
  extraction  Halpha+[NII] Gaussian fits (grid, then least_squares) with the noise extension rescaled per summed spectrum (E2); 3x3-box
              velocity field -> kinematic PA (arctan model on a grid); pseudo-slit of PSF-FWHM apertures along the kinematic axis;
              reliable = S/N(Halpha) >= 5 (+ sanity bounds); r_out = largest radius reliable on BOTH sides (two consecutive failures
              stop a side); inclination from Q with q0 = 0.2.
  g_bar       one exponential disc, R_d = RHALF/1.678 (arcsec -> kpc, flat LCDM H0 = 70, Om = 0.3); gas = Tacconi+2018 mu_gas(z, M*, dMS)
              with the repo's constants; exact Freeman thin-disc radial acceleration; enclosed-mass form = lower-g bracket;
              footings a0 = 9.3603e-11 (canonical) / 1.1312e-10 (alt) m/s^2.
  checks      C1 injection-recovery (C1a-d), C2 integrated Halpha flux vs HAFIT_FLUX_HA, C3 centroid redshift vs Z, D1 coherent
              rotation in >= 20% of the sample, H1-can / H1-alt the feasibility gate: N(g_bar(r_out) < a0) >= 5 clean discs at
              z >= 1.9 (CFG54's gate).  A NOT FEASIBLE verdict makes the main run exit 1 -- a declared, valid result.
MUTATE=1: every real cube's spaxels are spatially scrambled before the kinematic extraction (C1, C2, C3 run unscrambled) -- D1 must FAIL.
kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the theory is closed.
Run: python3 campaign_fresh_gravity/CFG89_kmos3d_outer_rc/cfg89_kmos3d_outer_rc.py      (MUTATE=1 for the control)
"""
import os, sys, math, json, time, csv, warnings
import numpy as np
from scipy import ndimage
from scipy.special import erf, i0e, i1e, k0e, k1e
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.dirname(HERE)
REPO = os.path.dirname(CFGDIR)
CUBES = os.path.join(REPO, "..", "_external_data", "kmos3d", "cubes")
CATF = os.path.join(REPO, "data_assembly", "kmos3d_phibss", "kmos3d_catalog.csv")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "cfg89_kmos3d_outer_rc"
SUFFIX = "_MUTATE" if MUTATE else ""

# ------------------------------------------------------------------------------------------------ frozen constants (FROZEN_CRITERIA.md)
C_KMS = 299792.458
SQ2 = math.sqrt(2.0)
L_HA, L_N2A, L_N2B = 0.656461, 0.654986, 0.658527            # um, vacuum: Halpha, [NII]6550, [NII]6585
L_OTHER = (0.671829, 0.673267, 0.630205, 0.636554, 0.667999)  # [SII] x2, [OI] x2, HeI (vacuum, um)
WIN = 2500.0                                                  # fit window half-width, km/s
VGRID = np.arange(-600.0, 600.0 + 1e-9, 10.0)
SGRID = np.array([0.0, 25.0, 50.0, 75.0, 100.0, 150.0, 200.0, 300.0])
SN_REL, SN_PRE, VREL, SREL = 5.0, 3.0, 600.0, 500.0
PIX = 0.2                                                     # arcsec per spaxel
Q0 = 0.2
USABLE_FRAC, FIT_FRAC, BOX_MIN, COVER_FRAC = 0.9, 0.7, 7, 0.8
N_GALMAP = 10
R2_MIN, DV_SIG, VSIG_MIN, GATE = 0.5, 3.0, 1.0, 0.25
G_SI, MSUN, KPC = 6.6743e-11, 1.98847e30, 3.0856775814913673e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}             # = CFG7_common.A0_SI
TAC = (0.12, -3.62, 0.66, 0.53, -0.35)                        # Tacconi+2018 (A, B, F, C, D), repo constants
NPROC = 14


# ================================================================================================ cube I/O
def load_cube(fn):
    from astropy.io import fits
    with fits.open(fn, memmap=False) as h:
        F = np.array(h[1].data, dtype=np.float64)
        N = np.array(h[2].data, dtype=np.float64)
        hd = h[1].header.copy(); h0 = h[0].header; hp = h[4].header
        lam = hd["CRVAL3"] + (np.arange(hd["NAXIS3"]) + 1 - hd["CRPIX3"]) * hd["CDELT3"]
        coef = [float(h0.get(f"HIERARCH ESO K3D RES COEFF{i}", 0.0) or 0.0) for i in range(6)]
        rmin = float(h0.get("HIERARCH ESO K3D RES MIN")); rmax = float(h0.get("HIERARCH ESO K3D RES MAX"))
        beta = hp.get("HIERARCH ESO K3D PSF MOFFAT BETA")
    V = np.isfinite(F) & np.isfinite(N) & (N > 0)
    return dict(F=F, N=N, V=V, lam=lam, dlam=float(hd["CDELT3"]), coef=coef, rmin=rmin, rmax=rmax,
                beta=(float(beta) if beta is not None else float("nan")), hdr=hd)


def resolution(cube, lam_um):
    R = sum(c * lam_um ** i for i, c in enumerate(cube["coef"]))
    return float(min(max(R, cube["rmin"]), cube["rmax"]))


def cat_pixel(cube, ra, dec):
    from astropy.wcs import WCS
    ny, nx = cube["F"].shape[1:]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        w = WCS(cube["hdr"]).celestial
        x, y = w.all_world2pix([[ra, dec]], 0)[0]
    inside = (-0.5 <= x <= nx - 0.5) and (-0.5 <= y <= ny - 0.5)
    if not inside:
        x, y = (nx - 1) / 2.0, (ny - 1) / 2.0
    return float(x), float(y), bool(inside)


def scramble(cube, seed):
    """MUTATE: permute the spatial positions of all spaxels with >= 1 finite channel (flux and noise move together)."""
    F, N = cube["F"], cube["N"]
    nz, ny, nx = F.shape
    anyf = np.isfinite(F).any(axis=0).ravel()
    idx = np.flatnonzero(anyf)
    perm = np.random.default_rng(seed).permutation(idx.size)
    F2 = F.reshape(nz, -1).copy(); N2 = N.reshape(nz, -1).copy()
    F2[:, idx] = F.reshape(nz, -1)[:, idx[perm]]; N2[:, idx] = N.reshape(nz, -1)[:, idx[perm]]
    cube["F"] = F2.reshape(nz, ny, nx); cube["N"] = N2.reshape(nz, ny, nx)
    cube["V"] = np.isfinite(cube["F"]) & np.isfinite(cube["N"]) & (cube["N"] > 0)


# ================================================================================================ the line fitter (E3)
class Fitter:
    def __init__(self, lam_w, dlam, Z, sig_instr):
        self.lam = lam_w; self.ehi = lam_w + dlam / 2.0; self.elo = lam_w - dlam / 2.0
        self.lc = float(lam_w.mean()); self.dl = (lam_w - self.lc) / 0.01      # continuum slope per 0.01 um
        self.Z = float(Z); self.si = float(sig_instr); self.dlam = float(dlam)
        vv, ss = np.meshgrid(VGRID, SGRID, indexing="ij")
        self.vv, self.ss = vv.ravel(), ss.ravel()
        self.GH = self.prof(L_HA, self.vv, self.ss)
        self.GN = self.prof(L_N2B, self.vv, self.ss) + self.prof(L_N2A, self.vv, self.ss) / 3.0

    def prof(self, lrest, v, s, sel=None):
        """channel-integrated unit-area Gaussian (fraction of the line flux in each channel); rows = nodes."""
        v = np.atleast_1d(np.asarray(v, float)); s = np.atleast_1d(np.asarray(s, float))
        ehi = self.ehi if sel is None else self.ehi[sel]; elo = self.elo if sel is None else self.elo[sel]
        mu = lrest * (1 + self.Z) * (1 + v / C_KMS)
        d = SQ2 * mu * np.sqrt(s * s + self.si ** 2) / C_KMS
        return 0.5 * (erf((ehi[None, :] - mu[:, None]) / d[:, None]) - erf((elo[None, :] - mu[:, None]) / d[:, None]))

    def grid_fit(self, F, W):
        """F, W: (m, n) window spectra and weights (0 on invalid channels).  Returns arrays (m,)."""
        GH, GN, dl = self.GH, self.GN, self.dl
        m = F.shape[0]; T = GH.shape[0]
        out = {k: np.full(m, np.nan) for k in ("c0", "c1", "aH", "aN", "v", "s", "chi2", "snr")}
        GH2, GN2, GHN = GH * GH, GN * GN, GH * GN
        eye4 = np.eye(4)
        for a in range(0, m, 32):
            bs = slice(a, min(m, a + 32)); Fb = F[bs]; Wb = W[bs]; mb = Fb.shape[0]
            WF = Wb * Fb; Wd = Wb * dl
            A = np.zeros((mb, T, 4, 4))
            A[..., 0, 0] = Wb.sum(1)[:, None]
            A[..., 0, 1] = A[..., 1, 0] = Wd.sum(1)[:, None]
            A[..., 1, 1] = (Wd * dl).sum(1)[:, None]
            A[..., 0, 2] = A[..., 2, 0] = Wb @ GH.T
            A[..., 1, 2] = A[..., 2, 1] = Wd @ GH.T
            A[..., 2, 2] = Wb @ GH2.T
            A[..., 0, 3] = A[..., 3, 0] = Wb @ GN.T
            A[..., 1, 3] = A[..., 3, 1] = Wd @ GN.T
            A[..., 3, 3] = Wb @ GN2.T
            A[..., 2, 3] = A[..., 3, 2] = Wb @ GHN.T
            rhs = np.empty((mb, T, 4))
            rhs[..., 0] = WF.sum(1)[:, None]; rhs[..., 1] = (WF * dl).sum(1)[:, None]
            rhs[..., 2] = WF @ GH.T; rhs[..., 3] = WF @ GN.T
            sFF = (WF * Fb).sum(1)[:, None]
            ridge = 1e-12 * np.einsum("...ii->...i", A).max(-1)                  # numerical guard only
            A4 = A + ridge[..., None, None] * eye4
            be4 = np.linalg.solve(A4, rhs[..., None])[..., 0]
            chi4 = sFF - (be4 * rhs).sum(-1)
            A3 = A4[..., :3, :3]
            be3 = np.linalg.solve(A3, rhs[..., :3, None])[..., 0]
            chi3 = sFF - (be3 * rhs[..., :3]).sum(-1)
            use4 = be4[..., 3] >= 0
            chi = np.where(use4, chi4, chi3)
            ib = np.argmin(chi, axis=1); r = np.arange(mb)
            u4 = use4[r, ib]
            Ai4 = np.linalg.inv(A4[r, ib]); Ai3 = np.linalg.inv(A3[r, ib])
            varH = np.where(u4, Ai4[:, 2, 2], Ai3[:, 2, 2])
            b4 = be4[r, ib]; b3 = be3[r, ib]
            out["c0"][bs] = np.where(u4, b4[:, 0], b3[:, 0]); out["c1"][bs] = np.where(u4, b4[:, 1], b3[:, 1])
            out["aH"][bs] = np.where(u4, b4[:, 2], b3[:, 2]); out["aN"][bs] = np.where(u4, b4[:, 3], 0.0)
            out["v"][bs] = self.vv[ib]; out["s"][bs] = self.ss[ib]; out["chi2"][bs] = chi[r, ib]
            out["snr"][bs] = out["aH"][bs] / np.sqrt(np.maximum(varH, 1e-300))
        return out

    def refine(self, f, n, valid, x0):
        """least_squares on (c0, c1, aH, aN, v, s_int); aH, aN in cube units (flux per channel-width normalisation)."""
        sel = valid
        fs, ns = f[sel], n[sel]
        ehi, elo, dl = self.ehi[sel], self.elo[sel], self.dl[sel]
        z1, si2 = 1.0 + self.Z, self.si ** 2

        def model(p):
            c0, c1, aH, aN, v, s = p
            fac = z1 * (1 + v / C_KMS); so = math.sqrt(s * s + si2)
            out = c0 + c1 * dl
            for lr, amp in ((L_HA, aH), (L_N2B, aN), (L_N2A, aN / 3.0)):
                mu = lr * fac; d = SQ2 * mu * so / C_KMS
                out = out + amp * 0.5 * (erf((ehi - mu) / d) - erf((elo - mu) / d))
            return out

        fun = lambda p: (fs - model(p)) / ns
        lb = np.array([-np.inf, -np.inf, -np.inf, 0.0, -700.0, 0.0])
        ub = np.array([np.inf, np.inf, np.inf, np.inf, 700.0, 600.0])
        x0 = np.clip(np.asarray(x0, float), lb, ub)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                r = least_squares(fun, x0, bounds=(lb, ub), method="trf", x_scale="jac")
        except Exception:
            return None
        err = np.full(6, np.nan)
        free = r.active_mask == 0
        try:
            J = r.jac[:, free]
            cov = np.linalg.inv(J.T @ J)
            d = np.diag(cov)
            err[free] = np.sqrt(np.where(d > 0, d, np.nan))
        except np.linalg.LinAlgError:
            pass
        return dict(p=r.x, err=err, status=int(r.status), chi2=float(2 * r.cost), nfev=int(r.nfev), active=r.active_mask.tolist())


def fit_record(fitter, g, ref, nvalid_frac):
    """assemble one fit record from the grid node (g: dict of scalars) and the refinement (ref) -- reliability per E3."""
    rec = dict(fitted=True, grid_snr=float(g["snr"]), nvalid_frac=float(nvalid_frac))
    if ref is None:
        rec.update(refined=False, reliable=False, snr=float("nan"), v=float(g["v"]), ev=float("nan"), s=float(g["s"]), es=float("nan"),
                   aH=float(g["aH"]), eaH=float("nan"), aN=float(g["aN"]), status=-9)
        return rec
    p, e = ref["p"], ref["err"]
    snr = p[2] / e[2] if (np.isfinite(e[2]) and e[2] > 0) else float("nan")
    ok = (ref["status"] >= 1 and np.isfinite(e[2]) and np.isfinite(e[4]) and np.isfinite(snr) and snr >= SN_REL
          and abs(p[4]) <= VREL and p[5] <= SREL)
    rec.update(refined=True, reliable=bool(ok), snr=float(snr), v=float(p[4]), ev=float(e[4]), s=float(p[5]), es=float(e[5]),
               aH=float(p[2]), eaH=float(e[2]), aN=float(p[3]), status=ref["status"], c0=float(p[0]), c1=float(p[1]))
    return rec


def fit_one(fitter, Fw, Nw, Vw, refine=True):
    """fit one window spectrum (grid then refine); None if < 70% valid channels."""
    frac = float(Vw.mean())
    if frac < FIT_FRAC:
        return None
    W = np.where(Vw, 1.0 / Nw ** 2, 0.0)
    Fz = np.where(Vw, Fw, 0.0)
    g = fitter.grid_fit(Fz[None], W[None])
    g = {k: v[0] for k, v in g.items()}
    ref = None
    if refine:
        ref = fitter.refine(Fz, np.where(Vw, Nw, 1.0), Vw, [g["c0"], g["c1"], g["aH"], max(g["aN"], 0.0), g["v"], g["s"]])
    return fit_record(fitter, g, ref, frac)


# ================================================================================================ summed spectra and noise (E1, E2)
def summed(cube, W, Fsrc=None):
    """W (ny, nx) >= 0 weights, zero on non-usable spaxels.  Returns full-band Fs, N2s, valid (all contributing spaxels valid)."""
    iy, ix = np.nonzero(W > 0)
    w = W[iy, ix]
    F = cube["F"] if Fsrc is None else Fsrc
    Vsel = cube["V"][:, iy, ix]
    Fs = np.where(Vsel, F[:, iy, ix], 0.0) @ w
    N2s = np.where(Vsel, cube["N"][:, iy, ix] ** 2, 0.0) @ (w ** 2)
    valid = Vsel.all(axis=1) & (N2s > 0) if iy.size else np.zeros(F.shape[0], bool)
    return Fs, N2s, valid


def rescale_factor(Fs, N2s, valid, lf):
    g = valid & (N2s > 0)
    y = Fs[g]
    if y.size < 60:
        return 1.0
    med = ndimage.median_filter(y, size=41, mode="nearest")
    r = (y - med) / np.sqrt(N2s[g])
    rr = r[lf[g]]
    if rr.size < 60:
        return 1.0
    return max(1.0, 1.4826 * float(np.median(np.abs(rr - np.median(rr)))))


def linefree_mask(lam, Zs_ha, Zhost):
    m = np.ones(lam.size, bool)
    for Z in Zs_ha:
        c = L_HA * (1 + Z)
        m &= np.abs(lam / c - 1) * C_KMS > 3000.0
    for lr in L_OTHER:
        c = lr * (1 + Zhost)
        m &= np.abs(lam / c - 1) * C_KMS > 1000.0
    return m


def ap_weights(ny, nx, xc, yc, rpix, os_=5):
    """fractional overlap of each spaxel with a circle (centre xc, yc and radius rpix in spaxel units), 5x5 sub-sampling."""
    sub = (np.arange(os_) + 0.5) / os_ - 0.5
    xs = (np.arange(nx)[:, None] + sub[None, :]).ravel()
    ys = (np.arange(ny)[:, None] + sub[None, :]).ravel()
    inside = ((xs[None, :] - xc) ** 2 + (ys[:, None] - yc) ** 2) <= rpix ** 2
    return inside.reshape(ny, os_, nx, os_).mean(axis=(1, 3))


# ================================================================================================ the extraction (E1-E10)
def incl_from_q(Q):
    c2 = (Q * Q - Q0 * Q0) / (1 - Q0 * Q0)
    if Q <= Q0 or c2 <= 0:
        return 90.0
    return math.degrees(math.acos(math.sqrt(min(c2, 1.0))))


def pa_fit(dx, dy, v, ev, sini, cosi):
    """E6: arctan velocity-field model on a (theta, r_t) grid; v_sys, V_a linear.  dx, dy in arcsec."""
    w = 1.0 / np.maximum(ev, 5.0) ** 2
    th = np.deg2rad(np.arange(0.0, 180.0, 2.0)); rt = np.geomspace(0.05, 2.0, 12)
    ci = max(cosi, 0.15)
    ct, st = np.cos(th)[:, None], np.sin(th)[:, None]
    xp = dx[None, :] * ct + dy[None, :] * st
    yp = -dx[None, :] * st + dy[None, :] * ct
    R = np.sqrt(xp ** 2 + (yp / ci) ** 2)
    cphi = np.where(R > 0, xp / np.where(R > 0, R, 1.0), 0.0)
    basis = (2 / np.pi) * np.arctan(R[:, None, :] / rt[None, :, None]) * cphi[:, None, :] * sini       # (nth, nrt, n)
    S1 = w.sum(); Sv = (w * v).sum(); Svv = (w * v * v).sum()
    Sb = (w * basis).sum(-1); Sbb = (w * basis ** 2).sum(-1); Sbv = (w * basis * v).sum(-1)
    det = S1 * Sbb - Sb ** 2
    good = det > 1e-12 * np.maximum(S1 * Sbb, 1e-300)
    Va = np.where(good, (S1 * Sbv - Sb * Sv) / np.where(good, det, 1.0), 0.0)
    vs = (Sv - Va * Sb) / S1
    chi = Svv - 2 * vs * Sv - 2 * Va * Sbv + vs ** 2 * S1 + 2 * vs * Va * Sb + Va ** 2 * Sbb
    chi = np.where(good, chi, np.inf)
    i_th, i_rt = np.unravel_index(np.argmin(chi), chi.shape)
    chi_c = Svv - Sv ** 2 / S1
    r2 = 1.0 - chi[i_th, i_rt] / chi_c if chi_c > 0 else float("nan")
    pa = math.degrees(th[i_th]) + (0.0 if Va[i_th, i_rt] >= 0 else 180.0)
    return dict(pa=pa % 360.0, r2=float(r2), rt=float(rt[i_rt]), va=float(abs(Va[i_th, i_rt])), vsys=float(vs[i_th, i_rt]),
                chi_model=float(chi[i_th, i_rt]), chi_const=float(chi_c))


def walk(ok_map, cov_map, kmax):
    """E8 walk on one side: ok_map[k] reliable-and-covered for k = 1..kmax.  Returns (run set, stop involved a not-covered aperture)."""
    run, fails, fov = [], [], False
    for k in range(1, kmax + 1):
        if ok_map.get(k, False):
            run.append(k); fails = []
        else:
            fails.append(k)
            if len(fails) == 2:
                fov = any(not cov_map.get(kk, False) for kk in fails)
                return run, fov
    return run, True          # ran off the aperture list = off the cube


def analyse(cube, Z, Zhost, psf_fwhm, Q, Z_extra_ha=(), ref_F=None):
    """the frozen extraction on one cube; Z = the redshift whose Halpha is fitted (Z_inj for C1), Zhost = the real galaxy's."""
    lam = cube["lam"]; nz, ny, nx = cube["F"].shape
    out = dict(status="ok")
    lo, hi = L_HA * (1 + Z) * (1 - WIN / C_KMS), L_HA * (1 + Z) * (1 + WIN / C_KMS)
    kv = np.flatnonzero(cube["V"].any(axis=(1, 2)))
    if kv.size == 0 or lo < lam[kv[0]] or hi > lam[kv[-1]]:
        out["status"] = "window-out"
        return out, [], None
    wi = np.flatnonzero((lam >= lo) & (lam <= hi))
    U = cube["V"][wi].mean(axis=0) >= USABLE_FRAC
    out["n_usable"] = int(U.sum())
    lf = linefree_mask(lam, (Z, Zhost) + tuple(Z_extra_ha), Zhost)
    Rres = resolution(cube, L_HA * (1 + Z)); sig_instr = C_KMS / (2.3548 * Rres)
    out["R_at_Ha"] = Rres; out["sig_instr"] = sig_instr
    fitter = Fitter(lam[wi], cube["dlam"], Z, sig_instr)

    # ---------------- E4: 3x3 boxes
    Vu = cube["V"] & U[None]
    Fz = np.where(Vu, cube["F"], 0.0); N2z = np.where(Vu, cube["N"] ** 2, 0.0)
    bad = ((~cube["V"]) & U[None]).astype(np.float64)
    k3 = np.ones((1, 3, 3))
    Fb = ndimage.convolve(Fz, k3, mode="constant", cval=0.0)
    N2b = ndimage.convolve(N2z, k3, mode="constant", cval=0.0)
    badb = ndimage.convolve(bad, k3, mode="constant", cval=0.0) > 0.5
    nU = ndimage.convolve(U.astype(np.float64), np.ones((3, 3)), mode="constant", cval=0.0)
    Vb = (~badb) & (N2b > 0) & (nU[None] >= BOX_MIN - 0.5)
    pos = [(j, i) for j in range(ny) for i in range(nx) if nU[j, i] >= BOX_MIN - 0.5 and Vb[wi, j, i].mean() >= FIT_FRAC]
    boxes = {}
    if pos:
        fs = np.array([rescale_factor(Fb[:, j, i], N2b[:, j, i], Vb[:, j, i], lf) for (j, i) in pos])
        Fw = np.array([Fb[wi, j, i] for (j, i) in pos]); Vw = np.array([Vb[wi, j, i] for (j, i) in pos])
        Nw = np.sqrt(np.array([N2b[wi, j, i] for (j, i) in pos])) * fs[:, None]
        Wg = np.where(Vw, 1.0 / np.where(Vw, Nw, 1.0) ** 2, 0.0)
        g = fitter.grid_fit(np.where(Vw, Fw, 0.0), Wg)
        for q, (j, i) in enumerate(pos):
            gq = {k: v[q] for k, v in g.items()}
            ref = None
            if gq["snr"] >= SN_PRE:
                ref = fitter.refine(np.where(Vw[q], Fw[q], 0.0), np.where(Vw[q], Nw[q], 1.0), Vw[q],
                                    [gq["c0"], gq["c1"], gq["aH"], max(gq["aN"], 0.0), gq["v"], gq["s"]])
            rec = fit_record(fitter, gq, ref, Vw[q].mean()); rec["f"] = float(fs[q])
            boxes[(j, i)] = rec
    rel = np.zeros((ny, nx), bool)
    for (j, i), rec in boxes.items():
        rel[j, i] = rec["reliable"]
    out["n_box_fit"] = len(boxes); out["n_box_rel"] = int(rel.sum())
    lab, nlab = ndimage.label(rel, structure=np.ones((3, 3)))
    if nlab == 0:
        out.update(E0=False, n_galmap=0)
        return out, [], None
    fl = np.array([sum(boxes[(j, i)]["aH"] for j, i in zip(*np.nonzero(lab == L))) for L in range(1, nlab + 1)])
    Lbest = int(np.argmax(fl)) + 1
    gm = lab == Lbest
    out["n_galmap"] = int(gm.sum()); out["E0"] = bool(gm.sum() >= N_GALMAP)
    jj, ii = np.nonzero(gm)
    fw = np.array([boxes[(j, i)]["aH"] for j, i in zip(jj, ii)])
    x0 = float((ii * fw).sum() / fw.sum()); y0 = float((jj * fw).sum() / fw.sum())
    out["x0"], out["y0"] = x0, y0
    if not out["E0"]:
        return out, [], None

    # ---------------- E5, E6
    inc = incl_from_q(Q); sini, cosi = math.sin(math.radians(inc)), math.cos(math.radians(inc))
    out["incl"] = inc; out["sini"] = sini
    vv = np.array([boxes[(j, i)]["v"] for j, i in zip(jj, ii)]); ev = np.array([boxes[(j, i)]["ev"] for j, i in zip(jj, ii)])
    pf = pa_fit((ii - x0) * PIX, (jj - y0) * PIX, vv, ev, sini, cosi)
    out.update(pa_kin=pf["pa"], r2_vf=pf["r2"], rt_vf=pf["rt"], va_vf=pf["va"], vsys_vf=pf["vsys"])

    # ---------------- E7: pseudo-slit
    D = max(float(psf_fwhm), 0.4); rpix = D / 2.0 / PIX
    out["ap_diam"] = D
    area = math.pi * rpix ** 2
    ca, sa = math.cos(math.radians(pf["pa"])), math.sin(math.radians(pf["pa"]))
    kmax = int(math.ceil(math.hypot(nx, ny))) + 2
    aps = {}
    curves = []
    for k in range(-kmax, kmax + 1):
        xc, yc = x0 + k * ca, y0 + k * sa
        if (xc < -rpix - 1 or xc > nx - 1 + rpix + 1 or yc < -rpix - 1 or yc > ny - 1 + rpix + 1) and k != 0:
            aps[k] = dict(covered=False, reliable=False); continue
        Wa = ap_weights(ny, nx, xc, yc, rpix) * U
        covered = Wa.sum() >= COVER_FRAC * area
        rec = dict(covered=bool(covered), reliable=False, fitted=False)
        if covered:
            Fs, N2s, valid = summed(cube, Wa)
            f = rescale_factor(Fs, N2s, valid, lf)
            Nw = np.sqrt(np.where(valid[wi], N2s[wi], 1.0)) * f
            r_ = fit_one(fitter, Fs[wi], Nw, valid[wi])
            if r_ is not None:
                rec.update(r_); rec["f"] = f
                if ref_F is not None:                       # C1 reference: the noiseless model in the SAME aperture, same noise and f
                    Fr, _, _ = summed(cube, Wa, Fsrc=ref_F)
                    rr_ = fit_one(fitter, Fr[wi], Nw, valid[wi])
                    rec["v_ref"] = rr_["v"] if rr_ is not None else float("nan")
                    rec["aH_ref"] = rr_["aH"] if rr_ is not None else float("nan")
        aps[k] = rec
    # ---------------- E8
    okp = {k: aps[k].get("covered", False) and aps[k].get("reliable", False) for k in range(1, kmax + 1)}
    okn = {k: aps[-k].get("covered", False) and aps[-k].get("reliable", False) for k in range(1, kmax + 1)}
    covp = {k: aps[k].get("covered", False) for k in range(1, kmax + 1)}
    covn = {k: aps[-k].get("covered", False) for k in range(1, kmax + 1)}
    runp, fovp = walk(okp, covp, kmax); runn, fovn = walk(okn, covn, kmax)
    both = sorted(set(runp) & set(runn))
    kout = both[-1] if both else 0
    out["k_run_pos"] = max(runp) if runp else 0; out["k_run_neg"] = max(runn) if runn else 0
    out["r_out"] = kout * PIX
    out["r_either"] = max(out["k_run_pos"], out["k_run_neg"]) * PIX
    # the limiting side = a side whose run ends exactly at r_out (if r_out is set by a gap instead, it is S/N-limited, not FOV-limited)
    out["fov_limited"] = bool(kout > 0 and ((fovp and out["k_run_pos"] == kout) or (fovn and out["k_run_neg"] == kout)))
    out["ap_c0_reliable"] = bool(aps[0].get("reliable", False))
    # ---------------- E9, E10
    if kout > 0:
        ap, an = aps[kout], aps[-kout]
        dv = ap["v"] - an["v"]; edv = math.hypot(ap["ev"], an["ev"])
        sel_s = [aps[s * k]["s"] for s in (1, -1) for k in range(1, kout + 1)
                 if (k in (runp if s == 1 else runn)) and (kout / 2.0 <= k <= kout)]
        sig0 = float(np.median(sel_s)) if sel_s else float("nan")
        vrot = dv / (2 * sini) if sini > 0 else float("nan")
        out.update(dv=dv, edv=edv, vrot=vrot, sigv_over_v=(edv / dv if dv > 0 else float("inf")), sigma0=sig0,
                   v_over_sigma=(vrot / sig0 if sig0 > 0 else float("inf")))
    else:
        out.update(dv=float("nan"), edv=float("nan"), vrot=float("nan"), sigv_over_v=float("inf"), sigma0=float("nan"),
                   v_over_sigma=float("nan"))
    out["K1"] = bool(out["E0"] and kout > 0 and np.isfinite(out["r2_vf"]) and out["r2_vf"] >= R2_MIN and out["dv"] >= DV_SIG * out["edv"])
    out["K2"] = bool(kout > 0 and np.isfinite(out["v_over_sigma"]) and out["v_over_sigma"] >= VSIG_MIN) if kout > 0 else False
    out["gate"] = bool(kout > 0 and out["sigv_over_v"] <= GATE)
    for k in sorted(aps):
        a = aps[k]
        if not a.get("covered", False) or not a.get("fitted", False):
            if a.get("covered", False):
                curves.append(dict(k=k, s=k * PIX, covered=1, fitted=0, reliable=0))
            continue
        inrun = (k > 0 and k in runp) or (k < 0 and -k in runn) or k == 0
        curves.append(dict(k=k, s=round(k * PIX, 3), covered=1, fitted=1, reliable=int(a["reliable"]), in_run=int(inrun),
                           snr=round(a["snr"], 3) if np.isfinite(a["snr"]) else "", v=round(a["v"], 2),
                           ev=round(a["ev"], 2) if np.isfinite(a["ev"]) else "", s_int=round(a["s"], 2),
                           es_int=round(a["es"], 2) if np.isfinite(a["es"]) else "", f_noise=round(a.get("f", float("nan")), 3)))
    refinfo = None
    if ref_F is not None:
        refinfo = dict(aps={k: dict(covered=a.get("covered", False), reliable=a.get("reliable", False), v=a.get("v"), ev=a.get("ev"),
                                    aH=a.get("aH"), eaH=a.get("eaH"), v_ref=a.get("v_ref"), aH_ref=a.get("aH_ref"))
                            for k, a in aps.items() if a.get("fitted", False)}, kmax=kmax, runp=runp, runn=runn, covp=covp, covn=covn)
    return out, curves, refinfo


def integrated(cube, Z, xc, yc):
    """C2/C3: the 1.5-arcsec-radius aperture at the catalogue position (unscrambled cube)."""
    lam = cube["lam"]; nz, ny, nx = cube["F"].shape
    lo, hi = L_HA * (1 + Z) * (1 - WIN / C_KMS), L_HA * (1 + Z) * (1 + WIN / C_KMS)
    kv = np.flatnonzero(cube["V"].any(axis=(1, 2)))
    if kv.size == 0 or lo < lam[kv[0]] or hi > lam[kv[-1]]:
        return dict(int_status="window-out")
    wi = np.flatnonzero((lam >= lo) & (lam <= hi))
    U = cube["V"][wi].mean(axis=0) >= USABLE_FRAC
    lf = linefree_mask(lam, (Z,), Z)
    Rres = resolution(cube, L_HA * (1 + Z)); sig_instr = C_KMS / (2.3548 * Rres)
    fitter = Fitter(lam[wi], cube["dlam"], Z, sig_instr)
    Wa = ap_weights(ny, nx, xc, yc, 1.5 / PIX) * U
    Fs, N2s, valid = summed(cube, Wa)
    f = rescale_factor(Fs, N2s, valid, lf)
    Nw = np.sqrt(np.where(valid[wi], N2s[wi], 1.0)) * f
    r = fit_one(fitter, Fs[wi], Nw, valid[wi])
    if r is None:
        return dict(int_status="too-few-channels")
    flux = r["aH"] * cube["dlam"] * 1e3; eflux = r["eaH"] * cube["dlam"] * 1e3
    return dict(int_status="ok", int_flux=flux, int_eflux=eflux, int_snr=r["snr"], int_v=r["v"], int_ev=r["ev"],
                int_reliable=r["reliable"], int_f=f, int_cover=float(Wa.sum() / (math.pi * (1.5 / PIX) ** 2)))


# ================================================================================================ C1: synthetic discs
def make_model(cube, Zinj, xc, yc, Ftot_cube, Rd, Q, pa_deg, vmax, rt, sig0, psf_fwhm, beta, sig_instr, rotating):
    """thin exponential disc, arctan rotation, Halpha + [NII] (0.3, 0.1), circular Moffat PSF, 5x oversampled, rebinned to 0.2"."""
    lam, dlam = cube["lam"], cube["dlam"]
    nz, ny, nx = cube["F"].shape
    os_, mg = 5, 5
    nyf, nxf = (ny + 2 * mg) * os_, (nx + 2 * mg) * os_
    xf = (np.arange(nxf) + 0.5) / os_ - 0.5 - mg
    yf = (np.arange(nyf) + 0.5) / os_ - 0.5 - mg
    X, Y = np.meshgrid(xf, yf)
    dx, dy = (X - xc) * PIX, (Y - yc) * PIX
    inc = incl_from_q(Q); sini, ci = math.sin(math.radians(inc)), max(math.cos(math.radians(inc)), 0.05)
    pa = math.radians(pa_deg)
    xp = dx * math.cos(pa) + dy * math.sin(pa); yp = -dx * math.sin(pa) + dy * math.cos(pa)
    R = np.sqrt(xp ** 2 + (yp / ci) ** 2)
    cphi = np.where(R > 0, xp / np.where(R > 0, R, 1.0), 0.0)
    S = np.exp(-R / Rd); S *= Ftot_cube / S.sum()
    vlos = vmax * (2 / np.pi) * np.arctan(R / rt) * cphi * sini if rotating else np.zeros_like(R)
    lc = L_HA * (1 + Zinj)
    ch = np.flatnonzero(np.abs(lam / lc - 1) * C_KMS <= 3500.0)
    elo = lam[ch] - dlam / 2; ehi = lam[ch] + dlam / 2
    so = math.sqrt(sig0 ** 2 + sig_instr ** 2)
    fac = ((1 + Zinj) * (1 + vlos / C_KMS)).ravel()
    spec = np.zeros((fac.size, ch.size))
    for lr, amp in ((L_HA, 1.0), (L_N2B, 0.3), (L_N2A, 0.1)):
        mu = lr * fac; d = SQ2 * mu * so / C_KMS
        spec += amp * 0.5 * (erf((ehi[None, :] - mu[:, None]) / d[:, None]) - erf((elo[None, :] - mu[:, None]) / d[:, None]))
    spec = spec / dlam * S.ravel()[:, None]
    cub = spec.T.reshape(ch.size, nyf, nxf)
    alpha = psf_fwhm / (2 * math.sqrt(2 ** (1 / beta) - 1))
    kk = np.arange(-50, 51) * PIX / os_
    KX, KY = np.meshgrid(kk, kk)
    ker = (1 + (KX ** 2 + KY ** 2) / alpha ** 2) ** (-beta); ker /= ker.sum()
    from scipy.signal import fftconvolve
    conv = fftconvolve(cub, ker[None], mode="same", axes=(1, 2))
    reb = conv.reshape(ch.size, ny + 2 * mg, os_, nx + 2 * mg, os_).sum(axis=(2, 4))[:, mg:mg + ny, mg:mg + nx]
    full = np.zeros_like(cube["F"])
    full[ch] = reb
    return full, inc


# ================================================================================================ workers
def run_real(task):
    row = task["row"]
    fn = os.path.join(CUBES, row["FILE"])
    base = dict(tid=task["tid"], kind="real", ID=row["ID"])
    if not os.path.exists(fn):
        base["status"] = "no-file"
        return base
    cube = load_cube(fn)
    xc, yc, inside = cat_pixel(cube, row["RA"], row["DEC"])
    base.update(cat_x=xc, cat_y=yc, cat_inside=inside, psf_beta=cube["beta"])
    base.update(integrated(cube, row["Z"], xc, yc))                   # C2/C3 always on the unscrambled cube
    if task["mutate"]:
        scramble(cube, 8989 + int(row["_row"]))
    kin, curves, _ = analyse(cube, row["Z"], row["Z"], row["PSF_FWHM"], row["Q"])
    base.update(kin)
    base["curves"] = curves
    return base


def run_inject(task):
    h = task["row"]
    cube = load_cube(os.path.join(CUBES, h["FILE"]))
    xc, yc, inside = cat_pixel(cube, h["RA"], h["DEC"])
    Zinj = L_HA * (1 + h["Z"]) * (1 + task["voff"] / C_KMS) / L_HA - 1
    Rres = resolution(cube, L_HA * (1 + Zinj)); sig_instr = C_KMS / (2.3548 * Rres)
    Rd = h["RHALF"] / 1.678
    vmax = (2 * 10 ** h["LMSTAR"] / 47.0) ** 0.25 if task["rotating"] else 0.0
    sig0 = (45.0 if h["window"] == "HIGH" else 30.0) if task["rotating"] else 80.0
    beta = cube["beta"] if np.isfinite(cube["beta"]) else 2.5
    model, inc = make_model(cube, Zinj, xc, yc, h["HAFIT_FLUX_HA"] * 1e-3, Rd, h["Q"], task["pa_true"], vmax, 0.4 * Rd, sig0,
                            h["PSF_FWHM"], beta, sig_instr, task["rotating"])
    model = np.where(cube["V"], model, 0.0)
    cube["F"] = np.where(cube["V"], cube["F"] + model, cube["F"])
    kin, curves, ref = analyse(cube, Zinj, h["Z"], h["PSF_FWHM"], h["Q"], ref_F=model)
    res = dict(tid=task["tid"], kind="inject", host=h["ID"], window=h["window"], rotating=task["rotating"], voff=task["voff"],
               Zinj=Zinj, pa_true=task["pa_true"], vmax=vmax, rt=0.4 * Rd, Rd=Rd, sig0_true=sig0, incl=inc, psf=h["PSF_FWHM"],
               beta=beta, cat_inside=inside)
    res.update({("kin_" + k): v for k, v in kin.items()})
    if ref is not None and kin.get("E0"):
        aps = ref["aps"]; kmax = ref["kmax"]
        pulls = [(a["v"] - a["v_ref"]) / a["ev"] for a in aps.values()
                 if a["reliable"] and a["v_ref"] is not None and np.isfinite(a["v_ref"]) and a["ev"] and np.isfinite(a["ev"]) and a["ev"] > 0]
        # r_exp: the E8 walk with S/N_true = aH_ref / sigma(aH) >= 5
        def oktrue(k):
            a = aps.get(k)
            if a is None or not a["covered"]:
                return False
            if a["aH_ref"] is None or not np.isfinite(a["aH_ref"]) or a["eaH"] is None or not np.isfinite(a["eaH"]) or a["eaH"] <= 0:
                return False
            return a["aH_ref"] / a["eaH"] >= SN_REL
        okp = {k: oktrue(k) for k in range(1, kmax + 1)}; okn = {k: oktrue(-k) for k in range(1, kmax + 1)}
        rp, _ = walk(okp, ref["covp"], kmax); rn, _ = walk(okn, ref["covn"], kmax)
        both = sorted(set(rp) & set(rn))
        res["r_exp"] = (both[-1] if both else 0) * PIX
        res["pulls"] = [float(p) for p in pulls]
    else:
        res["r_exp"] = float("nan"); res["pulls"] = []
    r_out = kin.get("r_out", float("nan"))
    res["v_true_rout"] = vmax * (2 / np.pi) * math.atan(r_out / (0.4 * Rd)) if (task["rotating"] and r_out and np.isfinite(r_out)) else float("nan")
    if kin.get("pa_kin") is not None and np.isfinite(kin.get("pa_kin", np.nan)):
        d = abs((kin["pa_kin"] - task["pa_true"] + 180.0) % 360.0 - 180.0)
        res["dpa"] = d
    else:
        res["dpa"] = float("nan")
    return res


def worker(task):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return run_real(task) if task["kind"] == "real" else run_inject(task)
    except Exception as e:                                          # recorded, never silent
        import traceback
        return dict(tid=task["tid"], kind=task["kind"], ID=task["row"].get("ID"), status="error", error=repr(e),
                    tb=traceback.format_exc()[-1500:])


# ================================================================================================ g_bar (declared once)
def g_disc(M, r_kpc, Rd_kpc):
    y = r_kpc / (2 * Rd_kpc)
    v2 = (2 * G_SI * M * MSUN / (Rd_kpc * KPC)) * y * y * (i0e(y) * k0e(y) - i1e(y) * k1e(y))
    return v2 / (r_kpc * KPC)


def g_enc(M, r_kpc, Rd_kpc):
    x = r_kpc / Rd_kpc
    return G_SI * M * MSUN * (1 - (1 + x) * np.exp(-x)) / (r_kpc * KPC) ** 2


def mu_gas_tacconi(z, logM, sfr, age_gyr):
    A, B, F, Cc, D = TAC
    t = age_gyr
    lssfr_ms = (-0.16 - 0.026 * t) * (logM + 0.025) - (6.51 - 0.11 * t) + 9.0          # Gyr^-1
    lssfr = math.log10(sfr) - logM + 9.0
    ldms = lssfr - lssfr_ms
    return 10 ** (A + B * (math.log10(1 + z) - F) ** 2 + Cc * ldms + D * (logM - 10.7)), ldms


# ================================================================================================ main
def fnum(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except Exception:
        return float("nan")


def pct(a):
    a = np.asarray([x for x in a if np.isfinite(x)], float)
    if a.size == 0:
        return dict(n=0)
    p = np.percentile(a, [0, 16, 50, 84, 100])
    return dict(n=int(a.size), min=float(p[0]), p16=float(p[1]), med=float(p[2]), p84=float(p[3]), max=float(p[4]))


def fmt_pct(d, f="{:.2f}"):
    if d.get("n", 0) == 0:
        return "n=0"
    return (f"n={d['n']}: min " + f + ", p16 " + f + ", median " + f + ", p84 " + f + ", max " + f).format(
        d["min"], d["p16"], d["med"], d["p84"], d["max"])


def main():
    sys.path.insert(0, CFGDIR)
    import CFG7_common as C
    import multiprocessing as mp
    from astropy.cosmology import FlatLambdaCDM
    assert abs(C.A0_SI["canonical"] - A0["canonical"]) < 1e-20 and abs(C.A0_SI["alt"] - A0["alt"]) < 1e-20
    R = C.Report(SLUG, MUTATE)
    P, check = R.P, R.check
    P(__doc__.split("Run: python3")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: every real cube's spaxels spatially scrambled before the kinematic extraction; D1 must FAIL ***")
    P(f"\n  cube directory (relative to the repo root): ../_external_data/kmos3d/cubes ; exists: {os.path.isdir(CUBES)}; "
      f"FITS files: {len([f for f in os.listdir(CUBES) if f.endswith('.fits')]) if os.path.isdir(CUBES) else 0}")

    # ------------------------------------------------------------------ catalogue and selection (S1-S6)
    rows = []
    with open(CATF) as fh:
        for n_, r in enumerate(csv.DictReader(fh)):
            d = dict(r)
            for k in ("FLAG_PRIMARYTARG", "FLAG_ADDGALDET", "FLAG_ZQUALITY", "RA", "DEC", "Z", "PSF_FWHM", "LMSTAR", "SFR", "RHALF",
                      "RHALFERR", "Q", "QERR", "HAFIT_FLAG", "HAFIT_FLUX_HA", "HAFIT_FLUX_HA_ERR", "HAFIT_FLUX_AP_CORR", "SPEC_RES"):
                d[k] = fnum(d[k])
            d["_row"] = n_
            rows.append(d)
    P(f"\n  catalogue rows: {len(rows)}")

    def window(z):
        if z >= 1.9:
            return "HIGH"
        if 0.6 <= z <= 1.1:
            return "LOW"
        if 1.1 < z < 1.9:
            return "MID"
        return None

    sel = []
    for d in rows:
        if d["FLAG_PRIMARYTARG"] != 1 or not (d["Z"] > 0) or d["HAFIT_FLAG"] not in (0.0, 2.0):
            continue
        if not (d["LMSTAR"] > 0 and d["SFR"] > 0 and d["RHALF"] > 0 and d["RHALFERR"] > 0 and 0 < d["Q"] <= 1 and d["QERR"] > 0):
            continue
        w = window(d["Z"])
        if w is None or d["FLAG_ZQUALITY"] not in (0.0, 1.0):
            continue
        d["window"] = w; d["zq"] = int(d["FLAG_ZQUALITY"])
        d["file_exists"] = os.path.exists(os.path.join(CUBES, d["FILE"]))
        sel.append(d)
    cnt = {(w, zq): sum(1 for d in sel if d["window"] == w and d["zq"] == zq) for w in ("HIGH", "LOW", "MID") for zq in (0, 1)}
    P("  selected (S1-S5): " + "; ".join(f"{w} zq={zq}: {cnt[(w, zq)]}" for w in ("HIGH", "LOW", "MID") for zq in (0, 1)))
    P(f"  cube files missing among selected: {sum(1 for d in sel if not d['file_exists'])}")
    R.num("selected_counts", {f"{w}_zq{zq}": cnt[(w, zq)] for w in ("HIGH", "LOW", "MID") for zq in (0, 1)})
    sel_ok = [d for d in sel if d["file_exists"]]
    keep = ("ID", "FIELD", "FILE", "RA", "DEC", "Z", "PSF_FWHM", "LMSTAR", "SFR", "RHALF", "Q", "HAFIT_FLUX_HA", "HAFIT_FLUX_HA_ERR",
            "HAFIT_FLUX_AP_CORR", "FLAG_ADDGALDET", "SPEC_RES", "OBSBAND", "_row", "window", "zq", "HAFIT_FLAG")
    real_tasks = [dict(tid=f"R{d['_row']}", kind="real", mutate=MUTATE, row={k: d[k] for k in keep}) for d in sel_ok]

    # ------------------------------------------------------------------ C1 hosts (rng 8901)
    rng = np.random.default_rng(8901)
    elig = {w: [d for d in sel_ok if d["window"] == w and d["zq"] == 0 and d["FLAG_ADDGALDET"] == 0] for w in ("HIGH", "LOW")}
    perm = {w: [elig[w][i] for i in rng.permutation(len(elig[w]))] for w in ("HIGH", "LOW")}
    pa_draw = rng.uniform(0.0, 360.0, 60)

    def valid_range(fn):
        c = load_cube(fn)
        kv = np.flatnonzero(c["V"].any(axis=(1, 2)))
        return c["lam"][kv[0]], c["lam"][kv[-1]]

    hosts = {"HIGH": [], "LOW": []}
    for w in ("HIGH", "LOW"):
        for d in perm[w]:
            if len(hosts[w]) >= 30:
                break
            lmin, lmax = valid_range(os.path.join(CUBES, d["FILE"]))
            own = (L_HA * (1 + d["Z"]) * (1 - WIN / C_KMS) >= lmin) and (L_HA * (1 + d["Z"]) * (1 + WIN / C_KMS) <= lmax)
            if not own:
                continue
            vo = None
            for cand in (-6000.0, 4000.0):
                lc = L_HA * (1 + d["Z"]) * (1 + cand / C_KMS)
                if lc * (1 - WIN / C_KMS) >= lmin and lc * (1 + WIN / C_KMS) <= lmax:
                    vo = cand; break
            if vo is None:
                continue
            hosts[w].append((d, vo))
    inj_tasks = []
    q = 0
    for w in ("HIGH", "LOW"):
        for n_, (d, vo) in enumerate(hosts[w]):
            rot = n_ < 20
            inj_tasks.append(dict(tid=f"I{w[0]}{n_:02d}", kind="inject", rotating=rot, voff=vo, pa_true=float(pa_draw[q]),
                                  row={k: d[k] for k in keep}))
            q += 1
    P(f"  C1 hosts: HIGH {len(hosts['HIGH'])}, LOW {len(hosts['LOW'])} (first 20 rotating, next 10 non-rotating per window); "
      f"offsets used: {sorted(set(t['voff'] for t in inj_tasks))}")

    # ------------------------------------------------------------------ run
    ctx = mp.get_context("spawn")
    t0 = time.time()
    results = []
    subsample = False
    with ctx.Pool(NPROC) as pool:
        it = pool.imap_unordered(worker, real_tasks, chunksize=1)
        for j, r in enumerate(it):
            results.append(r)
            if j + 1 == 28:
                proj = (time.time() - t0) / 28.0 * len(real_tasks)
                P(f"  timing: first 28 objects in {time.time() - t0:.0f} s; projected full run {proj / 60:.1f} min (fallback if > 180 min)")
                R.num("projected_minutes", proj / 60.0)
                if proj > 3 * 3600:
                    subsample = True
                    pool.terminate()
                    break
    if subsample:
        P("  *** RUNTIME FALLBACK (declared): random subsample of 120 objects per window, default_rng(8902) ***")
        rs = np.random.default_rng(8902)
        sub = []
        for w in ("HIGH", "LOW", "MID"):
            cand = [t for t in real_tasks if t["row"]["window"] == w]
            idx = rs.choice(len(cand), size=min(120, len(cand)), replace=False)
            sub += [cand[i] for i in sorted(idx)]
        real_tasks = sub
        results = []
        with ctx.Pool(NPROC) as pool:
            results = list(pool.imap_unordered(worker, real_tasks, chunksize=1))
    t_real = time.time() - t0
    with ctx.Pool(NPROC) as pool:
        inj = sorted(pool.imap_unordered(worker, inj_tasks, chunksize=1), key=lambda x: x["tid"])     # deterministic print order
    t_all = time.time() - t0
    P(f"  run times: real sample {t_real / 60:.1f} min; with C1 {t_all / 60:.1f} min; subsample fallback used: {subsample}")
    R.num("subsample_fallback", subsample)

    byid = {r["tid"]: r for r in results}
    errs = [r for r in results + inj if r.get("status") == "error"]
    P(f"  worker errors: {len(errs)}")
    for e in errs[:10]:
        P(f"    {e['tid']} {e.get('ID')}: {e['error']}\n{e.get('tb', '')}")
    R.num("worker_errors", [dict(tid=e["tid"], ID=e.get("ID"), error=e["error"]) for e in errs])

    # ------------------------------------------------------------------ per-object assembly + g_bar
    cosmo = FlatLambdaCDM(H0=70.0, Om0=0.3)
    objs = []
    for t in real_tasks:
        d = t["row"]; r = byid.get(t["tid"], dict(status="missing"))
        o = dict(ID=d["ID"], FIELD=d["FIELD"], FILE=d["FILE"], window=d["window"], zq=d["zq"], Z=d["Z"], LMSTAR=d["LMSTAR"], SFR=d["SFR"],
                 RHALF=d["RHALF"], Q=d["Q"], PSF_FWHM=d["PSF_FWHM"], ADDGAL=int(d["FLAG_ADDGALDET"]), HAFIT_FLUX_HA=d["HAFIT_FLUX_HA"],
                 HAFIT_FLUX_HA_ERR=d["HAFIT_FLUX_HA_ERR"], HAFIT_FLUX_AP_CORR=d["HAFIT_FLUX_AP_CORR"], SPEC_RES=d["SPEC_RES"],
                 HAFIT_FLAG=d["HAFIT_FLAG"])
        for k, v in r.items():
            if k not in ("curves", "tid", "kind", "ID"):
                o[k] = v
        o["status"] = r.get("status", "missing")
        o["curves"] = r.get("curves", [])
        kpa = cosmo.kpc_proper_per_arcmin(d["Z"]).value / 60.0
        o["kpc_per_arcsec"] = kpa
        o["Re_kpc"] = d["RHALF"] * kpa; o["Rd_kpc"] = o["Re_kpc"] / 1.678
        age = float(cosmo.age(d["Z"]).value)
        mu, ldms = mu_gas_tacconi(d["Z"], d["LMSTAR"], d["SFR"], age)
        o["mu_gas"] = mu; o["log_dMS"] = ldms; o["age_gyr"] = age
        Ms = 10 ** d["LMSTAR"]
        o["Mbar"] = Ms * (1 + mu)
        ro = o.get("r_out", float("nan"))
        o["r_out_kpc"] = ro * kpa if (ro is not None and np.isfinite(ro)) else float("nan")
        o["r_out_over_Re"] = ro / d["RHALF"] if (ro is not None and np.isfinite(ro)) else float("nan")
        o["r_out_over_psf"] = ro / d["PSF_FWHM"] if (ro is not None and np.isfinite(ro)) else float("nan")
        re_ = o.get("r_either", float("nan"))
        for tag, M in (("", o["Mbar"]), ("_gasx0.5", Ms * (1 + 0.5 * mu)), ("_gasx2", Ms * (1 + 2 * mu))):
            for fk, a0 in A0.items():
                if ro is not None and np.isfinite(ro) and ro > 0:
                    o[f"gdisc_a0{tag}_{fk}"] = g_disc(M, ro * kpa, o["Rd_kpc"]) / a0
                    o[f"genc_a0{tag}_{fk}"] = g_enc(M, ro * kpa, o["Rd_kpc"]) / a0
                else:
                    o[f"gdisc_a0{tag}_{fk}"] = float("nan"); o[f"genc_a0{tag}_{fk}"] = float("nan")
        for fk, a0 in A0.items():
            o[f"gdisc_a0_either_{fk}"] = (g_disc(o["Mbar"], re_ * kpa, o["Rd_kpc"]) / a0
                                          if (re_ is not None and np.isfinite(re_) and re_ > 0) else float("nan"))
        ok = o["status"] == "ok"
        o["E0"] = bool(ok and o.get("E0", False))
        o["rpos"] = bool(o["E0"] and (o.get("r_out") or 0) > 0)
        o["K1"] = bool(o["rpos"] and o.get("K1", False))
        o["K2"] = bool(o["K1"] and o.get("K2", False))
        o["notK3"] = bool(o["K2"] and o["ADDGAL"] == 0)
        o["clean"] = bool(o["notK3"] and o.get("gate", False))
        o["clean_noK3"] = bool(o["K2"] and o.get("gate", False))         # for R13
        objs.append(o)

    def S(win=None, zq=(0,), f=None):
        return [o for o in objs if (win is None or o["window"] in ((win,) if isinstance(win, str) else win)) and o["zq"] in zq
                and (f is None or f(o))]

    # ------------------------------------------------------------------ R10 stage table
    R.banner("R10 (reported) STAGE TABLE: selected -> window-in -> E0 -> r_out>0 -> K1 -> K2 -> not K3 -> gate (= clean discs)")
    stages = {}
    for w in ("HIGH", "LOW", "MID"):
        for zq in ((0,), (1,)):
            L = S(w, zq)
            st = [len(L), sum(o["status"] == "ok" for o in L), sum(o["E0"] for o in L), sum(o["rpos"] for o in L), sum(o["K1"] for o in L),
                  sum(o["K2"] for o in L), sum(o["notK3"] for o in L), sum(o["clean"] for o in L)]
            stages[f"{w}_zq{zq[0]}"] = st
            P(f"  {w:5s} zq={zq[0]}: " + " -> ".join(str(x) for x in st)
              + f"   (window-out {sum(o['status'] == 'window-out' for o in L)}, errors {sum(o['status'] == 'error' for o in L)})")
    R.num("stages", stages)

    # ------------------------------------------------------------------ C1
    R.banner("C1 INJECTION-RECOVERY (synthetic discs in the hosts' real cubes at a velocity offset; unaffected by MUTATE)")
    rot = [x for x in inj if x.get("rotating") and x.get("status") != "error"]
    nul = [x for x in inj if (not x.get("rotating")) and x.get("status") != "error"]
    P(f"  injections: rotating {len(rot)}, non-rotating {len(nul)}; errors {sum(1 for x in inj if x.get('status') == 'error')}")
    for x in sorted(inj, key=lambda x: x["tid"]):
        if x.get("status") == "error":
            P(f"    {x['tid']} ERROR {x['error']}"); continue
        P(f"    {x['tid']} host {x['host']:11s} {'ROT ' if x['rotating'] else 'NULL'} voff {x['voff']:+6.0f} i={x['incl']:5.1f} "
          f"psf {x['psf']:.2f} E0 {int(bool(x.get('kin_E0')))} r_out {x.get('kin_r_out', float('nan')):.1f} r_exp {x.get('r_exp', float('nan')):.1f} "
          f"PA err {x.get('dpa', float('nan')):5.1f} R2 {x.get('kin_r2_vf', float('nan')):.2f} "
          f"Vrot {x.get('kin_vrot', float('nan')):6.1f} Vtrue {x.get('v_true_rout', float('nan')):6.1f} K1 {int(bool(x.get('kin_K1')))}")
    pulls = np.array([p for x in rot for p in x.get("pulls", [])])
    pstd = 1.4826 * float(np.median(np.abs(pulls - np.median(pulls)))) if pulls.size else float("nan")
    check("C1a CONTROL (honest errors): robust std of (v - v_ref)/sigma_v over reliable pseudo-slit apertures of the rotating injections in "
          "[0.7, 1.5], with >= 30 apertures", f"N = {pulls.size}, robust std = {pstd:.3f}, median pull = "
          f"{float(np.median(pulls)) if pulls.size else float('nan'):+.3f}", pulls.size >= 30 and 0.7 <= pstd <= 1.5)
    e0r = [x for x in rot if x.get("kin_E0")]
    dr = np.array([x["kin_r_out"] - x["r_exp"] for x in e0r if np.isfinite(x.get("r_exp", np.nan))])
    c1b = dr.size > 0 and -0.2 - 1e-9 <= float(np.median(dr)) <= 0.2 + 1e-9 and float(np.mean(np.abs(dr) <= 0.4 + 1e-9)) >= 0.8
    check("C1b CONTROL (r_out not noise-inflated): over E0-extractable rotating injections, median(r_out - r_exp) in [-0.2, +0.2] arcsec "
          "and |r_out - r_exp| <= 0.4 arcsec in >= 80%",
          f"N = {dr.size}, median = {float(np.median(dr)) if dr.size else float('nan'):+.2f}\", fraction within 0.4\" = "
          f"{float(np.mean(np.abs(dr) <= 0.4 + 1e-9)) if dr.size else float('nan'):.2f}; r_out - r_exp values: "
          + ", ".join(f"{v:+.1f}" for v in dr), c1b)
    res_sel = [x for x in rot if x.get("kin_E0") and x.get("kin_r_out", 0) >= x["psf"] - 1e-9 and x["incl"] >= 30.0]
    fr = np.array([x["kin_vrot"] / x["v_true_rout"] - 1 for x in res_sel if np.isfinite(x.get("kin_vrot", np.nan)) and x["v_true_rout"] > 0])
    c1c = len(res_sel) >= 8 and fr.size == len(res_sel) and float(np.mean(np.abs(fr) <= 0.25)) >= 0.7
    check("C1c CONTROL (V at r_out): rotating injections with r_out >= PSF_FWHM and i >= 30 deg: |V_rot/V_true(r_out) - 1| <= 0.25 in "
          ">= 70% (>= 8 injections)",
          f"N = {len(res_sel)}, fraction within 25% = {float(np.mean(np.abs(fr) <= 0.25)) if fr.size else float('nan'):.2f}; "
          f"median V_rot/V_true - 1 = {float(np.median(fr)) if fr.size else float('nan'):+.3f}; values " + ", ".join(f"{v:+.2f}" for v in fr), c1c)
    k1r = [bool(x.get("kin_K1")) for x in res_sel]
    k1n = [bool(x.get("kin_K1")) for x in nul]
    c1d = len(res_sel) >= 8 and float(np.mean(k1r)) >= 0.8 and sum(k1n) <= 2 and len(nul) == 20
    check("C1d CONTROL (rotation detection): (a) >= 80% of rotating injections with r_out >= PSF_FWHM and i >= 30 deg pass K1 (>= 8); "
          "(b) <= 2 of the 20 non-rotating injections pass K1",
          f"(a) {sum(k1r)}/{len(res_sel)} = {float(np.mean(k1r)) if k1r else float('nan'):.2f}; (b) {sum(k1n)}/{len(nul)}", c1d)
    # R12
    small = [x for x in rot if x.get("kin_E0") and 0 < x.get("kin_r_out", 0) < x["psf"] - 1e-9 and x["incl"] >= 30.0]
    frs = np.array([x["kin_vrot"] / x["v_true_rout"] - 1 for x in small if np.isfinite(x.get("kin_vrot", np.nan)) and x["v_true_rout"] > 0])
    dpa = np.array([x["dpa"] for x in res_sel if np.isfinite(x.get("dpa", np.nan))])
    check("R12 (reported) C1 details: PA recovery (r_out >= PSF, i >= 30); C1c and C1d(a) in the 0 < r_out < PSF regime; E0 rates",
          f"median |dPA| = {float(np.median(dpa)) if dpa.size else float('nan'):.1f} deg (N = {dpa.size}); r_out < PSF: N = {len(small)}, "
          f"within 25% = {float(np.mean(np.abs(frs) <= 0.25)) if frs.size else float('nan'):.2f}, K1 = "
          f"{sum(bool(x.get('kin_K1')) for x in small)}/{len(small)}; E0: rotating {sum(bool(x.get('kin_E0')) for x in rot)}/{len(rot)}, "
          f"non-rotating {sum(bool(x.get('kin_E0')) for x in nul)}/{len(nul)}", True, load_bearing=False)
    R.num("C1", dict(pull_std=pstd, n_pulls=int(pulls.size), dr=dr.tolist(), fr=fr.tolist(), k1_rot=k1r, k1_null=k1n,
                     dpa_median=float(np.median(dpa)) if dpa.size else None))

    # ------------------------------------------------------------------ C2, C3
    R.banner("C2 / C3 INTEGRATED H-ALPHA (1.5\" radius aperture at the catalogue position, unscrambled cubes)")
    # every selected HIGH/LOW object after S7 with catalogue S/N >= 5; a failed or non-positive integrated fit enters as -inf (conservative)
    c2all = [o for o in S(("HIGH", "LOW"), (0,)) if o.get("int_status") not in (None, "window-out") and o["HAFIT_FLUX_HA_ERR"] > 0
             and o["HAFIT_FLUX_HA"] / o["HAFIT_FLUX_HA_ERR"] >= 5]
    good_c2 = lambda o: o.get("int_status") == "ok" and np.isfinite(o.get("int_flux", np.nan)) and o["int_flux"] > 0
    c2set = [o for o in c2all if good_c2(o)]
    lr = np.array([math.log10(o["int_flux"] / o["HAFIT_FLUX_HA"]) if good_c2(o) else -np.inf for o in c2all])
    lr2 = np.array([math.log10(o["int_flux"] / (o["HAFIT_FLUX_HA"] / o["HAFIT_FLUX_AP_CORR"])) if good_c2(o) else -np.inf for o in c2all
                    if o["HAFIT_FLUX_AP_CORR"] > 0])
    rob = lambda a: 1.4826 * float(np.median(np.abs(a - np.median(a)))) if a.size else float("nan")
    check("C2 CONTROL: integrated Halpha flux vs HAFIT_FLUX_HA (catalogue S/N >= 5): |median log ratio| <= 0.10 dex and robust scatter "
          "<= 0.15 dex", f"N = {lr.size} (of which failed or non-positive fits, entered as -inf: {lr.size - len(c2set)}); median "
          f"{float(np.median(lr)) if lr.size else float('nan'):+.3f} dex, robust scatter {rob(lr):.3f} dex; p16-p84 of the log ratio "
          f"{float(np.percentile(lr, 16)) if lr.size else float('nan'):+.3f} to {float(np.percentile(lr, 84)) if lr.size else float('nan'):+.3f}",
          lr.size > 0 and abs(float(np.median(lr))) <= 0.10 and rob(lr) <= 0.15)
    check("R16 (reported) C2 against HAFIT_FLUX_HA / HAFIT_FLUX_AP_CORR", f"N = {lr2.size}; median "
          f"{float(np.median(lr2)) if lr2.size else float('nan'):+.3f} dex, robust scatter {rob(lr2):.3f} dex", True, load_bearing=False)
    dvs = np.array([o["int_v"] for o in c2set if np.isfinite(o.get("int_v", np.nan))])
    check("C3 CONTROL: Halpha centroid redshift vs Z: |median dv| <= 30 km/s and robust scatter <= 60 km/s",
          f"N = {dvs.size}; median {float(np.median(dvs)) if dvs.size else float('nan'):+.1f} km/s, robust scatter {rob(dvs):.1f} km/s",
          dvs.size > 0 and abs(float(np.median(dvs))) <= 30.0 and rob(dvs) <= 60.0)
    R.num("C2", dict(n=int(lr.size), median=float(np.median(lr)) if lr.size else None, scatter=rob(lr),
                     median_apcorr=float(np.median(lr2)) if lr2.size else None, scatter_apcorr=rob(lr2)))
    R.num("C3", dict(n=int(dvs.size), median=float(np.median(dvs)) if dvs.size else None, scatter=rob(dvs)))

    # ------------------------------------------------------------------ D1
    R.banner("D1 COHERENT ROTATION IN THE REAL SAMPLE (the MUTATE target)")
    dset = [o for o in S(("HIGH", "LOW"), (0,)) if o["status"] != "window-out"]
    nk1 = sum(o["K1"] for o in dset)
    fk1 = nk1 / len(dset) if dset else float("nan")
    check("D1 rotation detected: >= 20% of all selected HIGH + LOW objects (FLAG_ZQUALITY = 0, after S7) pass K1"
          + ("  [MUTATE: scrambled spaxels]" if MUTATE else ""), f"{nk1}/{len(dset)} = {fk1:.3f}", len(dset) > 0 and fk1 >= 0.20)
    R.num("D1", dict(n_k1=nk1, n=len(dset), frac=fk1))

    # ------------------------------------------------------------------ HEADLINE
    R.banner("HEADLINE: HIGH (z >= 1.9) clean discs with g_bar(r_out) < a0 and < 0.3 a0 (Freeman disc, Tacconi gas), both footings")
    hi = S("HIGH", (0,), lambda o: o["clean"])
    P(f"  clean discs at z >= 1.9: {len(hi)} (of {len(S('HIGH', (0,)))} selected)")
    head = {}
    for fk in A0:
        n1 = sum(o[f"gdisc_a0_{fk}"] < 1 for o in hi); n3 = sum(o[f"gdisc_a0_{fk}"] < 0.3 for o in hi)
        head[fk] = dict(n_lt_a0=n1, n_lt_0p3=n3)
    for fk in A0:
        check(f"H1-{'can' if fk == 'canonical' else 'alt'} HEADLINE (feasibility gate): N(g_bar(r_out) < a0) >= 5 clean discs at z >= 1.9, "
              f"{fk} footing (a0 = {A0[fk]:.4e})", f"N(< a0) = {head[fk]['n_lt_a0']}, N(< 0.3 a0) = {head[fk]['n_lt_0p3']} -> "
              + ("FEASIBLE" if head[fk]["n_lt_a0"] >= 5 else "NOT FEASIBLE"), head[fk]["n_lt_a0"] >= 5)
    check("R1 (reported) N(< 0.3 a0) at z >= 1.9, both footings", "; ".join(f"{fk}: {head[fk]['n_lt_0p3']}" for fk in A0), True,
          load_bearing=False)
    R.num("headline", head)
    lo_ = S("LOW", (0,), lambda o: o["clean"])
    headlo = {fk: dict(n_lt_a0=sum(o[f"gdisc_a0_{fk}"] < 1 for o in lo_), n_lt_0p3=sum(o[f"gdisc_a0_{fk}"] < 0.3 for o in lo_)) for fk in A0}
    P(f"  comparison, LOW (0.6 <= z <= 1.1) clean discs: {len(lo_)}; " + "; ".join(
        f"{fk}: N(<a0) = {headlo[fk]['n_lt_a0']}, N(<0.3a0) = {headlo[fk]['n_lt_0p3']}" for fk in A0))
    R.num("headline_low", headlo)

    # ------------------------------------------------------------------ reported rows
    R.banner("REPORTED ROWS (not load-bearing)")
    dist = {}
    for w in ("HIGH", "LOW"):
        for tag, f in (("measured (E0, r_out > 0)", lambda o: o["rpos"]), ("clean discs", lambda o: o["clean"])):
            L = S(w, (0,), f)
            dd = dict(r_out_arcsec=pct([o["r_out"] for o in L]), r_out_kpc=pct([o["r_out_kpc"] for o in L]),
                      r_out_over_Re=pct([o["r_out_over_Re"] for o in L]), r_out_over_psf=pct([o["r_out_over_psf"] for o in L]),
                      gbar_can=pct([o["gdisc_a0_canonical"] for o in L]), gbar_alt=pct([o["gdisc_a0_alt"] for o in L]),
                      mu_gas=pct([o["mu_gas"] for o in L]))
            dist[f"{w}|{tag}"] = dd
            P(f"  [{w} | {tag}]")
            P(f"     r_out [arcsec]  {fmt_pct(dd['r_out_arcsec'])}")
            P(f"     r_out [kpc]     {fmt_pct(dd['r_out_kpc'])}")
            P(f"     r_out / R_e     {fmt_pct(dd['r_out_over_Re'])}")
            P(f"     r_out / PSF     {fmt_pct(dd['r_out_over_psf'])}")
            P(f"     g_bar/a0 (can)  {fmt_pct(dd['gbar_can'])}")
            P(f"     g_bar/a0 (alt)  {fmt_pct(dd['gbar_alt'])}")
            P(f"     mu_gas          {fmt_pct(dd['mu_gas'])}")
    check("R2 (reported) distributions of r_out/R_e and g_bar/a0 at r_out (HIGH and LOW; measured and clean) -- printed above", "see above",
          True, load_bearing=False)
    R.num("distributions", dist)

    def counts(L, key, thr):
        return sum(1 for o in L if np.isfinite(o.get(key, np.nan)) and o[key] < thr)
    rows3 = {}
    for tag in ("_gasx0.5", "", "_gasx2"):
        for fk in A0:
            rows3[f"{tag or 'base'}|{fk}"] = (counts(hi, f"gdisc_a0{tag}_{fk}", 1.0), counts(hi, f"gdisc_a0{tag}_{fk}", 0.3))
    check("R3 (reported) gas bracket (mu_gas x0.5 / x1 / x2), HIGH clean discs: N(< a0), N(< 0.3 a0)",
          "; ".join(f"{k}: {v[0]}, {v[1]}" for k, v in rows3.items()), True, load_bearing=False)
    rows4 = {fk: (counts(hi, f"genc_a0_{fk}", 1.0), counts(hi, f"genc_a0_{fk}", 0.3)) for fk in A0}
    check("R4 (reported) enclosed-mass (lower-g) bracket, HIGH clean discs: N(< a0), N(< 0.3 a0)",
          "; ".join(f"{k}: {v[0]}, {v[1]}" for k, v in rows4.items()), True, load_bearing=False)
    hi_res = [o for o in hi if o["r_out"] >= o["PSF_FWHM"] - 1e-9]
    rows5 = {fk: (counts(hi_res, f"gdisc_a0_{fk}", 1.0), counts(hi_res, f"gdisc_a0_{fk}", 0.3)) for fk in A0}
    check("R5 (reported) beam smearing: HIGH clean discs with r_out >= PSF_FWHM, and their N(< a0), N(< 0.3 a0)",
          f"{len(hi_res)} of {len(hi)} clean discs have r_out >= PSF_FWHM; " + "; ".join(f"{k}: {v[0]}, {v[1]}" for k, v in rows5.items())
          + f"; r_out/PSF (clean HIGH): {fmt_pct(pct([o['r_out_over_psf'] for o in hi]))}", True, load_bearing=False)
    rows6 = {fk: (counts(hi, f"gdisc_a0_either_{fk}", 1.0), counts(hi, f"gdisc_a0_either_{fk}", 0.3)) for fk in A0}
    check("R6 (reported) either-side r_out (clean HIGH discs, g_bar at the larger one-sided reach)",
          "; ".join(f"{k}: {v[0]}, {v[1]}" for k, v in rows6.items()), True, load_bearing=False)
    hi01 = S("HIGH", (0, 1), lambda o: o["clean"])
    rows7 = {fk: (counts(hi01, f"gdisc_a0_{fk}", 1.0), counts(hi01, f"gdisc_a0_{fk}", 0.3)) for fk in A0}
    check("R7 (reported) FLAG_ZQUALITY = 1 objects added (HIGH): clean discs, N(< a0), N(< 0.3 a0)",
          f"clean {len(hi01)}; " + "; ".join(f"{k}: {v[0]}, {v[1]}" for k, v in rows7.items()), True, load_bearing=False)
    mid = S("MID", (0,), lambda o: o["clean"])
    rows8 = {fk: (counts(mid, f"gdisc_a0_{fk}", 1.0), counts(mid, f"gdisc_a0_{fk}", 0.3)) for fk in A0}
    check("R8 (reported) MID window (1.1 < z < 1.9): clean discs, N(< a0), N(< 0.3 a0); r_out/R_e and g_bar/a0 (can)",
          f"clean {len(mid)}; " + "; ".join(f"{k}: {v[0]}, {v[1]}" for k, v in rows8.items())
          + f"; r_out/R_e {fmt_pct(pct([o['r_out_over_Re'] for o in mid]))}; g/a0 {fmt_pct(pct([o['gdisc_a0_canonical'] for o in mid]))}",
          True, load_bearing=False)
    rows9 = {fk: (sum(1 for o in hi if o[f"gdisc_a0_{fk}"] * 10 ** 0.2 < 1.0), sum(1 for o in hi if o[f"gdisc_a0_{fk}"] * 10 ** 0.2 < 0.3))
             for fk in A0}
    check("R9 (reported) counts robust to the 0.2-dex mass floor (g_bar x 10^0.2), HIGH clean discs",
          "; ".join(f"{k}: {v[0]}, {v[1]}" for k, v in rows9.items()), True, load_bearing=False)
    fov = {w: (sum(o.get("fov_limited", False) for o in S(w, (0,), lambda o: o["clean"])), len(S(w, (0,), lambda o: o["clean"])))
           for w in ("HIGH", "LOW")}
    check("R11 (reported) clean discs whose r_out is FOV-LIMITED", "; ".join(f"{w}: {a}/{b}" for w, (a, b) in fov.items()), True,
          load_bearing=False)
    k3 = [o for o in S("HIGH", (0,)) if o["clean_noK3"] and o["ADDGAL"] == 1]
    rows13 = {fk: counts(k3, f"gdisc_a0_{fk}", 1.0) for fk in A0}
    check("R13 (reported) K3-excluded HIGH objects (FLAG_ADDGALDET = 1) that otherwise pass K1, K2 and the gate; of them g_bar < a0",
          f"{len(k3)} objects; " + "; ".join(f"{k}: {v}" for k, v in rows13.items()) + (" ; IDs " + ", ".join(o["ID"] for o in k3) if k3 else ""),
          True, load_bearing=False)
    lst = sorted([o for o in hi if o["gdisc_a0_canonical"] < 1 or o["gdisc_a0_alt"] < 1], key=lambda o: o["gdisc_a0_canonical"])
    P("\n  R14 (reported) HIGH clean discs with g_bar(r_out) < a0 on either footing:")
    P(f"    {'ID':11s} {'z':>6s} {'logM*':>6s} {'Re_kpc':>6s} {'r_out\"':>6s} {'r_kpc':>6s} {'r/Re':>5s} {'r/PSF':>5s} {'g/a0 can':>8s} "
      f"{'g/a0 alt':>8s} {'mu_gas':>6s} {'Vrot':>6s} {'sV/V':>5s} {'V/s0':>5s} {'i':>5s} {'FoV':>3s}")
    for o in lst:
        P(f"    {o['ID']:11s} {o['Z']:6.3f} {o['LMSTAR']:6.2f} {o['Re_kpc']:6.2f} {o['r_out']:6.2f} {o['r_out_kpc']:6.2f} "
          f"{o['r_out_over_Re']:5.2f} {o['r_out_over_psf']:5.2f} {o['gdisc_a0_canonical']:8.3f} {o['gdisc_a0_alt']:8.3f} {o['mu_gas']:6.2f} "
          f"{o['vrot']:6.1f} {o['sigv_over_v']:5.2f} {o['v_over_sigma']:5.2f} {o['incl']:5.1f} {int(bool(o.get('fov_limited')))}")
    if not lst:
        P("    (none)")
    check("R14 (reported) the list above", f"{len(lst)} objects", True, load_bearing=False)
    rr = np.array([o["R_at_Ha"] / o["SPEC_RES"] for o in S(("HIGH", "LOW", "MID"), (0,))
                   if o["status"] == "ok" and o.get("R_at_Ha") and o["SPEC_RES"] > 0])
    check("R15 (reported) header-polynomial R(lambda_Ha) / catalogue SPEC_RES", f"N = {rr.size}; median {float(np.median(rr)) if rr.size else float('nan'):.3f}, "
          f"p16-p84 {float(np.percentile(rr, 16)) if rr.size else float('nan'):.3f}-{float(np.percentile(rr, 84)) if rr.size else float('nan'):.3f}",
          True, load_bearing=False)
    R.num("R", dict(R3=rows3, R4=rows4, R5=rows5, n_R5=len(hi_res), R6=rows6, R7=rows7, R8=rows8, n_mid_clean=len(mid), R9=rows9, R11=fov,
                    R13=rows13, R14=[o["ID"] for o in lst]))
    # POST HOC (added after the first main run, disclosed in the README; reported only, changes no check): C1c showed that the measured
    # V(r_out) sits a median ~28% below the injected circular velocity (beam smearing + aperture averaging), which biases K2 (V/sigma_0 >= 1)
    # towards rejecting rotators.  This row shows how much the headline count depends on K2.
    noK2 = S("HIGH", (0,), lambda o: o["K1"] and o["ADDGAL"] == 0 and o.get("gate", False) and not o["K2"])
    p1 = {fk: counts(noK2, f"gdisc_a0_{fk}", 1.0) for fk in A0}
    p1b = {fk: counts(noK2, f"gdisc_a0_{fk}", 0.3) for fk in A0}
    check("P1 (reported; POST HOC after the first run, prompted by the C1c failure) HIGH objects passing K1, not K3 and the gate but failing K2 "
          "(V_rot/sigma_0 < 1); of them g_bar(r_out) < a0 and < 0.3 a0 -- i.e. the headline without K2 = the headline + these",
          f"{len(noK2)} objects; " + "; ".join(f"{fk}: N(<a0) {p1[fk]}, N(<0.3a0) {p1b[fk]} -> without K2: {head[fk]['n_lt_a0'] + p1[fk]}, "
                                              f"{head[fk]['n_lt_0p3'] + p1b[fk]}" for fk in A0)
          + "; their V_rot/sigma_0: " + fmt_pct(pct([o["v_over_sigma"] for o in noK2])), True, load_bearing=False)
    R.num("P1_posthoc", dict(n=len(noK2), lt_a0=p1, lt_0p3=p1b, ids_lt_a0_alt=[o["ID"] for o in noK2 if o["gdisc_a0_alt"] < 1]))

    # ------------------------------------------------------------------ reading
    feas = {fk: head[fk]["n_lt_a0"] >= 5 for fk in A0}
    reading = ("FEASIBLE on both footings" if all(feas.values()) else "FEASIBLE on the alt footing only" if feas["alt"] and not feas["canonical"]
               else "FEASIBLE on the canonical footing only" if feas["canonical"] else "NOT FEASIBLE on either footing")
    P(f"\n    READING (declared gate): {reading}.  This is a feasibility count, not a test of B.")
    R.num("reading", reading)

    # ------------------------------------------------------------------ tables
    cols = ["ID", "FIELD", "FILE", "window", "zq", "Z", "LMSTAR", "SFR", "RHALF", "Q", "PSF_FWHM", "ADDGAL", "HAFIT_FLAG", "HAFIT_FLUX_HA",
            "HAFIT_FLUX_HA_ERR", "status", "int_status", "int_flux", "int_eflux", "int_snr", "int_v", "int_ev", "int_f", "int_cover",
            "n_usable", "n_box_fit", "n_box_rel", "n_galmap", "E0", "x0", "y0", "cat_x", "cat_y", "incl", "pa_kin", "r2_vf", "rt_vf",
            "ap_diam", "k_run_pos", "k_run_neg", "r_out", "r_either", "fov_limited", "dv", "edv", "vrot", "sigv_over_v", "sigma0",
            "v_over_sigma", "K1", "K2", "notK3", "gate", "clean", "kpc_per_arcsec", "Re_kpc", "Rd_kpc", "age_gyr", "log_dMS", "mu_gas",
            "Mbar", "r_out_kpc", "r_out_over_Re", "r_out_over_psf", "gdisc_a0_canonical", "gdisc_a0_alt", "genc_a0_canonical",
            "genc_a0_alt", "gdisc_a0_gasx0.5_canonical", "gdisc_a0_gasx2_canonical", "gdisc_a0_gasx0.5_alt", "gdisc_a0_gasx2_alt",
            "gdisc_a0_either_canonical", "gdisc_a0_either_alt", "R_at_Ha", "SPEC_RES"]

    def cell(v):
        if isinstance(v, (bool, np.bool_)):
            return int(v)
        if isinstance(v, (float, np.floating)):
            return "" if not np.isfinite(v) else f"{float(v):.6g}"
        return "" if v is None else v
    with open(os.path.join(HERE, f"cfg89_per_object{SUFFIX}.csv"), "w", newline="") as fh:
        wr = csv.writer(fh); wr.writerow(cols)
        for o in sorted(objs, key=lambda o: (o["window"], o["zq"], o["ID"])):
            wr.writerow([cell(o.get(c)) for c in cols])
    ccols = ["ID", "k", "s", "covered", "fitted", "reliable", "in_run", "snr", "v", "ev", "s_int", "es_int", "f_noise"]
    with open(os.path.join(HERE, f"cfg89_curves{SUFFIX}.csv"), "w", newline="") as fh:
        wr = csv.writer(fh); wr.writerow(ccols)
        for o in sorted(objs, key=lambda o: o["ID"]):
            if not o["E0"]:
                continue
            for c in o["curves"]:
                wr.writerow([o["ID"]] + [c.get(k, "") for k in ccols[1:]])
    icols = ["tid", "host", "window", "rotating", "voff", "Zinj", "pa_true", "kin_pa_kin", "dpa", "incl", "psf", "beta", "vmax", "rt", "Rd",
             "sig0_true", "kin_E0", "kin_n_galmap", "kin_r2_vf", "kin_r_out", "r_exp", "kin_vrot", "v_true_rout", "kin_sigv_over_v", "kin_K1",
             "kin_K2", "kin_gate", "n_pulls", "status", "error"]
    with open(os.path.join(HERE, f"cfg89_c1_injections{SUFFIX}.csv"), "w", newline="") as fh:
        wr = csv.writer(fh); wr.writerow(icols)
        for x in sorted(inj, key=lambda x: x["tid"]):
            x = dict(x); x["n_pulls"] = len(x.get("pulls", []))
            wr.writerow([cell(x.get(c)) for c in icols])
    P(f"\n  wrote cfg89_per_object{SUFFIX}.csv ({len(objs)} rows), cfg89_curves{SUFFIX}.csv, cfg89_c1_injections{SUFFIX}.csv ({len(inj)} rows)")
    P("\n  kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the theory is closed, and nothing here says the data favour B, "
      "the framework or LCDM.")
    nf = R.write(here=HERE)
    return nf


if __name__ == "__main__":
    sys.exit(1 if main() else 0)

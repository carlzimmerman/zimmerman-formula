#!/usr/bin/env python3
"""CFG669 Part 3 (criteria 621ff3964): improved model (sky, 2 Sersic, 30^2 source). Based on Part 2 (criteria 83f30af17): full lens + source + light model of B1938+666 (JWST GO 8281 F277W), scoring the sealed
CFG668 prediction at perturber A. Semilinear inversion (Warren & Dye 2003; Suyu et al. 2006): Sersic lens light, SIE + shear
mass, pixelated regularised source, PSF point component at A (linear, sign free). Run with python3 -I.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math, time
import warnings
import numpy as np
warnings.filterwarnings('ignore', category=RuntimeWarning)  # spurious Accelerate matmul FP flags (finiteness checked)
import scipy.sparse as sp
from scipy.ndimage import shift as ndshift
from scipy.optimize import minimize
from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data", "cfg668_go8281")
BAND = os.environ.get("CFG669_BAND", "f115w")
IMG = os.path.join(DATA, f"jw08281-o001_t001_nircam_clear-{BAND}_i2d.fits")
CAT = os.path.join(DATA, f"jw08281-o001_t001_nircam_clear-{BAND}_cat.ecsv")
CFG = {"f115w": dict(pred={"canonical": {"faint": 30.88, "excl": 32.07}, "alt": {"faint": 31.02, "excl": 32.21}}, contam=25.7, tooth=29.0, extra=(30.5,)),
       "f277w": dict(pred={"canonical": {"faint": 29.63, "excl": 30.82}, "alt": {"faint": 29.77, "excl": 30.96}}, contam=25.4, tooth=28.0, extra=(29.6,))}[BAND]
PRED = CFG["pred"]
OUT, RES = [], {"lane": "CFG669 part 3", "band": BAND, "criteria": "621ff3964", "scores": "CFG668 9162427f"}
T0 = time.time()


def P(s=""):
    print(f"[{time.time()-T0:7.1f}s] {s}", flush=True); OUT.append(str(s))


# ------------------------------------------------------------------ data
hd = fits.open(IMG, memmap=True)
sci, err = hd["SCI"], hd["ERR"]
w = WCS(sci.header); pixar = sci.header["PIXAR_SR"]; scale = math.sqrt(pixar) * 206264.806
cat = Table.read(CAT)
tgt = SkyCoord(294.6050 * u.deg, 66.8146 * u.deg)
i0 = int(np.argmin(cat["sky_centroid"].separation(tgt).arcsec))
x0, y0 = [int(round(float(v))) for v in w.world_to_pixel(cat["sky_centroid"][i0])]
Hb = int(round(4.0 / scale))
big = np.array(sci.data[y0 - Hb:y0 + Hb + 1, x0 - Hb:x0 + Hb + 1], float)
yy, xx = np.mgrid[0:big.shape[0], 0:big.shape[1]]
r1 = int(round(1.0 / scale)); m1 = (xx - Hb) ** 2 + (yy - Hb) ** 2 <= r1 ** 2
bx = int(round(1.2 / scale)); sbox = big[Hb - bx:Hb + bx + 1, Hb - bx:Hb + bx + 1] - np.nanmedian(big)
sbox = np.clip(np.nan_to_num(sbox), 0, None); gyy, gxx = np.mgrid[-bx:bx + 1, -bx:bx + 1]
cxw, cyw = Hb + (sbox * gxx).sum() / sbox.sum(), Hb + (sbox * gyy).sum() / sbox.sum()
pk = [(j, k) for j in range(Hb - r1, Hb + r1 + 1) for k in range(Hb - r1, Hb + r1 + 1)
      if m1[j, k] and np.isfinite(big[j, k]) and big[j, k] == np.nanmax(big[j - 1:j + 2, k - 1:k + 2])]
yb, xb = min(pk, key=lambda p: (p[1] - cxw) ** 2 + (p[0] - cyw) ** 2)
s5 = big[yb - 2:yb + 3, xb - 2:xb + 3]; g5y, g5x = np.mgrid[-2:3, -2:3]
lxg, lyg = xb + (s5 * g5x).sum() / s5.sum() + x0 - Hb, yb + (s5 * g5y).sum() / s5.sum() + y0 - Hb   # nucleus, mosaic pixels
lens_sky = w.pixel_to_world(lxg, lyg)
NC = int(round(1.3 / scale))                        # 2.6" cutout
cxp, cyp = int(round(lxg)), int(round(lyg))
D = np.array(sci.data[cyp - NC:cyp + NC + 1, cxp - NC:cxp + NC + 1], float)
E = np.array(err.data[cyp - NC:cyp + NC + 1, cxp - NC:cxp + NC + 1], float)
good = np.isfinite(D) & np.isfinite(E) & (E > 0)
NP = D.shape[0]
ox, oy = cxp - NC, cyp - NC
nx, ny = lxg - ox, lyg - oy                         # nucleus in cutout pixels


def sky_to_cut(dn, dw):
    c = lens_sky.spherical_offsets_by(-dw * u.arcsec, dn * u.arcsec)
    px, py = w.world_to_pixel(c); return float(px) - ox, float(py) - oy


AX, AY = sky_to_cut(0.576, 0.036)
P(f"cutout {NP}x{NP}, pixel {scale:.4f}\"; nucleus RA {lens_sky.ra.deg:.6f} Dec {lens_sky.dec.deg:.6f}; "
  f"A at cutout ({AX:.2f},{AY:.2f}), r = {math.hypot(AX-nx, AY-ny)*scale:.3f}\"; good pixels {good.sum()}")

# ------------------------------------------------------------------ PSF
cx_all, cy_all = np.array(cat["xcentroid"], float), np.array(cat["ycentroid"], float)
mag = np.array(cat["aper_total_abmag"], float)
sel = (~np.array(cat["is_extended"], bool)) & (mag >= 20) & (mag <= 23.5) & (np.array(cat["nn_dist"], float) * scale >= 3.0)
ny_m, nx_m = sci.data.shape
edge = int(2.0 / scale)
sel &= (cx_all > edge) & (cx_all < nx_m - edge) & (cy_all > edge) & (cy_all < ny_m - edge)
stamps = []
for k in np.where(sel)[0]:
    X, Y = int(round(cx_all[k])), int(round(cy_all[k]))
    st = np.array(sci.data[Y - 10:Y + 11, X - 10:X + 11], float)
    if st.shape != (21, 21) or not np.all(np.isfinite(st)):
        continue
    st = st - np.median(np.concatenate([st[:2].ravel(), st[-2:].ravel(), st[:, :2].ravel(), st[:, -2:].ravel()]))
    c5 = st[8:13, 8:13]; c5c = np.clip(c5, 0, None)
    if c5c.sum() <= 0:
        continue
    gy_, gx_ = np.mgrid[-2:3, -2:3]
    dx_, dy_ = (c5c * gx_).sum() / c5c.sum(), (c5c * gy_).sum() / c5c.sum()
    st = ndshift(st, (-dy_, -dx_), order=3)
    if st.sum() <= 0:
        continue
    stamps.append(st / st.sum())
if len(stamps) >= 5:
    hw = 7 if scale < 0.04 else 5; psf = np.median(np.array(stamps), axis=0)[10 - hw:11 + hw, 10 - hw:11 + hw]; psf_src = f"empirical, {len(stamps)} stars"
else:
    hw = 7 if scale < 0.04 else 5; g = np.mgrid[-hw:hw + 1, -hw:hw + 1]; sg = 0.092 / scale / 2.3548
    psf = np.exp(-(g[0] ** 2 + g[1] ** 2) / (2 * sg ** 2)); psf_src = f"Gaussian fallback ({len(stamps)} stars)"
psf = np.clip(psf, 0, None); psf /= psf.sum()
P(f"PSF: {psf_src}; peak fraction {psf.max():.3f}")
RES["psf"] = psf_src

# blurring matrix (NP^2 x NP^2)
N = NP * NP
rows, cols, vals = [], [], []
pr = psf.shape[0] // 2
for j in range(NP):
    for k in range(NP):
        for a in range(-pr, pr + 1):
            for b in range(-pr, pr + 1):
                jj, kk = j + a, k + b
                if 0 <= jj < NP and 0 <= kk < NP:
                    rows.append(jj * NP + kk); cols.append(j * NP + k); vals.append(psf[a + pr, b + pr])
BL = sp.csr_matrix((vals, (rows, cols)), shape=(N, N))


def point_image(px, py):
    """PSF-shaped point source at cutout position (px,py), unit total flux in data units"""
    im = np.zeros((NP, NP)); X, Y = int(math.floor(px)), int(math.floor(py))
    stamp = ndshift(np.pad(psf, 2), (py - Y, px - X), order=3)
    s0 = stamp.shape[0] // 2
    for a in range(stamp.shape[0]):
        for b in range(stamp.shape[1]):
            jj, kk = Y + a - s0, X + b - s0
            if 0 <= jj < NP and 0 <= kk < NP:
                im[jj, kk] += stamp[a, b]
    return im / max(stamp.sum(), 1e-30)


# ------------------------------------------------------------------ model pieces (arcsec, cutout frame)
SUB = 2
so = (np.arange(SUB) + 0.5) / SUB - 0.5
gy_im, gx_im = np.mgrid[0:NP, 0:NP]
sx = ((gx_im[:, :, None, None] + so[None, None, None, :]) - nx) * scale
sy = ((gy_im[:, :, None, None] + so[None, None, :, None]) - ny) * scale
SX, SY = np.broadcast_arrays(sx, sy)
SX, SY = SX.reshape(N, SUB * SUB), SY.reshape(N, SUB * SUB)
RAD = np.hypot(((gx_im - nx) * scale).ravel(), ((gy_im - ny) * scale).ravel())
ANN = (RAD >= 0.25) & (RAD <= 0.85)


def sersic(p):
    xc, yc, Re, n, q, ph = p
    c, s = math.cos(ph), math.sin(ph)
    x, y = SX - xc, SY - yc
    xp, yp = c * x + s * y, -s * x + c * y
    R = np.sqrt(q * xp ** 2 + yp ** 2 / q) + 1e-6
    bn = 2 * n - 1 / 3 + 4 / (405 * n)
    return np.exp(-bn * ((R / Re) ** (1 / n) - 1)).mean(axis=1)


def deflect(p):
    b, q, ph, dx, dy, g1, g2 = p
    x, y = SX - dx, SY - dy
    c, s = math.cos(ph), math.sin(ph)
    xp, yp = c * x + s * y, -s * x + c * y
    q = min(max(q, 0.2), 0.99); f = math.sqrt(1 - q * q)
    psi = np.sqrt(q * q * xp ** 2 + yp ** 2) + 1e-9
    axp = b / f * np.arctan(f * xp / psi)
    ayp = b / f * np.arctanh(np.clip(f * yp / psi, -0.999999, 0.999999))
    ax, ay = c * axp - s * ayp, s * axp + c * ayp
    ax += g1 * SX + g2 * SY; ay += g2 * SX - g1 * SY
    return SX - ax, SY - ay                         # source-plane positions


def grad_reg(ns):
    idx = np.arange(ns * ns).reshape(ns, ns); r, c_, v = [], [], []
    k = 0
    for j in range(ns):
        for i in range(ns):
            if i + 1 < ns:
                r += [k, k]; c_ += [idx[j, i], idx[j, i + 1]]; v += [1, -1]; k += 1
            if j + 1 < ns:
                r += [k, k]; c_ += [idx[j, i], idx[j + 1, i]]; v += [1, -1]; k += 1
    Hm = sp.csr_matrix((v, (r, c_)), shape=(k, ns * ns))
    return (Hm.T @ Hm).toarray() + 1e-8 * np.eye(ns * ns)


REGS = {}
Dv, Ev, Gv = D.ravel(), E.ravel(), good.ravel()
Wv = np.where(Gv, 1 / np.where(Gv, Ev, 1) ** 2, 0.0)
Dv0 = np.where(Gv, Dv, 0.0)


def design(pn, ns, extra_points):
    """columns: source pixels (ns^2), lens light (1), point sources (len(extra_points))"""
    bsx, bsy = deflect(pn[10:17])
    ax_ = bsx.reshape(NP * NP, -1)[ANN]; ay_ = bsy.reshape(NP * NP, -1)[ANN]
    x_lo, x_hi, y_lo, y_hi = ax_.min(), ax_.max(), ay_.min(), ay_.max()
    pad = 1e-6
    gxs = (bsx - x_lo) / (x_hi - x_lo + pad) * (ns - 1); gys = (bsy - y_lo) / (y_hi - y_lo + pad) * (ns - 1)
    ins = (gxs >= 0) & (gxs <= ns - 1) & (gys >= 0) & (gys <= ns - 1)
    i0_ = np.clip(np.floor(gxs).astype(int), 0, ns - 2); j0_ = np.clip(np.floor(gys).astype(int), 0, ns - 2)
    fx, fy = gxs - i0_, gys - j0_
    rr = np.repeat(np.arange(N), SUB * SUB)
    R_, C_, V_ = [], [], []
    for (di, dj, wt) in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        wv = (wt * ins / (SUB * SUB)).ravel()
        R_.append(rr); C_.append(((j0_ + dj) * ns + (i0_ + di)).ravel()); V_.append(wv)
    Lm = sp.csr_matrix((np.concatenate(V_), (np.concatenate(R_), np.concatenate(C_))), shape=(N, ns * ns))
    Ms = (BL @ Lm).toarray()
    ll1 = BL @ sersic(pn[0:6]); ll2 = BL @ sersic(np.r_[pn[0:2], pn[6:10]])
    cols_ = [Ms, ll1[:, None], ll2[:, None], np.ones((N, 1))] + [point_image(px, py).ravel()[:, None] for (px, py) in extra_points]
    return np.hstack(cols_)


def solve(pn, ns, lam_rel, points, data=None, want=False):
    d = Dv0 if data is None else np.where(Gv, data, 0.0)
    M = design(pn, ns, points)
    if ns not in REGS:
        REGS[ns] = grad_reg(ns)
    C = REGS[ns]; nsrc = ns * ns; nt = M.shape[1]
    Fm = M.T @ (M * Wv[:, None]); dv = M.T @ (Wv * d)
    lam = lam_rel * np.trace(Fm[:nsrc, :nsrc]) / np.trace(C)
    A = Fm.copy(); A[:nsrc, :nsrc] += lam * C
    A[nsrc:, nsrc:] += 1e-12 * np.eye(nt - nsrc) * np.trace(Fm) / nt
    try:
        Lc = np.linalg.cholesky(A)
    except np.linalg.LinAlgError:
        return (-1e30, None) if want else -1e30
    s = np.linalg.solve(A, dv)
    model = M @ s; chi2 = float(np.sum(Wv * (d - model) ** 2))
    reg = float(lam * s[:nsrc] @ C @ s[:nsrc])
    ldA = 2 * np.sum(np.log(np.diag(Lc)))
    ldC = nsrc * math.log(lam) + np.linalg.slogdet(C)[1]
    logE = -0.5 * (chi2 + reg) + 0.5 * ldC - 0.5 * ldA
    if not want:
        return logE
    cov = np.linalg.inv(A)
    return logE, dict(s=s, chi2=chi2, ngood=int(Gv.sum()), cov=cov, nsrc=nsrc, model=model, lam=lam)


# nonlinear parameter vector: sersic(xc,yc,Re,n,q,phi) + mass(b,q,phi,dx,dy,g1,g2)
P0 = RES.setdefault("p_part2", None)
p_init = np.array([0, 0, 0.15, 2.0, 0.8, 0.0, 1.0, 1.0, 0.9, 0.0, 0.45, 0.85, 0.0, 0, 0, 0, 0])
LO = np.array([-0.05, -0.05, 0.02, 0.5, 0.3, -math.pi, 0.1, 0.5, 0.3, -math.pi, 0.2, 0.3, -math.pi, -0.05, -0.05, -0.2, -0.2])
HI = np.array([0.05, 0.05, 4.0, 8.0, 1.0, math.pi, 4.0, 8.0, 1.0, math.pi, 0.8, 0.99, math.pi, 0.05, 0.05, 0.2, 0.2])
NS, LAM = 30, 1.0
NLIN = 4                                            # lens light x2, sky, then point sources start at nsrc + 3


def neg(p, ns=NS, lam=None, pts=None):
    if np.any(p < LO) or np.any(p > HI):
        return 1e30
    return -solve(p, ns, LAM if lam is None else lam, [(AX, AY)] if pts is None else pts)


def fit(p_start, restarts=4, maxfev=2500):
    best = p_start.copy(); bv = neg(best)
    rng = np.random.default_rng(669)
    for r in range(restarts):
        st = best if r == 0 else np.clip(best + rng.normal(0, 1, best.size) * (HI - LO) * 0.03, LO, HI)
        o = minimize(neg, st, method="Nelder-Mead", options=dict(maxfev=maxfev, xatol=1e-4, fatol=1e-3, adaptive=True))
        if o.fun < bv:
            best, bv = o.x, o.fun
        P(f"  restart {r}: -logE {o.fun:.2f} (best {bv:.2f})")
    return best, bv


def set_lambda(p):
    global LAM
    grid = np.logspace(-6, 3, 19); vals = [solve(p, NS, g, [(AX, AY)]) for g in grid]
    LAM = float(grid[int(np.argmax(vals))]); return LAM


if os.environ.get("CFG669_SMOKE") == "1":
    t = time.time(); v = neg(p_init); P(f"SMOKE: one evaluation -logE {v:.2f} in {time.time()-t:.3f}s"); sys.exit(0)
P("stage 1: nonlinear fit at lambda_rel = 1")
pb, _ = fit(p_init)
P(f"lambda_rel -> {set_lambda(pb)}")
P("stage 2: refit at evidence lambda")
pb, _ = fit(pb, restarts=2)
P(f"lambda_rel -> {set_lambda(pb)}")
pb, _ = fit(pb, restarts=1)
logE, sol = solve(pb, NS, LAM, [(AX, AY)], want=True)
chi2nu = sol["chi2"] / max(sol["ngood"] - pb.size, 1)
P(f"best: chi2 {sol['chi2']:.1f} / {sol['ngood']} pix (chi2_nu {chi2nu:.2f}); logE {logE:.2f}; params {np.round(pb, 4).tolist()}")
RES.update(params=pb.tolist(), lambda_rel=LAM, chi2=sol["chi2"], chi2_nu=chi2nu, logE=logE)

conv = 1e6 * pixar                                   # sum of MJy/sr pixels -> Jy
iA = sol["nsrc"] + 3
fA = sol["s"][iA]; sstat = math.sqrt(sol["cov"][iA, iA]) * math.sqrt(max(chi2nu, 1.0))
# arc-absorption systematic: the point component at other same-radius positions
rA = math.hypot(AX - nx, AY - ny); phA = math.atan2(AY - ny, AX - nx); amps = []
for k in range(12):
    ph = phA + math.radians(30 * k); px, py = nx + rA * math.cos(ph), ny + rA * math.sin(ph)
    if math.hypot(px - AX, py - AY) * scale < 0.25:
        continue
    _, so_ = solve(pb, NS, LAM, [(px, py)], want=True); amps.append(so_["s"][so_["nsrc"] + 3])
amps = np.array(amps); spos = 1.4826 * np.median(np.abs(amps - np.median(amps)))
sysv = [solve(pb, NS, LAM * f, [(AX, AY)], want=True)[1]["s"][NS * NS + 3] for f in (1 / 3, 3)]
sysv += [solve(pb, ns, LAM, [(AX, AY)], want=True)[1]["s"][ns * ns + 3] for ns in (18, 30)]
ssys = 0.5 * (max(sysv + [fA]) - min(sysv + [fA]))
stot = math.sqrt(sstat ** 2 + spos ** 2 + ssys ** 2)
ab = lambda f: -2.5 * math.log10(f * conv / 3631) if f > 0 else float("inf")
S = fA / stot; mA = ab(fA); mlim = ab(2 * stot)
P(f"A: f = {fA*conv:.3e} Jy; sigma stat {sstat*conv:.2e}, pos {spos*conv:.2e} (n={len(amps)}, same-radius amps median "
  f"{np.median(amps)*conv:.2e}), sys {ssys*conv:.2e} -> tot {stot*conv:.2e}; S = {S:.2f}; m_A = {mA:.2f}; 2sig limit {mlim:.2f} AB")
floor = math.sqrt(sol["cov"][iA, iA]) * conv; RES["floor_chi2nu1_2sig_AB"] = ab(2 * floor / conv)
P(f"diagnostic: chi2_nu = 1 floor (2 sigma) = {ab(2 * floor / conv):.2f} AB")
RES.update(f_A_Jy=fA * conv, sig_stat=sstat * conv, sig_pos=spos * conv, sig_sys=ssys * conv, sig_tot=stot * conv, S=S,
           m_A=mA, m_lim_2sig=mlim, same_radius_amps_Jy=(amps * conv).tolist())

# tooth: inject 28.0 and 29.6 AB at A
inj = {}
TM = CFG["tooth"]
for mg in (TM,) + CFG["extra"]:
    fl = 3631 * 10 ** (-0.4 * mg) / conv
    dinj = Dv + fl * point_image(AX, AY).ravel()
    _, si = solve(pb, NS, LAM, [(AX, AY)], data=dinj, want=True)
    fi = si["s"][si["nsrc"] + 3] - fA                                 # recovered injected flux (linear re-solve)
    inj[mg] = dict(recovered_AB=ab(fi), S=fi / stot)
    P(f"  inject {mg} AB (linear re-solve): recovered {ab(fi):.2f} AB, S = {fi/stot:.2f}")
fl = 3631 * 10 ** (-0.4 * TM) / conv
Dsave = Dv0.copy(); Dv0 = np.where(Gv, Dv + fl * point_image(AX, AY).ravel(), 0.0)
pj, _ = fit(pb, restarts=1, maxfev=1500)
_, sj = solve(pj, NS, LAM, [(AX, AY)], want=True); Dv0 = Dsave
fj = sj["s"][sj["nsrc"] + 3] - fA
inj["tooth_refit"] = dict(recovered_AB=ab(fj), S=fj / stot)
P(f"  inject {TM} AB (full nonlinear refit): recovered {ab(fj):.2f} AB, S = {fj/stot:.2f}")
tooth = all(abs(inj[k]["recovered_AB"] - TM) <= 0.5 and inj[k]["S"] >= 3 for k in (TM, "tooth_refit"))
RES["injection"] = {str(k): v for k, v in inj.items()}; RES["tooth_bites"] = tooth
P(f"TOOTH ({TM} AB): {'BITES' if tooth else 'FAILS'}")

for f, p in PRED.items():
    if not tooth:
        v = "NOT DIAGNOSTIC (tooth fails)"
    elif S >= 3 and mA < CFG["contam"]:
        v = f"NOT DIAGNOSTIC (contamination: brighter than {CFG['contam']} AB)"
    elif S >= 3 and mA <= p["faint"]:
        v = "SURVIVES"
    elif S < 2 and mlim > p["excl"]:
        v = "EXCLUDED"
    elif mlim < p["faint"]:
        v = "NOT DIAGNOSTIC"
    else:
        v = "TENSION"
    RES[f"verdict_{f}"] = v; P(f"VERDICT ({f}): {v}")

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    mod = sol["model"].reshape(NP, NP); res = (np.where(good, D, np.nan) - mod)
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    vmax = np.nanpercentile(D, 99.5)
    for a_, im_, t_ in zip(axs, (D, mod, res / E), ("data F277W", "model (lens + arc + sky + A)", "residual / sigma")):
        a_.imshow(im_, origin="lower", cmap="gray" if t_ != "residual / sigma" else "RdBu_r",
                  vmin=(-5 if t_ == "residual / sigma" else -0.02 * vmax), vmax=(5 if t_ == "residual / sigma" else vmax))
        a_.add_patch(plt.Circle((AX, AY), 0.075 / scale, fill=False, color="lime")); a_.set_title(t_); a_.set_xticks([]); a_.set_yticks([])
    fig.savefig(os.path.join(HERE, f"cfg669_v3_{BAND}.png"), dpi=110, bbox_inches="tight")
except Exception as e:
    P(f"(figure skipped: {e})")
json.dump(RES, open(os.path.join(HERE, f"cfg669_v3_{BAND}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg669_v3_{BAND}.out"), "w").write("\n".join(OUT) + "\n")

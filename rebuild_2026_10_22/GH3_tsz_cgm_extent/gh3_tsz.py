#!/usr/bin/env python3
"""GH3_tsz_cgm_extent: stacked ACT DR6.02 NILC Compton-y around the KiDS isolated lenses (bins 3-4) in R/R_vir annuli,
against beam-convolved predictions of Zhang+24's hot gas cut at k = 1, 1.8, 3 R_vir. Frozen criteria: FROZEN_CRITERIA.md
(05e38c3ad3). One thread; the y-map strip is read in Dec chunks (RSS < 1 GB).
kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed; nothing here says the data favour the framework.
    GH3_MAP=ComptonY|ComptonY_deproj_cib_1.0_10.7  GH3_SAMPLE=kids|kids_z025|g09  [GH3_MUTATE=1]
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh3_tsz.py
"""
import os, sys, io, json, math, time, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy import stats
T0 = time.time()
MAP = os.environ.get("GH3_MAP", "ComptonY"); SAMPLE = os.environ.get("GH3_SAMPLE", "kids"); MUT = os.environ.get("GH3_MUTATE") == "1"
TAG = f"_{MAP}_{SAMPLE}" + ("_MUTATE" if MUT else "")
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
EXT = os.path.join(os.path.dirname(REPO), "_external_data"); ACT = os.path.join(EXT, "act_dr6_nilc")
OUT, CHK = [], {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(k, ok, v): CHK[k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} ({v})")
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9

# ------------------------------------------------------------ map geometry (frozen)
NX, R0, R1 = 43200, 3239, 8040; NR = R1 - R0 + 1; ROWB = NX * 4
STRIP = os.path.join(ACT, f"strip_{MAP}.f32be")
assert os.path.getsize(STRIP) == NR * ROWB, os.path.getsize(STRIP)
def col_of(ra): ra = np.where(ra >= 180, ra - 360, ra); return 21600.0 - 120.0 * ra
def row_of(dec): return 7559.5 + 120.0 * dec
from astropy.io import fits
from astropy.wcs import WCS
hdr = fits.Header.fromstring(open(os.path.join(ACT, f"header_{MAP}.fits"), "rb").read(2880).decode("ascii"))
W = WCS(hdr)
tp = np.array([[12.3, -5.0], [133.7, 1.2], [200.1, -30.5], [355.2, 2.9]])
px = W.all_world2pix(tp, 0)
d3 = float(np.max(np.abs(np.c_[col_of(tp[:, 0]), row_of(tp[:, 1])] - px)))
check("K3_pixel_geometry", d3 < 0.01, f"max |d pix| {d3:.2e} vs astropy WCS")

# ------------------------------------------------------------ cosmology (native, as F2) and gas model
H_NAT, OM = 0.679, 0.3085
def chi_flat(z, om=OM):
    zz = np.linspace(0, 1.0, 4001); E = np.sqrt(om * (1 + zz) ** 3 + 1 - om)
    ch = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]); return np.interp(z, zz, ch)
DH = 299792.458 / (100 * H_NAT)                                            # Mpc
def DA(z): return DH * chi_flat(z) / (1 + z)                               # Mpc
ZT1 = np.array([[10.5, 178.0], [10.75, 210.0], [11.0, 295.0]])             # Zhang Table 1 (log M*, R_h kpc)
def Rvir_kpc(l): return np.interp(l, ZT1[:, 0], ZT1[:, 1])
BETA, RCK, NORM, TKEV, MUE = 0.43, 6.0, 1.84, 0.22, 1.14
SIGT, MEC2, MP, MSUN, KPC, KEV = 6.6524587e-29, 8.1871057e-14, 1.67262192e-27, 1.98847e30, 3.0856776e19, 1.602176634e-16
XE = np.array([0, 0.5, 1.0, 1.8, 3.0, 5.0]); NA = len(XE) - 1
FWHM = 1.6; SB = FWHM / (2 * math.sqrt(2 * math.log(2)))


def y_profile_kpc(Rk, l, k):
    """projected Compton-y at projected radii Rk [kpc] for a lens of native log M* l, gas cut at k R_vir."""
    Rv = Rvir_kpc(l); rcut = k * Rv
    rr = np.linspace(0, Rv, 20001); sh = (1 + (rr / RCK) ** 2) ** (-1.5 * BETA)
    Mshape = np.trapz(4 * np.pi * rr ** 2 * sh, rr)                         # kpc^3
    rho0 = NORM * 10 ** l * MSUN / (Mshape * KPC ** 3)                      # kg/m^3
    ne0 = rho0 / (MUE * MP)
    out = np.zeros_like(Rk, dtype=float)
    for i, R in enumerate(Rk):
        if R >= rcut: continue
        lmax = math.sqrt(rcut ** 2 - R ** 2); ll = np.linspace(0, lmax, 4001)
        out[i] = 2 * np.trapz((1 + (R * R + ll * ll) / RCK ** 2) ** (-1.5 * BETA), ll) * KPC
    return SIGT / MEC2 * TKEV * KEV * ne0 * out


# K1: beta = 2/3 projection closed form: int n0 (1+(R^2+l^2)/rc^2)^-1 dl over all l = pi rc^2 / sqrt(rc^2+R^2)  (n0 = 1)
_R, _rc = 30.0, 6.0; _ll = np.linspace(0, 3e5, 3_000_001)
k1n = 2 * np.trapz((1 + (_R ** 2 + _ll ** 2) / _rc ** 2) ** -1.0, _ll); k1c = math.pi * _rc ** 2 / math.sqrt(_rc ** 2 + _R ** 2)
check("K1_projection_closed_form", abs(k1n / k1c - 1) < 1e-4, f"{k1n / k1c - 1:+.1e}")

# fine-grid beam-convolved model in x = R/R_vir annuli, per (z, lm) cell
FG = 0.05; NF_ = int(14 / FG); fx = (np.arange(2 * NF_ + 1) - NF_) * FG; FXX, FYY = np.meshgrid(fx, fx); FTH = np.hypot(FXX, FYY)   # arcmin
BK = np.exp(-0.5 * FTH ** 2 / SB ** 2); BK /= BK.sum(); BKF = np.fft.rfft2(np.fft.ifftshift(BK))


def model_annuli(z, l, k):
    da = DA(z) * 1e3; thv = Rvir_kpc(l) / da * 180 / math.pi * 60                # R_vir in arcmin
    Rk = np.linspace(0, 14 * da * math.pi / 180 / 60, 600); yk = y_profile_kpc(Rk, l, k)
    img = np.interp(FTH * da * math.pi / 180 / 60, Rk, yk)
    conv = np.fft.irfft2(np.fft.rfft2(img) * BKF, s=img.shape)
    x = FTH / thv
    return np.array([conv[(x >= XE[a]) & (x < XE[a + 1])].mean() for a in range(NA)])


# ------------------------------------------------------------ samples
if SAMPLE.startswith("kids"):
    L = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
    lm70, z, ra, dec = L["logM"], L["z"], L["ra"], L["dec"]
    m = (lm70 >= 10.6) & (lm70 <= 11.0) & (z <= (0.25 if SAMPLE == "kids_z025" else 9))
    qDA = chi_flat(z[m], OM) / chi_flat(z[m], 0.3)
    lm = lm70[m] + 2 * np.log10(0.70 / H_NAT) + 2 * np.log10(qDA); z, ra, dec = z[m], ra[m], dec[m]
else:
    E = np.load(os.path.join(EXT, "gh1_work", "gh1_esd.npz"))
    S75 = os.path.join(REB, "X75_satellite_kinematics_mass_gap", "x75_satkin.py"); s75 = open(S75).read()
    s75 = s75[:s75.index("# ============================================================ measurement")]
    G75 = {"__file__": S75, "__name__": "x75_ro"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(s75, S75, "exec"), G75)
    Hh = G75["H"]; hb = G75["hbin"]; sel = (hb == 2) | (hb == 3)
    lm, z, ra, dec = G75["lm"][Hh][sel], G75["z"][Hh][sel], G75["ra"][Hh][sel], G75["dec"][Hh][sel]
inmap = (dec > -35.9) & (dec < 3.9)
lm, z, ra, dec = lm[inmap], z[inmap], ra[inmap], dec[inmap]
P(f"GH3  criteria 05e38c3ad3  map {MAP}  sample {SAMPLE}{' [MUTATE]' if MUT else ''}: {len(z)} lenses in the strip  [{time.time() - T0:.0f} s]")
rng = np.random.default_rng(303)
NRAND = 3
rra = np.repeat(ra, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND) / np.cos(np.radians(np.repeat(dec, NRAND)))
rde = np.clip(np.repeat(dec, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), -35.85, 3.85)
rz, rlm, rown = np.repeat(z, NRAND), np.repeat(lm, NRAND), np.repeat(np.arange(len(z)), NRAND)
rra = np.mod(rra, 360)
if MUT:                                                                     # randoms as lenses, a second random set as background
    ra, dec, z, lm = rra[::NRAND].copy(), rde[::NRAND].copy(), rz[::NRAND].copy(), rlm[::NRAND].copy()
    rra = np.mod(np.repeat(ra, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), 360); rde = np.clip(np.repeat(dec, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), -35.85, 3.85)

# ------------------------------------------------------------ stacking (Dec-chunked)
HW = 24                                                                     # stamp half-width, pixels (12')
DD = (np.arange(2 * HW + 1) - HW)


def annuli_for(arr_get, ra_, dec_, z_, lm_):
    """per-object annulus means (NaN if stamp invalid). arr_get(r0, r1, c0, c1) returns the map block."""
    out = np.full((len(ra_), NA), np.nan)
    da = DA(z_) * 1e3; thv = Rvir_kpc(lm_) / da * 180 / math.pi * 60
    cf, rf = col_of(ra_), row_of(dec_)
    for i in range(len(ra_)):
        c0, r0 = int(round(cf[i])), int(round(rf[i]))
        blk = arr_get(r0 - HW, r0 + HW + 1, c0 - HW, c0 + HW + 1)
        if blk is None or not np.all(np.isfinite(blk)) or np.any(blk == 0): continue
        dy = (r0 + DD[:, None] - rf[i]) / 120 * 60; dx = (c0 + DD[None, :] - cf[i]) / 120 * 60 * math.cos(math.radians(dec_[i]))
        x = np.hypot(dx, dy) / thv[i]
        out[i] = [blk[(x >= XE[a]) & (x < XE[a + 1])].mean() if np.any((x >= XE[a]) & (x < XE[a + 1])) else np.nan for a in range(NA)]
    return out


def stack_strip(ra_, dec_, z_, lm_, CH=400):
    """objects whose centre row (strip-relative) falls in [s0, s0+CH) are stacked from a block read with a HW+2 margin."""
    res = np.full((len(ra_), NA), np.nan); rows = np.round(row_of(dec_)).astype(int) - R0
    for s0 in range(0, NR, CH):
        sel = np.where((rows >= s0) & (rows < s0 + CH))[0]
        if not len(sel): continue
        a0, a1 = max(0, s0 - HW - 2), min(NR, s0 + CH + HW + 2)
        blk = np.fromfile(STRIP, dtype=">f4", count=(a1 - a0) * NX, offset=a0 * ROWB).reshape(a1 - a0, NX).astype(np.float32)
        def get(r0, r1, c0, c1, blk=blk, a0=a0):
            r0 -= R0 + a0; r1 -= R0 + a0
            if r0 < 0 or r1 > blk.shape[0]: return None
            return np.take(blk[r0:r1], np.arange(c0, c1) % NX, axis=1) if (c0 < 0 or c1 > NX) else blk[r0:r1, c0:c1]
        res[sel] = annuli_for(get, ra_[sel], dec_[sel], z_[sel], lm_[sel])
        del blk
    return res


# K2: synthetic beam source of known Y in a blank block, stacked through annuli_for
Ysyn = 1e-6                                                                 # arcmin^2
blank = np.zeros((400, 400), np.float32); rc0, cc0 = 200, 200
gr, gc = np.mgrid[0:400, 0:400]; th = np.hypot((gr - rc0) / 2.0, (gc - cc0) / 2.0)
blank += (Ysyn / (2 * math.pi * SB ** 2) * np.exp(-0.5 * th ** 2 / SB ** 2)).astype(np.float32)
Ysum = float(blank.sum() * 0.25)
blank[blank == 0] = 1e-30
def get_syn(r0, r1, c0, c1): return blank[r0 - (R0 + 4000) + 200: r1 - (R0 + 4000) + 200, c0 - 10000 + 200: c1 - 10000 + 200]
dec_s = (R0 + 4000 - 7559.5) / 120; ra_s = (21600 - 10000) / 120
ann = annuli_for(get_syn, np.array([ra_s]), np.array([dec_s]), np.array([0.2]), np.array([10.8]))[0]
thv_s = Rvir_kpc(10.8) / (DA(0.2) * 1e3) * 180 / math.pi * 60
cf_s, rf_s = col_of(np.array([ra_s]))[0], row_of(np.array([dec_s]))[0]
dyp = (round(rf_s) + DD[:, None] - rf_s) / 2.0; dxp = (round(cf_s) + DD[None, :] - cf_s) / 2.0 * math.cos(math.radians(dec_s))
gth = np.hypot(dxp, dyp); gv = Ysyn / (2 * math.pi * SB ** 2) * np.exp(-0.5 * gth ** 2 / SB ** 2); xg = gth / thv_s
pred = [gv[(xg >= XE[a]) & (xg < XE[a + 1])].mean() for a in range(NA)]
k2 = float(np.max(np.abs(np.array(ann) / np.array(pred) - 1)))
check("K2_synthetic_source", abs(Ysum / Ysyn - 1) < 0.02 and k2 < 0.02, f"Y recovered {Ysum / Ysyn:.4f}; annulus means vs beam at the same pixels: max rel {k2:.1e}")

AL = stack_strip(ra, dec, z, lm); P(f"  lenses stacked [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
AR = stack_strip(rra, rde, np.repeat(z, NRAND), np.repeat(lm, NRAND)); P(f"  randoms stacked [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
okL = np.all(np.isfinite(AL), 1); okR = np.all(np.isfinite(AR), 1)
P(f"  valid stamps: lenses {okL.sum()}/{len(okL)}, randoms {okR.sum()}/{len(okR)}")
NP_ = 30; edges = np.quantile(ra[okL], np.linspace(0, 1, NP_ + 1)); edges[0] -= 1; edges[-1] += 1
pl = np.clip(np.digitize(ra, edges) - 1, 0, NP_ - 1); prr = pl[np.repeat(np.arange(len(ra)), NRAND)]


def prof(maskL, maskR): return AL[maskL & okL].mean(0) - AR[maskR & okR].mean(0)


Y = prof(np.ones(len(ra), bool), np.ones(len(rra), bool))
JK = np.array([prof(pl != p, prr != p) for p in range(NP_)])
C = (NP_ - 1) / NP_ * (JK - JK.mean(0)).T @ (JK - JK.mean(0)); Ci = np.linalg.inv(C) * (NP_ - NA - 2) / (NP_ - 1)
err = np.sqrt(np.diag(C))
P(f"  stacked y (x1e8) per annulus {list(zip(XE[:-1], XE[1:]))}: {np.round(Y * 1e8, 3).tolist()} +- {np.round(err * 1e8, 3).tolist()}")
P(f"  raw lens stack (x1e8) {np.round(AL[okL].mean(0) * 1e8, 3).tolist()}; random stack {np.round(AR[okR].mean(0) * 1e8, 3).tolist()}")
chi0 = float(Y @ Ci @ Y); P(f"  null chi2 (y = 0): {chi0:.1f}/{NA} (p {stats.chi2.sf(chi0, NA):.3g})")
RES = {"criteria": "05e38c3ad3", "map": MAP, "sample": SAMPLE, "mutate": MUT, "n_lens": int(okL.sum()), "n_rand": int(okR.sum()),
       "annuli_x": XE.tolist(), "Y": Y.tolist(), "err": err.tolist(), "null_chi2": chi0}
if MUT:
    check("MUTATE_random_lenses_null", stats.chi2.sf(chi0, NA) > 0.01, f"p {stats.chi2.sf(chi0, NA):.3f}")
else:
    zg = np.round(np.clip(z[okL], 0.1, 0.5) / 0.025) * 0.025; lg = np.round(lm[okL] / 0.1) * 0.1
    cells, inv = np.unique(np.c_[zg, lg], axis=0, return_inverse=True); wcell = np.bincount(inv.ravel(), minlength=len(cells))
    fits_ = {}
    for k in (1.0, 1.8, 3.0):
        M = np.array([model_annuli(zc, lc, k) for zc, lc in cells]); mod = (M * wcell[:, None]).sum(0) / wcell.sum()
        r = Y - mod; c2 = float(r @ Ci @ r)
        A = float((mod @ Ci @ Y) / (mod @ Ci @ mod)); rA = Y - A * mod; c2A = float(rA @ Ci @ rA); sA = float(1 / math.sqrt(mod @ Ci @ mod))
        fits_[k] = dict(model=mod.tolist(), chi2=c2, p=float(stats.chi2.sf(c2, NA)), A=A, sA=sA, chi2_A=c2A, p_A=float(stats.chi2.sf(c2A, NA - 1)))
        P(f"  k = {k}: model (x1e8) {np.round(mod * 1e8, 3).tolist()}; chi2 {c2:.1f} (p {fits_[k]['p']:.3g}); free amplitude A {A:.2f}+-{sA:.2f}, chi2 {c2A:.1f} (p {fits_[k]['p_A']:.3g})  [{time.time() - T0:.0f} s]")
    c1, c3 = fits_[1.0], fits_[3.0]
    if c3["chi2"] < c1["chi2"] - 4 and c3["p"] > 0.01: V = "EXTENDED GAS PREFERRED"
    elif c1["chi2"] < c3["chi2"] - 4 and c1["p"] > 0.01: V = "MEASURED EXTENT PREFERRED"
    elif all(f["p"] < 0.01 for f in fits_.values()): V = "NEITHER FITS"
    else: V = "NOT DECIDED"
    RES.update(fits={str(k): v for k, v in fits_.items()}, verdict=V); P(f"\n=== VERDICT [{MAP}, {SAMPLE}]: {V}")
RES["checks"] = CHK; n = sum(CHK.values()); P(f"checks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"gh3_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"gh3{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)

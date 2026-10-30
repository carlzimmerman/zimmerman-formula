#!/usr/bin/env python3
"""GH5_tsz_desi_centrals: ACT DR6.02 NILC y stacked on DESI DR1 BGS MW-mass centrals (gh5_select.py), compensated as GH4,
against Zhang+24 gas cut at k = 1, 1.8, 3 R_vir with no free parameter. Frozen criteria: FROZEN_CRITERIA.md. One thread.
kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed; nothing here says the data favour the framework.
    GH5_MAP=ComptonY_deproj_cib_1.0_10.7|ComptonY  GH5_TIER=central|clean|iso3|comp08|passive|sf|kids  [GH5_MUTATE=1]
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh5_tsz_desi.py
"""
import os, sys, json, math, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy import stats
from scipy.spatial import cKDTree
T0 = time.time()
MAP = os.environ.get("GH5_MAP", "ComptonY_deproj_cib_1.0_10.7"); TIER = os.environ.get("GH5_TIER", "central")
MUT = os.environ.get("GH5_MUTATE") == "1"
SEED = int(os.environ.get("GH5_SEED", "303"))                               # != 303: post-freeze null-scatter diagnostic
TAG = f"_{MAP}_{TIER}" + ("_MUTATE" if MUT else "") + (f"_seed{SEED}" if SEED != 303 else "")
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
EXT = os.path.join(os.path.dirname(REPO), "_external_data"); ACT = os.path.join(EXT, "act_dr6_nilc")
LRD = os.path.join(REPO, "real_research", "data", "lensing_rar")
OUT, CHK = [], {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(k, ok, v): CHK[k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} ({v})")
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9

# ------------------------------------------------------------ map geometry (as GH3)
NX, R0, R1 = 43200, 3239, 8040; NR = R1 - R0 + 1; ROWB = NX * 4
STRIP = os.path.join(ACT, f"strip_{MAP}.f32be")
assert os.path.getsize(STRIP) == NR * ROWB, os.path.getsize(STRIP)
def col_of(ra): ra = np.where(ra >= 180, ra - 360, ra); return 21600.0 - 120.0 * ra
def row_of(dec): return 7559.5 + 120.0 * dec
from astropy.io import fits
from astropy.wcs import WCS
hdr = fits.Header.fromstring(open(os.path.join(ACT, f"header_{MAP}.fits"), "rb").read(2880).decode("ascii"))
tp = np.array([[12.3, -5.0], [133.7, 1.2], [200.1, -30.5], [355.2, 2.9]]); px = WCS(hdr).all_world2pix(tp, 0)
d3 = float(np.max(np.abs(np.c_[col_of(tp[:, 0]), row_of(tp[:, 1])] - px)))
check("K3_pixel_geometry", d3 < 0.01, f"max |d pix| {d3:.2e} vs astropy WCS")

# ------------------------------------------------------------ cosmology (native, as GH3) and gas model
H_NAT, OM = 0.679, 0.3085
def chi_flat(z, om=OM):
    zz = np.linspace(0, 1.0, 4001); E = np.sqrt(om * (1 + zz) ** 3 + 1 - om)
    ch = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]); return np.interp(z, zz, ch)
DH = 299792.458 / (100 * H_NAT)
def DA(z): return DH * chi_flat(z) / (1 + z)
ZT3 = np.array([[10.5, 178.0], [10.75, 210.0], [11.0, 295.0]])             # GH3's rows (K2 only)
ZTF = np.array([[9, 82.0], [9.5, 102.0], [10, 131.0], [10.5, 178.0], [10.75, 210.0], [11.0, 295.0], [11.25, 480.0], [11.5, 950.0]])
def Rvir_kpc(l, tab=ZTF): return np.interp(l, tab[:, 0], tab[:, 1])
BETA, RCK, NORM, TKEV, MUE = 0.43, 6.0, 1.84, 0.22, 1.14
SIGT, MEC2, MP, MSUN, KPC, KEV = 6.6524587e-29, 8.1871057e-14, 1.67262192e-27, 1.98847e30, 3.0856776e19, 1.602176634e-16
XE = np.array([0, 0.5, 1.0, 1.8, 3.0, 5.0, 8.0, 12.0, 20.0]); NA = len(XE) - 1; NC = NA - 1     # NC compensated annuli
XE3 = np.array([0, 0.5, 1.0, 1.8, 3.0, 5.0])
FWHM = 1.6; SB = FWHM / (2 * math.sqrt(2 * math.log(2)))
THMAX = 39.0 / 20.0                                                          # arcmin: 20 R_vir must fit inside 39'


def y_profile_kpc(Rk, l, k):
    Rv = Rvir_kpc(l); rcut = k * Rv
    rr = np.linspace(0, Rv, 20001); sh = (1 + (rr / RCK) ** 2) ** (-1.5 * BETA)
    rho0 = NORM * 10 ** l * MSUN / (np.trapz(4 * np.pi * rr ** 2 * sh, rr) * KPC ** 3); ne0 = rho0 / (MUE * MP)
    out = np.zeros_like(Rk, dtype=float)
    for i, R in enumerate(Rk):
        if R >= rcut: continue
        ll = np.linspace(0, math.sqrt(rcut ** 2 - R ** 2), 4001)
        out[i] = 2 * np.trapz((1 + (R * R + ll * ll) / RCK ** 2) ** (-1.5 * BETA), ll) * KPC
    return SIGT / MEC2 * TKEV * KEV * ne0 * out


_R, _rc = 30.0, 6.0; _ll = np.linspace(0, 3e5, 3_000_001)
k1n = 2 * np.trapz((1 + (_R ** 2 + _ll ** 2) / _rc ** 2) ** -1.0, _ll); k1c = math.pi * _rc ** 2 / math.sqrt(_rc ** 2 + _R ** 2)
check("K1_projection_closed_form", abs(k1n / k1c - 1) < 1e-4, f"{k1n / k1c - 1:+.1e}")
FG = 0.05


def model_annuli(z, l, k):
    """beam-convolved y averaged in the XE annuli (uncompensated, 8 values) for a (z, lm) cell."""
    da = DA(z) * 1e3; thv = Rvir_kpc(l) / da * 180 / math.pi * 60
    half = min(41.0, 21.0 * thv + 4 * FWHM); nf = int(half / FG)
    fx = (np.arange(2 * nf + 1) - nf) * FG; FXX, FYY = np.meshgrid(fx, fx); FTH = np.hypot(FXX, FYY)
    BK = np.exp(-0.5 * FTH ** 2 / SB ** 2); BK /= BK.sum()
    Rk = np.linspace(0, half * 1.5 * da * math.pi / 180 / 60, 900); yk = y_profile_kpc(Rk, l, k)
    img = np.interp(FTH * da * math.pi / 180 / 60, Rk, yk)
    conv = np.fft.irfft2(np.fft.rfft2(img) * np.fft.rfft2(np.fft.ifftshift(BK)), s=img.shape)
    idx = np.digitize(FTH / thv, XE) - 1; v = (idx >= 0) & (idx < NA)
    return np.bincount(idx[v], conv[v], NA) / np.bincount(idx[v], minlength=NA)


def comp(a): return a[..., :NC] - a[..., NC:NC + 1]                        # compensated aperture

# ------------------------------------------------------------ samples
if TIER == "kids":                                                          # K2 only: GH4's lenses, GH4's seed
    L = np.load(os.path.join(LRD, "lr_lenses.npz")); lm70, z, ra, dec = L["logM"], L["z"], L["ra"], L["dec"]
    m = (lm70 >= 10.6) & (lm70 <= 11.0); lm = lm70[m] + 2 * np.log10(0.70 / H_NAT) + 2 * np.log10(chi_flat(z[m], OM) / chi_flat(z[m], 0.3))
    z, ra, dec = z[m], ra[m], dec[m]; inm = (dec > -35.9) & (dec < 3.9); lm, z, ra, dec = lm[inm], z[inm], ra[inm], dec[inm]
else:
    D = np.load(os.path.join(EXT, "gh5_work", "gh5_lenses.npz")); c = D["cen"]
    frac = float(c.mean()); check("K4_central_fraction", 0.6 <= frac <= 0.8, f"{frac:.3f} (Zhang CEN 0.68)")
    ss = D["sfr"] - D["lm"]
    hi, ngc = D["comp"] > 0.8, (D["ra"] > 90) & (D["ra"] < 280)
    sel = dict(central=c, clean=D["clean"], iso3=D["iso"], comp08=c & hi, passive=c & (ss < -11), sf=c & (ss >= -11),
               # post-freeze diagnostics (no verdict weight): where does comp08's negative stack come from?
               diag_complo=c & ~hi, diag_ngc=c & ngc, diag_sgc=c & ~ngc, diag_hi_ngc=c & hi & ngc, diag_hi_sgc=c & hi & ~ngc, diag_hi_passive=c & hi & (ss < -11))[TIER]
    lm = D["lm"][sel] + 2 * np.log10(0.704 / H_NAT); z, ra, dec = D["z"][sel], D["ra"][sel], D["dec"][sel]
P(f"GH5  map {MAP}  tier {TIER}{' [MUTATE]' if MUT else ''}: {len(z)} lenses  [{time.time() - T0:.0f} s]")
rng = np.random.default_rng(SEED); NRAND = 3
rra = np.mod(np.repeat(ra, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND) / np.cos(np.radians(np.repeat(dec, NRAND))), 360)
rde = np.clip(np.repeat(dec, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), -35.85, 3.85)
if MUT:
    ra, dec = rra[::NRAND].copy(), rde[::NRAND].copy()
    rra = np.mod(np.repeat(ra, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), 360); rde = np.clip(np.repeat(dec, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), -35.85, 3.85)
rz, rlm = np.repeat(z, NRAND), np.repeat(lm, NRAND)


# ------------------------------------------------------------ stacking (Dec-chunked strip reads)
def stack_strip(ra_, dec_, z_, lm_, HW, xe, tab, CH=400, exact3=False):
    na = len(xe) - 1; res = np.full((len(ra_), na), np.nan); rows = np.round(row_of(dec_)).astype(int) - R0
    da = DA(z_) * 1e3; thv = Rvir_kpc(lm_, tab) / da * 180 / math.pi * 60; cf, rf = col_of(ra_), row_of(dec_)
    DD = np.arange(2 * HW + 1) - HW
    for s0 in range(0, NR, CH):
        sel = np.where((rows >= s0) & (rows < s0 + CH))[0]
        if not len(sel): continue
        a0, a1 = max(0, s0 - HW - 2), min(NR, s0 + CH + HW + 2)
        blk = np.fromfile(STRIP, dtype=">f4", count=(a1 - a0) * NX, offset=a0 * ROWB).reshape(a1 - a0, NX).astype(np.float32)
        for i in sel:
            c0, r0 = int(round(cf[i])), int(round(rf[i])); rr0 = r0 - HW - R0 - a0
            if rr0 < 0 or rr0 + 2 * HW + 1 > blk.shape[0]: continue
            cc = np.arange(c0 - HW, c0 + HW + 1)
            st = np.take(blk[rr0:rr0 + 2 * HW + 1], cc % NX, axis=1) if (cc[0] < 0 or cc[-1] >= NX) else blk[rr0:rr0 + 2 * HW + 1, cc[0]:cc[-1] + 1]
            if not np.all(np.isfinite(st)) or np.any(st == 0): continue
            dy = (r0 + DD[:, None] - rf[i]) / 2.0; dx = (c0 + DD[None, :] - cf[i]) / 2.0 * math.cos(math.radians(dec_[i]))
            idx = np.digitize(np.hypot(dx, dy) / thv[i], xe) - 1; v = (idx >= 0) & (idx < na)
            cnt = np.bincount(idx[v], minlength=na)
            if np.any(cnt == 0): continue
            res[i] = [st[idx == a].mean() for a in range(na)] if exact3 else np.bincount(idx[v], st[v], na) / cnt   # exact3: GH3's float32 means
        del blk
    return res


thL = Rvir_kpc(lm) / (DA(z) * 1e3) * 180 / math.pi * 60; thR = np.repeat(thL, NRAND)
AL = stack_strip(ra, dec, z, lm, 80, XE, ZTF); P(f"  lenses stacked [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
AR = stack_strip(rra, rde, rz, rlm, 80, XE, ZTF); P(f"  randoms stacked [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
okL = np.all(np.isfinite(AL), 1) & (thL <= THMAX); okR = np.all(np.isfinite(AR), 1) & (thR <= THMAX)
P(f"  valid: lenses {okL.sum()}/{len(okL)}, randoms {okR.sum()}/{len(okR)}")
NP_ = 50; edges = np.quantile(ra[okL], np.linspace(0, 1, NP_ + 1)); edges[0] -= 1; edges[-1] += 1
pl = np.clip(np.digitize(ra, edges) - 1, 0, NP_ - 1); prr = np.repeat(pl, NRAND)


def prof(XL, XR, mL, mR): return XL[mL & okL].mean(0) - XR[mR & okR].mean(0)
def prof_jk(XL, XR):
    v = prof(XL, XR, np.ones(len(ra), bool), np.ones(len(rra), bool))
    jk = np.array([prof(XL, XR, pl != p, prr != p) for p in range(NP_)]); d = jk - jk.mean(0)
    return v, (NP_ - 1) / NP_ * np.einsum("pi,pj->ij", d, d), jk


Yu, Cu, _ = prof_jk(AL, AR); Yc, Cc, JK = prof_jk(comp(AL), comp(AR))
Ci = np.linalg.inv(Cc) * (NP_ - NC - 2) / (NP_ - 1); err = np.sqrt(np.diag(Cc)); chi0 = float(Yc @ Ci @ Yc)
P(f"  annuli x {XE.tolist()}")
P(f"  uncompensated y (x1e8): {np.round(Yu * 1e8, 3).tolist()} +- {np.round(np.sqrt(np.diag(Cu)) * 1e8, 3).tolist()}")
P(f"  COMPENSATED y (x1e8): {np.round(Yc * 1e8, 3).tolist()} +- {np.round(err * 1e8, 3).tolist()}")
P(f"  null chi2: {chi0:.1f}/{NC} (p {stats.chi2.sf(chi0, NC):.3g})")
RES = {"map": MAP, "tier": TIER, "mutate": MUT, "n_lens": int(okL.sum()), "n_rand": int(okR.sum()), "annuli_x": XE.tolist(), "Y_uncomp": Yu.tolist(),
       "Y_comp": Yc.tolist(), "err_comp": err.tolist(), "null_chi2": chi0}
if MUT:
    check("MUTATE_random_lenses_null", stats.chi2.sf(chi0, NC) > 0.01, f"p {stats.chi2.sf(chi0, NC):.3f}")
    gc = json.load(open(os.path.join(HERE, f"gh5_results_{MAP}_{TIER}.json")))["fits"]; nf = {}
    for k_ in ("1.0", "1.8", "3.0"):
        mc = np.array(gc[k_]["model"]); r = Yc - mc; F = float(mc @ Ci @ mc); nf[k_] = dict(A=float(mc @ Ci @ Yc) / F, sA=1 / math.sqrt(F), chi2=float(r @ Ci @ r))
    RES["null_fits"] = nf; RES["null_dchi2"] = nf["1.0"]["chi2"] - nf["3.0"]["chi2"]
    P(f"  null stack on the real tier's models: A(k=3) {nf['3.0']['A']:.2f}+-{nf['3.0']['sA']:.2f}, A(k=1) {nf['1.0']['A']:.2f}+-{nf['1.0']['sA']:.2f}, dchi2 k1-k3 {RES['null_dchi2']:+.1f}")
elif TIER == "kids":
    g4 = json.load(open(os.path.join(REB, "GH4_tsz_two_halo_compensated", f"gh4_results_{MAP}_b34.json")))
    k2 = float(np.max(np.abs(Yc / np.array(g4["Y_comp"]) - 1))); check("K2_reproduces_GH4", k2 < 1e-6, f"max rel diff {k2:.1e}, {okL.sum()} vs {g4['n_lens']} lenses")
else:
    zg = np.round(np.clip(z[okL], 0.1, 0.5) / 0.025) * 0.025; lg = np.round(lm[okL] / 0.1) * 0.1
    cells, inv = np.unique(np.c_[zg, lg], axis=0, return_inverse=True); wcell = np.bincount(inv.ravel(), minlength=len(cells))
    fits_ = {}
    for k in (1.0, 1.8, 3.0):
        M = np.array([model_annuli(zc, lc, k) for zc, lc in cells]); mc = comp((M * wcell[:, None]).sum(0) / wcell.sum())
        r = Yc - mc; c2 = float(r @ Ci @ r); F = float(mc @ Ci @ mc); A = float(mc @ Ci @ Yc) / F; rA = Yc - A * mc; c2A = float(rA @ Ci @ rA)
        fits_[k] = dict(model=mc.tolist(), chi2=c2, p=float(stats.chi2.sf(c2, NC)), A=A, sA=1 / math.sqrt(F), chi2_A=c2A, p_A=float(stats.chi2.sf(c2A, NC - 1)),
                        A_jk=[float(mc @ Ci @ j) / F for j in JK])
        P(f"  k = {k}: model (x1e8) {np.round(mc * 1e8, 3).tolist()}; chi2 {c2:.1f} (p {fits_[k]['p']:.3g}); free A {A:.2f}+-{1 / math.sqrt(F):.2f}, chi2 {c2A:.1f} (p {fits_[k]['p_A']:.3g})  [{time.time() - T0:.0f} s]")
    c1, c3 = fits_[1.0], fits_[3.0]
    if c3["chi2"] < c1["chi2"] - 4 and c3["p"] > 0.01: V = "EXTENDED GAS PREFERRED"
    elif c1["chi2"] < c3["chi2"] - 4 and c1["p"] > 0.01: V = "MEASURED EXTENT PREFERRED"
    elif all(f["p"] < 0.01 for f in fits_.values()): V = "NEITHER FITS"
    else: V = "NOT DECIDED"
    RES.update(fits={str(k): v for k, v in fits_.items()}, verdict=V, dchi2=c1["chi2"] - c3["chi2"], ra_edges=edges.tolist()); P(f"\n=== VERDICT [{MAP}, {TIER}]: {V} (dchi2 k1-k3 {RES['dchi2']:+.1f})")
RES["checks"] = CHK; n = sum(CHK.values()); P(f"checks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"gh5_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"gh5{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)

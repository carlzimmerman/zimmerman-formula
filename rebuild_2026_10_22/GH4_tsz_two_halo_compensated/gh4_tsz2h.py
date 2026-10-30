#!/usr/bin/env python3
"""GH4_tsz_two_halo_compensated: GH3's ACT DR6.02 NILC y stack on the KiDS isolated lenses, upgraded with a compensated
aperture (mean y in 12-20 R_vir subtracted per lens) and an empirical two-halo template (excess of massive KiDS-bright
neighbours, amplitude b >= 0 free). Frozen criteria: FROZEN_CRITERIA.md (f5c49ae6a7). One thread; strip read in chunks.
kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed; nothing here says the data favour the framework.
    GH4_MAP=ComptonY_deproj_cib_1.0_10.7|ComptonY  GH4_SAMPLE=b34|b12  [GH4_MUTATE=1]
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh4_tsz2h.py
"""
import os, sys, json, math, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy import stats
from scipy.spatial import cKDTree
T0 = time.time()
MAP = os.environ.get("GH4_MAP", "ComptonY_deproj_cib_1.0_10.7"); SAMPLE = os.environ.get("GH4_SAMPLE", "b34")
MUT = os.environ.get("GH4_MUTATE") == "1"
TAG = f"_{MAP}_{SAMPLE}" + ("_MUTATE" if MUT else "")
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

# ------------------------------------------------------------ samples (GH3 selection; same random draws)
L = np.load(os.path.join(LRD, "lr_lenses.npz"))
lm70, z, ra, dec = L["logM"], L["z"], L["ra"], L["dec"]
m = (lm70 >= 10.6) & (lm70 <= 11.0) if SAMPLE == "b34" else (lm70 >= 8.5) & (lm70 < 10.6)
qDA = chi_flat(z[m], OM) / chi_flat(z[m], 0.3)
lm = lm70[m] + 2 * np.log10(0.70 / H_NAT) + 2 * np.log10(qDA); z, ra, dec, l70 = z[m], ra[m], dec[m], lm70[m]
inmap = (dec > -35.9) & (dec < 3.9)
lm, z, ra, dec, l70 = lm[inmap], z[inmap], ra[inmap], dec[inmap], l70[inmap]
P(f"GH4  criteria f5c49ae6a7  map {MAP}  sample {SAMPLE}{' [MUTATE]' if MUT else ''}: {len(z)} lenses in the strip  [{time.time() - T0:.0f} s]")
rng = np.random.default_rng(303); NRAND = 3
rra = np.repeat(ra, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND) / np.cos(np.radians(np.repeat(dec, NRAND)))
rde = np.clip(np.repeat(dec, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), -35.85, 3.85)
rra = np.mod(rra, 360)
if MUT:
    ra, dec = rra[::NRAND].copy(), rde[::NRAND].copy()
    rra = np.mod(np.repeat(ra, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), 360); rde = np.clip(np.repeat(dec, NRAND) + rng.uniform(-0.5, 0.5, len(ra) * NRAND), -35.85, 3.85)
rz, rlm, rl70 = np.repeat(z, NRAND), np.repeat(lm, NRAND), np.repeat(l70, NRAND)


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


# K2: GH3's stamp, annuli and validity rule reproduce GH3's committed Y (bins 3-4 only; same lenses and randoms)
if SAMPLE == "b34" and not MUT:
    g3 = json.load(open(os.path.join(REB, "GH3_tsz_cgm_extent", f"gh3_results_{MAP}_kids.json")))
    A3 = stack_strip(ra, dec, z, lm, 24, XE3, ZT3, exact3=True); B3 = stack_strip(rra, rde, rz, rlm, 24, XE3, ZT3, exact3=True)
    Y3 = A3[np.all(np.isfinite(A3), 1)].mean(0) - B3[np.all(np.isfinite(B3), 1)].mean(0)
    k2 = float(np.max(np.abs(Y3 / np.array(g3["Y"]) - 1)))
    check("K2_reproduces_GH3", k2 < 1e-6, f"max rel diff {k2:.1e} vs GH3 committed Y ({g3['n_lens']} lenses)")
    del A3, B3

thL = Rvir_kpc(lm) / (DA(z) * 1e3) * 180 / math.pi * 60; thR = np.repeat(thL, NRAND)
AL = stack_strip(ra, dec, z, lm, 80, XE, ZTF); P(f"  lenses stacked (+-40') [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
AR = stack_strip(rra, rde, rz, rlm, 80, XE, ZTF); P(f"  randoms stacked [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
okL = np.all(np.isfinite(AL), 1) & (thL <= THMAX); okR = np.all(np.isfinite(AR), 1) & (thR <= THMAX)
P(f"  valid: lenses {okL.sum()}/{len(okL)}, randoms {okR.sum()}/{len(okR)} (20 R_vir inside 39': drops {int((thL > THMAX).sum())} lenses)")

# ------------------------------------------------------------ two-halo template (massive KiDS-bright neighbours)
bs = fits.open(os.path.join(LRD, "KiDS_DR4_brightsample.fits"))[1].data; bl = fits.open(os.path.join(LRD, "KiDS_DR4_brightsample_LePhare.fits"))[1].data
assert np.all(bs["ID"] == bl["ID"])
gm = (bs["masked"] == 0) & (bl["MASS_MED"] > 0)
gra, gde, gz, gM = [np.asarray(a, float)[gm] for a in (bs["RAJ2000"], bs["DECJ2000"], bs["zphot_ANNz2"], bl["MASS_MED"])]
del bs, bl
def uvec(r, d): r, d = np.radians(r), np.radians(d); return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]
TREE = cKDTree(uvec(gra, gde)); RCH = 2 * math.sin(math.radians(40.5 / 60) / 2)
AREA = np.pi * (XE[1:] ** 2 - XE[:-1] ** 2)
P(f"  bright tracer: {gm.sum()} galaxies (masked == 0, MASS_MED > 0)  [{time.time() - T0:.0f} s]")


def tmpl_counts(ra_, dec_, z_, l70_, th_):
    """per-object neighbour surface density in x annuli: number-weighted and (M_nb/M_lens)^(5/3)-weighted."""
    Tn = np.zeros((len(ra_), NA)); Tm = np.zeros((len(ra_), NA)); U = uvec(ra_, dec_)
    for c0 in range(0, len(ra_), 4000):
        nb = TREE.query_ball_point(U[c0:c0 + 4000], RCH)
        for j, lst in enumerate(nb):
            i = c0 + j
            if not lst: continue
            lst = np.asarray(lst); cut = (np.abs(gz[lst] - z_[i]) < 0.06) & (gM[lst] > l70_[i] - 1.0); lst = lst[cut]
            if not len(lst): continue
            ch = np.linalg.norm(uvec(gra[lst], gde[lst]) - U[i], axis=1); sep = 2 * np.degrees(np.arcsin(ch / 2)) * 60
            keep = sep > 2.0 / 60; sep, lw = sep[keep], gM[lst][keep] - l70_[i]
            idx = np.digitize(sep / th_[i], XE) - 1; v = (idx >= 0) & (idx < NA)
            Tn[i] = np.bincount(idx[v], minlength=NA) / AREA; Tm[i] = np.bincount(idx[v], 10 ** (5 / 3 * lw[v]), NA) / AREA
    return Tn, Tm


TnL, TmL = tmpl_counts(ra, dec, z, l70, thL); TnR, TmR = tmpl_counts(rra, rde, rz, rl70, thR)
P(f"  template counted [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

NP_ = 50; edges = np.quantile(ra[okL], np.linspace(0, 1, NP_ + 1)); edges[0] -= 1; edges[-1] += 1
pl = np.clip(np.digitize(ra, edges) - 1, 0, NP_ - 1); prr = np.repeat(pl, NRAND)


def prof(XL, XR, mL, mR): return XL[mL & okL].mean(0) - XR[mR & okR].mean(0)
def prof_jk(XL, XR):
    v = prof(XL, XR, np.ones(len(ra), bool), np.ones(len(rra), bool))
    jk = np.array([prof(XL, XR, pl != p, prr != p) for p in range(NP_)])
    return v, (NP_ - 1) / NP_ * (jk - jk.mean(0)).T @ (jk - jk.mean(0))


Yu, Cu = prof_jk(AL, AR); Yc, Cc = prof_jk(comp(AL), comp(AR))
Tn, CTn = prof_jk(comp(TnL), comp(TnR)); Tm, _ = prof_jk(comp(TmL), comp(TmR)); Tnu, CTnu = prof_jk(TnL, TnR)
Ci = np.linalg.inv(Cc) * (NP_ - NC - 2) / (NP_ - 1); err = np.sqrt(np.diag(Cc))
P(f"  annuli x {XE.tolist()}")
P(f"  uncompensated y (x1e8): {np.round(Yu * 1e8, 3).tolist()} +- {np.round(np.sqrt(np.diag(Cu)) * 1e8, 3).tolist()}")
P(f"  COMPENSATED y (x1e8, minus [12,20)): {np.round(Yc * 1e8, 3).tolist()} +- {np.round(err * 1e8, 3).tolist()}")
P(f"  neighbour excess T_n uncompensated (per x^2): {np.round(Tnu, 4).tolist()} +- {np.round(np.sqrt(np.diag(CTnu)), 4).tolist()}")
P(f"  template T_n compensated: {np.round(Tn, 4).tolist()}; T_m compensated: {np.round(Tm, 4).tolist()}")
chi0 = float(Yc @ Ci @ Yc); P(f"  null chi2 (compensated y = 0): {chi0:.1f}/{NC} (p {stats.chi2.sf(chi0, NC):.3g})")
RES = {"criteria": "f5c49ae6a7", "map": MAP, "sample": SAMPLE, "mutate": MUT, "n_lens": int(okL.sum()), "n_rand": int(okR.sum()),
       "annuli_x": XE.tolist(), "Y_uncomp": Yu.tolist(), "err_uncomp": np.sqrt(np.diag(Cu)).tolist(), "Y_comp": Yc.tolist(),
       "err_comp": err.tolist(), "T_n": Tn.tolist(), "T_m": Tm.tolist(), "T_n_uncomp": Tnu.tolist(), "null_chi2": chi0}


def fit(Y, mod, T, freeA=False):
    """chi2 of Y - A*mod - b*T with b >= 0 (A = 1 unless freeA). Returns dict."""
    if not freeA:
        r0 = Y - mod
        b = max(0.0, float(T @ Ci @ r0 / (T @ Ci @ T))) if T is not None else 0.0
        r = r0 - (b * T if T is not None else 0); c2 = float(r @ Ci @ r); dof = NC - (1 if T is not None else 0)
        return dict(b=b, chi2=c2, p=float(stats.chi2.sf(c2, dof)), dof=dof)
    X = np.c_[mod, T]; F = X.T @ Ci @ X; th = np.linalg.solve(F, X.T @ Ci @ Y)
    if th[1] < 0:
        A = float(mod @ Ci @ Y / (mod @ Ci @ mod)); th = np.array([A, 0.0]); sA = 1 / math.sqrt(mod @ Ci @ mod)
    else: sA = math.sqrt(np.linalg.inv(F)[0, 0])
    r = Y - X @ th; c2 = float(r @ Ci @ r)
    return dict(A=float(th[0]), sA=float(sA), b=float(th[1]), chi2=c2, p=float(stats.chi2.sf(c2, NC - 2)))


if MUT:
    check("MUTATE_random_lenses_null", stats.chi2.sf(chi0, NC) > 0.01, f"p {stats.chi2.sf(chi0, NC):.3f}")
    sT = np.sqrt(np.diag(CTn)); k4 = float(np.max(np.abs(Tn) / sT))
    check("K4_template_on_randoms_null", k4 < 3, f"max |T_n|/sigma {k4:.2f} (compensated, random-as-lens)")
elif SAMPLE == "b12":
    f = fit(Yc, np.zeros(NC), Tn); RES["fit_2h_only"] = f
    P(f"  bins 1-2 (no gas model): y = b T_n: b {f['b']:.3e}, chi2 {f['chi2']:.1f}/{f['dof']} (p {f['p']:.3g})")
else:
    zg = np.round(np.clip(z[okL], 0.1, 0.5) / 0.025) * 0.025; lg = np.round(lm[okL] / 0.1) * 0.1
    cells, inv = np.unique(np.c_[zg, lg], axis=0, return_inverse=True); wcell = np.bincount(inv.ravel(), minlength=len(cells))
    fits_ = {}
    for k in (1.0, 1.8, 3.0):
        M = np.array([model_annuli(zc, lc, k) for zc, lc in cells]); mu = (M * wcell[:, None]).sum(0) / wcell.sum(); mc = comp(mu)
        fp, f0, fm, fA = fit(Yc, mc, Tn), fit(Yc, mc, None), fit(Yc, mc, Tm), fit(Yc, mc, Tn, True)
        fits_[k] = dict(model_uncomp=mu.tolist(), model_comp=mc.tolist(), primary=fp, b0=f0, Tm=fm, freeA=fA)
        P(f"  k = {k}: model comp (x1e8) {np.round(mc * 1e8, 3).tolist()}")
        P(f"      PRIMARY (A=1, b>=0 T_n): chi2 {fp['chi2']:.1f}/{fp['dof']} (p {fp['p']:.3g}), b {fp['b']:.2e} | b=0: {f0['chi2']:.1f} (p {f0['p']:.3g}) | T_m: {fm['chi2']:.1f} | free A {fA['A']:.2f}+-{fA['sA']:.2f}, b {fA['b']:.2e}, chi2 {fA['chi2']:.1f}  [{time.time() - T0:.0f} s]")
    def verdict(key):
        c1, c3 = fits_[1.0][key], fits_[3.0][key]
        if c3["chi2"] < c1["chi2"] - 4 and c3["p"] > 0.01: return "EXTENDED GAS PREFERRED"
        if c1["chi2"] < c3["chi2"] - 4 and c1["p"] > 0.01: return "MEASURED EXTENT PREFERRED"
        if all(fits_[k][key]["p"] < 0.01 for k in fits_): return "NEITHER FITS"
        return "NOT DECIDED"
    V = verdict("primary"); Vs = {kk: verdict(kk) for kk in ("b0", "Tm")}
    RES.update(fits={str(k): v for k, v in fits_.items()}, verdict=V, verdict_b0=Vs["b0"], verdict_Tm=Vs["Tm"],
               dchi2_k1_minus_k3=fits_[1.0]["primary"]["chi2"] - fits_[3.0]["primary"]["chi2"])
    P(f"\n=== VERDICT [{MAP}, {SAMPLE}]: {V}  (dchi2 k1-k3 {RES['dchi2_k1_minus_k3']:+.1f}; b=0: {Vs['b0']}; T_m: {Vs['Tm']})")
RES["checks"] = CHK; n = sum(CHK.values()); P(f"checks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"gh4_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"gh4{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)

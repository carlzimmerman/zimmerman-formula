#!/usr/bin/env python3
"""CFG228 Stage 1 -- VELOCITY-FREE measurements from the ALMA products: [CII] flux, continuum flux, sizes, the two tracers' gas masses, d_AB, the class rule, and the static input table.
ALPINE: six [CII] rotators (PI moment-0 map, continuum image, primary-beam maps, own-cube integration as a cross-check).  SPT0418-47: the authors' de-lensed L_[CII] and mu, our image-plane dust continuum
and image-plane [CII] (spw27 + spw25) as a differential-lensing check.  NO velocity is fitted here (the integrated-spectrum peak is only a systemic-velocity starting value for Stage 3).
Compilation; two un-optimised tracers; calibration-limited; not a detection; not a verdict.  LambdaCDM has no a0.  kappa = 1/2 FITTED.
Frozen criteria: FROZEN_CRITERIA.md here (71ec12282), committed before any pixel value was read.
Run: python3 campaign_fresh_gravity/CFG228_alma_cubes/cfg228_stage1.py        (MUTATE=4: every flux x 2)"""
import os, sys, math, json, glob, time, hashlib
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from scipy.integrate import quad
from scipy.signal import convolve2d

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MODE = os.environ.pop("MUTATE", "").strip()
TAG = "_MUTATE4" if MODE == "4" else ""
EXT = os.path.expanduser("~/new_physics/_external_data")
AL, SP = os.path.join(EXT, "alpine_alma"), os.path.join(EXT, "spt0418_alma")
DA = os.path.join(REPO, "data_assembly")
OUT, CHK = [], []
T0 = time.time()
SEED = 228
OM, H0 = 0.315, 67.4
CLIGHT = 299792.458
NU_CII = 1900.5369e9
HP, KB, CSI = 6.62607015e-34, 1.380649e-23, 2.99792458e8
FLUXMUT = 2.0 if MODE == "4" else 1.0


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def dl_mpc(zz):
    dc = CLIGHT / H0 * quad(lambda x: 1 / math.sqrt(OM * (1 + x) ** 3 + 1 - OM), 0, zz)[0]
    return dc * (1 + zz)


def kpc_per_arcsec(zz):
    dc = CLIGHT / H0 * quad(lambda x: 1 / math.sqrt(OM * (1 + x) ** 3 + 1 - OM), 0, zz)[0]
    return dc / (1 + zz) * 1e3 * math.pi / 648000.0


def L_line(S_jykms, nu_obs_ghz, dl):                                    # Solomon+92 form: L = 1.04e-3 S dv nu_obs D_L^2  [Lsun]
    return 1.04e-3 * S_jykms * nu_obs_ghz * dl ** 2


def planck(nu, T):
    return 2 * HP * nu ** 3 / CSI ** 2 / np.expm1(HP * nu / (KB * T))


def gas_from_dust(S_jy, nu_obs, zz, Td, beta=1.8, alpha850=6.9e12, cmb=True):
    """log10 M_gas [Msun] from the observed flux density: CMB contrast, modified black body to rest 850 micron, L_850 / alpha_850 (Dunne+22 Table 7 single-band factor incl. He)"""
    dlm = dl_mpc(zz) * 3.0856775814913673e22
    nu_r = nu_obs * (1 + zz)
    Lnu = 4 * math.pi * dlm ** 2 * S_jy * 1e-26 / (1 + zz)
    if cmb:
        Lnu = Lnu / (1 - planck(nu_r, 2.725 * (1 + zz)) / planck(nu_r, Td))
    nu850 = CSI / 850e-6
    L850 = Lnu * (nu850 / nu_r) ** beta * planck(nu850, Td) / planck(nu_r, Td)
    return math.log10(L850 / alpha850)


def img2d(fn):
    d = fits.getdata(fn)
    return np.squeeze(d).astype(float)


def beam_pix(h):
    om_b = math.pi / (4 * math.log(2)) * h["BMAJ"] * h["BMIN"]
    return om_b / abs(h["CDELT1"]) ** 2


def circ_mask(shape, cy, cx, r):
    yy, xx = np.indices(shape)
    return (yy - cy) ** 2 + (xx - cx) ** 2 <= r ** 2


def growth(im, cy, cx, rs_pix, nbeam):
    return np.array([np.nansum(im[circ_mask(im.shape, cy, cx, r)]) / nbeam for r in rs_pix])


def random_apertures(im, pb, cy, cx, rpix, n, rng, min_sep_pix, nbeam):
    vals, tries = [], 0
    ny, nx = im.shape
    while len(vals) < n and tries < 20000:
        tries += 1
        y, x = rng.uniform(rpix + 1, ny - rpix - 1), rng.uniform(rpix + 1, nx - rpix - 1)
        if math.hypot(y - cy, x - cx) < min_sep_pix or not (pb[int(y), int(x)] > 0.5):
            continue
        m = circ_mask(im.shape, y, x, rpix)
        if np.isnan(im[m]).any():
            continue
        vals.append(np.nansum(im[m]) / nbeam)
    return np.array(vals)


P(__doc__.split("Run:")[0].strip())
P(f"MUTATE = {MODE or 'none'}{' (every flux x 2)' if MODE == '4' else ''}")
COR = pd.read_csv(os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_galaxies.csv")).set_index("galaxy")
RNG = pd.read_csv(os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_rings.csv"))
GAL = {"CG32": "CANDELS_GOODSS_32", "DC396844": "DEIMOS_COSMOS_396844", "DC494057": "DEIMOS_COSMOS_494057", "DC552206": "DEIMOS_COSMOS_552206", "DC881725": "DEIMOS_COSMOS_881725", "VC5110377875": "vuds_cosmos_5110377875"}
RADS = np.arange(0.5, 4.0001, 0.25)
ROWS = []
P("\nALPINE (PI moment-0 map and continuum image, pb-corrected; aperture flux = growth-curve plateau; noise = 200 random apertures)")
P("  galaxy          z    nu_obs  beam (arcsec)  r_ap  S_CII (Jy km/s)  S/N   R_half(arcsec)   L_CII (Lsun)   logM[CII](a=30)   S_cont (mJy)  S/N  logM_dust T=25/35/45      d_AB")
for gname, tag in GAL.items():
    f = lambda kind: glob.glob(os.path.join(AL, f"*{tag}.{kind}"))[0]
    hm = fits.getheader(f("CIImom0.image.fits"))
    m0 = img2d(f("CIImom0.image.fits"))
    pbc = img2d(f("continuum.flux.fits.gz"))                                          # 0-1 primary-beam response (the moment-0 "flux" file is a weight map, max 425-625)
    pbm = pbc
    cont = img2d(f("continuum.image.fits"))
    hc = fits.getheader(f("continuum.image.fits"))
    nb = beam_pix(hm); pix = abs(hm["CDELT1"]) * 3600.0
    z = float(COR.loc[gname, "redshift"]); dl = dl_mpc(z); kpa = kpc_per_arcsec(z)
    nu_obs = hm["RESTFRQ"] / 1e9
    m0c = np.where(pbm > 0.3, m0 / pbm, np.nan) * FLUXMUT
    # centre: peak of the 3x3-boxcar-smoothed moment-0 within 3 arcsec of the map centre
    k = np.ones((3, 3)) / 9.0
    sm = convolve2d(np.nan_to_num(m0c), k, mode="same")
    ny, nx = m0c.shape
    cy0, cx0 = (ny - 1) / 2.0, (nx - 1) / 2.0
    win = circ_mask(m0c.shape, cy0, cx0, 3.0 / pix)
    iy, ix = np.unravel_index(np.argmax(np.where(win, sm, -np.inf)), sm.shape)
    g = growth(m0c, iy, ix, RADS / pix, nb)
    gmax = np.nanmax(g); r_ad = float(RADS[np.argmax(g >= 0.95 * gmax)])
    S = float(g[np.where(RADS == r_ad)[0][0]])
    rng = np.random.default_rng(SEED)
    rv = random_apertures(m0c, pbm, iy, ix, r_ad / pix, 200, rng, 6.0 / pix, nb)
    sS = float(np.std(rv))
    r_half = float(np.interp(0.5 * S, g, RADS)) if g[-1] > 0.5 * S else float("nan")
    Lc = L_line(S, nu_obs, dl); Mc = 30.0 * Lc
    # continuum in the same aperture
    cc = np.where(pbc > 0.3, cont / pbc, np.nan) * FLUXMUT
    nbc = beam_pix(hc)
    Sc = float(np.nansum(cc[circ_mask(cc.shape, iy, ix, r_ad / pix)]) / nbc)
    rc = random_apertures(cc, pbc, iy, ix, r_ad / pix, 200, np.random.default_rng(SEED + 1), 6.0 / pix, nbc)
    sC = float(np.std(rc)); det = Sc / sC >= 3.0
    nu_c = hc["CRVAL3"]
    Sc_use = Sc if det else 3 * sC
    Md = {T: gas_from_dust(Sc_use, nu_c, z, T) for T in (25.0, 35.0, 45.0)}
    dAB = math.log10(Mc) - Md[35.0] if det else float("nan")
    # own-cube integrated spectrum (cross-check) and the systemic-velocity starting value
    hcb = fits.getheader(f("cube.image.fits"))
    cube = fits.getdata(f("cube.image.fits")).astype(np.float32)[0]
    cube = cube / np.where(pbm > 0.3, pbm, np.nan).astype(np.float32)[None]
    n3 = cube.shape[0]
    nu_ax = hcb["CRVAL3"] + (np.arange(1, n3 + 1) - hcb["CRPIX3"]) * hcb["CDELT3"]
    vel = CLIGHT * (hcb["RESTFRQ"] - nu_ax) / hcb["RESTFRQ"]
    mk = circ_mask(cube.shape[1:], iy, ix, r_ad / pix)
    spec = np.array([np.nansum(cube[i][mk]) for i in range(n3)]) / nb
    sm_spec = np.convolve(spec, np.ones(5) / 5, mode="same")
    i_pk = int(np.argmax(np.where(np.abs(vel) < 1500, sm_spec, -np.inf)))
    v_pk = float(vel[i_pk])
    free = np.abs(vel - v_pk) > 1000
    base, sig_ch = float(np.median(spec[free])), float(np.std(spec[free]))
    sp = spec - base
    lo = hi = i_pk
    sm5 = np.convolve(sp, np.ones(3) / 3, mode="same")
    while lo > 0 and sm5[lo - 1] > 2 * sig_ch / math.sqrt(3): lo -= 1
    while hi < n3 - 1 and sm5[hi + 1] > 2 * sig_ch / math.sqrt(3): hi += 1
    dv = abs(CLIGHT * hcb["CDELT3"] / hcb["RESTFRQ"])
    S_cube = float(np.sum(sp[lo:hi + 1]) * dv * FLUXMUT); sS_cube = float(sig_ch * math.sqrt(hi - lo + 1) * dv * FLUXMUT)
    R_dec = float("nan"); resolved = False
    hw = 0.5 * math.sqrt(hm["BMAJ"] * hm["BMIN"]) * 3600.0
    if math.isfinite(r_half) and r_half > hw:
        R_dec = math.sqrt(r_half ** 2 - hw ** 2); resolved = True
    else:
        R_dec = 0.5 * hw
    ROWS.append(dict(gid=gname, cube_tag=tag, z=z, dl_mpc=dl, kpc_per_arcsec=kpa, nu_obs_ghz=nu_obs, beam_maj=hm["BMAJ"] * 3600, beam_min=hm["BMIN"] * 3600, beam_pa=hm["BPA"], pix_arcsec=pix, N_beam=nb,
                     cy=int(iy), cx=int(ix), r_ap_arcsec=r_ad, S_CII=S, sS_CII=sS, S_CII_cube=S_cube, sS_CII_cube=sS_cube, v_peak_kms=v_pk, line_chan_lo=int(lo), line_chan_hi=int(hi), R_half_arcsec=r_half, R_dec_arcsec=R_dec, resolved=resolved,
                     L_CII=Lc, logM_CII=math.log10(Mc), S_cont_mJy=Sc * 1e3, sS_cont_mJy=sC * 1e3, cont_SN=Sc / sC, cont_det=bool(det), nu_cont_ghz=nu_c / 1e9, logMd25=Md[25.0], logMd35=Md[35.0], logMd45=Md[45.0], d_AB=dAB,
                     logMstar=float(COR.loc[gname, "log_mstar_msun"]), sfr=float(COR.loc[gname, "sfr_msun_yr"]), inc_kin=float(COR.loc[gname, "inc_kin_deg"]), e_inc_kin=float(COR.loc[gname, "e_inc_kin_deg"]), pa_kin=float(COR.loc[gname, "pa_kin_deg"]),
                     inc_morph=float(COR.loc[gname, "inc_morph_deg"]), e_inc_morph=float(COR.loc[gname, "e_inc_morph_deg"])))
    P(f"  {gname:13s} {z:.4f}  {nu_obs:6.2f}  {hm['BMAJ'] * 3600:.2f}x{hm['BMIN'] * 3600:.2f}  {r_ad:4.2f}  {S:7.3f}+-{sS:5.3f}   {S / sS:5.1f}  {r_half:6.2f}        {Lc:.3e}      {math.log10(Mc):6.2f}         {Sc * 1e3:7.3f}+-{sC * 1e3:5.3f} {Sc / sC:5.1f}  {Md[25.0]:5.2f}/{Md[35.0]:5.2f}/{Md[45.0]:5.2f}   {dAB:+6.2f}")
    P(f"      own-cube [CII] flux {S_cube:.3f}+-{sS_cube:.3f} Jy km/s (channels {lo}-{hi}, dv {dv:.1f} km/s; ratio to the moment-0 flux {S_cube / S:.2f}); integrated-spectrum peak v = {v_pk:+.0f} km/s relative to RESTFRQ; R_half {r_half:.2f}\", beam HWHM {hw:.2f}\" -> R_e,dec {R_dec:.2f}\" = {R_dec * kpa:.2f} kpc{'' if resolved else ' (UNRESOLVED: 0.5 x the beam HWHM)'}")
AL_DF = pd.DataFrame(ROWS)

# ------------------------------------------------------------------ SPT0418-47
P("\nSPT0418-47 (the authors' lens model; no lens modelling here)")
zS = 4.2248
dlS = dl_mpc(zS); kpaS = kpc_per_arcsec(zS)
fc = os.path.join(SP, "member.uid___A001_X87a_X837.ari_l.SPT0418-47_sci.spw25_27_29_31_357701MHz.12m.cont.I.pbcor.fits")
fp = os.path.join(SP, "member.uid___A001_X87a_X837.ari_l.SPT0418-47_sci.spw25_27_29_31_357701MHz.12m.cont.I.pb.fits.gz")
hS = fits.getheader(fc)
imS = np.squeeze(fits.getdata(fc)).astype(float) * FLUXMUT
pbS = np.squeeze(fits.getdata(fp)).astype(float)
pixS = abs(hS["CDELT1"]) * 3600.0; nbS = beam_pix(hS)
cyS, cxS = hS["CRPIX2"] - 1, hS["CRPIX1"] - 1
rS = 2.2 / pixS
SCs = float(np.nansum(imS[circ_mask(imS.shape, cyS, cxS, rS)]) / nbS)
# random apertures in the 4-10 arcsec annulus, pb > 0.5
rngS = np.random.default_rng(SEED + 2)
vals = []
yy0, xx0 = np.indices(imS.shape)
rad = np.hypot(yy0 - cyS, xx0 - cxS) * pixS
tries = 0
while len(vals) < 200 and tries < 50000:
    tries += 1
    ang, rr = rngS.uniform(0, 2 * math.pi), rngS.uniform(4.5 / pixS, 8.5 / pixS)
    y, x = cyS + rr * math.sin(ang), cxS + rr * math.cos(ang)
    if not (rS < y < imS.shape[0] - rS and rS < x < imS.shape[1] - rS) or not (pbS[int(y), int(x)] > 0.5):
        continue
    mm = circ_mask(imS.shape, y, x, rS)
    vals.append(np.nansum(imS[mm]) / nbS)
sCs = float(np.std(vals))
nuS = hS["CRVAL3"]
mu, e_mu = 32.3, 2.5
S_int = SCs / mu
Md_S = {T: gas_from_dust(S_int, nuS, zS, T) for T in (25.0, 35.0, 45.0)}
L_pub = 1.8e9
M_CII_S = 30.0 * L_pub
d_S = math.log10(M_CII_S) - Md_S[35.0]
P(f"  dust: collapsed 357.7 GHz image, aperture 2.2 arcsec around the ring centre: S = {SCs * 1e3:.2f} +- {sCs * 1e3:.2f} mJy (S/N {SCs / sCs:.1f}; nu_obs {nuS / 1e9:.2f} GHz = rest {nuS * (1 + zS) / 1e12:.3f} THz, {CSI / (nuS * (1 + zS)) * 1e6:.1f} micron); de-lensed by mu = 32.3: {S_int * 1e3:.3f} mJy")
P(f"  gas: [CII] (published de-lensed L_[CII] 1.8e9 Lsun, alpha 30) log M = {math.log10(M_CII_S):.2f}; dust (T_d 25 / 35 / 45 K) log M = {Md_S[25.0]:.2f} / {Md_S[35.0]:.2f} / {Md_S[45.0]:.2f}; d_AB(35 K) = {d_S:+.2f}")
# image-plane [CII]: spw27 + spw25 cubes, central 2.2 arcsec aperture, baseline from line-free channels
def sub_cube(fn, half=130):
    hh = fits.getheader(fn)
    cy, cx = int(round(hh["CRPIX2"] - 1)), int(round(hh["CRPIX1"] - 1))
    with fits.open(fn, memmap=True) as hl:
        d = hl[0].data[0, :, cy - half:cy + half + 1, cx - half:cx + half + 1].astype(np.float32)
    n3 = hh["NAXIS3"]
    nu = hh["CRVAL3"] + (np.arange(1, n3 + 1) - hh["CRPIX3"]) * hh["CDELT3"]
    return d, nu, hh, (half, half)


def spec_of(fn):
    d, nu, hh, (cy, cx) = sub_cube(fn)
    mk = circ_mask(d.shape[1:], cy, cx, rS)
    nbb = beam_pix(hh)
    return np.array([np.nansum(d[i][mk]) for i in range(d.shape[0])]) / nbb * FLUXMUT, nu, hh


s27, nu27, h27 = spec_of(os.path.join(SP, "member.uid___A001_X87a_X837.ari_l.SPT0418-47_sci.spw27_362837MHz.12m.cube.I.pbcor.fits"))
s25, nu25, h25 = spec_of(os.path.join(SP, "member.uid___A001_X87a_X837.ari_l.SPT0418-47_sci.spw25_364649MHz.12m.cube.I.pbcor.fits"))
nu_line = NU_CII / (1 + zS)
use27, use25 = nu27 <= 363.74e9, nu25 > 363.74e9
nu_all = np.concatenate([nu27[use27], nu25[use25]]); s_all = np.concatenate([s27[use27], s25[use25]])
order = np.argsort(nu_all); nu_all, s_all = nu_all[order], s_all[order]
fm = np.abs(nu_all - nu_line) > 0.75e9
coef = np.polyfit((nu_all[fm] - nu_line) / 1e9, s_all[fm], 1)
base = np.polyval(coef, (nu_all - nu_line) / 1e9)
res = s_all - base
sig_chS = float(np.std(res[fm]))
lw = np.abs(nu_all - nu_line) <= 0.33e9
dvS = CLIGHT * 7.813e6 / nu_line
S_img = float(np.sum(res[lw]) * dvS); sS_img = float(sig_chS * math.sqrt(lw.sum()) * dvS)
L_img = L_line(S_img, nu_line / 1e9, dlS)
P(f"  image-plane [CII] (spw27 for nu <= 363.74 GHz, spw25 above; linear baseline from |nu - nu_line| > 0.75 GHz; line window +-0.33 GHz = +-{0.33e9 / nu_line * CLIGHT:.0f} km/s): S = {S_img:.2f} +- {sS_img:.2f} Jy km/s; L_image-plane = {L_img:.3e} Lsun; implied [CII] magnification = {L_img / L_pub:.1f} (dust mu 32.3 +- 2.5)")
ROWS_S = dict(gid="SPT0418-47", z=zS, dl_mpc=dlS, kpc_per_arcsec=kpaS, S_cont_mJy=SCs * 1e3, sS_cont_mJy=sCs * 1e3, cont_SN=SCs / sCs, mu=mu, e_mu=e_mu, L_CII=L_pub, logM_CII=math.log10(M_CII_S), logMd25=Md_S[25.0], logMd35=Md_S[35.0], logMd45=Md_S[45.0], d_AB=d_S,
              S_CII_imgplane=S_img, sS_CII_imgplane=sS_img, L_imgplane=L_img, mu_CII_implied=L_img / L_pub, nu_cont_ghz=nuS / 1e9)

# ------------------------------------------------------------------ d_AB, K_AB and the class rule
P("\nTWO-TRACER AGREEMENT AND THE CLASS RULE (Stage 1 §2: M2 iff N_both >= 5 and K_AB <= 0.10 and every |d_i - mu_d| <= 2 max(SD, 0.10); otherwise 'tracer disagreement, class downgraded')")


def class_rule(d):
    d = np.asarray([v for v in d if np.isfinite(v)], float)
    if len(d) < 2:
        return dict(N=len(d), mu=float("nan"), sd=float("nan"), K=float("nan"), M2=False)
    mu_, sd_ = float(d.mean()), float(d.std(ddof=1)); se = sd_ / math.sqrt(len(d)); K_ = math.sqrt(se ** 2 + (abs(mu_) / 2) ** 2)
    ok = len(d) >= 5 and K_ <= 0.10 and bool(np.all(np.abs(d - mu_) <= 2 * max(sd_, 0.10)))
    return dict(N=len(d), mu=mu_, sd=sd_, K=K_, M2=ok)


dlist = list(AL_DF["d_AB"].values) + [d_S]
CR_ALP = class_rule(AL_DF["d_AB"].values)
CR_ALL = class_rule(dlist)
P(f"  ALPINE (N_both = {CR_ALP['N']}): mean d_AB = {CR_ALP['mu']:+.2f}, SD {CR_ALP['sd']:.2f}, K_AB = {CR_ALP['K']:.2f} -> {'M2' if CR_ALP['M2'] else 'TRACER DISAGREEMENT, CLASS DOWNGRADED'}")
P(f"  ALPINE + SPT0418-47 (N_both = {CR_ALL['N']}): mean d_AB = {CR_ALL['mu']:+.2f}, SD {CR_ALL['sd']:.2f}, K_AB = {CR_ALL['K']:.2f} -> {'M2' if CR_ALL['M2'] else 'TRACER DISAGREEMENT, CLASS DOWNGRADED'}")
P("  per-galaxy d_AB (dust at 35 K; positive = the [CII] mass exceeds the dust-based mass): " + ", ".join(f"{r['gid']} {r['d_AB']:+.2f}" if r["cont_det"] else f"{r['gid']} (dust not detected: S/N {r['cont_SN']:.1f}, limit)" for r in ROWS) + f", SPT0418-47 {d_S:+.2f}")
CLS_M2 = CR_ALL["M2"]

# ------------------------------------------------------------------ static table (what the pre-flight and Stage 3 read)
SPL = {}
ST = []
for r in ROWS:
    kpa = r["kpc_per_arcsec"]
    Re_kpc = r["R_dec_arcsec"] * kpa
    both = r["cont_det"]
    lgas = 0.5 * (r["logM_CII"] + r["logMd35"]) if both else r["logM_CII"]
    cls = "M2" if (CLS_M2 and both) else ("S/L" if both else "S")
    bands = (max(CR_ALL["K"], 0.05), 0.21) if cls == "M2" else (0.213, 0.671)
    jr = RNG[RNG["galaxy"] == r["gid"]].sort_values("R_kpc").iloc[-1]
    ST.append(dict(gid=r["gid"], set="ALPINE", z=r["z"], kpc_per_arcsec=kpa, Re_kpc=Re_kpc, Re_resolved=r["resolved"], R_out_kpc=2 * Re_kpc, R_out_kpc_15=1.5 * Re_kpc, R_out_kpc_30=3.0 * Re_kpc,
                   logMstar=r["logMstar"], e_logMstar_inner=0.20, e_logMstar_outer=0.30, logMgas=lgas, logM_CII=r["logM_CII"], logMd25=r["logMd25"], logMd35=r["logMd35"], logMd45=r["logMd45"], cont_det=bool(both), gas_class=cls,
                   gas_band_inner=bands[0], gas_band_outer=bands[1], S_CII=r["S_CII"], sS_CII=r["sS_CII"], S_cont_mJy=r["S_cont_mJy"], sS_cont_mJy=r["sS_cont_mJy"],
                   inc_kin=r["inc_kin"], e_inc_kin=r["e_inc_kin"], jones_R_out_kpc=float(jr["R_kpc"]), jones_e_Vrot=float(jr["e_Vrot_kms"]), sfr=r["sfr"], d_AB=r["d_AB"]))
L_IRS = 2.4e12
ST.append(dict(gid="SPT0418-47", set="SPT0418", z=zS, kpc_per_arcsec=kpaS, Re_kpc=0.9 * 1.678, Re_resolved=True, R_out_kpc=4 * 0.9, R_out_kpc_15=2 * 0.9, R_out_kpc_30=5 * 0.9, logMstar=math.log10(9.5e9), e_logMstar_inner=0.14, e_logMstar_outer=0.30,
               logMgas=0.5 * (math.log10(M_CII_S) + Md_S[35.0]), logM_CII=math.log10(M_CII_S), logMd25=Md_S[25.0], logMd35=Md_S[35.0], logMd45=Md_S[45.0], cont_det=True, gas_class="S/L", gas_band_inner=0.213, gas_band_outer=0.671,
               S_CII=float("nan"), sS_CII=float("nan"), S_cont_mJy=SCs * 1e3, sS_cont_mJy=sCs * 1e3, inc_kin=54.0, e_inc_kin=2.0, jones_R_out_kpc=float("nan"), jones_e_Vrot=float("nan"), sfr=352.0, d_AB=d_S))
sdf = pd.DataFrame(ST)
sdf.to_csv(os.path.join(LANE, f"cfg228_stage1_static{TAG}.csv"), index=False, float_format="%.10g")
AL_DF.to_csv(os.path.join(LANE, f"cfg228_stage1_alpine_measurements{TAG}.csv"), index=False, float_format="%.10g")
json.dump(dict(class_alpine=CR_ALP, class_all=CR_ALL, spt=ROWS_S), open(os.path.join(LANE, f"cfg228_stage1_results{TAG}.json"), "w"), indent=1, default=float)

# ------------------------------------------------------------------ controls
P("\nCONTROLS")
# C1 beam normalisation: a 1 Jy point source convolved with the header's clean beam (peak 1 Jy/beam) summed in a large aperture and divided by N_beam returns 1 Jy
hh0 = fits.getheader(glob.glob(os.path.join(AL, "*DEIMOS_COSMOS_396844.CIImom0.image.fits"))[0])
nb0 = beam_pix(hh0); pix0 = abs(hh0["CDELT1"]) * 3600
yy_, xx_ = np.indices((256, 256)); dy, dx = yy_ - 128.0, xx_ - 128.0
pa_ = math.radians(hh0["BPA"]); sa = hh0["BMAJ"] * 3600 / pix0 / (2 * math.sqrt(2 * math.log(2))); sb = hh0["BMIN"] * 3600 / pix0 / (2 * math.sqrt(2 * math.log(2)))
u = dx * math.sin(pa_) + dy * math.cos(pa_); v_ = -(dx * math.cos(pa_)) + dy * math.sin(pa_)                # PA from north through east: major axis along (sin PA, cos PA)
beam_img = np.exp(-0.5 * ((u / sa) ** 2 + (v_ / sb) ** 2))
s_beam = np.nansum(beam_img[circ_mask(beam_img.shape, 128, 128, 6.0 / pix0)]) / nb0
check("C1 beam normalisation: a 1 Jy point source convolved with the header's Gaussian beam (peak 1 Jy/beam), summed within 6 arcsec and divided by N_beam = Omega_beam/Omega_pix, returns 1 Jy", f"{s_beam:.5f}; N_beam {nb0:.3f}", abs(s_beam - 1.0) < 0.01)
# C2 planted source recovery: a Gaussian source of 1 Jy km/s injected at random far positions of each moment map
def planted(gname, tag, nrec=50, flux=1.0):
    f = lambda kind: glob.glob(os.path.join(AL, f"*{tag}.{kind}"))[0]
    hm = fits.getheader(f("CIImom0.image.fits")); m0 = img2d(f("CIImom0.image.fits")); pbm = img2d(f("continuum.flux.fits.gz"))
    nb = beam_pix(hm); pix = abs(hm["CDELT1"]) * 3600.0
    row = [r for r in ROWS if r["gid"] == gname][0]
    m = np.where(pbm > 0.3, m0 / pbm, np.nan)
    fw = 1.5 * math.sqrt(hm["BMAJ"] * hm["BMIN"]) * 3600.0 / pix                    # source FWHM in pixels: 1.5 x the beam, then convolved with it
    fw_obs = math.sqrt(fw ** 2 + (math.sqrt(hm["BMAJ"] * hm["BMIN"]) * 3600.0 / pix) ** 2)
    sg = fw_obs / (2 * math.sqrt(2 * math.log(2)))
    peak = flux * nb / (2 * math.pi * sg ** 2)                                      # total S = sum / N_beam, Gaussian sum = peak 2 pi sg^2
    rg = np.random.default_rng(SEED + 7)
    rec = []
    yy, xx = np.indices(m.shape)
    tries = 0
    while len(rec) < nrec and tries < 5000:
        tries += 1
        y, x = rg.uniform(40, 216), rg.uniform(40, 216)
        if math.hypot(y - row["cy"], x - row["cx"]) < 40 or not (pbm[int(y), int(x)] > 0.6):
            continue
        inj = m + peak * np.exp(-((yy - y) ** 2 + (xx - x) ** 2) / (2 * sg ** 2))
        k3 = np.ones((3, 3)) / 9.0
        smm = convolve2d(np.nan_to_num(inj), k3, mode="same")
        w = circ_mask(m.shape, y, x, 3.0 / pix)
        iy_, ix_ = np.unravel_index(np.argmax(np.where(w, smm, -np.inf)), smm.shape)
        gg = growth(inj, iy_, ix_, RADS / pix, nb)
        rA = float(RADS[np.argmax(gg >= 0.95 * np.nanmax(gg))])
        rec.append(float(gg[np.where(RADS == rA)[0][0]]))
    return np.array(rec), row["sS_CII"]


pl = {}
for gname, tag in GAL.items():
    rec, sS_ = planted(gname, tag)
    pl[gname] = (float(rec.mean()), float(rec.std(ddof=1)), sS_)
ok2 = all(abs(v[0] - 1.0) < 0.15 for v in pl.values()) and all(abs(v[1] / v[2] - 1.0) < 0.30 for v in pl.values() if v[2] > 0)
check("C2 planted source: a 1 Jy km/s Gaussian (1.5 x the beam) injected at 50 random far positions of each moment map is recovered within 15% in the mean and its scatter matches the random-aperture noise to 30%", "; ".join(f"{g} mean {v[0]:.2f} SD {v[1]:.3f} vs noise {v[2]:.3f}" for g, v in pl.items()), ok2)
pl2 = {}
for gname, tag in GAL.items():
    Sg = [r for r in ROWS if r["gid"] == gname][0]["S_CII"]
    rec, sS_ = planted(gname, tag, flux=Sg)
    pl2[gname] = (float(rec.mean()) / Sg, float(rec.std(ddof=1)), sS_)
P("  [POST HOC, added after the first C2 result, labelled; not a control] C2b the same injection at each galaxy's OWN measured flux: recovered mean / injected and the scatter against the random-aperture noise: " + "; ".join(f"{g} {v[0]:.2f}, SD {v[1]:.3f} vs noise {v[2]:.3f}" for g, v in pl2.items()) + "  (a mean above 1 is the positive bias of the growth-curve maximum at low S/N; a scatter above the noise means the quoted flux error is underestimated by that ratio)")
# C3 formula
S_t, nu_t, dl_t = 2.0, 351.0, 40000.0
check("C3 the L_[CII] formula equals its closed form 1.04e-3 S nu D_L^2 to 1e-9 (S = 2 Jy km/s, nu = 351 GHz, D_L = 4e4 Mpc)", f"{L_line(S_t, nu_t, dl_t):.6e} vs {1.04e-3 * S_t * nu_t * dl_t ** 2:.6e}", abs(L_line(S_t, nu_t, dl_t) / (1.04e-3 * S_t * nu_t * dl_t ** 2) - 1) < 1e-9)
P(f"  [REPORTED, not a control] C3b: the image-plane [CII] luminosity of SPT0418-47 divided by the published de-lensed L_[CII] gives an implied [CII] magnification of {L_img / L_pub:.1f} against the dust mu = 32.3 +- 2.5 ({'within a factor 2' if 16 < L_img / L_pub < 65 else 'OUTSIDE a factor 2: the differential-lensing flag (the extended [CII] is magnified less than the compact dust) or a truncated line window'})")
# C4 monotone T_d and CMB
g_ = [gas_from_dust(1e-3, 356e9, 4.5, T) for T in (25, 30, 35, 40, 45)]
check("C4 the dust-based gas mass falls as T_d rises, and the CMB contrast correction raises the intrinsic luminosity (flux fixed)", f"log M at 25..45 K: {np.round(g_, 2).tolist()}; with / without CMB at 35 K: {gas_from_dust(1e-3, 356e9, 4.5, 35.0):.3f} / {gas_from_dust(1e-3, 356e9, 4.5, 35.0, cmb=False):.3f}", all(g_[i] > g_[i + 1] for i in range(4)) and gas_from_dust(1e-3, 356e9, 4.5, 35.0) > gas_from_dust(1e-3, 356e9, 4.5, 35.0, cmb=False))
# C5 class rule on planted samples
rr_ = np.random.default_rng(5)
dA = rr_.normal(0.0, 0.5, 7); dB = rr_.normal(0.02, 0.05, 7)
check("C5 the class rule returns 'downgraded' for a planted sample with 0.5 dex scatter and 'M2' for one with 0.05 dex scatter", f"scatter 0.5: {class_rule(dA)['M2']} (K {class_rule(dA)['K']:.2f}); scatter 0.05: {class_rule(dB)['M2']} (K {class_rule(dB)['K']:.2f})", (not class_rule(dA)["M2"]) and class_rule(dB)["M2"])
if MODE == "4":
    base_ = json.load(open(os.path.join(LANE, "cfg228_stage1_results.json")))
    B0 = pd.read_csv(os.path.join(LANE, "cfg228_stage1_static.csv")).set_index("gid")
    alp = sdf["set"].values == "ALPINE"
    dlt = (sdf.set_index("gid")["logM_CII"] - B0["logM_CII"]).values
    dd = (sdf.set_index("gid")["logMd35"] - B0["logMd35"]).values
    dab = (sdf.set_index("gid")["d_AB"] - B0["d_AB"]).values
    det_ = alp & sdf["cont_det"].values & np.isfinite(dab)
    check("MUTATE 4: every ALPINE flux x 2 raises the six [CII] gas masses by 0.30103 dex (to 1e-9; SPT0418-47's [CII] mass uses the published L_[CII] and is unchanged) and every dust-based mass by 0.301 dex, and leaves the ALPINE d_AB unchanged where both tracers are detected (SPT0418-47's d_AB moves because only its dust flux is scaled)",
          f"[CII] shifts {np.round(dlt, 4).tolist()}; dust shifts {np.round(dd, 3).tolist()}; d_AB shifts {np.round(dab[det_], 6).tolist()}", bool(np.allclose(dlt[alp], math.log10(2), atol=1e-9) and np.allclose(dd, math.log10(2), atol=2e-3) and np.allclose(dab[det_], 0.0, atol=2e-3)))
P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
open(os.path.join(LANE, f"cfg228_stage1{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>").replace(EXT, "<external>") + "\n")
sys.exit(0 if all(CHK) else 1)

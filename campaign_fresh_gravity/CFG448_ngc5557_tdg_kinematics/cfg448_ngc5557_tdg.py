#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG448 -- ARCHIVAL RESOLVED KINEMATICS OF THE NGC 5557 TIDAL DWARFS (E1/E2/E3): can CFG441's F1 fork be scored now?

Frozen rules: FROZEN_CRITERIA.md (committed alone first, bc9b42594). kappa = 1/2 FITTED; both a0 footings; no dark-matter
particle (the framework's cold-fluid mass is still required wherever the law needs it).

  Archive census (from the committed query results in fetched/ + FETCH_LOG.md).
  The one HI cube that exists (ATLAS3D WSRT, Serra+2012) is tested against U1-U5; its measured HI flux updates F1's gas
  bracket (U5, reported).  Kinematic score only if U1-U5 all pass: Delta = chi2(law+EFE) - chi2(Newton) > +9 on both
  footings -> SETTLING; < -9 -> LAW; else NON-DISCRIMINATING; none usable -> DATA NOT AVAILABLE + observation spec.
  C1: reproduce CFG441 F1 within 0.1 km/s.  C2: nu_mono import + footings.
  MUTATE=1: synthetic V_c := V_Newton (4 km/s error) must read SETTLING on both footings -> exit 1; V_c := V_law+EFE must
  read LAW (reported, same control).
Run: python3 campaign_fresh_gravity/CFG448_ngc5557_tdg_kinematics/cfg448_ngc5557_tdg.py   (needs the cube from
     cfg448_fetch_wsrt_cube.py in _external_data/cfg448/; ~20 s, < 1 GB RAM)
"""
import os, sys, math, csv, json
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from astropy.io import fits
from astropy.wcs import WCS
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG4_common as C4

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "cfg448_ngc5557_tdg" + ("_MUTATE" if MUTATE else "")
FE = os.path.join(HERE, "fetched")
EXT = os.path.join(CFG, "_external_data", "cfg448")
LINES, CHECKS, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LINES.append(s)


def check(name, detail, ok, load_bearing=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")


def banner(s):
    P("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)


P(__doc__.split("Run:")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: synthetic V_c := V_Newton -- the rule must return SETTLING (exit 1) ***")

G_KPC = 4.30091727e-6
KPC_M = 3.0856775814913673e19
ACC = 1e6 / KPC_M
FOOTS, A0, NU = C4.FOOTS, C4.A0, C4.nu_mono
THR = 9.0
D = 38.8                                    # Mpc (Duc+2014 Table 1, ATLAS3D)
ARC_KPC = D * 1e3 * math.pi / 180 / 3600    # kpc per arcsec

# ================================================================================================ C2
banner("C2  CONTROL: the committed nu_mono and the two footings")
deep = float(NU(1e-4) * math.sqrt(1e-4))
check("C2: nu_mono from CFG4_common (deep limit within 2%); footings 9.3603e-11 / 1.1312e-10", f"deep-limit ratio {deep:.4f}",
      abs(deep - 1) < 0.02 and abs(A0['canonical'] - 9.3603e-11) < 1e-15 and abs(A0['alt'] - 1.1312e-10) < 1e-15)


def v_newton(M, R):
    return math.sqrt(G_KPC * M / R)


def v_law(M, R, a0, Mhost=None, Dp=None):
    """CFG441 / CFG7 eq. 4 (FM12 eq. 60) 1-D EFE form; isolated if no host."""
    gNi = G_KPC * M / R ** 2 * ACC
    if Mhost is None:
        ai = gNi * float(NU(gNi / a0))
    else:
        gNe = G_KPC * Mhost / Dp ** 2 * ACC
        ai = gNi * float(NU((gNi + gNe) / a0)) + gNe * (float(NU((gNi + gNe) / a0)) - float(NU(gNe / a0)))
    return math.sqrt(ai / ACC * R)


def pred_err(fn, M, eM, R, eR):
    v0 = fn(M, R)
    dm = (fn(M * 1.01, R) - v0) / (0.01 * M) * eM
    dr = (fn(M, R * 1.01) - v0) / (0.01 * R) * eR
    return v0, math.hypot(dm, dr)


# host field (identical inputs to CFG441 F1)
ses = open(os.path.join(CFG, "CFG441_old_tdgs_tidal_origin", "fetched", "sesame_ngc5557.txt")).read().split("%J ")[1].split()
RA_H, DE_H = float(ses[0]), float(ses[1])
MK = None
for line in open(os.path.join(CFG, "CFG441_old_tdgs_tidal_origin", "fetched", "atlas3d_ngc5557.tsv")):
    if "NGC5557" in line and not line.startswith("#"):
        MK = float(line.split("\t")[10])
MHOST = 0.6 * 10 ** (-0.4 * (MK - 3.28))


def sep_deg(ra1, de1, ra2, de2):
    r = math.radians
    return math.degrees(math.acos(min(1.0, math.sin(r(de1)) * math.sin(r(de2)) + math.cos(r(de1)) * math.cos(r(de2)) *
                                      math.cos(r(ra1 - ra2)))))


def hms(h, m, s): return (h + m / 60 + s / 3600) * 15
def dms(d, m, s): return d + m / 60 + s / 3600


# Duc+2014 Table 1 / 2 (arXiv 1403.0626 LaTeX)
OBJ = {"E1": dict(ra=hms(14, 18, 55.9), de=dms(36, 28, 57), vHI=3252, Mstar=1.2e8, eMstar=0.7e8, Re=2.3),
       "E2": dict(ra=hms(14, 19, 24.5), de=dms(36, 30, 5), vHI=3196, Mstar=0.15e8, eMstar=0.1e8, Re=1.8),
       "E3": dict(ra=hms(14, 19, 58.1), de=dms(36, 31, 53), vHI=3165, Mstar=None, eMstar=None, Re=None)}
for k, o in OBJ.items():
    o["Dp"] = sep_deg(o["ra"], o["de"], RA_H, DE_H) * math.pi / 180 * D * 1e3

# ================================================================================================ C1
banner("C1  CONTROL: reproduce CFG441's F1 forecast with this lane's code")
R1 = 2 * OBJ["E1"]["Re"]
ref = {1.0: (16.4, 28.0, 29.1, 45.0, 47.1), 3.0: (24.2, 39.6, 41.1, 55.6, 58.0)}
dev = 0.0
for fg, r in ref.items():
    M = 1.2e8 * (1 + 1.4 * fg)
    got = (v_newton(M, R1), v_law(M, R1, A0["canonical"], MHOST, OBJ["E1"]["Dp"]), v_law(M, R1, A0["alt"], MHOST, OBJ["E1"]["Dp"]),
           v_law(M, R1, A0["canonical"]), v_law(M, R1, A0["alt"]))
    dev = max(dev, max(abs(a - b) for a, b in zip(got, r)))
    P(f"    M_HI = {fg:.0f} M_*: V_N {got[0]:.2f}; law+EFE {got[1]:.2f} / {got[2]:.2f}; iso {got[3]:.2f} / {got[4]:.2f} km/s "
      f"(CFG441: {r})")
P(f"    E1 projected distance {OBJ['E1']['Dp']:.2f} kpc; M_host {MHOST:.4e} Msun")
check("C1: CFG441 F1 reproduced within 0.1 km/s (all 10 numbers; CFG441 printed 1 decimal)", f"max |dev| = {dev:.3f} km/s",
      dev <= 0.1 + 1e-9)

# ================================================================================================ archive census
banner("ARCHIVES  what exists for NGC 5557-E1/E2/E3 (query results committed in fetched/; log in FETCH_LOG.md)")
F_HI = 1420.40575858e6 / (1 + OBJ["E1"]["vHI"] / 299792.458)


def rows(fn):
    with open(os.path.join(FE, fn)) as f:
        return list(csv.DictReader(f))


nrao = rows("nrao_tap_ngc5557.csv")
hi_line = []
for x in nrao:
    try:
        fmin, fmax = float(x["freq_min"]), float(x["freq_max"])
    except ValueError:
        continue
    res = [float(v) for v in (x.get("spectral_resolutions") or "").split(",") if v.strip()]
    covers = fmin <= F_HI <= fmax
    fine = bool(res) and min(res) <= 50e3
    if covers:
        hi_line.append((x["obs_publisher_did"], x["instrument_name"], x["configuration"], x["t_exptime"], fine,
                        (fmax - fmin) / 1e6))
eso_raw, eso_obs, koa = rows("eso_raw_ngc5557.csv"), rows("eso_obscore_ngc5557.csv"), rows("koa_kcwi_ngc5557.csv")
ap = rows("apertif_dr1_cubes_near.csv")
ap_min = min(sep_deg(float(a["centeralpha"]), float(a["centerdelta"]), OBJ["E1"]["ra"], OBJ["E1"]["de"]) for a in ap) if ap else None
P(f"    NRAO (VLA/EVLA, TAP obscore, 0.3 deg): {len(nrao)} rows; {len(hi_line)} cover the HI line at {F_HI / 1e6:.2f} MHz, of which "
  f"{sum(h[4] for h in hi_line)} have channels <= 50 kHz (spectral-line). Covering rows: " +
  "; ".join(f"{h[0].split('_')[0]} {h[1]}-{h[2]} {h[3]} s, {h[5]:.0f} MHz band, line-capable={h[4]}" for h in hi_line))
P(f"    ESO raw (MUSE/any, box 0.65x0.5 deg): {len(eso_raw)} rows; ESO ObsCore products (0.25 deg): {len(eso_obs)} rows")
P(f"    Keck KOA KCWI (0.25 deg): {len(koa)} rows")
P(f"    Apertif DR1 spectral cubes: nearest compound-beam centre {ap_min:.2f} deg from E1 (beam FWHM ~0.5 deg) -> not covered; "
  "Apertif DR2: no cube in the 210-220 deg x 34-39 deg box")
fashi = [l.split("\t") for l in open(os.path.join(FE, "fashi_ngc5557_field.tsv")) if l.strip() and not l.startswith("#")]
hdr = fashi[0]; fashi = [dict(zip(hdr, r)) for r in fashi[3:] if len(r) == len(hdr)]
FA = {}
for k, o in OBJ.items():
    best = min(fashi, key=lambda r: sep_deg(float(r["RAJ2000"]), float(r["DEJ2000"]), o["ra"], o["de"]))
    s = sep_deg(float(best["RAJ2000"]), float(best["DEJ2000"]), o["ra"], o["de"]) * 3600
    if s < 60 and abs(float(best["cz"]) - o["vHI"]) < 100:
        FA[k] = dict(name=best["Name"], sep=s, cz=float(best["cz"]), W50=float(best["W50"]), eW50=float(best["e_W50"]),
                     W20=float(best["W20"]), Sbf=float(best["Sbf"]) / 1e3, eSbf=float(best["e_Sbf"]) / 1e3)
        P(f"    FASHI (FAST, ~2.9' beam = {2.9 * 60 * ARC_KPC:.0f} kpc): {k} = {best['Name']} ({s:.0f}\" off), cz {FA[k]['cz']:.0f}, "
          f"W50 {FA[k]['W50']:.1f}+-{FA[k]['eW50']:.1f}, W20 {FA[k]['W20']:.1f} km/s, S {FA[k]['Sbf']:.3f}+-{FA[k]['eSbf']:.3f} Jy km/s "
          "(single dish: unresolved, U1 FAIL by construction)")
P("    Gemini archive: anonymous access refused (login required) -- not searched; Duc+2014's GMOS long-slit data are the known "
  "product (+-30 km/s). CADC (CFHT/SITELLE): TAP endpoints unreachable from this host -- not searched. Literature 2014-2026 "
  "(arXiv API, Semantic Scholar citations of Duc+2014 [77], web search): no new kinematics of the NGC 5557 dwarfs found.")
NUM["archives"] = dict(nrao_rows=len(nrao), nrao_hi_covering=[list(h) for h in hi_line], eso_raw=len(eso_raw), eso_obscore=len(eso_obs),
                       koa_kcwi=len(koa), apertif_dr1_nearest_deg=ap_min, fashi=FA)

# ================================================================================================ the WSRT cube
banner("WSRT CUBE  ATLAS3D HI (Serra+2012): U1-U5 for E1, E2, E3")
cube_path = os.path.join(EXT, "NGC5557_cube.fits.gz")
hd = fits.getheader(cube_path)
cube = fits.getdata(cube_path).astype(np.float32)
if cube.ndim == 4:
    cube = cube[0]
w = WCS(hd).celestial
m0 = fits.getdata(os.path.join(FE, "NGC5557_mom0.fits"))[0]
m1 = fits.getdata(os.path.join(FE, "NGC5557_mom1.fits"))[0]
PIX = abs(hd["CDELT2"]) * 3600
BMAJ, BMIN, BPA = hd["BMAJ"] * 3600, hd["BMIN"] * 3600, hd["BPA"]
DV = abs(hd["CDELT3"]) / 1e3
vel = (hd["CRVAL3"] + (np.arange(hd["NAXIS3"]) + 1 - hd["CRPIX3"]) * hd["CDELT3"]) / 1e3
BEAM_PIX = 1.1331 * BMAJ * BMIN / PIX ** 2
P(f"    cube {cube.shape}, pixel {PIX:.1f}\", beam {BMAJ:.1f}\" x {BMIN:.1f}\" (PA {BPA:.0f}) = {BMAJ * ARC_KPC:.1f} x {BMIN * ARC_KPC:.1f} kpc, "
  f"channel {DV:.2f} km/s, header RMS {hd['RMS'] * 1e3:.2f} mJy/beam")
# noise from emission-free channels/region (far from any object, outside the mom0 mask)
off = np.abs(vel - 3250) > 400
sig_ch = np.nanstd(cube[off][:, 40:120, 40:120])
P(f"    measured rms (line-free channels, 80x80 px corner) = {sig_ch * 1e3:.3f} mJy/beam")
lab, nlab = ndimage.label(m0 > 0)


def beam_fwhm_along(pa_deg):
    """beam FWHM (arcsec) along position angle pa (deg E of N)."""
    t = math.radians(pa_deg - BPA)
    return 1.0 / math.sqrt((math.cos(t) / BMAJ) ** 2 + (math.sin(t) / BMIN) ** 2)


RES = {}
for k, o in OBJ.items():
    x0, y0 = [int(round(float(v))) for v in w.world_to_pixel_values(o["ra"], o["de"])]
    L = lab[y0 - 3:y0 + 4, x0 - 3:x0 + 4]; L = L[L > 0]
    comp = np.bincount(L).argmax() if L.size else 0
    msk = lab == comp
    yy, xx = np.nonzero(msk)
    S_mom = float(m0[msk].sum() / BEAM_PIX)                          # Jy km/s
    win = np.abs(vel - o["vHI"]) <= 60
    S_cube = float(cube[win][:, msk].sum() * DV / BEAM_PIX)
    n_pix = msk.sum(); e_S = sig_ch * DV * math.sqrt(win.sum() * n_pix / BEAM_PIX) / 1.0
    MHI = 2.356e5 * D ** 2 * S_mom
    # intensity-weighted geometry
    wgt = m0[msk]; cx, cy = np.average(xx, weights=wgt), np.average(yy, weights=wgt)
    # velocity gradient: plane fit to mom1 in the mask, weighted by mom0
    A = np.c_[np.ones(n_pix), (xx - cx), (yy - cy)]
    Wt = np.sqrt(wgt)
    coef = np.linalg.lstsq(A * Wt[:, None], m1[msk] * Wt, rcond=None)[0]
    # sky: +x pixel = west (RA decreasing); gradient direction PA (E of N) of increasing velocity
    gE, gN = -coef[1] / PIX, coef[2] / PIX                           # km/s per arcsec toward E and N
    PA = math.degrees(math.atan2(gE, gN)) % 360
    grad = math.hypot(gE, gN)
    u = np.array([-math.sin(math.radians(PA)), math.cos(math.radians(PA))])   # pixel-frame unit vector along PA
    proj = ((xx - cx) * u[0] + (yy - cy) * u[1]) * PIX
    extent = float(proj.max() - proj.min() + PIX)                   # detected extent along the kinematic axis (mask edge)
    var = float(np.average(proj ** 2, weights=wgt)); fwhm_obs = 2.3548 * math.sqrt(var)
    Bk = beam_fwhm_along(PA)
    fwhm_dec = math.sqrt(max(fwhm_obs ** 2 - Bk ** 2, 0.0))
    # U3: PV along PA through centroid, 1-beam-wide strip; detection at offsets +-0.5..2 beams
    det = {}
    for side in (+1, -1):
        for kb in (0.5, 1.0, 1.5, 2.0):
            px, py = cx + side * kb * Bk / PIX * u[0], cy + side * kb * Bk / PIX * u[1]
            ix, iy = int(round(px)), int(round(py))
            spec = cube[:, iy - 1:iy + 2, ix - 1:ix + 2].mean(axis=(1, 2))
            sig_avg = sig_ch / math.sqrt(1.0)                       # neighbouring pixels within a beam are fully correlated
            hi = (spec > 3 * sig_avg) & (np.abs(vel - o["vHI"]) <= 80)
            run = max((len(s) for s in "".join("1" if h else "0" for h in hi).split("0")), default=0)
            sel = (np.abs(vel - o["vHI"]) <= 60) & (spec > 2 * sig_avg)
            vc = float(np.sum(spec[sel] * vel[sel]) / np.sum(spec[sel])) if sel.sum() else float("nan")
            det[(side, kb)] = dict(run=run, ok=run >= 3, vcen=vc, R_arcsec=kb * Bk)
    def indep(side):
        oks = [kb for kb in (0.5, 1.0, 1.5, 2.0) if det[(side, kb)]["ok"]]
        return any(b - a >= 1.0 - 1e-9 for a in oks for b in oks)
    U1 = extent >= 2 * Bk
    U2 = DV <= 10.0
    U3 = indep(+1) and indep(-1)
    U4 = False                                                       # no kinematic inclination (unresolved); no published b/a
    U5 = True
    r = dict(x0=x0, y0=y0, comp=int(comp), npix=int(n_pix), S_mom=S_mom, S_cube=S_cube, e_S_noise=e_S, MHI=MHI, PA=PA,
             grad_kms_per_arcsec=grad, vgrad_across_extent=grad * extent, extent_arcsec=extent, extent_beams=extent / Bk,
             beam_along_PA=Bk, fwhm_obs=fwhm_obs, fwhm_dec=fwhm_dec, fwhm_dec_kpc=fwhm_dec * ARC_KPC,
             det={f"{s:+d}x{kb}": v for (s, kb), v in det.items()}, U1=U1, U2=U2, U3=U3, U4=U4, U5=U5)
    RES[k] = r
    P(f"\n    {k}: mom0 component {comp} ({n_pix} px); S(mom0) {S_mom:.3f} Jy km/s, S(cube, mask, +-60 km/s) {S_cube:.3f} "
      f"(noise {e_S:.3f}) -> M_HI {MHI:.3e} Msun at {D} Mpc")
    P(f"        mom1 gradient {grad:.3f} km/s/arcsec toward PA {PA:.0f} deg -> {grad * extent:.1f} km/s across the detected extent")
    P(f"        extent along PA (mask edge) {extent:.0f}\" = {extent / Bk:.2f} beams (beam along PA {Bk:.1f}\"); intensity FWHM "
      f"{fwhm_obs:.1f}\" observed, {fwhm_dec:.1f}\" = {fwhm_dec * ARC_KPC:.1f} kpc beam-deconvolved")
    P("        detection (>= 3 sigma in >= 3 consecutive channels) at offsets along PA [beams]: " +
      ", ".join(f"{s:+d}x{kb}:{'Y' if det[(s, kb)]['ok'] else 'n'}({det[(s, kb)]['run']})" for s in (+1, -1)
                for kb in (0.5, 1.0, 1.5, 2.0)))
    P(f"        U1 >= 2 beams: {'PASS' if U1 else 'FAIL'};  U2 channel <= 10 km/s: {'PASS' if U2 else 'FAIL'} ({DV:.2f});  "
      f"U3 >= 2 independent detected positions per side: {'PASS' if U3 else 'FAIL'};  U4 inclination: FAIL (none);  "
      f"U5 M_HI: PASS (measured)")
USABLE = any(all(RES[k][u] for u in ("U1", "U2", "U3", "U4", "U5")) for k in RES)
NUM["wsrt"] = dict(beam=[BMAJ, BMIN, BPA], channel_kms=DV, rms_mJy=sig_ch * 1e3, objects=RES)
check("flux cross-check: WSRT mom0 vs cube-in-mask flux for E1 within 25%",
      f"{RES['E1']['S_mom']:.3f} vs {RES['E1']['S_cube']:.3f} Jy km/s", abs(RES['E1']['S_cube'] / RES['E1']['S_mom'] - 1) < 0.25,
      load_bearing=False)
if "E1" in FA:
    check("WSRT vs FASHI flux for E1 (FAST beam also contains surrounding tail gas; FAST >= WSRT expected)",
          f"WSRT {RES['E1']['S_mom']:.3f} vs FASHI {FA['E1']['Sbf']:.3f} Jy km/s (ratio {FA['E1']['Sbf'] / RES['E1']['S_mom']:.2f})",
          FA['E1']['Sbf'] >= 0.8 * RES['E1']['S_mom'], load_bearing=False)

# ================================================================================================ F1 updated with measured M_HI
banner("F1-UPDATE (reported): E1's predictions with the MEASURED HI mass (U5) instead of the 1-3 x M_* bracket")
o, r = OBJ["E1"], RES["E1"]
MHI_lo, MHI_hi = r["MHI"], 2.356e5 * D ** 2 * FA["E1"]["Sbf"] if "E1" in FA else r["MHI"]
F1U = []
for lab_, MHI in (("WSRT", MHI_lo), ("FASHI (upper: FAST beam incl. tail gas)", MHI_hi)):
    M = o["Mstar"] + 1.4 * MHI
    eM = math.hypot(o["eMstar"], 1.4 * 0.1 * MHI)
    row = dict(src=lab_, MHI=MHI, MHI_over_Mstar=MHI / o["Mstar"], Mbar=M, eMbar=eM)
    row["vN"], row["evN"] = pred_err(v_newton, M, eM, R1, 0.1 * R1)
    for ft in FOOTS:
        row[f"vE_{ft}"], row[f"evE_{ft}"] = pred_err(lambda MM, RR: v_law(MM, RR, A0[ft], MHOST, o["Dp"]), M, eM, R1, 0.1 * R1)
        row[f"vI_{ft}"] = v_law(M, R1, A0[ft])
    F1U.append(row)
    P(f"    {lab_}: M_HI {MHI:.3e} ({MHI / o['Mstar']:.2f} x M_*), M_bar {M:.3e} +- {eM:.2e}: at R = {R1:.1f} kpc V_N {row['vN']:.1f}+-{row['evN']:.1f}; "
      f"law+EFE {row['vE_canonical']:.1f}+-{row['evE_canonical']:.1f} / {row['vE_alt']:.1f}+-{row['evE_alt']:.1f}; iso {row['vI_canonical']:.1f} / "
      f"{row['vI_alt']:.1f} km/s (canonical / alt)")
gapU = min(min(rw[f"vE_{f}"] for f in FOOTS) - rw["vN"] for rw in F1U)
P(f"    smallest Newton to law+EFE gap {gapU:.1f} km/s -> 3-sigma split needs a total error <= {gapU / 3:.1f} km/s (CFG441: 11.6 / 3.9)")
P(f"    NOTE: the prediction errors are dominated by M_* (Duc+2014: 1.2 +- 0.7 e8) -- a 3-sigma split also needs a better M_*.")
NUM["F1_update"] = dict(rows=F1U, min_gap=gapU)

# ================================================================================================ indicative (never a verdict)
banner("INDICATIVE ONLY (U1-U4 fail; never a verdict): what the unresolved data say about E1's velocity scale")
vg = r["vgrad_across_extent"] / 2
P(f"    WSRT mom1 half-amplitude across the detected extent: {vg:.1f} km/s (beam-smeared, may be tail streaming per Duc+2014)")
if "E1" in FA:
    P(f"    FASHI W50/2 = {FA['E1']['W50'] / 2:.1f} km/s (integrated, incl. turbulence and any tail gas in a 33-kpc beam)")
for ft in FOOTS:
    rw = F1U[0]
    P(f"    {ft}: sin(i) needed for V_rot sin i = {vg:.1f} to equal  V_N: {vg / rw['vN']:.2f}   law+EFE: {vg / rw[f'vE_{ft}']:.2f}   "
      f"iso law: {vg / rw[f'vI_{ft}']:.2f}  -- all < 1, so NO model is excluded without an inclination")
NUM["indicative"] = dict(vgrad_half=vg)

# ================================================================================================ decision
banner("DECISION (frozen rule)")
if USABLE:
    VERDICT = "SCORED"   # not reached in this run; kept for completeness
else:
    VERDICT = "DATA NOT AVAILABLE"
P(f"    usable kinematic product for E1/E2/E3: {'YES' if USABLE else 'NO'} -> verdict: {VERDICT}")
NUM["verdict"] = VERDICT

# ================================================================================================ observation spec
banner("OBSERVATION SPECIFICATION (planning numbers; instrument values are approximate and must be checked with the official "
       "exposure calculators)")
Rout_as = R1 / ARC_KPC
beam_need = Rout_as / 2.0                     # R_out >= 2 beams from centre -> >= 2 independent positions per side
dv_need = 5.0
# mean HI column over E1 inside its deconvolved FWHM (from the WSRT flux) and an outer column of half that
area_as2 = math.pi * Rout_as ** 2          # E1's HI is unresolved by WSRT: assume its flux spread uniformly inside R_out
N_mean = 1.104e21 * (r["S_mom"] * 1e3) * 1.1331 / area_as2              # cm^-2
N_out = N_mean / 2
sig_v = 8.0
S_peak = N_out * beam_need ** 2 / 1.104e21 / (math.sqrt(2 * math.pi) * sig_v)  # mJy/beam (line peak, Gaussian sigma_v)
rms_need = S_peak / 5.0                       # peak S/N 5 per 5 km/s channel at the outer points
dnu = dv_need / 299792.458 * F_HI
INSTR = {"VLA C-config (L band, robust ~13\")": dict(SEFD=420.0, N=27, eff=0.92, wfac=1.3),
         "uGMRT band 5 (tapered to ~12\")": dict(SEFD=400.0, N=30, eff=0.9, wfac=1.4)}
SPEC = {}
for name, s in INSTR.items():
    t = (s["SEFD"] * s["wfac"] / (s["eff"] * rms_need * 1e-3)) ** 2 / (s["N"] * (s["N"] - 1) * 2 * dnu) / 3600
    SPEC[name] = t
P(f"    target radius R_out = 2 R_e = {R1:.1f} kpc = {Rout_as:.1f}\"; beam needed <= {beam_need:.1f}\" (R_out >= 2 beams); "
  f"channel <= {dv_need:.0f} km/s ({dnu / 1e3:.1f} kHz)")
P(f"    E1 mean N_HI if its WSRT flux fills R_out uniformly: {N_mean:.2e} cm^-2; assumed outer column N_mean/2 = {N_out:.2e}")
P(f"    peak line brightness at the outer points ({beam_need:.0f}\" beam, sigma_v {sig_v:.0f} km/s): {S_peak:.3f} mJy/beam -> rms needed "
  f"(peak S/N 5 per channel) {rms_need * 1e3:.0f} microJy/beam per {dv_need:.0f} km/s channel")
for name, t in SPEC.items():
    P(f"    {name}: on-source time ~{t:.0f} h")
P("    Also required: optical axis ratio / kinematic inclination (deep g/r imaging exists: CFHT MegaCam, Duc+2011/2014; "
  "Legacy Surveys), and a better M_* (SED with NIR). IFU H-alpha alternative: CFHT/SITELLE SN3 (R ~ 5000, 11' field, ~1\" "
  "seeing) or Keck/KCWI red arm -- E1's H-alpha is weak (SFR 5-10e-3 Msun/yr) and patchy, so HI is the primary tracer. "
  "MUSE: Dec +36.5 culminates at ~29 deg elevation from Paranal (airmass ~2) -- poor; MeerKAT similarly low (~23 deg).")
P("    Sample note: CFG441's frozen rule needs N_A >= 3 old tidal TDGs; E1 alone is a single-object reading.")
NUM["obs_spec"] = dict(R_out_arcsec=Rout_as, beam_need=beam_need, dv_need=dv_need, N_mean=N_mean, N_out=N_out, rms_need_mJy=rms_need,
                       hours=SPEC)


# ================================================================================================ the rule + MUTATE
def rule(V, eV, row):
    out = {}
    for ft in FOOTS:
        cN = (V - row["vN"]) ** 2 / (eV ** 2 + row["evN"] ** 2)
        cE = (V - row[f"vE_{ft}"]) ** 2 / (eV ** 2 + row[f"evE_{ft}"] ** 2)
        out[ft] = cE - cN
    if all(d > THR for d in out.values()):
        return "SETTLING", out
    if all(d < -THR for d in out.values()):
        return "LAW", out
    return "NON-DISCRIMINATING", out


banner("RULE TEST " + ("(MUTATE: synthetic V_c = V_Newton must give SETTLING)" if MUTATE else "(synthetic, reported: shows the rule's reach)"))
# bracket ends (CFG441) + the measured masses; prediction errors fixed at 0 for the synthetic test of the rule itself
rule_rows = []
for fg in (1.0, 3.0):
    M = 1.2e8 * (1 + 1.4 * fg)
    rw = dict(src=f"bracket {fg:.0f}xM*", vN=v_newton(M, R1), evN=0.0)
    for ft in FOOTS:
        rw[f"vE_{ft}"], rw[f"evE_{ft}"] = v_law(M, R1, A0[ft], MHOST, OBJ["E1"]["Dp"]), 0.0
    rule_rows.append(rw)
for rw in F1U:
    rule_rows.append(dict(rw, evN=0.0, **{f"evE_{f}": 0.0 for f in FOOTS}))
res_rule = []
for rw in rule_rows:
    vS, dS = rule(rw["vN"], 4.0, rw)
    vL, dL = rule(rw["vE_canonical"], 4.0, rw)
    res_rule.append(dict(src=rw["src"], newton_input=vS, d_newton=dS, law_input=vL, d_law=dL))
    P(f"    {rw['src']:<42s} V_c := V_N  -> {vS:<18s} (Delta {dS['canonical']:+.1f} / {dS['alt']:+.1f});  "
      f"V_c := V_law+EFE(canonical) -> {vL:<18s} (Delta {dL['canonical']:+.1f} / {dL['alt']:+.1f})")
# the same with the full measured-mass prediction errors (what a real 4 km/s measurement would face today)
for rw in F1U:
    vS, dS = rule(rw["vN"], 4.0, rw)
    P(f"    with today's M_* error ({rw['src'][:5]}): V_c := V_N -> {vS} (Delta {dS['canonical']:+.1f} / {dS['alt']:+.1f})")
    res_rule.append(dict(src=rw["src"] + " +pred errors", newton_input=vS, d_newton=dS))
for rw in rule_rows:
    v3, d3 = rule(rw["vN"], 3.0, rw)
    P(f"    (reported variant, 3 km/s error) {rw['src']:<42s} V_c := V_N -> {v3} (Delta {d3['canonical']:+.1f} / {d3['alt']:+.1f})")
    res_rule.append(dict(src=rw["src"] + " 3kms", newton_input_3kms=v3, d_newton_3kms=d3))
NUM["rule_test"] = res_rule
all_settle = all(x["newton_input"] == "SETTLING" for x in res_rule[:len(rule_rows)])
all_law = all(x["law_input"] == "LAW" for x in res_rule[:len(rule_rows)])
if MUTATE:
    miss = [x["src"] for x in res_rule[:len(rule_rows)] if x["newton_input"] != "SETTLING"]
    P(f"    MUTATE {'DETECTED at every mass' if not miss else 'NOT DETECTED (control FAILS, kept as it fell) at: ' + '; '.join(miss)}")
    NUM["mutate_missed"] = miss
    check("MUTATE: synthetic V_c := V_Newton (4 km/s) read as SETTLING on both footings at every mass (expected; exit 1 when detected)",
          f"all SETTLING = {all_settle}; law input all LAW = {all_law}", not all_settle)
else:
    check("rule reach: V_c = V_N -> SETTLING and V_c = V_law+EFE -> LAW at every mass with a 4 km/s error",
          f"SETTLING {all_settle}, LAW {all_law}", all_settle and all_law, load_bearing=False)

# ================================================================================================ write
lb = [c for c in CHECKS if c["load_bearing"]]
nf = sum(not c["ok"] for c in lb)
P(f"\n  {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} checks pass; load-bearing failures: {nf}")
P(f"  VERDICT: {VERDICT}")


def jclean(x):
    if isinstance(x, dict):
        return {str(k): jclean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jclean(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x


with open(os.path.join(HERE, SLUG + ".out"), "w") as f:
    f.write("\n".join(LINES) + "\n")
with open(os.path.join(HERE, SLUG + "_results.json"), "w") as f:
    json.dump(jclean(dict(checks=CHECKS, num=NUM)), f, indent=1)
sys.exit(1 if nf else 0)

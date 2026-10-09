#!/usr/bin/env python3
"""CFG573: GS4_24110 dust size from the public 0.13" continuum image, and its effect on CFG572's Delta_v (FROZEN_CRITERIA.md, eaee201fe).
Run: python3 cfg573_dust.py [--mutate].  The image lives in data_assembly/gs4_24110_cubes/ (not committed)."""
import os, sys, json, math
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.optimize import curve_fit
from scipy.integrate import quad
from scipy.special import i0, i1, k0, k1, erf
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IMG = os.path.join(ROOT, "data_assembly", "gs4_24110_cubes", "gs4_24110_cont.I.pbcor.fits")
PBF = os.path.join(ROOT, "data_assembly", "gs4_24110_cubes", "gs4_24110_cont.I.pb.fits.gz")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []; CHK = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(name, ok, extra=""): CHK.append((name, bool(ok))); P(f"[{'PASS' if ok else 'FAIL'}] {name} {extra}")
RA, DEC, Z = 53.166889, -27.798733, 1.9972
h = fits.getheader(IMG); img = np.squeeze(fits.getdata(IMG)).astype(float); pb = np.squeeze(fits.getdata(PBF)).astype(float)
w = WCS(h).celestial; pix = abs(h["CDELT1"]) * 3600; bmaj, bmin, bpa = h["BMAJ"] * 3600, h["BMIN"] * 3600, h["BPA"]
nu = h.get("CRVAL3", 264.927e9) / 1e9
dc = 2.99792458e5 / 70 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, Z)[0]; DA = dc / (1 + Z) * 1e3   # kpc
kpc_as = DA / 206264.806
beam_pix = math.pi / (4 * math.log(2)) * bmaj * bmin / pix ** 2
x0, y0 = w.world_to_pixel_values(RA, DEC)
if MUT: x0 += 2.0 / pix
yy, xx = np.mgrid[:img.shape[0], :img.shape[1]]
rr = np.hypot(xx - x0, yy - y0) * pix
ann = (rr > 2) & (rr < 6) & (pb >= 0.5) & np.isfinite(img)
sig = 1.4826 * np.nanmedian(np.abs(img[ann] - np.nanmedian(img[ann])))
P(f"image: beam {bmaj:.3f}x{bmin:.3f}\" PA {bpa:.0f}, pixel {pix:.4f}\", nu {nu:.2f} GHz, rms {sig * 1e6:.1f} uJy/beam, D_A {DA / 1e3:.0f} Mpc ({kpc_as:.2f} kpc/\")")
inr = (rr <= 0.5) & np.isfinite(img); pk = np.nanmax(img[inr]); snr = pk / sig
det = snr >= 5; P(f"peak within 0.5\": {pk * 1e6:.1f} uJy/beam, S/N {snr:.1f} -> {'DETECTED' if det else 'not detected'}")

def g2(XY, A, xc, yc, sx, sy, th):
    X, Y = XY; a = np.cos(th) ** 2 / (2 * sx ** 2) + np.sin(th) ** 2 / (2 * sy ** 2); b = -np.sin(2 * th) / (4 * sx ** 2) + np.sin(2 * th) / (4 * sy ** 2)
    c = np.sin(th) ** 2 / (2 * sx ** 2) + np.cos(th) ** 2 / (2 * sy ** 2)
    return A * np.exp(-(a * (X - xc) ** 2 + 2 * b * (X - xc) * (Y - yc) + c * (Y - yc) ** 2))
half = int(round(1.0 / pix))
def fit(im, xc, yc):
    xi, yi = int(round(xc)), int(round(yc)); cut = im[yi - half:yi + half + 1, xi - half:xi + half + 1]
    Y, X = np.mgrid[yi - half:yi + half + 1, xi - half:xi + half + 1]; m = np.isfinite(cut)
    s0 = bmaj / pix / 2.3548
    p, cv = curve_fit(g2, (X[m], Y[m]), cut[m], p0=[np.nanmax(cut), xc, yc, s0 * 1.5, s0 * 1.2, 0.0], maxfev=20000)
    A, xc2, yc2, sx, sy, th = p; sx, sy = abs(sx), abs(sy)
    fwhm_maj, fwhm_min = 2.3548 * max(sx, sy) * pix, 2.3548 * min(sx, sy) * pix
    dmaj = math.sqrt(max(fwhm_maj ** 2 - bmaj ** 2, 0)); dmin = math.sqrt(max(fwhm_min ** 2 - bmin ** 2, 0))
    flux = 2 * math.pi * A * sx * sy / beam_pix
    return dict(A=A, xc=xc2, yc=yc2, fwhm=(fwhm_maj, fwhm_min), dec=(dmaj, dmin), Re_as=math.sqrt(dmaj * dmin) / 2, flux=flux)
res = dict(snr=snr, detected=det, beam=(bmaj, bmin), rms_uJy=sig * 1e6)
if not det:
    json.dump(dict(controls=CHK, result=res), open(os.path.join(HERE, f"cfg573_dust{TAG}_results.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg573_dust{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    if MUT: P("MUTATE (2\" shifted position): no detection -> detected (exit 1)"); open(os.path.join(HERE, f"cfg573_dust{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1)
F = fit(img, x0, y0)
P(f"fit: FWHM {F['fwhm'][0]:.3f}x{F['fwhm'][1]:.3f}\" -> deconvolved {F['dec'][0]:.3f}x{F['dec'][1]:.3f}\"; R_e,dust = {F['Re_as']:.3f}\" = {F['Re_as'] * kpc_as:.2f} kpc; flux {F['flux'] * 1e6:.0f} uJy")
# noise realisations: add source-free cutouts
rng = np.random.default_rng(573); free = np.argwhere((rr > 3) & (rr < 8) & (pb >= 0.5))
Res = []
for _ in range(200):
    cy, cx = free[rng.integers(len(free))]; im2 = img.copy()
    xi, yi = int(round(x0)), int(round(y0))
    try:
        noise = img[cy - half:cy + half + 1, cx - half:cx + half + 1]
        if noise.shape != (2 * half + 1, 2 * half + 1) or not np.all(np.isfinite(noise)): continue
        im2[yi - half:yi + half + 1, xi - half:xi + half + 1] += noise
        Res.append(fit(im2, x0, y0)["Re_as"] * kpc_as)
    except Exception: pass
Res = np.array(Res); eRe = float(np.std(Res)); Re = F["Re_as"] * kpc_as
P(f"R_e,dust = {Re:.2f} +- {eRe:.2f} kpc ({len(Res)} noise realisations; added noise ~sqrt(2) x real, conservative); stellar/Halpha R_e 7.39 kpc")
exp_flux = 342e-6 * (nu / 242.6) ** 3.8; rec = F["flux"] / exp_flux
P(f"flux recovery: {F['flux'] * 1e6:.0f} uJy vs expected {exp_flux * 1e6:.0f} uJy (Boogaard 342 uJy at 1.2 mm scaled, beta 1.8) = {rec:.2f}" + ("  -> < 50%: extended emission resolved out; R_e,dust is a LOWER bound" if rec < 0.5 else ""))
res.update(Re_kpc=Re, eRe_kpc=eRe, Re_as=F["Re_as"], fwhm=F["fwhm"], dec=F["dec"], flux_uJy=F["flux"] * 1e6, flux_expected_uJy=exp_flux * 1e6, recovery=rec, lower_bound=rec < 0.5)

if not MUT:
    # C1 injection
    sxb, syb = bmaj / pix / 2.3548, bmin / pix / 2.3548; xi, yi = x0 + 3 / pix, y0
    th = math.radians(bpa + 90); im3 = img + g2((xx, yy), 300e-6, xi, yi, sxb, syb, th)
    Fi = fit(im3, xi, yi)
    check("C1 injected point source: deconvolved size < beam/3 and flux within 15%", Fi["Re_as"] * 2 < bmin / 3 and abs(Fi["flux"] / (300e-6 * 2 * math.pi * sxb * syb / beam_pix) - 1) < 0.15,
          f"(size {2 * Fi['Re_as']:.3f}\", flux ratio {Fi['flux'] / (300e-6 * 2 * math.pi * sxb * syb / beam_pix):.3f})")
    m2 = (np.hypot(xx - (x0 + 2 / pix), yy - y0) * pix <= 0.5) & np.isfinite(img)
    check("C2 blank sky 2\" away: no >= 5 sigma peak", np.nanmax(img[m2]) / sig < 5, f"(S/N {np.nanmax(img[m2]) / sig:.1f})")

# effect on Delta_v (CFG572 recipe)
sys.path.insert(0, os.path.join(ROOT, "campaign_fresh_gravity", "CFG44_fluid_target")); from Bcommon import nu_mono
from scipy.optimize import brentq
G = 4.30091e-6; RE = 7.39; RD = RE / 1.678; VC = 206.0
Bf = lambda y: y * y * (i0(y) * k0(y) - i1(y) * k1(y)); v2exp = lambda M, Rd: 2 * G * M / Rd * Bf(RE / (2 * Rd))
def v2gauss(M, Re_):
    s = Re_ / 1.1774; x = RE / s; f = erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * math.exp(-x * x / 2); return G * M * f / RE
J5 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json")))["results"]["GS4_24110"]
J2 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG572_gs4_24110_gas_now", "cfg572_gas_results.json")))["delta_v"]
MG = 10 ** 10.51
MODELS = ["F-DESI", "F-flat", "R-H", "L-fb(RAR-eq)"]
P("\n=== Delta_v at R_e with the measured dust shape (dust-route gas 10^10.51, canon footing) vs CFG572 (R_g = R_d) ===")
dv = {}
for lm in ("10.89", "10.76"):
    for shp in ("S1 exp", "S2 gauss"):
        row = []
        for mn in MODELS + ["Newton"]:
            vr = VC ** 2 if mn == "Newton" else 10 ** J5[lm][f"canon 9.36e-11|{mn}"]["logVbar2R_G"] * G / RE
            vg = (lambda M, R_: v2exp(M, R_ / 1.678)) if shp == "S1 exp" else v2gauss
            f = lambda dl, ds, dr: math.log10((v2exp(10 ** (float(lm) + ds), RD) + vg(MG * 10 ** dl, max(Re + dr, 0.05))) / vr)
            d0 = f(0, 0, 0); e = 0.5 * math.sqrt((f(0.2, 0, 0) - f(-0.2, 0, 0)) ** 2 + (f(0, 0.1, 0) - f(0, -0.1, 0)) ** 2 + (f(0, 0, eRe) - f(0, 0, -eRe)) ** 2)
            old = J2.get(f"{lm}|DUST a4.36|canon 9.36e-11|{mn}", {}).get("dv") if mn != "Newton" else J2[f"{lm}|DUST a4.36|Newton-max"]["dv"]
            ten = "tension" if abs(d0) > 2 * e else "consistent"
            dv[f"{lm}|{shp}|{mn}"] = dict(dv=d0, err=e, verdict=ten, cfg572=old)
            row.append(f"{mn} {d0:+.2f}+-{e:.2f} ({'tens' if ten == 'tension' else 'cons'}; was {old:+.2f})")
        P(f"  M* {lm} | {shp}: " + "; ".join(row))
res["delta_v"] = dv
json.dump(dict(controls=CHK, result=res), open(os.path.join(HERE, f"cfg573_dust{TAG}_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg573_dust{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT: P("MUTATE (2\" shifted position): a source was DETECTED -> NOT detected as broken"); open(os.path.join(HERE, f"cfg573_dust{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)
sys.exit(0 if all(ok for _, ok in CHK) else 1)

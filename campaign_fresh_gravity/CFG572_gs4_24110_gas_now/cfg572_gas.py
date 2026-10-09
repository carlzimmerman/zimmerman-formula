#!/usr/bin/env python3
"""CFG572: GS4_24110 (ASPECS 1mm.C10) gas mass from public data vs CFG571's frozen prediction (FROZEN_CRITERIA.md, 9c60f25ad).
Run: python3 cfg572_gas.py [--mutate].  Reads pipeline pbcor cubes from data_assembly/gs4_24110_cubes/ (not committed)."""
import os, sys, glob, json, math, tarfile
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUBES = os.path.join(ROOT, "data_assembly", "gs4_24110_cubes")
M1K = "--mutate1000" in sys.argv; MUT = "--mutate" in sys.argv or M1K; TAG = ("_MUTATE1000" if M1K else "_MUTATE") if MUT else ""; VSHIFT = (1000.0 if M1K else 2000.0) if MUT else 0.0  # +1000 = disclosed departure: +2000 falls outside the cubes' spectral coverage
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
CHK = []
def check(name, ok, extra=""): CHK.append((name, bool(ok))); P(f"[{'PASS' if ok else 'FAIL'}] {name} {extra}")
C = 2.99792458e5; Z = 1.9975; RA, DEC = 53.166889, -27.798733
LINES = {"CI10": (492.161, "X99e"), "CO43": (461.041, "X99a")}
dc = C / 70.0 * quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, Z)[0]; DL = dc * (1 + Z)   # Mpc

def find_cube(nu_obs, tag):
    tb = os.path.join(CUBES, tag + ".tar"); dd = os.path.join(CUBES, tag)
    if not os.path.isdir(dd):
        with tarfile.open(tb) as t:
            t.extractall(dd, members=[m for m in t.getmembers() if m.name.endswith(".pbcor.fits") and ".cube." in m.name])
    for f in sorted(glob.glob(os.path.join(dd, "**", "*.cube*.pbcor.fits"), recursive=True)):
        h = fits.getheader(f); w = WCS(h).spectral; n = h["NAXIS3"]
        fr = w.pixel_to_world_values(np.array([0, n - 1])) / 1e9
        if min(fr) <= nu_obs <= max(fr): return f
    return None

def measure(f, nu_rest):
    hd = fits.open(f)[0]; h = hd.header; d = np.squeeze(hd.data).astype(float)          # (chan, y, x)
    w = WCS(h).celestial; ws = WCS(h).spectral
    nu = ws.pixel_to_world_values(np.arange(d.shape[0])) / 1e9; nu_obs = nu_rest / (1 + Z)
    v = C * (nu_obs - nu) / nu_obs - VSHIFT                                                  # radio-ish velocity about the line
    pix = abs(h["CDELT1"]) * 3600; bmaj, bmin = h["BMAJ"] * 3600, h["BMIN"] * 3600
    beam_pix = math.pi / (4 * math.log(2)) * bmaj * bmin / pix ** 2
    x0, y0 = w.world_to_pixel_values(RA, DEC); dv = abs(np.median(np.diff(v)))
    yy, xx = np.mgrid[:d.shape[1], :d.shape[2]]
    def ap(xc, yc, r=1.5):
        m = (xx - xc) ** 2 + (yy - yc) ** 2 <= (r / pix) ** 2
        spec = np.nansum(d[:, m], axis=1) / beam_pix
        cont = np.nanmedian(spec[np.abs(v) > 600]); win = np.abs(v) <= 300
        return float(np.nansum(spec[win] - cont) * dv), spec - cont
    S, spec = ap(x0, y0)
    ring = []
    for k in range(8):
        th = 2 * math.pi * k / 8; rr = 6.5 / pix; ring.append(ap(x0 + rr * math.cos(th), y0 + rr * math.sin(th))[0])
    sig = float(np.std(ring, ddof=1)); ok3 = (min(nu) <= nu_obs <= max(nu)) and "BMAJ" in h
    return dict(S=S, sig=sig, ring=ring, beam=(bmaj, bmin), pix=pix, dv=dv, nu_obs=nu_obs, v=v.tolist(), spec=spec.tolist(), header_ok=ok3,
                x0=float(x0), y0=float(y0), shape=d.shape, file=os.path.basename(f), offpos=[ap(x0 + 7 / pix * math.cos(t), y0 + 7 / pix * math.sin(t))[0] for t in (0.3, 1.5, 2.7, 3.9, 5.1)])

def Lprime(S, nu_obs): return 3.25e7 * S * nu_obs ** -2 * DL ** 2 * (1 + Z) ** -3
def m_ci(Lp, X):
    T = 25.0; Q = 1 + 3 * math.exp(-23.6 / T) + 5 * math.exp(-62.5 / T)
    return 1.36 * 5.706e-4 * Q / 3 * math.exp(23.6 / T) * Lp / (6 * X)
def m_co43(Lp, r41): return 4.36 * Lp / r41

res = {}; meas = {}
for ln, (nu0, tag) in LINES.items():
    f = find_cube(nu0 / (1 + Z), tag)
    if f is None: P(f"{ln}: no cube covering {nu0 / (1 + Z):.3f} GHz"); continue
    m = measure(f, nu0); meas[ln] = m
    if m["sig"] == 0 or not np.isfinite(m["sig"]):
        P(f"{ln}: the shifted window falls outside the cube's spectral coverage -> not measurable"); res[ln] = dict(S=float("nan"), sig=float("nan"), detected=False, out_of_band=True, logM={}); continue
    P(f"\n{ln} ({m['file']}): nu_obs {m['nu_obs']:.3f} GHz, beam {m['beam'][0]:.2f}x{m['beam'][1]:.2f}\", dv {m['dv']:.1f} km/s, D_L {DL:.0f} Mpc")
    P(f"   S dv = {m['S']:.3f} +- {m['sig']:.3f} Jy km/s  (S/N {m['S'] / m['sig']:+.2f}); ring {np.round(m['ring'], 3).tolist()}")
    if not MUT:
        check(f"C3 {ln} header: frequency axis covers the line and beam keywords present", m["header_ok"])
        check(f"C2 {ln} off-source apertures consistent with zero (|S| < 3 sigma)", all(abs(s) < 3 * m["sig"] for s in m["offpos"]), str(np.round(m["offpos"], 3).tolist()))
    det = m["S"] >= 3 * m["sig"]; Sv = m["S"] if det else 3 * m["sig"]
    Lp = Lprime(Sv, m["nu_obs"])
    if ln == "CI10": br = {"X_CI 1.9e-5": m_ci(Lp, 1.9e-5), "X_CI 3.0e-5": m_ci(Lp, 3.0e-5)}
    else: br = {"r41 0.37": m_co43(Lp, 0.37), "r41 0.25": m_co43(Lp, 0.25), "r41 0.55": m_co43(Lp, 0.55)}
    lo = {}
    if det:
        Lp_lo = Lprime(max(m["S"] - m["sig"], 1e-9), m["nu_obs"]); Lp_hi = Lprime(m["S"] + m["sig"], m["nu_obs"])
        lo = {k: (math.log10(v * Lp_lo / Lp), math.log10(v * Lp_hi / Lp)) for k, v in br.items()}
    res[ln] = dict(S=m["S"], sig=m["sig"], detected=det, logM={k: math.log10(v) for k, v in br.items()}, logM_1sig=lo, upper_limit=not det)
    P(f"   {'DETECTED' if det else 'NOT detected: 3-sigma upper limit'}; log M_gas: " + ", ".join(f"{k} {'<' if not det else ''}{math.log10(v):.2f}" for k, v in br.items()))

# dust route (literature, Boogaard+2020 Table L850)
L850 = 32.1e29; eL = 3.2e29
md = L850 / 6.7e19
res["DUST"] = dict(logM={"alphaCO 4.36 (primary)": math.log10(md * 4.36 / 6.5), "Scoville alphaCO 6.5": math.log10(md)}, err_dex=0.2)
P(f"\nDUST (Boogaard+2020 L850 = 32.1e29): log M_mol = {math.log10(md * 4.36 / 6.5):.2f} (alpha_CO 4.36) / {math.log10(md):.2f} (6.5); +-0.2 dex scatter")

# C1 injection: a beam-shaped source added 10" from the target, recovered by the same aperture recipe
if not MUT:
    for ln, (nu0, tag) in LINES.items():
        if ln not in meas: continue
        f = find_cube(nu0 / (1 + Z), tag); inj = 0.5 if ln == "CI10" else 0.3
        pix = meas[ln]["pix"]
        hdd = fits.open(f)[0]; dd = np.squeeze(hdd.data).astype(float)
        # direct recovery: compare off-target aperture flux with and without injection
        def apflux(data, xc, yc, h):
            ws = WCS(h).spectral; nu = ws.pixel_to_world_values(np.arange(data.shape[0])) / 1e9; nuo = nu0 / (1 + Z)
            v = C * (nuo - nu) / nuo; dv = abs(np.median(np.diff(v)))
            bpix = math.pi / (4 * math.log(2)) * h["BMAJ"] * h["BMIN"] * 3600 ** 2 / pix ** 2
            yy, xx = np.mgrid[:data.shape[1], :data.shape[2]]; mm = (xx - xc) ** 2 + (yy - yc) ** 2 <= (1.5 / pix) ** 2
            sp = np.nansum(data[:, mm], axis=1) / bpix; cont = np.nanmedian(sp[np.abs(v) > 600]); win = np.abs(v) <= 300
            return float(np.nansum(sp[win] - cont) * dv), v, dv
        h = hdd.header; xi, yi = meas[ln]["x0"] - 10 / pix, meas[ln]["y0"]
        s0, v, dv = apflux(dd, xi, yi, h)
        sx = h["BMAJ"] * 3600 / pix / 2.3548; sy = h["BMIN"] * 3600 / pix / 2.3548
        yy, xx = np.mgrid[:dd.shape[1], :dd.shape[2]]; g = np.exp(-0.5 * (((xx - xi) / sx) ** 2 + ((yy - yi) / sy) ** 2))
        win = np.abs(v) <= 300; d2 = dd.copy(); d2[win] += g[None] * inj / (win.sum() * dv)
        s1, _, _ = apflux(d2, xi, yi, h); rec = (s1 - s0) / inj
        check(f"C1 {ln} injection of {inj} Jy km/s recovered within 20%", abs(rec - 1) < 0.2, f"(recovered fraction {rec:.3f})")

# comparison with CFG571 frozen predictions
J = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json")))["results"]["GS4_24110"]
P("\n=== vs CFG571 frozen required total log M_gas (R_g = R_d) ===")
cmp = {}
for lm in ("10.89", "10.76"):
    for key, d in J[lm].items():
        fn, mn = key.split("|"); cmp.setdefault(lm, {})[key] = d["logMgas_Rg=Rd"]
    P(f"  logM* {lm}: " + "; ".join(f"{k.split('|')[1]} [{k.split('|')[0][:5]}] {'FLOOR' if v is None else f'{v:.2f}'}" for k, v in cmp[lm].items()))
P("  measured: " + "; ".join(f"{ln} " + ", ".join(f"{k} {'<' if r.get('upper_limit') else ''}{v:.2f}" for k, v in r["logM"].items()) for ln, r in res.items()))

# Delta_v at Re (criteria): V_bar,meas^2 = V*^2 (Freeman) + V_gas^2 (exponential, Rg = Rd) vs each model's frozen V_bar,req^2 (CFG571 logVbar2R_G)
sys.path.insert(0, os.path.join(ROOT, "campaign_fresh_gravity", "CFG44_fluid_target")); from Bcommon import nu_mono
from scipy.special import i0, i1, k0, k1
from scipy.optimize import brentq
G = 4.30091e-6; RE = 7.39; RD = RE / 1.678; VC = 206.0; Uc = 1e6 / 3.0857e19
Bf = lambda y: y * y * (i0(y) * k0(y) - i1(y) * k1(y)); v2e = lambda M: 2 * G * M / RD * Bf(RE / (2 * RD))
RAT = {"F-DESI": 0.874, "F-flat": 1.0, "R-H": math.sqrt(0.315 * 2.997 ** 3 + 0.685), "L-fb(RAR-eq)": float(np.interp(1.997, [0, 1, 2, 2.5], [1, 1.2, 2.82, 4.88]))}
J5 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity", "CFG571_prereg_proprietary_alma", "cfg571_prereg_results.json")))["results"]["GS4_24110"]
def vreq2(fn, mn, lm):
    if lm in J5: return 10 ** J5[lm][f"{fn}|{mn}"]["logVbar2R_G"] * G / RE
    a0 = {"canon 9.36e-11": 9.3603e-11, "alt 1.13e-10": 1.1312e-10}[fn] * RAT[mn] / Uc; g = VC ** 2 / RE   # post-freeze branch: same CFG571 recipe
    return brentq(lambda gb: float(nu_mono(gb / a0)) * gb - g, g * 1e-8, g) * RE
routes = {"DUST a4.36": (res["DUST"]["logM"]["alphaCO 4.36 (primary)"], 0.2)}
if "CO43" in res and res["CO43"]["logM"]: routes["CO43 r41 0.37"] = (res["CO43"]["logM"]["r41 0.37"], 0.2)
if "CI10" in res and res["CI10"]["logM"]: routes["CI10 X1.9e-5 (3sig UL)"] = (res["CI10"]["logM"]["X_CI 1.9e-5"], 0.2)
P("\n=== Delta_v = log(V_bar,meas^2 / V_bar,req^2) at Re 7.39 kpc (positive = more baryons than the model allows) ===")
dvres = {}
for lm in ("10.89", "10.76", "11.1"):
    for rn, (lg, sg) in routes.items():
        row = []
        for fn in ("canon 9.36e-11", "alt 1.13e-10"):
            for mn in RAT:
                vr = vreq2(fn, mn, lm)
                f = lambda dl, ds: math.log10((v2e(10 ** (float(lm) + ds)) + v2e(10 ** (lg + dl))) / vr)
                d0 = f(0, 0); e = 0.5 * math.hypot(f(sg, 0) - f(-sg, 0), f(0, 0.1) - f(0, -0.1))
                ten = "tension" if abs(d0) > 2 * e else "consistent"
                dvres[f"{lm}|{rn}|{fn}|{mn}"] = dict(dv=d0, err=e, verdict=ten); row.append(f"{mn}[{fn[:5]}] {d0:+.2f}+-{e:.2f} {ten[:4]}")
        nw = math.log10((v2e(10 ** float(lm)) + v2e(10 ** lg)) / VC ** 2); st = math.log10(v2e(10 ** float(lm)) / VC ** 2)
        dvres[f"{lm}|{rn}|Newton-max"] = dict(dv=nw, stars_only=st)
        P(f"  M* {lm}{' (post-freeze, reported only)' if lm == '11.1' else ''} | {rn}: " + "; ".join(row) + f" || Newton max-baryon (V_bar = V_c) {nw:+.2f}; stars alone vs V_c^2 {st:+.2f}")

json.dump(dict(controls=CHK, measured=res, cfg571=cmp, delta_v=dvres if not MUT else None, spectra={ln: dict(v=m["v"], spec=m["spec"], S=m["S"], sig=m["sig"]) for ln, m in meas.items()}, D_L_Mpc=DL),
          open(os.path.join(HERE, f"cfg572_gas{TAG}_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg572_gas{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg572_gas_results.json")))["measured"]
    anydet = any(base[l]["detected"] for l in LINES if l in base)
    if any(res[l].get("out_of_band") for l in LINES if l in res and base[l]["detected"]):
        P("MUTATE as frozen (+2000 km/s) NOT RUNNABLE: the window leaves the spectral coverage; see the disclosed --mutate1000 variant")
        open(os.path.join(HERE, f"cfg572_gas{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)
    drop = all((not base[l]["detected"]) or (not res[l]["detected"]) for l in LINES if l in base)
    P(f"MUTATE (+{VSHIFT:.0f} km/s window): {'detected (exit 1)' if anydet and drop else ('non-diagnostic: no line detected at the true z' if not anydet else 'NOT detected')}")
    open(os.path.join(HERE, f"cfg572_gas{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if (anydet and drop) else 0)
sys.exit(0 if all(ok for _, ok in CHK) else 1)

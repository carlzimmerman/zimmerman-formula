#!/usr/bin/env python3
"""VARIANT of euc5_a1_fit.py for RESULT.md section 3e (2026-11-12, evening): one line differs, the F1 mock is built from
the single 10 Gyr solar template that AMENDMENT_A1.md names instead of the two-template mix.  Run with --f1-only
(it then writes nothing); the output is euc5_a1_f1literal.out.  Everything below is euc5_a1_fit.py unchanged.

EUC5 AMENDMENT A1, step 1: stellar velocity dispersions fitted to the public DESI DR1 spectra of Euclid lens galaxies.

Amendment: AMENDMENT_A1.md (commit 286752fa9c), sections A1.1-A1.3 and A1.5.  pPXF, E-MILES BaSTI templates.
Nothing is downloaded: the spectra are EUC2's (desi_spectra/), the templates are already in _external_data.

Run:  python3 -I euc5_a1_fit.py --data-dir <ECLIPSE dir with desi_spectra/> --templates <dir of E-MILES fits files>
Writes euc5_a1_dispersions.csv and euc5_a1_fit.out / euc5_a1_fit.json (validation F1, F3) next to this script.
"""
import argparse, csv, glob, json, math, os, sys, time
import numpy as np
from astropy.io import fits
from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E
C_KMS = 299792.458
FWHM_TPL = 2.51
DEGREE, MDEGREE, TAG = 8, 0, "a1"          # A1 as frozen; --config changes these (see AMENDMENT_A2.md)
EMISSION = [3727.09, 3729.88, 3869.86, 4102.89, 4341.68, 4862.68, 4960.30, 5008.24]      # vacuum, rest
OBS_BAD = [(5570.0, 5590.0), (6290.0, 6310.0), (6860.0, 6960.0), (7590.0, 7700.0)]
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def load_templates(tdir):
    fs = sorted(glob.glob(os.path.join(tdir, "Ebi1.30Z*T*_iTp0.00_baseFe.fits")))
    h = fits.getheader(fs[0]); lam_air = h["CRVAL1"] + h["CDELT1"] * np.arange(h["NAXIS1"])
    lam = util.air_to_vac(lam_air); keep = (lam >= 3400.0) & (lam <= 6100.0)
    return lam[keep], np.array([fits.getdata(f)[keep] for f in fs]).T, [os.path.basename(f) for f in fs]

class Fitter:
    def __init__(self, tdir):
        self.lam_t, self.T, self.names = load_templates(tdir)
        self.cache = {}
    def templates(self, velscale):
        key = round(velscale, 3)
        if key not in self.cache:
            # the vacuum grid is very nearly linear over this range; resample onto an exactly linear grid first
            lin = np.linspace(self.lam_t[0], self.lam_t[-1], len(self.lam_t))
            Tl = np.array([np.interp(lin, self.lam_t, self.T[:, j]) for j in range(self.T.shape[1])]).T
            tn, ln_t, _ = util.log_rebin([lin[0], lin[-1]], Tl, velscale=velscale)
            self.cache[key] = (tn / np.median(tn), np.exp(ln_t))
        return self.cache[key]
    def fit(self, wl, flux, ivar, mask, ws, z):
        rest = wl / (1.0 + z)
        seg = (rest >= 3750.0) & (rest <= 5600.0) & (wl >= 3650.0) & (wl <= 9700.0)
        if seg.sum() < 1000: return None
        i0, i1 = np.where(seg)[0][[0, -1]]; sl = slice(i0, i1 + 1)
        lam = rest[sl]; f = flux[sl].astype(float); iv = ivar[sl].astype(float); wo = wl[sl]
        good = (iv > 0) & (mask[sl] == 0) & np.isfinite(f)
        for l0 in EMISSION: good &= np.abs(lam - l0) > 10.0
        for a, b in OBS_BAD: good &= ~((wo >= a) & (wo <= b))
        var = np.where(iv > 0, 1.0 / np.where(iv > 0, iv, 1.0), np.nan)
        var = np.where(np.isfinite(var), var, np.nanmedian(var) * 1e4)
        fl = np.where(np.isfinite(f), f, 0.0)
        g, ln_lam, velscale = util.log_rebin([lam[0], lam[-1]], fl)
        v, _, _ = util.log_rebin([lam[0], lam[-1]], var, velscale=velscale)
        gd, _, _ = util.log_rebin([lam[0], lam[-1]], good.astype(float), velscale=velscale)
        n = min(len(g), len(v), len(gd)); g, v, gd, ln_lam = g[:n], v[:n], gd[:n], ln_lam[:n]
        ok = gd > 0.99; norm = np.median(g[ok]) if ok.sum() > 100 else 0.0
        if not norm > 0 or ok.sum() < 800: return None
        gal = g / norm; noise = np.sqrt(np.maximum(v, 1e-30)) / norm
        tem, lam_tem = self.templates(velscale)
        kw = dict(moments=2, degree=DEGREE, mdegree=MDEGREE, lam=np.exp(ln_lam), lam_temp=lam_tem, quiet=True)
        try:
            pp = ppxf(tem, gal, noise, velscale, [0.0, 200.0], goodpixels=np.where(ok)[0], **kw)
            ok2 = ok & (np.abs((gal - pp.bestfit) / noise) < 3.0)
            if ok2.sum() < 800: return None
            pp = ppxf(tem, gal, noise, velscale, [float(pp.sol[0]), float(max(pp.sol[1], 50.0))], goodpixels=np.where(ok2)[0], **kw)
        except Exception:
            return None
        lam_mean = float(np.mean(np.exp(ln_lam)[ok2]))
        s_tpl = FWHM_TPL / 2.3548200450309493 / lam_mean * C_KMS
        s_ins = float(np.median(C_KMS * ws[sl][good] / wo[good]))
        s2 = pp.sol[1] ** 2 + s_tpl ** 2 - s_ins ** 2
        err = float(pp.error[1] * math.sqrt(max(pp.chi2, 1.0)))
        return dict(sigma=float(math.sqrt(s2)) if s2 > 0 else float("nan"), err=err, sigma_fit=float(pp.sol[1]), V=float(pp.sol[0]), chi2=float(pp.chi2),
                    npix=int(ok2.sum()), snr=float(np.median(gal[ok2] / noise[ok2])), s_tpl=s_tpl, s_ins=s_ins)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--templates", required=True)
    ap.add_argument("--degree", type=int, default=8); ap.add_argument("--mdegree", type=int, default=0); ap.add_argument("--tag", default="a1")
    ap.add_argument("--f1-only", action="store_true", help="mock recovery only; writes nothing")
    a = ap.parse_args(); t0 = time.time()
    global DEGREE, MDEGREE, TAG
    DEGREE, MDEGREE, TAG = a.degree, a.mdegree, a.tag
    sdir = os.path.join(a.data_dir, "desi_spectra")
    F = Fitter(a.templates)
    P("EUC5 %s fit: pPXF, additive degree %d, multiplicative degree %d, %d E-MILES BaSTI templates (bimodal 1.30), vacuum wavelengths %.0f-%.0f A" % (TAG.upper(), DEGREE, MDEGREE, F.T.shape[1], F.lam_t[0], F.lam_t[-1]))
    rows, _ = E.load(a.data_dir); E.OUT.clear()
    Sm, _ = E.select(rows, ("A", "B")); byid = {r["id"]: r for r in Sm}
    M = [m for m in csv.DictReader(open(os.path.join(HERE, "..", "EUC2_desi_source_hunt", "euc2_matches.csv"))) if m["unique_identifier"] in byid]
    todo = []
    for m in M:
        k = byid[m["unique_identifier"]]; zd = float(m["z_desi"]); zw = int(float(m["zwarn"]))
        if m["flagged"] == "True": zref = float(m["desi_deflector_specz"])
        elif zw == 0 and (k["zlo"] - 0.1) <= zd <= (k["zhi"] + 0.1): zref = zd
        else: continue
        if os.path.exists(os.path.join(sdir, m["sparcl_id"] + ".npz")): todo.append((m, zref))
    P("deflector spectra of sample-S lenses on disk: %d on %d lenses (flagged %d)"
      % (len(todo), len({m["unique_identifier"] for m, _ in todo}), sum(m["flagged"] == "True" for m, _ in todo)))

    # ---------------------------------------------------------------- fit everything first (no b is computed here)
    res = []
    for m, zref in todo:
        sp = np.load(os.path.join(sdir, m["sparcl_id"] + ".npz"))
        r = F.fit(sp["wavelength"], sp["flux"], sp["ivar"], sp["mask"], sp["wave_sigma"], zref)
        if r is None: continue
        res.append(dict(unique_identifier=m["unique_identifier"], sparcl_id=m["sparcl_id"], primary=m["specprimary"], z_ref=zref, **r))
    P("fits returned: %d" % len(res))

    # ---------------------------------------------------------------- F1 recovery on a real grid with real noise
    snr_all = sorted((r["snr"], r["sparcl_id"]) for r in res)
    med_id = snr_all[len(snr_all) // 2][1]
    sp = np.load(os.path.join(sdir, med_id + ".npz")); wl = sp["wavelength"].astype(float); ws = sp["wave_sigma"].astype(float)
    iv = sp["ivar"].astype(float); msk = sp["mask"]; zm = 0.45
    names = F.names
    def col(tag): return [j for j, nm in enumerate(names) if tag in nm][0]
    mix = F.T[:, col("Zp0.06T10.0000")] / np.median(F.T[:, col("Zp0.06T10.0000")])          # F1 as AMENDMENT_A1.md words it: one 10 Gyr solar template
    lam_fine = np.linspace(F.lam_t[0], F.lam_t[-1], 4 * len(F.lam_t)); mix_f = np.interp(lam_fine, F.lam_t, mix)
    rng = np.random.default_rng(E.SEED); F1 = {}
    realf = sp["flux"].astype(float); gdp = (iv > 0) & (msk == 0)
    snr_real = float(np.median(np.abs(realf[gdp]) * np.sqrt(iv[gdp])))
    for s_in in (150.0, 250.0, 350.0):
        lam_obs_rest = wl / (1.0 + zm)
        s_ins_v = float(np.median(C_KMS * ws / wl)); s_tpl_v = FWHM_TPL / 2.3548200450309493 / 4700.0 * C_KMS
        s_k = math.sqrt(max(s_in ** 2 + s_ins_v ** 2 - s_tpl_v ** 2, 1.0))
        dv = C_KMS * (lam_fine[1] - lam_fine[0]) / 4700.0                      # km/s per fine pixel near the middle
        # broaden in log-lambda by resampling onto a constant-velocity grid
        lnl = np.linspace(math.log(lam_fine[0]), math.log(lam_fine[-1]), len(lam_fine)); vstep = C_KMS * (lnl[1] - lnl[0])
        fl_ln = np.interp(np.exp(lnl), lam_fine, mix_f)
        kx = np.arange(-int(6 * s_k / vstep) - 1, int(6 * s_k / vstep) + 2) * vstep; ker = np.exp(-0.5 * (kx / s_k) ** 2); ker /= ker.sum()
        br = np.convolve(fl_ln, ker, mode="same")
        model = np.interp(lam_obs_rest, np.exp(lnl), br) * (1.0 + 0.15 * (wl - 6500.0) / 3000.0)
        ok = np.isfinite(model) & (lam_obs_rest > F.lam_t[0] + 50) & (lam_obs_rest < F.lam_t[-1] - 50)
        sig_n = np.where(iv > 0, 1.0 / np.sqrt(np.where(iv > 0, iv, 1.0)), 0.0)
        scale = snr_real * np.median(sig_n[gdp]) / np.median(model[ok])
        rec = []
        for _ in range(40):
            fmock = np.where(ok, model * scale, 0.0) + rng.standard_normal(len(wl)) * sig_n
            r = F.fit(wl, fmock, np.where(ok, iv, 0.0), msk, ws, zm)
            if r is not None and np.isfinite(r["sigma"]): rec.append(r["sigma"])
        F1[s_in] = dict(n=len(rec), median=float(np.median(rec)) if rec else float("nan"), sd=float(np.std(rec)) if rec else float("nan"))
        P("  F1 input %3.0f km/s: recovered median %.1f (sd %.1f, %d of 40 fits), ratio %.3f" % (s_in, F1[s_in]["median"], F1[s_in]["sd"], len(rec), F1[s_in]["median"] / s_in))
    okF1 = all(abs(F1[s]["median"] / s - 1.0) <= 0.05 for s in F1)
    P("  %s F1  recovery within 5%% at all three (noise and grid of spectrum %s, median S/N %.1f per pixel)" % ("PASS" if okF1 else "FAIL", med_id[:8], snr_real))

    if a.f1_only: return
    # ---------------------------------------------------------------- F3 repeat spectra
    by = {}
    for r in res: by.setdefault(r["unique_identifier"], []).append(r)
    rep = [(v[0]["sigma"], v[0]["err"], v[1]["sigma"], v[1]["err"]) for v in by.values() if len(v) >= 2 and all(np.isfinite(x["sigma"]) for x in v[:2])]
    if rep:
        pull = [(a_ - c_) / math.hypot(b_, d_) for a_, b_, c_, d_ in rep]
        P("  F3  lenses with two DESI spectra: %d; median |ratio - 1| = %.3f; rms pull = %.2f" % (len(rep), np.median([abs(a_ / c_ - 1) for a_, b_, c_, d_ in rep]), float(np.sqrt(np.mean(np.square(pull))))))
    with open(os.path.join(HERE, "euc5_%s_dispersions.csv" % TAG), "w", newline="") as f:
        cols = ["unique_identifier", "sparcl_id", "primary", "z_ref", "sigma", "err", "sigma_fit", "V", "chi2", "npix", "snr", "s_tpl", "s_ins"]
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in res: w.writerow({k: (("%.4f" % r[k]) if isinstance(r[k], float) else r[k]) for k in cols})
    q = [r for r in res if np.isfinite(r["sigma"]) and 70 <= r["sigma"] <= 500 and r["err"] / r["sigma"] <= 0.25 and abs(r["V"]) <= 300 and r["npix"] >= 800]
    P("fits passing the quality cuts: %d spectra on %d lenses  (median sigma %.0f km/s, median error %.0f%%, median S/N %.1f)"
      % (len(q), len({r["unique_identifier"] for r in q}), np.median([r["sigma"] for r in q]), 100 * np.median([r["err"] / r["sigma"] for r in q]), np.median([r["snr"] for r in q])))
    json.dump(dict(F1={str(k): v for k, v in F1.items()}, F1_pass=bool(okF1), n_fits=len(res), n_pass=len(q), n_repeat=len(rep)), open(os.path.join(HERE, "euc5_%s_fit.json" % TAG), "w"), indent=1)
    P("(%.0f s)" % (time.time() - t0))
    open(os.path.join(HERE, "euc5_%s_fit.out" % TAG), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()

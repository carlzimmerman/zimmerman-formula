#!/usr/bin/env python3
"""
WALLABY PER-SIDE ROTATION-CURVE EXTRACTOR  (Door 5 prep -- directional-EFE scale-up)
=====================================================================================
PURPOSE
  The directional-EFE confrontation (banked: zimmerman-formula/real_research/reviews/
  directional_efe_2026/confrontation.out) needs N ~ 1,157 galaxies with SIGNED
  per-side rotation asymmetries (canonical a0=9.36e-11, max-clustering e_N,
  AQUAL-vs-BranchB at w=0.304, 3 sigma; N ~ 192-3057 for the AQUAL-amplitude band
  per laneB_FEASIBILITY.md).  WALLABY's WKAPP kinematic releases publish ONLY
  azimuthally-averaged flat-disk rotation curves (Deg et al. 2022 PASA 39 e059,
  Table 3: _ModRotCurve.fits carries a single VRot_model column -- no
  approaching/receding split).  BUT every catalogued source ships a SoFiA
  moment-1 velocity field (_mom1.fits, barycentric FREQUENCY in Hz) and every
  modelled source ships its tilted-ring geometry (_AvgMod.txt).  This script
  closes that gap: velocity field + geometry -> per-side outer rotation curves
  -> signed asymmetry
        A = 2 (v_app - v_rec) / (v_app + v_rec)
  (A > 0 means the APPROACHING side rotates faster) with a pixel-bootstrap error.

GATE (run first, always): synthetic WALLABY-like velocity field with a KNOWN
  injected aligned asymmetry A_true = +2% + realistic beam smearing + moment-1
  noise, at two resolutions (6-beam and 3.5-beam marginal case), plus a null
  (A_true = 0).  Recovery, bias, and bootstrap-pull calibration are printed
  honestly; the verdict is COMPUTED, not asserted.

PILOT (real data, labeled PILOT): if pilot_data/ holds the fetched WALLABY
  products (3 galaxies; fetch list below, CADC raven service), the extractor
  runs on the real moment-1 maps using the released WKAPP geometry, and its
  azimuthal-average is cross-checked against the released WKAPP VRot_model.

CONVENTIONS / SOURCES
  - WKAPP PA is the position angle of the RECEDING major axis, N through E
    (tilted-ring convention; FAT + 3DBarolo, Deg et al. 2022 sec. 4).
    PA_model_g is the global (on-sky WCS) value -- that is the one used here.
  - mom1 is SoFiA barycentric frequency: cz = c*(f0/f - 1), f0 = 1420405751.77 Hz.
  - a0 does not enter this extractor (it is a measurement tool); the a0 footing
    fork enters only at the confrontation stage (both footings banked in
    confrontation.out: N=1157 canonical / N=1424 alt, max-clustering).

DATA PROVENANCE (all public, anonymous access):
  CADC:  https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/raven/files/cadc:WALLABY/<file>
  CASDA: https://data.csiro.au (WALLABY PDR1 DOI 10.25919/09yg-d016 et seq.)
  Papers: Westmeier+2022 (PDR1 sources), Deg+2022 (PDR1 WKAPP kinematic models),
          Murugeshan+2024 arXiv:2409.13130 (PDR2 ~1800 sources + >120 models).

exit 0 on completion (gate verdicts are printed, honest FAIL is reportable).
"""
import os, sys, math, json
import numpy as np

try:
    from astropy.io import fits
    from astropy.wcs import WCS
    HAVE_ASTROPY = True
except ImportError:
    HAVE_ASTROPY = False

HERE = os.path.dirname(os.path.abspath(__file__))
PILOT_DIR = os.path.join(HERE, "pilot_data")
C_KMS = 299792.458
F0_HI = 1420405751.77  # Hz

RNG = np.random.default_rng(20260716)

# ----------------------------------------------------------------------------
# Core geometry + per-side estimator
# ----------------------------------------------------------------------------
def disk_coords(nx, ny, x0, y0, pix_as, pa_deg, inc_deg):
    """Sky grid -> deprojected disk-plane radius R ('') and cos(theta), with
    theta measured from the RECEDING major axis (PA convention: N through E).
    Pixel axes: x = column (RA decreases with +x is NOT assumed; caller passes
    pix_as as (d_east_per_pixel_x, d_north_per_pixel_y) in arcsec)."""
    y, x = np.mgrid[0:ny, 0:nx]
    dE = (x - x0) * pix_as[0]   # arcsec toward East
    dN = (y - y0) * pix_as[1]   # arcsec toward North
    pa = math.radians(pa_deg)
    x_maj = dE * math.sin(pa) + dN * math.cos(pa)     # along receding major axis
    y_min = -dE * math.cos(pa) + dN * math.sin(pa)    # perpendicular
    cosi = math.cos(math.radians(inc_deg))
    y_dep = y_min / max(cosi, 1e-6)
    R = np.hypot(x_maj, y_dep)
    with np.errstate(invalid="ignore", divide="ignore"):
        cth = np.where(R > 0, x_maj / R, 0.0)
    return R, cth


def perside_rings(vfield_kms, weight, R, cth, vsys, inc_deg, ring_edges,
                  cos_min=0.5, clip_kms=600.0):
    """Per-ring, per-side deprojected rotation speeds.
    Returns dict ring -> {'app': (v, n), 'rec': (v, n)} using an
    intensity-weighted mean of v_rot = (v_los - vsys)/(sin i * cos th)
    over pixels with |cos th| >= cos_min (wedge near the major axis)."""
    sini = math.sin(math.radians(inc_deg))
    dv = vfield_kms - vsys
    ok = np.isfinite(vfield_kms) & (np.abs(dv) < clip_kms) & (np.abs(cth) >= cos_min)
    if weight is None:
        weight = np.ones_like(vfield_kms)
    ok &= np.isfinite(weight) & (weight > 0)
    vrot = np.full_like(dv, np.nan)
    vrot[ok] = dv[ok] / (sini * cth[ok])
    out = {}
    for k in range(len(ring_edges) - 1):
        sel = ok & (R >= ring_edges[k]) & (R < ring_edges[k + 1])
        ring = {}
        for side, m in (("rec", sel & (cth > 0)), ("app", sel & (cth < 0))):
            v, w = vrot[m], weight[m]
            if v.size >= 4:
                # 3-sigma clip once (robustness to mom1 junk pixels)
                mu = np.average(v, weights=w)
                sd = math.sqrt(max(np.average((v - mu) ** 2, weights=w), 1e-12))
                g = np.abs(v - mu) < 3 * sd
                if g.sum() >= 4:
                    v, w = v[g], w[g]
                ring[side] = (float(np.average(v, weights=w)), int(v.size),
                              v.copy(), w.copy())
        if "app" in ring and "rec" in ring:
            out[k] = ring
    return out


def signed_asymmetry(rings, outer_keys):
    """A = 2(v_app - v_rec)/(v_app + v_rec) over the outer rings (ring-mean)."""
    va = [rings[k]["app"][0] for k in outer_keys if k in rings]
    vr = [rings[k]["rec"][0] for k in outer_keys if k in rings]
    if not va or not vr:
        return None, None, None
    va, vr = float(np.mean(va)), float(np.mean(vr))
    A = 2.0 * (va - vr) / (va + vr)
    return A, va, vr


def bootstrap_A(rings, outer_keys, nboot=400):
    """Pixel bootstrap within each (ring, side)."""
    As = []
    for _ in range(nboot):
        va_l, vr_l = [], []
        for k in outer_keys:
            if k not in rings:
                continue
            r = rings[k]
            for side, acc in (("app", va_l), ("rec", vr_l)):
                v, w = r[side][2], r[side][3]
                idx = RNG.integers(0, v.size, v.size)
                acc.append(np.average(v[idx], weights=w[idx]))
        if va_l and vr_l:
            va, vr = np.mean(va_l), np.mean(vr_l)
            As.append(2.0 * (va - vr) / (va + vr))
    if len(As) < 10:
        return None
    return float(np.std(As, ddof=1))


def extract(vfield_kms, weight, geom, ring_edges, outer_frac=0.5,
            cos_min=0.5, nboot=400, pix_as=None, nxny=None):
    """Full extraction. geom = dict(x0, y0, pa_deg, inc_deg, vsys).
    Returns dict with A, sigma_A, per-ring per-side curves."""
    ny, nx = vfield_kms.shape
    R, cth = disk_coords(nx, ny, geom["x0"], geom["y0"],
                         pix_as, geom["pa_deg"], geom["inc_deg"])
    rings = perside_rings(vfield_kms, weight, R, cth, geom["vsys"],
                          geom["inc_deg"], ring_edges, cos_min=cos_min)
    if not rings:
        return None
    kmax = max(rings.keys())
    r_out_min = outer_frac * ring_edges[kmax + 1]
    outer = [k for k in rings if 0.5 * (ring_edges[k] + ring_edges[k + 1]) >= r_out_min]
    if not outer:
        outer = [kmax]
    A, va, vr = signed_asymmetry(rings, outer)
    if A is None:
        return None
    sA = bootstrap_A(rings, outer, nboot=nboot)
    curves = {k: {"R_mid": 0.5 * (ring_edges[k] + ring_edges[k + 1]),
                  "v_app": rings[k]["app"][0], "n_app": rings[k]["app"][1],
                  "v_rec": rings[k]["rec"][0], "n_rec": rings[k]["rec"][1]}
              for k in sorted(rings)}
    return {"A": A, "sigma_A": sA, "v_app_outer": va, "v_rec_outer": vr,
            "outer_rings": sorted(outer), "curves": curves}


# ----------------------------------------------------------------------------
# Synthetic gate
# ----------------------------------------------------------------------------
def gaussian_convolve(img, sigma_pix):
    """FFT Gaussian convolution, NaN-safe (NaN treated as zero weight)."""
    ny, nx = img.shape
    ky = np.fft.fftfreq(ny)[:, None]
    kx = np.fft.fftfreq(nx)[None, :]
    ker = np.exp(-2.0 * (math.pi * sigma_pix) ** 2 * (kx ** 2 + ky ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(img) * ker))


def make_synthetic(A_true=0.02, beams_across=6.0, beam_as=30.0, pix_as=6.0,
                   inc_deg=60.0, pa_deg=42.0, vflat=120.0, vsys=1500.0,
                   sig_v=4.0, npix=200, seed=None):
    """WALLABY-like moment-1 map with an injected aligned per-side asymmetry.
      v_c(R, theta) = v_arctan(R) * (1 - (A_true/2) cos theta)
    so the azimuthal receding/approaching extremes give exactly
      A = 2(v_app - v_rec)/(v_app + v_rec) = A_true.
    Beam smearing: intensity-weighted convolution of the LOS field (the
    standard moment-1 smearing mechanism), then pixel noise sig_v/sqrt(w)."""
    rng = np.random.default_rng(seed)
    R_hi = 0.5 * beams_across * beam_as              # HI radius in arcsec
    x0 = y0 = npix / 2.0
    R, cth = disk_coords(npix, npix, x0, y0, (pix_as, pix_as), pa_deg, inc_deg)
    # arctan rotation curve, turnover at 0.25 R_hi
    vc = vflat * (2.0 / math.pi) * np.arctan(R / (0.25 * R_hi))
    vc = vc * (1.0 - 0.5 * A_true * cth)             # injected asymmetry
    sini = math.sin(math.radians(inc_deg))
    vlos = vsys + vc * sini * cth
    # exponential HI disk (face-on) -> projected intensity
    intens = np.exp(-R / (0.5 * R_hi))
    intens[R > 1.3 * R_hi] = 0.0
    sig_pix = (beam_as / 2.3548) / pix_as
    num = gaussian_convolve(intens * vlos, sig_pix)
    den = gaussian_convolve(intens, sig_pix)
    with np.errstate(invalid="ignore", divide="ignore"):
        v_obs = num / den
    mask = den > 0.05 * np.nanmax(den)               # SoFiA-like mask
    v_obs = np.where(mask, v_obs, np.nan)
    noise = rng.normal(0.0, sig_v, v_obs.shape) / np.sqrt(np.maximum(den / np.nanmax(den), 0.05))
    v_obs = v_obs + np.where(mask, noise, 0.0)
    w = np.where(mask, den, np.nan)
    geom = {"x0": x0, "y0": y0, "pa_deg": pa_deg, "inc_deg": inc_deg, "vsys": vsys}
    ring_edges = np.arange(0.0, 1.2 * R_hi, 0.5 * beam_as)
    return v_obs, w, geom, ring_edges, (pix_as, pix_as)


def run_gate(n_real=30):
    print("=" * 78)
    print("GATE: synthetic recovery of an injected ALIGNED per-side asymmetry")
    print("=" * 78)
    verdicts = {}
    cases = [
        ("6.0-beam, A_true=+2%",  dict(A_true=0.02, beams_across=6.0)),
        ("3.5-beam (marginal), A_true=+2%", dict(A_true=0.02, beams_across=3.5)),
        ("6.0-beam NULL, A_true=0", dict(A_true=0.0, beams_across=6.0)),
    ]
    for label, kw in cases:
        As, sAs = [], []
        for i in range(n_real):
            v, w, geom, edges, pix = make_synthetic(seed=1000 + i, **kw)
            res = extract(v, w, geom, edges, pix_as=pix, nboot=200)
            if res and res["sigma_A"]:
                As.append(res["A"]); sAs.append(res["sigma_A"])
        As, sAs = np.array(As), np.array(sAs)
        a_true = kw["A_true"]
        mean_A = As.mean(); rms = As.std(ddof=1); sem = rms / math.sqrt(len(As))
        pulls = (As - a_true) / sAs
        bias = mean_A - a_true
        # honest, computed verdicts
        unbiased = abs(bias) < max(3 * sem, 0.10 * abs(a_true) if a_true else 3 * sem)
        pull_ok = 0.6 < pulls.std(ddof=1) < 1.8
        sign_ok = (a_true == 0) or (np.sign(mean_A) == np.sign(a_true))
        ok = unbiased and pull_ok and sign_ok
        verdicts[label] = ok
        print(f"\n  [{label}]  n_real={len(As)}")
        print(f"    <A_hat> = {mean_A:+.5f}   (true {a_true:+.5f}; bias {bias:+.5f} +/- {sem:.5f})")
        print(f"    per-realization rms(A_hat) = {rms:.5f};  <sigma_boot> = {sAs.mean():.5f}")
        print(f"    pull rms = {pulls.std(ddof=1):.2f}  (1.0 = calibrated errors)")
        print(f"    sign recovered: {sign_ok};  unbiased: {unbiased};  pulls calibrated: {pull_ok}")
        print(f"    --> {'PASS' if ok else 'FAIL'}")
    all_ok = all(verdicts.values())
    msg = ("PASS -- 2% aligned asymmetry recovered, errors calibrated" if all_ok
           else "FAIL -- see case lines above (honest fail)")
    print(f"\n  GATE VERDICT: {msg}")
    return all_ok, verdicts


# ----------------------------------------------------------------------------
# Real-data pilot (labeled PILOT)
# ----------------------------------------------------------------------------
PILOT_GALAXIES = [
    # (name, mom1, mom0, AvgMod, ModRotCurve)   -- all under CADC raven, cadc:WALLABY/
    ("WALLABY J125548+041805 (NGC4808 field, 12'' high-res)",
     "WALLABY_J125548+041805_NGC_4808_High-Res_TR1_mom1.fits",
     "WALLABY_J125548+041805_NGC_4808_High-Res_TR1_mom0.fits",
     "WALLABY_J125548+041805_NGC_4808_High-Res_Kin_TR1_AvgMod.txt",
     "WALLABY_J125548+041805_NGC_4808_High-Res_Kin_TR1_ModRotCurve.fits", 12.0),
    ("WALLABY J165901-601241 (Norma field, 30'')",
     "WALLABY_J165901-601241_Norma_TR1_mom1.fits",
     "WALLABY_J165901-601241_Norma_TR1_mom0.fits",
     "WALLABY_J165901-601241_Norma_Kin_TR1_AvgMod.txt",
     "WALLABY_J165901-601241_Norma_Kin_TR1_ModRotCurve.fits", 30.0),
    ("WALLABY J100426-282638 (Hydra field, 30''; Deg+22 showcase)",
     "WALLABY_J100426-282638_Hydra_TR2_mom1.fits",
     "WALLABY_J100426-282638_Hydra_TR2_mom0.fits",
     "WALLABY_J100426-282638_Hydra_Kin_TR2_AvgMod.txt",
     "WALLABY_J100426-282638_Hydra_Kin_TR2_ModRotCurve.fits", 30.0),
]
RAVEN = "https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/raven/files/cadc:WALLABY/"


def fetch_pilot():
    import urllib.request, urllib.parse
    os.makedirs(PILOT_DIR, exist_ok=True)
    for row in PILOT_GALAXIES:
        for fn in row[1:5]:
            p = os.path.join(PILOT_DIR, fn)
            if not os.path.exists(p):
                url = RAVEN + urllib.parse.quote(fn)
                print(f"  [fetch] {fn}")
                urllib.request.urlretrieve(url, p)


def parse_avgmod(path):
    """Parse the WKAPP _AvgMod.txt: geometry block + rotation-curve block."""
    geom, rc = {}, []
    mode = None
    for line in open(path):
        t = line.strip()
        if t.startswith("Geometry Parameters"):
            mode = "geo"; continue
        if t.startswith("Rotation Curve"):
            mode = "rc"; continue
        if t.startswith("Surface Density"):
            mode = None; continue
        if mode == "geo" and "\t" in t:
            parts = [p.strip() for p in t.split("\t") if p.strip()]
            if len(parts) >= 2:
                key = parts[0].split("(")[0].strip()
                try:
                    geom[key] = float(parts[1])
                except ValueError:
                    pass
        elif mode == "rc":
            parts = t.split()
            if len(parts) >= 3:
                try:
                    rc.append((float(parts[0]), float(parts[1]), float(parts[2])))
                except ValueError:
                    pass
    return geom, rc


def run_pilot():
    print("\n" + "=" * 78)
    print("PILOT (real WALLABY data, labeled PILOT -- proof-of-life, N=3)")
    print("=" * 78)
    if not HAVE_ASTROPY:
        print("  astropy not available -> pilot SKIPPED (gate above is self-contained)")
        return []
    missing = [fn for row in PILOT_GALAXIES for fn in row[1:5]
               if not os.path.exists(os.path.join(PILOT_DIR, fn))]
    if missing:
        try:
            fetch_pilot()
        except Exception as e:
            print(f"  network fetch failed ({e}) -> pilot SKIPPED")
            return []
    results = []
    for name, f_m1, f_m0, f_avg, f_rc, beam_as in PILOT_GALAXIES:
        print(f"\n  --- {name} ---")
        geo, rc = parse_avgmod(os.path.join(PILOT_DIR, f_avg))
        hdu1 = fits.open(os.path.join(PILOT_DIR, f_m1))[0]
        hdu0 = fits.open(os.path.join(PILOT_DIR, f_m0))[0]
        w = WCS(hdu1.header)
        # mom1 Hz -> cz km/s (optical convention, barycentric)
        with np.errstate(invalid="ignore", divide="ignore"):
            vmap = C_KMS * (F0_HI / hdu1.data - 1.0)
        # geometry: WKAPP global PA (receding side, N->E), model center via WCS
        x0, y0 = w.wcs_world2pix([[geo["RA_model"], geo["DEC_model"]]], 0)[0]
        pix_e = -hdu1.header["CDELT1"] * 3600.0   # RA axis: East is -x if CDELT1<0
        pix_n = hdu1.header["CDELT2"] * 3600.0
        # disk_coords wants d_east per +x pixel: with CDELT1<0, +x is WEST -> pass
        # pix_as[0] = CDELT1*3600 (negative) so that dE = (x-x0)*CDELT1*3600 is correct.
        pix_as = (hdu1.header["CDELT1"] * 3600.0, pix_n)
        pa = geo.get("PA_model_g", geo.get("PA_model"))
        geom = {"x0": float(x0), "y0": float(y0), "pa_deg": pa,
                "inc_deg": geo["Inc_model"], "vsys": geo["VSys_model"]}
        rads = np.array([r[0] for r in rc])
        dr = np.median(np.diff(rads)) if len(rads) > 1 else 0.5 * beam_as
        ring_edges = np.concatenate([[max(rads[0] - dr / 2, 0.0)], rads + dr / 2])
        res = extract(vmap, hdu0.data, geom, ring_edges, pix_as=pix_as, nboot=400)
        if res is None:
            print("    extraction returned no valid rings -> honest null for this galaxy")
            continue
        # sanity cross-check vs released WKAPP azimuthally-averaged curve
        print(f"    inc={geom['inc_deg']:.1f} deg  PA_g={pa:.1f} deg  vsys={geom['vsys']:.1f} km/s")
        print(f"    ring   R('')    v_app    v_rec    (WKAPP VRot)")
        for k, c in res["curves"].items():
            vw = ""
            j = np.argmin(np.abs(rads - c["R_mid"]))
            if abs(rads[j] - c["R_mid"]) < dr:
                vw = f"({rc[j][1]:7.1f})"
            tag = "  <- outer" if k in res["outer_rings"] else ""
            print(f"    {k:4d} {c['R_mid']:8.1f} {c['v_app']:8.1f} {c['v_rec']:8.1f}   {vw}{tag}")
        # azimuthal mean vs WKAPP over matched rings (sanity, not a gate)
        both, wk = [], []
        for k, c in res["curves"].items():
            j = np.argmin(np.abs(rads - c["R_mid"]))
            if abs(rads[j] - c["R_mid"]) < dr:
                both.append(0.5 * (c["v_app"] + c["v_rec"])); wk.append(rc[j][1])
        if both:
            fr = np.median(np.array(both) / np.array(wk))
            print(f"    sanity: median (per-side mean)/(WKAPP VRot) = {fr:.3f} over {len(both)} rings")
        print(f"    SIGNED PER-SIDE ASYMMETRY (outer rings):")
        print(f"      A = 2(v_app-v_rec)/(v_app+v_rec) = {res['A']:+.4f} +/- {res['sigma_A']:.4f}  [PILOT]")
        results.append({"galaxy": name, "A": res["A"], "sigma_A": res["sigma_A"],
                        "v_app_outer": res["v_app_outer"], "v_rec_outer": res["v_rec_outer"]})
    return results


# ----------------------------------------------------------------------------
def main():
    print(__doc__.split("GATE")[0].strip())
    gate_ok, _ = run_gate(n_real=30)
    pilot = run_pilot()
    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"  gate (synthetic 2% recovery): {'PASS' if gate_ok else 'FAIL'}")
    if pilot:
        for r in pilot:
            print(f"  PILOT {r['galaxy'][:44]:46s} A = {r['A']:+.4f} +/- {r['sigma_A']:.4f}")
        print("  NOTE: PILOT values are proof-of-life only (N=3, no g_ext vector,")
        print("        no warp/flat-disk systematics budget); they feed NO physics claim.")
    out = {"gate_pass": bool(gate_ok), "pilot": pilot}
    with open(os.path.join(HERE, "perside_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results written: {os.path.join(HERE, 'perside_results.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

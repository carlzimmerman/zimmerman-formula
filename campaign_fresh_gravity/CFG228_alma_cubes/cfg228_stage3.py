#!/usr/bin/env python3
"""CFG228 Stage 3 -- the ROTATION of the six ALPINE rotators from the cubes: a thin-disc forward model through the header's beam, fitted to the sub-cube (Stage 1 §3 of the frozen criteria).
Run ONLY after the blind pre-flight (0c4c5778d) was committed.  Exponential [CII] brightness with R_d = R_e,[CII]/1.678 fixed from Stage 1; V(R) = (2/pi) V_a arctan(R/R_t); constant sigma_0; PA, systemic velocity, V_a, R_t, sigma_0 and the
line flux FREE; the inclination FIXED at the corpus value (marginalised at the scoring stage).  Each channel model is convolved with the header's elliptical Gaussian beam (FFT).  chi^2 over the voxels inside the moment-0 S/N > 2 mask, per-voxel noise from the
line-free channels, parameter errors from the (J^T J)^-1 inflated by N_beam (beam-correlated noise) and by max(1, chi^2/n).  Planted-rotation recovery (C-ext) on the galaxy's OWN geometry, beam and noise.
Compilation; calibration-limited; not a detection; not a verdict.  LambdaCDM has no a0.  kappa = 1/2 FITTED.
Frozen criteria: FROZEN_CRITERIA.md here (71ec12282).  Run: python3 campaign_fresh_gravity/CFG228_alma_cubes/cfg228_stage3.py        (MUTATE=1: planted V_a x 1.5 in the recovery test)"""
import os, sys, math, json, glob, time
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from astropy.io import fits
from scipy.special import ndtr
from scipy.signal import fftconvolve
from scipy.optimize import least_squares
from scipy.ndimage import binary_dilation, uniform_filter
import multiprocessing as mp

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.pop("MUTATE", "").strip() == "1"
EXT = os.path.expanduser("~/new_physics/_external_data")
AL = os.path.join(EXT, "alpine_alma")
CLIGHT = 299792.458
SEED = 228
FN, HB = 2, 24                                                          # fine oversampling factor; half-width of the sub-cube in data pixels
NMOCK = 50
START = dict(Va=100.0, Rt=0.6, sig=60.0)                                # common starting values (different from the planted ones)
PLANT = dict(Va=150.0, Rt=1.0, sig=40.0)
TAGS = {"CG32": "CANDELS_GOODSS_32", "DC396844": "DEIMOS_COSMOS_396844", "DC494057": "DEIMOS_COSMOS_494057", "DC552206": "DEIMOS_COSMOS_552206", "DC881725": "DEIMOS_COSMOS_881725", "VC5110377875": "vuds_cosmos_5110377875"}
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


ST = pd.read_csv(os.path.join(LANE, "cfg228_stage1_static.csv")).set_index("gid")
MS = pd.read_csv(os.path.join(LANE, "cfg228_stage1_alpine_measurements.csv")).set_index("gid")
COR = pd.read_csv(os.path.join(REPO, "data_assembly", "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_galaxies.csv")).set_index("galaxy")
_CACHE = {}


def prepare(g):
    if g in _CACHE:
        return _CACHE[g]
    tag = TAGS[g]
    f = lambda k: glob.glob(os.path.join(AL, f"*{tag}.{k}"))[0]
    hc = fits.getheader(f("cube.image.fits"))
    cube = fits.getdata(f("cube.image.fits")).astype(np.float32)[0]
    pb = np.squeeze(fits.getdata(f("continuum.flux.fits.gz"))).astype(float)
    m = MS.loc[g]
    cy, cx = int(m.cy), int(m.cx)
    sub = cube[:, cy - HB:cy + HB, cx - HB:cx + HB] / pb[cy - HB:cy + HB, cx - HB:cx + HB][None].astype(np.float32)
    n3 = cube.shape[0]
    nu = hc["CRVAL3"] + (np.arange(1, n3 + 1) - hc["CRPIX3"]) * hc["CDELT3"]
    vel = CLIGHT * (hc["RESTFRQ"] - nu) / hc["RESTFRQ"]
    vpk = float(m.v_peak_kms)
    sel, free = np.abs(vel - vpk) <= 700, np.abs(vel - vpk) > 1000
    rms = float(np.std(sub[free]))
    pix = abs(hc["CDELT1"]) * 3600.0
    pixf = pix / FN
    kpa = float(ST.loc[g, "kpc_per_arcsec"]); Rd_kpc = float(ST.loc[g, "Re_kpc"]) / 1.678
    bmaj, bmin, bpa = hc["BMAJ"] * 3600, hc["BMIN"] * 3600, hc["BPA"]
    xf = (np.arange(2 * HB * FN) - (FN * HB + (FN - 1) / 2.0)) * pixf
    Xe = -xf[None, :] * np.ones((2 * HB * FN, 1)); Yn = xf[:, None] * np.ones((1, 2 * HB * FN))
    kh = int(math.ceil(3.0 * bmaj / (2 * math.sqrt(2 * math.log(2))) / pixf)) + 4
    kx = np.arange(-kh, kh + 1) * pixf
    KX, KY = np.meshgrid(-kx, kx)
    sb = math.radians(bpa); smaj, smin = bmaj / (2 * math.sqrt(2 * math.log(2))), bmin / (2 * math.sqrt(2 * math.log(2)))
    kern = np.exp(-0.5 * (((KX * math.sin(sb) + KY * math.cos(sb)) / smaj) ** 2 + ((KX * math.cos(sb) - KY * math.sin(sb)) / smin) ** 2))
    m0 = np.squeeze(fits.getdata(f("CIImom0.image.fits"))).astype(float) / pb
    far = np.hypot(*(np.indices(m0.shape) - np.array([cy, cx])[:, None, None])) * pix > 6
    sm0 = 1.4826 * np.nanmedian(np.abs(m0[far] - np.nanmedian(m0[far])))
    mask = binary_dilation(uniform_filter(np.nan_to_num(m0[cy - HB:cy + HB, cx - HB:cx + HB]), 3) > 2 * sm0, iterations=1)
    if mask.sum() < 30:
        mask = circ = np.hypot(*(np.indices(mask.shape) - HB)) * pix <= 1.5 * float(m.R_half_arcsec)
    D = dict(g=g, data=sub[sel].astype(float), vwin=vel[sel], dv=abs(vel[1] - vel[0]), rms=rms, mask=mask, Xe=Xe, Yn=Yn, kern=kern, kpa=kpa, Rd=Rd_kpc, vpk=vpk, inc=float(ST.loc[g, "inc_kin"]), pa0=float(COR.loc[g, "pa_kin_deg"]),
             S=float(m.S_CII), Nbeam=float(m.N_beam), R_out=float(ST.loc[g, "R_out_kpc"]), R15=float(ST.loc[g, "R_out_kpc_15"]), R30=float(ST.loc[g, "R_out_kpc_30"]), RJ=float(ST.loc[g, "jones_R_out_kpc"]), free_idx=np.where(free)[0], sel_idx=np.where(sel)[0],
             sub=sub, sigma_m0=sm0, pix=pix, kpa_arcsec=kpa)
    _CACHE[g] = D
    return D


def model(D, theta, inc=None):
    PA, vsys, Va, Rt, sig, flux = theta
    inc = D["inc"] if inc is None else inc
    c, s = math.cos(math.radians(PA)), math.sin(math.radians(PA))
    xmaj = D["Xe"] * s + D["Yn"] * c; xmin = D["Xe"] * c - D["Yn"] * s
    ci, si = math.cos(math.radians(inc)), math.sin(math.radians(inc))
    Rsky = np.sqrt(xmaj ** 2 + (xmin / ci) ** 2) + 1e-9
    Rk = Rsky * D["kpa"]
    Vr = (2 / math.pi) * Va * np.arctan(Rk / Rt)
    vlos = vsys + Vr * si * (xmaj / Rsky)
    I = np.exp(-Rk / D["Rd"]); I = I / I.sum()
    vw = D["vwin"][:, None, None]
    wch = np.abs(ndtr((vw + 0.5 * D["dv"] - vlos[None]) / sig) - ndtr((vw - 0.5 * D["dv"] - vlos[None]) / sig))
    cubef = flux / D["dv"] * I[None] * wch
    cc = fftconvolve(cubef, D["kern"][None], mode="same", axes=(1, 2))
    return cc.reshape(len(D["vwin"]), 2 * HB, FN, 2 * HB, FN).mean(axis=(2, 4))


def fit(D, data=None):
    data = D["data"] if data is None else data
    mask = D["mask"]
    resid = lambda th: ((data - model(D, th)) / D["rms"])[:, mask].ravel()
    lo = [-360, D["vpk"] - 250, 10, 0.2, 5, 0.05 * D["S"]]; hi = [720, D["vpk"] + 250, 800, 3.0, 250, 5 * D["S"]]
    best = None
    for pa0 in (D["pa0"], D["pa0"] + 180):
        th0 = [pa0, D["vpk"], START["Va"], START["Rt"], START["sig"], D["S"]]
        try:
            ft = least_squares(resid, th0, bounds=(lo, hi), x_scale=[30, 30, 50, 0.5, 20, 0.5], max_nfev=80)
        except Exception:
            continue
        if best is None or ft.cost < best.cost:
            best = ft
    return best, (lo, hi)


def vrot(theta, R):
    return (2 / math.pi) * theta[2] * math.atan(R / theta[3])


def fit_summary(D, ft, bounds):
    th = ft.x; n = ft.fun.size
    chi2 = 2 * ft.cost
    lo, hi = bounds
    J = ft.jac
    onb = [abs(th[k] - lo[k]) < 1e-6 * max(1, abs(lo[k])) or abs(th[k] - hi[k]) < 1e-6 * max(1, abs(hi[k])) for k in range(6)]
    free_k = [k for k in range(6) if not onb[k]]
    try:
        cov = np.linalg.inv(J[:, free_k].T @ J[:, free_k]) * D["Nbeam"] * max(1.0, chi2 / n)
    except np.linalg.LinAlgError:
        cov = np.full((len(free_k), len(free_k)), np.nan)
    out = dict(theta=th.tolist(), chi2=chi2, n=int(n), onbound=onb, free=free_k)
    for lab, R in (("Rout", D["R_out"]), ("R15", D["R15"]), ("R30", D["R30"]), ("RJ", D["RJ"])):
        gvec = np.zeros(6)
        gvec[2] = (2 / math.pi) * math.atan(R / th[3])
        gvec[3] = (2 / math.pi) * th[2] * (-R / th[3] ** 2) / (1 + (R / th[3]) ** 2)
        gv = gvec[free_k]
        var = float(gv @ cov @ gv) if np.all(np.isfinite(cov)) else float("nan")
        out[f"V_{lab}"] = vrot(th, R); out[f"eV_{lab}"] = math.sqrt(var) if var >= 0 else float("nan")
    out["sigma0"] = th[4]; out["e_sigma0"] = math.sqrt(cov[free_k.index(4), free_k.index(4)]) if 4 in free_k and np.all(np.isfinite(cov)) else float("nan")
    return out


def worker_real(g):
    D = prepare(g)
    t = time.time()
    ft, bd = fit(D)
    r = fit_summary(D, ft, bd); r["seconds"] = time.time() - t; r["gid"] = g
    return r


def worker_mock(args):
    g, k, va = args
    D = prepare(g)
    rng = np.random.default_rng(SEED * 100 + 7 * k + (13 if va != PLANT["Va"] else 0) + len(g))
    th_true = [D["pa0"] + 20.0, D["vpk"] + 40.0, va, PLANT["Rt"], PLANT["sig"], D["S"]]
    clean = model(D, th_true)
    nch = clean.shape[0]; fi = D["free_idx"]
    starts = [i for i in range(len(fi) - nch) if fi[i + nch - 1] - fi[i] == nch - 1]
    i0 = starts[int(rng.integers(0, len(starts)))]
    noise = D["sub"][fi[i0:i0 + nch]].astype(float)
    ft, bd = fit(D, data=clean + noise)
    if ft is None:
        return dict(g=g, k=k, ok=False)
    s = fit_summary(D, ft, bd)
    return dict(g=g, k=k, ok=True, V_fit=s["V_Rout"], eV=s["eV_Rout"], V_true=vrot(th_true, D["R_out"]), onbound=s["onbound"])


if __name__ == "__main__":
    T0 = time.time()
    P(__doc__.split("Run:")[0].strip())
    P(f"MUTATE = {'1 (planted V_a x 1.5 in the recovery test)' if MUT else 'none'}")
    # ---------------------------------------------------------------- C-beam
    D0 = prepare("VC5110377875")
    delta = np.zeros((2 * HB * FN, 2 * HB * FN)); delta[HB * FN, HB * FN] = 1.0
    beam_img = fftconvolve(delta, D0["kern"], mode="same")
    sb_ = fits.getheader(glob.glob(os.path.join(AL, "*vuds_cosmos_5110377875.cube.image.fits"))[0])
    pixf = D0["pix"] / FN
    yy, xx = np.indices(beam_img.shape); y0, x0 = HB * FN, HB * FN
    dX, dY = -(xx - x0) * pixf, (yy - y0) * pixf
    bpa_ = math.radians(sb_["BPA"])
    u = dX * math.sin(bpa_) + dY * math.cos(bpa_); w = dX * math.cos(bpa_) - dY * math.sin(bpa_)
    smaj = math.sqrt(np.sum(beam_img * u ** 2) / np.sum(beam_img)); smin = math.sqrt(np.sum(beam_img * w ** 2) / np.sum(beam_img))
    fwhm_maj, fwhm_min = 2 * math.sqrt(2 * math.log(2)) * smaj, 2 * math.sqrt(2 * math.log(2)) * smin
    check("C-beam a point source through the model convolution returns the header's beam FWHM to 3% (VC5110377875)", f"major {fwhm_maj:.3f} vs {sb_['BMAJ'] * 3600:.3f}, minor {fwhm_min:.3f} vs {sb_['BMIN'] * 3600:.3f} arcsec", abs(fwhm_maj / (sb_["BMAJ"] * 3600) - 1) < 0.03 and abs(fwhm_min / (sb_["BMIN"] * 3600) - 1) < 0.03)
    # ---------------------------------------------------------------- real-data fits
    P("\nFORWARD-MODEL FITS (thin disc, arctan rotation curve, inclination FIXED at the corpus value; parameter errors inflated by N_beam and max(1, chi2/n))")
    ctx = mp.get_context("spawn")
    with ctx.Pool(4) as pool:
        REAL = pool.map(worker_real, list(TAGS))
    P("  galaxy          inc   PA      v_sys-v_peak  V_a (km/s)   R_t (kpc)  sigma_0 (km/s)   flux (Jy km/s; Stage 1)   chi2/n   V_rot(R_out) +- err   [R_out kpc]   V_rot(Jones R) [R_J]   Jones outer ring V +- err   on bound")
    RNG = pd.read_csv(os.path.join(REPO, "data_assembly", "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_rings.csv"))
    for r in REAL:
        g = r["gid"]; D = prepare(g); th = r["theta"]
        jr = RNG[RNG["galaxy"] == g].sort_values("R_kpc").iloc[-1]
        r["jones_V"], r["jones_eV"], r["jones_R"] = float(jr["Vrot_kms"]), float(jr["e_Vrot_kms"]), float(jr["R_kpc"])
        names = ["PA", "vsys", "Va", "Rt", "sig", "flux"]
        ob = ",".join(names[k] for k in range(6) if r["onbound"][k]) or "-"
        P(f"  {g:13s} {D['inc']:4.0f}  {th[0] % 360:6.1f}  {th[1] - D['vpk']:+8.1f}      {th[2]:7.1f}      {th[3]:5.2f}      {th[4]:6.1f}        {th[5]:5.2f} ({D['S']:.2f})        {r['chi2'] / r['n']:5.2f}    {r['V_Rout']:6.1f} +- {r['eV_Rout']:5.1f}   [{D['R_out']:5.2f}]      {r['V_RJ']:6.1f} [{D['RJ']:4.2f}]         {jr['Vrot_kms']:6.1f} +- {jr['e_Vrot_kms']:5.1f}        {ob}")
    # ---------------------------------------------------------------- planted-rotation recovery (C-ext)
    P(f"\nPLANTED-ROTATION RECOVERY (C-ext): {NMOCK} mocks per galaxy, planted V_a {PLANT['Va'] * (1.5 if MUT else 1.0):.0f} km/s, R_t {PLANT['Rt']} kpc, sigma_0 {PLANT['sig']:.0f} km/s, the galaxy's own corpus inclination, beam, geometry and REAL line-free-channel noise; "
      "the recovered V(R_out) must lie within 15% of the input in >= 90% of the mocks and its mean bias must be below 10%")
    va = PLANT["Va"] * (1.5 if MUT else 1.0)
    jobs = [(g, k, va) for g in TAGS for k in range(NMOCK)]
    with ctx.Pool(4) as pool:
        MK = pool.map(worker_mock, jobs, chunksize=5)
    REC = {}
    for g in TAGS:
        rr = [m for m in MK if m["g"] == g and m["ok"]]
        ratio = np.array([m["V_fit"] / m["V_true"] for m in rr])
        REC[g] = dict(n=len(rr), frac15=float(np.mean(np.abs(ratio - 1) <= 0.15)), bias=float(np.mean(ratio) - 1), sd=float(np.std(ratio, ddof=1)), mean_eV=float(np.mean([m["eV"] for m in rr if np.isfinite(m["eV"])])))
        P(f"  {g:13s} fits {len(rr):2d}/{NMOCK}: within 15% in {REC[g]['frac15']:.2f}, mean bias {REC[g]['bias']:+.3f}, SD of V_fit/V_true {REC[g]['sd']:.3f}; mean quoted error {REC[g]['mean_eV']:.1f} km/s")
    if not MUT:
        for g in TAGS:
            check(f"C-ext {g}: the recovered V(R_out) lies within 15% of the input in >= 90% of the mocks and the mean bias is below 10%", f"within 15%: {REC[g]['frac15']:.2f}; bias {REC[g]['bias']:+.3f}", REC[g]["frac15"] >= 0.90 and abs(REC[g]["bias"]) < 0.10)
    else:
        base = json.load(open(os.path.join(LANE, "cfg228_stage3_results.json")))["REC"]
        for g in TAGS:
            ratio15 = (1.0 + REC[g]["bias"]) * vrot([0, 0, va, PLANT["Rt"], 0, 0], prepare(g)["R_out"]) / (vrot([0, 0, PLANT["Va"], PLANT["Rt"], 0, 0], prepare(g)["R_out"]))
            check(f"MUTATE {g}: planted V x 1.5 returns V(R_out) x 1.5 (recovered / baseline-planted = 1.5 within 10%)", f"{ratio15:.3f}", abs(ratio15 / 1.5 - 1) < 0.10)
    P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
    tag = "_MUTATE" if MUT else ""
    json.dump(dict(REAL=REAL, REC=REC, params=dict(FN=FN, HB=HB, NMOCK=NMOCK, START=START, PLANT=PLANT, seed=SEED)), open(os.path.join(LANE, f"cfg228_stage3_results{tag}.json"), "w"), indent=1, default=float)
    open(os.path.join(LANE, f"cfg228_stage3{tag}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>").replace(EXT, "<external>") + "\n")
    sys.exit(0 if all(CHK) else 1)
